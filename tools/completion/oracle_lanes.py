#!/usr/bin/env python3
"""Independent lane health reporting."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


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
        "gambatte-headless": {
            "status": "PASS" if _available(ROOT / "tools/completion/gambatte_runner.py") else "UNAVAILABLE",
            "path": "tools/completion/gambatte_runner.py",
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
