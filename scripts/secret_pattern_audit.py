from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "secret-audit.md"
SKIP_DIRS = {".git", ".gradle", ".venv", "build", "dist", "node_modules", "__pycache__"}
TEXT_EXTENSIONS = {
    ".env",
    ".json",
    ".js",
    ".kt",
    ".kts",
    ".md",
    ".ps1",
    ".py",
    ".toml",
    ".ts",
    ".txt",
    ".yaml",
    ".yml",
}
PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("generic-secret-assignment", re.compile(r"(?i)\b(secret|token|api[_-]?key|password)\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+=-]{16,})")),
]


@dataclass
class Finding:
    file: str
    line: int
    kind: str
    preview: str


def relative(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base)).replace("\\", "/")
    except ValueError:
        return path.name


def should_scan(path: Path) -> bool:
    if path.name.lower() in {".env", ".npmrc", ".pypirc"}:
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def mask(line: str) -> str:
    compact = line.strip()
    if len(compact) <= 12:
        return "<redacted>"
    return f"{compact[:8]}...{compact[-4:]}"


def scan_file(path: Path, base: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings
    for index, line in enumerate(text.splitlines(), 1):
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(Finding(
                    file=relative(path, base),
                    line=index,
                    kind=kind,
                    preview=mask(line),
                ))
    return findings


def scan(base: Path) -> tuple[int, list[Finding]]:
    scanned = 0
    findings: list[Finding] = []
    for current, dirs, files in os.walk(base, topdown=True, onerror=lambda error: None):
        dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
        for file_name in files:
            path = Path(current) / file_name
            if not should_scan(path):
                continue
            scanned += 1
            findings.extend(scan_file(path, base))
    return scanned, findings


def render(base: Path, scanned: int, findings: list[Finding]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Secret Pattern Audit",
        "",
        f"Scan root: `{base.name}`",
        f"Last refreshed: {now}",
        f"Text files scanned: `{scanned}`",
        f"Findings: `{len(findings)}`",
        "",
        "This report redacts matched lines. Treat findings as review prompts, not confirmed leaks.",
        "",
    ]
    if not findings:
        lines.extend(["No secret-like patterns were detected.", ""])
        return "\n".join(lines)

    lines.extend(["| Kind | File | Line | Redacted Preview |", "|---|---|---:|---|"])
    for finding in findings:
        lines.append(f"| {finding.kind} | `{finding.file}` | {finding.line} | `{finding.preview}` |")
    lines.extend([
        "",
        "## Recommended Response",
        "",
        "- If a finding is a real credential, revoke and rotate it before editing history.",
        "- If it is a false positive, add a narrow allowlist rule in a future scanner revision.",
        "- Do not paste raw secrets into issues, reports, or chat logs.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan text files for redacted secret-like patterns.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to scan.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    base = Path(args.path).resolve()
    scanned, findings = scan(base)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(base, scanned, findings), encoding="utf-8")
    print(f"wrote {args.output} with {len(findings)} findings across {scanned} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
