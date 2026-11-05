# ShopApi — Incident Runbook & Post-Mortem Ledger

**Rule**: Happened once, never again. Every production failure is logged here with its permanent preventative guard.

## Incident Log

### Incident 001 — [Title / Example]
- **Symptom**: Service returned HTTP 500 on startup.
- **Root Cause**: Dependency added in code was omitted from manifest.
- **Remedy**: Added pinned dependency to manifest and rebuilt image.
- **Permanent Guard**: Pre-deploy test suite now validates manifest imports.
