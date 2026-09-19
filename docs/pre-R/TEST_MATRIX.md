# pre-R Test Matrix (V2)

**Status:** DESIGN — not executable yet  

| Mutation | Expected |
|----------|----------|
| Change result | Reject |
| Change request binding | Reject |
| Change / expand authority | Reject |
| Change destination | Reject |
| Remove / replace evidence | Reject |
| Change policy / expiry | Reject |
| Replay expired / revoked | Reject |
| Unknown key / invalid integrity | Reject |
| UI-added authorization | Reject |
| Backend-added authorization | Reject |
| Response as new privilege | New authorization required |
| Valid presentation transform | Admit only if contract permits |
| Unknown security state | Halt / reject |
