# Tool Registry

Generated: 2026-06-24T03:14:35.104963+00:00
Status: `OK`
Tools: `8`

| Tool | Command | Output | Reference |
|---|---|---|---|
| Grounded Evolution Radar | `python scripts/grounded_evolution_radar.py --root <workspace>` | `reports/grounded-evolution-radar.md` | OpenSSF Scorecard |
| Evolution Backlog | `python scripts/evolution_backlog.py` | `reports/evolution-backlog.md` | Backstage Software Templates |
| Reference Catalog Check | `python scripts/reference_catalog_check.py` | `reports/reference-catalog-check.md` | primary source documentation |
| Release Readiness | `python scripts/release_readiness_report.py --run-tests` | `reports/project-forge-release-readiness.md` | release-readiness gates |
| Report Index | `python scripts/report_index.py` | `reports/INDEX.md` | inspectable evidence |
| APK Release Forge | `python scripts/apk_release_forge.py <android-project>` | `reports/apk-release-forge.md` | Android app signing |
| Dependency Manifest Radar | `python scripts/dependency_manifest_radar.py <repo>` | `reports/dependency-radar.md` | Renovate |
| Secret Pattern Audit | `python scripts/secret_pattern_audit.py <repo>` | `reports/secret-audit.md` | Gitleaks-style local scan |

## Policy

- A tool is listed only when its script and primary report output exist.
- Each tool maps to a reference pattern so maintenance work stays grounded.
- Commands use explicit local paths or placeholders instead of hidden automation state.
