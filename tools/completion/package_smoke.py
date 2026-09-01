#!/usr/bin/env python3
"""Stage and exercise a ROM-free production package."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BINARY = ROOT / "build" / "poketcg"
DEFAULT_PACK = ROOT / "build" / "completion" / "data-pack.bin"
DEFAULT_PACKAGE = ROOT / "build" / "completion" / "package"
FORBIDDEN_SUFFIXES = {".gbc", ".sym", ".map", ".asm", ".dis"}


def fail(message: str) -> None:
    raise ValueError(message)


def run_binary(binary: Path, pack: Path, frames: int, *extra: str) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("POKETCG_ROM", None)
    return subprocess.run(
        [str(binary), "--headless", "--data-pack", str(pack), "--frames", str(frames), *extra],
        cwd=binary.parent,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, default=DEFAULT_BINARY)
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--package", dest="package_dir", type=Path, default=DEFAULT_PACKAGE)
    parser.add_argument("--frames", type=int, default=600)
    args = parser.parse_args(argv)
    try:
        if args.frames < 1:
            fail("--frames must be positive")
        if not args.binary.is_file() or not os.access(args.binary, os.X_OK):
            fail(f"missing executable: {args.binary}")
        if not args.pack.is_file():
            fail(f"missing data pack: {args.pack}")
        if args.package_dir.exists():
            fail(f"package directory already exists: {args.package_dir}")
        args.package_dir.parent.mkdir(parents=True, exist_ok=True)
        args.package_dir.mkdir()
        staged_binary = args.package_dir / "poketcg"
        staged_pack = args.package_dir / "data-pack.bin"
        shutil.copy2(args.binary, staged_binary)
        shutil.copy2(args.pack, staged_pack)
        staged_binary.chmod(staged_binary.stat().st_mode | 0o111)
        contents = sorted(path.relative_to(args.package_dir).as_posix() for path in args.package_dir.rglob("*"))
        expected_contents = ["data-pack.bin", "poketcg"]
        if contents != expected_contents:
            fail(f"package contents differ: {contents}")
        forbidden = [
            path.as_posix() for path in args.package_dir.rglob("*")
            if path.is_file() and path.suffix.casefold() in FORBIDDEN_SUFFIXES
        ]
        if forbidden:
            fail("forbidden ROM/build artifact in package: " + ",".join(forbidden))
        check = subprocess.run(
            [
                sys.executable, str(ROOT / "tools" / "gen_data.py"), "--pack-check",
                "--pack", str(staged_pack),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if check.returncode:
            fail("staged data pack failed verification: " + (check.stderr or check.stdout).strip())
        trace_path = args.package_dir.parent / "production-trace.json"
        smoke = run_binary(
            staged_binary, Path("data-pack.bin"), args.frames,
            "--trace-entries", str(trace_path),
        )
        if smoke.returncode != 0:
            fail(f"packaged executable failed: {smoke.stderr.strip()}")
        if f"frames: {args.frames}" not in smoke.stdout:
            fail(f"packaged executable did not render {args.frames} frames: {smoke.stdout.strip()}")
        missing = run_binary(staged_binary, Path("data-pack.bin"), 1, "--require-data", "00:4000")
        if "MISSING_DATA 00:4000" not in missing.stderr or missing.returncode == 0:
            fail("missing production span did not fail with MISSING_DATA bank:addr")
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 2
    package_path = args.package_dir.resolve()
    try:
        package_label = str(package_path.relative_to(ROOT))
    except ValueError:
        package_label = str(package_path)
    print(json.dumps({
        "status": "PASS",
        "package": package_label,
        "contents": expected_contents,
        "frames": args.frames,
        "missing_span": "MISSING_DATA 00:4000",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
