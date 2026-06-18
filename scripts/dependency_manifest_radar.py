from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "dependency-radar.md"
SKIP_DIRS = {".git", ".gradle", ".venv", "build", "dist", "node_modules", "__pycache__"}
MANIFESTS = {
    "package.json": "node",
    "pnpm-lock.yaml": "node-lock",
    "package-lock.json": "node-lock",
    "yarn.lock": "node-lock",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "poetry.lock": "python-lock",
    "build.gradle": "gradle",
    "build.gradle.kts": "gradle",
    "settings.gradle": "gradle",
    "settings.gradle.kts": "gradle",
    "gradle/libs.versions.toml": "gradle-catalog",
}


@dataclass
class Manifest:
    path: str
    ecosystem: str
    notes: list[str]


def relative(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base)).replace("\\", "/")
    except ValueError:
        return path.name


def package_json_notes(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ["package.json could not be parsed"]
    dependencies = len(data.get("dependencies") or {})
    dev_dependencies = len(data.get("devDependencies") or {})
    scripts = data.get("scripts") or {}
    notes = [f"{dependencies} runtime deps", f"{dev_dependencies} dev deps"]
    if "test" not in scripts:
        notes.append("no test script")
    if "lint" not in scripts:
        notes.append("no lint script")
    return notes


def notes_for(path: Path) -> list[str]:
    if path.name == "package.json":
        return package_json_notes(path)
    if path.name.endswith("lock") or path.name.endswith(".lock") or path.name.endswith("-lock.json"):
        return ["lockfile present"]
    if path.name == "requirements.txt":
        count = 0
        try:
            count = sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip() and not line.startswith("#"))
        except Exception:
            pass
        return [f"{count} requirement lines"]
    if path.name.startswith("build.gradle") or path.name.startswith("settings.gradle"):
        return ["Gradle manifest"]
    if path.name == "pyproject.toml":
        return ["Python project metadata"]
    return ["manifest present"]


def scan(base: Path) -> list[Manifest]:
    found: list[Manifest] = []
    for current, dirs, files in os.walk(base, topdown=True, onerror=lambda error: None):
        dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
        current_path = Path(current)
        names = set(files)
        for manifest_name, ecosystem in MANIFESTS.items():
            if "/" in manifest_name:
                candidate = current_path / manifest_name
                if candidate.exists():
                    found.append(Manifest(relative(candidate, base), ecosystem, notes_for(candidate)))
            elif manifest_name in names:
                candidate = current_path / manifest_name
                found.append(Manifest(relative(candidate, base), ecosystem, notes_for(candidate)))
    return sorted(found, key=lambda item: (item.ecosystem, item.path))


def render(base: Path, manifests: list[Manifest]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    ecosystems = sorted({item.ecosystem for item in manifests})
    lines = [
        "# Dependency Manifest Radar",
        "",
        f"Scan root: `{base.name}`",
        f"Last refreshed: {now}",
        f"Manifests found: `{len(manifests)}`",
        f"Ecosystems: `{', '.join(ecosystems) if ecosystems else 'none'}`",
        "",
    ]
    if not manifests:
        lines.extend(["No dependency manifests were found.", ""])
        return "\n".join(lines)

    lines.extend(["| Ecosystem | Manifest | Notes |", "|---|---|---|"])
    for manifest in manifests:
        lines.append(f"| {manifest.ecosystem} | `{manifest.path}` | {', '.join(manifest.notes)} |")

    lines.extend([
        "",
        "## Suggested Automation",
        "",
        "- Use Renovate or Dependabot for scheduled update PRs.",
        "- Group low-risk patch/minor updates and keep major updates separate.",
        "- Require tests or build checks before merging dependency changes.",
        "- Keep lockfiles committed for applications and reproducible builds.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Find dependency manifests and draft update guidance.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to scan.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    base = Path(args.path).resolve()
    manifests = scan(base)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(base, manifests), encoding="utf-8")
    print(f"wrote {args.output} with {len(manifests)} manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
