"""Mechanical conversion of legacy oracle fixtures to schema-2 records."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


_REGISTERS = ("a", "f", "b", "c", "d", "e", "hl", "sp")
_MAPPER = {
    "rom_bank": 1,
    "ram_bank": 0,
    "vram_bank": 0,
    "ram_enable": False,
}


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
    spans = [(int(address), _bytes(payload)) for address, payload in value.items()]
    merged: list[tuple[int, bytearray]] = []
    for address, payload in sorted(spans):
        if not payload:
            continue
        if not merged or address >= merged[-1][0] + len(merged[-1][1]):
            merged.append((address, bytearray(payload)))
            continue
        start, current = merged[-1]
        offset = address - start
        overlap = min(len(current) - offset, len(payload))
        if any(current[offset + index] != payload[index] for index in range(overlap)):
            raise ValueError("conflicting overlapping legacy seed spans")
        end = max(start + len(current), address + len(payload))
        current.extend(b"\x00" * (end - start - len(current)))
        current[offset:offset + len(payload)] = payload
    return {address: bytes(payload) for address, payload in merged}


def _banked(value: Any) -> dict[Any, dict[Any, bytes]]:
    if not isinstance(value, Mapping):
        raise TypeError("legacy banked seed must be a mapping")
    return {bank: _wram(value[bank]) for bank in sorted(value, key=lambda item: int(item))}


def legacy_to_schema(cases: Mapping[str, Sequence[Mapping[str, Any]]], contract: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Convert legacy ``CASES`` into deterministic, non-primary schema records.

    Legacy expected outputs and read probes are intentionally discarded.  The
    contract is accepted to keep the migration call-site uniform; schema-2
    contract declarations remain owned by the module's ``CONTRACT`` value.
    """
    del contract
    converted: dict[str, list[dict[str, Any]]] = {}
    for function, entries in cases.items():
        records: list[dict[str, Any]] = []
        for index, legacy in enumerate(entries):
            if not isinstance(legacy, Mapping):
                raise TypeError(f"legacy case {function}[{index}] must be a mapping")
            registers = {
                name: int(legacy.get(name, 0))
                for name in _REGISTERS
            }
            evidence = "native-stress" if legacy.get("oracle") is True else "dependency-blocked"
            try:
                seeds: dict[str, Any] = {"wram": _wram(legacy.get("wram", {}))}
                if "sram" in legacy:
                    seeds["sram"] = _banked(legacy["sram"])
                if "vram" in legacy:
                    seeds["vram"] = _banked(legacy["vram"])
            except ValueError:
                seeds = {"wram": {}}
                evidence = "dependency-blocked"
            records.append({
                "id": f"{function}-{index}",
                "mapper": dict(_MAPPER),
                "registers": registers,
                "bus": {},
                "seeds": seeds,
                "setup": [],
                "input_events": [],
                "instruction_budget": 100000,
                "cycle_budget": 400000,
                "completion": {"mode": "return"},
                "evidence": evidence,
            })
        converted[function] = records
    return converted
