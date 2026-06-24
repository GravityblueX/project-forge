from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "grounded_evolution_radar.py"
SPEC = importlib.util.spec_from_file_location("grounded_evolution_radar", MODULE_PATH)
radar = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = radar
SPEC.loader.exec_module(radar)

BACKLOG_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "evolution_backlog.py"
BACKLOG_SPEC = importlib.util.spec_from_file_location("evolution_backlog", BACKLOG_MODULE_PATH)
backlog = importlib.util.module_from_spec(BACKLOG_SPEC)
assert BACKLOG_SPEC and BACKLOG_SPEC.loader
sys.modules[BACKLOG_SPEC.name] = backlog
BACKLOG_SPEC.loader.exec_module(backlog)


class GroundedEvolutionRadarTests(unittest.TestCase):
    def test_detects_placeholder_test_commands(self) -> None:
        scripts = [(Path("package.json"), {"test": 'node -e "console.log(\\"no tests configured\\")"'})]

        ok, note = radar.has_meaningful_test(Path.cwd(), scripts)

        self.assertFalse(ok)
        self.assertIn("no tests configured", note)

    def test_accepts_real_node_test_commands(self) -> None:
        scripts = [(Path("package.json"), {"test": 'node --test "test/**/*.test.js"'})]

        ok, note = radar.has_meaningful_test(Path.cwd(), scripts)

        self.assertTrue(ok)
        self.assertIn("node --test", note)

    def test_accepts_apk_contract_scripts_as_meaningful_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            scripts_dir = repo / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "study-apk-contract.ps1").write_text("exit 0", encoding="utf-8")

            ok, note = radar.has_meaningful_test(repo, [])

        self.assertTrue(ok)
        self.assertIn("study-apk-contract.ps1", note)

    def test_discovers_git_repositories_while_skipping_heavy_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "example"
            build_repo = root / "build" / "ignored"
            (repo / ".git").mkdir(parents=True)
            (build_repo / ".git").mkdir(parents=True)

            repos = radar.discover_repos([root])

        self.assertIn(repo.resolve(), repos)
        self.assertNotIn(build_repo.resolve(), repos)

    def test_counts_security_md_as_a_safety_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            (repo / "SECURITY.md").write_text(
                "Authorized testing only. Do not include live credentials.",
                encoding="utf-8",
            )

            ok, note = radar.safety_signal(repo)

        self.assertTrue(ok)
        self.assertIn("boundary", note)

    def test_render_report_includes_reference_patterns_and_actions(self) -> None:
        report = radar.render_report([
            {
                "name": "demo",
                "path": "C:/demo",
                "remote": "git@example/demo.git",
                "branch": "main",
                "head": "abc123",
                "dirtyCount": 0,
                "score": 50,
                "actions": ["Add tests."],
                "checks": [
                    {
                        "name": "meaningful tests",
                        "ok": False,
                        "pattern": "native-test-runner",
                        "note": "no tests",
                    }
                ],
            }
        ])

        self.assertIn("Grounded Evolution Radar", report)
        self.assertIn("OpenSSF Scorecard", report)
        self.assertIn("Add tests.", report)

    def test_evolution_backlog_marks_reference_repos_as_non_managed(self) -> None:
        payload = {
            "generatedAt": "2026-06-24T00:00:00+00:00",
            "repositories": [
                {
                    "name": "slider-captcha-lab",
                    "path": "C:/work/slider-captcha-lab",
                    "remote": "git@github.com:GravityblueX/slider-captcha-lab.git",
                    "score": 100,
                    "checks": [],
                },
                {
                    "name": "friend-reference",
                    "path": "C:/work/friend-reference",
                    "remote": "git@github.com:friend/reference.git",
                    "score": 70,
                    "dirtyCount": 1,
                    "checks": [],
                },
            ],
        }

        generated = backlog.build_backlog(payload)
        managed = {entry["name"]: entry["managed"] for entry in generated["entries"]}

        self.assertTrue(managed["slider-captcha-lab"])
        self.assertFalse(managed["friend-reference"])

    def test_evolution_backlog_uses_primary_reference_sources(self) -> None:
        payload = {
            "generatedAt": "2026-06-24T00:00:00+00:00",
            "repositories": [
                {
                    "name": "YumeBox-MaterialDesign-Study",
                    "path": "C:/work/Yume",
                    "remote": "https://github.com/GravityblueX/YumeBox-MaterialDesign-Study.git",
                    "score": 85,
                    "checks": [
                        {"name": "meaningful tests", "ok": False},
                    ],
                }
            ],
        }

        generated = backlog.build_backlog(payload)
        rendered = backlog.render_markdown(generated)

        self.assertIn("Android app signing", rendered)
        self.assertIn("study APK contract output", rendered)
        self.assertIn("developer.android.com", rendered)


if __name__ == "__main__":
    unittest.main()
