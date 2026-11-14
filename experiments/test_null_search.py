"""独立标量统计量、手算阈值和解析概率检查。"""
import json
import unittest

import numpy as np
from scipy.stats import ttest_1samp

from simulate_null_search import CONFIG, generate, interval, paired_pvalues, summarize


class NullSearchTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_pvalues_match_independent_scipy_ttest(self):
        data = np.array([[[1., 2.], [3., 6.], [-1., 0.]],
                         [[2., 0.], [-4., -2.], [5., 1.]]])
        task, cluster = paired_pvalues(data)
        for i, sample in enumerate(data):
            self.assertAlmostEqual(task[i], ttest_1samp(sample.flatten(), 0, alternative="greater").pvalue)
            self.assertAlmostEqual(cluster[i], ttest_1samp([sum(row) / len(row) for row in sample], 0, alternative="greater").pvalue)

    def test_thresholds_and_strict_boundary_with_handcrafted_bank(self):
        cfg = {**self.config, "rhos": [0.], "replications": 4, "candidate_budgets": [1, 2]}
        bank = np.array([[[.05, .001], [.03, .04], [.024, .04], [.6, .02]]])
        report = summarize(cfg, bank, bank)
        first, second = [r["methods"] for r in report["rows"]]
        self.assertEqual(first["cluster_unadjusted"]["false_promotions"], 2)
        self.assertEqual(first["cluster_alpha_spending"]["false_promotions"], 1)
        self.assertEqual(second["cluster_unadjusted"]["false_promotions"], 4)
        self.assertEqual(second["cluster_bonferroni"]["false_promotions"], 3)
        self.assertEqual(second["cluster_alpha_spending"]["false_promotions"], 2)

    def test_known_wilson_and_standard_error(self):
        result = interval(5, 100)
        self.assertAlmostEqual(result["monte_carlo_se"], (.05 * .95 / 100) ** .5)
        lo, hi = result["pointwise_wilson_95_ci"]
        self.assertAlmostEqual(lo, .021543679, places=8)
        self.assertAlmostEqual(hi, .11175047, places=8)
        self.assertGreater(interval(0, 100)["pointwise_wilson_95_ci"][1], 0)

    def test_determinism_and_independent_null_probability(self):
        cfg = {**self.config, "rhos": [.5], "replications": 6000, "candidate_budgets": [1, 5]}
        task, cluster = generate(cfg)
        again_task, again_cluster = generate(cfg)
        np.testing.assert_array_equal(task, again_task)
        np.testing.assert_array_equal(cluster, again_cluster)
        for row in summarize(cfg, task, cluster)["rows"]:
            for name in ("cluster_unadjusted", "cluster_bonferroni", "cluster_alpha_spending"):
                p = row[name + "_exact_fwer"]
                se = np.sqrt(p * (1 - p) / cfg["replications"])
                self.assertLess(abs(row["methods"][name]["rate"] - p), 6 * se)

    def test_generate_rejects_nonzero_effect_before_sampling(self):
        for effect in (-0.2, 0.2):
            with self.assertRaisesRegex(ValueError, "all-null"):
                generate({**self.config, "effect": effect})

    def test_invalid_bank_rejected(self):
        cfg = {**self.config, "rhos": [0.], "replications": 1, "candidate_budgets": [1]}
        for value in [np.nan, -0.1, 1.1]:
            with self.assertRaises(ValueError):
                summarize(cfg, np.array([[[value]]]), np.array([[[.5]]]))


if __name__ == "__main__":
    unittest.main()
