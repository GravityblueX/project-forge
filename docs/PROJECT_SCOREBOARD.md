# Project Scoreboard

Last refreshed: 2026-06-24 01:02 UTC

| Rank | Project | Score | Audience | Tags |
|---:|---|---:|---|---|
| 1 | [Repo Health Radar](../projects/repo-health-radar.json) | 8.79 | solo developers and small teams | github, automation, maintenance |
| 2 | [Workflow Permission Auditor](../projects/workflow-permission-auditor.json) | 8.72 | GitHub repository owners | github-actions, security, automation |
| 3 | [Dependency Config Drafter](../projects/dependency-config-drafter.json) | 8.68 | developers adding automated dependency updates | dependencies, renovate, dependabot |
| 4 | [Repo Template Factory](../projects/repo-template-factory.json) | 8.59 | solo builders who start many small tools | templates, scaffolding, developer-tools |
| 5 | [Report Indexer](../projects/report-indexer.json) | 8.59 | busy maintainers with many generated reports | reports, docs, automation |
| 6 | [APK Release Forge](../projects/apk-release-forge.json) | 8.58 | Android learners and indie app maintainers | android, release, github-actions |
| 7 | [CI Failure Copilot](../projects/ci-failure-copilot.json) | 8.56 | maintainers who use GitHub Actions | github-actions, developer-tools, triage |
| 8 | [Maintenance Briefing Bot](../projects/maintenance-briefing-bot.json) | 8.54 | busy repository owners | reports, automation, planning |
| 9 | [Secret Pattern Audit](../projects/secret-pattern-audit.json) | 8.54 | solo developers and small teams | security, local-first, scanner |
| 10 | [Release Notes Studio](../projects/release-notes-studio.json) | 8.47 | developers who publish frequent small releases | release, changelog, git |
| 11 | [Dependency Update Conductor](../projects/dependency-update-conductor.json) | 8.43 | maintainers with several small repos | dependencies, renovate, dependabot |
| 12 | [Local Report Factory](../projects/local-report-factory.json) | 8.43 | people who need repeatable PDFs, HTML reports, and project summaries | reports, html, pdf |
| 13 | [Personal Release Notes Bot](../projects/personal-release-notes-bot.json) | 8.39 | solo builders with multiple small repos | changelog, github, portfolio |
| 14 | [Automation Runbook Studio](../projects/automation-runbook-studio.json) | 8.23 | power users who automate repetitive desktop and web workflows | automation, runbooks, ops |
| 15 | [Branch Protection Radar](../projects/branch-protection-radar.json) | 8.19 | GitHub repository owners | github, security, governance |
| 16 | [Privacy Screenshot Redactor](../projects/privacy-screenshot-redactor.json) | 8.09 | support teams, developers, and creators | privacy, images, local-first |
| 17 | [Local Knowledge Vault](../projects/local-knowledge-vault.json) | 8.08 | students, researchers, and personal knowledge workers | local-first, knowledge, privacy |
| 18 | [Browser Trust Lab](../projects/browser-trust-lab.json) | 8.02 | QA engineers and authorized security testers | browser, qa, diagnostics |
| 19 | [Action Version Pinner](../projects/action-version-pinner.json) | 7.98 | GitHub Actions users | github-actions, supply-chain, ci |
| 20 | [Game Session Ledger](../projects/game-session-ledger.json) | 7.92 | players who want light personal analytics | gaming, local-first, analytics |
| 21 | [Token Scope Doctor](../projects/token-scope-doctor.json) | 7.91 | developers using GitHub CLI and automation tokens | github, auth, security |

## Top Project Briefs

### Repo Health Radar

- Slug: `repo-health-radar`
- Value score: `8.79`
- Problem: Small repos quietly decay: broken CI, stale dependencies, missing releases, and unclear next actions.
- MVP: A CLI that scans GitHub repos, scores health, and writes a prioritized maintenance report.
- Next tasks: Implement gh-based repo discovery, Score CI, releases, issues, dependency files, and README quality, Generate docs/health-report.md, Add weekly GitHub Action
- Main risks: API rate limits, False positives for intentionally quiet repos, Private repo permissions

### Workflow Permission Auditor

- Slug: `workflow-permission-auditor`
- Value score: `8.72`
- Problem: Actions workflows often accumulate broad token permissions, mutable action refs, and risky triggers without anyone noticing.
- MVP: A local CLI that scans workflow YAML files and writes a risk-ranked report with concrete fixes.
- Next tasks: Scan workflow permissions and risky triggers, Flag mutable action refs, Generate reports/workflow-audit.md, Add remediation snippets
- Main risks: YAML parsing edge cases, False positives on intentionally broad release workflows, Different repositories use different policy tolerance

### Dependency Config Drafter

- Slug: `dependency-config-drafter`
- Value score: `8.68`
- Problem: Renovate and Dependabot are powerful, but the first configuration decision slows people down.
- MVP: A scanner that detects ecosystems and writes safe Renovate and Dependabot draft configs into a report.
- Next tasks: Detect npm, pip, and Gradle manifests, Draft Renovate config, Draft Dependabot config, Add review notes
- Main risks: Generated configs must be reviewed before use, Private registries need extra secrets, Automerge should remain disabled by default

### Repo Template Factory

- Slug: `repo-template-factory`
- Value score: `8.59`
- Problem: New projects lose time recreating README, license, CI, reports, and release checklists.
- MVP: A template generator that creates a clean local project skeleton with selected maintenance tools wired in.
- Next tasks: Create Python CLI scaffold command, Add README and license templates, Add optional report scripts, Generate dry-run preview
- Main risks: Templates can become stale, Too many options slow down creation, Should not overwrite user files without confirmation

### Report Indexer

- Slug: `report-indexer`
- Value score: `8.59`
- Problem: Reports lose value when the owner has to remember which file contains which signal.
- MVP: A report index generator that lists every generated report with its headline metric.
- Next tasks: Index markdown reports, Extract title and first useful metric, Generate reports/INDEX.md, Link index from README
- Main risks: Report formats may drift, Too much indexing can duplicate weekly briefing, Needs stable relative links

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

### Maintenance Briefing Bot

- Slug: `maintenance-briefing-bot`
- Value score: `8.54`
- Problem: Reports are useful only when the owner can quickly see what matters this week.
- MVP: A summarizer that merges health, CI, dependency, secret, and release reports into one short weekly briefing.
- Next tasks: Collect generated reports, Extract top risks and next actions, Generate reports/weekly-briefing.md, Add owner-friendly priority labels
- Main risks: Summaries can hide important details, Needs stable report formats, Should avoid hype and keep actions concrete

### Secret Pattern Audit

- Slug: `secret-pattern-audit`
- Value score: `8.54`
- Problem: Secrets can land in scripts, logs, reports, and config files long before a full security platform is installed.
- MVP: A redacting local scanner that checks common text files for secret-like patterns and writes a safe report.
- Next tasks: Add redacted pattern scanner, Skip generated and dependency directories, Generate reports/secret-audit.md, Provide allowlist support
- Main risks: False positives in documentation, Must never print raw secrets, Regex coverage is not a replacement for mature scanners

### Release Notes Studio

- Slug: `release-notes-studio`
- Value score: `8.47`
- Problem: Manual release notes are easy to skip, while fully automated notes often miss verification and artifact details.
- MVP: A CLI that turns git history into categorized release notes with verification and artifact sections.
- Next tasks: Read git history since last tag, Categorize conventional commits, Generate reports/release-notes.md, Add artifact checksum hooks
- Main risks: Messy commit messages reduce quality, Tag strategy differs by repo, Human review is still needed before publishing

### Dependency Update Conductor

- Slug: `dependency-update-conductor`
- Value score: `8.43`
- Problem: Dependency updates are valuable but noisy; small repos need grouping, scheduling, and clear risk notes.
- MVP: A tool that detects dependency manifests and drafts Renovate or Dependabot configuration suggestions.
- Next tasks: Scan dependency manifests, Group ecosystems by risk, Draft config templates, Generate reports/dependency-radar.md
- Main risks: Version advice may be ecosystem-specific, Breaking changes still need tests, Private package registries need custom configuration

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

### Branch Protection Radar

- Slug: `branch-protection-radar`
- Value score: `8.19`
- Problem: Default branches can remain unprotected even after a project starts publishing releases or accepting automation changes.
- MVP: A GitHub CLI based report that checks default branch protection across active repositories.
- Next tasks: Check default branch protection endpoint, Report active unprotected repositories, Recommend baseline status checks, Merge into weekly briefing
- Main risks: Private repo permissions may hide protection status, Solo projects may intentionally keep lightweight branches, Rulesets need separate handling

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

### Action Version Pinner

- Slug: `action-version-pinner`
- Value score: `7.98`
- Problem: Workflows that use moving refs such as main or master can change behavior without a code review.
- MVP: A scanner that lists unpinned actions and suggests safer version pinning work.
- Next tasks: Detect uses: owner/action@ref entries, Flag mutable refs, Group by workflow, Link to workflow auditor
- Main risks: Full SHA pinning can be noisy to maintain, Major-version refs are common and sometimes acceptable, Reusable workflows need separate handling

### Game Session Ledger

- Slug: `game-session-ledger`
- Value score: `7.92`
- Problem: Game time, mood, wins, losses, and learning goals are hard to review without annoying manual tracking.
- MVP: A lightweight local journal that logs sessions, tags games, and generates weekly summaries.
- Next tasks: Create session JSON format, Build CLI add/list/report commands, Generate weekly markdown summary, Add optional CSV export
- Main risks: May be too small unless polished, Manual entry friction, Needs privacy-first defaults

### Token Scope Doctor

- Slug: `token-scope-doctor`
- Value score: `7.91`
- Problem: Automation gets stuck when tokens have too little scope, but broad permanent tokens are risky.
- MVP: A diagnostic that explains current GitHub auth scopes, workflow limitations, and least-privilege next steps.
- Next tasks: Read gh auth status, Detect workflow scope gaps, Explain safe scope upgrades, Generate reports/token-scope.md
- Main risks: Do not print token values, Different hosts and auth methods behave differently, Scope names evolve over time
