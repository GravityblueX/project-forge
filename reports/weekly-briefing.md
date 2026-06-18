# Weekly Maintenance Briefing

Last refreshed: 2026-06-18 11:50 UTC

## Priority Queue

1. Fix `ashveil-console` CI by ensuring Prettier is installed in the workflow environment.
2. Review `10` workflow policy findings before enabling more automation.
3. Keep workflow templates inactive until the GitHub token has explicit `workflow` scope.
4. Review default branch protection for active repositories before relying on automation commits.

## Snapshot

### Repo Health

| Item | Data |
|---|---|
| 1 | [GravityblueX/slider-captcha-lab](https://github.com/GravityblueX/slider-captcha-lab) / 100 / active / Keep current maintenance rhythm. |
| 2 | [GravityblueX/ashveil-console](https://github.com/GravityblueX/ashveil-console) / 90 / active / Inspect recent failed workflow runs. |
| 3 | [GravityblueX/YumeBox-MaterialDesign-Study](https://github.com/GravityblueX/YumeBox-MaterialDesign-Study) / 86 / active / Write a README with install, run, and project status sections. |
| 4 | [GravityblueX/project-forge](https://github.com/GravityblueX/project-forge) / 73 / active / Add a minimal CI workflow for lint/build/test. |
| 5 | [GravityblueX/lux_net](https://github.com/GravityblueX/lux_net) / 70 / active / Add a LICENSE file if this is meant to be reusable. |

### CI Failures

| Item | Data |
|---|---|
| [GravityblueX/ashveil-console](https://github.com/GravityblueX/ashveil-console) | Continuous Optimization & Release / Missing formatter or linter dependency / optimize / [open](https://github.com/GravityblueX/ashveil-console/actions/runs/27741663827) |
| [GravityblueX/ashveil-console](https://github.com/GravityblueX/ashveil-console) | Continuous Optimization & Release / Missing formatter or linter dependency / optimize / [open](https://github.com/GravityblueX/ashveil-console/actions/runs/27671446730) |

### Workflow Audit

| Item | Data |
|---|---|
| medium | `automation/github-actions/curate.yml` / 11 / write-permission / Keep write permissions only on release or automation jobs that need them. |
| medium | `automation/github-actions/curate.yml` / 18 / broad-major-action-ref / Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/curate.yml` / 20 / broad-major-action-ref / Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/curate.yml` / 30 / broad-major-action-ref / Consider pinning to a full version tag or SHA for sensitive workflows. |
| medium | `automation/github-actions/maintenance-suite.yml` / 9 / write-permission / Keep write permissions only on release or automation jobs that need them. |

### Secret Audit

- Findings: `0`

### Dependency Radar

- See report for details.

### Dependency Update Config

- See report for details.

### Branch Protection

| Item | Data |
|---|---|
| [GravityblueX/project-forge](https://github.com/GravityblueX/project-forge) | `main` / unprotected / No branch protection endpoint data. |
| [GravityblueX/slider-captcha-lab](https://github.com/GravityblueX/slider-captcha-lab) | `main` / unprotected / No branch protection endpoint data. |
| [GravityblueX/ashveil-console](https://github.com/GravityblueX/ashveil-console) | `main` / unprotected / No branch protection endpoint data. |
| [GravityblueX/YumeBox-MaterialDesign-Study](https://github.com/GravityblueX/YumeBox-MaterialDesign-Study) | `Yume` / unprotected / No branch protection endpoint data. |
| [GravityblueX/BLOG-PAGE](https://github.com/GravityblueX/BLOG-PAGE) | `main` / unknown / gh: Upgrade to GitHub Pro or make this repository public to enable this feature. (HTTP 403) |

### Token Scope

- See report for details.

## Report Files

- `reports/repo-health.md`
- `reports/ci-failures.md`
- `reports/workflow-audit.md`
- `reports/secret-audit.md`
- `reports/dependency-radar.md`
- `reports/dependency-update-config.md`
- `reports/branch-protection.md`
- `reports/token-scope.md`
- `reports/release-notes.md`

## Draft Release Context

See `reports/release-notes.md` for the current release draft.
