# How to use [radon](https://pypi.org/project/radon/) with pre-commit?

Just add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/kalaverin/radon
    rev: 0.2.1
    hooks:
      - id: radon
        args: [--warn-time=120, --error-effort=2000]
```
