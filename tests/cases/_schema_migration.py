"""Mechanical conversion of legacy oracle fixtures to schema-2 records."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


_REGISTERS = ("a", "f", "b", "c", "d", "e", "hl", "sp")
_SETUP_REGISTERS = frozenset(("a", "f", "b", "c", "d", "e", "hl"))
_MAPPER = {
    "rom_bank": 1,
    "ram_bank": 0,
    "vram_bank": 0,
    "ram_enable": False,
    "mode": "symbol",
}


def _integer(value: Any, label: str, *, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
        raise ValueError(f"{label} must be an integer between 0 and {maximum}")
    return value


def _probes(value: Any, label: str) -> dict[int, int]:
    if not isinstance(value, Mapping):
        raise TypeError(f"legacy {label} probe must be a mapping")
    probes = {}
    for address, size in value.items():
        address = _integer(address, f"{label} address", maximum=0xFFFF)
        size = _integer(size, f"{label} size", maximum=0x10000)
        if not size:
            continue
        if address + size > 0x10000:
            raise ValueError(f"{label} probe span exceeds address space")
        probes[address] = size
    return probes


def _state(sram: Any, vram: Any, palette: Any) -> dict[str, list[list[int]]]:
    state: dict[str, list[list[int]]] = {}
    for region, value in (("sram", sram), ("vram", vram)):
        if value:
            if not isinstance(value, Mapping):
                raise TypeError(f"legacy {region} probe must be a mapping")
            entries = []
            for bank, probes in sorted(value.items(), key=lambda item: int(item[0])):
                bank = _integer(bank, f"{region} bank", maximum=255)
                entries.extend([bank, address, size] for address, size in sorted(_probes(probes, region).items()))
            state[region] = entries
    palette_probes = _probes(palette, "palette")
    if any(address + size > 0x80 for address, size in palette_probes.items()):
        raise ValueError("legacy palette probe span exceeds palette RAM")
    if palette_probes:
        state["palette"] = [[address, size] for address, size in sorted(palette_probes.items())]
    return state


def _setup(value: Any) -> list[dict[str, int | str]]:
    if not isinstance(value, list):
        raise TypeError("legacy setup must be a list")
    result = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise TypeError(f"legacy setup[{index}] must be a mapping")
        unknown = set(item) - _SETUP_REGISTERS - {"fn"}
        if unknown or not isinstance(item.get("fn"), str) or not item["fn"].strip():
            raise ValueError(f"legacy setup[{index}] has invalid keys")
        entry: dict[str, int | str] = {"fn": item["fn"]}
        for name in _SETUP_REGISTERS & set(item):
            entry[name] = _integer(item[name], f"legacy setup[{index}].{name}", maximum=0xFFFF if name == "hl" else 255)
        result.append(entry)
    return result

def _bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, Sequence) and not isinstance(value, str):
        return bytes(value)
    raise TypeError(f"legacy seed must be byte-like, got {type(value).__name__}")


def _wram(value: Any) -> dict[Any, bytes]:
    if not isinstance(value, Mapping):
        raise TypeError("legacy wram seed must be a mapping")
    image: dict[int, int] = {}
    # Legacy seeds are ordered bus writes; later spans intentionally patch earlier images.
    for raw_address, raw_payload in value.items():
        address = _integer(int(raw_address), "seed address", maximum=0xFFFF)
        payload = _bytes(raw_payload)
        if address + len(payload) > 0x10000:
            raise ValueError("legacy seed span exceeds address space")
        for offset, byte in enumerate(payload):
            image[address + offset] = byte
    if not image:
        return {}
    merged: dict[int, bytes] = {}
    addresses = sorted(image)
    start = previous = addresses[0]
    payload = bytearray((image[start],))
    for address in addresses[1:]:
        if address != previous + 1:
            merged[start] = bytes(payload)
            start = address
            payload = bytearray()
        payload.append(image[address])
        previous = address
    merged[start] = bytes(payload)
    return merged

def _seed_byte(spans: Mapping[int, bytes], address: int, default: int) -> int:
    for start, payload in spans.items():
        offset = address - start
        if 0 <= offset < len(payload):
            return payload[offset]
    return default




def _banked(value: Any) -> dict[Any, dict[Any, bytes]]:
    if not isinstance(value, Mapping):
        raise TypeError("legacy banked seed must be a mapping")
    return {bank: _wram(value[bank]) for bank in sorted(value, key=lambda item: int(item))}


def legacy_to_schema(cases: Mapping[str, Sequence[Mapping[str, Any]]], contract: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Convert legacy ``CASES`` and register contracts into schema-2 records."""
    for function in cases:
        fields = contract.get(function)
        if isinstance(fields, tuple):
            contract[function] = {"compare": fields, "preserve": fields}
            continue
        if not isinstance(fields, dict):
            raise TypeError(f"legacy contract {function} must be a tuple or schema-2 mapping")
        # The comparator observes `compare` and additionally requires `preserve` to be
        # a subset of it: a register that must not move is still a register under
        # observation. Authors reasonably write the two as disjoint sets (results vs
        # callee-saved), which the comparator rejects outright. Widening keeps the
        # stated intent, is strictly more rigorous, and is a no-op wherever the subset
        # relation already holds -- which is every landed contract.
        compare = tuple(fields.get("compare") or ())
        preserve = tuple(fields.get("preserve") or ())
        missing = tuple(name for name in preserve if name not in compare)
        if missing:
            contract[function] = {**fields, "compare": compare + missing}
    converted: dict[str, list[dict[str, Any]]] = {}
    for function, entries in cases.items():
        records: list[dict[str, Any]] = []
        for index, legacy in enumerate(entries):
            if not isinstance(legacy, Mapping):
                raise TypeError(f"legacy case {function}[{index}] must be a mapping")
            registers = {name: int(legacy.get(name, 0)) for name in _REGISTERS if name != "sp"}
            seeds: dict[str, Any] = {"wram": _wram(legacy.get("wram", {}))}
            if "sram" in legacy:
                seeds["sram"] = _banked(legacy["sram"])
            if "vram" in legacy:
                seeds["vram"] = _banked(legacy["vram"])
            default_ram_bank = next(reversed(seeds.get("sram", {})), 0)
            ram_bank = _seed_byte(seeds["wram"], 0xFF81, default_ram_bank)
            vram_bank = _seed_byte(seeds["wram"], 0xFF82, 0) & 1
            ram_enable = bool(legacy.get("ramg", bool(seeds.get("sram"))))
            keys = legacy.get("keys")
            if keys is not None:
                keys = _integer(keys, f"legacy case {function}[{index}].keys", maximum=255)
            if "ramg" in legacy and not isinstance(legacy["ramg"], bool):
                raise TypeError(f"legacy case {function}[{index}].ramg must be a boolean")
            evidence = legacy.get(
                "evidence",
                "native-stress" if legacy.get("oracle") is False else "primary",
            )
            if evidence not in {
                "primary", "scene", "intentional-transform", "native-stress",
                "dependency-blocked",
            }:
                raise ValueError(f"legacy case {function}[{index}] has invalid evidence")
            record: dict[str, Any] = {
                "id": f"{function}-{index}",
                "hardware": "cgb",
                "mapper": {
                    **_MAPPER,
                    "rom_bank": _integer(legacy["rom_bank"], "rom_bank", maximum=0xFF)
                                if legacy.get("rom_bank") is not None
                                else _MAPPER["rom_bank"],
                    "ram_bank": ram_bank,
                    "vram_bank": vram_bank,
                    "ram_enable": ram_enable,
                },
                "registers": registers,
                "bus": _probes(legacy.get("read", {}), "read"),
                "seeds": seeds,
                "setup": _setup(legacy.get("setup", [])),
                "input_events": [] if keys is None else [{"keys": keys}],
                "instruction_budget": _integer(
                    legacy.get("instruction_budget", 100000),
                    f"legacy case {function}[{index}].instruction_budget",
                    maximum=0xFFFFFFFF,
                ),
                "cycle_budget": _integer(
                    legacy.get("cycle_budget", 400000),
                    f"legacy case {function}[{index}].cycle_budget",
                    maximum=0xFFFFFFFF,
                ),
                "completion": {"mode": "return"},
                "evidence": evidence,
                "snapshot": bool(legacy.get("snapshot", False)),
            }
            reason = legacy.get("reason", legacy.get("why"))
            if evidence != "primary" and reason is not None:
                record["reason"] = reason
            state = _state(
                legacy.get("sread", {}),
                legacy.get("vread", {}),
                legacy.get("pread", {}),
            )
            if record["snapshot"]:
                for region in ("wram", "hram", "sram", "vram", "oam", "palette"):
                    state.setdefault(region, [])
            if state:
                record["state"] = state
            records.append(record)
        converted[function] = records
    return converted
