"""共享基线模型、端点和多重阈值的离线回归测试。"""
import copy
import json
from pathlib import Path
import unittest

import numpy as np
from scipy.stats import ttest_1samp

from simulate_null_search import paired_pvalues
from simulate_shared_baseline import draw_noise, generate, summarize


class SharedBaselineTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((Path(__file__).parent / "shared_baseline_config.json").read_text())
        self.config.update(replications=200, clusters=6, tasks_per_cluster=4,
                           rhos=[0, 0.8], candidate_budgets=[1, 3])

    def test_reproducible_generation_and_positive_shift(self):
        first = generate(self.config)
        second = generate(self.config)
        for a, b in zip(first, second):
            np.testing.assert_array_equal(a, b)
            self.assertTrue(np.all(a[:, :, 1] <= a[:, :, 0]))

    def test_t_statistics_match_independent_scipy_reference(self):
        data = np.random.default_rng(123).normal(size=(11, 6, 4))
        task, cluster = paired_pvalues(data)
        np.testing.assert_allclose(task, ttest_1samp(data.reshape(11, 24), 0, axis=1, alternative="greater").pvalue)
        np.testing.assert_allclose(cluster, ttest_1samp(data.mean(axis=2), 0, axis=1, alternative="greater").pvalue)

    def test_noise_covariance_matches_shared_baseline_structure(self):
        rng = np.random.default_rng(22)
        reps, share, rho = 100000, 0.5, 0.8
        baseline = np.sqrt(share) * draw_noise(rng, reps, 2, 2, rho)
        a = np.sqrt(1-share) * draw_noise(rng, reps, 2, 2, rho) - baseline
        b = np.sqrt(1-share) * draw_noise(rng, reps, 2, 2, rho) - baseline
        self.assertAlmostEqual(float(a.var()), 1, delta=0.02)
        for x, y, expected in [(a[:, 0, 0], a[:, 0, 1], rho),
                               (a[:, 0, 0], b[:, 0, 0], share),
                               (a[:, 0, 0], b[:, 0, 1], share*rho),
                               (a[:, 0, 0], b[:, 1, 0], 0)]:
            self.assertAlmostEqual(float(np.corrcoef(x, y)[0, 1]), expected, delta=0.015)

    def test_endpoint_labels_and_threshold_counts(self):
        config = copy.deepcopy(self.config)
        config.update(replications=2, rhos=[0], baseline_variance_fractions=[0.5], candidate_budgets=[1, 3])
        bank = np.array([[[[[0.01, 0.03, 0.1], [0.02, 0.2, 0.2]],
                            [[0.001, 0.03, 0.1], [0.01, 0.2, 0.2]]]]])
        rows = summarize(config, bank, bank)["rows"]
        self.assertEqual(rows[0]["endpoint"], "familywise_false_promotion")
        self.assertEqual(rows[2]["endpoint"], "any_true_promotion_power")
        self.assertEqual(rows[1]["methods"]["cluster_unadjusted"]["events"], 2)
        self.assertEqual(rows[1]["methods"]["cluster_bonferroni"]["events"], 1)
        self.assertEqual(rows[3]["methods"]["cluster_bonferroni"]["events"], 2)
        self.assertNotIn("independent_cluster_exact_fwer", rows[0])

    def test_bonferroni_subset_and_single_candidate_equivalence(self):
        report = summarize(self.config, *generate(self.config))
        for row in report["rows"]:
            methods = row["methods"]
            for unit in ("task", "cluster"):
                plain = methods[unit + "_unadjusted"]["events"]
                corrected = methods[unit + "_bonferroni"]["events"]
                self.assertLessEqual(corrected, plain)
                if row["candidate_budget"] == 1:
                    self.assertEqual(corrected, plain)

    def test_invalid_design_rejected_before_generation(self):
        for key, bad in [("effects", [0, -0.1]), ("effects", [0]), ("rhos", [1]),
                         ("baseline_variance_fractions", [-0.1]), ("clusters", 1),
                         ("candidate_budgets", [0]), ("alpha", 0)]:
            config = copy.deepcopy(self.config)
            config[key] = bad
            with self.assertRaises(ValueError):
                generate(config)

    def test_invalid_bank_rejected(self):
        task, cluster = generate(self.config)
        with self.assertRaises(ValueError):
            summarize(self.config, task[..., :-1], cluster)
        task.flat[0] = np.nan
        with self.assertRaises(ValueError):
            summarize(self.config, task, cluster)


if __name__ == "__main__":
    unittest.main()
