---
name: agent-project-onboarding
description: Multi-agent coordination and repository handoff framework. Scans codebases, scaffolds evidence-based 8-dossier contracts (AGENTS.md), organizes progressive disclosure documentation, routes tasks based on risk, and preserves production incident memory across AI agent sessions.
---

# Agent Project Onboarding

An open-source methodology, skill, and automation framework designed to eliminate the primary failure mode of AI coding agents: **context fragmentation, undocumented conventions, and uncoordinated drift across agent sessions**.

Whether collaborating with Claude Code, OpenAI Operator / Codex, Google Antigravity / Gemini, Cursor, or human engineers, this skill establishes an authoritative, vendor-neutral **Handoff Dossier** that keeps all agents grounded in project reality.

---

## Core Philosophy: Minimizing Context Fragmentation

1. **Independent of Model Memory**: A project must never rely on an LLM's transient chat memory or vendor-specific agent state. The Git repository is the sole durable source of truth.
2. **Progressive Disclosure (Token Efficiency)**: Do not dump thousands of lines of documentation into an agent's initial prompt context. Provide a concise, authoritative contract (`AGENTS.md`) with indexed pointers to modular dossiers.
3. **Evidence-Based Accounting of State**: Never allow agents to report "healthy" based on synthetic mock data. Maintain an explicit `CURRENT_STATE.md` with honest statuses (`DETECTED`, `VERIFIED`, `UNVERIFIED`, `UNKNOWN`, `NOT_APPLICABLE`).
4. **Memory of Past Incidents**: Record historical production failures in an append-only ledger (`INCIDENT_RUNBOOK.md`) so that new agents do not repeat known traps.
5. **Deterministic Routing**: Route mechanical edits, migrations, UX decisions, and security tasks to the model or human best suited for that risk profile.

---

## The 8-Dossier Architecture

Every on-boarded project maintains a standardized documentation bundle:

| # | Dossier | File Path | Purpose |
|---|---|---|---|
| **1** | **Agent Contract** | `AGENTS.md` | Core universal contract: permanent workspace, forbidden operations, test policy, token efficiency. |
| **2** | **Architecture Map** | `docs/ARCHITECTURE_MAP.md` | Discovered system components, top-level layout, and service boundaries. |
| **3** | **Current State** | `docs/CURRENT_STATE.md` | Honest audit of feature readiness, known broken modules, and active feature flags. |
| **4** | **Master Backlog** | `docs/MASTER_BACKLOG.md` | Prioritized single source of truth for work items (P0 to P3), acceptance criteria, and owners. |
| **5** | **Agent Routing Guide** | `docs/AGENT_ROUTING.md` | Decision matrix mapping task categories to agent models or human operators. |
| **6** | **Production Runbook** | `docs/PRODUCTION_RUNBOOK.md` | Step-by-step deploy, rollback, and verification commands. |
| **7** | **Incident Ledger** | `docs/INCIDENT_RUNBOOK.md` | "Happened Once, Never Again" post-mortems and symptom-to-remedy runbooks. |
| **8** | **Build & Deploy Matrix**| `docs/BUILD_DEPLOY_MATRIX.md` | "If I modify file X, what must I build, test, migrate, or restart?" |

---

## Structured Task Brief Format

When assigning tasks to an agent, use the standardized brief template to prevent hallucinations and scope creep:

````markdown
## Task: <TITLE>

**Context**: docs/CURRENT_STATE.md §<section>
**Priority**: P0 / P1 / P2

**Problem**: <Exact symptom, bug description, or requested capability>
**Acceptance Criteria**:
- Route / function X returns Y
- Unit test Z passes
- No regression in existing module W

**Touched Files**:
- path/to/target_file.py
- tests/test_target.py

**Inviolable Constraints**:
- Do not modify files outside the touched list.
- Do not introduce fake or stub data to make tests pass.
- Preserve existing comment headers and docstrings.

**Verification Command**:
```bash
python -m unittest tests/test_target.py
```
````

---

## CLI Automation (`scripts/onboard_project.py`)

### 1. Scan Repository Architecture
Inspect any codebase to detect languages, frameworks, databases, and existing documentation with evidence:
```bash
python scripts/onboard_project.py scan --path /path/to/project
```

### 2. Scaffold Onboarding Dossiers
Generate the complete 8-dossier scaffolding tailored to the detected stack (supports `--dry-run` and `--force`):
```bash
# Preview generation safely:
python scripts/onboard_project.py generate --path /path/to/project --project-name "my-service" --dry-run

# Execute scaffolding:
python scripts/onboard_project.py generate --path /path/to/project --project-name "my-service"
```

### 3. Audit Existing Onboarding Integrity
Verify that an existing project's documentation has no broken cross-references, missing required sections, or secret leaks:
```bash
python scripts/onboard_project.py audit-dossier --path /path/to/project
```

---

## Detailed References

- [Agent Contract Specification (`AGENTS.md`)](references/agent_contract_standard.md)
- [Progressive Disclosure Strategy](references/progressive_disclosure_strategy.md)
- [Model Routing Decision Matrix](references/agent_routing_matrix.md)
- [Incident Ledger Methodology](references/incident_ledger_standard.md)
- [Standard Task Brief Format](references/task_brief_standard.md)
- [Sample Task Briefs](examples/task_brief_examples.md)
