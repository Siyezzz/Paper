# Re-Opt Paper Roadmap

Date: 2026-09-22

## Repository Snapshot

Re-Opt currently frames multi-agent task delegation as a constrained task-graph scheduling problem. The codebase contains:

- a graph model for task nodes, dependencies, agent roles, and constraints;
- `critical-path-a-star-v0`, an inspectable priority scheduler;
- `budget-pruning-v0`, a constrained variant that drops optional work;
- seed benchmark graphs for coding/debugging and research synthesis tasks;
- regression, outcome intake, adoption review, and weight calibration utilities;
- 34 unit tests passing with the bundled Codex Python runtime.

This is a plausible research prototype, but not yet a publishable empirical paper. The missing piece is not code volume; it is external validation.

## Best Paper Framing

Working title:

> Re-Opt: Budget-Aware Task-Graph Scheduling for LLM Multi-Agent Workflows

Core claim to aim for:

> Representing LLM-agent collaboration as a task graph with explicit costs, risks, dependencies, and verification nodes can reduce wasted coordination and improve quality-per-token under realistic task budgets.

What should be novel:

- task delegation is optimized before execution instead of hand-designed as a fixed workflow;
- quality, cost, latency, risk, optional work, and verification are all first-class scheduling signals;
- the system updates scheduling weights from observed task outcomes while separating synthetic probes from real evidence;
- the paper evaluates not only success rate, but also token efficiency, time, and coordination overhead.

## Related Work Streams

Use these as the first literature map:

- LLM agents and planning: task decomposition, plan selection, memory, reflection, and tool use.
- LLM multi-agent systems: role specialization, orchestration patterns, communication protocols, and collaboration failure modes.
- Agent workflow frameworks: AutoGen, MetaGPT, LangGraph, CrewAI-style graph or role pipelines.
- Agent benchmarks: AgentBench, GAIA, WebArena, SWE-bench, MultiAgentBench, REALM-Bench, MLGym, BrowserGym, Terminal-Bench.
- Classical scheduling and planning: critical path, A*, branch-and-bound, DAG scheduling, online scheduling, multi-armed bandits.
- AutoML and automated workflow optimization: pipeline search, configuration selection, learning from task outcomes.

Useful starting sources:

- AgentBench: https://github.com/THUDM/AgentBench
- MultiAgentBench: https://aclanthology.org/2025.acl-long.421/
- AutoML-Agent, ICML 2025: https://proceedings.mlr.press/v267/trirat25a.html
- TMLR scope and policies: https://www.jmlr.org/tmlr/editorial-policies.html
- AutoML 2026 call for papers: https://2026.automl.cc/call-for-papers/

## What Other Papers Usually Include

A credible systems/ML paper in this area usually has:

- a crisp problem definition with variables, objective, and constraints;
- a method section with algorithm pseudocode and complexity/behavior discussion;
- baselines that include single-agent, fixed multi-agent workflow, random/greedy scheduling, and the strongest relevant framework baseline;
- benchmark tasks that are not authored only by the method designer;
- repeated runs because LLM-agent performance is stochastic;
- ablations showing which component matters;
- cost analysis, not only accuracy;
- failure analysis with concrete examples;
- released code, configs, prompts, model versions, and run logs.

## Datasets And Benchmarks Needed

Minimum viable benchmark:

- 30-50 task graphs derived from real agent tasks, split into coding, research, data analysis, document synthesis, and tool-use tasks.
- For each task: dependency graph, required artifacts, optional artifacts, token budget, time budget, evaluator, and expected quality criteria.
- At least 3 repeated runs per condition to estimate variance.

Stronger benchmark:

- Map existing tasks from SWE-bench Lite, GAIA, WebArena, AgentBench, MultiAgentBench, and REALM-Bench into Re-Opt graph format where possible.
- Add a public "Agent Workflow Scheduling" benchmark: JSON task graphs plus graders.
- Include both open-model and closed-model runs if budget allows.

Avoid relying only on the current seed benchmarks. They are good unit-test fixtures, but reviewers will see them as toy examples.

## Baselines

Use these baseline families:

- Single-agent linear execution with the same model and budget.
- Fixed role pipeline: Decomposer -> Researcher/Builder -> Critic -> Verifier -> Synthesizer.
- Topological greedy scheduler without risk/value weighting.
- Random valid topological scheduler.
- Critical-path-only scheduler.
- Budget-pruning scheduler without learned weights.
- Existing orchestration framework configured with comparable roles, such as AutoGen, LangGraph, CrewAI, or MetaGPT, if practical.

## Metrics

Primary metrics:

- task success or grader score;
- quality per 1k tokens;
- quality per minute;
- budget violation rate;
- wall-clock latency;
- number of failed or redundant subtasks;
- verifier-detected defect rate;
- missed optional value.

Secondary metrics:

- coordination overhead tokens;
- context-sharing overhead;
- stability across repeated runs;
- sensitivity to model choice;
- calibration error between predicted utility and observed outcome.

## Ablations

Run at least:

- no critical-path blocking score;
- no risk term;
- no uncertainty term;
- no budget pruning;
- no verifier reservation;
- fixed weights vs learned/calibrated weights;
- synthetic evidence only vs observed evidence only vs mixed evidence;
- small-task vs large-task split to test whether coordination overhead dominates.

## Venue Strategy

Most realistic path:

1. arXiv preprint once the benchmark and experimental section are honest.
2. AutoML if the framing emphasizes workflow/pipeline automation and adaptive configuration. AutoML 2026 explicitly lists pipeline automation topics.
3. AAMAS if the paper emphasizes multi-agent coordination, role assignment, and collaboration protocols.
4. TMLR if the paper has solid empirical validation and you want rolling review rather than a fixed conference deadline.
5. ICLR/ICML/NeurIPS only if the benchmark and results are much stronger, with broad significance beyond this prototype.

Workshop targets are also sensible before a main-track push: LLM agents, AutoML, planning, systems for ML, or agent evaluation workshops.

## Recommended Paper Structure

1. Introduction: why multi-agent workflows need optimization rather than fixed recipes.
2. Problem formulation: task graph, agents, constraints, objective.
3. Method: Re-Opt scheduler, role assignment, budget pruning, outcome update loop.
4. Benchmark: task graph construction, datasets, graders, models, budgets.
5. Experiments: main comparison, cost-quality frontier, ablations, robustness.
6. Analysis: when Re-Opt helps, when overhead hurts, failure cases.
7. Related work.
8. Limitations: task graph authoring cost, model dependence, evaluator bias, privacy/cost issues.
9. Conclusion.

## Immediate Next Steps

1. Freeze the current code as the seed algorithm.
2. Define a JSON schema for external benchmark task graphs.
3. Build 10 pilot tasks and run single-agent vs fixed-pipeline vs Re-Opt.
4. Add automatic logging of prompt tokens, completion tokens, wall-clock time, and artifacts.
5. Write a short "benchmark card" for every task.
6. Expand to 30-50 tasks only after the pilot exposes evaluator and logging problems.
7. Start the paper as a technical report while experiments run.

## Direction Upgrade After Literature Critique

After comparing against recent multi-agent, planning, workflow, and benchmark papers, the strongest version of this project is narrower:

> budget-aware orchestration of LLM multi-agent workflows via typed task/artifact graph scheduling.

The key change is to treat edges as artifact contracts, not just prerequisite links. Re-Opt should optimize task order, role assignment, optional-task pruning, communication cost, and verification budget together. This makes the work less like a generic multi-agent framework and more like a scheduler/evaluator that can sit underneath frameworks such as AutoGen, MetaGPT-like pipelines, or LangGraph-style workflows.

See `research/re-opt-critical-review.md` for the full critique and upgraded experimental plan.

## Go / No-Go Criteria

Go for arXiv/workshop when:

- Re-Opt beats fixed baselines on quality-per-token or quality-per-minute in at least two task families;
- results are stable over repeated runs;
- ablations show that graph/risk/budget components matter;
- all prompts, configs, task graphs, and logs are reproducible.

Go for AutoML/AAMAS/TMLR when:

- benchmark is public or at least fully specified;
- baselines include one strong framework or external method;
- failure analysis is concrete and balanced;
- claims are modest enough to survive reviewer scrutiny.

Do not submit to a top ML venue yet if the evidence is still only the three seed benchmarks in `reopt.benchmarks`.
