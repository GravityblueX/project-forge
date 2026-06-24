from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "GROUNDED_REFERENCE_CATALOG.md"
DEFAULT_JSON = ROOT / "reports" / "reference-catalog-check.json"
DEFAULT_MARKDOWN = ROOT / "reports" / "reference-catalog-check.md"


@dataclass(frozen=True)
class ReferenceExpectation:
    name: str
    url: str
    local_artifact: str
    reason: str


EXPECTED_REFERENCES = [
    ReferenceExpectation(
        "OpenSSF Scorecard",
        "https://github.com/ossf/scorecard",
        "scripts/grounded_evolution_radar.py",
        "repository health is represented as measurable local gates",
    ),
    ReferenceExpectation(
        "Renovate",
        "https://docs.renovatebot.com/configuration-options/",
        "renovate.json",
        "dependency cadence is scheduled and reviewable",
    ),
    ReferenceExpectation(
        "Backstage Software Templates",
        "https://backstage.io/docs/features/software-templates/",
        "scripts/repo_template_factory.py",
        "repeatable structure can graduate into templates",
    ),
    ReferenceExpectation(
        "Playwright Trace Viewer",
        "https://playwright.dev/docs/trace-viewer",
        "reports/grounded-evolution-radar.md",
        "diagnostic evidence should be inspectable",
    ),
    ReferenceExpectation(
        "Chrome DevTools Protocol Page domain",
        "https://chromedevtools.github.io/devtools-protocol/tot/Page/",
        "docs/GROUNDED_REFERENCE_CATALOG.md",
        "browser/frame references remain tied to official protocol docs",
    ),
    ReferenceExpectation(
        "Android app signing",
        "https://developer.android.com/studio/publish/app-signing",
        "scripts/apk_release_forge.py",
        "APK claims are separated into signing, metadata, and release evidence",
    ),
    ReferenceExpectation(
        "Gradle dependency verification",
        "https://docs.gradle.org/current/userguide/dependency_verification.html",
        "reports/yumebox-dependency-radar.md",
        "large Android builds need explicit supply-chain evidence",
    ),
    ReferenceExpectation(
        "OWASP MASVS",
        "https://mas.owasp.org/MASVS/",
        "reports/yumebox-apk-release.md",
        "mobile assurance is separate from simple installability",
    ),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def build_report() -> dict[str, Any]:
    catalog = read_text(CATALOG)
    rows: list[dict[str, Any]] = []
    for expected in EXPECTED_REFERENCES:
        local_path = ROOT / expected.local_artifact
        checks = [
            {"name": "name in catalog", "ok": expected.name in catalog, "detail": expected.name},
            {"name": "primary url in catalog", "ok": expected.url in catalog, "detail": expected.url},
            {"name": "local artifact exists", "ok": local_path.exists(), "detail": expected.local_artifact},
        ]
        rows.append({
            "name": expected.name,
            "url": expected.url,
            "local_artifact": expected.local_artifact,
            "reason": expected.reason,
            "ok": all(check["ok"] for check in checks),
            "checks": checks,
        })
    failures = [row for row in rows if not row["ok"]]
    return {
        "report_type": "reference_catalog_check",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "catalog": str(CATALOG),
        "ok": len(failures) == 0,
        "references": rows,
        "failures": failures,
        "policy": [
            "Use primary documentation or original project repositories as reference sources.",
            "Translate references into local tests, scripts, reports, or release gates.",
            "Do not copy third-party code, assets, branding, prompts, or private workflows.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Reference Catalog Check",
        "",
        f"Generated: {report['generated_at']}",
        f"Status: `{'OK' if report['ok'] else 'FAIL'}`",
        "",
        "## References",
        "",
        "| Reference | Result | Local Artifact |",
        "|---|---|---|",
    ]
    for row in report["references"]:
        lines.append(f"| [{row['name']}]({row['url']}) | {'OK' if row['ok'] else 'FAIL'} | `{row['local_artifact']}` |")
    lines.extend(["", "## Policy", ""])
    for item in report["policy"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify that reference catalog entries are primary and locally actionable.")
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    report = build_report()
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    args.markdown_out.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"ok": report["ok"], "json": str(args.json_out), "markdown": str(args.markdown_out)}, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
