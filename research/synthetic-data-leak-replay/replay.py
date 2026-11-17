import argparse
import hashlib
import json
from pathlib import Path


def canonical(data):
    return json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()


class EvidenceLedger:
    def __init__(self):
        self.events = []
        self.previous_hash = "GENESIS"

    def record(self, event, actor, details):
        item = {
            "sequence": len(self.events) + 1,
            "event": event,
            "actor": actor,
            "details": details,
            "previous_hash": self.previous_hash,
        }
        item["hash"] = hashlib.sha256(canonical(item)).hexdigest()
        self.previous_hash = item["hash"]
        self.events.append(item)
        return item

    def verify(self):
        previous = "GENESIS"

        for index, item in enumerate(self.events):
            if item["sequence"] != index + 1:
                return False

            if item["previous_hash"] != previous:
                return False

            unsigned = dict(item)
            recorded_hash = unsigned.pop("hash")

            if hashlib.sha256(canonical(unsigned)).hexdigest() != recorded_hash:
                return False

            previous = recorded_hash

        return True


def vulnerable_scenario():
    ledger = EvidenceLedger()

    ledger.record("PURPOSE_DEFINED", "organization", {
        "purpose": "student_service",
        "declared": True
    })

    ledger.record("DATA_COLLECTED", "organization", {
        "fields": ["email", "date_of_birth"],
        "synthetic": True
    })

    ledger.record("ACCESS_GRANTED", "legacy_system", {
        "recipient": "external_vendor",
        "admitted": False,
        "authorization": False,
        "scope_check": False
    })

    ledger.record("DATA_DISCLOSED", "legacy_system", {
        "recipient": "external_vendor",
        "disclosed": True,
        "synthetic": True
    })

    return ledger


def corrected_scenario():
    ledger = EvidenceLedger()

    ledger.record("PURPOSE_DEFINED", "organization", {
        "purpose": "student_service",
        "declared": True
    })

    ledger.record("DATA_COLLECTED", "organization", {
        "fields": ["email"],
        "synthetic": True
    })

    request = {
        "recipient": "external_vendor",
        "admitted": False,
        "authorized": False,
        "allowed_recipients": ["internal_service"],
    }

    permitted = (
        request["admitted"]
        and request["authorized"]
        and request["recipient"] in request["allowed_recipients"]
    )

    if permitted:
        ledger.record("DATA_DISCLOSED", "governed_system", {
            "recipient": request["recipient"],
            "disclosed": True
        })
        decision = "PERMITTED"
    else:
        ledger.record("ACCESS_DENIED", "governed_system", {
            "recipient": request["recipient"],
            "reason": "ADMISSION_AUTHORIZATION_AND_SCOPE_NOT_SATISFIED"
        })
        decision = "DENIED"

    return ledger, decision


def build_report():
    vulnerable = vulnerable_scenario()
    corrected, decision = corrected_scenario()

    leak = any(
        event["event"] == "DATA_DISCLOSED"
        for event in vulnerable.events
    )

    root_causes = [
        "Data collection was not sufficiently minimized.",
        "Recipient admission was not enforced.",
        "Explicit authorization was not enforced.",
        "Recipient scope was not enforced.",
    ]

    return {
        "classification": "SYNTHETIC_DEMONSTRATION",
        "implementation_proven": False,
        "sealed": False,
        "production_authorized": False,
        "baseline": {
            "incident_detected": leak,
            "ledger_valid": vulnerable.verify(),
            "events": vulnerable.events,
        },
        "investigation": {
            "root_causes": root_causes,
            "investigation_complete": True,
            "basis": "Synthetic event records only."
        },
        "corrected_replay": {
            "decision": decision,
            "unauthorized_disclosure_prevented": decision == "DENIED",
            "ledger_valid": corrected.verify(),
            "events": corrected.events,
        },
        "limitations": [
            "No real-world data was used.",
            "No real network or external recipient was contacted.",
            "This is not an implementation audit.",
            "This does not establish independent verification.",
            "This does not establish production safety."
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="evidence/replay.json")
    args = parser.parse_args()

    report = build_report()
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")

    print("CLASSIFICATION:", report["classification"])
    print("BASELINE INCIDENT:", report["baseline"]["incident_detected"])
    print("BASELINE LEDGER:", report["baseline"]["ledger_valid"])
    print("ROOT CAUSES:", len(report["investigation"]["root_causes"]))
    print("CORRECTED DECISION:", report["corrected_replay"]["decision"])
    print("CORRECTED LEDGER:", report["corrected_replay"]["ledger_valid"])
    print("IMPLEMENTATION PROVEN:", report["implementation_proven"])
    print("SEALED:", report["sealed"])
    print("PRODUCTION AUTHORIZED:", report["production_authorized"])
    print("REPORT:", path)


if __name__ == "__main__":
    main()
