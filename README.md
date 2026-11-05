<div align="center">

# Agent Project Onboarding

**Give every new AI coding agent the project context it actually needs.**

[![CI](https://github.com/egecagintepe/agent-project-onboarding/actions/workflows/ci.yml/badge.svg)](https://github.com/egecagintepe/agent-project-onboarding/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Agent Skills: v1](https://img.shields.io/badge/Agent%20Skills-v1.0-emerald.svg)](https://agentskills.io/specification)

*Multi-agent coordination framework and repository handoff protocol. Scans codebases, scaffolds honest 8-dossier contracts (AGENTS.md), and preserves production incident memory across AI agent sessions.*

```
   [ REPOSITORY ROOT ]
          │
          ├── AGENTS.md (Level 1: Universal Constitutional Contract ~ 60 lines)
          │
          └── docs/
               ├── ARCHITECTURE_MAP.md   (Level 2: System Wiring & Service Boundaries)
               ├── CURRENT_STATE.md      (Level 2: Honest Ledger: DETECTED vs VERIFIED)
               ├── MASTER_BACKLOG.md     (Level 2: Prioritized Single Source of Truth)
               ├── AGENT_ROUTING.md      (Level 3: Task Assignment by Risk Profile)
               ├── PRODUCTION_RUNBOOK.md (Level 3: Deploy & Verification Commands)
               ├── INCIDENT_RUNBOOK.md   (Level 3: "Happened Once, Never Again" Ledger)
               └── BUILD_DEPLOY_MATRIX.md(Level 3: Change-to-Action Impact Matrix)
```

</div>

---

## The Problem

When engineering teams collaborate with AI coding agents (Claude Code, Cursor, Codex, Gemini, Antigravity) across multiple sessions or tools:
1. **Context Fragmentation**: Every new agent session starts from zero. Critical rules, conventions, and operational boundaries are lost between prompts.
2. **Instruction Dilution (Prompt Saturation)**: Dumping 5,000 lines of documentation into an agent's initial prompt burns token budgets and dilutes attention, leading to hallucinations.
3. **Repeated Regressions**: New agents frequently repeat past production mistakes that were already diagnosed, suffered, and resolved by the team weeks earlier.
4. **Fabricated Status Reports**: Naive templates report "Core Backend: Healthy" or "Test Coverage: 100%" based on synthetic mocks without verifying live code.

---

## Quick Install (30 Seconds)

### Using Agent Skills CLI (`skills.sh`)
```bash
npx skills add egecagintepe/agent-project-onboarding
```

### Direct Agent Integration (Claude Code, Cursor, Codex)
```bash
git clone https://github.com/egecagintepe/agent-project-onboarding.git .agents/skills/agent-project-onboarding
```

### Standalone CLI Toolkit
```bash
git clone https://github.com/egecagintepe/agent-project-onboarding.git
cd agent-project-onboarding
```

---

## The 8-Dossier Architecture

`agent-project-onboarding` establishes a standardized, progressive-disclosure documentation package in any repository:

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

## Evidence-Based Status (No Fabricated Health)

Generated documentation strictly distinguishes verified facts from unverified static assumptions:

- `DETECTED`: Files or configurations exist in repository, but live behavior is unverified.
- `VERIFIED`: Confirmed operational via automated test execution or live smoke checks.
- `UNVERIFIED`: Detected in source code but currently lacking passing verification evidence.
- `UNKNOWN`: Cannot be determined from static repository inspection.
- `NOT_APPLICABLE`: Explicitly excluded or not part of this service.

Every unverified component is paired with an actionable `[TODO: VERIFY]` task.

---

## CLI Usage (`onboard_project.py`)

### 1. Scan Repository Architecture
Recursively inspects codebases to detect languages, frameworks, databases, and existing dossier coverage with concrete evidence:

```bash
python scripts/onboard_project.py scan --path /path/to/project
```

Output:
```text
=== Project Scan: /path/to/project ===
Languages:   Python, TypeScript
Frameworks:  Django, React
Databases:   PostgreSQL, Redis
Docker:      Yes
Dossier Coverage: 0.0% (0/8)

Detection Evidence:
  + Python: Detected .py files or Python dependency manifests
  + Django: Found 'manage.py' in repository root
  + PostgreSQL: Referenced in requirements.txt
  + Docker: Found Dockerfile or docker-compose file
```

### 2. Scaffold Onboarding Dossiers
Generate the complete 8-dossier scaffolding tailored to the detected stack. Non-destructive by default:

```bash
# Preview generation safely without writing files:
python scripts/onboard_project.py generate --path /path/to/project --project-name "Core Backend" --dry-run

# Execute scaffolding:
python scripts/onboard_project.py generate --path /path/to/project --project-name "Core Backend"
```

### 3. Audit Onboarding Integrity
Verifies all 8 dossiers exist, validates relative markdown links, and checks for accidental secret leakage:

```bash
python scripts/onboard_project.py audit-dossier --path /path/to/project
```

Output:
```text
=== Dossier Audit: PASS ===
All 8 dossiers exist, links resolve, and no secrets detected.
```

---

## Standard Task Brief Template

Assign tasks to AI agents with zero ambiguity using the standardized brief:

```markdown
## Task: <TITLE>

**Context**: docs/CURRENT_STATE.md §<section>
**Priority**: P0 / P1 / P2

**Problem**: <Exact symptom, bug description, or requested capability>
**Acceptance Criteria**:
- <Measurable condition 1>
- <Measurable condition 2>

**Touched Files**:
- path/to/file_a.py
- tests/test_file_a.py

**Inviolable Constraints**:
- Do not modify files outside the touched list.
- Do not introduce fake or stub data to make tests pass.
- Preserve existing comment headers and docstrings.

**Verification Command**:
```bash
python -m unittest tests/test_file_a.py
```
```

---

## Deep Documentation

- [Agent Contract Specification (`AGENTS.md`)](references/agent_contract_standard.md) — Constitutional rules
- [Progressive Disclosure Strategy](references/progressive_disclosure_strategy.md) — Token efficiency architecture
- [Model Routing Decision Matrix](references/agent_routing_matrix.md) — Matching task risk to agent strengths
- [Incident Ledger Methodology](references/incident_ledger_standard.md) — Post-mortem ledger standard
- [Standard Task Brief Format](references/task_brief_standard.md) — Bounded prompt handoff specification
- [Sample Task Briefs](examples/task_brief_examples.md) — Real-world prompt examples

---

## Verified Compatibility

| Environment | Supported | Notes |
|---|---|---|
| **Python** | 3.8, 3.9, 3.10, 3.11, 3.12 | Standard library only; zero external dependencies. |
| **Platforms** | Linux, macOS, Windows | Path traversal protection & cross-platform paths. |
| **Agent Skills** | Specification v1.0 | Validated with official `skills-ref validate`. |
| **AI Agents** | Claude Code, Cursor, Codex, Antigravity | Indexed via `SKILL.md` and root `AGENTS.md`. |

---

## Testing

Run the full automated test suite (14 tests):
```bash
python -m unittest discover -s tests
```

---

## License

This project is licensed under the [MIT License](LICENSE).
