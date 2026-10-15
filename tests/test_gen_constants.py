from __future__ import annotations

import unittest

from tools.gen_constants import constant_names, evaluate
from tools.profiles import get_profile


class DeckConstantTests(unittest.TestCase):
    def test_deck_macro_exports_deck_and_opponent_ids(self) -> None:
        profile = get_profile("vanilla")
        source = profile.source_path()
        names = constant_names(source)
        self.assertIn("GO_GO_RAIN_DANCE_DECK", names)
        self.assertIn("GO_GO_RAIN_DANCE_DECK_ID", names)
        requested = [
            "GO_GO_RAIN_DANCE_DECK", "GO_GO_RAIN_DANCE_DECK_ID",
            "CHARMANDER_AND_FRIENDS_DECK", "CHARMANDER_AND_FRIENDS_DECK_ID",
            "UNNAMED_DECK_ID",
        ]
        values = evaluate(source, requested)
        for deck in ("GO_GO_RAIN_DANCE_DECK", "CHARMANDER_AND_FRIENDS_DECK"):
            self.assertEqual(values[deck + "_ID"], values[deck] - 2)
        self.assertNotIn("UNNAMED_DECK_ID", values)
