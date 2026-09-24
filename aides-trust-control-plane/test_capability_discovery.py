import unittest
from capability_discovery import Capability, select_approved_capability

class CapabilityDiscoveryTests(unittest.TestCase):
    def test_selects_lowest_cost_approved_worker_that_can_prove_outcome(self):
        candidates=[Capability("cheap-unapproved",False,1,("audit",)),Capability("approved-expensive",True,9,("audit",)),Capability("approved-cheap",True,4,("audit",))]
        self.assertEqual(select_approved_capability("audit",candidates).capability_id,"approved-cheap")

    def test_fails_closed_when_no_approved_capability_can_prove(self):
        with self.assertRaises(PermissionError):
            select_approved_capability("audit",[Capability("x",False,1,("audit",))])

if __name__ == "__main__":
    unittest.main()
