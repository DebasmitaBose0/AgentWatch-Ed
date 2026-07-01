# Automated CI/CD Coverage & Security Guards (ELUSoC_2026)

## Overview
To maintain a high quality bar and secure code practices across the AgentWatch codebase, this pull request integrates:
1. **Bandit Security Linter** - Automatically scans the Python code for common security bugs, vulnerable imports, and shell injection flaws.
2. **Pytest-Cov Coverage Gate** - Enforces a minimum of 70% overall statement coverage, preventing regressions in codebase testing.

## Scripts & Configurations
- **`.github/workflows/coverage_security_guard.yml`**: Triggers Bandit linter and coverage tests on every PR to main.
- **`scripts/verify_coverage.py`**: Customizable coverage analysis script to enforce module-level constraints.
