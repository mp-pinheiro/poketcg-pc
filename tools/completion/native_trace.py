#!/usr/bin/env python3
"""Resolve the native call trace and diff its per-routine counts against the reference."""

from __future__ import annotations

import argparse
import os
import json
import struct
import subprocess
import sys
from bisect import bisect_right
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream

MAGIC = b"PTCGTRC2"
# used slots, then the total call count the run made across all of them; the
# tracer aggregates, so the file size is bounded by the routine count.
HEADER = struct.Struct("<8sQQIIQ")
RECORD = struct.Struct("<IIQ")


class NativeTraceError(RuntimeError):
    pass


def load_symbols(binary: Path) -> list[tuple[int, str]]:
    result = subprocess.run(
        ["nm", "--defined-only", str(binary)], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise NativeTraceError(f"nm failed on {binary}: {result.stderr.strip()[:200]}")
    symbols = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[1] in ("T", "t"):
            symbols.append((int(parts[0], 16), parts[2]))
    if not symbols:
        raise NativeTraceError(f"{binary} exposes no text symbols")
    symbols.sort()
    return symbols


def resolver(symbols: list[tuple[int, str]]):
    addresses = [address for address, _name in symbols]

    def resolve(address: int) -> str | None:
        index = bisect_right(addresses, address) - 1
        return symbols[index][1] if index >= 0 else None

    return resolve


def load_trace(path: Path) -> tuple[int, list[tuple[int, int, int]], bool, int]:
    raw = path.read_bytes()
    if len(raw) < HEADER.size:
        raise NativeTraceError(f"{path} is too short to be a call trace")
    magic, base, count, overflow, record_size, calls = HEADER.unpack_from(raw)
    if magic != MAGIC:
        raise NativeTraceError(f"{path} is not a native call trace")
    if record_size != RECORD.size:
        raise NativeTraceError(f"{path} record size {record_size} != {RECORD.size}")
    records = [
        RECORD.unpack_from(raw, HEADER.size + index * RECORD.size)
        for index in range(count)
    ]
    return base, records, bool(overflow), calls


def native_counts(
    binary: Path, trace: Path
) -> tuple[dict[str, int], dict[str, int], bool, int]:
    symbols = load_symbols(binary)
    resolve = resolver(symbols)
    base_symbol = next((address for address, name in symbols if name == "trace_set_frame"), None)
    if base_symbol is None:
        raise NativeTraceError(f"{binary} has no trace_set_frame symbol")
    _base, records, overflow, calls = load_trace(trace)
    counts: dict[str, int] = {}
    first_frame: dict[str, int] = {}
    for callee, frame, slot_calls in records:
        name = resolve(base_symbol + callee)
        if name is None:
            continue
        counts[name] = counts.get(name, 0) + slot_calls
        if name not in first_frame or frame < first_frame[name]:
            first_frame[name] = frame
    return counts, first_frame, overflow, calls


def build_report(
    scenario: str, frames: int, binary: Path, trace: Path, limit: int
) -> dict[str, Any]:
    counts, first_frame, overflow, total = native_counts(binary, trace)
    # The native lane counts DoFrames, so the reference must be bounded by the
    # same anchor count rather than by PPU frames, which span a different
    # amount of emulated time. `frames + 400` only caps the emulation length.
    reference = refstream.routine_trace(scenario, frames + 400, None, ordinals=frames)
    reference_counts = {row["routine"]: row["count"] for row in reference["calls"]}
    # Only names the reference can even report are comparable: the port has
    # adapters and helpers with no ROM counterpart, and 259 registered routines
    # have no native text symbol because the compiler inlined them.
    universe = sorted(set(reference_counts) & set(counts))
    rows = []
    for name in universe:
        native = counts[name]
        ref = reference_counts[name]
        if native != ref:
            rows.append({
                "routine": name,
                "native": native,
                "reference": ref,
                "delta": native - ref,
                "ratio": round(native / ref, 4) if ref else None,
                "native_first_frame": first_frame.get(name),
            })
    rows.sort(key=lambda row: (-abs(row["delta"]), row["routine"]))
    missing = sorted(set(reference_counts) - set(counts))
    return {
        "schema": 1,
        "format": "native-trace-diff-v1",
        "scenario": scenario,
        "frames": frames,
        "native_records": total,
        "native_overflow": overflow,
        "comparable_routines": len(universe),
        "reference_routines": len(reference_counts),
        "divergent_routines": len(rows),
        "reference_only": missing[:limit],
        "reference_only_total": len(missing),
        "rows": rows[:limit],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario")
    parser.add_argument("--frames", type=int, default=2000)
    parser.add_argument("--binary",
                        default=os.environ.get("POKETCG_BUILD", "build") + "-trace/poketcg")
    parser.add_argument("--trace", required=True)
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--json")
    args = parser.parse_args(argv)
    try:
        report = build_report(
            args.scenario, args.frames,
            Path(args.binary) if Path(args.binary).is_absolute() else ROOT / args.binary,
            Path(args.trace) if Path(args.trace).is_absolute() else ROOT / args.trace,
            args.limit,
        )
    except (NativeTraceError, refstream.RefstreamError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json:
        Path(args.json).write_text(text + "\n")
    print(text)
    return 0 if not report["rows"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
