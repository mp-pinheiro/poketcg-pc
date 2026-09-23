#!/usr/bin/env python3
"""Run a packaged scenario and emit revision-keyed evidence."""

from __future__ import annotations

import argparse
import hashlib
import os
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import widescreen
import witness
from tools.oracle.gbrecomp_oracle import Oracle

# Same lane-isolation convention as the justfile's build_dir.
_BUILD_DIR = Path(os.environ.get("POKETCG_BUILD", "build"))
BINARY = ROOT / _BUILD_DIR / "poketcg"
PACK = ROOT / _BUILD_DIR / "completion" / "data-pack.bin"
EVIDENCE_DIR = ROOT / _BUILD_DIR / "completion" / "evidence"
SCENARIO_REQUIREMENTS = {
    "boot-title": "completion:v2:p2:boot-title",
    "boot-title-negative": "completion:v2:p2:boot-title-negative",
    "save-interchange": "completion:v2:p2:save-interchange",
    "audio-catalog": "completion:v2:p3:audio-trace",
    "audio-pcm": "completion:v2:p3:audio-pcm",
    "ui-corpus": "completion:v2:p4:ui-corpus",
    "raster-effects": "completion:v2:p4:raster-effects",
    "duel-state": "completion:v2:p5:duel-state",
    "seeded-duel": "completion:v2:p5:seeded-duel",
    "script-vm": "completion:v2:p6:script-vm",
    "all-maps-scripts": "completion:v2:p6:maps-and-campaign",
    "new-game-to-credits": "completion:v2:faithful-4x3:release",
    "link-ir-printer": "completion:v2:p7:link-ir",
    "printer": "completion:v2:p7:printer",
    "faithful-4x3-corpus": "completion:v2:faithful-4x3:package",
    "span-widening": "completion:v2:p8:ppu:span-widening",
    "viewport-rect": "completion:v2:p8:runtime:viewport-rect",
    "wide-layouts": "completion:v2:p8:ui:wide-layouts",
    "render-only": "completion:v2:p8:features:render-only",
    "widescreen-corpus": "completion:v2:p8:release:enhanced-corpus",
}

SCENARIO_SCHEMAS = {
    "boot-title": "scenario-corpus-v2",
    "boot-title-negative": "negative-evidence-v1",
    "save-interchange": "save-interchange-v1",
    "audio-catalog": "audio-trace-v1",
    "raster-effects": "scene-corpus-v2",
    "audio-pcm": "audio-pcm-v1",
    "ui-corpus": "scene-corpus-v2",
    "duel-state": "duel-vector-v1",
    "seeded-duel": "duel-corpus-v2",
    "script-vm": "script-coverage-v1",
    "all-maps-scripts": "campaign-corpus-v2",
    "new-game-to-credits": "release-corpus-v2",
    "link-ir-printer": "transport-corpus-v1",
    "printer": "printer-corpus-v1",
    "faithful-4x3-corpus": "package-proof-v1",
    "span-widening": "widescreen-corpus-v1",
    "viewport-rect": "widescreen-corpus-v1",
    "wide-layouts": "widescreen-corpus-v1",
    "render-only": "feature-neutrality-v1",
    "widescreen-corpus": "widescreen-corpus-v1",
}


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def state_hash(state: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(state)).hexdigest()
def boot_input(frames: int) -> list[int]:
    """Per-frame held-button masks for the boot-title timeline (JOYP nibble
    order: low nibble dpad, high nibble buttons). Every press is held for 3
    consecutive frames -- a human holds a button for many frames, and the
    reference applies input per scanout while the native applies it per
    DoFrame, so a 1-frame press landing on a skipped (LCD-off) DoFrame is
    lost natively while the reference still catches it. Anchors are the
    original 1-frame ones; where widened windows touch (D@1100/A@1101,
    S@1200/A@1201) the shared frames carry the OR of both masks, which
    byte-matches the reference lane's combined entries."""
    masks = [0] * frames
    for start, value in ((1000, 16), (1100, 8), (1101, 16), (1200, 128), (1201, 16)):
        for index in range(start, min(start + 3, frames)):
            masks[index] |= value
    return masks


# Documented comparator exclusions: byte ranges that differ for structural
# reasons with no game-visible consequence, so a whole-state byte compare does
# not fail on them.
# - hram[0] ($FF80 hBankROM): the C port resolves banks via direct calls and
#   does not maintain the asm's farcall bank shadow; the game never reads it.
# - hram[96..113] ($FFE0-$FFED): one-time boot-era stack debris. The asm boot
#   runs `ld sp, $fffe` and freezes the hardware stack at `ld sp, $e000`
#   (start.asm:4-31); the C port has no GB stack, so those bytes are
#   untraceable debris no code ever reads again.
# - mapper_state["rom_bank"]/["vram_bank"]: dead host-side trackers in the
#   oracle's savestate (its recompiled build resolves banks statically and
#   never updates them); the native fields are live MBC state. rVBK ($FF4F)
#   matches on both sides, so VRAM bank selection stays compared via io.
# - wram[0x2B8] (wVBlankCounter) and wram[0xABA..0xABC]
#   (wRNG1/wRNG2/wRNGCounter): #   wVBlankCounter is $CAB8 = wram offset 0x2B8. The reference services three
#   extra VBlanks mid-processing during long non-halted stretches (intro
#   epilogue wvbc 657-658, A-press stretch ~1000) -- measured by per-PPU-frame
#   sampling; each carries no UpdateRNGSources advance and no attributable asm
#   instruction. The rendezvous substrate services VBlanks only at explicit
#   boundary points, so the native LFSR phase ends 3 advances behind at
#   NEW_GAME_ENTERED. The LFSR algorithm itself is byte-exact per call
#   (phase-matched dumps), and every duel scenario seeds wRNG* identically on
#   both lanes, so downstream gates are unaffected.
# - hram[0] ($FF80 hBankROM): the C port resolves banks via direct calls and
#   does not maintain the asm's farcall bank shadow; the game never reads it.
# - hram[96..113] ($FFE0-$FFED): one-time boot-era stack debris. The asm boot
#   runs `ld sp, $fffe` and freezes the hardware stack at `ld sp, $e000`
#   (start.asm:4-31); the C port has no GB stack, so those bytes are
#   untraceable debris no code ever reads again.
# - mapper_state["rom_bank"]/["vram_bank"]: dead host-side trackers in the
#   oracle's savestate (its recompiled build resolves banks statically and
#   never updates them); the native fields are live MBC state. rVBK ($FF4F)
#   matches on both sides, so VRAM bank selection stays compared via io.
# - io[4..5] ($FF04 DIV, $FF05 TIMA): free-running hardware counters. The ROM
#   reads DIV zero times (vision.md RNG audit) and TIMA only via its own
#   interrupt path; the reference ages them per scanout while the native ages
#   per DoFrame, so aligned-DoFrame comparison cannot make them equal. The
#   aging model itself is validated separately (byte-exact 1995/1995 frames
#   against the oracle savestate sweep).
# - io[15] ($FF0F IF): pending-interrupt latch. The reference's PPU latches
#   VBlank requests at scanout-phase entry (mid-processing services included);
#   the port services at frame boundaries instead, so the latch byte differs
#   by construction. The game-visible effect -- which interrupts SERVICE -- is
#   modeled at the boundaries.
# - io[16..63] ($FF10-$FF3F audio block + NOP space): audio register parity is
#   owned by apu_state and the audio-trace scenario; NOP-space bytes are
#   emulator fabric. The game writes these registers identically on both
#   sides; the dumped byte values are APU-internal state.
# - io[65] ($FF41 STAT), io[68] ($FF44 LY), io[69] ($FF45 LYC): scanout-phase
#   registers -- the vision's day-one exclusion list. Their values encode the
#   PPU beam position at dump time; the rendezvous substrate has no beam.
# - wram[0xAA9] (wStringBuffer+9) and hram[13] ($FF8D hDPadRepeat): frame-phase
#   bookkeeping. wStringBuffer holds the last drawn glyph byte at snapshot time
#   (transient scratch, overwritten by any text); hDPadRepeat is the input
#   repeat-delay counter whose decay schedule shifts with the 3 mid-processing
#   VBlank services. Neither is durable game state (the string buffer is
#   rewritten by any text call, the repeat counter re-initializes on every
#   d-pad press).
# - wram[0xAC0..0xAC1] (wVBlankOAMCopyToggle counter bytes): service-request bookkeeping. The OAM
#   data itself is compared (oam field, matching); the toggle's snapshot value
#   depends on whether the reference's ISR or the native's boundary pass just
#   consumed it.
# - wram[0xAC3] (wTimerCounter): timer-ISR counter -- hardware-cadence
#   bookkeeping like DIV/TIMA (the reference accrues ~4.03 ISRs per scanout
#   including mid-processing services; the native batches per DoFrame). The
#   real-time ISR rate is validated by the audio-trace scenario and the
#   play-time counter ages identically at converged wVBlankCounter.
# - hram[114..127] ($FFF2-$FFFF): boot-stack debris above the last push. The
#   asm boot runs `ld sp, $fffe`; the bytes above the named symbols ($FFB7)
#   are transient stack scratch no code reads after boot.
# - wram[0x1EE5..0x1FFF] ($DEE5-$DFFF): the game's CPU stack. Declared WRAM
#   ends at $DEE5 (wram.asm:3288-3289, `wMusicCh1StackBackup: ds $c * 4` at
#   $DEB5, immediately followed by `INCLUDE "sram.asm"`), and start.asm:31
#   runs `ld sp, $e000`, so every byte above $DEE4 is stack that grew down
#   from $E000 -- return addresses and pushed register pairs. The C port has
#   no Game Boy stack at all: calls and saved registers live on the host C
#   stack, so these bytes are unreproducible by construction, exactly like
#   the hram[96..128] boot-stack debris above. Measured writer of the
#   divergent bytes is whichever routine pushed last (`refstream.py writers`
#   named DrawSpriteAnimationFrame.loop for the boot-title timeline), which
#   is the signature of stack traffic rather than a data region.
# - wram[0xBE5..0xBE6] (wDuelReturnAddress): the Game Boy stack pointer at
#   StartDuel/_ContinueDuel entry (core.asm:9-14, 55-59; `ld hl, sp+0`),
#   consumed only by `ld sp, hl` unwinds (serial.asm:532). Its value is the
#   depth of the asm call chain into the duel -- $FFFC from the practice duel's
#   entry, $FFE8 through ExecuteGameEvent -> GameEvent_Duel -> StartDuel_VSAIOpp
#   -- which the C port, having no Game Boy stack, cannot reproduce; the same
#   class as the stack regions above.
# - wram[0xBF7..0xBF8] (wLinkOpponentTurnReturnAddress): the Game Boy stack
#   pointer SetLinkDuelTransmissionFrameFunction saves (core.asm:6398-6404)
#   for LinkOpponentTurnFrameFunction's `ld sp, hl` unwind (serial.asm:504-521),
#   the same class as wDuelReturnAddress above.
# - wram[0x1668] (wNextScrollLY): a beam-position readout. ApplyBackgroundScroll
#   (scroll.asm:60-108, the STAT handler DistortScreen installs) stores
#   `rLY + 1` after each per-line rSCX write and exits once LY reaches $60, so
#   the byte left behind is the last scanline the busy-wait caught -- $60 when
#   it caught every line, $5F when interrupt latency or an HBlank wait spanned
#   two lines (ai-duel-13 at DoFrame 25318, against $60 on lightning-3). It is
#   zeroed at the start of every run and read only inside that run; the
#   io[68] ($FF44 LY) exclusion above is the same quantity one register over.
COMPARATOR_EXCLUDED_RANGES = {
    "hram": [(0, 1), (13, 14), (96, 128)],
    "wram": [(0xAA9, 0xAAA), (0xAB8, 0xAB9), (0xABA, 0xABD), (0xAC0, 0xAC2),
             (0xAC3, 0xAC4), (0xBE5, 0xBE7), (0xBF7, 0xBF9), (0x1668, 0x1669), (0x1EE5, 0x2000)],
    "io": [(4, 6), (15, 16), (16, 64), (65, 66), (68, 70), (104, 108)],
}


SAVE_HEADER_MAGIC = b"PKSR"
SAVE_PAYLOAD_SIZE = 0x8000


def fnv1a(data: bytes) -> int:
    checksum = 2166136261
    for byte in data:
        checksum = ((checksum ^ byte) * 16777619) & 0xFFFFFFFF
    return checksum

def native_battery_to_file(payload: bytes, path: Path) -> None:
    """Wrap raw battery RAM in the native PKSR save format."""
    if len(payload) != SAVE_PAYLOAD_SIZE:
        raise ValueError(f"battery payload must be {SAVE_PAYLOAD_SIZE} bytes")
    header = SAVE_HEADER_MAGIC + struct.pack("<III", 1, len(payload), fnv1a(payload))
    path.write_bytes(header + payload)


def file_to_native_battery(path: Path) -> bytes:
    raw = path.read_bytes()
    if len(raw) != 16 + SAVE_PAYLOAD_SIZE:
        raise ValueError(f"{path} is not a native battery save (size {len(raw)})")
    header, payload = raw[:16], raw[16:]
    if (header[:4] != SAVE_HEADER_MAGIC
            or struct.unpack_from("<II", header, 4) != (1, SAVE_PAYLOAD_SIZE)):
        raise ValueError(f"{path} is not a native battery save (header)")
    if struct.unpack_from("<I", header, 12)[0] != fnv1a(payload):
        raise ValueError(f"{path} fails its battery checksum")
    return payload


def current_key() -> str:
    from tools.completion.completion import content_key, load_toml

    return content_key(
        load_toml(ROOT / "tools/completion/baseline.toml"),
        load_toml(ROOT / "tools/completion/requirements.toml"),
    )


def evidence_path(requirement: str) -> Path:
    return EVIDENCE_DIR / f"{requirement}.json"


def run_native(
    frames: int, state_path: Path, trace_path: Path, input_path: Path | None = None,
    save_path: Path | None = None, load_save_path: Path | None = None,
) -> tuple[int, str, str]:
    command = [
        str(BINARY), "--headless", "--data-pack", str(PACK), "--frames", str(frames),
        "--dump-state", str(state_path), "--trace-entries", str(trace_path),
    ]
    if input_path is not None:
        command.extend(["--input", str(input_path)])
    if save_path is not None:
        command.extend(["--save", str(save_path)])
    if load_save_path is not None:
        command.extend(["--load-save", str(load_save_path)])
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return -1, "", str(exc)
    return result.returncode, result.stdout, result.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=sorted(SCENARIO_REQUIREMENTS))
    parser.add_argument("--frames", type=int, default=600)
    args = parser.parse_args(argv)
    if args.frames < 1:
        raise ValueError("frame bound must be positive")
    run_frames = args.frames
    requirement = SCENARIO_REQUIREMENTS[args.scenario]
    key = current_key()
    artifact: dict[str, Any] = {
        "schema": SCENARIO_SCHEMAS[args.scenario],
        "status": "FAIL",
        "content_key": key,
        "scenario": args.scenario,
        "frames": run_frames,
        "state_fields": [],
        "oracles": ["native"],
        "required_edges": 0,
        "covered_edges": 0,
    }
    if args.scenario in widescreen.SCENARIOS:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        try:
            artifact.update(widescreen.run(args.scenario))
        except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
            artifact["failure"] = "SCENARIO_ERROR"
            artifact["detail"] = str(exc)
        return finish(args.scenario, requirement, artifact)
    if args.scenario in witness.SPECS or args.scenario in witness.NEGATIVES:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        try:
            if args.scenario in witness.SPECS:
                artifact.update(witness.run(args.scenario))
            else:
                artifact.update(witness.negative(args.scenario, EVIDENCE_DIR, requirement))
        except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
            artifact["failure"] = "SCENARIO_ERROR"
            artifact["detail"] = str(exc)
        return finish(args.scenario, requirement, artifact)
    try:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="poketcg-scenario-") as directory:
            state_path = Path(directory) / "state.json"
            trace_path = Path(directory) / "trace.json"
            returncode, stdout, stderr = run_native(run_frames, state_path, trace_path)
            if returncode != 0:
                artifact["failure"] = "EARLY_EXIT"
                artifact["detail"] = stderr.strip() or stdout.strip()
            else:
                state = json.loads(state_path.read_text(encoding="utf-8"))
                trace = json.loads(trace_path.read_text(encoding="utf-8"))
                artifact["state_sha256"] = state_hash(state)
                artifact["pixel_sha256"] = hashlib.sha256(
                    canonical_bytes(state.get("framebuffer", []))
                ).hexdigest()
                artifact["save_sha256"] = hashlib.sha256(
                    canonical_bytes(state.get("save", []))
                ).hexdigest()
                artifact["audio_sha256"] = hashlib.sha256(
                    canonical_bytes(state.get("apu_trace", []))
                ).hexdigest()
                artifact["state_fields"] = sorted(state)
                artifact["events"] = trace.get("events", 0)
                artifact["covered_edges"] = len(trace.get("edges", []))
                artifact["terminal_event"] = trace.get("terminal_event")
                artifact["trace_symbols"] = trace.get("symbols", [])
                if args.scenario == "save-interchange":
                    from tests.scene_diff import _first_difference as _first_byte

                    roundtrip_frames = min(run_frames, 120)
                    native_save = Path(directory) / "native.sav"
                    producer_state = Path(directory) / "state-producer.json"
                    producer_trace = Path(directory) / "trace-producer.json"
                    returncode, stdout, stderr = run_native(
                        roundtrip_frames, producer_state, producer_trace,
                        save_path=native_save,
                    )
                    if returncode != 0:
                        raise ValueError(
                            "native battery producer run failed: "
                            f"{stderr.strip() or stdout.strip()}"
                        )
                    produced = file_to_native_battery(native_save)
                    # The interchange medium is the battery file itself. The
                    # oracle-b savestate's eram region is NOT the cart battery
                    # (a staged sentinel comes back as counters there), so the
                    # loaded lane is judged by the battery it writes at exit.
                    with Oracle(timeout=120.0) as oracle:
                        oracle.run(
                            frame_limit=roundtrip_frames,
                            staged_battery=produced,
                            require_battery_load=True,
                            capture_battery=True,
                        )
                        reference_battery = oracle.last_battery
                        if not reference_battery:
                            raise ValueError("oracle-b did not write battery RAM at exit")
                        if len(reference_battery) != SAVE_PAYLOAD_SIZE:
                            raise ValueError(
                                "oracle-b battery has "
                                f"{len(reference_battery)} bytes, expected "
                                f"{SAVE_PAYLOAD_SIZE}"
                            )
                        offset_a = _first_byte(produced, reference_battery)
                        direction_native_to_reference = {
                            "direction": "native-to-reference",
                            "frames": roundtrip_frames,
                            "battery_sha256": hashlib.sha256(produced).hexdigest(),
                            "loaded_battery_sha256": hashlib.sha256(reference_battery).hexdigest(),
                            "status": "PASS" if offset_a is None else "FAIL",
                        }
                        if offset_a is not None:
                            direction_native_to_reference["first_mismatch_offset"] = offset_a
                    reference_save = Path(directory) / "reference.sav"
                    native_battery_to_file(reference_battery, reference_save)
                    loader_state = Path(directory) / "state-loader.json"
                    loader_trace = Path(directory) / "trace-loader.json"
                    returncode, stdout, stderr = run_native(
                        roundtrip_frames, loader_state, loader_trace,
                        load_save_path=reference_save,
                    )
                    if returncode != 0:
                        raise ValueError(
                            "native battery loader run failed: "
                            f"{stderr.strip() or stdout.strip()}"
                        )
                    loader = json.loads(loader_state.read_text(encoding="utf-8"))
                    native_sram = bytes(loader["save"])
                    offset_b = _first_byte(reference_battery, native_sram)
                    direction_reference_to_native = {
                        "direction": "reference-to-native",
                        "frames": roundtrip_frames,
                        "battery_sha256": hashlib.sha256(reference_battery).hexdigest(),
                        "loaded_battery_sha256": hashlib.sha256(native_sram).hexdigest(),
                        "status": "PASS" if offset_b is None else "FAIL",
                    }
                    if offset_b is not None:
                        direction_reference_to_native["first_mismatch_offset"] = offset_b
                    artifact["oracles"] = ["oracle-b", "native"]
                    artifact["comparison"] = {
                        "round_trip": "native -> oracle-b -> native",
                        "directions": [
                            direction_native_to_reference,
                            direction_reference_to_native,
                        ],
                        "status": (
                            "PASS"
                            if direction_native_to_reference["status"] == "PASS"
                            and direction_reference_to_native["status"] == "PASS"
                            else "FAIL"
                        ),
                    }
                    artifact["state_fields"] = [
                        "save", "sram_bank_0", "sram_bank_1", "sram_bank_2", "sram_bank_3",
                    ]
                    artifact["events"] = 2
                    if (direction_native_to_reference["status"] == "PASS"
                            and direction_reference_to_native["status"] == "PASS"):
                        artifact["status"] = "PASS"
                        artifact["terminal_event"] = "SAVE_ROUND_TRIP"
                        artifact.pop("failure", None)
                    else:
                        artifact["failure"] = "SAVE_ROUND_TRIP_MISMATCH"
                else:
                    artifact["failure"] = "REFERENCE_COMPARISON_MISSING"
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        artifact["failure"] = "SCENARIO_ERROR"
        artifact["detail"] = str(exc)
    return finish(args.scenario, requirement, artifact)


def finish(scenario: str, requirement: str, artifact: dict[str, Any]) -> int:
    from tools.completion.completion import check_evidence, requirement_by_id, write_evidence_artifact

    write_evidence_artifact(requirement, artifact)
    status, reason = check_evidence(requirement_by_id(requirement))
    output = {
        "status": artifact["status"],
        "scenario": scenario,
        "validation": status,
        **{
            key: artifact[key]
            for key in ("failure", "content_key", "frames", "covered_edges")
            if key in artifact
        },
    }
    if reason:
        output["reason"] = reason
    print(json.dumps(output, sort_keys=True))
    if status == "pass":
        return 0
    if status in {"unavailable", "unsupported"}:
        return 3
    return 2


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools" / "completion"))
    raise SystemExit(main())
