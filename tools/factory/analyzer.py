#!/usr/bin/env python3
"""Pinned GB Recompiled semantic analyzer boundary.

This module deliberately has no textual classifier.  Semantic records are only
accepted from the pinned GB Recompiled executable; when it is unavailable the
factory stops rather than inventing a feature class.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
from pathlib import Path
from typing import Any

import common

VERSION = "gb-recompiled-0.1.0"
ABI = "0.1.0"
FEATURE_CLASSES = (
    "direct", "direct-callee", "branch-loop", "bus-banked", "finite-dispatch",
    "event-input", "hardware-transform", "stack-sensitive", "unsupported",
)


class AnalyzerUnavailable(RuntimeError):
    """The pinned analyzer cannot provide authoritative semantic facts."""


def tool_path(root: Path = common.ROOT) -> Path:
    configured = os.environ.get("FACTORY_GBRECOMP")
    candidate = Path(configured) if configured else root / ".factory" / "tools" / "gbrecomp" / "0.1.0" / "gbrecomp"
    if not candidate.is_file() or not os.access(candidate, os.X_OK):
        raise AnalyzerUnavailable(f"GB Recompiled 0.1.0 is unavailable: {candidate}")
    return candidate


def tool_version(root: Path = common.ROOT) -> dict[str, Any]:
    path = tool_path(root)
    try:
        completed = subprocess.run([str(path), "--version-json"], check=True, capture_output=True, text=True)
        value = json.loads(completed.stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise AnalyzerUnavailable("GB Recompiled --version-json failed") from exc
    if not isinstance(value, dict) or value.get("version") != ABI or value.get("abi") != ABI:
        raise AnalyzerUnavailable("GB Recompiled version/ABI is not pinned to 0.1.0")
    return value

def _digest(value: Any) -> str:
    if isinstance(value, (bytes, bytearray, memoryview)):
        return hashlib.sha256(bytes(value)).hexdigest()
    if isinstance(value, (str, os.PathLike)) and Path(value).is_file():
        return hashlib.sha256(Path(value).read_bytes()).hexdigest()
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def cache_identity(inputs: dict[str, Any]) -> str:
    """Hash every analyzer input, including policy and wrapper identity."""
    required = ("rom", "symbols", "map", "pret_revision", "version", "annotations", "policy", "gate", "wrapper")
    missing = [name for name in required if name not in inputs]
    if missing:
        raise ValueError(f"analyzer cache inputs missing: {', '.join(missing)}")
    canonical = {name: _digest(inputs[name]) for name in required}
    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def cache_path(root: Path = common.ROOT) -> Path:
    return root / ".factory" / "v2" / "analyzer.sqlite3"


def cache_records(records: list[dict[str, Any]], *, inputs: dict[str, Any] | None = None, root: Path = common.ROOT) -> str:
    if inputs is None:
        raise ValueError("analyzer cache identity inputs are required")
    identity = cache_identity(inputs)
    path = cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS semantic_index (key TEXT PRIMARY KEY, record TEXT NOT NULL)")
        for record in records:
            key = hashlib.sha256((identity + json.dumps(record, sort_keys=True, separators=(",", ":"))).encode()).hexdigest()
            db.execute("INSERT OR REPLACE INTO semantic_index(key, record) VALUES (?, ?)", (key, json.dumps(record, sort_keys=True)))
        db.commit()
    return identity


def analyze_routine(routine: dict[str, Any], asm: str, *, analysis: dict[str, Any] | None = None, root: Path = common.ROOT) -> dict[str, Any]:
    """Validate one result emitted by GB Recompiled; never infer from assembly text."""
    version = tool_version(root)
    result = analysis if analysis is not None else routine.get("gbrecomp_result")
    if not isinstance(result, dict):
        raise AnalyzerUnavailable("GB Recompiled result is required; textual assembly classification is disabled")
    feature = result.get("feature_class")
    if feature not in FEATURE_CLASSES:
        raise AnalyzerUnavailable("GB Recompiled result has no reviewed feature class")
    return {
        "analyzer_version": VERSION,
        "tool_version": version,
        "feature_class": feature,
        "machine_body_sha256": str(result.get("machine_body_sha256", "")),
        "cfg_edges": list(result.get("cfg_edges", [])),
        "direct_calls": list(result.get("direct_calls", [])),
        "finite_indirect_targets": list(result.get("finite_indirect_targets", [])),
        "semantic_seed": dict(result.get("semantic_seed", {})),
        "diagnostics": list(result.get("diagnostics", [])),
    }


def analyze_packet(packet: dict[str, Any], *, root: Path = common.ROOT) -> dict[str, Any]:
    version = tool_version(root)
    records = [analyze_routine(routine, str(routine.get("asm") or ""), root=root) for routine in packet.get("routines") or []]
    inputs = packet.get("analyzer_inputs")
    if not isinstance(inputs, dict):
        raise AnalyzerUnavailable("packet lacks complete analyzer_inputs for content-addressed cache")
    inputs = dict(inputs)
    inputs["version"] = version
    inputs.setdefault("wrapper", Path(__file__).read_bytes())
    return {"analyzer_version": VERSION, "records": records, "cache_sha256": cache_records(records, inputs=inputs, root=root)}

def mutation_inputs(consumed_registers: list[str] | tuple[str, ...], *, limit: int = 128) -> list[dict[str, int]]:
    """Generate deterministic boundary/poison seeds for the exploration worker."""
    if limit < 1:
        return []
    names = tuple(dict.fromkeys(str(name) for name in consumed_registers))
    values = (0, 1, 0xFF, 0x100, 0x7FFF, 0x8000, 0xFFFF)
    result: list[dict[str, int]] = []
    for name in names:
        for value in values:
            if len(result) >= limit:
                return result
            result.append({name: value})
    if len(result) < limit:
        result.append({name: 0xA5A5 for name in names})
    return result[:limit]
