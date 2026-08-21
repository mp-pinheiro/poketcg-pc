#!/usr/bin/env python3
"""Land verified artifacts: gate, commit, push, record.

Runs in the central checkout, where the ROM, generated headers, and oracle
venv exist. Replaces integrate.py's eight-phase saga with one straight-line
per-batch sequence: fetch, apply, commit, gate, commit, push, record. A gate
failure undoes the source commit and either splits the batch in half or, at
batch size one, quarantines the artifact and moves on.
"""
from __future__ import annotations

import argparse
import datetime
import functools
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
import workers

GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
GATE_COMMAND_DEFAULT = ("just", "oracle-release-gate")
PROGRESS_COMMAND_DEFAULT = ("python3", "tools/progress/report.py", "build")
GATE_TIMEOUT_S = 3600
PROGRESS_TIMEOUT_S = 300
LANDINGS_NAME = "landings.jsonl"
QUARANTINE_NAME = "quarantine.jsonl"


class LandError(RuntimeError):
    pass


def _run(command: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False, env=GIT_ENV,
    )
    if result.returncode != 0:
        raise LandError(f"{' '.join(command)} failed: {(result.stdout + result.stderr)[-4000:]}")
    return result


def _revision(cwd: Path, revision: str) -> str:
    value = _run(["jj", "log", "--no-graph", "-r", revision, "-T", "commit_id"], cwd, 120).stdout.strip()
    if len(value) != 40:
        raise LandError(f"cannot resolve {revision}")
    return value


def _artifact_members(artifact_sha256: str) -> list[Path]:
    if not workers.artifact_exists(artifact_sha256):
        raise LandError(f"artifact {artifact_sha256} is missing or corrupt")
    root = workers.V2_ARTIFACTS / artifact_sha256
    metadata = json.loads((root / ".factory-artifact.json").read_text())
    if metadata.get("kind") != "group":
        return [root]
    members = metadata.get("members")
    if not isinstance(members, list) or not all(isinstance(member, str) for member in members):
        raise LandError(f"group artifact {artifact_sha256} has invalid members")
    return [root / "members" / member for member in members]


def _bundle_paths(bundle: Path) -> tuple[dict, list[str]]:
    try:
        identity = json.loads((bundle / "packet.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise LandError(f"artifact bundle {bundle} lacks packet identity") from exc
    basename = identity.get("basename")
    routines = identity.get("routines")
    if not isinstance(basename, str) or not isinstance(routines, list):
        raise LandError(f"artifact bundle {bundle} identity is invalid")
    paths = [
        f"src/home/{basename}.c",
        f"src/home/{basename}.h",
        f"src/probe/{basename}.c",
        f"tests/cases/{basename}.py",
    ]
    for routine in routines:
        name = routine.get("name") if isinstance(routine, dict) else None
        if not isinstance(name, str):
            raise LandError(f"artifact bundle {bundle} has invalid routine identity")
        paths.append(f"tools/oracle/mutation_receipts/{name}.json")
    if any(not (bundle / relative).is_file() for relative in paths):
        raise LandError(f"artifact bundle {bundle} is missing an owned path")
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
        raise LandError("landing has no artifact paths")
    return tuple(sorted(routines))


@functools.cache
def _artifact_identity(artifact_sha256: str) -> tuple[frozenset[str], frozenset[str]]:
    basenames: set[str] = set()
    routines: set[str] = set()
    for bundle in _artifact_members(artifact_sha256):
        identity, _ = _bundle_paths(bundle)
        basenames.add(str(identity["basename"]))
        for routine in identity["routines"]:
            routines.add(str(routine["name"]))
    return frozenset(basenames), frozenset(routines)


def _report_module(root: Path):
    spec = importlib.util.spec_from_file_location(
        "factory_land_report", root / "tools" / "progress" / "report.py",
    )
    if spec is None or spec.loader is None:
        raise LandError(f"cannot load report module from {root}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _work_records(root: Path) -> list[dict]:
    report = _report_module(root)
    inventory = report.load_inventory()
    routines_set, _ = report.load_routines()
    gate = report.load_gate()
    return report.compute(inventory, routines_set, gate)["work_records"]


def _read_shas(path: Path, key: str) -> set[str]:
    if not path.is_file():
        return set()
    shas: set[str] = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        value = entry.get(key)
        if isinstance(value, str):
            shas.add(value)
    return shas


def _append_jsonl(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as stream:
        stream.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")


def _stale_owned_artifacts(
    root: Path,
    artifacts: list[str],
    main_revision: str,
) -> tuple[list[str], list[dict]]:
    compatible: list[str] = []
    quarantined: list[dict] = []
    for artifact_sha256 in artifacts:
        changed: set[str] = set()
        basenames: set[str] = set()
        bases: set[str] = set()
        for bundle in _artifact_members(artifact_sha256):
            identity, paths = _bundle_paths(bundle)
            basename = identity.get("basename")
            if isinstance(basename, str):
                basenames.add(basename)
            base_commit = identity.get("base_commit")
            if not isinstance(base_commit, str) or not base_commit:
                changed.add("<unresolvable-base-commit>")
                continue
            bases.add(base_commit)
            try:
                base_revision = _revision(root, base_commit)
                output = _run(
                    ["git", "diff", "--name-only",
                     f"{base_revision}..{main_revision}", "--", *paths],
                    root,
                    120,
                ).stdout
            except LandError:
                changed.add("<unresolvable-base-commit>")
                continue
            changed.update(line.strip() for line in output.splitlines() if line.strip())
        if changed:
            record = {
                "quarantined_at": _now_iso(),
                "artifact_sha256": artifact_sha256,
                "basename": ",".join(sorted(basenames)),
                "failure_class": "stale-owned-path",
                "changed_paths": sorted(changed),
                "base_commits": sorted(bases),
                "main_commit": main_revision,
            }
            _append_jsonl(root / ".factory" / QUARANTINE_NAME, record)
            quarantined.append(record)
            print(f"LAND quarantine {artifact_sha256[:16]} stale-owned-path "
                  f"paths={record['changed_paths']}")
        else:
            compatible.append(artifact_sha256)
    return compatible, quarantined

def _now_iso() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


def select_artifacts(root: Path, explicit: list[str] | None) -> list[str]:
    if explicit is not None:
        ordered: list[str] = []
        for sha in explicit:
            if not isinstance(sha, str) or len(sha) != 64:
                raise LandError(f"artifact hash must be 64 hex characters: {sha!r}")
            if sha not in ordered:
                ordered.append(sha)
        return ordered

    excluded = _read_shas(root / ".factory" / LANDINGS_NAME, "artifact_sha256")
    excluded |= _read_shas(root / ".factory" / QUARANTINE_NAME, "artifact_sha256")
    work_state = {record["name"]: record.get("state") for record in _work_records(root)}

    candidates: dict[str, frozenset[str]] = {}
    for record in workers.artifact_records():
        sha = record["artifact_sha256"]
        if sha in excluded:
            continue
        _basenames, routines = _artifact_identity(sha)
        if not routines or all(work_state.get(name) == "complete" for name in routines):
            continue
        candidates[sha] = routines

    owner: dict[str, str] = {}
    for sha, routines in candidates.items():
        for name in routines:
            if name not in owner or sha < owner[name]:
                owner[name] = sha
    return sorted(sha for sha, routines in candidates.items() if all(owner[name] == sha for name in routines))


def batch_artifacts(shas: list[str], batch_size: int) -> list[list[str]]:
    batches: list[list[str]] = []
    pending = list(shas)
    while pending:
        batch: list[str] = []
        used: set[str] = set()
        leftover: list[str] = []
        for sha in pending:
            basenames, _routines = _artifact_identity(sha)
            if len(batch) < batch_size and not (basenames & used):
                batch.append(sha)
                used |= basenames
            else:
                leftover.append(sha)
        batches.append(batch)
        pending = leftover
    return batches


def _land_batch(
    root: Path,
    artifacts: list[str],
    *,
    gate_command: tuple[str, ...],
    progress_command: tuple[str, ...],
    push: bool,
    counter: list[int],
) -> tuple[list[dict], list[dict]]:
    _run(["jj", "git", "fetch", "--remote", "origin"], root, 300)
    dirty = _run(["jj", "diff", "--summary"], root, 120).stdout.strip()
    if dirty:
        raise LandError(f"working copy is dirty before batch: {dirty[:200]}")
    pre_batch_revision = _revision(root, "main")
    origin_revision = _revision(root, "main@origin")
    if pre_batch_revision != origin_revision:
        raise LandError(
            f"main {pre_batch_revision[:12]} diverges from origin main {origin_revision[:12]}"
        )
    artifacts, stale = _stale_owned_artifacts(root, artifacts, pre_batch_revision)
    if not artifacts:
        return [], stale


    routines = apply_v2_artifacts(root, artifacts)
    _run(["jj", "commit", "-m", f"feat(port): land {len(routines)} routines"], root, 120)
    source_revision = _revision(root, "@-")

    gate_started = time.monotonic()
    gate_completed = subprocess.run(
        gate_command, cwd=root, text=True, capture_output=True, timeout=GATE_TIMEOUT_S, check=False,
    )
    gate_seconds = time.monotonic() - gate_started
    gate_tail = (gate_completed.stdout + gate_completed.stderr)[-2000:]
    gate_ok = gate_completed.returncode == 0
    if gate_ok:
        gate_path = root / "site" / "data" / "gate.json"
        try:
            gate_data = json.loads(gate_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            gate_ok = False
            gate_tail = f"{gate_tail}\n{type(exc).__name__}: {exc}"
        else:
            gate_ok = gate_data.get("commit") == source_revision and gate_data.get("complete") is True

    if not gate_ok:
        _run(["jj", "abandon", "@-"], root, 120)
        if _run(["jj", "diff", "--summary"], root, 120).stdout.strip():
            raise LandError("working copy dirty after abandoning a failed batch")
        if _revision(root, "main") != pre_batch_revision:
            _run(["jj", "bookmark", "set", "main", "-r", pre_batch_revision], root, 120)
        if len(artifacts) > 1:
            middle = len(artifacts) // 2
            left, right = artifacts[:middle], artifacts[middle:]
            left_landed, left_quarantined = _land_batch(
                root, left, gate_command=gate_command, progress_command=progress_command,
                push=push, counter=counter,
            )
            right_landed, right_quarantined = _land_batch(
                root, right, gate_command=gate_command, progress_command=progress_command,
                push=push, counter=counter,
            )
            return left_landed + right_landed, stale + left_quarantined + right_quarantined
        sha = artifacts[0]
        basenames, _routines = _artifact_identity(sha)
        record = {
            "quarantined_at": _now_iso(),
            "artifact_sha256": sha,
            "basename": ",".join(sorted(basenames)),
            "gate_tail": gate_tail,
        }
        _append_jsonl(root / ".factory" / QUARANTINE_NAME, record)
        print(f"LAND quarantine {sha[:16]} {record['basename']}")
        return [], stale + [record]

    progress_completed = subprocess.run(
        progress_command, cwd=root, text=True, capture_output=True, timeout=PROGRESS_TIMEOUT_S, check=False,
    )
    if progress_completed.returncode == 0:
        _run(["jj", "commit", "-m", "chore(progress): refresh port status"], root, 120)
        publication_revision = _revision(root, "@-")
    else:
        publication_revision = source_revision
        print(
            "LAND progress-failed batch: "
            f"{(progress_completed.stdout + progress_completed.stderr)[-1000:].strip()}; "
            "gate passed and the landing is recorded; rerun the progress command, "
            "then commit and push manually"
        )

    landed_at = _now_iso()
    batch_id = hashlib.sha256(json.dumps(sorted(artifacts), separators=(",", ":")).encode()).hexdigest()
    landed_records: list[dict] = []
    for sha in artifacts:
        basenames, sha_routines = _artifact_identity(sha)
        record = {
            "landed_at": landed_at,
            "artifact_sha256": sha,
            "basename": ",".join(sorted(basenames)),
            "routines": sorted(sha_routines),
            "source_revision": source_revision,
            "publication_revision": publication_revision,
            "batch_id": batch_id,
            "seconds_gate": round(gate_seconds, 3),
        }
        _append_jsonl(root / ".factory" / LANDINGS_NAME, record)
        landed_records.append(record)

    if push:
        try:
            _run(["jj", "git", "push", "--remote", "origin", "--bookmark", "main"], root, 300)
            remote_revision = _revision(root, "main@origin")
            if remote_revision != publication_revision:
                _run(["jj", "bookmark", "set", "main", "-r", publication_revision], root, 120)
                _run(["jj", "git", "push", "--remote", "origin", "--bookmark", "main"], root, 300)
                remote_revision = _revision(root, "main@origin")
            if remote_revision != publication_revision:
                print(
                    f"LAND push-incomplete batch remote={remote_revision[:12]} "
                    f"publication={publication_revision[:12]}; run "
                    "'jj git push --remote origin --bookmark main' to finish publishing"
                )
        except (LandError, subprocess.TimeoutExpired) as exc:
            print(
                f"LAND push-failed batch: {exc}; run "
                "'jj git push --remote origin --bookmark main' to publish later"
            )

    counter[0] += 1
    print(
        f"LAND batch {counter[0]} artifacts={len(artifacts)} gate={round(gate_seconds, 1)}s "
        f"source={source_revision[:12]} publication={publication_revision[:12]}"
    )
    return landed_records, stale


def _print_eta() -> int:
    landings_path = common.ROOT / ".factory" / LANDINGS_NAME
    raw_lines = landings_path.read_text().splitlines() if landings_path.is_file() else []
    records: list[dict] = []
    skipped = 0
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            skipped += 1

    usable = [r for r in records if isinstance(r.get("landed_at"), str)]
    skipped += len(records) - len(usable)
    if skipped:
        print(f"ETA skipped={skipped}")
    if len(usable) < 5:
        print(f"ETA status=unavailable landings={len(usable)}")
        return 0

    def parse(value: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(value)

    timestamps = sorted(parse(r["landed_at"]) for r in usable)
    first_hour = timestamps[0].replace(minute=0, second=0, microsecond=0)
    last_hour = timestamps[-1].replace(minute=0, second=0, microsecond=0)
    total_hours = int((last_hour - first_hour).total_seconds() // 3600)
    samples = [0] * total_hours
    for ts in timestamps:
        hour_index = int((ts.replace(minute=0, second=0, microsecond=0) - first_hour).total_seconds() // 3600)
        if 0 <= hour_index < total_hours:
            samples[hour_index] += 1

    work_records = _work_records(common.ROOT)
    remaining = sum(
        1 for record in work_records
        if record.get("state") in ("ready", "blocked") and not record.get("operational_blocker")
    )

    seed = hashlib.sha256(landings_path.read_bytes()).hexdigest()[:16]
    rng = random.Random(seed)
    cap = 4 * remaining + 100
    draws: list[int] = []
    for _ in range(10000):
        if remaining == 0:
            draws.append(0)
            continue
        if not samples:
            draws.append(cap)
            continue
        consumed = 0
        elapsed = 0
        while consumed < remaining and elapsed < cap:
            consumed += rng.choice(samples)
            elapsed += 1
        draws.append(elapsed)
    draws.sort()

    def percentile(fraction: float) -> int:
        index = min(len(draws) - 1, max(0, round(fraction * (len(draws) - 1))))
        return draws[index]

    p50, p85, p95 = percentile(0.50), percentile(0.85), percentile(0.95)
    now = datetime.datetime.now(datetime.UTC)

    def date_after(hours: int) -> str:
        return (now + datetime.timedelta(hours=hours)).strftime("%Y-%m-%d")

    status = "calibrated" if len(usable) >= 30 and total_hours >= 11 else "provisional"
    print(
        f"ETA status={status} landings={len(usable)} buckets={total_hours} "
        f"p50={p50} p85={p85} p95={p95} p50_at={date_after(p50)} "
        f"p85_at={date_after(p85)} p95_at={date_after(p95)}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", action="append", dest="artifacts", default=None,
                        help="land exactly these artifact SHA-256 hashes")
    parser.add_argument("--all", action="store_true", help="land every eligible verified artifact")
    parser.add_argument("--batch", type=int, default=4, help="max artifacts per landing batch")
    parser.add_argument("--root", type=Path, default=common.ROOT, help="checkout to land into")
    parser.add_argument("--gate-command", action="append", dest="gate_command", default=None)
    parser.add_argument("--progress-command", action="append", dest="progress_command", default=None)
    parser.add_argument("--no-push", action="store_true", help="commit and gate locally without pushing")
    parser.add_argument("--eta", action="store_true", help="print a landing forecast and exit")
    arguments = parser.parse_args(argv)

    if arguments.eta:
        return _print_eta()

    if bool(arguments.artifacts) == bool(arguments.all):
        print("LAND error exactly one of --all or --artifact is required", file=sys.stderr)
        return 2

    root = arguments.root.resolve()
    gate_command = tuple(arguments.gate_command) if arguments.gate_command else GATE_COMMAND_DEFAULT
    progress_command = (
        tuple(arguments.progress_command) if arguments.progress_command else PROGRESS_COMMAND_DEFAULT
    )

    try:
        shas = select_artifacts(root, arguments.artifacts)
        if not shas:
            print("LAND done landed=0 quarantined=0")
            return 0

        batches = batch_artifacts(shas, arguments.batch)
        landed: list[dict] = []
        quarantined: list[dict] = []
        counter = [0]
        for batch in batches:
            batch_landed, batch_quarantined = _land_batch(
                root, batch, gate_command=gate_command, progress_command=progress_command,
                push=not arguments.no_push, counter=counter,
            )
            landed.extend(batch_landed)
            quarantined.extend(batch_quarantined)
    except LandError as exc:
        print(f"LAND error {exc}", file=sys.stderr)
        return 2

    print(f"LAND done landed={len(landed)} quarantined={len(quarantined)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
