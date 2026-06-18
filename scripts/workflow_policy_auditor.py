from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "workflow-audit.md"
WORKFLOW_EXTENSIONS = {".yml", ".yaml"}
ACTION_RE = re.compile(r"uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([^\s#]+)")
MUTABLE_REFS = {"main", "master", "HEAD", "latest", "dev", "develop"}


@dataclass
class Finding:
    severity: str
    file: str
    line: int
    rule: str
    detail: str
    fix: str


def relative(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base)).replace("\\", "/")
    except ValueError:
        return path.name


def workflow_files(base: Path) -> list[Path]:
    roots = [base / ".github" / "workflows", base / "automation" / "github-actions"]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        files.extend(path for path in sorted(root.rglob("*")) if path.suffix in WORKFLOW_EXTENSIONS)
    return files


def has_top_level_permissions(lines: list[str]) -> bool:
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("permissions:"):
            return True
    return False


def audit_file(path: Path, base: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    rel = relative(path, base)
    findings: list[Finding] = []

    if not has_top_level_permissions(lines):
        findings.append(Finding(
            severity="high",
            file=rel,
            line=1,
            rule="missing-top-level-permissions",
            detail="Workflow does not declare top-level GITHUB_TOKEN permissions.",
            fix="Add the narrowest required `permissions:` block at workflow or job level.",
        ))

    for index, line in enumerate(lines, 1):
        stripped = line.strip()
        lowered = stripped.lower()
        match = ACTION_RE.search(stripped)
        if match:
            action, ref = match.groups()
            normalized_ref = ref.strip("\"'")
            if normalized_ref in MUTABLE_REFS:
                findings.append(Finding(
                    severity="high",
                    file=rel,
                    line=index,
                    rule="mutable-action-ref",
                    detail=f"`{action}` uses moving ref `{normalized_ref}`.",
                    fix="Pin to a release tag or audited commit SHA.",
                ))
            elif re.fullmatch(r"v\d+", normalized_ref):
                findings.append(Finding(
                    severity="medium",
                    file=rel,
                    line=index,
                    rule="broad-major-action-ref",
                    detail=f"`{action}` uses broad major tag `{normalized_ref}`.",
                    fix="Consider pinning to a full version tag or SHA for sensitive workflows.",
                ))

        if "pull_request_target" in lowered:
            findings.append(Finding(
                severity="high",
                file=rel,
                line=index,
                rule="pull-request-target",
                detail="`pull_request_target` runs with elevated repository context.",
                fix="Use `pull_request` unless elevated permissions are explicitly required.",
            ))

        if "contents: write" in lowered or "packages: write" in lowered or "actions: write" in lowered:
            findings.append(Finding(
                severity="medium",
                file=rel,
                line=index,
                rule="write-permission",
                detail=f"Workflow grants `{stripped}`.",
                fix="Keep write permissions only on release or automation jobs that need them.",
            ))

        if "schedule:" in lowered:
            findings.append(Finding(
                severity="low",
                file=rel,
                line=index,
                rule="scheduled-workflow",
                detail="Scheduled workflow should be checked for rate, permissions, and idempotence.",
                fix="Keep schedule frequency modest and make generated commits deterministic.",
            ))

    return findings


def render(base: Path, files: list[Path], findings: list[Finding]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    severity_order = {"high": 0, "medium": 1, "low": 2}
    findings = sorted(findings, key=lambda item: (severity_order[item.severity], item.file, item.line))
    lines = [
        "# Workflow Policy Audit",
        "",
        f"Scan root: `{base.name}`",
        f"Last refreshed: {now}",
        f"Workflow files scanned: `{len(files)}`",
        f"Findings: `{len(findings)}`",
        "",
    ]
    if not files:
        lines.extend(["No workflow files were found.", ""])
        return "\n".join(lines)
    if not findings:
        lines.extend(["No workflow policy findings were detected.", ""])
        return "\n".join(lines)

    lines.extend(["| Severity | File | Line | Rule | Fix |", "|---|---|---:|---|---|"])
    for finding in findings:
        lines.append(
            f"| {finding.severity} | `{finding.file}` | {finding.line} | {finding.rule} | {finding.fix} |"
        )

    lines.extend(["", "## Details", ""])
    for finding in findings:
        lines.extend([
            f"### {finding.severity.upper()} - {finding.rule}",
            "",
            f"- File: `{finding.file}`",
            f"- Line: `{finding.line}`",
            f"- Detail: {finding.detail}",
            f"- Suggested fix: {finding.fix}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit GitHub Actions workflow policy risks.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to scan.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    base = Path(args.path).resolve()
    files = workflow_files(base)
    findings: list[Finding] = []
    for path in files:
        findings.extend(audit_file(path, base))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(base, files, findings), encoding="utf-8")
    print(f"wrote {args.output} with {len(findings)} findings across {len(files)} workflows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
