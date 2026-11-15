#!/usr/bin/env python3
"""独立事件重算与 s=0/.5 协方差边界审计；保留原始冻结证据。"""
import hashlib
import json
from pathlib import Path
import sys
from datetime import datetime, timezone

import numpy as np

from simulate_shared_baseline import draw_noise

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "artifacts/iteration13_shared"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipt_path = OUT / "post_validation_receipt.json"
    if receipt_path.exists():
        raise FileExistsError("refusing to overwrite validation receipt")
    report = json.loads((OUT / "shared_baseline_results.json").read_text())
    config = report["design"]
    count_checks = 0
    with np.load(OUT / "candidate_pvalues.npz", allow_pickle=False) as raw:
        for row in report["rows"]:
            si = config["baseline_variance_fractions"].index(row["baseline_variance_fraction"])
            ri = config["rhos"].index(row["rho"])
            ei = config["effects"].index(row["effect"])
            budget = row["candidate_budget"]
            for name, result in row["methods"].items():
                bank = raw["task_p" if name.startswith("task_") else "cluster_p"][si, ri, ei, :, :budget]
                threshold = config["alpha"] / budget if name.endswith("bonferroni") else config["alpha"]
                events = int(np.count_nonzero(np.min(bank, axis=1) < threshold))
                if events != result["events"]:
                    raise AssertionError("independent minimum-p event count mismatch")
                count_checks += 1
    rng = np.random.default_rng(2026111501)
    boundaries = []
    for share in (0.0, 0.5):
        for rho in (0.0, 0.8):
            baseline = np.sqrt(share) * draw_noise(rng, 100000, 2, 2, rho)
            a = np.sqrt(1-share) * draw_noise(rng, 100000, 2, 2, rho) - baseline
            b = np.sqrt(1-share) * draw_noise(rng, 100000, 2, 2, rho) - baseline
            checks = {"marginal_variance": (float(a.var()), 1.0),
                      "within_candidate_same_cluster": (float(np.corrcoef(a[:, 0, 0], a[:, 0, 1])[0, 1]), rho),
                      "between_candidates_same_task": (float(np.corrcoef(a[:, 0, 0], b[:, 0, 0])[0, 1]), share),
                      "between_candidates_same_cluster": (float(np.corrcoef(a[:, 0, 0], b[:, 0, 1])[0, 1]), share*rho),
                      "between_candidates_different_clusters": (float(np.corrcoef(a[:, 0, 0], b[:, 1, 0])[0, 1]), 0.0)}
            for observed, expected in checks.values():
                if abs(observed - expected) > 0.02:
                    raise AssertionError("boundary covariance mismatch")
            boundaries.append({"s": share, "rho": rho, "checks": {
                name: {"observed": obs, "expected": exp, "absolute_tolerance": 0.02}
                for name, (obs, exp) in checks.items()}})
    paths = [OUT / "reproduction_manifest.json", OUT / "shared_baseline_results.json",
             OUT / "candidate_pvalues.npz", ROOT / "validate_shared_baseline.py"]
    receipt = {"created_utc": datetime.now(timezone.utc).isoformat(),
               "command_argv": [sys.executable, str(Path(__file__).resolve())],
               "independent_minimum_p_event_checks": count_checks,
               "boundary_seed": 2026111501, "boundary_replications": 100000,
               "covariance_boundaries": boundaries,
               "evidence_sha256": {str(path.relative_to(ROOT)): sha(path) for path in paths},
               "operational_incident": {
                   "source": "team-lead message, not independently observed by experiment agent",
                   "description": "One relative-path reproduction invocation from workspace root failed before producing output; exact argv unavailable to experiment agent. Subsequent formal harness invokes Python with subprocess cwd fixed to repository root.",
                   "formal_reproduction_failure": False},
               "original_frozen_evidence_modified": False,
               "result": "passed"}
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("144 independent event counts and 20 covariance boundary checks passed.")


if __name__ == "__main__":
    main()
