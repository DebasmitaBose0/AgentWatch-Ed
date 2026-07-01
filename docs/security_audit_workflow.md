# Automated Security Audit Workflow (ELUSoC_2026)

## Background
Securing downstream execution requires continuous automated security audits. Running linting tools on pull requests protects developers from committing potential exploits.

## Design
We configure a GitHub Actions workflow using **Bandit** to lint the codebase for common security patterns.

## Files
- `.github/workflows/security_audit_scan.yml` - Workflow running security audit scans.
- `scripts/run_bandit_audit.py` - Script driving the scan cross-platform.
- `tests/test_bandit_audit.py` - Unit verification.
- `pyproject.toml` - Dev dependency declarations.
