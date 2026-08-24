#!/usr/bin/env python3
"""Structural classifier over pret assembly text.

`feature_class` is routing and bucketing metadata only; the oracle is the sole
acceptance authority.  Nothing here decides whether a port is correct, so this
module deliberately never runs a subprocess, never needs a recompiler, and
never raises for ordinary input: a packet must always be buildable.

The parse is a parse of pret assembly — the authoritative text the port is
diffed against — not a regex guess at semantics.  Reviewed corrections live in
`analyzer_overrides.toml` and win over every inferred rule.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import tomllib
from pathlib import Path
from typing import Any

import common

VERSION = "asm-structural-1"
FEATURE_CLASSES = (
    "direct", "direct-callee", "branch-loop", "bus-banked", "finite-dispatch",
    "event-input", "hardware-transform", "stack-sensitive", "unsupported",
)

_SKIP_TOKENS = frozenset({"section", "include", "db", "dw", "ds"})

_LABEL = re.compile(r"^([A-Za-z_.][A-Za-z0-9_.]*):{1,2}\s*(.*)$")
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")
_BRANCHES = frozenset({"call", "jp", "jr", "rst"})

# Operand tokens that look like identifiers but name machine state, not a
# symbol: without this filter `jr nc, .loop` reports a callee named "nc".
_REGISTERS = frozenset({
    "a", "b", "c", "d", "e", "h", "l", "af", "bc", "de", "hl", "sp", "pc",
    "z", "nz", "nc", "hli", "hld",
})

_INDIRECT_OPERANDS = frozenset({"hl", "bc", "de"})
_BANK_MARKERS = ("rromb", "hbankrom", "bankswitch")


def tokenize(asm: str) -> list[tuple[str, tuple[str, ...]]]:
    """Instructions and label definitions of one asm slice, in source order.

    A label definition is emitted as ``("label", (name,))`` so callers can
    resolve backward branches without a second pass; every other entry is
    ``(mnemonic, operands)`` with the mnemonic lowercased.
    """
    out: list[tuple[str, tuple[str, ...]]] = []
    for raw in asm.splitlines():
        line = raw.split(";", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        match = _LABEL.match(stripped)
        if match and not line[:1].isspace():
            out.append(("label", (match.group(1),)))
            stripped = match.group(2).strip()
            if not stripped:
                continue
        head, _, rest = stripped.partition(" ")
        if head.startswith("."):
            out.append(("label", (head,)))
            continue
        if head.lower() in _SKIP_TOKENS:
            continue
        operands = tuple(part.strip() for part in rest.split(",") if part.strip())
        out.append((head.lower(), operands))
    return out


def _bare(operand: str) -> str:
    return operand.strip().strip("[]()").strip().lower()


def facts(insns: list[tuple[str, tuple[str, ...]]]) -> dict[str, Any]:
    """Structural facts of one slice; no semantics, no ROM, no side effects."""
    mnemonics: set[str] = set()
    callees: set[str] = set()
    labels: list[str] = []
    edges: list[list[str]] = []
    indirect = False
    bank_ops = False
    stack_ops = False
    loops = False
    count = 0
    current = ""

    for mnemonic, operands in insns:
        if mnemonic == "label":
            name = operands[0]
            labels.append(name)
            current = name
            continue
        count += 1
        mnemonics.add(mnemonic)
        if mnemonic == "ldh" or any(
            marker in operand.lower()
            for operand in operands
            for marker in _BANK_MARKERS
        ):
            bank_ops = True
        if mnemonic in {"push", "pop"} or (
            mnemonic in {"add", "ld"} and operands and _bare(operands[0]) == "sp"
        ):
            stack_ops = True
        if mnemonic in _BRANCHES:
            for operand in operands:
                bare = _bare(operand)
                if mnemonic in {"jp", "call"} and bare in _INDIRECT_OPERANDS:
                    indirect = True
                    continue
                if bare in _REGISTERS or not _IDENTIFIER.match(operand.strip()):
                    continue
                target = operand.strip()
                edges.append([current, target])
                if target in labels:
                    loops = True
                elif not target.startswith("."):
                    callees.add(target)

    return {
        "instructions": count,
        "mnemonics": sorted(mnemonics),
        "callees": sorted(callees),
        "indirect": indirect,
        "bank_ops": bank_ops,
        "stack_ops": stack_ops,
        "loops": loops,
        "labels": labels,
        "cfg_edges": edges,
    }


_OVERRIDES: dict[str, dict[str, Any]] | None = None


def overrides() -> dict[str, dict[str, Any]]:
    """Reviewed per-routine corrections; empty when the table is absent."""
    global _OVERRIDES
    if _OVERRIDES is None:
        path = Path(__file__).with_name("analyzer_overrides.toml")
        table: dict[str, Any] = {}
        if path.is_file():
            try:
                with path.open("rb") as stream:
                    table = tomllib.load(stream)
            except (OSError, tomllib.TOMLDecodeError):
                table = {}
        _OVERRIDES = {
            name: value for name, value in table.items() if isinstance(value, dict)
        }
    return _OVERRIDES


def classify(structure: dict[str, Any], *, callees: list[str], name: str) -> str:
    """Bucket one routine, most-constraining rule first.

    Precedence, in this exact order:
      1. reviewed override table entry
      2. ``unsupported`` when no instruction parsed
      3. ``finite-dispatch`` when the slice branches through a register
      4. ``stack-sensitive`` when it pushes, pops, or moves sp
      5. ``bus-banked`` when it touches a bank register or ldh
      6. ``branch-loop`` when a branch targets an earlier label in the slice
      7. ``direct-callee`` when it calls a named symbol
      8. ``direct`` otherwise

    ``event-input`` and ``hardware-transform`` are reachable only through the
    override table: no structural rule can establish either.
    """
    override = overrides().get(name, {})
    reviewed = override.get("feature_class")
    if reviewed in FEATURE_CLASSES:
        return str(reviewed)
    if not structure["instructions"]:
        return "unsupported"
    if structure["indirect"]:
        return "finite-dispatch"
    if structure["stack_ops"]:
        return "stack-sensitive"
    if structure["bank_ops"]:
        return "bus-banked"
    if structure["loops"]:
        return "branch-loop"
    if structure["callees"] or callees:
        return "direct-callee"
    return "direct"


def analyze_routine(routine: dict[str, Any], asm: str) -> dict[str, Any]:
    """Structural record for one routine slice.  Never raises for asm text."""
    name = str(routine.get("name") or "")
    insns = tokenize(asm)
    structure = facts(insns)
    declared = [
        str(callee.get("name"))
        for callee in routine.get("callees") or []
        if isinstance(callee, dict) and callee.get("name")
    ]
    override = overrides().get(name, {})
    diagnostics: list[str] = []
    if not structure["instructions"]:
        diagnostics.append("no instruction parsed from the asm slice")
    for key in sorted(override):
        if key != "feature_class":
            diagnostics.append(f"override {key}={override[key]!r}")
    finite = override.get("finite_indirect_targets")
    return {
        "analyzer_version": VERSION,
        "feature_class": classify(structure, callees=declared, name=name),
        "machine_body_sha256": hashlib.sha256(asm.encode()).hexdigest(),
        "cfg_edges": structure["cfg_edges"],
        "direct_calls": structure["callees"],
        "finite_indirect_targets": list(finite) if isinstance(finite, list) else [],
        "semantic_seed": {
            "instructions": structure["instructions"],
            "labels": len(structure["labels"]),
            "indirect": structure["indirect"],
            "bank_ops": structure["bank_ops"],
            "stack_ops": structure["stack_ops"],
            "loops": structure["loops"],
        },
        "diagnostics": diagnostics,
    }


def _digest(value: Any) -> str:
    if isinstance(value, (bytes, bytearray, memoryview)):
        return hashlib.sha256(bytes(value)).hexdigest()
    if isinstance(value, (str, Path)) and Path(value).is_file():
        return hashlib.sha256(Path(value).read_bytes()).hexdigest()
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


CACHE_INPUTS = ("rom", "symbols", "pret_revision", "analyzer")


def default_inputs(root: Path = common.ROOT) -> dict[str, Any]:
    """The four things that determine a structural analysis of this tree."""
    inventory = root / "site" / "data" / "inventory.json"
    revision = "unknown"
    if inventory.is_file():
        try:
            revision = str(json.loads(inventory.read_text()).get("pret_commit") or "unknown")
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            revision = "unknown"
    return {
        "rom": root / "poketcg" / "poketcg.gbc",
        "symbols": root / "poketcg" / "poketcg.sym",
        "pret_revision": revision,
        "analyzer": Path(__file__).read_bytes(),
    }


def cache_identity(inputs: dict[str, Any]) -> str:
    """Hash every analyzer input, including this module's own bytes."""
    missing = [name for name in CACHE_INPUTS if name not in inputs]
    if missing:
        raise ValueError(f"analyzer cache inputs missing: {', '.join(missing)}")
    canonical = {name: _digest(inputs[name]) for name in CACHE_INPUTS}
    return hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def cache_path(root: Path = common.ROOT) -> Path:
    return root / ".factory" / "v2" / "analyzer.sqlite3"


def cache_records(records: list[dict[str, Any]], *, inputs: dict[str, Any] | None = None,
                  root: Path = common.ROOT) -> str:
    if inputs is None:
        inputs = default_inputs(root)
    identity = cache_identity(inputs)
    path = cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        # Concurrent orchestrators both cache here; the default journal and
        # zero busy timeout turn the second writer into "database is locked".
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=30000")
        db.execute("CREATE TABLE IF NOT EXISTS semantic_index (key TEXT PRIMARY KEY, record TEXT NOT NULL)")
        for record in records:
            key = hashlib.sha256(
                (identity + json.dumps(record, sort_keys=True, separators=(",", ":"))).encode()
            ).hexdigest()
            db.execute(
                "INSERT OR REPLACE INTO semantic_index(key, record) VALUES (?, ?)",
                (key, json.dumps(record, sort_keys=True)),
            )
        db.commit()
    return identity
