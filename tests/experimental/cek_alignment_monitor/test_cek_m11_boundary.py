"""M11 boundary: CEK does not import or modify sealed M11."""

from __future__ import annotations

from pathlib import Path

import experimental.cek_alignment_monitor as cek_pkg


def test_cek_does_not_import_m11() -> None:
    root = Path(cek_pkg.__file__).resolve().parent
    for py in root.glob("*.py"):
        text = py.read_text()
        assert "swi_v2.module11" not in text
        assert "from swi_v2 import module11" not in text


def test_m11_does_not_import_cek_if_present() -> None:
    candidates = list(Path(".").rglob("module11/**/*.py"))
    for base in (Path("swi_v2/module11"), Path("/tmp/swi_clean/swi_v2/module11")):
        if base.exists():
            candidates = list(base.rglob("*.py"))
            break
    for py in candidates:
        text = py.read_text(errors="ignore")
        assert "cek_alignment_monitor" not in text, f"M11 imports CEK: {py}"
