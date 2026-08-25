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
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
import heal
import surgery
import workers

GIT_ENV = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
GATE_COMMAND_DEFAULT = ("just", "oracle-release-gate")
PROGRESS_COMMAND_DEFAULT = ("python3", "tools/progress/report.py", "build")
GATE_TIMEOUT_S = 3600
PROGRESS_TIMEOUT_S = 300
LANDINGS_NAME = "landings.jsonl"
QUARANTINE_NAME = "quarantine.jsonl"

# The only trees a graft writes: the quartet plus the per-routine mutation
# receipts. Rolling a rejected batch back through these paths instead of the
# whole working copy keeps a concurrent orchestrator's uncommitted work - a
# harness fix under tools/factory, say - alive. Omitting the receipts left
# stray files behind, which is what the marker-regression smoke stage checks.
SURGERY_TREES = ("src/home", "src/probe", "tests/cases",
                 "tools/oracle/mutation_receipts")

# The statics block shares the routine marker shape, so it has to be filtered
# out of the census; every other match is a landed routine's C fragment.
C_MARKER = re.compile(r"^/\* >>> factory ([A-Za-z_][\w.]*) \*/$", re.MULTILINE)


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


def _has_conflict(cwd: Path, revision: str) -> bool:
    """Whether `revision` carries unresolved merge conflicts.

    `jj resolve --list` cannot serve as this check because it exits non-zero
    precisely when a revision is clean.
    """
    listed = _run(["jj", "log", "--no-graph", "-r", revision, "-T", "conflict"], cwd, 120)
    return listed.stdout.strip() == "true"


def _is_ancestor(cwd: Path, ancestor: str, descendant: str) -> bool:
    """True when `descendant` already contains `ancestor`."""
    listed = _run(["jj", "log", "--no-graph", "-r", f"{ancestor} & ::{descendant}",
                   "-T", "commit_id"], cwd, 120).stdout.strip()
    return listed.startswith(ancestor)


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


RECEIPT_PREFIX = "tools/oracle/mutation_receipts/"


def marker_census(cwd: Path) -> set[str]:
    """Every routine with a landed C fragment under src/home.

    Landing must be monotone in this set: a batch that shrinks it has erased a
    routine some earlier batch proved, which is exactly how PokemonDomeLoadMap
    was lost when a same-basename sibling copied a stale whole file over it.
    """
    names: set[str] = set()
    home = cwd / "src" / "home"
    if not home.is_dir():
        return names
    for path in sorted(home.glob("*.c")):
        names.update(C_MARKER.findall(path.read_text(errors="replace")))
    names.discard("statics")
    return names


def apply_v2_artifacts(cwd: Path, artifact_sha256s: list[str]) -> tuple[str, ...]:
    """Graft each bundle's marker blocks into the checkout.

    The quartet is transplanted through surgery.extract/apply, never copied
    wholesale: apply() replaces a block in place when its marker exists and
    appends otherwise, and merges statics append-only against the destination's
    current block. Two artifacts for one basename therefore compose instead of
    the later one erasing the earlier. Mutation receipts stay a plain copy -
    one file per routine, shared with nothing.
    """
    grafted = 0
    routines: set[str] = set()
    for artifact_sha256 in sorted(set(artifact_sha256s)):
        for bundle in _artifact_members(artifact_sha256):
            identity, paths = _bundle_paths(bundle)
            surgery.apply(cwd, identity, surgery.extract(bundle, identity))
            grafted += 1
            for relative in paths:
                if not relative.startswith(RECEIPT_PREFIX):
                    continue
                destination = cwd / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(bundle / relative, destination)
            for routine in identity["routines"]:
                routines.add(str(routine["name"]))
    if not grafted:
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


def _latest_timestamps(path: Path, key: str) -> dict[str, datetime.datetime]:
    """Newest `key` timestamp per artifact_sha256 in a JSONL ledger."""
    latest: dict[str, datetime.datetime] = {}
    if not path.is_file():
        return latest
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        sha, stamp = entry.get("artifact_sha256"), entry.get(key)
        if not isinstance(sha, str) or not isinstance(stamp, str):
            continue
        try:
            moment = datetime.datetime.fromisoformat(stamp)
        except ValueError:
            continue
        if sha not in latest or moment > latest[sha]:
            latest[sha] = moment
    return latest


def unexcluded_by_revocation(root: Path) -> set[str]:
    """Revoked artifacts that still need re-landing.

    A revocation says a recorded landing never reached the tree, so the artifact
    must become selectable again. It stops being selectable the moment a landing
    newer than that revocation is recorded: without that expiry every artifact
    ever revoked is re-grafted and re-gated on every batch forever, at roughly
    140s of gate time apiece. A revocation with no comparable landing timestamp
    keeps the artifact selectable, because losing a landing is worse than
    regrafting one.
    """
    revoked = heal.revoked_artifacts(root)
    if not revoked:
        return revoked
    landings = _latest_timestamps(root / ".factory" / LANDINGS_NAME, "landed_at")
    revocations = _latest_timestamps(root / ".factory" / heal.REVOCATIONS_NAME, "revoked_at")
    return {
        sha for sha in revoked
        if sha not in landings or sha not in revocations
        or revocations[sha] > landings[sha]
    }


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
    # A revoked artifact is a landing this checkout recorded but never kept. The
    # payload is immutable and gate-verified, so re-landing it is the repair;
    # leaving it excluded is what made the loss permanent.
    excluded -= unexcluded_by_revocation(root)
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


def _reject_batch(
    root: Path,
    artifacts: list[str],
    failure_class: str,
    detail: str,
    *,
    gate_command: tuple[str, ...],
    progress_command: tuple[str, ...],
    push: bool,
    counter: list[int],
    stale: list[dict],
) -> tuple[list[dict], list[dict]]:
    """Bisect a rejected batch, or quarantine it once it is a singleton.

    The caller must already have restored the working copy and left main where
    it was: the recursion re-enters _land_batch, which demands a clean tree, and
    it must not hold tree.lock, which the recursive call takes on a new
    descriptor.
    """
    if len(artifacts) > 1:
        middle = len(artifacts) // 2
        left_landed, left_quarantined = _land_batch(
            root, artifacts[:middle], gate_command=gate_command,
            progress_command=progress_command, push=push, counter=counter,
        )
        right_landed, right_quarantined = _land_batch(
            root, artifacts[middle:], gate_command=gate_command,
            progress_command=progress_command, push=push, counter=counter,
        )
        return (left_landed + right_landed,
                stale + left_quarantined + right_quarantined)
    sha = artifacts[0]
    basenames, _routines = _artifact_identity(sha)
    record = {
        "quarantined_at": _now_iso(),
        "artifact_sha256": sha,
        "basename": ",".join(sorted(basenames)),
        "failure_class": failure_class,
        "detail": detail,
    }
    common.append_jsonl(root / ".factory" / QUARANTINE_NAME, record)
    print(f"LAND quarantine {sha[:16]} {failure_class} {record['basename']}")
    return [], stale + [record]


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
    stale: list[dict] = []

    # Exclusive only while the working copy is mid-rewrite: a lane rsyncing a
    # half-applied quartet would verify a tree that never existed. The gate and
    # progress runs below stay outside the lock - they touch only site/,
    # build-barrier/, and tools/oracle/gbref/build/, all rsync-excluded, and a
    # 3600s exclusive hold would stall every lane.
    with common.file_lock(common.locks_dir(root) / "tree.lock", timeout=1800):
        before_markers = marker_census(root)
        rejection: tuple[str, str] | None = None
        try:
            routines = apply_v2_artifacts(root, artifacts)
        except (surgery.SurgeryError, LandError, OSError) as exc:
            rejection = ("graft-failed", f"{type(exc).__name__}: {exc}"[-2000:])
        else:
            dropped = sorted(before_markers - marker_census(root))
            if dropped:
                rejection = ("marker-regression",
                             f"landing dropped landed markers: {dropped}")
        if rejection is None:
            _run(["jj", "commit", "-m", f"feat(port): land {len(routines)} routines"], root, 120)
            source_revision = _revision(root, "@-")
        else:
            # Nothing is committed yet, so discarding the graft is the entire
            # undo and main never moved. Restore only the trees surgery writes:
            # a bare `jj restore` also throws away whatever another session has
            # uncommitted in tools/, which is how a concurrent orchestrator's
            # harness fix silently disappeared mid-session.
            _run(["jj", "restore", *SURGERY_TREES], root, 120)
    if rejection is not None:
        return _reject_batch(
            root, artifacts, rejection[0], rejection[1], gate_command=gate_command,
            progress_command=progress_command, push=push, counter=counter, stale=stale,
        )

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
        # Must close before the bisect recursion below: the recursive call takes
        # this same lock on a new descriptor and would block on its own caller.
        with common.file_lock(common.locks_dir(root) / "tree.lock", timeout=1800):
            # By revision, never `@-`: another session may have committed on top
            # of this landing, and abandoning `@-` would destroy its commit
            # instead of this batch. Abandoning the named revision rebases any
            # such descendant onto the parent and keeps its content.
            _run(["jj", "abandon", source_revision], root, 120)
            _run(["jj", "restore", *SURGERY_TREES], root, 120)
            if _run(["jj", "diff", "--summary", *SURGERY_TREES], root, 120).stdout.strip():
                raise LandError("working copy dirty after abandoning a failed batch")
            # Only rewind the bookmark this batch advanced. If another session
            # has moved main on, rewinding would unpublish its work.
            if _revision(root, "main") == source_revision:
                _run(["jj", "bookmark", "set", "main", "-r", pre_batch_revision], root, 120)
        return _reject_batch(
            root, artifacts, "gate", gate_tail, gate_command=gate_command,
            progress_command=progress_command, push=push, counter=counter, stale=stale,
        )

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
        common.append_jsonl(root / ".factory" / LANDINGS_NAME, record)
        landed_records.append(record)

    if push:
        try:
            # The release pipeline pushes to main during the gate, which leaves
            # the local bookmark conflicted: it still names this publication
            # while origin names the release. `jj log -r main` refuses a
            # conflicted name, so anchor on main@origin, a single remote ref
            # that resolves either way. Without the rebase the landing is
            # stranded off-trunk with nothing naming it; the gate already
            # accepted the content, so a graft that no longer applies surfaces
            # as a conflict here rather than as a silent loss.
            _run(["jj", "git", "fetch", "--remote", "origin"], root, 300)
            head = _revision(root, "main@origin")
            if head != publication_revision and not _is_ancestor(root, head, publication_revision):
                _run(["jj", "rebase", "-s", source_revision, "-d", head], root, 300)
                publication_revision = _revision(root, "@-")
                if _has_conflict(root, publication_revision):
                    raise LandError("rebase onto the advanced main conflicts")
                # The side a conflicted bookmark resolved to need not be an
                # ancestor, which plain `bookmark set` refuses as backwards.
                _run(["jj", "bookmark", "set", "main", "-r", publication_revision,
                      "--allow-backwards"], root, 120)
            _run(["jj", "git", "push", "--remote", "origin", "--bookmark", "main"], root, 300)
            remote_revision = _revision(root, "main@origin")
            if remote_revision != publication_revision:
                _run(["jj", "bookmark", "set", "main", "-r", publication_revision,
                      "--allow-backwards"], root, 120)
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
        # One lander per checkout. Everything below writes the working copy, the
        # central gate's build-barrier, and site/data - none of it survives two
        # interleaved drivers. Refuse immediately rather than queue: a busy
        # session should keep generating and let the holder land the artifacts.
        with common.file_lock(common.locks_dir(root) / "land.lock", blocking=False):
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
    except common.LockBusy:
        print("LAND busy detail=another session holds the land lock")
        return 3
    except LandError as exc:
        print(f"LAND error {exc}", file=sys.stderr)
        return 2

    print(f"LAND done landed={len(landed)} quarantined={len(quarantined)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
