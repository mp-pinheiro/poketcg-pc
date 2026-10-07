#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.profiles import get_profile, load_catalog  # noqa: E402

NAME = r"[A-Za-z_][A-Za-z0-9_]*"
MARKER_RE = re.compile(rf"^/\* (>>>|<<<) (factory|part) ({NAME}) \*/$")
DIRECTIVE_RE = re.compile(rf"^/\* (---|===) (factory|part) ({NAME}) \*/$")
LOOSE_RE = re.compile(r"^\s*/\*\s*(>>>|<<<|---|===)\s")
KINDS = ("factory", "part")
SHARED_TREES = ("src/home", "src/probe")
PROBE_ROW_RE = re.compile(r'\{\s*"([A-Za-z_][A-Za-z0-9_.]*)"\s*,\s*(adapt_\w+)\s*\}')
IDENT_RE = re.compile(NAME)


class BlockError(ValueError):
    pass


@dataclass
class Block:
    kind: str
    name: str
    open_line: int
    close_line: int
    body: list[str]


@dataclass
class Directive:
    op: str
    kind: str
    name: str
    line: int


@dataclass
class Parsed:
    path: Path
    lines: list[str]
    blocks: list[Block] = field(default_factory=list)
    directives: list[Directive] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def block(self, name: str) -> Block | None:
        return next((block for block in self.blocks if block.name == name), None)

    def outside(self) -> list[int]:
        inside = set()
        for block in self.blocks:
            inside.update(range(block.open_line, block.close_line + 1))
        inside.update(directive.line for directive in self.directives)
        return [index for index in range(len(self.lines)) if index not in inside]


def parse(text: str, path: Path = Path("<text>")) -> Parsed:
    parsed = Parsed(path, text.split("\n"))
    current: tuple[str, str, int] | None = None
    seen: set[str] = set()
    removals: set[str] = set()
    for index, line in enumerate(parsed.lines):
        marker = MARKER_RE.match(line)
        directive = DIRECTIVE_RE.match(line)
        where = f"{path}:{index + 1}"
        if marker is None and directive is None:
            if LOOSE_RE.match(line):
                parsed.errors.append(f"{where}: malformed marker: {line.strip()}")
            continue
        if directive is not None:
            if current is not None:
                parsed.errors.append(f"{where}: directive inside block {current[1]}")
            op, kind, name = directive.groups()
            parsed.directives.append(Directive(op, kind, name, index))
            if name in (removals if op == "---" else seen):
                parsed.errors.append(f"{where}: duplicate name {name}")
            (removals if op == "---" else seen).add(name)
            continue
        op, kind, name = marker.groups()
        if op == ">>>":
            if current is not None:
                parsed.errors.append(f"{where}: {kind} {name} opens inside {current[0]} {current[1]} (line {current[2] + 1})")
            current = (kind, name, index)
            continue
        if current is None:
            parsed.errors.append(f"{where}: {kind} {name} closes without an open block")
            continue
        if (kind, name) != current[:2]:
            parsed.errors.append(f"{where}: {kind} {name} closes {current[0]} {current[1]} (line {current[2] + 1})")
        else:
            if name in seen:
                parsed.errors.append(f"{where}: duplicate name {name}")
            seen.add(name)
            parsed.blocks.append(Block(kind, name, current[2], index, parsed.lines[current[2] + 1:index]))
        current = None
    if current is not None:
        parsed.errors.append(f"{path}:{current[2] + 1}: {current[0]} {current[1]} never closes")
    return parsed


def code_mask(text: str) -> str:
    out = []
    index = 0
    length = len(text)
    while index < length:
        char = text[index]
        pair = text[index:index + 2]
        if pair == "/*":
            end = text.find("*/", index + 2)
            end = length if end < 0 else end + 2
            out.append("".join("\n" if c == "\n" else " " for c in text[index:end]))
            index = end
        elif pair == "//":
            end = text.find("\n", index)
            end = length if end < 0 else end
            out.append(" " * (end - index))
            index = end
        elif char in "\"'":
            end = index + 1
            while end < length and text[end] != char:
                end += 2 if text[end] == "\\" else 1
            end = min(end + 1, length)
            out.append(char + "".join("\n" if c == "\n" else "_" for c in text[index + 1:end - 1]) + (char if end - index > 1 else ""))
            index = end
        else:
            out.append(char)
            index += 1
    return "".join(out)


@dataclass
class Item:
    first: int
    last: int
    kind: str
    name: str | None


def guard_lines(code: list[str]) -> set[int]:
    directives = [(index, line.strip()) for index, line in enumerate(code) if line.strip()]
    if len(directives) < 3 or not re.fullmatch(r"#\s*endif", directives[-1][1]):
        return set()
    for position, (index, line) in enumerate(directives[:-2]):
        if not line.startswith("#"):
            return set()
        match = re.fullmatch(rf"#\s*ifndef\s+({NAME})", line)
        if match and re.fullmatch(rf"#\s*define\s+{match.group(1)}", directives[position + 1][1]):
            return {index, directives[position + 1][0], directives[-1][0]}
        if line.startswith(("#if", "#endif", "#else", "#elif")):
            return set()
    return set()


def directive_name(line: str) -> tuple[str, str | None]:
    match = re.match(rf"\s*#\s*(\w+)\s*({NAME})?", line)
    if not match:
        return "", None
    return match.group(1), match.group(2)


def scan_items(lines: list[str], code: list[str], start: int, end: int, guards: set[int]) -> list[Item]:
    items: list[Item] = []
    index = start
    while index < end:
        if index in guards or not code[index].strip():
            index += 1
            continue
        stripped = code[index].strip()
        if stripped.startswith("#"):
            first = index
            kind = "include"
            name = None
            depth = 0
            while True:
                word, ident = directive_name(code[index])
                if word in {"if", "ifdef", "ifndef"}:
                    depth += 1
                    kind = kind if kind != "include" else "include"
                elif word == "endif":
                    depth -= 1
                elif word == "define":
                    kind = "define"
                    name = name or ident
                elif word not in {"include", "else", "elif", "endif"}:
                    kind = "define"
                while code[index].rstrip().endswith("\\") and index + 1 < end:
                    index += 1
                if depth <= 0:
                    break
                index += 1
                if index >= end:
                    raise BlockError(f"unterminated conditional starting at line {first + 1}")
                if code[index].strip() and not code[index].strip().startswith("#"):
                    kind = "define"
            items.append(Item(first, index, kind, name))
            index += 1
            continue
        first = index
        text = []
        braces = parens = 0
        body = False
        last_significant = ""
        done_line = None
        while index < end and done_line is None:
            line = code[index]
            column = 0
            while column < len(line):
                char = line[column]
                if char == "(":
                    parens += 1
                elif char == ")":
                    parens -= 1
                elif char == "{":
                    if braces == 0 and parens == 0 and last_significant == ")":
                        body = True
                    braces += 1
                elif char == "}":
                    braces -= 1
                    if braces == 0 and parens == 0 and body:
                        done_line = index
                elif char == ";" and braces == 0 and parens == 0:
                    done_line = index
                if not char.isspace():
                    last_significant = char
                column += 1
                if done_line is not None:
                    break
            text.append(line if done_line is None else line[:column])
            if done_line is None:
                index += 1
        if done_line is None:
            raise BlockError(f"declaration starting at line {first + 1} never ends")
        rest = code[done_line][column:].strip()
        kind, name = classify("\n".join(text), body)
        if items and items[-1].last == first and items[-1].kind not in {"include", "define"}:
            items[-1].last = done_line
        else:
            items.append(Item(first, done_line, kind, name))
        if rest:
            code = code[:done_line] + [" " * column + code[done_line][column:]] + code[done_line + 1:]
            index = done_line
            if rest.startswith("#"):
                raise BlockError(f"preprocessor text after a declaration on line {done_line + 1}")
            continue
        index = done_line + 1
    return items


def classify(text: str, body: bool) -> tuple[str, str | None]:
    flat = " ".join(text.split())
    if flat.startswith("typedef"):
        pointer = re.search(rf"\(\s*\*\s*({NAME})\s*\)", flat)
        if pointer and "{" not in flat:
            return "typedef", pointer.group(1)
        tail = re.search(rf"({NAME})\s*(?:\[[^\]]*\]\s*)*;?\s*$", flat.rstrip(";").rstrip())
        return "typedef", tail.group(1) if tail else None
    tag = re.match(rf"(?:struct|union|enum)\s+({NAME})\s*\{{", flat)
    if tag and re.search(r"\}\s*;?\s*$", flat):
        return "type", tag.group(1)
    depth = 0
    for position, char in enumerate(flat):
        if char == "(" and depth == 0:
            head = flat[:position].rstrip()
            after = flat[position + 1:].lstrip()
            if after.startswith("*"):
                pointer = re.match(rf"\*\s*({NAME})", after)
                return "data", pointer.group(1) if pointer else None
            name = re.search(rf"({NAME})$", head)
            if name and name.group(1) not in {"sizeof", "return"}:
                return ("function" if body else "prototype"), name.group(1)
            break
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "=" and depth == 0:
            break
    declarator = re.split(r"[=\[;,]", flat, maxsplit=1)[0].rstrip()
    name = re.search(rf"({NAME})$", declarator)
    return "data", name.group(1) if name else None


@dataclass
class Context:
    routines: frozenset[str]
    adapters: dict[str, str]


def contract_keys(node: ast.AST) -> list[str]:
    targets = node.targets if isinstance(node, ast.Assign) else []
    keys = []
    for target in targets:
        if (isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name)
                and target.value.id in {"CONTRACT", "CASES"}
                and isinstance(target.slice, ast.Constant) and isinstance(target.slice.value, str)):
            keys.append(target.slice.value)
        if isinstance(target, ast.Name) and target.id in {"CONTRACT", "CASES"} and isinstance(node.value, ast.Dict):
            keys += [key.value for key in node.value.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
    return keys


def routine_names(modules: list[Path]) -> frozenset[str]:
    names: set[str] = set()
    for path in modules:
        for node in ast.walk(ast.parse(path.read_text())):
            names.update(contract_keys(node))
    return frozenset(name.replace(".", "_") for name in names) | frozenset(names)


def adapter_routines(text: str) -> dict[str, str]:
    return {adapter: routine.replace(".", "_") for routine, adapter in PROBE_ROW_RE.findall(text)}


def block_kind(name: str | None, context: Context) -> str:
    return "factory" if name is not None and name in context.routines else "part"


def unique(name: str, taken: set[str]) -> str:
    candidate = name
    suffix = 2
    while candidate in taken:
        candidate = f"{name}_{suffix}"
        suffix += 1
    taken.add(candidate)
    return candidate


def wrap_text(text: str, path: Path, context: Context, fine_defines: bool = False) -> str:
    parsed = parse(text, path)
    if parsed.errors:
        raise BlockError("; ".join(parsed.errors))
    lines = parsed.lines
    code = code_mask(text).split("\n")
    header = path.suffix == ".h"
    guards = guard_lines(code) if header else set()
    adapters = adapter_routines(text) if context.adapters is None else context.adapters
    taken = {block.name for block in parsed.blocks} | {directive.name for directive in parsed.directives}
    occupied = set()
    for block in parsed.blocks:
        occupied.update(range(block.open_line, block.close_line + 1))
    occupied.update(directive.line for directive in parsed.directives)
    occupied.update(guards)
    regions = []
    start = None
    for index in range(len(lines)):
        if index in occupied:
            if start is not None:
                regions.append((start, index))
                start = None
        elif start is None:
            start = index
    if start is not None:
        regions.append((start, len(lines)))
    inserts_before: dict[int, list[str]] = {}
    inserts_after: dict[int, list[str]] = {}
    moves: dict[int, list[int]] = {}
    for region_start, region_end in regions:
        items = scan_items(lines, code, region_start, region_end, guards)
        comment_lines = [index for index in range(region_start, region_end)
                         if index not in guards and lines[index].strip() and not code[index].strip()]
        claimed: set[int] = set()
        previous_end = region_start - 1
        groups: list[list[Item]] = []
        for item in items:
            if groups and item.kind in {"include", "define"} and groups[-1][-1].kind == item.kind \
                    and not (fine_defines and item.kind == "define"):
                groups[-1].append(item)
            else:
                groups.append([item])
        named: list[tuple[int, int, str, str]] = []
        for position, group in enumerate(groups):
            first, last = group[0].first, group[-1].last
            leading = [index for index in comment_lines if previous_end < index < first and index not in claimed]
            if leading:
                first = min(first, leading[0])
                claimed.update(leading)
            claimed.update(index for index in comment_lines if first <= index <= last)
            item = group[0]
            if item.kind == "include":
                following = next((g[0].name for g in groups[position + 1:] if g[0].name), None)
                base = "includes" if not named and region_start == regions[0][0] else f"includes_{following or 'tail'}"
                kind = "part"
            elif item.kind == "define":
                base = item.name or "defines"
                kind = "part"
            elif item.kind == "function" and item.name and item.name.startswith("adapt_") and item.name in adapters:
                base = adapters[item.name]
                kind = block_kind(base, context)
            elif item.kind in {"function", "prototype"}:
                base = item.name or "declaration"
                if item.kind == "prototype" and not header:
                    base = f"{base}_decl"
                kind = block_kind(item.name, context) if item.kind == "function" or header else "part"
            else:
                base = item.name or "declaration"
                kind = "part"
            named.append((first, last, kind, unique(base, taken)))
            previous_end = last
        trailing = [index for index in comment_lines if index not in claimed]
        if trailing:
            next_block = next((block for block in parsed.blocks if block.open_line == region_end), None)
            if next_block is not None and all(index > previous_end for index in trailing):
                moves.setdefault(next_block.open_line, []).extend(trailing)
            elif named:
                first, last, kind, name = named[-1]
                named[-1] = (min(first, trailing[0]), max(last, trailing[-1]), kind, name)
            else:
                named.append((trailing[0], trailing[-1], "part", unique("notes", taken)))
        for first, last, kind, name in named:
            inserts_before.setdefault(first, []).append(f"/* >>> {kind} {name} */")
            inserts_after.setdefault(last, []).append(f"/* <<< {kind} {name} */")
    moved = {index for indexes in moves.values() for index in indexes}
    out: list[str] = []
    for index, line in enumerate(lines):
        if index in moved:
            continue
        out.extend(inserts_before.get(index, ()))
        out.append(line)
        if index in moves:
            out.extend(lines[moved_index] for moved_index in moves[index])
        out.extend(inserts_after.get(index, ()))
    return "\n".join(out)


def coarse(block: Block, lines: list[str], code: list[str]) -> bool:
    if block.kind == "factory" and block.name == "statics":
        return True
    if block.kind != "part":
        return False
    try:
        items = scan_items(lines, code, block.open_line + 1, block.close_line, set())
    except BlockError:
        return False
    return all(item.kind in {"include", "define"} for item in items) \
        and sum(1 for item in items if item.kind == "define") >= 2


def split_text(text: str, path: Path, context: Context) -> str:
    parsed = parse(text, path)
    if parsed.errors:
        raise BlockError("; ".join(parsed.errors))
    code = code_mask(text).split("\n")
    drop = set()
    for block in parsed.blocks:
        if coarse(block, parsed.lines, code):
            drop.update((block.open_line, block.close_line))
    if not drop:
        return text
    unwrapped = "\n".join(line for index, line in enumerate(parsed.lines) if index not in drop)
    return wrap_text(unwrapped, path, context, fine_defines=True)


def tree_paths(roots: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for root in roots:
        if root.is_file():
            paths.append(root)
        elif root.is_dir():
            paths.extend(sorted(root.glob("*.c")) + sorted(root.glob("*.h")))
    return paths


def default_roots() -> list[Path]:
    roots = [ROOT / tree for tree in SHARED_TREES]
    _, profiles = load_catalog(ROOT / "profiles" / "profiles.json")
    for profile in profiles.values():
        overlay = profile.overlay_path(ROOT)
        if overlay is not None:
            roots += [overlay / "home", overlay / "probe"]
    return roots


def is_override(path: Path) -> bool:
    _, profiles = load_catalog(ROOT / "profiles" / "profiles.json")
    resolved = path.resolve()
    for profile in profiles.values():
        overlay = profile.overlay_path(ROOT)
        if overlay is not None and overlay.resolve() in resolved.parents:
            return True
    return False


def lint_file(path: Path) -> list[str]:
    text = path.read_text()
    parsed = parse(text, path)
    errors = list(parsed.errors)
    if parsed.directives and not is_override(path):
        errors += [f"{path}:{directive.line + 1}: {directive.op} directive outside an override tree"
                   for directive in parsed.directives]
    code = code_mask(text).split("\n")
    guards = guard_lines(code) if path.suffix == ".h" else set()
    for index in parsed.outside():
        if index not in guards and parsed.lines[index].strip():
            errors.append(f"{path}:{index + 1}: outside any block: {parsed.lines[index].strip()[:80]}")
            break
    return errors


def context_for(path: Path, contexts: dict[str, Context]) -> Context:
    resolved = path.resolve()
    for key, context in contexts.items():
        if key != "shared" and Path(key) in resolved.parents:
            return context
    return contexts["shared"]


def build_contexts() -> dict[str, Context]:
    _, profiles = load_catalog(ROOT / "profiles" / "profiles.json")
    contexts = {"shared": Context(routine_names(profiles["vanilla"].case_modules(ROOT)), None)}
    for profile in profiles.values():
        overlay = profile.overlay_path(ROOT)
        if overlay is not None:
            contexts[str(overlay.resolve())] = Context(routine_names(profile.case_modules(ROOT)), None)
    return contexts


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse, lint and wrap named factory and part blocks in C sources.")
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="check markers and that every construct sits in a block")
    lint.add_argument("paths", nargs="*", type=Path)
    wrap = sub.add_parser("wrap", help="wrap every construct outside a block in a named block")
    wrap.add_argument("paths", nargs="*", type=Path)
    wrap.add_argument("--check", action="store_true", help="report files wrap would change, write nothing")
    split = sub.add_parser("split", help="split statics and multi-define blocks into one block per define")
    split.add_argument("paths", nargs="*", type=Path)
    split.add_argument("--check", action="store_true", help="report files split would change, write nothing")
    args = parser.parse_args()
    paths = tree_paths(args.paths or default_roots())
    if args.command == "lint":
        errors: list[str] = []
        blocks = 0
        for path in paths:
            errors += lint_file(path)
            blocks += len(parse(path.read_text(), path).blocks)
        for error in errors:
            print(error)
        print(f"lint-blocks: files={len(paths)} blocks={blocks} errors={len(errors)}")
        return 1 if errors else 0
    contexts = build_contexts()
    changed = 0
    failures = 0
    for path in paths:
        text = path.read_text()
        try:
            transform = split_text if args.command == "split" else wrap_text
            wrapped = transform(text, path, context_for(path, contexts))
        except BlockError as error:
            print(f"{path}: {error}")
            failures += 1
            continue
        if wrapped != text:
            changed += 1
            if not args.check:
                path.write_text(wrapped)
    print(f"{args.command}-blocks: files={len(paths)} changed={changed} failed={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
