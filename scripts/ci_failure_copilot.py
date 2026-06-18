from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "ci-failures.md"


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


def run_gh_text(args: list[str], *, timeout: int = 60) -> str:
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
        return completed.stderr.strip() or completed.stdout.strip()
    return completed.stdout


def gh_api(path: str, *, timeout: int = 45) -> Any:
    return run_gh(["api", path], timeout=timeout)


def detect_owner(owner: str | None) -> str:
    if owner:
        return owner
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
        "name,nameWithOwner,url,isArchived,isFork,pushedAt",
    ])


def failed_runs(owner_repo: str, per_repo: int) -> list[dict[str, Any]]:
    try:
        data = gh_api(f"repos/{owner_repo}/actions/runs?status=failure&per_page={per_repo}", timeout=30)
    except Exception:
        return []
    return data.get("workflow_runs", [])


def failed_jobs(owner_repo: str, run_id: int) -> list[dict[str, Any]]:
    try:
        data = gh_api(f"repos/{owner_repo}/actions/runs/{run_id}/jobs?per_page=20", timeout=30)
    except Exception:
        return []
    return [job for job in data.get("jobs", []) if job.get("conclusion") == "failure"]


def classify(text: str) -> str:
    lowered = text.lower()
    if "prettier: not found" in lowered or "eslint: not found" in lowered:
        return "Missing formatter or linter dependency"
    if any(token in lowered for token in ("npm", "pnpm", "yarn", "package-lock", "node_modules")):
        return "JavaScript dependency or package script failure"
    if any(token in lowered for token in ("gradle", "android", "apk", "kotlin")):
        return "Android or Gradle build failure"
    if any(token in lowered for token in ("pytest", "python", "pip", "traceback")):
        return "Python test or dependency failure"
    if any(token in lowered for token in ("permission", "403", "resource not accessible", "token")):
        return "GitHub permission or token failure"
    if any(token in lowered for token in ("prettier", "eslint", "ruff", "lint")):
        return "Formatter or linter failure"
    return "Unclassified CI failure"


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\s*")


def clean_log_line(line: str) -> str:
    line = ANSI_RE.sub("", line).replace("\ufeff", "")
    parts = line.split("\t")
    if len(parts) >= 3:
        line = parts[-1]
    return TIMESTAMP_RE.sub("", line).strip()


def extract_snippets(log_text: str, *, limit: int = 6) -> list[str]:
    needles = ("##[error]", "error", "failed", "not found", "exit code", "traceback", "exception")
    snippets: list[str] = []
    for raw_line in log_text.splitlines():
        line = clean_log_line(raw_line)
        lowered = line.lower()
        if not line or line.startswith("Run ") or line.startswith("with:"):
            continue
        if any(needle in lowered for needle in needles):
            snippets.append(line)

    deduped: list[str] = []
    for line in snippets:
        if line not in deduped:
            deduped.append(line)
    return deduped[-limit:]


def summarize_run(owner_repo: str, run: dict[str, Any]) -> dict[str, Any]:
    jobs = failed_jobs(owner_repo, int(run["id"]))
    job_names = ", ".join(job.get("name", "unknown") for job in jobs) or "failed job unavailable"
    log_text = run_gh_text(["run", "view", str(run["id"]), "--repo", owner_repo, "--log-failed"], timeout=90)
    snippets = extract_snippets(log_text)
    reason = classify(f"{run.get('name', '')} {run.get('display_title', '')} {job_names} {' '.join(snippets)}")
    return {
        "repo": owner_repo,
        "repo_url": f"https://github.com/{owner_repo}",
        "run_name": run.get("name") or "workflow",
        "title": run.get("display_title") or run.get("head_commit", {}).get("message", ""),
        "url": run.get("html_url"),
        "created_at": run.get("created_at"),
        "branch": run.get("head_branch"),
        "jobs": job_names,
        "reason": reason,
        "snippets": snippets,
    }


def render(owner: str, failures: list[dict[str, Any]]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# CI Failure Copilot",
        "",
        f"Owner: `{owner}`",
        f"Last refreshed: {now}",
        "",
    ]
    if not failures:
        lines.extend([
            "No recent failed workflow runs were found in the scanned repositories.",
            "",
            "Next action: keep the scan scheduled and focus on repository health tasks.",
        ])
        return "\n".join(lines).rstrip() + "\n"

    lines.extend([
        "| Repository | Workflow | Likely Area | Failed Job | Run |",
        "|---|---|---|---|---|",
    ])
    for item in failures:
        lines.append(
            f"| [{item['repo']}]({item['repo_url']}) | {item['run_name']} | {item['reason']} | {item['jobs']} | [open]({item['url']}) |"
        )

    lines.extend(["", "## Fix Queue", ""])
    for index, item in enumerate(failures, 1):
        lines.extend([
            f"### {index}. {item['repo']} - {item['run_name']}",
            "",
            f"- Branch: `{item.get('branch') or 'unknown'}`",
            f"- Created: `{item.get('created_at') or 'unknown'}`",
            f"- Failed jobs: {item['jobs']}",
            f"- Likely area: {item['reason']}",
            f"- Run: {item['url']}",
            "- Key log lines:",
        ])
        for snippet in item.get("snippets") or ["No concise error snippet extracted."]:
            lines.append(f"  - `{snippet}`")
        lines.extend([
            "- Suggested next step: patch the first missing dependency or failing command shown above, then rerun the workflow.",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize recent GitHub Actions failures.")
    parser.add_argument("--owner", help="GitHub user or organization.")
    parser.add_argument("--limit", type=int, default=30, help="Maximum repositories to scan.")
    parser.add_argument("--per-repo", type=int, default=3, help="Failed runs to inspect per repository.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    owner = detect_owner(args.owner)
    repos = [repo for repo in list_repos(owner, args.limit) if not repo.get("isArchived")]
    failures: list[dict[str, Any]] = []
    for repo in repos:
        owner_repo = repo["nameWithOwner"]
        for run in failed_runs(owner_repo, args.per_repo):
            failures.append(summarize_run(owner_repo, run))
    failures.sort(key=lambda item: item.get("created_at") or "", reverse=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(owner, failures), encoding="utf-8")
    print(f"wrote {args.output} with {len(failures)} failed runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
