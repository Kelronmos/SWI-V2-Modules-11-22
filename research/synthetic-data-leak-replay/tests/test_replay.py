import unittest

from replay import (
    vulnerable_scenario,
    corrected_scenario,
    build_report,
    EvidenceLedger,
)


class DataLeakReplayTests(unittest.TestCase):

    def test_baseline_reproduces_disclosure(self):
        ledger = vulnerable_scenario()

        self.assertTrue(any(
            event["event"] == "DATA_DISCLOSED"
            for event in ledger.events
        ))

    def test_baseline_evidence_chain_is_valid(self):
        self.assertTrue(vulnerable_scenario().verify())

    def test_corrected_workflow_denies_unauthorized_recipient(self):
        ledger, decision = corrected_scenario()

        self.assertEqual(decision, "DENIED")
        self.assertFalse(any(
            event["event"] == "DATA_DISCLOSED"
            for event in ledger.events
        ))

    def test_corrected_evidence_chain_is_valid(self):
        ledger, _ = corrected_scenario()
        self.assertTrue(ledger.verify())

    def test_report_preserves_proof_boundaries(self):
        report = build_report()

        self.assertFalse(report["implementation_proven"])
        self.assertFalse(report["sealed"])
        self.assertFalse(report["production_authorized"])

    def test_root_causes_are_recorded(self):
        report = build_report()

        self.assertGreaterEqual(
            len(report["investigation"]["root_causes"]), 1
        )

    def test_tampering_is_detected(self):
        ledger = EvidenceLedger()
        ledger.record("PURPOSE_DEFINED", "test", {"purpose": "test"})
        ledger.record("DATA_COLLECTED", "test", {"synthetic": True})

        self.assertTrue(ledger.verify())

        ledger.events[0]["details"]["purpose"] = "changed"

        self.assertFalse(ledger.verify())


if __name__ == "__main__":
    unittest.main()
