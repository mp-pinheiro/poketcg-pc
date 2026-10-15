from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.completion.revision import _git_source_revision


class SourceRevisionTests(unittest.TestCase):
    def test_merge_is_source_but_daily_snapshot_is_not(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args: str) -> str:
                return subprocess.run(
                    ["git", *args], cwd=root, text=True, capture_output=True, check=True,
                ).stdout.strip()

            def commit(subject: str) -> str:
                git("add", ".")
                git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "-c", "commit.gpgsign=false", "commit", "-qm", subject)
                return git("rev-parse", "HEAD")

            git("init", "-q", "-b", "main")
            (root / "runtime.c").write_text("base\n")
            initial = commit("feat(runtime): establish base")
            git("checkout", "-qb", "feature")
            (root / "feature.c").write_text("feature\n")
            commit("feat(runtime): add feature")
            git("checkout", "-q", "main")
            (root / "runtime.c").write_text("main\n")
            commit("fix(runtime): change main")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "-c", "commit.gpgsign=false", "merge", "--no-ff", "-m", "feat(runtime): merge feature", "feature")
            merge = git("rev-parse", "HEAD")
            self.assertNotEqual(merge, initial)
            self.assertEqual(_git_source_revision(root), merge)
            progress = root / "site/data/progress.json"
            progress.parent.mkdir(parents=True)
            progress.write_text("{}\n")
            commit("chore(progress): daily snapshot")
            self.assertEqual(_git_source_revision(root), merge)
