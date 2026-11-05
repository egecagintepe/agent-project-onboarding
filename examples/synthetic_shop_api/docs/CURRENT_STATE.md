# ShopApi — Current State (Honest Inventory)

**Principle**: Truthful ledger of verified vs unverified capabilities. Never fabricate feature health.

## 1. Component Readiness Ledger

| Component / Subsystem | Status | Verification Evidence / Actionable TODO |
|---|---|---|
| Core Application Backend | **DETECTED** | Found framework manifests (FastAPI); runtime health **UNVERIFIED** until tests pass. |
| Database Persistence | **DETECTED** | PostgreSQL, Redis; schema migration status **UNVERIFIED**. |
| Background Task Queue | **DETECTED** | Celery; worker daemon status and idempotency **UNVERIFIED**. |
| Public API Endpoints | **DETECTED** | Route declarations exist (API routing patterns discovered in main.py); live HTTP contract responses **UNVERIFIED**. |
| Automated Test Suite | **DETECTED** | Runner: pytest; run test suite to verify pass rate. |

**Status Definitions**:
- `DETECTED`: Files or configurations exist in repository, but live behavior is unverified.
- `VERIFIED`: Confirmed operational via automated test execution or live smoke checks.
- `UNVERIFIED`: Detected but currently lacking passing verification evidence.
- `UNKNOWN`: Cannot be determined from static repository inspection.
- `NOT_APPLICABLE`: Explicitly excluded or not part of this service.

## 2. Active Technical Debt & Known Gaps

- [TODO: VERIFY] Execute repository test harness and record baseline pass rate.
- [TODO: VERIFY] Check whether active migrations match database state.
