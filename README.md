# Financial Workflow Evolution

## Research question

How should paired evidence for an evolving financial research workflow be evaluated when tasks are clustered by company, sector, or market regime?

## One proposed contribution

A **cluster- and search-aware Gaussian calibration study** for financial-agent workflow promotion. Matched controls compare task/cluster inference and unadjusted/Bonferroni thresholds in independent and shared-baseline fixed candidate banks. The broader fresh-confirmation protocol is a specification with a conditional analytic error bound, not an executed adaptive-evolution result.

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
- Iteration 13 adds frozen shared-baseline Gaussian candidate banks with separate null-error and positive-effect endpoints; see `paper/MAIN.md` Section 5.7 and `experiments/artifacts/iteration13_shared/`. At rho=.8, K=20, s=.5, cluster Bonferroni false promotion is .03760 and any-true-promotion power at effect .2 is .16290. This is not adaptive validation reuse or financial/LLM evidence.
- Iteration 14 adds two source-grounded issuer transfer checks (NVIDIA and Intel) using unchanged handwritten policies; see `paper/ISSUER_TRANSFER_CHECK.md` and `experiments/artifacts/iteration14_financial/`. These are author-designed reported-fiscal-year arithmetic tasks with constructed timing/unit scenarios, not a blind holdout or real LLM experiment. Both the conservative contract and ordinary metadata solver over-abstain on moving week-calendar fiscal endpoints. The earlier ordinary-solver advantage is not a universal cross-convention result.
- The latest related-work recheck and its inspection limits are in `docs/NOVELTY_AUDIT_2026-11-16.md`; SkillsBench already implements structural configuration checks, so generic metadata validation is not a novelty claim.
- Iteration 15 adds a calendar-aware ordinary-validator development control on nine exposed scenarios: 6 correct answers, 0 wrong accepted, 3 safe abstentions; both ablations produce 3 wrong accepted answers. This repairs exposed-case failures without establishing skill evolution or unseen-task performance. See `paper/CALENDAR_VALIDATOR_DEVELOPMENT.md` and `docs/ITERATION15_PRIMARY_RECHECK.md`.
- Iteration 16 freezes the ordinary validator before a new NVIDIA FY2026/FY2025 source-pair check: 2 correct answers, 0 wrong accepted, 1 safe abstention; the availability and unit ablations each admit 1 wrong answer. One previously exposed issuer and three dependent scenarios do not establish generalization or evolving-skill utility. See `paper/FROZEN_SOURCE_VINTAGE_CHECK.md` and `experiments/artifacts/iteration16_vintage/vintage_results.json`.
- The November 17 primary-source audit is `docs/NOVELTY_AUDIT_2026-11-17.md`. FinSkillOps directly overlaps the proposed financial skill lifecycle; admission, regression checks and retirement alone are not a novelty claim.
- Iteration 16 freezes the stronger ordinary baseline before a new NVIDIA FY2026/FY2025 source-year check: 2 correct answers, 0 wrong accepted and 1 safe abstention; each ablation makes 1 wrong accepted answer. This is one new annual pair from an exposed issuer, not independent financial confirmation or generated-skill evidence. See `paper/FROZEN_SOURCE_VINTAGE_CHECK.md`.
- The November 17 primary audit adds FinSkillOps as a direct financial skill-lifecycle precedent, ruling out generic financial admission/scope/retirement as sufficient novelty. See `docs/NOVELTY_AUDIT_2026-11-17.md`.
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
