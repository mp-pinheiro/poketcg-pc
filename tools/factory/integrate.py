#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import common
import workers

ROOT = common.ROOT
FACTORY = common.FACTORY
GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
V2_INTEGRATION_ROOT = FACTORY / "integration-repo"


class IntegrationError(RuntimeError):
    pass


@dataclass(frozen=True)
class IntegrationResult:
    source_revision: str
    publication_revision: str
    remote_revision: str
    gate_sha256: str
    progress_sha256: str
    routine_names: tuple[str, ...]

    def as_dict(self) -> dict:
        return {
            "source_revision": self.source_revision,
            "publication_revision": self.publication_revision,
            "remote_revision": self.remote_revision,
            "gate_sha256": self.gate_sha256,
            "progress_sha256": self.progress_sha256,
            "routine_names": list(self.routine_names),
        }


def _run(command: list[str], cwd: Path, timeout: int = 1800) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
        env=GIT_ENV,
    )
    if result.returncode != 0:
        raise IntegrationError(f"{' '.join(command)} failed: {(result.stdout + result.stderr)[-4000:]}")
    return result


def _revision(cwd: Path, revision: str) -> str:
    value = _run(["jj", "log", "--no-graph", "-r", revision, "-T", "commit_id"], cwd, 120).stdout.strip()
    if len(value) != 40:
        raise IntegrationError(f"cannot resolve {revision}")
    return value


def _origin_url() -> str:
    value = _run(["git", "config", "--get", "remote.origin.url"], ROOT, 120).stdout.strip()
    if not value:
        raise IntegrationError("origin URL is unavailable")
    return value


def ensure_v2_clone() -> Path:
    if not V2_INTEGRATION_ROOT.exists():
        V2_INTEGRATION_ROOT.parent.mkdir(parents=True, exist_ok=True)
        _run(["jj", "git", "clone", "--colocate", _origin_url(), str(V2_INTEGRATION_ROOT)], ROOT, 600)
    _run(
        ["jj", "config", "set", "--repo", "experimental-advance-branches.enabled-branches", "[]"],
        V2_INTEGRATION_ROOT,
        120,
    )
    return V2_INTEGRATION_ROOT


def _tree_sha256(cwd: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(cwd.rglob("*")):
        if not path.is_file() or any(part in {".git", ".jj", "build", ".factory"} for part in path.relative_to(cwd).parts):
            continue
        relative = path.relative_to(cwd).as_posix()
        digest.update(relative.encode())
        digest.update(b"\0")
        digest.update(_file_sha256(path).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def _saga_path(batch_id: str) -> Path:
    return FACTORY / "v2" / "integrations" / f"{batch_id}.json"


def _write_saga(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
    os.replace(temporary, path)




def saga_records() -> list[dict]:
    root = FACTORY / "v2" / "integrations"
    records: list[dict] = []
    if not root.is_dir():
        return records
    for path in sorted(root.glob("*.json")):
        try:
            value = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            records.append({"path": str(path), "status": "corrupt"})
            continue
        if isinstance(value, dict):
            records.append({
                "path": str(path),
                "batch_id": value.get("batch_id"),
                "phase": value.get("phase"),
                "result": value.get("result"),
            })
    return records


def mark_saga_phase(batch_id: str, phase: str, data: dict) -> None:
    path = _saga_path(batch_id)
    try:
        saga = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrationError("integration saga is missing or corrupt") from exc
    if saga.get("phase") != "pushed":
        raise IntegrationError("integration saga is not ready for projection proof")
    pushed = saga.get("phases", {}).get("pushed", {})
    saga["phase"] = phase
    saga.setdefault("phases", {})[phase] = {
        **data,
        "input_tree_sha256": pushed.get("output_tree_sha256"),
        "output_tree_sha256": pushed.get("output_tree_sha256"),
    }
    _write_saga(path, saga)
def _clean(cwd: Path) -> None:
    if _run(["jj", "diff", "--summary"], cwd, 120).stdout.strip():
        raise IntegrationError("integration clone has unexpected dirty paths")


def _artifact_members(artifact_sha256: str) -> list[Path]:
    if not workers.artifact_exists(artifact_sha256):
        raise IntegrationError(f"artifact {artifact_sha256} is missing or corrupt")
    root = workers.V2_ARTIFACTS / artifact_sha256
    metadata = json.loads((root / ".factory-artifact.json").read_text())
    if metadata.get("kind") != "group":
        return [root]
    members = metadata.get("members")
    if not isinstance(members, list) or not all(isinstance(member, str) for member in members):
        raise IntegrationError(f"group artifact {artifact_sha256} has invalid members")
    return [root / "members" / member for member in members]


def _bundle_paths(bundle: Path) -> tuple[dict, list[str]]:
    try:
        identity = json.loads((bundle / "packet.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrationError(f"artifact bundle {bundle} lacks packet identity") from exc
    basename = identity.get("basename")
    routines = identity.get("routines")
    if not isinstance(basename, str) or not isinstance(routines, list):
        raise IntegrationError(f"artifact bundle {bundle} identity is invalid")
    paths = [
        f"src/home/{basename}.c",
        f"src/home/{basename}.h",
        f"src/probe/{basename}.c",
        f"tests/cases/{basename}.py",
    ]
    for routine in routines:
        name = routine.get("name") if isinstance(routine, dict) else None
        if not isinstance(name, str):
            raise IntegrationError(f"artifact bundle {bundle} has invalid routine identity")
        paths.append(f"tools/oracle/mutation_receipts/{name}.json")
    if any(not (bundle / relative).is_file() for relative in paths):
        raise IntegrationError(f"artifact bundle {bundle} is missing an owned path")
    return identity, paths


def apply_v2_artifacts(cwd: Path, artifact_sha256s: list[str]) -> tuple[str, ...]:
    applied: set[str] = set()
    routines: set[str] = set()
    for artifact_sha256 in sorted(set(artifact_sha256s)):
        for bundle in _artifact_members(artifact_sha256):
            identity, paths = _bundle_paths(bundle)
            for relative in paths:
                source = bundle / relative
                destination = cwd / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                applied.add(relative)
            for routine in identity["routines"]:
                routines.add(str(routine["name"]))
    if not applied:
        raise IntegrationError("integration has no artifact paths")
    return tuple(sorted(routines))


def _candidate_proof(cwd: Path, routines: tuple[str, ...]) -> None:
    _run(["just", "build-barrier"], cwd, 1800)
    _run(
        [
            "uv", "run", "--project", "tools/oracle", "--frozen", "--python", "3.12.3",
            "python", "tests/test_leaves.py",
            *[argument for routine in routines for argument in ("--fn", routine)],
            "--oracle-mode", "refresh",
            "--cache-dir", str(cwd / ".factory" / "oracle-cache"),
            "--probe", str(cwd / "build-barrier" / "poketcg_probe"),
        ],
        cwd,
        1800,
    )


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrate_v2(
    artifact_sha256s: list[str],
    *,
    expected_remote_revision: str,
    phase: Callable[[str, dict], None],
    forecast_payload: dict | None = None,
    factory_state_payload: dict | None = None,
    batch_id: str | None = None,
) -> IntegrationResult:
    batch_id = batch_id or hashlib.sha256(json.dumps({
        "artifacts": sorted(artifact_sha256s),
        "expected_remote_revision": expected_remote_revision,
    }, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    saga_path = _saga_path(batch_id)
    saved_saga: dict | None = None
    if saga_path.is_file():
        try:
            saved_saga = json.loads(saga_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            raise IntegrationError("integration saga is corrupt") from exc
        if saved_saga.get("expected_remote_revision") != expected_remote_revision or saved_saga.get("artifact_sha256s") != sorted(artifact_sha256s):
            raise IntegrationError("integration saga identity conflict")
        if saved_saga.get("phase") in {"pushed", "projections-stable"}:
            result = saved_saga.get("result")
            if not isinstance(result, dict):
                raise IntegrationError("completed integration saga has no result")
            clone = ensure_v2_clone()
            _run(["jj", "git", "fetch", "--remote", "origin"], clone, 600)
            if _revision(clone, "main@origin") != result.get("remote_revision"):
                raise IntegrationError("integration saga remote proof disagrees")
            return IntegrationResult(
                source_revision=str(result["source_revision"]),
                publication_revision=str(result["publication_revision"]),
                remote_revision=str(result["remote_revision"]),
                gate_sha256=str(result["gate_sha256"]),
                progress_sha256=str(result["progress_sha256"]),
                routine_names=tuple(str(name) for name in result["routine_names"]),
            )
    saga: dict = saved_saga or {
        "schema": 2,
        "batch_id": batch_id,
        "artifact_sha256s": sorted(artifact_sha256s),
        "expected_remote_revision": expected_remote_revision,
        "phase": "started",
        "phases": {},
    }
    if saved_saga is None:
        _write_saga(saga_path, saga)
    phase_order = ("started", "prepared", "applied", "source-committed", "gate-passed", "publication-committed", "main-set", "pushed", "projections-stable")
    resume_phase = str(saga.get("phase") or "started")
    if resume_phase not in phase_order:
        raise IntegrationError(f"unknown integration saga phase {resume_phase}")
    clone = ensure_v2_clone()
    if resume_phase not in {"started", "prepared"}:
        proven = saga.get("phases", {}).get(resume_phase)
        if not isinstance(proven, dict) or not isinstance(proven.get("output_tree_sha256"), str):
            raise IntegrationError(f"integration saga lacks tree proof for {resume_phase}")
        if _tree_sha256(clone) != proven["output_tree_sha256"]:
            raise IntegrationError(f"integration clone disagrees with proven {resume_phase} tree")
    if resume_phase in {"started", "prepared"}:
        _clean(clone)
    _run(["jj", "git", "fetch", "--remote", "origin"], clone, 600)
    remote = _revision(clone, "main@origin")
    if remote != expected_remote_revision:
        raise IntegrationError(f"remote main changed: expected {expected_remote_revision}, found {remote}")

    def record_phase(name: str, data: dict) -> None:
        previous = saga.get("phases", {}).get(phase_order[max(0, phase_order.index(name) - 1)], {})
        input_tree = previous.get("output_tree_sha256") if isinstance(previous, dict) else None
        output_tree = _tree_sha256(clone)
        phase_data = {
            **data,
            "input_tree_sha256": input_tree or output_tree,
            "output_tree_sha256": output_tree,
            "source_revision": data.get("source_revision"),
            "publication_revision": data.get("publication_revision"),
        }
        saga["phase"] = name
        saga["phases"][name] = phase_data
        _write_saga(saga_path, saga)
        phase(name, phase_data)

    if resume_phase == "started":
        record_phase("prepared", {"remote_revision": remote, "artifacts": sorted(artifact_sha256s)})
    start_at = phase_order.index(resume_phase)
    if start_at <= phase_order.index("prepared"):
        _run(["jj", "new", "main@origin"], clone, 120)
        routines = apply_v2_artifacts(clone, artifact_sha256s)
        if forecast_payload is not None:
            path = clone / "site" / "data" / "factory-forecast.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(forecast_payload, sort_keys=True, separators=(",", ":")) + "\n")
        if factory_state_payload is not None:
            path = clone / "site" / "data" / "factory-state.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(factory_state_payload, sort_keys=True, separators=(",", ":")) + "\n")
        record_phase("applied", {"routines": list(routines)})
    else:
        applied = saga.get("phases", {}).get("applied", {})
        routines = tuple(str(name) for name in applied.get("routines", []))
        if not routines:
            raise IntegrationError("integration saga lacks proven applied routines")
    if start_at <= phase_order.index("applied"):
        _candidate_proof(clone, tuple(routines))
        _run(["jj", "commit", "-m", f"feat(port): land {len(routines)} routines"], clone, 120)
        source_revision = _revision(clone, "@-")
        record_phase("source-committed", {"source_revision": source_revision})
    else:
        source_revision = str(saga.get("phases", {}).get("source-committed", {}).get("source_revision") or "")
        if len(source_revision) != 40:
            raise IntegrationError("integration saga lacks proven source revision")
    if start_at <= phase_order.index("source-committed"):
        _run(["just", "oracle-release-gate"], clone, 3600)
        gate_path = clone / "site" / "data" / "gate.json"
        gate_sha256 = _file_sha256(gate_path)
        gate = json.loads(gate_path.read_text())
        if gate.get("commit") != source_revision:
            raise IntegrationError("release gate did not record the source revision")
        record_phase("gate-passed", {"source_revision": source_revision, "gate_sha256": gate_sha256})
    else:
        gate_sha256 = str(saga.get("phases", {}).get("gate-passed", {}).get("gate_sha256") or "")
        if len(gate_sha256) != 64:
            raise IntegrationError("integration saga lacks proven gate")
    if start_at <= phase_order.index("gate-passed"):
        _run([sys.executable, "tools/progress/report.py", "build"], clone, 300)
        _run(["jj", "commit", "-m", "chore(progress): refresh port status"], clone, 120)
        publication_revision = _revision(clone, "@-")
        progress_sha256 = _file_sha256(clone / "site" / "data" / "progress.json")
        record_phase("publication-committed", {"publication_revision": publication_revision, "progress_sha256": progress_sha256})
    else:
        publication_data = saga.get("phases", {}).get("publication-committed", {})
        publication_revision = str(publication_data.get("publication_revision") or "")
        progress_sha256 = str(publication_data.get("progress_sha256") or "")
        if len(publication_revision) != 40 or len(progress_sha256) != 64:
            raise IntegrationError("integration saga lacks proven publication")
    if start_at <= phase_order.index("publication-committed"):
        _run(["jj", "bookmark", "set", "main", "-r", publication_revision], clone, 120)
        record_phase("main-set", {"publication_revision": publication_revision})
    if start_at <= phase_order.index("main-set"):
        _run(["jj", "git", "push", "--remote", "origin", "--bookmark", "main"], clone, 600)
        remote_revision = _revision(clone, "main@origin")
        if remote_revision != publication_revision:
            raise IntegrationError("pushed remote revision does not equal publication revision")
        record_phase("pushed", {"remote_revision": remote_revision})
    else:
        remote_revision = str(saga.get("phases", {}).get("pushed", {}).get("remote_revision") or "")
        if remote_revision != publication_revision:
            raise IntegrationError("integration saga remote proof disagrees")
    result = IntegrationResult(
        source_revision=source_revision,
        publication_revision=publication_revision,
        remote_revision=remote_revision,
        gate_sha256=gate_sha256,
        progress_sha256=progress_sha256,
        routine_names=tuple(routines),
    )
    saga["result"] = result.as_dict()
    _write_saga(saga_path, saga)
    return result
