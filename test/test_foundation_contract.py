"""Foundation contract fixture tests — PROPOSED contract only."""
from swi_v2.kernel.admission import compute_integrity_reference
from swi_v2.kernel.contracts import (
    SUPPORTED_EVIDENCE_SCHEMA_VERSIONS,
    SUPPORTED_FOUNDATION_VERSIONS,
)


def test_supported_versions_are_explicitly_proposed():
    assert "1.0-proposed" in SUPPORTED_FOUNDATION_VERSIONS
    assert "1.0-proposed" in SUPPORTED_EVIDENCE_SCHEMA_VERSIONS


def test_integrity_reference_is_deterministic():
    a = compute_integrity_reference("p", "1.0-proposed", "1.0-proposed", "id", "src")
    b = compute_integrity_reference("p", "1.0-proposed", "1.0-proposed", "id", "src")
    assert a == b
    assert len(a) == 64
