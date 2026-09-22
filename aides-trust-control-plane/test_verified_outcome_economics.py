import pytest
from verified_outcome_economics import MissionOutcome, cost_per_verified_outcome

def test_cpvo_counts_only_verified_outcomes():
    outcomes = [
        MissionOutcome("m1", 10.0, True),
        MissionOutcome("m2", 20.0, False),
        MissionOutcome("m3", 30.0, True),
    ]
    assert cost_per_verified_outcome(outcomes) == 30.0

def test_cpvo_requires_verified_outcome():
    with pytest.raises(ValueError):
        cost_per_verified_outcome([MissionOutcome("m1", 5.0, False)])
