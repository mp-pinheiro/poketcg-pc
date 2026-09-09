#!/usr/bin/env python3
"""Audit case declarations before they enter a primary or release gate."""

from __future__ import annotations

import argparse
import re
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "oracle"))

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests" / "cases"))
sys.path.insert(0, str(ROOT))
from schema import SchemaValidationError, validate_cases
sys.path.insert(0, str(ROOT / "tests"))
from routines import ALL, EXCLUSIONS

ALLOWED_EXCLUSION_KINDS = {
    "dead-zero-callsites",
    "hardware-transform",
    "sgb-only",
    "fallthrough-only",
    "trampoline-direct-call",
    "dependency-pending",
}

def load_modules(only: str | None = None) -> list[tuple[Path, object]]:
    result = []
    for path in sorted((ROOT / "tests/cases").glob("*.py")):
        if path.name == "__init__.py":
            continue
        if only is not None and path.stem != only:
            continue
        spec = importlib.util.spec_from_file_location(f"audit_{path.stem}", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result.append((path, module))
    return result

MARKER = re.compile(r"^# (>>>|<<<) (factory(?:-mutation|-completion|-cases-statics)?) (\w+)[ \t]*$")
C_BLOCK = re.compile(r"^/\* >>> factory (\w+) \*/$", re.M)


def marker_faults(path: Path) -> list[str]:
    """Every `# >>> kind fn` closed by its own `# <<< kind fn` before the next
    opener: a whole-file copy from a stale workspace erases sibling blocks and
    leaves exactly these orphans behind."""
    faults = []
    open_block = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = MARKER.match(line)
        if match is None:
            continue
        side, kind, fn = match.groups()
        if side == ">>>":
            if open_block is not None:
                faults.append(f"{open_block[0]} {open_block[1]} opened at line {open_block[2]} is never closed")
            open_block = (kind, fn, number)
        elif open_block is None or (kind, fn) != open_block[:2]:
            faults.append(f"line {number}: `# <<< {kind} {fn}` closes "
                          f"{'nothing' if open_block is None else f'{open_block[0]} {open_block[1]}'}")
            open_block = None
        else:
            open_block = None
    if open_block is not None:
        faults.append(f"{open_block[0]} {open_block[1]} opened at line {open_block[2]} is never closed")
    return faults


def uncased_routines(modules: list[tuple[Path, object]]) -> list[tuple[str, str]]:
    """Routines with a factory C body and no case in their basename's module
    nor an exclusion: the oracle never runs them, so a lost block is silent."""
    cased: set[str] = set()
    for _path, module in modules:
        for fn in getattr(module, "SCHEMA2_CASES", {}) or getattr(module, "CASES", {}):
            cased.add(fn)
            # A local-label entry (`Script_f631.ows_f63c`, docs/port-contract.md's
            # script entry continuation) is cased under the ROM symbol; its C
            # block carries the identifier form.
            cased.add(fn.replace(".", "_"))
    excluded = {fn for entries in EXCLUSIONS.values() if isinstance(entries, dict) for fn in entries}
    missing = []
    for source in sorted((ROOT / "src/home").glob("*.c")):
        for fn in C_BLOCK.findall(source.read_text()):
            if fn != "statics" and fn not in cased and fn not in excluded:
                missing.append((source.name, fn))
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("routine", "release"), required=True)
    parser.add_argument("--only", help="restrict per-module checks to this basename")
    args = parser.parse_args()
    failures = 0
    all_modules = load_modules()
    modules = all_modules if args.only is None else [
        (path, module) for path, module in all_modules if path.stem == args.only
    ]
    for basename, entries in EXCLUSIONS.items():
        if not isinstance(entries, dict):
            print(f"EXCLUSION {basename}: entries must be a mapping")
            failures += 1
            continue
        owned = set()
        for path, module in all_modules:
            if path.stem == basename:
                owned = set(getattr(module, "SCHEMA2_CASES", {}))
                break
        for fn, exclusion in entries.items():
            if fn not in ALL:
                print(f"EXCLUSION {basename}:{fn}: not in registry")
                failures += 1
            if not isinstance(exclusion, dict) or any(
                not isinstance(exclusion.get(key), str) or not exclusion[key].strip()
                for key in ("kind", "source", "reason")
            ):
                print(f"EXCLUSION {basename}:{fn}: requires kind/source/reason")
                failures += 1
                continue
            match = re.fullmatch(r"(.+):([1-9][0-9]*)-([1-9][0-9]*)", exclusion["source"])
            if match is None:
                print(f"EXCLUSION {basename}:{fn}: source must include line range")
                failures += 1
                continue
            source = ROOT / match.group(1)
            start, end = int(match.group(2)), int(match.group(3))
            if not source.is_file():
                print(f"EXCLUSION {basename}:{fn}: missing source {exclusion['source']}")
                failures += 1
            elif not start <= end <= len(source.read_text().splitlines()):
                print(f"EXCLUSION {basename}:{fn}: source range out of bounds")
                failures += 1
            if fn in owned:
                print(f"EXCLUSION {basename}:{fn}: cannot also declare schema cases")
                failures += 1
            if args.stage == "release" and exclusion["kind"] == "dependency-pending":
                print(f"EXCLUSION dependency-pending blocks release {basename}:{fn}")
                failures += 1
    for path in sorted((ROOT / "tests/cases").glob("*.py")):
        for fault in marker_faults(path):
            print(f"MARKERS {path.name}: {fault}")
            failures += 1
    if args.only is None:
        for source, fn in uncased_routines(all_modules):
            print(f"UNCASED {source}: {fn} has a factory body and no case")
            failures += 1
    for path, module in modules:
        if not hasattr(module, "SCHEMA2_CASES") and getattr(module, "CASES", {}):
            print(f"MIGRATION_PENDING {path}: legacy CASES has no SCHEMA2_CASES")
            failures += 1
            continue
        cases = getattr(module, "SCHEMA2_CASES", {})
        flattened = {}
        for fn, records in cases.items():
            if not isinstance(records, list):
                print(f"SCHEMA {path}: {fn} cases must be a list")
                failures += 1
                continue
            for record in records:
                if not isinstance(record, dict) or not isinstance(record.get("id"), str):
                    print(f"SCHEMA {path}: {fn} case must have a stable id")
                    failures += 1
                    continue
                flattened[record["id"]] = record
        try:
            validate_cases(flattened)
        except SchemaValidationError as exc:
            print(f"SCHEMA {path}: {exc}")
            failures += 1
        if args.stage == "release":
            mutations = getattr(module, "MUTATIONS", None)
            if flattened and not isinstance(mutations, dict):
                print(f"SCHEMA {path}: release stage requires MUTATIONS mapping")
                failures += 1
            elif flattened and not mutations:
                print(f"SCHEMA {path}: release stage requires non-empty MUTATIONS")
                failures += 1
    if failures:
        print(f"AUDIT_FAIL stage={args.stage} failures={failures}")
        return 2
    print(f"AUDIT_OK stage={args.stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
