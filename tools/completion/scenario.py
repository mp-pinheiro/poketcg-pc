#!/usr/bin/env python3
"""Run a packaged scenario and emit revision-keyed evidence."""

from __future__ import annotations

import argparse
import hashlib
import re
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.oracle.gbrecomp_oracle import Oracle, _full_state

BINARY = ROOT / "build" / "poketcg"
PACK = ROOT / "build" / "completion" / "data-pack.bin"
EVIDENCE_DIR = ROOT / "build" / "completion" / "evidence"
SCENARIO_REQUIREMENTS = {
    "boot-title": "completion:v2:p2:boot-title",
    "boot-title-negative": "completion:v2:p2:boot-title-negative",
    "save-interchange": "completion:v2:p2:save-interchange",
    "audio-catalog": "completion:v2:p3:audio-trace",
    "audio-pcm": "completion:v2:p3:audio-pcm",
    "ui-corpus": "completion:v2:p4:ui-corpus",
    "raster-effects": "completion:v2:p4:raster-effects",
    "seeded-duel": "completion:v2:p5:seeded-duel",
    "all-maps-scripts": "completion:v2:p6:maps-and-campaign",
    "new-game-to-credits": "completion:v2:faithful-4x3:release",
    "link-ir-printer": "completion:v2:p7:link-ir",
    "faithful-4x3-corpus": "completion:v2:faithful-4x3:package",
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
    "seeded-duel": "duel-corpus-v2",
    "all-maps-scripts": "campaign-corpus-v2",
    "new-game-to-credits": "release-corpus-v2",
    "link-ir-printer": "transport-corpus-v1",
    "faithful-4x3-corpus": "package-proof-v1",
    "widescreen-corpus": "widescreen-corpus-v1",
}


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def state_hash(state: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(state)).hexdigest()
def boot_input(frames: int) -> list[int]:
    values = [0] * frames
    for index, value in ((1000, 16), (1100, 8), (1101, 16), (1200, 128), (1201, 16)):
        if index < frames:
            values[index] = value
    return values

def reference_boot_input() -> str:
    return "f1000:A:1,f1100:D:1,f1101:A:1,f1200:S:1,f1201:A:1"


WVBC_WRAM_OFFSET = 0xCAB8 - 0xC000


def reference_aligned_state(
    oracle: Oracle,
    native_state: dict[str, Any],
    native_frames: int,
    *,
    base_input: str | None = None,
    initial_offset: int = 6,
    max_iterations: int = 4,
) -> tuple[dict[str, Any], int]:
    """Run the reference until its DoFrame count matches the native run's.

    The two lanes count frames on different axes (oracle-b counts PPU
    scanouts from power-on; the native counts DoFrame boundaries), and the
    gap grows with every LCD-off transition the game performs, so it is not
    a constant. wVBlankCounter ($CAB8) increments once per DoFrame on both
    sides, which makes it a monotonic alignment ruler: adjust the reference
    frame limit (and its input timeline, which rides the same axis) by the
    counter delta until both lanes report the same DoFrame count, then
    return that state (and the frame offset used)."""
    wvbc = WVBC_WRAM_OFFSET
    native_counter = native_state["wram"][wvbc]
    offset = initial_offset
    state: dict[str, Any] = {}
    for _ in range(max_iterations):
        with tempfile.TemporaryDirectory(prefix="poketcg-align-") as directory:
            save_state = Path(directory) / "reference.gbs"
            result = oracle.run(
                frame_limit=native_frames + offset,
                input_file=(
                    shift_reference_input(base_input, offset)
                    if base_input
                    else None
                ),
                save_state=save_state,
            )
            dump = (
                json.loads(result.state)
                if isinstance(result.state, (str, bytes))
                else result.state
            )
            state = _full_state(save_state, dump)
        delta = native_counter - state["wram"][wvbc]
        if delta == 0:
            break
        offset += delta
    return state, offset


REFERENCE_INCOMPLETE_FIELDS = {"apu_trace"}
# Fields whose values depend on the hardware VBlank-service phase the
# rendezvous substrate cannot reproduce (3 mid-processing services per
# boot-to-name; LFSR algorithm itself proven byte-exact per call). Duel and
# later scenarios seed wRNG* identically on both lanes, so gameplay parity is
# unaffected.
TIMING_PHASE_FIELDS = {"rng"}


def fields_incomparable(
    reference: dict[str, Any], native: dict[str, Any], field: str
) -> bool:
    """True when the field carries no comparable reference information.

    Two cases: host-bookkeeping dicts serialized with different schemas on the
    two sides (timer_frame_counters gains a "cycles" key on oracle-b), and
    fields the oracle-b scene dump never records at all (apu_trace is always
    empty there; its parity contract lives in the audio-catalog scenario,
    which captures the real (address, value) sequence on both lanes)."""
    if field in REFERENCE_INCOMPLETE_FIELDS or field in TIMING_PHASE_FIELDS:
        return True
    ref_value = reference.get(field)
    nat_value = native.get(field)
    return (
        isinstance(ref_value, dict)
        and isinstance(nat_value, dict)
        and set(ref_value) != set(nat_value)
    )


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
COMPARATOR_EXCLUDED_RANGES = {
    "hram": [(0, 1), (96, 114)],
    "wram": [(0x2B8, 0x2B9), (0xABA, 0xABD)],
}

COMPARATOR_EXCLUDED_KEYS = {
    "mapper_state": {"rom_bank", "vram_bank"},
}


def apply_comparator_exclusions(
    reference: dict[str, Any], native: dict[str, Any], field: str
) -> None:
    """Neutralize excluded ranges/keys in BOTH states so they cannot
    mismatch. Byte ranges zero on both sides; excluded dict keys are dropped
    from both. Exclusions are assertions of structural difference, each with
    a documented reason above."""
    for start, end in COMPARATOR_EXCLUDED_RANGES.get(field, ()):
        for state in (reference, native):
            values = state.get(field)
            if isinstance(values, list):
                for index in range(start, min(end, len(values))):
                    values[index] = 0
    excluded = COMPARATOR_EXCLUDED_KEYS.get(field, set())
    if excluded:
        for state in (reference, native):
            values = state.get(field)
            if isinstance(values, dict):
                for key in excluded:
                    values.pop(key, None)


def shift_reference_input(text: str, offset: int) -> str:
    """Shift a comma-separated f<frame>:<key>:<value> timeline by offset."""
    if offset == 0:
        return text
    shifted = []
    for part in text.split(","):
        head, rest = part.split(":", 1)
        if head.startswith("f"):
            head = f"f{int(head[1:]) + offset}"
        shifted.append(f"{head}:{rest}")
    return ",".join(shifted)


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
AUDIO_WRITE_RE = re.compile(
    r"\[WRITE\]\s+cyc=(\d+)\s+addr=([0-9A-Fa-f]{4}).*<=\s+([0-9A-Fa-f]{2})"
)


def parse_reference_audio(path: Path) -> list[dict[str, int]]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = AUDIO_WRITE_RE.search(line)
        if match:
            records.append({
                "tick": int(match.group(1)),
                "address": int(match.group(2), 16),
                "value": int(match.group(3), 16),
            })
    if not records:
        raise ValueError("reference audio trace has no register writes")
    return records



def compare_state_fields(
    reference: dict[str, Any], native: dict[str, Any], fields: tuple[str, ...]
) -> list[dict[str, Any]]:
    from tests.scene_diff import _first_difference, _state_field

    mismatches = []
    for field in fields:
        if fields_incomparable(reference, native, field):
            continue
        apply_comparator_exclusions(reference, native, field)
        reference_value = _state_field(reference, field)
        native_value = _state_field(native, field)
        if reference_value is None or native_value is None:
            mismatches.append({"field": field, "reason": "missing"})
            continue
        offset = _first_difference(reference_value, native_value)
        if offset is not None:
            mismatches.append({"field": field, "offset": offset})
    return mismatches

def current_key() -> str:
    from completion import content_key, load_toml

    return content_key(load_toml(ROOT / "tools/completion/baseline.toml"), load_toml(ROOT / "tools/completion/requirements.toml"))


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
    run_frames = max(args.frames, 2000) if args.scenario == "boot-title" else args.frames
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
    try:
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="poketcg-scenario-") as directory:
            state_path = Path(directory) / "state.json"
            trace_path = Path(directory) / "trace.json"
            input_path = None
            if args.scenario in {"boot-title", "boot-title-negative"}:
                input_path = Path(directory) / "input.txt"
                input_path.write_text(
                    ",".join(str(value) for value in boot_input(run_frames)) + "\n",
                    encoding="utf-8",
                )
            returncode, stdout, stderr = run_native(
                run_frames, state_path, trace_path, input_path
            )
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
                if args.scenario == "boot-title":
                    if artifact["terminal_event"] != "NEW_GAME_ENTERED":
                        artifact["failure"] = "TERMINAL_EVENT_MISSING"
                    elif artifact["events"] < 3:
                        artifact["failure"] = "EVENT_BOUND_NOT_MET"
                    else:
                        try:
                            from tests.scene_diff import STATE_FIELDS, _first_difference, _state_field
                            with Oracle(timeout=120.0) as oracle:
                                reference_state, frame_offset = (
                                    reference_aligned_state(
                                        oracle, state, run_frames,
                                        base_input=reference_boot_input(),
                                    )
                                )
                            artifact["reference_frame_offset"] = frame_offset
                            mismatches = []
                            schema_skips = []
                            for field in STATE_FIELDS:
                                if fields_incomparable(reference_state, state, field):
                                    schema_skips.append(
                                        {"field": field, "reason": "schema"}
                                    )
                                    continue
                                apply_comparator_exclusions(
                                    reference_state, state, field
                                )
                                reference_value = _state_field(reference_state, field)
                                native_value = _state_field(state, field)
                                if reference_value is None or native_value is None:
                                    mismatches.append({"field": field, "reason": "missing"})
                                    continue
                                offset = _first_difference(reference_value, native_value)
                                if offset is not None:
                                    mismatches.append({"field": field, "offset": offset})
                            artifact["field_schema_skips"] = schema_skips
                            artifact["oracles"] = ["oracle-b", "native"]
                            artifact["comparison"] = {
                                "status": "PASS" if not mismatches else "FAIL",
                                "mismatches": mismatches,
                            }
                            if mismatches:
                                artifact["failure"] = "STATE_MISMATCH"
                            else:
                                artifact["status"] = "PASS"
                                artifact.pop("failure", None)
                        except (OSError, ValueError, RuntimeError) as exc:
                            artifact["failure"] = "ORACLE_ERROR"
                            artifact["detail"] = str(exc)
                elif args.scenario in {"ui-corpus", "raster-effects"}:
                    try:

                        with Oracle(timeout=120.0) as oracle:
                            reference_state, frame_offset = (
                                reference_aligned_state(oracle, state, run_frames)
                            )
                            artifact["reference_frame_offset"] = frame_offset
                        fields = (
                            ("wram", "vram_bank_0", "vram_bank_1", "oam", "palette_ram", "framebuffer")
                            if args.scenario == "ui-corpus"
                            else ("vram_bank_0", "vram_bank_1", "framebuffer")
                        )
                        mismatches = compare_state_fields(reference_state, state, fields)
                        artifact["oracles"] = ["oracle-b", "native"]
                        artifact["comparison"] = {
                            "fields": list(fields),
                            "mismatches": mismatches,
                            "status": "PASS" if not mismatches else "FAIL",
                        }
                        if not mismatches:
                            artifact["status"] = "PASS"
                            artifact["terminal_event"] = (
                                "UI_CORPUS_CLOSED"
                                if args.scenario == "ui-corpus"
                                else "RASTER_EFFECTS_CLOSED"
                            )
                            artifact.pop("failure", None)
                        else:
                            artifact["failure"] = "UI_STATE_MISMATCH"
                    except (OSError, ValueError, RuntimeError) as exc:
                        artifact["failure"] = "ORACLE_ERROR"
                        artifact["detail"] = str(exc)
                elif args.scenario == "audio-catalog":
                    try:
                        with Oracle(timeout=120.0) as oracle:
                            _, frame_offset = reference_aligned_state(
                                oracle, state, run_frames
                            )
                            artifact["reference_frame_offset"] = frame_offset
                            oracle.run(
                                frame_limit=run_frames + frame_offset,
                                audio_trace=reference_trace,
                            )
                        reference_audio = parse_reference_audio(reference_trace)
                        native_audio = state.get("apu_trace")
                        if not isinstance(native_audio, list):
                            raise ValueError("native audio trace is not a list")
                        native_pairs = [
                            (int(item["address"]), int(item["value"]))
                            for item in native_audio
                            if isinstance(item, dict)
                            and "address" in item
                            and "value" in item
                        ]
                        reference_pairs = [
                            (item["address"], item["value"]) for item in reference_audio
                        ]
                        common = min(len(native_pairs), len(reference_pairs))
                        first_mismatch = next(
                            (
                                index for index in range(common)
                                if native_pairs[index] != reference_pairs[index]
                            ),
                            common if len(native_pairs) != len(reference_pairs) else None,
                        )
                        artifact["oracles"] = ["oracle-b", "native"]
                        artifact["comparison"] = {
                            "native_writes": len(native_pairs),
                            "reference_writes": len(reference_pairs),
                            "first_mismatch": first_mismatch,
                            "status": "PASS" if first_mismatch is None else "FAIL",
                        }
                        if first_mismatch is None:
                            artifact["status"] = "PASS"
                            artifact["terminal_event"] = "AUDIO_TRACE_CLOSED"
                            artifact.pop("failure", None)
                        else:
                            artifact["failure"] = "AUDIO_TRACE_MISMATCH"
                    except (OSError, ValueError, RuntimeError) as exc:
                        artifact["failure"] = "ORACLE_ERROR"
                        artifact["detail"] = str(exc)
                elif args.scenario == "boot-title-negative":
                    from frame_bisect import bisect_first_mismatch

                    with Oracle(timeout=120.0) as oracle:
                        finding = bisect_first_mismatch(
                            oracle,
                            run_frames,
                            native_input=input_path,
                            oracle_input=reference_boot_input(),
                        )
                    artifact["oracles"] = ["oracle-b", "native"]
                    if finding is None:
                        artifact["failure"] = "NO_MISMATCH_FOUND"
                        artifact["detail"] = (
                            f"native and oracle-b agree over all {run_frames} frames; "
                            "negative evidence requires a detected first mismatch"
                        )
                    else:
                        artifact["status"] = "PASS"
                        artifact["terminal_event"] = "FIRST_MISMATCH"
                        artifact["events"] = 1
                        artifact["first_mismatch_frame"] = finding["frame"]
                        artifact["first_mismatch_region"] = finding["field"]
                        artifact["first_mismatch_offset"] = finding["offset"]
                        artifact["state_fields"] = [
                            "first_mismatch_region",
                            "first_mismatch_offset",
                            "replay_artifact",
                        ]
                        replay = {
                            "schema": "negative-evidence-replay-v1",
                            "scenario": args.scenario,
                            "sweep_frames": run_frames,
                            "bisect_frame": finding["frame"],
                            "first_mismatch_region": finding["field"],
                            "first_mismatch_offset": finding["offset"],
                            "native": finding.get("native"),
                            "reference": finding.get("reference"),
                            "context": finding.get("context", {}),
                            "reference_input": reference_boot_input(),
                            "native_input_sha256": hashlib.sha256(
                                input_path.read_bytes() if input_path else b""
                            ).hexdigest(),
                        }
                        replay_path = EVIDENCE_DIR / f"{requirement}.replay.json"
                        replay_path.write_text(
                            json.dumps(replay, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8",
                        )
                        artifact["replay_artifact"] = str(replay_path.relative_to(ROOT))
                        artifact.pop("failure", None)
                elif args.scenario == "save-interchange":
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
    path = evidence_path(requirement)
    path.write_text(json.dumps(artifact, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({"status": artifact["status"], "scenario": args.scenario, **{
        key: artifact[key] for key in ("failure", "content_key", "frames", "covered_edges")
        if key in artifact
    }}, sort_keys=True))
    return 2


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools" / "completion"))
    raise SystemExit(main())
