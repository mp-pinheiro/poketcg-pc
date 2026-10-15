from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.oracle import release_gate


class ReleaseAttestationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "-q")
        for name in ("baseline.toml", "gambatte_pins.toml"):
            path = self.root / "tools/completion" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name + "\n")
        self.source = self.root / "runtime.c"
        self.source.write_text("int runtime = 1;\n")
        docs = self.root / "docs"
        docs.mkdir()
        self.vision = docs / "vision.md"
        self.vision.write_text("# `completion:v2:p1:test`\n")
        (self.root / "tools/completion/requirements.toml").write_text(
            '[manifest]\nschema = 2\nmilestones = ["test"]\nsource = "docs/vision.md"\n'
            f'source_sha256 = "{hashlib.sha256(self.vision.read_bytes()).hexdigest()}"\n'
            '\n[[requirement]]\nid = "completion:v2:p1:test"\nanchor = "docs/vision.md:1"\n'
        )
        self.git("add", ".")
        subprocess.run(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
             "commit", "-q", "-m", "fixture"],
            cwd=self.root, capture_output=True, text=True, check=True,
        )
        self.audit = {
            "complete": True,
            "routine_registry": {"sample": ["One", "Two"]},
            "mapping": {"registrations": 2},
            "requirements": {"completion:v2:p1:test": {"status": "pass"}},
            "milestones": {"test": True},
            "counts": {
                "unclassified_bytes": 0, "orphan_registrations": 0,
                "final_routines": {"count": 2, "total": 2},
                "production_integration": {"roots": 1, "root_total": 1},
                "requirements": {"passing": 1, "total": 1, "remaining": 0},
                "milestone_gates": {"passing": 1, "total": 1},
                "trusted_oracle_evidence": {"count": 1, "total": 1},
            },
        }
        self.constituents = {
            name: {"status": "PASS", "returncode": 0}
            for name in release_gate.REQUIRED_CONSTITUENTS
        }

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, text=True, check=True,
        ).stdout.strip()

    def pointer(self, *, revision: str = "attested-source", constituents: dict | None = None) -> dict:
        external = {
            "baseline": release_gate.file_digest(self.root / "tools/completion/baseline.toml"),
            "requirements": release_gate.requirements_file_identity(
                self.root, "tools/completion/requirements.toml"
            )["contract_sha256"],
            "gambatte_pins": release_gate.file_digest(
                self.root / "tools/completion/gambatte_pins.toml"
            ),
        }
        attestation = {
            "schema": 4,
            "revision": revision,
            "complete": True,
            "proof_inputs_stable": True,
            "source_tree_sha256": release_gate.source_tree_digest(self.root),
            "execution_tree_sha256": release_gate.execution_tree_digest(self.root),
            "external": external,
            "audit": self.audit,
            "constituents": self.constituents if constituents is None else constituents,
        }
        pointer = {
            "schema": 4, "revision": revision, "validated_revision": revision,
            "complete": True, "attestation": attestation,
        }
        pointer["attestation_sha256"] = hashlib.sha256(
            json.dumps(attestation, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return pointer

    def test_docs_only_cross_revision_validation_needs_no_run_files(self) -> None:
        pointer = self.pointer()
        self.vision.write_text("# `completion:v2:p1:test`\nUpdated prose.\n")
        manifest = self.root / "tools/completion/requirements.toml"
        text = manifest.read_text()
        text = text.replace(
            hashlib.sha256(b"# `completion:v2:p1:test`\n").hexdigest(),
            hashlib.sha256(self.vision.read_bytes()).hexdigest(),
        )
        manifest.write_text(text)
        self.git("add", ".")
        self.assertEqual(release_gate.validate_attestation(
            pointer, self.root, "new-documentation-revision",
        ), (True, None))

    def test_execution_inputs_and_non_allowlisted_markdown_invalidate(self) -> None:
        pointer = self.pointer(revision="current")
        for path, contents in (
            ("runtime.c", "int runtime = 2;\n"),
            ("tests/case.json", "{}\n"),
            ("tools/config.toml", "acceptance = false\n"),
            ("tools/completion/gambatte_pins.toml", "changed\n"),
            ("AGENTS.md", "changed instructions\n"),
            ("notes/other.md", "changed markdown\n"),
        ):
            with self.subTest(path=path):
                fresh = copy.deepcopy(pointer)
                target = self.root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(contents)
                self.git("add", ".")
                self.assertFalse(release_gate.validate_attestation(
                    fresh, self.root, "current",
                )[0])
                self.git("reset", "--hard", "HEAD")
                self.git("clean", "-fd")
    def test_semantic_requirement_change_invalidates(self) -> None:
        pointer = self.pointer(revision="current")
        path = self.root / "tools/completion/requirements.toml"
        path.write_text(path.read_text() + 'acceptance_rule = "changed"\n')
        self.git("add", ".")
        self.assertFalse(release_gate.validate_attestation(pointer, self.root, "current")[0])
    def test_registration_provenance_must_match_audit_counts(self) -> None:
        for edit in (
            lambda audit: audit["routine_registry"]["sample"].append("One"),
            lambda audit: audit["routine_registry"]["sample"].__setitem__(1, "One"),
            lambda audit: audit["routine_registry"]["sample"].__setitem__(1, "One.Sub"),
            lambda audit: audit["mapping"].__setitem__("registrations", 3),
        ):
            audit = copy.deepcopy(self.audit)
            edit(audit)
            self.assertFalse(
                release_gate.all_release_conditions(audit, self.constituents)
            )


    def test_attestation_schema_and_empty_revision_are_rejected(self) -> None:
        for schema, measured_revision in ((3, "current"), (4, "")):
            with self.subTest(schema=schema, measured_revision=measured_revision):
                pointer = self.pointer(revision=measured_revision)
                pointer["attestation"]["schema"] = schema
                pointer["attestation_sha256"] = hashlib.sha256(
                    json.dumps(pointer["attestation"], sort_keys=True,
                               separators=(",", ":")).encode()
                ).hexdigest()
                self.assertFalse(
                    release_gate.validate_attestation(pointer, self.root, "current")[0]
                )

    def test_untracked_execution_input_rejected(self) -> None:
        (self.root / "new_case.json").write_text("{}")
        with self.assertRaises(release_gate.GateError):
            release_gate.execution_tree_digest(self.root)

    def test_incomplete_receipts_and_tampering_fail(self) -> None:
        pointer = self.pointer(revision="current")
        self.assertEqual(
            release_gate.validate_attestation(pointer, self.root, "current"),
            (True, None),
        )
        pointer["complete"] = False
        self.assertFalse(release_gate.validate_attestation(pointer, self.root, "current")[0])
        pointer = self.pointer(revision="current")
        pointer["attestation"]["complete"] = False
        pointer["attestation_sha256"] = hashlib.sha256(
            json.dumps(pointer["attestation"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertFalse(release_gate.validate_attestation(pointer, self.root, "current")[0])
        pointer = self.pointer(revision="current")
        pointer["attestation"]["audit"] = {"complete": False}
        self.assertFalse(release_gate.validate_attestation(pointer, self.root, "current")[0])
        pointer = self.pointer(revision="current")
        pointer["attestation"]["constituents"].pop("hatches")
        pointer["attestation_sha256"] = hashlib.sha256(
            json.dumps(pointer["attestation"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertFalse(release_gate.validate_attestation(pointer, self.root, "current")[0])
        pointer = self.pointer(revision="current")
        pointer["attestation"]["constituents"]["hatches"] = {
            "status": "FAIL", "returncode": 1,
        }
        pointer["attestation_sha256"] = hashlib.sha256(
            json.dumps(pointer["attestation"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        self.assertFalse(release_gate.validate_attestation(pointer, self.root, "current")[0])
    def test_gate_reuse_returns_provenance_without_runner_side_effects(self) -> None:
        pointer = self.pointer(revision="current")
        external = pointer["attestation"]["external"]
        runtime_names = (
            "rom", "symbols", "binary", "data_pack", "probe", "package_binary",
            "package_data_pack", "barrier_probe", "health_rom", "gbref_runner",
            "gambatte_core", "gambatte_boot", "python", "gbrt_runtime_tree", "oracle_b",
            "python_version", "profile",
        )
        external.update({name: hashlib.sha256(name.encode()).hexdigest() for name in runtime_names})
        pointer["attestation"]["external"] = external
        pointer["attestation_sha256"] = hashlib.sha256(
            json.dumps(pointer["attestation"], sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        pointer["validated_revision"] = "old-validation"
        gate_path = self.root / "site/data/gate.json"
        gate_path.parent.mkdir(parents=True, exist_ok=True)
        gate_path.write_text(json.dumps(pointer))
        marker = self.root / "runner-fired"

        def runner(*args, **kwargs):
            marker.write_text("ran")
            return {"status": "PASS", "returncode": 0}

        output = io.StringIO()
        with (
            patch.object(release_gate, "ROOT", self.root),
            patch.object(release_gate, "GATE_PATH", gate_path),
            patch.object(release_gate, "ensure_clean"),
            patch.object(release_gate, "revision", return_value="current"),
            patch.object(release_gate, "external_identity", return_value=external),
            patch.object(release_gate, "run_constituent", side_effect=runner),
            contextlib.redirect_stdout(output),
        ):
            status = release_gate.main([])
        result = json.loads(output.getvalue())
        self.assertEqual(status, 0, result)
        self.assertTrue(result["reused"])
        self.assertEqual(result["measured_revision"], "current")
        self.assertEqual(result["validated_revision"], "current")
        self.assertFalse(marker.exists())

    def test_changed_symlink_target_invalidates_cross_revision_proof(self) -> None:
        target = self.root / "build/runtime.c"
        target.parent.mkdir()
        target.write_text("int runtime = 1;\n")
        (self.root / ".gitignore").write_text("build/\n")
        self.source.unlink()
        self.source.symlink_to("build/runtime.c")
        self.git("add", ".")
        pointer = self.pointer()
        self.assertEqual(
            release_gate.validate_attestation(pointer, self.root, "docs-only"), (True, None)
        )
        target.write_text("int runtime = 2;\n")
        self.assertFalse(release_gate.validate_attestation(pointer, self.root, "docs-only")[0])

    def test_private_runtime_executable_mode_and_case_contents_change_identity(self) -> None:
        runtime = self.root / "private-runtime"
        runtime.write_text("executable\n")
        runtime.chmod(0o755)
        before = release_gate.runtime_file_digest(runtime)
        runtime.chmod(0o644)
        self.assertNotEqual(release_gate.runtime_file_digest(runtime), before)
        cases = self.root / "private-cases"
        cases.mkdir()
        case = cases / "case.py"
        case.write_text("CASES = {'routine': [1]}\n")
        before = release_gate.directory_digest(cases)
        case.write_text("CASES = {'routine': [2]}\n")
        self.assertNotEqual(release_gate.directory_digest(cases), before)

    def test_receipt_requirement_rows_must_match_declared_scope(self) -> None:
        pointer = self.pointer(revision="current")
        self.assertEqual(release_gate.validate_attestation(pointer, self.root, "current"), (True, None))
        for rows in (
            {"completion:v2:p1:wrong": {"status": "pass"}},
            {"completion:v2:p1:test": {"status": "failing"}},
            {},
        ):
            with self.subTest(rows=rows):
                altered = copy.deepcopy(pointer)
                altered["attestation"]["audit"]["requirements"] = rows
                altered["attestation_sha256"] = hashlib.sha256(
                    json.dumps(altered["attestation"], sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest()
                self.assertFalse(
                    release_gate.validate_attestation(altered, self.root, "current")[0]
                )
