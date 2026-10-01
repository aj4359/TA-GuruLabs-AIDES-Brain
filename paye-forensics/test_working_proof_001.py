import json, unittest
from pathlib import Path
from working_proof_001 import reconstruct

class WorkingProof001Tests(unittest.TestCase):
    def setUp(self):
        p=Path(__file__).with_name("fixtures")/"working_proof_001.json"
        self.case=json.loads(p.read_text(encoding="utf-8"))
    def test_is_deterministic(self):
        self.assertEqual(reconstruct(self.case), reconstruct(self.case))
    def test_bik_transition_visible(self):
        self.assertEqual(len(reconstruct(self.case)["benefit_in_kind_transitions"]),2)
    def test_hypotheses_not_findings(self):
        self.assertTrue(all(x["status"]=="HYPOTHESIS" for x in reconstruct(self.case)["hypotheses"]))
    def test_never_files_with_hmrc(self):
        self.assertFalse(reconstruct(self.case)["hmrc_submission_performed"])

if __name__=="__main__": unittest.main()
