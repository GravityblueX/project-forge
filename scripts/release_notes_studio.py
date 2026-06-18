from __future__ import annotations

import argparse
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "release-notes.md"
CATEGORIES = {
    "feat": "Features",
    "fix": "Fixes",
    "docs": "Documentation",
    "chore": "Maintenance",
    "refactor": "Refactors",
    "test": "Tests",
    "ci": "CI",
    "build": "Build",
    "perf": "Performance",
}


def run_git(args: list[str], repo: Path) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def latest_tag(repo: Path) -> str | None:
    tag = run_git(["describe", "--tags", "--abbrev=0"], repo)
    return tag or None


def commits(repo: Path, since: str | None, limit: int) -> list[str]:
    revision = f"{since}..HEAD" if since else "HEAD"
    output = run_git(["log", revision, f"--max-count={limit}", "--pretty=format:%h%x09%s"], repo)
    return [line for line in output.splitlines() if line.strip()]


def categorize(subject: str) -> str:
    prefix = subject.split(":", 1)[0].split("(", 1)[0].lower()
    return CATEGORIES.get(prefix, "Other")


def render(repo: Path, tag: str | None, lines_in: list[str]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    grouped: dict[str, list[str]] = defaultdict(list)
    for line in lines_in:
        if "\t" in line:
            sha, subject = line.split("\t", 1)
        else:
            sha, subject = "", line
        grouped[categorize(subject)].append(f"- `{sha}` {subject}".strip())

    lines = [
        "# Release Notes Studio",
        "",
        f"Repository: `{repo.name}`",
        f"Last refreshed: {now}",
        f"Range: `{tag + '..HEAD' if tag else 'recent commits'}`",
        "",
        "## Draft Release Notes",
        "",
    ]
    if not lines_in:
        lines.extend(["No commits were found for the selected range.", ""])
    else:
        for category in [*CATEGORIES.values(), "Other"]:
            items = grouped.get(category)
            if not items:
                continue
            lines.extend([f"### {category}", ""])
            lines.extend(items)
            lines.append("")

    lines.extend([
        "## Verification",
        "",
        "- Build command: `<fill in>`",
        "- Test command: `<fill in>`",
        "- Artifact checksums: `<fill in>`",
        "- Smoke test result: `<fill in>`",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate draft release notes from git history.")
    parser.add_argument("path", nargs="?", default=".", help="Git repository path.")
    parser.add_argument("--since", help="Tag or revision to start from. Defaults to latest tag.")
    parser.add_argument("--limit", type=int, default=80, help="Maximum commits to include.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    repo = Path(args.path).resolve()
    tag = args.since or latest_tag(repo)
    lines = commits(repo, tag, args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(repo, tag, lines), encoding="utf-8")
    print(f"wrote {args.output} with {len(lines)} commits")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
