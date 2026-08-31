#!/usr/bin/env python3
"""Validate the versioned, oracle-neutral scenario corpus format."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = 2
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_FIELDS = {
    "schema", "scenario", "base_snapshot_sha256", "input", "patches",
    "event_anchors", "bounds", "terminal", "required_symbols", "required_edges",
    "checkpoints", "expected", "oracles", "feature_config",
}


class CorpusError(ValueError):
    pass


def input_hash(rle: list[dict[str, int]]) -> str:
    encoded = json.dumps(rle, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def encode_rle(frames: list[int]) -> list[dict[str, int]]:
    result: list[dict[str, int]] = []
    for buttons in frames:
        if not isinstance(buttons, int) or not 0 <= buttons <= 0xFF:
            raise CorpusError("input buttons must be bytes")
        if result and result[-1]["buttons"] == buttons:
            result[-1]["frames"] += 1
        else:
            result.append({"buttons": buttons, "frames": 1})
    return result


def decode_rle(rle: list[dict[str, int]]) -> list[int]:
    frames: list[int] = []
    for entry in rle:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("buttons"), int)
            or not isinstance(entry.get("frames"), int)
            or not 0 <= entry["buttons"] <= 0xFF
            or entry["frames"] < 1
        ):
            raise CorpusError("malformed RLE input entry")
        frames.extend([entry["buttons"]] * entry["frames"])
    return frames


def require_hash(value: object, field: str) -> None:
    if not isinstance(value, str) or not HASH_RE.fullmatch(value):
        raise CorpusError(f"{field} is not a SHA-256")


def validate(record: dict[str, Any]) -> dict[str, Any]:
    if record.get("schema") != SCHEMA:
        raise CorpusError("corpus schema is not version 2")
    missing = sorted(REQUIRED_FIELDS - record.keys())
    if missing:
        raise CorpusError("corpus missing fields: " + ",".join(missing))
    if not isinstance(record.get("scenario"), str) or not record["scenario"]:
        raise CorpusError("corpus scenario is missing")
    require_hash(record["base_snapshot_sha256"], "base_snapshot_sha256")
    input_record = record["input"]
    if not isinstance(input_record, dict):
        raise CorpusError("corpus input is not an object")
    rle = input_record.get("rle")
    if not isinstance(rle, list):
        raise CorpusError("corpus input RLE is missing")
    frames = decode_rle(rle)
    if input_record.get("sha256") != input_hash(rle):
        raise CorpusError("corpus input hash differs from RLE")
    bounds = record["bounds"]
    if (
        not isinstance(bounds, dict)
        or not isinstance(bounds.get("min_frames"), int)
        or not isinstance(bounds.get("max_frames"), int)
        or bounds["min_frames"] < 0
        or bounds["max_frames"] < bounds["min_frames"]
        or len(frames) < bounds["min_frames"]
    ):
        raise CorpusError("corpus frame bounds are invalid")
    terminal = record["terminal"]
    if not isinstance(terminal, dict) or not isinstance(terminal.get("event"), str):
        raise CorpusError("corpus terminal predicate is missing")
    anchors = record["event_anchors"]
    if not isinstance(anchors, list) or any(
        not isinstance(anchor, dict)
        or not isinstance(anchor.get("event"), str)
        or not isinstance(anchor.get("frame"), int)
        or anchor["frame"] < 0
        for anchor in anchors
    ):
        raise CorpusError("corpus event anchors are invalid")
    for field in ("patches", "required_symbols", "required_edges", "checkpoints", "oracles"):
        if not isinstance(record[field], list):
            raise CorpusError(f"corpus {field} is not a list")
    expected = record["expected"]
    if not isinstance(expected, dict):
        raise CorpusError("corpus expected output is missing")
    for field in ("state_sha256", "pixels_sha256", "audio_sha256", "save_sha256"):
        require_hash(expected.get(field), f"expected.{field}")
    if not isinstance(record["feature_config"], dict):
        raise CorpusError("corpus feature configuration is not an object")
    return {
        "scenario": record["scenario"],
        "frames": len(frames),
        "events": len(anchors),
        "oracles": len(record["oracles"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        record = json.loads(args.check.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            raise CorpusError("corpus is not an object")
        summary = validate(record)
    except (OSError, json.JSONDecodeError, CorpusError) as exc:
        print(f"corpus: FAIL {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"schema": SCHEMA, "status": "PASS", **summary}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
