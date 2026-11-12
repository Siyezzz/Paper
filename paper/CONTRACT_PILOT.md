# Iteration 9: Financial Skill Applicability under Contract Changes

**Date:** 2026-11-12. **Status:** executable evaluator pilot, not submission-ready. This English supplement extends, rather than replaces, `PAPER_DRAFT.md` and the cluster-calibration study in `paper/MAIN.md`.

## Abstract

A financial skill can pass admission checks yet become inapplicable when input publication availability, units, or reporting periods change. We isolate this failure using a deterministic growth-calculation skill and explicitly constructed financial-semantic fixtures. A chronological fixture split contains three discovery, three validation, and fourteen evaluation cases. Seven fixed policies compare unconditional reuse, validation-only admission, invocation-level contract checks, three contract ablations, and a metadata-aware from-scratch solver. On the fourteen cases, unconditional and validation-only reuse each produce six correct answers, seven wrong accepted answers, and one abstention. Contract checks retain six correct answers and eliminate wrong accepted answers, but abstain eight times, including one unnecessary abstention on a safely convertible scale change. The ordinary metadata-aware solver returns seven correct answers without wrong acceptance. Thus the pilot verifies an auditable failure detector but supplies no evidence that skill evolution outperforms ordinary validation. All values, dates and policies are constructed; no real LLM experiment or observed financial-data study is claimed.

## 1. Research question and relation to prior work

The provisional question is: when should a previously admitted financial skill be prevented from executing, and when can it transfer safely to a different data contract? Skill admission is distinct from invocation applicability. A passed validation collection cannot establish that every later input satisfies the skill's preconditions.

Dream-RSI evolves exploration policies using historical discovery replay [1]. RRSI already regularizes harness edits, candidate selection, costs and component pruning [2]. FactorMiner already combines executable financial skills, memory, deterministic evaluation and factor admission/replacement [3]. SkillsBench already measures matched skill/no-skill efficacy using deterministic checks [4]. Consequently, generic evolution, admission, cost control, pruning, migration and paired scoring are not adequate novelty claims.

Our potential contribution is a task-based study of financial semantic invalidation with traceable rejection and safe-transfer evidence, not a new theory of contracts or inference. The current fixtures merely establish that a proposed evaluator can express the distinction. The audit in `docs/NOVELTY_AUDIT_2026-11-12.md` specifies version and retrieval boundaries. No exhaustive priority claim is made.

## 2. Frozen deterministic protocol

The skill computes `(current/base - 1) * 100` using Decimal arithmetic at precision 50. Admission requires three correct validation examples and valid metadata. Configuration and policy hashes are recorded before evaluation execution. Policies receive input metadata but not expected answers. The executable split dates are discovery through 2023, validation through 2024, and evaluation decisions in 2025; these are test-fixture dates, not claimed historical experiment dates.

Runtime checks cover publication availability relative to the decision, matching unit/currency, year-on-year period alignment and convention, matching metric, and nonzero denominator. A rejected invocation does not permanently delete a skill: a subsequent compatible input may execute it. The current contract is conservative about unequal scales; a separate ordinary solver normalizes known scales of the same currency. No FX conversion, restatement reconciliation, leap-day alignment or intraday availability model is implemented.

The evaluation set includes consistent same-scale transfer, matched fiscal-year transfer, declines, mismatched scales/currencies, quarter-versus-year comparison, accounting-convention changes, unavailable publications, metric mismatch, zero base and an input published after policy freeze but before its decision. This last case separates prohibited training leakage from legitimate later task inputs.

**Holdout limitation:** all policies and cases were authored within this study, and the fixture source is visible. Hashing and split checks establish execution separation, not independent authorship or a blind, externally sampled holdout. These fourteen cases are not statistical independent replications. No confidence interval or population-level superiority claim is inferred.

## 3. Results

Metrics below are generated from `experiments/artifacts/financial_contract_results.json`. Correct answers exclude abstentions; conditional accuracy is correct answers divided by accepted answers. A wrong answer includes answering a case whose stipulated valid response is abstention.

| Policy | Correct / 14 | Wrong accepted | Abstentions | Unnecessary abstentions | Coverage | Accuracy conditional on answering |
|---|---:|---:|---:|---:|---:|---:|
| Naive frozen | 6 | 7 | 1 | 0 | 92.86% | 46.15% |
| Validation-only | 6 | 7 | 1 | 0 | 92.86% | 46.15% |
| Contract | 6 | 0 | 8 | 1 | 42.86% | 100% |
| From-scratch metadata solver | 7 | 0 | 7 | 0 | 50.00% | 100% |
| No availability check | 6 | 2 | 6 | 1 | 57.14% | 75.00% |
| No unit check | 6 | 2 | 6 | 0 | 57.14% | 75.00% |
| No period check | 6 | 2 | 6 | 1 | 57.14% | 75.00% |

The full contract produces seven safe abstentions and one unnecessary abstention. Reporting only its 100% conditional accuracy would conceal its limited coverage. Each ablation exposes two specified wrong acceptances. These are designed checks, not empirical estimates of financial failure prevalence.

**Negative result:** the ordinary solver is strictly more useful than the conservative skill contract on the convertible-scale fixture while matching its zero wrong acceptance. The present result therefore supports ordinary metadata validation, not an advantage from self-evolution. No latency or monetary savings were measured. A learnable skill-generation loop is still absent.

## 4. Reproduction and evidence

Run from the repository root:

```bash
python experiments/simulate_cluster_gate.py --reps 20000 --clusters 12 --tasks-per-cluster 5 --seed 20261105 --out experiments/artifacts/baseline_reproduction.json
python experiments/financial_contract_pilot.py --out experiments/artifacts/financial_contract_results.json
python -m unittest discover -s experiments -v
```

The original Monte Carlo study reproduces to the published three-decimal values: at ICC 0.8 under the null, naive rejection is 0.212 and cluster-mean rejection 0.048. This remains a Gaussian simulation, not financial evidence. The new pilot retains fixtures, fixed config, source hashes, versions and per-case answers/rejection reasons. Initial implementation failures and fixture corrections must be disclosed in the artifact notes, not interpreted as policy optimization against a blind test.

## 5. Next falsification gate and submission readiness

The practical next experiment needs dated public financial source snapshots and independently authored answers. Freeze skill-generation prompts, model versions, budgets, source cutoffs, candidate count and scoring before an untouched evaluation. Compare no-skill model execution, static curated skills, generated skills without contracts, generated skills with contracts, and ordinary validators. Preserve model responses and all rejected candidates; measure generation plus execution cost rather than claiming that calls are free. Test revocation/recovery and safe scale/period transfer separately. More abstention alone is not evidence of higher utility.

The sequential confirmation design in `PAPER_DRAFT.md` remains untested. Additional priorities are equal-budget sequential-search simulation, small-sample inference comparisons and complete related-work implementation audits. Until then, a methodology/evaluation workshop is only a plausible venue category; no open deadline, acceptance or full-paper readiness is claimed. Actual platform spend is unknown. USD 10/day is a research target, not a measured expense.

## References independently rechecked in this iteration

[1] Tong Zheng et al. Dream-RSI: Recursive Self-Improvement through Evolving Worlds. arXiv:2609.14858v2. https://arxiv.org/abs/2609.14858v2 (abstract verified; full HTML retrieval failed).

[2] Peng Xia et al. RRSI: Regularized Recursive Self-Improvement of Agent Harnesses. arXiv:2609.24972v3. https://arxiv.org/abs/2609.24972v3 (abstract and truncated HTML extraction inspected).

[3] Yanlong Wang et al. FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery. arXiv:2602.14670v2. https://arxiv.org/abs/2602.14670v2 (abstract and truncated HTML extraction inspected).

[4] Xiangyi Li et al. SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks. arXiv:2602.12670v4. https://arxiv.org/abs/2602.12670v4 (abstract and truncated HTML extraction inspected).
