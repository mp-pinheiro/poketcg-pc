import json
import os
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VRAM_START = 0x8000
SRAM_START = 0xA000
WRAM_START = 0xC000
WRAMX_START = 0xD000
IO_START = 0xFF00
HRAM_START = 0xFF80
CALL_FRAME = range(0xCFF0, 0xCFF6)
STACK_WINDOW = range(0xDC30, 0xDD00)
STACK_TOP = 0xDCC0
STACK_CANARY = 0xDFF0
_LINE = re.compile(r"^([0-9A-Fa-f]{2,3}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")
_PATHS: dict[tuple[str | None, str | None], Path] = {}
_TABLES: dict[Path, dict[str, tuple[int, int]]] = {}


def sym_path() -> Path:
    key = (os.environ.get("POKETCG_PROFILE"), os.environ.get("POKETCG_PROFILE_VARIANT"))
    path = _PATHS.get(key)
    if path is None:
        catalog = json.loads((ROOT / "profiles" / "profiles.json").read_text())
        name = key[0] or catalog["default"]
        source = catalog["profiles"][name]["source"]
        checkout = source["checkout"]
        if key[1]:
            checkout = tomllib.loads((ROOT / "profiles" / name / f"{key[1]}.toml").read_text())["variant"]["checkout"]
        path = ROOT / checkout / source["sym"]
        _PATHS[key] = path
    return path


def symbols() -> dict[str, tuple[int, int]]:
    path = sym_path()
    table = _TABLES.get(path)
    if table is None:
        table = {}
        for line in path.read_text().splitlines():
            match = _LINE.match(line.strip())
            if match:
                table.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
        _TABLES[path] = table
    return table


def _lookup(name: str) -> tuple[int, int]:
    try:
        return symbols()[name]
    except KeyError:
        raise KeyError(f"{name} is not a symbol of {sym_path()}") from None


def sym(name: str) -> int:
    return _lookup(name)[1]


def sym_bank(name: str) -> int:
    return _lookup(name)[0]


def data(value: int) -> int:
    return value
