import contextlib
import json
import os
import re
import tomllib
from collections.abc import Iterable
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
_ABSENT: list[tuple[int, int]] = []
_CARD_ID_SIZES: dict[str, int] = {}
_CONSTANTS: dict[Path, dict[str, int]] = {}
_ROM_DATA: dict[Path, bytes] = {}


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


def _symbol_table(path: Path) -> dict[str, tuple[int, int]]:
    table = _TABLES.get(path)
    if table is None:
        table = {}
        for line in path.read_text().splitlines():
            match = _LINE.match(line.strip())
            if match:
                table.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
        _TABLES[path] = table
    return table


def symbols() -> dict[str, tuple[int, int]]:
    return _symbol_table(sym_path())


def profile_symbols(profile: str, variant: str | None = None) -> dict[str, tuple[int, int]]:
    key = (profile, variant)
    path = _PATHS.get(key)
    if path is None:
        catalog = json.loads((ROOT / "profiles" / "profiles.json").read_text())
        source = catalog["profiles"][profile]["source"]
        checkout = source["checkout"]
        if variant:
            checkout = tomllib.loads((ROOT / "profiles" / profile / f"{variant}.toml").read_text())["variant"]["checkout"]
        path = ROOT / checkout / source["sym"]
        _PATHS[key] = path
    return _symbol_table(path)


def frame_callback_pointer(value: int, source_profile: str, source_bank: int | None,
                           source_variant: str | None = None) -> bytes:
    bank = 0 if value < 0x4000 else source_bank
    if bank is None:
        return value.to_bytes(2, "little")
    target_addresses = {
        target[1]
        for name, (source_bank, source_address) in profile_symbols(source_profile, source_variant).items()
        if source_bank == bank
        and source_address == value
        and (target := symbols().get(name)) is not None
        and (value < 0x4000 or target[0] == source_bank)
    }
    if len(target_addresses) == 1:
        return next(iter(target_addresses)).to_bytes(2, "little")
    return value.to_bytes(2, "little")


def _lookup(name: str) -> tuple[int, int]:
    try:
        return symbols()[name]
    except KeyError:
        if _ABSENT:
            return _ABSENT[-1]
        raise KeyError(f"{name} is not a symbol of {sym_path()}") from None


@contextlib.contextmanager
def absent_symbols_as(bank: int, address: int):
    _ABSENT.append((bank, address))
    try:
        yield
    finally:
        _ABSENT.pop()


def sym(name: str) -> int:
    return _lookup(name)[1]


def sym_bank(name: str) -> int:
    return _lookup(name)[0]

def sym_pointer(name: str) -> bytes:
    return sym(name).to_bytes(2, "little")


def data(value: int) -> int:
    return value

def _generated_value(name: str, filename: str) -> int:
    catalog = json.loads((ROOT / "profiles" / "profiles.json").read_text())
    profile = os.environ.get("POKETCG_PROFILE") or catalog["default"]
    build = os.environ.get("POKETCG_BUILD") or catalog["profiles"][profile]["build"]["default_build_dir"]
    path = ROOT / build / "generated" / profile / "generated" / filename
    table = _CONSTANTS.get(path)
    if table is None:
        table = {}
        for key, value in re.findall(r"^#define (\w+) (0x[0-9A-Fa-f]+u|\(-\d+\))$", path.read_text(), re.MULTILINE):
            table[key] = int(value.removesuffix("u").strip("()"), 0)
        _CONSTANTS[path] = table
    return table[name]


def const(name: str) -> int:
    return _generated_value(name, "constants.h")


def text_id(name: str) -> int:
    return _generated_value(name, "text_ids.h")


def rom_byte(bank: int, address: int) -> int:
    catalog = json.loads((ROOT / "profiles" / "profiles.json").read_text())
    profile = os.environ.get("POKETCG_PROFILE") or catalog["default"]
    path = sym_path().with_name(catalog["profiles"][profile]["source"]["rom"])
    image = _ROM_DATA.get(path)
    if image is None:
        image = path.read_bytes()
        _ROM_DATA[path] = image
    offset = address if address < 0x4000 else bank * 0x4000 + address - 0x4000
    return image[offset]


def card_max_hp(card_id: int) -> int:
    width = 3 if card_id_size() == 2 else 2
    bank = sym_bank("CardPointers")
    pointer = sym("CardPointers") + card_id * width
    address = rom_byte(bank, pointer) | (rom_byte(bank, pointer + 1) << 8)
    if width == 3:
        bank = rom_byte(bank, pointer + 2)
    return rom_byte(bank, address + const("CARD_DATA_HP"))


def map_script_offset(slot: int) -> int:
    catalog = json.loads((ROOT / "profiles" / "profiles.json").read_text())
    profile = os.environ.get("POKETCG_PROFILE") or catalog["default"]
    width = 3 if catalog["profiles"][profile]["features"].get("multi_bank_scripts", False) else 2
    return slot * width

def card_id_size() -> int:
    catalog = json.loads((ROOT / "profiles" / "profiles.json").read_text())
    profile = os.environ.get("POKETCG_PROFILE") or catalog["default"]
    size = _CARD_ID_SIZES.get(profile)
    if size is None:
        size = 2 if catalog["profiles"][profile]["features"].get("nine_bit_card_ids", False) else 1
        _CARD_ID_SIZES[profile] = size
    return size


def card_id_bytes(card_id: int) -> bytes:
    return card_id.to_bytes(card_id_size(), "little")


def deck_offset(index: int) -> int:
    return index * card_id_size()


def deck_bytes(card_ids: Iterable[int]) -> bytes:
    return b"".join(card_id_bytes(card_id) for card_id in card_ids)


def deck_entry(index: int, card_id: int, base: int | None = None) -> dict[int, bytes]:
    address = sym("wDeckToBuild") if base is None else base
    return {address + deck_offset(index): card_id_bytes(card_id)}


def deck_entries(card_ids: Iterable[int], base: int | None = None) -> dict[int, bytes]:
    address = sym("wDeckToBuild") if base is None else base
    size = card_id_size()
    return {address + index * size: card_id_bytes(card_id) for index, card_id in enumerate(card_ids)}
