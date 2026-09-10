#!/usr/bin/env python3
"""The sound driver as a closed state machine, proven one tick at a time.

The driver's whole state is `SECTION "WRAM Audio"` ($DD80-$DEE4); its input is
the song and SFX data in ROM and one timer tick (SoundTimerHandler); its output
is the next state and the APU register writes. Game code reaches it only
through the four request bytes at $DD80-$DD83. So a seed is 357 bytes taken on
the reference at a tick entry, and the proof runs N ticks from that seed on the
gbref runner (`completion: tick`) and on the native probe (`repeat`), comparing
the driver state and the write stream after every tick.

`seeds` takes the corpus from the recorded sessions: every K-th tick and the
first tick after each PlaySong/PlaySFX, deduplicated by state. `diff` runs the
corpus and reports the first divergent tick per seed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools" / "completion"))

import refstream
import session

SEEDS = ROOT / "build" / "audio" / "seeds"
REPORT = ROOT / "build" / "audio" / "tickdiff.json"
DRIVER_BASE = 0xDD80
DRIVER_SIZE = 0xDEE5 - 0xDD80
DRIVER_BANK = 0x3D
APU_BASE = 0xFF10
APU_SIZE = 0x30
SOUND_TIMER_HANDLER = 0x4003
PLAY_SONG = 0x3785
PLAY_SFX = 0x3796
ROM = ROOT / "poketcg" / "poketcg.gbc"
SYMBOLS = ROOT / "poketcg" / "poketcg.sym"
RUNNER = ROOT / "tools" / "oracle" / "gbref" / "build" / "gbref_runner"
PROBE = ROOT / os.environ.get("POKETCG_BUILD", "build") / "poketcg_probe"
DEFAULT_TICKS = 4096
DEFAULT_EVERY = 1024
SEED_FORMAT = "audio-seed-v1"


class TickError(RuntimeError):
    pass


def seed_path(digest: str) -> Path:
    return SEEDS / f"{digest}.json"


def take_seeds(name: str, *, every: int) -> tuple[int, int]:
    """Replay one session on the reference; write a seed at every `every`-th
    tick and at the first tick after each song or SFX request. Returns
    (ticks seen, seeds written)."""
    masks, meta = session.load_session(name)
    ratchet = session.read_ratchet().get(name)
    if ratchet is None:
        raise TickError(f"{name} has never been verified")
    limit = min(len(masks), int(ratchet["confirmed_ordinal"]))
    frames = session.reference_frames(masks, meta)
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    SEEDS.mkdir(parents=True, exist_ok=True)
    ticks = 0
    written = 0
    requested = False
    with refstream.Core(padded, pokes=meta["pokes"] or None) as core:
        core.input_axis = "ordinal"
        read = core.library.gambatte_cpuread

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal ticks, written, requested
            if address == PLAY_SONG or address == PLAY_SFX:
                requested = True
                return
            if address != SOUND_TIMER_HANDLER or core.bank_of(address) != DRIVER_BANK:
                return
            ticks += 1
            if not requested and ticks % every:
                return
            requested = False
            state = core.area("WRAM")[DRIVER_BASE - 0xC000:DRIVER_BASE - 0xC000 + DRIVER_SIZE]
            apu = bytes(read(core.core, address) for address in range(APU_BASE, APU_BASE + APU_SIZE))
            digest = hashlib.sha256(state + apu).hexdigest()[:16]
            path = seed_path(digest)
            if path.is_file():
                return
            path.write_text(json.dumps({
                "schema": 1, "format": SEED_FORMAT, "digest": digest, "session": name,
                "ordinal": core.ordinal, "tick": ticks, "song": state[0], "song_bank": state[1],
                "sfx": state[2], "hbank": read(core.core, 0xFF80), "wram": state.hex(), "apu": apu.hex(),
            }, sort_keys=True) + "\n")
            written += 1

        core.install_exec(on_exec)
        core.run(frames, stop=lambda: core.ordinal > limit)
    return ticks, written


def seed_worker(name: str, every: int) -> tuple[str, str]:
    command = [sys.executable, str(Path(__file__).resolve()), "seeds", name, "--every", str(every), "--jobs", "1"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return name, result.stderr.strip()[-300:] or f"exit {result.returncode}"
    return name, result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""


def seeds(names: list[str], *, every: int, jobs: int) -> int:
    if len(names) == 1 and jobs == 1:
        ticks, written = take_seeds(names[0], every=every)
        print(f"SEEDS {names[0]} ticks={ticks} written={written}")
        return 0
    names = sorted(names, key=lambda name: -(session.read_ratchet().get(name, {}).get("confirmed_ordinal", 0)))
    failed = 0
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for name, line in pool.map(lambda name: seed_worker(name, every), names):
            if not line.startswith("SEEDS"):
                failed += 1
                print(f"SEEDS {name} failed: {line}")
            else:
                print(line)
    print(f"SEEDS corpus={len(list(SEEDS.glob('*.json')))}")
    return 1 if failed else 0


def load_symbols() -> list[tuple[int, str]]:
    rows = []
    for line in SYMBOLS.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and ":" in parts[0]:
            bank, address = parts[0].split(":")
            if bank == "00" and 0xC000 <= int(address, 16) < 0xE000:
                rows.append((int(address, 16), parts[1]))
    rows.sort()
    return rows


def symbol_at(symbols: list[tuple[int, str]], address: int) -> str:
    name = "?"
    for base, label in symbols:
        if base > address:
            break
        name = label if base == address else f"{label}+{address - base}"
    return name


def run_reference(seed: dict[str, Any], ticks: int) -> dict[str, Any]:
    request = {
        "completion": "tick", "repeat": ticks, "hardware": "cgb", "entry": SOUND_TIMER_HANDLER,
        "rom_bank": DRIVER_BANK, "hbank_rom": seed.get("hbank", DRIVER_BANK), "ram_bank": 0,
        "ram_enable": 0, "vram_bank": 0, "instruction_budget": 2_000_000, "cycle_budget": 8_000_000,
        "a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0,
        "seed_wram": f"{DRIVER_BASE:x}={seed['wram']};{APU_BASE:x}={seed['apu']}",
        "read_bus": f"{DRIVER_BASE:x}:{DRIVER_SIZE:x}",
    }
    result = subprocess.run([str(RUNNER), "--rom", str(ROM.resolve())], input=json.dumps(request),
                            capture_output=True, text=True, check=False)
    line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
    if not line.startswith("{"):
        raise TickError(f"gbref runner produced no result: {result.stderr.strip()[-200:]}")
    return json.loads(line)


def run_native(seed: dict[str, Any], ticks: int) -> dict[str, Any]:
    request = {
        "fn": "SoundTimerHandler", "repeat": ticks, "rom_bank": DRIVER_BANK,
        "wram": {str(DRIVER_BASE): seed["wram"], str(APU_BASE): seed["apu"]},
        "read": {str(DRIVER_BASE): DRIVER_SIZE},
    }
    env = dict(os.environ, POKETCG_ROM=str(ROM.resolve()))
    result = subprocess.run([str(PROBE)], input=json.dumps(request), capture_output=True, text=True,
                            env=env, check=False)
    line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
    if not line.startswith("{"):
        raise TickError(f"native probe produced no result: {result.stderr.strip()[-200:]}")
    return json.loads(line)


def compare(seed: dict[str, Any], ticks: int, symbols: list[tuple[int, str]]) -> dict[str, Any]:
    reference = run_reference(seed, ticks)
    native = run_native(seed, ticks)
    row: dict[str, Any] = {"digest": seed["digest"], "session": seed["session"], "ordinal": seed["ordinal"],
                           "song": seed["song"], "sfx": seed["sfx"], "ticks": ticks}
    if reference.get("status") != "REFERENCE_OK":
        row.update(status="reference-failed", detail=f"{reference.get('status')} at tick {reference.get('tick')}")
        return row
    if "error" in native:
        row.update(status="native-failed", detail=native["error"])
        return row
    ref_ticks = reference["ticks"]
    nat_ticks = native["ticks"]
    for index in range(min(len(ref_ticks), len(nat_ticks))):
        ref_bus, nat_bus = ref_ticks[index]["bus"], nat_ticks[index]["bus"]
        ref_writes, nat_writes = ref_ticks[index]["writes"], nat_ticks[index]["writes"]
        if ref_bus == nat_bus and ref_writes == nat_writes:
            continue
        differing = []
        for offset in range(0, min(len(ref_bus), len(nat_bus)), 2):
            if ref_bus[offset:offset + 2] != nat_bus[offset:offset + 2]:
                address = DRIVER_BASE + offset // 2
                differing.append({"address": f"0x{address:04X}", "symbol": symbol_at(symbols, address),
                                  "reference": ref_bus[offset:offset + 2], "native": nat_bus[offset:offset + 2]})
        row.update(status="diverged", tick=index + 1, fields=differing[:12],
                   writes={"reference": ref_writes, "native": nat_writes} if ref_writes != nat_writes else None)
        return row
    if len(ref_ticks) != len(nat_ticks):
        row.update(status="short", detail=f"reference {len(ref_ticks)} ticks, native {len(nat_ticks)}")
        return row
    row["status"] = "clean"
    return row


def diff(digests: list[str], *, ticks: int, jobs: int, json_path: Path | None) -> int:
    paths = [seed_path(digest) for digest in digests] if digests else sorted(SEEDS.glob("*.json"))
    if not paths:
        raise TickError(f"no seeds under {SEEDS.relative_to(ROOT)}: run `just audio-seeds`")
    for binary in (RUNNER, PROBE):
        if not binary.is_file():
            raise TickError(f"missing {binary.relative_to(ROOT)}")
    seeds_loaded = [json.loads(path.read_text()) for path in paths]
    symbols = load_symbols()
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        for row in pool.map(lambda seed: compare(seed, ticks, symbols), seeds_loaded):
            rows.append(row)
            if row["status"] == "clean":
                print(f"TICK {row['digest']} status=clean song={row['song']} sfx={row['sfx']} ticks={ticks}")
            elif row["status"] == "diverged":
                fields = " ".join(f"{f['symbol']}={f['native']}!={f['reference']}" for f in row["fields"][:4])
                print(f"TICK {row['digest']} status=diverged tick={row['tick']} song={row['song']} "
                      f"sfx={row['sfx']} session={row['session']} ordinal={row['ordinal']} {fields}"
                      + (" writes-differ" if row.get("writes") else ""))
            else:
                print(f"TICK {row['digest']} status={row['status']} {row.get('detail', '')}")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    summary = " ".join(f"{status}={count}" for status, count in sorted(counts.items()))
    print(f"TICKDIFF seeds={len(rows)} ticks={ticks} {summary}")
    report = {"schema": 1, "format": "audio-tickdiff-v1", "ticks": ticks, "counts": counts, "rows": rows}
    out = json_path or REPORT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    return 0 if counts.get("clean", 0) == len(rows) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    seeds_parser = sub.add_parser("seeds", help="take driver seeds from recorded sessions")
    seeds_parser.add_argument("names", nargs="*", help="sessions; default every verified session")
    seeds_parser.add_argument("--every", type=int, default=DEFAULT_EVERY, help="ticks between seeds")
    seeds_parser.add_argument("--jobs", type=int, default=4)
    diff_parser = sub.add_parser("diff", help="run the corpus on both lanes, tick by tick")
    diff_parser.add_argument("digests", nargs="*", help="seed digests; default the whole corpus")
    diff_parser.add_argument("--ticks", type=int, default=DEFAULT_TICKS)
    diff_parser.add_argument("--jobs", type=int, default=4)
    diff_parser.add_argument("--json", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "seeds":
            names = args.names or [name for name in session.session_names()
                                   if name in session.read_ratchet() and not name.startswith("_")]
            return seeds(names, every=args.every, jobs=args.jobs)
        return diff(args.digests, ticks=args.ticks, jobs=args.jobs, json_path=args.json)
    except (TickError, session.SessionError, refstream.RefstreamError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
