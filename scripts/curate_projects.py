from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"
SCOREBOARD = ROOT / "docs" / "PROJECT_SCOREBOARD.md"

WEIGHTS = {
    "user_pain": 2.0,
    "technical_feasibility": 1.4,
    "distribution": 1.2,
    "portfolio_signal": 1.3,
    "maintenance_inverse": 1.0,
    "reuse_potential": 1.1,
    "ethical_safety": 1.5,
}


@dataclass
class Project:
    slug: str
    title: str
    audience: str
    problem: str
    mvp: str
    scores: dict[str, int]
    next_tasks: list[str]
    risks: list[str]
    tags: list[str]

    @property
    def value_score(self) -> float:
        total = 0.0
        weight_total = 0.0
        for key, weight in WEIGHTS.items():
            total += self.scores.get(key, 0) * weight
            weight_total += weight
        return round(total / max(weight_total, 1), 2)


def load_projects() -> list[Project]:
    projects: list[Project] = []
    for path in sorted(PROJECTS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        projects.append(Project(
            slug=data["slug"],
            title=data["title"],
            audience=data["audience"],
            problem=data["problem"],
            mvp=data["mvp"],
            scores={k: int(v) for k, v in data["scores"].items()},
            next_tasks=[str(x) for x in data.get("next_tasks", [])],
            risks=[str(x) for x in data.get("risks", [])],
            tags=[str(x) for x in data.get("tags", [])],
        ))
    return sorted(projects, key=lambda item: item.value_score, reverse=True)


def render(projects: list[Project]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Project Scoreboard",
        "",
        f"Last refreshed: {now}",
        "",
        "| Rank | Project | Score | Audience | Tags |",
        "|---:|---|---:|---|---|",
    ]
    for index, project in enumerate(projects, 1):
        tags = ", ".join(project.tags)
        lines.append(f"| {index} | [{project.title}](../projects/{project.slug}.json) | {project.value_score:.2f} | {project.audience} | {tags} |")

    lines.extend(["", "## Top Project Briefs", ""])
    for project in projects:
        lines.extend([
            f"### {project.title}",
            "",
            f"- Slug: `{project.slug}`",
            f"- Value score: `{project.value_score:.2f}`",
            f"- Problem: {project.problem}",
            f"- MVP: {project.mvp}",
            f"- Next tasks: {', '.join(project.next_tasks[:4])}",
            f"- Main risks: {', '.join(project.risks[:3])}",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    projects = load_projects()
    if not projects:
        raise SystemExit("No project cards found")
    SCOREBOARD.parent.mkdir(parents=True, exist_ok=True)
    SCOREBOARD.write_text(render(projects), encoding="utf-8")
    print(f"refreshed {SCOREBOARD} with {len(projects)} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
