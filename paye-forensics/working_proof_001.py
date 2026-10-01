from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class TaxEvent:
    date: str
    kind: str
    source: str
    details: dict[str, Any]

def reconstruct(case: dict[str, Any]) -> dict[str, Any]:
    events=[TaxEvent(**e) for e in case["events"]]
    events=sorted(events,key=lambda e:(e.date,e.kind,e.source))
    evidence=[{"event":asdict(e),"source_ref":e.source} for e in events]
    employments=[e for e in events if e.kind in {"EMPLOYMENT_START","EMPLOYMENT_END"}]
    starts=[e for e in employments if e.kind=="EMPLOYMENT_START"]
    ends=[e for e in employments if e.kind=="EMPLOYMENT_END"]
    open_employments=[]
    for s in starts:
        employer=s.details["employer"]
        if not any(x.details.get("employer")==employer and x.date>=s.date for x in ends):
            open_employments.append(employer)
    bik=[asdict(e) for e in events if e.kind=="BENEFIT_IN_KIND"]
    hypotheses=[]
    if len(starts)>1:
        hypotheses.append({"id":"H1","statement":"Multiple employment records may have affected allowance allocation or tax code treatment.","status":"HYPOTHESIS"})
    if open_employments:
        hypotheses.append({"id":"H2","statement":"One or more employments appear open in the supplied evidence.","status":"HYPOTHESIS","employers":open_employments})
    if bik:
        hypotheses.append({"id":"H3","statement":"Benefit-in-kind treatment changed during the history and should be reconciled against coding/payrolling evidence.","status":"HYPOTHESIS"})
    missing=[]
    for required in case.get("required_evidence",[]):
        if required not in {e.source for e in events}: missing.append(required)
    return {
        "case_id":case["case_id"],
        "tax_history_graph":[asdict(e) for e in events],
        "evidence":evidence,
        "benefit_in_kind_transitions":bik,
        "hypotheses":hypotheses,
        "missing_evidence":missing,
        "confidence":"LIMITED" if missing else "SUPPORTED_BY_SUPPLIED_SYNTHETIC_EVIDENCE",
        "recommended_investigation_steps":[
            "Reconcile employment start/end chronology against P45/P60 and payroll records.",
            "Reconcile tax-code changes against the employment chronology.",
            "Check benefit-in-kind coding/payrolling treatment for each effective period.",
            "Resolve missing evidence before presenting any hypothesis as a finding."
        ],
        "hmrc_submission_performed":False
    }
