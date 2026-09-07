#!/usr/bin/env python3
"""Verify a session against the ROM, one DoFrame at a time.

A session is one byte of input per DoFrame, in InputFrame order (src/input.h).
It comes from one of two places:

  derive   the reference plays a frame-indexed movie (the TAS) and the byte its
           own ReadJoypad saw at every DoFrame is logged. No human, and the
           session reaches wherever the ROM reaches on that movie.
  play     `just play --record-input` logs what a human played.

Verification is the same either way. The reference replays the session on the
DoFrame axis once and caches a CRC-32 per ordinal of the masked game state
(WRAM, HRAM, OAM, VRAM); the port writes the same digest stream through
--digest-out; the first ordinal whose digests differ is exact, found in one
native run. Only then does a targeted reference capture at that ordinal name
the bytes, their RAM symbols and the routine that last wrote them.

Ordinals are 1-based on both sides: native, frame_boundary_doframe_ordinal
after the increment; reference, the count of $0552 anchor hits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import zlib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import scenario as scenario_module

SESSIONS = ROOT / "tests" / "sessions"
CACHE = ROOT / "build" / "completion" / "sessions"
RATCHET_PATH = ROOT / "tools" / "completion" / "session_ratchet.json"
NATIVE_TIMEOUT = 1800
DIGEST_FORMAT = "session-digest-v1"
# wram, hram, oam, vram; then the reference's PPU frame and wVBlankCounter.
REFERENCE_RECORD = struct.Struct("<4IIB")
NATIVE_RECORD = struct.Struct("<4I")
REGIONS = ("wram", "hram", "oam", "vram")
REGION_LENGTHS = {"wram": 0x2000, "hram": 0x80, "oam": 0xA0, "vram": 0x4000}
REGION_BASES = {"wram": 0xC000, "hram": 0xFF80, "oam": 0xFE00, "vram": 0x8000}

# Timer-phase state on top of the scenario ledger. The whole sound driver runs
# from the timer interrupt (time.asm:9-26: SoundTimerHandler on every fourth
# TimerHandler, ~60.24 Hz), asynchronous to DoFrame, so at a DoFrame anchor
# its command pointers and counters are one tick apart between lanes on a
# schedule no asm instruction decides -- the same reason the ledger already
# excludes wTimerCounter. The span is exactly SECTION "WRAM Audio"
# (wram.asm:2992-3289, $DD80 up to the stack at $DEE5). Audio correctness is
# the audio-catalog scenario's, compared as an APU write sequence.
# wPlayTimeCounter ($CAC5-$CAC9) is the same ISR's other product
# (time.asm:15-16): during a map load the ROM's timer keeps firing for the
# frames the CPU is busy, ticks the port's batched timer cannot see, and
# nothing but the diary reads the result. wPlayTimeCounterEnable ($CAC4)
# stays compared: the game sets it, so it must match.
TIMING_PHASE = {"wram": [(0xCAC5 - 0xC000, 0xCACA - 0xC000),
                         (0xDD80 - 0xC000, 0xDEE5 - 0xC000)]}
# Ledger entries whose justification is the frame axis. hDPadRepeat ($FF8D)
# is excluded there because the reference's mid-processing VBlank services
# shift its decay schedule against the native frame count; on the DoFrame
# axis HandleDPadRepeat runs once per anchor on both lanes, so the counter is
# exactly comparable, and hiding it only defers the divergence to hDPadHeld.
COMPARE_DESPITE_LEDGER = {"hram": [(0x0D, 0x0E)]}


class SessionError(RuntimeError):
    pass


def session_dir(name: str) -> Path:
    return SESSIONS / name


def load_session(name: str) -> tuple[list[int], dict[str, Any]]:
    directory = session_dir(name)
    input_path = directory / "input.txt"
    meta_path = directory / "session.json"
    if not input_path.is_file():
        raise SessionError(f"no session input at {input_path.relative_to(ROOT)}")
    masks = refstream.load_masks(input_path)
    meta = json.loads(meta_path.read_text()) if meta_path.is_file() else {}
    return masks, meta


def reference_frames(masks: list[int], meta: dict[str, Any]) -> int:
    """PPU frames to give the reference. A derived session knows its movie's
    length; a recording gets twice its DoFrames, DoFrames being the sparser
    axis (refstream.py: 78,207 movie frames hold 55,080 DoFrames)."""
    return int(meta.get("reference_frames") or len(masks) * 2 + 400)


def read_ratchet() -> dict[str, dict[str, int]]:
    if not RATCHET_PATH.is_file():
        return {}
    return json.loads(RATCHET_PATH.read_text())


def write_ratchet(ratchet: dict[str, dict[str, int]]) -> None:
    RATCHET_PATH.write_text(json.dumps(ratchet, indent=2, sort_keys=True) + "\n")


def mask_ranges() -> dict[str, list[tuple[int, int]]]:
    ranges: dict[str, list[tuple[int, int]]] = {region: [] for region in REGIONS}
    for region in ("wram", "hram", "oam"):
        ranges[region] += [tuple(r) for r in scenario_module.COMPARATOR_EXCLUDED_RANGES.get(region, ())]
    for region, extra in TIMING_PHASE.items():
        ranges[region] += extra
    for region, keep in COMPARE_DESPITE_LEDGER.items():
        table = bytearray(REGION_LENGTHS[region])
        for start, end in ranges[region]:
            for index in range(max(0, start), min(len(table), end)):
                table[index] = 1
        for start, end in keep:
            for index in range(max(0, start), min(len(table), end)):
                table[index] = 0
        ranges[region] = runs(table)
    return ranges


def runs(table: bytearray) -> list[tuple[int, int]]:
    out = []
    start = None
    for index, flag in enumerate(table):
        if flag and start is None:
            start = index
        elif not flag and start is not None:
            out.append((start, index))
            start = None
    if start is not None:
        out.append((start, len(table)))
    return out


def mask_text() -> str:
    lines = ["# masked before digesting, on both lanes; regenerated by session.py"]
    for region, spans in mask_ranges().items():
        for start, end in spans:
            lines.append(f"{region} 0x{start:04X} 0x{end:04X}")
    return "\n".join(lines) + "\n"


def mask_tables() -> dict[str, bytes]:
    tables = {}
    for region, spans in mask_ranges().items():
        table = bytearray(REGION_LENGTHS[region])
        for start, end in spans:
            for index in range(max(0, start), min(len(table), end)):
                table[index] = 1
        tables[region] = bytes(table)
    return tables


def masked(data: bytes, table: bytes) -> bytes:
    if not any(table):
        return data
    out = bytearray(data)
    for index, flag in enumerate(table):
        if flag:
            out[index] = 0
    return bytes(out)


def reference_regions(core: refstream.Core) -> dict[str, bytes]:
    return {
        "wram": core.area("WRAM")[:0x2000],
        "hram": core.hram_block(),
        "oam": core.area("OAM")[:0xA0],
        "vram": core.area("VRAM")[:0x4000],
    }


def native_regions(dump: dict[str, Any]) -> dict[str, bytes]:
    return {
        "wram": bytes(dump["wram"]),
        "hram": bytes(dump["hram"]),
        "oam": bytes(dump["oam"]),
        "vram": bytes(dump["vram_bank_0"]) + bytes(dump["vram_bank_1"]),
    }


def digest(regions: dict[str, bytes], tables: dict[str, bytes]) -> tuple[int, int, int, int]:
    return tuple(zlib.crc32(masked(regions[r], tables[r])) & 0xFFFFFFFF for r in REGIONS)


def stream_key(masks: list[int], frames: int, axis: str) -> str:
    import gambatte_runner

    pins = gambatte_runner.load_pins()
    h = hashlib.sha256()
    h.update(DIGEST_FORMAT.encode())
    h.update(axis.encode())
    h.update(struct.pack("<I", frames))
    h.update(bytes(m & 0xFF for m in masks))
    h.update(mask_text().encode())
    h.update(pins["rom"]["sha256"].encode())
    h.update(pins["core"]["sha256"].encode())
    return h.hexdigest()[:24]


def build_reference(name: str, masks: list[int], frames: int, *, axis: str = "ordinal",
                    record_input: bool = False) -> dict[str, Any]:
    """One reference replay: a digest record per DoFrame anchor, cached by
    input. With `record_input` the byte ReadJoypad saw at each anchor is
    returned as well, in InputFrame order, which is how a movie becomes a
    session."""
    key = stream_key(masks, frames, axis)
    directory = CACHE / name / key
    meta_path = directory / "meta.json"
    if meta_path.is_file() and not record_input:
        meta = json.loads(meta_path.read_text())
        meta["cached"] = True
        return meta
    tables = mask_tables()
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    records = bytearray()
    inputs = bytearray()
    with refstream.Core(padded) as core:
        core.input_axis = axis
        read = core.library.gambatte_cpuread
        hits = 0

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal hits
            if address != refstream.DOFRAME_ANCHOR:
                return
            hits += 1
            regions = reference_regions(core)
            crcs = digest(regions, tables)
            records.extend(REFERENCE_RECORD.pack(*crcs, core.frame, regions["wram"][0xAB8]))
            if record_input:
                held = read(core.core, 0xFF90)
                inputs.append(((held << 4) | (held >> 4)) & 0xFF)

        core.install_exec(on_exec)
        core.run(frames)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "digests.bin").write_bytes(bytes(records))
    meta = {
        "schema": 1, "format": DIGEST_FORMAT, "name": name, "axis": axis, "key": key,
        "frames": frames, "anchors": hits, "record": REFERENCE_RECORD.size,
        "directory": str(directory.relative_to(ROOT)), "cached": False,
    }
    if record_input:
        meta["inputs"] = list(inputs)
    meta_path.write_text(json.dumps({k: v for k, v in meta.items() if k != "inputs"},
                                    sort_keys=True) + "\n")
    return meta


def load_reference(meta: dict[str, Any]) -> bytes:
    return (ROOT / meta["directory"] / "digests.bin").read_bytes()


def run_native(directory: Path, input_path: Path, n: int, *, digest_out: Path | None = None,
               mask_path: Path | None = None, dump_ordinals: list[int] | None = None) -> tuple[Path, str]:
    state_path = directory / "state.json"
    command = [
        str(scenario_module.BINARY), "--headless",
        "--data-pack", str(scenario_module.PACK),
        "--frames", "0",
        "--stop-ordinal", str(n),
        "--input-ordinal", str(input_path),
        "--dump-state", str(state_path),
    ]
    if digest_out:
        command += ["--digest-out", str(digest_out)]
        if mask_path:
            command += ["--digest-mask", str(mask_path)]
    if dump_ordinals:
        command += ["--dump-state-ordinals", ",".join(str(v) for v in dump_ordinals)]
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                timeout=NATIVE_TIMEOUT, check=False)
    except subprocess.TimeoutExpired as exc:
        text = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else str(exc.stderr or "")
        return state_path, f"HANG no exit within {NATIVE_TIMEOUT}s\n{text}"
    if result.returncode != 0:
        return state_path, result.stderr.strip()[-2000:] or f"exit {result.returncode}"
    return state_path, ""


def first_divergence(reference: bytes, native: bytes) -> tuple[int | None, int, list[str]]:
    """(first divergent ordinal, native ordinals, regions that differ there)."""
    ref_count = len(reference) // REFERENCE_RECORD.size
    nat_count = len(native) // NATIVE_RECORD.size
    for index in range(min(ref_count, nat_count)):
        ref = REFERENCE_RECORD.unpack_from(reference, index * REFERENCE_RECORD.size)
        nat = NATIVE_RECORD.unpack_from(native, index * NATIVE_RECORD.size)
        if ref[:4] != nat:
            return index + 1, nat_count, [REGIONS[i] for i in range(4) if ref[i] != nat[i]]
    return None, nat_count, []


def reference_capture(name: str, masks: list[int], frames: int, ordinal: int) -> dict[str, bytes]:
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    captured: dict[str, bytes] = {}
    with refstream.Core(padded) as core:
        core.input_axis = "ordinal"
        hits = 0

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal hits
            if address != refstream.DOFRAME_ANCHOR:
                return
            hits += 1
            if hits == ordinal:
                captured.update(reference_regions(core))

        core.install_exec(on_exec)
        core.run(frames, stop=lambda: hits >= ordinal)
    if not captured:
        raise SessionError(f"reference never reached ordinal {ordinal}")
    return captured


def lag_between(reference: bytes, ordinal: int) -> dict[str, int]:
    """Reference PPU frames and VBlanks between anchors ordinal-1 and ordinal.
    More than one PPU frame is a lag frame the port has to model as a service
    pass (frame_boundary_consume_services) at whatever the game was doing."""
    this = REFERENCE_RECORD.unpack_from(reference, (ordinal - 1) * REFERENCE_RECORD.size)
    if ordinal < 2:
        return {"frames": this[4], "vblanks": this[5]}
    prev = REFERENCE_RECORD.unpack_from(reference, (ordinal - 2) * REFERENCE_RECORD.size)
    return {"frames": this[4] - prev[4], "vblanks": (this[5] - prev[5]) & 0xFF}


def region_field(region: str, offset: int) -> tuple[str, int]:
    if region == "vram":
        return ("vram_bank_1", offset - 0x2000) if offset >= 0x2000 else ("vram_bank_0", offset)
    return region, offset


def attribute(name: str, masks: list[int], frames: int, ordinal: int,
              native: dict[str, bytes], reference: dict[str, bytes]) -> list[dict[str, Any]]:
    tables = mask_tables()
    picked: list[tuple[str, int, int, int, str]] = []
    seen: set[str] = set()
    for region in REGIONS:
        table = tables[region]
        nat, ref = native[region], reference[region]
        for offset in range(min(len(nat), len(ref))):
            if table[offset] or nat[offset] == ref[offset]:
                continue
            field, field_offset = region_field(region, offset)
            symbol, _base = refstream.resolve_region(field, field_offset)
            if symbol in seen:
                continue
            seen.add(symbol)
            picked.append((field, field_offset, nat[offset], ref[offset], symbol))
    picked = picked[:16]
    addresses = sorted({refstream.FIELD_WINDOWS[f][0] + o for f, o, _n, _r, _s in picked})
    writers = {
        int(entry["address"], 16): entry
        for entry in refstream.writers(f"session:{name}", frames, addresses, events=True,
                                       masks=masks, axis="ordinal", ordinals=ordinal)
    } if addresses else {}
    out = []
    for field, offset, got, want, symbol in picked:
        address = refstream.FIELD_WINDOWS[field][0] + offset
        entry = writers.get(address)
        # A write during DoFrame K carries core.ordinal K-1 (the anchor for K
        # has not fired yet), so "before ordinal K" is exactly the set whose
        # last element produced the value the reference holds at anchor K.
        prior = refstream.writer_before(entry, ordinal) if entry else None
        out.append({
            "field": field, "offset": offset, "address": f"0x{address:04X}",
            "symbol": symbol, "native": got, "reference": want,
            "writer": prior["routine"] if prior else "",
            "writer_label": prior["label"] if prior else "",
        })
    return out


def verify(name: str, *, write: bool, json_path: Path | None) -> int:
    masks, meta = load_session(name)
    n = len(masks)
    frames = reference_frames(masks, meta)
    report: dict[str, Any] = {"schema": 2, "format": "session-verify-v2", "name": name,
                              "ordinals": n, "goal": meta.get("goal", "")}
    ref_meta = build_reference(name, masks, frames)
    reference = load_reference(ref_meta)
    ref_count = len(reference) // REFERENCE_RECORD.size
    if ref_count < n:
        report.update(status="ref-short", confirmed=0, reference_ordinals=ref_count)
        print(f"SESSION {name} status=ref-short confirmed=0 ordinals={n} reference={ref_count}")
        emit(report, json_path)
        return 4
    with tempfile.TemporaryDirectory(prefix=f"session-{name}-") as tmp:
        directory = Path(tmp)
        mask_path = directory / "mask.txt"
        mask_path.write_text(mask_text())
        digest_path = directory / "native.bin"
        _state, failure = run_native(directory, session_dir(name) / "input.txt", n,
                                     digest_out=digest_path, mask_path=mask_path)
        native = digest_path.read_bytes() if digest_path.is_file() else b""
        ordinal, reached, regions = first_divergence(reference, native)
        if ordinal is None and reached < n:
            status, confirmed = "native-short", reached
        elif ordinal is None:
            status, confirmed = "clean", n
        else:
            status, confirmed = "diverged", ordinal - 1
        report.update(status=status, confirmed=confirmed, reached=reached, native_failure=failure,
                      reference=ref_meta["directory"])
        print(f"SESSION {name} status={status} confirmed={confirmed} ordinals={n}")
        if status == "diverged":
            lag = lag_between(reference, ordinal)
            report["divergence"] = {"ordinal": ordinal, "regions": regions, "lag": lag}
            print(f"WINDOW ordinal={ordinal} regions={','.join(regions)} "
                  f"reference_frames={lag['frames']} reference_vblanks={lag['vblanks']}"
                  + ("  LAG: the reference ran extra VBlanks here; model them with "
                     "frame_boundary_consume_services" if lag["frames"] > 1 else ""))
            capture_dir = directory / "capture"
            capture_dir.mkdir()
            state_path, cap_failure = run_native(capture_dir, session_dir(name) / "input.txt",
                                                 ordinal, dump_ordinals=[ordinal])
            dump_path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
            if not dump_path.is_file():
                raise SessionError(f"no native dump at ordinal {ordinal}: {cap_failure[-300:]}")
            native_state = native_regions(json.loads(dump_path.read_text()))
            reference_state = reference_capture(name, masks, frames, ordinal)
            details = attribute(name, masks, frames, ordinal, native_state, reference_state)
            report["divergence"]["rows"] = details
            for row in details[:8]:
                print(f"DIVERGE ordinal={ordinal} field={row['field']} address={row['address']} "
                      f"symbol={row['symbol']} native={row['native']} reference={row['reference']} "
                      f"writer={row['writer']}")
        if status == "native-short" and failure:
            for line in failure.strip().splitlines()[-3:]:
                print(f"NATIVE {line}")
    ratchet = read_ratchet()
    previous = ratchet.get(name, {}).get("confirmed_ordinal")
    exit_code = {"clean": 0, "diverged": 1, "native-short": 1}[status]
    if previous is not None and confirmed < previous and not write:
        print(f"REGRESSION {name} key=confirmed_ordinal was={previous} now={confirmed}")
        report["regression"] = {"was": previous, "now": confirmed}
        exit_code = 3
    elif previous is None or confirmed > previous or write:
        ratchet[name] = {"confirmed_ordinal": confirmed}
        write_ratchet(ratchet)
    emit(report, json_path)
    return exit_code


def derive(name: str, movie: Path, goal: str) -> int:
    """The reference plays a frame-indexed movie; the byte each DoFrame read
    becomes the session. Then the session is replayed on the DoFrame axis and
    its digests must equal the movie run's: the ROM reads JOYP only inside
    ReadJoypad, so both axes are one execution."""
    movie_masks = refstream.load_masks(movie)
    frames = len(movie_masks) + 400
    movie_run = build_reference(f"{name}-movie", movie_masks, frames, axis="frame", record_input=True)
    inputs = movie_run["inputs"]
    directory = session_dir(name)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "input.txt").write_text("\n".join(str(b) for b in inputs) + "\n")
    meta = {
        "schema": 1, "name": name, "goal": goal, "ordinals": len(inputs),
        "derived_from": str(movie.relative_to(ROOT) if movie.is_absolute() else movie),
        "movie_frames": len(movie_masks), "reference_frames": frames,
        "recorded": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    session_run = build_reference(name, inputs, frames, axis="ordinal")
    movie_digests = load_reference(movie_run)
    session_digests = load_reference(session_run)
    mismatch = None
    for index in range(min(len(movie_digests), len(session_digests)) // REFERENCE_RECORD.size):
        a = REFERENCE_RECORD.unpack_from(movie_digests, index * REFERENCE_RECORD.size)[:4]
        b = REFERENCE_RECORD.unpack_from(session_digests, index * REFERENCE_RECORD.size)[:4]
        if a != b:
            mismatch = index + 1
            break
    meta["axis_match"] = mismatch is None and session_run["anchors"] == movie_run["anchors"]
    meta["axis_mismatch_ordinal"] = mismatch
    (directory / "session.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(f"DERIVED {name} ordinals={len(inputs)} movie_frames={len(movie_masks)} "
          f"axis_match={meta['axis_match']}"
          + (f" mismatch_ordinal={mismatch}" if mismatch else ""))
    return 0 if meta["axis_match"] else 1


def emit(report: dict[str, Any], json_path: Path | None) -> None:
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def session_names() -> list[str]:
    if not SESSIONS.is_dir():
        return []
    return sorted(p.name for p in SESSIONS.iterdir() if (p / "input.txt").is_file())


def lowest_confirmed() -> str:
    names = session_names()
    if not names:
        raise SessionError("no sessions under tests/sessions")
    ratchet = read_ratchet()
    return min(names, key=lambda name: (ratchet.get(name, {}).get("confirmed_ordinal", -1), name))


def status() -> int:
    ratchet = read_ratchet()
    print(f"{'session':<24} {'ordinals':>8} {'confirmed':>9}  goal")
    for name in session_names():
        masks, meta = load_session(name)
        confirmed = ratchet.get(name, {}).get("confirmed_ordinal", "-")
        print(f"{name:<24} {len(masks):>8} {confirmed!s:>9}  {meta.get('goal', '')}")
    return 0


def record_meta(name: str, goal: str) -> int:
    masks, meta = load_session(name)
    meta.update({
        "schema": 1, "name": name, "goal": goal or meta.get("goal", ""),
        "ordinals": len(masks),
        "recorded": datetime.now(UTC).isoformat(timespec="seconds"),
    })
    (session_dir(name) / "session.json").write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n")
    print(f"SESSION {name} ordinals={len(masks)} goal={meta['goal']!r}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("name", nargs="?", default="")
    verify_parser.add_argument("--write-ratchet", action="store_true",
                               help="accept a lower confirmed ordinal")
    verify_parser.add_argument("--json")
    sub.add_parser("status")
    meta_parser = sub.add_parser("meta")
    meta_parser.add_argument("name")
    meta_parser.add_argument("--goal", default="")
    derive_parser = sub.add_parser("derive")
    derive_parser.add_argument("name")
    derive_parser.add_argument("--movie", required=True, type=Path,
                               help="per-rendered-frame mask file, e.g. build/completion/tas/input.txt")
    derive_parser.add_argument("--goal", default="")
    args = parser.parse_args(argv)
    try:
        if args.command == "status":
            return status()
        if args.command == "meta":
            return record_meta(args.name, args.goal)
        if args.command == "derive":
            movie = args.movie if args.movie.is_absolute() else ROOT / args.movie
            return derive(args.name, movie, args.goal or f"derived from {args.movie}")
        name = args.name or lowest_confirmed()
        return verify(name, write=args.write_ratchet,
                      json_path=Path(args.json) if args.json else None)
    except (SessionError, refstream.RefstreamError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
