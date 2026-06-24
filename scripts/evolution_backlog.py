from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RADAR = ROOT / "reports" / "grounded-evolution-radar.json"
DEFAULT_OUTPUT = ROOT / "reports" / "evolution-backlog.md"
DEFAULT_JSON = ROOT / "reports" / "evolution-backlog.json"


@dataclass(frozen=True)
class ReferenceSource:
    key: str
    name: str
    url: str
    lesson: str


REFERENCE_SOURCES = [
    ReferenceSource(
        "scorecard",
        "OpenSSF Scorecard",
        "https://github.com/ossf/scorecard",
        "turn repository quality into explicit checks instead of taste calls",
    ),
    ReferenceSource(
        "renovate",
        "Renovate",
        "https://docs.renovatebot.com/configuration-options/",
        "make dependency change cadence scheduled, grouped, and reviewable",
    ),
    ReferenceSource(
        "backstage-templates",
        "Backstage Software Templates",
        "https://backstage.io/docs/features/software-templates/",
        "treat good project structure as a repeatable template",
    ),
    ReferenceSource(
        "playwright-trace",
        "Playwright Trace Viewer",
        "https://playwright.dev/docs/trace-viewer",
        "preserve inspectable evidence for browser failures",
    ),
    ReferenceSource(
        "cdp-page",
        "Chrome DevTools Protocol Page domain",
        "https://chromedevtools.github.io/devtools-protocol/tot/Page/",
        "model deep pages and frames as observable browser state",
    ),
    ReferenceSource(
        "node-test-runner",
        "Node.js test runner",
        "https://nodejs.org/api/test.html",
        "prefer fast language-native contract tests for small tools",
    ),
    ReferenceSource(
        "android-signing",
        "Android app signing",
        "https://developer.android.com/studio/publish/app-signing",
        "verify installability through package metadata and signatures",
    ),
    ReferenceSource(
        "gradle-verification",
        "Gradle dependency verification",
        "https://docs.gradle.org/current/userguide/dependency_verification.html",
        "make supply-chain integrity explicit for large builds",
    ),
    ReferenceSource(
        "owasp-masvs",
        "OWASP MASVS",
        "https://mas.owasp.org/MASVS/",
        "separate study build evidence from production mobile assurance",
    ),
]


PROJECT_PROFILES: dict[str, dict[str, Any]] = {
    "GravityblueX-First-Identify": {
        "kind": "full-stack project-management app",
        "sources": ["scorecard", "node-test-runner", "renovate"],
        "next": [
            "Add API contract coverage for the highest-value auth and project routes.",
            "Add a release-readiness report that records build, test, seed-data, and security-boundary status.",
            "Promote only runtime-imported server modules into strict TypeScript coverage before widening the tsconfig.",
        ],
    },
    "ashveil-console": {
        "kind": "admin console",
        "sources": ["node-test-runner", "renovate", "scorecard"],
        "next": [
            "Add fixture-backed route regression tests for the risk audit and permission matrix views.",
            "Add a smoke report artifact that records API health, protected-route behavior, and frontend route coverage.",
            "Keep the existing Prettier debt isolated until a dedicated formatting-only pass is scheduled.",
        ],
    },
    "slider-captcha-lab": {
        "kind": "authorized browser diagnostics lab",
        "sources": ["playwright-trace", "cdp-page", "scorecard"],
        "next": [
            "Extend the authorized evidence pack with optional local screenshots or Playwright trace artifacts.",
            "Keep every profile marked local-owned-or-explicitly-authorized and refuse third-party target defaults.",
            "Use trace-style artifacts for diagnosis, not CAPTCHA bypass or anti-bot evasion.",
        ],
    },
    "kiogarezaki": {
        "kind": "AI lab workspace",
        "sources": ["backstage-templates", "node-test-runner", "scorecard"],
        "next": [
            "Archive root workspace verification output in the next weekly project report.",
            "Generate a weekly project promotion report from project TASKS, NOTES, and package metadata.",
            "Move stale early recovery notes into an archive once no automation references them.",
        ],
    },
    "project-forge": {
        "kind": "maintenance toolkit",
        "sources": ["scorecard", "backstage-templates", "renovate"],
        "next": [
            "Ship a release-readiness report for the toolkit itself before creating the first tag.",
            "Convert repeated report scripts into a small templateable command registry.",
            "Keep reference sources primary and linked so generated advice is auditable.",
        ],
    },
    "YumeBox-MaterialDesign-Study": {
        "kind": "Android APK study fork",
        "sources": ["android-signing", "gradle-verification", "owasp-masvs"],
        "next": [
            "Archive the study APK contract output with each future release report.",
            "Add a real device matrix only after adb install evidence is available for owned or authorized devices.",
            "Keep debug-keystore signing labeled as study/testing evidence, not production release assurance.",
        ],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_lookup() -> dict[str, ReferenceSource]:
    return {source.key: source for source in REFERENCE_SOURCES}


def is_gravitybluex_repo(row: dict[str, Any]) -> bool:
    remote = str(row.get("remote", ""))
    return "github.com:GravityblueX/" in remote or "github.com/GravityblueX/" in remote


def row_check(row: dict[str, Any], name: str) -> dict[str, Any] | None:
    for check in row.get("checks", []):
        if check.get("name") == name:
            return check
    return None


def gap_items(row: dict[str, Any]) -> list[str]:
    items: list[str] = []
    for check in row.get("checks", []):
        if check.get("ok"):
            continue
        name = check.get("name")
        if name == "meaningful tests":
            items.append("Add a fast contract test command that exercises real behavior.")
        elif name == "dependency automation":
            items.append("Add conservative Renovate or Dependabot grouping without automerge.")
        elif name == "diagnostic artifacts":
            items.append("Emit markdown and JSON evidence for verification runs.")
        elif name == "release evidence":
            items.append("Create a release-readiness report before tagging.")
        elif name == "safety boundary":
            items.append("Document authorized use, local-only scope, and non-production caveats.")
        elif name == "ci workflow":
            items.append("Add a minimal CI gate that runs build and tests.")
        elif name == "license":
            items.append("Add license metadata if reuse is intended.")
        elif name == "readme":
            items.append("Add a README with purpose, setup, verification, and boundaries.")
    return items


def managed_backlog(row: dict[str, Any]) -> dict[str, Any]:
    name = str(row["name"])
    profile = PROJECT_PROFILES.get(name, {})
    sources = [source_lookup()[key] for key in profile.get("sources", ["scorecard"])]
    items = list(profile.get("next", []))
    gaps = gap_items(row)
    if gaps:
        items = gaps + items
    elif int(row.get("score", 0)) >= 100:
        items.append("Keep score at 100 by turning the next important manual check into an automated contract.")

    return {
        "name": name,
        "path": row.get("path"),
        "remote": row.get("remote"),
        "kind": profile.get("kind", "managed repository"),
        "score": row.get("score"),
        "managed": True,
        "sources": [source.__dict__ for source in sources],
        "items": dedupe(items),
        "currentEvidence": {
            "tests": (row_check(row, "meaningful tests") or {}).get("note", ""),
            "diagnostics": (row_check(row, "diagnostic artifacts") or {}).get("note", ""),
            "release": (row_check(row, "release evidence") or {}).get("note", ""),
        },
    }


def reference_backlog(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": row.get("name"),
        "path": row.get("path"),
        "remote": row.get("remote"),
        "kind": "reference-only repository",
        "score": row.get("score"),
        "managed": False,
        "sources": [],
        "items": [
            "Do not push or rewrite this repository from the maintenance pass.",
            "Use it only as a pattern reference after checking license and owner permission.",
            "Keep local changes isolated from GravityblueX-owned project commits.",
        ],
        "currentEvidence": {
            "dirtyCount": row.get("dirtyCount"),
            "head": row.get("head"),
        },
    }


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        output.append(item)
    return output


def build_backlog(payload: dict[str, Any]) -> dict[str, Any]:
    repos = payload.get("repositories", [])
    entries = []
    for row in sorted(repos, key=lambda item: str(item.get("name", "")).lower()):
        if is_gravitybluex_repo(row):
            entries.append(managed_backlog(row))
        else:
            entries.append(reference_backlog(row))
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "radarGeneratedAt": payload.get("generatedAt"),
        "referenceSources": [source.__dict__ for source in REFERENCE_SOURCES],
        "entries": entries,
    }


def render_markdown(backlog: dict[str, Any]) -> str:
    generated = datetime.fromisoformat(backlog["generatedAt"]).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Evolution Backlog",
        "",
        f"Last refreshed: {generated}",
        "",
        "This backlog converts the grounded radar into project-specific next work.",
        "It separates managed repositories from reference-only repositories so borrowed ideas do not become accidental pushes.",
        "",
        "## Reference Sources",
        "",
        "| Source | Lesson | URL |",
        "|---|---|---|",
    ]
    for source in backlog["referenceSources"]:
        lines.append(f"| {source['name']} | {source['lesson']} | {source['url']} |")

    managed = [entry for entry in backlog["entries"] if entry["managed"]]
    references = [entry for entry in backlog["entries"] if not entry["managed"]]

    lines.extend(["", "## Managed Repositories", ""])
    for entry in sorted(managed, key=lambda item: (-int(item.get("score", 0)), str(item["name"]).lower())):
        lines.extend([
            f"### {entry['name']}",
            "",
            f"- Kind: {entry['kind']}",
            f"- Score: `{entry['score']}`",
            f"- Remote: `{entry['remote']}`",
            f"- Evidence: tests `{entry['currentEvidence'].get('tests', '')}`; diagnostics `{entry['currentEvidence'].get('diagnostics', '')}`; release `{entry['currentEvidence'].get('release', '')}`",
            f"- Reference anchors: {', '.join(source['name'] for source in entry['sources'])}",
            "",
            "Next work:",
        ])
        for item in entry["items"]:
            lines.append(f"- {item}")
        lines.append("")

    lines.extend(["## Reference-Only Repositories", ""])
    for entry in sorted(references, key=lambda item: str(item["name"]).lower()):
        lines.extend([
            f"### {entry['name']}",
            "",
            f"- Remote: `{entry['remote']}`",
            f"- Dirty files: `{entry['currentEvidence'].get('dirtyCount')}`",
            "",
            "Boundary:",
        ])
        for item in entry["items"]:
            lines.append(f"- {item}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a reference-grounded backlog from the evolution radar.")
    parser.add_argument("--radar", type=Path, default=DEFAULT_RADAR, help="Input grounded radar JSON.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Markdown output path.")
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help="JSON output path.")
    args = parser.parse_args()

    payload = read_json(args.radar)
    backlog = build_backlog(payload)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_markdown(backlog), encoding="utf-8")
    args.json.write_text(json.dumps(backlog, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {args.output} with {len(backlog['entries'])} entries")
    print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
