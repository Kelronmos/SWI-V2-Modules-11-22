# V2 Release Gate

## Foundation phase close (current)

Not: “Modules 11–22 complete.”

Yes: contract frozen · local travel proven · two-checkout CI when green · M11/Kernel seal **only** if `V2_CLOSING_AND_M11_SEAL_MANUAL.md` checklist passes.

## Blockers for M11 SEAL

1. Live two-checkout **CI_VERIFIED** (not local-only)  
2. Primary proof uses **real V1 producer** artifact  
3. Full negative matrix  
4. Kernel isolation on reject  
5. Docs match code  

## Blockers for M12+

M11 not sealed · map not frozen · CRTG not required for M12 start but must not be falsely claimed

## Status line

```text
M11 NOT SEALED · TWO_CHECKOUT PENDING · CRTG DESIGN PENDING · M12–22 BLOCKED
```
