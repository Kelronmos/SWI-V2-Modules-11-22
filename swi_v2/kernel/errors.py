"""Controlled error model for SWI Volume 2."""


class ModuleKernelError(Exception):
    """Fail-closed kernel / admission / module boundary failure."""


class FoundationAdmissionError(ModuleKernelError):
    """Module 11 could not admit input under the foundation contract."""


class UnsupportedFoundationVersion(FoundationAdmissionError):
    """Foundation or schema version is not accepted by this V2 build."""


class InvalidFoundationEvidence(FoundationAdmissionError):
    """Evidence structure or fields are invalid for the declared contract."""


class IntegrityVerificationError(FoundationAdmissionError):
    """Integrity reference failed verification."""


class UnexpectedFieldError(FoundationAdmissionError):
    """Evidence envelope contained fields outside the declared contract schema."""


class ReplayError(FoundationAdmissionError):
    """Evidence with an already-seen evidence_id was presented again to a guard."""


class StateTransitionError(ModuleKernelError):
    """Invalid kernel or workflow state transition (e.g. execute after HALT)."""


class ContractError(ModuleKernelError):
    """Module or kernel contract violated."""


class AuthorityError(ModuleKernelError):
    """Authority boundary violation: undeclared or escalated authority."""


class AuthorityHalt(AuthorityError):
    """Missing or unknown authority required for the requested transition."""
