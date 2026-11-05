# Agent Contract Standard (`AGENTS.md`)

This specification defines the universal contract that governs AI coding agents in any software repository.

---

## 1. Why a Root Agent Contract?

AI models lack persistent state across independent sessions. When a new agent session is spawned (or a human switches between Claude, Codex, Gemini, or Cursor), the agent has zero memory of previous constraints, implicit conventions, forbidden operations, or architectural rules.

A root `AGENTS.md` file serves as the **constitutional contract**. It is indexed by agent harnesses upon workspace load, establishing immediate alignment before any code is generated or commands are executed.

---

## 2. Mandatory Sections

Every production-grade `AGENTS.md` must include:

### 1. Progressive Disclosure Reading Order
Instructs the agent on the exact sequence to inspect documents (e.g. `AGENTS.md` -> `ARCHITECTURE_MAP.md` -> `CURRENT_STATE.md` -> `MASTER_BACKLOG.md`). Agents must not begin editing before understanding project state.

### 2. Inviolable Safety Invariants
Strict operational prohibitions:
- No faking success with mocked test data.
- Never delete or run destructive operations on user databases.
- Never leak secrets, `.env` files, or API credentials into outputs or commits.
- Never force-push or mutate upstream release branch history.
- Work solely within the single authorized project directory (no arbitrary clones).

### 3. Verification & Testing Policy
Explicit commands the agent must run to verify changes. Distinguish lightweight checks (e.g. `linter`, `check`, fast unit tests) from heavyweight deployment verification.

### 4. Dossier Index
Links to the 7 accompanying architectural dossiers in `docs/`.

---

## 3. Tool-Specific Shims (`CLAUDE.md`, `GEMINI.md`, Cursor Rules)

When specific agent tools expect specialized filenames, use thin symlinks or shims that point back to `AGENTS.md`:

```markdown
# Claude Code Project Contract
Please refer to the authoritative project contract in [AGENTS.md](AGENTS.md) and architectural dossiers in [docs/](docs/).
```
This guarantees single-source-of-truth governance across all agent environments.
