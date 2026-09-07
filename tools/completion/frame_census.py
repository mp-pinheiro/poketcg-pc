#!/usr/bin/env python3
"""Per-anchor divergence census: the earliest ordinal each byte goes wrong."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import scenario as scenario_module

# The raw `io` store is not comparable against an emulator: the reference side
# is bus readback (gambatte_cpuread) while the native side dumps g_io, so
# unmapped addresses that read $FF on hardware but hold $00 in the array show
# as 44 constant phantom bytes. `io_readback` is the native gb_read8 result for
# $FF00-$FF7F (src/state_dump.c) and is the like-for-like comparison; plain
# `io` stays available via --domains for inspecting the store itself.
DEFAULT_DOMAINS = ("wram", "hram", "oam", "io_readback")
FIELD_BASE = {
    "wram": 0xC000, "hram": 0xFF80, "io": 0xFF00, "io_readback": 0xFF00,
    "oam": 0xFE00,
}
REFERENCE_DOMAIN = {"io_readback": "io"}


class FrameCensusError(RuntimeError):
    pass


def exclusion_mask(field: str, length: int) -> bytes:
    ledger = REFERENCE_DOMAIN.get(field, field)
    mask = bytearray(length)
    for start, end in scenario_module.COMPARATOR_EXCLUDED_RANGES.get(ledger, ()):
        for index in range(max(0, start), min(length, end)):
            mask[index] = 1
    return bytes(mask)


def run_native(directory: Path, frames: int, dump_frames: list[int], masks: list[int]) -> Path:
    input_path = directory / "input.txt"
    input_path.write_text(",".join(str(value) for value in masks) + "\n")
    state_path = directory / "state.json"
    command = [
        str(scenario_module.BINARY), "--headless",
        "--data-pack", str(scenario_module.PACK),
        "--frames", str(frames),
        "--input", str(input_path),
        "--dump-state", str(state_path),
        "--dump-state-frames", ",".join(str(frame) for frame in dump_frames),
        "--trace-entries", str(directory / "trace.json"),
    ]
    result = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, timeout=300, check=False
    )
    if result.returncode != 0:
        raise FrameCensusError(f"native run failed: {result.stderr.strip()[:400]}")
    return state_path


def native_dumps(state_path: Path) -> dict[int, dict[str, Any]]:
    dumps = {}
    for path in state_path.parent.glob(f"{state_path.stem}-f*.json"):
        frame = int(path.stem.split("-f")[1])
        dumps[frame] = json.loads(path.read_text())
    return dumps


def compare_frame(
    native: dict[str, Any], stream: refstream.Stream, ordinal: int, domains: tuple[str, ...],
    extra_excluded: dict[str, list[tuple[int, int]]] | None = None,
) -> list[tuple[str, int, int, int]]:
    """(field, offset, native byte, reference byte) for one anchor ordinal.
    `extra_excluded` adds field-relative [start, end) ranges on top of the
    scenario ledger for callers whose axis makes more state timing-phase."""
    rows = []
    for field in domains:
        reference = stream.domain(ordinal, REFERENCE_DOMAIN.get(field, field))
        values = native.get(field)
        if not isinstance(values, list):
            continue
        mask = bytearray(exclusion_mask(field, len(reference)))
        for start, end in (extra_excluded or {}).get(field, ()):
            for index in range(max(0, start), min(len(mask), end)):
                mask[index] = 1
        for offset in range(min(len(reference), len(values))):
            if mask[offset]:
                continue
            if values[offset] != reference[offset]:
                rows.append((field, offset, values[offset], reference[offset]))
    return rows


def earliest_divergence(
    scenario: str, frames: int, step: int, domains: tuple[str, ...], refine: bool,
    masks: list[int] | None = None
) -> dict[str, Any]:
    # A movie is frame-indexed while an anchor is one reference DoFrame, and the
    # two axes advance at different rates, so the reference run is bounded by the
    # movie's length and stops on the anchor count instead.
    bound = len(masks) if masks else frames + 400
    stream = refstream.open_stream(scenario, bound, frames + 100, masks)
    masks = refstream.scenario_masks(scenario, frames, masks)
    coarse = [frame for frame in range(step, frames + 1, step)]
    first: dict[tuple[str, int], tuple[int, int, int]] = {}
    with tempfile.TemporaryDirectory() as directory:
        state_path = run_native(Path(directory), frames, coarse, masks)
        for frame, native in sorted(native_dumps(state_path).items()):
            ordinal = frame - 1
            if ordinal >= stream.count:
                continue
            for field, offset, got, want in compare_frame(native, stream, ordinal, domains):
                first.setdefault((field, offset), (frame, got, want))
    if refine and first:
        windows = sorted({
            frame
            for coarse_frame, _got, _want in first.values()
            for frame in range(max(1, coarse_frame - step + 1), coarse_frame + 1)
        })
        with tempfile.TemporaryDirectory() as directory:
            state_path = run_native(Path(directory), frames, windows, masks)
            for frame, native in sorted(native_dumps(state_path).items()):
                ordinal = frame - 1
                if ordinal >= stream.count:
                    continue
                for field, offset, got, want in compare_frame(native, stream, ordinal, domains):
                    key = (field, offset)
                    if key in first and frame < first[key][0]:
                        first[key] = (frame, got, want)
    return {"stream": stream, "first": first}


def build_report(
    scenario: str, frames: int, step: int, domains: tuple[str, ...], refine: bool,
    attribute: bool, masks: list[int] | None = None
) -> dict[str, Any]:
    found = earliest_divergence(scenario, frames, step, domains, refine, masks)
    masks = refstream.scenario_masks(scenario, frames + 400, masks)

    first = found["first"]
    if not first:
        return {
            "schema": 1, "format": "frame-census-v1", "scenario": scenario,
            "frames": frames, "step": step, "status": "PASS",
            "domains": list(domains), "bytes": 0, "regions": 0, "rows": [],
        }
    attribution: dict[int, dict[str, Any]] = {}
    if attribute:
        addresses = sorted({
            FIELD_BASE[field] + offset for field, offset in first if field in FIELD_BASE
        })
        attribution = {
            int(entry["address"], 16): entry
            for entry in refstream.writers(scenario, frames + 400, addresses,
                                           events=True, masks=masks)
        }
    grouped: dict[tuple[str, str, int], dict[str, Any]] = {}
    for (field, offset), (frame, got, want) in sorted(first.items(), key=lambda item: item[1][0]):
        symbol, base = refstream.resolve_region(field, offset)
        row = grouped.setdefault(
            (field, symbol, base),
            {
                "field": field, "symbol": symbol,
                "address": f"0x{FIELD_BASE.get(field, 0) + base:04X}",
                "first_divergent_ordinal": frame - 1,
                "bytes": 0, "samples": [],
            },
        )
        row["bytes"] += 1
        row["first_divergent_ordinal"] = min(row["first_divergent_ordinal"], frame - 1)
        if len(row["samples"]) < 4:
            sample = {
                "offset": offset,
                "address": f"0x{FIELD_BASE.get(field, 0) + offset:04X}",
                "ordinal": frame - 1, "native": got, "reference": want,
            }
            entry = attribution.get(FIELD_BASE.get(field, 0) + offset)
            if entry is not None:
                prior = refstream.writer_before(entry, frame - 1)
                sample["reference_writer"] = prior
            row["samples"].append(sample)
    rows = sorted(grouped.values(), key=lambda row: (row["first_divergent_ordinal"], -row["bytes"]))
    return {
        "schema": 1, "format": "frame-census-v1", "scenario": scenario,
        "frames": frames, "step": step, "status": "FAIL",
        "domains": list(domains), "bytes": len(first), "regions": len(rows), "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario")
    parser.add_argument("--frames", type=int, default=2000)
    parser.add_argument("--step", type=int, default=25)
    parser.add_argument("--domains", default=",".join(DEFAULT_DOMAINS))
    parser.add_argument("--no-refine", action="store_true")
    parser.add_argument("--no-attribute", action="store_true")
    parser.add_argument("--json")
    parser.add_argument("--masks", help="per-frame JOYP timeline replacing the "
                                        "scenario's own input, e.g. a TAS movie")
    args = parser.parse_args(argv)
    domains = tuple(part.strip() for part in args.domains.split(",") if part.strip())
    try:
        report = build_report(
            args.scenario, args.frames, args.step, domains,
            not args.no_refine, not args.no_attribute,
            refstream.load_masks(args.masks) if args.masks else None,
        )
    except (FrameCensusError, refstream.RefstreamError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json:
        Path(args.json).write_text(text + "\n")
    print(text)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
