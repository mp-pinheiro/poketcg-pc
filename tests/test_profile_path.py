from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

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

    def test_environment_variant_selects_fixture_paths(self) -> None:
        with mock.patch.dict(os.environ, {"POKETCG_PROFILE_VARIANT": "boundary"}):
            expected = str(get_profile("extended", ROOT).sym_path(ROOT))
            self.assertEqual(self.run_path("sym"), expected)

    def test_shared_build_keeps_profile_pack_artifacts_isolated(self) -> None:
        with mock.patch.dict(os.environ, {"POKETCG_BUILD": "build-shared", "POKETCG_PROFILE_VARIANT": ""}):
            vanilla = get_profile("vanilla", ROOT)
            extended = get_profile("extended", ROOT)
            self.assertNotEqual(vanilla.data_pack_path(ROOT), extended.data_pack_path(ROOT))
            for profile in (vanilla, extended):
                self.assertEqual(profile.data_pack_path(ROOT), profile.artifact_path("data_pack", ROOT))
                for kind in ("data_pack", "pack_manifest"):
                    self.assertEqual(profile.artifact_path(kind, ROOT).parent, ROOT / "build-shared/completion")
