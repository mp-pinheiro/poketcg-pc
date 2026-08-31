"""Replay a scene and compare every declared native/reference state field."""

from __future__ import annotations

import argparse
import struct
import json
import subprocess
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.oracle.gbrecomp_oracle import Oracle, OracleError, Result

STATE_FIELDS = (
    "wram", "hram", "sram_bank_0", "sram_bank_1", "sram_bank_2",
    "sram_bank_3", "vram_bank_0", "vram_bank_1", "oam", "io", "palette_ram",
    "mapper_state", "input_latch", "timer_frame_counters", "rng", "apu_state",
    "apu_trace", "framebuffer", "save", "transport", "printer", "scratch",
)


def _canonical(state: dict) -> bytes:
    return json.dumps(state, sort_keys=True, separators=(",", ":")).encode()


ALIASES = {
    "wram": ("wram", "wram_bank_0_c000_cfff", "wram_bank_1_d000_dfff"),
    "hram": ("hram", "hram_ff80_fffe"),
    "palette_ram": ("palette_ram", "pal", "palette"),
}


def _value_bytes(value: object, *, framebuffer: bool = False) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        try:
            return bytes.fromhex(value)
        except ValueError:
            return value.encode()
    if isinstance(value, list):
        if framebuffer and value and isinstance(value[0], (list, tuple)):
            pixels = bytearray()
            for pixel in value:
                if len(pixel) != 3:
                    raise ValueError("framebuffer pixel is not RGB")
                channels = [min(31, (int(channel) * 31 + 127) // 255) for channel in pixel]
                pixels.extend(struct.pack("<H", channels[0] | channels[1] << 5 | channels[2] << 10))
            return bytes(pixels)
        if value and isinstance(value[0], list):
            return b"".join(_value_bytes(part) for part in value)
        if all(isinstance(item, int) and 0 <= item <= 255 for item in value):
            return bytes(value)
        if all(isinstance(item, int) and 0 <= item <= 0xFFFF for item in value):
            return b"".join(struct.pack("<H", item) for item in value)
    if isinstance(value, int):
        return struct.pack("<Q", value)
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def _state_field(state: dict, name: str) -> bytes | None:
    keys = (name,) if name in state else ALIASES.get(name, (name,))
    values = [state[key] for key in keys if key in state]
    if not values:
        return None
    return b"".join(
        _value_bytes(value, framebuffer=name == "framebuffer") for value in values
    )


def _first_difference(left: bytes, right: bytes) -> int | None:
    for offset, (mine, theirs) in enumerate(zip(left, right)):
        if mine != theirs:
            return offset
    return min(len(left), len(right)) if len(left) != len(right) else None


def compare(result: Result, c_state: dict | None, *, perturb: str | None = None) -> int:
    if c_state is None:
        print("no native state supplied: nothing compared", file=sys.stderr)
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
    oracle_state = result.state
    for name in STATE_FIELDS:
        mine = _state_field(oracle_state, name)
        theirs = _state_field(c_state, name)
        if mine is None:
            print(f"unsupported: oracle does not expose {name}", file=sys.stderr)
            failures += 1
            continue
        if theirs is None:
            print(f"missing: native state does not supply {name}", file=sys.stderr)
            failures += 1
            continue
        offset = _first_difference(mine, theirs)
        if offset is None:
            print(f"match: {name} ({len(mine)} bytes)")
            continue
        oracle_value = mine[offset] if offset < len(mine) else None
        native_value = theirs[offset] if offset < len(theirs) else None
        print(
            f"STATE_MISMATCH region={name} offset=0x{offset:04X} "
            f"oracle={oracle_value} native={native_value}"
        )
        failures += 1
    return failures

def run_native(binary: Path, pack: Path, frames: int, state_path: Path) -> dict:
    try:
        completed = subprocess.run(
            [
                str(binary), "--headless", "--data-pack", str(pack),
                "--frames", str(frames), "--dump-state", str(state_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise OracleError("native scene timed out") from exc
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise OracleError(f"native scene failed ({completed.returncode}): {detail}")
    try:
        state = json.loads(state_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise OracleError(f"native scene state is invalid: {exc}") from exc
    if not isinstance(state, dict):
        raise OracleError("native scene state is not an object")
    return state



def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", dest="input_file")
    parser.add_argument("--frames", type=int, default=30)
    parser.add_argument("--c-state", type=Path)
    parser.add_argument("--native", type=Path, help="packaged native executable")
    parser.add_argument(
        "--native-pack", type=Path, default=Path("build/completion/data-pack.bin")
    )
    parser.add_argument("--oracle", type=Path)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument(
        "--perturb", help="perturb a native region for failure testing, REGION:OFFSET"
    )
    parser.add_argument(
        "--replay-only", action="store_true",
        help="check replay determinism only; do not claim a state comparison",
    )
    args = parser.parse_args()
    try:
        with Oracle(args.oracle, timeout=args.timeout) as oracle:
            first = oracle.run(input_file=args.input_file, frame_limit=args.frames)
            second = oracle.run(input_file=args.input_file, frame_limit=args.frames)
        if _canonical(first.state) != _canonical(second.state):
            print("replay mismatch: repeated reference states differ", file=sys.stderr)
            return 1
        print(f"replay: identical ({first.completed_frames} completed frames)")
        native_state = None
        if args.native:
            with tempfile.TemporaryDirectory(prefix="poketcg-native-") as directory:
                first_path = Path(directory) / "first.json"
                second_path = Path(directory) / "second.json"
                native_state = run_native(
                    args.native, args.native_pack, args.frames, first_path
                )
                second_native = run_native(
                    args.native, args.native_pack, args.frames, second_path
                )
            if _canonical(native_state) != _canonical(second_native):
                print("replay mismatch: repeated native states differ", file=sys.stderr)
                return 1
        if args.replay_only and not args.c_state and native_state is None:
            return 0
        c_state = (
            json.loads(args.c_state.read_text()) if args.c_state
            else native_state
        )
        return 1 if compare(first, c_state, perturb=args.perturb) else 0
    except (OSError, ValueError, OracleError) as exc:
        print(f"scene_diff: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
