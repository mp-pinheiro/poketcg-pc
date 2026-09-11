#!/usr/bin/env python3
"""The first call an interval runs differently, in order.

`--trace-calls` aggregates per-routine counts and cannot say which call came
first, so a divergence whose entry state matches on both lanes could not be
told apart from a frame-boundary shift. The native lane records an ordered
`(frame, callee)` log for a DoFrame window only (`--trace-window LO HI`), the
reference already lists its routine entries in order (`session.py routines`),
and this aligns the two and reports the first index where they part. Both
sequences are filtered to the routines the reference tracer can name: the port
defines helpers the ROM has no routine for, and those are structure, not
divergence.
"""

from __future__ import annotations

import argparse
import difflib
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import native_trace
import refstream
import session

INTERLEAVED = {
    "TimerHandler", "SerialTimerHandler", "SoundTimerHandler", "SerialHandler",
    "IncrementPlayTimeCounter", "VBlankHandler", "LCDCHandler", "Func_fc26c",
    "AssertSongFinished", "_AssertSongFinished", "AssertSFXFinished", "_AssertSFXFinished",
}
PLUMBING = ("BankswitchROM", "BankpushROM", "BankpopROM", "Bankswitch3dTo3f")

MAGIC = b"PTCGWND1"
HEADER = struct.Struct("<8sQQ")
RECORD = struct.Struct("<II")
TRACE_BINARY = ROOT / "build-trace" / "poketcg"


class WindowError(RuntimeError):
    pass


def load_window(path: Path) -> list[tuple[int, int]]:
    raw = path.read_bytes()
    if len(raw) < HEADER.size:
        raise WindowError(f"{path} is too short for a window trace")
    magic, _base, used = HEADER.unpack_from(raw)
    if magic != MAGIC:
        raise WindowError(f"{path} is not a window trace")
    rows = []
    for index in range(used):
        offset = HEADER.size + index * RECORD.size
        frame, callee = RECORD.unpack_from(raw, offset)
        rows.append((frame, callee))
    return rows


def native_symbols() -> set[str]:
    """The names the port's binary defines. A routine the port has no symbol for
    cannot appear in its stream at all -- the ROM's repeat wrappers (`Xx2`,
    `Xx4`) and its no-ops are inlined by the translator -- so those entries in
    the reference stream carry no order information and are dropped."""
    return {name for _address, name in native_trace.load_symbols(TRACE_BINARY)}


def native_order(name: str, lo: int, hi: int) -> dict[int, list[str]]:
    if not TRACE_BINARY.is_file():
        raise WindowError(f"no trace binary at {TRACE_BINARY.relative_to(ROOT)}: run `just build-trace`")
    masks, meta = session.load_session(name)
    frames = session.reference_frames(masks, meta)
    reference = session.build_reference(name, masks, frames, pokes=meta["pokes"], save=meta["save"])
    lag = ROOT / reference["directory"] / "lag.txt"
    directory = session.session_dir(name)
    symbols = native_trace.load_symbols(TRACE_BINARY)
    resolve = native_trace.resolver(symbols)
    base_symbol = next((address for address, name in symbols if name == "trace_set_frame"), None)
    if base_symbol is None:
        raise WindowError(f"{TRACE_BINARY} has no trace_set_frame symbol")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = tmp / "window.bin"
        command = [
            str(TRACE_BINARY), "--headless",
            "--data-pack", str(ROOT / "build" / "completion" / "data-pack.bin"),
            "--frames", "0",
            "--stop-ordinal", str(hi + 2),
            "--input-ordinal", str(directory / "input.txt"),
            "--lag-track", str(lag),
            "--dump-state", str(tmp / "state.json"),
            "--trace-window", str(lo), str(hi),
            "--trace-window-out", str(out),
        ]
        pokes = directory / "pokes.txt"
        if pokes.is_file():
            command += ["--poke-ordinal", str(pokes)]
        save = directory / session.SAVE_FILE
        if save.is_file():
            wrapped = tmp / "save.pksr"
            wrapped.write_bytes(session.native_save_file(save.read_bytes()))
            command += ["--load-save", str(wrapped)]
        overreads = lag.with_name("overreads.txt")
        if overreads.is_file():
            command += ["--overread-track", str(overreads)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise WindowError(f"native run failed: {result.stderr.strip()[-300:]}")
        rows = load_window(out)
    by_frame: dict[int, list[str]] = {}
    for frame, callee in rows:
        by_frame.setdefault(frame, []).append(resolve(base_symbol + callee))
    return by_frame


def reference_order(name: str, ordinal: int) -> list[str]:
    result = subprocess.run(
        ["python3", str(Path(__file__).resolve().parent / "session.py"), "routines",
         name, str(ordinal), "--all"],
        cwd=ROOT, capture_output=True, text=True, check=True)
    rows = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit():
            rows.append(parts[1])
    return rows


def game_only(names: list[str], files: dict[str, str]) -> list[str]:
    """The order the game code ran in: the ROM interleaves its ISR bodies between
    instructions the port runs in one block, so the driver and the interrupt
    entries carry no order information and are dropped from both lanes."""
    out = []
    for name in names:
        if name in INTERLEAVED or name.startswith(PLUMBING):
            continue
        if files.get(name, "").startswith("src/audio/"):
            continue
        out.append(name)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("ordinal", type=int)
    parser.add_argument("--limit", type=int, default=6)
    parser.add_argument("--min-block", type=int, default=3,
                        help="smallest block difference that is not structural noise")
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args(argv)

    known = set(refstream.routine_entry_addresses()[1].values())
    inventory = json.loads((ROOT / "site" / "data" / "inventory.json").read_text())["functions"]
    files = {name: info.get("file", "") for name, info in inventory.items()}
    defined = native_symbols()
    known &= defined
    reference = game_only([n for n in reference_order(args.name, args.ordinal) if n in known], files)
    try:
        by_frame = native_order(args.name, args.ordinal - 1, args.ordinal + 1)
    except (WindowError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2

    ordered = [name for _frame, names in sorted(by_frame.items()) for name in names]
    native = game_only([n for n in ordered if n in known], files)
    if not native:
        print(json.dumps({"status": "FAIL", "detail": "the window recorded no calls"}), file=sys.stderr)
        return 2

    def collapse(names: list[str]) -> list[str]:
        out: list[str] = []
        for name in names:
            if not out or out[-1] != name:
                out.append(name)
        return out

    anchor = reference.index("DoFrame") if "DoFrame" in reference else 0
    candidates = [n - anchor for n, name in enumerate(native) if name == "DoFrame"]
    candidates = [c for c in candidates if c >= 0] or [0]

    def score(start: int) -> float:
        slice_ = native[start:start + len(reference)]
        return difflib.SequenceMatcher(None, reference, slice_, autojunk=False).ratio()

    start = max(candidates, key=score)
    native = native[start:start + len(reference)]
    shared = set(reference) & set(native)
    reference = collapse([n for n in reference if n in shared])
    native = collapse([n for n in native if n in shared])
    matcher = difflib.SequenceMatcher(None, reference, native, autojunk=False)
    blocks = [op for op in matcher.get_opcodes() if op[0] != "equal"]
    significant = [op for op in blocks
                   if max(op[2] - op[1], op[4] - op[3]) >= args.min_block
                   and op[2] < len(reference) and op[4] < len(native)]
    equal = sum(op[2] - op[1] for op in matcher.get_opcodes() if op[0] == "equal")
    print(f"WINDOW {args.name} ordinal={args.ordinal} anchored_at={start} reference={len(reference)} "
          f"native={len(native)} equal={equal} blocks={len(blocks)} "
          f"significant={len(significant)}")
    for tag, i1, i2, j1, j2 in significant[:args.limit]:
        print(f"  {tag:8s} reference[{i1}:{i2}] native[{j1}:{j2}]")
        for name in reference[i1:i2][:6]:
            print(f"      reference only: {name}")
        for name in native[j1:j2][:6]:
            print(f"      native only:    {name}")
    if args.json:
        args.json.write_text(json.dumps({"schema": 1, "name": args.name, "ordinal": args.ordinal,
                                         "blocks": [list(op) for op in significant],
                                         "reference": reference, "native": native},
                                        indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
