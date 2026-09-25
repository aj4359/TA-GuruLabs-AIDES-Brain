from dataclasses import dataclass
from enum import Enum

class Reversibility(str, Enum):
    YES = "yes"
    PARTIAL = "partial"
    NO = "no"

@dataclass(frozen=True)
class RecoveryContract:
    reversible: Reversibility
    recovery_method_ref: str | None
    recovery_authority: str | None
    checkpoint_ref: str | None
    recovery_tested: bool
    irreversible_warning_acknowledged: bool = False

def assert_recovery_ready(contract: RecoveryContract) -> None:
    if contract.reversible in (Reversibility.YES, Reversibility.PARTIAL):
        if not contract.recovery_method_ref or not contract.recovery_authority:
            raise PermissionError("Reversible action lacks recovery method/authority")
    if contract.reversible is Reversibility.NO and not contract.irreversible_warning_acknowledged:
        raise PermissionError("Irreversible action requires explicit warning acknowledgement")
