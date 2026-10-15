from __future__ import annotations

import contextlib
import io
import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.completion import completion, evidence


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

    def write_documentation_inputs(self, *, anchor: str = "docs/vision.md:3") -> dict:
        vision = self.root / "docs/vision.md"
        vision.parent.mkdir(parents=True, exist_ok=True)
        vision.write_text(
            "Vision\n"
            "- `completion:v2:p2:boot-title-negative`: claim\n"
            "- `completion:v2:p2:boot-title`: claim\n",
            encoding="utf-8",
        )
        source_hash = evidence.sha256_path(vision)
        requirements = self.root / "tools/completion/requirements.toml"
        requirements.parent.mkdir(parents=True, exist_ok=True)
        requirements.write_text(
            "[manifest]\nschema = 2\nversion = \"test\"\n"
            "source = \"docs/vision.md\"\n"
            f"source_sha256 = \"{source_hash}\"\n"
            "\n[[requirement]]\nid = \"completion:v2:p2:boot-title\"\n"
            f"anchor = \"{anchor}\"\n"
            "artifact_schema = \"scenario-corpus-v2\"\n"
            "terminal_event = \"NEW_GAME_ENTERED\"\n"
            "min_frames = 1\nmin_events = 1\nstate_fields = [\"wram\", \"framebuffer\"]\n",
            encoding="utf-8",
        )
        (self.root / "tools/completion/baseline.toml").write_text(
            "[baseline]\nepoch = 1\n", encoding="utf-8"
        )
        self.requirement.pop("specification", None)
        return completion.load_toml(requirements)

    def test_documentation_changes_preserve_semantic_manifest_and_artifact(self) -> None:
        document = self.write_documentation_inputs()
        manifest = self.manifest()
        artifact = self.artifact(manifest)
        evidence.validate_documentation(self.root, document)
        old_identity = evidence.requirements_file_identity(
            self.root, "tools/completion/requirements.toml"
        )
        vision = self.root / "docs/vision.md"
        vision.write_text(
            "Intro\n\n"
            "- `completion:v2:p2:boot-title-negative`: claim\n"
            "- `completion:v2:p2:boot-title`: claim\n",
            encoding="utf-8",
        )
        requirements = self.root / "tools/completion/requirements.toml"
        text = requirements.read_text(encoding="utf-8")
        text = text.replace(
            document["manifest"]["source_sha256"], evidence.sha256_path(vision)
        )
        text = text.replace("docs/vision.md:3", "docs/vision.md:4")
        requirements.write_text(text, encoding="utf-8")
        moved = completion.load_toml(requirements)
        evidence.validate_documentation(self.root, moved)
        self.assertEqual(self.manifest(), manifest)
        self.assertEqual(
            evidence.requirements_file_identity(
                self.root, "tools/completion/requirements.toml"
            ),
            old_identity,
        )
        self.assertEqual(
            evidence.validate_requirement(self.root, self.requirement, artifact, self.manifest()),
            ("pass", None),
        )

    def test_documentation_provenance_rejects_stale_hash_and_wrong_anchor(self) -> None:
        document = self.write_documentation_inputs()
        vision = self.root / "docs/vision.md"
        vision.write_text(
            "Intro\n"
            "- `completion:v2:p2:boot-title-negative`: claim\n"
            "- `completion:v2:p2:boot-title`: claim\n",
            encoding="utf-8",
        )
        with self.assertRaises(evidence.EvidenceError):
            evidence.validate_documentation(self.root, document)
        document = self.write_documentation_inputs(anchor="docs/vision.md:2")
        with self.assertRaises(evidence.EvidenceError):
            evidence.validate_documentation(self.root, document)

    def test_unknown_and_native_producer_comparator_corpus_dependency_changes_invalidate(self) -> None:
        self.requirement.pop("specification", None)
        document = self.write_documentation_inputs()
        baseline = self.manifest()
        self.assertEqual(baseline["schema"], 2)
        self.requirement["future_contract_field"] = "changed"
        self.assertNotEqual(self.manifest(), baseline)
        self.requirement.pop("future_contract_field")
        for field, path, value in (
            ("producer_files", "producer.py", "changed producer\n"),
            ("comparator_files", "comparator.py", "changed comparator\n"),
            ("native", "native.bin", "changed native\n"),
        ):
            original = (self.root / path).read_text(encoding="utf-8")
            (self.root / path).write_text(value, encoding="utf-8")
            self.assertNotEqual(self.manifest(), baseline, field)
            (self.root / path).write_text(original, encoding="utf-8")
        self.assertNotEqual(
            evidence.input_manifest(
                self.root, self.requirement, lane_manifest=None,
                corpus=[{"path": "reference.txt"}], dependencies=[]
            ),
            baseline,
        )
        self.assertNotEqual(
            evidence.input_manifest(
                self.root, self.requirement, lane_manifest=None, corpus=[],
                dependencies=[{"id": "completion:v2:dependency", "input_digest": "x", "payload_sha256": "y"}]
            ),
            baseline,
        )

    def test_semantic_contract_file_changes_reject_existing_evidence(self) -> None:
        self.write_documentation_inputs()
        self.requirement["producer_files"].append("tools/completion")
        manifest = self.manifest()
        artifact = self.artifact(manifest)
        path = self.root / "tools/completion/requirements.toml"
        original = path.read_text()
        for before, after in (
            ("min_frames = 1", "min_frames = 2"),
            ('state_fields = ["wram", "framebuffer"]', 'state_fields = ["wram"]'),
            ('artifact_schema = "scenario-corpus-v2"', 'artifact_schema = "new-schema"'),
            ("min_events = 1", 'min_events = 1\ndeps = ["new-dependency"]'),
            ("min_events = 1", "min_events = 1\nfuture_contract_field = true"),
        ):
            with self.subTest(change=after):
                path.write_text(original.replace(before, after))
                self.assertEqual(
                    evidence.validate_requirement(
                        self.root, self.requirement, artifact, self.manifest()
                    )[0],
                    "stale",
                )
        path.write_text(original)

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
