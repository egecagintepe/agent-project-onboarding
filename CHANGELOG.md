# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
