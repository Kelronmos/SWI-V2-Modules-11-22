import pytest
from swi_v2.s9.manifest import build_manifest


def test_refuse_short_commit():
    with pytest.raises(ValueError):
        build_manifest(source_repository="r", source_commit="ab", report_id="R1")


def test_manifest_never_s9_proven():
    m = build_manifest(
        source_repository="Kelronmos/SWI-V2-Modules-11-22",
        source_commit="aa62042888886f5252e2b80e7aec8dce49e4bab3",
        report_id="R1",
        report_status="SATISFIED",
    )
    assert m["s9_proven"] is False
    assert m["production_authorized"] is False
    assert "manifest_hash" in m
