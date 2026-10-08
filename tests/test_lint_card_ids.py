from __future__ import annotations

import unittest
from pathlib import Path

from tools.lint_card_ids import block_failures


def failures(body: str) -> list[tuple[str, int, str, str]]:
    return block_failures(Path("sample.c"), "Function", body, {"GetCard"})


class CardIdNarrowingTests(unittest.TestCase):
    def test_card_id_values_cannot_be_narrowed(self) -> None:
        bodies = (
            "CardId card = GetCard(index);\nuint8_t byte = card;",
            "CardId card;\nuint8_t byte;\nbyte = card;",
            "void Function(CardId card) {\nuint8_t byte = card;\n}",
            "CardId card;\nuint8_t byte = (uint8_t)card;",
            "CardId card;\nuint8_t byte =\n    card;",
            "CardId card;\nuint8_t byte = (uint8_t)card == 1u;",
            "CardId card;\nuint8_t byte = (uint8_t)(card & 0x1ffu);",
            "CardId card;\nuint8_t byte = (uint8_t)(card << 0);",
            "CardId card;\nuint8_t byte = (uint8_t)(card >> 0);",
            "void Function(CardId card) {\nuint8_t byte = 0u + card;\n}",
            "void Function(CardId card) {\nif ((uint8_t)(0u + card) == 0u)\nreturn;\n}",
            "void Function(CardId card) {\nuint8_t first, byte;\nbyte = card;\n}",
            "void Function(CardId card) {\nuint8_t byte = card;\n{ uint8_t card = 0u; }\n}",
            "uint8_t Function(CardId card) {\nreturn card;\n}",
            "void Function(const CardId card) {\nuint8_t byte = card;\n}",
        )
        for body in bodies:
            with self.subTest(body=body):
                self.assertTrue(failures(body))

    def test_byte_extraction_and_comparisons_are_not_semantic_ids(self) -> None:
        bodies = (
            ("CardId card;\nuint8_t low = (uint8_t)(card & 0xffu);\nuint8_t high = (uint8_t)(card >> 8);\n"
             "uint8_t valid = (uint8_t)(card <= 0x1ffu);\nuint8_t below = card < 10u;\nCardId copy = card;\n"),
            "uint8_t matches = GetCard(0u) == 7u;",
            "CardId card;\nuint8_t matches = (card) == 7u;",
            "CardId card;\nuint8_t matches = (uint8_t)((card) == 7u);",
            "void Function(void) {\nuint8_t card = 3u;\nuint8_t index = card;\n{ CardId card = 0x100u; }\n}",
            "uint8_t Function(CardId card) {\nreturn (uint8_t)(card & 0xFFu);\n}",
        )
        for body in bodies:
            with self.subTest(body=body):
                self.assertEqual(failures(body), [])
