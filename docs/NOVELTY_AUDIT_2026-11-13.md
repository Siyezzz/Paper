# Primary-Source Novelty Audit and Constraint Matrix (2026-11-13)

## 1. Scope, sources, and verification boundaries

This audit independently retrieved the four original arXiv abstract pages and experimental HTML pages to check identifiers, titles, versions, and the evidence relevant to financial skill admission, revocation, and transfer. Access date: 2026-11-13. All original abstract pages returned successfully. All HTML responses included methods and experiments, but explicitly ended with `[content truncated]` at different appendices. The conclusions below therefore concern only the returned text; truncation must not be interpreted as absence from the full paper. Full PDFs, complete appendices, code, and external project pages were not independently audited.

**Primary page URLs actually requested:**
- Dream-RSI: https://arxiv.org/abs/2609.14858; HTML: https://arxiv.org/html/2609.14858v2
- RRSI: https://arxiv.org/abs/2609.24972; HTML: https://arxiv.org/html/2609.24972v3
- FactorMiner: https://arxiv.org/abs/2602.14670; HTML: https://arxiv.org/html/2602.14670v2
- SkillsBench: https://arxiv.org/abs/2602.12670; HTML: https://arxiv.org/html/2602.12670v4

## 2. Identifier, title, and version checks

Additional verification record: requesting the four original abstract URLs again returned the same titles and version histories. This pass returned no HTTP rejection, timeout, or identifier–title mismatch, so no failed-access record is invented. Important limitations remain: WebFetch returns processed page text rather than independently archived raw HTTP/PDF bytes. Some author spellings differed between the two SkillsBench responses, so the processed output is not reliable verbatim evidence for the complete author list. This audit does not reuse the previous audit's author table or claim that the complete author list has been verified; exact bibliographic authorship still requires verification against raw page bytes or the PDF. HTML truncation and the RRSI numerical discrepancy are retained below.

| Identifier | Title returned by the primary page | Abstract-page version history | Evidence visible in this pass |
|---|---|---|---|
| 2609.14858 | *Dream-RSI: Recursive Self-Improvement through Evolving Worlds* | v1 2026-09-14; v2 2026-10-06 | The abstract describes programmable exploration orchestration, replay of historical discovery trees, and offline policy improvement; 9 tasks across 4 domains. |
| 2609.24972 | *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses* | v1 2026-09-21; v2 2026-09-23; v3 2026-10-04 | The abstract describes harness-component editing around a frozen backbone, regularized proposal/selection, a critic, a pruner, OOD evaluation, and cost control. |
| 2602.14670 | *FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery* | v1 2026-02-16; v2 2026-08-19 | The abstract describes financial alpha-factor discovery, executable financial skills, experience memory, and a retrieve–generate–evaluate–distill loop. |
| 2602.12670 | *SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks* | v1 2026-02-13; v2 2026-03-07; v3 2026-03-13; v4 2026-06-14 | The abstract describes 87 tasks, 8 domains, 18 model–harness configurations, and matched no-Skills/curated-Skills evaluation. |

## 3. Paper-by-paper checks concerning financial skill admission, revocation, and transfer

### Dream-RSI

**Supported by the returned text:** Section 3 treats historical discovery trees as a replay simulator. A policy agent rewrites executable policy code and selects the next online policy using historical replay scores. Offline replay reads recorded children rather than generating unknown outcomes outside the historical trees. The embedded prompt text returned in D.2 discusses closing or deprioritizing failed frontiers, distinguishing repairable failures from repeatedly unpromising directions, and reopening a branch after later success when closure was based only on an earlier failure.

**Unsupported extrapolation:** These objects are search-tree branches and exploration policies, not financial skills, tool permissions, or executing calls. Closing/reopening a branch is not runtime skill revocation/re-enablement after financial semantic change. The visible finance-related passage concerns Lasso as background for model selection/cross-validation in finance and other domains. No financial trading task or skill-call revocation triggered by accounting-definition, unit, or data-availability change was established. The HTML response is truncated in D.2; if only directly readable prose before truncation is admitted, the detailed branch-closure rules are also incomplete.

### RRSI

**Supported by the returned text:** Section 3.1 explicitly permits tools, skills, memory, and subagents to be modified, added, or removed. In Section 3.3, the pruner reports unproductive components to the proposer as deletion targets for subsequent rounds based on recent gains. The critic screens candidate diffs for task leakage and inert machinery before full evaluation. DomainGuard in Algorithm 2 is one of the candidate-harness acceptance gates. The visible Section 4 supports cross-benchmark OOD and cross-model harness transfer.

**Unsupported extrapolation:** Pruner deletion targets inform subsequent candidate-edit proposals; they are not demonstrated immediate runtime deletion. The visible DomainGuard text provides no financial rules, function implementation, triggering examples, or tool-call interception. Harness-component pruning, candidate acceptance gates, and OOD/cross-model transfer therefore cannot be relabeled as call revocation after financial semantic change. The abstract's “up to 4.3 points” conflicts with the visible main-text JobBench table's +4.7 points; this audit does not base conclusions on that disputed number. The HTML response is truncated after a subsection heading in Appendix D.3.

### FactorMiner

**Supported by the returned text:** Sections 3.2/3.4, Section 4.4, and Appendix A support a standalone reusable Agent Skill, `check_ic → check_correlation → admit`, factor admission/replacement, and experience-memory evolution. The paper reports selecting and freezing Top-40 factors on CSI500 2024 before evaluating them on CSI500, CSI1000, CSI300, and Crypto in 2025. This is frozen-factor cross-market generalization and configuration reuse, not online revocation. The memory section describes consolidating redundancy, discarding low-utility information, and reclassifying variants into failure directions, but the visible evidence includes no deletion interface, deletion logs, or deletion-specific ablation. Developing online memory updates for non-stationary markets is explicitly listed as future work.

**Unsupported extrapolation:** Replacing factor-library members is not Agent Skill revocation. Memory cleanup is not stopping a running skill. Cross-market evaluation is not dynamic admission under new market/accounting semantics. No runtime blocking of financial skill calls after currency, unit, availability-date, accounting-period, or metric-definition change was established. The HTML response is truncated within the factor-library entries in Appendix D.

### SkillsBench

**Supported by the returned text:** Sections 3/4 explicitly evaluate the same tasks under matched no-Skills and curated-Skills conditions and calculate paired differences at the configuration–task level. The visible appendix specifies 18 configurations × 87 tasks × 2 conditions × 3 trials. The main text separately reports a self-generated-Skills condition for three dedicated harnesses; it must not be mixed into the main-condition slot count. Finance & Economics contains 9 tasks, with aggregate domain pass rate increasing from 19.1% to 33.3%, but the visible text is insufficient to enumerate the complete task list.

**Unsupported extrapolation:** Section 6's complexity contract, applicability boundaries, and required lightweight fallback are introduced as “We propose extending,” not as verified implemented fields, validation logic, or a revocation system. Financial tasks and paired evaluation establish efficacy measurement under fixed conditions; the visible text does not show longitudinal skill admission→revocation states, triggers, or post-revocation call records. The response is truncated after the Appendix D.6 heading. Referenced material such as D.6.1 and M.9/Table 19 was not returned and cannot be reconstructed from headings.

## 4. Novelty constraints imposed by the ordinary metadata-validator negative result

The local constructed fixture `experiments/artifacts/financial_contract_results.json` explicitly limits rejection to invocation-scoped rechecking rather than permanent skill deletion. It is not observed financial data, an LLM experiment, a learned policy, or empirical generalization. Across 14 constructed cases, the contract policy records 6 correct answers, 0 wrong accepted answers, and 8 abstentions (7 safe and 1 unnecessary). The from-scratch metadata solver records 7 correct answers, 0 wrong accepted answers, and 7 abstentions, with coverage 0.5 and coverage-conditioned accuracy 1.0. These results cannot support contract/evolution superiority over an ordinary metadata-aware solver; the ordinary solver instead has more correct answers and higher coverage on this fixture.

This imposes the following hard constraints on novelty claims:

1. **Having a schema/metadata is not sufficient novelty.** A contribution must establish a specific financial semantic-lifecycle problem and reproducible gains beyond availability, unit, period, metric, and zero-base checks already handled by ordinary validators.
2. **Separate persistent revocation from per-invocation rejection.** The current artifact supports only rechecking and rejection before each call. It must not be described as skill deletion, persistent revocation, a learned lifecycle, or hot-unloading.
3. **Report coverage costs and ordinary baselines.** Eliminating errors merely by abstaining more does not establish stronger capability. At minimum, compare frozen/validation-only skills and an ordinary metadata solver under equal budgets, identical tasks, and identical adjudication, reporting wrong accepted answers, safe abstentions, unnecessary abstentions, coverage-conditioned accuracy, and coverage.
4. **Establish semantics rather than field matching.** Candidate novelty should focus on combinations of availability and decision time, accounting-period/fiscal-year convention transfer, metric-identity changes, convertible versus nonconvertible units, revisions/restatements, and cross-market context—not renamed metadata checks.
5. **Do not cite these four papers as evidence of unshown financial runtime mechanisms.** Dream-RSI branch closure, RRSI component pruning/DomainGuard, FactorMiner factor admission/replacement/memory evolution, and SkillsBench paired evaluation/contract proposals do not individually establish call blocking after financial semantic change.
6. **Specify the object and trigger of transfer.** Cross-benchmark/model harness transfer, frozen-factor cross-market evaluation, and paired skill-package efficacy tests are different claims from contract-aware skill transfer. Specify source/target data contracts, permitted transformations, rejection reasons, and post-transfer performance/safety curves.
7. **Make the negative result a conclusion rather than concealing it.** The ordinary metadata solver is no worse than the contract policy on this fixture. A defensible contribution statement is an auditable financial contract invocation gate with negative results and boundaries, while evolution superiority remains unestablished—not “self-improvement produces gains.”

## 5. Falsifiable research question and evidence gates

The remaining research question is: once a skill is admitted under one financial data contract, can explicit contracts safely block inapplicable calls or permit demonstrably safe transfer after publication availability, unit scale, accounting period, or metric semantics change, without achieving safety merely through additional abstention?

Minimum evidence gates include source-traceable temporal snapshots/public reports; independently authored holdout tasks; equal-budget comparisons of ordinary metadata validators, frozen skills, contract gates, and any evolution policy; multiple random seeds; explicit invocation-level versus persistent-lifecycle definitions; and actual model execution or an explicit deterministic-evaluator-only scope. The constructed fixture establishes only detection of specified errors, not their prevalence in public financial data, learned discovery, online drift, economic utility, or submission-level superiority.

## 6. Submission fit: qualitative only

The topic is qualitatively closer to workshops/tracks on agent evaluation, trustworthy financial AI, financial data/agent safety, or AI systems evaluation. The current material does not verify any specific open venue, deadline, acceptance probability, or submission readiness; no dates are invented. Given the evidence, a methods-and-evaluation pilot is a more accurate positioning than a completed financial-agent system.

## 7. Audit conclusion

The four identifiers and titles were checked against the original arXiv abstract pages. The papers respectively cover exploration replay, harness evolution, financial factor skills/memory, and paired skill benchmarking, but the text actually returned in this pass does not directly establish a complete financial semantic change→runtime skill revocation→safe transfer loop. The ordinary metadata-validator negative result further constrains novelty: claim an auditable contract gate, explicit negative results, and a hypothesis requiring validation—not priority for self-evolution, skill admission, pruning, or financial transfer in general.
