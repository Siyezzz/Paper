"""构造夹具的独立边界与分割检查。"""
from copy import deepcopy
from decimal import Decimal
import unittest

from financial_contract_fixtures import cases
from financial_contract_pilot import check_splits, execute, freeze, metadata_solver, read_config, run


class FinancialContractTests(unittest.TestCase):
    def setUp(self):
        self.items = cases()
        self.config = read_config()

    def test_duplicate_ids_and_cross_split_overlap_rejected(self):
        for split in ("discovery", "heldout"):
            items = self.items + [deepcopy(self.items[0])]
            items[-1]["split"] = split
            with self.assertRaisesRegex(ValueError, "duplicate ID or split overlap"):
                check_splits(items, self.config)

    def test_chronological_split_rejected(self):
        for split, decision in (("discovery", "2024-06-01"), ("validation", "2025-01-01"), ("heldout", "2024-12-31")):
            items = cases()
            item = next(c for c in items if c["split"] == split)
            item["decision_at"] = decision
            with self.assertRaisesRegex(ValueError, "chronological"):
                check_splits(items, self.config)

    def test_future_validation_publication_is_leakage(self):
        discovery = [c for c in self.items if c["split"] == "discovery"]
        validation = [c for c in self.items if c["split"] == "validation"]
        validation[0]["current"]["available_at"] = "2025-01-01"
        with self.assertRaisesRegex(ValueError, "temporal leakage"):
            freeze(discovery, validation, self.config)

    def test_heldout_cannot_enter_admission(self):
        with self.assertRaisesRegex(ValueError, "heldout forbidden"):
            freeze([], [self.items[-1]], self.config)

    def test_heldout_changes_cannot_change_frozen_policy(self):
        first = run()
        changed = cases()
        for item in changed:
            if item["split"] == "heldout":
                item["expected"] = "999999"
                item["current"]["value"] = "123456"
        self.assertEqual(first["frozen"], run(changed)["frozen"])

    def test_post_decision_unavailable_but_post_freeze_available_valid(self):
        output = run()["results"]["contract"]["cases"]
        lookup = {r["id"]: r for r in output}
        self.assertIsNone(lookup["H07"]["answer"])
        self.assertIsNone(lookup["H08"]["answer"])
        self.assertTrue(lookup["H11"]["correct_answer"])
        self.assertTrue(lookup["H13"]["correct_answer"])

    def test_exact_decimal_growth_and_safe_scale_invariance(self):
        output = run()["results"]["contract"]["cases"]
        lookup = {r["id"]: r for r in output}
        self.assertEqual(Decimal(lookup["H01"]["answer"]), Decimal("20"))
        self.assertEqual(lookup["H01"]["answer"], lookup["H02"]["answer"])
        self.assertEqual(Decimal(lookup["H03"]["answer"]), Decimal("-25"))

    def test_independent_solver_normalizes_scale_and_rejects_currency(self):
        lookup = {r["id"]: r for r in self.items}
        self.assertEqual(Decimal(metadata_solver(lookup["H04"])), Decimal("20"))
        self.assertIsNone(metadata_solver(lookup["H05"]))

    def test_runtime_revocation_is_local_and_recovery_is_possible(self):
        output = run()["results"]["contract"]["cases"]
        lookup = {r["id"]: r for r in output}
        self.assertEqual(lookup["H10"]["event"], "invocation_revoked")
        self.assertTrue(lookup["H11"]["correct_answer"])

    def test_policy_has_no_access_to_expected_answers(self):
        result = run()
        for item in self.items:
            if item["split"] == "heldout":
                inputs = {k: v for k, v in item.items() if k != "expected"}
                for policy in self.config["policies"]:
                    execute(inputs, policy, result["frozen"])

    def test_ablation_exposes_each_boundary(self):
        results = run()["results"]
        self.assertEqual(results["contract"]["metrics"]["wrong_accepted_answers"], 0)
        for check in ("availability", "unit", "period"):
            self.assertGreater(results["contract_no_" + check]["metrics"]["wrong_accepted_answers"], 0)

    def test_abstentions_do_not_inflate_answer_accuracy(self):
        results = run()["results"]
        contract = results["contract"]["metrics"]
        self.assertEqual(contract["correct_answers"], 6)
        self.assertEqual(contract["safe_abstentions"], 7)
        self.assertEqual(contract["unnecessary_abstentions"], 1)
        self.assertEqual(contract["correct_answer_rate"], 6 / 14)
        self.assertEqual(contract["coverage_conditioned_accuracy"], 1)
        oracle = results["from_scratch_metadata_solver"]["metrics"]
        self.assertEqual(oracle["correct_answers"], 7)
        self.assertEqual(oracle["wrong_accepted_answers"], 0)

    def test_reproducible_run(self):
        self.assertEqual(run(), run())


if __name__ == "__main__":
    unittest.main()
