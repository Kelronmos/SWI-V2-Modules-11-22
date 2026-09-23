"""SWI Z3 formal transition model — law-registry authority boundary.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED · NOT PRODUCTION AUTHORIZED

This module is NOT a second authorization engine.
Executable authority remains:
  experimental/law/authority.py
  → swi_v2.kernel.authority.require_authorization_for_action

PURPOSE
  Encode the observed transition contract of tip 4cb10a0 as an SMT model
  and search for counterexamples to F-001…F-006.

SOURCE CONTRACT (read-only audit correspondence)
  experimental/law/authority.py
  experimental/law/registry.py
  swi_v2/kernel/authority.py

MODEL SCOPE
  Abstract single-step transitions over the public registry mutation API
  (ingest / append_event / supersede). Does not model private attribute
  assignment, durable storage, multi-process replay, or legal meaning.

DISCIPLINE
  TESTED ≠ FORMALLY CHECKED ≠ SEALED ≠ PRODUCTION AUTHORIZED ≠ LEGAL COMPLIANCE

  A green result means: the formalized transition model has no counterexample
  for the checked properties. It does not prove the Python implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

from z3 import And, Bool, Implies, Not, Or, Solver, String, StringVal, sat, unsat

# ---------------------------------------------------------------------------
# Constants matching experimental/law/authority.py
# ---------------------------------------------------------------------------

ADMIN = "LAW_REGISTRY_ADMIN"

# Decision labels (abstract)
HALT = "HALT"
REJECT = "REJECT"
ACCEPT_CONTINUE = "ACCEPT_CONTINUE"  # auth OK; integrity not yet applied


@dataclass(frozen=True)
class PropertyResult:
    prop_id: str
    name: str
    expected: str  # "UNSAT" | "SAT"
    actual: str
    passed: bool
    note: str = ""


def _admin():
    return StringVal(ADMIN)


def build_transition_model():
    """Symbolic single-step law-registry mutation transition.

    Inputs:
      auth_present, auth_scope, req_action, integrity_ok, policy_maps

    Derived:
      decision ∈ {HALT, REJECT, ACCEPT_CONTINUE}
      authorized ⇔ decision == ACCEPT_CONTINUE
      write ⇔ authorized ∧ integrity_ok

    Kernel rules (require_authorization_for_action):
      ¬auth_present                         → HALT
      auth_present ∧ (scope∉D ∨ action∉D)   → REJECT
      auth_present ∧ scope∈D ∧ action∈D     → ACCEPT_CONTINUE
    with D = {LAW_REGISTRY_ADMIN}.

    Integrity is separate: even after ACCEPT_CONTINUE, bad hash → no write.
    Policy mapping is orthogonal and never enables authorization.
    """
    auth_present = Bool("auth_present")
    auth_scope = String("auth_scope")
    req_action = String("req_action")
    integrity_ok = Bool("integrity_ok")
    policy_maps = Bool("policy_maps")

    # Kernel decision (lane hard-binds req_action to ADMIN in Python;
    # model keeps req_action free to check the kernel contract).
    is_halt = Not(auth_present)
    scope_ok = auth_scope == _admin()
    action_ok = req_action == _admin()
    is_reject = And(auth_present, Or(Not(scope_ok), Not(action_ok)))
    is_accept = And(auth_present, scope_ok, action_ok)

    # Mutual exclusion of decision (for clarity in models)
    decision_partition = Or(
        And(is_halt, Not(is_reject), Not(is_accept)),
        And(Not(is_halt), is_reject, Not(is_accept)),
        And(Not(is_halt), Not(is_reject), is_accept),
    )

    authorized = is_accept

    # Transition: write only if authorized AND integrity passes.
    # This is the observed registry behavior, not an axiom of "writes are good".
    write = And(authorized, integrity_ok)

    # Rejection / halt ⇒ zero write (same step)
    reject_or_halt = Or(is_halt, is_reject)
    zero_write_on_reject = Implies(reject_or_halt, Not(write))

    # Policy never participates in authorization
    policy_does_not_authorize = Implies(Not(authorized), Not(And(policy_maps, write)))

    return {
        "auth_present": auth_present,
        "auth_scope": auth_scope,
        "req_action": req_action,
        "integrity_ok": integrity_ok,
        "policy_maps": policy_maps,
        "is_halt": is_halt,
        "is_reject": is_reject,
        "is_accept": is_accept,
        "authorized": authorized,
        "write": write,
        "decision_partition": decision_partition,
        "zero_write_on_reject": zero_write_on_reject,
        "policy_does_not_authorize": policy_does_not_authorize,
    }


def _check(extra, *, expect_unsat: bool, background: Optional[Sequence] = None) -> Tuple[str, bool]:
    s = Solver()
    if background:
        for c in background:
            s.add(c)
    s.add(extra)
    r = s.check()
    if r == unsat:
        actual = "UNSAT"
    elif r == sat:
        actual = "SAT"
    else:
        actual = "UNKNOWN"
    expected = "UNSAT" if expect_unsat else "SAT"
    return actual, actual == expected


def run_checks() -> List[PropertyResult]:
    m = build_transition_model()
    bg = [m["decision_partition"]]

    results: List[PropertyResult] = []

    # F-001: missing authority cannot write
    actual, ok = _check(
        And(Not(m["auth_present"]), m["write"]),
        expect_unsat=True,
        background=bg,
    )
    results.append(
        PropertyResult(
            "F-001",
            "missing_authority_cannot_write",
            "UNSAT",
            actual,
            ok,
            "AuthorityHalt path; no registry assign",
        )
    )

    # F-002: wrong scope cannot write
    actual, ok = _check(
        And(m["auth_present"], m["auth_scope"] != _admin(), m["write"]),
        expect_unsat=True,
        background=bg,
    )
    results.append(
        PropertyResult(
            "F-002",
            "wrong_scope_cannot_write",
            "UNSAT",
            actual,
            ok,
            "AuthorityError path",
        )
    )

    # F-003: wrong requested_action cannot write
    actual, ok = _check(
        And(m["auth_present"], m["req_action"] != _admin(), m["write"]),
        expect_unsat=True,
        background=bg,
    )
    results.append(
        PropertyResult(
            "F-003",
            "wrong_action_cannot_write",
            "UNSAT",
            actual,
            ok,
            "Kernel: requested_action must be in declared_scopes",
        )
    )

    # F-004: policy mapping cannot authorize a write
    actual, ok = _check(
        And(m["policy_maps"], m["write"], Not(m["authorized"])),
        expect_unsat=True,
        background=bg,
    )
    results.append(
        PropertyResult(
            "F-004",
            "policy_cannot_authorize_write",
            "UNSAT",
            actual,
            ok,
            "PolicyMapping has no registry mutation API",
        )
    )

    # F-005: authorization does not itself force write
    actual, ok = _check(
        And(m["authorized"], Not(m["write"])),
        expect_unsat=False,
        background=bg,
    )
    results.append(
        PropertyResult(
            "F-005",
            "authorization_not_execution",
            "SAT",
            actual,
            ok,
            "Auth OK + integrity fail → no write (intentional SAT)",
        )
    )

    # F-006: rejection/halt implies zero-write
    actual, ok = _check(
        And(Or(m["is_halt"], m["is_reject"]), m["write"]),
        expect_unsat=True,
        background=bg,
    )
    results.append(
        PropertyResult(
            "F-006",
            "rejection_zero_write",
            "UNSAT",
            actual,
            ok,
            "HALT/REJECT steps do not assign registry state",
        )
    )

    return results


def format_report(results: Sequence[PropertyResult]) -> str:
    lines = [
        "SWI Z3 LAW AUTHORITY CHECK",
        "==========================",
        "",
        "STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED",
        "SCOPE:  finite single-step authority/law-registry transition model",
        "TIP:    designed against experimental/law contract @ 4cb10a0",
        "",
    ]
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        lines.append(
            f"{r.prop_id}  {r.name:<36}  expected={r.expected:<5}  actual={r.actual:<7}  [{mark}]"
        )
        if r.note:
            lines.append(f"         {r.note}")
    all_ok = all(r.passed for r in results)
    lines.append("")
    lines.append(f"MODEL RESULT: {'PASS' if all_ok else 'FAIL'}")
    lines.append(
        "LIMITATION: Formal model ≠ Python proof. "
        "Correspondence requires independent audit."
    )
    lines.append(
        "NOT CLAIMED: seal, production authorization, legal compliance, "
        "durable replay protection."
    )
    return "\n".join(lines)


def main() -> int:
    results = run_checks()
    print(format_report(results))
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
