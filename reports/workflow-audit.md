# Workflow Policy Audit

Scan root: `project-forge`
Last refreshed: 2026-06-18 11:01 UTC
Workflow files scanned: `2`
Findings: `10`

| Severity | File | Line | Rule | Fix |
|---|---|---:|---|---|
| medium | `automation/github-actions/curate.yml` | 11 | write-permission | Keep write permissions only on release or automation jobs that need them. |
| medium | `automation/github-actions/curate.yml` | 18 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/curate.yml` | 20 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/curate.yml` | 30 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/maintenance-suite.yml` | 9 | write-permission | Keep write permissions only on release or automation jobs that need them. |
| medium | `automation/github-actions/maintenance-suite.yml` | 15 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/maintenance-suite.yml` | 16 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/maintenance-suite.yml` | 28 | broad-major-action-ref | Consider pinning to a full version tag or SHA for sensitive workflows. |
| low | `automation/github-actions/curate.yml` | 7 | scheduled-workflow | Keep schedule frequency modest and make generated commits deterministic. |
| low | `automation/github-actions/maintenance-suite.yml` | 5 | scheduled-workflow | Keep schedule frequency modest and make generated commits deterministic. |

## Details

### MEDIUM - write-permission

- File: `automation/github-actions/curate.yml`
- Line: `11`
- Detail: Workflow grants `contents: write`.
- Suggested fix: Keep write permissions only on release or automation jobs that need them.

### MEDIUM - broad-major-action-ref

- File: `automation/github-actions/curate.yml`
- Line: `18`
- Detail: `actions/checkout` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `automation/github-actions/curate.yml`
- Line: `20`
- Detail: `actions/setup-python` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `automation/github-actions/curate.yml`
- Line: `30`
- Detail: `stefanzweifel/git-auto-commit-action` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - write-permission

- File: `automation/github-actions/maintenance-suite.yml`
- Line: `9`
- Detail: Workflow grants `contents: write`.
- Suggested fix: Keep write permissions only on release or automation jobs that need them.

### MEDIUM - broad-major-action-ref

- File: `automation/github-actions/maintenance-suite.yml`
- Line: `15`
- Detail: `actions/checkout` uses broad major tag `v4`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `automation/github-actions/maintenance-suite.yml`
- Line: `16`
- Detail: `actions/setup-python` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### MEDIUM - broad-major-action-ref

- File: `automation/github-actions/maintenance-suite.yml`
- Line: `28`
- Detail: `stefanzweifel/git-auto-commit-action` uses broad major tag `v5`.
- Suggested fix: Consider pinning to a full version tag or SHA for sensitive workflows.

### LOW - scheduled-workflow

- File: `automation/github-actions/curate.yml`
- Line: `7`
- Detail: Scheduled workflow should be checked for rate, permissions, and idempotence.
- Suggested fix: Keep schedule frequency modest and make generated commits deterministic.

### LOW - scheduled-workflow

- File: `automation/github-actions/maintenance-suite.yml`
- Line: `5`
- Detail: Scheduled workflow should be checked for rate, permissions, and idempotence.
- Suggested fix: Keep schedule frequency modest and make generated commits deterministic.
