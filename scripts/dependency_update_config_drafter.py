from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "dependency-update-config.md"
SKIP_DIRS = {".git", ".gradle", ".venv", "build", "dist", "node_modules", "__pycache__"}


def relative(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base)).replace("\\", "/")
    except ValueError:
        return path.name


def detect(base: Path) -> dict[str, list[str]]:
    ecosystems: dict[str, list[str]] = {"npm": [], "pip": [], "gradle": []}
    for current, dirs, files in os.walk(base, topdown=True, onerror=lambda error: None):
        dirs[:] = [directory for directory in dirs if directory not in SKIP_DIRS]
        path = Path(current)
        names = set(files)
        if "package.json" in names:
            ecosystems["npm"].append(relative(path, base) or ".")
        if "requirements.txt" in names or "pyproject.toml" in names:
            ecosystems["pip"].append(relative(path, base) or ".")
        if names.intersection({"build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"}):
            ecosystems["gradle"].append(relative(path, base) or ".")
    return {key: sorted(value) for key, value in ecosystems.items() if value}


def renovate_config(ecosystems: dict[str, list[str]]) -> str:
    config = {
        "$schema": "https://docs.renovatebot.com/renovate-schema.json",
        "extends": ["config:recommended"],
        "schedule": ["before 5am on monday"],
        "dependencyDashboard": True,
        "labels": ["dependencies"],
        "packageRules": [
            {
                "matchUpdateTypes": ["minor", "patch", "pin", "digest"],
                "groupName": "low-risk dependency updates",
                "automerge": False,
            },
            {
                "matchUpdateTypes": ["major"],
                "labels": ["dependencies", "major-update"],
                "automerge": False,
            },
        ],
    }
    if "gradle" in ecosystems:
        config["labels"].append("gradle")
    return json.dumps(config, indent=2)


def dependabot_config(ecosystems: dict[str, list[str]]) -> str:
    package_map = {"npm": "npm", "pip": "pip", "gradle": "gradle"}
    lines = [
        "version: 2",
        "updates:",
    ]
    for ecosystem, directories in ecosystems.items():
        for directory in directories:
            normalized = "/" if directory == "." else f"/{directory}"
            lines.extend([
                f"  - package-ecosystem: \"{package_map[ecosystem]}\"",
                f"    directory: \"{normalized}\"",
                "    schedule:",
                "      interval: \"weekly\"",
                "    open-pull-requests-limit: 5",
            ])
    return "\n".join(lines)


def render(base: Path, ecosystems: dict[str, list[str]]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Dependency Update Config Draft",
        "",
        f"Scan root: `{base.name}`",
        f"Last refreshed: {now}",
        "",
    ]
    if not ecosystems:
        lines.extend([
            "No supported dependency ecosystems were detected.",
            "",
            "Supported MVP ecosystems: npm, pip, Gradle.",
            "",
        ])
        return "\n".join(lines)

    lines.extend(["## Detected Ecosystems", "", "| Ecosystem | Directories |", "|---|---|"])
    for ecosystem, directories in ecosystems.items():
        lines.append(f"| {ecosystem} | {', '.join(f'`{item}`' for item in directories)} |")

    lines.extend([
        "",
        "## Renovate Draft",
        "",
        "Save as `renovate.json` after review.",
        "",
        "```json",
        renovate_config(ecosystems),
        "```",
        "",
        "## Dependabot Draft",
        "",
        "Save as `.github/dependabot.yml` after review.",
        "",
        "```yaml",
        dependabot_config(ecosystems),
        "```",
        "",
        "## Review Notes",
        "",
        "- Keep major updates separate from patch/minor batches.",
        "- Require tests before enabling automerge.",
        "- Add private registry credentials only through encrypted secrets.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Draft Renovate and Dependabot configs from detected manifests.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to scan.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Report path.")
    args = parser.parse_args()

    base = Path(args.path).resolve()
    ecosystems = detect(base)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(base, ecosystems), encoding="utf-8")
    print(f"wrote {args.output} with {len(ecosystems)} ecosystems")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
