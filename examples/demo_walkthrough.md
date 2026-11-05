# Agent Project Onboarding — Reproducible Demo Walkthrough

This walkthrough demonstrates the end-to-end workflow of `agent-project-onboarding` against a realistic, synthetic microservice (`examples/synthetic_shop_api`).

---

## 1. Initial State: Un-onboarded Codebase

The target project is a Python microservice with FastAPI, PostgreSQL models, Celery tasks, and Pytest tests:
```text
examples/synthetic_shop_api/
├── Dockerfile
├── main.py          (FastAPI routes: /healthz, /api/v1/items, /api/v1/orders)
├── models.py        (Persistence models)
├── requirements.txt (fastapi, uvicorn, celery, redis, psycopg2-binary, pytest)
├── tasks.py         (Background worker tasks)
└── tests/
    └── test_main.py (Unit test harness)
```

At this stage, an AI coding agent (Claude Code, Cursor, Codex) entering this repository has **no explicit contract**, no boundary constraints, and no guidance on test commands.

---

## 2. Step 1: Scan Codebase Architecture

Run the static codebase scanner:
```bash
python scripts/onboard_project.py scan --path examples/synthetic_shop_api
```

### Real Output:
```text
=== Project Scan: examples/synthetic_shop_api ===
Languages:   Python
Frameworks:  FastAPI
Databases:   PostgreSQL, Redis
Docker:      Yes
Dossier Coverage: 0.0% (0/8)

Detection Evidence:
  + Celery: Found celery.py or tasks.py
  + Python: Detected .py files or Python dependency manifests (requirements.txt / pyproject.toml)
  + FastAPI: Mentioned in main.py
  + PostgreSQL: Referenced in requirements.txt
  + Redis: Referenced in requirements.txt
  + pytest: Referenced in requirements.txt
  + Docker: Found Dockerfile or docker-compose file
```

---

## 3. Step 2: Safe Scaffolding Preview (`--dry-run`)

Preview the exact dossier files that will be created without modifying disk:
```bash
python scripts/onboard_project.py generate --path examples/synthetic_shop_api --project-name ShopApi --dry-run
```

### Real Output:
```text
=== [DRY-RUN] Scaffolding Dossier for 'ShopApi' ===
  + Created: AGENTS.md
  + Created: docs/ARCHITECTURE_MAP.md
  + Created: docs/CURRENT_STATE.md
  + Created: docs/MASTER_BACKLOG.md
  + Created: docs/AGENT_ROUTING.md
  + Created: docs/PRODUCTION_RUNBOOK.md
  + Created: docs/INCIDENT_RUNBOOK.md
  + Created: docs/BUILD_DEPLOY_MATRIX.md
```

---

## 4. Step 3: Scaffold the 8-Dossier Framework

Generate the actual framework files:
```bash
python scripts/onboard_project.py generate --path examples/synthetic_shop_api --project-name ShopApi
```

### Real Output:
```text
=== Scaffolding Dossier for 'ShopApi' ===
  + Created: AGENTS.md
  + Created: docs/ARCHITECTURE_MAP.md
  + Created: docs/CURRENT_STATE.md
  + Created: docs/MASTER_BACKLOG.md
  + Created: docs/AGENT_ROUTING.md
  + Created: docs/PRODUCTION_RUNBOOK.md
  + Created: docs/INCIDENT_RUNBOOK.md
  + Created: docs/BUILD_DEPLOY_MATRIX.md
```

The resulting `AGENTS.md` and `docs/CURRENT_STATE.md` are tailored directly to the detected stack:
- **Test Command**: Auto-configured to `pytest` based on manifest evidence.
- **Readiness Ledger**: Components (`FastAPI`, `PostgreSQL`, `Celery`, `API Endpoints`) are marked `DETECTED` citing explicit evidence, rather than fabricated as `VERIFIED`.

---

## 5. Step 4: Audit Dossier Integrity

Validate that all 8 dossiers exist, internal Markdown links resolve, and no secrets were leaked:
```bash
python scripts/onboard_project.py audit-dossier --path examples/synthetic_shop_api
```

### Real Output:
```text
=== Dossier Audit: PASS ===
All 8 dossiers exist, links resolve, and no secrets detected.
```

---

## 6. Step 5: Non-Destructive Protection (Re-run Safety)

Rerunning `generate` on an already-onboarded project safely preserves existing files by default:
```bash
python scripts/onboard_project.py generate --path examples/synthetic_shop_api --project-name ShopApi
```

### Real Output:
```text
=== Scaffolding Dossier for 'ShopApi' ===
  ~ Skipped existing: AGENTS.md (use --force to overwrite)
  ~ Skipped existing: docs/ARCHITECTURE_MAP.md (use --force to overwrite)
  ~ Skipped existing: docs/CURRENT_STATE.md (use --force to overwrite)
  ~ Skipped existing: docs/MASTER_BACKLOG.md (use --force to overwrite)
  ~ Skipped existing: docs/AGENT_ROUTING.md (use --force to overwrite)
  ~ Skipped existing: docs/PRODUCTION_RUNBOOK.md (use --force to overwrite)
  ~ Skipped existing: docs/INCIDENT_RUNBOOK.md (use --force to overwrite)
  ~ Skipped existing: docs/BUILD_DEPLOY_MATRIX.md (use --force to overwrite)
```

Existing developer edits, custom invariants, and backlog tickets are **never silently overwritten**.
