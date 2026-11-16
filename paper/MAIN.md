# Cluster- and Search-Aware Gaussian Calibration for Financial Workflow Promotion

## Abstract

Financial workflow revisions may be evaluated on correlated tasks and selected from multiple candidates. We study how sampling-unit inference and candidate multiplicity interact in balanced Gaussian random-intercept simulations. Single-candidate experiments use 12 independent clusters, five tasks per cluster, intracluster correlations up to 0.8 and standardized effects up to 0.4. Fixed-bank extensions compare task/cluster inference with unadjusted/Bonferroni thresholds, including shared baseline noise and separate null and positive-effect endpoints. At intracluster correlation 0.8 with 20 candidates and a shared-baseline variance fraction of 0.5, task-level Bonferroni falsely promotes at least one candidate in 50.52% of replications, versus 3.76% for cluster Bonferroni. The latter detects at least one true improvement of 0.2 with probability 16.29%; increasing its candidate budget from one to 20 lowers detection from 17.84% in this design. These results illustrate the need to assess valid sampling-unit inference and a search-error budget together, while exposing limited power. Gaussian cluster t calibration and Bonferroni control are established results, not new inference theory. The experiments do not evaluate adaptive validation reuse, genuine model-generated skills or financial-agent utility. A separate one-issuer deterministic pilot favors ordinary metadata validation over the conservative skill contract; an external two-issuer check exposes a shared exact-anniversary rule that rejects four answerable week-calendar fiscal comparisons.

**Keywords:** self-evolving agents; financial research; clustered inference; paired evaluation; workflow evolution; SEA.

## 1. Introduction

A financial research agent may be tested on several reports from the same issuer, multiple issuers from one sector, or repeated observations from a single market regime. These tasks provide useful coverage, but they do not necessarily provide independent evidence. Shared accounting conventions, business models, market shocks, data vendors, and evaluation templates can induce correlated outcomes. An evaluation procedure that counts every task as an independent observation can therefore become overconfident about a workflow update.

This issue matters for self-evolving agents. A workflow may be revised after a failure, tested on several related tasks, and promoted when its measured performance exceeds a threshold. If validation tasks share a common source of variation, the apparent number of independent replications is smaller than the raw task count. The system may retain a change that works for one company family or market regime but does not generalize.

This paper addresses one narrow methodological question: **how should paired evidence for a financial-agent workflow update be aggregated when tasks are clustered?** We propose a cluster-aware promotion gate. For each task, the candidate and baseline are evaluated on the same input and the difference in quality is computed. Task-level differences are then averaged within pre-defined clusters. Statistical inference is conducted across cluster means, not across all task rows.

The contribution is deliberately modest. We do not introduce a new self-evolving-agent architecture, a new portfolio optimizer, or a new theory of clustered inference. We adapt a standard random-intercept model and cluster-level inference to a practical promotion decision for financial research workflows. The aim is to make an existing SEA-style evidence gate less likely to confuse repeated, correlated tasks with independent validation.

The executed contribution is a cluster- and search-aware Gaussian calibration study for workflow promotion: matched controls separate sampling-unit inference from candidate-count correction in independent and shared-baseline fixed banks. The broader fresh-confirmation sequential protocol is specified in `PAPER_DRAFT.md`; its conditional error bound is analytic, and its adaptive and financial-agent extensions remain unexecuted.

## 2. Related Work

### 2.1 Self-evolving agents and financial workflows

GEPA studies reflective prompt evolution from execution trajectories and candidate evaluation [1]. EMAS is the closest system-level precedent: it evolves a frozen-model multi-agent workflow through recurring trace-level diagnoses, localized prompt or topology revisions, paired validation against the predecessor, and persistence of accepted versions [2]. EvoTS-Agent applies validation-guided evolution to financial time-series change-point detection [3]. Steward proposes a governed multi-agent investment system with memory, outcome grading, reversible prompt learning, and protected invariants [4]. These works establish that reflective or feedback-driven evolution is already an active research area, including in finance. The present paper does not claim otherwise.

Financial-agent evaluation also increasingly emphasizes verifiable tasks and leakage controls. OpenFinGym provides a multi-task environment for quantitative agents. Our focus is narrower: even if task answers are verifiable, the statistical unit used to compare candidate and baseline workflows still matters when tasks share company, sector, or regime structure.

The additional primary-source recheck on November 16, 2026 (`docs/NOVELTY_AUDIT_2026-11-16.md`) further narrows this positioning. Dream-RSI studies replay-based harness selection; RRSI includes regularized harness revision and acceptance controls; FactorMiner already uses executable financial skills and experience memory. SkillsBench's Appendix C describes `task.md` validation: it distinguishes strict top-level schema validation from metadata vocabulary checks enforced at review time, and requires a nonempty `allowed_hosts` list for allowlist network mode. These task-configuration checks must not be conflated with an implemented `SKILL.md` applicability contract. The independent Iteration 15 recheck (`docs/ITERATION15_PRIMARY_RECHECK.md`) confirms this distinction and rechecks all four supplied arXiv identifiers and linked versions. Its Section 6 proposes, rather than establishes as an implemented benchmark requirement, an explicit skill complexity and applicability contract. Generic metadata checking, skill persistence, admission and cost gates are consequently insufficient contributions. A financial semantic-applicability claim would require a controlled comparison with an ordinary validator on dated financial definitions and reporting conventions; the present deterministic checks do not establish superiority. Returned HTML is truncated and implementations are not audited; unobserved methods cannot be assumed absent.

### 2.2 Clustered inference

The statistical problem is related to clustered data analysis. Observations within a cluster may share latent shocks, making the variance of a task-level mean larger than the independent-observation formula implies. The familiar design-effect expression shows how the effective information content depends on the number of tasks per cluster and the intracluster correlation. Cluster-robust inference and small-sample corrections are well established; this paper does not claim to invent them. It studies a concrete use in the candidate-promotion loop of financial research agents.

### 2.3 Position relative to SEA

The user's SEA repository provides a local experience kernel and an offline candidate-comparison module. Its comparison code consumes externally generated paired evaluation reports; it does not itself execute candidate agents, authenticate evidence, or install successors. The repository documents paired quality-cost differences, retention checks, uncertainty-aware bounds, Pareto preservation, and UCB1 experiment allocation. The current study focuses on a specific limitation that arises before promotion: how to represent dependence among the task outcomes supplied to such a comparison module.

## 3. Problem Formulation

Let candidate workflow version 1 and baseline version 0 be evaluated on the same task i in cluster c. Let q be a pre-defined task-quality score and k a normalized total cost. Define the paired utility difference:

\[
d_{ci}=(q^1_{ci}-q^0_{ci})-\lambda(k^1_{ci}-k^0_{ci}),
\]

where lambda is fixed before evaluation. The Monte Carlo experiment sets lambda to zero and studies quality differences only. Cost can be included in a later multi-objective study.

We model paired differences as:

\[
d_{ci}=\Delta+u_c+\epsilon_{ci},
\]

where Delta is the average candidate effect, u_c is a cluster-level shock with variance sigma_u squared, and epsilon_ci is task-specific noise with variance sigma_epsilon squared. Clusters are independent, and tasks are exchangeable within a cluster for this calibration model.

The intracluster correlation is:

\[
\rho=\frac{\sigma_u^2}{\sigma_u^2+\sigma_\epsilon^2}.
\]

With C clusters and m tasks per cluster, the variance of the overall task mean is:

\[
\operatorname{Var}(\bar d)=\frac{\sigma^2}{Cm}[1+(m-1)\rho],
\]

where sigma squared is the total marginal variance. The term in brackets is the design effect. The corresponding effective sample size is:

\[
n_{\mathrm{eff}}=\frac{Cm}{1+(m-1)\rho}.
\]

This expression illustrates why a dataset with many task rows may contain much less independent information when tasks are strongly clustered.

## 4. Cluster-Aware Promotion Gate

For each cluster, compute the mean paired difference:

\[
\bar d_c=\frac{1}{m_c}\sum_{i=1}^{m_c}d_{ci}.
\]

The estimand is the equal-weight population mean of cluster-average paired differences, Delta = E_c[mean_i d_ci]. Unequal cluster sizes generally make this different from a task-weighted effect. All executed simulations use balanced clusters; no unequal-cluster calibration is claimed. The executed null is H0: Delta <= 0, with promotion margin zero. A simulated positive effect such as 0.2 changes the data-generating mean, not the tested margin. A future practical margin must be fixed separately before confirmation.

The proposed simple gate tests the mean of the independent cluster means:

\[
t_{\mathrm{cluster}}=\frac{\bar d_{\cdot}}{s_{\bar d_c}/\sqrt C}, \qquad df=C-1.
\]

A one-sided promotion decision at level alpha is made only if the corresponding p-value is below alpha, subject to a separately specified retention and safety gate. This paper studies only the clustered quality-difference component; a p-value alone is not sufficient for deployment.

The comparator is a task-level paired t-test that treats all C times m task differences as independent. It quantifies the consequence of ignoring the cluster structure.

Under independent identically distributed Gaussian cluster means with positive variance, the statistic has an exact t distribution with C-1 degrees of freedom at the null boundary for every C >= 2. Few clusters reduce power; they do not invalidate this Gaussian result. Unequal variances, heavy tails, crossed dependence or misspecified clusters require separate justification. A full agent study should compare suitable small-sample cluster-robust methods or a wild-cluster bootstrap, with each method's assumptions stated.

## 5. Monte Carlo Experiment

### 5.1 Data-generating process

We simulate paired workflow utility differences under:

\[
d_{ci}=\Delta+u_c+\epsilon_{ci},
\]

with total marginal variance normalized to one. The cluster shock and task noise are independent zero-mean Gaussian variables with variances rho and 1-rho. The design uses 12 independent clusters and five tasks per cluster (60 task observations). We vary rho in {0, 0.2, 0.5, 0.8} and standardized effects Delta in {0, 0.2, 0.4}. Each condition uses 20,000 Monte Carlo replications with fixed random seed 20261105. The nominal one-sided significance level is 0.05.

When Delta equals zero, the rejection frequency estimates Type-I error. When Delta is positive, it estimates power under the specified data-generating process. Both tests use exactly the same simulated paired differences.

### 5.2 Results

| ICC rho | Effect Delta | Task-level rejection | Cluster-mean rejection |
|---:|---:|---:|---:|
| 0.0 | 0.0 | 0.051 | 0.050 |
| 0.2 | 0.0 | 0.109 | 0.050 |
| 0.5 | 0.0 | 0.170 | 0.049 |
| 0.8 | 0.0 | 0.212 | 0.048 |
| 0.0 | 0.2 | 0.451 | 0.424 |
| 0.2 | 0.2 | 0.473 | 0.294 |
| 0.5 | 0.2 | 0.479 | 0.209 |
| 0.8 | 0.2 | 0.493 | 0.177 |
| 0.0 | 0.4 | 0.925 | 0.896 |
| 0.2 | 0.4 | 0.855 | 0.695 |
| 0.5 | 0.4 | 0.801 | 0.513 |
| 0.8 | 0.4 | 0.766 | 0.406 |

Under the null, the task-level test becomes increasingly anti-conservative as the intracluster correlation rises. At rho 0.8, its rejection rate is 0.212, compared with 0.048 for the cluster-mean test. The cluster-level approach therefore better preserves the nominal error rate in this simulated random-intercept setting.

The correction has a power cost. For a modest standardized effect of 0.2, cluster-mean power falls from 0.424 at zero ICC to 0.177 at ICC 0.8. When within-cluster observations are correlated, the number of independent clusters, rather than the raw number of task rows, limits the available information. A workflow-promotion protocol should therefore report both the estimated effect and its uncertainty, and plan enough independent clusters before testing.

### 5.3 Interpretation

The simulation supports a limited methodological conclusion: **financial-agent workflow evaluation should not treat correlated company-, sector-, or regime-level tasks as independent replications.** A cluster-aware gate can reduce false promotion under the specified dependence model, but it may require substantially more independent clusters to detect modest improvements.

The result does not establish universal calibration. The data-generating process is a Gaussian exchangeable random-intercept model; real financial tasks may have unequal cluster sizes, multiple crossed dependencies, serial correlation, non-normal errors, and changing cluster definitions. Within the stated model, cluster means are i.i.d. Gaussian and the boundary-null t calibration is exact, including six clusters. The finite Monte Carlo estimates measure rejection frequency with simulation uncertainty; they do not establish calibration outside this model.

### 5.4 Cluster-count sensitivity

As a cluster-count sensitivity analysis, we reran the same 20,000-replication grid with five tasks per cluster and 6 or 24 independent clusters, retaining the seed, ICCs, effects, and nominal level. Under the null at rho = 0.8, task-level rejection was 0.227 with 6 clusters and 0.214 with 24 clusters, while the cluster-mean test was 0.052 and 0.048, respectively. For the modest effect Delta = 0.2 at rho = 0.8, cluster-mean power was 0.115 with 6 clusters and 0.267 with 24 clusters (versus 0.413 and 0.608 for the task-level comparator). The calibration direction therefore persists across these cluster counts, while the power penalty is material when the number of independent clusters is small. These are still synthetic replications of the same model, not evidence from financial reports or an agent deployment.

The raw outputs are `experiments/artifacts/cluster_sensitivity_6.json` and `experiments/artifacts/cluster_sensitivity_24.json`; both use seed 20261105 and the unchanged simulation code.

### 5.5 Source-grounded applicability check (Iteration 11)

A separate deterministic micro-pilot now grounds the arithmetic input in Microsoft FY2024/FY2023 reported annual revenue (245,122 and 211,915 million USD), corroborated by three company-hosted source snapshots. The dated July 30, 2024 release supplies a selected availability convention, not proof of earliest public availability. One compatible case and two explicitly constructed temporal/unit scenarios reuse the unchanged policies. Across these three dependent cases, naive reuse gives 1 correct and 2 wrong accepted answers; the contract gives 1 correct, 0 wrong accepted and 1 unnecessary abstention; the ordinary metadata solver gives 2 correct, 0 wrong accepted and no unnecessary abstention. Details, primary URLs, source locks, independent arithmetic oracle and per-case outputs are in `paper/SOURCE_GROUNDED_PILOT.md` and `experiments/artifacts/source_grounded/results.json`.

This supplies source provenance, not independent-cluster evidence: there is one issuer and one annual pair, no blind holdout, no observed contract-change series and no learned evolution. The ordinary solver remains the stronger comparator. The inherited API attempt returned no scorable text, so it cannot fill the real-model evidence gap; `docs/API_PILOT_AUDIT_2026-11-13.md` records access failures and the distinction between prompt variants and actual generated/executed skills. The newly repeated related-work audit is `docs/NOVELTY_AUDIT_2026-11-13.md`; it does not establish priority from incomplete HTML inspection.

### 5.6 Fixed-bank multiple-candidate null experiment (Iteration 12)

We extended the calibration study to a frozen finite bank of independent all-null candidates, with seed 20261114, 20,000 replications, 12 clusters, five tasks per cluster, ICCs {0, 0.2, 0.5, 0.8}, and candidate budgets {1, 5, 20}. Every candidate receives a fresh independent Gaussian sample. The same saved task-level and cluster-level p-value banks supply all five comparators: unadjusted task testing, unadjusted cluster testing, task Bonferroni, cluster Bonferroni, and cluster error spending with alpha/[r(r+1)]. This is not adaptive candidate generation or repeated reuse of a validation set.

At ICC 0.8 with 20 candidates, the probability of at least one false promotion was:

| Rule | False-promotion probability | Pointwise 95% Wilson Monte Carlo interval |
|---|---:|---|
| Task-level, unadjusted | 0.99265 | [0.99137, 0.99374] |
| Cluster-mean, unadjusted | 0.63715 | [0.63046, 0.64379] |
| Task-level, Bonferroni | 0.85090 | [0.84590, 0.85577] |
| Cluster-mean, Bonferroni | 0.04945 | [0.04653, 0.05254] |
| Cluster-mean, error spending | 0.04770 | [0.04483, 0.05074] |

Thus correcting only the candidate count did not repair invalid task-level p-values, and correcting only the sampling unit did not control repeated promotion. The calibrated independent Gaussian model gives exact familywise probabilities 1-(1-alpha)^K for unadjusted cluster tests and 1-(1-alpha/K)^K for cluster Bonferroni; at K=20 these are 0.641514 and 0.048830. The spending rule uses only alpha*K/(K+1)=0.047619 at K=20, so its lower observed rate is not evidence of higher power or superiority.

Configuration, raw per-candidate p-values, all grid results, reproduction commands, environment and hashes are retained in `experiments/null_search_config.json` and `experiments/artifacts/iteration12_search/`. Recomputing the report from the saved p-values exactly reproduces it. These pointwise intervals describe Monte Carlo uncertainty, not financial population uncertainty or simultaneous coverage over the grid. Positive effects and shared baseline noise were untested in Iteration 12 and are examined separately below; adaptive proposals, validation reuse, heavy tails and crossed dependence remain untested. This controlled ablation motivates combining valid sampling-unit inference with a search-error budget; it does not validate the complete sequential protocol or establish financial skill utility.

### 5.7 Shared-baseline calibration and positive effects (Iteration 13)

A separate configuration frozen before generation uses seed 20261115, 20,000 replications, 12 clusters × five tasks, ICCs {0, .5, .8}, candidate prefixes {1, 5, 20}, effects {0, .2}, and baseline variance fractions s in {0, .5}. For candidate j, d_j = Delta + sqrt(1-s) C_j - sqrt(s) B, where independent unit-variance Gaussian random-intercept fields C_j and B have ICC rho and B is shared across candidates. Each difference has marginal variance one and within-candidate ICC rho; between-candidate correlations are s for the same task and s*rho for different tasks within a cluster. Four matched controls cross task/cluster inference with unadjusted/Bonferroni thresholds. All candidates in a cell have the same effect. The null endpoint is familywise false promotion; the positive-effect endpoint is the probability of at least one true promotion, not selected-candidate precision or mixed-null error control.

The following values are extracted from `experiments/artifacts/iteration13_shared/shared_baseline_results.json` at rho=.8 and K=20:

| Baseline fraction s | Effect | Endpoint | Task unadjusted | Cluster unadjusted | Task Bonferroni | Cluster Bonferroni |
|---:|---:|---|---:|---:|---:|---:|
| 0 | 0 | False promotion | .99350 | .64350 | .85885 | .05040 |
| .5 | 0 | False promotion | .75750 | .35675 | .50520 | .03760 |
| 0 | .2 | Any true promotion | 1.00000 | .97950 | .99870 | .26205 |
| .5 | .2 | Any true promotion | .95025 | .70775 | .83170 | .16290 |

For shared-baseline cluster Bonferroni, the pointwise 95% Wilson Monte Carlo intervals are [.03505, .04033] under the null and [.15785, .16808] for effect .2. Shared baseline noise reduces the observed probability of any promotion relative to independent candidates in these cells, but does not repair invalid task-level inference. Cluster Bonferroni is conservative here and its ability to detect modest effects is limited. Its marginal Gaussian cluster tests are exact, and Bonferroni needs no candidate independence; this is established inference applied to the promotion setting, not a new statistical guarantee. Unadjusted methods' higher positive-effect detection must be read alongside their inflated null error rates.

A retained negative result is that, at s=.5 and rho=.8, increasing K from 1 to 5 to 20 changes cluster Bonferroni null false promotion from .04825 to .04070 to .03760, while any-true-promotion power at effect .2 falls from .17840 to .17075 to .16290. More candidates do not improve detection in this frozen design. These point estimates are not a paired significance test of the decline or a claim about all correlated search designs. The independent-candidate familywise formulas in Section 5.6 do not apply to shared banks.

The complete p-value bank, frozen configuration, environment, generating-code hashes, reproduction commands and test logs are retained under `experiments/artifacts/iteration13_shared/`. Saved p-values exactly reproduce the complete JSON-value report. Effects share Gaussian draws and candidate budgets use nested prefixes; methods and cells are not independent Monte Carlo comparisons. Intervals are pointwise, not simultaneous or paired-difference tests. The configuration is author-frozen, not externally preregistered. This experiment still has no adaptive proposals, repeated validation reuse, heterogeneous candidate effects, empirical financial observations or generated/executed LLM skills. The ordinary metadata solver's advantage in the deterministic pilots remains unchanged.

### 5.8 External-issuer reporting-calendar failure check (Iteration 14)

An author-designed transfer check adds NVIDIA FY2025/FY2024 and Intel FY2024/FY2023 reported annual revenue from company-hosted release snapshots. The existing admission fixtures and all handwritten execution policies remain unchanged. Each issuer supplies three dependent scenarios: a constructed decision after the selected release, a constructed decision before that release, and an equivalent billion-USD representation of the current amount. The task asks for the percentage change between reported adjacent fiscal years; it does not ask for constant-duration or per-day-normalized growth. An independently implemented integer-rational arithmetic oracle scores answers to 12 decimal places. Source-specific extraction, selected release dates and inferred fiscal starts are analyst supplied; there is no autonomous extraction or blind, independent-author holdout.

| Unchanged policy | Tasks | Correct answers | Wrong accepted | Safe abstentions | Unnecessary abstentions |
|---|---:|---:|---:|---:|---:|
| Naive frozen | 6 | 2 | 4 | 0 | 0 |
| Conservative contract | 6 | 0 | 0 | 2 | 4 |
| Ordinary metadata solver | 6 | 0 | 0 | 2 | 4 |

Both stricter policies reject all six tasks. NVIDIA's fiscal endpoints move from January 28, 2024 to January 26, 2025; Intel's move from December 30, 2023 to December 28, 2024. The implementations require exact year-shifted month/day equality and therefore reject even the four answerable reported-fiscal-year comparisons. This is a semantic applicability failure of an over-restrictive calendar rule, not evidence that these reported annual values are invalid or that the skill mechanism adds utility. The ordinary solver's advantage in the earlier scale-conversion pilot does not generalize to this convention. No policy was revised after seeing these outcomes. These tasks are now exposed development evidence and cannot serve as unseen confirmation of a later calendar-aware revision.

`paper/ISSUER_TRANSFER_CHECK.md` and `experiments/artifacts/iteration14_financial/` retain source URLs, raw snapshots, hashes, excerpts, task definitions, oracle targets, per-invocation outputs and reproduction information. Scenarios share one annual pair per issuer; six rows are not six independent financial clusters. Current webpage snapshots do not establish historical source vintages or earliest availability. An accompanying source-lock repair checks actual disk inputs and executor objects before/after invocation, with mutation tests; it is an in-process consistency check, not tamper-proof attestation. This increment adds a reproducible negative financial-convention result, not financial performance or persisted model-generated skill evidence.

### 5.9 Calendar-aware ordinary-validator development comparison (Iteration 15)

A handwritten calendar-aware ordinary validator was evaluated on nine previously exposed scenarios derived from the same three issuer annual pairs. It answers 6 cases correctly, makes no wrong accepted answers, and has no unnecessary abstentions in this development set; the old metadata solver answers 2 and the conservative contract 1. Removing availability checks produces 3 wrong accepted answers, while removing unit normalization produces 3 wrong accepted answers and only 3 correct answers. These are local development comparisons, not causal estimates or generalization evidence. The explicit author-selected duration rules accept July–June 365/366-day Microsoft years and 364/371-day issuer week-years; the week-year starts are partly inferred and the duration thresholds are not source facts. See `paper/CALENDAR_VALIDATOR_DEVELOPMENT.md` and the byte-locked raw results in `experiments/artifacts/iteration15_calendar/`.

The result changes the immediate methodological priority: the Iteration 14 failure is addressable by a stronger ordinary calendar-aware validator on the exposed cases, so it is not evidence that an evolving skill helps. No independent holdout, generated skill, or live LLM execution is established. The next test must freeze the validator, task semantics, scoring, candidate budget, and execution budget before independently authored issuer/source-vintage tasks are opened; generated skills must then be persisted and executed against the same ordinary baseline.

## 6. Implications for SEA

SEA's current candidate-comparison interface accepts paired task-level reports and checks task identifiers, evaluator consistency, discovery/evaluation separation, and retention. The inspected implementation does not represent a task-cluster identifier in its comparison contract. The proposed extension is modest:

1. Add a pre-registered cluster_id to every paired task record.
2. Verify that candidate and baseline task IDs and cluster assignments match.
3. Aggregate paired differences within clusters.
4. Conduct promotion inference across independent cluster units.
5. Report the number of clusters, cluster-size distribution, ICC sensitivity range, effect estimate, uncertainty, and power limitation.
6. Preserve existing retention, cost, provenance, and rollback checks.

The statistical gate should be an optional, versioned evaluator component rather than a silent change to SEA's existing behavior. It must be tested independently before it is used to promote workflow candidates.

## 7. Limitations

First, the Monte Carlo design is synthetic; the separate source-grounded micro-pilot contains one issuer and constructed scenarios, not independent financial-cluster evidence. Neither includes a successful live language-model execution or historical-return study. Second, the random-intercept model assumes independent clusters and exchangeable within-cluster dependence. Third, marginal Gaussian cluster t-tests are exact under the stated assumptions, but few clusters limit power and Bonferroni can be conservative; calibration under non-Gaussian or crossed dependence is untested. Fourth, fixed-bank experiments evaluate statistical components, not adaptive validation reuse or end-to-end self-evolution. Fifth, Iteration 14 adds checks of actual runtime objects and on-disk inputs, repairing the earlier source-lock check that only rehashed its in-memory record. These checks do not provide a blind test, tamper-proof attestation or external preregistration. Sixth, the results do not establish investment performance or financial skill utility: ordinary metadata validation is stronger in the original and Microsoft pilots, but both stricter policies over-abstain on the new week-calendar issuer pairs. Only two new annual pairs are added, and their scenario rows are dependent. Iteration 15 resolves these exposed failures with handwritten calendar-aware rules on development cases; this does not demonstrate unseen-task generalization or evolving-skill utility.

## 8. Conclusion

This study measures the joint effect of task clustering and candidate multiplicity in Gaussian workflow-promotion simulations. Among the compared rules in the high-ICC fixed banks, task Bonferroni leaves severe false-promotion inflation and unadjusted cluster testing leaves candidate-search inflation. Cluster Bonferroni controls error under its stated marginal-validity assumptions, including shared candidates, but has limited detection power: 16.29% at effect .2 in the shared high-ICC, 20-candidate example. Increasing candidate count does not improve detection in that design. These results support planning independent evidence and search budgets together, not a universal necessity or optimality theorem. The next financial study must use independently authored multi-issuer/source-vintage tasks and actual persisted model-generated skills against equal-budget ordinary validators, retaining both the ordinary solver's advantage in earlier scale-conversion cases and the shared over-abstention failure on the two new issuer calendars. The external-issuer check establishes a limitation of the unchanged handwritten policies, not an evolutionary benefit. Adaptive reuse and real-agent utility remain unestablished.

## References

1. Agrawal, L. A., et al. (2026). GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html
2. Fei, C., Si, Q., Liang, K., Xiao, Y., Kalnis, P., & Guo, H. (2026). EMAS: Stabilizing Multi-Agent System Evolution through Evidence-Guided Revision. arXiv:2608.07196. https://arxiv.org/abs/2608.07196
3. Jiang, L., et al. (2026). EvoTS-Agent: A Self-Evolving LLM Agent for Financial Time Series Change Point Detection. arXiv:2608.17933. https://arxiv.org/abs/2608.17933
4. Feng, Y., et al. (2026). Governed Self-Evolution for Autonomous Investing: A Multi-Agent LLM System with an Invariant Core. arXiv:2610.30557. https://arxiv.org/abs/2610.30557
5. Siyezzz. (2026). SEA: Self-Evolving Agent. GitHub repository. https://github.com/Siyezzz/SEA
6. Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. Journal of Human Resources, 50(2), 317–372. https://doi.org/10.3368/jhr.50.2.317
7. Zhang, K., et al. (2026). OpenFinGym: A Verifiable, Multi-Task Gym Environment for Evaluating Quant Agents. Findings of EMNLP 2026. https://aclanthology.org/2026.findings-emnlp.2258/

Bibliography audit update (2026-11-15): primary abstract/proceedings/publisher pages independently matched title and author metadata for entries 1–4, 6 and 7 (GEPA, EMAS, EvoTS-Agent, Steward, Cameron–Miller and OpenFinGym). The fetched EMAS HTML was not fully inspected in this round; section-level acceptance and checkpoint-selection claims remain inherited rather than newly verified. This is not a replication of those papers or an implementation audit. Entry 5 and the inherited SEA code-inspection claims were not re-audited. The four requested additional arXiv records are tracked separately in the dated novelty audits.
