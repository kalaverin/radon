<p align="center">
  <img src="./static/example/png">
</p>

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

Read more about [Radon](https://pypi.org/project/radon/) and used Halstead [metrics implementation](https://radon.readthedocs.io/en/stable/intro.html).


## You can configure these thresholds:

```
--warn-difficulty WARN_DIFFICULTY
--warn-effort WARN_EFFORT
--warn-time WARN_TIME
--warn-volume WARN_VOLUME
--warn-complexity WARN_COMPLEXITY
--error-difficulty ERROR_DIFFICULTY
--error-effort ERROR_EFFORT
--error-time ERROR_TIME
--error-volume ERROR_VOLUME
--error-complexity ERROR_COMPLEXITY
```
