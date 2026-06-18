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
```

When GitHub workflow permissions are available, copy it to:

```text
.github/workflows/curate.yml
```

It runs the curator weekly and on every push. If the generated scoreboard
changes, the workflow commits the refreshed file back to the repo.
