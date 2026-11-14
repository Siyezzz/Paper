# When Should Financial Research Agents Accept Their Own Revisions?
## Cluster-Aware and Search-Aware Evaluation for Self-Evolving Workflows

**Status: evolving research draft, not submission-ready. The original methodological proposal is preserved in `paper/PAPER_DRAFT_before_iteration9.md`. Iteration 9 adds a separately labeled constructed deterministic contract pilot. Iteration 11 adds a one-company source-grounded arithmetic micro-pilot (`paper/SOURCE_GROUNDED_PILOT.md`), with explicitly constructed decision/scale scenarios; neither is a real-LLM or observed market-contract-change experiment. The failed API attempt supplies no scorable model output.**

## Abstract

Self-evolving financial research agents modify persistent workflows using experience from previous tasks. A central challenge is deciding whether a proposed revision merits adoption. Paired validation controls task difficulty, but does not by itself address dependence among financial tasks or repeated adaptive search against a validation set. We formulate workflow promotion as a sequential decision over clustered, paired quality differences. We outline a protocol that separates candidate discovery from fresh-cluster confirmation, allocates an explicit error budget across revisions, and reserves a sealed audit set for the final validation-selected workflow. Under conditional validity of each confirmation test, the probability of ever promoting a revision whose expected improvement fails to exceed a pre-specified margin is bounded by the total allocated error budget. This is an application of established statistical principles, not a new general inference theorem. The repository now contains both a single-revision Gaussian calibration simulation and an independently sampled, fixed-bank all-null multiple-candidate experiment (Iteration 12; `paper/MAIN.md`, Section 5.6). The latter separates sampling-unit correction from candidate-count correction, but does not validate adaptive reuse or the full sequential protocol, and neither demonstrates improvement in a real financial agent. We specify experiments that distinguish dependence correction, adaptive selection, evaluation cost, and genuine agent-level utility. The proposed study asks when self-evolution produces credible evidence of improvement, rather than assuming that more revisions imply a better financial system.

## 1. Introduction

Financial research workflows contain recurring decisions about retrieving evidence, computing quantities, checking definitions, and reconciling sources. A language-model agent can revise these procedures without changing its model weights. Such revisions can persist across tasks and therefore constitute a meaningful form of workflow evolution. However, a revision that performs better on a validation collection may merely exploit features of that collection.

Two properties make financial research a useful setting for studying this problem. First, distinct tasks often share an issuer, reporting period, accounting template, or sector-level context. A collection of task IDs is not necessarily a collection of independent experimental units. Second, the workflow may repeatedly propose revisions after inspecting earlier validation outcomes. Even a well-calibrated test for a single fixed candidate can become unreliable when its data are reused adaptively.

Existing systems already establish the feasibility of evidence-guided workflow evolution. EMAS diagnoses recurrent trace-level failures, proposes localized changes, and compares candidates against their predecessors on paired validation tasks [1]. EvolveTrade updates the prompt policy of a trading agent using realized experience [2]. SHARP constrains financial-policy evolution to auditable rubric edits and uses walk-forward validation [3]. EvoTS-Agent evolves executable financial time-series analysis trajectories [4]. Consequently, neither persistent workflow revision nor financial self-evolution is a sufficient novelty claim.

We focus instead on the reliability of the promotion decision. Our proposed contribution is a reproducible evaluation study of a cluster-aware, search-aware confirmation protocol. Its value must be demonstrated against established statistical alternatives and realistic financial research tasks. The current artifact is a study specification with an existing single-revision simulation, not evidence of end-to-end agent performance.

## 2. Evaluation Setting

Let W_(r-1) be the current workflow and W'_r a proposed revision at round r. Both use the same frozen foundation model, tool interfaces, and task inputs. The mutable state consists of prompts and bounded workflow edits. Discovery data may be used freely to diagnose failures and construct a candidate.

Before confirmation begins, freeze the candidate, score definition, execution budget, cluster sampling rule, and minimum practically relevant improvement delta. Each task has a verifiable score q in [0,1], such as correct numeric extraction with a matching source reference. Cost is reported separately in the primary study so that a monetary conversion does not obscure quality effects.

For task i in evaluation cluster c, define the paired difference:

    d_(r,c,i) = q(W'_r, x_(r,c,i)) - q(W_(r-1), x_(r,c,i)).

The primary estimand is the expected cluster-mean quality difference over a pre-defined target cluster population:

    Delta_r = E_c[ mean_i d_(r,c,i) ].

This gives equal importance to sampled clusters. It is generally different from a task-weighted effect when cluster sizes vary. The paper must specify which estimand reflects the intended use case before results are observed.

A company-level cluster does not automatically remove sector or temporal dependence. The main controlled experiment assumes independent clusters; crossed-dependence experiments deliberately violate that simplification. Any real-task conclusion must state what sampling design makes its proposed independent units plausible.

## 3. Confirmation Protocol

### 3.1 Discovery and confirmation separation

Candidate generation uses a development collection. After the candidate is frozen, confirmation uses previously unexposed clusters. Earlier confirmation outcomes may inform later candidates, but the next confirmation batch must remain independent of that candidate's construction under the assumed sampling model. Merely renaming tasks or drawing new tasks from an already exposed issuer is insufficient to establish independence.

### 3.2 Cluster-aware comparison

Compute a mean paired difference within each independent cluster. A transparent baseline applies a one-sided t-test to these cluster means for the null H_r: Delta_r <= delta. Under independent Gaussian cluster means with suitable equal-variance assumptions, this test has the standard t calibration. With few, unequal, or heavy-tailed clusters, that calibration is not universal. Comparators should include suitable small-sample cluster-robust and wild-cluster procedures, with their own assumptions stated explicitly.

For the original balanced random-intercept model,

    d_(c,i) = Delta + u_c + epsilon_(c,i),

with m tasks per cluster and intracluster correlation rho, the variance inflation relative to independent tasks is 1 + (m - 1)rho. This established design-effect calculation motivates cluster-aware evaluation; it is not a new statistical result.

### 3.3 Sequential error allocation

Let F_(r-1) contain the entire history before round r confirmation. Allocate alpha_r = alpha / [r(r+1)] before observing the round's outcomes. Require a conditionally valid p-value under the round-specific null:

    P(p_r <= a | F_(r-1)) <= a, for all a in [0,1].

Promote only if p_r <= alpha_r and any separately frozen retention requirements pass. Since sum_r alpha_r = alpha, a union bound limits the probability of at least one false promotion to alpha under these conditional-validity assumptions. The argument permits adaptively proposed candidates because each test must remain valid conditional on the prior history. It does not make a reused fixed validation set conditionally valid.

This protocol addresses false promotion of non-improving revisions relative to the current predecessor and specified target distribution. It does not guarantee that every realized task improves, that total financial returns increase, or that the target population remains stable over time. Additional retention rules can prevent promotion but cannot restore the validity of a faulty confirmation test.

### 3.4 Trial ledger and final audit

Record every candidate, parent version, edit, discovery snapshot, confirmation batch, cluster assignment, score, p-value, allocated error budget, cost, and decision. The ledger supports reproducibility; it is not itself a statistical correction.

Choose the final endpoint using the registered promotion process and a fixed stopping rule. A sealed audit collection is opened only after this endpoint has been frozen. Report its result even if the final workflow loses to the initial baseline. Using the audit to choose among checkpoints would invalidate its role as an untouched final evaluation.

## 4. Experimental Design

### 4.1 Existing pilot and evidence boundary

The public Paper repository contains a balanced Gaussian random-intercept simulation with 12 clusters, five tasks per cluster, multiple intracluster correlations and effect sizes, and 20,000 replications per condition. Its manuscript reports that naive task-level testing becomes anti-conservative while cluster-mean testing remains near the nominal level in that model. These numerical results were independently reproduced on 2026-11-12 from the existing source; the retained output and pinned environment are recorded in `experiments/artifacts/baseline_reproduction.json` and `experiments/artifacts/reproduction_manifest.json`. This reproduction verifies the stated simulation configuration, not the proposed adaptive-search or real-agent extensions.

The pilot tests one fixed comparison. It does not test adaptive search, repeated validation reuse, fresh-cluster confirmation, real LLM outputs, or market performance. On 2026-11-12 the original 20,000-replication configuration was independently rerun and its displayed three-decimal results reproduced; the output is `experiments/artifacts/baseline_reproduction.json`. At ICC 0.8 under the null, task-level rejection is approximately 0.212 versus 0.048 for the cluster-mean test. This remains a synthetic calibration result.

### 4.2 Dependence and sequential search

Extend the pilot across balanced and unequal cluster sizes, Gaussian and heavy-tailed errors, and crossed issuer/period dependence. Simulate candidate sequences with known null and positive effects. Distinguish a frozen candidate bank from genuinely adaptive candidate construction; conclusions from the former cannot establish reliability under the latter.

Compare four primary conditions: naive task-level testing with fresh batches; cluster-aware testing with fresh batches; task-level testing with sequential error spending; and cluster-aware testing with sequential error spending. Add reused-validation conditions as separate stress tests. This separates the effect of inference from the effect of fresh data.

Run comparisons both at equal total task-execution budget and at equal candidate budget. Fresh confirmation consumes evidence, so a method receiving more independent data must not be credited solely for a statistical improvement. Report probability of any false promotion, power or probability of detecting true improvements, selected-endpoint true effect, confirmation cost, and selection optimism. Include Monte Carlo uncertainty.

### 4.3 Financial research task study

Construct a source-grounded benchmark from dated public financial reports. Suitable tasks include extracting a cash-flow quantity, distinguishing fiscal from calendar periods, identifying the correct denominator for a ratio, and verifying a claimed change against an original table. Fix answers and scoring rules before evaluating candidates. Use time-stamped source snapshots and objective checks wherever possible.

Compare a frozen workflow, ungated revisions, a simple empirical paired gate, a cluster-aware gate, and the combined confirmation protocol. Keep candidate proposals identical where possible to isolate evaluation effects, then run a separate closed-loop experiment to study how different accepted histories affect subsequent proposals. Use multiple runs and disclose all failures. General world knowledge from model pretraining remains a limitation; source-grounded evaluation and numerical perturbation tests can help diagnose reliance on memorized answers.

No successful scorable live model experiment or independently authored multi-issuer financial benchmark has yet been executed. Iteration 11 did execute a one-issuer, source-grounded arithmetic micro-pilot (`paper/SOURCE_GROUNDED_PILOT.md`), whose temporal and scale scenarios are constructed rather than observed drift. The constructed deterministic pilot and this micro-pilot are evaluator checks, not substitutes for the financial-agent study.

## 5. Related Work and Positioning

EMAS is the closest workflow-evolution precedent [1]. Its described acceptance rules compare validation correctness and token use, and its text acknowledges adaptive selection from repeated fixed-set validation. This motivates the present question, but does not establish priority over all possible related systems or implementations. EvolveTrade [2], SHARP [3], and EvoTS-Agent [4] show that financial workflow and policy evolution are already active research directions. A submission must directly compare their evaluation protocols rather than assert that they ignore validation.

Cluster-robust inference is established methodology [5]. The proposed sequential argument is a basic application of conditional test validity and an error-spending union bound. The intended research contribution is the task design, failure-mode measurements, and controlled comparison in a financial self-evolution loop. Broad novelty remains unestablished until a systematic literature and implementation audit is completed.

## 6. Limitations

Fresh, genuinely independent financial-task clusters may be expensive or unavailable. Issuer clustering alone may miss common market shocks. Conservative error spending can substantially reduce power over long evolution runs. Conditional validity is an assumption to justify and test, not a property conferred by a ledger. A sealed audit remains vulnerable to indirect disclosure or repeated author inspection. Quality-score improvements do not establish investment value, causal economic reasoning, or safe autonomous deployment.

A credible negative result is possible: the protocol may reject nearly all revisions at affordable sample sizes. This would still quantify a practical limitation, but would not support claiming that the agent improved.

## 7. Expected Reporting Structure

The final paper should contain a false-promotion calibration figure, a power-versus-independent-cluster plot, an equal-budget sequential-search comparison, a financial-task result table, and complete endpoint trajectories. Each result must link to executable code, frozen configuration, data or fixtures, raw output, and an environment manifest. The proposed adaptive sequential and independently authored multi-issuer financial experiments remain unexecuted. Iteration 12 executes only a fixed independent all-null candidate-bank ablation; its five matched controls and Monte Carlo intervals are reported in `paper/MAIN.md`, Section 5.6, with raw p-values in `experiments/artifacts/iteration12_search/`. This is not a reused-validation experiment, a closed-loop evolution trajectory or a positive-effect power study. The separately completed deterministic evaluator increment, its negative solver comparison, and its evidence boundaries are reported in `paper/CONTRACT_PILOT.md`; the one-issuer source-grounded micro-pilot is reported in `paper/SOURCE_GROUNDED_PILOT.md`. None validates the complete sequential protocol.

## References Checked During Topic Assessment

[1] Chao Fei et al. EMAS: Stabilizing Multi-Agent System Evolution through Evidence-Guided Revision. arXiv:2608.07196. https://arxiv.org/abs/2608.07196

[2] Sehee Kim, Yumin Choi, Minki Kang, and Sung Ju Hwang. EvolveTrade: Experience-Driven Policy Refinement for Self-Evolving LLM Trading Agents. arXiv:2609.17632. https://arxiv.org/abs/2609.17632

[3] Xiwen Chen, Wenhui Zhu, Songzhu Zheng, Kashif Rasul, Yueyue Deng, and Huayu Li. SHARP: A Self-Evolving Human-Auditable Rubric Policy for Financial Trading Agents. arXiv:2605.06822. https://arxiv.org/abs/2605.06822

[4] Lei Jiang et al. EvoTS-Agent: A Self-Evolving LLM Agent for Financial Time Series Change Point Detection. arXiv:2608.17933. https://arxiv.org/abs/2608.17933

[5] A. Colin Cameron and Douglas L. Miller. A Practitioner's Guide to Cluster-Robust Inference. Journal of Human Resources, 50(2), 317–372, 2015. https://doi.org/10.3368/jhr.50.2.317 (Bibliographic entry inherited from the repository; publisher metadata was not independently fetched in this session.)
