#!/usr/bin/env python3
"""Compare one schema-2 function case through GBRT and the native probe."""

from __future__ import annotations
import argparse
import importlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests" / "cases"))

REGISTERS = ("a", "f", "b", "c", "d", "e", "hl")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fn", required=True)
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--rom", type=Path, required=True)
    seed_wram_spec = ""
    seed_sram_spec = ""
    seed_vram_spec = ""
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--symbols", type=Path, required=True)
    args = parser.parse_args()
    if args.case.suffix == ".py":
        spec = importlib.util.spec_from_file_location("schema2_case", args.case)
        if spec is None or spec.loader is None:
            raise SystemExit("SCHEMA cannot load case module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        records = getattr(module, "SCHEMA2_CASES", {}).get(args.fn, [])
        if args.index < 0 or args.index >= len(records):
            raise SystemExit(f"SCHEMA case index {args.index} is out of range for {args.fn}")
        case = records[args.index]
        completion = case.get("completion")
        mode = completion.get("mode") if isinstance(completion, dict) else completion
        contract = getattr(module, "CONTRACT", {}).get(args.fn, {})
        if not isinstance(contract, dict) or "compare" not in contract or "preserve" not in contract:
            raise SystemExit("SCHEMA contract must declare compare and preserve")
        compare_fields = list(contract["compare"])
        preserve_fields = list(contract["preserve"])
        entry = next(
            int(parts[0].split(":", 1)[1], 16)
            for parts in (line.split() for line in args.symbols.read_text().splitlines())
            if len(parts) >= 2 and parts[-1] == args.fn and ":" in parts[0]
        )
        case.update({
            "fn": args.fn,
            "entry": entry,
            "compare": compare_fields,
            "preserve": preserve_fields,
            "state": {"wram": [], "sram": [], "vram": []},
            "sram": {},
            "vram": {},
        })
        mapper = dict(case["mapper"])
        mapper.pop("vram_bank", None)
        mapper.pop("mode", None)
        case["mapper"] = mapper
        seeds = case.pop("seeds", {})
        seed_wram_map = {}
        seed_parts = []
        for address, payload in seeds.get("wram", {}).items():
            parsed_address = int(address, 0) if isinstance(address, str) else int(address)
            encoded = bytes(payload).hex()
            seed_wram_map[str(parsed_address)] = encoded
            seed_parts.append(f"{parsed_address:04x}={encoded}")
        seed_sram_parts = []
        for bank, spans in seeds.get("sram", {}).items():
            for address, payload in spans.items():
                parsed_bank = int(bank, 0) if isinstance(bank, str) else int(bank)
                parsed_address = int(address, 0) if isinstance(address, str) else int(address)
                encoded = bytes(payload).hex()
                seed_sram_parts.append(f"{parsed_bank:x}:{parsed_address:x}={encoded}")
                case["state"]["sram"].append([parsed_bank, parsed_address, len(bytes(payload))])
        seed_vram_parts = []
        for bank, spans in seeds.get("vram", {}).items():
            for address, payload in spans.items():
                parsed_bank = int(bank, 0) if isinstance(bank, str) else int(bank)
                parsed_address = int(address, 0) if isinstance(address, str) else int(address)
                encoded = bytes(payload).hex()
                seed_vram_parts.append(f"{parsed_bank:x}:{parsed_address:x}={encoded}")
                case["state"]["vram"].append([parsed_bank, parsed_address, len(bytes(payload))])
        case["state"]["wram"] = [[int(address, 0) if isinstance(address, str) else int(address), len(bytes(payload))]
                                 for address, payload in seeds.get("wram", {}).items()]
        seed_wram_spec = ";".join(seed_parts)
        seed_sram_spec = ";".join(seed_sram_parts)
        seed_vram_spec = ";".join(seed_vram_parts)
        case["completion"] = mode
        case["evidence"] = case.get("evidence", "primary")
    else:
        case = json.loads(args.case.read_text())
    if case.get("fn") != args.fn:
        raise SystemExit("SCHEMA case function does not match --fn")
    completion = case.get("completion")
    mode = completion if isinstance(completion, str) else completion.get("mode") if isinstance(completion, dict) else None
    if mode not in ("return", "pre-ret", "event") or not isinstance(case.get("registers"), dict):
        raise SystemExit("SCHEMA case requires completion=return|pre-ret|event and registers")
    if not args.rom.is_absolute() or not args.symbols.is_absolute():
        raise SystemExit("SCHEMA --rom and --symbols must be absolute paths")
    if not args.rom.is_file() or not args.symbols.is_file():
        raise SystemExit("ARTIFACT ROM or symbols path is unavailable")
    required = {
        "id", "fn", "entry", "completion", "instruction_budget", "cycle_budget",
        "mapper", "registers", "compare", "preserve", "state", "bus", "sram", "vram",
        "setup", "input_events", "evidence",
    }
    if mode == "pre-ret":
        required.add("stop_pc" if isinstance(completion, str) else "completion")
    if mode == "event":
        if isinstance(completion, str):
            required.update({"event_addr", "event_value", "event_mask"})
    if set(case) != required:
        raise SystemExit("SCHEMA case keys do not match schema-2")
    if not isinstance(case["registers"], dict) or not set(case["registers"]).issubset(REGISTERS):
        raise SystemExit("SCHEMA registers contain unknown fields")
    if (not isinstance(case["compare"], list) or not isinstance(case["preserve"], list)
            or not case["compare"] or not set(case["preserve"]).issubset(case["compare"])
            or any(field not in REGISTERS for field in case["compare"] + case["preserve"])):
        raise SystemExit("SCHEMA compare/preserve contract is invalid")
    if case["evidence"] != "primary":
        raise SystemExit("SCHEMA comparator slice requires primary evidence")
    for name in ("entry", "instruction_budget", "cycle_budget"):
        value = case[name]
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise SystemExit(f"SCHEMA invalid positive integer {name}")
    if case["entry"] > 0xffff or case["instruction_budget"] > 0xffffffff or case["cycle_budget"] > 0xffffffff:
        raise SystemExit("SCHEMA numeric field out of range")
    if mode == "pre-ret" and (
        isinstance(case["stop_pc"], bool) or not isinstance(case["stop_pc"], int)
        or not 0 <= case["stop_pc"] <= 0xffff
    ):
        raise SystemExit("SCHEMA pre-ret requires stop_pc in address range")
    if mode == "event" and isinstance(completion, str) and any(
        isinstance(case[name], bool) or not isinstance(case[name], int)
        or case[name] < 0 or case[name] > (0xffff if name == "event_addr" else 0xff)
        for name in ("event_addr", "event_value", "event_mask")
    ):
        raise SystemExit("SCHEMA event predicate is out of range")
    if not isinstance(case["id"], str) or not case["id"]:
        raise SystemExit("SCHEMA id must be non-empty")
    if not all(isinstance(case[name], dict) for name in ("bus", "sram", "vram")):
        raise SystemExit("SCHEMA state sections must be objects")
    if not isinstance(case["setup"], list) or not isinstance(case["input_events"], list):
        raise SystemExit("SCHEMA setup and input_events must be arrays")
    if not isinstance(case["state"], dict) or set(case["state"]) != {"wram", "sram", "vram"}:
        raise SystemExit("SCHEMA state must declare wram, sram, and vram spans")
    if not all(isinstance(case["state"][name], list) for name in ("wram", "sram", "vram")):
        raise SystemExit("SCHEMA state spans must be arrays")
    if not isinstance(case["mapper"], dict) or set(case["mapper"]) != {
        "rom_bank", "ram_bank", "ram_enable"
    }:
        raise SystemExit("SCHEMA mapper must declare rom_bank, ram_bank, ram_enable")
    if any(seeds.get(region) for region in ("hram", "oam", "palette")):
        raise SystemExit("SCHEMA canonical HRAM/OAM/palette seeds require runner state support")
    if args.fn not in args.symbols.read_text():
        raise SystemExit("ARTIFACT function is absent from symbols")
    registers = {name: int(case["registers"].get(name, 0)) for name in REGISTERS}
    env = os.environ.copy()
    env["POKETCG_ROM"] = str(args.rom.resolve())
    request = {
        "completion": mode,
        "entry": int(case["entry"]),
        "instruction_budget": int(case["instruction_budget"]),
        "cycle_budget": int(case["cycle_budget"]),
        "rom_bank": int(case["mapper"]["rom_bank"]),
        "ram_bank": int(case["mapper"]["ram_bank"]),
        "ram_enable": int(bool(case["mapper"]["ram_enable"])),
        **registers,
    }
    if mode == "pre-ret":
        request["stop_pc"] = int(case["stop_pc"] if isinstance(completion, str) else completion["pc"])
    if mode == "event":
        if isinstance(completion, dict):
            request["predicate"] = completion["predicate"]
        else:
            request["predicate"] = (
                f"mem:{int(case['event_addr']):#x}=={int(case['event_value']):#x}"
                f"&{int(case['event_mask']):#x}"
            )
    if seed_wram_spec:
        request["seed_wram"] = seed_wram_spec
    if seed_sram_spec:
        request["seed_sram"] = seed_sram_spec
    if seed_vram_spec:
        request["seed_vram"] = seed_vram_spec
    primary = subprocess.run(
        [str(args.runner), "--rom", str(args.rom.resolve())],
        input=json.dumps(request), text=True, capture_output=True, check=False,
        timeout=30, env=env,
    )
    if primary.returncode != 0:
        raise SystemExit(primary.stdout or primary.stderr)
    payload = next((line for line in reversed(primary.stdout.splitlines())
                    if line.startswith("{")), None)
    if payload is None:
        raise SystemExit("BACKEND missing JSON result")
    reference = json.loads(payload)
    if reference.get("status") != "REFERENCE_OK" or reference.get("completion") != mode:
        raise SystemExit("BACKEND invalid completion result")
    pairs = {}
    for pair in ("af", "bc", "de"):
        value = reference.get(pair)
        if not isinstance(value, int) or not 0 <= value <= 0xffff:
            raise SystemExit(f"BACKEND missing or invalid {pair}")
        pairs[pair] = value
    hl = reference.get("hl")
    if not isinstance(hl, int) or not 0 <= hl <= 0xffff:
        raise SystemExit("BACKEND missing or invalid hl")
    reference.update({
        "a": pairs["af"] >> 8, "f": pairs["af"] & 0xff,
        "b": pairs["bc"] >> 8, "c": pairs["bc"] & 0xff,
        "d": pairs["de"] >> 8, "e": pairs["de"] & 0xff,
    })
    preservation = {
        name: (registers[name], reference.get(name))
        for name in case["preserve"]
        if reference.get(name) != registers[name]
    }
    if preservation:
        print(json.dumps({"status": "PORT", "fn": case["fn"],
                          "mismatches": {f"preserve:{name}": values
                                         for name, values in preservation.items()}}))
        return 1
    wram_spans = tuple((int(addr), int(size)) for addr, size in case["state"]["wram"])
    sram_spans = tuple((int(bank), int(addr), int(size)) for bank, addr, size in case["state"]["sram"])
    vram_spans = tuple((int(bank), int(addr), int(size)) for bank, addr, size in case["state"]["vram"])
    probe_request = {
        "fn": case["fn"], **registers,
        "wram": seed_wram_map,
        "read": {str(addr): size for addr, size in wram_spans},
        "sread": {str(bank): {str(addr): size for bb, addr, size in sram_spans if bb == bank}
                  for bank in sorted({bank for bank, _, _ in sram_spans})},
        "vread": {str(bank): {str(addr): size for bb, addr, size in vram_spans if bb == bank}
                  for bank in sorted({bank for bank, _, _ in vram_spans})},
    }
    probe = subprocess.run(
        [str(args.probe)], input=json.dumps(probe_request),
        text=True, capture_output=True, check=False, timeout=30, env=env,
    )
    if probe.returncode != 0:
        raise SystemExit(probe.stderr)
    native = json.loads(probe.stdout)
    mismatches = {
        name: (reference.get(name), native.get(name))
        for name in case["compare"]
        if reference.get(name) != native.get(name)
    }

    def reference_spans(field: str, base: int, spans: tuple[tuple[int, int], ...]) -> str:
        data = bytes.fromhex(reference[field])
        return "".join(data[address - base:address - base + size].hex()
                       for address, size in spans)

    def native_spans(field: str, spans: tuple[tuple[int, int, int], ...]) -> str:
        grouped = native.get(field, {})
        if field == "wram":
            return "".join(grouped.get(str(address), "")
                           for _bank, address, _size in spans)
        return "".join(
            "".join(grouped.get(str(bank), {}).get(str(address), "")
                    for bb, address, _size in spans if bb == bank)
            for bank in sorted({bank for bank, _address, _size in spans})
        )

    expected_wram = reference_spans("wram", 0xC000, wram_spans)
    actual_wram = native_spans("wram", tuple((0, address, size) for address, size in wram_spans))
    if expected_wram != actual_wram:
        mismatches["wram"] = "reference/native state differs"
    expected_vram = "".join(
        reference_spans("vram", 0x8000, tuple((address, size) for bb, address, size in vram_spans if bb == bank))
        for bank in sorted({bank for bank, _address, _size in vram_spans})
    )
    if expected_vram != native_spans("vram", vram_spans):
        mismatches["vram"] = "reference/native state differs"
    reference_sram = bytes.fromhex(reference["sram"])
    expected_sram = "".join(
        reference_sram[bank * 0x2000 + address - 0xA000:
                       bank * 0x2000 + address - 0xA000 + size].hex()
        for bank, address, size in sram_spans
    )
    if expected_sram != native_spans("sram", sram_spans):
        mismatches["sram"] = "reference/native state differs"
    if mismatches:
        print(json.dumps({"status": "PORT", "fn": case["fn"], "mismatches": mismatches}))
        return 1
    print(json.dumps({"status": "PASS", "fn": case["fn"], "registers": native}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
