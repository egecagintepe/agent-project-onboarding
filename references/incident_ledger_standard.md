# Incident Memory Ledger Standard

A critical challenge in long-lived software repositories managed by AI agents is **regressive mistakes**: an agent inadvertently repeats an operational blunder that was previously diagnosed, suffered, and resolved by another developer weeks earlier.

The Incident Memory Ledger eliminates this failure mode through structured post-mortems and preventative guards.

---

## 1. The Rule: "Happened Once, Never Again"

Every time an outage, deployment failure, corrupted migration, or severe bug occurs in production or staging, a post-mortem entry must be appended to `docs/INCIDENT_RUNBOOK.md`.

---

## 2. Standard Incident Entry Template

```markdown
### Incident <NUM> — <Short Descriptive Title> (<YYYY-MM-DD>)

**Symptom**:
What went wrong from the user or monitoring perspective? (e.g. "Home page returned HTTP 500", "Worker hung with 100% CPU").

**Root Cause**:
What was the technical mechanism? (e.g. "Django settings relied on an uninstalled module", "PostgreSQL statement timeout was 0 and ran out of memory on a 20-table join").

**Immediate Remedy**:
What exact safe commands were used to restore service?

**Permanent Preventative Guard**:
What permanent code check, automated test, or linter was added to guarantee this cannot happen again?
- Link to specific test or preflight script (e.g. `tests/test_incident_regression.py`).

**Forbidden Operations During Recovery**:
What panicked actions must NEVER be taken during this incident? (e.g. "Do not run docker compose down", "Do not run migrate --fake").
```

---

## 3. Mandatory Agent Preflight Check

Before modifying production infrastructure or core framework settings, the agent must check `docs/INCIDENT_RUNBOOK.md` to ensure the proposed change does not recreate a known failure pattern.
