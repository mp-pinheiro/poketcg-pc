from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.compose_profile import block_lines, deduplicate, mutation_source, units
from tools.factory_blocks import Block
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


class DeduplicateCompileTests(unittest.TestCase):
    def test_probe_addition_keeps_its_include_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = get_profile("extended", ROOT)
            includes = Block("part", "includes", 0, 0, ["#include <stdint.h>"])
            main = Block("factory", "main", 0, 0, [
                "int main(void) { return extra(3u) == 10u ? 0 : 1; }",
            ])
            extra = Block("factory", "extra", 0, 0, [
                "static uint8_t extra(uint8_t value) { return (uint8_t)(value * value + 1u); }",
            ])
            shared = root / "src/probe/sample.c"
            override = profile.overlay_path(root) / "probe/sample.c"
            shared.parent.mkdir(parents=True)
            override.parent.mkdir(parents=True)
            shared.write_text("\n".join(block_lines(includes) + block_lines(main)) + "\n")
            override.write_text("\n".join(block_lines(includes) + block_lines(extra)) + "\n")
            deduplicate(profile, root)
            source = root / "composed.c"
            source.write_text(next(unit for unit in units(profile, root) if unit.tree == "probe").text())
            binary = root / "program"
            compiled = subprocess.run(
                ["cc", "-std=c11", "-Werror", str(source), "-o", str(binary)],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(compiled.returncode, 0, compiled.stderr)
            result = subprocess.run([str(binary)], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
