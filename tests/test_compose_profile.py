from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.compose_profile import mutation_source
from tools.profiles import get_profile

ROOT = Path(__file__).resolve().parents[1]


class MutationSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.profile = get_profile("extended", ROOT)
        self.shared = self.root / "src/home/sample.c"
        self.fragment = self.profile.overlay_path(self.root) / "home/sample.c"
        self.shared.parent.mkdir(parents=True)
        self.fragment.parent.mkdir(parents=True)
        self.shared.write_text("/* >>> factory Target */\nint Target(void)\n{\n\treturn 0x10u;\n}\n/* <<< factory Target */\n")

    def test_unrelated_override_does_not_own_shared_mutation(self) -> None:
        self.fragment.write_text("/* >>> factory Other */\nint Other(void)\n{\n\treturn 0x10u;\n}\n/* <<< factory Other */\n")
        self.assertEqual(mutation_source(self.profile, "sample", "Target", "0x10u", self.root), self.shared)

    def test_override_owns_its_routine_even_with_shared_anchor(self) -> None:
        self.fragment.write_text("/* >>> factory Target */\nint Target(void)\n{\n\treturn 0x10u + 1u;\n}\n/* <<< factory Target */\n")
        self.assertEqual(mutation_source(self.profile, "sample", "Target", "0x10u", self.root), self.fragment)
