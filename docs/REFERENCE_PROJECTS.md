# Reference Projects

Project Forge borrows boring, durable ideas from mature automation projects.
These references are used for direction, not copied implementation.

## Maintenance And Security

- [OpenSSF Scorecard](https://github.com/ossf/scorecard): repository health checks for security posture, branch
  protection, dependency update signals, pinned dependencies, and token
  permissions.
- Gitleaks: local and CI-friendly secret detection with redacted reporting.
- pre-commit: small checks that run before risky changes land.
- [Dependabot](https://docs.github.com/en/code-security/dependabot) and
  [Renovate](https://docs.renovatebot.com/): automated dependency update workflows with
  controlled grouping and scheduling.

## Release Automation

- Release Drafter: release notes assembled from merged changes and labels.
- GitHub Actions Starter Workflows: repeatable CI templates for common stacks.
- semantic-release: consistent versioning and changelog conventions.

## Project Generation

- Cookiecutter and Copier: templates that turn repeatable project structure into
  a command instead of a manual checklist.
- [Backstage Software Templates](https://backstage.io/docs/features/software-templates/):
  catalog-driven service creation with ownership
  and operational metadata.

## Debuggability And Tests

- [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer): a model
  for leaving inspectable traces behind when automation fails.
- [Node.js test runner](https://nodejs.org/api/test.html): a low-friction
  built-in test runner for JavaScript smoke and contract tests.
- [Vue Test Utils](https://test-utils.vuejs.org/guide/): focused component tests
  when UI behavior needs real rendering coverage.

## What Project Forge Keeps

- Score every idea before building it.
- Prefer reports and checklists that can run locally and in CI.
- Redact risky data by default.
- Keep templates inactive until the owner explicitly enables workflow files.
- Prefer boring evidence over speculative ideas: build output, test output,
  release artifacts, reports, and reproducible scripts.
