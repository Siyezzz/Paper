# Cluster-Aware Evaluation for Evidence-Gated Evolution of Financial Research Agents

## Abstract

Financial research agents may be evaluated on multiple tasks drawn from the same company, sector, or market regime. Such tasks are not generally independent. If a workflow-evolution system treats every task as an independent observation, it can overstate the evidence that a candidate configuration improves on its baseline. This paper studies a simple correction: a cluster-aware paired promotion gate that computes candidate–baseline differences on matched tasks and aggregates them at the level of independently sampled task clusters. We formalize the evaluation problem with a random-intercept model and derive the design effect and effective sample size. We evaluate task-level and cluster-level one-sided t-tests in a Monte Carlo experiment with 12 independent clusters, five tasks per cluster, intracluster correlations from 0 to 0.8, and standardized effects from 0 to 0.4. Under the null, the task-level test's rejection rate rises from approximately 5.1% at zero correlation to 21.2% at an intracluster correlation of 0.8, whereas the cluster-mean test remains close to the nominal 5% level in this simulated design. This calibration comes at a cost: the cluster-level test has lower power for modest effects. The results support a limited conclusion: task clustering should be represented in the evaluation protocol before an agent workflow is promoted. The experiment is synthetic and does not demonstrate that a financial agent or portfolio strategy improves.

**Keywords:** self-evolving agents; financial research; clustered inference; paired evaluation; workflow evolution; SEA.

## 1. Introduction

A financial research agent may be tested on several reports from the same issuer, multiple issuers from one sector, or repeated observations from a single market regime. These tasks provide useful coverage, but they do not necessarily provide independent evidence. Shared accounting conventions, business models, market shocks, data vendors, and evaluation templates can induce correlated outcomes. An evaluation procedure that counts every task as an independent observation can therefore become overconfident about a workflow update.

This issue matters for self-evolving agents. A workflow may be revised after a failure, tested on several related tasks, and promoted when its measured performance exceeds a threshold. If validation tasks share a common source of variation, the apparent number of independent replications is smaller than the raw task count. The system may retain a change that works for one company family or market regime but does not generalize.

This paper addresses one narrow methodological question: **how should paired evidence for a financial-agent workflow update be aggregated when tasks are clustered?** We propose a cluster-aware promotion gate. For each task, the candidate and baseline are evaluated on the same input and the difference in quality is computed. Task-level differences are then averaged within pre-defined clusters. Statistical inference is conducted across cluster means, not across all task rows.

The contribution is deliberately modest. We do not introduce a new self-evolving-agent architecture, a new portfolio optimizer, or a new theory of clustered inference. We adapt a standard random-intercept model and cluster-level inference to a practical promotion decision for financial research workflows. The aim is to make an existing SEA-style evidence gate less likely to confuse repeated, correlated tasks with independent validation.

The paper makes one contribution: a cluster-aware paired evaluation rule for workflow promotion, accompanied by a Monte Carlo calibration study that measures its false-positive and power trade-offs under an explicit intracluster-correlation model.

## 2. Related Work

### 2.1 Self-evolving agents and financial workflows

GEPA studies reflective prompt evolution from execution trajectories and candidate evaluation [1]. EMAS is the closest system-level precedent: it evolves a frozen-model multi-agent workflow through recurring trace-level diagnoses, localized prompt or topology revisions, paired validation against the predecessor, and persistence of accepted versions [2]. EvoTS-Agent applies validation-guided evolution to financial time-series change-point detection [3]. Steward proposes a governed multi-agent investment system with memory, outcome grading, reversible prompt learning, and protected invariants [4]. These works establish that reflective or feedback-driven evolution is already an active research area, including in finance. The present paper does not claim otherwise.

Financial-agent evaluation also increasingly emphasizes verifiable tasks and leakage controls. OpenFinGym provides a multi-task environment for quantitative agents. Our focus is narrower: even if task answers are verifiable, the statistical unit used to compare candidate and baseline workflows still matters when tasks share company, sector, or regime structure.

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

The proposed simple gate tests the mean of the independent cluster means:

\[
t_{\mathrm{cluster}}=\frac{\bar d_{\cdot}}{s_{\bar d_c}/\sqrt C}, \qquad df=C-1.
\]

A one-sided promotion decision at level alpha is made only if the corresponding p-value is below alpha, subject to a separately specified retention and safety gate. This paper studies only the clustered quality-difference component; a p-value alone is not sufficient for deployment.

The comparator is a task-level paired t-test that treats all C times m task differences as independent. It quantifies the consequence of ignoring the cluster structure.

The cluster-mean test is intentionally simple and transparent. It is not guaranteed to be optimal with unequal cluster sizes, few clusters, non-exchangeable within-cluster dependence, or heavy-tailed outcomes. A full agent study should compare small-sample cluster-robust methods or a wild-cluster bootstrap.

## 5. Monte Carlo Experiment

### 5.1 Data-generating process

We simulate paired workflow utility differences under:

\[
d_{ci}=\Delta+u_c+\epsilon_{ci},
\]

with total marginal variance normalized to one. The cluster shock and task noise are generated independently with variances rho and 1-rho. The design uses 12 independent clusters and five tasks per cluster (60 task observations). We vary rho in {0, 0.2, 0.5, 0.8} and standardized effects Delta in {0, 0.2, 0.4}. Each condition uses 20,000 Monte Carlo replications with fixed random seed 20261105. The nominal one-sided significance level is 0.05.

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

The result does not establish universal calibration. The data-generating process is a simple exchangeable random-intercept model; real financial tasks may have unequal cluster sizes, multiple crossed dependencies, serial correlation, non-normal errors, and changing cluster definitions.

### 5.4 Cluster-count sensitivity

As a pre-specified sensitivity check, we reran the same 20,000-replication grid with five tasks per cluster and 6 or 24 independent clusters, retaining the seed, ICCs, effects, and nominal level. Under the null at rho = 0.8, task-level rejection was 0.227 with 6 clusters and 0.214 with 24 clusters, while the cluster-mean test was 0.052 and 0.048, respectively. For the modest effect Delta = 0.2 at rho = 0.8, cluster-mean power was 0.115 with 6 clusters and 0.267 with 24 clusters (versus 0.413 and 0.608 for the task-level comparator). The calibration direction therefore persists across these cluster counts, while the power penalty is material when the number of independent clusters is small. These are still synthetic replications of the same model, not evidence from financial reports or an agent deployment.

The raw outputs are `experiments/artifacts/cluster_sensitivity_6.json` and `experiments/artifacts/cluster_sensitivity_24.json`; both use seed 20261105 and the unchanged simulation code.

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

First, the Monte Carlo design is synthetic and does not use real financial reports, a live language model, or historical U.S.-equity returns. Second, the random-intercept model assumes independent clusters and exchangeable within-cluster dependence. Third, the cluster-mean t-test can be conservative and underpowered with few clusters; it is not a substitute for careful design or small-sample robust inference. Fourth, this paper evaluates one statistical component of workflow promotion, not the full end-to-end self-evolution system. Fifth, the results do not establish investment performance or the economic value of a financial agent.

## 8. Conclusion

This study isolates a basic issue in the evaluation of evolving financial research agents: tasks grouped by company, sector, or market regime may not provide independent evidence. In a controlled Monte Carlo design, treating all task rows as independent inflated the null rejection rate as within-cluster correlation increased. Testing across cluster means controlled the nominal error rate in the specified simulation, but reduced power for modest effects. The practical implication is not that cluster means are universally optimal, but that task dependence must be represented explicitly in the promotion protocol. The next empirical step is to implement cluster metadata in a versioned SEA evaluator and test it on independently sampled financial research tasks. No claim of real-agent or market-performance improvement is made.

## References

1. Agrawal, L. A., et al. (2026). GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. ICLR 2026. https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html
2. Fei, C., Si, Q., Liang, K., Xiao, Y., Kalnis, P., & Guo, H. (2026). EMAS: Stabilizing Multi-Agent System Evolution through Evidence-Guided Revision. arXiv:2608.07196. https://arxiv.org/abs/2608.07196
3. Jiang, L., et al. (2026). EvoTS-Agent: A Self-Evolving LLM Agent for Financial Time Series Change Point Detection. arXiv:2608.17933. https://arxiv.org/abs/2608.17933
4. Feng, Y., et al. (2026). Governed Self-Evolution for Autonomous Investing: A Multi-Agent LLM System with an Invariant Core. arXiv:2610.30557. https://arxiv.org/abs/2610.30557
5. Siyezzz. (2026). SEA: Self-Evolving Agent. GitHub repository. https://github.com/Siyezzz/SEA
6. Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. Journal of Human Resources, 50(2), 317–372. https://doi.org/10.3368/jhr.50.2.317
7. Zhang, K., et al. (2026). OpenFinGym: A Verifiable, Multi-Task Gym Environment for Evaluating Quant Agents. Findings of EMNLP 2026. https://aclanthology.org/2026.findings-emnlp.2258/

Bibliography audit note (2026-11-12): duplicate and conflicting reference numbers were repaired without changing the inherited bibliographic claims. Entries 1–7 remain inherited records, not newly independently verified in this iteration. The separate current primary-source audit is `docs/NOVELTY_AUDIT_2026-11-12.md`; submission requires rechecking all inherited entries and code-inspection claims.
