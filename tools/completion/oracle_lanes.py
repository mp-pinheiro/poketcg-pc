#!/usr/bin/env python3
"""Independent lane serializers and health reporting."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def serialize_gbrt(registers: dict[str, int], bus: list[dict[str, int]], state: dict[str, Any]) -> bytes:
    return json.dumps({
        "lane": "gbrt-native",
        "registers": registers,
        "bus": bus,
        "state": state,
    }, sort_keys=True, separators=(",", ":")).encode()


def parse_gbrt(payload: bytes) -> dict[str, Any]:
    value = json.loads(payload)
    if value.get("lane") != "gbrt-native" or not isinstance(value.get("registers"), dict):
        raise ValueError("invalid GBRT lane record")
    return value


def serialize_pyboy(registers: dict[str, int], domains: dict[str, bytes], io: bytes) -> bytes:
    return json.dumps({
        "lane": "pyboy",
        "registers": registers,
        "domains": {name: data.hex() for name, data in sorted(domains.items())},
        "io": io.hex(),
    }, sort_keys=True, separators=(",", ":")).encode()


def parse_pyboy(payload: bytes) -> dict[str, Any]:
    value = json.loads(payload)
    if value.get("lane") != "pyboy" or not isinstance(value.get("domains"), dict):
        raise ValueError("invalid PyBoy lane record")
    return value


def serialize_oracle_b(frames: int, state: dict[str, Any], save_state_sha256: str) -> bytes:
    return json.dumps({
        "lane": "oracle-b",
        "frames": frames,
        "state": state,
        "save_state_sha256": save_state_sha256,
    }, sort_keys=True, separators=(",", ":")).encode()


def parse_oracle_b(payload: bytes) -> dict[str, Any]:
    value = json.loads(payload)
    if value.get("lane") != "oracle-b" or not isinstance(value.get("frames"), int):
        raise ValueError("invalid Oracle-B lane record")
    return value


def serialize_bizhawk(domains: dict[str, bytes], registers: dict[str, int], trace: list[dict[str, int]]) -> bytes:
    return json.dumps({
        "lane": "bizhawk-gambatte",
        "domains": {name: data.hex() for name, data in sorted(domains.items())},
        "registers": registers,
        "trace": trace,
    }, sort_keys=True, separators=(",", ":")).encode()


def parse_bizhawk(payload: bytes) -> dict[str, Any]:
    value = json.loads(payload)
    if value.get("lane") != "bizhawk-gambatte" or not isinstance(value.get("domains"), dict):
        raise ValueError("invalid BizHawk lane record")
    return value


def _available(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def health() -> dict[str, dict[str, Any]]:
    gbrt = ROOT / "tools" / "oracle" / "gbref" / "build" / "gbref_runner"
    oracle_b = Path(os.environ.get(
        "POKETCG_ORACLEB", str(Path.home() / ".local/share/gbrecompiled/poketcg/poketcg")
    ))
    return {
        "gbrt-native": {
            "status": "PASS" if _available(gbrt) else "UNAVAILABLE",
            "path": str(gbrt.relative_to(ROOT)) if gbrt.is_relative_to(ROOT) else str(gbrt),
        },
        "pyboy": {
            "status": "PASS" if (ROOT / "tools" / "oracle" / "pyboy_oracle.py").is_file() else "UNAVAILABLE",
            "path": "tools/oracle/pyboy_oracle.py",
        },
        "oracle-b": {
            "status": "PASS" if _available(oracle_b) else "UNAVAILABLE",
            "path": str(oracle_b),
        },
        "bizhawk-gambatte": {
            "status": "PASS" if (ROOT / "tools" / "completion" / "bizhawk_capture.lua").is_file() else "UNAVAILABLE",
            "path": "tools/completion/bizhawk_capture.lua",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--health", action="store_true")
    args = parser.parse_args(argv)
    if not args.health:
        parser.error("--health is required")
    result = health()
    print(json.dumps({"schema": 1, "lanes": result}, sort_keys=True))
    return 0 if all(item["status"] == "PASS" for item in result.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
