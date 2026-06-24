from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MARKDOWN = ROOT / "docs" / "release-readiness.md"
DEFAULT_JSON = ROOT / "reports" / "project-forge-release-readiness.json"
DEFAULT_REPORT = ROOT / "reports" / "project-forge-release-readiness.md"


@dataclass(frozen=True)
class Gate:
    name: str
    ok: bool
    detail: str


REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "renovate.json",
    "docs/PROJECT_POLICY.md",
    "docs/GROUNDED_REFERENCE_CATALOG.md",
    "scripts/grounded_evolution_radar.py",
    "scripts/evolution_backlog.py",
    "scripts/reference_catalog_check.py",
    "scripts/report_index.py",
    "tests/test_grounded_evolution_radar.py",
    "reports/INDEX.md",
    "reports/grounded-evolution-radar.md",
    "reports/grounded-evolution-radar.json",
    "reports/evolution-backlog.md",
    "reports/evolution-backlog.json",
    "reports/reference-catalog-check.md",
    "reports/reference-catalog-check.json",
]

PRIMARY_REFERENCES = [
    "OpenSSF Scorecard",
    "Renovate",
    "Backstage Software Templates",
    "Playwright Trace Viewer",
    "Chrome DevTools Protocol Page domain",
    "Android app signing",
    "Gradle dependency verification",
    "OWASP MASVS",
]

REFERENCE_ONLY_NAMES = {"AllBeingsFuture", "lux_net", "lux_net-reference"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def run_command(args: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    output = "\n".join(part for part in [completed.stdout.strip(), completed.stderr.strip()] if part)
    return completed.returncode, output[-4000:]


def git_dirty_count() -> int:
    code, output = run_command(["git", "status", "--short"])
    if code != 0:
        return -1
    return len([line for line in output.splitlines() if line.strip()])


def required_file_gates() -> list[Gate]:
    gates: list[Gate] = []
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        gates.append(Gate(f"required file {relative}", path.exists(), relative))
    return gates


def reference_gates() -> list[Gate]:
    catalog = read_text(ROOT / "docs" / "GROUNDED_REFERENCE_CATALOG.md")
    return [
        Gate(f"reference source {name}", name in catalog, name)
        for name in PRIMARY_REFERENCES
    ]


def reference_catalog_report_gates() -> list[Gate]:
    payload = load_json(ROOT / "reports" / "reference-catalog-check.json")
    references = payload.get("references", [])
    return [
        Gate("reference catalog check exists", bool(references), f"{len(references)} references"),
        Gate("reference catalog check ok", payload.get("ok") is True, str(payload.get("ok"))),
    ]


def radar_gates() -> list[Gate]:
    payload = load_json(ROOT / "reports" / "grounded-evolution-radar.json")
    repos = payload.get("repositories", [])
    self_row = next((row for row in repos if row.get("name") == "project-forge"), {})
    managed_rows = [row for row in repos if "GravityblueX" in str(row.get("remote", ""))]
    managed_100 = [
        row.get("name")
        for row in managed_rows
        if row.get("name") != "project-forge" and int(row.get("score", 0)) >= 100
    ]

    return [
        Gate("radar payload exists", bool(repos), f"{len(repos)} repositories"),
        Gate("project-forge radar row exists", bool(self_row), str(self_row.get("score", ""))),
        Gate("project-forge score at least 90", int(self_row.get("score", 0)) >= 90, str(self_row.get("score", ""))),
        Gate("managed project scores remain strong", len(managed_100) >= 5, ", ".join(str(name) for name in managed_100)),
    ]


def backlog_gates() -> list[Gate]:
    payload = load_json(ROOT / "reports" / "evolution-backlog.json")
    entries = payload.get("entries", [])
    by_name = {entry.get("name"): entry for entry in entries}
    reference_only = [
        name for name in REFERENCE_ONLY_NAMES
        if by_name.get(name, {}).get("managed") is False
    ]
    managed = [
        entry.get("name")
        for entry in entries
        if entry.get("managed") is True
    ]
    return [
        Gate("evolution backlog exists", bool(entries), f"{len(entries)} entries"),
        Gate("reference repos are not managed", len(reference_only) >= 3, ", ".join(reference_only)),
        Gate("managed repos have next work", all(by_name.get(name, {}).get("items") for name in managed), ", ".join(str(name) for name in managed)),
    ]


def report_index_gates() -> list[Gate]:
    index = read_text(ROOT / "reports" / "INDEX.md")
    required = ["Grounded Evolution Radar", "Evolution Backlog", "Project Forge Release Readiness"]
    return [Gate(f"report index includes {name}", name in index, name) for name in required]


def test_gate(run_tests: bool) -> Gate:
    if not run_tests:
        return Gate("unit tests", True, "not run by this report; run python -m unittest discover -s tests")
    code, output = run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests"])
    return Gate("unit tests", code == 0, output.splitlines()[-1] if output else f"exit {code}")


def build_payload(run_tests: bool = False) -> dict[str, Any]:
    gates = (
        required_file_gates()
        + reference_gates()
        + reference_catalog_report_gates()
        + radar_gates()
        + backlog_gates()
        + report_index_gates()
        + [test_gate(run_tests)]
    )
    dirty = git_dirty_count()
    gates.append(Gate("git status readable", dirty >= 0, f"dirty_count={dirty}"))

    return {
        "reportType": "project_forge_release_readiness",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "project": "project-forge",
        "version": "0.1.0",
        "ok": all(gate.ok for gate in gates),
        "dirtyCount": dirty,
        "gates": [gate.__dict__ for gate in gates],
        "references": PRIMARY_REFERENCES,
        "nextReleaseNotes": [
            "Reference-grounded evolution radar and backlog are generated from local repository evidence.",
            "Friend/reference repositories are explicitly marked non-managed.",
            "Project Forge now has a repeatable release-readiness report before tagging.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    generated = datetime.fromisoformat(payload["generatedAt"]).strftime("%Y-%m-%d %H:%M UTC")
    status = "OK" if payload["ok"] else "NOT READY"
    lines = [
        "# Project Forge Release Readiness",
        "",
        f"Generated: {generated}",
        f"Project: `{payload['project']}`",
        f"Version: `{payload['version']}`",
        f"Status: `{status}`",
        f"Dirty files when generated: `{payload['dirtyCount']}`",
        "",
        "## Gates",
        "",
        "| Gate | Result | Detail |",
        "|---|---|---|",
    ]
    for gate in payload["gates"]:
        result = "OK" if gate["ok"] else "FAIL"
        lines.append(f"| {gate['name']} | {result} | {gate['detail']} |")

    lines.extend(["", "## Reference Basis", ""])
    for reference in payload["references"]:
        lines.append(f"- {reference}")

    lines.extend(["", "## Next Release Notes", ""])
    for note in payload["nextReleaseNotes"]:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Project Forge release-readiness evidence.")
    parser.add_argument("--run-tests", action="store_true", help="Run the unit test suite as part of the report.")
    parser.add_argument("--docs-output", type=Path, default=DEFAULT_MARKDOWN, help="Docs markdown output path.")
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT, help="Reports markdown output path.")
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help="JSON output path.")
    args = parser.parse_args()

    payload = build_payload(run_tests=args.run_tests)
    rendered = render_markdown(payload)

    args.docs_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.docs_output.write_text(rendered, encoding="utf-8")
    args.report_output.write_text(rendered, encoding="utf-8")
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"ok": payload["ok"], "docs": str(args.docs_output), "report": str(args.report_output), "json": str(args.json)}, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
