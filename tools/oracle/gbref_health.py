#!/usr/bin/env python3
"""Run the shared register, memory, and MBC5 conformance vectors."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from conformance_rom import (
    CYCLE_COUNT, ENTRY, INSTRUCTION_COUNT, PRE_RET_PC, SRAM_BANK0_VALUE,
    SRAM_BANK3_VALUE, SRAM_TRACE_ADDRESS, TRACE_ADDRESS, TRACE_BYTES,
    WRAM_HEALTH_ADDR, build_rom,
)

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tools/oracle/gbref/build/gbref_runner"
REAL_ROM = ROOT / "poketcg" / "poketcg.gbc"
COPY_RET_ANCHORS = (("CopyGfxData", 0x0731), ("CopyDataHLtoDE", 0x0744))
RESET_ANIMATION_ENTRY = 0x48BC
RESET_ANIMATION_QUEUE = 0xD423
RESET_ANIMATION_STATE = 0xD4AC
PROBE = ROOT / "build-barrier/poketcg_probe"


def unhealthy(label: str, expected: object, actual: object) -> int:
    print(f"BACKEND_UNHEALTHY {label} expected={expected!r} actual={actual!r}")
    return 2


def final_json(output: str) -> dict[str, object] | None:
    for line in reversed(output.splitlines()):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return None


def run_runner(rom: Path, request: dict[str, object]) -> tuple[dict[str, object] | None, str]:
    result = subprocess.run([str(RUNNER), "--rom", str(rom)], input=json.dumps(request),
                            text=True, capture_output=True, check=False)
    return final_json(result.stdout), result.stderr or result.stdout


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        rom = Path(directory) / "conformance.gb"
        rom.write_bytes(build_rom())
        base = {"entry": ENTRY, "instruction_budget": 200, "cycle_budget": 2000,
                "rom_bank": 1, "ram_bank": 0, "ram_enable": 0,
                "a": 0, "f": 0, "b": 0, "c": 0, "d": 0, "e": 0, "hl": 0}
        payload, diagnostic = run_runner(rom, {**base, "completion": "return"})
        if payload is None:
            return unhealthy("gbrt invalid result", {"status": "REFERENCE_OK"}, diagnostic)
        expected_registers = {"af": 0x5500, "bc": 0xBBCC, "de": 0xDDEE, "hl": 0x1234}
        actual_registers = {key: payload.get(key) for key in expected_registers}
        if payload.get("status") != "REFERENCE_OK" or actual_registers != expected_registers:
            return unhealthy("registers", expected_registers, actual_registers)
        if (payload.get("pc") != 0xFEA0 or payload.get("sp") != 0xFFFE or
                payload.get("completion") != "return"):
            return unhealthy("calls/stack", {"completion": "return", "pc": 0xFEA0, "sp": 0xFFFE},
                             {key: payload.get(key) for key in ("completion", "pc", "sp")})
        return_actual = {"instructions": payload.get("instructions"),
                         "cycles": payload.get("cycles")}
        return_expected = {"instructions": INSTRUCTION_COUNT + 1,
                           "cycles": CYCLE_COUNT + 16}
        if (not isinstance(return_actual["instructions"], int) or
                return_actual["instructions"] != INSTRUCTION_COUNT + 1 or
                not isinstance(return_actual["cycles"], int) or
                return_actual["cycles"] != CYCLE_COUNT + 16):
            return unhealthy("return", return_expected, return_actual)
        try:
            wram = bytes.fromhex(str(payload.get("wram", "")))
            hram = bytes.fromhex(str(payload.get("hram", "")))
            sram = bytes.fromhex(str(payload.get("sram", "")))
        except ValueError:
            return unhealthy("wram/hram/mbc5-ram", "hex state", payload)
        wram_health_offset = WRAM_HEALTH_ADDR - TRACE_ADDRESS
        if (len(wram) < max(len(TRACE_BYTES), wram_health_offset + 1) or
                len(hram) < 1 or len(sram) < 4 * 0x2000):
            return unhealthy("wram/hram/mbc5-ram", "complete state buffers",
                             {"wram": len(wram), "hram": len(hram), "sram": len(sram)})
        wram_health = wram[wram_health_offset:wram_health_offset + 1]
        hram_health = hram[:1]
        if wram_health != b"\x55" or hram_health != b"\x55":
            return unhealthy("wram/hram", {"wram": "55", "hram": "55"},
                             {"wram": wram_health.hex(), "hram": hram_health.hex()})
        trace = wram[:len(TRACE_BYTES)]
        expected_mbc = {"trace": TRACE_BYTES.hex(), "sram0": f"{SRAM_BANK0_VALUE:02x}",
                        "sram3": f"{SRAM_BANK3_VALUE:02x}"}
        actual_mbc = {"trace": trace.hex(),
                      "sram0": sram[SRAM_TRACE_ADDRESS - 0xA000:SRAM_TRACE_ADDRESS - 0xA000 + 1].hex(),
                      "sram3": sram[3 * 0x2000 + SRAM_TRACE_ADDRESS - 0xA000:
                                    3 * 0x2000 + SRAM_TRACE_ADDRESS - 0xA000 + 1].hex()}
        if actual_mbc != expected_mbc:
            return unhealthy("mbc5-rom/mbc5-ram", expected_mbc, actual_mbc)
        expected_latches = {"rom_bank": 5, "ram_bank": 0, "ram_enable": 0}
        actual_latches = {key: payload.get(key) for key in expected_latches}
        if actual_latches != expected_latches:
            return unhealthy("latches", expected_latches, actual_latches)
        raw_expected = {"rom_bank_low": 0x45, "rom_bank_upper": 1,
                        "fixed_rom_bank": 0, "switch_rom_bank": 5}
        raw_actual = {key: payload.get(key) for key in raw_expected}
        if raw_actual != raw_expected:
            return unhealthy("raw-diagnostics", raw_expected, raw_actual)

        pre, diagnostic = run_runner(rom, {**base, "completion": "pre-ret", "stop_pc": PRE_RET_PC})
        if pre is None:
            return unhealthy("pre-ret", {"pc": PRE_RET_PC}, diagnostic)
        pre_actual = {"pc": pre.get("pc"), "sp": pre.get("sp"),
                      "instructions": pre.get("instructions"), "cycles": pre.get("cycles")}
        pre_expected = {"pc": PRE_RET_PC, "sp": 0xFFFC,
                        "instructions": INSTRUCTION_COUNT, "cycles": CYCLE_COUNT}
        if (pre_actual["pc"] != PRE_RET_PC or pre_actual["sp"] != 0xFFFC or
                pre_actual["instructions"] != INSTRUCTION_COUNT or
                not isinstance(pre_actual["cycles"], int) or
                pre_actual["cycles"] != CYCLE_COUNT):
            return unhealthy("pre-ret", pre_expected, pre_actual)


        if not REAL_ROM.is_file():
            return unhealthy("copy-ret-anchors rom", "poketcg.gbc", str(REAL_ROM))
        try:
            real_rom = REAL_ROM.read_bytes()
        except OSError as error:
            return unhealthy("copy-ret-anchors rom", "readable poketcg.gbc", str(error))
        for label, anchor in COPY_RET_ANCHORS:
            if anchor >= len(real_rom):
                return unhealthy(f"copy-ret-anchors {label}", "ROM byte C9",
                                 {"address": anchor, "rom_size": len(real_rom)})
            if real_rom[anchor] != 0xC9:
                return unhealthy(f"copy-ret-anchors {label}", "ROM byte C9",
                                 {"address": anchor, "byte": real_rom[anchor]})
            copy_ret, diagnostic = run_runner(
                REAL_ROM, {"entry": anchor, "instruction_budget": 1, "cycle_budget": 1,
                           "completion": "pre-ret", "stop_pc": anchor,
                           "mapper_mode": "reset"})
            copy_expected = {"status": "REFERENCE_OK", "pc": anchor, "sp": 0xFFFC,
                             "instructions": 0, "cycles": 0}
            copy_actual = ({key: copy_ret.get(key) for key in copy_expected}
                           if copy_ret is not None else diagnostic)
            if (copy_ret is None or copy_ret.get("status") != "REFERENCE_OK" or
                    any(type(copy_ret.get(key)) is not int or copy_ret[key] != value
                        for key, value in copy_expected.items() if key != "status")):
                return unhealthy(f"copy-ret-anchors {label}", copy_expected, copy_actual)

        setup_entry = PRE_RET_PC
        ambush = {
            "setup": [{
                "entry": setup_entry,
                "rom_bank": 7, "ram_bank": 3, "ram_enable": 1,
                "a": 0xFF, "f": 0xF0, "b": 0xEE, "c": 0xDD,
                "d": 0xCC, "e": 0xBB, "hl": 0xAA,
            }],
            **base,
            "completion": "return",
        }
        parsed, diagnostic = run_runner(rom, ambush)
        if parsed is None:
            return unhealthy("top-level-keys", {"status": "REFERENCE_OK"}, diagnostic)
        try:
            tls_wram = bytes.fromhex(str(parsed.get("wram", "")))
            tls_sram = bytes.fromhex(str(parsed.get("sram", "")))
        except ValueError:
            return unhealthy("top-level-keys", "hex state", parsed)
        tls_trace = tls_wram[:len(TRACE_BYTES)]
        if tls_trace != TRACE_BYTES:
            return unhealthy("top-level-keys mapper", {"trace": TRACE_BYTES.hex()},
                             {"trace": tls_trace.hex()})
        tls_sram0 = tls_sram[SRAM_TRACE_ADDRESS - 0xA000:SRAM_TRACE_ADDRESS - 0xA000 + 1]
        tls_sram3 = tls_sram[3 * 0x2000 + SRAM_TRACE_ADDRESS - 0xA000:
                             3 * 0x2000 + SRAM_TRACE_ADDRESS - 0xA000 + 1]
        expected_top_sram = {"sram0": f"{SRAM_BANK0_VALUE:02x}", "sram3": f"{SRAM_BANK3_VALUE:02x}"}
        if tls_sram0.hex() != expected_top_sram["sram0"] or tls_sram3.hex() != expected_top_sram["sram3"]:
            return unhealthy("top-level-keys sram", expected_top_sram,
                             {"sram0": tls_sram0.hex(), "sram3": tls_sram3.hex()})
        top_latches = {key: parsed.get(key) for key in expected_latches}
        if top_latches != expected_latches:
            return unhealthy("top-level-keys latches", expected_latches, top_latches)

        reset_animation, diagnostic = run_runner(
            REAL_ROM, {
                "entry": RESET_ANIMATION_ENTRY, "instruction_budget": 1000,
                "cycle_budget": 10000, "rom_bank": 7, "ram_bank": 0,
                "ram_enable": 0, "completion": "return",
                "a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
                "d": 0xDD, "e": 0xEE, "hl": 0x1234,
                "seed_wram": (
                    f"{RESET_ANIMATION_QUEUE:04x}=" + "01" * 7 + ";"
                    f"{RESET_ANIMATION_STATE:04x}=aabbcc"
                ),
            })
        reset_expected = {
            "status": "REFERENCE_OK", "completion": "return",
            "pc": 0xFEA0, "sp": 0xFFFE, "bc": 0xBBCC, "hl": 0x1234,
        }
        reset_actual = ({key: reset_animation.get(key) for key in reset_expected}
                        if reset_animation is not None else diagnostic)
        if (reset_animation is None or
                not all(type(reset_animation.get(key)) is type(value)
                        for key, value in reset_expected.items()
                        if key not in ("status", "completion")) or
                any(reset_animation.get(key) != value
                    for key, value in reset_expected.items())):
            return unhealthy("reset-animation", reset_expected, reset_actual)

        if not PROBE.is_file():
            return unhealthy("native probe", "MBC5ConformanceVector", str(PROBE))
        native_env = os.environ.copy()
        native_env["POKETCG_ROM"] = str(rom.resolve())
        native_result = subprocess.run(
            [str(PROBE)], input=json.dumps({"fn": "MBC5ConformanceVector",
                "read": {str(TRACE_ADDRESS): len(TRACE_BYTES)},
                "sread": {"0": {str(SRAM_TRACE_ADDRESS): 1}, "3": {str(SRAM_TRACE_ADDRESS): 1}}}),
            text=True, capture_output=True, check=False, timeout=30, env=native_env)
        native = final_json(native_result.stdout)
        if native is None:
            return unhealthy("native invalid result", expected_mbc, native_result.stdout)
        nwram = native.get("wram", {})
        nsram = native.get("sram", {})
        native_actual = {"trace": nwram.get(str(TRACE_ADDRESS), ""),
                         "sram0": nsram.get("0", {}).get(str(SRAM_TRACE_ADDRESS)),
                         "sram3": nsram.get("3", {}).get(str(SRAM_TRACE_ADDRESS))}
        if native_actual != expected_mbc:
            return unhealthy("native mbc5", expected_mbc, native_actual)
        native_latches = {key: native.get(key) for key in expected_latches}
        if native_latches != expected_latches:
            return unhealthy("native latches", expected_latches, native_latches)

    print("BACKEND_HEALTHY gbrt conformance=registers,calls,stack,wram,hram,pre-ret,"
          "copy-ret-anchors,top-level-keys,reset-animation,mbc5-rom,mbc5-ram,latches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
