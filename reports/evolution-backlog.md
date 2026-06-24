# Evolution Backlog

Last refreshed: 2026-06-24 01:51 UTC

This backlog converts the grounded radar into project-specific next work.
It separates managed repositories from reference-only repositories so borrowed ideas do not become accidental pushes.

## Reference Sources

| Source | Lesson | URL |
|---|---|---|
| OpenSSF Scorecard | turn repository quality into explicit checks instead of taste calls | https://github.com/ossf/scorecard |
| Renovate | make dependency change cadence scheduled, grouped, and reviewable | https://docs.renovatebot.com/configuration-options/ |
| Backstage Software Templates | treat good project structure as a repeatable template | https://backstage.io/docs/features/software-templates/ |
| Playwright Trace Viewer | preserve inspectable evidence for browser failures | https://playwright.dev/docs/trace-viewer |
| Chrome DevTools Protocol Page domain | model deep pages and frames as observable browser state | https://chromedevtools.github.io/devtools-protocol/tot/Page/ |
| Node.js test runner | prefer fast language-native contract tests for small tools | https://nodejs.org/api/test.html |
| Android app signing | verify installability through package metadata and signatures | https://developer.android.com/studio/publish/app-signing |
| Gradle dependency verification | make supply-chain integrity explicit for large builds | https://docs.gradle.org/current/userguide/dependency_verification.html |
| OWASP MASVS | separate study build evidence from production mobile assurance | https://mas.owasp.org/MASVS/ |

## Managed Repositories

### ashveil-console

- Kind: admin console
- Score: `100`
- Remote: `git@github.com:GravityblueX/ashveil-console.git`
- Evidence: tests `package.json: npm run test --prefix backend && npm run test --prefix frontend; backend\package.json: node --test "test/**/*.test.js"; frontend\package.json: node --test "test/**/*.test.js"`; diagnostics `39 report artifacts, 0 logs`; release `44 git tags, 1 release docs`
- Reference anchors: Node.js test runner, Renovate, OpenSSF Scorecard

Next work:
- Add fixture-backed route regression tests for the risk audit and permission matrix views.
- Add a smoke report artifact that records API health, protected-route behavior, and frontend route coverage.
- Keep the existing Prettier debt isolated until a dedicated formatting-only pass is scheduled.
- Keep score at 100 by turning the next important manual check into an automated contract.

### GravityblueX-First-Identify

- Kind: full-stack project-management app
- Score: `100`
- Remote: `git@github.com:GravityblueX/GravityblueX-First-Identify.git`
- Evidence: tests `package.json: turbo test; client\package.json: jest; server\package.json: jest`; diagnostics `4 report artifacts, 0 logs`; release `1 git tags`
- Reference anchors: OpenSSF Scorecard, Node.js test runner, Renovate

Next work:
- Add API contract coverage for the highest-value auth and project routes.
- Add a release-readiness report that records build, test, seed-data, and security-boundary status.
- Promote only runtime-imported server modules into strict TypeScript coverage before widening the tsconfig.
- Keep score at 100 by turning the next important manual check into an automated contract.

### kiogarezaki

- Kind: AI lab workspace
- Score: `100`
- Remote: `git@github.com:GravityblueX/kiogarezaki.git`
- Evidence: tests `projects\idea-triage-board\package.json: npm run build && node --test dist/tests/*.test.js; projects\personal-craft-console\package.json: npm run build && node --test dist/tests/*.test.js`; diagnostics `1 report artifacts, 0 logs`; release `4 git tags`
- Reference anchors: Backstage Software Templates, Node.js test runner, OpenSSF Scorecard

Next work:
- Archive root workspace verification output in the next weekly project report.
- Generate a weekly project promotion report from project TASKS, NOTES, and package metadata.
- Move stale early recovery notes into an archive once no automation references them.
- Keep score at 100 by turning the next important manual check into an automated contract.

### project-forge

- Kind: maintenance toolkit
- Score: `100`
- Remote: `git@github.com:GravityblueX/project-forge.git`
- Evidence: tests `1 Python test files`; diagnostics `29 report artifacts, 0 logs`; release `1 release docs`
- Reference anchors: OpenSSF Scorecard, Backstage Software Templates, Renovate

Next work:
- Ship a release-readiness report for the toolkit itself before creating the first tag.
- Convert repeated report scripts into a small templateable command registry.
- Keep reference sources primary and linked so generated advice is auditable.
- Keep score at 100 by turning the next important manual check into an automated contract.

### slider-captcha-lab

- Kind: authorized browser diagnostics lab
- Score: `100`
- Remote: `git@github.com:GravityblueX/slider-captcha-lab.git`
- Evidence: tests `1 Python test files`; diagnostics `10 report artifacts, 0 logs`; release `5 git tags, 3 release docs`
- Reference anchors: Playwright Trace Viewer, Chrome DevTools Protocol Page domain, OpenSSF Scorecard

Next work:
- Extend the authorized evidence pack with optional local screenshots or Playwright trace artifacts.
- Keep every profile marked local-owned-or-explicitly-authorized and refuse third-party target defaults.
- Use trace-style artifacts for diagnosis, not CAPTCHA bypass or anti-bot evasion.
- Keep score at 100 by turning the next important manual check into an automated contract.

### YumeBox-MaterialDesign-Study

- Kind: Android APK study fork
- Score: `100`
- Remote: `git@github.com:GravityblueX/YumeBox-MaterialDesign-Study.git`
- Evidence: tests `scripts\study-apk-contract.ps1; scripts\verify-installable-apk.ps1`; diagnostics `11 report artifacts, 2 logs`; release `15 git tags, 9 release docs`
- Reference anchors: Android app signing, Gradle dependency verification, OWASP MASVS

Next work:
- Archive the study APK contract output with each future release report.
- Add a real device matrix only after adb install evidence is available for owned or authorized devices.
- Keep debug-keystore signing labeled as study/testing evidence, not production release assurance.
- Keep score at 100 by turning the next important manual check into an automated contract.

### nocturne-admin

- Kind: managed repository
- Score: `91`
- Remote: `git@github.com:GravityblueX/ashveil-console.git`
- Evidence: tests `package.json: npm run test --prefix backend && npm run test --prefix frontend`; diagnostics `39 report artifacts, 0 logs`; release `1 release docs`
- Reference anchors: OpenSSF Scorecard

Next work:
- Add conservative Renovate or Dependabot grouping without automerge.

## Reference-Only Repositories

### AllBeingsFuture

- Remote: `git@github.com:AllBeingsFuture/AllBeingsFuture.git`
- Dirty files: `2`

Boundary:
- Do not push or rewrite this repository from the maintenance pass.
- Use it only as a pattern reference after checking license and owner permission.
- Keep local changes isolated from GravityblueX-owned project commits.

### lux_net

- Remote: `git@github.com:tmzncty/lux_net.git`
- Dirty files: `3`

Boundary:
- Do not push or rewrite this repository from the maintenance pass.
- Use it only as a pattern reference after checking license and owner permission.
- Keep local changes isolated from GravityblueX-owned project commits.

### lux_net-reference

- Remote: `git@github.com:tmzncty/lux_net.git`
- Dirty files: `0`

Boundary:
- Do not push or rewrite this repository from the maintenance pass.
- Use it only as a pattern reference after checking license and owner permission.
- Keep local changes isolated from GravityblueX-owned project commits.
