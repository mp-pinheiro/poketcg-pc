"""Replay one gb-recompiled scene and compare its meaningful state regions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.oracle.gbrecomp_oracle import Oracle, OracleError, Result

SNAPSHOT_REGIONS = ("wram", "hram", "sram", "vram", "oam", "io", "pal", "scratch")
COMPARABLE = {
    "wram": (0xC000, 0x2000),
    "hram": (0xFF80, 0x7F),
}


def _canonical(state: dict) -> bytes:
    return json.dumps(state, sort_keys=True, separators=(",", ":")).encode()


def _c_region(state: dict, name: str) -> bytes | None:
    aliases = {
        "wram": ("wram", "wram_bank_0_c000_cfff", "wram_bank_1_d000_dfff"),
        "hram": ("hram", "hram_ff80_fffe"),
    }
    keys = aliases.get(name, (name,))
    values = [state[key] for key in keys if key in state]
    if not values:
        return None
    if len(values) > 1 and name == "wram":
        value = values
    else:
        value = values[0]
    if isinstance(value, list) and value and isinstance(value[0], list):
        return b"".join(bytes(part) for part in value)
    if isinstance(value, list):
        return bytes(value)
    if isinstance(value, str):
        return bytes.fromhex(value)
    raise ValueError(f"C state region {name!r} is neither a byte list nor hex")


def _oracle_region(result: Result, name: str) -> bytes:
    addr, size = COMPARABLE[name]
    return result.mem(addr, size)


def _first_difference(left: bytes, right: bytes) -> int | None:
    for offset, (mine, theirs) in enumerate(zip(left, right)):
        if mine != theirs:
            return offset
    return min(len(left), len(right)) if len(left) != len(right) else None


def compare(result: Result, c_state: dict | None, *, perturb: str | None = None) -> int:
    if c_state is None:
        # Comparing nothing is not a pass. The replay-determinism half of #13's
        # acceptance is checked by the caller and stands on its own; this half has
        # simply not run, and reporting success for it would be a false green.
        print("no C state supplied: nothing compared", file=sys.stderr)
        print("pass --c-state <snapshot.json> to run the comparison", file=sys.stderr)
        return 1
    failures = 0
    if perturb:
        region, raw_offset = perturb.split(":", 1)
        offset = int(raw_offset, 0)
        data = c_state.get(region)
        if isinstance(data, str):
            data = list(bytes.fromhex(data))
            c_state[region] = data
        if not isinstance(data, list) or not 0 <= offset < len(data):
            raise ValueError(f"cannot perturb {region}:{offset}")
        data[offset] ^= 1
    for name in SNAPSHOT_REGIONS:
        if name not in COMPARABLE:
            print(f"not meaningful: {name}")
            continue
        theirs = _c_region(c_state, name)
        if theirs is None:
            # A comparable region the C state does not supply is a gap in the input,
            # not a match. Falling through here previously reached
            # _first_difference(mine, None) and raised TypeError.
            print(f"missing: {name} absent from the C state vector")
            failures += 1
            continue
        mine = _oracle_region(result, name)
        if len(theirs) > len(mine):
            theirs = theirs[:len(mine)]
        offset = _first_difference(mine, theirs)
        if name == "hram" and offset is None:
            print("not meaningful: hram offset 0x007F ($FFFF) absent from Oracle B")
        if offset is None:
            print(f"match: {name} ({len(mine)} bytes)")
        else:
            got = mine[offset] if offset < len(mine) else None
            expected = theirs[offset] if offset < len(theirs) else None
            print(f"mismatch: {name} offset 0x{offset:04X} oracle={got} c={expected}")
            failures += 1
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", dest="input_file")
    parser.add_argument("--frames", type=int, default=30)
    parser.add_argument("--c-state", type=Path)
    parser.add_argument("--oracle", type=Path)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--perturb", help="perturb a C region for failure testing, REGION:OFFSET")
    parser.add_argument("--replay-only", action="store_true",
                        help="check replay determinism only; do not claim a C comparison")
    args = parser.parse_args()
    try:
        with Oracle(args.oracle, timeout=args.timeout) as oracle:
            first = oracle.run(input_file=args.input_file, frame_limit=args.frames)
            second = oracle.run(input_file=args.input_file, frame_limit=args.frames)
        if _canonical(first.state) != _canonical(second.state):
            print("replay mismatch: repeated scene states differ", file=sys.stderr)
            return 1
        print(f"replay: identical ({first.completed_frames} completed frames)")
        if args.replay_only and not args.c_state:
            return 0
        c_state = json.loads(args.c_state.read_text()) if args.c_state else None
        return 1 if compare(first, c_state, perturb=args.perturb) else 0
    except (OSError, ValueError, OracleError) as exc:
        print(f"scene_diff: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
