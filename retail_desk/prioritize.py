"""Evidence-weighted prioritisation; numerical scores are NOT probabilities of success."""
import json
import sys
from datetime import datetime,timezone
from pathlib import Path

WEIGHTS={"buyer_demand":25,"purchase_evidence":20,"speed_to_market":15,"margin":15,"organic_distribution":10,"delivery_reliability":10,"strategic_fit":5}
REQUIRED=("id","name","buyer","product","sources","scores","economics","gates")
def evaluate(item):
    missing=[field for field in REQUIRED if field not in item]
    if missing: return {"id":item.get("id","unknown"),"decision":"RESEARCH","score":None,"reasons":["Missing fields: "+", ".join(missing)]}
    scores=item["scores"]
    invalid=[k for k in WEIGHTS if type(scores.get(k)) not in (int,float) or not 0<=scores[k]<=5]
    if invalid: return {"id":item["id"],"name":item["name"],"decision":"RESEARCH","score":None,"reasons":["Invalid or missing evidence scores: "+", ".join(invalid)]}
    sources=item["sources"]
    independent={s.get("publisher","").strip().lower() for s in sources if isinstance(s,dict) and s.get("url","").startswith("https://") and s.get("publisher","").strip()}
    gates=item["gates"]
    required_gates=("rights_cleared","platform_eligible","deliverable_verified","checkout_verified","privacy_review")
    missing_gates=[k for k in required_gates if gates.get(k) is not True]
    econ=item["economics"]
    try:
        price=float(econ["price_gbp"])
        fees=float(econ["fees_gbp"])
        fulfilment=float(econ["fulfilment_gbp"])
        refund_reserve=float(econ["refund_reserve_gbp"])
        contribution=round(price-fees-fulfilment-refund_reserve,2)
        if min(price,fees,fulfilment,refund_reserve)<0: raise ValueError("negative cost")
    except (KeyError,ValueError,TypeError):
        return {"id":item["id"],"name":item["name"],"decision":"RESEARCH","score":None,"reasons":["Missing/invalid unit economics"]}
    score=round(sum(scores[k]*weight/5 for k,weight in WEIGHTS.items()),1)
    reasons=[]
    if len(independent)<2: reasons.append("Fewer than two independent sources; demand unverified")
    if not item.get("purchase_signal_verified",False): reasons.append("No independently verified purchase-intent evidence")
    if missing_gates: reasons.append("Unpassed safety/release gates: "+", ".join(missing_gates))
    if contribution<=0: reasons.append("No positive estimated contribution per unit")
    if reasons: decision="RESEARCH" if len(independent)<2 or not item.get("purchase_signal_verified",False) else "BLOCKED"
    elif score>=75: decision="PILOT_CANDIDATE"
    elif score>=55: decision="IMPROVE"
    else: decision="STOP_OR_PARK"
    return {"id":item["id"],"name":item["name"],"score":score,"decision":decision,
            "estimated_contribution_gbp":contribution,"evidence_publishers":len(independent),
            "reasons":reasons,"note":"Heuristic priority score, NOT a statistical likelihood of success. Manual verification required."}

def rank(items):
    evaluated=[evaluate(item) for item in items]
    # Candidates first, then improve, then unverified, then blocked/parked. Scores never override hard gates.
    order={"PILOT_CANDIDATE":0,"IMPROVE":1,"RESEARCH":2,"BLOCKED":3,"STOP_OR_PARK":4}
    evaluated.sort(key=lambda v:(order[v["decision"]],-(v["score"] if v["score"] is not None else -1),v["id"]))
    return {"created_utc":datetime.now(timezone.utc).isoformat(),"scoring_version":"1.0",
            "metric_warning":"Not an empirically calibrated success probability; never label scores as % chance of success.",
            "candidates":evaluated,
            "allocation_policy":"Max one new pilot alongside existing near-sale products. AIDE can recommend reallocations; human approves expenditures, product launch, reprioritisation of committed deliverables."}
if __name__=="__main__":
    src=Path(sys.argv[1]) if len(sys.argv)>1 else Path("retail_desk/opportunities.json")
    dest=Path(sys.argv[2]) if len(sys.argv)>2 else Path("retail_desk/output/priorities.json")
    data=json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(data,list): raise ValueError("Expected JSON array")
    report=rank(data)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Assessed {len(data)} evidence cards; pilot candidates: {sum(x['decision']=='PILOT_CANDIDATE' for x in report['candidates'])}")
