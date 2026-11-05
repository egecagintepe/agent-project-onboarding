# Contributing to Agent Project Onboarding

We welcome contributions to standardize and improve AI agent collaboration across open-source and enterprise repositories.

## Guidelines

1. **Standard Library Only**: Core tools must remain standard library Python to ensure zero-install execution in any agent sandbox.
2. **Framework Agnostic**: Onboarding concepts must apply cleanly to any programming language or architecture.
3. **Automated Testing**: Any new scanner detection, scaffold template, or audit check must include unit tests under `tests/`.

## Local Testing

```bash
python -m unittest discover -s tests
```

