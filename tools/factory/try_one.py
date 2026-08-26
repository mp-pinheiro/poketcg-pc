#!/usr/bin/env python3
"""Port one routine with k independent candidates and the real verifier."""
from __future__ import annotations

import argparse
import functools
import json
import hashlib
import re
import time
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
import heal
import lanes
import packet as packet_mod
import prompt as prompt_mod
import surgery
import verify
import workers

TRY_ROOT = common.FACTORY / "try"
CURRENT_FIELDS = (
    "schema", "fn", "attempt_id", "generation", "context_sha256",
    "base_commit", "state",
)
ATTEMPT_STATES = frozenset({"issued", "red", "green", "stale"})


class OperationalBlocker(LookupError):
    def __init__(self, fn: str, blocker: dict[str, Any]) -> None:
        self.fn = fn
        self.blocker = blocker
        super().__init__(str(blocker.get("reason") or "operational blocker"))


class PreflightBlocker(LookupError):
    def __init__(self, fn: str, detail: str) -> None:
        self.fn = fn
        self.detail = detail
        super().__init__(detail)


class StaleAttempt(RuntimeError):
    pass


def _attempt_root(fn: str) -> Path:
    return TRY_ROOT / fn


def _current_path(fn: str) -> Path:
    return _attempt_root(fn) / "current.json"


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _read_current(fn: str) -> dict[str, Any] | None:
    path = _current_path(fn)
    if not path.is_file():
        return None
    try:
        current = _read_json(path)
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    if (
        set(current) != set(CURRENT_FIELDS)
        or current.get("schema") != common.SCHEMA
        or current.get("fn") != fn
        or not isinstance(current.get("attempt_id"), str)
        or not isinstance(current.get("generation"), int)
        or not isinstance(current.get("context_sha256"), str)
        or not isinstance(current.get("base_commit"), str)
        or current.get("state") not in ATTEMPT_STATES
    ):
        return None
    return current


def _store_current(current: dict[str, Any]) -> None:
    _write_json(_current_path(str(current["fn"])), current)


def _case_classification(fn: str, source: str | None) -> str:
    basename = Path(source or fn).stem
    return common.classify_case_module(
        common.ROOT / "tests" / "cases" / f"{basename}.py"
    )
def _check_operational_blocker(fn: str) -> None:
    blocker = packet_mod.report_module().load_operational_blockers().get(fn)
    if blocker is not None:
        raise OperationalBlocker(fn, blocker)



@functools.cache
def _home_source_lines(basename: str) -> tuple[str, ...] | None:
    """Lines of src/home/<basename>.c, cached: the capability report asks about
    every blocked root, and re-reading one file per routine dominated its cost.
    """
    path = common.ROOT / "src" / "home" / f"{basename}.c"
    if not path.is_file():
        return None
    return tuple(path.read_text(errors="replace").splitlines())


def _already_implemented(fn: str, source: str | None) -> bool:
    """True when the ported tree already defines this routine.

    62 inventory routines are reported todo yet already carry a C body, so every
    attempt on them fails `redefinition of <fn>` regardless of the retry budget.
    Excluding them at preflight keeps a guaranteed-red class out of the frontier
    and surfaces it as a registry discrepancy to reconcile rather than as a
    translation to retry.

    The match requires a non-identifier character (or start of line) immediately
    before `fn`, so a routine like `Preload_Ronald1InPsychicClubLobby` is never
    matched by an unrelated `_Preload_Ronald1InPsychicClubLobby(` definition that
    merely contains it as a substring.
    """
    lines = _home_source_lines(Path(source or fn).stem)
    if lines is None:
        return False
    pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(fn) + r"\(")
    for line in lines:
        stripped = line.strip()
        if not pattern.search(stripped):
            continue
        if stripped.startswith(("//", "*", "/*", "#")) or stripped.endswith(";"):
            continue
        return True
    return False


def resolve(fn: str) -> tuple[dict[str, Any], dict[str, Any]]:
    _check_operational_blocker(fn)
    # Shared tree.lock for the same reason lanes.py takes it around an rsync: a
    # packet built while another session's surgery is half applied describes a
    # tree that never existed, and the only visible effect is that this attempt
    # goes `stale` on its next verification. A concurrent orchestrator whose
    # candidates take longer than the lander's cycle then verifies nothing at
    # all, because every one of its attempts is reissued before it can be used.
    with common.file_lock(common.locks_dir() / "tree.lock", exclusive=False,
                          timeout=1800):
        report = packet_mod.report_module()
        functions, _inventory = packet_mod.compute_functions()
        matched = [f for f in functions if f["name"] == fn]
        if not matched:
            raise LookupError(f"{fn} is not in the pret inventory")
        if len(matched) > 1:
            raise LookupError(f"{fn} is ambiguous across {len(matched)} inventory records")
        routine = matched[0]
        classification = _case_classification(fn, routine.get("file"))
        if classification == "native-migration-required":
            raise PreflightBlocker(fn, classification)
        if _already_implemented(fn, routine.get("file")):
            raise PreflightBlocker(fn, "already-implemented")
        work_id = routine.get("work_id")
        if not isinstance(work_id, str) or not work_id:
            raise LookupError(f"{fn} has no canonical work id; it is out of scope")
        packets = packet_mod.build_packets_for_work_ids({work_id}, issue_numbers={work_id: 0})
        if len(packets) != 1:
            raise LookupError(f"{fn} produced {len(packets)} packets")
        return routine, packets[0]


# Retry model ladder: generations 0-5 use the session task model, 6-11 switch
# model family (cross-model diversity beats same-model resampling on
# correlated failures), 12+ spend the strongest model. Retry limit is 16.
LADDER = ((12, "port-candidate-max"), (6, "port-candidate-hard"))


def dispatch_line(fn: str, run_dir: Path, index: int, generation: int) -> str:
    agent = "port-candidate"
    for floor, name in LADDER:
        if generation >= floor:
            agent = name
            break
    return (f"task(agent=\"{agent}\", task=\"Read {run_dir / 'prompt.txt'} and write the "
            f"TranslationReplyV2 JSON object it asks for to "
            f"{run_dir / f'candidate-{index}.json'}. Emit no prose.\")")


def await_candidate(path: Path, wait: float) -> dict[str, Any]:
    """Read a candidate as soon as it exists, waiting at most ``wait`` seconds."""
    deadline = time.monotonic() + wait
    while not path.is_file():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"no candidate at {path} after {wait:.0f}s")
        time.sleep(1.0)
    return _read_json(path)


def _attempt_result(fn: str, attempt_id: str | None) -> dict[str, Any] | None:
    if not attempt_id:
        return None
    try:
        return _read_json(_attempt_root(fn) / "attempts" / attempt_id / "result.json")
    except (OSError, json.JSONDecodeError, ValueError):
        return None


def _feedback_for(fn: str, parent_attempt_id: str | None) -> str | None:
    """Verbatim diagnostics of the attempt this retry supersedes.

    A retry that cannot see why the previous attempt failed re-derives the same
    answer: 7 of 9 measured routines produced byte-identical diagnostics across
    three independent candidates. Feeding the exact tool output back is what makes
    a later generation a genuinely different draw rather than a costlier copy.
    """
    prior = _attempt_result(fn, parent_attempt_id)
    if prior is None:
        return None
    blocks = []
    for entry in prior.get("results") or []:
        if entry.get("outcome") == "productive":
            continue
        detail = str(entry.get("detail") or "").strip()
        if detail:
            blocks.append(f"phase={entry.get('phase')} "
                          f"failure_class={entry.get('failure_class')}\n{detail[:1500]}")
            blocks.extend(_divergence_directive(detail))
    return "\n\n".join(blocks) or None


_PRESERVE_MISMATCH = re.compile(r"preserve:([a-z]+)")


def _divergence_directive(detail: str) -> list[str]:
    """Spell out the one repair a REFERENCE_DIVERGENCE diagnostic admits.

    compare_one.py raises this status before the candidate's C is ever executed,
    so it is never a translation bug: the case declared `preserve` for a
    register the real ROM clobbers. Left as raw JSON the class ate 9-17
    generations per routine, so name the fix instead of restating the failure.
    """
    if "REFERENCE_DIVERGENCE" not in detail:
        return []
    regs = sorted(set(_PRESERVE_MISMATCH.findall(detail)))
    if not regs:
        return []
    named = ", ".join(regs)
    return [
        "HOW TO FIX THE ABOVE: this is a CONTRACT error, not a translation bug."
        " The oracle checks `preserve` against the real ROM before it ever runs"
        f" your C, and the ROM does NOT preserve {named}. Each"
        " `preserve:<reg>: [x, y]` pair is (the value the case entered with, the"
        " value the ROM actually left). Remove"
        f" {named} from this routine's `preserve` tuple and list"
        " them in `compare` instead, so they are still checked against the"
        " reference's output. Do not change the C to try to keep them."
    ]


def _diagnostic_signature(entry: dict[str, Any]) -> str:
    """Stable identity of one failure, ignoring lane paths that vary per run."""
    detail = re.sub(r"lane-\d+", "lane-N", str(entry.get("detail") or ""))[:400]
    payload = f"{entry.get('phase')}\0{entry.get('failure_class')}\0{detail}"
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _failure_signatures(fn: str, attempt_id: str | None) -> frozenset[str]:
    result = _attempt_result(fn, attempt_id)
    if result is None:
        return frozenset()
    return frozenset(
        _diagnostic_signature(entry)
        for entry in result.get("results") or []
        if entry.get("outcome") != "productive"
    )


def _attempt_parent(fn: str, attempt_id: str) -> str | None:
    try:
        packet = _read_json(_attempt_root(fn) / "attempts" / attempt_id / "packet.json")
    except (OSError, json.JSONDecodeError, ValueError):
        return None
    parent = packet.get("parent_attempt_id")
    return parent if isinstance(parent, str) and parent else None


def is_trapped(fn: str, current: dict[str, Any]) -> bool:
    """True when the newest two generations failed with identical diagnostics.

    An identical signature across generations proves the packet -- not the sample
    -- decides the outcome, so a further retry is a costlier copy of the same
    answer. This is what lets the attempt budget be generous without burning it on
    deterministic traps, and it is the difference between a red that teaches
    something and a red that is silently forgotten.
    """
    attempt_id = str(current.get("attempt_id") or "")
    signatures = _failure_signatures(fn, attempt_id)
    if not signatures:
        return False
    return signatures == _failure_signatures(fn, _attempt_parent(fn, attempt_id))


def record_trap(fn: str, current: dict[str, Any]) -> None:
    """Append a trapped routine and its signatures to the shared trap ledger.

    Reds clustered by signature are the most valuable artefact the factory can
    emit: one shared signature covered 63 routines and a single harness fix
    cleared all of them. A red that is merely dropped from both pools teaches
    nothing and strands every routine that depends on it.
    """
    attempt_id = str(current.get("attempt_id") or "")
    entry = {
        "fn": fn,
        "attempt_id": attempt_id,
        "generation": current.get("generation"),
        "signatures": sorted(_failure_signatures(fn, attempt_id)),
    }
    common.append_jsonl(common.FACTORY / "traps.jsonl", entry)


def issue_attempt(fn: str, generation: int, *, parent_attempt_id: str | None = None) -> dict[str, Any]:
    routine, packet = resolve(fn)
    packet["attempt_generation"] = generation
    packet["parent_attempt_id"] = parent_attempt_id
    context_sha256 = packet_mod.translation_context_sha256(packet)
    attempt_id = packet["attempt_id"]
    run_dir = _attempt_root(fn) / "attempts" / attempt_id
    run_dir.mkdir(parents=True, exist_ok=False)
    _write_json(run_dir / "packet.json", packet)
    feedback = _feedback_for(fn, parent_attempt_id)
    (run_dir / "prompt.txt").write_text(prompt_mod.render(packet, feedback=feedback))
    current = {
        "schema": common.SCHEMA,
        "fn": fn,
        "attempt_id": attempt_id,
        "generation": generation,
        "context_sha256": context_sha256,
        "base_commit": packet["base_commit"],
        "state": "issued",
    }
    _store_current(current)
    return {"current": current, "packet": packet, "routine": routine, "run_dir": run_dir}


def load_current_attempt(fn: str) -> dict[str, Any] | None:
    current = _read_current(fn)
    if current is None:
        return None
    run_dir = _attempt_root(fn) / "attempts" / current["attempt_id"]
    packet_path = run_dir / "packet.json"
    try:
        packet = _read_json(packet_path)
        common.validate_packet(packet)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise StaleAttempt(f"cannot load attempt {current['attempt_id']}: {exc}") from exc
    if packet.get("attempt_id") != current["attempt_id"]:
        raise StaleAttempt("current attempt packet identity differs")
    return {"current": current, "packet": packet, "run_dir": run_dir}


def verification_packet(issued: dict[str, Any]) -> dict[str, Any] | None:
    current = issued["current"]
    fn = str(current["fn"])
    _routine, fresh = resolve(fn)
    context_sha256 = packet_mod.translation_context_sha256(fresh)
    if context_sha256 != current["context_sha256"]:
        current["state"] = "stale"
        _store_current(current)
        return None
    fresh["attempt_id"] = current["attempt_id"]
    fresh["id"] = current["attempt_id"]
    fresh["attempt_generation"] = current["generation"]
    fresh["parent_attempt_id"] = issued["packet"].get("parent_attempt_id")
    common.validate_packet(fresh)
    issued["packet"] = fresh
    issued["current"]["base_commit"] = fresh["base_commit"]
    _write_json(issued["run_dir"] / "packet.json", fresh)
    _store_current(issued["current"])
    return fresh


def attempt(built: dict[str, Any], reply: dict[str, Any], *, lane_index: int,
            candidate: int) -> dict[str, Any]:
    started = time.monotonic()
    record: dict[str, Any] = {"candidate": candidate, "lane_index": lane_index}
    try:
        translation = workers.validate_translation_v2(built, reply)
    except (TypeError, ValueError) as exc:
        return {**record, "outcome": "diagnostic", "phase": "validate",
                "failure_class": "schema", "witness": {}, "detail": str(exc),
                "seconds": round(time.monotonic() - started, 2)}
    try:
        lane = lanes.ensure(lane_index, packet=built)
        baseline = surgery.read_statics(lane, built["basename"])
        surgery.apply(lane, built, translation, statics_baseline=baseline)
    except (OSError, RuntimeError, ValueError) as exc:
        return {**record, "outcome": "diagnostic", "phase": "surgery",
                "failure_class": "schema", "witness": {},
                "detail": f"{type(exc).__name__}: {exc}",
                "seconds": round(time.monotonic() - started, 2)}
    try:
        result = verify.verify_packet(built, lane, True)
    except (OSError, RuntimeError, TypeError, ValueError,
            common.PhaseTimeout, common.WaveDeadlineExpired) as exc:
        result = {"status": "infra-error", "phase": "verify",
                  "detail": f"{type(exc).__name__}: {exc}"}
    seconds = round(time.monotonic() - started, 2)
    green = result.get("status") == "green"
    record = {
        **record,
        "outcome": "productive" if green else "diagnostic",
        "phase": str(result.get("phase") or result.get("status")),
        "failure_class": result.get("failure_class"),
        "witness": result.get("witness") or {},
        "detail": str(result.get("detail") or "")[-2000:],
        "seconds": seconds,
    }
    if green:
        # Bundling reads back what surgery wrote, so it can fail on a
        # translation the oracle already accepted. That is a diagnostic about
        # this candidate, not a reason to abort the whole wave with a traceback
        # and lose every other candidate's result.
        try:
            stored = workers.store_artifact(workers.stage_bundle(built, lane))
        except (OSError, RuntimeError, TypeError, ValueError) as exc:
            return {**record, "outcome": "diagnostic", "phase": "bundle",
                    "failure_class": "bundle",
                    "detail": f"{type(exc).__name__}: {exc}"[-2000:]}
        record["artifact_sha256"] = stored["artifact_sha256"]
    return record


def _quarantined_artifacts() -> set[str]:
    path = common.FACTORY / "quarantine.jsonl"
    if not path.is_file():
        return set()
    shas: set[str] = set()
    for line in path.read_text().splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        sha = entry.get("artifact_sha256")
        if isinstance(sha, str):
            shas.add(sha)
    return shas


def _artifact_attempted_names() -> set[str]:
    # A revoked artifact is one whose landing never reached the tree: its routine
    # must stop counting as attempted, so a re-land that the gate then rejects
    # returns the routine to the fresh pool instead of stranding it.
    excluded = _quarantined_artifacts() | heal.revoked_artifacts()
    names: set[str] = set()
    for record in workers.artifact_records():
        if record.get("artifact_sha256") in excluded:
            continue
        for routine in (record.get("identity") or {}).get("routines") or []:
            if isinstance(routine, dict) and isinstance(routine.get("name"), str):
                names.add(routine["name"])
    return names


def _pending_artifact_basenames() -> set[str]:
    """Basenames with a verified artifact staged but not yet landed.

    Landing such an artifact rewrites its basename's case module, so issuing a
    sibling against the current tree wastes its candidates on a context about
    to go stale. Green attempt state is no proxy: it persists after landing.
    """
    landed: set[str] = set()
    path = common.FACTORY / "landings.jsonl"
    if path.is_file():
        for line in path.read_text().splitlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            sha = entry.get("artifact_sha256")
            if isinstance(sha, str):
                landed.add(sha)
    excluded = (landed | _quarantined_artifacts()) - heal.revoked_artifacts()
    basenames: set[str] = set()
    for record in workers.artifact_records():
        if record.get("artifact_sha256") in excluded:
            continue
        basename = (record.get("identity") or {}).get("basename")
        if isinstance(basename, str):
            basenames.add(basename)
    return basenames


def _green_attempt_is_quarantined(fn: str, current: dict[str, Any],
                                  quarantined: set[str]) -> bool:
    if current.get("state") != "green":
        return False
    result_path = (
        _attempt_root(fn) / "attempts" / str(current["attempt_id"]) / "result.json"
    )
    try:
        result = _read_json(result_path)
    except (OSError, json.JSONDecodeError, ValueError):
        return False
    return any(
        isinstance(entry.get("artifact_sha256"), str)
        and entry["artifact_sha256"] in quarantined
        for entry in result.get("results") or []
        if isinstance(entry, dict)
    )



def _rows_by_name(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row["name"]): row for row in records}


def _current_states() -> dict[str, dict[str, Any]]:
    if not TRY_ROOT.is_dir():
        return {}
    states: dict[str, dict[str, Any]] = {}
    for path in sorted(TRY_ROOT.iterdir()):
        if not path.is_dir():
            continue
        current = _read_current(path.name)
        if current is not None:
            states[path.name] = current
    return states


def _score_rows(rows: list[dict[str, Any]], *, retry: bool) -> list[tuple[int, dict[str, Any]]]:
    functions, _inventory = packet_mod.compute_functions()
    graph, dependents = packet_mod.blocker_graph(functions)
    scored = [
        (packet_mod.cascade(graph, dependents, {row["name"]}), row)
        for row in rows
    ]
    if retry:
        return sorted(
            scored,
            key=lambda item: (
                int(_read_current(item[1]["name"])["generation"]),
                -item[0], item[1]["size"], item[1]["name"],
            ),
        )
    return sorted(scored, key=lambda item: (-item[0], item[1]["size"], item[1]["name"]))


DONE_STATES = frozenset({"awaiting-gate", "complete", "failing", "excluded"})
# Registering is correct only when the existing body is a faithful port. Some
# bodies are aliases or documented simplifications (the 52 Music1_*/Music2_*
# command handlers delegate to the dispatcher instead of consuming their own
# stack-passed operand; AIMakeDecision skips OppActionTable dispatch). Adding a
# CONTRACT key registers the routine in tests/routines.py, so registering an
# unfaithful body reds `oracle-release-gate` for every concurrent session.
IMPLEMENTED_UNBLOCK = (
    "diff the existing C body against the asm FIRST, then either register it "
    "(cases, probe, mutation) if it is faithful, or re-port it if it is an "
    "alias or simplification - the factory preflight rejects this routine as "
    "already-implemented, so no candidate can ever be issued for it"
)


def capability_frontier(records: list[dict[str, Any]], *, limit: int = 5
                        ) -> tuple[int, list[tuple[int, str, str, str]]]:
    """(routines reachable today, levers ranked by marginal unblock count).

    Marginal, not transitive-dependents: a routine gated by four blocked roots is
    freed by none of them alone, so a dependents count wildly overstates what one
    capability buys. Each lever is scored by re-running the reachability fixpoint
    with exactly that one obstruction removed.

    Two obstruction kinds are modelled, because both are permanently unportable
    for the loop as it stands: an operational blocker in blocked.toml, and a
    routine whose C body already exists (resolve() raises
    PreflightBlocker("already-implemented") for it forever).
    """
    rows = {str(row["name"]): row for row in records}
    edges = {name: [b for b in (row.get("blockers") or []) if b in rows]
             for name, row in rows.items()}
    done = {name for name, row in rows.items() if row.get("state") in DONE_STATES}
    blocked_roots = {name for name, row in rows.items()
                     if row.get("operational_blocker")}
    implemented = {
        name for name, row in rows.items()
        if row.get("state") in {"ready", "blocked"}
        and _already_implemented(name, row.get("source"))
    }
    excluded = {name for name, row in rows.items() if row.get("state") == "excluded"}
    unportable = blocked_roots | implemented

    def reachable(cleared: frozenset[str], forced: frozenset[str] = frozenset()) -> int:
        ported = done | forced
        gained = 0
        changed = True
        while changed:
            changed = False
            for name in rows:
                if name in ported or name in excluded:
                    continue
                if name in unportable and name not in cleared:
                    continue
                if all(blocker in ported for blocker in edges[name]):
                    ported.add(name)
                    gained += 1
                    changed = True
        return gained

    base = reachable(frozenset())
    levers: list[tuple[int, str, str, str]] = []
    for name in sorted(blocked_roots):
        marginal = reachable(frozenset({name})) - base
        unblock = str((rows[name].get("operational_blocker") or {}).get("unblock", ""))
        levers.append((marginal, "blocked", name, unblock))
    for name in sorted(implemented):
        marginal = reachable(frozenset({name}), frozenset({name})) - base
        levers.append((marginal, "implemented", name, IMPLEMENTED_UNBLOCK))
    levers.sort(key=lambda item: (-item[0], item[2]))
    return base, levers[:limit]


def print_capability_frontier(records: list[dict[str, Any]], *, limit: int = 5) -> None:
    reachable, levers = capability_frontier(records, limit=limit)
    for marginal, kind, name, unblock in levers:
        print(f"CAPABILITY {kind} {name} marginal={marginal} "
              f"unblock={' '.join(unblock.split())[:240]}")
    blocked_roots = sum(1 for row in records if row.get("operational_blocker"))
    implemented = sum(
        1 for row in records
        if row.get("state") in {"ready", "blocked"}
        and _already_implemented(str(row["name"]), row.get("source"))
    )
    print(f"CAPABILITY status reachable={reachable} blocked_roots={blocked_roots} "
          f"already_implemented={implemented}")


def subcommand_next(count: int, retry_red: bool, retry_limit: int) -> int:
    report = packet_mod.report_module()
    records = report.compute(report.load_inventory(), report.load_routines()[0],
                             report.load_gate())["work_records"]
    prepared = 0
    fresh_selected = 0
    retry_selected = 0
    preflight_blocked = 0
    # Every concurrent orchestrator issues under one lock: the read of the
    # current attempt states and the writes that claim them must not interleave,
    # or two sessions claim the same routine and one session's candidates are
    # discarded as stale.
    with common.file_lock(common.locks_dir() / "select.lock", timeout=900):
        # Cheap, tracked-file-free repairs, under the same lock that claims a
        # routine: without them a landing lost from the tree is never re-offered
        # and an issued attempt on a now-blocked routine reports `active`
        # forever, so the loop announces work in flight while nothing can move.
        revoked = heal.revoke_lost_landings(apply=True)
        reaped = heal.reap_stale_issued(_current_states(), _rows_by_name(records))
        current = _current_states()
        attempted = _artifact_attempted_names()
        quarantined = _quarantined_artifacts()
        active_attempts = sum(
            1 for state in current.values() if state["state"] == "issued"
        )
        ready = [row for row in records if row["state"] == "ready"]
        unresolved = [row for row in records if row["state"] in {"ready", "blocked"}]
        if retry_red:
            pool = [
                row for row in ready
                if row["name"] not in attempted
                and current.get(row["name"], {}).get("state") == "red"
                and current[row["name"]]["generation"] < retry_limit
                and not is_trapped(row["name"], current[row["name"]])
            ]
        else:
            pool = [
                row for row in ready
                if (
                    row["name"] not in attempted
                    or current.get(row["name"], {}).get("state") == "stale"
                )
                and (
                    current.get(row["name"], {}).get("state") in {None, "stale"}
                    or _green_attempt_is_quarantined(
                        row["name"], current.get(row["name"], {}), quarantined
                    )
                )
            ]
        # A basename is owned by whichever attempt claimed it first, in this
        # session or another: surgery is per basename, so two live attempts on one
        # basename spend two candidate budgets to land one translation.
        by_name = _rows_by_name(records)
        seen = {
            Path(by_name[name]["source"]).stem
            for name, state in current.items()
            if state["state"] == "issued" and name in by_name
        }
        scored = list(_score_rows(pool, retry=retry_red))
        if not retry_red:
            # A staged, unlanded artifact rewrites its basename's case module
            # at landing, so a sibling issued now spends its candidates on a
            # context about to go stale (44 of the last 64 stales were
            # same-basename). Stable sort: pending basenames only fill what
            # the rest of the frontier cannot.
            pending = _pending_artifact_basenames()
            scored.sort(key=lambda item: Path(item[1]["source"]).stem in pending)
        for cascade, row in scored:
            if prepared >= count:
                break
            stem = Path(row["source"]).stem
            if stem in seen:
                continue
            seen.add(stem)
            classification = _case_classification(row["name"], row.get("source"))
            if classification == "native-migration-required":
                preflight_blocked += 1
                print(f"NEXT {row['name']} blocked phase=preflight detail={classification}")
                continue
            kind = "retry" if retry_red else "fresh"
            state = current.get(row["name"])
            generation = (
                state["generation"] + 1
                if state and (kind == "retry" or state["state"] == "stale")
                else 0
            )
            parent = state.get("attempt_id") if state else None
            fn = row["name"]
            try:
                issued = issue_attempt(fn, generation, parent_attempt_id=parent)
            except PreflightBlocker as exc:
                preflight_blocked += 1
                print(f"NEXT {fn} blocked phase=preflight detail={exc.detail}")
                continue
            except (LookupError, OSError, RuntimeError, ValueError) as exc:
                print(f"NEXT {fn} red detail={exc}")
                continue
            prepared += 1
            if kind == "retry":
                retry_selected += 1
            else:
                fresh_selected += 1
            run_dir = issued["run_dir"]
            print(f"NEXT {fn} size={row['size']}B basename={stem} cascade={cascade} "
                  f"attempt_id={issued['current']['attempt_id']} generation={generation}")
            print(f"python3 tools/factory/try_one.py --fn {fn} --candidates 3 "
                  f"--attempt-dir {run_dir}")

    current = _current_states()
    active = sum(1 for state in current.values() if state["state"] == "issued")
    exhausted = sum(
        1 for state in current.values()
        if state["state"] == "red" and state["generation"] >= retry_limit
    )
    eligible = len(pool)
    if prepared:
        status, exit_code = "selected", 0
    elif active:
        status, exit_code = "active", 3
    elif unresolved:
        status, exit_code = "stalled", 4
    else:
        status, exit_code = "complete", 5
    print(
        f"NEXT status={status} selected={prepared} fresh={fresh_selected} "
        f"retry={retry_selected} active={active} preflight_blocked={preflight_blocked} "
        f"exhausted={exhausted} eligible={eligible} reaped={len(reaped)} "
        f"revoked={len(revoked)}"
    )
    # A stall is only actionable if it names the next capability, so the report
    # goes out with the verdict rather than waiting for someone to ask.
    if status == "stalled":
        print_capability_frontier(records)
    return exit_code


def _result_paths() -> list[Path]:
    if not TRY_ROOT.is_dir():
        return []
    return sorted(TRY_ROOT.glob("*/attempts/*/result.json"))


def summarize() -> int:
    records = []
    for path in _result_paths():
        try:
            records.append(_read_json(path))
        except (OSError, json.JSONDecodeError, ValueError):
            print(f"unreadable {path}")
    green, phases, candidates = [], {}, 0
    for record in records:
        outcomes = record.get("results") or []
        candidates += len(outcomes)
        if any(entry.get("outcome") == "productive" for entry in outcomes):
            green.append(record["fn"])
        for entry in outcomes:
            if entry.get("outcome") != "productive":
                phase = entry.get("phase") or "unknown"
                phases[phase] = phases.get(phase, 0) + 1
    ordered = dict(sorted(phases.items(), key=lambda item: (-item[1], item[0])))
    print(f"GATE routines={len(records)} green={len(green)} candidates={candidates}")
    print(f"GATE green_routines={sorted(green)}")
    print(f"GATE failure_phases={ordered}")
    return 0 if records and len(set(green)) >= 4 else 1


def _prepare_direct(fn: str) -> dict[str, Any]:
    _check_operational_blocker(fn)
    # Same lock as subcommand_next: a direct try must not race a loop's
    # selection into a double claim on one routine.
    with common.file_lock(common.locks_dir() / "select.lock", timeout=900):
        existing = load_current_attempt(fn)
        if existing is None:
            return issue_attempt(fn, 0)
        state = existing["current"]
        if state["state"] == "issued":
            return existing
        return issue_attempt(
            fn,
            state["generation"] + 1,
            parent_attempt_id=state["attempt_id"],
        )


def _set_attempt_state(current: dict[str, Any], state: str, *, retry_limit: int,
                       unsupported: bool = False) -> None:
    fn = str(current["fn"])
    # A verification that finishes after its attempt was reaped and reissued must
    # discard its own result, not stamp it over the newer attempt: the on-disk
    # attempt id, not this process's memory, is the identity of record.
    on_disk = _read_current(fn)
    if on_disk is not None and on_disk["attempt_id"] != current["attempt_id"]:
        print(f"TRY {fn} superseded detail=attempt {str(current['attempt_id'])[:8]} "
              f"was replaced by {str(on_disk['attempt_id'])[:8]}")
        return
    current["state"] = state
    if unsupported:
        current["generation"] = max(current["generation"], retry_limit)
    # A red leaves the retry pool for exactly two reasons: the same diagnostic
    # twice (the packet decides, not the sample) or an exhausted budget. Either
    # way it must be recorded, because a red dropped from both pools without a
    # trace strands every routine that depends on it and stops convergence.
    retired = is_trapped(fn, current) or current["generation"] >= retry_limit
    if state == "red" and retired:
        record_trap(fn, current)
    _store_current(current)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fn", help="pret routine name")
    parser.add_argument("--summary", action="store_true",
                        help="aggregate every recorded run instead of verifying")
    parser.add_argument("--candidates", type=int, default=3)
    parser.add_argument("--reply", type=Path,
                        help="verify this recorded reply instead of polling for candidates")
    parser.add_argument("--wait", type=float, default=0.0,
                        help="seconds to wait for each candidate-<i>.json")
    parser.add_argument("--attempt-dir", type=Path,
                        help="explicit current attempt directory for dispatch output")
    parser.add_argument("--next", type=int, nargs="?", const=5, default=None,
                        help="prepare prompts for the next N routines")
    parser.add_argument("--retry-red", action="store_true",
                        help="with --next, select only retryable red attempts")
    parser.add_argument("--retry-limit", type=int, default=heal.DEFAULT_RETRY_LIMIT,
                        help="maximum attempt generation for autonomous retries; "
                             "each retry carries the previous diagnostic, and a "
                             "repeated signature is trapped rather than retried, so "
                             "the budget is spent only where retries are informative")
    parser.add_argument("--capabilities", type=int, nargs="?", const=5, default=None,
                        help="rank the remaining obstructions by how many routines "
                             "clearing each one alone would make reachable")
    arguments = parser.parse_args(argv)

    if arguments.retry_limit < 1:
        parser.error("--retry-limit must be at least 1")
    fn = arguments.fn
    if arguments.next is not None and fn:
        parser.error("--next and --fn are mutually exclusive")
    if arguments.capabilities is not None and (fn or arguments.next is not None):
        parser.error("--capabilities is exclusive with --fn and --next")
    if arguments.summary:
        return summarize()
    if arguments.capabilities is not None:
        if arguments.capabilities < 1:
            parser.error("--capabilities must be at least 1")
        report = packet_mod.report_module()
        records = report.compute(report.load_inventory(), report.load_routines()[0],
                                 report.load_gate())["work_records"]
        print_capability_frontier(records, limit=arguments.capabilities)
        return 0
    if arguments.next is not None:
        return subcommand_next(arguments.next, arguments.retry_red, arguments.retry_limit)
    if not fn:
        parser.error("--fn is required unless --summary, --next, or --capabilities is given")
    try:
        issued = _prepare_direct(fn)
    except OperationalBlocker as exc:
        blocker = exc.blocker
        print(f"TRY {fn} blocked phase=resolve detail={blocker.get('reason', 'operational blocker')} "
              f"unblock={blocker.get('unblock', 'clear the blocker')}")
        return 4
    except PreflightBlocker as exc:
        print(f"TRY {fn} blocked phase=preflight detail={exc.detail}")
        return 4
    except (LookupError, OSError, RuntimeError, ValueError) as exc:
        print(f"TRY {fn} red phases=['resolve'] detail={exc}")
        return 2

    try:
        built = verification_packet(issued)
    except OperationalBlocker as exc:
        blocker = exc.blocker
        print(f"TRY {fn} blocked phase=resolve detail={blocker.get('reason', 'operational blocker')} "
              f"unblock={blocker.get('unblock', 'clear the blocker')}")
        return 4
    except PreflightBlocker as exc:
        print(f"TRY {fn} blocked phase=preflight detail={exc.detail}")
        return 4
    except (LookupError, OSError, RuntimeError, ValueError) as exc:
        print(f"TRY {fn} red phases=['context'] detail={exc}")
        return 2
    if built is None:
        print(f"TRY {fn} stale phase=context detail=translation context changed")
        return 3

    routine = issued["routine"] if "routine" in issued else resolve(fn)[0]
    run_dir = arguments.attempt_dir.resolve() if arguments.attempt_dir else issued["run_dir"]
    if run_dir != issued["run_dir"]:
        run_dir = issued["run_dir"]
    replies: list[tuple[int, dict[str, Any] | None, str]] = []
    if arguments.reply is not None:
        try:
            recorded = _read_json(arguments.reply)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"TRY {fn} red phases=['reply'] detail={exc}")
            return 2
        if recorded.get("attempt_id") != issued["current"]["attempt_id"]:
            print("candidate 0: stale candidate ignored")
            print(f"TRY {fn} pending candidates=0 prompt={run_dir / 'prompt.txt'} "
                  f"size={routine['size']}B")
            return 3
        replies.append((0, recorded, ""))
    else:
        for index in range(arguments.candidates):
            path = run_dir / f"candidate-{index}.json"
            if not path.is_file() and arguments.wait <= 0:
                print(f"awaiting candidate {index}: {path}")
                print(dispatch_line(fn, run_dir, index,
                                    issued["current"].get("generation", 0)))
                continue
            try:
                reply = await_candidate(path, arguments.wait)
            except TimeoutError as exc:
                print(f"candidate {index} missing: {exc}")
                continue
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                print(f"candidate {index} unreadable: {exc}")
                replies.append((index, None, f"{type(exc).__name__}: {exc}"))
                continue
            if reply.get("attempt_id") != issued["current"]["attempt_id"]:
                print(f"candidate {index}: stale candidate ignored")
                continue
            replies.append((index, reply, ""))
        if not replies:
            print(f"TRY {fn} pending candidates=0 prompt={run_dir / 'prompt.txt'} "
                  f"size={routine['size']}B")
            return 3

    results: list[dict[str, Any]] = []
    green: dict[str, Any] | None = None
    # One claimed lane for the whole attempt: ensure() re-syncs it per candidate,
    # so candidate n's surgery cannot survive into candidate n+1, and no other
    # session can rsync into the slot while this process holds it.
    with lanes.claim() as lane_index:
        for index, reply, error in replies:
            if reply is None:
                record = {"candidate": index, "outcome": "diagnostic", "phase": "reply",
                          "failure_class": "schema", "witness": {}, "detail": error,
                          "seconds": 0.0}
            else:
                record = attempt(built, reply, lane_index=lane_index, candidate=index)
            results.append(record)
            print(f"candidate {index}: {record['outcome']} phase={record['phase']} "
                  f"{record['seconds']}s")
            if record["outcome"] == "productive":
                green = record
                break

    _write_json(issued["run_dir"] / "result.json", {
        "fn": fn,
        "work_id": routine["work_id"],
        "size": routine["size"],
        "feature_class": built["routines"][0]["feature_class"],
        "attempt_id": built["attempt_id"],
        "results": results,
    })
    unsupported = any(entry.get("failure_class") == "unsupported-evidence" for entry in results)
    _set_attempt_state(
        issued["current"],
        "green" if green is not None else "red",
        retry_limit=arguments.retry_limit,
        unsupported=unsupported,
    )
    if green is not None:
        print(f"TRY {fn} green candidate={green['candidate']} seconds={green['seconds']} "
              f"artifact={green['artifact_sha256'][:16]}")
        return 0
    if unsupported:
        print(f"TRY {fn} blocked phase=cases failure_class=unsupported-evidence "
              f"detail=no primary oracle case")
        return 4
    phases = [record["phase"] for record in results]
    print(f"TRY {fn} red phases={phases}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
