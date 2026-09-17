"""
M11 post-admission cryptographic seal.

STATUS: IMPLEMENTED / TESTED (post-admission seal path)
Architecture:
  AdmittedInput (only) → canonical → digest → chain → Merkle → Ed25519 → SealedEvidence

Does NOT:
  - accept FoundationEvidenceEnvelope or raw dict as seal input
  - claim CRTG, Foundation Seal 5, production key management, or M11 SEALED
  - claim that signing equals replay protection
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Optional

from .contracts import AdmittedInput
from .ed25519_sig import (
    SignatureVerificationError,
    canonical_message,
    sign_ed25519,
    verify_ed25519,
)
from .merkle import MerkleProof, MerkleTree


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_admitted_input(admitted: AdmittedInput) -> bytes:
    material = {
        "payload": admitted.payload,
        "foundation_version": admitted.foundation_version,
        "evidence_schema_version": admitted.evidence_schema_version,
        "evidence_id": admitted.evidence_id,
        "integrity_reference": admitted.integrity_reference,
        "source_reference": admitted.source_reference,
        "admitted_by": admitted.admitted_by,
    }
    return canonical_message(material)


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
    seal_version: str = "1.0-proposed"


def create_seal(
    admitted: AdmittedInput,
    private_key: bytes,
    public_key: bytes,
    previous_chain_hash: Optional[str] = None,
) -> SealedEvidence:
    """Seal only AdmittedInput from M11. Rejects envelope/dict bypass."""
    if not isinstance(admitted, AdmittedInput):
        raise TypeError(
            "create_seal requires AdmittedInput from M11 admission; "
            f"got {type(admitted).__name__}"
        )

    canonical = _canonical_admitted_input(admitted)
    evidence_digest = _sha256_hex(canonical)

    chain_material = {
        "evidence_id": admitted.evidence_id,
        "evidence_digest": evidence_digest,
        "previous_chain_hash": previous_chain_hash,
    }
    chain_hash = _sha256_hex(canonical_message(chain_material))

    tree = MerkleTree([canonical, chain_hash.encode("utf-8")])
    proof = tree.prove(0)

    signing_material = {
        "seal_version": "1.0-proposed",
        "evidence_id": admitted.evidence_id,
        "evidence_digest": evidence_digest,
        "previous_chain_hash": previous_chain_hash,
        "chain_hash": chain_hash,
        "merkle_root": tree.root.hex(),
    }
    signature = sign_ed25519(private_key, canonical_message(signing_material))

    return SealedEvidence(
        evidence_id=admitted.evidence_id,
        evidence_digest=evidence_digest,
        previous_chain_hash=previous_chain_hash,
        chain_hash=chain_hash,
        merkle_root=tree.root.hex(),
        merkle_proof=proof,
        signature=signature,
        public_key=public_key,
    )


def verify_seal(admitted: AdmittedInput, sealed: SealedEvidence) -> bool:
    """Independent verification. Returns False on any covered mismatch."""
    if not isinstance(admitted, AdmittedInput):
        return False

    try:
        canonical = _canonical_admitted_input(admitted)
        expected_digest = _sha256_hex(canonical)

        if expected_digest != sealed.evidence_digest:
            return False
        if admitted.evidence_id != sealed.evidence_id:
            return False

        chain_material = {
            "evidence_id": admitted.evidence_id,
            "evidence_digest": expected_digest,
            "previous_chain_hash": sealed.previous_chain_hash,
        }
        expected_chain = _sha256_hex(canonical_message(chain_material))
        if expected_chain != sealed.chain_hash:
            return False

        proof = sealed.merkle_proof
        if proof.root.hex() != sealed.merkle_root:
            return False
        if not MerkleTree.verify(proof):
            return False

        signing_material = {
            "seal_version": sealed.seal_version,
            "evidence_id": admitted.evidence_id,
            "evidence_digest": expected_digest,
            "previous_chain_hash": sealed.previous_chain_hash,
            "chain_hash": expected_chain,
            "merkle_root": sealed.merkle_root,
        }
        verify_ed25519(
            sealed.public_key,
            canonical_message(signing_material),
            sealed.signature,
        )
        return True
    except (SignatureVerificationError, ValueError, TypeError, Exception):
        return False
