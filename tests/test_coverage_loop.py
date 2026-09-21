from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.completion import coverage_ledger


class CoverageLoopTests(unittest.TestCase):
    def test_recorded_seed_is_attempted_not_pending(self) -> None:
        ledger = {
            "routines": {
                "Effect": {"file": "effect_functions.asm", "sessions": []},
            }
        }
        carriers = {
            "Effect": [{
                "card": "TEST_CARD",
                "slot": "attack1",
                "command": "EFFECTCMDTYPE_AI_SELECTION",
            }]
        }

        frontier = coverage_ledger.target_frontier(
            ledger,
            [],
            records={},
            existing={"effect-test-card-1-ai-seed"},
            by_routine=carriers,
        )

        self.assertEqual(frontier["pending"], [])
        self.assertEqual(len(frontier["attempted"]), 1)
        self.assertEqual(frontier["stale"], [])

    def test_target_collision_never_overwrites_session(self) -> None:
        original = coverage_ledger.session.SESSIONS
        with tempfile.TemporaryDirectory() as tmp:
            coverage_ledger.session.SESSIONS = Path(tmp)
            existing = Path(tmp) / "effect-test-seed"
            existing.mkdir()
            sentinel = existing / "session.json"
            sentinel.write_text("sentinel\n")
            try:
                with self.assertRaises(coverage_ledger.CoverageError):
                    coverage_ledger.ensure_target_destinations_available("effect-test")
                self.assertEqual(sentinel.read_text(), "sentinel\n")
            finally:
                coverage_ledger.session.SESSIONS = original

    def test_stale_corpus_fails_open_to_discovery(self) -> None:
        original = coverage_ledger.EXPLORE_DIR
        with tempfile.TemporaryDirectory() as tmp:
            coverage_ledger.EXPLORE_DIR = Path(tmp)
            summary = Path(tmp) / "explore-seed.json"
            corpus = Path(tmp) / "explore-seed"
            corpus.mkdir()
            summary.write_text(json.dumps({"ledger_digest": "digest"}))
            index = corpus / "corpus.json"
            try:
                index.write_text(json.dumps({"entries": [{"script": "old.txt"}]}))
                self.assertFalse(coverage_ledger.corpus_current("seed", "digest"))
                index.write_text(json.dumps({
                    "entries": [{"script": "current.txt", "routines": []}],
                }))
                self.assertTrue(coverage_ledger.corpus_current("seed", "digest"))
            finally:
                coverage_ledger.EXPLORE_DIR = original

    def test_next_step_distinguishes_work_done_and_gate(self) -> None:
        cases = [
            ({"missing": 3, "pending_targets": 1, "intake_seed": "seed",
              "discover_seeds": ["discover"], "attempted_targets": 2}, "target", 0),
            ({"missing": 3, "pending_targets": 0, "intake_seed": "seed",
              "discover_seeds": ["discover"], "attempted_targets": 2}, "intake", 0),
            ({"missing": 3, "pending_targets": 0, "intake_seed": None,
              "discover_seeds": ["discover"], "attempted_targets": 2}, "discover", 0),
            ({"missing": 3, "pending_targets": 0, "intake_seed": None,
              "discover_seeds": [], "attempted_targets": 2}, "gate", 3),
            ({"missing": 0, "pending_targets": 0, "intake_seed": None,
              "discover_seeds": [], "attempted_targets": 2}, "done", 2),
        ]

        for arguments, expected_kind, expected_code in cases:
            with self.subTest(kind=expected_kind):
                kind, code, _detail = coverage_ledger.choose_coverage_step(**arguments)
                self.assertEqual((kind, code), (expected_kind, expected_code))


if __name__ == "__main__":
    unittest.main()
