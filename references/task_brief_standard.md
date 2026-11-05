# Standard Task Brief Specification

When delegating engineering work to an AI agent, ambiguity is the primary source of bugs and hallucinations. The Standard Task Brief provides a structured, predictable handoff format.

---

## 1. Specification Fields

1. **Title & Backlog Reference**: Ties the prompt to an explicit ID in `docs/MASTER_BACKLOG.md`.
2. **Context**: Specific documentation chapter or runbook section providing context.
3. **Problem Statement**: Factual, reproducible description of the symptom or missing feature.
4. **Acceptance Criteria**: Measurable conditions of success (e.g. status codes, return types, test passes).
5. **Touched Files**: Explicit list of files the agent is authorized to modify. Edits outside this list are forbidden.
6. **Inviolable Constraints**: Project-specific rules and forbidden actions.
7. **Verification Command**: The exact command the agent must run to prove completion.

---

## 2. Empty States and Negative Testing

A task brief should always clarify expected behavior when data is absent:
- "If user has no transactions, return HTTP 200 with `[]`, do NOT throw 500 or 404."
- "If external service times out, fall back to cached copy; do not crash the view."
