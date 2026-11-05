# Agent Project Onboarding

[![CI Status](https://github.com/egecagintepe/agent-project-onboarding/actions/workflows/ci.yml/badge.svg)](https://github.com/egecagintepe/agent-project-onboarding/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Zero-loss AI agent handoff, onboarding, and multi-agent coordination protocol.

It provides an open-source methodology and CLI toolkit to scan codebases, generate standardized 8-dossier contracts (`AGENTS.md`), structure progressive disclosure documentation, route tasks to optimal AI models, and preserve production incident memory across AI agent sessions (Claude Code, Cursor, Codex, Gemini, Antigravity).

---

## The Problem: AI Agent Drift & Memory Loss

When teams collaborate with AI coding agents across multiple sessions or tools:
- **No Shared Memory**: LLM sessions start from scratch with zero memory of past constraints or decisions.
- **Prompt Token Saturation**: Dumping massive wikis into prompt context burns token quotas and causes attention decay.
- **Repeated Regressions**: New agents frequently repeat past production mistakes that were already diagnosed and solved weeks ago.
- **Model Mismatch**: Assigning complex database migrations or architecture decisions to lightweight models leads to outages.

---

## The Solution: The 8-Dossier Architecture

`agent-project-onboarding` establishes a standardized, progressive-disclosure documentation package in every repository:

```
[Repository Root]
├── AGENTS.md                   # Universal constitutional contract (Invariants, test policy)
└── docs/
    ├── ARCHITECTURE_MAP.md     # How the system is actually wired (subsystems, services)
    ├── CURRENT_STATE.md        # Honest status ledger (what works vs broken vs stubbed)
    ├── MASTER_BACKLOG.md       # Prioritized single source of truth for all work items
    ├── AGENT_ROUTING.md        # Model decision matrix (which agent handles which task)
    ├── PRODUCTION_RUNBOOK.md   # Authoritative deploy, rollback, and verification steps
    ├── INCIDENT_RUNBOOK.md     # "Happened Once, Never Again" post-mortem ledger
    └── BUILD_DEPLOY_MATRIX.md  # "If I modify file X, what must I build/migrate/restart?"
```

---

## Installation & Setup

### 1. As an AI Agent Skill (Claude Code, Cursor, Antigravity)

Clone or symlink into your agent skills directory:

```bash
git clone https://github.com/egecagintepe/agent-project-onboarding.git .agents/skills/agent-project-onboarding
```

Compatible agents will automatically index `SKILL.md` to guide onboarding new codebases and formatting handoff prompts.

### 2. Standalone CLI Toolkit

```bash
git clone https://github.com/egecagintepe/agent-project-onboarding.git
cd agent-project-onboarding
```

---

## CLI Usage (`onboard_project.py`)

### 1. Scan Repository Architecture
Inspect any codebase to identify languages, frameworks, databases, and existing dossier coverage:

```bash
python scripts/onboard_project.py scan --path /path/to/my-project
```

Sample output:
```
=== Project Scan: /path/to/my-project ===
Languages:   Python, TypeScript
Frameworks:  Django, React
Databases:   PostgreSQL, Redis
Docker:      Yes
Dossier Coverage: 0.0% (0/8)
```

### 2. Scaffold Standardized 8-Dossier Framework
Automatically generate customized `AGENTS.md` and `docs/` dossiers tailored to the detected stack:

```bash
python scripts/onboard_project.py generate --path /path/to/my-project --project-name "E-Commerce Core"
```

### 3. Audit Onboarding Integrity
Verify that all 8 dossiers exist, internal markdown links resolve, and no secrets or tokens are leaked:

```bash
python scripts/onboard_project.py audit-dossier --path /path/to/my-project
```

Sample output:
```
=== Dossier Audit: PASS ===
All 8 dossiers exist, links resolve, and no secrets detected.
```

---

## Standard Task Brief Template

To eliminate agent hallucination and scope creep, assign tasks using this structured brief:

```markdown
## Task: <TITLE>

**Context**: docs/CURRENT_STATE.md §<section>
**Priority**: P0 / P1 / P2

**Problem**: <Exact bug description or required feature>
**Acceptance Criteria**:
- <Measurable success condition 1>
- <Measurable success condition 2>

**Touched Files**:
- path/to/file_a.py
- tests/test_file_a.py

**Inviolable Constraints**:
- Do not modify files outside the touched list.
- Do not use fake or synthetic data to force tests to pass.

**Verification Command**:
```bash
python -m unittest tests/test_file_a.py
```
```

---

## Documentation

- [Agent Contract Specification (`AGENTS.md`)](references/agent_contract_standard.md)
- [Progressive Disclosure Strategy](references/progressive_disclosure_strategy.md)
- [Model Routing Decision Matrix](references/agent_routing_matrix.md)
- [Incident Ledger Methodology](references/incident_ledger_standard.md)
- [Standard Task Brief Format](references/task_brief_standard.md)
- [Sample Task Briefs](examples/task_brief_examples.md)

---

## Testing

Run unit tests:
```bash
python -m unittest discover -s tests
```

---

## License

This project is licensed under the [MIT License](LICENSE).
