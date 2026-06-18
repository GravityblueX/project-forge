# Project Scoreboard

Last refreshed: 2026-06-18 10:12 UTC

| Rank | Project | Score | Audience | Tags |
|---:|---|---:|---|---|
| 1 | [Repo Health Radar](../projects/repo-health-radar.json) | 8.79 | solo developers and small teams | github, automation, maintenance |
| 2 | [APK Release Forge](../projects/apk-release-forge.json) | 8.58 | Android learners and indie app maintainers | android, release, github-actions |
| 3 | [CI Failure Copilot](../projects/ci-failure-copilot.json) | 8.56 | maintainers who use GitHub Actions | github-actions, developer-tools, triage |
| 4 | [Local Report Factory](../projects/local-report-factory.json) | 8.43 | people who need repeatable PDFs, HTML reports, and project summaries | reports, html, pdf |
| 5 | [Personal Release Notes Bot](../projects/personal-release-notes-bot.json) | 8.39 | solo builders with multiple small repos | changelog, github, portfolio |
| 6 | [Automation Runbook Studio](../projects/automation-runbook-studio.json) | 8.23 | power users who automate repetitive desktop and web workflows | automation, runbooks, ops |
| 7 | [Privacy Screenshot Redactor](../projects/privacy-screenshot-redactor.json) | 8.09 | support teams, developers, and creators | privacy, images, local-first |
| 8 | [Local Knowledge Vault](../projects/local-knowledge-vault.json) | 8.08 | students, researchers, and personal knowledge workers | local-first, knowledge, privacy |
| 9 | [Browser Trust Lab](../projects/browser-trust-lab.json) | 8.02 | QA engineers and authorized security testers | browser, qa, diagnostics |
| 10 | [Game Session Ledger](../projects/game-session-ledger.json) | 7.92 | players who want light personal analytics | gaming, local-first, analytics |

## Top Project Briefs

### Repo Health Radar

- Slug: `repo-health-radar`
- Value score: `8.79`
- Problem: Small repos quietly decay: broken CI, stale dependencies, missing releases, and unclear next actions.
- MVP: A CLI that scans GitHub repos, scores health, and writes a prioritized maintenance report.
- Next tasks: Implement gh-based repo discovery, Score CI, releases, issues, dependency files, and README quality, Generate docs/health-report.md, Add weekly GitHub Action
- Main risks: API rate limits, False positives for intentionally quiet repos, Private repo permissions

### APK Release Forge

- Slug: `apk-release-forge`
- Value score: `8.58`
- Problem: Small Android projects often fail at repeatable APK builds, release notes, artifacts, and version hygiene.
- MVP: A reusable GitHub Actions template and local strict build script for Android APK releases.
- Next tasks: Generalize YumeBox build scripts, Create version bump helper, Generate release notes from commits, Upload APK artifacts and checksums
- Main risks: Different Gradle project layouts, Signing key handling, Large Android SDK setup time

### CI Failure Copilot

- Slug: `ci-failure-copilot`
- Value score: `8.56`
- Problem: CI failures are noisy; the useful signal is buried in logs and old failed notifications pile up.
- MVP: A local CLI that summarizes recent failed runs, groups root causes, and drafts fix checklists.
- Next tasks: Fetch recent workflow failures with gh api, Extract failing step logs, Classify dependency, lint, test, packaging, and permission failures, Write markdown triage reports
- Main risks: Large log volume, Secrets redaction, Ambiguous root causes

### Local Report Factory

- Slug: `local-report-factory`
- Value score: `8.43`
- Problem: Reports are often handcrafted, inconsistent, and hard to regenerate after data changes.
- MVP: A template-driven report generator that turns JSON or CSV into polished HTML and PDF bundles.
- Next tasks: Define report manifest format, Render HTML with Jinja templates, Add PDF export path, Include repo health and browser diagnostic examples
- Main risks: PDF rendering dependencies, Template design quality, Input schema sprawl

### Personal Release Notes Bot

- Slug: `personal-release-notes-bot`
- Value score: `8.39`
- Problem: Good work disappears because releases, changelogs, screenshots, and artifacts are not summarized consistently.
- MVP: A CLI that reads commits and GitHub artifacts, then drafts human-friendly release notes.
- Next tasks: Read commits since latest tag, Group changes by feature, fix, build, docs, Link artifacts and workflow runs, Write release draft markdown
- Main risks: Commit messages may be messy, Artifact retention limits, Release style preferences vary

### Automation Runbook Studio

- Slug: `automation-runbook-studio`
- Value score: `8.23`
- Problem: Automations become fragile when steps, permissions, credentials, and recovery instructions are not documented.
- MVP: A runbook format plus validator that turns automation steps into auditable markdown and JSON.
- Next tasks: Define runbook JSON schema, Generate markdown documentation, Validate required safety fields, Add examples for GitHub, browser QA, and releases
- Main risks: Too abstract without examples, Needs good templates, May overlap with workflow engines

### Privacy Screenshot Redactor

- Slug: `privacy-screenshot-redactor`
- Value score: `8.09`
- Problem: Screenshots often leak names, tokens, emails, URLs, and private file paths before sharing.
- MVP: A local image tool that detects text regions and helps redact sensitive snippets before export.
- Next tasks: Prototype manual rectangle redaction, Add OCR text extraction, Highlight likely secrets and emails, Export before/after audit metadata
- Main risks: OCR setup complexity, False negatives are sensitive, Needs clear privacy guarantees

### Local Knowledge Vault

- Slug: `local-knowledge-vault`
- Value score: `8.08`
- Problem: Useful notes, PDFs, screenshots, and repo docs are scattered and hard to retrieve privately.
- MVP: A local indexer that summarizes folders into searchable markdown cards without uploading private files.
- Next tasks: Index markdown, text, and filenames, Generate daily digest, Add SQLite full-text search, Add optional local embedding backend
- Main risks: Document parsing edge cases, Privacy expectations, Search quality without embeddings

### Browser Trust Lab

- Slug: `browser-trust-lab`
- Value score: `8.02`
- Problem: Modern pages hide state in frames, extensions, browser profiles, and event chains, making authorized diagnosis hard.
- MVP: A local-first browser diagnostic tool that records frames, selectors, event chains, and profile differences.
- Next tasks: Extract reusable pieces from slider-captcha-lab, Add profile comparison reports, Add frame tree visualization, Export HTML evidence bundles
- Main risks: Must keep strict authorized-use boundaries, Browser APIs change often, Can be misunderstood as a bypass tool

### Game Session Ledger

- Slug: `game-session-ledger`
- Value score: `7.92`
- Problem: Game time, mood, wins, losses, and learning goals are hard to review without annoying manual tracking.
- MVP: A lightweight local journal that logs sessions, tags games, and generates weekly summaries.
- Next tasks: Create session JSON format, Build CLI add/list/report commands, Generate weekly markdown summary, Add optional CSV export
- Main risks: May be too small unless polished, Manual entry friction, Needs privacy-first defaults
