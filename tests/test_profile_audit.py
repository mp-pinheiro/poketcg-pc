from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.profile_audit import NORMALIZED, Normalizer, Tree, parse_routines, string_constants

CONSTANT_SPELLING = NORMALIZED.index("constant-spelling")


def normalized(root: Path, operand: str) -> list[str]:
    checkout = root / operand.strip("$")
    (checkout / "src" / "constants").mkdir(parents=True)
    (checkout / "src" / "constants" / "duel_constants.asm").write_text(
        'DEF PLAYER_TURN EQUS "HIGH(wPlayerDuelVariables)"\n')
    (checkout / "src" / "turn.asm").write_text(f"Turn:\n\tld a, {operand}\n\tret\n")
    constants = string_constants(checkout, {"WPLAYERDUELVARIABLES": 0xC200})
    tree = Tree(parse_routines(checkout / "src"), constants, [])
    return Normalizer(tree, constants).lines(tree.routines["Turn"], CONSTANT_SPELLING)


class ConstantSpellingTests(unittest.TestCase):
    def test_label_derived_constant_matches_its_value(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            symbolic = normalized(root, "PLAYER_TURN")
            self.assertEqual(symbolic, normalized(root, "$c2"))
            self.assertNotEqual(symbolic, normalized(root, "$c3"))


if __name__ == "__main__":
    unittest.main()
