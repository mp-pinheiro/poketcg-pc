#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

import common

VERSION = "gb-recompiled-0.1.0-semantic-seed"
FEATURE_CLASSES = (
    "direct", "direct-callee", "branch-loop", "bus-banked", "finite-dispatch",
    "event-input", "hardware-transform", "stack-sensitive", "unsupported",
)


def _body_hash(asm: str) -> str:
    return hashlib.sha256(asm.encode()).hexdigest()


def classify(asm: str, *, size: int = 0, callees: int = 0) -> str:
    text = asm.lower()
    if not text.strip() or "illegal" in text or "unresolved" in text:
        return "unsupported"
    if re.search(r"\b(jp|jr|call)\s*\(\s*(hl|bc)\s*\)", text):
        return "finite-dispatch"
    if re.search(r"\b(rst|halt|stop|wait|joypad|event)\b", text):
        return "event-input"
    if re.search(r"\b(gb_read|gb_write|bankswitch|rsvbk|rvbk|ldh|mapper|wram|sram|vram)\b", text):
        return "bus-banked"
    if re.search(r"\b(ldi|ldd|memcpy|memset|transform|compress|decompress)\b", text):
        return "hardware-transform"
    if re.search(r"\b(ld\s+sp|add\s+sp|push|pop)\b", text):
        return "stack-sensitive"
    if re.search(r"\b(jr|jp)\b", text) and re.search(r"\b(loop|again|next|back)\b", text):
        return "branch-loop"
    if callees or re.search(r"\bcall\b", text):
        return "direct-callee"
    if size > 16 and re.search(r"\b(jr|jp)\b", text):
        return "branch-loop"
    return "direct"


def analyze_routine(routine: dict[str, Any], asm: str) -> dict[str, Any]:
    callees = routine.get("callees") or []
    feature_class = classify(asm, size=int(routine.get("size") or 0), callees=len(callees))
    seed = {
        "entry": routine.get("name"),
        "size": int(routine.get("size") or 0),
        "body_sha256": _body_hash(asm),
        "feature_class": feature_class,
        "consumed_registers": sorted(set(re.findall(r"\b(?:a|f|b|c|d|e|h|l|hl|bc|de|sp)\b", asm.lower()))),
        "reference_edges": sorted(set(re.findall(r"\b(?:call|jp|jr)\s+([A-Za-z_][A-Za-z0-9_]*)", asm))),
    }
    return {
        "analyzer_version": VERSION,
        "feature_class": feature_class,
        "machine_body_sha256": seed["body_sha256"],
        "cfg_edges": seed["reference_edges"],
        "direct_calls": seed["reference_edges"] if feature_class == "direct-callee" else [],
        "finite_indirect_targets": [],
        "semantic_seed": seed,
        "diagnostics": [],
    }


def cache_path(root: Path = common.ROOT) -> Path:
    return root / ".factory" / "v2" / "analyzer.sqlite3"


def cache_records(records: list[dict[str, Any]], *, root: Path = common.ROOT) -> str:
    path = cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS semantic_index (key TEXT PRIMARY KEY, record TEXT NOT NULL)")
        for record in records:
            key = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            db.execute("INSERT OR REPLACE INTO semantic_index(key, record) VALUES (?, ?)", (key, json.dumps(record, sort_keys=True)))
        db.commit()
    return hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def analyze_packet(packet: dict[str, Any]) -> dict[str, Any]:
    records = []
    for routine in packet.get("routines") or []:
        records.append(analyze_routine(routine, str(routine.get("asm") or "")))
    return {
        "analyzer_version": VERSION,
        "records": records,
        "cache_sha256": cache_records(records),
    }
