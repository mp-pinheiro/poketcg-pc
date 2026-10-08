#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.factory_blocks import code_mask, parse

SHARED_TREES = ("src/home", "src/probe")
SOURCE_RE = re.compile(r"^\s*(?:static\s+)?CardId\s+(\w+)\s*\(", re.MULTILINE)
TOKEN_RE = re.compile(
    r"(?P<string>\"[^\"\n]*\"|'[^'\n]*')"
    r"|(?P<number>0[xX][0-9A-Fa-f]+[uUlL]*|\d+[uUlL]*)"
    r"|(?P<name>[A-Za-z_]\w*)"
    r"|(?P<op><<=|>>=|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^]=|[{}()\[\];,=+\-*/%&|^!~<>?:.])"
)
TRACKED = {"uint8_t", "CardId"}
QUALIFIERS = {"const", "static", "volatile", "register", "inline"}
TYPE_WORDS = {
    "uint8_t", "uint16_t", "uint32_t", "int8_t", "int16_t", "int32_t", "int", "unsigned", "signed",
    "char", "short", "long", "size_t", "CardId", "const", "volatile", "void", "bool", "_Bool",
}
NARROW_TYPES = {"uint8_t", "int8_t", "char", "bool", "_Bool"}
BINARY = {
    "||": 3, "&&": 4, "|": 5, "^": 6, "&": 7, "==": 8, "!=": 8, "<": 9, ">": 9, "<=": 9, ">=": 9,
    "<<": 10, ">>": 10, "+": 11, "-": 11, "*": 12, "/": 12, "%": 12,
}
LOGICAL = {"||", "&&", "==", "!=", "<", ">", "<=", ">="}
ASSIGN = {"=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="}
WIDENING_ASSIGN = {"=", "+=", "-=", "|=", "^="}
DECLARATION_BEFORE = {None, ";", "{", "}", "(", ",", ":"}
ALLOWED: dict[tuple[str, str], str] = {}


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    start: int


def card_id_sources() -> set[str]:
    names: set[str] = set()
    for suffix in ("*.h", "*.c"):
        for path in sorted((ROOT / "src" / "home").glob(suffix)):
            names.update(SOURCE_RE.findall(code_mask(path.read_text())))
    return names


def tokenize(body: str) -> list[Token]:
    code = "\n".join("" if line.lstrip().startswith("#") else line for line in body.split("\n"))
    return [Token(match.lastgroup or "op", match.group(0), match.start()) for match in TOKEN_RE.finditer(code)]


def number(text: str) -> int | None:
    try:
        return int(text.rstrip("uUlL"), 0)
    except ValueError:
        return None


class Checker:
    def __init__(self, body: str, sources: set[str]) -> None:
        self.tokens = tokenize(body)
        self.sources = sources
        self.scopes: list[dict[str, str]] = [{}]
        self.hits: list[tuple[int, str]] = []
        self.declaration_assignments: set[int] = set()

    def text(self, index: int) -> str | None:
        return self.tokens[index].text if 0 <= index < len(self.tokens) else None

    def matching(self, index: int) -> int:
        opener = self.tokens[index].text
        closer = {"(": ")", "[": "]", "{": "}"}[opener]
        depth = 0
        for position in range(index, len(self.tokens)):
            if self.tokens[position].text == opener:
                depth += 1
            elif self.tokens[position].text == closer:
                depth -= 1
                if depth == 0:
                    return position
        return len(self.tokens) - 1

    def resolve(self, name: str) -> str | None:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def cast_type(self, index: int) -> tuple[str, int] | None:
        if self.text(index) != "(":
            return None
        cursor = index + 1
        words = []
        while cursor < len(self.tokens) and (self.tokens[cursor].text in TYPE_WORDS or self.tokens[cursor].text == "*"):
            words.append(self.tokens[cursor].text)
            cursor += 1
        if not words or self.text(cursor) != ")":
            return None
        return " ".join(word for word in words if word not in {"const", "volatile"}), cursor + 1

    def parse_expression(self, index: int, minimum: int = 1) -> tuple[tuple, int]:
        left, index = self.parse_unary(index)
        while index < len(self.tokens):
            operator = self.tokens[index].text
            if operator == "?" and minimum <= 2:
                middle, index = self.parse_expression(index + 1, 1)
                if self.text(index) != ":":
                    return left, index
                right, index = self.parse_expression(index + 1, 2)
                left = ("ternary", left, middle, right)
                continue
            if operator in ASSIGN and minimum <= 1:
                right, index = self.parse_expression(index + 1, 1)
                left = ("assign", operator, left, right)
                continue
            precedence = BINARY.get(operator)
            if precedence is None or precedence < minimum:
                return left, index
            right, index = self.parse_expression(index + 1, precedence + 1)
            left = ("binary", operator, left, right)
        return left, index

    def parse_unary(self, index: int) -> tuple[tuple, int]:
        if index >= len(self.tokens):
            return ("other",), index
        token = self.tokens[index]
        if token.text in {"!", "~", "-", "+", "*", "&", "++", "--"}:
            operand, end = self.parse_unary(index + 1)
            return ("unary", token.text, operand), end
        if token.text == "sizeof":
            if self.text(index + 1) == "(":
                return ("number", 1), self.matching(index + 1) + 1
            _, end = self.parse_unary(index + 1)
            return ("number", 1), end
        if token.text == "(":
            cast = self.cast_type(index)
            if cast is not None and self.text(cast[1]) != "{":
                operand, end = self.parse_unary(cast[1])
                return ("cast", cast[0], operand), end
            close = self.matching(index)
            if self.text(close + 1) == "{" and (cast is not None or close == index + 2):
                return self.parse_postfix(("other",), self.matching(close + 1) + 1)
            inner, end = self.parse_expression(index + 1, 1)
            return self.parse_postfix(("paren", inner), close + 1 if end <= close else end)
        if token.text == "{":
            return ("other",), self.matching(index) + 1
        if token.kind == "name":
            return self.parse_postfix(("name", token.text), index + 1)
        if token.kind == "number":
            return ("number", number(token.text)), index + 1
        if token.kind == "string":
            return ("other",), index + 1
        return ("other",), index

    def parse_postfix(self, node: tuple, index: int) -> tuple[tuple, int]:
        while index < len(self.tokens):
            text = self.tokens[index].text
            if text == "(":
                node = ("call", node)
                index = self.matching(index) + 1
            elif text == "[":
                node = ("index", node)
                index = self.matching(index) + 1
            elif text in {".", "->"}:
                node = ("member", node)
                index += 2
            elif text in {"++", "--"}:
                index += 1
            else:
                return node, index
        return node, index

    def byte_constant(self, node: tuple) -> bool:
        while node[0] == "paren":
            node = node[1]
        return node[0] == "number" and node[1] is not None and node[1] <= 0xFF

    def wide(self, node: tuple) -> bool:
        kind = node[0]
        if kind == "name":
            return self.resolve(node[1]) == "CardId"
        if kind == "call":
            return node[1][0] == "name" and node[1][1] in self.sources and self.resolve(node[1][1]) is None
        if kind == "paren":
            return self.wide(node[1])
        if kind == "unary":
            return node[1] in {"-", "+", "~", "++", "--"} and self.wide(node[2])
        if kind == "cast":
            return node[1] not in NARROW_TYPES and "*" not in node[1] and self.wide(node[2])
        if kind == "binary":
            operator, left, right = node[1], node[2], node[3]
            if operator in LOGICAL:
                return False
            if operator == "&":
                return not (self.byte_constant(left) or self.byte_constant(right)) and (self.wide(left) or self.wide(right))
            if operator == ">>":
                shift = right[1] if right[0] == "number" else None
                return self.wide(left) and not (shift is not None and shift >= 8)
            if operator == "<<":
                return self.wide(left)
            return self.wide(left) or self.wide(right)
        if kind == "ternary":
            return self.wide(node[2]) or self.wide(node[3])
        if kind == "assign":
            return self.wide(node[3])
        return False

    def previous_significant(self, index: int) -> str | None:
        cursor = index - 1
        while cursor >= 0 and self.tokens[cursor].text in QUALIFIERS:
            cursor -= 1
        return self.tokens[cursor].text if cursor >= 0 else None

    def parameter_list(self, index: int) -> bool:
        depth = 0
        for cursor in range(index - 1, -1, -1):
            text = self.tokens[cursor].text
            if text == ")":
                depth += 1
            elif text == "(":
                if depth == 0:
                    return cursor > 0 and self.tokens[cursor - 1].kind == "name" and self.tokens[cursor - 1].text not in {"for", "if", "while", "switch", "return", "sizeof"}
                depth -= 1
            elif text in {";", "{", "}"} and depth == 0:
                return False
        return False

    def declare(self, index: int) -> None:
        type_name = self.tokens[index].text
        in_parameters = self.parameter_list(index)
        cursor = index + 1
        while cursor < len(self.tokens):
            pointer = False
            while self.text(cursor) in {"*", "const", "volatile"}:
                pointer = pointer or self.text(cursor) == "*"
                cursor += 1
            if cursor >= len(self.tokens) or self.tokens[cursor].kind != "name":
                return
            name = self.tokens[cursor]
            cursor += 1
            if self.text(cursor) == "(" and not in_parameters:
                return
            array = False
            while self.text(cursor) == "[":
                array = True
                cursor = self.matching(cursor) + 1
            kind = "pointer" if pointer else ("array" if array else type_name)
            if self.text(cursor) == "=":
                self.declaration_assignments.add(cursor)
                if self.text(cursor + 1) == "{":
                    cursor = self.matching(cursor + 1) + 1
                else:
                    value, cursor = self.parse_expression(cursor + 1, 2)
                    if kind == "uint8_t" and self.wide(value):
                        self.hits.append((name.start, name.text))
            self.scopes[-1][name.text] = kind
            if in_parameters or self.text(cursor) != ",":
                return
            cursor += 1

    def function_return(self, index: int) -> str | None:
        name = index
        if self.text(name + 1) != "(":
            return None
        close = self.matching(name + 1)
        if self.text(close + 1) != "{":
            return None
        cursor = name - 1
        if cursor >= 0 and self.tokens[cursor].text == "*":
            return "pointer"
        return self.tokens[cursor].text if cursor >= 0 else None

    def run(self) -> list[tuple[int, str]]:
        braces: list[tuple[str, str | None]] = []
        returns: str | None = None
        pending: str | None = None
        index = 0
        while index < len(self.tokens):
            token = self.tokens[index]
            text = token.text
            if text == "{":
                if pending is not None:
                    braces.append(("function", returns))
                    returns = pending
                    pending = None
                else:
                    braces.append(("block", None))
                    self.scopes.append({})
                index += 1
                continue
            if text == "}":
                if braces:
                    kind, outer = braces.pop()
                    if kind == "function":
                        returns = outer
                        self.scopes.pop()
                    elif len(self.scopes) > 1:
                        self.scopes.pop()
                index += 1
                continue
            if token.kind == "name" and not braces and self.text(index + 1) == "(":
                result = self.function_return(index)
                if result is not None:
                    pending = result
                    self.scopes.append({})
            if text in TRACKED and self.previous_significant(index) in DECLARATION_BEFORE:
                self.declare(index)
                index += 1
                continue
            if text == "(":
                cast = self.cast_type(index)
                if cast is not None and cast[0] == "uint8_t" and self.text(cast[1]) != "{":
                    operand, _ = self.parse_unary(cast[1])
                    if self.wide(operand):
                        self.hits.append((token.start, "(uint8_t) cast"))
            if text == "return" and returns == "uint8_t":
                value, _ = self.parse_expression(index + 1)
                if self.wide(value):
                    self.hits.append((token.start, "return"))
            if (text in WIDENING_ASSIGN and index not in self.declaration_assignments and index > 0
                    and self.tokens[index - 1].kind == "name"
                    and self.text(index - 2) not in {".", "->"}
                    and self.resolve(self.tokens[index - 1].text) == "uint8_t"):
                value, _ = self.parse_expression(index + 1, 2)
                if self.wide(value):
                    self.hits.append((self.tokens[index - 1].start, self.tokens[index - 1].text))
            index += 1
        return self.hits


def block_failures(path: Path, block_name: str, body: str,
                   sources: set[str]) -> list[tuple[str, int, str, str]]:
    lines = body.split("\n")
    failures = []
    for start, variable in sorted(set(Checker(body, sources).run())):
        number_of_line = body.count("\n", 0, start)
        failures.append((block_name, number_of_line, variable, lines[number_of_line].strip()))
    return failures


def lint(paths: list[Path]) -> tuple[list[str], set[tuple[str, str]]]:
    sources = card_id_sources()
    failures: list[str] = []
    used: set[tuple[str, str]] = set()
    for path in paths:
        text = path.read_text(errors="replace")
        masked_lines = code_mask(text).split("\n")
        for block in parse(text, path).blocks:
            body = "\n".join(masked_lines[block.open_line + 1:block.close_line])
            for name, offset, variable, line in block_failures(path, block.name, body, sources):
                key = (path.stem, name)
                if key in ALLOWED:
                    used.add(key)
                    continue
                failures.append(f"{path.relative_to(ROOT)}:{block.open_line + 2 + offset}: {name} narrows a card id into "
                                f"uint8_t ({variable}): {line}")
    return failures, used


def main() -> int:
    parser = argparse.ArgumentParser(description="Reject card ids narrowed into uint8_t in shared C.")
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = [path.resolve() for path in args.paths] if args.paths else [
        path for tree in SHARED_TREES for path in sorted((ROOT / tree).glob("*.c"))
    ]
    failures, used = lint(paths)
    if not args.paths:
        failures += [f"stale allowlist entry {stem}:{name} ({reason})" for (stem, name), reason in sorted(ALLOWED.items())
                     if (stem, name) not in used]
    for failure in failures:
        print(failure)
    print(f"lint-card-ids: files={len(paths)} failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
