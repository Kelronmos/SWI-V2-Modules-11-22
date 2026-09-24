"""Interpretive policy mapping.

STATUS: RESEARCH / EXPERIMENTAL · NOT SEALED

A mapping is an interpretation of source material.
It is not itself legal authority.
It can never mutate the underlying LawArtifact.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyMapping:
    mapping_id: str

    law_id: str
    law_version: str

    source_reference: str

    policy_statement: str

    interpretation_basis: str

    mapping_hash: str

    status: str = "INTERPRETIVE_MAPPING"
