#!/usr/bin/env python3
"""Which unexecuted routines does an input tail reach? One native run per tail.

A recorded session's input plus a suffix of explore.py action labels is the
cheapest question in the loop: it runs on the native lane alone (~1 s), needs
no reference replay, and the same label list records the session verbatim
(`session.py seeded --then`, `board-seed --then`). It measures reach, never
correctness: a hit says the input arrives somewhere no session has been, and
the proof is the recorded session's own verify.

The native trace names every C symbol the binary defines, including helpers
the ROM has no routine for, so a raw new-symbol count overstates reach by a
constant ~130. Intersecting with the ledger's routine set and subtracting its
executed set leaves the exact signal.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import coverage_ledger
import explore
import native_trace
import refstream
import scenario as scenario_module
import session as session_module

TRACE_BINARY = ROOT / "build-trace" / "poketcg"


class ProbeError(RuntimeError):
    pass


def parse_tail(text: str) -> list[str]:
    """A comma-separated explore label list, the same form session.py --then takes."""
    labels = [part.strip() for part in text.split(",") if part.strip()]
    known = {label for label, *_rest in explore.actions()}
    unknown = [label for label in labels if label not in known]
    if unknown:
        raise ProbeError(f"unknown action labels {unknown}; see explore.py actions()")
    return labels


def native_reach(base: str, tail: list[str]) -> dict[str, int]:
    """Per-routine native call counts for the base session's input plus tail."""
    if not TRACE_BINARY.is_file():
        raise ProbeError(f"no trace binary at {TRACE_BINARY.relative_to(ROOT)}: run `just build-trace`")
    directory = session_module.session_dir(base)
    input_path = directory / "input.txt"
    if not input_path.is_file():
        raise ProbeError(f"no session input at {input_path.relative_to(ROOT)}")
    masks = explore.path_to_masks(tail, refstream.load_masks(input_path))
    with tempfile.TemporaryDirectory(prefix="probe-") as raw:
        tmp = Path(raw)
        timeline = tmp / "input.txt"
        timeline.write_text(",".join(str(mask) for mask in masks) + "\n")
        trace = tmp / "calls.bin"
        command = [
            str(TRACE_BINARY), "--headless",
            "--data-pack", str(scenario_module.PACK),
            "--frames", "0",
            "--stop-ordinal", str(len(masks)),
            "--input-ordinal", str(timeline),
            "--trace-calls", str(trace),
        ]
        pokes = directory / "pokes.txt"
        if pokes.is_file():
            command += ["--poke-ordinal", str(pokes)]
        save = directory / "save.sav"
        if save.is_file():
            wrapped = tmp / "save.pksr"
            wrapped.write_bytes(session_module.native_save_file(save.read_bytes()))
            command += ["--load-save", str(wrapped)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        if not trace.is_file():
            detail = (result.stderr or result.stdout).strip()[-200:]
            raise ProbeError(f"native run wrote no trace: {detail}")
        counts, _first, _overflow, _calls = native_trace.native_counts(TRACE_BINARY, trace)
    return counts


def probe(base: str, tail: list[str], ledger: dict[str, Any], executed: set[str],
          marks: list[str]) -> dict[str, Any]:
    counts = native_reach(base, tail)
    routines = ledger["routines"]
    reached = sorted(
        name for name in counts
        if name in routines and not routines[name].get("excluded")
        and not routines[name].get("unmeasurable") and name not in executed
    )
    return {
        "tail": ",".join(tail),
        "routines": len(counts),
        "unexecuted": reached,
        "marks": sorted(name for name in marks if counts.get(name)),
        "missing_marks": sorted(name for name in marks if not counts.get(name)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", help="recorded session whose input the tail extends")
    parser.add_argument("--tail", action="append", default=[],
                        help="comma-separated explore labels (repeatable; empty probes the base)")
    parser.add_argument("--mark", action="append", default=[],
                        help="routine that must run for the tail to count (repeatable, comma-separated)")
    parser.add_argument("--jobs", type=int, default=4, help="tails probed in parallel")
    parser.add_argument("--limit", type=int, default=12, help="unexecuted names printed per tail")
    parser.add_argument("--json", help="write the full report here")
    args = parser.parse_args(argv)

    marks: list[str] = []
    for item in args.mark:
        marks += [name.strip() for name in item.split(",") if name.strip()]
    try:
        tails = [parse_tail(text) for text in (args.tail or [""])]
        ledger = coverage_ledger.load_ledger()
        executed = coverage_ledger.executed_set(ledger)
        with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
            rows = list(pool.map(lambda tail: probe(args.base, tail, ledger, executed, marks), tails))
    except (ProbeError, coverage_ledger.CoverageError, native_trace.NativeTraceError,
            refstream.RefstreamError, session_module.SessionError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2

    for row in rows:
        names = row["unexecuted"][:args.limit]
        more = len(row["unexecuted"]) - len(names)
        print(f"PROBE {args.base} tail={row['tail'] or '-'} routines={row['routines']} "
              f"unexecuted={len(row['unexecuted'])}"
              + (f" marks={len(row['marks'])}/{len(marks)}" if marks else "")
              + (f" {', '.join(names)}" if names else "")
              + (f" +{more}" if more > 0 else ""), flush=True)
    best = max(rows, key=lambda row: (len(row["marks"]), len(row["unexecuted"])))
    print(f"BEST tail={best['tail'] or '-'} unexecuted={len(best['unexecuted'])} "
          f"marks={','.join(best['marks']) or '-'}")
    if args.json:
        Path(args.json).write_text(json.dumps({"schema": 1, "base": args.base, "rows": rows},
                                              indent=2, sort_keys=True) + "\n")
    return 0 if best["unexecuted"] or best["marks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
