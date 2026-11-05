# ShopApi — Production Runbook

**Purpose**: Authoritative deploy, verify, and rollback instructions.

## 1. Preflight Checklist
1. Ensure working tree is clean (`git status`).
2. Verify all local tests pass.
3. Verify remote branch synchronization.

## 2. Deployment Commands
```bash
# Example deployment command (customize for your target infrastructure):
git pull origin main
# Rebuild containers or dependencies if needed
```

## 3. Post-Deployment Verification
```bash
# Verify health endpoint returns 200 OK:
curl -f https://example.com/healthz
```

## 4. Rollback Protocol
If health checks fail, revert to previous stable release commit:
```bash
git checkout <PREVIOUS_COMMIT>
```
