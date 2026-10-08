#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from profiles import Profile, ProfileError, get_profile, load_catalog, symbol_table

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.gen_constants import constant_names, evaluate  # noqa: E402

SYM_RE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")
ROM_LITERAL_RE = re.compile(r"\b0[xX]([4-7][0-9A-Fa-f]{3})[uU]?\b")
COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)
STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
BANK_WINDOW_RE = re.compile(
    r"0x3FFF|~0x8000|<<\s*14|mbc5_write|rRTC|0x4000u\s*\)\s*;|0x7F00|[<>]=?\s*0x4000u|0x4000u\s*\|"
)
LABEL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?")
LOCAL_RE = re.compile(r"^\.([A-Za-z0-9_]+):?$")
LOCAL_REF_RE = re.compile(r"(?<![A-Za-z0-9_])\.([A-Za-z0-9_]+)")
NUMBER_RE = re.compile(r"\$([0-9A-Fa-f]+)|%([01]+)|(?<![A-Za-z0-9_.$%])(\d+)\b")
IDENT_RE = re.compile(r"(?<![A-Za-z0-9_.])[A-Za-z_][A-Za-z0-9_]*")
ARITHMETIC_RE = re.compile(r"[0-9+\-*/()<>&|^~ ]+")
FUNCTION_RE = re.compile(r"^[A-Za-z_][\w \t\*]*?\b([A-Za-z_]\w*)\s*\([^;{}]*\)\s*\{", re.MULTILINE)
BLOCK_RE = re.compile(r"^/\* (>>>|---|===) (?:factory|part) (\w+) \*/[ \t]*$", re.MULTILINE)
PROBE_ROW_RE = re.compile(r'\{\s*"([A-Za-z_][A-Za-z0-9_.]*)"\s*,\s*adapt_\w+\s*\}')
BYTE_MNEMONICS = frozenset({"CP", "AND", "OR", "XOR", "SUB", "ADD", "ADC", "SBC", "DB"})
REGISTERS8 = frozenset({"A", "B", "C", "D", "E", "H", "L", "[HL]"})
REGISTERS16 = frozenset({"BC", "DE", "HL", "SP"})
POINTER_REGISTERS = frozenset({"[HL]", "[HLI]", "[HLD]", "[HL+]", "[HL-]", "[BC]", "[DE]", "[C]"})
CALLS = frozenset({"CALL", "FARCALL", "BANK1CALL"})
BUILTIN_CONSTANTS = {"TRUE": 1, "FALSE": 0}
NORMALIZED = ("identical", "local-label", "tail-call", "jump-to-next", "constant-spelling")


def masked_source(text: str) -> str:
    def blank(match: re.Match[str]) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    return STRING_RE.sub(blank, COMMENT_RE.sub(blank, text))


@dataclass(frozen=True)
class Routine:
    name: str
    path: str
    lines: tuple[str, ...]
    following: str | None


@dataclass
class Tree:
    routines: dict[str, Routine]
    constants: dict[str, int]
    addresses: list[tuple[int, str]]


def parse_routines(source: Path) -> dict[str, Routine]:
    result: dict[str, Routine] = {}
    for path in sorted(source.rglob("*.asm")):
        relative = path.relative_to(source).as_posix()
        order: list[str] = []
        bodies: dict[str, list[str]] = {}
        current: str | None = None
        for raw in path.read_text(errors="replace").splitlines():
            code = raw.split(";", 1)[0].rstrip()
            match = LABEL_RE.match(code)
            if match:
                current = match.group(1)
                order.append(current)
                bodies.setdefault(current, [])
                rest = code[match.end():].strip()
                if rest:
                    bodies[current].append(re.sub(r"\s+", " ", rest).upper())
                continue
            line = re.sub(r"\s+", " ", code.strip()).upper()
            if line and current is not None:
                bodies[current].append(line)
        for index, name in enumerate(order):
            if name in result:
                continue
            following = order[index + 1] if index + 1 < len(order) else None
            result[name] = Routine(name, relative, tuple(bodies[name]), following)
    return result


def load_tree(profile: Profile, checkout: Path) -> Tree:
    constants = {name.upper(): value for name, value in evaluate(checkout, constant_names(checkout)).items()}
    for name, value in BUILTIN_CONSTANTS.items():
        constants.setdefault(name, value)
    addresses = sorted(
        (address, name.upper())
        for name, (_, address) in symbol_table_at(profile, checkout).items()
        if "." not in name and address >= 0x8000
    )
    return Tree(parse_routines(checkout / "src"), constants, addresses)


def symbol_table_at(profile: Profile, checkout: Path) -> dict[str, tuple[int, int]]:
    path = checkout / profile.sym_name
    result: dict[str, tuple[int, int]] = {}
    if not path.is_file():
        return symbol_table(profile, ROOT)
    for line in path.read_text(errors="replace").splitlines():
        match = re.match(r"^([0-9A-Fa-f]{2,3}):([0-9A-Fa-f]{4})\s+(\S+)\s*$", line.strip())
        if match:
            result.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
    return result


def canonical_number(match: re.Match[str]) -> str:
    if match.group(1):
        return str(int(match.group(1), 16))
    if match.group(2):
        return str(int(match.group(2), 2))
    return str(int(match.group(3)))


def fold(text: str, mask: int) -> str:
    compact = text.replace(" ", "")
    if compact and ARITHMETIC_RE.fullmatch(compact):
        try:
            return str(eval(compact.replace("/", "//"), {"__builtins__": {}}, {}) & mask)
        except (SyntaxError, ZeroDivisionError, TypeError, ValueError):
            return compact
    return compact


def nearest_symbol(addresses: list[tuple[int, str]], address: int) -> str:
    low, high = 0, len(addresses)
    while low < high:
        middle = (low + high) // 2
        if addresses[middle][0] <= address:
            low = middle + 1
        else:
            high = middle
    if low == 0:
        return str(address)
    base, name = addresses[low - 1]
    return name if base == address else f"{name}+{address - base}"


class Normalizer:
    def __init__(self, tree: Tree, stable: dict[str, int]) -> None:
        self.tree = tree
        self.stable = stable

    def operand(self, text: str, locals_seen: dict[str, str], level: int) -> str:
        text = LOCAL_REF_RE.sub(lambda match: locals_seen.get(match.group(1), "." + match.group(1)), text)
        if level < 4:
            return text.replace(" ", "")
        text = NUMBER_RE.sub(canonical_number, text)
        text = IDENT_RE.sub(lambda match: str(self.stable[match.group(0)]) if match.group(0) in self.stable else match.group(0), text)
        text = text.replace(" ", "")
        if text.startswith("[") and text.endswith("]") and text not in POINTER_REGISTERS:
            inner = text[1:-1]
            inner = re.sub(r"\+0(?![0-9])", "", inner)
            folded = fold(inner, 0xFFFF)
            if folded.isdigit() and int(folded) >= 0x8000:
                inner = nearest_symbol(self.tree.addresses, int(folded))
            text = f"[{inner}]"
        return text

    def high_ram(self, operand: str) -> bool:
        if not (operand.startswith("[") and operand.endswith("]")) or operand in POINTER_REGISTERS:
            return False
        inner = operand[1:-1].split("+", 1)[0]
        if inner.isdigit():
            return int(inner) >= 0xFF00
        return inner.startswith("H") and inner not in {"HL", "HLI", "HLD"}

    def lines(self, routine: Routine, level: int) -> list[str]:
        locals_seen: dict[str, str] = {}
        for line in routine.lines:
            match = LOCAL_RE.match(line)
            if match:
                locals_seen.setdefault(match.group(1), f".L{len(locals_seen)}" if level >= 1 else "." + match.group(1))
        items: list[tuple[str, str]] = []
        for line in routine.lines:
            match = LOCAL_RE.match(line)
            if match:
                items.append(("label", locals_seen[match.group(1)]))
                continue
            mnemonic, _, rest = line.partition(" ")
            operands = [self.operand(part.strip(), locals_seen, level) for part in rest.split(",")] if rest else []
            if level >= 4:
                if mnemonic == "LB" and len(operands) == 3 and operands[0] in REGISTERS16:
                    items.append(("op", f"LD {operands[0][0]},{fold(operands[1], 0xFF)}"))
                    items.append(("op", f"LD {operands[0][1]},{fold(operands[2], 0xFF)}"))
                    continue
                if mnemonic in BYTE_MNEMONICS and operands:
                    operands[-1] = fold(operands[-1], 0xFF)
                elif mnemonic == "DW":
                    operands = [fold(operand, 0xFFFF) for operand in operands]
                elif mnemonic in {"LD", "LDH"} and len(operands) == 2:
                    if operands[0] in REGISTERS8:
                        operands[1] = fold(operands[1], 0xFF)
                    elif operands[0] in REGISTERS16:
                        operands[1] = fold(operands[1], 0xFFFF)
                        if operands[0] in {"BC", "DE", "HL"} and operands[1].isdigit():
                            value = int(operands[1])
                            items.append(("op", f"LD {operands[0][0]},{value >> 8}"))
                            items.append(("op", f"LD {operands[0][1]},{value & 0xFF}"))
                            continue
                    if any(self.high_ram(operand) for operand in operands):
                        mnemonic = "LDH"
            if level >= 2:
                if mnemonic in {"FARCALL", "BANK1CALL"}:
                    mnemonic = "CALL"
                if mnemonic == "JR":
                    mnemonic = "JP"
                if mnemonic == "JP" and len(operands) == 1 and operands[0] != "HL":
                    mnemonic = "TAIL"
            items.append(("op", f"{mnemonic} {','.join(operands)}".strip()))
        if level >= 2:
            merged: list[tuple[str, str]] = []
            index = 0
            while index < len(items):
                kind, text = items[index]
                mnemonic, _, target = text.partition(" ")
                if (kind == "op" and mnemonic == "CALL" and target and "," not in target
                        and index + 1 < len(items) and items[index + 1] == ("op", "RET")):
                    merged.append(("op", f"TAIL {target}"))
                    index += 2
                    continue
                merged.append(items[index])
                index += 1
            items = merged
        if level >= 3:
            following = routine.following.upper() if routine.following else None
            pruned: list[tuple[str, str]] = []
            for index, (kind, text) in enumerate(items):
                mnemonic, _, target = text.partition(" ")
                if kind == "op" and mnemonic == "TAIL":
                    after = items[index + 1] if index + 1 < len(items) else None
                    if after is not None and after == ("label", target):
                        continue
                    if after is None and following and target == following:
                        continue
                pruned.append((kind, text))
            items = pruned
        return [text for _, text in items]


@dataclass(frozen=True)
class Difference:
    name: str
    status: str
    vanilla_path: str | None
    profile_path: str | None

    @property
    def moved(self) -> bool:
        return bool(self.vanilla_path and self.profile_path and self.vanilla_path != self.profile_path)

    @property
    def needs_port(self) -> bool:
        return self.status in {"semantic", "new"}


def basename_of(path: str | None) -> str | None:
    return Path(path).stem if path else None


@lru_cache(maxsize=None)
def inventory_functions(path: Path) -> frozenset[str]:
    if not path.is_file():
        return frozenset()
    return frozenset(json.loads(path.read_text())["functions"])


def compare(vanilla: Profile, profile: Profile, vanilla_checkout: Path, profile_checkout: Path) -> list[Difference]:
    vanilla_tree = load_tree(vanilla, vanilla_checkout)
    profile_tree = load_tree(profile, profile_checkout)
    unstable = {
        name for name, value in vanilla_tree.constants.items()
        if name in profile_tree.constants and profile_tree.constants[name] != value
    }
    vanilla_normalizer = Normalizer(vanilla_tree, {k: v for k, v in vanilla_tree.constants.items() if k not in unstable})
    profile_normalizer = Normalizer(profile_tree, {k: v for k, v in profile_tree.constants.items() if k not in unstable})
    universe = (inventory_functions(vanilla.artifact_path("inventory", ROOT))
                | inventory_functions(profile.artifact_path("inventory", ROOT)))
    if not universe:
        universe = frozenset(vanilla_tree.routines) | frozenset(profile_tree.routines)
    differences = []
    for name in sorted(universe):
        before = vanilla_tree.routines.get(name)
        after = profile_tree.routines.get(name)
        if before is None and after is None:
            continue
        if after is None:
            status = "removed"
        elif before is None:
            status = "new"
        else:
            status = "semantic"
            for level, label in enumerate(NORMALIZED):
                if vanilla_normalizer.lines(before, level) == profile_normalizer.lines(after, level):
                    status = label
                    break
        differences.append(Difference(name, status, before.path if before else None, after.path if after else None))
    return differences


def c_names(routine: str) -> tuple[str, ...]:
    return (routine, routine.replace(".", "_"))


def defined_functions(directory: Path) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    if not directory.is_dir():
        return result
    for path in sorted(directory.glob("*.c")):
        text = path.read_text(errors="replace")
        for match in FUNCTION_RE.finditer(masked_source(text)):
            result[match.group(1)].add(path.stem)
    return result


def override_markers(directory: Path) -> dict[str, dict[str, set[str]]]:
    result: dict[str, dict[str, set[str]]] = {">>>": defaultdict(set), "---": defaultdict(set), "===": defaultdict(set)}
    if not directory.is_dir():
        return result
    for path in sorted(directory.glob("*.c")):
        for match in BLOCK_RE.finditer(path.read_text(errors="replace")):
            result[match.group(1)][match.group(2)].add(path.stem)
    return result


def routine_report(differences: list[Difference], basenames: list[str], show_all: bool) -> int:
    selected = set(basenames)
    rows: dict[str, list[str]] = defaultdict(list)
    totals: Counter[str] = Counter()
    for difference in differences:
        owners = {basename_of(difference.vanilla_path), basename_of(difference.profile_path)} - {None}
        if selected and not owners & selected:
            continue
        totals[difference.status] += 1
        if difference.status == "identical" and not difference.moved and not show_all:
            continue
        where = basename_of(difference.profile_path) or basename_of(difference.vanilla_path)
        moved = f" moved {difference.vanilla_path} -> {difference.profile_path}" if difference.moved else ""
        rows[str(where)].append(f"  {difference.status:17s} {difference.name}{moved}")
    for basename in sorted(rows):
        print(f"{basename}:")
        print("\n".join(rows[basename]))
    port = totals["semantic"] + totals["new"]
    print(" ".join(f"{key}={totals[key]}" for key in (*NORMALIZED, "semantic", "new", "removed")) + f" port={port}")
    return 0


def audit(profile: Profile, differences: list[Difference]) -> list[str]:
    failures: list[str] = []
    shared_home = ROOT / "src" / "home"
    overlay = profile.overlay_path(ROOT)
    overlay_home = overlay / "home" if overlay else None
    shared_defined = defined_functions(shared_home)
    overlay_defined = defined_functions(overlay_home) if overlay_home else {}
    markers = override_markers(overlay_home) if overlay_home else {">>>": {}, "---": {}, "===": {}}
    removed_basenames = profile.removed_basenames
    for difference in differences:
        names = c_names(difference.name)
        everywhere = {stem for name in names for stem in shared_defined.get(name, ())}
        shared_files = everywhere - removed_basenames
        overlay_files = {stem for name in names for stem in overlay_defined.get(name, ())}
        replaced = overlay_files or any(name in markers[">>>"] for name in names)
        declared = any(name in markers["==="] for name in names)
        removed = any(name in markers["---"] for name in names)
        if difference.needs_port and not (replaced or declared):
            if everywhere and not shared_files and not overlay_files:
                continue
            where = basename_of(difference.profile_path)
            failures.append(f"routine differs without override: {difference.name} ({difference.status}, {where})")
        if difference.status == "removed" and not (removed or declared) and (shared_files or overlay_files):
            failures.append(f"routine missing from profile asm is still compiled: {difference.name} ({', '.join(sorted(shared_files | overlay_files))})")
    return failures


def symbols(path: Path) -> dict[str, tuple[int, int]]:
    result: dict[str, tuple[int, int]] = {}
    for line in path.read_text(errors="replace").splitlines():
        match = SYM_RE.match(line.strip())
        if match and "." not in match.group(3):
            result.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
    return result


def c_paths(root: Path) -> list[Path]:
    return sorted(root.glob("*.c")) + sorted(root.glob("*.h"))


def rom_literal_failures(vanilla: Profile, profile: Profile, vanilla_checkout: Path, profile_checkout: Path) -> list[str]:
    failures = []
    shared_home = ROOT / "src" / "home"
    overlay = profile.overlay_path(ROOT)
    overlay_home = overlay / "home" if overlay else None
    vanilla_symbols = symbols(vanilla_checkout / vanilla.sym_name)
    profile_symbols = symbols(profile_checkout / profile.sym_name)
    changed_addresses = {
        vanilla_address[1]
        for name, vanilla_address in vanilla_symbols.items()
        if name in profile_symbols
        and vanilla_address != profile_symbols[name]
        and 0x4000 <= vanilla_address[1] < 0x8000
    }
    for path in c_paths(shared_home):
        if (overlay_home and (overlay_home / f"{path.stem}.c").is_file()) or path.stem in profile.removed_basenames:
            continue
        source = masked_source(path.read_text(errors="replace"))
        for line in source.splitlines():
            if BANK_WINDOW_RE.search(line):
                continue
            for match in ROM_LITERAL_RE.finditer(line):
                address = int(match.group(1), 16)
                if address in changed_addresses:
                    failures.append(f"profile-specific ROM literal: {path.relative_to(ROOT)}:0x{address:04X}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Diff each ported profile's asm against the catalog's default profile routine by routine after normalization.")
    parser.add_argument("--profile", help="profile to audit (POKETCG_PROFILE, else every profile but the catalog default)")
    parser.add_argument("--base-checkout", type=Path, help="default profile checkout overriding the catalog's")
    parser.add_argument("--checkout", type=Path, help="audited profile checkout overriding the catalog's")
    parser.add_argument("--routines", nargs="*", metavar="BASENAME",
                        help="list per-routine classes (all basenames when none given) instead of auditing")
    parser.add_argument("--all", action="store_true", help="with --routines, also list identical routines")
    args = parser.parse_args()
    try:
        default, catalog = load_catalog()
        base = get_profile(default, ROOT)
        requested = args.profile or os.environ.get("POKETCG_PROFILE")
        names = [requested] if requested and requested != default else [name for name in catalog if name != default]
        profiles = [get_profile(name, ROOT) for name in names]
    except ProfileError as error:
        raise SystemExit(str(error)) from error
    if len(profiles) != 1 and (args.routines is not None or args.checkout):
        raise SystemExit("--routines and --checkout need one profile: pass --profile or set POKETCG_PROFILE")
    base_checkout = (args.base_checkout or base.source_path(ROOT)).resolve()
    status = 0
    for profile in profiles:
        profile_checkout = (args.checkout or profile.source_path(ROOT)).resolve()
        differences = compare(base, profile, base_checkout, profile_checkout)
        if args.routines is not None:
            return routine_report(differences, args.routines, args.all)
        failures = audit(profile, differences) + rom_literal_failures(base, profile, base_checkout, profile_checkout)
        totals = Counter(difference.status for difference in differences)
        summary = " ".join(f"{key}={totals[key]}" for key in (*NORMALIZED, "semantic", "new", "removed"))
        if failures:
            print(f"profile-audit: FAIL profile={profile.name} {summary}")
            for failure in failures:
                print(failure)
            status = 1
            continue
        print(f"profile-audit: PASS profile={profile.name} {summary}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
