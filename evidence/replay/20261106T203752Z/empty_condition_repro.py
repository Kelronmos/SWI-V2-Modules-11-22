from swi_v2.kernel.governing_permit import evaluate_governing_permit

result = evaluate_governing_permit(
    conditions=[],
    L={"read"},
    G={"read"},
    S={"read"},
    H={"read"},
    evidence={"receipt_id": "EMPTY-CONDITION-REPLAY"},
)

print("OUTCOME:", result.outcome.value)
print("REASON:", result.reason)
print("CONDITIONS:", sorted(result.conditions))
print("FAILED LAYERS:", result.failed_layers)
print("PROVEN:", result.proven)
print("SEALED:", result.sealed)
print("PRODUCTION AUTHORIZED:", result.production_authorized)
