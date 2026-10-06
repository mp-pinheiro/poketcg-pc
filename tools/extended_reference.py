#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "profiles" / "extended" / "reference.toml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    args = parser.parse_args()
    contract = tomllib.loads(args.contract.read_text())
    namespace = ROOT / contract["session_namespace"]
    ratchet = ROOT / contract["ratchet"]
    records = json.loads(ratchet.read_text()) if ratchet.is_file() else {}
    failures = []
    for name in contract["required"]:
        directory = namespace / name
        record = records.get(name, {})
        if not (directory / "session.json").is_file() or not (directory / "input.txt").is_file():
            failures.append(f"{name}: missing session")
            continue
        meta = json.loads((directory / "session.json").read_text())
        length = int(meta.get("length", 0))
        confirmed = int(record.get("confirmed_ordinal", -1))
        if length < 1 or confirmed != length:
            failures.append(f"{name}: ratchet {confirmed} != length {length}")
    if failures:
        for failure in failures:
            print(failure)
        return 1
    print("extended-reference: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
