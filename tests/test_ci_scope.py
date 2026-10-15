from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.ci_scope import documentation_only


class CiScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.write("runtime.c", "int runtime = 1;\n")
        self.write("README.md", "# Read me\n")
        self.write("docs/vision.md", "# Acceptance\n")
        self.requirements = self.write(
            "tools/completion/requirements.toml",
            '[manifest]\nsource = "docs/vision.md"\nsource_sha256 = "before"\n'
            'schema = 2\n[[requirement]]\nid = "boot"\nanchor = "docs/vision.md:1"\n'
            'min_frames = 600\n',
        )
        self.baseline = self.commit("feat(runtime): base")

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments], cwd=self.root, text=True, capture_output=True, check=True,
        ).stdout.strip()

    def write(self, path: str, content: str) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def commit(self, subject: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-qm", subject)
        return self.git("rev-parse", "HEAD")

    def test_prose_and_requirement_locations_use_documentation_scope(self) -> None:
        self.write("README.md", "# Short readme\n")
        self.write("docs/vision.md", "# Revised acceptance\n")
        self.requirements.write_text(
            self.requirements.read_text().replace('"before"', '"after"').replace(
                'anchor = "docs/vision.md:1"', 'anchor = "docs/vision.md:2"',
            ),
        )
        self.write("site/data/progress.json", '{}\n')
        current = self.commit("docs(guide): revise prose")
        self.assertTrue(documentation_only(self.root, self.baseline, current))

    def test_semantic_contract_change_uses_full_scope(self) -> None:
        self.requirements.write_text(self.requirements.read_text().replace(
            "min_frames = 600", "min_frames = 601",
        ))
        current = self.commit("test(boot): raise frame bound")
        self.assertFalse(documentation_only(self.root, self.baseline, current))

    def test_scalar_type_change_uses_full_scope(self) -> None:
        self.requirements.write_text(self.requirements.read_text().replace(
            "min_frames = 600", "min_frames = 600.0",
        ))
        current = self.commit("test(boot): change bound type")
        self.assertFalse(documentation_only(self.root, self.baseline, current))

    def test_code_change_cannot_hide_behind_later_snapshot_commit(self) -> None:
        self.write("runtime.c", "int runtime = 2;\n")
        self.commit("fix(runtime): change behavior")
        self.write("site/data/progress.json", '{}\n')
        current = self.commit("chore(progress): refresh snapshot")
        self.assertFalse(documentation_only(self.root, self.baseline, current))

    def test_instruction_and_unclassified_markdown_require_full_scope(self) -> None:
        for path in ("AGENTS.md", ".github/copilot-instructions.md", "assets/help.md"):
            with self.subTest(path=path):
                self.write(path, "# Machine input\n")
                current = self.commit("chore(input): add instructions")
                self.assertFalse(documentation_only(self.root, self.baseline, current))
                self.baseline = current

    def test_requirement_file_mode_change_is_not_documentation(self) -> None:
        self.requirements.chmod(0o755)
        current = self.commit("chore(input): change mode")
        self.assertFalse(documentation_only(self.root, self.baseline, current))

    def test_requirement_file_deletion_requires_full_scope(self) -> None:
        self.requirements.unlink()
        current = self.commit("chore(input): remove contract")
        self.assertFalse(documentation_only(self.root, self.baseline, current))

    def test_invalid_base_never_skips_verification(self) -> None:
        with self.assertRaises(RuntimeError):
            documentation_only(self.root, "missing-ref", self.baseline)


if __name__ == "__main__":
    unittest.main()
