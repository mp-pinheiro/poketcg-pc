#!/usr/bin/env python3
"""Bisect the first diverging frame between the native port and oracle-b.

Runs both lanes on the same input timeline for N frames each, compares the
final states with tests/scene_diff normalization, and binary-searches the
smallest N whose states diverge, then linear-scans fields/offsets. The oracle
lane costs one oracle-b process per probed frame count; the sweep is
O(log frames) probes of O(frame) work, which stays bounded for scene-length
frame counts.

Output: one JSON object with the first mismatch -- {"frame", "field",
"offset", "native", "reference"} -- plus the compared field list. Exit 0 when
a mismatch was found; exit 2 when the lanes agree over the whole range.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scenario import (
    SCENARIO_REQUIREMENTS,
    boot_input,
    reference_boot_frame_offset,
    reference_boot_input,
    run_native,
    shift_reference_input,
)
from tests.scene_diff import STATE_FIELDS, _first_difference, _state_field
from tools.oracle.gbrecomp_oracle import Oracle

# Fields the two lanes cannot agree on by construction today: oracle-b scene
# dumps never record apu_trace (it is always []) and add a "cycles" key to
# timer_frame_counters that the native dump does not emit. Pass --fields to
# compare them anyway once their producers line up.
STRUCTURALLY_INCOMPARABLE = ("apu_trace", "timer_frame_counters")
DEFAULT_FIELDS = tuple(
    field for field in STATE_FIELDS if field not in STRUCTURALLY_INCOMPARABLE
)

# Scenarios with a defined input timeline; every other scenario boots cold.
SCENARIO_INPUTS = {
    "boot-title": (boot_input, reference_boot_input),
    "boot-title-negative": (boot_input, reference_boot_input),
}


def first_field_mismatch(
    reference: dict[str, Any], native: dict[str, Any], fields: tuple[str, ...]
) -> dict[str, Any] | None:
    for field in fields:
        reference_bytes = _state_field(reference, field)
        native_bytes = _state_field(native, field)
        if reference_bytes is None or native_bytes is None:
            return {"field": field, "offset": None, "reason": "missing"}
        offset = _first_difference(reference_bytes, native_bytes)
        if offset is not None:
            return {
                "field": field,
                "offset": offset,
                "native": native_bytes[offset],
                "reference": reference_bytes[offset],
                "context": {
                    "native": native_bytes[max(0, offset - 8):offset + 8].hex(),
                    "reference": reference_bytes[max(0, offset - 8):offset + 8].hex(),
                },
            }
    return None


def bisect_first_mismatch(
    oracle: Oracle,
    max_frames: int,
    *,
    native_input: Path | None = None,
    oracle_input: str | None = None,
    fields: tuple[str, ...] = DEFAULT_FIELDS,
    frame_offset: int = 0,
) -> dict[str, Any] | None:
    """Smallest native frame N in [1, max_frames] whose end-of-run states
    diverge, with the first diverging field/offset at that frame; None when
    the lanes agree over the whole range. The reference runs frame_offset
    scanout frames ahead of every native frame (boot phase alignment) and its
    input timeline shifts by the same amount."""
    states: dict[int, tuple[dict[str, Any], dict[str, Any]]] = {}
    shifted_input = (
        shift_reference_input(oracle_input, frame_offset)
        if oracle_input and frame_offset
        else oracle_input
    )

    def run_pair(frames: int) -> tuple[dict[str, Any], dict[str, Any]]:
        if frames in states:
            return states[frames]
        with tempfile.TemporaryDirectory(prefix="poketcg-bisect-") as directory:
            state_path = Path(directory) / "state.json"
            trace_path = Path(directory) / "trace.json"
            returncode, stdout, stderr = run_native(
                frames, state_path, trace_path, native_input
            )
            if returncode != 0:
                raise RuntimeError(
                    f"native run failed at {frames} frames: "
                    f"{stderr.strip() or stdout.strip()}"
                )
            native_state = json.loads(state_path.read_text(encoding="utf-8"))
            # The plain oracle dump lacks oam/vram/io/palette and the sram
            # banks; the whole-state save is what fills those in.
            reference = oracle.run(
                input_file=shifted_input,
                frame_limit=frames + frame_offset,
                save_state=Path(directory) / "reference.gbs",
            )
        pair = (native_state, reference.state)
        states[frames] = pair
        return pair

    def diverges(frames: int) -> bool:
        native_state, reference_state = run_pair(frames)
        return first_field_mismatch(reference_state, native_state, fields) is not None

    if not diverges(max_frames):
        return None
    low, high = 1, max_frames
    while low < high:
        middle = (low + high) // 2
        if diverges(middle):
            high = middle
        else:
            low = middle + 1
    native_state, reference_state = run_pair(low)
    return {
        "frame": low,
        **(first_field_mismatch(reference_state, native_state, fields) or {}),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=sorted(SCENARIO_REQUIREMENTS))
    parser.add_argument(
        "--frames", type=int, default=2000,
        help="upper frame bound for the bisect (default 2000)",
    )
    parser.add_argument(
        "--fields", default=None,
        help="comma-separated state fields to compare "
             "(default: scene-comparable subset of scene_diff.STATE_FIELDS)",
    )
    args = parser.parse_args(argv)
    if args.frames < 1:
        parser.error("--frames must be positive")
    if args.fields:
        fields = tuple(field.strip() for field in args.fields.split(",") if field.strip())
    else:
        fields = DEFAULT_FIELDS
    builders = SCENARIO_INPUTS.get(args.scenario)
    native_input_values = builders[0](args.frames) if builders else None
    oracle_input = builders[1]() if builders else None
    finding: dict[str, Any] | None = None
    with Oracle(timeout=120.0) as oracle:
        frame_offset = reference_boot_frame_offset(oracle)
        if native_input_values is None:
            finding = bisect_first_mismatch(
                oracle,
                args.frames,
                oracle_input=oracle_input,
                fields=fields,
                frame_offset=frame_offset,
            )
        else:
            with tempfile.TemporaryDirectory(prefix="poketcg-bisect-input-") as directory:
                native_input = Path(directory) / "input.txt"
                native_input.write_text(
                    ",".join(str(value) for value in native_input_values) + "\n",
                    encoding="utf-8",
                )
                finding = bisect_first_mismatch(
                    oracle,
                    args.frames,
                    native_input=native_input,
                    oracle_input=oracle_input,
                    fields=fields,
                    frame_offset=frame_offset,
                )
    payload: dict[str, Any] = {
        "scenario": args.scenario,
        "max_frames": args.frames,
        "reference_frame_offset": frame_offset,
        "fields": list(fields),
        **(finding
           if finding
           else {"frame": None, "field": None, "offset": None,
                 "native": None, "reference": None, "status": "CLEAN"}),
    }
    if finding:
        payload["status"] = "FIRST_MISMATCH"
    print(json.dumps(payload, sort_keys=True, indent=2))
    return 0 if finding else 2


if __name__ == "__main__":
    raise SystemExit(main())
