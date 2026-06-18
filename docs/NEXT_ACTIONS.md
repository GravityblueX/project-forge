# Next Actions

This file is the working queue for Project Forge. Keep it practical: each task
should be small enough for one focused coding session.

## Priority 1: Repo Health Radar

Why first: it can maintain the owner's existing repos and creates value for
every other project.

- [ ] Build `repo_health_radar.py` around `gh repo list`.
- [ ] Score README, license, CI, release, issue, and dependency signals.
- [ ] Generate `reports/repo-health.md`.
- [ ] Add a weekly workflow.

## Priority 2: CI Failure Copilot

Why second: it directly reduces notification and failed workflow burden.

- [ ] Fetch recent failed workflow runs.
- [ ] Pull failing job logs.
- [ ] Extract root-cause snippets.
- [ ] Draft fix checklist markdown.

## Priority 3: APK Release Forge

Why third: it compounds the Android work already done in YumeBox.

- [ ] Extract reusable strict build script patterns.
- [ ] Create a minimal Gradle project detector.
- [ ] Generate release notes and checksum files.
- [ ] Package as a reusable template.

## Parking Lot

- Browser Trust Lab can absorb the best parts of `slider-captcha-lab` later.
- Local Report Factory can become the shared reporting layer for all tools.
- Privacy Screenshot Redactor is high-signal but should wait until OCR and UI
  choices are clearer.
