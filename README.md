# Financial Workflow Evolution

## Research question

How should paired evidence for an evolving financial research workflow be evaluated when tasks are clustered by company, sector, or market regime?

## One proposed contribution

A **cluster-aware paired promotion gate** for financial-agent workflow evolution. Candidate and baseline are run on the same tasks; paired differences are aggregated using the pre-registered task-cluster structure before a workflow revision is promoted.

This adapts established clustered-inference ideas to an EMAS/SEA-style workflow-evolution setting. It does not claim to invent self-evolving agents, paired validation, recurrence gating, or cluster-robust inference.

## Essential related work

- **EMAS** (Fei et al., 2026), arXiv:2608.07196: closest system-level evolution precedent; co-authored by Prof. Yanghua Xiao. Read the full paper and official implementation before making novelty claims.
- **GEPA** (Agrawal et al., ICLR 2026): reflective prompt evolution and Pareto-aware candidate search.
- **EvoTS-Agent** (2026): validation-guided evolution for financial time-series workflows.
- **Steward** (2026 preprint): governed self-evolution for U.S.-equity investing.
- **Cameron & Miller (2015)**: cluster-robust inference.

See docs/EMAS_CRITICAL_READING.md, docs/WRITING_PROTOCOL.md, and docs/ITERATION_LEDGER.md.

## Current status

- Methodological Monte Carlo simulation exists.
- No live LLM-agent experiment has been run.
- No real U.S.-equity backtest has been run.
- Results are synthetic and do not establish financial performance.
- SEA source code has been inspected; its runtime is not yet integrated.
- Current paper is a methodological pilot, not submission-ready.

## Reproduce

Python 3.10+, NumPy and SciPy:

```bash
python experiments/simulate_cluster_gate.py --reps 20000 --clusters 12 --tasks-per-cluster 5 --out experiments/results.json
python -m unittest discover -s experiments -v
```

## Writing standard

The manuscript follows a repository-first, claim-ledger workflow based on research-ideation, ml-paper-writing, and paper-self-review skills. EMAS is a structural and methodological reference; its text, figures, code, and results are not copied.

## Iteration policy

The iteration count is recorded in docs/ITERATION_LEDGER.md. Only material research, experiment, analysis, or manuscript changes increment the count.
