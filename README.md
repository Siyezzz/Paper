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
- No successful, scorable live LLM-agent experiment has been run. The inherited API attempt produced only access/transport failures; see `docs/API_PILOT_AUDIT_2026-11-13.md`.
- A one-company, source-grounded deterministic arithmetic micro-pilot now exists; see `paper/SOURCE_GROUNDED_PILOT.md`. Its decision dates and scale-change scenarios are constructed, not observed market changes.
- No real U.S.-equity backtest has been run.
- Gaussian results are simulated; the contract fixtures are constructed; the source-grounded micro-pilot combines observed revenue with constructed scenarios. None establishes financial performance.
- SEA source code has been inspected; its runtime is not yet integrated.
- Iteration 12 adds a fixed independent all-null candidate-bank experiment with five matched inference/search controls, complete p-value banks and pointwise Monte Carlo intervals; see `paper/MAIN.md` Section 5.6 and `experiments/artifacts/iteration12_search/`. It does not test adaptive validation reuse, positive-effect power or real model-generated skills.
- The latest related-work recheck and its processed-text inspection limits are in `docs/NOVELTY_AUDIT_2026-11-14.md`.
- Current paper is a methodological pilot, not submission-ready.
- Iteration 9 independently rechecks Dream-RSI, RRSI, FactorMiner and SkillsBench against current primary pages; see `docs/NOVELTY_AUDIT_2026-11-12.md` for versions and inspection limits.
- A constructed deterministic financial skill-contract pilot has been executed; see `paper/CONTRACT_PILOT.md`. Its policies are hand-written, its dates and financial values are test fixtures, and it must not be described as real LLM or observed financial evidence. The ordinary metadata solver outperforms the conservative contract on one convertible-scale case.

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
