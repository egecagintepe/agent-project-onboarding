# ShopApi — Architecture Map

**Last Verified**: [UNVERIFIED — Pending Initial Acceptance Audit]  
**Purpose**: Authoritative map of how systems, services, and data flows are wired in reality.

## 1. Discovered System Components (Evidence-Based)

- Celery: Found celery.py or tasks.py
- Python: Detected .py files or Python dependency manifests (requirements.txt / pyproject.toml)
- FastAPI: Mentioned in main.py
- PostgreSQL: Referenced in requirements.txt
- Redis: Referenced in requirements.txt
- pytest: Referenced in requirements.txt
- Docker: Found Dockerfile or docker-compose file

## 2. Top-Level Directory Layout (Discovered on Disk)

```
tests/
```

## 3. Service Boundaries & Communication

- Document service-to-service communication, RPC/REST boundaries, and database ownership here.
- [TODO: VERIFY] Confirm whether message queues (Celery, Redis, RabbitMQ) or external third-party APIs are active.
