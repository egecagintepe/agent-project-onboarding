# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-05

### Added
- Initial public release of `agent-project-onboarding`.
- The 8-Dossier architecture specification (`AGENTS.md`, Architecture Map, Current State, Master Backlog, Agent Routing, Production Runbook, Incident Runbook, Build Matrix).
- `onboard_project.py` CLI toolkit for automated repository scanning, dossier scaffolding, and markdown integrity auditing.
- Secret leakage detection and internal markdown link resolution checks.
- Comprehensive guides for progressive disclosure token efficiency, model routing matrices, incident ledger methodology, and structured task briefs.
- 100% passing automated test suite covering multi-stack scanning, idempotent scaffolding, and audit validation.
- GitHub Actions CI workflow covering Python 3.8 through 3.12 across Ubuntu and Windows.
