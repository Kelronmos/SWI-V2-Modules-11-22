"""Authority gate for law-registry mutations.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED
Re-uses kernel authority primitives; does not weaken them.

Kernel contract (require_authorization_for_action):
  - authorization_scope must be in declared_scopes
  - requested_action must also be in declared_scopes
Therefore the lane binds the mutation to the explicit admin scope
rather than treating the mutation name itself as the scope/action.
"""
from __future__ import annotations

from enum import Enum
from typing import Optional

from swi_v2.kernel.authority import (
    AuthorityDecision,
    require_authorization_for_action,
)


class LawMutation(str, Enum):
    INGEST = "INGEST"
    SUPERSEDE = "SUPERSEDE"
    QUARANTINE = "QUARANTINE"
    REVOKE = "REVOKE"


LAW_REGISTRY_ADMIN_SCOPE = "LAW_REGISTRY_ADMIN"


def authorize_law_mutation(
    *,
    mutation: LawMutation,
    authorization_present: bool,
    authorization_scope: Optional[str],
) -> AuthorityDecision:
    """Fail-closed gate for any change to the law registry.

    Missing authority → AuthorityHalt (HALT)
    Wrong / missing scope → AuthorityError (REJECT)

    The kernel primitive requires that *both* the presented scope and the
    requested_action belong to the declared set. We therefore bind the
    requested_action to LAW_REGISTRY_ADMIN_SCOPE itself. The specific
    mutation (INGEST / SUPERSEDE / …) remains an internal lane parameter
    and is not smuggled as an undeclared authority field.
    """
    # mutation is retained for future audit / evidence recording;
    # it is deliberately not passed as requested_action.
    _ = mutation

    return require_authorization_for_action(
        authorization_present=authorization_present,
        authorization_scope=authorization_scope,
        requested_action=LAW_REGISTRY_ADMIN_SCOPE,
        declared_scopes={LAW_REGISTRY_ADMIN_SCOPE},
    )
