# Re-Opt Critical Review And Direction Upgrade

Date: 2026-09-22

## Scope

This memo critiques the current Re-Opt idea against recent popular LLM-agent, multi-agent, workflow, planning, and benchmark papers. The goal is to turn Re-Opt from a neat local prototype into a research direction with a defensible contribution.

## Papers Checked In This Pass

Search queries used:

- "LLM multi-agent benchmark workflow planning scheduling"
- "agent workflow generation benchmark"
- "multi-agent LLM systems failure modes"
- "AutoML agent multi-agent workflow paper"
- "planning benchmark LLM agents"

Paper set:

| Paper | Year | What Re-Opt should learn |
| --- | ---: | --- |
| AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | 2023 | Multi-agent work needs programmable conversation/control patterns, not only role labels. |
| MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework | 2023/2024 | Structured artifacts and standard operating procedures reduce cascading ambiguity. |
| ChatDev: Communicative Agents for Software Development | 2023/2024 | End-to-end workflows can be compelling, but reviewers will ask whether the workflow generalizes beyond the demo domain. |
| AgentBench: Evaluating LLMs as Agents | 2023 | Agent papers need diverse environments and failure-mode reporting. |
| SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | 2023/2024 | Real-world tasks plus objective tests are much stronger than handcrafted examples. |
| WebArena: A Realistic Web Environment for Building Autonomous Agents | 2023/2024 | Reproducible environments matter; task success must be grounded in functional correctness. |
| GAIA: A Benchmark for General AI Assistants | 2023/2024 | Good benchmarks have unambiguous answers but require tool use, reasoning, and multi-step work. |
| MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents | 2025 | Multi-agent evaluation should measure collaboration quality, not only final task score. |
| REALM-Bench: A Real-World Planning Benchmark for LLMs and Multi-Agent Systems | 2025 | Planning/scheduling domains already exist; Re-Opt must either reuse them or explain why its graph-scheduling benchmark differs. |
| MLGym: A New Framework and Benchmark for Advancing AI Research Agents | 2025 | Research-agent evaluation needs open-ended tasks but still requires a controlled environment and repeatable scoring. |
| AutoML-Agent: A Multi-Agent LLM Framework for Full-Pipeline AutoML | 2025 | A domain-specialized multi-agent pipeline can be publishable when it has a complete task pipeline and serious baselines. |
| Why Do Multi-Agent LLM Systems Fail? | 2025 | Re-Opt needs failure-mode mitigation, especially specification errors, inter-agent misalignment, verification, and termination. |
| WorFBench: Benchmarking Agentic Workflow Generation | 2025 | Workflow graph generation is already a benchmarked problem; Re-Opt should not pretend workflow graphs are unexplored. |
| NESTFUL: A Benchmark for Nested Sequences of API Calls | 2025 | Agent orchestration breaks on dependency chains; Re-Opt should track dataflow, not only prerequisite order. |
| Agent Planning Benchmark | 2026 | Planning failures should be separated from execution failures; Re-Opt should evaluate scheduler quality independently of agent execution. |

Reference links:

- AutoGen: https://arxiv.org/abs/2308.08155
- MetaGPT: https://arxiv.org/abs/2308.00352
- ChatDev: https://arxiv.org/abs/2307.07924
- AgentBench: https://arxiv.org/abs/2308.03688
- SWE-bench: https://arxiv.org/abs/2310.06770
- WebArena: https://arxiv.org/abs/2307.13854
- GAIA: https://arxiv.org/abs/2311.12983
- MultiAgentBench: https://aclanthology.org/2025.acl-long.421/
- REALM-Bench: https://arxiv.org/abs/2502.18836
- MLGym: https://arxiv.org/abs/2502.14499
- AutoML-Agent: https://proceedings.mlr.press/v267/trirat25a.html
- Why Do Multi-Agent LLM Systems Fail?: https://arxiv.org/abs/2503.13657
- WorFBench: https://arxiv.org/abs/2410.07869
- NESTFUL: https://arxiv.org/abs/2409.03797
- Agent Planning Benchmark: https://arxiv.org/abs/2606.04874

## Honest Critique Of The Current Re-Opt Idea

### 1. The current novelty is too soft

The current pitch says multi-agent task delegation is a constrained graph scheduling problem. That is sensible, but by itself it is not enough. AutoGen, MetaGPT, ChatDev, and LangGraph-like systems already make workflow structure explicit, while WorFBench and APB directly benchmark workflow/planning generation.

What is weak:

- "Represent task as graph" is not novel enough.
- "Use A* / critical path inspiration" can sound like metaphor rather than algorithm.
- The current priority formula is handcrafted and lightly justified.
- The system optimizes a schedule, but does not yet prove that schedule quality predicts task outcome.

Fix:

Make the contribution narrower and sharper:

> Re-Opt separates workflow planning from workflow execution and optimizes the cost-quality-risk frontier of multi-agent task graphs under budget constraints.

The paper should be about budgeted orchestration, not merely multi-agent decomposition.

### 2. The benchmark is the real missing paper

The current seed benchmarks are useful engineering fixtures, but they are too small and too authored-by-us. Reviewers will not trust claims drawn from three synthetic graphs.

What is weak:

- No external dataset.
- No human-authored benchmark card.
- No held-out task set.
- No repeated stochastic runs.
- No grader beyond internal utility estimates.

Fix:

Create `ReOptBench`, a benchmark of task-graph scheduling instances:

- 50-100 task graphs converted from real agent workloads.
- Each graph has nodes, dependencies, dataflow, optional nodes, risk labels, verification nodes, token/time budgets, and a grader.
- Separate "planning-only" evaluation from "execution" evaluation.
- Include graphs derived from SWE-bench Lite, GAIA, WebArena, MultiAgentBench, REALM-Bench, and MLGym tasks.

If that is too large, start with 20 pilot tasks and present the paper as a benchmark/system workshop paper.

### 3. Re-Opt currently ignores communication failure

Multi-agent systems often fail at handoffs: missing assumptions, stale shared state, premature agreement, and weak termination. The current Re-Opt graph tracks dependencies, but not information quality.

What is weak:

- Edges only mean prerequisite ordering.
- There is no formal handoff artifact.
- There is no communication budget or context compression cost.
- There is no check for whether a downstream agent received enough state.

Fix:

Upgrade the graph from a task DAG to an artifact/dataflow DAG:

```text
node = work unit
edge = artifact contract
artifact = schema + producer + consumer + validation check + context size
```

Then optimize:

```text
quality - execution_cost - latency - communication_cost - verification_cost - failure_risk
```

This makes Re-Opt more distinctive: it is not just "who does what"; it is "what exact artifact crosses the boundary, and what does it cost to verify?"

### 4. The method needs baselines that are embarrassing if omitted

If Re-Opt only compares against itself, the paper will not survive. Existing papers have trained reviewers to expect clear, compute-matched baselines.

Must-have baselines:

- single-agent linear execution;
- fixed role pipeline;
- random valid topological order;
- greedy topological order by value/cost;
- critical-path-only scheduler;
- planner-only LLM that writes a workflow without optimization;
- AutoGen or LangGraph fixed workflow baseline;
- Re-Opt without budget pruning;
- Re-Opt without verifier nodes;
- Re-Opt without communication-cost terms.

The strongest result would not be "Re-Opt wins every task." A more believable result is:

> Re-Opt improves quality-per-token and budget compliance on large/ambiguous tasks, while fixed or single-agent workflows remain better for small tasks.

### 5. The learning loop is under-evidenced

The current outcome/intake/weight adoption machinery is interesting, but right now it is not learning enough to justify itself as a central contribution.

What is weak:

- Updates come from too few outcomes.
- Synthetic evidence and observed evidence are separated, which is good, but the paper needs many real observed outcomes.
- Utility weights are hard to interpret without calibration plots.

Fix:

Demote the learning loop in the first paper unless you can gather enough runs. Use it as an ablation:

- fixed handcrafted weights;
- grid-searched weights on validation tasks;
- outcome-calibrated weights;
- per-domain weights.

Report calibration:

- predicted utility vs observed score;
- budget violation prediction;
- whether learned weights transfer to held-out task families.

### 6. The name risks sounding like generic optimization

"Re-Opt" is pleasant, but the paper title should carry the actual claim. Reviewers should know the paper is about budgeted orchestration before reading the abstract.

Better titles:

- "Budgeted Orchestration of LLM Multi-Agent Workflows via Task-Graph Scheduling"
- "ReOptBench: Evaluating Cost-Aware Scheduling for LLM Multi-Agent Workflows"
- "When More Agents Are Not Enough: Budget-Aware Scheduling for Multi-Agent LLM Workflows"

If the benchmark is strong, lead with `ReOptBench`. If the algorithm is strong, lead with budgeted orchestration.

## Better Research Direction

The improved direction should be:

> Build a benchmark and scheduler for cost-aware orchestration of LLM multi-agent workflows, where the input is a task/artifact graph and the output is an execution plan that decides role assignment, ordering, communication artifacts, pruning, and verification under token/time budgets.

This direction has a cleaner gap:

- Existing frameworks make multi-agent workflows easier to build.
- Existing benchmarks evaluate agent execution or planning.
- Fewer works isolate the scheduler/orchestrator as the object being optimized under explicit cost, risk, artifact, and verification constraints.

## V2 System Design

### Graph

Use a typed graph:

```text
TaskNode:
  id
  type: discover | build | verify | synthesize | decide | memory
  required: bool
  expected_value
  risk
  uncertainty
  token_cost_estimate
  time_cost_estimate
  allowed_roles
  verifier_required

ArtifactEdge:
  from
  to
  schema
  context_tokens
  validation
  freshness
```

### Scheduler

Implement four scheduler families:

- fixed pipeline;
- greedy value/cost;
- critical-path budgeted scheduler;
- Re-Opt scheduler with communication and verification costs.

Optional later:

- beam search over schedules;
- contextual bandit for role assignment;
- learned utility model from run traces.

### Evaluation Split

Separate:

- planning-only: does the scheduler produce a valid, budget-feasible plan?
- execution: does the selected plan improve outcome with real agents?
- robustness: what happens when tools fail, artifacts are stale, or optional tasks are pruned?

This follows APB's lesson: do not mix planning failure and execution failure into one opaque number.

## Experimental Plan

Pilot:

- 20 tasks;
- 4 task families: coding, web/tool-use, research synthesis, data/ML workflow;
- 4 schedulers;
- 3 repeated runs per scheduler/task;
- same model, same tool set, same budget.

Main:

- 50-100 tasks;
- train/validation/test split for weight calibration;
- compare against one external framework baseline;
- release graph JSON, prompts, configs, raw trajectories, and graders.

Metrics:

- final task score;
- quality per 1k tokens;
- quality per minute;
- budget violation rate;
- communication overhead;
- verifier catch rate;
- artifact contract violation rate;
- scheduler invalid-plan rate;
- optional-value missed.

## Positioning Against The Literature

Against AutoGen:

- AutoGen is a programmable multi-agent conversation framework.
- Re-Opt should be a scheduler/evaluator that can choose or prune orchestration plans.

Against MetaGPT/ChatDev:

- They encode domain workflows.
- Re-Opt should optimize workflow structure under explicit constraints and show when domain SOPs are too expensive.

Against AgentBench/WebArena/GAIA/SWE-bench:

- They evaluate agent capability on tasks.
- Re-Opt should use them as task sources or downstream environments, not compete as a general ability benchmark.

Against MultiAgentBench/REALM-Bench:

- They evaluate multi-agent collaboration/planning.
- Re-Opt should focus on orchestration cost, artifact contracts, and budgeted scheduling.

Against WorFBench/APB/NESTFUL:

- They diagnose workflow generation, planning, and nested tool use.
- Re-Opt should explicitly separate planner quality, schedule validity, artifact dataflow, and execution outcome.

## What To Change In The Re-Opt Repo

Priority changes:

1. Add a task graph JSON schema.
2. Add `ArtifactEdge` or equivalent dataflow/contract representation.
3. Add benchmark loader for external task graphs.
4. Add planning-only validators.
5. Add baseline schedulers.
6. Add run logger for tokens, time, artifacts, role calls, and verifier outcomes.
7. Add benchmark cards for every task.
8. Add a CLI that runs a scheduler matrix and emits a paper-ready results table.

Avoid for now:

- claiming self-improving memory as the main contribution;
- using only synthetic outcomes;
- adding more roles before fixing evaluation;
- overfitting the scheduler to three seed graphs.

## Stronger Abstract Shape

Current abstract would probably sound too speculative. A stronger version:

> Multi-agent LLM systems often improve coverage on complex tasks, but fixed collaboration workflows waste tokens, violate budgets, and fail at handoffs. We study multi-agent orchestration as a budgeted task-graph scheduling problem. We introduce ReOptBench, a benchmark of task and artifact graphs derived from coding, web, research, and ML-agent workloads, and Re-Opt, a cost-aware scheduler that assigns roles, orders tasks, prunes optional work, and reserves verification budget. Across N tasks and M repeated runs, Re-Opt improves quality-per-token by X% and reduces budget violations by Y% over fixed role pipelines, with the largest gains on high-uncertainty tasks. Ablations show that artifact contracts and verifier reservation account for most of the improvement, while small tasks favor simpler single-agent execution.

This shape has falsifiable claims and leaves room for negative results.

## Bottom Line

The original idea is promising, but too broad and too under-evaluated. The best upgrade is to stop pitching Re-Opt as "multi-agent optimization in general" and turn it into:

> a benchmark-backed, budget-aware orchestration scheduler for task/artifact graphs.

That gives the project a clearer novelty boundary, stronger baselines, and a natural route to an arXiv/workshop paper first, then AutoML/AAMAS/TMLR if the benchmark and results hold.
