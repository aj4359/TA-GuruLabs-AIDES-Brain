import unittest
from runtime_boundary import MissionEnvelope, RuntimeReceipt, accept_runtime_receipt

class RuntimeBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.m=MissionEnvelope("m1","prove bounded outcome","authority://a1","audit",10.0)

    def test_runtime_is_replaceable_when_receipt_satisfies_aides_contract(self):
        r=RuntimeReceipt("external-runtime","exec://1",4.0,("evidence://1",),{"ok":True})
        self.assertEqual(accept_runtime_receipt(self.m,r).runtime_id,"external-runtime")

    def test_runtime_cannot_bypass_cost_envelope(self):
        with self.assertRaises(PermissionError):
            accept_runtime_receipt(self.m,RuntimeReceipt("x","exec://2",11.0,("evidence://2",),{}))

    def test_runtime_cannot_claim_success_without_evidence(self):
        with self.assertRaises(ValueError):
            accept_runtime_receipt(self.m,RuntimeReceipt("x","exec://3",1.0,(),{}))

if __name__=="__main__":
    unittest.main()
