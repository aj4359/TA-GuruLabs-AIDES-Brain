import pytest
from recovery_contract import RecoveryContract, Reversibility, assert_recovery_ready

def test_reversible_action_requires_recovery_plan():
    with pytest.raises(PermissionError):
        assert_recovery_ready(RecoveryContract(Reversibility.YES, None, None, None, False))

def test_irreversible_action_requires_acknowledgement():
    with pytest.raises(PermissionError):
        assert_recovery_ready(RecoveryContract(Reversibility.NO, None, "owner", None, False))

def test_irreversible_action_can_be_explicitly_authorised():
    assert_recovery_ready(RecoveryContract(Reversibility.NO, None, "owner", None, False, True))
