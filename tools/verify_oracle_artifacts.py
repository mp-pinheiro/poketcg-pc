#!/usr/bin/env python3
"""Verify immutable inputs used by the function oracles."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tools" / "oracle" / "artifacts.json"


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str) -> int:
    print(f"ARTIFACT {message}", file=sys.stderr)
    return 2


def verify_pret(root: Path, manifest: dict, commit_only: bool = False) -> int:
    checkout = root / "poketcg"
    if not checkout.is_dir():
        return fail(f"missing checkout {checkout}")
    expected_commit = manifest["pret"]["commit"]
    actual_commit = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    if not actual_commit.startswith(expected_commit):
        return fail(f"pret commit expected={expected_commit} actual={actual_commit}")
    if commit_only:
        print(f"ARTIFACT pret commit={actual_commit}")
        return 0
    rom = checkout / "poketcg.gbc"
    if not rom.is_file():
        return fail(f"missing ROM {rom}")
    expected_rom = manifest["pret"]["rom_sha1"]
    actual_rom = digest(rom, "sha1")
    if actual_rom != expected_rom:
        return fail(f"ROM sha1 expected={expected_rom} actual={actual_rom}")
    print(f"ARTIFACT pret commit={actual_commit} rom_sha1={actual_rom}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--commit-only", action="store_true")
    args = parser.parse_args()
    manifest = json.loads((args.root / "tools/oracle/artifacts.json").read_text())
    return verify_pret(args.root, manifest, args.commit_only)

if __name__ == "__main__":
    raise SystemExit(main())
