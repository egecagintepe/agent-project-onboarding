#!/usr/bin/env python3
"""
Agent Project Onboarding CLI Toolkit.
Scans codebases, scaffolds honest 8-dossier agent handoff frameworks,
and audits documentation integrity, links, and secret leakage.
Standard library only (zero external dependencies).
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Any, Tuple, Optional

DOSSIER_FILES = [
    ("AGENTS.md", "Project root agent contract"),
    ("docs/ARCHITECTURE_MAP.md", "System architecture & component wiring"),
    ("docs/CURRENT_STATE.md", "Honest inventory of feature readiness & active flags"),
    ("docs/MASTER_BACKLOG.md", "Prioritized single source of truth for work items"),
    ("docs/AGENT_ROUTING.md", "Model & human task allocation guide"),
    ("docs/PRODUCTION_RUNBOOK.md", "Step-by-step deploy & rollback procedures"),
    ("docs/INCIDENT_RUNBOOK.md", "Post-mortem ledger of past failures & safe remedies"),
    ("docs/BUILD_DEPLOY_MATRIX.md", "Change-to-action impact matrix")
]

SECRET_SCAN_PATTERNS = [
    (r"(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-+=]{12,}['\"]", "High-entropy secret assignment"),
    (r"-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----", "Private cryptographic key"),
    (r"gh[opsu]_[A-Za-z0-9_]{30,}", "GitHub Personal Access Token"),
    (r"xox[baprs]-[0-9a-zA-Z-]{10,}", "Slack Token")
]

def validate_safe_target_path(base_dir: str, rel_path: str) -> str:
    """
    Validates that resolving rel_path against base_dir stays strictly inside base_dir.
    Rejects:
    - Path traversal attempts (e.g., '../outside')
    - Sibling directory prefix collisions (e.g. '/tmp/repo-evil' when base is '/tmp/repo')
    - Symlinks that escape project boundaries
    - Direct symlink paths to protect against link hijacking
    """
    base_abs = os.path.abspath(base_dir)
    base_real = os.path.realpath(base_abs)

    target_abs = os.path.abspath(os.path.join(base_abs, rel_path))

    # Path boundary check via commonpath (prevents sibling prefix collisions like /repo vs /repo-evil)
    try:
        common = os.path.commonpath([base_abs, target_abs])
    except ValueError:
        raise PermissionError(f"Security violation: Target '{target_abs}' is on a different drive than base '{base_abs}'.")

    if common != base_abs:
        raise PermissionError(f"Security violation: Target path '{target_abs}' escapes project root '{base_abs}'.")

    # Reject symlinks on the target itself
    if os.path.islink(target_abs):
        raise PermissionError(f"Security violation: Symlink target '{target_abs}' is not permitted.")

    # Check that realpath (after resolving intermediate symlinks) stays within real project root
    target_real = os.path.realpath(target_abs)
    try:
        common_real = os.path.commonpath([base_real, target_real])
    except ValueError:
        raise PermissionError(f"Security violation: Target '{target_real}' is on a different drive than base '{base_real}'.")

    if common_real != base_real:
        raise PermissionError(f"Security violation: Symlink target '{target_real}' escapes project root '{base_real}'.")

    return target_abs

def scan_project(path: str) -> Dict[str, Any]:
    path = os.path.realpath(path)
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Path not found: {path}")

    files = []
    top_level_dirs = set()
    for root, dirs, filenames in os.walk(path):
        # Ignore common non-source directories
        for d in [".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next", ".astro"]:
            if d in dirs:
                dirs.remove(d)

        rel_root = os.path.relpath(root, path).replace("\\", "/")
        if rel_root != "." and "/" not in rel_root:
            top_level_dirs.add(rel_root)

        for f in filenames:
            rel = os.path.relpath(os.path.join(root, f), path).replace("\\", "/")
            files.append(rel)

    languages = []
    frameworks = []
    databases = []
    testing_tools = []
    evidence = []
    task_queues = []
    has_api = False
    api_evidence = []
    has_docker = False

    file_set = set(files)
    test_files_count = sum(1 for f in files if f.startswith(("tests/", "test/")) or f.endswith(("_test.py", "test_.py", ".test.js", ".test.ts", ".spec.ts", ".spec.js")))

    # Routes / API files check
    if any(f in file_set for f in ["urls.py", "routes.py", "api.py", "openapi.json", "openapi.yaml", "openapi.yml", "swagger.yaml", "swagger.json", "swagger.yml"]):
        has_api = True
        api_evidence.append("Found API manifest or routing declaration file")
    if any(f.startswith(("routes/", "controllers/", "api/", "endpoints/")) for f in files):
        has_api = True
        api_evidence.append("Found routes/controllers/api directory")

    # Celery / Task queue files check
    if any(f.endswith("celery.py") or f.endswith("tasks.py") or "/tasks/" in f for f in files):
        if "Celery" not in task_queues:
            task_queues.append("Celery")
            evidence.append("Celery: Found celery.py or tasks.py")

    # 1. Languages with evidence
    if any(f.endswith(".py") for f in files) or "requirements.txt" in file_set or "pyproject.toml" in file_set:
        languages.append("Python")
        evidence.append("Python: Detected .py files or Python dependency manifests (requirements.txt / pyproject.toml)")
    if any(f.endswith((".ts", ".tsx")) for f in files) or "tsconfig.json" in file_set:
        languages.append("TypeScript")
        evidence.append("TypeScript: Detected .ts/.tsx files or tsconfig.json")
    elif any(f.endswith((".js", ".jsx")) for f in files) or "package.json" in file_set:
        languages.append("JavaScript")
        evidence.append("JavaScript: Detected .js/.jsx files or package.json")
    if any(f.endswith(".go") for f in files) or "go.mod" in file_set:
        languages.append("Go")
        evidence.append("Go: Detected .go files or go.mod")
    if any(f.endswith(".rs") for f in files) or "Cargo.toml" in file_set:
        languages.append("Rust")
        evidence.append("Rust: Detected .rs files or Cargo.toml")
    if any(f.endswith(".rb") for f in files) or "Gemfile" in file_set:
        languages.append("Ruby")
        evidence.append("Ruby: Detected .rb files or Gemfile")

    # 2. Frameworks with evidence
    if "manage.py" in file_set:
        frameworks.append("Django")
        evidence.append("Django: Found 'manage.py' in repository root")

    for f in files:
        if f.endswith((".py", ".json", ".js", ".ts", ".toml", ".txt", ".cfg", ".ini", ".env", ".yaml", ".yml")):
            try:
                full_path = os.path.join(path, f)
                if os.path.getsize(full_path) < 500000:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read().lower()
                        if "fastapi" in content and "FastAPI" not in frameworks:
                            frameworks.append("FastAPI")
                            evidence.append(f"FastAPI: Mentioned in {f}")
                        if "express" in content and "Express" not in frameworks:
                            frameworks.append("Express")
                            evidence.append(f"Express: Mentioned in {f}")
                        if "next" in content and "package.json" in f and "Next.js" not in frameworks:
                            frameworks.append("Next.js")
                            evidence.append(f"Next.js: Found in {f}")
                        if "react" in content and "React" not in frameworks:
                            frameworks.append("React")
                            evidence.append(f"React: Mentioned in {f}")
                        if "svelte" in content and "Svelte" not in frameworks:
                            frameworks.append("Svelte")
                            evidence.append(f"Svelte: Mentioned in {f}")
                        if ("postgresql" in content or "postgres" in content or "psycopg" in content) and "PostgreSQL" not in databases:
                            databases.append("PostgreSQL")
                            evidence.append(f"PostgreSQL: Referenced in {f}")
                        if "redis" in content and "Redis" not in databases:
                            databases.append("Redis")
                            evidence.append(f"Redis: Referenced in {f}")
                        if "sqlite" in content and "SQLite" not in databases:
                            databases.append("SQLite")
                            evidence.append(f"SQLite: Referenced in {f}")
                        if "pytest" in content and "pytest" not in testing_tools:
                            testing_tools.append("pytest")
                            evidence.append(f"pytest: Referenced in {f}")
                        if "jest" in content and "jest" not in testing_tools:
                            testing_tools.append("jest")
                            evidence.append(f"jest: Referenced in {f}")
                        if "celery" in content and "Celery" not in task_queues:
                            task_queues.append("Celery")
                            evidence.append(f"Celery: Mentioned in {f}")
                        if "bullmq" in content and "BullMQ" not in task_queues:
                            task_queues.append("BullMQ")
                            evidence.append(f"BullMQ: Mentioned in {f}")
                        if ("urlpatterns" in content or "app.get(" in content or "app.post(" in content or "router.get(" in content or "apirouter" in content) and not has_api:
                            has_api = True
                            api_evidence.append(f"API routing patterns discovered in {f}")
            except Exception:
                pass

    if ("FastAPI" in frameworks or "Express" in frameworks or "Django" in frameworks) and not has_api:
        has_api = True
        api_evidence.append(f"Web framework routing conventions ({', '.join(f for f in frameworks if f in ('FastAPI', 'Express', 'Django'))})")

    if any("dockerfile" in f.lower() for f in files) or any("docker-compose" in f.lower() for f in files):
        has_docker = True
        evidence.append("Docker: Found Dockerfile or docker-compose file")

    # Check existing documentation
    existing_dossiers = []
    for rel_path, desc in DOSSIER_FILES:
        if rel_path in file_set:
            existing_dossiers.append(rel_path)

    return {
        "project_root": path,
        "languages": languages,
        "frameworks": frameworks,
        "databases": databases,
        "testing_tools": testing_tools,
        "task_queues": task_queues,
        "has_api": has_api,
        "api_evidence": api_evidence,
        "test_files_count": test_files_count,
        "has_docker": has_docker,
        "top_level_directories": sorted(list(top_level_dirs)),
        "evidence": evidence,
        "existing_dossiers": existing_dossiers,
        "dossier_coverage_pct": round((len(existing_dossiers) / len(DOSSIER_FILES)) * 100, 1)
    }

def generate_dossier(path: str, project_name: str = "My Project", dry_run: bool = False, force: bool = False) -> Dict[str, Any]:
    path = os.path.realpath(path)
    scan_data = scan_project(path)
    created_files = []
    skipped_files = []
    file_contents = {}

    docs_dir = os.path.join(path, "docs")

    # Format discovered top-level directories honestly
    dirs_repr = "\n".join(f"{d}/" for d in scan_data["top_level_directories"]) if scan_data["top_level_directories"] else "docs/\n(No other top-level directories discovered yet)"

    # Evidence bullet points
    evidence_repr = "\n".join(f"- {e}" for e in scan_data["evidence"]) if scan_data["evidence"] else "- None detected automatically"

    # 1. AGENTS.md
    agents_md = f"""# {project_name} — Universal Agent Contract (AGENTS.md)

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

- **Languages Detected**: {', '.join(scan_data['languages']) or 'Unverified'}
- **Frameworks Detected**: {', '.join(scan_data['frameworks']) or 'Standard'}
- **Databases Detected**: {', '.join(scan_data['databases']) or 'Standard'}
- **Automated Verification**:
  ```bash
  # Run targeted test suite before committing changes:
  {scan_data['testing_tools'][0] if scan_data['testing_tools'] else 'python -m unittest'}
  ```

## 4. Dossier Directory Map

- `docs/ARCHITECTURE_MAP.md` — Subsystems, services, and cross-domain data flows.
- `docs/CURRENT_STATE.md` — Honest feature inventory, readiness statuses, and active flags.
- `docs/MASTER_BACKLOG.md` — Prioritized backlog of engineering work items.
- `docs/AGENT_ROUTING.md` — Task allocation guidelines based on task risk profile.
- `docs/PRODUCTION_RUNBOOK.md` — Authoritative deployment, verification, and rollback commands.
- `docs/INCIDENT_RUNBOOK.md` — Historical production incident ledger ("Happened Once, Never Again").
- `docs/BUILD_DEPLOY_MATRIX.md` — Impact matrix mapping changed files to required rebuild actions.
"""
    file_contents["AGENTS.md"] = agents_md

    # 2. docs/ARCHITECTURE_MAP.md
    arch_md = f"""# {project_name} — Architecture Map

**Last Verified**: [UNVERIFIED — Pending Initial Acceptance Audit]  
**Purpose**: Authoritative map of how systems, services, and data flows are wired in reality.

## 1. Discovered System Components (Evidence-Based)

{evidence_repr}

## 2. Top-Level Directory Layout (Discovered on Disk)

```
{dirs_repr}
```

## 3. Service Boundaries & Communication

- Document service-to-service communication, RPC/REST boundaries, and database ownership here.
- [TODO: VERIFY] Confirm whether message queues (Celery, Redis, RabbitMQ) or external third-party APIs are active.
"""
    file_contents["docs/ARCHITECTURE_MAP.md"] = arch_md

    # 3. docs/CURRENT_STATE.md
    if scan_data["frameworks"]:
        backend_status = "DETECTED"
        backend_evidence = f"Found framework manifests ({', '.join(scan_data['frameworks'])}); runtime health **UNVERIFIED** until tests pass."
    elif scan_data["languages"]:
        backend_status = "DETECTED"
        backend_evidence = f"Found language manifests ({', '.join(scan_data['languages'])}); framework and runtime health **UNVERIFIED**."
    else:
        backend_status = "UNKNOWN"
        backend_evidence = "No backend language or framework manifests detected."

    if scan_data["databases"]:
        db_status = "DETECTED"
        db_evidence = f"{', '.join(scan_data['databases'])}; schema migration status **UNVERIFIED**."
    else:
        db_status = "UNKNOWN"
        db_evidence = "No database driver or manifest references detected."

    if scan_data.get("task_queues"):
        queue_status = "DETECTED"
        queue_evidence = f"{', '.join(scan_data['task_queues'])}; worker daemon status and idempotency **UNVERIFIED**."
    elif "Redis" in scan_data["databases"]:
        queue_status = "UNVERIFIED"
        queue_evidence = "Redis detected (cache/broker); worker queue integration unverified."
    else:
        queue_status = "UNKNOWN"
        queue_evidence = "No background worker or queue configuration detected."

    if scan_data.get("has_api"):
        api_status = "DETECTED"
        api_details = "; ".join(scan_data.get("api_evidence", ["Route declarations exist"]))
        api_evidence = f"Route declarations exist ({api_details}); live HTTP contract responses **UNVERIFIED**."
    else:
        api_status = "UNKNOWN"
        api_evidence = "No API routes, controllers, or OpenAPI specifications detected."

    if scan_data["testing_tools"]:
        test_status = "DETECTED"
        test_evidence = f"Runner: {', '.join(scan_data['testing_tools'])}; run test suite to verify pass rate."
    elif scan_data.get("test_files_count", 0) > 0:
        test_status = "UNVERIFIED"
        test_evidence = f"Found {scan_data['test_files_count']} test files but runner configuration unverified; execute harness to confirm."
    else:
        test_status = "UNKNOWN"
        test_evidence = "No automated test runner or test suite detected."

    state_md = f"""# {project_name} — Current State (Honest Inventory)

**Principle**: Truthful ledger of verified vs unverified capabilities. Never fabricate feature health.

## 1. Component Readiness Ledger

| Component / Subsystem | Status | Verification Evidence / Actionable TODO |
|---|---|---|
| Core Application Backend | **{backend_status}** | {backend_evidence} |
| Database Persistence | **{db_status}** | {db_evidence} |
| Background Task Queue | **{queue_status}** | {queue_evidence} |
| Public API Endpoints | **{api_status}** | {api_evidence} |
| Automated Test Suite | **{test_status}** | {test_evidence} |

**Status Definitions**:
- `DETECTED`: Files or configurations exist in repository, but live behavior is unverified.
- `VERIFIED`: Confirmed operational via automated test execution or live smoke checks.
- `UNVERIFIED`: Detected but currently lacking passing verification evidence.
- `UNKNOWN`: Cannot be determined from static repository inspection.
- `NOT_APPLICABLE`: Explicitly excluded or not part of this service.

## 2. Active Technical Debt & Known Gaps

- [TODO: VERIFY] Execute repository test harness and record baseline pass rate.
- [TODO: VERIFY] Check whether active migrations match database state.
"""
    file_contents["docs/CURRENT_STATE.md"] = state_md

    # 4. docs/MASTER_BACKLOG.md
    backlog_md = f"""# {project_name} — Master Backlog

**Rule**: All work items originate here. Single source of truth for features, bug fixes, and refactoring.

## Active Sprint

| ID | Priority | Title | Assignee | Acceptance Criteria | Status |
|---|---|---|---|---|---|
| BL-001 | P0 | Baseline verification & test suite execution | Agent / Team | All existing unit tests pass cleanly | UNVERIFIED |
| BL-002 | P1 | Audit dependencies and security posture | Agent | Zero vulnerable direct dependencies | PENDING |

## Icebox / Future Work
- BL-003: Performance profiling and query optimization
"""
    file_contents["docs/MASTER_BACKLOG.md"] = backlog_md

    # 5. docs/AGENT_ROUTING.md
    routing_md = f"""# {project_name} — Agent Routing Guide

**Purpose**: Directs tasks to the appropriate model or human role based on task risk and reasoning requirements.

| Task Category | Recommended Model / Role | Rationale | Risk Profile |
|---|---|---|---|
| Scoped backend bugfix (1-3 files) | **Codex / Lightweight Agent** | Fast, deterministic code editing with clear unit test acceptance criteria. | Low |
| Architecture & multi-service design | **Claude / Gemini Pro / Lead** | Large context window synthesis and trade-off evaluation. | Medium |
| Database schema migrations | **Agent Drafting + Human Review** | Low tolerance for data corruption; requires explicit human review. | High |
| UI/UX Component Polish | **Frontend Specialist Agent** | Visual polish, responsiveness, accessibility standards. | Low |
| Production deployment & rollback | **Guarded CLI / Human Operator** | Mutating live production state; strictly follow guarded runbooks. | High |
| Secret rotation & credentials | **Human Operator ONLY** | AI agents must never view, generate, or touch production secret keys. | Critical |
"""
    file_contents["docs/AGENT_ROUTING.md"] = routing_md

    # 6. docs/PRODUCTION_RUNBOOK.md
    prod_md = f"""# {project_name} — Production Runbook

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
"""
    file_contents["docs/PRODUCTION_RUNBOOK.md"] = prod_md

    # 7. docs/INCIDENT_RUNBOOK.md
    inc_md = f"""# {project_name} — Incident Runbook & Post-Mortem Ledger

**Rule**: Happened once, never again. Every production failure is logged here with its permanent preventative guard.

## Incident Log

### Incident 001 — [Title / Example]
- **Symptom**: Service returned HTTP 500 on startup.
- **Root Cause**: Dependency added in code was omitted from manifest.
- **Remedy**: Added pinned dependency to manifest and rebuilt image.
- **Permanent Guard**: Pre-deploy test suite now validates manifest imports.
"""
    file_contents["docs/INCIDENT_RUNBOOK.md"] = inc_md

    # 8. docs/BUILD_DEPLOY_MATRIX.md
    matrix_md = f"""# {project_name} — Build & Deploy Matrix

**Question**: "I modified file X, what must I build, test, migrate, or restart?"

| Modified Path | Dependency Install | DB Migrate | Container Rebuild | Restart Service |
|---|---|---|---|---|
| Dependencies (`requirements.txt`, `package.json`) | **REQUIRED** | — | **REQUIRED** | Web + Worker |
| Database Models / Migrations | — | **REQUIRED** | — | Web + Worker |
| Application Views / Logic | — | — | — | Web |
| Frontend Assets | Build bundle | — | — | Web |
| Documentation only (`docs/`, `*.md`) | — | — | — | None |
"""
    file_contents["docs/BUILD_DEPLOY_MATRIX.md"] = matrix_md

    # Write or preview files safely
    for rel_path, content in file_contents.items():
        # Validate path boundary, reject sibling collisions and symlink escapes
        target_abs = validate_safe_target_path(path, rel_path)

        if os.path.exists(target_abs) and not force:
            skipped_files.append(rel_path)
            continue

        if not dry_run:
            os.makedirs(os.path.dirname(target_abs), exist_ok=True)
            with open(target_abs, "w", encoding="utf-8") as f:
                f.write(content)
        created_files.append(rel_path)

    return {
        "dry_run": dry_run,
        "created_files": created_files,
        "skipped_files": skipped_files
    }

def audit_dossier(path: str) -> Dict[str, Any]:
    path = os.path.realpath(path)
    issues = []
    missing_dossiers = []

    for rel_path, desc in DOSSIER_FILES:
        target = os.path.join(path, rel_path)
        if not os.path.exists(target):
            missing_dossiers.append({"file": rel_path, "description": desc})

    broken_links = []
    secret_findings = []

    md_files = []
    for root, dirs, files in os.walk(path):
        if any(ignored in root for ignored in [".git", "node_modules", ".venv", "venv", "__pycache__"]):
            continue
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    for md_file in md_files:
        try:
            with open(md_file, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()

            for match in link_pattern.finditer(content):
                url = match.group(2).strip()
                if url.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean_target = url.split("#")[0]
                if clean_target:
                    target_full = os.path.normpath(os.path.join(os.path.dirname(md_file), clean_target))
                    if not os.path.exists(target_full):
                        broken_links.append({
                            "source_file": os.path.relpath(md_file, path).replace("\\", "/"),
                            "target": url
                        })

            for pat, desc in SECRET_SCAN_PATTERNS:
                if re.search(pat, content):
                    secret_findings.append({
                        "file": os.path.relpath(md_file, path).replace("\\", "/"),
                        "description": desc
                    })

        except Exception as e:
            issues.append(f"Error reading {md_file}: {e}")

    passed = len(missing_dossiers) == 0 and len(broken_links) == 0 and len(secret_findings) == 0

    return {
        "passed": passed,
        "missing_dossiers": missing_dossiers,
        "broken_links": broken_links,
        "secret_findings": secret_findings,
        "issues": issues
    }

def main():
    parser = argparse.ArgumentParser(description="Agent Project Onboarding CLI")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Subcommand: scan
    scan_parser = subparsers.add_parser("scan", help="Scan codebase architecture and existing dossiers")
    scan_parser.add_argument("--path", default=".", help="Target repository root path")
    scan_parser.add_argument("--json", action="store_true", help="Output pure JSON")

    # Subcommand: generate
    gen_parser = subparsers.add_parser("generate", help="Scaffold 8-dossier agent onboarding framework")
    gen_parser.add_argument("--path", default=".", help="Target repository root path")
    gen_parser.add_argument("--project-name", default="Project", help="Human-readable project name")
    gen_parser.add_argument("--dry-run", action="store_true", help="Preview generated files without writing to disk")
    gen_parser.add_argument("--force", action="store_true", help="Overwrite existing dossier files")
    gen_parser.add_argument("--json", action="store_true", help="Output pure JSON")

    # Subcommand: audit-dossier
    audit_parser = subparsers.add_parser("audit-dossier", help="Audit onboarding documentation integrity")
    audit_parser.add_argument("--path", default=".", help="Target repository root path")
    audit_parser.add_argument("--json", action="store_true", help="Output pure JSON")

    args = parser.parse_args()

    if args.subcommand == "scan":
        res = scan_project(args.path)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"=== Project Scan: {res['project_root']} ===")
            print(f"Languages:   {', '.join(res['languages']) or 'None detected'}")
            print(f"Frameworks:  {', '.join(res['frameworks']) or 'None detected'}")
            print(f"Databases:   {', '.join(res['databases']) or 'None detected'}")
            print(f"Docker:      {'Yes' if res['has_docker'] else 'No'}")
            print(f"Dossier Coverage: {res['dossier_coverage_pct']}% ({len(res['existing_dossiers'])}/{len(DOSSIER_FILES)})")
            if res["evidence"]:
                print("\nDetection Evidence:")
                for ev in res["evidence"]:
                    print(f"  + {ev}")

    elif args.subcommand == "generate":
        gen_res = generate_dossier(args.path, project_name=args.project_name, dry_run=args.dry_run, force=args.force)
        if args.json:
            print(json.dumps(gen_res, indent=2))
        else:
            prefix = "[DRY-RUN] " if gen_res["dry_run"] else ""
            print(f"=== {prefix}Scaffolding Dossier for '{args.project_name}' ===")
            for c in gen_res["created_files"]:
                print(f"  + Created: {c}")
            for s in gen_res["skipped_files"]:
                print(f"  ~ Skipped existing: {s} (use --force to overwrite)")

    elif args.subcommand == "audit-dossier":
        audit_res = audit_dossier(args.path)
        if args.json:
            print(json.dumps(audit_res, indent=2))
        else:
            status = "PASS" if audit_res["passed"] else "FAIL"
            print(f"=== Dossier Audit: {status} ===")
            if audit_res["missing_dossiers"]:
                print("Missing Dossiers:")
                for m in audit_res["missing_dossiers"]:
                    print(f"  - {m['file']} ({m['description']})")
            if audit_res["broken_links"]:
                print("Broken Internal Links:")
                for b in audit_res["broken_links"]:
                    print(f"  - In {b['source_file']} -> {b['target']}")
            if audit_res["secret_findings"]:
                print("Potential Secret Leaks:")
                for s in audit_res["secret_findings"]:
                    print(f"  - In {s['file']}: {s['description']}")
            if audit_res["passed"]:
                print("All 8 dossiers exist, links resolve, and no secrets detected.")
        sys.exit(0 if audit_res["passed"] else 1)

if __name__ == "__main__":
    main()
