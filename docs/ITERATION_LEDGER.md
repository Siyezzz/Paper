# Paper Iteration Ledger

This ledger counts research-design and manuscript iterations, not hidden model updates or autonomous learning events. An iteration is counted only when a concrete decision, experiment, or manuscript artifact changes and is recorded.

**Current count: 9 completed iterations (0–8).**
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
| 8 | EMAS deep reading | Read EMAS paper and official method/results/limitations/reproducibility docs; compare against our proposal | Confirmed EMAS is the closest precedent and co-authored by the user's supervisor; generic evidence-guided evolution is not novel. Cluster-aware evaluation remains a possible narrow extension, pending supervisor alignment and stronger methods comparison. | Current revision |

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
