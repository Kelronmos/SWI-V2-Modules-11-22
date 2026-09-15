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


class StateTransitionError(ModuleKernelError):
    """Invalid kernel or workflow state transition (e.g. execute after HALT)."""


class ContractError(ModuleKernelError):
    """Module or kernel contract violated."""
