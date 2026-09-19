# SWI_V103_API_Foundation — Position relative to V2

**External repo:** https://github.com/Kelronmos/SWI_V103_API_Foundation  
**V2 stance:** LEGACY STUB · **NOT** a runtime dependency · **NOT** on M11 sealed path

## Why document here

“V1.03 API Foundation” can be confused with V1 modules 00–10. V103 holds minimal Rust structs and an incomplete zip scaffold. It has **no** proven link to V2 admission or the M11 seal.

Detail in V103: `docs/STATUS.md`, `docs/CONNECTION_REQUIREMENTS.md`, `docs/LIMITATIONS.md`.

## Connection state

```text
V103 ──(none)──► V2 M11
V1  ──(serialized evidence)──► V2 M11   ← active path
```

Any future HTTP adapter must not create authority or bypass admission.

## Non-claims

Do not cite V103 for production API, security standing scores, Firefly integration, or sealed continuity.
