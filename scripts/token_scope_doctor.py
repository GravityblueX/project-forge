from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "token-scope.md"
TOKEN_RE = re.compile(r"(gh[pousr]_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]{8,})")


def run_gh_auth_status() -> tuple[int, str]:
    completed = subprocess.run(
        ["gh", "auth", "status"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout + completed.stderr


def redact(text: str) -> str:
    redacted_lines = []
    for line in TOKEN_RE.sub("<redacted-token>", text).splitlines():
        if line.strip().lower().startswith("- token:"):
            indent = line[: len(line) - len(line.lstrip())]
            redacted_lines.append(f"{indent}- Token: <redacted-token>")
        else:
            redacted_lines.append(line)
    return "\n".join(redacted_lines)


def detect_scopes(text: str) -> set[str]:
    scopes: set[str] = set()
    for line in text.splitlines():
        lowered = line.lower()
        if "token scopes:" not in lowered:
            continue
        _, _, scope_text = line.partition(":")
        for scope in re.split(r"[, ]+", scope_text.replace("'", "").replace('"', "")):
            scope = scope.strip()
            if scope:
                scopes.add(scope)
    return scopes


def render(status_code: int, auth_text: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    redacted = redact(auth_text).strip() or "No gh auth status output."
    scopes = detect_scopes(auth_text)
    has_workflow = "workflow" in scopes
    has_repo = "repo" in scopes or "public_repo" in scopes

    lines = [
        "# Token Scope Doctor",
        "",
        f"Last refreshed: {now}",
        f"`gh auth status` exit code: `{status_code}`",
        "",
        "## Diagnosis",
        "",
    ]
    if status_code != 0:
        lines.append("- GitHub CLI authentication is not healthy. Run `gh auth login` and retry.")
    elif not has_repo:
        lines.append("- Repository access scope was not detected. GitHub API uploads may fail.")
    else:
        lines.append("- Repository access appears available.")

    if has_workflow:
        lines.append("- `workflow` scope appears available, so workflow files can be managed through the API.")
    else:
        lines.append("- `workflow` scope was not detected. Keep workflow templates outside `.github/workflows/` until the token is upgraded.")

    lines.extend([
        "",
        "## Least-Privilege Notes",
        "",
        "- Do not paste token values into reports or chat logs.",
        "- Prefer short-lived or narrowly scoped tokens for automation.",
        "- Add `workflow` only when you explicitly need to create or edit GitHub Actions workflow files.",
        "",
        "## Redacted gh Auth Status",
        "",
        "```text",
        redacted,
        "```",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose GitHub CLI auth scope gaps without printing token values.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    status_code, auth_text = run_gh_auth_status()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(status_code, auth_text), encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
