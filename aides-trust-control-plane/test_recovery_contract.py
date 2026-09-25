import unittest
from recovery_contract import RecoveryContract, Reversibility, assert_recovery_ready

class RecoveryContractTests(unittest.TestCase):
    def test_reversible_action_requires_recovery_plan(self):
        with self.assertRaises(PermissionError):
            assert_recovery_ready(RecoveryContract(Reversibility.YES,None,None,None,False))
    def test_irreversible_action_requires_acknowledgement(self):
        with self.assertRaises(PermissionError):
            assert_recovery_ready(RecoveryContract(Reversibility.NO,None,"owner",None,False))
    def test_irreversible_action_can_be_explicitly_authorised(self):
        assert_recovery_ready(RecoveryContract(Reversibility.NO,None,"owner",None,False,True))

if __name__=="__main__": unittest.main()
