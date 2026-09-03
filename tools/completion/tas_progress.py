#!/usr/bin/env python3
"""How far the port tracks the ROM through a TAS movie, and what stops it."""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import composition_audit
import native_trace


class ProgressError(RuntimeError):
    pass


def basename_of(path: str) -> str:
    return Path(path).stem


def case_basenames() -> dict[str, str]:
    import importlib.util

    mapping: dict[str, str] = {}
    for path in sorted((ROOT / "tests" / "cases").glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"case_{path.stem}", path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:  # noqa: BLE001 - a broken case module must not stop the gate
            print(f"skipped {path.name}: {exc}", file=sys.stderr)
            continue
        for name in getattr(module, "CONTRACT", {}):
            mapping.setdefault(name, path.stem)
    return mapping


def run_native(binary: Path, pack: Path, masks: Path, frames: int, trace: Path,
               timeout: float) -> str:
    """Runs the instrumented lane and returns what stopped it, empty when clean.

    src/trace.c writes the trace on SIGABRT, so a run that dies on an unported
    script entry is still measured up to that point, and a run that hangs in a
    wait loop is signalled here to get the same treatment. Either way the reason
    is reported as `blocked_by` instead of swallowing the numbers, which is what
    keeps every iteration of the loop comparable.
    """
    if trace.exists():
        trace.unlink()
    command = [str(binary), "--headless", "--data-pack", str(pack),
               "--frames", str(frames), "--input", str(masks),
               "--trace-calls", str(trace)]
    process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True)
    hung = False
    try:
        _out, errors = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        hung = True
        process.send_signal(signal.SIGABRT)
        try:
            _out, errors = process.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            process.kill()
            raise ProgressError(
                f"native run ignored SIGABRT after {timeout:g}s") from None

    if hung:
        reason = f"HANG no exit within {timeout:g}s"
    elif process.returncode == 0:
        return ""
    else:
        reason = (errors.strip().splitlines() or ["unknown"])[-1][:200]
    if not trace.exists():
        raise ProgressError(f"native run failed with no trace: {reason}")
    return reason


def report(
    reference_path: Path, binary: Path, trace: Path, limit: int, blocked_by: str = ""
) -> dict[str, Any]:
    reference = json.loads(reference_path.read_text())
    rows = {row["routine"]: row for row in reference["calls"]}
    if not rows or "first_ordinal" not in next(iter(rows.values())):
        raise ProgressError(f"{reference_path} lacks first_ordinal; re-run refstream trace")
    native, _first, overflow, records = native_trace.native_counts(binary, trace)
    symbols = {name for _address, name in native_trace.load_symbols(binary)}
    inventory = json.loads((ROOT / "site" / "data" / "inventory.json").read_text())["functions"]
    owners = case_basenames()

    # A reference routine the port has no symbol for is not comparable: the port
    # inlines local labels, and bank trampolines like BankpushROM have no C body
    # by design. Only a routine the binary exports can be called and missed.
    comparable = {name for name in rows if name in symbols}
    reached = {name for name in comparable if name in native}
    missing = sorted(
        (rows[name]["first_ordinal"], name) for name in comparable - reached
    )
    reached_ordinal = max((rows[name]["first_ordinal"] for name in reached), default=0)
    total_ordinals = int(reference.get("ordinals_reached") or 0)

    # A routine the ROM first runs at an ordinal the port already passed cannot
    # be what stops it: the port demonstrably got there without it. Those are
    # structural differences (bank trampolines, dispatch the port inlines).
    # Only misses at or beyond the frontier can block progress.
    frontier = [(ordinal, name) for ordinal, name in missing if ordinal >= reached_ordinal]
    structural = len(missing) - len(frontier)

    # `blockers` below is filtered to ordinals at or past reached_ordinal, and
    # reached_ordinal is a max over reached routines, so one incidental call to
    # a late routine raises the bar and reclassifies every genuine miss under it
    # as structural. That is not hypothetical: a single DisableSpriteAnim call
    # (reference ordinal 21,337) hid StartDuel and twenty duel-setup routines at
    # 21,074. `misses` is the same data unfiltered, so the earliest thing the
    # ROM does that the port does not is always misses[0].
    def describe(ordinal: int, name: str) -> dict[str, Any]:
        source = inventory.get(name, {}).get("file", "")
        return {
            "routine": name,
            "reference_first_ordinal": ordinal,
            "reference_calls": rows[name]["count"],
            "source": source,
            "basename": owners.get(name, basename_of(source) if source else "?"),
        }

    misses = [describe(ordinal, name) for ordinal, name in missing[:limit]]
    blockers = [describe(ordinal, name) for ordinal, name in frontier[:limit]]
    by_basename: dict[str, int] = {}
    for _ordinal, name in frontier:
        source = inventory.get(name, {}).get("file", "")
        key = owners.get(name, basename_of(source) if source else "?")
        by_basename[key] = by_basename.get(key, 0) + 1
    audits = composition_audit.counts()
    return {
        "schema": 1,
        "format": "tas-progress-v2",
        "reference": str(reference_path.relative_to(ROOT)),
        "blocked_by": blocked_by,
        "native_records": records,
        "native_overflow": overflow,
        "reference_ordinals": total_ordinals,
        "reached_ordinal": reached_ordinal,
        "progress_pct": round(100.0 * reached_ordinal / total_ordinals, 2) if total_ordinals else None,
        "comparable_routines": len(comparable),
        "reached_routines": len(reached),
        "executed_routines": len(native),
        "translated_routines": len(inventory),
        "missing_routines": len(missing),
        "structural_misses": structural,
        "frontier_misses": len(frontier),
        "misses": misses,
        "blockers": blockers,
        "frontier_by_basename": dict(sorted(by_basename.items(), key=lambda kv: -kv[1])),
        **audits,
    }


RATCHET_PATH = ROOT / "tools" / "completion" / "tas_ratchet.json"
# Progress may only move one way: the routine set sizes rise, the audit counts
# fall. `reached_ordinal` is deliberately not ratcheted. It is a max over the
# reference first_ordinal of every routine the port reached, so one incidental
# call to a routine the ROM first runs late sets it arbitrarily high while the
# port is stuck far earlier. That is measured, not theoretical: an incidental
# GoToPreviousCardPage call (reference ordinal 46,969) reported 66.15% while
# the port actually tracked to 24,677, and completing SwitchCardPage's dispatch
# removed the incidental call and appeared as a 22,000-ordinal regression.
# Read it as a ceiling on depth, never as progress; the set sizes are the gate.
RATCHET_RISING = ("reached_routines", "executed_routines")
RATCHET_FALLING = ("loops", "banks", "jumps")


def check_ratchet(payload: dict[str, Any]) -> dict[str, Any] | None:
    if not RATCHET_PATH.is_file():
        return None
    recorded = json.loads(RATCHET_PATH.read_text())
    for key in RATCHET_RISING:
        if key in recorded and payload[key] < recorded[key]:
            return {"status": "REGRESSION", "key": key,
                    "was": recorded[key], "now": payload[key]}
    for key in RATCHET_FALLING:
        if key in recorded and payload[key] > recorded[key]:
            return {"status": "REGRESSION", "key": key,
                    "was": recorded[key], "now": payload[key]}
    return None


def write_ratchet(payload: dict[str, Any]) -> dict[str, int]:
    recorded = json.loads(RATCHET_PATH.read_text()) if RATCHET_PATH.is_file() else {}
    for key in RATCHET_RISING:
        recorded[key] = max(int(payload[key]), int(recorded.get(key, 0)))
    for key in RATCHET_FALLING:
        current = int(payload[key])
        recorded[key] = min(current, int(recorded.get(key, current)))
    RATCHET_PATH.write_text(json.dumps(recorded, indent=2, sort_keys=True) + "\n")
    return recorded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", default="build/completion/tas/ref-5530b.json")
    parser.add_argument("--masks", default="build/completion/tas/input.txt")
    parser.add_argument("--binary", default="build-trace/poketcg")
    parser.add_argument("--pack", default="build/completion/data-pack.bin")
    parser.add_argument("--trace", default="build/completion/tas/native-progress.bin")
    parser.add_argument("--frames", type=int, default=78207)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--run-timeout", type=float, default=240.0,
                        help="seconds before the run is aborted for its trace")
    parser.add_argument("--skip-run", action="store_true", help="reuse an existing trace")
    parser.add_argument("--write-ratchet", action="store_true",
                        help="raise the ratchet to the measured values")
    parser.add_argument("--json")
    args = parser.parse_args(argv)

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path

    try:
        blocked_by = ""
        if not args.skip_run:
            blocked_by = run_native(
                resolve(args.binary), resolve(args.pack), resolve(args.masks),
                args.frames, resolve(args.trace), args.run_timeout)
        payload = report(resolve(args.reference), resolve(args.binary),
                         resolve(args.trace), args.limit, blocked_by)
    except (ProgressError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2

    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.json:
        resolve(args.json).write_text(text + "\n")
    print(text)
    if args.write_ratchet:
        print(json.dumps({"ratchet": write_ratchet(payload)}, sort_keys=True))
        return 0
    regression = check_ratchet(payload)
    if regression:
        print(json.dumps(regression, sort_keys=True), file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
