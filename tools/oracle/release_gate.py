#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.completion.evidence import (
    EvidenceError,
    requirements_file_identity,
    validate_documentation,
)
from tools.completion.revision import DERIVED_PATHS, current_source_revision
from tools.profiles import get_profile

DOCS_PATHS = ("README.md", "CHANGELOG.md")
DOCS_PREFIX = "docs/"
DOCS_SUFFIX = ".md"
ATTESTATION_SCHEMA = 4
POINTER_SCHEMA = 4
GATE_PATH = ROOT / "site" / "data" / "gate.json"
HISTORY_PATH = ROOT / "site" / "data" / "history.jsonl"
COMPLETION = ROOT / "tools" / "completion" / "completion.py"
GAMBATTE_PINS = ROOT / "tools" / "completion" / "gambatte_pins.toml"
RELEASE_SMOKE_FRAMES = 200
CONSTITUENT_TIMEOUTS = {"function-gate": 1800.0}
REQUIRED_CONSTITUENTS = frozenset({
    "package-smoke", "completion-audit", "hatches", "mutations",
    "function-gate", "lane-health", "gambatte-health", "gambatte-capture",
})


class GateError(RuntimeError):
    pass


def atomic_write(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def revision() -> str:
    return current_source_revision(ROOT)

def ensure_clean() -> None:
    try:
        result = subprocess.run(
            ["jj", "diff", "--name-only"], cwd=ROOT, capture_output=True, text=True,
            timeout=15, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GateError(f"cannot inspect working tree: {exc}") from exc
    if result.returncode != 0:
        raise GateError("working tree status failed")
    if result.stdout.strip():
        raise GateError("release gate requires a clean working tree")


def documentation_only_path(path: str) -> bool:
    return path in DOCS_PATHS or (
        path.startswith(DOCS_PREFIX) and path.endswith(DOCS_SUFFIX)
    )


def execution_tree_digest(root: Path = ROOT) -> str:
    try:
        tracked = subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, capture_output=True, timeout=30, check=False
        )
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "-z"],
            cwd=root, capture_output=True, timeout=30, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GateError(f"cannot enumerate execution tree: {exc}") from exc
    if tracked.returncode or untracked.returncode:
        raise GateError("cannot enumerate execution tree")
    paths = sorted(filter(None, tracked.stdout.split(b"\0")))
    untracked_paths = [os.fsdecode(path) for path in untracked.stdout.split(b"\0") if path]
    execution_untracked = [
        path for path in untracked_paths
        if path not in DERIVED_PATHS and not documentation_only_path(path)
    ]
    if execution_untracked:
        raise GateError("untracked execution inputs prevent release proof reuse")
    digest = hashlib.sha256()
    for raw_path in paths:
        name = os.fsdecode(raw_path)
        if name in DERIVED_PATHS or documentation_only_path(name):
            continue
        path = root / name
        try:
            metadata = path.lstat()
            if path.is_symlink():
                content = runtime_file_digest(path).encode()
                mode = b"symlink"
            else:
                content = path.read_bytes()
                mode = str(metadata.st_mode & 0o111).encode()
        except OSError as exc:
            raise GateError(f"cannot read tracked path {path}: {exc}") from exc
        if name == "tools/completion/requirements.toml":
            try:
                content = requirements_file_identity(root, name)["contract_sha256"].encode()
            except (EvidenceError, KeyError, TypeError) as exc:
                raise GateError(f"cannot identify requirements contract: {exc}") from exc
        digest.update(raw_path)
        digest.update(b"\0")
        digest.update(mode)
        digest.update(b"\0")
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def source_tree_digest(root: Path = ROOT) -> str:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, capture_output=True, timeout=30, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GateError(f"cannot enumerate committed source tree: {exc}") from exc
    if result.returncode:
        raise GateError("cannot enumerate committed source tree")
    digest = hashlib.sha256()
    for raw_path in sorted(filter(None, result.stdout.split(b"\0"))):
        if os.fsdecode(raw_path) in DERIVED_PATHS:
            continue
        path = root / os.fsdecode(raw_path)
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise GateError(f"cannot read committed path {path}: {exc}") from exc
        digest.update(raw_path)
        digest.update(b"\0")
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()

def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
    except OSError:
        return "missing"
    return digest.hexdigest()


def runtime_file_digest(path: Path) -> str:
    content = file_digest(path)
    if content == "missing":
        return content
    try:
        identity = {
            "sha256": content,
            "executable": path.stat().st_mode & 0o111,
            "symlink": os.readlink(path) if path.is_symlink() else None,
        }
    except OSError:
        return "missing"
    return hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()


def directory_digest(path: Path) -> str:
    if not path.is_dir():
        return "missing"
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if "__pycache__" in item.parts or item.suffix == ".pyc":
            continue
        relative = item.relative_to(path).as_posix().encode()
        metadata = item.lstat()
        if item.is_symlink():
            content = runtime_file_digest(item).encode()
            kind = b"symlink"
        elif item.is_file():
            content = item.read_bytes()
            kind = b"file:" + str(metadata.st_mode & 0o111).encode()
        elif item.is_dir():
            content = b""
            kind = b"dir:" + str(metadata.st_mode & 0o111).encode()
        else:
            continue
        digest.update(relative)
        digest.update(b"\0")
        digest.update(kind)
        digest.update(b"\0")
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def external_identity(args: argparse.Namespace) -> dict[str, str]:
    from tools.completion import gambatte_runner

    profile = get_profile(os.environ.get("POKETCG_PROFILE"), ROOT)
    try:
        pins = gambatte_runner.load_pins()
    except gambatte_runner.GambatteError as exc:
        raise GateError(f"cannot identify Gambatte runtime: {exc}") from exc
    core = pins.get("core")
    if not isinstance(core, dict) or not isinstance(core.get("path"), str) or not core["path"]:
        raise GateError("Gambatte core pin has no runtime path")
    core_path = gambatte_runner.resolve(core["path"])
    boot = pins.get("boot", {})
    boot_path = (
        gambatte_runner.resolve(str(boot.get("path", "")))
        if boot.get("mode") == "bios" else None
    )
    paths = {
        "baseline": ROOT / "tools/completion/baseline.toml",
        "requirements": ROOT / "tools/completion/requirements.toml",
        "gambatte_pins": gambatte_runner.PINS_PATH,
        "rom": args.rom or profile.rom_path(ROOT),
        "symbols": args.symbols or profile.sym_path(ROOT),
        "binary": args.binary or profile.binary_path(ROOT),
        "data_pack": args.data_pack or profile.data_pack_path(ROOT),
        "profile_map": profile.map_path(ROOT),
        "profile_symbols": profile.sym_path(ROOT),
        "profile_rom": profile.rom_path(ROOT),
        "pack_manifest": profile.artifact_path("pack_manifest", ROOT),
        "probe": profile.probe_path(ROOT),
        "package_binary": ROOT / "build/poketcg",
        "package_data_pack": ROOT / "build/completion/data-pack.bin",
        "package_pack_manifest": ROOT / "build/completion/data-pack.json",
        "completion_map": ROOT / "poketcg/poketcg.map",
        "completion_symbols": ROOT / "poketcg/poketcg.sym",
        "barrier_probe": ROOT / "build-barrier/poketcg_probe",
        "health_rom": ROOT / "poketcg/poketcg.gbc",
        "gbref_runner": ROOT / "tools/oracle/gbref/build/gbref_runner",
        "gambatte_core": core_path,
        "gambatte_source": gambatte_runner.resolve(pins["source"]["path"]),
        "gambatte_rom": gambatte_runner.resolve(pins["rom"]["path"]),
        "python": Path(sys.executable),
    }
    result: dict[str, str] = {}
    for name, path in paths.items():
        if name == "requirements":
            try:
                result[name] = requirements_file_identity(ROOT, path)["contract_sha256"]
            except (EvidenceError, KeyError, TypeError):
                result[name] = "missing"
        else:
            result[name] = (
                file_digest(Path(path)) if name in {"baseline", "gambatte_pins"}
                else runtime_file_digest(Path(path))
            )
    result["gambatte_boot"] = runtime_file_digest(boot_path) if boot_path is not None else "not-required"
    runtime = Path(os.environ.get(
        "GBRT_RUNTIME_DIR", str(Path.home() / ".local/gbrecomp/gb-recompiled-linux/runtime")
    ))
    result["gbrt_runtime_tree"] = directory_digest(runtime)
    result["case_corpus"] = directory_digest(profile.case_path(ROOT))
    result["generated_headers"] = directory_digest(
        profile.build_path(ROOT) / "generated" / profile.name / "generated"
    )
    result["oracle_b"] = runtime_file_digest(Path(os.environ.get(
        "POKETCG_ORACLEB", str(Path.home() / ".local/share/gbrecompiled/poketcg/poketcg")
    )))
    result["python_version"] = hashlib.sha256(sys.version.encode()).hexdigest()
    profile_inputs = {
        "profile": profile.as_dict(),
        "variant": profile.variant,
        "case_path": os.environ.get("POKETCG_CASE_PATH"),
        "build": os.environ.get("POKETCG_BUILD"),
        "profile_variant": os.environ.get("POKETCG_PROFILE_VARIANT"),
        "gbrt_runtime_dir": os.environ.get("GBRT_RUNTIME_DIR"),
        "oracle_b": os.environ.get("POKETCG_ORACLEB"),
    }
    result["profile"] = hashlib.sha256(
        json.dumps(profile_inputs, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return result


def content_key(revision_id: str, tree: str, external: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for name, value in (("revision", revision_id), ("tree", tree), *sorted(external.items())):
        digest.update(name.encode())
        digest.update(b"\0")
        digest.update(value.encode())
        digest.update(b"\0")
    return digest.hexdigest()[:32]


def run_constituent(
    name: str, command: list[str], log_path: Path, timeout: float,
) -> dict[str, Any]:
    started = time.monotonic()
    environment = os.environ.copy()
    if name == "completion-audit":
        environment["POKETCG_RELEASE_GATE_IN_FLIGHT"] = "1"
        environment["POKETCG_CFG_TRACE"] = str(log_path.parent / "production-trace.json")
    try:
        completed = subprocess.run(
            command, cwd=ROOT, env=environment, capture_output=True, text=True,
            timeout=timeout, check=False
        )
        output = completed.stdout + ("\n" + completed.stderr if completed.stderr else "")
        log_path.write_text(output, encoding="utf-8")
        status = "PASS" if completed.returncode == 0 else "FAIL"
        return {
            "status": status,
            "returncode": completed.returncode,
            "duration": round(time.monotonic() - started, 3),
            "log": str(log_path.relative_to(ROOT)),
        }
    except subprocess.TimeoutExpired as exc:
        log_path.write_text(str(exc), encoding="utf-8")
        return {
            "status": "TIMEOUT",
            "returncode": None,
            "duration": round(time.monotonic() - started, 3),
            "log": str(log_path.relative_to(ROOT)),
        }
    except OSError as exc:
        log_path.write_text(str(exc), encoding="utf-8")
        return {
            "status": "UNAVAILABLE",
            "returncode": None,
            "duration": round(time.monotonic() - started, 3),
            "log": str(log_path.relative_to(ROOT)),
        }


def parse_json_log(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    decoder = json.JSONDecoder()
    for index in range(len(text)):
        if text[index] != "{":
            continue
        try:
            value, end = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if end and isinstance(value, dict):
            return value
    return None


def all_release_conditions(
    audit_report: dict[str, Any] | None,
    constituents: dict[str, dict[str, Any]],
) -> bool:
    if not isinstance(audit_report, dict) or audit_report.get("complete") is not True:
        return False
    counts = audit_report.get("counts")
    if not isinstance(counts, dict):
        return False
    if counts.get("unclassified_bytes") != 0 or counts.get("orphan_registrations") != 0:
        return False
    registry = audit_report.get("routine_registry")
    if (
        not isinstance(registry, dict)
        or not registry
        or not all(isinstance(stem, str) and stem for stem in registry)
        or not all(
            isinstance(names, list) and names
            and all(isinstance(name, str) and name for name in names)
            for names in registry.values()
        )
    ):
        return False
    registered = [name for names in registry.values() for name in names]
    mapping = audit_report.get("mapping")
    if (
        len(set(registered)) != len(registered)
        or not isinstance(mapping, dict)
        or type(mapping.get("registrations")) is not int
        or mapping["registrations"] != len(registered)
    ):
        return False
    final_routines = counts.get("final_routines")
    if (
        not isinstance(final_routines, dict)
        or len({name.split(".", 1)[0] for name in registered})
        != final_routines.get("total")
    ):
        return False
    for field, count_name in (("requirements", "requirements"), ("milestones", "milestone_gates")):
        rows = audit_report.get(field)
        count = counts.get(count_name)
        if not isinstance(rows, dict) or not isinstance(count, dict) or count.get("total") != len(rows):
            return False
        if field == "requirements":
            if count.get("remaining") != 0 or not all(
                isinstance(row, dict) and row.get("status") == "pass" for row in rows.values()
            ):
                return False
        elif not all(value is True for value in rows.values()):
            return False
    for name, numerator, denominator in (
        ("final_routines", "count", "total"),
        ("production_integration", "roots", "root_total"),
        ("requirements", "passing", "total"),
        ("milestone_gates", "passing", "total"),
        ("trusted_oracle_evidence", "count", "total"),
    ):
        row = counts.get(name)
        if not isinstance(row, dict):
            return False
        total = row.get(denominator)
        count = row.get(numerator)
        if type(total) is not int or type(count) is not int or total <= 0 or count != total:
            return False
    return isinstance(constituents, dict) and set(constituents) == REQUIRED_CONSTITUENTS and all(
        isinstance(item, dict) and item.get("status") == "PASS" and item.get("returncode") == 0
        for item in constituents.values()
    )


def validate_attestation(
    pointer: dict[str, Any],
    root: Path,
    expected_revision: str,
) -> tuple[bool, str | None]:
    root = root.resolve()
    if not isinstance(pointer, dict) or pointer.get("schema") != POINTER_SCHEMA:
        return False, "release pointer schema differs"
    if pointer.get("complete") is not True:
        return False, "release pointer is incomplete"
    attestation = pointer.get("attestation")
    digest = pointer.get("attestation_sha256")
    if not isinstance(attestation, dict) or not isinstance(digest, str):
        return False, "release pointer lacks attestation identity"
    material = json.dumps(attestation, sort_keys=True, separators=(",", ":"))
    if hashlib.sha256(material.encode()).hexdigest() != digest:
        return False, "release attestation digest differs"
    if attestation.get("schema") != ATTESTATION_SCHEMA:
        return False, "release attestation schema differs"
    if attestation.get("complete") is not True:
        return False, "release attestation is incomplete"
    measured_revision = attestation.get("revision")
    if not isinstance(measured_revision, str) or not measured_revision.strip():
        return False, "release attestation revision is malformed"
    if pointer.get("revision") != measured_revision:
        return False, "release pointer and attestation revisions differ"
    if attestation.get("proof_inputs_stable") is not True:
        return False, "release attestation inputs were not stable during measurement"
    source_digest = attestation.get("source_tree_sha256")
    if not isinstance(source_digest, str) or len(source_digest) != 64 or any(
        char not in "0123456789abcdef" for char in source_digest
    ):
        return False, "release attestation source tree identity is malformed"
    try:
        validate_documentation(root)
        if attestation.get("execution_tree_sha256") != execution_tree_digest(root):
            return False, "release attestation execution tree differs"
    except (GateError, EvidenceError, OSError, ValueError) as exc:
        return False, str(exc)
    if measured_revision == expected_revision:
        if attestation.get("source_tree_sha256") != source_tree_digest(root):
            return False, "release attestation source tree differs"
    external = attestation.get("external")
    if not isinstance(external, dict):
        return False, "release attestation external identity is malformed"
    paths = {
        "baseline": root / "tools/completion/baseline.toml",
        "requirements": root / "tools/completion/requirements.toml",
        "gambatte_pins": root / "tools/completion/gambatte_pins.toml",
    }
    try:
        identities = {
            "baseline": file_digest(paths["baseline"]),
            "requirements": requirements_file_identity(root, paths["requirements"])["contract_sha256"],
            "gambatte_pins": file_digest(paths["gambatte_pins"]),
        }
        document = tomllib.loads(paths["requirements"].read_text())
        declared_requirements = {row["id"] for row in document["requirement"]}
        declared_milestones = set(document["manifest"]["milestones"])
    except (EvidenceError, KeyError, TypeError, OSError, ValueError) as exc:
        return False, str(exc)
    for name, value in identities.items():
        if external.get(name) != value:
            return False, f"release attestation external identity differs: {name}"
    constituents = attestation.get("constituents")
    if not all_release_conditions(attestation.get("audit"), constituents):
        return False, "release conditions are not met"
    audit = attestation["audit"]
    if set(audit["requirements"]) != declared_requirements or set(audit["milestones"]) != declared_milestones:
        return False, "release attestation does not cover the declared requirements and milestones"
    return True, None


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--rom", type=Path)
    result.add_argument("--symbols", type=Path)
    result.add_argument("--binary", type=Path)
    result.add_argument("--data-pack", type=Path)
    result.add_argument("--timeout", type=float, default=180.0)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        ensure_clean()
        revision_id = revision()
        source_tree = source_tree_digest(ROOT)
        tree = execution_tree_digest(ROOT)
        external = external_identity(args)
        key = content_key(revision_id, tree, external)
        try:
            prior = json.loads(GATE_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            prior = None
        if isinstance(prior, dict):
            valid, _ = validate_attestation(prior, ROOT, revision_id)
            attestation = prior.get("attestation")
            local_runtime_ready = all(value not in (None, "missing") for value in external.values())
            if (
                valid and local_runtime_ready and isinstance(attestation, dict)
                and attestation.get("external") == external
            ):
                print(json.dumps({
                    "status": "PASS",
                    "complete": True,
                    "reused": True,
                    "measured_revision": attestation["revision"],
                    "validated_revision": revision_id,
                    "content_key": prior.get("content_key"),
                    "attestation_sha256": prior["attestation_sha256"],
                }, sort_keys=True))
                return 0
        run_base = ROOT / "build" / "completion" / "runs" / key
        run_base.mkdir(parents=True, exist_ok=True)
        run_dir = run_base / f"{int(time.time())}-{os.getpid()}"
        run_dir.mkdir()
        constituents: dict[str, dict[str, Any]] = {}
        package_command = [
            sys.executable, str(ROOT / "tools/completion/package_smoke.py"),
            "--package", str(run_dir / "package"),
        ]
        if args.binary:
            package_command.extend(["--binary", str(args.binary)])
        if args.data_pack:
            package_command.extend(["--pack", str(args.data_pack)])
        gambatte_capture_command = [
            sys.executable,
            str(ROOT / "tools/completion/gambatte_runner.py"),
            "capture",
            "release-smoke",
            "--frames",
            str(RELEASE_SMOKE_FRAMES),
            "--output",
            str(run_dir / "gambatte-smoke.json"),
            "--import-output",
            str(run_dir / "gambatte-smoke.imported.json"),
        ]
        commands = {
            "completion-audit": [sys.executable, str(COMPLETION), "audit"],
            "package-smoke": package_command,
            "hatches": [sys.executable, str(ROOT / "tools/audit_hatches.py"), "--stage", "release"],
            "mutations": [sys.executable, str(ROOT / "tools/audit_mutations.py"), "--stage", "release"],
            "function-gate": ["just", "oracle-fn-gate"],
            "lane-health": ["just", "completion-lanes-health"],
            "gambatte-health": ["just", "completion-gambatte-health"],
            "gambatte-capture": gambatte_capture_command,
        }
        for name, command in commands.items():
            constituents[name] = run_constituent(
                name, command, run_dir / f"{name}.log",
                max(args.timeout, CONSTITUENT_TIMEOUTS.get(name, 0.0)),
            )
            if constituents[name].get("status") != "PASS":
                break
        audit_report = parse_json_log(run_dir / "completion-audit.log")
        try:
            proof_inputs_stable = (
                execution_tree_digest(ROOT) == tree and external_identity(args) == external
            )
            validate_documentation(ROOT)
        except (EvidenceError, GateError, OSError, ValueError):
            proof_inputs_stable = False
        summary = {
            "schema": ATTESTATION_SCHEMA,
            "revision": revision_id,
            "source_tree_sha256": source_tree,
            "execution_tree_sha256": tree,
            "proof_inputs_stable": proof_inputs_stable,
            "content_key": key,
            "external": external,
            "constituents": constituents,
            "audit": audit_report or {},
        }
        complete = proof_inputs_stable and all_release_conditions(audit_report, constituents)
        canonical = dict(summary)
        canonical["complete"] = complete
        attestation_material = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
        attestation_digest = hashlib.sha256(attestation_material.encode()).hexdigest()
        (run_dir / "attestation.json").write_text(attestation_material + "\n", encoding="utf-8")
        pointer = {
            "schema": POINTER_SCHEMA,
            "complete": complete,
            "content_key": key,
            "attestation_sha256": attestation_digest,
            "attestation": canonical,
            "run_dir": str(run_dir.relative_to(ROOT)),
            "revision": revision_id,
            "validated_revision": revision_id,
            "constituents": constituents,
            "counts": (audit_report or {}).get("counts", {}),
        }
        atomic_write(GATE_PATH, json.dumps(pointer, sort_keys=True, separators=(",", ":")) + "\n")
        history = {name: value for name, value in pointer.items() if name != "attestation"}
        history["timestamp"] = int(time.time())
        with HISTORY_PATH.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(history, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        print(json.dumps({
            "status": "PASS" if complete else "INCOMPLETE",
            "complete": complete,
            "content_key": key,
            "attestation_sha256": attestation_digest,
            "run_dir": str(run_dir.relative_to(ROOT)),
        }, sort_keys=True))
        return 0 if complete else 2
    except GateError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
