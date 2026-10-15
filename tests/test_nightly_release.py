from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.nightly_release import source_changed


class NightlyReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

        def git(*args: str) -> str:
            return subprocess.run(
                ["git", *args], cwd=self.root, text=True, capture_output=True, check=True,
            ).stdout.strip()

        self.git = git
        git("init", "-q", "-b", "main")
        git("config", "user.name", "Fixture")
        git("config", "user.email", "fixture@example.invalid")
        git("config", "commit.gpgsign", "false")
        (self.root / "runtime.c").write_text("base\n")
        self.baseline = self.commit("feat(runtime): base")

    def commit(self, subject: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-qm", subject)
        return self.git("rev-parse", "HEAD")

    def test_all_derived_paths_are_excluded(self) -> None:
        values = {
            "site/data/gate.json": "{}\n",
            "site/data/history.jsonl": "{}\n",
            "site/data/progress.json": "{}\n",
        }
        for path, content in values.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        current = self.commit("chore(progress): derived snapshots")
        self.assertFalse(source_changed(self.root, self.baseline, current))

    def test_source_change_with_derived_changes_is_meaningful(self) -> None:
        (self.root / "runtime.c").write_text("changed\n")
        derived = self.root / "site/data/progress.json"
        derived.parent.mkdir(parents=True)
        derived.write_text("{}\n")
        current = self.commit("feat(runtime): source and snapshot")
        self.assertTrue(source_changed(self.root, self.baseline, current))

    def test_reverted_content_equal_to_baseline_is_unchanged(self) -> None:
        (self.root / "runtime.c").write_text("temporary\n")
        self.commit("feat(runtime): temporary change")
        (self.root / "runtime.c").write_text("base\n")
        reverted = self.commit("revert(runtime): restore baseline")
        self.assertFalse(source_changed(self.root, self.baseline, reverted))

    def test_deleted_source_is_meaningful(self) -> None:
        (self.root / "runtime.c").unlink()
        current = self.commit("refactor(runtime): remove source")
        self.assertTrue(source_changed(self.root, self.baseline, current))

    def test_executable_mode_change_is_meaningful(self) -> None:
        script = self.root / "runtime.sh"
        script.write_text("#!/bin/sh\nexit 0\n")
        self.baseline = self.commit("feat(runtime): add script")
        script.chmod(0o755)
        current = self.commit("chore(runtime): make script executable")
        self.assertTrue(source_changed(self.root, self.baseline, current))

    def test_invalid_refs_raise_instead_of_skipping(self) -> None:
        with self.assertRaises(RuntimeError):
            source_changed(self.root, "missing-ref", self.baseline)
