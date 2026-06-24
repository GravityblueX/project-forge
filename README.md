# Project Forge

Project Forge is a small incubator for high-value, maintainable software ideas.

It is designed for a busy owner: each project has a card, a clear MVP, a value
score, and a weekly automation that refreshes the project scoreboard.

## Principles

- Build useful tools, not empty repos.
- Prefer local-first, authorized, privacy-preserving workflows.
- Keep each project small enough to become a real MVP.
- Track value with repeatable scoring instead of hype.
- Avoid projects that depend on bypassing third-party controls or violating terms.

## Current Seeds

Run:

```bash
python scripts/curate_projects.py
```

This regenerates:

```text
docs/PROJECT_SCOREBOARD.md
```

## Ready-to-Run Tools

Project Forge now includes a small maintenance toolkit:

```bash
python scripts/repo_health_radar.py --owner GravityblueX --deep
python scripts/ci_failure_copilot.py --owner GravityblueX
python scripts/apk_release_forge.py C:\path\to\android-project
python scripts/workflow_policy_auditor.py .
python scripts/secret_pattern_audit.py .
python scripts/dependency_manifest_radar.py .
python scripts/release_notes_studio.py .
python scripts/maintenance_briefing.py
python scripts/token_scope_doctor.py
python scripts/dependency_update_config_drafter.py C:\path\to\repo
python scripts/branch_protection_radar.py --owner GravityblueX
python scripts/repo_template_factory.py --name valuable-tool
python scripts/grounded_evolution_radar.py --root C:\Users\123\Documents\Codex\2026-06-18\new-chat-5\work --root C:\Users\123\Desktop
python scripts/evolution_backlog.py
python scripts/release_readiness_report.py --run-tests
python scripts/report_index.py
```

Run the project verification suite:

```bash
python -m unittest discover -s tests
```

Generated reports are written to `reports/`.

Start with:

```text
reports/INDEX.md
reports/weekly-briefing.md
reports/grounded-evolution-radar.md
reports/evolution-backlog.md
reports/project-forge-release-readiness.md
```

## References

The direction is documented in `docs/REFERENCE_PROJECTS.md` and
`docs/GROUNDED_REFERENCE_CATALOG.md`. The toolkit is inspired by mature
maintenance tools such as OpenSSF Scorecard, Renovate, Release Drafter,
Gitleaks, pre-commit, Cookiecutter, Copier, Backstage templates, Playwright
Trace Viewer, Android app signing, and OWASP MASVS.

## Project Cards

Project cards live in `projects/*.json`. A card describes:

- audience
- problem
- MVP
- defensibility
- maintenance burden
- monetization or portfolio value
- next concrete tasks

## Automation

The workflow template lives at:

```text
automation/github-actions/curate.yml
automation/github-actions/maintenance-suite.yml
```

When GitHub workflow permissions are available, copy it to:

```text
.github/workflows/curate.yml
```

It runs the curator weekly and on every push. If the generated scoreboard
changes, the workflow commits the refreshed file back to the repo.
