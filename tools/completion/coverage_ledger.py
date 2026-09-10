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
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
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
EXPLORE_DIR = ROOT / "build" / "completion"
DISCOVER_BUDGET = 6000
DISCOVER_JOBS = 2
DISCOVER_LIMIT = 4
INTAKE_TOP = 3
VERIFY_STATUS = {0: "clean", 1: "diverged", 2: "failed", 3: "regression", 4: "ref-short"}


class CoverageError(RuntimeError):
    pass


def trace_plan(name: str) -> dict[str, Any]:
    """The session's masks, pokes, stream key and the ordinal the trace stops at."""
    masks, meta = session.load_session(name)
    ratchet = session.read_ratchet().get(name)
    if ratchet is None:
        raise CoverageError(f"{name} has never been verified: run `just session-verify {name}` first")
    frames = session.reference_frames(masks, meta)
    return {"name": name, "masks": masks, "frames": frames, "pokes": meta["pokes"], "meta": meta,
            "save": meta["save"], "ordinals": min(len(masks), int(ratchet["confirmed_ordinal"])),
            "key": session.stream_key(masks, frames, "ordinal", meta["pokes"], meta["save"])}


def routine_files() -> tuple[dict[str, str], dict[str, str]]:
    """routine -> asm file for the whole inventory, and routine -> exclusion
    kind for the routines scope.toml removes from the denominator."""
    inventory = json.loads(INVENTORY.read_text())
    functions = inventory["functions"]
    excluded, _names, _count, _bytes = resolve_scope(load_scope(), functions, inventory)
    return ({name: info["file"] for name, info in functions.items()},
            {name: row["kind"] for name, row in excluded.items()})


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
    return (record is not None and record["key"] == plan["key"]
            and record["ordinals"] == plan["ordinals"])


def trace_session(name: str) -> dict[str, Any]:
    """One reference replay through the confirmed ordinal; the cache record."""
    plan = trace_plan(name)
    inventory, _excluded = routine_files()
    routines: dict[str, list[int]] = {}
    events = 0
    if plan["ordinals"] > 0:
        trace = refstream.routine_trace(name, plan["frames"], None, ordinals=plan["ordinals"],
                                        masks=plan["masks"], axis="ordinal", pokes=plan["pokes"] or None,
                                        save=plan["save"])
        if trace["ordinals_reached"] < plan["ordinals"]:
            raise CoverageError(f"{name}: the reference reached {trace['ordinals_reached']} of "
                                f"{plan['ordinals']} ordinals")
        events = trace["events"]
        routines = {row["routine"]: [row["count"], row["first_ordinal"]]
                    for row in sorted(trace["calls"], key=lambda row: row["routine"])
                    if row["routine"] in inventory}
    record = {
        "schema": 1, "format": TRACE_FORMAT, "session": name, "key": plan["key"],
        "ordinals": plan["ordinals"], "events": events,
        "seed": session_seed(plan["meta"], set(session.session_names())),
        "digest": hashlib.sha256("\n".join(sorted(routines)).encode()).hexdigest()[:16],
        "routines": routines,
    }
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path(name).write_text(json.dumps(record, separators=(",", ":"), sort_keys=True) + "\n")
    return record


def trace_worker(name: str) -> tuple[str, str]:
    command = [sys.executable, str(Path(__file__).resolve()), "trace", name]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return name, result.stderr.strip()[-400:] or f"exit {result.returncode}"
    return name, ""


def collect(names: list[str], *, jobs: int, forced: set[str]) -> dict[str, dict[str, Any]]:
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
        print(f"SKIP unverified={len(pending)}: {', '.join(pending[:6])}", file=sys.stderr)
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
                print(f"TRACED {name} ordinals={record['ordinals']} "
                      f"routines={len(record['routines'])}", file=sys.stderr)
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
    for routine in sorted(files):
        entry: dict[str, Any] = {"file": files[routine], "sessions": by_routine.get(routine, [])}
        if routine in excluded:
            entry["excluded"] = excluded[routine]
        routines[routine] = entry
        if routine in excluded:
            continue
        row = per_file.setdefault(files[routine], {"executed": 0, "total": 0})
        row["total"] += 1
        if entry["sessions"]:
            row["executed"] += 1
    executed = sum(row["executed"] for row in per_file.values())
    total = sum(row["total"] for row in per_file.values())
    sessions = {}
    for name in names:
        record = records[name]
        sessions[name] = {
            "routines": len(record["routines"]), "ordinals": record["ordinals"],
            "digest": record["digest"], "events": record["events"],
            "seed": record.get("seed") if record.get("seed") in known else None,
        }
    return {
        "schema": 1, "format": LEDGER_FORMAT,
        "revision": current_source_revision(ROOT),
        "generated": datetime.now(UTC).isoformat(timespec="seconds"),
        "totals": {"executed": executed, "total": total, "sessions": len(names),
                   "excluded": len(excluded)},
        "session_order": names,
        "sessions": sessions,
        "files": {file: per_file[file] for file in sorted(per_file)},
        "routines": routines,
    }


def load_ledger() -> dict[str, Any]:
    if not LEDGER.is_file():
        raise CoverageError(f"no ledger at {LEDGER.relative_to(ROOT)}: run `just coverage-ledger`")
    ledger = json.loads(LEDGER.read_text())
    if ledger.get("format") != LEDGER_FORMAT:
        raise CoverageError(f"{LEDGER.relative_to(ROOT)} is not a {LEDGER_FORMAT} ledger")
    return ledger


def executed_set(ledger: dict[str, Any]) -> set[str]:
    return {routine for routine, entry in ledger["routines"].items() if entry["sessions"]}


def unexecuted(ledger: dict[str, Any]) -> dict[str, str]:
    """routine -> file for every in-scope routine no session executes."""
    return {routine: entry["file"] for routine, entry in ledger["routines"].items()
            if not entry["sessions"] and "excluded" not in entry}


def read_ratchet() -> dict[str, int]:
    return json.loads(RATCHET.read_text()) if RATCHET.is_file() else {}


def apply_ratchet(ledger: dict[str, Any], *, write: bool) -> int:
    executed = ledger["totals"]["executed"]
    previous = read_ratchet().get("executed")
    if previous is not None and executed < previous and not write:
        print(f"REGRESSION coverage key=executed was={previous} now={executed}")
        return 3
    if previous is None or executed > previous or write:
        RATCHET.write_text(json.dumps({"executed": executed}, indent=2, sort_keys=True) + "\n")
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
            raise CoverageError(f"{target} names neither an inventory routine nor an asm file stem")
    return out


def affected(ledger: dict[str, Any], routines: list[str]) -> list[str]:
    """The sessions a change to `routines` can move: every session executing
    one of them, the sessions they were branched from, and the core set."""
    names = ledger["session_order"]
    hit: set[str] = set()
    for routine in routines:
        hit.update(names[position] for position in ledger["routines"][routine]["sessions"])
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
    print(f"LEDGER sessions={totals['sessions']} executed={totals['executed']} "
          f"total={totals['total']} excluded={totals['excluded']} "
          f"unexecuted={totals['total'] - totals['executed']}")
    return apply_ratchet(ledger, write=write_ratchet)


def status(limit: int) -> int:
    ledger = load_ledger()
    totals = ledger["totals"]
    print(f"LEDGER revision={ledger['revision'][:12]} sessions={totals['sessions']} "
          f"executed={totals['executed']}/{totals['total']}")
    rows = sorted(ledger["files"].items(), key=lambda row: (row[1]["executed"] - row[1]["total"], row[0]))
    for file, row in rows[:limit]:
        miss = row["total"] - row["executed"]
        if miss == 0:
            break
        print(f"FILE miss={miss} executed={row['executed']}/{row['total']} {file}")
    return 0


def verify_affected(names: list[str]) -> int:
    worst = 0
    for name in names:
        code = session.verify(name, write=False, json_path=None)
        worst = max(worst, code)
    print(f"AFFECTED sessions={len(names)} exit={worst}")
    return worst


def executed_digest(ledger: dict[str, Any]) -> str:
    return hashlib.sha256("\n".join(sorted(executed_set(ledger))).encode()).hexdigest()[:16]


def explore_paths(seed: str) -> tuple[Path, Path]:
    return EXPLORE_DIR / f"explore-{seed}.json", EXPLORE_DIR / f"explore-{seed}"


def corpus_current(seed: str, digest: str) -> bool:
    json_path, corpus = explore_paths(seed)
    if not json_path.is_file() or not (corpus / "corpus.json").is_file():
        return False
    return json.loads(json_path.read_text()).get("ledger_digest") == digest


def session_total(name: str) -> int:
    """The session's own length, which the ledger's confirmed-capped `ordinals` is not."""
    path = session.session_dir(name) / "session.json"
    if path.is_file():
        total = json.loads(path.read_text()).get("ordinals")
        if isinstance(total, int) and total > 0:
            return total
    return len(session.load_session(name)[0])


def is_clean(name: str) -> bool:
    return session.read_ratchet().get(name, {}).get("confirmed_ordinal", 0) >= session_total(name)


def rank_seeds(ledger: dict[str, Any]) -> list[tuple[str, int]]:
    """Sessions by how many unexecuted routines sit in the files they already
    touch: a search from a seed explores the screens around that seed."""
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
        score = sum(missing.get(file, 0) for file in touched) if is_clean(name) else 0
        rows.append((name, score))
    rows.sort(key=lambda row: (-row[1], -ledger["sessions"][row[0]]["routines"], row[0]))
    return rows


def explore_seed(seed: str, *, budget: int, digest: str) -> tuple[str, str, str]:
    json_path, corpus = explore_paths(seed)
    if corpus_current(seed, digest):
        return seed, "cached", str(corpus.relative_to(ROOT))
    command = [sys.executable, str(ROOT / "tools" / "completion" / "explore.py"),
               "--seed-session", seed, "--budget", str(budget), "--known", str(LEDGER),
               "--corpus", str(corpus), "--json", str(json_path)]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0 or not json_path.is_file():
        return seed, "failed", result.stderr.strip()[-400:]
    data = json.loads(json_path.read_text())
    data["seed_session"] = seed
    data["ledger_digest"] = digest
    json_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return seed, "explored", f"new={data['new']} entries={data.get('corpus_entries', 0)} seconds={data['seconds']}"


def discover(seeds: list[str], *, budget: int, jobs: int, limit: int) -> int:
    ledger = load_ledger()
    digest = executed_digest(ledger)
    unknown = sorted(set(seeds) - set(ledger["sessions"]))
    if unknown:
        raise CoverageError(f"not in the ledger: {', '.join(unknown)}")
    if not seeds:
        ranked = [name for name, score in rank_seeds(ledger) if score > 0]
        seeds = [name for name in ranked if not corpus_current(name, digest)]
        if limit:
            seeds = seeds[:limit]
    if not seeds:
        print(f"DISCOVER ledger={digest} seeds=0: every ranked seed has a corpus at this ledger")
        return 0
    print(f"DISCOVER ledger={digest} seeds={len(seeds)} budget={budget} jobs={jobs}", file=sys.stderr)
    failed = 0
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for seed, outcome, detail in pool.map(
                lambda seed: explore_seed(seed, budget=budget, digest=digest), seeds):
            print(f"DISCOVER {seed} {outcome} {detail}")
            failed += outcome == "failed"
    return 1 if failed else 0


def next_session_name(seed: str) -> str:
    existing = set(session.session_names())
    k = 1
    while f"{seed}-explore-{k}" in existing:
        k += 1
    return f"{seed}-explore-{k}"


def commit_line(name: str) -> list[str]:
    return ["jj", "commit", f"tests/sessions/{name}", "tools/completion/session_ratchet.json",
            "-m", f"feat(session): record {name}"]


def intake(seed: str, *, top: int, land: bool) -> int:
    """Record the seed's corpus scripts that reach the most routines no session
    executes, verify each, and land it either way: a diverged session is how
    a fact enters the tracker."""
    ledger = load_ledger()
    if not is_clean(seed):
        confirmed = session.read_ratchet().get(seed, {}).get("confirmed_ordinal", 0)
        raise CoverageError(
            f"{seed} is diverged at {confirmed + 1} of {session_total(seed)}: a session extending it "
            f"can only re-report that fact. Fix it first, or intake from a clean seed.")
    _json_path, corpus = explore_paths(seed)
    index = corpus / "corpus.json"
    if not index.is_file():
        raise CoverageError(f"no corpus for {seed}: run `just coverage-discover {seed}`")
    entries = json.loads(index.read_text()).get("entries", [])
    if any("routines" not in entry for entry in entries):
        raise CoverageError(f"{index.relative_to(ROOT)} predates ledger scoring: rerun `just coverage-discover {seed}`")
    covered = executed_set(ledger)
    chosen: list[tuple[dict[str, Any], int]] = []
    remaining = list(entries)
    while remaining and len(chosen) < top:
        best = max(remaining, key=lambda entry: (len(set(entry["routines"]) - covered), -entry["frames"]))
        gain = len(set(best["routines"]) - covered)
        if gain == 0:
            break
        chosen.append((best, gain))
        covered |= set(best["routines"])
        remaining.remove(best)
    if not chosen:
        print(f"INTAKE {seed} scripts=0: the corpus reaches nothing the ledger lacks")
        return 0
    worst = 0
    for entry, gain in chosen:
        name = next_session_name(seed)
        try:
            session.from_script(name, seed=seed, script=corpus / entry["script"], goal="")
        except session.SessionError as exc:
            print(f"INTAKE {seed} skip script={entry['script']}: {exc}")
            continue
        code = session.verify(name, write=False, json_path=None)
        print(f"INTAKE {name} script={entry['script']} gain={gain} verify={VERIFY_STATUS.get(code, code)}")
        if code in (2, 4):
            worst = max(worst, code)
            continue
        land_session(name, land=land)
    return worst


def land_session(name: str, *, land: bool) -> None:
    command = commit_line(name)
    if land:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise CoverageError(f"landing {name} failed: {result.stderr.strip()[-300:]}")
        print(f"LANDED {name}")
    else:
        print("COMMIT " + " ".join(f"'{part}'" if " " in part else part for part in command))


TARGETS_PATH = ROOT / "build" / "completion" / "effects" / "targets.json"
TARGET_BASE = "practice-win"
TARGET_AT = 23227
TARGET_OPPONENT = 2
TARGET_PRIZES = 6


def session_slug(card: str) -> str:
    return card.lower().replace("_", "-")


def target(names: list[str], *, land: bool, limit: int) -> int:
    """One arranged AI duel per carrier card for the effect routines no
    session executes; each is verified and landed, and a carrier the AI never
    plays becomes a player-controlled search seed with that deck poked."""
    import effects

    ledger = load_ledger()
    executed = executed_set(ledger)
    by_routine = effects.load_map()["by_routine"]
    if names:
        wanted = expand_targets(ledger, names)
    else:
        wanted = sorted(routine for routine in unexecuted(ledger) if routine in by_routine)
    groups: dict[tuple[str, int | None], set[str]] = {}
    for routine in wanted:
        if routine in executed or routine not in by_routine:
            continue
        carrier = effects.carriers(routine)[0]
        slot = int(carrier["slot"][-1]) if carrier["slot"].startswith("attack") else None
        groups.setdefault((carrier["card"], slot), set()).add(routine)
    if not groups:
        print("TARGET none: every carried effect routine is executed by a session")
        return 0
    record = json.loads(TARGETS_PATH.read_text()) if TARGETS_PATH.is_file() else {}
    existing = set(session.session_names())
    ordered = sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
    worst = 0
    done = 0
    for (card, slot), routines in ordered:
        if limit and done >= limit:
            break
        name = f"effect-{session_slug(card)}" + (f"-{slot}" if slot else "")
        if name in existing or f"{name}-seed" in existing:
            continue
        try:
            deck = effects.build_deck(card, attack_slot=slot)
        except effects.EffectsError as exc:
            print(f"TARGET skip card={card} slot={slot}: {exc}")
            continue
        done += 1
        deck_path = TARGETS_PATH.parent / f"{name}.deck"
        deck_path.parent.mkdir(parents=True, exist_ok=True)
        deck_path.write_text("\n".join(str(c) for c in deck) + "\n")
        goal = (f"Card effect target: {card} attack {slot}" if slot else f"Card effect target: {card}") \
            + f" ({', '.join(sorted(routines)[:4])})"
        session.ai_duel(name, base=TARGET_BASE, at=TARGET_AT, deck=TARGET_OPPONENT, seed=None,
                        prizes=TARGET_PRIZES, period=24, tail=1500, goal=goal, cards=deck,
                        watch=routines, arrange=True)
        watched = json.loads((session.session_dir(name) / "session.json").read_text())["watched"]
        reached = {routine: ordinal for routine, ordinal in watched.items() if ordinal is not None}
        for routine in routines:
            record[routine] = {"card": card, "slot": slot, "session": name,
                               "reached": reached.get(routine), "deck": str(deck_path.relative_to(ROOT))}
        TARGETS_PATH.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
        if not reached:
            for path in (session.session_dir(name)).iterdir():
                path.unlink()
            session.session_dir(name).rmdir()
            name = f"{name}-seed"
            session.deck_seed(name, base=TARGET_BASE, at=TARGET_AT, deck=TARGET_OPPONENT, cards=deck,
                              goal=f"Search seed: {card} in hand, the AI never played it "
                                   f"({', '.join(sorted(routines)[:4])})")
            for routine in routines:
                record[routine]["session"] = name
            TARGETS_PATH.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
        code = session.verify(name, write=False, json_path=None)
        print(f"TARGET {name} card={card} routines={len(routines)} reached={len(reached)} "
              f"verify={VERIFY_STATUS.get(code, code)}")
        if code in (2, 4):
            worst = max(worst, code)
            continue
        land_session(name, land=land)
    return worst


def main(argv: list[str] | None = None) -> int:
    sys.stdout.reconfigure(line_buffering=True)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    ledger_parser = sub.add_parser("ledger", help="trace stale sessions and rebuild the ledger")
    ledger_parser.add_argument("names", nargs="*", help="sessions to retrace even when their cache is current")
    ledger_parser.add_argument("--jobs", type=int, default=DEFAULT_JOBS)
    ledger_parser.add_argument("--force", action="store_true", help="retrace every session")
    ledger_parser.add_argument("--write-ratchet", action="store_true", help="accept a lower executed count")
    status_parser = sub.add_parser("status", help="files ranked by routines no session executes")
    status_parser.add_argument("--limit", type=int, default=20)
    affected_parser = sub.add_parser("affected", help="sessions a change to these routines can move")
    affected_parser.add_argument("targets", nargs="+")
    verify_parser = sub.add_parser("verify-affected", help="session-verify the affected sessions, serially")
    verify_parser.add_argument("targets", nargs="+")
    sweep_parser = sub.add_parser("sweep", help="session-verify every recorded session, serially")
    sweep_parser.add_argument("names", nargs="*")
    discover_parser = sub.add_parser("discover", help="coverage searches from ledger-ranked seeds")
    discover_parser.add_argument("seeds", nargs="*", help="seed sessions; default the ranked frontier")
    discover_parser.add_argument("--budget", type=int, default=DISCOVER_BUDGET)
    discover_parser.add_argument("--jobs", type=int, default=DISCOVER_JOBS)
    discover_parser.add_argument("--limit", type=int, default=DISCOVER_LIMIT,
                                 help="ranked seeds to search when none are named; 0 for all")
    intake_parser = sub.add_parser("intake", help="record, verify and land a seed's best corpus scripts")
    intake_parser.add_argument("seed")
    intake_parser.add_argument("--top", type=int, default=INTAKE_TOP)
    intake_parser.add_argument("--land", action="store_true", help="jj commit each session")
    target_parser = sub.add_parser("target", help="arranged AI duels for the card effects no session executes")
    target_parser.add_argument("names", nargs="*", help="effect routines or pret file stems; default every unexecuted carried effect")
    target_parser.add_argument("--limit", type=int, default=0, help="carrier decks to record this run; 0 for all")
    target_parser.add_argument("--land", action="store_true", help="jj commit each session")
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
            return build(names, jobs=args.jobs, forced=forced, write_ratchet=args.write_ratchet)
        if args.command == "status":
            return status(args.limit)
        if args.command in ("affected", "verify-affected"):
            ledger = load_ledger()
            names = affected(ledger, expand_targets(ledger, args.targets))
            if args.command == "affected":
                for name in names:
                    print(name)
                return 0
            return verify_affected(names)
        if args.command == "discover":
            return discover(args.seeds, budget=args.budget, jobs=args.jobs, limit=args.limit)
        if args.command == "intake":
            return intake(args.seed, top=args.top, land=args.land)
        if args.command == "target":
            return target(args.names, land=args.land, limit=args.limit)
        if args.command == "trace":
            record = trace_session(args.name)
            print(f"TRACED {args.name} ordinals={record['ordinals']} routines={len(record['routines'])}")
            return 0
        return verify_affected(args.names or ledger_sessions())
    except (CoverageError, session.SessionError, refstream.RefstreamError,
            OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
