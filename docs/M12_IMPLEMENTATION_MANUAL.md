# M12 Implementation Manual — THE MASTERY ARCHIVE

**Contract authority:** `docs/M12_CONTRACT.md` (frozen)  
**Status:** Pass 1 complete · Pass 2+ not started

## Doctrine

Evidence before claim · boundary before expansion · contract before code · test for behaviour · CI for reproducibility · seal for controlled dependency · never claim what the code cannot demonstrate.

## Pass order

1. **Contract** — done (`M12_CONTRACT.md`)
2. **Data model** — `NormalizedEvidence` typed model matching §5 of the contract
3. **Normalization function** — validate boundary → extract preserved fields → normalize payload → construct output; remove `accepted_placeholder`
4. **Tests** — acceptance, rejection (dict/None/str/bytes/list), identity/provenance/integrity/admitted_by preservation, determinism, immutability, isolation (`module12_process(raw_envelope)` must fail; admit then process must succeed), no M13+ imports
5. **CI + audit** — property map, worksheet, independent rediscovery, then seal

## Recommended layout (only when implementing)

```text
swi_v2/module12/
  __init__.py          # process() → NormalizedEvidence
  models.py            # NormalizedEvidence
  normalization.py     # pure normalize rules
  errors.py            # M12-specific errors if needed

test/
  test_module12_contract.py
  test_module12_normalization.py
  test_module12_rejection.py
  test_module12_determinism.py
  test_module12_immutability.py
  test_module12_isolation.py
```

Do not create empty files for appearance.

## Placeholder removal

When real implementation lands, production path must not return `accepted_placeholder`. Old scaffold tests that assert placeholder are evidence of the scaffold only.

## Stop conditions

Stop if: M11 dependency unclear · `NormalizedEvidence` ambiguous · tests cannot show a claimed invariant · M12 needs M13 features · security claim lacks evidence.

## M13 handoff (after seal only)

M13 accepts **`NormalizedEvidence`**, not “anything M12 once returned.”
