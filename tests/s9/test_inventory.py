from pathlib import Path
from swi_v2.s9.inventory import walk_inventory, classify_path


def test_classify_path():
    assert classify_path("swi_v2/kernel/authority.py") == "module"
    assert classify_path("docs/foo.md") == "doc"
    assert classify_path("tests/s9/test_x.py") == "test"


def test_walk_inventory_counts(tmp_path):
    (tmp_path / "a.py").write_text("x=1\n")
    inv = walk_inventory(tmp_path, "deadbeef")
    assert inv["total_nodes"] >= 1
    assert inv["source_commit"] == "deadbeef"
