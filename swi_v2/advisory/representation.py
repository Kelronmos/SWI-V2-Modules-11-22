"""Representation integrity — DOCUMENT_ID ≠ REPRESENTATION_ID ≠ HASH ≠ AUTHORITY."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RepresentationLevel(str, Enum):
    LEVEL_0_EXISTENCE = "LEVEL_0_EXISTENCE"
    LEVEL_1_METADATA = "LEVEL_1_METADATA"
    LEVEL_2_OPERATIONAL = "LEVEL_2_OPERATIONAL"
    LEVEL_3_RESTRICTED = "LEVEL_3_RESTRICTED"
    LEVEL_4_FULL = "LEVEL_4_FULL"


@dataclass(frozen=True)
class Representation:
    document_id: str
    representation_id: str
    level: RepresentationLevel
    content: str
    parent_representation_id: Optional[str] = None

    def lineage(self) -> tuple:
        return (self.document_id, self.representation_id, self.parent_representation_id)


def representation_hash(rep: Representation) -> str:
    payload = f"{rep.document_id}|{rep.representation_id}|{rep.level.value}|{rep.content}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
