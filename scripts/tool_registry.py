from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports" / "tool-registry.json"
DEFAULT_MARKDOWN = ROOT / "reports" / "tool-registry.md"


@dataclass(frozen=True)
class ToolEntry:
    name: str
    script: str
    command: str
    output: str
    reference: str
    purpose: str


TOOLS = [
    ToolEntry(
        "Grounded Evolution Radar",
        "scripts/grounded_evolution_radar.py",
        "python scripts/grounded_evolution_radar.py --root <workspace>",
        "reports/grounded-evolution-radar.md",
        "OpenSSF Scorecard",
        "score local repositories from observable health signals",
    ),
    ToolEntry(
        "Evolution Backlog",
        "scripts/evolution_backlog.py",
        "python scripts/evolution_backlog.py",
        "reports/evolution-backlog.md",
        "Backstage Software Templates",
        "turn repository signals into next maintainable work",
    ),
    ToolEntry(
        "Reference Catalog Check",
        "scripts/reference_catalog_check.py",
        "python scripts/reference_catalog_check.py",
        "reports/reference-catalog-check.md",
        "primary source documentation",
        "keep borrowed patterns tied to primary sources and local artifacts",
    ),
    ToolEntry(
        "Release Readiness",
        "scripts/release_readiness_report.py",
        "python scripts/release_readiness_report.py --run-tests",
        "reports/project-forge-release-readiness.md",
        "release-readiness gates",
        "prove that Project Forge reports, tests, and boundaries are ready",
    ),
    ToolEntry(
        "Report Index",
        "scripts/report_index.py",
        "python scripts/report_index.py",
        "reports/INDEX.md",
        "inspectable evidence",
        "make generated reports discoverable from a single index",
    ),
    ToolEntry(
        "APK Release Forge",
        "scripts/apk_release_forge.py",
        "python scripts/apk_release_forge.py <android-project>",
        "reports/apk-release-forge.md",
        "Android app signing",
        "summarize Android release assets and signing evidence",
    ),
    ToolEntry(
        "Dependency Manifest Radar",
        "scripts/dependency_manifest_radar.py",
        "python scripts/dependency_manifest_radar.py <repo>",
        "reports/dependency-radar.md",
        "Renovate",
        "surface dependency manifests before update automation",
    ),
    ToolEntry(
        "Secret Pattern Audit",
        "scripts/secret_pattern_audit.py",
        "python scripts/secret_pattern_audit.py <repo>",
        "reports/secret-audit.md",
        "Gitleaks-style local scan",
        "find obvious secret patterns with redacted reporting",
    ),
]


def build_registry() -> dict[str, object]:
    entries = []
    for tool in TOOLS:
        script_path = ROOT / tool.script
        output_path = ROOT / tool.output
        entries.append({
            **asdict(tool),
            "script_exists": script_path.exists(),
            "output_exists": output_path.exists(),
        })
    failures = [
        entry for entry in entries
        if not entry["script_exists"] or not entry["output_exists"]
    ]
    return {
        "report_type": "tool_registry",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ok": len(failures) == 0,
        "tool_count": len(entries),
        "tools": entries,
        "failures": failures,
    }


def render_markdown(registry: dict[str, object]) -> str:
    lines = [
        "# Tool Registry",
        "",
        f"Generated: {registry['generated_at']}",
        f"Status: `{'OK' if registry['ok'] else 'FAIL'}`",
        f"Tools: `{registry['tool_count']}`",
        "",
        "| Tool | Command | Output | Reference |",
        "|---|---|---|---|",
    ]
    for tool in registry["tools"]:
        lines.append(
            f"| {tool['name']} | `{tool['command']}` | `{tool['output']}` | {tool['reference']} |"
        )
    lines.extend([
        "",
        "## Policy",
        "",
        "- A tool is listed only when its script and primary report output exist.",
        "- Each tool maps to a reference pattern so maintenance work stays grounded.",
        "- Commands use explicit local paths or placeholders instead of hidden automation state.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a registry of Project Forge maintenance tools.")
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    registry = build_registry()
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    args.markdown_out.write_text(render_markdown(registry), encoding="utf-8")
    print(json.dumps({"ok": registry["ok"], "json": str(args.json_out), "markdown": str(args.markdown_out)}, indent=2))
    return 0 if registry["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
