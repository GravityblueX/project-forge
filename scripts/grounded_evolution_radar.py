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
DEFAULT_OUTPUT = ROOT / "reports" / "grounded-evolution-radar.md"
DEFAULT_JSON = ROOT / "reports" / "grounded-evolution-radar.json"
SKIPPED_DIRS = {".gradle", ".idea", ".next", ".turbo", "build", "dist", "node_modules", "target"}


@dataclass(frozen=True)
class ReferencePattern:
    key: str
    label: str
    source: str
    local_signal: str
    why: str


PATTERNS = [
    ReferencePattern(
        "health-gates",
        "security and maintenance gates",
        "OpenSSF Scorecard",
        "README, license, CI workflow, dependency manifest, non-empty tests",
        "turns vague polish into repeatable repo-health checks",
    ),
    ReferencePattern(
        "dependency-rhythm",
        "controlled dependency update rhythm",
        "Renovate / Dependabot",
        "renovate.json or .github/dependabot.yml",
        "keeps updates boring, reviewable, and scheduled",
    ),
    ReferencePattern(
        "templateable-workflows",
        "templateable project scaffolding",
        "Backstage Software Templates / Copier / Cookiecutter",
        "project metadata, reusable scripts, generated reports",
        "makes good structure reusable instead of one-off",
    ),
    ReferencePattern(
        "debug-traces",
        "inspectable failure evidence",
        "Playwright Trace Viewer",
        "reports, logs, screenshots, JSON diagnostics, APK verification artifacts",
        "lets failures be replayed or audited without guesswork",
    ),
    ReferencePattern(
        "native-test-runner",
        "low-friction test runner",
        "Node.js test runner / language-native tests",
        "test command that executes real assertions",
        "prevents placeholder tests from pretending to be quality gates",
    ),
    ReferencePattern(
        "evidence-contracts",
        "machine-readable engineering evidence",
        "OpenAPI inventories / Android release manifests / Backstage catalogs",
        "api-surface, release-asset-manifest, project-registry, and contract reports",
        "turns one-off fixes into repeatable artifacts that other tools can audit",
    ),
]


def run_git(repo: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def discover_repos(roots: list[Path]) -> list[Path]:
    repos: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for current, directories, _files in os.walk(root, topdown=True, onerror=lambda _error: None):
            directories[:] = [name for name in directories if name not in SKIPPED_DIRS]
            if ".git" in directories:
                repos.add(Path(current).resolve())
                directories.remove(".git")
    return sorted(repos, key=lambda path: str(path).lower())


def iter_files(root: Path, wanted_names: set[str] | None = None) -> list[Path]:
    matches: list[Path] = []
    for current, directories, files in os.walk(root, topdown=True, onerror=lambda _error: None):
        directories[:] = [name for name in directories if name not in SKIPPED_DIRS]
        for name in files:
            if wanted_names is None or name in wanted_names:
                matches.append(Path(current) / name)
    return matches


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(read_text(path))
    except Exception:
        return {}


def package_scripts(repo: Path) -> list[tuple[Path, dict[str, str]]]:
    scripts: list[tuple[Path, dict[str, str]]] = []
    for package in iter_files(repo, {"package.json"}):
        data = load_json(package)
        package_scripts = data.get("scripts")
        if isinstance(package_scripts, dict):
            scripts.append((package.relative_to(repo), {str(k): str(v) for k, v in package_scripts.items()}))
    return scripts


def has_any(repo: Path, paths: list[str]) -> bool:
    return any((repo / path).exists() for path in paths)


def count_files(repo: Path, names: list[str]) -> int:
    return len(iter_files(repo, set(names)))


def has_meaningful_test(repo: Path, scripts: list[tuple[Path, dict[str, str]]]) -> tuple[bool, str]:
    test_commands = []
    for package_path, package_scripts in scripts:
        command = package_scripts.get("test", "")
        if command:
            test_commands.append(f"{package_path}: {command}")
    if not test_commands:
        python_tests = [
            path for path in iter_files(repo)
            if (path.name.startswith("test_") and path.suffix == ".py")
            or path.name.endswith("_test.py")
        ]
        if python_tests:
            return True, f"{len(python_tests)} Python test files"
        contract_scripts = [
            path for path in [
                repo / "scripts" / "study-apk-contract.ps1",
                repo / "scripts" / "verify-installable-apk.ps1",
            ]
            if path.exists()
        ]
        if contract_scripts:
            notes = "; ".join(str(path.relative_to(repo)) for path in contract_scripts)
            return True, notes
        return False, "no test command or common test files"

    placeholders = ["no tests configured", "echo", "not implemented"]
    meaningful = [
        command for command in test_commands
        if not any(marker in command.lower() for marker in placeholders)
    ]
    if meaningful:
        return True, "; ".join(meaningful[:3])
    return False, "; ".join(test_commands[:3])


def has_build(scripts: list[tuple[Path, dict[str, str]]], repo: Path) -> tuple[bool, str]:
    build_commands = [
        f"{package_path}: {package_scripts['build']}"
        for package_path, package_scripts in scripts
        if package_scripts.get("build")
    ]
    if build_commands:
        return True, "; ".join(build_commands[:3])
    if has_any(repo, ["gradlew", "gradlew.bat", "build.gradle", "build.gradle.kts"]):
        return True, "Gradle project"
    if has_any(repo, ["pyproject.toml", "requirements.txt"]):
        return True, "Python project manifest"
    return False, "no build command detected"


def release_signal(repo: Path) -> tuple[bool, str]:
    tags = run_git(repo, ["tag", "--list"])
    tag_count = len([line for line in tags.splitlines() if line.strip()])
    release_docs = list(repo.glob("release-notes*.md")) + list((repo / "docs").glob("*release*")) if (repo / "docs").exists() else list(repo.glob("release-notes*.md"))
    if tag_count or release_docs:
        details = []
        if tag_count:
            details.append(f"{tag_count} git tags")
        if release_docs:
            details.append(f"{len(release_docs)} release docs")
        return True, ", ".join(details)
    return False, "no local tags or release docs"


def diagnostic_signal(repo: Path) -> tuple[bool, str]:
    report_dirs = [repo / "reports", repo / "docs", repo / ".release-assets"]
    files = []
    for directory in report_dirs:
        if directory.exists():
            files.extend(iter_files(directory))
    logs = list(repo.glob("*.log"))
    diagnostics = [path for path in files if path.suffix.lower() in {".md", ".json", ".html", ".png"}]
    if diagnostics or logs:
        return True, f"{len(diagnostics)} report artifacts, {len(logs)} logs"
    return False, "no local report artifacts"


def contract_artifact_signal(repo: Path) -> tuple[bool, str]:
    artifact_names = [
        "api-surface",
        "openapi",
        "bom.cdx",
        "dependency-sbom",
        "dependency-inventory",
        "apk-installability-report",
        "build-environment",
        "release-asset-manifest",
        "release-provenance",
        "runtime-boundary",
        "study-apk-contract",
        "project-registry",
        "catalog-info",
        "project-promotion",
        "safety-contract",
        "workspace-verification",
        "release-readiness",
    ]
    matches = [
        path
        for path in iter_files(repo)
        if any(name in path.name for name in artifact_names)
        and path.suffix.lower() in {".md", ".json", ".mjs", ".ps1", ".py"}
    ]
    if matches:
        examples = ", ".join(str(path.relative_to(repo)) for path in matches[:4])
        return True, f"{len(matches)} contract artifact(s): {examples}"
    return False, "no API, release asset, APK, or project registry contract artifacts"


def safety_signal(repo: Path) -> tuple[bool, str]:
    text = "\n".join(
        read_text(repo / name)
        for name in ["README.md", "DISCLAIMER.md", "SAFETY.md", "SECURITY.md", "docs/PROJECT_POLICY.md"]
    )
    if any(word in text.lower() for word in ["authorized", "授权", "disclaimer", "仅用于", "safety"]):
        return True, "explicit safety or authorization boundary found"
    return False, "no explicit safety boundary found"


def score_repo(repo: Path) -> dict[str, Any]:
    scripts = package_scripts(repo)
    remote = run_git(repo, ["remote", "get-url", "origin"])
    branch = run_git(repo, ["branch", "--show-current"])
    head = run_git(repo, ["rev-parse", "--short", "HEAD"])
    dirty_count = len([line for line in run_git(repo, ["status", "--short"]).splitlines() if line.strip()])

    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, weight: int, note: str, pattern: str) -> None:
        checks.append({
            "name": name,
            "ok": ok,
            "weight": weight,
            "points": weight if ok else 0,
            "note": note,
            "pattern": pattern,
        })

    add("readme", has_any(repo, ["README.md", "readme.md"]), 8, "README present" if has_any(repo, ["README.md", "readme.md"]) else "missing README", "health-gates")
    add("license", has_any(repo, ["LICENSE", "LICENSE.md"]), 6, "license present" if has_any(repo, ["LICENSE", "LICENSE.md"]) else "missing license", "health-gates")
    add("ci workflow", (repo / ".github" / "workflows").exists(), 10, "workflow directory present" if (repo / ".github" / "workflows").exists() else "no workflow directory", "health-gates")

    build_ok, build_note = has_build(scripts, repo)
    add("build signal", build_ok, 10, build_note, "native-test-runner")

    test_ok, test_note = has_meaningful_test(repo, scripts)
    add("meaningful tests", test_ok, 12, test_note, "native-test-runner")

    dependency_files = count_files(repo, ["package.json", "pyproject.toml", "requirements.txt", "build.gradle.kts", "libs.versions.toml"])
    add("dependency manifests", dependency_files > 0, 7, f"{dependency_files} manifest files" if dependency_files else "no common manifest", "dependency-rhythm")
    add("dependency automation", has_any(repo, ["renovate.json", ".github/dependabot.yml", ".github/dependabot.yaml"]), 7, "automation config found" if has_any(repo, ["renovate.json", ".github/dependabot.yml", ".github/dependabot.yaml"]) else "no dependency update config", "dependency-rhythm")

    release_ok, release_note = release_signal(repo)
    add("release evidence", release_ok, 8, release_note, "templateable-workflows")

    diagnostics_ok, diagnostics_note = diagnostic_signal(repo)
    add("diagnostic artifacts", diagnostics_ok, 8, diagnostics_note, "debug-traces")

    contract_ok, contract_note = contract_artifact_signal(repo)
    add("contract artifacts", contract_ok, 0, contract_note, "evidence-contracts")

    safety_ok, safety_note = safety_signal(repo)
    add("safety boundary", safety_ok, 6, safety_note, "health-gates")

    max_points = sum(check["weight"] for check in checks)
    points = sum(check["points"] for check in checks)
    score = round(points / max(max_points, 1) * 100)

    missing = [check for check in checks if not check["ok"]]
    actions = []
    for check in missing:
        if check["name"] == "meaningful tests":
            actions.append("Replace placeholder tests with fast smoke or contract tests.")
        elif check["name"] == "dependency automation":
            actions.append("Draft Renovate or Dependabot config with conservative grouping.")
        elif check["name"] == "ci workflow":
            actions.append("Add a minimal CI workflow that runs build and tests.")
        elif check["name"] == "diagnostic artifacts":
            actions.append("Emit markdown/JSON reports for every release or maintenance run.")
        elif check["name"] == "safety boundary":
            actions.append("Add explicit authorized-use and non-abuse boundaries.")
        elif check["name"] == "release evidence":
            actions.append("Create a tagged release or release-readiness report when build outputs are reproducible.")
        elif check["name"] == "contract artifacts":
            actions.append("Add a machine-readable API, release asset, APK, or project registry contract report.")
        elif check["name"] == "readme":
            actions.append("Add README usage, verification, and project status sections.")
        elif check["name"] == "license":
            actions.append("Add license metadata when the repo is intended for reuse.")

    return {
        "name": repo.name,
        "path": str(repo),
        "remote": remote,
        "branch": branch,
        "head": head,
        "dirtyCount": dirty_count,
        "score": score,
        "checks": checks,
        "actions": actions[:6] or ["Keep current maintenance rhythm and tighten next measurable gate."],
    }


def render_report(rows: list[dict[str, Any]]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Grounded Evolution Radar",
        "",
        f"Last refreshed: {now}",
        "",
        "This report maps local repositories to proven patterns from mature projects.",
        "It is intentionally boring: each recommendation is tied to an observable local signal.",
        "",
        "## Reference Patterns",
        "",
        "| Pattern | Borrowed From | Local Signal | Why It Matters |",
        "|---|---|---|---|",
    ]
    for pattern in PATTERNS:
        lines.append(f"| {pattern.label} | {pattern.source} | {pattern.local_signal} | {pattern.why} |")

    lines.extend([
        "",
        "## Repository Scores",
        "",
        "| Rank | Repository | Score | Dirty | Top Next Action |",
        "|---:|---|---:|---:|---|",
    ])
    ranked = sorted(rows, key=lambda row: (row["score"], row["name"]), reverse=True)
    for index, row in enumerate(ranked, 1):
        lines.append(f"| {index} | `{row['name']}` | {row['score']} | {row['dirtyCount']} | {row['actions'][0]} |")

    lines.extend(["", "## Details", ""])
    for row in ranked:
        lines.extend([
            f"### {row['name']}",
            "",
            f"- Path: `{row['path']}`",
            f"- Remote: `{row['remote'] or 'none'}`",
            f"- Branch: `{row['branch'] or 'unknown'}`",
            f"- HEAD: `{row['head'] or 'unknown'}`",
            f"- Dirty files: `{row['dirtyCount']}`",
            f"- Score: `{row['score']}`",
            "",
            "| Check | Result | Pattern | Evidence |",
            "|---|---|---|---|",
        ])
        for check in row["checks"]:
            result = "OK" if check["ok"] else "Gap"
            lines.append(f"| {check['name']} | {result} | {check['pattern']} | {check['note']} |")
        lines.extend(["", "Next actions:"])
        for action in row["actions"]:
            lines.append(f"- {action}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a reference-grounded evolution radar for local repos.")
    parser.add_argument("--root", action="append", type=Path, help="Root directory to scan. Can be used more than once.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Markdown report path.")
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help="JSON report path.")
    args = parser.parse_args()

    roots = args.root or [ROOT.parent, Path.home() / "Desktop"]
    repos = [repo for repo in discover_repos(roots) if is_git_repo(repo)]
    rows = [score_repo(repo) for repo in repos]

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "roots": [str(root) for root in roots],
        "patterns": [pattern.__dict__ for pattern in PATTERNS],
        "repositories": rows,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(rows), encoding="utf-8")
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.output} with {len(rows)} repositories")
    print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
