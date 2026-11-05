import unittest
from simulate_cluster_gate import run

class ClusterGateTests(unittest.TestCase):
    def test_cluster_method_controls_null_rejection(self):
        result = run(reps=12000, clusters=12, tasks_per_cluster=5,
                     rhos=(0.0, 0.5, 0.8), effects=(0.0,), seed=12345)
        rows = result["rows"]
        for row in rows:
            self.assertLess(abs(row["cluster_mean_rejection_rate"] - 0.05), 0.015)
        self.assertGreater(rows[1]["naive_task_level_rejection_rate"], 0.10)
        self.assertGreater(rows[2]["naive_task_level_rejection_rate"], 0.10)

    def test_power_decreases_as_cluster_correlation_increases(self):
        result = run(reps=12000, clusters=12, tasks_per_cluster=5,
                     rhos=(0.0, 0.5, 0.8), effects=(0.2,), seed=54321)
        power = [r["cluster_mean_rejection_rate"] for r in result["rows"]]
        self.assertGreater(power[0], power[1])
        self.assertGreater(power[1], power[2])

if __name__ == "__main__":
    unittest.main()
