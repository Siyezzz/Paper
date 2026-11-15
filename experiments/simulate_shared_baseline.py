#!/usr/bin/env python3
"""固定共享基线 Gaussian 候选库；全零误晋升与全正任一真晋升分开报告。"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import norm

from simulate_null_search import paired_pvalues

ROOT = Path(__file__).resolve().parent


def validate(config):
    for key in ("seed", "replications", "clusters", "tasks_per_cluster"):
        if type(config[key]) is not int or config[key] < (2 if key in ("replications", "clusters") else 1):
            raise ValueError("invalid integer design parameter: " + key)
    for key in ("rhos", "baseline_variance_fractions"):
        if not config[key] or any(not np.isfinite(x) or not 0 <= x < 1 for x in config[key]):
            raise ValueError("invalid correlation grid: " + key)
    if not config["effects"] or any(not np.isfinite(x) or x < 0 for x in config["effects"]):
        raise ValueError("effects must be finite and nonnegative")
    if 0 not in config["effects"] or not any(x > 0 for x in config["effects"]):
        raise ValueError("both all-null and all-positive scenarios are required")
    if not config["candidate_budgets"] or any(type(k) is not int or k < 1 for k in config["candidate_budgets"]):
        raise ValueError("invalid candidate budgets")
    if not np.isfinite(config["alpha"]) or not 0 < config["alpha"] < 1:
        raise ValueError("invalid alpha")


def draw_noise(rng, reps, clusters, tasks, rho):
    return (np.sqrt(rho) * rng.standard_normal((reps, clusters, 1))
            + np.sqrt(1 - rho) * rng.standard_normal((reps, clusters, tasks)))


def generate(config):
    validate(config)
    rng = np.random.default_rng(config["seed"])
    reps, clusters, tasks = (config[k] for k in ("replications", "clusters", "tasks_per_cluster"))
    budget = max(config["candidate_budgets"])
    shape = (len(config["baseline_variance_fractions"]), len(config["rhos"]),
             len(config["effects"]), reps, budget)
    task_p, cluster_p = np.empty(shape), np.empty(shape)
    for si, share in enumerate(config["baseline_variance_fractions"]):
        for ri, rho in enumerate(config["rhos"]):
            baseline = np.sqrt(share) * draw_noise(rng, reps, clusters, tasks, rho)
            for candidate in range(budget):
                noise = np.sqrt(1 - share) * draw_noise(rng, reps, clusters, tasks, rho) - baseline
                for ei, effect in enumerate(config["effects"]):
                    task_p[si, ri, ei, :, candidate], cluster_p[si, ri, ei, :, candidate] = paired_pvalues(noise + effect)
    return task_p, cluster_p


def interval(successes, total):
    rate = successes / total
    z = norm.ppf(0.975)
    denominator = 1 + z * z / total
    center = (rate + z * z / (2 * total)) / denominator
    radius = z * np.sqrt(rate * (1 - rate) / total + z * z / (4 * total * total)) / denominator
    return {"events": int(successes), "replications": int(total), "rate": float(rate),
            "monte_carlo_se": float(np.sqrt(rate * (1 - rate) / total)),
            "pointwise_wilson_95_ci": [float(center - radius), float(center + radius)]}


def summarize(config, task_p, cluster_p):
    validate(config)
    shape = (len(config["baseline_variance_fractions"]), len(config["rhos"]),
             len(config["effects"]), config["replications"], max(config["candidate_budgets"]))
    for bank in (task_p, cluster_p):
        if bank.shape != shape or not np.isfinite(bank).all() or ((bank < 0) | (bank > 1)).any():
            raise ValueError("invalid p-value bank")
    rows = []
    for si, share in enumerate(config["baseline_variance_fractions"]):
        for ri, rho in enumerate(config["rhos"]):
            for ei, effect in enumerate(config["effects"]):
                for budget in config["candidate_budgets"]:
                    task = task_p[si, ri, ei, :, :budget]
                    cluster = cluster_p[si, ri, ei, :, :budget]
                    masks = {
                        "task_unadjusted": (task < config["alpha"]).any(axis=1),
                        "cluster_unadjusted": (cluster < config["alpha"]).any(axis=1),
                        "task_bonferroni": (task < config["alpha"] / budget).any(axis=1),
                        "cluster_bonferroni": (cluster < config["alpha"] / budget).any(axis=1),
                    }
                    row = {"baseline_variance_fraction": share, "rho": rho, "effect": effect,
                           "candidate_budget": budget,
                           "endpoint": "familywise_false_promotion" if effect == 0 else "any_true_promotion_power",
                           "methods": {name: interval(mask.sum(), len(mask)) for name, mask in masks.items()}}
                    if share == 0 and effect == 0:
                        row["independent_cluster_exact_fwer"] = {
                            "cluster_unadjusted": 1 - (1 - config["alpha"]) ** budget,
                            "cluster_bonferroni": 1 - (1 - config["alpha"] / budget) ** budget}
                    rows.append(row)
    return {"design": config,
            "raw_axes": ["baseline_variance_fraction", "rho", "effect", "replication", "candidate"],
            "model": "d[j,r,c,i]=delta+sqrt(1-s)*C[j,r,c,i]-sqrt(s)*B[r,c,i]; C and B are mutually independent unit-variance Gaussian random-intercept fields with ICC rho; B shared across candidates",
            "covariance": {"marginal_variance": 1, "within_candidate_task_correlation": "rho",
                           "between_candidates_same_task_correlation": "s",
                           "between_candidates_same_cluster_different_task_correlation": "s*rho",
                           "different_clusters_correlation": 0},
            "coupling": "Within each (s,rho), identical Gaussian draws are shifted by delta for all effects; K uses nested prefixes. Cells and methods are not independent Monte Carlo comparisons.",
            "scope": "Frozen candidate bank, no adaptation or data-dependent proposals; Gaussian simulation, no financial/LLM observations. All candidates in each cell have the same effect. No mixed-null FWER or selected-candidate precision claim.",
            "selection": "Any one-sided p strictly below alpha (unadjusted) or alpha/K (Bonferroni) among first K candidates.",
            "inference": "Task paired t uses C*m-1 df; cluster-mean paired t uses C-1 df. Cluster t is exact marginally under Gaussian iid clusters; Bonferroni does not require candidate independence.",
            "intervals": "Pointwise 95% Wilson Monte Carlo intervals; not simultaneous confidence intervals or paired method-difference tests.",
            "rows": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "shared_baseline_config.json")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    raw_config = args.config.read_bytes()
    config = json.loads(raw_config)
    validate(config)
    raw_path = args.out_dir / "candidate_pvalues.npz"
    result_path = args.out_dir / "shared_baseline_results.json"
    snapshot = args.out_dir / "frozen_config.json"
    if not args.out_dir.is_dir():
        raise FileNotFoundError("output directory must exist before generation")
    if not args.verify_only:
        if any(path.exists() for path in (raw_path, result_path, snapshot)):
            raise FileExistsError("refusing to overwrite existing evidence")
        snapshot.write_bytes(raw_config)
        task_p, cluster_p = generate(config)
        np.savez_compressed(raw_path, task_p=task_p, cluster_p=cluster_p)
    if snapshot.read_bytes() != raw_config:
        raise AssertionError("configuration differs from frozen snapshot")
    with np.load(raw_path, allow_pickle=False) as bank:
        report = summarize(config, bank["task_p"], bank["cluster_p"])
    report["config_sha256"] = hashlib.sha256(raw_config).hexdigest()
    report["raw_pvalues_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    if args.verify_only:
        if json.loads(result_path.read_text(encoding="utf-8")) != report:
            raise AssertionError("stored report differs from p-value recomputation")
        print("Stored p-values exactly reproduce the complete JSON-value report.")
    else:
        result_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report["rows"], indent=2))


if __name__ == "__main__":
    main()
