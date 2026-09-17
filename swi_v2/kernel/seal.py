"""
M11 post-admission cryptographic seal.

STATUS: IMPLEMENTED / TESTED (post-admission seal path)
NOT: M11 SEALED · CRTG · Foundation Seal 5 · production key governance

Admission integrity may use default=str (V1/V2 contract). Seal canonicalization does not.
Verifier reconstructs expected Merkle tree/proof from AdmittedInput (no proof substitution).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Optional

from .contracts import AdmittedInput
from .ed25519_sig import sign_ed25519, verify_ed25519
from .merkle import MerkleProof, MerkleTree

SEAL_DOMAIN = "SWI-M11-SEAL-V1"
SEAL_VERSION = "1.0-proposed"
COMMITMENT_PREFIX = b"SWI-M11-SEAL-COMMITMENT-V1:"
CHAIN_PREFIX = b"SWI-M11-CHAIN-V1:"
CHAIN_GENESIS = hashlib.sha256(b"SWI-M11-CHAIN-GENESIS-V1:").hexdigest()
SIGN_DOMAIN = "SWI-M11-SEAL-SIGN-V1"


class SealCanonicalizationError(ValueError):
    pass


def _validate_json_types(obj: Any, path: str = "$") -> None:
    if obj is None or isinstance(obj, bool):
        return
    if isinstance(obj, int) and not isinstance(obj, bool):
        return
    if isinstance(obj, float):
        return
    if isinstance(obj, str):
        return
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            _validate_json_types(v, f"{path}[{i}]")
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise SealCanonicalizationError(f"non-string key at {path}")
            _validate_json_types(v, f"{path}.{k}")
        return
    raise SealCanonicalizationError(
        f"unsupported type {type(obj).__name__} at {path}"
    )


def seal_canonicalize(material: Mapping[str, Any]) -> bytes:
    _validate_json_types(material)
    return json.dumps(
        material, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seal_material_from_admitted(admitted: AdmittedInput) -> dict:
    return {
        "domain": SEAL_DOMAIN,
        "seal_version": SEAL_VERSION,
        "payload": admitted.payload,
        "foundation_version": admitted.foundation_version,
        "evidence_schema_version": admitted.evidence_schema_version,
        "evidence_id": admitted.evidence_id,
        "integrity_reference": admitted.integrity_reference,
        "source_reference": admitted.source_reference,
        "admitted_by": admitted.admitted_by,
    }


def _canonical_admitted_input(admitted: AdmittedInput) -> bytes:
    """Single canonical representation for seal cryptography."""
    if not isinstance(admitted, AdmittedInput):
        raise TypeError("expected AdmittedInput")
    return seal_canonicalize(seal_material_from_admitted(admitted))


def commitment_from_admitted(admitted: AdmittedInput) -> str:
    return _sha256_hex(COMMITMENT_PREFIX + _canonical_admitted_input(admitted))


def _chain_hash(previous: str, commitment: str) -> str:
    return _sha256_hex(CHAIN_PREFIX + previous.encode("utf-8") + commitment.encode("utf-8"))


@dataclass(frozen=True)
class SealedEvidence:
    evidence_id: str
    evidence_digest: str
    previous_chain_hash: Optional[str]
    chain_hash: str
    merkle_root: str
    merkle_proof: MerkleProof
    signature: bytes
    public_key: bytes
    seal_version: str = SEAL_VERSION
    domain: str = SEAL_DOMAIN


def create_seal(
    admitted: AdmittedInput,
    private_key: bytes,
    public_key: bytes,
    previous_chain_hash: Optional[str] = None,
) -> SealedEvidence:
    if not isinstance(admitted, AdmittedInput):
        raise TypeError(
            f"create_seal requires AdmittedInput; got {type(admitted).__name__}"
        )

    evidence_digest = commitment_from_admitted(admitted)
    prev = previous_chain_hash if previous_chain_hash is not None else CHAIN_GENESIS
    chain_hash = _chain_hash(prev, evidence_digest)
    tree = MerkleTree([evidence_digest.encode("utf-8"), chain_hash.encode("utf-8")])
    proof = tree.prove(0)
    signing_material = {
        "domain": SIGN_DOMAIN,
        "seal_version": SEAL_VERSION,
        "evidence_id": admitted.evidence_id,
        "commitment": evidence_digest,
        "previous_chain_hash": prev,
        "chain_hash": chain_hash,
        "merkle_root": tree.root.hex(),
    }
    signature = sign_ed25519(private_key, seal_canonicalize(signing_material))
    return SealedEvidence(
        evidence_id=admitted.evidence_id,
        evidence_digest=evidence_digest,
        previous_chain_hash=prev,
        chain_hash=chain_hash,
        merkle_root=tree.root.hex(),
        merkle_proof=proof,
        signature=signature,
        public_key=public_key,
    )


def verify_seal(admitted: AdmittedInput, sealed: SealedEvidence) -> bool:
    """Independently reconstruct commitment, chain, Merkle proof, signature."""
    if not isinstance(admitted, AdmittedInput):
        return False
    try:
        expected_digest = commitment_from_admitted(admitted)
        if expected_digest != sealed.evidence_digest:
            return False
        if admitted.evidence_id != sealed.evidence_id:
            return False
        if sealed.domain != SEAL_DOMAIN or sealed.seal_version != SEAL_VERSION:
            return False

        prev = (
            sealed.previous_chain_hash
            if sealed.previous_chain_hash is not None
            else CHAIN_GENESIS
        )
        expected_chain = _chain_hash(prev, expected_digest)
        if expected_chain != sealed.chain_hash:
            return False

        expected_tree = MerkleTree(
            [expected_digest.encode("utf-8"), expected_chain.encode("utf-8")]
        )
        expected_proof = expected_tree.prove(0)
        if sealed.merkle_root != expected_tree.root.hex():
            return False
        if sealed.merkle_proof != expected_proof:
            return False
        if not MerkleTree.verify(sealed.merkle_proof):
            return False

        signing_material = {
            "domain": SIGN_DOMAIN,
            "seal_version": sealed.seal_version,
            "evidence_id": admitted.evidence_id,
            "commitment": expected_digest,
            "previous_chain_hash": prev,
            "chain_hash": expected_chain,
            "merkle_root": sealed.merkle_root,
        }
        verify_ed25519(
            sealed.public_key,
            seal_canonicalize(signing_material),
            sealed.signature,
        )
        return True
    except Exception:
        return False
