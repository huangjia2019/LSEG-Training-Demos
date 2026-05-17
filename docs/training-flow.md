# Training Flow

This flow is designed for a one-day LSEG engineering workshop.

## Morning: Run The Cases

Start from concrete demos before introducing the pattern vocabulary.

1. Run `workshop1-compliance`: regulatory document impact analysis.
2. Run `workshop2-ticket-review`: multi-agent ticket review.
3. Run `workshop3-copilot-demo`: spec-driven development with Copilot.

Each demo has a no-key path. If Azure OpenAI credentials are available, learners can switch from mock execution to model-backed execution by creating `.env` from `.env.example`.

## Afternoon: Pattern Selection

After learners see outputs, ask them to explain the architecture.

For each case:

1. What is the business boundary?
2. Which cognitive functions are dominant?
3. Which execution topology fits?
4. Which 2-3 patterns matter most?
5. What would block production deployment?

The target is not to name every pattern. The target is to choose a small, defensible pattern set.

## Instructor Demo Track

Use the showcase demos when the audience includes non-engineers or when a full local setup is too heavy.

- `showcases/finance/demo-doc-analysis`: best first-hour business demo.
- `showcases/finance/demo-MAS-analyst`: broader compliance manager use-case gallery.

## Suggested Time Boxes

| Segment | Time | Activity |
|---|---:|---|
| Setup | 15 min | Clone repo, create virtual env, run one demo |
| Workshop 1 | 35 min | Regulatory document analysis |
| Workshop 2 | 35 min | Multi-agent ticket review |
| Workshop 3 | 30 min | Copilot + SDD flow |
| Pattern card | 45 min | Group design discussion |
| Share-out | 30 min | Each group presents one architecture |

