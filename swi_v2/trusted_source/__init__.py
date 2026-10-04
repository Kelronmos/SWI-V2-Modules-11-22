"""SWI trusted-source spine inspection (read-only, fail-closed).

GREEN = structural checks passed only.
Does NOT prove law, policy, standard authority, or production authorization.
"""

from swi_v2.trusted_source.spine_inspector import (
    FieldStatus,
    InspectionResult,
    SpineBreak,
    inspect_record,
    inspect_paths,
    format_report,
)

__all__ = [
    "FieldStatus",
    "InspectionResult",
    "SpineBreak",
    "inspect_record",
    "inspect_paths",
    "format_report",
]
