#!/usr/bin/env python3
"""Vectorized Monte Carlo study of cluster-aware paired evaluation."""
import argparse, json
from pathlib import Path
import numpy as np
from scipy.stats import t

def run(reps=20000, clusters=12, tasks_per_cluster=5,
        rhos=(0.0, 0.2, 0.5, 0.8), effects=(0.0, 0.2, 0.4),
        seed=20261105):
    rng = np.random.default_rng(seed)
    rows = []
    n = clusters * tasks_per_cluster
    for rho in rhos:
        for effect in effects:
            u = rng.normal(0, np.sqrt(rho), (reps, clusters, 1))
            e = rng.normal(0, np.sqrt(1-rho),
                           (reps, clusters, tasks_per_cluster))
            d = effect + u + e
            flat = d.reshape(reps, n)
            stat = flat.mean(axis=1) / (flat.std(axis=1, ddof=1) / np.sqrt(n))
            p_naive = t.sf(stat, n-1)
            cm = d.mean(axis=2)
            stat_c = cm.mean(axis=1) / (cm.std(axis=1, ddof=1) / np.sqrt(clusters))
            p_cluster = t.sf(stat_c, clusters-1)
            rows.append({
                "rho": rho, "effect_sd": effect, "clusters": clusters,
                "tasks_per_cluster": tasks_per_cluster, "total_tasks": n,
                "replications": reps,
                "naive_task_level_rejection_rate": float(np.mean(p_naive < .05)),
                "cluster_mean_rejection_rate": float(np.mean(p_cluster < .05)),
                "nominal_alpha": .05
            })
    return {"seed": seed, "model": "random-intercept paired-difference model",
            "formula": "d_ci = effect + u_c + epsilon_ci; ICC=rho",
            "sampling_unit": "independent task cluster", "rows": rows}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--reps", type=int, default=20000)
    p.add_argument("--clusters", type=int, default=12)
    p.add_argument("--tasks-per-cluster", type=int, default=5)
    p.add_argument("--seed", type=int, default=20261105)
    p.add_argument("--out", default="results.json")
    a = p.parse_args()
    result = run(a.reps, a.clusters, a.tasks_per_cluster, seed=a.seed)
    Path(a.out).write_text(json.dumps(result, indent=2))
    for r in result["rows"]:
        print("rho={:.1f} effect={:.1f} naive={:.3f} cluster={:.3f}".format(
            r["rho"], r["effect_sd"],
            r["naive_task_level_rejection_rate"],
            r["cluster_mean_rejection_rate"]))
