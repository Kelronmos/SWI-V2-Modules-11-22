"""Experimental package must not import runtime/M11 or expose executor."""

import ast
from pathlib import Path

import experimental.cek_alignment_monitor as pkg
from experimental.cek_alignment_monitor.monitor import AlignmentMonitor

FORBIDDEN = ("swi_v2.module11", "swi_v2.runtime", "swi_core")


def test_no_forbidden_imports_in_package_source():
    root = Path(pkg.__file__).resolve().parent
    for py in root.glob("*.py"):
        tree = ast.parse(py.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for bad in FORBIDDEN:
                        assert not alias.name.startswith(bad)
            if isinstance(node, ast.ImportFrom) and node.module:
                for bad in FORBIDDEN:
                    assert not node.module.startswith(bad)


def test_monitor_has_no_executor_or_auth_api():
    mon = AlignmentMonitor()
    for name in ("authorize", "permit", "execute", "seal", "admit", "bind"):
        assert not hasattr(mon, name)


def test_package_exports_measurement_only():
    names = set(pkg.__all__)
    for banned in ("authorize", "execute", "seal", "admit", "Authority", "Executor"):
        assert banned not in names
