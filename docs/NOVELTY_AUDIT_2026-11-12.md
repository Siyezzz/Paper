# Primary-source audit and novelty matrix — 2026-11-12

## Scope and retrieval boundary

This audit independently fetched the arXiv abstract pages for the four identifiers below on 2026-11-12 and repeated that check in a second pass. Version-specific HTML was inspected through WebFetch's processed text for all four papers; all four extractions were truncated and do not constitute a complete paper/code audit. Dream-RSI HTML, previously unavailable, was retrieved in the second pass. SkillsBench HTML initially failed in that pass and succeeded on retry. The bibliography identifiers, first authors, titles and latest revision dates match the returned abstract records. No peer-review status is inferred from arXiv publication. Processed HTML responses sometimes describe their input as supplied page text and generate plausible section anchors; this audit therefore cites only requested, returned page-level URLs and identifies sections by printed headings, not unverified anchors. Raw complete HTML/PDF bytes and code were not independently archived or inspected.

| Work and pinned primary URL | Verified version | What the inspected primary text supports | Consequence for our proposed study |
|---|---|---|---|
| Zheng et al., *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*, https://arxiv.org/abs/2609.14858v2 | v2, revised 2026-10-06 | A programmable exploration layer around an unchanged base agent; historical discovery trees serve as replay simulators to refine exploration policies. Abstract reports nine tasks in four domains. Second-pass HTML includes policy selection and reversible search-branch closure in Appendix D.2. | Replaying experience and improving search policies are not new. Branch closure is not evidence of skill-call revocation after financial semantic change; the inspected extraction does not establish that mechanism. Full methods/code comparison remains open. |
| Xia et al., *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses*, https://arxiv.org/abs/2609.24972v3 | v3, revised 2026-10-04 | Frozen-backbone harness evolution; bounded edits, history-guided exploration, critic, stability-aware selection, cost control and component pruning. HTML sections 2–4 and Appendix D describe these mechanisms. | Generic admission, pruning, transfer, bounded edits and cost-aware evolution are already precedents, not our novelty. A skill-contract study must measure a finance-specific semantic failure, not rename pruning. |
| Wang et al., *FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery*, https://arxiv.org/abs/2602.14670v2 | v2, revised 2026-08-19 | Executable financial skills and structured experience memory; retrieve–generate–evaluate–distill loop. Inspected HTML sections 3–4 describe IC/correlation-based admission, replacement, frozen 2024-selected factors evaluated in 2025 and memory ablations. | Financial skills, memory, admission, replacement and cross-market evaluation are not new. IC/ICIR are prediction measures, not demonstrated net trading returns. |
| Li et al., *SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks*, https://arxiv.org/abs/2602.12670v4 | v4, revised 2026-06-14 | Abstract: 87 tasks, eight domains, 18 model–harness configurations, matched no-Skills/curated-Skills evaluation. Inspected HTML sections 3–5 include deterministic checks and a separate self-generated-Skills condition on three configurations. | Paired deterministic skill evaluation and compact skills are not new. Longitudinal admission/revocation should be distinguished from fixed task efficacy. |

## Second-pass verification record

The following are page-level evidence URLs actually requested in this pass. Section references are printed headings, not independently verified fragment anchors.

| Primary abstract record | Independently returned authorship and submission history |
|---|---|
| https://arxiv.org/abs/2609.14858 | Tong Zheng first author; 17 authors returned, ending with Yunsong Guo. v1: 2026-09-14; v2: 2026-10-06. Title matches the matrix. |
| https://arxiv.org/abs/2609.24972 | Peng Xia first author; 14 authors returned, ending with Chen-Yu Lee. v1: 2026-09-21; v2: 2026-09-23; v3: 2026-10-04. Title matches the matrix. |
| https://arxiv.org/abs/2602.14670 | Yanlong Wang, Jian Xu, Hongkang Zhang, Shao-Lun Huang, Danny Dongning Sun, Xiao-Ping Zhang. v1: 2026-02-16; v2: 2026-08-19. Title matches the matrix. |
| https://arxiv.org/abs/2602.12670 | Xiangyi Li first author; long author list returned, ending with Dawn Song. v1: 2026-02-13; v2: 2026-03-07; v3: 2026-03-13; v4: 2026-06-14. Title matches the matrix. |

- **Dream-RSI:** https://arxiv.org/html/2609.14858v2 . Section 3 selects policies using historical replay scores; Appendix D.2 describes closing unsuccessful search branches and reopening them after a later success. Section 4.3 mentions finance as a Lasso application, not a financial accounting-change experiment. The processed extraction stops during Appendix D.2; Appendix E was not inspected. No financial availability/unit/period-triggered skill-call invalidation was established in the inspected material.
- **RRSI:** https://arxiv.org/html/2609.24972v3 . Section 3.1 explicitly allows tools, skills, memory and subagents to be modified, added or removed. Section 3.3 and Appendix D.2 report unproductive components to the proposer as deletion targets for later rounds. Deletion proposals are not evidence of immediate runtime call blocking. Algorithm 2's DomainGuard is not enough to infer financial semantic checks. The extraction stops during Appendix D.3; later appendices E–F were not inspected. Financial temporal/accounting-triggered revocation was not established.
- **FactorMiner:** https://arxiv.org/html/2602.14670v2 . Sections 3.2–3.4 distinguish executable evaluation skills, factor-library admission/replacement, and experience-memory evolution. Section 4.2.4 tests recent periods, while Section 6 lists “develop online memory updates for non-stationary markets” as future work. Factor decay, memory deletion and factor replacement must not be relabeled as skill-call revocation. The extraction stops in Appendix D after factor 014; remaining factor entries and code were not inspected. No accounting-definition/unit-version-triggered skill invalidation was established.
- **SkillsBench:** https://arxiv.org/html/2602.12670v4 . Section 5.1.1's visible prose reports self-generated-skill deficits of 8.1, 11.3 and 11.5 pp; the second-pass extraction does **not** expose the dedicated Appendix D.6 results table and stops immediately after that heading. Section 6 proposes extending SKILL.md frontmatter with an explicit “complexity contract,” “applicability boundaries,” and “a required lightweight fallback path.” Thus contracts and applicability boundaries themselves are not a new contribution. A proposal is not evidence of implemented financial-change detection or runtime revocation. The financial-domain aggregate and SEC-filings tasks do not establish such a mechanism; unseen task assets/trajectories and Appendix F.3 remain unaudited.

**Local terminology correction:** `experiments/artifacts/financial_contract_results.json` explicitly says rejection is invocation-scoped, not permanent skill deletion. Any manuscript claim must describe a per-call applicability gate unless persistent revocation is separately implemented and tested. The local fixture does not demonstrate genuine online drift or a learned skill lifecycle.

## Corrections and numerical caution

- SkillsBench's current abstract omits self-generated-Skills numbers, but its inspected current HTML DOES report that condition. Abstract omission is not evidence of removal from the full paper. The inspected Section 5.1.1 prose reports negative changes of 8.1, 11.3 and 11.5 percentage points for three configurations; the second-pass extraction did not expose the dedicated appendix table, so table-level verification is not claimed. These are protocol-specific, not proof that automatic skill evolution cannot work. We do not use older '-1.3 pp' summaries as current evidence.
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
| Cluster-aware testing calibrates the existing balanced Gaussian pilot | supported_by_saved_experiment, conditional on independent reproduction | `experiments/artifacts/reproduction_manifest.json` records the 20,000-replicate baseline and 6/24-cluster sensitivity commands, source hashes and test exit code 0; Iteration 10 reran the scripts and tests, while this second literature pass did not |
| Financial semantic contract checks can expose unsafe reuse in designed cases | supported_by_saved_constructed_artifact; not independently rerun in this literature pass | `experiments/artifacts/financial_contract_results.json` records 14 cases: contract has 6 correct answers, 0 wrong accepted answers, 8 abstentions including 1 unnecessary abstention; this is fixture detection, not field effectiveness |
| Contract-aware evolution outperforms an ordinary metadata-aware solver | not established; existing artifact does not support superiority | Saved results explicitly state the metadata solver solves all answerable cases directly; no learned evolution or real-LLM comparison is established |
| Skill revocation improves real financial workflows | hypothesis | Needs dated public source snapshots, independently authored answers and model execution |
| The paper is submission-ready | unsupported_remove_or_qualify | No source-grounded financial benchmark, real-LLM loop or full closest-method comparison |

## Submission fit and next evidence gate

The current artifact is a methodological and evaluator pilot. An agent-evaluation or trustworthy-financial-AI workshop is a plausible *category*, not a verified open venue or deadline. A stronger submission requires source-grounded financial tasks, independently authored holdout, equal-budget model runs with/without skills and ordinary validators, multiple seeds, sequential-search calibration, and full closest-method/code audit. No publication acceptance or deadline is promised.

## Research spending

USD 10/day is a research-effort budget target, not a payment record. Platform billing is inaccessible. Actual spend is **unknown**; no claim of spending USD 10 is made. No recharge, subscription purchase or artificial repetition was performed.
