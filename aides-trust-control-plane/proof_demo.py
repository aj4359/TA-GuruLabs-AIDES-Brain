from dataclasses import dataclass, asdict
from capability_discovery import Capability, select_approved_capability
from runtime_boundary import MissionEnvelope, RuntimeReceipt, accept_runtime_receipt
from recovery_contract import RecoveryContract, Reversibility, validate_recovery_contract
from ta_verified import VerificationRecord, assert_verified
from verified_outcome_economics import MissionOutcome, cost_per_verified_outcome

@dataclass(frozen=True)
class ProofDemo:
    mission: dict
    authority: dict
    workforce: dict
    work: dict
    recovery: dict
    verification: dict
    economics: dict

def run_demo() -> ProofDemo:
    mission=MissionEnvelope("demo-001","Produce a bounded, evidenced customer outcome","authority://demo-owner","audit",10.0)
    worker=select_approved_capability("audit",[
        Capability("worker-unapproved",False,1.0,("audit",)),
        Capability("worker-approved",True,4.0,("audit",)),
        Capability("worker-approved-expensive",True,8.0,("audit",)),
    ])
    receipt=accept_runtime_receipt(mission,RuntimeReceipt("replaceable-runtime","exec://demo-001",4.0,("evidence://demo-001",),{"outcome":"complete"}))
    recovery=RecoveryContract(Reversibility.YES,"recovery://demo-001","authority://demo-owner","checkpoint://demo-001",True,False)
    validate_recovery_contract(recovery)
    verified=VerificationRecord(
        claim="bounded customer outcome completed",
        acceptance_criteria="evidence present; cost within envelope; recovery defined",
        scenario="demo-001", evidence_refs=list(receipt.evidence_refs),
        failure_correction_history=[], result="PASS", version="0.1",
        timestamp="2026-09-25T00:00:00Z", limitations=["demonstrator fixture"],
        release_decision="VERIFIED_LIMITED_RELEASE")
    assert_verified(verified)
    cpvo=cost_per_verified_outcome([MissionOutcome(receipt.attributable_cost,True)])
    return ProofDemo(
        mission={"id":mission.mission_id,"objective":mission.objective},
        authority={"ref":mission.authority_ref,"max_cost":mission.max_cost},
        workforce={"selected":worker.capability_id,"approved":worker.approved},
        work={"execution_ref":receipt.execution_ref,"evidence_refs":list(receipt.evidence_refs)},
        recovery={"reversible":recovery.reversible.value,"tested":recovery.recovery_tested},
        verification={"result":verified.result,"release":verified.release_decision},
        economics={"attributable_cost":receipt.attributable_cost,"cpvo":cpvo},
    )

if __name__=="__main__":
    import json
    print(json.dumps(asdict(run_demo()),indent=2))
