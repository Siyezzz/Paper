---
name: paper-evaluation-design
description: Design empirical evaluations for AI research with credible baselines, ablations, split hygiene, cost reporting, and failure analysis.
---

# Paper Evaluation Design

Use this skill when a paper needs an experimental protocol, benchmark design, ablation plan, or evaluation audit.

## Design checklist

1. Specify the estimand: what effect, capability, or trade-off the experiment is meant to measure.
2. Define the task stream, unit of analysis, data provenance, train/validation/test separation, and any time-order constraints.
3. Choose baselines that isolate the proposed mechanism. Include a simple baseline and the closest strong prior approach.
4. Plan ablations that remove one causal component at a time. Do not use an ablation that changes several mechanisms simultaneously as sole evidence.
5. Report quality, robustness, latency, token/compute cost, safety or error rates, and relevant distributional trade-offs.
6. Include failure cases and a predeclared stopping/selection rule. For online or sequential systems, test retention on prior tasks and transfer to future or held-out tasks.

## Output

Produce a table mapping each research claim to a dataset or environment, metric, baseline, ablation, and potential threat to validity. Mark any unsupported causal claim as a hypothesis rather than a conclusion.
