# Model & Agent Routing Decision Matrix

No single AI model or agent harness is optimal for all engineering tasks. Matching task characteristics to model strengths maximizes quality while minimizing operational risk.

---

## Task Routing Matrix

| Task Category | Optimal Agent / Role | Model Strengths & Characteristics | Risk Profile |
|---|---|---|---|
| **Scoped Backend Bug (1-3 files)** | **Codex / Lightweight Agent** | High speed, exact syntactic edits, deterministic test verification. | Low |
| **System Architecture & Service Boundaries** | **Claude / Gemini Pro / Lead** | Large context synthesis, trade-off reasoning, high-level API design. | Medium |
| **Database Schema Migrations** | **Agent Drafting + Human Approval** | Migration scripts can be drafted by agents but MUST be reviewed by human engineers. | High |
| **Frontend UI/UX Polish** | **Frontend Specialist Agent** | Visual balance, responsiveness, accessibility tokens, micro-interactions. | Low |
| **Production Deployment & Rollback** | **Guarded CLI / Human Operator** | Mutating live production state; strictly follow guarded runbooks. | High |
| **Security Auditing & Threat Modeling** | **Agent Test Authoring + Human Review** | Agents generate regression test cases; humans evaluate the attack surface. | Critical |
| **Secret Rotation & Key Management** | **Human Operator ONLY** | AI agents must never view, generate, or touch production secret keys. | Critical |

---

## Collaboration Protocol

For complex, multi-stage engineering efforts (e.g. adding a new microservice or major feature):
1. **Design Phase**: Use a reasoning-optimized model to draft the architecture and database schema in a pull request.
2. **Review Phase**: Human engineer reviews and approves the schema migrations.
3. **Implementation Phase**: Delegate mechanical component and test writing to fast code-generation agents.
4. **Verification Phase**: Run automated integration tests in CI.
