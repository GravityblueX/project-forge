from __future__ import annotations

import argparse
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "apk-release-forge.md"
SKIP_DIRS = {".git", ".gradle", "build", "node_modules", ".idea", ".vscode"}


def find_gradle_roots(base: Path) -> list[Path]:
    markers = ("settings.gradle", "settings.gradle.kts", "build.gradle", "build.gradle.kts")
    roots: set[Path] = set()
    for current, dirs, files in os.walk(base, topdown=True, onerror=lambda error: None):
        dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
        if any(marker in files for marker in markers):
            roots.add(Path(current))
    return sorted(roots)


def find_apks(base: Path) -> list[Path]:
    apks: list[Path] = []
    for current, dirs, files in os.walk(base, topdown=True, onerror=lambda error: None):
        dirs[:] = [directory for directory in dirs if directory not in {".git", ".gradle", "node_modules"}]
        for file_name in files:
            if file_name.endswith(".apk"):
                apks.append(Path(current) / file_name)
    return sorted(apks)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def display_path(path: Path, base: Path) -> str:
    try:
        relative = path.relative_to(base)
    except ValueError:
        return path.name
    return "." if str(relative) == "." else str(relative)


def render(base: Path, gradle_roots: list[Path], apks: list[Path]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# APK Release Forge",
        "",
        f"Scan root: `{base.name}`",
        f"Last refreshed: {now}",
        "",
        "## Gradle Projects",
        "",
    ]
    if not gradle_roots:
        lines.append("No Gradle projects were found under the scan root.")
    for root in gradle_roots:
        wrapper = root / "gradlew"
        wrapper_bat = root / "gradlew.bat"
        command = ".\\gradlew.bat assembleRelease" if wrapper_bat.exists() else "./gradlew assembleRelease"
        lines.extend([
            f"### {root.name}",
            "",
            f"- Path: `{display_path(root, base)}`",
            f"- Wrapper: `{'yes' if wrapper.exists() or wrapper_bat.exists() else 'no'}`",
            f"- Suggested build command: `{command}`",
            "- Release checklist:",
            "  - Ensure versionCode/versionName are bumped.",
            "  - Run unit tests before release assembly.",
            "  - Build release APK/AAB from a clean tree.",
            "  - Generate SHA-256 checksums for published artifacts.",
            "  - Attach release notes and checksums to the GitHub release.",
            "",
        ])

    lines.extend(["## APK Artifacts", ""])
    if not apks:
        lines.append("No built APK artifacts were found yet.")
    else:
        lines.extend(["| APK | Size | SHA-256 |", "|---|---:|---|"])
        for apk in apks:
            size_mb = apk.stat().st_size / 1024 / 1024
            lines.append(f"| `{display_path(apk, base)}` | {size_mb:.2f} MB | `{sha256(apk)}` |")

    lines.extend([
        "",
        "## Reusable Release Notes Template",
        "",
        "```markdown",
        "## Changes",
        "",
        "- ",
        "",
        "## Verification",
        "",
        "- Build command: `./gradlew assembleRelease` or `.\\gradlew.bat assembleRelease`",
        "- SHA-256: `<paste checksum>`",
        "- Smoke test: `<device/emulator + result>`",
        "```",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect Android projects and APK release artifacts.")
    parser.add_argument("path", nargs="?", default=".", help="Repository or workspace path to scan.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    base = Path(args.path).resolve()
    gradle_roots = find_gradle_roots(base)
    apks = find_apks(base)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(base, gradle_roots, apks), encoding="utf-8")
    print(f"wrote {args.output} with {len(gradle_roots)} gradle projects and {len(apks)} APKs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
