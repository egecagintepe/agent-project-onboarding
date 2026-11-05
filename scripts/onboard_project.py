#!/usr/bin/env python3
"""
Agent Project Onboarding CLI Toolkit.
Scans project repositories, scaffolds standardized 8-dossier agent handoff systems,
and audits documentation integrity and security.
Standard library only (zero external dependencies).
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, List, Any, Tuple

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

def scan_project(path: str) -> Dict[str, Any]:
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Path not found: {path}")

    files = []
    for root, dirs, filenames in os.walk(path):
        # Ignore common non-source directories
        for d in [".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".next", ".astro"]:
            if d in dirs:
                dirs.remove(d)
        for f in filenames:
            rel = os.path.relpath(os.path.join(root, f), path).replace("\\", "/")
            files.append(rel)

    languages = []
    frameworks = []
    databases = []
    testing_tools = []
    has_docker = False

    # Detection logic
    file_set = set(files)

    # Languages
    if any(f.endswith(".py") for f in files) or "requirements.txt" in file_set or "pyproject.toml" in file_set:
        languages.append("Python")
    if any(f.endswith((".ts", ".tsx")) for f in files) or "tsconfig.json" in file_set:
        languages.append("TypeScript")
    elif any(f.endswith((".js", ".jsx")) for f in files) or "package.json" in file_set:
        languages.append("JavaScript")
    if any(f.endswith(".go") for f in files) or "go.mod" in file_set:
        languages.append("Go")
    if any(f.endswith(".rs") for f in files) or "Cargo.toml" in file_set:
        languages.append("Rust")
    if any(f.endswith(".rb") for f in files) or "Gemfile" in file_set:
        languages.append("Ruby")

    # Frameworks
    if "manage.py" in file_set:
        frameworks.append("Django")
    for f in files:
        if f.endswith((".py", ".json", ".js", ".ts", ".toml", ".txt", ".cfg", ".ini", ".env", ".yaml", ".yml")):
            try:
                full_path = os.path.join(path, f)
                if os.path.getsize(full_path) < 500000:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                        if "fastapi" in content.lower() and "FastAPI" not in frameworks:
                            frameworks.append("FastAPI")
                        if "express" in content.lower() and "Express" not in frameworks:
                            frameworks.append("Express")
                        if "next" in content.lower() and "package.json" in f and "Next.js" not in frameworks:
                            frameworks.append("Next.js")
                        if "react" in content.lower() and "React" not in frameworks:
                            frameworks.append("React")
                        if "svelte" in content.lower() and "Svelte" not in frameworks:
                            frameworks.append("Svelte")
                        if ("postgresql" in content.lower() or "postgres" in content.lower() or "psycopg" in content.lower()):
                            if "PostgreSQL" not in databases:
                                databases.append("PostgreSQL")
                        if "redis" in content.lower() and "Redis" not in databases:
                            databases.append("Redis")
                        if "sqlite" in content.lower() and "SQLite" not in databases:
                            databases.append("SQLite")
                        if "pytest" in content.lower() and "pytest" not in testing_tools:
                            testing_tools.append("pytest")
                        if "jest" in content.lower() and "jest" not in testing_tools:
                            testing_tools.append("jest")
            except Exception:
                pass

    if any("dockerfile" in f.lower() for f in files) or any("docker-compose" in f.lower() for f in files):
        has_docker = True

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
        "has_docker": has_docker,
        "existing_dossiers": existing_dossiers,
        "dossier_coverage_pct": round((len(existing_dossiers) / len(DOSSIER_FILES)) * 100, 1)
    }

def generate_dossier(path: str, project_name: str = "My Project") -> List[str]:
    scan_data = scan_project(path)
    created_files = []

    docs_dir = os.path.join(path, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    # 1. AGENTS.md
    agents_md = f"""# {project_name} — Universal Agent Contract (AGENTS.md)

This document is the binding operational contract for all AI coding agents (Claude, Codex, Gemini, Antigravity, Cursor) and human contributors.

## 1. Onboarding Reading Order (Progressive Disclosure)

New agents must read documentation in this strict order:
1. `AGENTS.md` (this file — invariants & boundaries)
2. `docs/ARCHITECTURE_MAP.md` (how the system is wired)
3. `docs/CURRENT_STATE.md` (what is working vs broken)
4. `docs/MASTER_BACKLOG.md` (the prioritized backlog)
5. `docs/AGENT_ROUTING.md` (which agent should perform which task)

## 2. Inviolable Safety Invariants

1. **No Fake Success**: Never report a task as completed using mock or synthetic test data unless explicitly requested.
2. **Preserve Database State**: Never run destructive database commands (`DROP TABLE`, `TRUNCATE`) or `--fake` migrations.
3. **Zero Secret Leaks**: Never print `.env` files, API tokens, passwords, or private keys in logs, transcripts, or commit messages.
4. **Git Discipline**: Never force-push (`git push --force`) to release branches.
5. **Permanent Workspace**: Work exclusively within the project root. Never create parallel clones or disconnected workspaces.

## 3. Technology Stack & Verification Commands

- **Languages**: {', '.join(scan_data['languages']) or 'General'}
- **Frameworks**: {', '.join(scan_data['frameworks']) or 'Standard'}
- **Databases**: {', '.join(scan_data['databases']) or 'Standard'}
- **Testing**:
  ```bash
  # Run targeted tests before committing changes
  {scan_data['testing_tools'][0] if scan_data['testing_tools'] else 'python -m unittest'}
  ```

## 4. Dossier Directory Map

- `docs/ARCHITECTURE_MAP.md` — Subsystems, services, and cross-domain data flows.
- `docs/CURRENT_STATE.md` — Honest feature inventory and active feature flags.
- `docs/MASTER_BACKLOG.md` — Prioritized backlog of engineering work items.
- `docs/AGENT_ROUTING.md` — Model routing guidelines (which AI model handles which task).
- `docs/PRODUCTION_RUNBOOK.md` — Authoritative deployment, verification, and rollback commands.
- `docs/INCIDENT_RUNBOOK.md` — Historical production incident ledger ("Happened Once, Never Again").
- `docs/BUILD_DEPLOY_MATRIX.md` — Impact matrix mapping changed files to required rebuild actions.
"""
    agents_path = os.path.join(path, "AGENTS.md")
    if not os.path.exists(agents_path):
        with open(agents_path, "w", encoding="utf-8") as f:
            f.write(agents_md)
        created_files.append("AGENTS.md")

    # 2. docs/ARCHITECTURE_MAP.md
    arch_md = f"""# {project_name} — Architecture Map

**Last Updated**: {scan_data.get('date', 'Initial Scaffolding')}
**Purpose**: Authoritative map of how systems, services, and data flows are wired in reality.

## 1. System Topology

- **Primary Stack**: {', '.join(scan_data['languages']) or 'Polyglot'}
- **Application Services**: {', '.join(scan_data['frameworks']) or 'Standard'}
- **Persistence & Caching**: {', '.join(scan_data['databases']) or 'Standard'}
- **Containerization**: {'Docker / Compose enabled' if scan_data['has_docker'] else 'Native host'}

## 2. Directory Map

```
docs/           Authoritative dossiers and runbooks
src/            Application core source code
tests/          Automated regression and acceptance suites
scripts/        Operational automation and diagnostic tools
```

## 3. Service Boundaries & Data Flow

Describe core subsystem boundaries and external integrations here.
"""
    arch_path = os.path.join(docs_dir, "ARCHITECTURE_MAP.md")
    if not os.path.exists(arch_path):
        with open(arch_path, "w", encoding="utf-8") as f:
            f.write(arch_md)
        created_files.append("docs/ARCHITECTURE_MAP.md")

    # 3. docs/CURRENT_STATE.md
    state_md = f"""# {project_name} — Current State (Honest Inventory)

**Purpose**: Truthful ledger of what works, what is broken, and what is stubbed. Never fake status.

## 1. Component Status Summary

| Area | Status | Known Limitations / Notes |
|---|---|---|
| Core Backend | Healthy | Fully operational |
| Database | Configured | Migrations tracked in Git |
| Background Jobs | Operational | Idempotent worker execution |
| Public API | Active | Versioned endpoints |

## 2. Known Issues & Tech Debt

- Record known flaky tests, edge-case race conditions, or pending refactors here.
"""
    state_path = os.path.join(docs_dir, "CURRENT_STATE.md")
    if not os.path.exists(state_path):
        with open(state_path, "w", encoding="utf-8") as f:
            f.write(state_md)
        created_files.append("docs/CURRENT_STATE.md")

    # 4. docs/MASTER_BACKLOG.md
    backlog_md = f"""# {project_name} — Master Backlog

**Rule**: All work items originate here. Single source of truth for features, bug fixes, and refactoring.

## Active Sprint

| ID | Priority | Title | Assignee | Acceptance Criteria |
|---|---|---|---|---|
| BL-001 | P0 | Project onboarding & baseline verification | Agent / Team | Tests pass, CI green |
| BL-002 | P1 | Establish core test suite and regression coverage | Agent | Unit test coverage > 80% |

## Icebox / Future Work
- BL-003: Performance profiling and query optimization
"""
    backlog_path = os.path.join(docs_dir, "MASTER_BACKLOG.md")
    if not os.path.exists(backlog_path):
        with open(backlog_path, "w", encoding="utf-8") as f:
            f.write(backlog_md)
        created_files.append("docs/MASTER_BACKLOG.md")

    # 5. docs/AGENT_ROUTING.md
    routing_md = f"""# {project_name} — Agent Routing Guide

**Purpose**: Directs each category of task to the AI agent or human role best equipped to solve it safely.

| Task Category | Recommended Model / Role | Rationale |
|---|---|---|
| Scoped backend bugfix (1-3 files) | **Codex / Lightweight Agent** | Fast, deterministic code editing with clear unit test acceptance |
| Architecture & multi-service design | **Claude / Gemini Pro / Lead** | High context window synthesis and trade-off evaluation |
| Database schema migrations | **Agent + Human Review** | Low tolerance for data risk; requires explicit migration review |
| UI/UX Component Refactoring | **Frontend Specialist Agent** | Visual polish, responsiveness, accessibility standards |
| Production deployment & rollback | **Guarded CLI / Human** | Irreversible state mutation; must follow runbook strictly |
| Secret rotation & credentials | **Human Operator Only** | Agents must never view or store production secrets |
"""
    routing_path = os.path.join(docs_dir, "AGENT_ROUTING.md")
    if not os.path.exists(routing_path):
        with open(routing_path, "w", encoding="utf-8") as f:
            f.write(routing_md)
        created_files.append("docs/AGENT_ROUTING.md")

    # 6. docs/PRODUCTION_RUNBOOK.md
    prod_md = f"""# {project_name} — Production Runbook

**Purpose**: Authoritative deploy, verify, and rollback instructions.

## 1. Preflight Checklist
1. Ensure working tree is clean (`git status`).
2. Verify all local tests pass.
3. Verify remote branch synchronization.

## 2. Deployment Commands
```bash
# Example deployment command
git pull origin main
# Rebuild containers or dependencies if needed
```

## 3. Post-Deployment Verification
```bash
# Verify health endpoint returns 200 OK
curl -f https://example.com/healthz
```

## 4. Rollback Protocol
If health checks fail, revert to previous stable release tag:
```bash
git checkout <PREVIOUS_COMMIT>
```
"""
    prod_path = os.path.join(docs_dir, "PRODUCTION_RUNBOOK.md")
    if not os.path.exists(prod_path):
        with open(prod_path, "w", encoding="utf-8") as f:
            f.write(prod_md)
        created_files.append("docs/PRODUCTION_RUNBOOK.md")

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
    inc_path = os.path.join(docs_dir, "INCIDENT_RUNBOOK.md")
    if not os.path.exists(inc_path):
        with open(inc_path, "w", encoding="utf-8") as f:
            f.write(inc_md)
        created_files.append("docs/INCIDENT_RUNBOOK.md")

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
    matrix_path = os.path.join(docs_dir, "BUILD_DEPLOY_MATRIX.md")
    if not os.path.exists(matrix_path):
        with open(matrix_path, "w", encoding="utf-8") as f:
            f.write(matrix_md)
        created_files.append("docs/BUILD_DEPLOY_MATRIX.md")

    return created_files

def audit_dossier(path: str) -> Dict[str, Any]:
    path = os.path.abspath(path)
    issues = []
    missing_dossiers = []

    for rel_path, desc in DOSSIER_FILES:
        target = os.path.join(path, rel_path)
        if not os.path.exists(target):
            missing_dossiers.append({"file": rel_path, "description": desc})

    # Link checking across all markdown files in root & docs/
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

            # Check links
            for match in link_pattern.finditer(content):
                url = match.group(2).strip()
                if url.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                # Split anchor
                clean_target = url.split("#")[0]
                if clean_target:
                    target_full = os.path.normpath(os.path.join(os.path.dirname(md_file), clean_target))
                    if not os.path.exists(target_full):
                        broken_links.append({
                            "source_file": os.path.relpath(md_file, path).replace("\\", "/"),
                            "target": url
                        })

            # Check secret leaks
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

    elif args.subcommand == "generate":
        created = generate_dossier(args.path, project_name=args.project_name)
        if args.json:
            print(json.dumps({"created_files": created}, indent=2))
        else:
            print(f"=== Generated {len(created)} Dossier Files ===")
            for c in created:
                print(f"  + {c}")
            if not created:
                print("All standard dossier files already exist.")

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
