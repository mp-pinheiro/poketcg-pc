from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.oracle import release_gate


class ReleaseAttestationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "-q")
        for name in ("baseline.toml", "requirements.toml", "gambatte_pins.toml"):
            path = self.root / "tools/completion" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name + "\n")
        self.source = self.root / "runtime.c"
        self.source.write_text("int runtime = 1;\n")
        for name in ("gate.json", "progress.json", "history.jsonl"):
            path = self.root / "site/data" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}\n")
        self.git("add", ".")
        self.audit = {
            "complete": True,
            "counts": {
                "unclassified_bytes": 0,
                "orphan_registrations": 0,
                "final_routines": {"count": 2, "total": 2},
                "production_integration": {"roots": 1, "root_total": 1},
                "requirements": {"passing": 2, "total": 2},
                "milestone_gates": {"passing": 1, "total": 1},
                "trusted_oracle_evidence": {"count": 1, "total": 1},
            },
        }
        self.constituents = {
            name: {"status": "PASS", "returncode": 0}
            for name in (
                "package-smoke", "completion-audit", "hatches", "mutations",
                "function-gate", "lane-health", "gambatte-health", "gambatte-capture",
            )
        }

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, text=True, check=True,
        ).stdout.strip()

    def pointer(self, constituents: dict | None = None) -> dict:
        attestation = {
            "schema": 3,
            "revision": "attested-source",
            "complete": True,
            "source_tree_sha256": release_gate.source_tree_digest(self.root),
            "external": {
                name: release_gate.file_digest(self.root / "tools/completion" / filename)
                for name, filename in (
                    ("baseline", "baseline.toml"),
                    ("requirements", "requirements.toml"),
                    ("gambatte_pins", "gambatte_pins.toml"),
                )
            },
            "audit": self.audit,
            "constituents": self.constituents if constituents is None else constituents,
        }
        return {
            "schema": 3,
            "revision": "attested-source",
            "complete": True,
            "attestation": attestation,
            "attestation_sha256": hashlib.sha256(
                json.dumps(attestation, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest(),
        }

    def test_missing_constituent_cannot_attest_release(self) -> None:
        for name in (None, *self.constituents):
            with self.subTest(missing=name):
                supplied = {} if name is None else {
                    key: value for key, value in self.constituents.items() if key != name
                }
                self.assertFalse(release_gate.validate_attestation(
                    self.pointer(supplied), self.root, "attested-source",
                )[0])

    def test_missing_counts_are_not_completion(self) -> None:
        for name in (
            "final_routines", "production_integration", "requirements",
            "milestone_gates", "trusted_oracle_evidence",
        ):
            audit = copy.deepcopy(self.audit)
            audit["counts"].pop(name)
            with self.subTest(missing=name):
                self.assertFalse(release_gate.all_release_conditions(audit, self.constituents))

    def test_report_outputs_do_not_invalidate_source_attestation(self) -> None:
        pointer = self.pointer()
        self.assertEqual(release_gate.validate_attestation(
            pointer, self.root, "attested-source",
        ), (True, None))
        for name in ("gate.json", "progress.json", "history.jsonl"):
            (self.root / "site/data" / name).write_text("changed output\n")
        self.assertEqual(release_gate.validate_attestation(
            pointer, self.root, "attested-source",
        ), (True, None))
        self.source.write_text("int runtime = 2;\n")
        self.assertEqual(release_gate.validate_attestation(
            pointer, self.root, "attested-source",
        ), (False, "release attestation source tree differs"))

    def test_embedded_audit_tampering_fails_without_local_run_files(self) -> None:
        pointer = self.pointer()
        pointer["attestation"]["audit"] = {"complete": False}
        self.assertEqual(release_gate.validate_attestation(
            pointer, self.root, "attested-source",
        ), (False, "release attestation digest differs"))
