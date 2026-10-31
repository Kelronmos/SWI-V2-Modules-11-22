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

def _fallback_validate(record: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """Minimal but useful validation when jsonschema is unavailable."""
    errors: List[str] = []
    for req in schema.get("required", []):
        if req not in record:
            errors.append(f"missing required field: {req}")
    props = schema.get("properties", {})
    if "schema_version" in props:
        const = props["schema_version"].get("const")
        if const is not None and record.get("schema_version") != const:
            errors.append(f"invalid schema_version: {record.get('schema_version')}")
    if "outcome" in props and "outcome" in record:
        enum = props["outcome"].get("enum")
        if enum and record["outcome"] not in enum:
            errors.append(f"UNKNOWN_STATUS/invalid outcome: {record['outcome']}")
    type_map = {"string": str, "integer": int, "boolean": bool, "object": dict, "array": list}
    for key, prop in props.items():
        if key not in record or record[key] is None:
            continue
        t = prop.get("type")
        if t is None:
            continue
        types = t if isinstance(t, list) else [t]
        if record[key] is None and "null" in types:
            continue
        py_types = tuple(type_map[x] for x in types if x in type_map)
        if py_types and not isinstance(record[key], py_types):
            errors.append(f"{key}: invalid type {type(record[key]).__name__}, expected {types}")
    if "governance" in record and "governance" in props:
        gschema = props["governance"]
        if gschema.get("type") == "object" and not isinstance(record["governance"], dict):
            errors.append("governance: invalid type, expected object")
        elif isinstance(record.get("governance"), dict):
            for req in gschema.get("required", []):
                if req not in record["governance"]:
                    errors.append(f"governance missing required field: {req}")
    return errors

def validate_record(record: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if HAS_JSONSCHEMA:
        errors: List[str] = []
        validator = Draft202012Validator(schema)
        for e in sorted(validator.iter_errors(record), key=lambda x: list(x.path)):
            errors.append(f"{'/'.join(str(p) for p in e.path)}: {e.message}")
        return (len(errors) == 0, errors)
    errors = _fallback_validate(record, schema)
    return (len(errors) == 0, errors)

def assert_valid(record: Dict[str, Any], schema: Dict[str, Any]) -> None:
    ok, errors = validate_record(record, schema)
    if not ok:
        raise SchemaValidationError(errors)
