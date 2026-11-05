from .models import Domain, State

VALUES = {
    State.SATISFIED: 1.0,
    State.PARTIAL: 0.5,
    State.FAILED: 0.0,
    State.UNKNOWN: 0.0,
}


def evaluate(boards):
    by_domain = {}
    errors = []

    try:
        for board in boards:
            if board.domain in by_domain:
                raise ValueError(
                    "Duplicate board: " + board.domain.value
                )
            board.validate()
            by_domain[board.domain] = board
    except (ValueError, AttributeError) as exc:
        errors.append(str(exc))

    missing = sorted(
        domain.value
        for domain in set(Domain) - set(by_domain)
    )

    results = {}

    if not errors:
        for domain, board in by_domain.items():
            applicable = [
                requirement
                for requirement in board.requirements
                if requirement.state != State.NOT_APPLICABLE
            ]

            total_weight = sum(
                requirement.weight for requirement in applicable
            )

            score = None
            if total_weight > 0:
                weighted_total = sum(
                    requirement.weight * VALUES[requirement.state]
                    for requirement in applicable
                )
                score = round(
                    100 * weighted_total / total_weight, 2
                )

            unresolved = [
                requirement.id
                for requirement in applicable
                if requirement.state in (
                    State.PARTIAL,
                    State.FAILED,
                    State.UNKNOWN,
                )
            ]

            mandatory_blockers = [
                requirement.id
                for requirement in applicable
                if requirement.mandatory
                and requirement.id in unresolved
            ]

            results[domain.value] = {
                "evidence_coverage_score": score,
                "unresolved": unresolved,
                "mandatory_blockers": mandatory_blockers,
                "requirements": len(board.requirements),
                "applicable_requirements": len(applicable),
            }

    prohibition = (
        not errors
        and any(
            requirement.prohibits_action
            and bool(requirement.evidence_refs)
            for board in by_domain.values()
            for requirement in board.requirements
        )
    )

    unresolved_exists = any(
        result["unresolved"]
        for result in results.values()
    )

    all_boards_unassessed = (
        not errors
        and not missing
        and bool(results)
        and all(
            result["applicable_requirements"] == 0
            for result in results.values()
        )
    )

    if errors or missing:
        status = "BLOCKED"
    elif prohibition:
        status = "DENY"
    elif unresolved_exists:
        status = "BLOCKED"
    elif all_boards_unassessed:
        status = "NOT_ASSESSED"
    else:
        status = "MATCH"

    return {
        "status": status,
        "boards": results,
        "missing_boards": missing,
        "errors": errors,
        "permit": "NOT_ISSUED",
        "execution": "NOT_PERFORMED",
        "production_authorized": False,
    }
