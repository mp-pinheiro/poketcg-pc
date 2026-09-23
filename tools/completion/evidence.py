from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any


class EvidenceError(ValueError):
    pass


def _canonical(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise EvidenceError("canonical objects require string keys")
        return {key: _canonical(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical(item) for item in value]
    if isinstance(value, (set, frozenset)):
        items = [_canonical(item) for item in value]
        return sorted(items, key=lambda item: canonical_bytes(item))
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise EvidenceError(f"cannot canonicalize {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            _canonical(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise EvidenceError(f"invalid canonical JSON: {exc}") from exc


def canonical_digest(value: dict[str, Any]) -> str:
    if not isinstance(value, dict):
        raise EvidenceError("canonical digest requires an object")
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
    except OSError as exc:
        raise EvidenceError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def repository_path(root: Path, path: str | Path) -> tuple[Path, str]:
    root = root.resolve()
    candidate = Path(path)
    resolved = (
        candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    )
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise EvidenceError(f"path is outside repository: {path}") from exc
    return resolved, relative.as_posix()


def file_identity(root: Path, path: str | Path) -> dict[str, str]:
    resolved, relative = repository_path(root, path)
    if not resolved.is_file():
        raise EvidenceError(f"missing evidence input: {relative}")
    return {"path": relative, "sha256": sha256_path(resolved)}


def _declared_child(path: Path) -> bool:
    return (
        path.is_file()
        and "__pycache__" not in path.parts
        and ".venv" not in path.parts
        and "build" not in path.parts
        and path.suffix != ".pyc"
    )


def _declared_files(root: Path, values: Any) -> list[dict[str, str]]:
    if values is None:
        values = ["tools/completion"]
    if not isinstance(values, list):
        raise EvidenceError("declared files must be a list")
    paths: dict[str, Path] = {}
    for value in values:
        if isinstance(value, str):
            candidate, relative = repository_path(root, value)
            if candidate.is_file():
                paths[relative] = candidate
            elif candidate.is_dir():
                for child in sorted(
                    item for item in candidate.rglob("*") if _declared_child(item)
                ):
                    child_relative = child.relative_to(root).as_posix()
                    paths[child_relative] = child
            else:
                raise EvidenceError(f"missing declared input: {relative}")
            continue
        if not isinstance(value, dict):
            raise EvidenceError("declared file entry is malformed")
        path = value.get("path", value.get("tree"))
        if not isinstance(path, str):
            raise EvidenceError("declared file entry has no path")
        candidate, relative = repository_path(root, path)
        tree = bool(value.get("tree"))
        if candidate.is_file() and not tree:
            paths[relative] = candidate
        elif candidate.is_dir():
            for child in sorted(
                item for item in candidate.rglob("*") if _declared_child(item)
            ):
                child_relative = child.relative_to(root).as_posix()
                paths[child_relative] = child
        else:
            raise EvidenceError(f"missing declared input: {relative}")
    return [
        {"path": relative, "sha256": sha256_path(path)}
        for relative, path in sorted(paths.items())
    ]


def _load_toml(path: Path) -> dict[str, Any]:
    import tomllib

    try:
        with path.open("rb") as stream:
            value = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise EvidenceError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvidenceError(f"{path} is not an object")
    return value


def _specification(root: Path, requirement: dict[str, Any]) -> dict[str, Any]:
    supplied = requirement.get("specification")
    if supplied is not None:
        if not isinstance(supplied, dict):
            raise EvidenceError("requirement specification is malformed")
        return _canonical(supplied)
    baseline_path = root / "tools" / "completion" / "baseline.toml"
    manifest_path = root / "tools" / "completion" / "requirements.toml"
    vision_path = root / "docs" / "vision.md"
    baseline = _load_toml(baseline_path).get("baseline")
    manifest = _load_toml(manifest_path).get("manifest")
    if not isinstance(baseline, dict) or not isinstance(manifest, dict):
        raise EvidenceError("baseline or manifest table is malformed")
    if not vision_path.is_file():
        raise EvidenceError("missing normative vision source")
    return {
        "requirement": {
            key: _canonical(value)
            for key, value in requirement.items()
            if key
            not in {
                "producer_files",
                "comparator_files",
                "runtime",
                "native",
                "reference",
                "corpus",
                "dependencies",
            }
        },
        "baseline": _canonical(baseline),
        "manifest": _canonical(manifest),
        "vision": {"path": "docs/vision.md", "sha256": sha256_path(vision_path)},
    }


def _runtime_identity(requirement: dict[str, Any]) -> dict[str, Any]:
    configured = requirement.get("runtime", {})
    if configured is None:
        configured = {}
    if not isinstance(configured, dict):
        raise EvidenceError("runtime identity is malformed")
    environment = configured.get("environment", {})
    if environment is None:
        environment = {}
    if not isinstance(environment, dict):
        raise EvidenceError("runtime environment is malformed")
    values: dict[str, Any] = {}
    for key, value in sorted(environment.items()):
        if not isinstance(key, str):
            raise EvidenceError("runtime environment key is malformed")
        if key.casefold() in {"token", "password", "secret", "credential"} or any(
            forbidden in key.casefold()
            for forbidden in ("token", "password", "secret", "credential")
        ):
            raise EvidenceError(f"credential-like environment key is forbidden: {key}")
        if value is True:
            values[key] = os.environ.get(key)
        elif value is False or value is None:
            continue
        else:
            values[key] = value
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": sys.platform,
        "build_flags": configured.get("build_flags", {}),
        "comparison_masks": configured.get("comparison_masks", {}),
        "seeds": configured.get("seeds", []),
        "environment": values,
    }


def _native_identity(
    root: Path, requirement: dict[str, Any], lane_manifest: dict[str, Any] | None
) -> dict[str, Any]:
    if lane_manifest is not None:
        if not isinstance(lane_manifest, dict):
            raise EvidenceError("lane manifest is malformed")
        return _canonical(lane_manifest)
    configured = requirement.get("native", {})
    if configured is None:
        configured = {}
    if not isinstance(configured, dict):
        raise EvidenceError("native identity is malformed")
    if "files" in configured:
        files = configured["files"]
    else:
        files = ["build/poketcg", "build/completion/data-pack.bin"]
    if not isinstance(files, list):
        raise EvidenceError("native files are malformed")
    return {
        "files": _declared_files(root, files) if files else [],
        "probe": _canonical(configured.get("probe", {})),
        "pack": _canonical(configured.get("pack", {})),
    }


def _reference_identity(root: Path, requirement: dict[str, Any]) -> dict[str, Any]:
    configured = requirement.get("reference", {})
    if configured is None:
        configured = {}
    if not isinstance(configured, dict):
        raise EvidenceError("reference identity is malformed")
    files = configured.get("files", ["tools/completion/gambatte_pins.toml"])
    return {
        "files": _declared_files(root, files),
        "stream_key": _canonical(configured.get("stream_key", {})),
        "sync": _canonical(configured.get("sync", {})),
        "core": _canonical(configured.get("core", {})),
    }


def _corpus_identity(root: Path, corpus: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(corpus, list) or not all(
        isinstance(entry, dict) for entry in corpus
    ):
        raise EvidenceError("corpus must be a list of objects")
    rows: list[dict[str, Any]] = []
    for entry in corpus:
        row = _canonical(entry)
        for field in ("input", "save", "pokes", "path"):
            value = row.get(field)
            if isinstance(value, str):
                candidate, relative = repository_path(root, value)
                row[field] = relative
                if candidate.is_file():
                    row[f"{field}_sha256"] = sha256_path(candidate)
        rows.append(row)
    return rows


def _dependency_identity(dependencies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not isinstance(dependencies, list) or not all(
        isinstance(entry, dict) for entry in dependencies
    ):
        raise EvidenceError("dependencies must be a list of objects")
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in dependencies:
        requirement_id = entry.get("id", entry.get("requirement_id"))
        input_digest = entry.get("input_digest")
        payload_sha256 = entry.get("payload_sha256")
        if not all(
            isinstance(value, str) and value
            for value in (requirement_id, input_digest, payload_sha256)
        ):
            raise EvidenceError(
                "dependency requires id, input_digest, and payload_sha256"
            )
        if requirement_id in seen:
            raise EvidenceError(f"dependency repeats: {requirement_id}")
        seen.add(requirement_id)
        rows.append(
            {
                "id": requirement_id,
                "input_digest": input_digest,
                "payload_sha256": payload_sha256,
            }
        )
    return rows


def input_manifest(
    root: Path,
    requirement: dict[str, Any],
    *,
    lane_manifest: dict[str, Any] | None,
    corpus: list[dict[str, Any]],
    dependencies: list[dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(requirement, dict) or not isinstance(requirement.get("id"), str):
        raise EvidenceError("requirement requires a stable id")
    producer_files = requirement.get("producer_files")
    comparator_files = requirement.get("comparator_files")
    return {
        "schema": 1,
        "requirement": requirement["id"],
        "specification": _specification(root, requirement),
        "producer_files": _declared_files(root, producer_files),
        "comparator_files": _declared_files(root, comparator_files),
        "runtime": _runtime_identity(requirement),
        "native": _native_identity(root, requirement, lane_manifest),
        "reference": _reference_identity(root, requirement),
        "corpus": _corpus_identity(root, corpus),
        "dependencies": _dependency_identity(dependencies),
    }


def payload_sha256(artifact: dict[str, Any]) -> str:
    if not isinstance(artifact, dict):
        raise EvidenceError("artifact is malformed")
    value = {
        key: item
        for key, item in artifact.items()
        if key not in {"validation_receipt", "validated_revision", "payload_sha256"}
    }
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def _require_observations(root: Path, artifact: dict[str, Any]) -> str | None:
    observations = artifact.get("observations")
    if not isinstance(observations, list) or not observations:
        return "artifact has no raw observations"
    for observation in observations:
        if not isinstance(observation, dict):
            return "observation is malformed"
        path = observation.get("path")
        digest = observation.get("sha256")
        if not isinstance(path, str) or not isinstance(digest, str):
            return "observation lacks path or sha256"
        try:
            actual = file_identity(root, path)["sha256"]
        except EvidenceError as exc:
            return str(exc)
        if actual != digest:
            return f"observation digest differs: {path}"
    return None


def _requires_independent_observation(requirement_id: str) -> bool:
    return not requirement_id.startswith("completion:v2:reset:")


def _all_checks_pass(value: Any) -> bool:
    if not isinstance(value, dict) or not value:
        return False
    for item in value.values():
        if isinstance(item, str):
            if item != "PASS":
                return False
        elif isinstance(item, dict):
            if item.get("status") != "PASS":
                return False
        else:
            return False
    return True


def _validate_observation_kind(
    requirement: dict[str, Any], artifact: dict[str, Any]
) -> str | None:
    requirement_id = requirement["id"]
    if not _requires_independent_observation(requirement_id):
        return None
    oracles = artifact.get("oracles")
    if not isinstance(oracles, list) or not all(
        isinstance(value, str) for value in oracles
    ):
        return "artifact has no oracle identities"
    normalized = {value.casefold() for value in oracles}
    if requirement_id == "completion:v2:p2:leaves":
        if not isinstance(artifact.get("corpus"), dict) or not isinstance(
            artifact.get("receipts"), dict
        ):
            return "leaf proof lacks corpus or mutation receipts"
        return None
    if requirement_id == "completion:v2:faithful-4x3:package":
        return (
            None
            if _all_checks_pass(artifact.get("checks"))
            else "package proof lacks passing checks"
        )
    if requirement_id in {
        "completion:v2:p0:substrate",
        "completion:v2:p1:hardware-removal",
    }:
        if "native" not in normalized:
            return "artifact has no native observation"
        if not normalized & {"oracle-b", "pyboy", "oracle-diff-all"}:
            return "artifact lacks independent oracle proof"
        return (
            None
            if _all_checks_pass(artifact.get("checks"))
            else "artifact lacks passing command checks"
        )
    if "native" not in normalized:
        return "artifact has no native observation"
    if not normalized & {
        "oracle-b",
        "pyboy",
        "gambatte",
        "reference",
        "linked-reference",
    }:
        return "native-only evidence is not independent proof"
    comparison = artifact.get("comparison")
    if not isinstance(comparison, dict) or comparison.get("status") != "PASS":
        return "artifact lacks a passing measured comparison"
    return None


def validate_requirement(
    root: Path,
    requirement: dict[str, Any],
    artifact: dict[str, Any],
    expected_manifest: dict[str, Any],
) -> tuple[str, str | None]:
    if not isinstance(artifact, dict):
        return "invalid", "artifact is malformed"
    if artifact.get("schema") != requirement.get("artifact_schema"):
        return "stale", "artifact schema does not match requirement"
    if artifact.get("status") != "PASS":
        return "failing", "artifact status is not PASS"
    expected_digest = canonical_digest(expected_manifest)
    artifact_manifest = artifact.get("input_manifest")
    if not isinstance(artifact_manifest, dict):
        return "stale", "artifact has no semantic input manifest"
    if canonical_digest(artifact_manifest) != expected_digest:
        return "stale", "artifact input manifest differs"
    if artifact.get("input_digest") != expected_digest:
        return "stale", "artifact input digest differs"
    if (
        not isinstance(artifact.get("produced_revision"), str)
        or not artifact["produced_revision"]
    ):
        return "invalid", "artifact has no produced revision"
    if artifact.get("terminal_event") != requirement.get("terminal_event"):
        return "failing", "required terminal event is absent"
    frames = artifact.get("frames")
    if not isinstance(frames, int) or frames < requirement.get("min_frames", 0):
        return "failing", "minimum frame bound is not met"
    events = artifact.get("events")
    if not isinstance(events, int) or events < requirement.get("min_events", 0):
        return "failing", "minimum event bound is not met"
    fields = artifact.get("state_fields")
    if not isinstance(fields, list) or not set(
        requirement.get("state_fields", [])
    ) <= set(fields):
        return "failing", "representation fields are incomplete"
    if (
        artifact.get("unsupported")
        or artifact.get("timeout")
        or artifact.get("partial")
    ):
        return "failing", "artifact records unsupported, timeout, or partial evidence"
    if (
        _dependency_identity(artifact.get("dependencies", []))
        != expected_manifest["dependencies"]
    ):
        return "stale", "artifact dependency identities differ"
    observation_error = _require_observations(root, artifact)
    if observation_error:
        return "invalid", observation_error
    proof_error = _validate_observation_kind(requirement, artifact)
    if proof_error:
        return "failing", proof_error
    return "pass", None


def validation_receipt(
    root: Path, artifact: dict[str, Any], input_digest: str, validated_revision: str
) -> dict[str, Any]:
    if not isinstance(validated_revision, str) or not validated_revision:
        raise EvidenceError("validation receipt requires a revision")
    return {
        "schema": "validation-receipt-v1",
        "validated_revision": validated_revision,
        "input_digest": input_digest,
        "payload_sha256": payload_sha256(artifact),
    }


def write_validation_receipt(
    root: Path,
    artifact_path: Path,
    artifact: dict[str, Any],
    input_digest: str,
    validated_revision: str,
) -> Path:
    receipt = validation_receipt(root, artifact, input_digest, validated_revision)
    path = artifact_path.with_suffix(artifact_path.suffix + ".validation.json")
    path.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return path


def validate_finality_record(
    root: Path,
    record: dict[str, Any],
    *,
    routine: str,
    body_sha256: str,
    contract_sha256: str,
) -> tuple[bool, str | None]:
    if not isinstance(record, dict) or record.get("schema") != "routine-finality-v1":
        return False, "missing routine-finality-v1 evidence"
    if record.get("routine") != routine:
        return False, "finality routine differs"
    if record.get("body_sha256") != body_sha256:
        return False, "finality body hash differs"
    if record.get("contract_sha256") != contract_sha256:
        return False, "finality contract hash differs"
    kind = record.get("kind")
    if kind not in {"return", "event", "intentional-transform"}:
        return False, "finality kind is invalid"
    refs = record.get("evidence_refs")
    if not isinstance(refs, list) or not refs:
        return False, "finality evidence references are missing"
    for reference in refs:
        if not isinstance(reference, dict):
            return False, "finality evidence reference is malformed"
        path = reference.get("path")
        digest = reference.get("sha256")
        if not isinstance(path, str) or not isinstance(digest, str):
            return False, "finality evidence reference lacks identity"
        try:
            actual = file_identity(root, path)["sha256"]
        except EvidenceError as exc:
            return False, str(exc)
        if actual != digest:
            return False, f"finality evidence digest differs: {path}"
    if kind in {"event", "intentional-transform"}:
        witness = record.get("bilateral_witness")
        cfg = record.get("cfg_obligation")
        if not isinstance(witness, dict) or witness.get("status") != "PASS":
            return False, "finality event lacks bilateral witness"
        oracles = witness.get("oracles")
        if not isinstance(oracles, list) or {"native", "reference"} - set(oracles):
            return False, "finality event lacks native/reference witness"
        if not isinstance(cfg, dict) or cfg.get("status") != "closed":
            return False, "finality event lacks closed CFG obligation"
    if kind == "intentional-transform":
        transform = record.get("transform")
        if not isinstance(transform, str) or not transform:
            return False, "intentional-transform finality lacks transform name"
    return True, None
