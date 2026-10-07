#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

from profiles import ProfileError, get_profile

ROOT = Path(__file__).resolve().parent.parent
SYM_RE = re.compile(r"^([0-9A-Fa-f]{2}):([0-9A-Fa-f]{4})\s+(\S+)\s*$")
ROM_LITERAL_RE = re.compile(r"\b0[xX]([4-7][0-9A-Fa-f]{3})[uU]?\b")
COMMENT_RE = re.compile(r"/\*.*?\*/|//[^\n]*", re.DOTALL)
STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
BANK_WINDOW_RE = re.compile(
    r"0x3FFF|~0x8000|<<\s*14|mbc5_write|rRTC|0x4000u\s*\)\s*;|0x7F00|[<>]=?\s*0x4000u|0x4000u\s*\|"
)


def masked_source(text: str) -> str:
    def blank(match: re.Match[str]) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    return STRING_RE.sub(blank, COMMENT_RE.sub(blank, text))


LABEL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)::?")


def asm_lines(path: Path) -> list[str]:
    lines = []
    for raw in path.read_text(errors="replace").splitlines():
        line = raw.split(";", 1)[0]
        line = re.sub(r"\s+", " ", line.strip()).upper()
        if line:
            lines.append(line)
    return lines


def asm_body(path: Path) -> str:
    return "\n".join(asm_lines(path))


def asm_routines(path: Path) -> dict[str, str]:
    routines: dict[str, list[str]] = {}
    current = "(header)"
    for raw in path.read_text(errors="replace").splitlines():
        code = raw.split(";", 1)[0]
        match = LABEL_RE.match(code)
        if match:
            current = match.group(1)
            routines.setdefault(current, [])
            continue
        line = re.sub(r"\s+", " ", code.strip()).upper()
        if line:
            routines.setdefault(current, []).append(line)
    return {name: "\n".join(body) for name, body in routines.items()}


def asm_by_basename(root: Path) -> dict[str, list[tuple[str, str]]]:
    result: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for path in sorted(root.rglob("*.asm")):
        result[path.stem].append((path.relative_to(root).as_posix(), asm_body(path)))
    return result


def routines_by_basename(root: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = defaultdict(dict)
    for path in sorted(root.rglob("*.asm")):
        result[path.stem].update(asm_routines(path))
    return result


def routine_report(vanilla: Path, extended: Path, basenames: list[str]) -> int:
    vanilla_routines = routines_by_basename(vanilla / "src")
    extended_routines = routines_by_basename(extended / "src")
    selected = basenames or sorted(set(vanilla_routines) & set(extended_routines))
    totals = {"same": 0, "changed": 0, "vanilla-only": 0, "extended-only": 0}
    for basename in selected:
        before = vanilla_routines.get(basename, {})
        after = extended_routines.get(basename, {})
        rows = []
        for name in sorted(set(before) | set(after)):
            if name == "(header)":
                continue
            if name not in after:
                status = "vanilla-only"
            elif name not in before:
                status = "extended-only"
            elif before[name] != after[name]:
                status = "changed"
            else:
                status = "same"
            totals[status] += 1
            if status != "same":
                rows.append(f"  {status:13s} {name}")
        if rows:
            print(f"{basename}:")
            print("\n".join(rows))
    print(" ".join(f"{key}={value}" for key, value in totals.items()))
    return 0


def symbols(path: Path) -> dict[str, tuple[int, int]]:
    result: dict[str, tuple[int, int]] = {}
    for line in path.read_text(errors="replace").splitlines():
        match = SYM_RE.match(line.strip())
        if match and "." not in match.group(3):
            result.setdefault(match.group(3), (int(match.group(1), 16), int(match.group(2), 16)))
    return result


def c_paths(root: Path) -> list[Path]:
    return sorted(root.glob("*.c")) + sorted(root.glob("*.h"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default="extended")
    parser.add_argument("--vanilla", type=Path)
    parser.add_argument("--extended", type=Path)
    parser.add_argument("--routines", nargs="*", metavar="BASENAME",
                        help="report per-routine asm differences instead of auditing")
    args = parser.parse_args()
    try:
        vanilla = get_profile("vanilla", ROOT).source_path(ROOT)
        extended = get_profile(args.profile, ROOT).source_path(ROOT)
    except ProfileError as error:
        raise SystemExit(str(error)) from error
    vanilla = (args.vanilla or vanilla).resolve()
    extended = (args.extended or extended).resolve()
    if args.routines is not None:
        return routine_report(vanilla, extended, args.routines)
    shared_home = ROOT / "src" / "home"
    overlay_home = ROOT / "src" / "profiles" / args.profile / "home"
    failures: list[str] = []
    vanilla_profile = get_profile("vanilla", ROOT)
    extended_profile = get_profile(args.profile, ROOT)
    vanilla_asm = asm_by_basename(vanilla / "src")
    extended_asm = asm_by_basename(extended / "src")
    for basename in sorted(set(vanilla_asm) & set(extended_asm)):
        if {body for _, body in vanilla_asm[basename]} == {body for _, body in extended_asm[basename]}:
            continue
        if basename in extended_profile.removed_basenames:
            continue
        if (shared_home / f"{basename}.c").is_file() and not (overlay_home / f"{basename}.c").is_file():
            failures.append(f"asm differs without Extended overlay: {basename}")
    vanilla_symbols = symbols(vanilla / vanilla_profile.sym_name)
    extended_symbols = symbols(extended / extended_profile.sym_name)
    changed_addresses = {
        vanilla_address[1]
        for name, vanilla_address in vanilla_symbols.items()
        if name in extended_symbols
        and vanilla_address != extended_symbols[name]
        and 0x4000 <= vanilla_address[1] < 0x8000
    }
    for path in c_paths(shared_home):
        if (overlay_home / f"{path.stem}.c").is_file() or path.stem in extended_profile.removed_basenames:
            continue
        source = masked_source(path.read_text(errors="replace"))
        for line in source.splitlines():
            if BANK_WINDOW_RE.search(line):
                continue
            for match in ROM_LITERAL_RE.finditer(line):
                address = int(match.group(1), 16)
                if address in changed_addresses:
                    failures.append(f"profile-specific ROM literal: {path.relative_to(ROOT)}:0x{address:04X}")
    if failures:
        print("profile-audit: FAIL")
        for failure in failures:
            print(failure)
        return 1
    print(f"profile-audit: PASS profile={args.profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
