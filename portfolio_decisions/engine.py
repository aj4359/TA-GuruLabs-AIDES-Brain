"""Cross-portfolio prioritisation: evidence-first, conservative, and side-effect free."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WEIGHTS = {"customer_evidence":25, "verified_readiness":20, "time_to_revenue":15,
           "unit_economics":15, "distribution_access":10, "strategic_fit":10, "execution_risk":5}
VALID = {"retail", "software", "recruitment", "media", "games", "agent_services",
         "internal", "trading_research", "other"}
def assess(entry):
    name = str(entry.get("name", "Unnamed"))
    ident = str(entry.get("id", "unknown"))
    lane = entry.get("lane", "other")
    result = {"id": ident, "name": name, "lane": lane, "priority_score": None,
              "decision": "RESEARCH", "reasons": [], "probability_of_success": None}
    if lane not in VALID:
        result["reasons"].append("Unsupported lane"); return result
    scores = entry.get("scores", {})
    if any(type(scores.get(k)) not in (int, float) or not 0 <= scores[k] <= 5 for k in WEIGHTS):
        result["reasons"].append("Evidence scores incomplete or invalid"); return result
    score = round(sum(scores[k] * weight / 5 for k, weight in WEIGHTS.items()), 1)
    result["priority_score"] = score
    evidence = entry.get("evidence", [])
    independent = {str(x.get("publisher", "")).strip().lower() for x in evidence if
                   isinstance(x, dict) and str(x.get("url", "")).startswith("https://")
                   and x.get("publisher")}
    receipts = entry.get("receipts", {})
    gates = entry.get("gates", {})
    if len(independent) < 2 and not receipts.get("verified_sale", False):
        result["reasons"].append("Insufficient independent demand evidence; verified sales receipt absent")
    if not receipts.get("working_artifact", False):
        result["reasons"].append("Working artifact not verified")
    if not receipts.get("delivery_or_usage_path", False):
        result["reasons"].append("Delivery or usage path not verified")
    if not gates.get("rights_and_privacy", False):
        result["reasons"].append("Rights/privacy gate not cleared")
    if not gates.get("commercial_and_platform", False):
        result["reasons"].append("Commercial/platform gate not cleared")
    if entry.get("estimated_unit_contribution_gbp") is not None:
        contribution = entry["estimated_unit_contribution_gbp"]
        if type(contribution) not in (int,float) or contribution <= 0:
            result["reasons"].append("Non-positive or invalid estimated unit contribution")
    elif lane != "internal":
        result["reasons"].append("Commercial contribution not evidenced")
    if result["reasons"]:
        result["decision"] = "RESEARCH_OR_UNBLOCK"
    elif score >= 75:
        result["decision"] = "PROPOSE_PRIORITY"
    elif score >= 55:
        result["decision"] = "IMPROVE_AND_REVIEW"
    else:
        result["decision"] = "PARK_CANDIDATE"
    # No algorithmic stop/deletion; all recommendations require portfolio review.
    return result

def report(entries):
    if not isinstance(entries, list):
        raise ValueError("Expected an array of evidence cards")
    rows = [assess(x) for x in entries]
    rank = {"PROPOSE_PRIORITY":0,"IMPROVE_AND_REVIEW":1,"RESEARCH_OR_UNBLOCK":2,"RESEARCH":3,"PARK_CANDIDATE":4}
    rows.sort(key=lambda x: (rank.get(x["decision"],5), -(x["priority_score"] if x["priority_score"] is not None else -1),x["id"]))
    return {"generated_utc":datetime.now(timezone.utc).isoformat(),
            "basis":"evidence cards only; no automatic inference from repository presence",
            "scoring_note":"Heuristic ranking, not a statistically calibrated probability of success",
            "active_lane_cap":3,
            "allocation_rule":"Maintain existing release-factory lanes; recommend changes only after a human-authorised portfolio review",
            "proposals":rows}

if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv)>1 else Path("portfolio_decisions/evidence.json")
    target = Path(sys.argv[2]) if len(sys.argv)>2 else Path("portfolio_decisions/output/priorities.json")
    output = report(json.loads(source.read_text(encoding="utf-8")))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
    print(f"Evaluated {len(output['proposals'])} evidence cards")
