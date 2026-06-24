# Grounded Reference Catalog

This catalog keeps the project-evolution work tied to primary sources and concrete local signals. It is a guide for borrowing patterns, not code, assets, product names, or private workflow details.

| Area | Primary Source | Borrowed Pattern | Local Use |
| --- | --- | --- | --- |
| Repository health | OpenSSF Scorecard: https://github.com/ossf/scorecard | Make health measurable with checks. | `grounded_evolution_radar.py` scores README, license, tests, dependency cadence, diagnostics, and safety boundaries. |
| Dependency cadence | Renovate docs: https://docs.renovatebot.com/configuration-options/ | Scheduled grouped updates without silent automerge. | Each managed repo gets conservative `renovate.json` before broader automation. |
| Repeatable project setup | Backstage Software Templates: https://backstage.io/docs/features/software-templates/ | Encode good structure as a repeatable workflow. | `project-forge` should turn successful project/report patterns into templates. |
| Browser diagnostics | Playwright Trace Viewer: https://playwright.dev/docs/trace-viewer | Preserve inspectable failure evidence. | `slider-captcha-lab` should emit local-only evidence packs rather than opaque pass/fail logs. |
| Browser state model | Chrome DevTools Protocol Page domain: https://chromedevtools.github.io/devtools-protocol/tot/Page/ | Treat frames and page state as explicit data. | Deep-page diagnostics should record frame maps and selectors under authorized scope only. |
| Fast tests | Node.js test runner: https://nodejs.org/api/test.html | Prefer low-friction contract tests. | Small Node projects use native `node --test`; Python tools use `unittest`. |
| Android installability | Android app signing: https://developer.android.com/studio/publish/app-signing | Verify package metadata and signing before release claims. | Yume study APKs keep zipalign, badging, signature, digest, and installability reports. |
| Build supply chain | Gradle dependency verification: https://docs.gradle.org/current/userguide/dependency_verification.html | Record dependency trust explicitly. | Yume should graduate from APK evidence to dependency verification when the build stabilizes. |
| Mobile assurance | OWASP MASVS: https://mas.owasp.org/MASVS/ | Separate security assurance from simple installability. | Study APK evidence is not presented as production mobile security certification. |

## Operating Rules

- Use primary docs or the original project repository when adding a reference.
- Translate references into local checks, scripts, reports, or tests.
- Do not copy third-party source, assets, names, prompts, private workflows, or commercial positioning.
- Keep CAPTCHA/browser work limited to local, owned, or explicitly authorized pages.
- Mark friend repositories as reference-only unless the owner explicitly asks for direct changes.
