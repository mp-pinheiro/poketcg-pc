from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.progress.report import append_history


class ProgressHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "history.jsonl"
        self.point = {
            "timestamp": 172800,
            "commit": "source-a",
            "code": 8,
            "code_total": 10,
            "functions": 2,
            "functions_total": 3,
        }

    def records(self) -> list[dict]:
        return [json.loads(line) for line in self.path.read_text().splitlines()]

    def test_same_day_release_records_and_measurements_are_preserved(self) -> None:
        previous = dict(self.point, timestamp=172801, code=7)
        release = {"schema": 3, "timestamp": 172802, "attestation_sha256": "release-a"}
        prefix = "".join(json.dumps(record) + "\n" for record in (previous, release))
        self.path.write_text(prefix)
        append_history(self.path, dict(self.point, timestamp=172803))
        self.assertTrue(self.path.read_text().startswith(prefix))
        self.assertEqual(self.records(), [previous, release, dict(self.point, timestamp=172803)])

    def test_unchanged_measurements_do_not_duplicate_with_release_between(self) -> None:
        append_history(self.path, self.point)
        release = {"schema": 3, "timestamp": 172802, "attestation_sha256": "release-b"}
        with self.path.open("a") as stream:
            stream.write(json.dumps(release) + "\n")
        before = self.path.read_bytes()
        append_history(self.path, dict(self.point, timestamp=172803, commit="derived-only"))
        self.assertEqual(self.path.read_bytes(), before)

    def test_new_day_records_unchanged_measures(self) -> None:
        append_history(self.path, self.point)
        tomorrow = dict(self.point, timestamp=259200)
        append_history(self.path, tomorrow)
        self.assertEqual(self.records(), [self.point, tomorrow])
