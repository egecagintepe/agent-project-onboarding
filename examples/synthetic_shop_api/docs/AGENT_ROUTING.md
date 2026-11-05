# ShopApi — Agent Routing Guide

**Purpose**: Directs tasks to the appropriate model or human role based on task risk and reasoning requirements.

| Task Category | Recommended Model / Role | Rationale | Risk Profile |
|---|---|---|---|
| Scoped backend bugfix (1-3 files) | **Codex / Lightweight Agent** | Fast, deterministic code editing with clear unit test acceptance criteria. | Low |
| Architecture & multi-service design | **Claude / Gemini Pro / Lead** | Large context window synthesis and trade-off evaluation. | Medium |
| Database schema migrations | **Agent Drafting + Human Review** | Low tolerance for data corruption; requires explicit human review. | High |
| UI/UX Component Polish | **Frontend Specialist Agent** | Visual polish, responsiveness, accessibility standards. | Low |
| Production deployment & rollback | **Guarded CLI / Human Operator** | Mutating live production state; strictly follow guarded runbooks. | High |
| Secret rotation & credentials | **Human Operator ONLY** | AI agents must never view, generate, or touch production secret keys. | Critical |
