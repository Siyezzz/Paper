# Paper Iteration Ledger

This ledger counts research-design and manuscript iterations, not hidden model updates or autonomous learning events. An iteration is counted only when a concrete decision, experiment, or manuscript artifact changes and is recorded.

**Current count: 13 completed iterations (0–12).**
**Current manuscript status: focused methodological draft; not submission-ready.**

| Iteration | Stage | Main action | Outcome | Status |
|---:|---|---|---|---|
| 0 | Initial framing | Broad self-evolving financial agents for portfolio, risk and resource allocation | Too broad; no single falsifiable contribution | Superseded |
| 1 | Concept definition | Freeze foundation model; distinguish configuration evolution from weight updates | Parameter-frozen scope defined | Retained as setting |
| 2 | Literature positioning | Compare prompt optimization, financial agents and workflow evolution | Generic prompt evolution rejected as novelty | Retained |
| 3 | Experiment design | Define baselines, financial metrics and held-out evaluation | Identified attribution, leakage and risk problems | Partly retained |
| 4 | Report-to-Flow | Write Skill v0.1 and convert reports to typed evidence-linked flows | Useful infrastructure, but not sufficient as the paper's main novelty | Infrastructure |
| 5 | Academic drafting | Create proposal-style manuscript and claim audit | Draft had no real agent results; not a completed paper | Superseded |
| 6 | Statistical pilot | Monte Carlo study of task dependence and paired evaluation | Cluster dependence identified as a possible evaluation issue; synthetic only | Retained as pilot |
| 7 | Focused contribution | Narrow to cluster-aware evaluation and write reproducible simulation to GitHub | One methodological contribution selected | Previous baseline |
| 8 | EMAS deep reading | Read EMAS paper and official method/results/limitations/reproducibility docs; compare against our proposal | Confirmed EMAS is the closest precedent and co-authored by the user's supervisor; generic evidence-guided evolution is not novel. Cluster-aware evaluation remains a possible narrow extension, pending supervisor alignment and stronger methods comparison. | Previous revision |
| 9 | Reproduction and applicability pilot, 2026-11-12 | Reproduced the 20,000-replication pilot, independently verified four requested arXiv records, added fixed deterministic financial contract fixtures and seven policies, corrected bibliography numbering | Fourteen constructed evaluation cases: naive/validation-only 6 correct and 7 wrong accepted; contract 6 correct and 0 wrong accepted, with one unnecessary abstention; ordinary metadata solver 7 correct and 0 wrong accepted. All 15 final tests pass. | Previous revision |
| 10 | Cluster-count sensitivity, 2026-11-12 | Re-ran the frozen Gaussian cluster-gate grid at 6 and 24 independent clusters, retaining five tasks per cluster, 20,000 replications, seed 20261105, ICCs and effects | At rho=0.8 under the null, task-level rejection was 0.227 (6 clusters) and 0.214 (24), versus 0.052 and 0.048 for cluster means. At effect=0.2, rho=0.8, cluster-mean power was 0.115 and 0.267. Direction persists; power depends strongly on independent-cluster count. | Previous revision |
| 11 | Source-grounded applicability and API audit, 2026-11-13 | Added a source-locked Microsoft revenue micro-pilot, audited inherited API failures, rechecked requested related work, and tightened manuscript claims | Provenance improved, but ordinary metadata validation still dominates the conservative contract; no evolutionary advantage or real-model evidence | Previous revision |
| 12 | Fixed-bank null-search ablation, 2026-11-14 | Reproduced prior experiments and added five matched inference/search controls on a frozen independent all-null candidate bank | Cluster-unit correction and candidate multiplicity control are both needed in this Gaussian model; no adaptive-reuse or financial-agent benefit demonstrated | Current revision; not submission-ready |

### Iteration 12 evidence and critique — 2026-11-14

- Parent: `382b5e22341840005b9b1b7aa66735720fe9bac8` (remote main synchronized before work); iteration SHA is the commit containing this entry.
- Reproduction: baseline Gaussian output, deterministic financial-contract pilot, and source-grounded Microsoft pilot reproduced in `experiments/artifacts/iteration12_search/`; existing result JSON matched. Initial 27 offline tests passed; after the fixed-bank experiment was added, all 32 tests passed. A subsequent safety patch rejects nonzero effects directly at the generate(config) entry before RNG initialization; the added regression test brings the final suite to 33 passing tests. The frozen configuration, p-value bank and report were not regenerated. The original manifest retains its generating-version hashes and has a post_run_validation addendum pointing to the independent post_validation_receipt.json and final validation logs. Stored p-values reproduce the complete report by JSON-value equality under --verify-only, not a claim of identical serialized bytes.
- Frozen design: seed 20261114; 20,000 replications; 12 clusters × 5 tasks; ICC 0, .2, .5, .8; candidate prefixes 1, 5, 20; zero effect only; five controls. The bank is a finite set of independent candidates with fresh independent Gaussian samples, not an adaptive search or reused validation set. Full p-values, config, report, exact command, environment and hashes are retained under `experiments/artifacts/iteration12_search/`; configuration SHA256 `aa914541ebc68860e1463576cee34c42255a288bcaae5a5633dd8ecd19a8233f`; p-value bank SHA256 `5747d75f8e6f5f1995ce92eb14cdb90c5fc87f78536df560edec5d9b60ae6be3`.
- Primary endpoint: at ICC .8, K=20, false-promotion rates were task unadjusted .99265; cluster unadjusted .63715; task Bonferroni .85090; cluster Bonferroni .04945; cluster alpha-spending .04770. Pointwise 95% Wilson Monte Carlo intervals and exact theoretical cluster-familywise comparisons are in `paper/MAIN.md` 5.6 and raw JSON. Alpha spending at K=20 spends .047619, so the lower observed rate is not superiority evidence.
- Interpretation/claim change: only the combination of a valid cluster unit and candidate multiplicity control preserves the nominal familywise level in this controlled Gaussian null. Bonferroni alone applied to invalid task-level p-values leaves severe excess false promotion; cluster-aware inference without search correction also allows repeated false promotion. No positive-effect power, adaptive proposals, shared baseline noise, data reuse, heavy tails, crossed dependence or empirical financial tasks were tested.
- Literature: `docs/NOVELTY_AUDIT_2026-11-14.md` records titles/version histories for Dream-RSI, RRSI, FactorMiner and SkillsBench, their visible method overlap, and processed-HTML truncation. No priority claim is made; source code and complete PDFs/appendices remain unaudited.
- Operational failure: the first manual run selected a not-yet-created output directory and exited `FileNotFoundError` on saving the compressed p-value bank after computation. No result was written from that attempt; formal evidence was then generated in the already-existing iteration12 directory via the reproduction harness and verified from raw p-values. Keep this failed command out of the evidence set but disclose the incident here.
- Cost: zero API calls, no credentials read; actual spend unknown. USD 10/day remains an effort target. No charges, purchases or subscriptions occurred.
- Next gate: simulate positive effects and a shared baseline under frozen configs; implement actual repeated reuse/adaptive selection separately; then create independently authored, multi-issuer source-vintage tasks and execute genuine persisted/generated skills under equal budgets against ordinary validators. Existing model API raw artifacts remain untouched and untracked.

### Iteration 9 evidence and critique

- Parent commit: `245c882`; the iteration commit is the commit containing this ledger entry (obtain with `git log -1 --format=%H -- docs/ITERATION_LEDGER.md`, avoiding a self-referential SHA).
- Evidence: `experiments/artifacts/baseline_reproduction.json`, `financial_contract_results.json`, `test_results.txt`, and `reproduction_manifest.json`; fixed code/config and per-case outputs are retained.
- Manuscript increment: `paper/CONTRACT_PILOT.md`; prior methodological proposal preserved as `paper/PAPER_DRAFT_before_iteration9.md`. Existing `paper/MAIN.md` remains the Gaussian methodological study, with duplicate reference numbering repaired and inherited citations flagged.
- Negative finding: ordinary metadata validation solves the convertible-scale case rejected by the skill contract; no demonstrated evolutionary advantage. Invocation-scoped revocation is not permanent skill deletion.
- Failures during development: undefined fixture value names were corrected; H09's fiscal period change originally left publication earlier than period end, causing an extra abstention. Its date was repaired for internal fixture consistency, not by tuning policy. Intermediate metrics were 5 contract / 6 solver correct before that repair. Concurrent edits also produced a transient assertion failure; the final stable 15-test run passes. These cases are author-designed, not an independently blind holdout.
- Claim change: prioritize financial semantic applicability and safe transfer as a falsifiable evaluator direction; do not claim generic skill evolution, pruning, admission or cost control as novelty. See `docs/NOVELTY_AUDIT_2026-11-12.md`.
- Outstanding: no observed financial benchmark, independent holdout authorship, real-LLM generated/executed skills, sequential-search simulation, or full primary-paper/code audit. Actual spend unknown; USD 10/day remains a target, not recorded expenditure.

### Iteration 10 evidence and critique

- Parent commit: `3eb0710`; the iteration commit is the commit containing this ledger entry. This is post hoc sensitivity analysis of the existing frozen model, not a pre-registered hypothesis test.
- Evidence: `experiments/artifacts/cluster_sensitivity_6.json` and `experiments/artifacts/cluster_sensitivity_24.json`; code, seed and grid are unchanged from the baseline simulation. Environment: Python 3.13.14, NumPy 2.5.4, SciPy 1.18.1, Windows 11.
- Manuscript increment: `paper/MAIN.md`, Section 5.4. The new paragraph reports raw rejection and power values and links both artifacts.
- Interpretation: the calibration direction is not unique to 12 clusters in this synthetic random-intercept design, but the cluster-level power penalty is substantial with few independent clusters. This does not add real-financial or LLM evidence.
- Checks: baseline and contract artifacts reproduced; all 15 tests pass after the change.
- Limitations: 6 and 24 clusters are sensitivity replications of the same authored Gaussian model, not independent financial task samples; no venue-readiness claim changes.

### Iteration 11 evidence and critique — 2026-11-13


- Parent commit: `5fe553abb036113b728ba7561b11eb4a8b005cc9`, an inherited, unpushed API-harness commit, preserved without rewriting. Remote `main` was an ancestor at `582aebb`; fetch over SSH/443 succeeded. The iteration commit is the commit containing this entry.
- Reproduction: all original 18 tests passed; the fixed 20,000-replication, seed-20261105 Gaussian baseline and original 14-case deterministic contract pilot reproduced without artifact differences. The expanded suite passed 25 intermediate tests and all 27 final offline tests. A resumed-environment rerun also passed all 27; its environment and commands are recorded in `experiments/artifacts/iteration11_reproduction_manifest.json`.
- New observed input: Microsoft FY2024/FY2023 GAAP annual revenue, 245,122/211,915 million USD, corroborated across three company-hosted pages saved with hashes and excerpts. The independent arithmetic implementation gives 15.669962013071...% growth. This is one issuer and one annual pair, not independent task clusters.
- Three explicitly designed scenarios reuse unchanged policies: naive 1 correct / 2 wrong accepted; contract 1 correct / 0 wrong accepted / 1 unnecessary abstention; ordinary metadata solver 2 correct / 0 wrong accepted / no unnecessary abstention. Decision dates and equivalent-unit representation are constructed; historical website vintages, observed drift and blind holdout are not claimed. See `paper/SOURCE_GROUNDED_PILOT.md` and `experiments/artifacts/source_grounded/results.json`.
- Inherited API failure audit: 168 attempts, 164 HTTP 403 and 4 transport errors, zero successful/scorable outputs or usage records. These are access failures, not incorrect model answers. Original local raw output remains untouched and untracked; its SHA256 and aggregate audit are saved. No new live API call was made. The `generated_skill` identifiers currently represent prompt variants, not persisted generated skills or externally enforced contracts.
- Reliability increment: globally stop on the first missing key, HTTP 401 or HTTP 403; record real start/end timestamps and protocol/source/prompt hashes. Offline mocks verify failure stop and successful control flow, not provider availability.
- Literature increment: independently rechecked all four requested arXiv IDs against primary abstract/processed HTML pages; inspection is truncated, exact author spellings and full code audits remain unresolved. See `docs/NOVELTY_AUDIT_2026-11-13.md`.
- Claim change: provenance now extends beyond synthetic financial numbers, but ordinary validation still dominates this conservative contract. No evolutionary advantage, market benefit or publication readiness is established. Original proposal text is retained; `paper/MAIN.md` Section 5.5 and linked supplements isolate the new evidence.
- Next gate: independently authored multi-issuer, source-vintage holdout; freeze scoring and generation prompts before opening it; persist a genuinely generated skill, execute it separately, and compare ordinary validators under matched budgets. The sequential-search and stronger statistical baselines remain unexecuted.
- Spending and access: USD 10/day is a target; actual spend remains unknown without billing. Prior project memory reports an exposed API credential: user must revoke/rotate it before any resumed live run. No key was read or used in this iteration, and no recharge/subscription was purchased.

## Writing-skill protocol from Iteration 8 onward

Process guides used:
- `research-ideation`: research question card, evidence needs, falsification criteria and feasibility gate.
- `ml-paper-writing`: related-work and drafting modes; repository-first writing; claim ledger; abstract/introduction narrative; mathematical precision; figure-first review; verified citations.
- `paper-self-review`: structure, logic, claim audit, citations, figures/tables and overclaim review.
- `citation-workflow`: bibliographic verification from canonical sources; no references generated from memory.

These skills are process guidance, not proof of quality. Each paper revision must include a claim ledger and evidence links.

## Rules for future iteration counting

Increment the count only when:
1. a research question or contribution is materially changed;
2. a new experiment is run and its result is recorded;
3. an analysis reveals a flaw and causes a method revision;
4. a manuscript section is substantively rewritten after review;
5. a reproducibility or citation audit changes the paper.

Do not count cosmetic wording changes, repeated reflections, or unexecuted plans.

Every iteration records date, issue, evidence, critique, change, tests, limitations, and Git commit SHA.

No result may be added to the paper unless its code, input data or fixture, output, and environment are recorded.
