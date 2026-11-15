# Independent novelty audit — 2026-11-15

## Scope and evidence status

This round's independent reviewer accessed all four primary abstract records and versioned HTML pages and returned the title, version-history and method-level checks recorded below. The lead also independently fetched the Dream-RSI abstract. This is a completed primary-page recheck in this round, with the inspection limits stated here; it is not merely inherited from the 2026-11-14 audit. All HTML responses were truncated; complete PDFs, remaining appendices and implementation repositories were not audited. Absence from the inspected text is not evidence of absence from a paper. This audit does not establish priority or reproduce published results.

| Record | Independently matched title | Version history checked |
|---|---|---|
| https://arxiv.org/abs/2609.14858 | Dream-RSI: Recursive Self-Improvement through Evolving Worlds | v1 2026-09-14; v2 2026-10-06 |
| https://arxiv.org/abs/2609.24972 | RRSI: Regularized Recursive Self-Improvement of Agent Harnesses | v1 2026-09-21; v2 09-23; v3 10-04 |
| https://arxiv.org/abs/2602.14670 | FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery | v1 2026-02-16; v2 08-19 |
| https://arxiv.org/abs/2602.12670 | SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks | v1 2026-02-13; v2 03-07; v3 03-13; v4 06-14 |

## Method-level findings

**Dream-RSI** — https://arxiv.org/html/2609.14858v2, Section 3 and Equation 1. Offline replay deterministically reveals existing children of a fixed historical discovery tree; it does not generate outcomes outside that tree. Selection includes the incumbent and maximizes mean replay score on the same replay worlds. This yields a selection property for the fixed pool's mean score, not guaranteed online improvement, per-tree non-regression, unseen-task generalization or multiplicity-adjusted significance. Response truncated near Appendix D.2 code. Formal cluster inference, executed financial skills and semantic revocation were not established in the visible text.

**RRSI** — https://arxiv.org/html/2609.24972v3, Section 3.3 and Appendix D.1–D.2. A critic inspects candidate diffs before evaluation for task/entity/answer leakage and inert edits. A pruner targets unhelpful components for a subsequent proposal that must be reevaluated and pass gates; this is not immediate runtime revocation. Algorithm 2 includes noise tolerance, score/cost gates and DomainGuard. DomainGuard internals were not visible. The body describes S* as the evolve-set historical best, while the visible algorithm updates it using the selected incumbent: retain this discrepancy. Response truncated at Appendix D.3; later noise-band acceptance details were not inspected. No formal multiplicity correction or financial semantic revocation was verified.

**FactorMiner** — https://arxiv.org/html/2602.14670v2, Sections 3.2–3.4, Algorithm 1, Section 4.2.1 and Appendix A. Skills are executable tools encapsulating financial evaluation, with persistent experience memory. `check_ic → check_correlation → admit` admits factors; replacement modifies the factor library, not a persistent skill. The visible Table 1 caption states Top-40 selection on CSI500 (2024), freezing before 2025 multi-dataset evaluation. Correlation filtering is not familywise error control. Initial screening uses absolute IC in Algorithm 1 but signed IC in an appendix expression; replacement correlations also differ in absolute/signed notation. These require reconciliation before implementation comparison. Response truncated near factor 014 in Appendix D. Paired/cluster inference, Bonferroni and persistent skill revocation were not verified.

**SkillsBench** — https://arxiv.org/html/2602.12670v4, Sections 4 and 6, Appendix D.1–D.2. The design is 87 tasks × 18 configurations × two matched conditions × three trials = 9,396 slots, not 9,396 verified independent observations. Paired deltas are defined at configuration–task level; exact per-trial seed matching was not verified. Figure captions mention 95% intervals, but Appendix N is needed to determine CI construction, bootstrap pairing, clustering and multiplicity. That appendix was unavailable in the returned HTML, which truncated after Appendix D.6. The complexity contract in Section 6 is a proposed extension. Skill packages may contain executable scripts; a skill is not itself necessarily an executable tool. Semantic revocation was not established.

## Consequences for the manuscript

Generic skill evolution, admission, pruning, cost gates, transfer, executable tools and persistent memory are not sufficient novelty claims. Factor replacement must not be called skill revocation; fixed-pool replay monotonicity must not be called online improvement. Do not assert that these systems lack statistical corrections based on missing appendices. Our current evidence remains Gaussian calibration plus deterministic evaluator checks. A defensible financial contribution still requires source-vintage tasks, independent holdout units and genuine persisted model-generated skills against ordinary validators under equal budgets.

## Additional bibliography metadata

The lead independently matched primary title/author metadata for GEPA (ICLR proceedings), EMAS arXiv:2608.07196, EvoTS-Agent arXiv:2608.17933, Steward arXiv:2610.30557, OpenFinGym ACL Anthology 2026.findings-emnlp.2258 and Cameron–Miller DOI 10.3368/jhr.50.2.317. This is metadata verification, not full-text or implementation verification. The fetched EMAS HTML was not fully inspected this round; section-level claims remain inherited. A local cached-text inspection was denied, so no section-level recheck is claimed. SEA implementation claims were not re-audited.
