#!/usr/bin/env python3
"""The coverage ledger: which routines every recorded session executes.

One reference routine-entry trace per session through the session's
confirmed ordinal, cached under build/completion/coverage/ and keyed by the
session's stream key and that ordinal: on a clean prefix the port matches the
ROM at every anchor, so what the ROM executes there is what the port has
proven. The native call trace undercounts (the port passes call-site
arguments directly, dispatches the sound driver's command handlers inline and
inlines helpers), so the ROM side is the measure. site/data/coverage.json is
the assembled ledger; coverage_ratchet.json holds the monotone executed count.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import scenario as scenario_module
import session
from tools.completion.revision import current_source_revision
from tools.progress.report import load_scope, resolve_scope

CACHE = ROOT / "build" / "completion" / "coverage"
LEDGER = ROOT / "site" / "data" / "coverage.json"
RATCHET = ROOT / "tools" / "completion" / "coverage_ratchet.json"
INVENTORY = ROOT / "site" / "data" / "inventory.json"
LEDGER_FORMAT = "coverage-ledger-v1"
TRACE_FORMAT = "coverage-trace-v1"
CORE_SESSIONS = ("boot-menu", "first-duel")
DEFAULT_JOBS = 4
DEFAULT_VERIFY_JOBS = 4
EXPLORE_DIR = ROOT / "build" / "completion"
DISCOVER_BUDGET = 6000
DISCOVER_JOBS = 2
DISCOVER_LIMIT = 4
INTAKE_TOP = 3
VERIFY_STATUS = {
    0: "clean",
    1: "diverged",
    2: "failed",
    3: "regression",
    4: "ref-short",
}


class CoverageError(RuntimeError):
    pass


def trace_plan(name: str) -> dict[str, Any]:
    """The session's masks, pokes, stream key and the ordinal the trace stops at."""
    masks, meta = session.load_session(name)
    ratchet = session.read_ratchet().get(name)
    if ratchet is None:
        raise CoverageError(
            f"{name} has never been verified: run `just session-verify {name}` first"
        )
    frames = session.reference_frames(masks, meta)
    return {
        "name": name,
        "masks": masks,
        "frames": frames,
        "pokes": meta["pokes"],
        "meta": meta,
        "save": meta["save"],
        "ordinals": min(len(masks), int(ratchet["confirmed_ordinal"])),
        "key": session.stream_key(
            masks, frames, "ordinal", meta["pokes"], meta["save"]
        ),
    }


def routine_files() -> tuple[dict[str, str], dict[str, str]]:
    """routine -> asm file for the whole inventory, and routine -> exclusion
    kind for the routines scope.toml removes from the denominator."""
    inventory = json.loads(INVENTORY.read_text())
    functions = inventory["functions"]
    excluded, _names, _count, _bytes = resolve_scope(load_scope(), functions, inventory)
    return (
        {name: info["file"] for name, info in functions.items()},
        {name: row["kind"] for name, row in excluded.items()},
    )


def unnameable() -> set[str]:
    """Inventory routines the reference tracer has no entry address for, so no
    replay can ever report them: the 12 the registration bijection still
    misses plus the labels whose entry the trace table does not carry (duel
    animation slots, `FadePalIntoAnother`, the Man1/legendary script
    commands). They are not coverage work and must not enter the worklist -
    closing one means registering it, not recording a session."""
    _addresses, table = refstream.routine_entry_addresses()
    named = set(table.values())
    return {name for name in routine_files()[0] if name not in named}


def ledger_sessions() -> list[str]:
    return [name for name in session.session_names() if not name.startswith("_")]


def session_seed(meta: dict[str, Any], names: set[str]) -> str | None:
    seed = meta.get("derived_from")
    return seed if isinstance(seed, str) and seed in names else None


def cache_path(name: str) -> Path:
    return CACHE / f"{name}.json"


def load_cache(name: str) -> dict[str, Any] | None:
    path = cache_path(name)
    if not path.is_file():
        return None
    record = json.loads(path.read_text())
    return record if record.get("format") == TRACE_FORMAT else None


def is_current(record: dict[str, Any] | None, plan: dict[str, Any]) -> bool:
    return (
        record is not None
        and record["key"] == plan["key"]
        and record["ordinals"] == plan["ordinals"]
    )


def trace_session(name: str) -> dict[str, Any]:
    """One reference replay through the confirmed ordinal; the cache record."""
    plan = trace_plan(name)
    inventory, _excluded = routine_files()
    routines: dict[str, list[int]] = {}
    events = 0
    if plan["ordinals"] > 0:
        trace = refstream.routine_trace(
            name,
            plan["frames"],
            None,
            ordinals=plan["ordinals"],
            masks=plan["masks"],
            axis="ordinal",
            pokes=plan["pokes"] or None,
            save=plan["save"],
        )
        if trace["ordinals_reached"] < plan["ordinals"]:
            raise CoverageError(
                f"{name}: the reference reached {trace['ordinals_reached']} of "
                f"{plan['ordinals']} ordinals"
            )
        events = trace["events"]
        routines = {
            row["routine"]: [row["count"], row["first_ordinal"]]
            for row in sorted(trace["calls"], key=lambda row: row["routine"])
            if row["routine"] in inventory
        }
    record = {
        "schema": 1,
        "format": TRACE_FORMAT,
        "session": name,
        "key": plan["key"],
        "ordinals": plan["ordinals"],
        "events": events,
        "seed": session_seed(plan["meta"], set(session.session_names())),
        "digest": hashlib.sha256("\n".join(sorted(routines)).encode()).hexdigest()[:16],
        "routines": routines,
    }
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path(name).write_text(
        json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n"
    )
    return record


def trace_worker(name: str) -> tuple[str, str]:
    command = [sys.executable, str(Path(__file__).resolve()), "trace", name]
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return name, result.stderr.strip()[-400:] or f"exit {result.returncode}"
    return name, ""


def collect(
    names: list[str], *, jobs: int, forced: set[str]
) -> dict[str, dict[str, Any]]:
    """Every named session's trace record, tracing the stale and the forced
    ones in worker processes, one reference core each."""
    plans: dict[str, dict[str, Any]] = {}
    pending: list[str] = []
    for name in names:
        try:
            plans[name] = trace_plan(name)
        except CoverageError:
            pending.append(name)
    if pending:
        print(
            f"SKIP unverified={len(pending)}: {', '.join(pending[:6])}", file=sys.stderr
        )
    records: dict[str, dict[str, Any]] = {}
    stale: list[str] = []
    for name, plan in plans.items():
        record = load_cache(name)
        if name not in forced and is_current(record, plan):
            records[name] = record
        else:
            stale.append(name)
    if stale:
        stale.sort(key=lambda name: -plans[name]["ordinals"])
        print(f"TRACE sessions={len(stale)} jobs={jobs}", file=sys.stderr)
        failures: list[str] = []
        with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
            for name, failure in pool.map(trace_worker, stale):
                if failure:
                    failures.append(f"{name}: {failure}")
                    continue
                record = load_cache(name)
                if not is_current(record, plans[name]):
                    failures.append(f"{name}: the worker left no current trace")
                    continue
                records[name] = record
                print(
                    f"TRACED {name} ordinals={record['ordinals']} "
                    f"routines={len(record['routines'])}",
                    file=sys.stderr,
                )
        if failures:
            raise CoverageError("; ".join(failures))
    return records


def assemble(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    files, excluded = routine_files()
    names = sorted(records)
    index = {name: position for position, name in enumerate(names)}
    known = set(names)
    by_routine: dict[str, list[int]] = {}
    for name in names:
        for routine in records[name]["routines"]:
            by_routine.setdefault(routine, []).append(index[name])
    routines: dict[str, dict[str, Any]] = {}
    per_file: dict[str, dict[str, int]] = {}
    blind = unnameable()
    for routine in sorted(files):
        entry: dict[str, Any] = {
            "file": files[routine],
            "sessions": by_routine.get(routine, []),
        }
        if routine in excluded:
            entry["excluded"] = excluded[routine]
        elif routine in blind:
            entry["unmeasurable"] = "tracer-unnamed"
        routines[routine] = entry
        if routine in excluded:
            continue
        row = per_file.setdefault(files[routine], {"executed": 0, "total": 0})
        row["total"] += 1
        if routine in blind:
            row["unmeasurable"] = row.get("unmeasurable", 0) + 1
        if entry["sessions"]:
            row["executed"] += 1
    executed = sum(row["executed"] for row in per_file.values())
    total = sum(row["total"] for row in per_file.values())
    sessions = {}
    for name in names:
        record = records[name]
        sessions[name] = {
            "routines": len(record["routines"]),
            "ordinals": record["ordinals"],
            "digest": record["digest"],
            "events": record["events"],
            "seed": record.get("seed") if record.get("seed") in known else None,
        }
    return {
        "schema": 1,
        "format": LEDGER_FORMAT,
        "revision": current_source_revision(ROOT),
        "generated": datetime.now(UTC).isoformat(timespec="seconds"),
        "totals": {
            "executed": executed,
            "total": total,
            "sessions": len(names),
            "excluded": len(excluded),
        },
        "session_order": names,
        "sessions": sessions,
        "files": {file: per_file[file] for file in sorted(per_file)},
        "routines": routines,
    }


def load_ledger() -> dict[str, Any]:
    if not LEDGER.is_file():
        raise CoverageError(
            f"no ledger at {LEDGER.relative_to(ROOT)}: run `just coverage-ledger`"
        )
    ledger = json.loads(LEDGER.read_text())
    if ledger.get("format") != LEDGER_FORMAT:
        raise CoverageError(
            f"{LEDGER.relative_to(ROOT)} is not a {LEDGER_FORMAT} ledger"
        )
    return ledger


def executed_set(ledger: dict[str, Any]) -> set[str]:
    return {
        routine for routine, entry in ledger["routines"].items() if entry["sessions"]
    }


def unexecuted(ledger: dict[str, Any]) -> dict[str, str]:
    """routine -> file for every in-scope routine no session executes and a
    replay could report. `unmeasurable` routines are held out: the reference
    tracer has no entry address for them, so they are a registration gap, not
    a coverage gap (`unnameable`)."""
    return {
        routine: entry["file"]
        for routine, entry in ledger["routines"].items()
        if not entry["sessions"]
        and "excluded" not in entry
        and "unmeasurable" not in entry
    }


def unmeasurable(ledger: dict[str, Any]) -> dict[str, str]:
    """routine -> reason for the routines no replay can report."""
    return {
        routine: entry["unmeasurable"]
        for routine, entry in ledger["routines"].items()
        if entry.get("unmeasurable")
    }


def read_ratchet() -> dict[str, int]:
    return json.loads(RATCHET.read_text()) if RATCHET.is_file() else {}


def apply_ratchet(ledger: dict[str, Any], *, write: bool) -> int:
    executed = ledger["totals"]["executed"]
    previous = read_ratchet().get("executed")
    if previous is not None and executed < previous and not write:
        print(f"REGRESSION coverage key=executed was={previous} now={executed}")
        return 3
    if previous is None or executed > previous or write:
        RATCHET.write_text(
            json.dumps({"executed": executed}, indent=2, sort_keys=True) + "\n"
        )
    return 0


def expand_targets(ledger: dict[str, Any], targets: list[str]) -> list[str]:
    """Routine names as given; a name that is an inventory file's stem instead
    (`effect_functions`) expands to every routine of that file."""
    routines = ledger["routines"]
    by_stem: dict[str, list[str]] = {}
    for routine, entry in routines.items():
        by_stem.setdefault(Path(entry["file"]).stem, []).append(routine)
    out: list[str] = []
    for target in targets:
        if target in routines:
            out.append(target)
        elif target in by_stem:
            out.extend(by_stem[target])
        else:
            raise CoverageError(
                f"{target} names neither an inventory routine nor an asm file stem"
            )
    return out


def affected(ledger: dict[str, Any], routines: list[str]) -> list[str]:
    """The sessions a change to `routines` can move: every session executing
    one of them, the sessions they were branched from, and the core set."""
    names = ledger["session_order"]
    hit: set[str] = set()
    for routine in routines:
        hit.update(
            names[position] for position in ledger["routines"][routine]["sessions"]
        )
    pending = list(hit)
    while pending:
        seed = ledger["sessions"][pending.pop()].get("seed")
        if seed and seed not in hit:
            hit.add(seed)
            pending.append(seed)
    hit.update(core for core in CORE_SESSIONS if core in ledger["sessions"])
    return sorted(hit, key=lambda name: (ledger["sessions"][name]["ordinals"], name))


def build(names: list[str], *, jobs: int, forced: set[str], write_ratchet: bool) -> int:
    records = collect(names, jobs=jobs, forced=forced)
    ledger = assemble(records)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, separators=(",", ":"), sort_keys=True) + "\n")
    totals = ledger["totals"]
    print(
        f"LEDGER sessions={totals['sessions']} executed={totals['executed']} "
        f"total={totals['total']} excluded={totals['excluded']} "
        f"unexecuted={totals['total'] - totals['executed']}"
    )
    return apply_ratchet(ledger, write=write_ratchet)


def status(limit: int) -> int:
    ledger = load_ledger()
    totals = ledger["totals"]
    blind = unmeasurable(ledger)
    print(
        f"LEDGER revision={ledger['revision'][:12]} sessions={totals['sessions']} "
        f"executed={totals['executed']}/{totals['total']}"
    )
    if blind:
        print(
            f"UNMEASURABLE routines={len(blind)} reason=tracer-unnamed "
            f"(a registration gap, not coverage: {', '.join(sorted(blind)[:4])}, ...)"
        )
    frontier = target_frontier(ledger, [])
    if frontier["stale"]:
        raise CoverageError(
            "target records disagree with recorded sessions: "
            + "; ".join(frontier["stale"])
        )
    print(
        f"PRODUCER target pending_groups={len(frontier['pending'])} "
        f"attempted_groups={len(frontier['attempted'])}"
    )
    rows = sorted(
        ledger["files"].items(),
        key=lambda row: (row[1]["executed"] - row[1]["total"], row[0]),
    )
    for file, row in rows[:limit]:
        miss = row["total"] - row["executed"]
        if miss == 0:
            break
        print(
            f"FILE miss={miss} executed={row['executed']}/{row['total']} {file}"
            + (
                f" unmeasurable={row['unmeasurable']}"
                if row.get("unmeasurable")
                else ""
            )
        )
    return 0


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _lane_files(root: Path) -> tuple[Path, Path]:
    if root.resolve() == ROOT.resolve():
        return scenario_module.BINARY, scenario_module.PACK
    return (
        root / "build" / "poketcg",
        root / "build" / "completion" / "data-pack.bin",
    )


def _lane_manifest(scope: str, *, root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    binary, pack = _lane_files(root)
    if not binary.is_file() or not pack.is_file():
        raise CoverageError(
            f"no lane to freeze: build {binary.name} and the data pack first"
        )
    return {
        "schema": "native-lane-input-v1",
        "scope": scope,
        "binary": {
            "path": binary.relative_to(root).as_posix(),
            "sha256": _file_sha256(binary),
        },
        "pack": {
            "path": pack.relative_to(root).as_posix(),
            "sha256": _file_sha256(pack),
        },
    }


def freeze_lane(
    *, destination: Path, manifest: dict[str, Any], source_root: Path = ROOT
) -> Path:
    source_root = source_root.resolve()
    binary, pack = _lane_files(source_root)
    if not binary.is_file() or not pack.is_file():
        raise CoverageError(
            f"no lane to freeze: build {binary.name} and the data pack first"
        )
    destination = destination.resolve()
    request = json.loads(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    if destination.exists():
        existing = destination / "manifest.json"
        try:
            stored = json.loads(existing.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise CoverageError(
                f"frozen lane is malformed: {destination}: {exc}"
            ) from exc
        if stored.get("request") != request:
            raise CoverageError(f"refusing to overwrite frozen lane: {destination}")
        files = stored.get("files", {})
        if not isinstance(files, dict):
            raise CoverageError(f"frozen lane files are malformed: {destination}")
        for relative, expected in files.items():
            path = destination / relative
            if (
                not isinstance(expected, str)
                or not path.is_file()
                or _file_sha256(path) != expected
            ):
                raise CoverageError(f"frozen lane content differs: {path}")
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = (
        destination.parent / f".{destination.name}.{os.getpid()}.{time.monotonic_ns()}"
    )
    try:
        (temporary / "completion").mkdir(parents=True)
        binary_before = _file_sha256(binary)
        pack_before = _file_sha256(pack)
        binary_destination = temporary / binary.name
        pack_destination = temporary / "completion" / pack.name
        shutil.copy2(binary, binary_destination)
        shutil.copy2(pack, pack_destination)
        binary_after = _file_sha256(binary)
        pack_after = _file_sha256(pack)
        files = {
            binary_destination.relative_to(temporary).as_posix(): _file_sha256(
                binary_destination
            ),
            pack_destination.relative_to(temporary).as_posix(): _file_sha256(
                pack_destination
            ),
        }
        if binary_before != binary_after or pack_before != pack_after:
            raise CoverageError("source lane changed while freezing")
        if files[binary_destination.relative_to(temporary).as_posix()] != binary_before:
            raise CoverageError("binary copy is torn")
        if files[pack_destination.relative_to(temporary).as_posix()] != pack_before:
            raise CoverageError("data pack copy is torn")
        lane = {
            "schema": "frozen-lane-v1",
            "request": request,
            "files": files,
        }
        (temporary / "manifest.json").write_text(
            json.dumps(lane, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, destination)
    except BaseException:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
    return destination


def current_frozen_lane(scope: str, *, root: Path = ROOT) -> Path:
    root = root.resolve()
    manifest = _lane_manifest(scope, root=root)
    digest = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return freeze_lane(
        destination=root / ".factory" / "runtime" / "lanes" / digest,
        manifest=manifest,
        source_root=root,
    )


def verify_worker(
    name: str,
    lane: Path,
    ratchet: bool = False,
    publish: bool = True,
) -> tuple[str, int, str]:
    command = [
        sys.executable,
        str(ROOT / "tools" / "completion" / "session.py"),
        "verify",
        name,
    ]
    if ratchet:
        command.append("--write-ratchet")
    if not publish:
        command.append("--no-publish")
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env=dict(os.environ, POKETCG_BUILD=str(lane.relative_to(ROOT))),
    )
    lines = [
        line
        for line in result.stdout.splitlines()
        if line.startswith(("SESSION", "REGRESSION", "NATIVE", "SCHEDULE", "WINDOW"))
    ]
    return name, result.returncode, "\n".join(lines) or result.stderr.strip()[-300:]


def verify_affected(
    names: list[str],
    *,
    jobs: int = DEFAULT_VERIFY_JOBS,
    sample: int = 0,
    ratchet: bool = False,
    publish: bool = True,
) -> int:
    ledger = load_ledger()
    ordered = sorted(
        names, key=lambda name: ledger["sessions"].get(name, {}).get("ordinals", 0)
    )
    if sample:
        ordered = ordered[:sample]
    lane = current_frozen_lane("verify-affected")
    worst = 0
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for name, code, text in pool.map(
            lambda name: verify_worker(name, lane, ratchet, publish),
            ordered,
        ):
            worst = max(worst, code)
            for line in text.splitlines():
                if not line.startswith("SESSION") or "status=clean" not in line:
                    print(line)
            if code == 0:
                print(f"CLEAN {name}")
    print(f"AFFECTED sessions={len(ordered)} jobs={jobs} exit={worst}")
    return worst


def executed_digest(ledger: dict[str, Any]) -> str:
    return hashlib.sha256("\n".join(sorted(executed_set(ledger))).encode()).hexdigest()[
        :16
    ]


def explore_paths(seed: str) -> tuple[Path, Path]:
    return EXPLORE_DIR / f"explore-{seed}.json", EXPLORE_DIR / f"explore-{seed}"


def discover_producer_key(seed: str, *, budget: int = DISCOVER_BUDGET) -> str:
    masks, meta = session.load_session(seed)
    pokes = refstream.pokes_text(meta.get("pokes") or {})
    save = meta.get("save") or b""
    if not isinstance(save, bytes):
        raise CoverageError(f"{seed} has malformed save input")
    inputs = hashlib.sha256(
        bytes(mask & 0xFF for mask in masks) + pokes.encode() + save
    ).hexdigest()
    runtime = {
        relative: _file_sha256(ROOT / relative) if (ROOT / relative).is_file() else None
        for relative in (
            "poketcg/poketcg.gbc",
            "tools/completion/gambatte_pins.toml",
            "tools/completion/coverage_ledger.py",
            "tools/completion/explore.py",
            "tools/completion/refstream.py",
            "tools/completion/session.py",
        )
    }
    return hashlib.sha256(
        json.dumps(
            {
                "schema": "coverage-discover-producer-v2",
                "seed": seed,
                "inputs": inputs,
                "runtime": runtime,
                "action_vocabulary": runtime["tools/completion/explore.py"],
                "budget": budget,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def corpus_current(seed: str, digest: str) -> bool:
    json_path, corpus = explore_paths(seed)
    index_path = corpus / "corpus.json"
    if not json_path.is_file() or not index_path.is_file():
        return False
    try:
        summary = json.loads(json_path.read_text())
        entries = json.loads(index_path.read_text()).get("entries", [])
    except (json.JSONDecodeError, OSError):
        return False
    return summary.get("producer_key") == digest and all(
        isinstance(entry, dict) and "routines" in entry for entry in entries
    )


def session_total(name: str) -> int:
    """The session's own length, which the ledger's confirmed-capped `ordinals` is not."""
    path = session.session_dir(name) / "session.json"
    if path.is_file():
        total = json.loads(path.read_text()).get("ordinals")
        if isinstance(total, int) and total > 0:
            return total
    return len(session.load_session(name)[0])


def is_clean(name: str) -> bool:
    return session.read_ratchet().get(name, {}).get(
        "confirmed_ordinal", 0
    ) >= session_total(name)


EXPLORE_TIMEOUT = 2700


def ledger_ordinals(seed: str) -> int:
    return int(load_ledger()["sessions"].get(seed, {}).get("ordinals", 0))


REPLAY_UNIT = 25_000


def rank_seeds(ledger: dict[str, Any]) -> list[tuple[str, int]]:
    """Sessions by unexecuted routines in the files they touch, divided by what
    a search from them costs: every expansion replays the seed's timeline, so a
    876k-ordinal route pays ~35x a 23k one for the same screens. Ranking on the
    raw count alone picked `credits-1` and spent 40 minutes on zero expansions."""
    missing: dict[str, int] = {}
    for file in unexecuted(ledger).values():
        missing[file] = missing.get(file, 0) + 1
    names = ledger["session_order"]
    files: dict[str, set[str]] = {name: set() for name in names}
    for entry in ledger["routines"].values():
        for position in entry["sessions"]:
            files[names[position]].add(entry["file"])
    rows = []
    for name, touched in files.items():
        reach = sum(missing.get(file, 0) for file in touched) if is_clean(name) else 0
        ordinals = ledger["sessions"][name].get("ordinals", 0)
        score = round(reach * REPLAY_UNIT / (REPLAY_UNIT + ordinals))
        rows.append((name, score))
    rows.sort(
        key=lambda row: (-row[1], ledger["sessions"][row[0]].get("ordinals", 0), row[0])
    )
    return rows


def explore_seed(seed: str, *, budget: int, digest: str) -> tuple[str, str, str]:
    json_path, corpus = explore_paths(seed)
    if corpus_current(seed, digest):
        return seed, "cached", str(corpus.relative_to(ROOT))
    command = [
        sys.executable,
        str(ROOT / "tools" / "completion" / "explore.py"),
        "--seed-session",
        seed,
        "--budget",
        str(budget),
        "--known",
        str(LEDGER),
        "--corpus",
        str(corpus),
        "--json",
        str(json_path),
    ]
    started = time.monotonic()
    print(
        f"DISCOVER start {seed} ordinals={ledger_ordinals(seed)} budget={budget}",
        file=sys.stderr,
        flush=True,
    )
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=EXPLORE_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return seed, "timeout", f"no result in {EXPLORE_TIMEOUT}s"
    if result.returncode != 0 or not json_path.is_file():
        return (
            seed,
            "failed",
            f"{time.monotonic() - started:.0f}s {result.stderr.strip()[-360:]}",
        )
    data = json.loads(json_path.read_text())
    data["seed_session"] = seed
    data["producer_key"] = digest
    data["scored_ledger_digest"] = executed_digest(load_ledger())
    json_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return (
        seed,
        "explored",
        f"new={data['new']} entries={data.get('corpus_entries', 0)} seconds={data['seconds']}",
    )


def distinct_prefixes(
    ledger: dict[str, Any], ranked: list[str], limit: int
) -> list[str]:
    """One seed per replayed prefix. Every `effect-*` seed is the same
    practice-win branch with a different deck, so two of them search the same
    screens and the second's discoveries are all duplicates the intake drops."""
    picked: list[str] = []
    seen: set[str] = set()
    for name in ranked:
        entry = ledger["sessions"][name]
        family = entry.get("seed") or name
        if family in seen:
            continue
        seen.add(family)
        picked.append(name)
        if len(picked) >= limit:
            break
    return picked


def discover_frontier(ledger: dict[str, Any], limit: int) -> tuple[str, list[str]]:
    """The ranked seeds whose producer inputs have no reusable corpus."""
    digest = executed_digest(ledger)
    ranked = [name for name, score in rank_seeds(ledger) if score > 0]
    fresh = [
        name for name in ranked if not corpus_current(name, discover_producer_key(name))
    ]
    seeds = distinct_prefixes(ledger, fresh, limit) if limit else fresh
    return digest, seeds


def discover(seeds: list[str], *, budget: int, jobs: int, limit: int) -> int:
    ledger = load_ledger()
    scored_digest = executed_digest(ledger)
    unknown = sorted(set(seeds) - set(ledger["sessions"]))
    if unknown:
        raise CoverageError(f"not in the ledger: {', '.join(unknown)}")
    if not seeds:
        _digest, seeds = discover_frontier(ledger, limit)
    if not seeds:
        print(
            f"DISCOVER scope=coverage ledger={scored_digest} seeds=0: every ranked seed has a corpus at this ledger"
        )
        return 0
    print(
        f"DISCOVER scope=coverage ledger={scored_digest} seeds={len(seeds)} budget={budget} jobs={jobs}",
        file=sys.stderr,
    )
    failed = 0
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for seed, outcome, detail in pool.map(
            lambda seed: explore_seed(
                seed,
                budget=budget,
                digest=discover_producer_key(seed, budget=budget),
            ),
            seeds,
        ):
            print(f"DISCOVER scope=coverage {seed} {outcome} {detail}")
            failed += outcome in {"failed", "timeout"}
    return 1 if failed else 0


def next_session_name(seed: str) -> str:
    existing = set(session.session_names())
    k = 1
    while f"{seed}-explore-{k}" in existing:
        k += 1
    return f"{seed}-explore-{k}"


def commit_line(name: str) -> list[str]:
    return [
        "jj",
        "commit",
        f"tests/sessions/{name}",
        "tools/completion/session_ratchet.json",
        "-m",
        f"feat(session): record {name}",
    ]


def session_save_digest(name: str) -> str:
    save = session.session_dir(name) / session.SAVE_FILE
    return hashlib.sha256(save.read_bytes() if save.is_file() else b"").hexdigest()


def recorded_script_identities() -> set[tuple[str, str]]:
    identities: set[tuple[str, str]] = set()
    for name in session.session_names():
        metadata = session.session_dir(name) / "session.json"
        if not metadata.is_file():
            continue
        input_digest = json.loads(metadata.read_text()).get("input_sha256")
        if isinstance(input_digest, str):
            identities.add((input_digest, session_save_digest(name)))
    return identities


def script_identity(
    seed: str, script: Path, seed_data: tuple[list[int], dict[str, Any]] | None = None
) -> tuple[str, str]:
    seed_masks, seed_meta = seed_data or session.load_session(seed)
    masks = refstream.load_masks(script)
    if masks[: len(seed_masks)] != seed_masks:
        raise CoverageError(
            f"{script} does not start with {seed}'s {len(seed_masks)} ordinals"
        )
    poke_text = refstream.pokes_text(seed_meta.get("pokes") or {})
    input_digest = hashlib.sha256(
        bytes(mask & 0xFF for mask in masks) + poke_text.encode()
    ).hexdigest()
    save_digest = hashlib.sha256(seed_meta.get("save") or b"").hexdigest()
    return input_digest, save_digest


def intake_entries(
    seed: str, ledger: dict[str, Any]
) -> tuple[Path, list[dict[str, Any]]]:
    if not is_clean(seed):
        confirmed = session.read_ratchet().get(seed, {}).get("confirmed_ordinal", 0)
        raise CoverageError(
            f"{seed} is diverged at {confirmed + 1} of {session_total(seed)}: a session extending it "
            f"can only re-report that fact. Fix it first, or intake from a clean seed."
        )
    _json_path, corpus = explore_paths(seed)
    index = corpus / "corpus.json"
    if not index.is_file():
        raise CoverageError(
            f"no corpus for {seed}: run `just coverage-discover {seed}`"
        )
    entries = json.loads(index.read_text()).get("entries", [])
    if any("routines" not in entry for entry in entries):
        raise CoverageError(
            f"{index.relative_to(ROOT)} predates ledger scoring: rerun `just coverage-discover {seed}`"
        )
    missing = set(unexecuted(ledger))
    recorded = recorded_script_identities()
    seed_data = session.load_session(seed)
    eligible = [
        entry
        for entry in entries
        if set(entry["routines"]) & missing
        and script_identity(seed, corpus / entry["script"], seed_data) not in recorded
    ]
    return corpus, eligible


def intake(seed: str, *, top: int, land: bool) -> int:
    """Record the seed's unrecorded scripts that add the most missing routines."""
    ledger = load_ledger()
    corpus, remaining = intake_entries(seed, ledger)
    covered = executed_set(ledger)
    chosen: list[tuple[dict[str, Any], int]] = []
    while remaining and len(chosen) < top:
        best = max(
            remaining,
            key=lambda entry: (len(set(entry["routines"]) - covered), -entry["frames"]),
        )
        gain = len(set(best["routines"]) - covered)
        if gain == 0:
            break
        chosen.append((best, gain))
        covered |= set(best["routines"])
        remaining.remove(best)
    if not chosen:
        print(
            f"INTAKE {seed} scripts=0: no unrecorded script reaches a routine the ledger lacks"
        )
        return 0
    worst = 0
    for entry, gain in chosen:
        name = next_session_name(seed)
        try:
            session.from_script(
                name, seed=seed, script=corpus / entry["script"], goal=""
            )
        except session.SessionError as exc:
            print(f"INTAKE {seed} skip script={entry['script']}: {exc}")
            continue
        code = session.verify(name, write=False, json_path=None, publish=False)
        print(
            f"INTAKE {name} script={entry['script']} gain={gain} verify={VERIFY_STATUS.get(code, code)}"
        )
        if code in (2, 4):
            worst = max(worst, code)
            continue
        land_session(name, land=land)
    return worst


def intake_one(
    seed: str,
    *,
    input_sha256: str,
    save_sha256: str,
) -> dict[str, Any]:
    """Materialize and verify one previously selected corpus script.

    The controller passes both script identities from its descriptor.  This
    refuses to substitute a newly ranked script after an interrupted run.
    """
    ledger = load_ledger()
    corpus, entries = intake_entries(seed, ledger)
    covered = executed_set(ledger)
    seed_data = session.load_session(seed)
    candidates: list[tuple[int, int, str, dict[str, Any]]] = []
    for entry in entries:
        script = corpus / str(entry.get("script", ""))
        try:
            input_digest, save_digest = script_identity(seed, script, seed_data)
        except (CoverageError, OSError, ValueError):
            continue
        if (input_digest, save_digest) != (input_sha256, save_sha256):
            continue
        routines = entry.get("routines", [])
        if not isinstance(routines, list) or not all(
            isinstance(routine, str) for routine in routines
        ):
            continue
        gain = len(set(routines) - covered)
        frames = int(entry.get("frames", 0) or 0)
        candidates.append((gain, frames, script.as_posix(), entry))
    if not candidates:
        raise CoverageError(
            f"no unseen corpus script for {seed} with the requested identities"
        )
    _gain, _frames, _script_name, entry = sorted(
        candidates,
        key=lambda row: (-row[0], row[1], row[2]),
    )[0]
    script = corpus / str(entry["script"])
    name = next_session_name(seed)
    session.from_script(
        name, seed=seed, script=script, goal=session.script_goal(seed, script)
    )
    code = session.verify(name, write=False, json_path=None, publish=False)
    return {
        "seed": seed,
        "session": name,
        "script": str(script.relative_to(ROOT)),
        "input_sha256": input_sha256,
        "save_sha256": save_sha256,
        "coverage_gain": _gain,
        "frames": _frames,
        "verify": code,
    }


def land_session(name: str, *, land: bool) -> None:
    command = commit_line(name)
    if land:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            raise CoverageError(
                f"landing {name} failed: {result.stderr.strip()[-300:]}"
            )
        print(f"LANDED {name}")
    else:
        print(
            "COMMIT "
            + " ".join(f"'{part}'" if " " in part else part for part in command)
        )


TARGETS_PATH = ROOT / "build" / "completion" / "effects" / "targets.json"
TARGET_BASE = "practice-win"
TARGET_AT = 23227
TARGET_OPPONENT = 2
TARGET_PRIZES = 6
TARGET_STALL_PRIZES = 2


def session_slug(card: str) -> str:
    return card.lower().replace("_", "-")


def target_name(card: str, slot: int | None, ai: bool) -> str:
    suffix = f"-{slot}" if slot else ""
    if ai:
        suffix += "-ai"
    return f"effect-{session_slug(card)}{suffix}"


def load_target_records() -> dict[str, dict[str, Any]]:
    return json.loads(TARGETS_PATH.read_text()) if TARGETS_PATH.is_file() else {}


def target_groups(
    ledger: dict[str, Any],
    names: list[str],
    by_routine: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[tuple[str, int | None, bool], set[str]]:
    if by_routine is None:
        import effects

        by_routine = effects.load_map()["by_routine"]
    wanted = expand_targets(ledger, names) if names else sorted(unexecuted(ledger))
    groups: dict[tuple[str, int | None, bool], set[str]] = {}
    for routine in wanted:
        carriers = by_routine.get(routine)
        if not carriers or ledger["routines"][routine]["sessions"]:
            continue
        carrier = carriers[0]
        slot = (
            int(carrier["slot"][-1]) if carrier["slot"].startswith("attack") else None
        )
        ai = carrier["command"] == "EFFECTCMDTYPE_AI_SELECTION"
        groups.setdefault((carrier["card"], slot, ai), set()).add(routine)
    return groups


def target_frontier(
    ledger: dict[str, Any],
    names: list[str],
    *,
    records: dict[str, dict[str, Any]] | None = None,
    existing: set[str] | None = None,
    by_routine: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, list[tuple[str, int | None, list[str], bool]] | list[str]]:
    records = load_target_records() if records is None else records
    existing = set(session.session_names()) if existing is None else existing
    pending: list[tuple[str, int | None, list[str], bool]] = []
    attempted: list[tuple[str, int | None, list[str], bool]] = []
    stale: list[str] = []
    groups = target_groups(ledger, names, by_routine)
    for (card, slot, ai), routines_set in sorted(
        groups.items(), key=lambda item: (-len(item[1]), item[0])
    ):
        routines = sorted(routines_set)
        recorded = [records[routine] for routine in routines if routine in records]
        for row in recorded:
            recorded_session = row.get("session")
            if (
                not isinstance(recorded_session, str)
                or recorded_session not in existing
            ):
                stale.append(
                    f"{card}:{slot or 'trainer'} record points to {recorded_session!r}"
                )
        name = target_name(card, slot, ai)
        item = (card, slot, routines, ai)
        if recorded or name in existing or f"{name}-seed" in existing:
            attempted.append(item)
        else:
            pending.append(item)
    return {"pending": pending, "attempted": attempted, "stale": stale}


def ensure_target_destinations_available(name: str) -> None:
    collisions = [
        candidate
        for candidate in (name, f"{name}-seed")
        if session.session_dir(candidate).exists()
    ]
    if collisions:
        raise CoverageError(
            "refusing to overwrite recorded target session(s): " + ", ".join(collisions)
        )


def target_one(
    card: str, slot: int | None, routines: list[str], ai: bool = False
) -> dict[str, Any]:
    import effects

    name = target_name(card, slot, ai)
    ensure_target_destinations_available(name)
    deck = effects.build_deck(card, attack_slot=slot)
    deck_path = TARGETS_PATH.parent / f"{name}.deck"
    deck_path.parent.mkdir(parents=True, exist_ok=True)
    deck_path.write_text("\n".join(str(c) for c in deck) + "\n")
    goal = (
        (
            f"Card effect target: {card} attack {slot}"
            if slot
            else f"Card effect target: {card}"
        )
        + (" AI selection" if ai else "")
        + f" ({', '.join(sorted(routines)[:4])})"
    )
    options = {
        "seed": 1 if ai else None,
        "prizes": 1 if ai else TARGET_PRIZES,
        "period": 8 if ai else 24,
        "tail": 3000 if ai else 1500,
    }
    session.session_dir(name).mkdir()
    try:
        session.ai_duel(
            name,
            base=TARGET_BASE,
            at=TARGET_AT,
            deck=TARGET_OPPONENT,
            goal=goal,
            cards=deck,
            watch=set(routines),
            arrange=True,
            **options,
        )
    except session.SessionError as exc:
        if "did not finish" not in str(exc):
            raise
        stall_options = dict(options)
        stall_options["prizes"] = TARGET_STALL_PRIZES
        session.ai_duel(
            name,
            base=TARGET_BASE,
            at=TARGET_AT,
            deck=TARGET_OPPONENT,
            goal=goal,
            cards=deck,
            watch=set(routines),
            arrange=True,
            **stall_options,
        )
    watched = json.loads((session.session_dir(name) / "session.json").read_text())[
        "watched"
    ]
    reached = {
        routine: ordinal for routine, ordinal in watched.items() if ordinal is not None
    }
    if not reached:
        for path in session.session_dir(name).iterdir():
            path.unlink()
        session.session_dir(name).rmdir()
        name = f"{name}-seed"
        session.session_dir(name).mkdir()
        session.deck_seed(
            name,
            base=TARGET_BASE,
            at=TARGET_AT,
            deck=TARGET_OPPONENT,
            cards=deck,
            goal=f"Search seed: {card} in hand, the AI never played it "
            f"({', '.join(sorted(routines)[:4])})",
        )
    code = session.verify(name, write=False, json_path=None, publish=False)
    return {
        "card": card,
        "slot": slot,
        "ai": ai,
        "session": name,
        "routines": sorted(routines),
        "reached": reached,
        "deck": str(deck_path.relative_to(ROOT)),
        "verify": code,
    }


def target_worker(
    item: tuple[str, int | None, list[str], bool], lane: Path
) -> dict[str, Any]:
    card, slot, routines, ai = item
    command = [
        sys.executable,
        str(ROOT / "tools" / "completion" / "coverage_ledger.py"),
        "target-one",
        card,
        "--routines",
        ",".join(routines),
    ]
    if slot:
        command += ["--slot", str(slot)]
    if ai:
        command.append("--ai")
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        env=dict(os.environ, POKETCG_BUILD=str(lane.relative_to(ROOT))),
    )
    for line in reversed(result.stdout.splitlines()):
        if line.startswith("{"):
            return json.loads(line)
    return {
        "card": card,
        "slot": slot,
        "ai": ai,
        "session": None,
        "routines": routines,
        "error": (result.stderr.strip() or result.stdout.strip())[-300:],
    }


def target(
    names: list[str], *, land: bool, limit: int, jobs: int = DEFAULT_VERIFY_JOBS
) -> int:
    ledger = load_ledger()
    frontier = target_frontier(ledger, names)
    stale = frontier["stale"]
    if stale:
        raise CoverageError(
            "target records disagree with recorded sessions: " + "; ".join(stale)
        )
    pending = frontier["pending"]
    attempted = frontier["attempted"]
    queue = pending[:limit] if limit else pending
    if not queue:
        attempted_routines = sum(len(item[2]) for item in attempted)
        print(
            f"TARGET scope=coverage none: pending=0 attempted_groups={len(attempted)} "
            f"attempted_routines={attempted_routines}; this producer is exhausted. "
            "Run `just coverage-next`."
        )
        return 0
    record = load_target_records()
    lane = current_frozen_lane("target")
    worst = 0
    print(
        f"TARGET scope=coverage carriers={len(queue)} pending={len(pending)} jobs={jobs}",
        file=sys.stderr,
    )
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for row in pool.map(lambda item: target_worker(item, lane), queue):
            if row.get("error"):
                print(
                    f"TARGET scope=coverage error card={row['card']} slot={row['slot']}: {row['error']}"
                )
                worst = max(worst, 2)
                continue
            for routine in row["routines"]:
                record[routine] = {
                    "card": row["card"],
                    "slot": row["slot"],
                    "ai": row.get("ai", False),
                    "session": row["session"],
                    "reached": row["reached"].get(routine),
                    "deck": row["deck"],
                }
            TARGETS_PATH.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
            code = row["verify"]
            print(
                f"TARGET scope=coverage {row['session']} card={row['card']} routines={len(row['routines'])} "
                f"reached={len(row['reached'])} verify={VERIFY_STATUS.get(code, code)}"
            )
            if code in (2, 4):
                worst = max(worst, code)
                continue
            land_session(row["session"], land=land)
    return worst


def current_intake_seed(ledger: dict[str, Any]) -> str | None:
    for seed, score in rank_seeds(ledger):
        if score <= 0 or not corpus_current(seed, discover_producer_key(seed)):
            continue
        _corpus, entries = intake_entries(seed, ledger)
        if entries:
            return seed
    return None


def workflow_frontier(limit: int = 4) -> dict[str, Any]:
    ledger = load_ledger()
    targets = target_frontier(ledger, [])
    intake_seed = current_intake_seed(ledger)
    ledger_digest, discover = discover_frontier(ledger, limit)
    return {
        "scope": "coverage",
        "ledger_digest": ledger_digest,
        "targets": targets,
        "intake_seed": intake_seed,
        "discover": discover,
        "missing": sorted(unexecuted(ledger)),
        "unmeasurable": sorted(unmeasurable(ledger)),
    }


def choose_coverage_step(
    *,
    missing: int,
    pending_targets: int,
    intake_seed: str | None,
    discover_seeds: list[str],
    attempted_targets: int,
) -> tuple[str, int, str]:
    """Pure decision table for the coverage producers."""
    if pending_targets:
        return ("target", 0, "just coverage-target --limit 20 --land")
    if intake_seed is not None:
        return ("intake", 0, f"just coverage-intake {intake_seed} --top 3 --land")
    if discover_seeds:
        return ("discover", 0, "just coverage-discover --limit 2 --jobs 2")
    if missing == 0:
        return ("done", 2, "all in-scope routines have recorded coverage")
    return (
        "gate",
        3,
        (
            f"{missing} in-scope routines remain; target exhausted "
            f"({attempted_targets} attempted groups), and no intake or discovery work remains"
        ),
    )


def next_action() -> int:
    ledger = load_ledger()
    missing = len(unexecuted(ledger))
    frontier = target_frontier(ledger, [])
    stale = frontier["stale"]
    if stale:
        raise CoverageError(
            "target records disagree with recorded sessions: " + "; ".join(stale)
        )
    intake_seed = current_intake_seed(ledger)
    _digest, discover_seeds = discover_frontier(ledger, 2)
    kind, code, detail = choose_coverage_step(
        missing=missing,
        pending_targets=len(frontier["pending"]),
        intake_seed=intake_seed,
        discover_seeds=discover_seeds,
        attempted_targets=len(frontier["attempted"]),
    )
    print(f"NEXT scope=coverage kind={kind} missing={missing} detail={detail}")
    return code


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    ledger_parser = sub.add_parser(
        "ledger", help="trace stale sessions and rebuild the ledger"
    )
    ledger_parser.add_argument(
        "names", nargs="*", help="sessions to retrace even when their cache is current"
    )
    ledger_parser.add_argument("--jobs", type=int, default=DEFAULT_JOBS)
    ledger_parser.add_argument(
        "--force", action="store_true", help="retrace every session"
    )
    ledger_parser.add_argument(
        "--write-ratchet", action="store_true", help="accept a lower executed count"
    )
    status_parser = sub.add_parser(
        "status", help="files ranked by routines no session executes"
    )
    status_parser.add_argument("--limit", type=int, default=20)
    sub.add_parser(
        "next", help="print the next coverage producer, done, or decision gate"
    )
    affected_parser = sub.add_parser(
        "affected", help="sessions a change to these routines can move"
    )
    affected_parser.add_argument("targets", nargs="+")
    verify_parser = sub.add_parser(
        "verify-affected", help="session-verify the affected sessions in parallel"
    )
    verify_parser.add_argument("targets", nargs="+")
    verify_parser.add_argument("--jobs", type=int, default=DEFAULT_VERIFY_JOBS)
    verify_parser.add_argument(
        "--sample",
        type=int,
        default=0,
        help="verify only the cheapest N affected sessions",
    )
    sweep_parser = sub.add_parser(
        "sweep", help="session-verify every recorded session in parallel"
    )
    sweep_parser.add_argument("names", nargs="*")
    sweep_parser.add_argument("--jobs", type=int, default=DEFAULT_VERIFY_JOBS)
    sweep_parser.add_argument(
        "--write-ratchet",
        action="store_true",
        help="record each session's confirmed ordinal; needed for new sessions",
    )
    discover_parser = sub.add_parser(
        "discover", help="coverage searches from ledger-ranked seeds"
    )
    discover_parser.add_argument(
        "seeds", nargs="*", help="seed sessions; default the ranked frontier"
    )
    discover_parser.add_argument("--budget", type=int, default=DISCOVER_BUDGET)
    discover_parser.add_argument("--jobs", type=int, default=DISCOVER_JOBS)
    discover_parser.add_argument(
        "--limit",
        type=int,
        default=DISCOVER_LIMIT,
        help="ranked seeds to search when none are named; 0 for all",
    )
    discover_one_parser = sub.add_parser("discover-one", help=argparse.SUPPRESS)
    discover_one_parser.add_argument("seed")
    discover_one_parser.add_argument("--budget", type=int, required=True)
    discover_one_parser.add_argument("--digest", required=True)
    frontier_parser = sub.add_parser("workflow-frontier", help=argparse.SUPPRESS)
    frontier_parser.add_argument("--limit", type=int, default=4)
    intake_parser = sub.add_parser(
        "intake", help="record, verify and land a seed's best corpus scripts"
    )
    intake_parser.add_argument("seed")
    intake_parser.add_argument("--top", type=int, default=INTAKE_TOP)
    intake_parser.add_argument(
        "--land", action="store_true", help="jj commit each session"
    )
    intake_one_parser = sub.add_parser("intake-one", help=argparse.SUPPRESS)
    intake_one_parser.add_argument("seed")
    intake_one_parser.add_argument("--input-sha256", required=True)
    intake_one_parser.add_argument("--save-sha256", required=True)
    target_parser = sub.add_parser(
        "target", help="arranged AI duels for the card effects no session executes"
    )
    target_parser.add_argument(
        "names",
        nargs="*",
        help="effect routines or pret file stems; default every unexecuted carried effect",
    )
    target_parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="carrier decks to record this run; 0 for all",
    )
    target_parser.add_argument(
        "--land", action="store_true", help="jj commit each session"
    )
    target_parser.add_argument("--jobs", type=int, default=DEFAULT_VERIFY_JOBS)
    one_parser = sub.add_parser("target-one", help=argparse.SUPPRESS)
    one_parser.add_argument("card")
    one_parser.add_argument("--slot", type=int)
    one_parser.add_argument("--routines", required=True)
    one_parser.add_argument("--ai", action="store_true")
    trace_parser = sub.add_parser("trace", help=argparse.SUPPRESS)
    trace_parser.add_argument("name")
    args = parser.parse_args(argv)
    try:
        if args.command == "ledger":
            names = ledger_sessions()
            unknown = sorted(set(args.names) - set(names))
            if unknown:
                raise CoverageError(f"not recorded sessions: {', '.join(unknown)}")
            forced = set(names) if args.force else set(args.names)
            return build(
                names, jobs=args.jobs, forced=forced, write_ratchet=args.write_ratchet
            )
        if args.command == "status":
            return status(args.limit)
        if args.command == "next":
            return next_action()
        if args.command in ("affected", "verify-affected"):
            ledger = load_ledger()
            names = affected(ledger, expand_targets(ledger, args.targets))
            if args.command == "affected":
                for name in names:
                    print(name)
                return 0
            return verify_affected(names, jobs=args.jobs, sample=args.sample)
        if args.command == "discover":
            return discover(
                args.seeds, budget=args.budget, jobs=args.jobs, limit=args.limit
            )
        if args.command == "discover-one":
            seed, outcome, detail = explore_seed(
                args.seed, budget=args.budget, digest=args.digest
            )
            print(
                json.dumps(
                    {"seed": seed, "outcome": outcome, "detail": detail},
                    sort_keys=True,
                )
            )
            return 0 if outcome in {"cached", "explored"} else 2
        if args.command == "workflow-frontier":
            print(json.dumps(workflow_frontier(args.limit), sort_keys=True))
            return 0
        if args.command == "intake":
            return intake(args.seed, top=args.top, land=args.land)
        if args.command == "intake-one":
            print(
                json.dumps(
                    intake_one(
                        args.seed,
                        input_sha256=args.input_sha256,
                        save_sha256=args.save_sha256,
                    ),
                    sort_keys=True,
                )
            )
            return 0
        if args.command == "target":
            return target(args.names, land=args.land, limit=args.limit, jobs=args.jobs)
        if args.command == "target-one":
            row = target_one(args.card, args.slot, args.routines.split(","), args.ai)
            print(json.dumps(row, sort_keys=True))
            return 0
        if args.command == "trace":
            record = trace_session(args.name)
            print(
                f"TRACED {args.name} ordinals={record['ordinals']} routines={len(record['routines'])}"
            )
            return 0
        return verify_affected(
            args.names or ledger_sessions(),
            jobs=args.jobs,
            ratchet=getattr(args, "write_ratchet", False),
        )
    except (
        CoverageError,
        session.SessionError,
        refstream.RefstreamError,
        OSError,
        ValueError,
    ) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
