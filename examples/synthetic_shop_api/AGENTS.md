# ShopApi — Universal Agent Contract (AGENTS.md)

This document is the binding operational contract for all AI coding agents (Claude Code, Codex, Gemini, Antigravity, Cursor) and human contributors.

## 1. Onboarding Reading Order (Progressive Disclosure)

To avoid context saturation and instruction dilution, inspect documents in this order:
1. `AGENTS.md` (this file — invariants, workspace rules & test policy)
2. `docs/ARCHITECTURE_MAP.md` (subsystem boundaries and actual wiring)
3. `docs/CURRENT_STATE.md` (honest ledger of what is verified vs unverified)
4. `docs/MASTER_BACKLOG.md` (the prioritized backlog)
5. `docs/AGENT_ROUTING.md` (task assignment guidelines)

## 2. Inviolable Safety Invariants

1. **No Fabricated Success**: Never report a task as completed or tested based on mock, synthetic, or unverified test results.
2. **Preserve Database State**: Never run destructive schema modifications (`DROP TABLE`, `TRUNCATE`) or `--fake` migrations without explicit approval.
3. **Zero Secret Exposure**: Never print `.env` files, API tokens, passwords, or private keys in logs, transcripts, or commit messages.
4. **Git Discipline**: Never force-push (`git push --force`) to release branches.
5. **Permanent Workspace**: Work exclusively within the project root. Never create parallel clones or disconnected workspaces.

## 3. Technology Stack & Verification Commands

- **Languages Detected**: Python
- **Frameworks Detected**: FastAPI
- **Databases Detected**: PostgreSQL, Redis
- **Automated Verification**:
  ```bash
  # Run targeted test suite before committing changes:
  pytest
  ```

## 4. Dossier Directory Map

- `docs/ARCHITECTURE_MAP.md` — Subsystems, services, and cross-domain data flows.
- `docs/CURRENT_STATE.md` — Honest feature inventory, readiness statuses, and active flags.
- `docs/MASTER_BACKLOG.md` — Prioritized backlog of engineering work items.
- `docs/AGENT_ROUTING.md` — Task allocation guidelines based on task risk profile.
- `docs/PRODUCTION_RUNBOOK.md` — Authoritative deployment, verification, and rollback commands.
- `docs/INCIDENT_RUNBOOK.md` — Historical production incident ledger ("Happened Once, Never Again").
- `docs/BUILD_DEPLOY_MATRIX.md` — Impact matrix mapping changed files to required rebuild actions.
