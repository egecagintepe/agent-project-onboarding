# Progressive Disclosure Strategy (Token Efficiency)

One of the most common anti-patterns in AI agent engineering is loading excessive documentation into the agent's initial prompt context.

---

## The Failure Mode of "Prompt Dumping"

Dumping a 5,000-line documentation wiki into an agent's context window:
1. **Consumes Token Quota**: Leaves less room for source code, diffs, and test outputs.
2. **Dilutes Critical Instructions**: Models suffer from attention decay when instructions are buried in massive prose walls.
3. **Encourages Hallucination**: Agents attempt to solve multiple unrelated backlog items simultaneously.

---

## The Progressive Disclosure Tiering

Organize repository documentation into concentric rings of depth:

```
               ┌────────────────────────┐
               │ Level 1: Constitutional│ (AGENTS.md ~ 50 lines)
               └───────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │ Level 2: Project Radar │ (ARCHITECTURE_MAP & CURRENT_STATE)
               └───────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │ Level 3: Deep Runbooks │ (INCIDENT_RUNBOOK, DEPLOY_MATRIX)
               └────────────────────────┘ (Read ONLY when touching that subsystem)
```

### Level 1: Constitutional Contract (`AGENTS.md`)
- Kept under 80 lines.
- Summarizes invariants, verification commands, and reading order.

### Level 2: System Radar (`ARCHITECTURE_MAP.md`, `CURRENT_STATE.md`)
- Explains subsystem boundaries, active feature flags, and known broken modules.
- Read when orienting to a new sprint.

### Level 3: Deep Technical Runbooks (`INCIDENT_RUNBOOK.md`, `BUILD_DEPLOY_MATRIX.md`)
- Highly specialized operational details.
- Read **only** when the agent touches the specific domain (e.g. database migration, deployment, or incident recovery).
