"""Education role model — relationship structure, not authority inheritance."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class EducationRole(str, Enum):
    CHILD_STUDENT = "CHILD_STUDENT"
    TEACHER_DESIGNATED_STAFF = "TEACHER_DESIGNATED_STAFF"
    PARENT_GUARDIAN = "PARENT_GUARDIAN"
    SCHOOL_ADMINISTRATION = "SCHOOL_ADMINISTRATION"
    MINISTRY_EDUCATION_BODY = "MINISTRY_EDUCATION_BODY"
    GOVERNMENT_COMPETENT_AUTHORITY = "GOVERNMENT_COMPETENT_AUTHORITY"


_DEFAULT_SCOPES: dict[EducationRole, FrozenSet[str]] = {
    EducationRole.CHILD_STUDENT: frozenset({"self_notice"}),
    EducationRole.TEACHER_DESIGNATED_STAFF: frozenset({"class_notice", "self_notice"}),
    EducationRole.PARENT_GUARDIAN: frozenset({"child_notice", "self_notice"}),
    EducationRole.SCHOOL_ADMINISTRATION: frozenset({"school_notice", "class_notice"}),
    EducationRole.MINISTRY_EDUCATION_BODY: frozenset({"policy_notice", "school_notice"}),
    EducationRole.GOVERNMENT_COMPETENT_AUTHORITY: frozenset({"policy_notice"}),
}


@dataclass(frozen=True)
class RoleScope:
    role: EducationRole
    scopes: FrozenSet[str]
    jurisdiction: str = ""

    @classmethod
    def for_role(cls, role: EducationRole, *, jurisdiction: str = "") -> "RoleScope":
        return cls(role=role, scopes=_DEFAULT_SCOPES[role], jurisdiction=jurisdiction)


def role_may_receive(scope: RoleScope, notice_scope: str) -> bool:
    return notice_scope in scope.scopes
