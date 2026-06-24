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


if __name__ == "__main__":
    unittest.main()
