"""Authority gate for law-registry mutations.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED
Re-uses kernel authority primitives; does not weaken them.
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
    """
    return require_authorization_for_action(
        authorization_present=authorization_present,
        authorization_scope=authorization_scope,
        requested_action=mutation.value,
        declared_scopes={LAW_REGISTRY_ADMIN_SCOPE},
    )
