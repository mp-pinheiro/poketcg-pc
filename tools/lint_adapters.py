#!/usr/bin/env python3
"""Gate against probe adapters that reimplement the routine they marshal.

An adapter's only job is to marshal ``ProbeState`` in and out around exactly one
call to the ported routine. Anything else is a second implementation that can
agree with the first while both are wrong -- the shape of every false green that
has shipped here (issue #19).

Two rules are enforced; see the report in issue #19 for the full reasoning.

  * R1 -- no integer literal >= 0x8000 in an adapter body. A marshalling layer
    has no business naming Game Boy addresses; the two shipped defects were
    exactly ``0xCAA0``/``0xCAA8`` and ``0xCAA5``. Decimal literals >= 0x8000 are
    caught too, so the rule cannot be ducked by dropping the ``0x``.

  * R3 -- exactly one routine call per adapter. ``pair``/``split`` are
    marshalling helpers, not routines; casts (``(uint8_t)``) and keywords
    (``sizeof``/``if``) are not calls. An adapter with zero calls is a pure
    reimplementation; one with two is re-deriving an output the routine already
    produced.

The allowlist below is deliberately tiny and each entry carries the reason the
adapter legitimately needs the construct. A stale entry -- the rule no longer
fires on it -- is itself a failure, so the list cannot silently bloat.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROBE_DIR = REPO_ROOT / "src" / "probe"

# R1 boundary: the smallest Game Boy address ($8000 / VRAM origin). No literal a
# marshalling layer touches should reach it.
ADDR_THRESHOLD = 0x8000

# Identifiers that look like ``name(`` but are not routine calls: C type casts,
# keywords, and the marshalling helpers.
NON_CALLS = {
	"uint8_t", "uint16_t", "uint32_t", "uint64_t",
	"int8_t", "int16_t", "int32_t", "int64_t",
	"size_t", "ssize_t", "ptrdiff_t",
	"int", "char", "void", "unsigned", "signed",
	"long", "short", "float", "double", "bool", "_Bool",
	"sizeof", "alignof", "_Alignof", "defined", "_Generic",
	"if", "for", "while", "switch", "return", "do", "else", "goto",
	"pair", "split",
}

# adapter -> {rule: why it is allowed}. Keep this tiny.
ALLOWLIST: dict[str, dict[str, str]] = {
	"adapt_GetCardSymbolData": {
		"R3": (
			"GetCardSymbolData's C signature returns only the table's first byte "
			"(a); the asm (menus.asm:643-651) additionally leaves b=0, c=2*id, "
			"hl=CardSymbolTable+2*id as residue no C field carries. The adapter "
			"recovers the index by calling CardTypeToSymbolID, which "
			"GetCardSymbolData itself calls at menus.asm:644 -- faithful to the "
			"asm's own call sequence, not a reimplementation. Dropping this entry "
			"needs the menus slice to widen GetCardSymbolData's return struct."
		),
	},
}

ADAPTER_SIG_RE = re.compile(r"\bstatic\s+void\s+(adapt_\w+)\s*\([^)]*\)\s*\{")
INT_LITERAL_RE = re.compile(r"(0[xX][0-9a-fA-F]+|\d+)([uUlL]*)")
CALL_RE = re.compile(r"\b([A-Za-z_]\w*)\s*\(")


@dataclass
class Adapter:
	name: str
	body: str
	path: Path
	start_line: int  # 1-based line of the '{'


@dataclass
class Violation:
	rule: str
	path: Path
	adapter: str
	line: int
	message: str


@dataclass
class Report:
	violations: list[Violation] = field(default_factory=list)
	stale_allowlist: list[str] = field(default_factory=list)

	@property
	def ok(self) -> bool:
		return not self.violations and not self.stale_allowlist


def strip_comments_and_strings(text: str) -> str:
	"""Blank out comments, string and char literals, preserving offsets and
	newlines so byte offsets still map to source line numbers."""
	out: list[str] = []
	i = 0
	n = len(text)
	state = "code"
	while i < n:
		c = text[i]
		nxt = text[i + 1] if i + 1 < n else ""
		if state == "code":
			if c == "/" and nxt == "/":
				out.extend((" ", " "))
				i += 2
				state = "line"
			elif c == "/" and nxt == "*":
				out.extend((" ", " "))
				i += 2
				state = "block"
			elif c == '"':
				out.append(" ")
				i += 1
				state = "string"
			elif c == "'":
				out.append(" ")
				i += 1
				state = "char"
			else:
				out.append(c)
				i += 1
		elif state == "line":
			if c == "\n":
				out.append(c)
				state = "code"
			else:
				out.append(" ")
			i += 1
		elif state == "block":
			if c == "*" and nxt == "/":
				out.extend((" ", " "))
				i += 2
				state = "code"
			else:
				out.append("\n" if c == "\n" else " ")
				i += 1
		elif state == "string":
			if c == "\\" and nxt:
				out.extend((" ", "\n" if nxt == "\n" else " "))
				i += 2
			elif c == '"':
				out.append(" ")
				i += 1
				state = "code"
			else:
				out.append("\n" if c == "\n" else " ")
				i += 1
		else:  # char
			if c == "\\" and nxt:
				out.extend((" ", "\n" if nxt == "\n" else " "))
				i += 2
			elif c == "'":
				out.append(" ")
				i += 1
				state = "code"
			else:
				out.append("\n" if c == "\n" else " ")
				i += 1
	return "".join(out)


def matching_brace(text: str, open_idx: int) -> int:
	"""Index of the '}' matching the '{' at open_idx. Caller must pass text with
	comments/strings already stripped so every brace is structural."""
	depth = 0
	for i in range(open_idx, len(text)):
		if text[i] == "{":
			depth += 1
		elif text[i] == "}":
			depth -= 1
			if depth == 0:
				return i
	return -1


def extract_adapters(stripped: str, path: Path) -> list[Adapter]:
	adapters: list[Adapter] = []
	for m in ADAPTER_SIG_RE.finditer(stripped):
		name = m.group(1)
		brace = m.end() - 1  # the '{'
		close = matching_brace(stripped, brace)
		if close < 0:
			continue
		body = stripped[brace + 1:close]
		start_line = stripped.count("\n", 0, brace) + 1
		adapters.append(Adapter(name, body, path, start_line))
	return adapters


def line_of(adapter: Adapter, offset_in_body: int) -> int:
	return adapter.start_line + adapter.body.count("\n", 0, offset_in_body)


def rule_r1(adapter: Adapter) -> list[Violation]:
	"""No integer literal >= 0x8000."""
	out: list[Violation] = []
	for m in INT_LITERAL_RE.finditer(adapter.body):
		lit = m.group(1)
		value = int(lit, 16) if lit.lower().startswith("0x") else int(lit, 10)
		if value >= ADDR_THRESHOLD:
			out.append(Violation(
				"R1", adapter.path, adapter.name,
				line_of(adapter, m.start()),
				f"integer literal {lit} (={value}) >= ${ADDR_THRESHOLD:04x} in "
				f"adapter body -- marshalling layers hardcode no Game Boy address",
			))
	return out


def routine_calls(adapter: Adapter) -> list[str]:
	"""Names of routine calls in the body, in order, excluding casts/keywords/
	marshalling helpers."""
	calls: list[str] = []
	for m in CALL_RE.finditer(adapter.body):
		name = m.group(1)
		if name in NON_CALLS:
			continue
		calls.append(name)
	return calls


def rule_r3(adapter: Adapter) -> list[Violation]:
	"""Exactly one routine call per adapter."""
	out: list[Violation]
	calls = routine_calls(adapter)
	if len(calls) == 1:
		return []
	if not calls:
		msg = "zero routine calls -- adapter reimplements the routine instead of marshalling it"
	else:
		msg = (f"{len(calls)} routine calls {calls} -- an adapter marshals "
		       f"exactly one call; extra calls re-derive an output the routine "
		       f"already produced")
	out = [Violation("R3", adapter.path, adapter.name, adapter.start_line, msg)]
	return out


RULES = {"R1": rule_r1, "R3": rule_r3}


def lint_path(path: Path, report: Report) -> None:
	stripped = strip_comments_and_strings(path.read_text())
	for adapter in extract_adapters(stripped, path):
		allowed = ALLOWLIST.get(adapter.name, {})
		for rule_id, fn in RULES.items():
			raw = fn(adapter)
			if rule_id in allowed:
				if not raw:
					# The allowance no longer applies: nothing to suppress, so the
					# entry is dead weight and must go.
					report.stale_allowlist.append(
						f"{path}:{adapter.name}: stale allowlist entry for "
						f"{rule_id} (rule no longer fires) -- remove it")
				continue
			report.violations.extend(raw)


def lint(targets: list[Path]) -> Report:
	report = Report()
	for target in sorted(targets):
		if target.is_dir():
			for path in sorted(target.glob("*.c")):
				lint_path(path, report)
		else:
			lint_path(target, report)
	return report


def emit(report: Report, stream) -> None:
	for v in report.violations:
		print(f"{v.path}:{v.line}: {v.rule} {v.adapter}: {v.message}", file=stream)
	for msg in report.stale_allowlist:
		print(f"{msg}", file=stream)


def main(argv: list[str] | None = None) -> int:
	ap = argparse.ArgumentParser(description=__doc__)
	ap.add_argument("paths", nargs="*", type=Path,
		help="files or dirs of probe adapters to lint (default: src/probe)")
	args = ap.parse_args(argv)

	targets = args.paths or [DEFAULT_PROBE_DIR]
	missing = [t for t in targets if not t.exists()]
	if missing:
		for t in missing:
			print(f"error: {t}: no such file or directory", file=sys.stderr)
		return 2

	report = lint(targets)
	emit(report, sys.stderr)
	if not report.ok:
		print("\nlint-adapters: FAILED", file=sys.stderr)
	return 0 if report.ok else 1


if __name__ == "__main__":
	raise SystemExit(main())
