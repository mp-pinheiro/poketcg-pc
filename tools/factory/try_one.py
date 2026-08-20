#!/usr/bin/env python3
"""Port one routine with k independent candidates and the real verifier.

This is the instrument that separates "can a model produce an acceptable
fragment set" from "can the control plane account for it": there is no Forgejo,
no ledger, no lease, and no model client. Candidates arrive either from a
recorded reply file or from generator agents the orchestrating session
dispatches, which drop `candidate-<i>.json` into the run directory.

Verification is `verify.verify_packet` — the same phase order the factory uses —
so a green here is a green there. Every failure is reported as a phase verdict;
the process never exits with a traceback.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common
import lanes
import packet as packet_mod
import prompt as prompt_mod
import surgery
import verify
import workers

TRY_ROOT = common.FACTORY / "try"


def resolve(fn: str) -> tuple[dict[str, Any], dict[str, Any]]:
    functions, _inventory = packet_mod.compute_functions()
    matched = [f for f in functions if f["name"] == fn]
    if not matched:
        raise LookupError(f"{fn} is not in the pret inventory")
    if len(matched) > 1:
        raise LookupError(f"{fn} is ambiguous across {len(matched)} inventory records")
    routine = matched[0]
    work_id = routine.get("work_id")
    if not isinstance(work_id, str) or not work_id:
        raise LookupError(f"{fn} has no canonical work id; it is out of scope")
    packets = packet_mod.build_packets_for_work_ids({work_id}, issue_numbers={work_id: 0})
    if len(packets) != 1:
        raise LookupError(f"{fn} produced {len(packets)} packets")
    return routine, packets[0]


def dispatch_line(fn: str, run_dir: Path, index: int) -> str:
    return (f"task(agent=\"port-worker\", task=\"Read {run_dir / 'prompt.txt'} and write the "
            f"TranslationReplyV2 JSON object it asks for to "
            f"{run_dir / f'candidate-{index}.json'}. Emit no prose.\")")


def await_candidate(path: Path, wait: float) -> dict[str, Any]:
    """Read a candidate as soon as it exists, waiting at most ``wait`` seconds.

    A zero wait still reads a candidate already on disk, which is the whole
    point when generation and verification are separate invocations.
    """
    deadline = time.monotonic() + wait
    while not path.is_file():
        if time.monotonic() >= deadline:
            raise TimeoutError(f"no candidate at {path} after {wait:.0f}s")
        time.sleep(1.0)
    return json.loads(path.read_text())


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


def _reuse(path: Path, fresh: dict[str, Any]) -> dict[str, Any]:
    """Keep the packet a prompt was rendered from, so candidates written
    against that prompt still carry a matching attempt_id. A packet built for
    a different tree state is discarded rather than reused."""
    if not path.is_file():
        return fresh
    try:
        previous = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return fresh
    same = (
        isinstance(previous, dict)
        and previous.get("base_commit") == fresh["base_commit"]
        and previous.get("inventory_fingerprint") == fresh["inventory_fingerprint"]
        and [r["work_id"] for r in previous.get("routines") or []]
        == [r["work_id"] for r in fresh["routines"]]
    )
    return common.validate_packet(previous) if same else fresh


def summarize() -> int:
    """Print the stop/go gate result over every recorded run."""
    records = []
    for path in sorted(TRY_ROOT.glob("*/result.json")):
        try:
            records.append(json.loads(path.read_text()))
        except (OSError, json.JSONDecodeError):
            print(f"unreadable {path}")
    green, phases, candidates = [], {}, 0
    for record in records:
        outcomes = record.get("results") or []
        candidates += len(outcomes)
        if any(entry.get("outcome") == "productive" for entry in outcomes):
            green.append(record["fn"])
        for entry in outcomes:
            if entry.get("outcome") != "productive":
                phases[entry.get("phase") or "unknown"] = phases.get(entry.get("phase") or "unknown", 0) + 1
    ordered = dict(sorted(phases.items(), key=lambda item: (-item[1], item[0])))
    print(f"GATE routines={len(records)} green={len(green)} candidates={candidates}")
    print(f"GATE green_routines={sorted(green)}")
    print(f"GATE failure_phases={ordered}")
    for record in records:
        status = "green" if record["fn"] in green else "red"
        print(f"  {record['fn']:<40} {status:<5} {record.get('size')}B "
              f"{record.get('feature_class')} phases="
              f"{[entry.get('phase') for entry in record.get('results') or []]}")
    return 0 if len(green) >= 4 else 1


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
    arguments = parser.parse_args(argv)

    fn = arguments.fn
    if arguments.summary:
        return summarize()
    if not arguments.fn:
        parser.error("--fn is required unless --summary is given")
    run_dir = TRY_ROOT / fn
    run_dir.mkdir(parents=True, exist_ok=True)
    try:
        routine, built = resolve(fn)
    except (LookupError, OSError, RuntimeError, ValueError) as exc:
        print(f"TRY {fn} red phases=['resolve'] detail={exc}")
        return 2
    stored_packet = run_dir / "packet.json"
    built = _reuse(stored_packet, built)
    (run_dir / "prompt.txt").write_text(prompt_mod.render(built))
    stored_packet.write_text(json.dumps(built, sort_keys=True, indent=2))

    replies: list[tuple[int, dict[str, Any] | None, str]] = []
    if arguments.reply is not None:
        try:
            recorded = json.loads(arguments.reply.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            print(f"TRY {fn} red phases=['reply'] detail={exc}")
            return 2
        recorded["attempt_id"] = built["attempt_id"]
        replies.append((0, recorded, ""))
    else:
        for index in range(arguments.candidates):
            path = run_dir / f"candidate-{index}.json"
            if not path.is_file() and arguments.wait <= 0:
                print(f"awaiting candidate {index}: {path}")
                print(dispatch_line(fn, run_dir, index))
                continue
            try:
                replies.append((index, await_candidate(path, arguments.wait), ""))
            except TimeoutError as exc:
                print(f"candidate {index} missing: {exc}")
            except (OSError, json.JSONDecodeError) as exc:
                print(f"candidate {index} unreadable: {exc}")
                replies.append((index, None, f"{type(exc).__name__}: {exc}"))
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

    (run_dir / "result.json").write_text(json.dumps({
        "fn": fn,
        "work_id": routine["work_id"],
        "size": routine["size"],
        "feature_class": built["routines"][0]["feature_class"],
        "attempt_id": built["attempt_id"],
        "results": results,
    }, sort_keys=True, indent=2) + "\n")

    if green is not None:
        print(f"TRY {fn} green candidate={green['candidate']} seconds={green['seconds']} "
              f"artifact={green['artifact_sha256'][:16]}")
        return 0
    phases = [record["phase"] for record in results]
    print(f"TRY {fn} red phases={phases}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
