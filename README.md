# Financial Workflow Evolution

One focused research question: how should an evolving financial research agent evaluate a workflow update when tasks are clustered by company, sector, or market regime?

## One contribution
A cluster-aware paired promotion gate for SEA-style workflow evolution. Candidate–baseline differences are computed on matched tasks and aggregated at the independent task-cluster level.

This is an application of established clustered-inference principles, not a claim to invent cluster-robust statistics or self-evolving agents.

## Status
- Methodological Monte Carlo simulation completed.
- No live LLM-agent experiment has been run.
- No real U.S.-equity market backtest has been run.
- Results are synthetic; they do not establish financial performance.
- SEA source code was inspected; its runtime has not yet been integrated into this experiment.

## Reproduce
Python 3.10+, NumPy and SciPy:
python experiments/simulate_cluster_gate.py --reps 20000 --clusters 12 --tasks-per-cluster 5 --out experiments/results.json
python -m unittest discover -s experiments -v

## Limitation
The cluster-mean t-test is a transparent baseline, not a universally optimal estimator. With few clusters it loses power. Future work should compare small-sample cluster-robust methods or wild-cluster bootstrap under pre-registered assumptions.
