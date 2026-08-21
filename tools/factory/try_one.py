#!/usr/bin/env python3
"""Port one routine with k independent candidates and the real verifier."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
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



def resolve(fn: str) -> tuple[dict[str, Any], dict[str, Any]]:
    _check_operational_blocker(fn)
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
    work_id = routine.get("work_id")
    if not isinstance(work_id, str) or not work_id:
        raise LookupError(f"{fn} has no canonical work id; it is out of scope")
    packets = packet_mod.build_packets_for_work_ids({work_id}, issue_numbers={work_id: 0})
    if len(packets) != 1:
        raise LookupError(f"{fn} produced {len(packets)} packets")
    return routine, packets[0]


def dispatch_line(fn: str, run_dir: Path, index: int) -> str:
    return (f"task(agent=\"port-candidate\", task=\"Read {run_dir / 'prompt.txt'} and write the "
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


def issue_attempt(fn: str, generation: int, *, parent_attempt_id: str | None = None) -> dict[str, Any]:
    routine, packet = resolve(fn)
    packet["attempt_generation"] = generation
    packet["parent_attempt_id"] = parent_attempt_id
    context_sha256 = packet_mod.translation_context_sha256(packet)
    attempt_id = packet["attempt_id"]
    run_dir = _attempt_root(fn) / "attempts" / attempt_id
    run_dir.mkdir(parents=True, exist_ok=False)
    _write_json(run_dir / "packet.json", packet)
    (run_dir / "prompt.txt").write_text(prompt_mod.render(packet))
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
        stored = workers.store_artifact(workers.stage_bundle(built, lane))
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
    quarantined = _quarantined_artifacts()
    names: set[str] = set()
    for record in workers.artifact_records():
        if record.get("artifact_sha256") in quarantined:
            continue
        for routine in (record.get("identity") or {}).get("routines") or []:
            if isinstance(routine, dict) and isinstance(routine.get("name"), str):
                names.add(routine["name"])
    return names
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


def subcommand_next(count: int, retry_red: bool, retry_limit: int) -> int:
    report = packet_mod.report_module()
    records = report.compute(report.load_inventory(), report.load_routines()[0],
                             report.load_gate())["work_records"]
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
    prepared = 0
    fresh_selected = 0
    retry_selected = 0
    preflight_blocked = 0
    seen: set[str] = set()
    for cascade, row in _score_rows(pool, retry=retry_red):
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
        lane = 700 + 10 * prepared
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
        print(f"NEXT {fn} lane={lane} size={row['size']}B basename={stem} cascade={cascade} "
              f"attempt_id={issued['current']['attempt_id']} generation={generation}")
        print(f"python3 tools/factory/try_one.py --fn {fn} --candidates 3 --lane {lane} "
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
        f"exhausted={exhausted} eligible={eligible}"
    )
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
    current["state"] = state
    if unsupported:
        current["generation"] = max(current["generation"], retry_limit)
    _store_current(current)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fn", help="pret routine name")
    parser.add_argument("--summary", action="store_true",
                        help="aggregate every recorded run instead of verifying")
    parser.add_argument("--candidates", type=int, default=3)
    parser.add_argument("--lane", type=int, default=700, help="first lane index")
    parser.add_argument("--reply", type=Path,
                        help="verify this recorded reply instead of polling for candidates")
    parser.add_argument("--wait", type=float, default=0.0,
                        help="seconds to wait for each candidate-<i>.json")
    parser.add_argument("--attempt-dir", type=Path,
                        help="explicit current attempt directory for dispatch output")
    parser.add_argument("--next", type=int, nargs="?", const=4, default=None,
                        help="prepare prompts for the next N routines")
    parser.add_argument("--retry-red", action="store_true",
                        help="with --next, select only retryable red attempts")
    parser.add_argument("--retry-limit", type=int, default=1,
                        help="maximum attempt generation for autonomous retries")
    arguments = parser.parse_args(argv)

    if arguments.retry_limit < 1:
        parser.error("--retry-limit must be at least 1")
    fn = arguments.fn
    if arguments.next is not None and fn:
        parser.error("--next and --fn are mutually exclusive")
    if arguments.summary:
        return summarize()
    if arguments.next is not None:
        return subcommand_next(arguments.next, arguments.retry_red, arguments.retry_limit)
    if not fn:
        parser.error("--fn is required unless --summary or --next is given")
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
                print(dispatch_line(fn, run_dir, index))
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
    for index, reply, error in replies:
        if reply is None:
            record = {"candidate": index, "outcome": "diagnostic", "phase": "reply",
                      "failure_class": "schema", "witness": {}, "detail": error,
                      "seconds": 0.0}
        else:
            record = attempt(built, reply, lane_index=arguments.lane + index,
                             candidate=index)
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
