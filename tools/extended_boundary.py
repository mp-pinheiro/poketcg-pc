#!/usr/bin/env python3
"""Build the Extended boundary fixture and oracle-check the native port against it.

The fixture copies the pinned Extended checkout, pads CardPointers to $1ff
entries whose records at $00fe, $00ff, $0100 and $01ff duplicate card 1, sets
NUM_CARDS to $1ff, builds that ROM, generates its inventory and configures a
native Extended tree against it, then runs tests/profiles/extended/boundary
through the live oracle. The record names which lookups passed and that $0200
is rejected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.profiles import get_profile

BOUNDARY_IDS = (0x00FE, 0x00FF, 0x0100, 0x01FF)
REJECTED_ID = 0x0200
CASE_PATH = "tests/profiles/extended/boundary"
RESULT_RE = re.compile(r"^(PASS|FAIL) (\S+?): (\d+)(?:/(\d+))? cases")
CASE_RE = re.compile(r"^  (ok|fail)\s+(\S+?)\[(\d+)\]")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def patch_fixture(source: Path) -> None:
    pointers = source / "src" / "data" / "card_pointers.asm"
    lines = pointers.read_text().splitlines()
    start = next(index for index, line in enumerate(lines) if line.startswith("\tdab "))
    end = next(index for index in range(start, len(lines)) if lines[index] == "\tdwb NULL, $0")
    entries = lines[start:end]
    if not entries:
        raise SystemExit("Extended CardPointers has no card entries")
    while len(entries) < 0x1FF:
        entries.append(entries[-1])
    for card_id in BOUNDARY_IDS:
        entries[card_id - 1] = entries[0]
    pointers.write_text("\n".join(lines[:start] + entries + lines[end:]) + "\n")
    constants = source / "src" / "constants" / "card_constants.asm"
    text = constants.read_text()
    marker = "DEF NUM_CARDS EQU const_value - 1"
    if marker not in text:
        raise SystemExit("Extended NUM_CARDS definition not found")
    constants.write_text(text.replace(marker, "DEF NUM_CARDS EQU $1ff", 1))


def run(command: list[str], cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise SystemExit(f"{' '.join(command)} failed:\n{result.stdout[-2000:]}{result.stderr[-2000:]}")
    return result.stdout


def build_fixture(root: Path, workdir: Path) -> tuple[Path, Path]:
    profile = get_profile("extended", root)
    source = workdir / profile.checkout
    if source.exists():
        shutil.rmtree(source)
    shutil.copytree(profile.source_path(root), source, ignore=shutil.ignore_patterns(".git"))
    patch_fixture(source)
    rgbasm = shutil.which("rgbasm")
    if rgbasm is None:
        raise SystemExit("RGBDS 1.0.0 is required for the Extended boundary fixture")
    rgbds = str(Path(rgbasm).parent) + "/"
    run(["make", "-C", str(source), "clean"])
    run(["make", "-C", str(source), "DEBUG=1", f"RGBDS={rgbds}"])
    rom = source / profile.rom_name
    if not rom.is_file():
        raise SystemExit(f"boundary fixture ROM missing: {rom}")
    inventory = workdir / "inventory.json"
    run([sys.executable, "tools/progress/inventory.py", "--profile", "extended",
         "--source", str(source), "--output", str(inventory)])
    return source, inventory


def build_native(root: Path, workdir: Path, source: Path, inventory: Path) -> Path:
    native = workdir / "native"
    run(["cmake", "-G", "Ninja", "-B", str(native), "-DCMAKE_BUILD_TYPE=RelWithDebInfo",
         "-DPOKETCG_ENABLE_EXTENDED=ON", f"-DPOKETCG_EXTENDED_DISASM={source}",
         f"-DPOKETCG_EXTENDED_INVENTORY={inventory}", "-DPORT_FILES="])
    jobs = os.environ.get("POKETCG_NINJA_JOBS", "-j2")
    run(["ninja", jobs, "-C", str(native), "poketcg_extended_probe", "poketcg-extended"])
    profile = get_profile("extended", root)
    probe = native / profile.probe
    if not probe.is_file():
        raise SystemExit(f"boundary native probe missing: {probe}")
    pack = native / "completion" / "data-pack.bin"
    run([sys.executable, "tools/gen_data.py", "--profile", "extended",
         "--rom", str(source / profile.rom_name), "--map", str(source / profile.map_name),
         "--sym", str(source / profile.sym_name), "--inventory", str(inventory),
         "--sparse-pack", "--pack", str(pack), "--pack-manifest", str(pack.with_suffix(".json"))])
    return probe


def run_oracle(root: Path, rom: Path, probe: Path) -> tuple[dict[str, dict[str, int]], dict[str, str]]:
    env = dict(os.environ)
    env.update({"POKETCG_PROFILE": "extended", "POKETCG_CASE_PATH": CASE_PATH, "POKETCG_ROM": str(rom)})
    result = subprocess.run(
        ["uv", "run", "--project", "tools/oracle", "--frozen", "--python", "3.12.3", "python",
         "tests/test_leaves.py", "--group", "boundary", "--oracle-mode", "live",
         "--probe", str(probe), "--rom", str(rom)],
        cwd=root, env=env, text=True, capture_output=True, check=False,
    )
    routines: dict[str, dict[str, int]] = {}
    cases: dict[str, str] = {}
    for line in result.stdout.splitlines():
        match = RESULT_RE.match(line)
        if match:
            status, name, first, second = match.groups()
            total = int(second) if second else int(first)
            failing = int(first) if second else 0
            routines[name] = {"status": status.lower(), "cases": total, "failing": failing}
            continue
        match = CASE_RE.match(line)
        if match:
            cases[f"{match.group(2)}-{match.group(3)}"] = match.group(1)
    if not routines:
        raise SystemExit(f"boundary oracle produced no results:\n{result.stdout[-3000:]}{result.stderr[-3000:]}")
    return routines, cases


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workdir", type=Path, default=ROOT / "build-extended" / "completion" / "boundary")
    parser.add_argument("--output", type=Path, default=ROOT / "build-extended" / "completion" / "extended-boundary.json")
    parser.add_argument("--check", action="store_true", help="exit nonzero unless every fixture case passes")
    args = parser.parse_args()
    profile = get_profile("extended", ROOT)
    args.workdir.mkdir(parents=True, exist_ok=True)
    source, inventory = build_fixture(ROOT, args.workdir)
    probe = build_native(ROOT, args.workdir, source, inventory)
    rom = source / profile.rom_name
    routines, cases = run_oracle(ROOT, rom, probe)
    lookups = {
        f"{card_id:04x}": cases.get(f"GetCardPointer-{index}", "missing")
        for index, card_id in enumerate(BOUNDARY_IDS)
    }
    lookups[f"{REJECTED_ID:04x}-rejected"] = cases.get(f"GetCardPointer-{len(BOUNDARY_IDS)}", "missing")
    failing = sorted(name for name, row in routines.items() if row["status"] != "pass")
    result = {
        "schema": 2,
        "profile": profile.name,
        "source_commit": profile.source_commit,
        "rom_sha256": sha256(rom),
        "card_ids": list(BOUNDARY_IDS),
        "rejected_card_id": REJECTED_ID,
        "catalog_card_count": 0xE4,
        "fixture_card_count": 0x1FF,
        "storage": {"collection_bytes": 0x200, "deck_entries": 60, "deck_entry_bytes": 2, "deck_compressed_bytes": 68},
        "lookups": lookups,
        "routines": routines,
        "failing": failing,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    for key, status in lookups.items():
        print(f"extended-boundary: {key} {status.upper()}")
    for name, row in sorted(routines.items()):
        print(f"extended-boundary: {row['status'].upper()} {name} cases={row['cases']} failing={row['failing']}")
    if failing:
        print(f"extended-boundary: FAIL rom_sha256={result['rom_sha256']} failing={len(failing)}")
        return 1 if args.check else 0
    print(f"extended-boundary: PASS rom_sha256={result['rom_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
