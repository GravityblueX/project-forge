from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUTPUT = REPORTS / "weekly-briefing.md"
SCORE_RE = re.compile(r"\|\s*\d+\s*\|\s*\[?([^|\]]+)")
FINDING_RE = re.compile(r"Findings:\s*`?(\d+)`?")


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def first_table_rows(text: str, limit: int = 5) -> list[str]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        if line.lower().startswith("| rank") or line.lower().startswith("| repository") or line.lower().startswith("| severity"):
            continue
        rows.append(line)
        if len(rows) >= limit:
            break
    return rows


def count_findings(text: str) -> int | None:
    match = FINDING_RE.search(text)
    return int(match.group(1)) if match else None


def render(reports_dir: Path) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    repo_health = read(reports_dir / "repo-health.md")
    ci_failures = read(reports_dir / "ci-failures.md")
    workflow_audit = read(reports_dir / "workflow-audit.md")
    secret_audit = read(reports_dir / "secret-audit.md")
    dependency_radar = read(reports_dir / "dependency-radar.md")
    release_notes = read(reports_dir / "release-notes.md")

    lines = [
        "# Weekly Maintenance Briefing",
        "",
        f"Last refreshed: {now}",
        "",
        "## Priority Queue",
        "",
    ]

    priorities: list[str] = []
    if "prettier: not found" in ci_failures:
        priorities.append("Fix `ashveil-console` CI by ensuring Prettier is installed in the workflow environment.")
    workflow_findings = count_findings(workflow_audit)
    if workflow_findings:
        priorities.append(f"Review `{workflow_findings}` workflow policy findings before enabling more automation.")
    secret_findings = count_findings(secret_audit)
    if secret_findings:
        priorities.append(f"Review `{secret_findings}` redacted secret-pattern findings and rotate anything real.")
    if "no test script" in dependency_radar:
        priorities.append("Add missing test scripts to Node projects before relying on automated dependency PRs.")
    if not priorities:
        priorities.append("No urgent maintenance blocker found in the generated reports.")

    for index, priority in enumerate(priorities, 1):
        lines.append(f"{index}. {priority}")

    lines.extend(["", "## Snapshot", ""])
    sections = [
        ("Repo Health", repo_health),
        ("CI Failures", ci_failures),
        ("Workflow Audit", workflow_audit),
        ("Secret Audit", secret_audit),
        ("Dependency Radar", dependency_radar),
    ]
    for title, text in sections:
        lines.extend([f"### {title}", ""])
        rows = first_table_rows(text)
        if rows:
            lines.extend(["| Item | Data |", "|---|---|"])
            for row in rows[:5]:
                cells = [cell.strip() for cell in row.strip("|").split("|")]
                item = cells[0] if cells else title
                data = " / ".join(cells[1:]) if len(cells) > 1 else "see report"
                lines.append(f"| {item} | {data} |")
        else:
            finding_count = count_findings(text)
            lines.append(f"- Findings: `{finding_count}`" if finding_count is not None else "- See report for details.")
        lines.append("")

    lines.extend([
        "## Report Files",
        "",
        "- `reports/repo-health.md`",
        "- `reports/ci-failures.md`",
        "- `reports/workflow-audit.md`",
        "- `reports/secret-audit.md`",
        "- `reports/dependency-radar.md`",
        "- `reports/release-notes.md`",
        "",
        "## Draft Release Context",
        "",
    ])
    release_rows = first_table_rows(release_notes, limit=3)
    if release_rows:
        lines.extend(release_rows)
    else:
        lines.append("See `reports/release-notes.md` for the current release draft.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge generated reports into one weekly maintenance briefing.")
    parser.add_argument("--reports", type=Path, default=REPORTS, help="Reports directory.")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="Briefing output path.")
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(args.reports), encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
