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

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tests" / "cases"))
sys.path.insert(0, str(ROOT))

REGISTERS = ("a", "f", "b", "c", "d", "e", "hl")

def _merge_spans(spans):
    merged = []
    for address, size in sorted(set(spans)):
        end = address + size
        if merged and address <= merged[-1][0] + merged[-1][1]:
            start, previous_size = merged[-1]
            merged[-1] = (start, max(start + previous_size, end) - start)
        else:
            merged.append((address, size))
    return tuple(merged)


def _merge_banked_spans(spans):
    merged = []
    for bank in sorted({bank for bank, _address, _size in spans}):
        merged.extend(
            (bank, address, size)
            for address, size in _merge_spans(
                (address, size)
                for candidate, address, size in spans
                if candidate == bank
            )
        )
    return tuple(merged)



def _number(value, label):
    if isinstance(value, bool) or not isinstance(value, int):
        raise SystemExit(f"SCHEMA {label} must be an integer")
    return value


def _symbols(path):
    result = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2 and ":" in parts[0]:
            bank, address = parts[0].split(":", 1)
            try:
                result[parts[-1]] = (int(bank, 16), int(address, 16))
            except ValueError:
                continue
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fn", required=True)
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--symbols", type=Path, required=True)
    args = parser.parse_args()
    post_call_byte = None
    seed_wram_spec = ""
    seed_sram_spec = ""
    seed_vram_spec = ""
    seed_wram_map = {}
    seed_sram_map = {}
    seed_vram_map = {}
    seeds = {}
    seed_native_rom_bank = False
    native_vram_bank = 0
    symbols = _symbols(args.symbols)
    if args.fn not in symbols:
        raise SystemExit("ARTIFACT function is absent from symbols")
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
        entry = symbols[args.fn][1]
        case.update({
            "fn": args.fn,
            "entry": entry,
            "compare": compare_fields,
            "preserve": preserve_fields,
            "state": case.get(
                "state",
                {name: [] for name in ("wram", "hram", "sram", "vram", "oam", "palette")},
            ),
            "sram": case.get("sram", {}),
            "vram": case.get("vram", {}),
        })
        case["ir_peer"] = bool(case.get("ir_peer", False))
        case["state"] = {
            name: list(case["state"].get(name, []))
            for name in ("wram", "hram", "sram", "vram", "oam", "palette")
        }
        mapper = dict(case["mapper"])
        native_vram_bank = int(mapper.pop("vram_bank"))
        mapper_mode = mapper.pop("mode", "fixed")
        native_hbank_rom = mapper.pop("hbank_rom", None)
        seed_native_rom_bank = True
        if mapper_mode == "symbol" and entry >= 0x4000:
            mapper["rom_bank"] = symbols[args.fn][0]
        elif mapper_mode not in {"fixed", "symbol"}:
            raise SystemExit("SCHEMA mapper mode must be fixed or symbol")
        case["mapper"] = mapper
        seeds = case.pop("seeds", {})
        post_call_byte = case.pop("post_call_byte", None)
        if post_call_byte is not None:
            if isinstance(post_call_byte, bool) or not isinstance(post_call_byte, int) or not 0 <= post_call_byte <= 0xff:
                raise SystemExit("SCHEMA post_call_byte must be an integer in range 0..255")
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
                seed_sram_map.setdefault(str(parsed_bank), {})[str(parsed_address)] = encoded
                seed_sram_parts.append(f"{parsed_bank:x}:{parsed_address:x}={encoded}")
                case["state"]["sram"].append([parsed_bank, parsed_address, len(bytes(payload))])
        seed_vram_parts = []
        for bank, spans in seeds.get("vram", {}).items():
            for address, payload in spans.items():
                parsed_bank = int(bank, 0) if isinstance(bank, str) else int(bank)
                parsed_address = int(address, 0) if isinstance(address, str) else int(address)
                encoded = bytes(payload).hex()
                seed_vram_map.setdefault(str(parsed_bank), {})[str(parsed_address)] = encoded
                seed_vram_parts.append(f"{parsed_bank:x}:{parsed_address:x}={encoded}")
                case["state"]["vram"].append([parsed_bank, parsed_address, len(bytes(payload))])
        seed_wram_spec = ";".join(seed_parts)
        seed_sram_spec = ";".join(seed_sram_parts)
        seed_vram_spec = ";".join(seed_vram_parts)
        if mode == "pre-ret" and isinstance(completion, dict):
            case["stop_pc"] = int(completion["pc"])
        case["completion"] = mode
    else:
        case = json.loads(args.case.read_text())
    case.setdefault("state", {name: [] for name in ("wram", "hram", "sram", "vram", "oam", "palette")})
    case.setdefault("snapshot", False)
    case.setdefault("sram", {})
    case.setdefault("vram", {})
    case.setdefault("setup", [])
    case.setdefault("input_events", [])
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
        "id", "hardware", "fn", "entry", "completion", "instruction_budget",
        "cycle_budget", "mapper", "registers", "compare", "preserve", "state",
        "snapshot", "bus", "sram", "vram", "setup", "input_events", "evidence",
        "ir_peer",
    }
    # `stack` is optional: only a routine entered mid-frame declares caller-pushed
    # words, so demanding the key everywhere would invalidate every landed case.
    optional = {"stack", "post_call_byte", "reason", "why"}
    if mode == "pre-ret":
        required.add("stop_pc" if isinstance(completion, str) else "completion")
    if mode == "event":
        if isinstance(completion, str):
            required.update({"event_addr", "event_value", "event_mask"})
    if set(case) - optional != required:
        raise SystemExit("SCHEMA case keys do not match schema-2")
    stack_words = case.get("stack") or []
    if (not isinstance(stack_words, list) or len(stack_words) > 4
            or any(isinstance(word, bool) or not isinstance(word, int)
                   or not 0 <= word <= 0xffff for word in stack_words)):
        raise SystemExit("SCHEMA stack must hold at most 4 words below 0x10000")
    if post_call_byte is not None and (
            isinstance(post_call_byte, bool) or not isinstance(post_call_byte, int)
            or not 0 <= post_call_byte <= 0xff):
        raise SystemExit("SCHEMA post_call_byte must be an integer in range 0..255")
    if case["hardware"] not in {"dmg", "cgb"}:
        raise SystemExit("SCHEMA hardware must be dmg or cgb")
    if not isinstance(case["registers"], dict) or not set(case["registers"]).issubset(REGISTERS):
        raise SystemExit("SCHEMA registers contain unknown fields")
    if (not isinstance(case["compare"], list) or not isinstance(case["preserve"], list)
            or not set(case["preserve"]).issubset(case["compare"])
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
    if not isinstance(case.get("snapshot", False), bool):
        raise SystemExit("SCHEMA snapshot must be boolean")
    if not all(isinstance(case[name], dict) for name in ("bus", "sram", "vram")):
        raise SystemExit("SCHEMA state sections must be objects")
    if not isinstance(case["state"], dict):
        raise SystemExit("SCHEMA state must be an object")
    state_regions = ("wram", "hram", "sram", "vram", "oam", "palette")
    if case["snapshot"]:
        if set(case["state"]) != set(state_regions):
            raise SystemExit("SCHEMA snapshot state must declare all observable regions")
        if not all(isinstance(case["state"][name], list) for name in state_regions):
            raise SystemExit("SCHEMA snapshot state spans must be arrays")
    elif not all(isinstance(entries, list) for entries in case["state"].values()):
        raise SystemExit("SCHEMA state spans must be arrays")
    if not isinstance(case["setup"], list) or not isinstance(case["input_events"], list):
        raise SystemExit("SCHEMA setup and input_events must be arrays")
    # A timeline, one entry per rendered frame, with the last entry held for the
    # rest of the run. The cap matches MAX_INPUT_EVENTS in runner.c.
    if len(case["input_events"]) > 16 or any(
        not isinstance(event, dict)
        or set(event) != {"keys"}
        or isinstance(event["keys"], bool)
        or not isinstance(event["keys"], int)
        or not 0 <= event["keys"] <= 0xff
        for event in case["input_events"]
    ):
        raise SystemExit("SCHEMA input_events must be up to 16 {keys: 0..255} frames")
    resolved_setup = []
    for setup in case["setup"]:
        if not isinstance(setup, dict) or "fn" not in setup or not isinstance(setup["fn"], str):
            raise SystemExit("SCHEMA setup entries require a function name")
        if setup["fn"] not in symbols:
            raise SystemExit(f"SCHEMA setup function is absent from symbols: {setup['fn']}")
        if set(setup) - {"fn", *REGISTERS}:
            raise SystemExit("SCHEMA setup contains unknown fields")
        regs = {}
        for name in set(setup) & set(REGISTERS):
            value = _number(setup[name], f"setup.{name}")
            if not 0 <= value <= (0xffff if name == "hl" else 0xff):
                raise SystemExit(f"SCHEMA setup.{name} is out of range")
            regs[name] = value
        bank, address = symbols[setup["fn"]]
        resolved_setup.append({"fn": setup["fn"], "entry": address, "rom_bank": bank, **regs})
    if not isinstance(case["mapper"], dict) or set(case["mapper"]) != {
        "rom_bank", "ram_bank", "ram_enable"
    }:
        raise SystemExit("SCHEMA mapper must declare rom_bank, ram_bank, ram_enable")
    def span_number(value, label, minimum, maximum):
        value = _number(value, label)
        if not minimum <= value <= maximum:
            raise SystemExit(f"SCHEMA {label} is out of range")
        return value
    for address, size in case["bus"].items():
        span_number(int(address, 0) if isinstance(address, str) else address,
                    "bus address", 0, 0xffff)
        span_number(size, "bus size", 1, 0x10000)
    for name in state_regions:
        width = 3 if name in {"sram", "vram"} else 2
        limit = 0xA0 if name == "oam" else (0x80 if name in {"hram", "palette"} else 0x10000)
        for span in case["state"][name]:
            if not isinstance(span, (list, tuple)) or len(span) != width:
                raise SystemExit(f"SCHEMA state.{name} spans are invalid")
            for value in span:
                _number(value, f"state.{name}")
            offset = 1 if name in {"sram", "vram"} else 0
            if span[offset] + span[offset + 1] > limit:
                raise SystemExit(f"SCHEMA state.{name} span exceeds region")
    if args.fn not in args.symbols.read_text():
        raise SystemExit("ARTIFACT function is absent from symbols")
    registers = {name: int(case["registers"].get(name, 0)) for name in REGISTERS}
    env = os.environ.copy()
    env["POKETCG_ROM"] = str(args.rom.resolve())
    # The native probe renders no frames, so it cycles the timeline on each
    # completed joypad poll instead (src/mem.c). `keys` stays the entry the run
    # starts on -- index 0, matching runner.c -- and is the whole story for a
    # zero- or one-entry timeline.
    keys = case["input_events"][0]["keys"] if case["input_events"] else 0
    request = {
        "completion": mode,
        "hardware": case["hardware"],
        "entry": int(case["entry"]),
        "instruction_budget": int(case["instruction_budget"]),
        "cycle_budget": int(case["cycle_budget"]),
        "rom_bank": int(case["mapper"]["rom_bank"]),
        "ram_bank": int(case["mapper"]["ram_bank"]),
        "ram_enable": int(bool(case["mapper"]["ram_enable"])),
        "vram_bank": native_vram_bank,
        **({"hbank_rom": int(native_hbank_rom)}
           if native_hbank_rom is not None else {}),
        "setup": resolved_setup,
        "input_events": case["input_events"],
        **registers,
    }
    if case.get("ir_peer"):
        request["ir_peer"] = 1
    if stack_words:
        request["stack"] = [int(word) for word in stack_words]
    if post_call_byte is not None:
        request["post_call_byte"] = post_call_byte
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
    wram_spans = _merge_spans(
        (int(addr), int(size)) for addr, size in case["state"]["wram"]
    )
    sram_candidates = [
        (int(bank), int(addr), int(size))
        for bank, addr, size in case["state"]["sram"]
    ]
    sram_candidates.extend(
        (int(bank), int(addr), len(bytes.fromhex(encoded)))
        for bank, spans in seed_sram_map.items()
        for addr, encoded in spans.items()
    )
    sram_spans = _merge_banked_spans(sram_candidates)
    vram_candidates = [
        (int(bank), int(addr), int(size))
        for bank, addr, size in case["state"]["vram"]
    ]
    vram_candidates.extend(
        (int(bank), int(addr), len(bytes.fromhex(encoded)))
        for bank, spans in seed_vram_map.items()
        for addr, encoded in spans.items()
    )
    vram_spans = _merge_banked_spans(vram_candidates)
    hram_spans = _merge_spans(
        (int(addr), int(size)) for addr, size in case["state"]["hram"]
    )
    oam_spans = _merge_spans(
        (int(addr), int(size)) for addr, size in case["state"]["oam"]
    )
    palette_spans = _merge_spans(
        (int(addr), int(size)) for addr, size in case["state"]["palette"]
    )
    bus_candidates = [
        (int(address, 0) if isinstance(address, str) else int(address), int(size))
        for address, size in case["bus"].items()
    ]
    bus_candidates.extend((int(address), len(bytes.fromhex(encoded)))
                          for address, encoded in seed_wram_map.items())
    bus_candidates.extend(wram_spans)
    bus_spans = _merge_spans(bus_candidates)
    request["read_bus"] = ";".join(f"{addr:x}:{size:x}" for addr, size in bus_spans)
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
        print(json.dumps({
            "status": "REFERENCE_DIVERGENCE",
            "fn": case["fn"],
            "mismatches": {f"preserve:{name}": values
                           for name, values in preservation.items()},
            "instructions": reference.get("instructions"),
            "cycles": reference.get("cycles"),
            "pc": reference.get("pc"),
            "sp": reference.get("sp"),
        }, sort_keys=True))
        return 1
    probe_request = {
        "fn": case["fn"], **registers,
        "wram": seed_wram_map,
        "sram": seed_sram_map,
        "vram": seed_vram_map,
        "ram_bank": int(case["mapper"]["ram_bank"]),
        "vram_bank": native_vram_bank,
        "ramg": int(bool(case["mapper"]["ram_enable"])),
        "read": {str(addr): size for addr, size in bus_spans},
        "sread": {str(bank): {str(addr): size for bb, addr, size in sram_spans if bb == bank}
                  for bank in sorted({bank for bank, _, _ in sram_spans})},
        "vread": {str(bank): {str(addr): size for bb, addr, size in vram_spans if bb == bank}
                  for bank in sorted({bank for bank, _, _ in vram_spans})},
        "pread": {str(addr): size for addr, size in palette_spans},
        "setup": case["setup"],
        "keys": keys,
        "input_events": case["input_events"],
    }
    if stack_words:
        probe_request["stack"] = [int(word) for word in stack_words]
    if post_call_byte is not None:
        probe_request["post_call_byte"] = post_call_byte
    if seed_native_rom_bank:
        probe_request["rom_bank"] = int(case["mapper"]["rom_bank"])
    probe = subprocess.run(
        [str(args.probe)], input=json.dumps(probe_request),
        text=True, capture_output=True, check=False, timeout=30, env=env,
    )
    if probe.returncode != 0:
        raise SystemExit(probe.stderr or probe.stdout or
                         f"BACKEND native probe exited {probe.returncode}")
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

    expected_bus = reference.get("bus", "")
    actual_bus = "".join(native.get("wram", {}).get(str(addr), "") for addr, _size in bus_spans)
    if expected_bus != actual_bus:
        mismatch_nibble = next(
            (index for index, (left, right) in enumerate(zip(expected_bus, actual_bus))
             if left != right),
            min(len(expected_bus), len(actual_bus)),
        )
        mismatch_byte = mismatch_nibble // 2
        offset = mismatch_byte
        mismatch_address = None
        for address, size in bus_spans:
            if offset < size:
                mismatch_address = address + offset
                break
            offset -= size
        start = max(0, mismatch_byte - 4) * 2
        end = (mismatch_byte + 5) * 2
        mismatches["bus"] = {
            "address": mismatch_address,
            "reference": expected_bus[start:end],
            "native": actual_bus[start:end],
            "reference_size": len(expected_bus) // 2,
            "native_size": len(actual_bus) // 2,
            "spans": bus_spans,
        }
    reference_vram = bytes.fromhex(reference["vram"])
    expected_vram = "".join(
        reference_vram[
            bank * 0x2000 + address - 0x8000:
            bank * 0x2000 + address - 0x8000 + size
        ].hex()
        for bank, address, size in vram_spans
    )
    if expected_vram != native_spans("vram", vram_spans):
        mismatches["vram"] = "reference/native state differs"
    reference_palette = bytes.fromhex(reference["palette"])
    expected_palette = "".join(
        reference_palette[address:address + size].hex()
        for address, size in palette_spans
    )
    actual_palette = "".join(
        native.get("palette", {}).get(str(address), "")
        for address, _size in palette_spans
    )
    if expected_palette != actual_palette:
        mismatches["palette"] = "reference/native state differs"
    if case["snapshot"]:
        def compare_linear_region(field: str, spans: tuple[tuple[int, int], ...]) -> None:
            expected = bytes.fromhex(reference.get(field, ""))
            grouped = native.get(field, {})
            actual = "".join(
                grouped.get(str(address), "")
                for address, _size in spans
            )
            wanted = "".join(
                expected[address:address + size].hex()
                for address, size in spans
            )
            if wanted != actual:
                mismatches[field] = "reference/native snapshot differs"

        compare_linear_region("wram", tuple(wram_spans))
        compare_linear_region("hram", tuple(hram_spans))
        compare_linear_region("oam", tuple(oam_spans))
    reference_sram = bytes.fromhex(reference["sram"])
    expected_sram = "".join(
        reference_sram[bank * 0x2000 + address - 0xA000:
                       bank * 0x2000 + address - 0xA000 + size].hex()
        for bank, address, size in sram_spans
    )
    actual_sram = native_spans("sram", sram_spans)
    if expected_sram != actual_sram:
        mismatch_nibble = next(
            (index for index, (left, right) in enumerate(zip(expected_sram, actual_sram))
             if left != right),
            min(len(expected_sram), len(actual_sram)),
        )
        mismatch_byte = mismatch_nibble // 2
        start = max(0, mismatch_byte - 4) * 2
        end = (mismatch_byte + 5) * 2
        mismatches["sram"] = {
            "byte": mismatch_byte,
            "reference": expected_sram[start:end],
            "native": actual_sram[start:end],
        }
    if mismatches:
        print(json.dumps({"status": "PORT", "fn": case["fn"], "mismatches": mismatches}))
        return 1
    print(json.dumps({"status": "PASS", "fn": case["fn"], "registers": native}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
