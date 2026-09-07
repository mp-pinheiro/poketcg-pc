#!/usr/bin/env python3
"""Verify a recorded human session against the ROM, one DoFrame at a time.

A session is what `just play --record-input` wrote: one byte per DoFrame, the
input the native port actually read. The reference replays the same bytes on
the same axis (refstream's DoFrame anchor, $0552) and the first ordinal where
the two lanes disagree names the byte, its RAM symbol and the reference routine
that wrote it. That routine is the deliverable.

Layout, under tests/sessions/<name>/:
  input.txt     one decimal byte per line, in InputFrame order (src/input.h)
  session.json  {"schema":1,"name","goal","ordinals","terminal_event","recorded"}

Ordinals are 1-based on the native side (frame_boundary_doframe_ordinal after
the increment) and 0-based in the reference stream (records before the hit
counter advances); both are taken at the same instruction, so
reference_index = ordinal - 1 with no phase correction.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import frame_census
import refstream
import scenario as scenario_module

SESSIONS = ROOT / "tests" / "sessions"
RATCHET_PATH = ROOT / "tools" / "completion" / "session_ratchet.json"
# Game state, not hardware fabric: WRAM, HRAM and OAM are what the game reads
# back. IO readback is adjudicated elsewhere -- TAC's unused bits and $FF75
# read differently on the two references (docs/tas-progress-loop.md, "The two
# references disagree"), so they are census rows there and noise here. Every
# IO register the game relies on has a WRAM/HRAM shadow (wLCDC, hSCX, wBGP...)
# that this comparison does see. Palette RAM starts as whatever the no-BIOS
# core leaves in it and the game never reads it back; the scenario census
# owns palette parity.
DOMAINS = ("wram", "hram", "oam")
# Timer-phase state on top of the scenario ledger. The whole sound driver runs
# from the timer interrupt (time.asm:9-26: SoundTimerHandler on every fourth
# TimerHandler, ~60.24 Hz), asynchronous to DoFrame, so at a DoFrame anchor
# its command pointers and counters are one tick apart between lanes on a
# schedule no asm instruction decides -- the same reason the ledger already
# excludes wTimerCounter. The span is exactly SECTION "WRAM Audio"
# (wram.asm:2992-3289, $DD80 up to the stack at $DEE5). Audio correctness is
# the audio-catalog scenario's, compared as an APU write sequence.
TIMING_PHASE = {"wram": [(0xDD80 - 0xC000, 0xDEE5 - 0xC000)]}
# One refstream anchor is RECORD_STRIDE bytes held whole in memory while the
# stream is built; 20,000 ordinals is 174 MB, and WSL has died on this repo
# for less. Longer play is a second session, never a bigger cap.
ORDINAL_CAP = 20000
# The bracket search: 32 geometric probes, then 32 linear probes over the
# bracket per pass until it is exact. One native run per pass.
PROBES_PER_PASS = 32
MAX_PASSES = 6
NATIVE_TIMEOUT = 300


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


def read_ratchet() -> dict[str, dict[str, int]]:
    if not RATCHET_PATH.is_file():
        return {}
    return json.loads(RATCHET_PATH.read_text())


def write_ratchet(ratchet: dict[str, dict[str, int]]) -> None:
    RATCHET_PATH.write_text(json.dumps(ratchet, indent=2, sort_keys=True) + "\n")


def run_native(directory: Path, input_path: Path, n: int, ordinals: list[int]) -> tuple[Path, str]:
    state_path = directory / "state.json"
    command = [
        str(scenario_module.BINARY), "--headless",
        "--data-pack", str(scenario_module.PACK),
        "--frames", "0",
        "--stop-ordinal", str(n),
        "--input-ordinal", str(input_path),
        "--dump-state", str(state_path),
        "--dump-state-ordinals", ",".join(str(value) for value in ordinals),
        "--trace-calls", str(directory / "calls.bin"),
    ]
    try:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True,
            timeout=NATIVE_TIMEOUT, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stderr = (exc.stderr or b"")
        text = stderr.decode(errors="replace") if isinstance(stderr, bytes) else str(stderr)
        return state_path, f"HANG no exit within {NATIVE_TIMEOUT}s\n{text}"
    if result.returncode != 0:
        return state_path, result.stderr.strip()[-2000:] or f"exit {result.returncode}"
    return state_path, ""


def geometric(n: int, count: int) -> list[int]:
    probes = {1, n}
    value = 1
    while value < n and len(probes) < count:
        value *= 2
        probes.add(min(value, n))
    return sorted(probes)


def linear(lo: int, hi: int, count: int) -> list[int]:
    """Probes strictly inside (lo, hi], always including hi."""
    span = hi - lo
    if span <= count:
        return list(range(lo + 1, hi + 1))
    step = span / count
    return sorted({hi} | {lo + max(1, round(step * i)) for i in range(1, count + 1)})


def compare_at(native: dict[str, Any], stream: refstream.Stream, ordinal: int) -> list[tuple[str, int, int, int]]:
    index = ordinal - 1
    if index >= stream.count:
        return []
    return frame_census.compare_frame(native, stream, index, DOMAINS, TIMING_PHASE)


def probe(directory: Path, input_path: Path, n: int, ordinals: list[int],
          stream: refstream.Stream) -> tuple[dict[int, list[tuple[str, int, int, int]]], int, str]:
    """Native run dumping the given ordinals; returns per-ordinal diffs, the
    highest ordinal the native lane reached, and its stderr when it died."""
    state_path, failure = run_native(directory, input_path, n, ordinals)
    dumps = frame_census.native_dumps(state_path)
    diffs = {ordinal: compare_at(native, stream, ordinal) for ordinal, native in dumps.items()}
    reached = max(dumps) if dumps else 0
    if not failure and state_path.is_file():
        final = json.loads(state_path.read_text())
        reached = max(reached, n) if final.get("runtime") else reached
    return diffs, reached, failure


def first_divergence(name: str, masks: list[int], stream: refstream.Stream) -> dict[str, Any]:
    """Bracket the first divergent ordinal: 32 geometric probes, then 32 linear
    probes over the bracket per pass until it is one ordinal wide. For 20,000
    ordinals that is four native runs (bracket 10,000 -> 313 -> 10 -> exact)."""
    n = len(masks)
    input_path = session_dir(name) / "input.txt"
    lo, hi = 0, None
    rows: list[tuple[str, int, int, int]] = []
    reached = 0
    failure = ""
    with tempfile.TemporaryDirectory(prefix=f"session-{name}-") as tmp:
        directory = Path(tmp)
        for pass_index in range(MAX_PASSES):
            if pass_index == 0:
                ordinals = geometric(n, PROBES_PER_PASS)
            else:
                assert hi is not None
                if hi - lo <= 1:
                    break
                ordinals = linear(lo, hi, PROBES_PER_PASS)
            pass_dir = directory / f"pass{pass_index}"
            pass_dir.mkdir()
            diffs, pass_reached, pass_failure = probe(pass_dir, input_path, n, ordinals, stream)
            reached = max(reached, pass_reached)
            failure = failure or pass_failure
            divergent = sorted(ordinal for ordinal, diff in diffs.items() if diff)
            clean = sorted(ordinal for ordinal, diff in diffs.items() if not diff)
            if not divergent:
                if hi is None:
                    return {"ordinal": None, "rows": [], "reached": reached, "failure": failure}
                lo = max([lo] + [o for o in clean if o < hi])
                break
            hi = divergent[0]
            rows = diffs[hi]
            lo = max([lo] + [o for o in clean if o < hi])
    return {"ordinal": hi, "rows": rows, "reached": reached, "failure": failure}


def attribute(name: str, masks: list[int], frames: int, rows: list[tuple[str, int, int, int]],
              ordinal: int) -> list[dict[str, Any]]:
    addresses = sorted({
        frame_census.FIELD_BASE[field] + offset
        for field, offset, _got, _want in rows if field in frame_census.FIELD_BASE
    })[:16]
    writers = {
        int(entry["address"], 16): entry
        for entry in refstream.writers(f"session:{name}", frames, addresses,
                                       events=True, masks=masks, axis="ordinal")
    } if addresses else {}
    out = []
    for field, offset, got, want in rows[:64]:
        symbol, _base = refstream.resolve_region(field, offset)
        address = frame_census.FIELD_BASE.get(field, 0) + offset
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
    # One row per symbol, earliest offset first, so the status lines stay short.
    seen: set[str] = set()
    unique = []
    for row in out:
        if row["symbol"] in seen:
            continue
        seen.add(row["symbol"])
        unique.append(row)
    return unique


def verify(name: str, *, write: bool, json_path: Path | None) -> int:
    masks, meta = load_session(name)
    n = len(masks)
    report: dict[str, Any] = {"schema": 1, "format": "session-verify-v1", "name": name,
                              "ordinals": n, "goal": meta.get("goal", "")}
    if n > ORDINAL_CAP:
        report["status"] = "too-long"
        print(f"SESSION {name} status=too-long ordinals={n} cap={ORDINAL_CAP}")
        return 2
    frames = n * 2 + 400
    stream = refstream.open_stream(f"session:{name}", frames, n, masks, axis="ordinal")
    try:
        if stream.count < n:
            report.update(status="ref-short", confirmed=0, reference_ordinals=stream.count)
            print(f"SESSION {name} status=ref-short confirmed=0 ordinals={n} reference={stream.count}")
            emit(report, json_path)
            return 4
        found = first_divergence(name, masks, stream)
    finally:
        stream.close()
    if found["ordinal"] is None and found["reached"] < n:
        confirmed = found["reached"]
        status = "native-short"
    elif found["ordinal"] is None:
        confirmed, status = n, "clean"
    else:
        confirmed, status = found["ordinal"] - 1, "diverged"
    report.update(status=status, confirmed=confirmed, reached=found["reached"],
                  native_failure=found["failure"])
    print(f"SESSION {name} status={status} confirmed={confirmed} ordinals={n}")
    if status == "diverged":
        details = attribute(name, masks, frames, found["rows"], found["ordinal"])
        report["divergence"] = {"ordinal": found["ordinal"], "rows": details}
        for row in details[:8]:
            print(f"DIVERGE ordinal={found['ordinal']} field={row['field']} address={row['address']} "
                  f"symbol={row['symbol']} native={row['native']} reference={row['reference']} "
                  f"writer={row['writer']}")
    if status == "native-short" and found["failure"]:
        tail = found["failure"].strip().splitlines()[-3:]
        for line in tail:
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


def emit(report: dict[str, Any], json_path: Path | None) -> None:
    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")


def lowest_confirmed() -> str:
    ratchet = read_ratchet()
    names = sorted(p.name for p in SESSIONS.iterdir() if (p / "input.txt").is_file()) if SESSIONS.is_dir() else []
    if not names:
        raise SessionError("no sessions under tests/sessions")
    return min(names, key=lambda name: (ratchet.get(name, {}).get("confirmed_ordinal", -1), name))


def status() -> int:
    ratchet = read_ratchet()
    names = sorted(p.name for p in SESSIONS.iterdir() if (p / "input.txt").is_file()) if SESSIONS.is_dir() else []
    print(f"{'session':<24} {'ordinals':>8} {'confirmed':>9}  goal")
    for name in names:
        masks, meta = load_session(name)
        confirmed = ratchet.get(name, {}).get("confirmed_ordinal", "-")
        print(f"{name:<24} {len(masks):>8} {str(confirmed):>9}  {meta.get('goal', '')}")
    return 0


def record_meta(name: str, goal: str) -> int:
    """Write session.json for a freshly recorded input.txt."""
    masks, meta = load_session(name)
    meta.update({
        "schema": 1, "name": name, "goal": goal or meta.get("goal", ""),
        "ordinals": len(masks),
        "terminal_event": meta.get("terminal_event", ""),
        "recorded": datetime.now(timezone.utc).isoformat(timespec="seconds"),
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
    args = parser.parse_args(argv)
    try:
        if args.command == "status":
            return status()
        if args.command == "meta":
            return record_meta(args.name, args.goal)
        name = args.name or lowest_confirmed()
        return verify(name, write=args.write_ratchet,
                      json_path=Path(args.json) if args.json else None)
    except (SessionError, frame_census.FrameCensusError, refstream.RefstreamError,
            OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
