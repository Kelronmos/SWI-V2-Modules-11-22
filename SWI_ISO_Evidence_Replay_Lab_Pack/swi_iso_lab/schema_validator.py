"""JSON Schema validation for evidence records (Draft 2020-12)."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from jsonschema import Draft202012Validator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

class SchemaValidationError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("; ".join(errors))

def load_schema(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_record(record: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if HAS_JSONSCHEMA:
        validator = Draft202012Validator(schema)
        for e in sorted(validator.iter_errors(record), key=lambda x: list(x.path)):
            errors.append(f"{'/'.join(str(p) for p in e.path)}: {e.message}")
        return (len(errors) == 0, errors)
    for req in schema.get("required", []):
        if req not in record:
            errors.append(f"missing required field: {req}")
    if "schema_version" in schema.get("properties", {}):
        const = schema["properties"]["schema_version"].get("const")
        if const and record.get("schema_version") != const:
            errors.append(f"invalid schema_version: {record.get('schema_version')}")
    if "outcome" in record and "outcome" in schema.get("properties", {}):
        enum = schema["properties"]["outcome"].get("enum")
        if enum and record["outcome"] not in enum:
            errors.append(f"UNKNOWN_STATUS/invalid outcome: {record['outcome']}")
    return (len(errors) == 0, errors)

def assert_valid(record: Dict[str, Any], schema: Dict[str, Any]) -> None:
    ok, errors = validate_record(record, schema)
    if not ok:
        raise SchemaValidationError(errors)
