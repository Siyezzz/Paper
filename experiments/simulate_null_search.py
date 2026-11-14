#!/usr/bin/env python3
"""固定独立全零候选库的多重搜索模拟；不调用模型或外部服务。"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import norm, t

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "null_search_config.json"


def paired_pvalues(differences):
    reps, clusters, tasks = differences.shape
    flat = differences.reshape(reps, clusters * tasks)
    means = differences.mean(axis=2)
    naive_stat = flat.mean(axis=1) / (flat.std(axis=1, ddof=1) / np.sqrt(clusters * tasks))
    cluster_stat = means.mean(axis=1) / (means.std(axis=1, ddof=1) / np.sqrt(clusters))
    return t.sf(naive_stat, clusters * tasks - 1), t.sf(cluster_stat, clusters - 1)


def generate(config):
    if config["effect"] != 0:
        raise ValueError("this experiment implements only the all-null design")
    rng = np.random.default_rng(config["seed"])
    reps, clusters, tasks = (config[k] for k in ("replications", "clusters", "tasks_per_cluster"))
    budget = max(config["candidate_budgets"])
    task_p = np.empty((len(config["rhos"]), reps, budget))
    cluster_p = np.empty_like(task_p)
    for i, rho in enumerate(config["rhos"]):
        for candidate in range(budget):
            intercept = rng.normal(0, np.sqrt(rho), (reps, clusters, 1))
            residual = rng.normal(0, np.sqrt(1 - rho), (reps, clusters, tasks))
            task_p[i, :, candidate], cluster_p[i, :, candidate] = paired_pvalues(intercept + residual)
    return task_p, cluster_p


def interval(successes, total):
    rate = successes / total
    z = norm.ppf(0.975)
    denominator = 1 + z * z / total
    center = (rate + z * z / (2 * total)) / denominator
    radius = z * np.sqrt(rate * (1 - rate) / total + z * z / (4 * total * total)) / denominator
    return {"false_promotions": int(successes), "replications": total, "rate": rate,
            "monte_carlo_se": float(np.sqrt(rate * (1 - rate) / total)),
            "pointwise_wilson_95_ci": [float(center - radius), float(center + radius)]}


def summarize(config, task_p, cluster_p):
    expected_shape = (len(config["rhos"]), config["replications"], max(config["candidate_budgets"]))
    for bank in (task_p, cluster_p):
        if bank.shape != expected_shape or not np.isfinite(bank).all() or ((bank < 0) | (bank > 1)).any():
            raise ValueError("invalid p-value bank")
    rows = []
    alpha = config["alpha"]
    for i, rho in enumerate(config["rhos"]):
        for budget in config["candidate_budgets"]:
            task = task_p[i, :, :budget]
            cluster = cluster_p[i, :, :budget]
            ranks = np.arange(1, budget + 1)
            spending = alpha / (ranks * (ranks + 1))
            masks = {
                "task_unadjusted": (task < alpha).any(axis=1),
                "cluster_unadjusted": (cluster < alpha).any(axis=1),
                "task_bonferroni": (task < alpha / budget).any(axis=1),
                "cluster_bonferroni": (cluster < alpha / budget).any(axis=1),
                "cluster_alpha_spending": (cluster < spending).any(axis=1),
            }
            rows.append({"rho": rho, "candidate_budget": budget,
                         "cluster_unadjusted_exact_fwer": 1 - (1 - alpha) ** budget,
                         "cluster_bonferroni_exact_fwer": 1 - (1 - alpha / budget) ** budget,
                         "cluster_alpha_spending_exact_fwer": float(1 - np.prod(1 - spending)),
                         "spending_total_alpha": float(spending.sum()),
                         "methods": {name: interval(int(mask.sum()), len(mask)) for name, mask in masks.items()}})
    return {"design": config, "raw_axes": ["rho", "replication", "candidate"],
            "null_model": "d[r,c,i] = u[r,c] + e[r,c,i], Var(u)=rho, Var(e)=1-rho; candidates independent",
            "selection": "any one-sided p strictly below its pre-fixed threshold in the first K candidates",
            "rows": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    raw_config = args.config.read_bytes()
    config = json.loads(raw_config)
    if config["effect"] != 0:
        raise ValueError("this experiment implements only the all-null design")
    raw_path = args.out_dir / "candidate_pvalues.npz"
    result_path = args.out_dir / "null_search_results.json"
    if not args.verify_only:
        if raw_path.exists() or result_path.exists():
            raise FileExistsError("refusing to overwrite existing experiment evidence")
        task_p, cluster_p = generate(config)
        np.savez_compressed(raw_path, task_p=task_p, cluster_p=cluster_p)
    with np.load(raw_path, allow_pickle=False) as bank:
        report = summarize(config, bank["task_p"], bank["cluster_p"])
    report["config_sha256"] = hashlib.sha256(raw_config).hexdigest()
    report["raw_pvalues_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    if args.verify_only:
        if json.loads(result_path.read_text(encoding="utf-8")) != report:
            raise AssertionError("stored report differs from raw p-value recomputation")
        print("Stored p-values exactly reproduce the complete report.")
    else:
        result_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report["rows"], indent=2))


if __name__ == "__main__":
    main()
