#!/usr/bin/env python3
"""Requirement evidence from recorded sessions on the DoFrame axis.

The reference (Gambatte) and the port replay one session; the masked digest
stream must match at every anchor (session.verify), then sampled anchors are
compared byte for byte across the requirement's representation fields.
"""

from __future__ import annotations

import hashlib
import json
import struct
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import session

ROOT = session.ROOT
FRAME_PIXELS = 160 * 144
EVENT_NAMES = {
    1: "BOOT_STARTED",
    2: "TITLE_READY",
    3: "START_MENU_READY",
    4: "NEW_GAME_ENTERED",
    5: "OVERWORLD_READY",
}
IO_COMPARED = (
    0x00, 0x01, 0x02, 0x06, 0x07,
    0x40, 0x42, 0x43, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4D, 0x4F,
    0x51, 0x52, 0x53, 0x54, 0x55, 0x56,
    0x68, 0x6A, 0x70,
)
APU_FIRST, APU_LAST = 0xFF10, 0xFF3F
APU_READBACK = {
    0xFF10: (0x80, 0xFF), 0xFF11: (0x3F, 0xFF), 0xFF12: (0x00, 0xFF), 0xFF13: (0xFF, 0x00),
    0xFF14: (0xBF, 0x40), 0xFF15: (0xFF, 0x00), 0xFF16: (0x3F, 0xFF), 0xFF17: (0x00, 0xFF),
    0xFF18: (0xFF, 0x00), 0xFF19: (0xBF, 0x40), 0xFF1A: (0x7F, 0xFF), 0xFF1B: (0xFF, 0x00),
    0xFF1C: (0x9F, 0xFF), 0xFF1D: (0xFF, 0x00), 0xFF1E: (0xBF, 0x40), 0xFF1F: (0xFF, 0x00),
    0xFF20: (0xFF, 0x00), 0xFF21: (0x00, 0xFF), 0xFF22: (0x00, 0xFF), 0xFF23: (0xBF, 0x40),
    0xFF24: (0x00, 0xFF), 0xFF25: (0x00, 0xFF), 0xFF26: (0x70, 0x80),
}
NR52 = 0xFF26
BOOT_ROM_PCS = ((0x0000, 0x0100), (0x0200, 0x0900))


@dataclass(frozen=True)
class Spec:
    sessions: tuple[str, ...]
    fields: tuple[str, ...]
    terminal: str
    event: str | None = None
    samples: int = 24


SPECS: dict[str, Spec] = {
    "boot-title": Spec(
        sessions=("boot-menu",),
        fields=(
            "wram", "hram", "vram_bank_0", "vram_bank_1", "oam", "io", "palette_ram",
            "framebuffer", "input_latch", "timer_frame_counters",
        ),
        terminal="NEW_GAME_ENTERED",
        event="NEW_GAME_ENTERED",
    ),
    "ui-corpus": Spec(
        sessions=("boot-deck-machine", "practice-win"),
        fields=("wram", "vram_bank_0", "vram_bank_1", "oam", "palette_ram", "framebuffer"),
        terminal="UI_CORPUS_CLOSED",
    ),
    "raster-effects": Spec(
        sessions=("effect-gastly-lv17-2-board",),
        fields=("framebuffer", "vram_bank_0", "vram_bank_1"),
        terminal="RASTER_EFFECTS_CLOSED",
    ),
    "audio-catalog": Spec(
        sessions=("boot-menu", "seed-deck-machines", "challenge-machine"),
        fields=("apu_state", "apu_trace", "timer_frame_counters"),
        terminal="AUDIO_TRACE_CLOSED",
    ),
}


class WitnessError(RuntimeError):
    pass


def apu_readback(address: int, value: int) -> int:
    if address >= 0xFF27 and address <= 0xFF2F:
        return 0xFF
    if address >= 0xFF30:
        return value
    fixed, keep = APU_READBACK[address]
    return fixed | (value & keep)


def in_boot_rom(pc: int) -> bool:
    return any(start <= pc < end for start, end in BOOT_ROM_PCS)


def sample_anchors(count: int, samples: int) -> list[int]:
    chosen = {max(1, round(index * count / samples)) for index in range(1, samples + 1)}
    chosen.add(count)
    return sorted(chosen)


def verify_report(name: str) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"witness-{name}-") as directory:
        json_path = Path(directory) / "verify.json"
        session.verify(name, write=False, json_path=json_path, publish=False)
        return json.loads(json_path.read_text(encoding="utf-8"))


def reference_pass(
    name: str,
    masks: list[int],
    meta: dict[str, Any],
    frames: int,
    anchors: list[int],
    *,
    want_frames: bool,
    want_apu: bool,
    want_save: bool,
) -> dict[str, Any]:
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    count = anchors[-1]
    wanted = set(anchors)
    captured: dict[int, dict[str, Any]] = {}
    stable: dict[int, bool] = {}
    apu_writes: list[tuple[int, int, int]] = []
    with refstream.Core(padded, pokes=meta["pokes"], save=meta["save"]) as core:
        core.input_axis = "ordinal"
        hits = 0
        last_frame = b""
        pending: int | None = None
        read = core.library.gambatte_cpuread
        handle = core.core

        def on_write(address: int, _cycle: int) -> None:
            if APU_FIRST <= address <= APU_LAST and hits < count and not in_boot_rom(core.pc()):
                apu_writes.append((hits, address, read(handle, address)))

        def on_exec(address: int, _cycle: int) -> None:
            nonlocal hits, last_frame, pending
            if address != refstream.DOFRAME_ANCHOR:
                return
            hits += 1
            if want_frames:
                frame = bytes(core._framebuffer)
                if pending is not None:
                    stable[pending] = stable.get(pending, False) and frame == captured[pending]["framebuffer"]
                    pending = None
                if hits in wanted:
                    stable[hits] = frame == last_frame
                    pending = hits
                last_frame = frame
            if hits in wanted:
                record = session.reference_regions(core)
                record["io"] = core.io_block()
                record["palette_ram"] = core.palette_block()
                if want_frames:
                    record["framebuffer"] = last_frame
                if want_save and hits == count:
                    record["save"] = core.area("CartRAM")[:0x8000]
                captured[hits] = record

        if want_apu:
            core.on_write(on_write)
        core.install_exec(on_exec)
        core.run(frames, stop=lambda: hits > count)
        if pending is not None:
            stable[pending] = False
    if len(captured) != len(wanted):
        raise WitnessError(f"reference reached {len(captured)} of {len(wanted)} anchors for {name}")
    return {"anchors": captured, "stable": stable, "apu_writes": apu_writes}


def native_pass(name: str, count: int, anchors: list[int], lag_path: Path, directory: Path) -> dict[int, dict[str, Any]]:
    state_path, failure, _off = session.run_native(
        directory, session.session_dir(name) / "input.txt", count, lag_path=lag_path, dump_ordinals=anchors
    )
    dumps: dict[int, dict[str, Any]] = {}
    for ordinal in anchors:
        dump_path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
        if not dump_path.is_file():
            raise WitnessError(f"native dump missing at ordinal {ordinal} for {name}: {failure[-300:]}")
        dumps[ordinal] = json.loads(dump_path.read_text(encoding="utf-8"))
    return dumps


def count_diff(left: bytes, right: bytes) -> int:
    if len(left) != len(right):
        return max(len(left), len(right))
    return sum(1 for a, b in zip(left, right) if a != b)


def compare_anchor(
    field: str,
    ordinal: int,
    native: dict[str, Any],
    reference: dict[str, Any],
    stable: bool,
    tables: dict[str, bytes],
    masks: list[int],
) -> int | None:
    if field in {"wram", "hram", "oam"}:
        return count_diff(
            session.masked(bytes(native[field]), tables[field]),
            session.masked(reference[field], tables[field]),
        )
    if field in {"vram_bank_0", "vram_bank_1"}:
        half = 0x2000 if field.endswith("1") else 0
        table = tables["vram"][half : half + 0x2000]
        return count_diff(
            session.masked(bytes(native[field]), table),
            session.masked(reference["vram"][half : half + 0x2000], table),
        )
    if field == "palette_ram":
        return count_diff(bytes(native["palette_ram"]), reference["palette_ram"])
    if field == "io":
        readback = native["io_readback"]
        return sum(1 for offset in IO_COMPARED if readback[offset] != reference["io"][offset])
    if field == "framebuffer":
        if not stable:
            return None
        pixels = struct.unpack(f"<{FRAME_PIXELS}I", reference["framebuffer"])
        return sum(1 for a, b in zip(native["framebuffer"], pixels) if (a & 0x7FFF) != (b & 0x7FFF))
    if field == "input_latch":
        expected = masks[ordinal - 1] if ordinal - 1 < len(masks) else 0
        return int(native["input_latch"] != expected)
    if field == "rng":
        return count_diff(bytes(native["rng"]), reference["wram"][0xABA:0xABD])
    if field in {"save", "sram_bank_0", "sram_bank_1", "sram_bank_2", "sram_bank_3"}:
        if "save" not in reference:
            return None
        if field == "save":
            return count_diff(bytes(native["save"]), reference["save"])
        bank = int(field[-1])
        return count_diff(bytes(native[field]), reference["save"][bank * 0x2000 : (bank + 1) * 0x2000])
    if field == "apu_state":
        readback = native["io_readback"]
        return sum(
            1
            for address in range(APU_FIRST, 0xFF30)
            if (readback[address - 0xFF00] & (0xF0 if address == NR52 else 0xFF))
            != (reference["io"][address - 0xFF00] & (0xF0 if address == NR52 else 0xFF))
        )
    return None


def compare_apu_trace(native_dump: dict[str, Any], reference_writes: list[tuple[int, int, int]]) -> dict[str, Any]:
    native_writes = [(int(row["address"]), int(row["value"])) for row in native_dump["apu_trace"]]
    common = min(len(native_writes), len(reference_writes))
    first = None
    for index in range(common):
        address, value = native_writes[index]
        _ordinal, ref_address, ref_readback = reference_writes[index]
        if address != ref_address:
            first = index
            break
        want = apu_readback(address, value)
        if address == NR52:
            want &= 0xF0
            ref_readback &= 0xF0
        if want != ref_readback:
            first = index
            break
    if first is None and len(native_writes) != len(reference_writes):
        first = common
    return {
        "native_writes": len(native_writes),
        "reference_writes": len(reference_writes),
        "first_mismatch": first,
        "status": "PASS" if first is None else "FAIL",
    }


def event_names(mask: int) -> list[str]:
    return [name for value, name in EVENT_NAMES.items() if mask & (1 << value)]


def witness_session(name: str, spec: Spec) -> dict[str, Any]:
    masks, meta = session.load_session(name)
    count = len(masks)
    frames = session.reference_frames(masks, meta)
    report = verify_report(name)
    row: dict[str, Any] = {
        "name": name,
        "ordinals": count,
        "verify": {
            key: report.get(key)
            for key in ("status", "confirmed", "reached", "schedule_mismatches", "audio_first_divergence")
        },
    }
    if report.get("divergence"):
        row["divergence"] = {key: report["divergence"].get(key) for key in ("ordinal", "regions")}
    if (
        report.get("status") != "clean"
        or report.get("confirmed") != count
        or report.get("schedule_mismatches")
        or report.get("audio_first_divergence") is not None
    ):
        row["status"] = "FAIL"
        return row
    anchors = sample_anchors(count, spec.samples)
    fields = set(spec.fields)
    want_frames = "framebuffer" in fields
    want_apu = bool(fields & {"apu_trace", "apu_state"})
    want_save = bool(fields & {"save", "sram_bank_0", "sram_bank_1", "sram_bank_2", "sram_bank_3"})
    reference = reference_pass(
        name, masks, meta, frames, anchors,
        want_frames=want_frames, want_apu=want_apu, want_save=want_save,
    )
    ref_meta = session.build_reference(name, masks, frames, pokes=meta["pokes"], save=meta["save"])
    lag_path = ROOT / ref_meta["directory"] / "lag.txt"
    with tempfile.TemporaryDirectory(prefix=f"witness-native-{name}-") as directory:
        native = native_pass(name, count, anchors, lag_path, Path(directory))
    tables = session.mask_tables()
    census: dict[str, dict[str, int]] = {}
    failures: list[str] = []
    for field in spec.fields:
        if field in {"timer_frame_counters", "apu_trace"}:
            continue
        compared = 0
        differing = 0
        for ordinal in anchors:
            diff = compare_anchor(
                field, ordinal, native[ordinal], reference["anchors"][ordinal],
                reference["stable"].get(ordinal, False), tables, masks,
            )
            if diff is None:
                continue
            compared += 1
            differing += diff
        census[field] = {"anchors": compared, "differing": differing}
        if compared == 0 or differing:
            failures.append(f"{field}: {differing} differing over {compared} anchors")
    if "timer_frame_counters" in fields:
        census["timer_frame_counters"] = {
            "anchors": count,
            "differing": int(report.get("schedule_mismatches") or 0),
        }
    if "apu_trace" in fields:
        apu = compare_apu_trace(native[count], reference["apu_writes"])
        row["apu_trace"] = apu
        census["apu_trace"] = {"anchors": apu["reference_writes"], "differing": 0 if apu["status"] == "PASS" else 1}
        if apu["status"] != "PASS":
            failures.append(f"apu_trace: first mismatch at write {apu['first_mismatch']}")
    runtime = native[count].get("runtime", {})
    observed = event_names(int(runtime.get("event_mask", 0)))
    row["events"] = {"count": int(runtime.get("events", 0)), "observed": observed}
    row["frames"] = int(runtime.get("frames", 0))
    if spec.event and spec.event not in observed:
        failures.append(f"native never marked {spec.event}")
    row["anchors"] = anchors
    row["census"] = census
    row["status"] = "PASS" if not failures else "FAIL"
    if failures:
        row["failures"] = failures
    return row


def corpus_entry(name: str) -> dict[str, str]:
    directory = session.session_dir(name)
    entry = {
        "session": name,
        "input": str((directory / "input.txt").relative_to(ROOT)),
        "path": str((directory / "session.json").relative_to(ROOT)),
    }
    for key, file_name in (("pokes", "pokes.txt"), ("save", session.SAVE_FILE)):
        if (directory / file_name).is_file():
            entry[key] = str((directory / file_name).relative_to(ROOT))
    return entry


def corpus_for(sessions: tuple[str, ...]) -> list[dict[str, str]]:
    return [corpus_entry(name) for name in sessions]


def corpus(scenario: str) -> list[dict[str, str]]:
    return corpus_for(SPECS[scenario].sessions)


def run(scenario: str) -> dict[str, Any]:
    spec = SPECS[scenario]
    rows = [witness_session(name, spec) for name in spec.sessions]
    passed = all(row["status"] == "PASS" for row in rows)
    fragment: dict[str, Any] = {
        "oracles": ["gambatte", "native"],
        "state_fields": list(spec.fields),
        "frames": sum(row.get("frames", 0) for row in rows),
        "events": sum(row.get("events", {}).get("count", 0) for row in rows),
        "comparison": {
            "status": "PASS" if passed else "FAIL",
            "axis": "doframe-ordinal",
            "sessions": rows,
        },
        "session_sha256": hashlib.sha256(
            json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
    }
    if passed:
        fragment["status"] = "PASS"
        fragment["terminal_event"] = spec.terminal
    else:
        fragment["status"] = "FAIL"
        fragment["failure"] = "SESSION_WITNESS_MISMATCH"
        fragment["detail"] = "; ".join(
            f"{row['name']}: " + "; ".join(row.get("failures") or [json.dumps(row.get("verify"))])
            for row in rows
            if row["status"] != "PASS"
        )
    return fragment


NEGATIVES: dict[str, tuple[str, int, int]] = {
    "boot-title-negative": ("boot-menu", 600, 0x01),
}


def first_mismatch(native: dict[str, bytes], reference: dict[str, bytes]) -> dict[str, Any] | None:
    tables = session.mask_tables()
    for region in session.REGIONS[: session.GATED]:
        table = tables[region]
        left, right = native[region], reference[region]
        for offset in range(min(len(left), len(right))):
            if table[offset] or left[offset] == right[offset]:
                continue
            field, field_offset = session.region_field(region, offset)
            symbol, _base = refstream.resolve_region(field, field_offset)
            return {
                "field": field,
                "offset": field_offset,
                "symbol": symbol,
                "native": left[offset],
                "reference": right[offset],
            }
    return None


def negative(scenario: str, evidence_dir: Path, requirement: str) -> dict[str, Any]:
    name, at, bits = NEGATIVES[scenario]
    masks, meta = session.load_session(name)
    count = len(masks)
    frames = session.reference_frames(masks, meta)
    ref_meta = session.build_reference(name, masks, frames, pokes=meta["pokes"], save=meta["save"])
    reference = session.load_reference(ref_meta)
    lag_path = ROOT / ref_meta["directory"] / "lag.txt"
    perturbed = list(masks)
    for ordinal in range(at - 1, min(count, at + 7)):
        perturbed[ordinal] |= bits
    fragment: dict[str, Any] = {
        "oracles": ["gambatte", "native"],
        "state_fields": ["first_mismatch_region", "first_mismatch_offset", "replay_artifact"],
        "frames": count,
        "events": 0,
        "status": "FAIL",
    }
    with tempfile.TemporaryDirectory(prefix=f"witness-negative-{name}-") as directory:
        lane = Path(directory)
        input_path = lane / "input.txt"
        input_path.write_text("\n".join(str(value) for value in perturbed) + "\n", encoding="utf-8")
        for file_name in ("pokes.txt", session.SAVE_FILE):
            source = session.session_dir(name) / file_name
            if source.is_file():
                (lane / file_name).write_bytes(source.read_bytes())
        mask_path = lane / "mask.txt"
        mask_path.write_text(session.mask_text())
        digest_path = lane / "native.bin"
        _state, failure, _off = session.run_native(
            lane, input_path, count, lag_path=lag_path, digest_out=digest_path, mask_path=mask_path
        )
        native_digests = digest_path.read_bytes() if digest_path.is_file() else b""
        ordinal, reached, regions, _audio = session.first_divergence(reference, native_digests)
        if ordinal is None:
            fragment["failure"] = "NO_MISMATCH_FOUND"
            fragment["detail"] = (
                f"perturbing {name} at ordinal {at} left {reached} ordinals byte-identical: {failure[-200:]}"
            )
            return fragment
        capture = lane / "capture"
        capture.mkdir()
        state_path, capture_failure, _off = session.run_native(
            capture, input_path, ordinal, lag_path=lag_path, dump_ordinals=[ordinal]
        )
        dump_path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
        if not dump_path.is_file():
            raise WitnessError(f"no native dump at ordinal {ordinal}: {capture_failure[-300:]}")
        native_state = session.native_regions(json.loads(dump_path.read_text(encoding="utf-8")))
        digest = hashlib.sha256(input_path.read_bytes()).hexdigest()
    reference_state = session.reference_capture(name, masks, frames, ordinal, meta["pokes"], save=meta["save"])
    finding = first_mismatch(native_state, reference_state)
    if finding is None:
        fragment["failure"] = "MISMATCH_UNATTRIBUTED"
        fragment["detail"] = f"digests diverge at ordinal {ordinal} in {regions} but no compared byte differs"
        return fragment
    replay = {
        "schema": "negative-evidence-replay-v1",
        "scenario": scenario,
        "session": name,
        "perturbation": {"ordinal": at, "ordinals": 8, "mask_bits": bits},
        "native_input_sha256": digest,
        "first_mismatch_ordinal": ordinal,
        "regions": regions,
        "finding": finding,
    }
    replay_path = evidence_dir / f"{requirement}.replay.json"
    replay_path.write_text(json.dumps(replay, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    fragment.update(
        {
            "status": "PASS",
            "terminal_event": "FIRST_MISMATCH",
            "events": 1,
            "comparison": {"status": "PASS", "kind": "first-mismatch", "regions": regions},
            "first_mismatch_frame": ordinal,
            "first_mismatch_region": finding["field"],
            "first_mismatch_offset": finding["offset"],
            "first_mismatch_symbol": finding["symbol"],
            "replay_artifact": str(replay_path.relative_to(ROOT)),
        }
    )
    return fragment
