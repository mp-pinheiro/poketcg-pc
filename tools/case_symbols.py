#!/usr/bin/env python3
"""Rewrite address literals in tests/cases modules as `_symbols` references: python3 tools/case_symbols.py [--check] [MODULE ...]"""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import sys
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.profiles import load_catalog  # noqa: E402

CASES = ROOT / "tests" / "cases"
SKIP = {"_symbols.py", "_schema_migration.py"}
SYMBOLS_MODULE = "tests.cases._symbols"

WRAM = (0xC000, 0xE000)
SRAM = (0xA000, 0xC000)
HRAM = (0xFF80, 0xFFFF)
CALL_FRAME = range(0xCFF0, 0xCFF6)
STACK_WINDOW = range(0xDC30, 0xDD00)
STACK_TOP = 0xDCC0
STACK_CANARY = 0xDFF0
BASES = {0xC000: "WRAM_START", 0xD000: "WRAMX_START", 0xA000: "SRAM_START", 0xFF80: "HRAM_START"}
REGISTERS = {"a", "f", "b", "c", "d", "e", "h", "l", "af", "bc", "de", "hl", "sp"}
SRAM_KEYS = {"sram", "sread", "expect_sram"}
JUNK = {0xBEEF, 0xABCD, 0xBCDE, 0xBBCC, 0xDDEE, 0xC3FF}
OPERAND_MODULES = {
    "division.py": {"_case"},
    "random.py": set(),
    "write_number.py": {"one_digit_case", "two_digit_case", "four_digit_case", "one_byte_case", "two_byte_case"},
}
BANK_IMAGE_MODULES = {"clear_sram.py", "sram.py"}
FIXTURE_KEY = re.compile(r"[0-9A-Fa-f]{4}")
PREDICATE = re.compile(r"mem:0x([0-9A-Fa-f]{4})")
_LINE = re.compile(r"^([0-9A-Fa-f]{2,3}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")


def ram_region(value: int) -> str | None:
    if WRAM[0] <= value < WRAM[1]:
        return "wram"
    if SRAM[0] <= value < SRAM[1]:
        return "sram"
    if HRAM[0] <= value < HRAM[1]:
        return "hram"
    return None


def read_sym(path: Path) -> list[tuple[int, int, str]]:
    rows = []
    for line in path.read_text().splitlines():
        match = _LINE.match(line.strip())
        if match:
            rows.append((int(match.group(1), 16), int(match.group(2), 16), match.group(3)))
    return rows


@dataclass
class Tables:
    ram: dict[tuple[str, int | None], list[tuple[int, str]]]
    ends: dict[str, int]
    rom: dict[int, list[tuple[int, str]]]
    named: dict[str, tuple[int, int]]

    @classmethod
    def load(cls) -> "Tables":
        _, profiles = load_catalog(ROOT / "profiles" / "profiles.json")
        rows = read_sym(profiles["vanilla"].sym_path(ROOT))
        others = [
            {name for _, _, name in read_sym(profile.sym_path(ROOT))}
            for key, profile in profiles.items() if key != "vanilla"
        ]
        shared = {name for _, _, name in rows if all(name in names for names in others)}
        order = {name: index for index, (_, _, name) in enumerate(rows)}
        named: dict[str, tuple[int, int]] = {}
        groups: dict[tuple[str, int | None, int], list[str]] = {}
        rom: dict[tuple[int, int], list[str]] = {}
        for bank, address, name in rows:
            named.setdefault(name, (bank, address))
            region = ram_region(address)
            if region is not None and address >= 0xA000:
                if "." in name or name.startswith("v"):
                    continue
                key_bank = bank if region == "sram" else None
                groups.setdefault((region, key_bank, address), []).append(name)
            elif address < 0x8000:
                rom.setdefault((bank, address), []).append(name)

        def ram_pick(names: list[str]) -> str:
            return min(names, key=lambda n: (n not in shared, order[n]))

        def rom_pick(names: list[str]) -> str:
            return min(names, key=lambda n: ("." in n, n not in shared, order[n]))

        ram: dict[tuple[str, int | None], list[tuple[int, str]]] = {}
        for (region, bank, address), names in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1] or 0, kv[0][2])):
            ram.setdefault((region, bank), []).append((address, ram_pick(names)))
        rom_tables: dict[int, list[tuple[int, str]]] = {}
        for (bank, address), names in sorted(rom.items()):
            rom_tables.setdefault(bank, []).append((address, rom_pick(names)))
        wram_high = max(address for address, _ in ram[("wram", None)])
        backup = named.get("wMusicCh1StackBackup")
        wram_end = max(wram_high + 1, backup[1] + 0x30 if backup else 0)
        hram_end = max(address for address, _ in ram[("hram", None)]) + 1
        return cls(ram, {"wram": wram_end, "hram": hram_end, "sram": SRAM[1]}, rom_tables, named)

    def aliases_at(self, region: str, bank: int | None, address: int) -> str | None:
        for start, name in self.ram.get((region, bank), []):
            if start == address:
                return name
        return None

    def containing(self, region: str, bank: int | None, value: int) -> tuple[str, int, int] | None:
        rows = self.ram.get((region, bank), [])
        best = None
        for index, (start, name) in enumerate(rows):
            if start > value:
                break
            end = rows[index + 1][0] if index + 1 < len(rows) else self.ends[region]
            best = (name, value - start, end - start)
        if best is None or best[1] >= best[2]:
            return None
        return best

    def rom_label(self, bank: int, pc: int) -> tuple[str, int] | None:
        best = None
        for start, name in self.rom.get(bank, []):
            if start > pc:
                break
            best = (name, pc - start)
        return best


def offset_expr(head: str, offset: int) -> str:
    if offset == 0:
        return head
    if offset < 0:
        return f"{head} - {-offset:#x}" if -offset > 9 else f"{head} - {-offset}"
    return f"{head} + 0x{offset:X}" if offset > 9 else f"{head} + {offset}"


@dataclass
class Edit:
    start: tuple[int, int]
    end: tuple[int, int]
    text: str


@dataclass
class Result:
    path: Path
    edits: list[Edit] = field(default_factory=list)
    names: set[str] = field(default_factory=set)
    notes: list[dict] = field(default_factory=list)


def set_parents(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore[attr-defined]


def parent(node: ast.AST) -> ast.AST | None:
    return getattr(node, "parent", None)


def str_key(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def field_name(node: ast.AST) -> str | None:
    up = parent(node)
    if isinstance(up, ast.keyword):
        return up.arg
    if isinstance(up, ast.Dict):
        for key, value in zip(up.keys, up.values):
            if value is node:
                return str_key(key)
    return None


def is_dict_key(node: ast.AST) -> bool:
    up = parent(node)
    return isinstance(up, ast.Dict) and any(key is node for key in up.keys)


def call_name(call: ast.Call) -> str:
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def assign_target(node: ast.AST) -> str | None:
    cur = node
    while parent(cur) is not None:
        up = parent(cur)
        if isinstance(up, (ast.Assign, ast.AnnAssign)):
            target = up.targets[0] if isinstance(up, ast.Assign) else up.target
            if isinstance(target, ast.Name):
                return target.id
            if isinstance(target, ast.Tuple) and isinstance(up.value, ast.Tuple) and cur in up.value.elts:
                index = up.value.elts.index(cur)
                element = target.elts[index]
                return element.id if isinstance(element, ast.Name) else None
            return None
        if isinstance(up, (ast.stmt, ast.Lambda, ast.comprehension)):
            return None
        cur = up
    return None


def register_context(node: ast.AST) -> bool:
    name = field_name(node)
    return name in REGISTERS


def stack_context(node: ast.AST) -> bool:
    up = parent(node)
    return isinstance(up, (ast.List, ast.Tuple)) and field_name(up) == "stack"


def entry_sp_context(node: ast.AST) -> bool:
    name = field_name(node)
    if name == "entry_sp":
        return True
    target = assign_target(node)
    return target is not None and "ENTRY_SP" in target.upper()


def positional_call(node: ast.AST) -> str | None:
    up = parent(node)
    if isinstance(up, ast.Call) and node in up.args:
        return call_name(up)
    return None


def in_state(node: ast.AST) -> bool:
    cur = node
    while parent(cur) is not None:
        up = parent(cur)
        if isinstance(up, ast.Dict):
            for key, value in zip(up.keys, up.values):
                if value is cur and str_key(key) == "state":
                    return True
        if isinstance(up, (ast.Assign, ast.AnnAssign)):
            target = up.targets[0] if isinstance(up, ast.Assign) else up.target
            return isinstance(target, ast.Name) and target.id == "STATE"
        cur = up
    return False


def sram_bank(node: ast.AST) -> int | None:
    if not is_dict_key(node):
        return None
    inner = parent(node)
    outer = parent(inner)
    if not isinstance(outer, ast.Dict):
        return None
    for key, value in zip(outer.keys, outer.values):
        if value is inner and isinstance(key, ast.Constant) and type(key.value) is int:
            if field_name(outer) in SRAM_KEYS:
                return key.value
    return None


def needs_parens(node: ast.AST) -> bool:
    up = parent(node)
    if isinstance(up, ast.BinOp):
        if isinstance(up.op, ast.Add):
            return False
        if isinstance(up.op, ast.Sub) and up.left is node:
            return False
        return True
    return isinstance(up, (ast.UnaryOp, ast.Attribute, ast.Subscript)) and getattr(up, "value", None) is node


class Rewriter:
    def __init__(self, tables: Tables, path: Path):
        self.tables = tables
        self.path = path
        self.text = path.read_text()
        self.lines = self.text.splitlines(keepends=True)
        self.tree = ast.parse(self.text)
        set_parents(self.tree)
        self.result = Result(path)
        self.claimed: set[int] = set()
        self.tokens = {
            token.start: token
            for token in tokenize.generate_tokens(io.StringIO(self.text).readline)
            if token.type in (tokenize.NUMBER, tokenize.STRING)
        }

    def char_col(self, line: int, col: int) -> int:
        return len(self.lines[line - 1].encode()[:col].decode())

    def span(self, node: ast.AST) -> tuple[tuple[int, int], tuple[int, int]]:
        start = (node.lineno, self.char_col(node.lineno, node.col_offset))
        end = (node.end_lineno, self.char_col(node.end_lineno, node.end_col_offset))
        if isinstance(node, ast.Constant):
            token = self.tokens.get(start)
            if token is None or token.end != end:
                raise SystemExit(f"{self.path.name}:{node.lineno}: literal is not a single token")
        return start, end

    def source(self, node: ast.AST) -> str:
        return ast.get_source_segment(self.text, node) or ""

    def note(self, node: ast.AST, kind: str, **extra) -> None:
        self.result.notes.append({"file": self.path.name, "line": node.lineno, "kind": kind,
                                  "literal": self.source(node), **extra})

    def replace(self, node: ast.AST, text: str, *names: str) -> None:
        start, end = self.span(node)
        if needs_parens(node) and not text.isidentifier() and not re.fullmatch(r"[\w.]+\(\"?[\w.]+\"?\)", text):
            text = f"({text})"
        self.result.edits.append(Edit(start, end, text))
        self.result.names.update(names)
        self.claimed.add(id(node))

    def address(self, value: int, node: ast.AST, preferred: str | None = None) -> tuple[str, set[str]] | None:
        region = ram_region(value)
        bank = None
        if region == "sram":
            bank = sram_bank(node)
            if self.path.name in BANK_IMAGE_MODULES:
                self.note(node, "sram-bank-image")
                return offset_expr("SRAM_START", value - SRAM[0]), {"SRAM_START"}
            if bank is None:
                bank = 0
                self.note(node, "sram-bank-0")
        if region == "wram" and value >= self.tables.ends["wram"]:
            if value == STACK_CANARY:
                return "STACK_CANARY", {"STACK_CANARY"}
            self.note(node, "beyond-declared-wram")
            return offset_expr("WRAMX_START", value - 0xD000), {"WRAMX_START"}
        if region == "hram" and value >= self.tables.ends["hram"]:
            self.note(node, "beyond-declared-hram")
            return offset_expr("HRAM_START", value - 0xFF80), {"HRAM_START"}
        if preferred is not None:
            located = self.tables.named.get(preferred)
            if located is not None and located[1] == value and ram_region(located[1]) == region \
                    and "." not in preferred and not preferred.startswith("v") \
                    and (region != "sram" or located[0] == bank):
                return f'sym("{preferred}")', {"sym"}
        found = self.tables.containing(region, bank, value)
        if found is None and region == "sram":
            self.note(node, "sram-no-symbol", bank=bank)
            return offset_expr("SRAM_START", value - SRAM[0]), {"SRAM_START"}
        if found is None:
            self.note(node, "no-symbol")
            return None
        name, offset, extent = found
        if offset >= 0x100:
            self.note(node, "large-offset", symbol=name, offset=offset)
        return offset_expr(f'sym("{name}")', offset), {"sym"}

    def classify(self, node: ast.Constant) -> None:
        value = node.value
        up = parent(node)
        if isinstance(up, ast.Call) and call_name(up) == "data":
            return
        module = self.path.name
        if value in JUNK and (register_context(node) or stack_context(node)
                              or (assign_target(node) or "").startswith("_SAVED_")):
            self.note(node, "data", reason="junk register or stack word")
            self.replace(node, f"data({self.source(node)})", "data")
            return
        if module in OPERAND_MODULES and (register_context(node)
                                          or positional_call(node) in OPERAND_MODULES[module]):
            self.note(node, "data", reason="arithmetic operand")
            self.replace(node, f"data({self.source(node)})", "data")
            return
        if value in BASES and ((isinstance(up, ast.BinOp) and isinstance(up.op, ast.Sub) and up.right is node)
                               or isinstance(up, ast.Compare) or in_state(node)):
            self.replace(node, BASES[value], BASES[value])
            return
        if in_state(node) and value == 0xB000:
            self.replace(node, "SRAM_START + 0x1000", "SRAM_START")
            return
        if value in CALL_FRAME:
            self.note(node, "call-frame")
            self.replace(node, offset_expr("CALL_FRAME.start", value - CALL_FRAME.start), "CALL_FRAME")
            return
        if value == STACK_CANARY:
            self.replace(node, "STACK_CANARY", "STACK_CANARY")
            return
        if value in (STACK_WINDOW.start, STACK_WINDOW.stop) and not entry_sp_context(node):
            bound = "start" if value == STACK_WINDOW.start else "stop"
            self.note(node, "stack-window-bound")
            self.replace(node, f"STACK_WINDOW.{bound}", "STACK_WINDOW")
            return
        if value in STACK_WINDOW:
            if not entry_sp_context(node):
                self.note(node, "stack-window")
            self.replace(node, offset_expr("STACK_TOP", value - STACK_TOP), "STACK_TOP")
            return
        if entry_sp_context(node):
            self.note(node, "entry-sp-outside-window")
        preferred = assign_target(node)
        resolved = self.address(value, node, preferred)
        if resolved is None:
            return
        text, names = resolved
        self.replace(node, text, *names)

    def routine_bank(self, name: str) -> int | None:
        located = self.tables.named.get(name)
        return located[0] if located is not None else None

    def enclosing_routine(self, node: ast.AST) -> str | None:
        cur = node
        while parent(cur) is not None:
            cur = parent(cur)
            if isinstance(cur, ast.For):
                for sub in ast.walk(cur.iter):
                    if isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Name) \
                            and sub.value.id == "SCHEMA2_CASES" and str_key(sub.slice):
                        return str_key(sub.slice)
            if isinstance(cur, ast.Assign):
                for target in cur.targets:
                    for sub in ast.walk(target):
                        if isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Name) \
                                and sub.value.id == "SCHEMA2_CASES" and str_key(sub.slice):
                            return str_key(sub.slice)
        return None

    def rewrite_pc(self, node: ast.Constant, bank: int | None, routine: str | None, bank_node: ast.AST | None) -> None:
        pc = node.value
        if pc < 0x4000:
            bank = 0
        elif bank is None and routine is not None:
            bank = self.routine_bank(routine)
        if bank is None:
            self.note(node, "pc-unresolved")
            return
        found = self.tables.rom_label(bank, pc)
        if found is None:
            self.note(node, "pc-unresolved")
            return
        label, offset = found
        self.replace(node, offset_expr(f'sym("{label}")', offset), "sym")
        if isinstance(bank_node, ast.Constant) and type(bank_node.value) is int and bank_node.value == bank \
                and self.tables.named[label][0] == bank:
            start, end = self.span(bank_node)
            self.result.edits.append(Edit(start, end, f'sym_bank("{label}")'))
            self.result.names.add("sym_bank")
            self.claimed.add(id(bank_node))

    def completion_pcs(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Dict):
                keys = {str_key(k): v for k, v in zip(node.keys, node.values) if str_key(k)}
                pc = keys.get("pc")
                if isinstance(pc, ast.Constant) and type(pc.value) is int and pc.value < 0x8000:
                    bank_node = keys.get("bank")
                    bank = bank_node.value if isinstance(bank_node, ast.Constant) and type(bank_node.value) is int else None
                    self.rewrite_pc(pc, bank, self.enclosing_routine(node), bank_node)
                predicate = keys.get("predicate")
                if isinstance(predicate, ast.Constant) and isinstance(predicate.value, str) \
                        and PREDICATE.search(predicate.value):
                    self.rewrite_predicate(predicate)
            if isinstance(node, ast.For) and isinstance(node.target, ast.Tuple):
                self.tuple_pcs(node)

    def tuple_pcs(self, loop: ast.For) -> None:
        names = [t.id if isinstance(t, ast.Name) else None for t in loop.target.elts]
        pc_name = None
        for sub in ast.walk(ast.Module(body=loop.body, type_ignores=[])):
            if isinstance(sub, ast.Dict):
                for key, value in zip(sub.keys, sub.values):
                    if str_key(key) == "pc" and isinstance(value, ast.Name) and value.id in names:
                        pc_name = value.id
        if pc_name is None or not isinstance(loop.iter, (ast.Tuple, ast.List)):
            return
        index = names.index(pc_name)
        for element in loop.iter.elts:
            if not isinstance(element, (ast.Tuple, ast.List)) or len(element.elts) != len(names):
                continue
            pc = element.elts[index]
            routine = next((str_key(e) for e in element.elts if str_key(e)), None)
            if isinstance(pc, ast.Constant) and type(pc.value) is int and id(pc) not in self.claimed:
                self.rewrite_pc(pc, None, routine, None)

    def rewrite_predicate(self, node: ast.Constant) -> None:
        start, end = self.span(node)
        token = self.lines[node.lineno - 1][start[1]:end[1]] if node.lineno == node.end_lineno else ""
        if not token or token[0] not in "\"'" or token.startswith(("'''", '"""')):
            self.note(node, "predicate-unhandled")
            return
        quote = token[0]
        body = token[1:-1]
        inner = "'" if quote == '"' else '"'

        def sub(match: re.Match) -> str:
            digits = match.group(1)
            value = int(digits, 16)
            resolved = self.address(value, node)
            if resolved is None:
                raise ValueError(digits)
            text, names = resolved
            self.result.names.update(names)
            text = text.replace('"', inner)
            spec = "04X" if digits.isupper() and not digits.isdigit() else "04x"
            return "mem:0x{" + text + ":" + spec + "}"

        try:
            rewritten = PREDICATE.sub(sub, body)
        except ValueError:
            self.note(node, "predicate-unhandled")
            return
        self.result.edits.append(Edit(start, end, "f" + quote + rewritten + quote))
        self.claimed.add(id(node))

    def fixture_changes(self) -> None:
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue
            name = call_name(node)
            if not (name.endswith("_fixture") or name == "case"):
                continue
            entries: list[tuple[int, ast.AST]] = []
            removals: list[ast.keyword] = []
            for kw in node.keywords:
                if kw.arg is None and isinstance(kw.value, ast.Dict) \
                        and all(str_key(k) and FIXTURE_KEY.fullmatch(str_key(k)) for k in kw.value.keys):
                    entries.extend((int(str_key(k), 16), v) for k, v in zip(kw.value.keys, kw.value.values))
                    removals.append(kw)
                elif kw.arg is not None and FIXTURE_KEY.fullmatch(kw.arg) and not kw.arg.isdigit():
                    entries.append((int(kw.arg, 16), kw.value))
                    removals.append(kw)
            if not entries:
                continue
            parts = []
            for value, payload in entries:
                anchor = payload
                resolved = self.address(value, anchor)
                if resolved is None:
                    parts = None
                    break
                text, names = resolved
                self.result.names.update(names)
                parts.append(f"{text}: {self.source(payload)}")
            if parts is None:
                self.note(node, "fixture-unresolved")
                continue
            first = removals[0]
            start = (first.lineno, self.char_col(first.lineno, first.col_offset))
            end = (first.end_lineno, self.char_col(first.end_lineno, first.end_col_offset))
            self.result.edits.append(Edit(start, end, "changes={" + ", ".join(parts) + "}"))
            for kw in removals[1:]:
                self.remove_keyword(node, kw)
            for kw in removals:
                for sub in ast.walk(kw):
                    self.claimed.add(id(sub))

    def remove_keyword(self, call: ast.Call, kw: ast.keyword) -> None:
        items = sorted([*call.args, *call.keywords], key=lambda n: (n.lineno, n.col_offset))
        index = items.index(kw)
        prev = items[index - 1]
        start = (prev.end_lineno, self.char_col(prev.end_lineno, prev.end_col_offset))
        end = (kw.end_lineno, self.char_col(kw.end_lineno, kw.end_col_offset))
        self.result.edits.append(Edit(start, end, ""))

    def run(self) -> Result:
        self.fixture_changes()
        self.completion_pcs()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Constant) and type(node.value) is int and not isinstance(node.value, bool) \
                    and ram_region(node.value) and id(node) not in self.claimed:
                self.classify(node)
        return self.result


def import_names(tree: ast.Module) -> tuple[ast.ImportFrom | None, set[str]]:
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == SYMBOLS_MODULE:
            return node, {alias.name for alias in node.names}
    return None, set()


def apply(text: str, edits: list[Edit], names: set[str]) -> str:
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    def pos(point: tuple[int, int]) -> int:
        return offsets[point[0] - 1] + point[1]

    ordered = sorted(edits, key=lambda e: pos(e.start), reverse=True)
    last = None
    for edit in ordered:
        if last is not None and pos(edit.end) > last:
            raise SystemExit(f"overlapping edits at {edit.start}")
        last = pos(edit.start)
    out = text
    for edit in ordered:
        out = out[:pos(edit.start)] + edit.text + out[pos(edit.end):]
    if not names:
        return out
    tree = ast.parse(out)
    existing, have = import_names(tree)
    wanted = sorted(names | have, key=lambda n: (not n.isupper(), n))
    statement = f"from {SYMBOLS_MODULE} import {', '.join(wanted)}\n"
    lines = out.splitlines(keepends=True)
    if existing is not None:
        lines[existing.lineno - 1:existing.end_lineno] = [statement]
        return "".join(lines)
    anchor = 0
    body = tree.body
    index = 0
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        anchor = body[0].end_lineno
        index = 1
    while index < len(body) and isinstance(body[index], ast.ImportFrom) and body[index].module == "__future__":
        anchor = body[index].end_lineno
        index += 1
    lines.insert(anchor, statement)
    return "".join(lines)


def shadowed(text: str, names: set[str]) -> list[str]:
    tree = ast.parse(text)
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in names:
            found.add(node.id)
        elif isinstance(node, ast.arg) and node.arg in names:
            found.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names:
            found.add(node.name)
        elif isinstance(node, ast.alias) and (node.asname or node.name) in names \
                and not (isinstance(parent(node), ast.ImportFrom) and parent(node).module == SYMBOLS_MODULE):
            found.add(node.asname or node.name)
    return sorted(found)


def modules(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(p).resolve() for p in paths]
    return sorted(p for p in CASES.glob("*.py") if p.name not in SKIP)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("modules", nargs="*")
    parser.add_argument("--check", action="store_true", help="report pending rewrites without writing")
    parser.add_argument("--report", type=Path, help="write the per-site notes as JSON")
    parser.add_argument("--out", type=Path, help="write rewritten modules into this directory")
    args = parser.parse_args()
    tables = Tables.load()
    notes: list[dict] = []
    pending = 0
    for path in modules(args.modules):
        rewriter = Rewriter(tables, path)
        result = rewriter.run()
        notes.extend(result.notes)
        if not result.edits:
            continue
        pending += 1
        text = apply(rewriter.text, result.edits, result.names)
        clash = shadowed(rewriter.text, result.names)
        if clash:
            notes.append({"file": path.name, "line": 0, "kind": "shadowed-import", "names": clash})
        compile(text, str(path), "exec")
        if args.check:
            print(f"{path.relative_to(ROOT)}: {len(result.edits)} rewrites pending")
            continue
        target = args.out / path.name if args.out else path
        target.write_text(text)
    if args.report:
        args.report.write_text(json.dumps(notes, indent=1))
    kinds: dict[str, int] = {}
    for item in notes:
        kinds[item["kind"]] = kinds.get(item["kind"], 0) + 1
    print(f"case_symbols: {pending} modules {'pending' if args.check else 'rewritten'}; notes " +
          ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())))
    return 1 if args.check and pending else 0


if __name__ == "__main__":
    raise SystemExit(main())
