from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "branch-protection.md"


def run_gh(args: list[str], *, timeout: int = 45) -> Any:
    completed = subprocess.run(
        ["gh", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
        env={**os.environ, "NO_COLOR": "1"},
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    output = completed.stdout.strip()
    return json.loads(output) if output else None


def gh_api(path: str, *, timeout: int = 45) -> Any:
    return run_gh(["api", path], timeout=timeout)


def detect_owner(explicit: str | None) -> str:
    if explicit:
        return explicit
    env_owner = os.environ.get("GH_OWNER") or os.environ.get("GITHUB_OWNER")
    if env_owner:
        return env_owner
    return str(gh_api("user")["login"])


def list_repos(owner: str, limit: int) -> list[dict[str, Any]]:
    return run_gh([
        "repo",
        "list",
        owner,
        "--limit",
        str(limit),
        "--json",
        "nameWithOwner,url,isArchived,defaultBranchRef,isPrivate",
    ])


def protection_state(owner_repo: str, branch: str) -> tuple[str, str]:
    try:
        data = gh_api(f"repos/{owner_repo}/branches/{branch}/protection", timeout=25)
    except Exception as exc:
        text = str(exc).lower()
        if "404" in text or "not found" in text:
            return "unprotected", "No branch protection endpoint data."
        return "unknown", str(exc).splitlines()[0][:120]
    checks = data.get("required_status_checks") if isinstance(data, dict) else None
    reviews = data.get("required_pull_request_reviews") if isinstance(data, dict) else None
    details = []
    if checks:
        details.append("required status checks")
    if reviews:
        details.append("required PR reviews")
    return "protected", ", ".join(details) or "protection enabled"


def render(owner: str, rows: list[dict[str, str]]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    unprotected = sum(1 for row in rows if row["state"] == "unprotected")
    lines = [
        "# Branch Protection Radar",
        "",
        f"Owner: `{owner}`",
        f"Last refreshed: {now}",
        f"Repositories scanned: `{len(rows)}`",
        f"Unprotected default branches: `{unprotected}`",
        "",
        "| Repository | Branch | State | Notes |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| [{row['repo']}]({row['url']}) | `{row['branch']}` | {row['state']} | {row['notes']} |")
    lines.extend([
        "",
        "## Suggested Policy",
        "",
        "- Protect active repositories that publish releases or receive outside contributions.",
        "- Require at least build/test status checks before merge on important repos.",
        "- Keep archived repositories unchanged unless they are restored.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check default branch protection across GitHub repositories.")
    parser.add_argument("--owner", help="GitHub user or organization.")
    parser.add_argument("--limit", type=int, default=50, help="Maximum repositories to scan.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    owner = detect_owner(args.owner)
    repos = [repo for repo in list_repos(owner, args.limit) if not repo.get("isArchived")]
    rows: list[dict[str, str]] = []
    for repo in repos:
        branch_data = repo.get("defaultBranchRef") or {}
        branch = branch_data.get("name") or "main"
        state, notes = protection_state(repo["nameWithOwner"], branch)
        rows.append({
            "repo": repo["nameWithOwner"],
            "url": repo["url"],
            "branch": branch,
            "state": state,
            "notes": notes,
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(owner, rows), encoding="utf-8")
    print(f"wrote {args.output} with {len(rows)} repositories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
