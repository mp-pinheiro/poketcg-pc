#!/usr/bin/env python3
"""How far the port tracks the ROM through a TAS movie, and what stops it."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import native_trace


class ProgressError(RuntimeError):
    pass


def basename_of(path: str) -> str:
    return Path(path).stem


def case_basenames() -> dict[str, str]:
    import importlib.util

    mapping: dict[str, str] = {}
    for path in sorted((ROOT / "tests" / "cases").glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"case_{path.stem}", path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as exc:  # noqa: BLE001 - a broken case module must not stop the gate
            print(f"skipped {path.name}: {exc}", file=sys.stderr)
            continue
        for name in getattr(module, "CONTRACT", {}):
            mapping.setdefault(name, path.stem)
    return mapping


def run_native(binary: Path, pack: Path, masks: Path, frames: int, trace: Path) -> None:
    result = subprocess.run(
        [str(binary), "--headless", "--data-pack", str(pack), "--frames", str(frames),
         "--input", str(masks), "--trace-calls", str(trace)],
        cwd=ROOT, capture_output=True, text=True, timeout=1800, check=False,
    )
    if result.returncode != 0:
        raise ProgressError(f"native run failed: {result.stderr.strip()[:300]}")


def report(
    reference_path: Path, binary: Path, trace: Path, limit: int
) -> dict[str, Any]:
    reference = json.loads(reference_path.read_text())
    rows = {row["routine"]: row for row in reference["calls"]}
    if not rows or "first_ordinal" not in next(iter(rows.values())):
        raise ProgressError(f"{reference_path} lacks first_ordinal; re-run refstream trace")
    native, _first, overflow, records = native_trace.native_counts(binary, trace)
    symbols = {name for _address, name in native_trace.load_symbols(binary)}
    inventory = json.loads((ROOT / "site" / "data" / "inventory.json").read_text())["functions"]
    owners = case_basenames()

    # A reference routine the port has no symbol for is not comparable: the port
    # inlines local labels, and bank trampolines like BankpushROM have no C body
    # by design. Only a routine the binary exports can be called and missed.
    comparable = {name for name in rows if name in symbols}
    reached = {name for name in comparable if name in native}
    missing = sorted(
        (rows[name]["first_ordinal"], name) for name in comparable - reached
    )
    reached_ordinal = max((rows[name]["first_ordinal"] for name in reached), default=0)
    total_ordinals = int(reference.get("ordinals_reached") or 0)

    # A routine the ROM first runs at an ordinal the port already passed cannot
    # be what stops it: the port demonstrably got there without it. Those are
    # structural differences (bank trampolines, dispatch the port inlines).
    # Only misses at or beyond the frontier can block progress.
    frontier = [(ordinal, name) for ordinal, name in missing if ordinal >= reached_ordinal]
    structural = len(missing) - len(frontier)

    blockers = []
    for ordinal, name in frontier[:limit]:
        source = inventory.get(name, {}).get("file", "")
        blockers.append({
            "routine": name,
            "reference_first_ordinal": ordinal,
            "reference_calls": rows[name]["count"],
            "source": source,
            "basename": owners.get(name, basename_of(source) if source else "?"),
        })
    by_basename: dict[str, int] = {}
    for _ordinal, name in frontier:
        source = inventory.get(name, {}).get("file", "")
        key = owners.get(name, basename_of(source) if source else "?")
        by_basename[key] = by_basename.get(key, 0) + 1
    return {
        "schema": 1,
        "format": "tas-progress-v1",
        "reference": str(reference_path.relative_to(ROOT)),
        "native_records": records,
        "native_overflow": overflow,
        "reference_ordinals": total_ordinals,
        "reached_ordinal": reached_ordinal,
        "progress_pct": round(100.0 * reached_ordinal / total_ordinals, 2) if total_ordinals else None,
        "comparable_routines": len(comparable),
        "reached_routines": len(reached),
        "missing_routines": len(missing),
        "structural_misses": structural,
        "frontier_misses": len(frontier),
        "blockers": blockers,
        "frontier_by_basename": dict(sorted(by_basename.items(), key=lambda kv: -kv[1])),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", default="build/completion/tas/ref-5530b.json")
    parser.add_argument("--masks", default="build/completion/tas/input.txt")
    parser.add_argument("--binary", default="build-trace/poketcg")
    parser.add_argument("--pack", default="build/completion/data-pack.bin")
    parser.add_argument("--trace", default="build/completion/tas/native-progress.bin")
    parser.add_argument("--frames", type=int, default=78207)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--skip-run", action="store_true", help="reuse an existing trace")
    parser.add_argument("--json")
    args = parser.parse_args(argv)

    def resolve(value: str) -> Path:
        path = Path(value)
        return path if path.is_absolute() else ROOT / path

    try:
        if not args.skip_run:
            run_native(resolve(args.binary), resolve(args.pack), resolve(args.masks),
                       args.frames, resolve(args.trace))
        payload = report(resolve(args.reference), resolve(args.binary),
                         resolve(args.trace), args.limit)
    except (ProgressError, OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.json:
        resolve(args.json).write_text(text + "\n")
    print(text)
    return 0 if not payload["missing_routines"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
