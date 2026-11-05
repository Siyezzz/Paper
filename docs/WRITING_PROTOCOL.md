# Academic Writing Protocol

## Process references

This project follows:
- Claude Scholar research-ideation: research question card, falsification criteria, evidence records and proposal-readiness gate.
- Claude Scholar ml-paper-writing: repository-first writing, related-work mode, drafting mode, claim ledger, citation verification and narrative discipline.
- writing-guide.md: one central takeaway; precise What/Why/So What; specific introduction; equations that define objects; figures and tables that carry the argument.
- paper-self-review: structure, logic, claim audit, citation audit, figure/table review and final verdict.

## Paper structure to learn from EMAS

Use EMAS as a structural exemplar, not text to copy:
1. Introduction: precise gap, why it matters, approach, contributions.
2. Related Work: organize around decisions/problems, not a list of paper summaries.
3. Methodology: define system state, lifecycle, diagnosis, candidate operations and acceptance rule.
4. Experiments: research questions, baselines, metrics, evolution trajectories and ablations.
5. Limitations: explicit failure cases, selection bias, compute cost and scope.
6. Reproducibility: exact data splits, configurations, source commit, artifact manifests and scripts.
7. Appendix: detailed configurations, statistical checks, additional results and failure examples.

## Claim ledger

Every manuscript claim receives one status:
- supported_by_experiment
- supported_by_primary_source
- hypothesis
- unsupported_remove_or_qualify

Do not write hypotheses in past tense as results. Do not assert novelty without a systematic search and direct comparison to closest methods.

## Style constraints

- One main contribution, not a list of loosely connected features.
- One idea per paragraph.
- Use equations only when they define a meaningful object or derive a testable implication.
- Report negative and non-monotonic results.
- Distinguish validation-selected deployment performance from best-observed test performance.
- Do not overclaim causality from uncontrolled comparisons.
- Prefer a small number of strong, interpretable figures.

## Revision gate

Before every manuscript commit:
1. run experiment scripts;
2. run tests;
3. regenerate result tables from raw output;
4. check claims against the evidence ledger;
5. verify citations;
6. compare the new draft with the previous revision and state what changed;
7. update docs/ITERATION_LEDGER.md.
