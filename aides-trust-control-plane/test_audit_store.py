import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from audit_store import AuditChain


class AuditChainTests(unittest.TestCase):
    def test_valid_chain_verifies(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "audit.jsonl"
            chain = AuditChain(path)
            chain.append(
                transaction_id="tx-1",
                event_type="REQUESTED",
                actor_id="AIDE:SCOUT",
                authority={"result":"require-human-approval"},
                evidence={"confidence":95},
                decision={"status":"blocked"},
            )
            chain.append(
                transaction_id="tx-1",
                event_type="APPROVED",
                actor_id="HUMAN:FOUNDER",
                authority={"result":"approved"},
                evidence={"approval_ref":"demo"},
                decision={"status":"approved"},
            )
            ok, message = chain.verify()
            self.assertTrue(ok, message)

    def test_tampering_is_detected(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "audit.jsonl"
            chain = AuditChain(path)
            chain.append(
                transaction_id="tx-1",
                event_type="REQUESTED",
                actor_id="AIDE:SCOUT",
                authority={"result":"require-human-approval"},
                evidence={"confidence":95},
                decision={"status":"blocked"},
            )
            row = json.loads(path.read_text(encoding="utf-8").strip())
            row["decision"]["status"] = "executed"
            path.write_text(json.dumps(row) + "\n", encoding="utf-8")
            ok, _ = chain.verify()
            self.assertFalse(ok)

    def test_broken_link_is_detected(self):
        with TemporaryDirectory() as td:
            path = Path(td) / "audit.jsonl"
            chain = AuditChain(path)
            for i in range(2):
                chain.append(
                    transaction_id="tx-1",
                    event_type=f"STEP_{i}",
                    actor_id="AIDE:SCOUT",
                    authority={"result":"allowed"},
                    evidence={},
                    decision={"status":"recorded"},
                )
            rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
            rows[1]["previous_hash"] = "f" * 64
            path.write_text("\n".join(json.dumps(x) for x in rows) + "\n", encoding="utf-8")
            ok, _ = chain.verify()
            self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
