#!/usr/bin/env python3
"""Remove routines the Extended asm no longer has from an overlay basename.

Deletes each routine's factory block from the overlay C file and header, its
probe adapter (factory block or bare `adapt_<Name>` definition) and probe
table row, and its CONTRACT/CASES/MUTATIONS entries in the Extended case
module. With no routine names, prunes every routine the vanilla asm has and
the Extended asm lacks.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from profile_audit import routines_by_basename

from tools.profiles import get_profile


def factory_block(name: str) -> re.Pattern[str]:
    escaped = re.escape(name)
    return re.compile(
        rf"/\* >>> factory {escaped} \*/\n.*?/\* <<< factory {escaped} \*/\n\n?",
        re.DOTALL,
    )


def adapter_block(name: str) -> re.Pattern[str]:
    escaped = re.escape(name.replace(".", "_"))
    return re.compile(rf"static void adapt_{escaped}\(ProbeState \*s\)\n\{{\n.*?\n\}}\n\n?", re.DOTALL)


def table_row(name: str) -> re.Pattern[str]:
    return re.compile(rf'\t\{{ "{re.escape(name)}", adapt_{re.escape(name.replace(".", "_"))} \}},\n')


def strip_blocks(text: str, patterns: list[re.Pattern[str]]) -> tuple[str, int]:
    removed = 0
    for pattern in patterns:
        text, count = pattern.subn("", text)
        removed += count
    return text, removed


def case_entry(kind: str, name: str) -> re.Pattern[str]:
    escaped = re.escape(name)
    return re.compile(
        rf"^{kind}\[\"{escaped}\"\] = (?:[\{{\[][^\n]*[\}}\]]\n|[\{{\[]\n.*?^[\}}\]]\n)",
        re.DOTALL | re.MULTILINE,
    )


def literal_entry(name: str) -> re.Pattern[str]:
    escaped = re.escape(name)
    return re.compile(
        rf"^    '{escaped}': (?:[\{{\[][^\n]*[\}}\]],\n|[\{{\[]\n.*?^    [\}}\]],\n|\{{   [^\n]*\n.*?^        [^\n]*\}},\n)",
        re.DOTALL | re.MULTILINE,
    )


def prune_case_module(path: Path, names: list[str]) -> int:
    text = path.read_text()
    removed = 0
    for name in names:
        for kind in ("CONTRACT", "CASES", "MUTATIONS"):
            text, count = case_entry(kind, name).subn("", text)
            removed += count
        text, count = literal_entry(name).subn("", text)
        removed += count
        text, count = factory_markers(name).subn("", text)
        removed += count
    path.write_text(text)
    return removed


def factory_markers(name: str) -> re.Pattern[str]:
    escaped = re.escape(name)
    return re.compile(rf"^# >>> factory(?:-mutation)? {escaped}\n.*?^# <<< factory(?:-mutation)? {escaped}\n\n?", re.DOTALL | re.MULTILINE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("basename")
    parser.add_argument("routines", nargs="*")
    parser.add_argument("--profile", default="extended")
    args = parser.parse_args()
    profile = get_profile(args.profile, ROOT)
    overlay = profile.overlay_path(ROOT)
    if overlay is None:
        raise SystemExit(f"profile {profile.name} has no overlay root")
    names = args.routines
    if not names:
        vanilla = routines_by_basename(get_profile("vanilla", ROOT).source_path(ROOT) / "src")
        target = routines_by_basename(profile.source_path(ROOT) / "src")
        target_labels = {name for routines in target.values() for name in routines}
        names = sorted(name for name in vanilla.get(args.basename, {}) if name not in target_labels and name != "(header)")
    if not names:
        print("nothing to prune")
        return 0
    home = overlay / "home" / f"{args.basename}.c"
    header = overlay / "home" / f"{args.basename}.h"
    probe = overlay / "probe" / f"{args.basename}.c"
    cases = profile.case_path(ROOT) / f"{args.basename}.py"
    for path, patterns in (
        (home, [factory_block(name) for name in names]),
        (header, [factory_block(name) for name in names]),
        (probe, [factory_block(name) for name in names] + [adapter_block(name) for name in names]
         + [table_row(name) for name in names]),
    ):
        if not path.is_file():
            continue
        text, removed = strip_blocks(path.read_text(), patterns)
        path.write_text(text)
        print(f"{path.relative_to(ROOT)}: removed {removed} block(s)")
    if cases.is_file():
        print(f"{cases.relative_to(ROOT)}: removed {prune_case_module(cases, names)} entr(ies)")
    for name in names:
        print(f"pruned {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
