# Primary-source audit and novelty matrix — 2026-11-12

## Scope and retrieval boundary

This audit independently fetched the arXiv abstract pages for the four identifiers below on 2026-11-12. Version-specific HTML was also inspected through extracted text for RRSI, FactorMiner and SkillsBench; these extractions were truncated and do not constitute a complete paper/code audit. Dream-RSI HTML retrieval failed, so its comparison is abstract-only. Search summaries were not substituted for primary text. The bibliography identifiers match the retrieved titles. No peer-review status is inferred from arXiv publication.

| Work and pinned primary URL | Verified version | What the inspected primary text supports | Consequence for our proposed study |
|---|---|---|---|
| Zheng et al., *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*, https://arxiv.org/abs/2609.14858v2 | v2, revised 2026-10-06 | A programmable exploration layer around an unchanged base agent; historical discovery trees serve as replay simulators to refine exploration policies. Abstract reports nine tasks in four domains. | Replaying experience and improving search policies are not new. Financial semantic applicability/revocation cannot be judged from this abstract alone. Full methods/code comparison remains open. |
| Xia et al., *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses*, https://arxiv.org/abs/2609.24972v3 | v3, revised 2026-10-04 | Frozen-backbone harness evolution; bounded edits, history-guided exploration, critic, stability-aware selection, cost control and component pruning. HTML sections 2–4 and Appendix D describe these mechanisms. | Generic admission, pruning, transfer, bounded edits and cost-aware evolution are already precedents, not our novelty. A skill-contract study must measure a finance-specific semantic failure, not rename pruning. |
| Wang et al., *FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery*, https://arxiv.org/abs/2602.14670v2 | v2, revised 2026-08-19 | Executable financial skills and structured experience memory; retrieve–generate–evaluate–distill loop. Inspected HTML sections 3–4 describe IC/correlation-based admission, replacement, frozen 2024-selected factors evaluated in 2025 and memory ablations. | Financial skills, memory, admission, replacement and cross-market evaluation are not new. IC/ICIR are prediction measures, not demonstrated net trading returns. |
| Li et al., *SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks*, https://arxiv.org/abs/2602.12670v4 | v4, revised 2026-06-14 | Abstract: 87 tasks, eight domains, 18 model–harness configurations, matched no-Skills/curated-Skills evaluation. Inspected HTML sections 3–5 include deterministic checks and a separate self-generated-Skills condition on three configurations. | Paired deterministic skill evaluation and compact skills are not new. Longitudinal admission/revocation should be distinguished from fixed task efficacy. |

## Corrections and numerical caution

- SkillsBench's current abstract omits self-generated-Skills numbers, but its inspected current HTML DOES report that condition. Abstract omission is not evidence of removal from the full paper. The inspected table reports negative changes of 8.1, 11.3 and 11.5 percentage points for three configurations; these are protocol-specific, not proof that automatic skill evolution cannot work. We do not use older '-1.3 pp' summaries as current evidence.
- RRSI's abstract reports up to 4.3 points OOD, while the extracted main table/text contains a 4.7-point JobBench change. This audit records the discrepancy instead of selecting the larger number. No numeric RRSI superiority claim is needed in our manuscript.
- FactorMiner's high-quality-candidate yield ablation uses relaxed thresholds distinct from its main admission settings. Candidate yield is not final admission, and neither is realized profit.
- No claim that these works universally omit financial temporal/accounting revocation follows from truncated extracts. The inspected material did not establish a directly matched benchmark; complete paper, appendix and implementation reviews remain necessary.

## Falsifiable provisional gap

The next question is whether a skill accepted under one financial data contract should remain callable after publication availability, unit scale or accounting-period semantics change, and whether explicit contracts allow safe transfer without merely abstaining more often. This is a candidate *task and evaluation contribution*, not a priority claim for contracts, typing, program verification, selective prediction or statistical inference.

A constructed deterministic fixture can establish that the evaluator detects specified errors. It cannot establish prevalence in public reports, learned skill discovery, genuine online drift, economic utility, or superiority over a metadata-aware ordinary program. The latter is a mandatory baseline: equality with it is a useful negative result against attributing gains to evolution.

## Claim ledger

| Claim | Status | Evidence / missing evidence |
|---|---|---|
| The four arXiv IDs match the named papers | supported_by_primary_source | Independently fetched abstract pages and revision histories above |
| Generic self-evolving skills, admission, cost control and pruning are sufficient novelty | unsupported_remove_or_qualify | Direct overlap with RRSI, FactorMiner and SkillsBench |
| Cluster-aware testing calibrates the existing balanced Gaussian pilot | supported_by_experiment, conditional on reproduction | Existing script; this iteration saves rerun output |
| Financial semantic contract checks can expose unsafe reuse in designed cases | hypothesis until executable pilot is run | Requires per-case answers, abstentions, transfer and ablations |
| Contract-aware evolution outperforms an ordinary metadata-aware solver | hypothesis; not established | Must retain from-scratch deterministic solver and later real-LLM controls |
| Skill revocation improves real financial workflows | hypothesis | Needs dated public source snapshots, independently authored answers and model execution |
| The paper is submission-ready | unsupported_remove_or_qualify | No source-grounded financial benchmark, real-LLM loop or full closest-method comparison |

## Submission fit and next evidence gate

The current artifact is a methodological and evaluator pilot. An agent-evaluation or trustworthy-financial-AI workshop is a plausible *category*, not a verified open venue or deadline. A stronger submission requires source-grounded financial tasks, independently authored holdout, equal-budget model runs with/without skills and ordinary validators, multiple seeds, sequential-search calibration, and full closest-method/code audit. No publication acceptance or deadline is promised.

## Research spending

USD 10/day is a research-effort budget target, not a payment record. Platform billing is inaccessible. Actual spend is **unknown**; no claim of spending USD 10 is made. No recharge, subscription purchase or artificial repetition was performed.
