# LAW-TRUTH Limitations (live)

Synced with docs/pre-R/LIMITATIONS.md and the diagnostic evidence.

## Proven

Within the enforced experimental API path  
(`enforce` → `require_executable` / `privileged_action`)  
a REJECT/HALT state cannot reach privileged execution.

## Unproven / remaining gaps

- Process-wide bypass resistance  
- Arbitrary alternate execution paths  
- Runtime monkey-patching / direct mutation of kernel objects  
- Complete structural coverage (Level 4)  
- Independent verification of escape impossibility (Level 5)  
- Automatic recovery protocol (PR-011)  
- Production key custody / network transport / UI adapter  
- Live V1 export script vs Trainer.process(admission=…) mismatch (PR-015)

## Standing architectural separation

PRE-CONSEQUENCES is a separate architecture and is **not implemented**.  
No equivalence, interoperability, or runtime claim is made.
