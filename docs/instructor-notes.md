# Instructor Notes

## Which Demo Is Newest?

The A*STAR `demo-doc-analysis` showcase is newer than `demo-MAS-analyst`.

- `demo-MAS-analyst`: earlier V1-style compliance manager gallery.
- `demo-doc-analysis`: newer five-step regulatory document pipeline with stronger persona, traceability, and explainability.

For the first hour of a general audience briefing, use `demo-doc-analysis`.

## Which Demo Should Learners Run?

Use the three `workshops/` folders.

They are smaller, CLI-based, and already include mock fallback behavior. This reduces workshop risk because participants can see the full flow without API keys.

## Mapping To Design Patterns

| Workshop | Pattern Teaching Point |
|---|---|
| `workshop1-compliance` | Compliance agents need citations, quality gates, and human review. The architecture is not just RAG; it is RAG plus governance. |
| `workshop2-ticket-review` | Multi-agent does not mean free-form chat. Each agent has a narrow contract and passes structured JSON. |
| `workshop3-copilot-demo` | Spec-driven development makes the same document drive Copilot, system prompts, and validation. |

## Production Reality Check

Ask learners to separate four levels:

1. **Demo works**: can run locally and show mock outputs.
2. **Prototype works**: calls Azure OpenAI and handles real samples.
3. **Pilot works**: integrates with internal documents, identity, and audit logs.
4. **Production works**: monitored, reversible, governed, and owned by a team.

Most agent projects fail by jumping from level 1 to level 4 in their imagination. The pattern card is the forcing function that slows that jump down.

