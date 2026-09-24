import pytest
from capability_discovery import Capability, select_approved_capability

def test_selects_lowest_cost_approved_worker_that_can_prove_outcome():
    candidates=[Capability("cheap-unapproved",False,1,("audit",)),Capability("approved-expensive",True,9,("audit",)),Capability("approved-cheap",True,4,("audit",))]
    assert select_approved_capability("audit",candidates).capability_id=="approved-cheap"

def test_fails_closed_when_no_approved_capability_can_prove():
    with pytest.raises(PermissionError):
        select_approved_capability("audit",[Capability("x",False,1,("audit",))])
