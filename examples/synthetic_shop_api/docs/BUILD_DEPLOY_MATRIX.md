# ShopApi — Build & Deploy Matrix

**Question**: "I modified file X, what must I build, test, migrate, or restart?"

| Modified Path | Dependency Install | DB Migrate | Container Rebuild | Restart Service |
|---|---|---|---|---|
| Dependencies (`requirements.txt`, `package.json`) | **REQUIRED** | — | **REQUIRED** | Web + Worker |
| Database Models / Migrations | — | **REQUIRED** | — | Web + Worker |
| Application Views / Logic | — | — | — | Web |
| Frontend Assets | Build bundle | — | — | Web |
| Documentation only (`docs/`, `*.md`) | — | — | — | None |
