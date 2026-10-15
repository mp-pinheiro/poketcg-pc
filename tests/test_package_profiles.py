from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.package_profiles import verify_stage


class ProfilePackagePolicyTests(unittest.TestCase):
    def test_rejects_nested_rom_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            stage = Path(temporary)
            artifact = stage / "assets" / "original.gbc"
            artifact.parent.mkdir()
            artifact.write_bytes(b"unshippable")
            with self.assertRaisesRegex(SystemExit, "profile package contains forbidden file"):
                verify_stage(stage)
