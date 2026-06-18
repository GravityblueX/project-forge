from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
OUTPUT = REPORTS / "INDEX.md"


def title_for(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return path.stem.replace("-", " ").title()


def first_metric(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if path.name == "weekly-briefing.md":
            priority_count = sum(1 for line in lines if re.match(r"^\d+\. ", line))
            return f"Priority items: `{priority_count}`"
        for line in lines:
            if any(label in line for label in (
                "Findings:",
                "Manifests found:",
                "Workflow files scanned:",
                "Text files scanned:",
                "Unprotected default branches:",
                "Repositories scanned:",
                "`gh auth status` exit code:",
                "Reports indexed:",
            )):
                return line.strip()
    except Exception:
        pass
    return "See report"


def render(reports: list[Path]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Report Index",
        "",
        f"Last refreshed: {now}",
        f"Reports indexed: `{len(reports)}`",
        "",
        "| Report | File | Signal |",
        "|---|---|---|",
    ]
    for path in reports:
        lines.append(f"| {title_for(path)} | [`{path.name}`]({path.name}) | {first_metric(path)} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an index for all markdown reports.")
    parser.add_argument("--reports", type=Path, default=REPORTS, help="Reports directory.")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="Index output path.")
    args = parser.parse_args()

    reports = sorted(path for path in args.reports.glob("*.md") if path.name != args.output.name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(reports), encoding="utf-8")
    print(f"wrote {args.output} with {len(reports)} reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
