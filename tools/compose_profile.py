#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from tools.factory_blocks import Block, BlockError, Directive, parse  # noqa: E402
from tools.profiles import Profile, get_profile  # noqa: E402

KINDS = (("home", ".c"), ("home", ".h"), ("probe", ".c"))
ADAPTER_RE = re.compile(r"^\s*static\s+void\s+(adapt_\w+)\s*\(", re.MULTILINE)
ROW_RE = re.compile(r"\{\s*\"[^\"]*\"\s*,\s*(adapt_\w+)\s*\}")
ROW_FULL_RE = re.compile(r"\{\s*\"([^\"]*)\"\s*,\s*(adapt_\w+)\s*\}")
TABLE_RE = re.compile(r"^probe_entries_\w+$")


@dataclass(frozen=True)
class Unit:
    basename: str
    tree: str
    suffix: str
    shared: Path | None
    override: Path | None

    @property
    def relative(self) -> str:
        return f"{self.tree}/{self.basename}{self.suffix}"

    @property
    def composed(self) -> bool:
        return self.shared is not None and self.override is not None

    @property
    def source(self) -> Path:
        return self.override if self.override is not None else self.shared

    def text(self, line_marks: bool = False) -> str:
        if not self.composed:
            return self.source.read_text()
        return compose(self.shared.read_text(), self.override.read_text(),
                       probe=self.tree == "probe",
                       origins=(self.shared, self.override) if line_marks else None)

    def owner(self, name: str) -> Path:
        if self.override is not None:
            parsed = parse(self.override.read_text(), self.override)
            if parsed.block(name) is not None or self.shared is None:
                return self.override
        return self.shared


def units(profile: Profile, root: Path = ROOT) -> list[Unit]:
    overlay = profile.overlay_path(root)
    result: list[Unit] = []
    for tree, suffix in KINDS:
        shared_dir = root / "src" / tree
        override_dir = overlay / tree if overlay is not None else None
        stems = {path.stem for path in shared_dir.glob(f"*{suffix}")} - set(profile.removed_basenames)
        overrides = {path.stem for path in override_dir.glob(f"*{suffix}")} if override_dir and override_dir.is_dir() else set()
        for stem in sorted(stems | overrides):
            shared = shared_dir / f"{stem}{suffix}"
            override = override_dir / f"{stem}{suffix}" if stem in overrides else None
            result.append(Unit(stem, tree, suffix, shared if shared.is_file() and stem in stems else None, override))
    return result


def block_lines(block: Block) -> list[str]:
    return [f"/* >>> {block.kind} {block.name} */", *block.body, f"/* <<< {block.kind} {block.name} */"]


def line_mark(path: Path, line: int) -> str:
    return f'#line {line} "{path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path}"'


def compose(shared: str, override: str, *, probe: bool = False, origins: tuple[Path, Path] | None = None) -> str:
    base = parse(shared, origins[0] if origins else Path("<shared>"))
    patch = parse(override, origins[1] if origins else Path("<override>"))
    errors = base.errors + patch.errors
    names = {block.name for block in base.blocks}
    removed = {directive.name for directive in patch.directives if directive.op == "---"}
    moved = {block.name for block in patch.blocks if block.name in removed}
    replaced = {block.name: block for block in patch.blocks if block.name in names and block.name not in moved}
    merge_rows = None
    if probe:
        table = next((name for name in replaced if TABLE_RE.match(name)), None)
        if table is not None:
            merge_rows = table_rows(replaced.pop(table).body)
    entries: list[Block | Directive] = sorted(
        [*patch.blocks, *patch.directives],
        key=lambda entry: entry.open_line if isinstance(entry, Block) else entry.line)
    for entry in entries:
        if isinstance(entry, Directive) and entry.op == "---" and entry.name not in names:
            errors.append(f"{entry.op} {entry.kind} {entry.name} names no shared block")
        if isinstance(entry, Directive) and entry.op == "===" and entry.name in replaced:
            errors.append(f"{entry.op} {entry.kind} {entry.name} also has an override block")
    if errors:
        raise BlockError("; ".join(errors))
    following: dict[str | None, list[Block]] = {}
    anchor: str | None = None
    for entry in entries:
        if entry.name in names and entry.name not in moved:
            anchor = entry.name
        elif isinstance(entry, Block):
            following.setdefault(anchor, []).append(entry)
    starts = {block.open_line: block for block in base.blocks}

    def emit(block: Block, source_index: int) -> list[str]:
        lines = block_lines(block)
        if origins is None:
            return lines
        return [line_mark(origins[source_index], block.open_line + 1), *lines]

    out: list[str] = []
    resync = False
    head_done = False
    index = 0
    while index < len(base.lines):
        block = starts.get(index)
        if block is None:
            if resync and origins is not None:
                out.append(line_mark(origins[0], index + 1))
                resync = False
            out.append(base.lines[index])
            index += 1
            continue
        if not head_done:
            for extra in following.get(None, ()):
                out += emit(extra, 1)
                resync = True
            head_done = True
        if block.name in replaced:
            out += emit(replaced[block.name], 1)
            resync = True
        elif block.name not in removed:
            if resync and origins is not None:
                out.append(line_mark(origins[0], index + 1))
                resync = False
            out += base.lines[block.open_line:block.close_line + 1]
        for extra in following.get(block.name, ()):
            out += emit(extra, 1)
            resync = True
        index = block.close_line + 1
    if not head_done:
        for extra in following.get(None, ()):
            out += emit(extra, 1)
    text = "\n".join(out)
    return filter_table(text, merge_rows) if probe else text


def table_rows(lines: list[str]) -> list[tuple[str, str]]:
    return [(name, adapter) for line in lines for name, adapter in ROW_FULL_RE.findall(line)]


def filter_table(text: str, extra: list[tuple[str, str]] | None = None) -> str:
    defined = set(ADAPTER_RE.findall(text))
    parsed = parse(text)
    table = next((block for block in parsed.blocks if TABLE_RE.match(block.name)), None)
    if table is None:
        return text
    lines = parsed.lines
    if extra is None:
        kept = [line for line in table.body
                if not (ROW_RE.search(line) and ROW_RE.search(line).group(1) not in defined)]
        return "\n".join(lines[:table.open_line + 1] + kept + lines[table.close_line:])
    rows = dict(table_rows(table.body))
    order = list(rows)
    for name, adapter in extra:
        if name not in rows:
            order.append(name)
        rows[name] = adapter
    header = next(line for line in table.body if table.name in line)
    body = [header, *(f'\t{{ "{name}", {rows[name]} }},' for name in order if rows[name] in defined),
            "\t{ NULL, NULL },", "};"]
    return "\n".join(lines[:table.open_line + 1] + body + lines[table.close_line:])


def rendered(unit: Unit, line_marks: bool) -> str:
    if unit.composed:
        return unit.text(line_marks=line_marks)
    text = unit.override.read_text()
    return f"{line_mark(unit.override, 1)}\n{text}" if line_marks else text


def write(profile: Profile, out: Path, line_marks: bool) -> list[Path]:
    written = []
    for unit in units(profile):
        if unit.override is None:
            continue
        target = out / unit.relative
        text = rendered(unit, line_marks)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.is_file() or target.read_text() != text:
            target.write_text(text)
        written.append(target)
    return written


def materialize(profile: Profile, root: Path = ROOT) -> Path | None:
    if profile.overlay_path(root) is None:
        return None
    out = profile.build_path(root) / "compose"
    write(profile, out, line_marks=False)
    return out


def merged_paths(profile: Profile, tree: str, suffix: str, root: Path = ROOT) -> list[Path]:
    out = materialize(profile, root)
    return [out / unit.relative if unit.override is not None else unit.shared
            for unit in units(profile, root) if unit.tree == tree and unit.suffix == suffix]


def owner(profile: Profile, tree: str, suffix: str, basename: str, name: str, root: Path = ROOT) -> Path | None:
    for unit in units(profile, root):
        if (unit.tree, unit.suffix, unit.basename) == (tree, suffix, basename):
            return unit.owner(name)
    return None


def mutation_source(profile: Profile, basename: str, symbol: str, before: str, root: Path = ROOT) -> Path:
    shared = root / "src" / "home" / f"{basename}.c"
    overlay = profile.overlay_path(root)
    fragment = overlay / "home" / f"{basename}.c" if overlay is not None else None
    if fragment is None or not fragment.is_file():
        return shared
    if not shared.is_file():
        return fragment
    patch = parse(fragment.read_text(), fragment)
    if any(patch.block(name) is not None for name in (symbol, symbol.replace(".", "_"))):
        return fragment
    base = parse(shared.read_text(), shared)
    removed = {directive.name for directive in patch.directives if directive.op == "---"}
    if any(base.block(name) is not None and name not in removed for name in (symbol, symbol.replace(".", "_"))):
        return shared
    if any(before in "\n".join(block.body) for block in patch.blocks):
        return fragment
    if any(block.name in removed and before in "\n".join(block.body) for block in base.blocks):
        return fragment
    return shared


def identical_overrides(unit: Unit) -> list[str]:
    if not unit.composed:
        return []
    shared = {block.name: block for block in parse(unit.shared.read_text(), unit.shared).blocks}
    patch = parse(unit.override.read_text(), unit.override)
    moved = {directive.name for directive in patch.directives if directive.op == "---"}
    return [block.name for block in patch.blocks
            if block.name in shared and block.name not in moved and shared[block.name].body == block.body]


def deduplicate(profile: Profile, root: Path = ROOT) -> int:
    removed = 0
    for unit in units(profile, root):
        names = set(identical_overrides(unit))
        if not names:
            continue
        patch = parse(unit.override.read_text(), unit.override)
        if patch.errors:
            raise BlockError("\n".join(patch.errors))
        lines = patch.lines
        keep_anchors = (
            (unit.tree == "home" and unit.suffix == ".c")
            or any(block.name not in names for block in patch.blocks)
        )
        for block in reversed(patch.blocks):
            if block.name not in names:
                continue
            declaration = (
                [f"/* === {block.kind} {block.name} */"]
                if keep_anchors else []
            )
            lines[block.open_line:block.close_line + 1] = declaration
            removed += 1
        text = "\n".join(lines)
        if text.strip():
            unit.override.write_text(text)
        else:
            unit.override.unlink()
        print(f"shared {unit.relative}: {', '.join(sorted(names))}")
    print(f"deduplicate: profile={profile.name} blocks={removed}")
    return 0


def seed(profile: Profile, basename: str, names: list[str], root: Path = ROOT) -> int:
    overlay = profile.overlay_path(root)
    if overlay is None:
        raise SystemExit(f"profile {profile.name} has no overlay_root")
    copied = 0
    for tree, suffix in KINDS:
        shared = root / "src" / tree / f"{basename}{suffix}"
        if not shared.is_file():
            continue
        blocks = {block.name: block for block in parse(shared.read_text(), shared).blocks}
        fragment = overlay / tree / f"{basename}{suffix}"
        existing = parse(fragment.read_text(), fragment) if fragment.is_file() else None
        additions = []
        for name in names:
            if name in blocks and (existing is None or existing.block(name) is None):
                additions += block_lines(blocks[name])
        if not additions:
            continue
        body = fragment.read_text().rstrip("\n") if fragment.is_file() else ""
        fragment.parent.mkdir(parents=True, exist_ok=True)
        fragment.write_text((body + "\n" if body else "") + "\n".join(additions) + "\n")
        copied += 1
        print(f"seeded {fragment.relative_to(root)}")
    if not copied:
        raise SystemExit(f"no shared block named {', '.join(names)} in {basename}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose a profile's translation units from shared blocks and its override blocks.")
    sub = parser.add_subparsers(dest="command", required=True)
    write_parser = sub.add_parser("write", help="write every unit with an override under OUT/{home,probe}")
    write_parser.add_argument("--profile", required=True)
    write_parser.add_argument("--out", type=Path, required=True)
    write_parser.add_argument("--line-marks", action="store_true")
    sources_parser = sub.add_parser("sources", help="print the profile's build inputs and outputs for CMake")
    sources_parser.add_argument("--profile", required=True)
    sources_parser.add_argument("--out", type=Path, required=True)
    unit_parser = sub.add_parser("unit", help="compose one unit")
    unit_parser.add_argument("--shared", type=Path)
    unit_parser.add_argument("--override", type=Path, required=True)
    unit_parser.add_argument("--out", type=Path, required=True)
    unit_parser.add_argument("--probe", action="store_true")
    unit_parser.add_argument("--line-marks", action="store_true")
    seed_parser = sub.add_parser("seed", help="copy shared blocks into the profile's fragments as override starting points")
    seed_parser.add_argument("--profile", required=True)
    seed_parser.add_argument("basename")
    seed_parser.add_argument("names", nargs="+")
    check_parser = sub.add_parser("check", help="compose every unit and report errors")
    check_parser.add_argument("--profile", required=True)
    deduplicate_parser = sub.add_parser("deduplicate", help="replace identical overrides with shared declarations")
    deduplicate_parser.add_argument("--profile", required=True)
    args = parser.parse_args()
    if args.command == "unit":
        shared = args.shared.resolve() if args.shared else None
        override = args.override.resolve()
        unit = Unit(override.stem, "probe" if args.probe else "home", override.suffix, shared, override)
        text = rendered(unit, args.line_marks)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        if not args.out.is_file() or args.out.read_text() != text:
            args.out.write_text(text)
        return 0
    profile = get_profile(args.profile, ROOT)
    if args.command == "seed":
        return seed(profile, args.basename, args.names)
    if args.command == "deduplicate":
        return deduplicate(profile)
    if args.command == "sources":
        category = {("home", ".c"): "home", ("home", ".h"): "header", ("probe", ".c"): "probe"}
        for unit in units(profile):
            if unit.override is None:
                print(f"{category[(unit.tree, unit.suffix)]}={unit.shared}")
                continue
            target = args.out / unit.relative
            print(f"{category[(unit.tree, unit.suffix)]}={target}")
            print(f"unit={target}|{unit.shared or '-'}|{unit.override}|{int(unit.tree == 'probe')}")
        return 0
    if args.command == "check":
        failures = 0
        for unit in units(profile):
            try:
                unit.text()
            except BlockError as error:
                print(f"{unit.override}: {error}")
                failures += 1
                continue
            for name in identical_overrides(unit):
                print(f"{unit.override}: override {name} is identical to the shared block")
                failures += 1
        print(f"compose-check: profile={profile.name} units={sum(1 for unit in units(profile) if unit.composed)} failures={failures}")
        return 1 if failures else 0
    written = write(profile, args.out, args.line_marks)
    print(f"compose: profile={profile.name} units={len(written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
