from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "template-preview.md"

FILES = {
    "README.md": "# {name}\n\nA small, maintainable project.\n\n## Run\n\n```bash\npython -m {module}\n```\n",
    "LICENSE": "MIT License\n\nCopyright (c) {year} {owner}\n",
    ".gitignore": "__pycache__/\n*.py[cod]\n.venv/\n.env\nreports/\n",
    "pyproject.toml": "[project]\nname = \"{name}\"\nversion = \"0.1.0\"\ndescription = \"A small, maintainable project.\"\nrequires-python = \">=3.11\"\n",
    "scripts/health_check.py": "from __future__ import annotations\n\nprint(\"health check ok\")\n",
    "reports/.gitkeep": "",
}


def module_name(name: str) -> str:
    return name.lower().replace("-", "_").replace(" ", "_")


def render_preview(name: str, owner: str, files: dict[str, str]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Repo Template Factory Preview",
        "",
        f"Last refreshed: {now}",
        f"Project name: `{name}`",
        f"Owner: `{owner}`",
        "",
        "## Files",
        "",
    ]
    for path, content in files.items():
        lines.extend([
            f"### `{path}`",
            "",
            "```text",
            content.strip()[:1200] or "<empty>",
            "```",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview or create a small maintainable project skeleton.")
    parser.add_argument("--name", default="valuable-tool", help="Project name.")
    parser.add_argument("--owner", default="GravityblueX", help="Owner name for generated metadata.")
    parser.add_argument("--output", type=Path, default=REPORT, help="Preview report path.")
    parser.add_argument("--create", type=Path, help="Create files under this directory. Existing files are never overwritten.")
    args = parser.parse_args()

    values = {
        "name": args.name,
        "module": module_name(args.name),
        "owner": args.owner,
        "year": str(datetime.now(timezone.utc).year),
    }
    rendered = {path: template.format(**values) for path, template in FILES.items()}

    if args.create:
        target = args.create.resolve()
        target.mkdir(parents=True, exist_ok=True)
        for rel, content in rendered.items():
            path = target / rel
            if path.exists():
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_preview(args.name, args.owner, rendered), encoding="utf-8")
    print(f"wrote {args.output} with {len(rendered)} template files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
