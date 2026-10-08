from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

from tools.profiles import get_profile

ROOT = Path(__file__).resolve().parents[1]


class ProfilePathTests(unittest.TestCase):
    def run_path(self, kind: str, profile: str | None = None) -> str:
        env = dict(os.environ, POKETCG_PROFILE="extended")
        command = [sys.executable, str(ROOT / "tools/profile_path.py"), kind]
        if profile is not None:
            command.extend(["--profile", profile])
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def test_environment_selects_profile(self) -> None:
        expected = str(get_profile("extended", ROOT).sym_path(ROOT))
        self.assertEqual(self.run_path("sym"), expected)

    def test_explicit_profile_overrides_environment(self) -> None:
        expected = str(get_profile("vanilla", ROOT).sym_path(ROOT))
        self.assertEqual(self.run_path("sym", "vanilla"), expected)
