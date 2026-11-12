# Research Plan

## Working title

**When Should Financial Research Agents Accept Their Own Revisions? Cluster-Aware and Search-Aware Evaluation for Self-Evolving Workflows**

## Recommendation

Do not write another paper claiming that an LLM trading agent achieves high returns. The existing Paper repository already has a defensible methodological starting point: it studies when an evolving financial workflow has enough evidence to promote a revision. The strongest publishable direction is to turn this into an **evaluation protocol for self-evolving financial research agents**, not an investment-performance claim.

## Central question

When a financial research workflow proposes many adaptive revisions and evaluates them on related tasks, how can a promotion gate distinguish genuine improvement from correlated noise and repeated validation-set selection?

## Proposed contribution

A versioned promotion protocol with four explicit controls:

1. **Paired comparison**: candidate and predecessor run on the same task.
2. **Cluster-aware inference**: company, sector, and market-regime clusters are registered before evaluation; uncertainty is estimated over independent clusters rather than raw task rows.
3. **Search-aware correction**: every evaluated candidate, including rejected candidates, is recorded in a trial ledger. For report-quality scores, use fresh evaluation clusters and a pre-registered sequential error budget with conditionally valid tests; logging alone does not correct adaptive reuse. DSR/PBO apply only to an optional return-series experiment and are not substitutes for this guarantee.
4. **Sealed-test governance**: the test set is never used to select or revise a workflow; deployment performance is reported only for the validation-selected checkpoint.

The paper's novelty claim must remain narrow: this is an evaluation and governance protocol for evidence-gated evolution. It does not claim to invent self-evolving agents, paired validation, clustered inference, or deflated Sharpe ratios.

## Hypotheses

- H1: Treating clustered task outcomes as independent inflates false promotions as intracluster correlation increases.
- H2: A cluster-aware gate controls false promotions more effectively, but loses power when the number of independent clusters is small.
- H3: Repeated adaptive candidate search causes naive validation selection to overestimate improvement; a complete trial ledger and search-aware correction reduce this optimism.
- H4: Combining cluster-aware inference with sealed-test governance is safer than either control alone.

## Minimum experiments

### E1: Cluster calibration

Use the existing random-intercept Monte Carlo design, but extend it with unequal cluster sizes, heavy-tailed noise, and crossed company/sector-regime dependence. Compare task-level t-test, cluster-mean test, CR2 small-sample inference, and wild-cluster bootstrap. Report type-I error, power, confidence-interval coverage, and false-promotion rate.

### E2: Adaptive search simulation

Generate a fixed set of candidate revisions with heterogeneous true effects. Let an evolution loop repeatedly select, evaluate, and retain candidates using the validation set. Vary the number of trials, validation reuse, and candidate correlation. Compare naive best-validation selection with ledger-aware search correction and a sealed test. Report selection optimism and test degradation.

### E3: Protocol ablation

Evaluate four gates: naive task-level; cluster-aware only; search-aware only; combined protocol. Keep the data-generating process and candidate budget fixed. The primary result should be a calibration/power/optimism trade-off, not a return headline.

### E4: Optional real-agent pilot

Only after the statistical protocol is stable, connect SEA or a small deterministic financial research workflow. Use reproducible report-quality tasks, not live trading. Register task clusters, freeze the evaluator, and publish every candidate and rejection. This pilot is necessary for a stronger submission but is not allowed to be presented as completed until actually run.

## Evaluation contract

- All task definitions, cluster IDs, evaluator version, and candidate budgets are pre-registered.
- Candidate and predecessor use identical task inputs and execution budgets.
- All attempted candidates are logged, including invalid and rejected candidates.
- The test set is read-only and cannot feed diagnosis, prompt editing, or checkpoint selection.
- Results are reported for the validation-selected endpoint, not the best test checkpoint.
- Financial quantities are reported with explicit gross/net cost assumptions; no investment recommendation is implied.

## Claim discipline

### Supported now

The repository contains a synthetic cluster-aware paired-evaluation simulation and an English methodological draft. The current simulation supports only the random-intercept calibration result already reported in `paper/MAIN.md`.

### Not supported now

No live LLM-agent experiment, real financial report benchmark, historical portfolio backtest, or end-to-end SEA runtime integration has been completed. No empirical claim about investment performance may be added.

## Target positioning

The paper is best positioned as a reproducible methodology / evaluation paper for workshops in machine learning, agents, computational finance, or trustworthy AI. A full conference paper requires E2 and E3 at minimum; a stronger journal submission also needs E4 and direct comparison against the closest evolution systems.

## Key related work to verify in the final bibliography

- EMAS, arXiv:2608.07196: evidence-guided workflow evolution and paired validation; closest systems precedent.
- EvolveTrade, arXiv:2609.17632: experience-driven prompt-policy refinement for LLM trading agents.
- SHARP, arXiv:2605.06822: bounded, auditable rubric evolution with attribution and walk-forward validation.
- EvoTS-Agent, arXiv:2608.17933: validation-guided self-evolution for financial time-series change-point detection.
- Cameron & Miller (2015): cluster-robust inference.
- Bailey & López de Prado (2014): deflated Sharpe ratio.

All citations and numerical claims must be checked against primary sources before submission.

## Evidence note from initial primary-source checks

- The EMAS text explicitly uses a fixed Validation set repeatedly and acknowledges adaptive-selection risk; it also says empirical Validation rules do not guarantee improvement on held-out Test tasks. Its described acceptance rules compare total correct answers and token counts, not a stated multiplicity-adjusted statistical test. This motivates studying search-aware promotion, but does not establish that every possible implementation lacks other safeguards.
- EMAS groups traces by a structured diagnostic key and requires recurrence across distinct samples. Its limitations note that the key can merge traces with distinct causes. Do not conflate this evidence aggregation with statistical clustering by company, sector, or market regime.
- EvolveTrade revises prompts from decision traces and realized returns; SHARP constrains updates to auditable rubric edits with attribution and walk-forward validation; EvoTS-Agent evolves financial time-series change-point detection trajectories using validation feedback. These are close precedents. The paper's defensible gap is the statistical reliability of repeated promotion under correlated validation units, not self-evolution itself.
- The initial check is based on public primary-source pages/abstracts and the provided EMAS text; full citation, method, and implementation audits remain necessary.
