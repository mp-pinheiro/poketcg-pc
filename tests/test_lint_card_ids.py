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

    def test_wide_integer_aliases_keep_card_id_provenance(self) -> None:
        bodies = (
            "uint16_t id16 = GetCard(index);\nuint8_t card = (uint8_t)id16;",
            "uint32_t first = GetCard(index);\nuint16_t second = first;\nuint8_t card = second;",
            "uint16_t id16;\nid16 = GetCard(index);\nuint8_t card = id16;",
            "CardId original;\nuint16_t alias = original;\nuint8_t card;\ncard = alias;",
            "uint8_t Function(void) {\nuint16_t id16 = GetCard(0);\nreturn id16;\n}",
            "uint16_t id16 = GetCard(index);\nif ((uint8_t)id16 == 7u) return;",
        )
        for body in bodies:
            with self.subTest(body=body):
                self.assertTrue(failures(body))

    def test_for_initializer_shadowing_does_not_erase_outer_card_id(self) -> None:
        statements = (
            "for (uint16_t card = 0; card < 1; ++card) {}",
            "for (uint16_t card = 0; card < 1; ++card) consume(card);",
            "for (uint16_t card = 0; card < 1; ++card) if (flag) consume(card); else consume(card);",
            "for (uint16_t card = 0; card < 1; ++card) for (uint32_t card = 0; card < 1; ++card) {}",
        )
        for statement in statements:
            with self.subTest(statement=statement):
                self.assertTrue(failures(f"uint8_t Function(CardId card) {{ {statement} return (uint8_t)card; }}"))

    def test_for_initializer_shadowing_keeps_ordinary_loop_values_local(self) -> None:
        body = "uint8_t Function(CardId card) { for (uint16_t card = 0; card < 1; ++card) { uint8_t byte = (uint8_t)card; } return (uint8_t)(card & 0xFFu); }"
        self.assertEqual(failures(body), [])

    def test_integer_alias_extraction_and_shadowing_remain_allowed(self) -> None:
        bodies = (
            "uint16_t id16 = GetCard(index);\nuint8_t low = id16 & 0xFFu;",
            "uint16_t id16 = GetCard(index);\nuint8_t high = id16 >> 8;",
            "uint16_t ordinary = 512u;\nuint8_t byte = (uint8_t)ordinary;",
            "uint16_t id16 = GetCard(index);\n{ uint16_t id16 = 4u;\nuint8_t byte = id16;\n}",
        )
        for body in bodies:
            with self.subTest(body=body):
                self.assertEqual(failures(body), [])

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
