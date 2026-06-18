from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "repo-health.md"


@dataclass
class CheckResult:
    name: str
    points: int
    max_points: int
    note: str


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
    if not output:
        return None
    return json.loads(output)


def gh_api(path: str, *, timeout: int = 45) -> Any:
    return run_gh(["api", path], timeout=timeout)


def detect_owner(explicit_owner: str | None) -> str:
    if explicit_owner:
        return explicit_owner
    env_owner = os.environ.get("GH_OWNER") or os.environ.get("GITHUB_OWNER")
    if env_owner:
        return env_owner
    user = gh_api("user")
    login = user.get("login")
    if not login:
        raise RuntimeError("Could not detect GitHub owner. Pass --owner OWNER.")
    return str(login)


def list_repos(owner: str, limit: int) -> list[dict[str, Any]]:
    fields = [
        "name",
        "nameWithOwner",
        "url",
        "description",
        "isArchived",
        "isFork",
        "isPrivate",
        "updatedAt",
        "pushedAt",
        "defaultBranchRef",
        "primaryLanguage",
        "licenseInfo",
        "stargazerCount",
        "forkCount",
        "issues",
    ]
    return run_gh([
        "repo",
        "list",
        owner,
        "--limit",
        str(limit),
        "--json",
        ",".join(fields),
    ])


def has_path(owner_repo: str, path: str) -> bool:
    try:
        gh_api(f"repos/{owner_repo}/contents/{path}", timeout=20)
        return True
    except Exception:
        return False


def latest_release(owner_repo: str) -> bool:
    try:
        gh_api(f"repos/{owner_repo}/releases/latest", timeout=20)
        return True
    except Exception:
        return False


def recent_failed_runs(owner_repo: str) -> int:
    try:
        data = gh_api(f"repos/{owner_repo}/actions/runs?status=failure&per_page=5", timeout=25)
    except Exception:
        return 0
    return len(data.get("workflow_runs", []))


def score_repo(repo: dict[str, Any], *, deep: bool) -> tuple[int, list[CheckResult], list[str]]:
    owner_repo = str(repo["nameWithOwner"])
    checks: list[CheckResult] = []
    actions: list[str] = []

    if repo.get("isArchived"):
        checks.append(CheckResult("active", 0, 10, "archived"))
        actions.append("Confirm whether the repository should stay archived.")
    else:
        checks.append(CheckResult("active", 10, 10, "active"))

    if repo.get("description"):
        checks.append(CheckResult("description", 8, 8, "present"))
    else:
        checks.append(CheckResult("description", 0, 8, "missing"))
        actions.append("Add a one-sentence repository description.")

    if repo.get("licenseInfo"):
        checks.append(CheckResult("license", 8, 8, repo["licenseInfo"].get("name", "present")))
    else:
        checks.append(CheckResult("license", 0, 8, "missing"))
        actions.append("Add a LICENSE file if this is meant to be reusable.")

    default_branch = repo.get("defaultBranchRef") or {}
    if default_branch.get("name"):
        checks.append(CheckResult("default branch", 6, 6, default_branch["name"]))
    else:
        checks.append(CheckResult("default branch", 0, 6, "unknown"))

    issue_data = repo.get("issues") or {}
    open_issues = int(issue_data.get("totalCount") or 0)
    if open_issues <= 10:
        checks.append(CheckResult("issue load", 7, 7, f"{open_issues} open"))
    elif open_issues <= 50:
        checks.append(CheckResult("issue load", 4, 7, f"{open_issues} open"))
        actions.append("Triage open issues into now/next/later labels.")
    else:
        checks.append(CheckResult("issue load", 1, 7, f"{open_issues} open"))
        actions.append("Run an issue pruning pass before adding new features.")

    if deep:
        readme = has_path(owner_repo, "README.md") or has_path(owner_repo, "readme.md")
        workflows = has_path(owner_repo, ".github/workflows")
        dependency_files = any(has_path(owner_repo, path) for path in (
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "build.gradle",
            "build.gradle.kts",
            "gradle/libs.versions.toml",
        ))
        release = latest_release(owner_repo)
        failures = recent_failed_runs(owner_repo)

        checks.append(CheckResult("readme", 12 if readme else 0, 12, "present" if readme else "missing"))
        checks.append(CheckResult("ci", 10 if workflows else 0, 10, "workflow directory found" if workflows else "no workflow directory"))
        checks.append(CheckResult("dependencies", 7 if dependency_files else 2, 7, "manifest found" if dependency_files else "no common manifest"))
        checks.append(CheckResult("release", 7 if release else 0, 7, "latest release exists" if release else "no release"))
        checks.append(CheckResult("recent failures", max(0, 8 - failures * 2), 8, f"{failures} recent failures"))

        if not readme:
            actions.append("Write a README with install, run, and project status sections.")
        if not workflows:
            actions.append("Add a minimal CI workflow for lint/build/test.")
        if not release:
            actions.append("Create a first tagged release once the current build is reproducible.")
        if failures:
            actions.append("Inspect recent failed workflow runs.")

    total = sum(check.points for check in checks)
    maximum = sum(check.max_points for check in checks)
    score = round(total / max(maximum, 1) * 100)
    return score, checks, actions


def render(owner: str, rows: list[tuple[dict[str, Any], int, list[CheckResult], list[str]]], *, deep: bool) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Repo Health Radar",
        "",
        f"Owner: `{owner}`",
        f"Last refreshed: {now}",
        f"Mode: {'deep GitHub API checks' if deep else 'fast repo metadata checks'}",
        "",
        "| Rank | Repository | Score | Status | Top Action |",
        "|---:|---|---:|---|---|",
    ]
    for index, (repo, score, checks, actions) in enumerate(rows, 1):
        owner_repo = repo["nameWithOwner"]
        status = "archived" if repo.get("isArchived") else "active"
        top_action = actions[0] if actions else "Keep current maintenance rhythm."
        lines.append(f"| {index} | [{owner_repo}]({repo['url']}) | {score} | {status} | {top_action} |")

    lines.extend(["", "## Details", ""])
    for repo, score, checks, actions in rows:
        lines.extend([
            f"### {repo['nameWithOwner']}",
            "",
            f"- Score: `{score}`",
            f"- Description: {repo.get('description') or 'missing'}",
            f"- Updated: `{repo.get('updatedAt') or 'unknown'}`",
            f"- Pushed: `{repo.get('pushedAt') or 'unknown'}`",
            f"- Open issues: `{(repo.get('issues') or {}).get('totalCount') or 0}`",
            "",
            "| Check | Points | Note |",
            "|---|---:|---|",
        ])
        for check in checks:
            lines.append(f"| {check.name} | {check.points}/{check.max_points} | {check.note} |")
        lines.extend(["", "Recommended next actions:"])
        for action in actions[:5] or ["No urgent action." ]:
            lines.append(f"- {action}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a GitHub repository health report.")
    parser.add_argument("--owner", help="GitHub user or organization. Defaults to GH_OWNER/GITHUB_OWNER/current auth user.")
    parser.add_argument("--limit", type=int, default=50, help="Maximum repositories to scan.")
    parser.add_argument("--deep", action="store_true", help="Run extra API checks for README, CI, releases, and failures.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    owner = detect_owner(args.owner)
    repos = list_repos(owner, args.limit)
    rows = []
    for repo in repos:
        score, checks, actions = score_repo(repo, deep=args.deep)
        rows.append((repo, score, checks, actions))
    rows.sort(key=lambda item: (item[1], item[0]["nameWithOwner"]), reverse=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(owner, rows, deep=args.deep), encoding="utf-8")
    print(f"wrote {args.output} with {len(rows)} repositories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
