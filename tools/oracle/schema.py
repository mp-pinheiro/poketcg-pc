"""Deterministic validation for oracle schema-2 function cases.

This module only validates case declarations.  It deliberately does not execute
ROM code, infer mapper state, or accept expected-output assertions.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

SCHEMA_VERSION = 2
EVIDENCE = frozenset({
    "primary",
    "scene",
    "intentional-transform",
    "native-stress",
    "dependency-blocked",
})
COMPLETIONS = frozenset({"return", "pre-ret", "event"})

_CASE_KEYS = frozenset({
    "id", "hardware", "mapper", "registers", "bus", "seeds", "state", "setup",
    "input_events", "instruction_budget", "cycle_budget", "completion", "evidence",
    "reason",
})
_MAPPER_KEYS = frozenset({
    "rom_bank", "ram_bank", "vram_bank", "ram_enable", "mode",
})
_SEED_REGIONS = frozenset({"wram", "hram", "sram", "vram", "oam", "palette"})
_REGISTER_NAMES = frozenset({"a", "f", "b", "c", "d", "e", "hl", "sp"})


class SchemaValidationError(ValueError):
    """A case does not conform to the schema-2 declaration contract."""


def _fail(path: str, message: str) -> None:
    raise SchemaValidationError(f"{path}: {message}")


def _mapping(value: Any, path: str) -> Mapping[Any, Any]:
    if not isinstance(value, Mapping):
        _fail(path, "must be an object")
    return value


def _integer(value: Any, path: str, *, minimum: int = 0, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        _fail(path, "must be an integer")
    if value < minimum or (maximum is not None and value > maximum):
        bound = f"between {minimum} and {maximum}" if maximum is not None else f">= {minimum}"
        _fail(path, f"must be {bound}")
    return value


def _bytes(value: Any, path: str) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        result = bytearray()
        for index, byte in enumerate(value):
            result.append(_integer(byte, f"{path}[{index}]", maximum=255))
        return bytes(result)
    _fail(path, "must be bytes or a sequence of byte values")


def _check_unknown(value: Mapping[Any, Any], allowed: frozenset[str], path: str) -> None:
    unknown = sorted(str(key) for key in value if key not in allowed)
    if unknown:
        _fail(path, f"unknown key(s): {', '.join(unknown)}")


def _address(value: Any, path: str, *, maximum: int = 0xFFFF) -> int:
    if isinstance(value, bool):
        _fail(path, "must be an integer address")
    if isinstance(value, int):
        result = value
    elif isinstance(value, str):
        text = value.strip()
        try:
            result = int(text, 0)
        except ValueError:
            _fail(path, "must be an integer address")
    else:
        _fail(path, "must be an integer address")
    if result < 0 or result > maximum:
        _fail(path, f"must be between 0 and {maximum}")
    return result


def _span_seeds(value: Any, path: str) -> list[tuple[int, int, str]]:
    entries = _mapping(value, path)
    spans: list[tuple[int, int, str]] = []
    for key, payload in entries.items():
        address = _address(key, f"{path}.{key}")
        data = _bytes(payload, f"{path}.{key}")
        if not data:
            _fail(f"{path}.{key}", "seed span must not be empty")
        end = address + len(data) - 1
        if end > 0xFFFF:
            _fail(f"{path}.{key}", "seed span exceeds address space")
        spans.append((address, end, f"{path}.{key}"))
    spans.sort()
    for previous, current in zip(spans, spans[1:]):
        if current[0] <= previous[1]:
            _fail(path, f"conflicting seed spans: {previous[2]} overlaps {current[2]}")
    return spans


def _validate_seeds(seeds: Any) -> None:
    regions = _mapping(seeds, "seeds")
    _check_unknown(regions, _SEED_REGIONS, "seeds")
    for region, value in regions.items():
        if region in {"sram", "vram"}:
            banks = _mapping(value, f"seeds.{region}")
            for bank, spans in banks.items():
                _address(bank, f"seeds.{region}.{bank}", maximum=255)
                _span_seeds(spans, f"seeds.{region}.{bank}")
        else:
            _span_seeds(value, f"seeds.{region}")
def _validate_bus(value: Any) -> None:
    entries = _mapping(value, "case.bus")
    for address, size in entries.items():
        address = _address(address, f"case.bus.{address}")
        size = _integer(size, f"case.bus.{address}", minimum=1)
        if address + size > 0x10000:
            _fail(f"case.bus.{address}", "span exceeds address space")


def _validate_state(value: Any) -> None:
    state = _mapping(value, "case.state")
    _check_unknown(state, frozenset({"wram", "sram", "vram", "palette"}), "case.state")
    for region, entries in state.items():
        if not isinstance(entries, list):
            _fail(f"case.state.{region}", "must be an array")
        width = 2 if region in {"wram", "palette"} else 3
        for index, entry in enumerate(entries):
            if not isinstance(entry, list) or len(entry) != width:
                _fail(f"case.state.{region}[{index}]", f"must contain {width} integers")
            offset = 0
            if region in {"sram", "vram"}:
                _integer(entry[0], f"case.state.{region}[{index}].bank", maximum=255)
                offset = 1
            maximum = 0x7F if region == "palette" else 0xFFFF
            address = _integer(
                entry[offset],
                f"case.state.{region}[{index}].address",
                maximum=maximum,
            )
            size = _integer(entry[offset + 1], f"case.state.{region}[{index}].size", minimum=1)
            limit = 0x80 if region == "palette" else 0x10000
            if address + size > limit:
                _fail(f"case.state.{region}[{index}]", "span exceeds address space")


def _validate_setup(value: Any) -> None:
    if not isinstance(value, list):
        _fail("case.setup", "must be an array")
    allowed = frozenset({"fn", "a", "f", "b", "c", "d", "e", "hl"})
    for index, item in enumerate(value):
        item = _mapping(item, f"case.setup[{index}]")
        _check_unknown(item, allowed, f"case.setup[{index}]")
        if not isinstance(item.get("fn"), str) or not item["fn"].strip():
            _fail(f"case.setup[{index}].fn", "must be a non-empty string")
        for name, register in item.items():
            if name != "fn":
                _integer(register, f"case.setup[{index}].{name}", maximum=0xFFFF if name == "hl" else 255)


def _validate_input_events(value: Any) -> None:
    if not isinstance(value, list):
        _fail("case.input_events", "must be an array")
    for index, event in enumerate(value):
        event = _mapping(event, f"case.input_events[{index}]")
        if set(event) != {"keys"}:
            _fail(f"case.input_events[{index}]", "must contain exactly the keys field")
        _integer(event["keys"], f"case.input_events[{index}].keys", maximum=255)
def validate_case(case: Mapping[str, Any], *, case_id: str | None = None) -> Mapping[str, Any]:
    """Validate one schema-2 case and return it unchanged.

    ``case_id`` is the registry key, when one exists; requiring it to agree
    with the declaration prevents dictionary position from becoming identity.
    """
    case = _mapping(case, "case")
    _check_unknown(case, _CASE_KEYS, "case")
    declared_id = case.get("id")
    if not isinstance(declared_id, str) or not declared_id.strip():
        _fail("case.id", "must be a non-empty string")
    if case_id is not None and declared_id != case_id:
        _fail("case.id", f"does not match registry id {case_id!r}")
    if case.get("hardware") not in {"dmg", "cgb"}:
        _fail("case.hardware", "must be dmg or cgb")

    mapper = _mapping(case.get("mapper"), "case.mapper")
    _check_unknown(mapper, _MAPPER_KEYS, "case.mapper")
    for required in ("rom_bank", "ram_bank", "vram_bank"):
        if required not in mapper:
            _fail("case.mapper", f"missing explicit {required}")
        _integer(mapper[required], f"case.mapper.{required}", maximum=255)
    if "ram_enable" in mapper and not isinstance(mapper["ram_enable"], bool):
        _fail("case.mapper.ram_enable", "must be a boolean")
    if "mode" in mapper and not isinstance(mapper["mode"], str):
        _fail("case.mapper.mode", "must be a string")

    registers = _mapping(case.get("registers"), "case.registers")
    _check_unknown(registers, _REGISTER_NAMES, "case.registers")
    for name, value in registers.items():
        _integer(value, f"case.registers.{name}", maximum=0xFFFF if name in {"hl", "sp"} else 255)

    if "bus" in case:
        _validate_bus(case["bus"])
    _validate_seeds(case.get("seeds", {}))
    if "state" in case:
        _validate_state(case["state"])
    _validate_setup(case.get("setup", []))
    _validate_input_events(case.get("input_events", []))
    _integer(case.get("instruction_budget"), "case.instruction_budget", minimum=1)
    _integer(case.get("cycle_budget"), "case.cycle_budget", minimum=1)

    completion = _mapping(case.get("completion"), "case.completion")
    mode = completion.get("mode")
    if mode not in COMPLETIONS:
        _fail("case.completion.mode", "must be one of return, pre-ret, event")
    allowed = {"mode"} | ({"pc"} if mode == "pre-ret" else {"predicate"} if mode == "event" else set())
    _check_unknown(completion, frozenset(allowed), "case.completion")
    if mode == "pre-ret":
        _integer(completion.get("pc"), "case.completion.pc", maximum=0xFFFF)
    elif mode == "event" and (not isinstance(completion.get("predicate"), str) or not completion["predicate"].strip()):
        _fail("case.completion.predicate", "must be a non-empty string")
    evidence = case.get("evidence")
    if evidence not in EVIDENCE:
        _fail("case.evidence", "must be one of the declared evidence kinds")
    if "reason" in case:
        if evidence == "primary" or not isinstance(case["reason"], str) or not case["reason"].strip():
            _fail("case.reason", "must be a non-empty string on a non-primary case")
    return case


def validate_cases(cases: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Mapping[str, Any]]:
    """Validate a registry while making every dictionary key an explicit ID."""
    cases = _mapping(cases, "cases")
    for case_id, case in cases.items():
        if not isinstance(case_id, str) or not case_id.strip():
            _fail("cases", "registry keys must be non-empty strings")
        validate_case(case, case_id=case_id)
    return cases
