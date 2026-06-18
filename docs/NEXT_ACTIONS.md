# Next Actions

This file is the working queue for Project Forge. Keep it practical: each task
should be small enough for one focused coding session.

## Priority 1: Repo Health Radar

Why first: it can maintain the owner's existing repos and creates value for
every other project.

- [x] Build `repo_health_radar.py` around `gh repo list`.
- [x] Score README, license, CI, release, issue, and dependency signals.
- [x] Generate `reports/repo-health.md`.
- [ ] Add a weekly workflow.

## Priority 1.5: Maintenance Suite

Why now: it turns the incubator into a practical owner dashboard.

- [x] Add workflow policy auditor.
- [x] Add redacted secret pattern audit.
- [x] Add dependency manifest radar.
- [x] Add release notes studio.
- [x] Add weekly briefing merger.
- [x] Add token scope diagnostics.
- [x] Add dependency update config drafter.
- [x] Add branch protection radar.
- [x] Add report indexer.
- [x] Add repo template factory preview.
- [ ] Activate the workflow after GitHub token workflow permission is available.

## Priority 2: CI Failure Copilot

Why second: it directly reduces notification and failed workflow burden.

- [x] Fetch recent failed workflow runs.
- [x] Pull failing job names and classify likely failure area.
- [x] Extract root-cause snippets from logs.
- [x] Draft fix checklist markdown.

## Priority 3: APK Release Forge

Why third: it compounds the Android work already done in YumeBox.

- [x] Extract reusable release checklist patterns.
- [x] Create a minimal Gradle project detector.
- [x] Generate release notes and checksum guidance.
- [ ] Package as a reusable template.

## Parking Lot

- Browser Trust Lab can absorb the best parts of `slider-captcha-lab` later.
- Local Report Factory can become the shared reporting layer for all tools.
- Privacy Screenshot Redactor is high-signal but should wait until OCR and UI
  choices are clearer.
