# Known Limitations — Volume 2

- The V1→V2 evidence handoff is an authored CI pipeline (checkout → export → upload-artifact → download-artifact → admit), not native or emergent inter-system communication.
- V2 verifies the evidence artifact’s schema and integrity; it does not verify the identity of whatever produced it (see CRTG — PROPOSED / DESIGN PENDING, not implemented).
- A real V1 foundation evidence producer path exists and has been exercised (local two-venv and cited two-checkout CI); unit tests may still use fixtures for negative cases. Integrity of the artifact is not the same as truth or authenticated origin.
- Module 11 is IMPLEMENTED / TESTED and remains **NOT SEALED** until the formal A–G audit and seal record are complete.
- Modules 12–22 are not substantively implemented (12 is a type-boundary / placeholder scaffold only).
- No universal AI safety or production certification claims.
