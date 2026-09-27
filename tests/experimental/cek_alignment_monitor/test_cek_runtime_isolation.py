"""Experimental package must not import runtime / M11 / expose executor."""

from __future__ import annotations

import ast
from pathlib import Path

import experimental.cek_alignment_monitor as pkg
from experimental.cek_alignment_monitor.monitor import AlignmentMonitor
from tests.experimental.cek_alignment_monitor.conftest import assert_monitor_surface

FORBIDDEN_IMPORT_ROOTS = ("swi_v2.module11", "swi_v2.runtime", "swi_core")


def test_no_forbidden_imports_in_package_source() -> None:
    root = Path(pkg.__file__).resolve().parent
    for py in root.glob("*.py"):
        tree = ast.parse(py.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for bad in FORBIDDEN_IMPORT_ROOTS:
                        assert not alias.name.startswith(bad)
            if isinstance(node, ast.ImportFrom) and node.module:
                for bad in FORBIDDEN_IMPORT_ROOTS:
                    assert not node.module.startswith(bad)


def test_monitor_has_no_executor_or_auth_api() -> None:
    mon = AlignmentMonitor()
    assert_monitor_surface(mon)


def test_package_exports_measurement_only() -> None:
    names = set(pkg.__all__)
    for banned in ("authorize", "execute", "seal", "admit", "Authority", "Executor"):
        assert banned not in names
