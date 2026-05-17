# Pattern Selection Card

Use this card after a demo runs successfully. The goal is to turn "the code works" into "we understand why this architecture works".

## 1. Scenario Boundary

- User:
- Trigger:
- Input artifacts:
- Output artifact:
- Failure cost:
- Human reviewer:

## 2. Cognitive Function

Choose the dominant cognitive functions:

- Perception: ingest, parse, normalize, triage.
- Memory: retrieve, preserve, summarize, learn from history.
- Reasoning: compare, classify, plan, hypothesize.
- Action: call tools, write reports, trigger workflows.
- Reflection: critique, self-check, repair, replay experience.
- Collaboration: split work across agents or people.
- Governance: approve, audit, constrain, monitor.

## 3. Execution Topology

Choose the topology:

- Chain: one step after another.
- Route: classify then send to different paths.
- Parallel: run independent checks at the same time.
- Orchestrate: one controller manages multiple tools/agents.
- Loop: retry, self-check, or repair until a condition is met.
- Hierarchy: manager-worker structure.

## 4. Candidate Patterns

Pick 2-3 patterns only.

| Pattern | Why this pattern | What it prevents | Tradeoff |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

## 5. Production Gate

Before deployment, answer:

- What source citations are required?
- Which actions need human approval?
- What must be logged for audit?
- What is the rollback path?
- What is the cost / latency budget?
- How will we detect silent degradation?

## 6. Final Architecture Sketch

Write the final architecture in one paragraph:

> This system uses ___ as the main cognitive function and ___ as the execution topology. The core pattern combination is ___ + ___ + ___. Human review is inserted at ___. The main production risk is ___, so we add ___ before deployment.

