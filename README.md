# LSEG Agent Training Demos

Training demos for the LSEG / Refinitiv AI Agent workshop.

The repo has three layers:

1. **Runnable workshops**: small Python projects that learners can download, install, and run locally.
2. **Visual walkthroughs**: static HTML pages and blueprint PNGs that explain the same workshops step by step.
3. **Showcase demos**: richer Streamlit demos for instructor walkthroughs, screenshots, and follow-up sessions.

All runnable workshops include a no-key demo path. Azure OpenAI keys are optional for deeper exercises.

## Quick Start

```bash
git clone https://github.com/huangjia2019/LSEG-Training-Demos.git
cd LSEG-Training-Demos
```

Run one workshop:

```bash
cd workshops/workshop1-compliance
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

The same pattern works for `workshop2-ticket-review` and `workshop3-copilot-demo`.

Open the visual walkthrough for the same case:

```bash
open ../visual/index.html
```

Or open these files directly in a browser:

- `workshops/workshop1-compliance/visual/index.html`
- `workshops/workshop2-ticket-review/visual/index.html`
- `workshops/workshop3-copilot-demo/visual/index.html`

## What To Run In Class

| Case | Folder | Best Use | Main Patterns |
|---|---|---|---|
| Regulatory document analysis | `workshops/workshop1-compliance` | Morning hands-on: run a spec-driven compliance agent | RAG Pipeline, Semantic Compaction, Approval Gate, Observability Harness |
| Multi-agent ticket review | `workshops/workshop2-ticket-review` | Afternoon architecture discussion: agent responsibilities and risk routing | Handoff Chain, Fan-out/Gather, Adversarial Review, Approval Gate |
| Copilot + SDD meeting agent | `workshops/workshop3-copilot-demo` | Copilot workflow: spec → prompt → code → validation | Prompt Chaining, Skill Package, Progressive Commitment |
| MAS document analysis pipeline | `showcases/finance/demo-doc-analysis` | Instructor demo / screenshots / general audience briefing | Context Triage, RAG Pipeline, Progress Tracking, Human-in-the-loop Review |
| MAS compliance analyst agent | `showcases/finance/demo-MAS-analyst` | Broader finance use-case gallery | Tool Dispatch, Product Mapping, Compliance Gate |

## Web Walkthrough

The public case library has a finance landing page and one page per demo:

- https://kage-ai.com/training/finance/
- https://kage-ai.com/zh/cases/finance/

Use these pages when a live local run is not convenient. They include run commands, flow diagrams, screenshots, and pattern mappings for each demo.

The repo also includes local visual walkthrough pages. They are useful when you want to inspect the architecture without a web server:

- `workshops/workshop1-compliance/visual/index.html`
- `workshops/workshop2-ticket-review/visual/index.html`
- `workshops/workshop3-copilot-demo/visual/index.html`

## Recommended Workshop Flow

1. **Run** one of the runnable workshops locally.
2. **Observe** the pipeline output and quality gates.
3. **Map** the implementation to the pattern matrix.
4. **Select** 2-3 patterns using the pattern selection card.
5. **Discuss** what additional governance is needed before production.

See:

- `docs/training-flow.md`
- `docs/pattern-selection-card.md`

## Assets

The `assets/` folder contains diagrams for slides and the website:

- `finance-training-cases.png`
- `regulatory-document-agent-flow.png`
- `ticket-review-multi-agent-flow.png`
- `sdd-copilot-loop.png`
- `pattern-selection-card-flow.png`
- `agent-pattern-matrix-black.png`
- `visual/workshop-ladder-blueprint.png`
- `visual/workshop1-pattern-blueprint.png`
- `visual/workshop2-pattern-blueprint.png`
- `visual/workshop3-pattern-blueprint.png`
- `visual/mas-document-analysis-blueprint.png`
- `visual/mas-compliance-analyst-blueprint.png`
- `screenshots/*.png`

## Source Library

This learner package is curated from the private long-term demo library:

`huangjia2019/training-demo-private`
