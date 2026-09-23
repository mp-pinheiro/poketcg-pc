from __future__ import annotations

import contextlib
import io
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.completion import completion, evidence, producers


class CompletionEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        for name, content in (
            ("producer.py", "producer\n"),
            ("comparator.py", "comparator\n"),
            ("native.bin", "native\n"),
            ("reference.txt", "reference\n"),
            ("raw.json", "raw\n"),
        ):
            (self.root / name).write_text(content, encoding="utf-8")
        self.requirement = {
            "id": "completion:v2:p2:boot-title",
            "artifact_schema": "scenario-corpus-v2",
            "terminal_event": "NEW_GAME_ENTERED",
            "min_frames": 1,
            "min_events": 1,
            "state_fields": ["wram", "framebuffer"],
            "specification": {"norm": "v1"},
            "producer_files": ["producer.py"],
            "comparator_files": ["comparator.py"],
            "native": {"files": ["native.bin"]},
            "reference": {"files": ["reference.txt"]},
        }

    def tearDown(self) -> None:
        self.directory.cleanup()

    def manifest(self) -> dict:
        return evidence.input_manifest(
            self.root,
            self.requirement,
            lane_manifest=None,
            corpus=[],
            dependencies=[],
        )

    def artifact(self, manifest: dict) -> dict:
        return {
            "schema": "scenario-corpus-v2",
            "status": "PASS",
            "input_manifest": manifest,
            "input_digest": evidence.canonical_digest(manifest),
            "produced_revision": "source-revision",
            "dependencies": [],
            "terminal_event": "NEW_GAME_ENTERED",
            "frames": 1,
            "events": 1,
            "state_fields": ["wram", "framebuffer"],
            "oracles": ["native", "reference"],
            "comparison": {"status": "PASS"},
            "observations": [evidence.file_identity(self.root, "raw.json")],
        }

    def test_canonical_digest_is_order_stable_and_rejects_nan(self) -> None:
        self.assertEqual(
            evidence.canonical_digest({"a": [1, 2], "b": "x"}),
            evidence.canonical_digest({"b": "x", "a": [1, 2]}),
        )
        with self.assertRaises(evidence.EvidenceError):
            evidence.canonical_digest({"nan": math.nan})

    def test_validator_requires_current_comparator_and_raw_observation(self) -> None:
        manifest = self.manifest()
        artifact = self.artifact(manifest)
        self.assertEqual(
            evidence.validate_requirement(
                self.root, self.requirement, artifact, manifest
            ),
            ("pass", None),
        )
        (self.root / "comparator.py").write_text("changed\n", encoding="utf-8")
        changed = self.manifest()
        self.assertEqual(
            evidence.validate_requirement(
                self.root, self.requirement, artifact, changed
            )[0],
            "stale",
        )
        (self.root / "raw.json").unlink()
        self.assertEqual(
            evidence.validate_requirement(
                self.root, self.requirement, artifact, manifest
            )[0],
            "invalid",
        )

    def test_check_evidence_uses_explicit_root_and_validation_receipt(self) -> None:
        manifest = self.manifest()
        artifact = self.artifact(manifest)
        path = completion.evidence_path(self.requirement["id"], root=self.root)
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(artifact), encoding="utf-8")
        self.assertEqual(
            completion.check_evidence(
                self.requirement, root=self.root, expected_manifest=manifest
            )[0],
            "stale",
        )
        receipt = evidence.validation_receipt(
            self.root,
            artifact,
            artifact["input_digest"],
            "source-revision",
        )
        path.with_suffix(path.suffix + ".validation.json").write_text(
            json.dumps(receipt), encoding="utf-8"
        )
        self.assertEqual(
            completion.check_evidence(
                self.requirement, root=self.root, expected_manifest=manifest
            ),
            ("pass", None),
        )
        (self.root / "raw.json").write_text("tampered\n", encoding="utf-8")
        self.assertEqual(
            completion.check_evidence(
                self.requirement, root=self.root, expected_manifest=manifest
            )[0],
            "invalid",
        )

    def test_validator_rejects_native_only_evidence(self) -> None:
        manifest = self.manifest()
        artifact = self.artifact(manifest)
        artifact["oracles"] = ["native"]
        self.assertEqual(
            evidence.validate_requirement(
                self.root, self.requirement, artifact, manifest
            )[0],
            "failing",
        )

    def test_scenario_exit_tracks_validator_result(self) -> None:
        from tools.completion import scenario

        def run(status: str) -> int:
            output = io.StringIO()
            with (
                mock.patch.object(
                    scenario, "run_native", return_value=(1, "", "missing")
                ),
                mock.patch("tools.completion.completion.write_evidence_artifact"),
                mock.patch(
                    "tools.completion.completion.check_evidence",
                    return_value=(status, "detail"),
                ),
                contextlib.redirect_stdout(output),
            ):
                return scenario.main(["boot-title", "--frames", "1"])

        self.assertEqual(run("pass"), 0)
        self.assertEqual(run("failing"), 2)
        self.assertEqual(run("unavailable"), 3)

    def test_every_requirement_has_a_typed_producer_descriptor(self) -> None:
        manifest = completion.load_toml(completion.MANIFEST_PATH)
        requirements = manifest["requirement"]
        self.assertEqual({row["id"] for row in requirements}, set(producers.ids()))
        for requirement in requirements:
            descriptor = producers.describe(requirement["id"])
            self.assertEqual(requirement["producer"], descriptor["producer"])
            self.assertTrue(
                descriptor["handler"] is None or isinstance(descriptor["handler"], str)
            )
            self.assertTrue(descriptor["producer_files"])
            self.assertTrue(descriptor["comparator_files"])

    def test_session_no_publish_keeps_tracker_unwritten(self) -> None:
        from tools.completion import session

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            previous = session.TRACKER_DIR
            session.TRACKER_DIR = root / "tracker"
            try:
                output = root / "report.json"
                session.emit(
                    {"name": "session", "status": "clean"}, output, publish=False
                )
                self.assertTrue(output.is_file())
                self.assertFalse((session.TRACKER_DIR / "verify-session.json").exists())
            finally:
                session.TRACKER_DIR = previous


if __name__ == "__main__":
    unittest.main()
