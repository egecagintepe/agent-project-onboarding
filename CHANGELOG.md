# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-11-05

### Security & Hardening
- **Path Boundary Validation & Sibling Collision Defense**: Replaced naive `target.startswith(base)` containment with strict `os.path.commonpath` boundary validation. Resolves sibling-directory prefix collision vulnerabilities (e.g. `/path/repo` vs `/path/repo-evil`) and enforces symlink escape rejection.
- **Evidence-Conditioned Component Readiness**: Component statuses (including Public API Endpoints, Databases, Queues, and Test Suites) are now marked `DETECTED` strictly when concrete evidence exists in the repository; otherwise they default honestly to `UNKNOWN`.
- **Markdown Code Fence Nesting**: Fixed outer code fence formatting in documentation and examples (`README.md`, `SKILL.md`, `task_brief_examples.md`) using 4-backtick blocks so inner code blocks render cleanly.
- **Regression Test Coverage**: Expanded automated test suite to 24 tests, adding coverage for sibling directory prefix collisions, symlink escape rejection, and evidence-conditioned component ledger generation.

## [1.0.1] - 2026-11-05

### Security & Hardening
- **CRITICAL STATUS FIX**: Removed all fabricated component health claims. Scaffolding now uses honest, evidence-based statuses: `DETECTED`, `VERIFIED`, `UNVERIFIED`, `UNKNOWN`, and `NOT_APPLICABLE`.
- **Evidence-Based Technology Detection**: Scanner records explicit file references and code strings providing proof for detected languages, frameworks, and databases.
- **Non-Destructive Protection**: Scaffolding now skips existing documentation by default; added `--dry-run` for previewing and `--force` for explicit overwrites.
- **Path Traversal Protection**: Enforced realpath verification preventing directory escape vulnerabilities during file generation.
- **Accurate Handoff Terminology**: Replaced absolute claims with bounded, accurate guarantees on minimizing context fragmentation.
- **Official Agent Skills Compliance**: Validated frontmatter and directory layout against the official Agent Skills specification (`npx skills-ref validate`).
- **Comprehensive E2E Test Suite**: Expanded test coverage to 14 unit and integration tests including CLI subprocess validation.

## [1.0.0] - 2026-11-05

### Added
- Preliminary release of `agent-project-onboarding`.
