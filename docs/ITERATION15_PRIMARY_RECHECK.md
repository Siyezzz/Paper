# Iteration 15: Independent Primary-Source Recheck

Recheck date: 2026-11-16. Scope: financial semantic applicability, ordinary validators, and boundaries of skill-lifecycle claims.

## Evidence and access limits

The existing `docs/NOVELTY_AUDIT_2026-11-16.md` was read for prior limitations. This report records a new round of eight WebFetch requests: four arXiv abstract pages and the four versioned HTML pages linked by those abstract pages. All eight requests returned content. The supplied identifiers were checked against the returned titles rather than assumed correct. No broad search was needed.

WebFetch is an extraction/processing interface, not a byte-preserving archival download. The abstract returns displayed titles, abstracts, author lists, HTML links, and submission histories. The HTML returns supplied targeted excerpts and explicit visibility limits. Some extractor replies describe their input as "provided" or "pasted" text; that is the extractor's wording, not evidence of a separately supplied user transcript. The evidence here is the content returned by the named URL requests. Quotes below reproduce returned excerpts; equations are normalized for readability. No encoded attachment was decoded, no PDF was downloaded or read, no implementation repository or validator source was inspected, and no experiment was reproduced. Reported reference-harness behavior remains an author claim, not independently verified execution.

Every HTML return reported truncation. An unobserved mechanism must not be described as absent from the whole paper or its code. Prior audit details not directly visible in this round are not automatically revalidated. No claim of priority, full equivalence, or established project effectiveness follows from this recheck.

## 1. Dream-RSI

### Requests and identity

- Abstract fetched: https://arxiv.org/abs/2609.14858
- Versioned HTML fetched: https://arxiv.org/html/2609.14858v2
- Returned title: **Dream-RSI: Recursive Self-Improvement through Evolving Worlds**.
- Abstract history: v1, 2026-09-14 00:10:47 UTC; v2, 2026-10-06 09:37:58 UTC. The abstract page linked v2 HTML.

The abstract directly states: "A lightweight orchestration layer makes exploration explicit and programmable while leaving the underlying base agent unchanged." It describes accumulated discovery history as a replay simulator and redeployment of the improved policy online.

### Directly observed text

Section 3, Offline evaluation:

> "The recorded tree T_i never changes; only the observed portion grows."

> "Unlike online execution, offline replay returns recorded children of the selected nodes deterministically rather than generating new candidates."

> "These choices vary across policies and budget preferences, but every branch is traversed in its recorded parent–child order, and no outcome outside T_i is produced."

The mathematical notation T_i above is normalized from the returned math rendering. Appendix D.2, Listing 2, visible lines 7–10:

```text
The environment is a frozen, irregular branch×attempt grid. A policy opens a root
or refines the next cell of an already-open branch. Each revealed cell costs one
probe. The policy sees only the cells it has revealed so far; unrevealed scores are
unknown.
```

Section 3 separately defines eligible nodes as the root plus current leaves. That mathematical action-set definition does not establish any specific metadata API. In this round, `question.meta` and `legal_roots` were not directly visible. Appendix D.2 showed `## API` at line 28 and `question.reset()` at line 30 before truncation. In particular, the metadata fields and range-check details discussed in the previous audit must not be labeled newly confirmed by this round.

Appendix B.1 describes numerical correctness checks against a reference PyTorch implementation under the official KernelBench protocol. Section 4.3 mentions finance as an application domain of the Lasso regularization path. Neither excerpt establishes financial concept/unit/entity/source-version applicability checking. Structural constraints described in prose do not establish an inspected structural-validator implementation.

### Claim boundary and visibility limit

Fixed-tree replay supports reuse and evaluation of recorded outcomes. It does not itself establish validity on unrecorded outcomes, financial time applicability, or persistent-skill revocation and migration recertification. No such complete mechanism was directly established in the returned excerpts; this is not an absence assertion.

The last directly visible HTML position reported was Appendix D.2, Listing 2, line 30, `question.reset()`, followed by `[content truncated]`. Appendix B.3 was only a heading; Appendix E entries in the table of contents do not mean their bodies were read. Unseen APIs, code, and later appendices remain unverified.

## 2. RRSI

### Requests and identity

- Abstract fetched: https://arxiv.org/abs/2609.24972
- Versioned HTML fetched: https://arxiv.org/html/2609.24972v3
- Returned title: **RRSI: Regularized Recursive Self-Improvement of Agent Harnesses**.
- Abstract history: v1, 2026-09-21 17:54:49 UTC; v2, 2026-09-23 22:10:39 UTC; v3, 2026-10-04 02:18:13 UTC. The abstract page linked v3 HTML.

The abstract identifies prompts, control flow, tooling, memory, and context management around a frozen backbone as the harness. It describes a critic and pruner, not financial source-version governance.

### Directly observed text

Section 3.3, Leakage Screening:

> "Before full evaluation, a critic reads each candidate diff and rejects edits that explicitly encode task names, entity names, task-specific values, answers, or other logic specific to the evolve benchmark, as well as edits that add inert machinery."

Appendix D.1, Algorithm 1, explicitly comments that "the critic reads the diff, not the proposal".

Section 3.3, Lasso/L1-Style Structural Pruning:

> "Components that remain unproductive are reported to the proposer as deletion targets in subsequent rounds."

Appendix D.2:

> "The proposer receives B_t together with any previously accepted edits associated with those components and is instructed to remove unproductive machinery in subsequent proposals."

B_t is normalized mathematical notation. The described route is therefore deletion targets → subsequent proposals → candidate evaluation and acceptance gates → selected next harness. The returned algorithm does not describe an immediate runtime revocation path when a component is marked unproductive. This distinction must not be inflated into a universal assertion that RRSI can never revoke anything.

Algorithm 2 includes:

```text
g ← DomainGuard(H_t, H')  // per-domain specific checks
```

The comment and notation are normalized from the returned algorithm. The candidate must pass the historical score floor, the cost/admissibility condition, and g. This establishes an explicit domain-check gate in the paper's pseudocode. It does not establish its implementation or the content of financial/source-version/time checks.

Appendix D.3, equation (17), for candidates within the empirical noise tolerance after the stability floor:

```text
w_s ΔS - w_c ΔC + w_n ν_t(H') > 0
```

The algorithm comment says "inside the band: no credit for score", while the displayed equation retains `w_s ΔS`. With no verified weights in this return, the score term must not be silently treated as zero. The novelty term counts previously unwon structural component types; it does not encode financial semantic validity.

Section 2 states that a verifier can be unit tests in coding or an LLM judge in workspace environments. Task scoring, leakage screening, and an abstract DomainGuard must not be conflated with an independently inspected financial applicability validator.

### Claim boundary and visibility limit

Generic candidate admission, pruning, cost gates, and domain-check interfaces are adjacent prior work. A project contribution requires evidence of the specific financial applicability and lifecycle behavior claimed, plus a strong ordinary-validator comparison. The returned text does not settle whether uninspected code contains additional checks.

The last directly visible HTML position was Appendix D.3, equation (17), immediately followed by `[content truncated]`. Subsequent explanation, complete weights, concrete DomainGuard checks, and repository behavior were not inspected.

## 3. FactorMiner

### Requests and identity

- Abstract fetched: https://arxiv.org/abs/2602.14670
- Versioned HTML fetched: https://arxiv.org/html/2602.14670v2
- Returned title: **FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery**.
- Abstract history: v1, 2026-02-16 11:48:52 UTC; v2, 2026-08-19 04:16:20 UTC. The abstract page linked v2 HTML.

The abstract directly describes "a Modular Skill Architecture that encapsulates systematic financial evaluation into executable tools" and experience memory recording successful patterns and failure constraints. This is directly relevant financial prior work, not merely a general agent paper.

### Directly observed text

Section 3.2:

> "Validation Pipeline: A rigorous, standardized protocol for factor assessment (check_ic → check_correlation → admit)."

> "By offloading the evaluation to a deterministic, code-based skill, FactorMiner avoids "hallucinated metrics": the reported IC and ICIR are computed deterministically."

The returned text describes 60+ executable financial operators, configuration-based market support, and independently optimizable execution backends. These are financial execution and validation capabilities; they cannot be presented as absent.

Section 3.3 describes formation, evolution, and retrieval of memory. In particular:

> "The signal m_t serves as a prompt-level constraint for the LLM policy"

The returned continuation says memory uses compact natural-language templates with canonical examples, retrieved against library diagnostics and recent rejection reasons. The m_t notation is normalized. Forbidden directions constrain further mining; this does not by itself establish revoked skill identities or a pre-execution revocation check.

Section 3.4:

> "The correlation constraint (Stage 2) ensures diversity, while the replacement mechanism (Stage 2.5) allows high-quality factors to replace inferior ones."

Appendix A:

> "then α replaces the single correlated factor g, allowing the library to evolve toward higher quality while preserving diversity."

The replacement object is a factor in factor library L, not a persistent skill. The main algorithm uses absolute correlation and a general fitness-improvement threshold; Appendix A equation (11) uses explicit IC thresholds and writes its correlation set with signed `rho > theta`. These formulations should not be described as mechanically identical without implementation inspection.

Section 4.1:

> "All datasets cover a training period from 2024-Q1 to 2024-Q4 and a held-out test period in 2025."

> "We do not fine-tune or update the LLM weights; self-evolution comes from retrieval-conditioned generation, deterministic skill execution, library admission, and memory distillation."

Section 4.2.1:

> "Top-40 factors are selected once on CSI500 (2024) and then frozen for evaluation on multiple datasets."

Table 1 states that combination weights/signs are determined on 2024 and factor-selection models train on 2024 and test on 2025. The separate Section 4.2.4 experiment uses the full 110-factor library; the Top-40 protocol must not be automatically transferred to that experiment.

### Claim boundary and visibility limit

Financial operators, IC/correlation validation, factor admission/replacement, memory, and cross-market evaluation are already directly supported by this paper. Financial document concept/unit/entity/source-version correctness and persistent-skill lifecycle governance are different evaluation objects. A time split or typed operator signature is insufficient evidence of unit-aware, source-version-aware skill certification; a configuration switch is insufficient evidence of migration recertification. The returned text did not directly establish that complete lifecycle, but uninspected paper/code portions could contain additional mechanisms.

The returned HTML reached Appendix D, Full Factor Library, through factor 014, then `[content truncated]`. Factors 015–110, complete implementations, numerical results reproduction, and any undisplayed material were not checked. The text also contains a memory example involving an admitted factor with correlation 0.82 versus an Appendix A default threshold of 0.5; the return does not resolve whether configurations or stages differ. Do not invent an explanation.

## 4. SkillsBench

### Requests and identity

- Abstract fetched: https://arxiv.org/abs/2602.12670
- Versioned HTML fetched: https://arxiv.org/html/2602.12670v4
- Returned title: **SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks**.
- Abstract history: v1, 2026-02-13 07:06:06 UTC; v2, 2026-03-07 00:51:15 UTC; v3, 2026-03-13 07:33:01 UTC; v4, 2026-06-14 21:21:07 UTC. The abstract page linked v4 HTML.

The abstract reports 87 tasks, eight domains, 18 model-harness configurations, and matched no-Skills/curated-Skills evaluation. These are paper-reported results, not independently reproduced measurements.

### Directly observed text

Section 2:

> "Each Skill contains a required SKILL.md file with natural-language instructions and may optionally include auxiliary resources such as scripts, templates, reference files, or worked examples."

> "Thus, a Skill is neither model weights nor an executable tool by itself; it becomes actionable through a compatible harness that injects its instructions and exposes its resources."

Appendix C concerns **task.md**, whereas Section 6 proposes changes to **SKILL.md**. They must not be conflated.

Appendix C.1:

> "The schema is strict at the top level: unknown keys are rejected at parse time"

> "values within the free-form metadata block are open by design"

The example declares `schema_version: "1.3"`; that alone does not establish which other versions the parser accepts.

Appendix C.2:

> "The closed tier is enforced at review time rather than at parse time: metadata is parsed as a free-form mapping with no load-time enumeration check, so off-taxonomy values are surfaced during review rather than rejected by the parser."

The closed tier includes category, task_type, modality, interface, skill_type, and difficulty. This is a controlled vocabulary at review, not a claim of closed metadata parsing.

Appendix C.3:

> "The allowlist mode requires a non-empty allowed_hosts list—a parse-time error otherwise—so an allowlist declaration is never left under-specified."

These are ordinary structural and cross-field validation rules. Appendix C says the reference harness implements the stated enforcement and its test suite covers it; this recheck did not inspect that implementation or run those tests. Hostname syntax, wildcard behavior, DNS handling, and detailed network isolation were not established by the returned excerpt.

Section 6:

> "We propose extending the SKILL.md frontmatter with an explicit complexity contract: expected tool and token cost, applicability boundaries, and a required lightweight fallback path."

Its continuation begins "This would help agents". This is a proposal, not direct evidence that the contract is implemented and enforced. A required field inside a proposed contract must not be described as an existing parser requirement.

Finance evidence is bounded: visible examples contain `category: finance-economics`; Table 3 reports nine Finance & Economics tasks; Section 5.1.3 mentions SEC filings. The formal taxonomy and task mapping are referred to Appendix M.9/Table 19, whose bodies were not displayed in this return. Cross-model portability, multi-harness evaluation recommendations, and task-submission re-evaluation do not directly establish skill migration recertification or production revocation.

### Claim boundary and visibility limit

Ordinary schema and cross-field validators are concrete adjacent mechanisms, not a straw baseline limited to JSON parseability. This paper does not supply a directly observed empirical comparison against the project's proposed financial lifecycle mechanism. The returned excerpts did not establish a full source-version-triggered admission/revocation/recertification protocol; this is not a claim that none exists anywhere.

The last visible numbered heading was Appendix D.6, Self-Generated Skills Condition, followed by `[content truncated]`; D.5 was the last subsection with visible body text. Appendix M.9/Table 19 and later statistical appendices were not read. An in-text reference does not establish access to the referenced body.

## Implications for the project's claims and comparisons

1. Do not claim generic skill evolution, replay, memory, candidate admission, pruning, cost gates, financial factor validation/replacement, portability, paired evaluation, or schema checking as isolated novelty.
2. State a narrow, testable hypothesis: explicit financial concepts, units, entities, source versions and availability times affect the admission and pre-execution use of persistent model-generated skills, including revocation and migration revalidation when relevant evidence changes. This describes a mechanism to demonstrate, not an established unique contribution.
3. The ordinary-validator baseline should include required fields, types, enumerations, cross-field constraints, and directly comparable source-ID/date/expiry rules. SkillsBench Appendix C directly motivates a baseline stronger than parseability alone. Also compare with deterministic rules encoding known financial boundaries; repackaging those rules as skills does not establish added capability.
4. Evaluate actual persistent skills with lifecycle ablations and matched candidates, tasks, model/tool permissions, and budgets. Report incorrect use, missed and excessive revocation, correctness, and cost. A statistical factor replacement is not a substitute for that evaluation.
5. Use genuine source versions and availability times; do not permit future-document or target-answer access during skill generation/selection. Keep test and selection protocols distinct. Paired evaluation is prior practice, and neither fixed-pool selection nor noise floors nor factor decorrelation substitutes for justified inference.

This round narrows defensible wording. It neither proves the absence of an equivalent mechanism in uninspected materials nor validates the project's implementation or financial-task efficacy. Existing audit and MAIN files were not edited by this work; no commit or push was made.
