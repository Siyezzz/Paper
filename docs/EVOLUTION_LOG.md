# Research Evolution Log

## Iteration 0 — Broad project
The first plan combined report-to-flow, portfolio optimization, risk assessment, resource allocation, prompt evolution, memory, tools, and workflow evolution.
Critique: too many contributions and no single falsifiable claim.
Decision: reduce to one contribution: cluster-aware paired evaluation for promoting financial-agent workflow updates.

## Iteration 1 — Task-level paired gate
Candidate and baseline are evaluated on identical tasks; paired quality differences are calculated.
Critique: task rows from the same company, sector, or regime may be correlated. Unique task IDs do not establish independent observations.
Decision: model task clusters and compare task-level inference with cluster-level inference.

## Iteration 2 — Monte Carlo calibration
Implemented a random-intercept data-generating process with 12 independent clusters, five tasks per cluster, ICC values 0, 0.2, 0.5, 0.8, and standardized effects 0, 0.2, 0.4. Ran 20,000 replications per condition.
Observed result: under the null, task-level rejection increased to 0.212 at ICC 0.8; cluster-mean rejection was 0.048. For effect 0.2 and ICC 0.8, cluster-mean power was 0.177.
Interpretation: cluster-aware inference addresses over-rejection in this model but loses power. It is not universally superior.

## Iteration 3 — Reproducibility checks
Added two unit tests: cluster-level null rejection remains near nominal alpha in selected settings; power falls as ICC increases for a modest effect. Both tests pass.

## Remaining limitations
Synthetic outcomes, not real financial-agent observations. Only a random-intercept exchangeable cluster model. Cluster-mean t-test is a simple baseline; wild-cluster bootstrap and crossed clustering remain future comparisons. No LLM agent, SEA runtime, or real market backtest was run.

## Next experiment
Add cluster_id to the SEA comparison report schema in a separate experimental branch, without silently changing the current evaluator. Validate paired task matching, cluster assignment integrity, and cluster-level aggregation on simulated and then human-annotated financial research tasks.
