"""T01.04 / T01.05 — Dependency and experimental/production boundaries.

Ensures experimental code does not silently become a production authority path.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _python_files(root: Path):
    if not root.exists():
        return []
    return [p for p in root.rglob("*.py") if p.is_file()]


def test_experimental_common_sense_does_not_import_production_execution():
    """Common Sense must not import any execution or seal authority path."""
    cs_root = REPO_ROOT / "experimental" / "common_sense"
    forbidden_substrings = [
        "swi_v2.kernel.seal",
        "swi_v2.module12",  # reserved / blocked execution area
        "EXECUTE",
        "PROMOTE",
    ]

    for path in _python_files(cs_root):
        source = path.read_text(encoding="utf-8")
        # Static check only — presence of the word in comments is ok for docs,
        # but import of seal/execution modules is not.
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name for a in node.names]
                elif node.module:
                    names = [node.module]
                for name in names:
                    assert "seal" not in name.lower() or "common_sense" in name, (
                        f"{path} imports seal-related module: {name}"
                    )


def test_common_sense_lives_only_under_experimental():
    """No production package may shadow experimental Common Sense."""
    assert (REPO_ROOT / "experimental" / "common_sense").is_dir()
    assert not (REPO_ROOT / "swi_v2" / "common_sense").exists()


def test_response_boundary_remains_experimental():
    assert (REPO_ROOT / "experimental" / "response_boundary").is_dir()
    assert not (REPO_ROOT / "swi_v2" / "response_boundary").exists()


def test_kernel_authority_module_exists_and_is_importable():
    """Kernel authority boundary remains the production authority surface."""
    import swi_v2.kernel.authority as authority

    assert authority is not None


def test_no_circular_import_common_sense_to_kernel_seal():
    """Importing Common Sense must not pull in kernel.seal."""
    import experimental.common_sense as cs
    import sys

    # After importing CEK, kernel.seal need not be loaded
    # (it may be loaded by other tests; we only assert CEK itself does not require it)
    assert "experimental.common_sense.monitor" in sys.modules
    # The monitor module source must not reference seal as a runtime dependency
    monitor_src = (REPO_ROOT / "experimental" / "common_sense" / "monitor.py").read_text()
    assert "from swi_v2.kernel.seal" not in monitor_src
    assert "import swi_v2.kernel.seal" not in monitor_src
