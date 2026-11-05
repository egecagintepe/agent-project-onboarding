# Sample Task Briefs

Here are production-tested task briefs illustrating the standard handoff format.

---

## Example 1: Scoped Backend Bugfix

```markdown
## Task: BL-042 — Handle Redis Connection Outage Gracefully in Schedule View

**Context**: docs/MASTER_BACKLOG.md §BL-042, docs/INCIDENT_RUNBOOK.md §Incident 009
**Priority**: P1

**Problem**:
When Redis is temporarily unreachable, accessing `/api/v1/schedules/` raises an unhandled `redis.exceptions.ConnectionError` and returns HTTP 500 to clients.

**Acceptance Criteria**:
1. When Redis is down, `/api/v1/schedules/` returns HTTP 200 with fallback uncached data.
2. A warning log is emitted: `Cache unavailable for schedules, serving live data`.
3. Unit test `test_schedule_view_redis_down_returns_200` passes.

**Touched Files**:
- `services/schedule_service.py`
- `tests/test_schedules.py`

**Inviolable Constraints**:
- Do not modify files outside the touched list.
- Do not catch general `Exception`; catch only `redis.exceptions.RedisError`.

**Verification**:
```bash
python -m unittest tests/test_schedules.py
```
```

---

## Example 2: Database Migration with Safe Defaults

```markdown
## Task: BL-051 — Add 'last_login_ip' to User Model

**Context**: docs/ARCHITECTURE_MAP.md §Users, docs/BUILD_DEPLOY_MATRIX.md
**Priority**: P2

**Problem**:
We need to track user login IP addresses for security auditing without locking the `users` table during deployment.

**Acceptance Criteria**:
1. New field `last_login_ip` added as a nullable or default-valued column.
2. Migration file generated and passes dry-run check.
3. Unit test verifies model serialization includes the new field.

**Touched Files**:
- `models/user.py`
- `migrations/0014_add_last_login_ip.py`
- `tests/test_user_model.py`

**Inviolable Constraints**:
- Do NOT add a non-nullable field without a default (will lock PostgreSQL table).
- Follow zero-downtime migration guidelines in docs/BUILD_DEPLOY_MATRIX.md.

**Verification**:
```bash
python manage.py makemigrations --check --dry-run
python manage.py test tests.test_user_model
```
```
