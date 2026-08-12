#!/usr/bin/env python3
"""Build self-contained translation packets from the port frontier.

Consumes the same inventory/scope/registry model as tools/progress/report.py
(imported, not re-implemented), groups ready routines by pret source file,
splits oversized groups, and emits one JSON packet per group under
.factory/queue/.  A packet carries everything a stateless translator needs:
exact ASM slices, C prototypes of every ported callee, resolved constants,
and the append-mode context of the target files.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import (  # noqa: E402
    QUEUE, ROOT, block_routine, blocked_routines, write_json,
)

PRET = ROOT / "poketcg"
MAX_ROUTINES = 8
MAX_ASM_LINES = 300


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compute_functions() -> list[dict]:
    """Run report.py's compute() in-process; no files are written."""
    report = _load_module("factory_report", ROOT / "tools/progress/report.py")
    inventory = report.load_inventory()
    routines, _ = report.load_routines()
    gate = report.load_gate()
    return report.compute(inventory, routines, gate)["functions"], inventory


def _pret_number(text: str, default: int = 0) -> int:
    text = text.strip()
    try:
        if text.startswith("$"):
            return int(text[1:], 16)
        if text.startswith("%"):
            return int(text[1:], 2)
        return int(text, 0)
    except ValueError:
        return default


def load_constants() -> dict[str, str]:
    """NAME -> value text for every pret constant (EQU, DEF..EQU, const_def)."""
    table: dict[str, str] = {}
    equ = re.compile(r"^\s*(?:DEF\s+)?([A-Za-z_][A-Za-z0-9_]*)\s+EQU\s+(.+?)\s*$")
    const_def = re.compile(r"^\s*const_def(?:\s+(\S+))?(?:\s*,\s*(\S+))?")
    const_line = re.compile(r"^\s*const\s+([A-Za-z_][A-Za-z0-9_]*)")
    const_skip = re.compile(r"^\s*const_skip(?:\s+(\S+))?")
    for path in sorted((PRET / "src" / "constants").rglob("*.asm")):
        current, step = 0, 1
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.split(";", 1)[0]
            match = const_def.match(line)
            if match:
                current = _pret_number(match.group(1) or "0")
                step = _pret_number(match.group(2) or "1", 1)
                continue
            match = const_skip.match(line)
            if match:
                current += step * _pret_number(match.group(1) or "1", 1)
                continue
            match = const_line.match(line)
            if match:
                table.setdefault(match.group(1), f"${current:02X}")
                current += step
                continue
            match = equ.match(line)
            if match:
                table.setdefault(match.group(1), match.group(2))
    return table


def asm_lines(file: str) -> list[str]:
    return (PRET / file).read_text(errors="replace").splitlines()


def slice_asm(lines: list[str], start_line: int, sibling_lines: list[int]) -> str:
    """Exact source lines of one routine: [its label line, next label line)."""
    following = [n for n in sibling_lines if n > start_line]
    end = min(following) if following else len(lines) + 1
    return "\n".join(lines[start_line - 1:end - 1]).rstrip()


CONST_TOKEN = re.compile(r"\b([A-Z][A-Z0-9_]{2,})\b")


def constants_for(asm: str, table: dict[str, str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for token in CONST_TOKEN.findall(asm):
        if token in table:
            found[token] = table[token]
    return dict(sorted(found.items()))


SYMBOL_ADDR = re.compile(r"#define (\w+)_ADDR\s+(0x[0-9A-Fa-f]+)u")
SYMBOL_TOKEN = re.compile(r"\b([whs][A-Z][A-Za-z0-9_]*)\b")


def load_symbols() -> dict[str, str]:
    """pret RAM symbol -> numeric address, from the generated layout headers."""
    table: dict[str, str] = {}
    for name in ("wram.h", "hram.h", "sram.h"):
        path = ROOT / "include" / "generated" / name
        if path.exists():
            for symbol, addr in SYMBOL_ADDR.findall(path.read_text()):
                table.setdefault(symbol, addr)
    return table


def symbols_for(asm: str, table: dict[str, str]) -> dict[str, str]:
    found = {}
    for token in SYMBOL_TOKEN.findall(asm):
        if token in table:
            found[token] = table[token]
    return dict(sorted(found.items()))


def c_name(routine: str) -> str:
    return routine.replace(".", "_")


_PROTO_CACHE: dict[str, tuple[str, str] | None] = {}
_SCALARS = {"void", "uint8_t", "uint16_t", "uint32_t", "int8_t", "int16_t",
            "int32_t", "int", "unsigned", "size_t", "_Bool", "bool", "char"}


def _struct_typedef(text: str, type_name: str) -> str | None:
    match = re.search(
        rf"typedef\s+struct\s*\{{[^{{}}]*\}}\s*{re.escape(type_name)}\s*;",
        text, flags=re.DOTALL)
    return " ".join(match.group(0).split()) if match else None


def prototype_for(routine: str) -> tuple[str, str] | None:
    """(header basename, prototype + struct typedef) for a ported routine."""
    if routine in _PROTO_CACHE:
        return _PROTO_CACHE[routine]
    needle = re.compile(rf"\b{re.escape(c_name(routine))}\s*\(")
    result = None
    for header in sorted((ROOT / "src" / "home").glob("*.h")):
        text = header.read_text()
        match = needle.search(text)
        if not match:
            continue
        line_start = text.rfind("\n", 0, match.start()) + 1
        semi = text.find(";", match.start())
        if semi < 0:
            continue
        proto = " ".join(text[line_start:semi + 1].split())
        return_type = proto.split()[0]
        if return_type not in _SCALARS and not proto.startswith("static"):
            typedef = _struct_typedef(text, return_type)
            if typedef:
                proto = f"{typedef}  {proto}"
        result = (header.name, proto)
        break
    _PROTO_CACHE[routine] = result
    return result


def pick_example(asm: str) -> str:
    if "SetupText" in asm or "ProcessText" in asm:
        return "menus"
    if re.search(r"EnableSRAM|DisableSRAM|\bsGfx|\$[AB][0-9A-Fa-f]{3}\b", asm):
        return "card_collection"
    if re.search(r"\bv0|\bv1|BGMap|WriteDataBlocksToBGMap|Tiles0|VRAM", asm):
        return "tiles"
    return "card_data"


def existing_context(basename: str) -> dict | None:
    home = ROOT / "src" / "home" / f"{basename}.c"
    if not home.exists():
        return None
    header = ROOT / "src" / "home" / f"{basename}.h"
    cases = ROOT / "tests" / "cases" / f"{basename}.py"
    contract_keys: list[str] = []
    legacy_tail = True
    if cases.exists():
        module = _load_module(f"packet_cases_{basename}", cases)
        contract_keys = list(getattr(module, "CONTRACT", {}).keys())
        legacy_tail = "legacy_to_schema" in cases.read_text()
    text = home.read_text()
    includes = [l for l in text.splitlines() if l.startswith("#include")]
    return {
        "contract_keys": contract_keys,
        "includes": includes,
        "header": header.read_text() if header.exists() else "",
        "legacy_tail": legacy_tail,
    }


def blocker_graph(functions: list[dict]) -> tuple[dict[str, set[str]], dict[str, list[str]]]:
    graph = {f["name"]: set(f["blockers"]) for f in functions if f["status"] == "todo"}
    dependents: dict[str, list[str]] = {}
    for name, blockers in graph.items():
        for blocker in blockers:
            dependents.setdefault(blocker, []).append(name)
    return graph, dependents


def cascade(graph: dict[str, set[str]], dependents: dict[str, list[str]],
            seeds: set[str]) -> int:
    """Todo routines that become ready, transitively, once `seeds` land."""
    pending = {n: set(b) for n, b in graph.items() if n not in seeds}
    wave, gained = list(seeds), 0
    while wave:
        nxt = []
        for done in wave:
            for name in dependents.get(done, ()):
                blockers = pending.get(name)
                if blockers is None:
                    continue
                blockers.discard(done)
                if not blockers:
                    del pending[name]
                    nxt.append(name)
                    gained += 1
        wave = nxt
    return gained


def build_packets(dir_filter: str | None, max_routines: int, max_asm_lines: int,
                  limit: int | None) -> list[dict]:
    functions, _inventory = compute_functions()
    blocked = blocked_routines()
    by_name = {f["name"]: f for f in functions}
    graph, dependents = blocker_graph(functions)
    cascade_cache: dict[str, int] = {}
    def cascade_of(name: str) -> int:
        if name not in cascade_cache:
            cascade_cache[name] = cascade(graph, dependents, {name})
        return cascade_cache[name]

    ready = [f for f in functions
             if f["status"] == "todo" and f["ready"] and f["name"] not in blocked]
    if dir_filter:
        ready = [f for f in ready if (f["file"] or "").startswith(dir_filter)]

    groups: dict[str, list[dict]] = {}
    for f in sorted(ready, key=lambda f: f["line"]):
        groups.setdefault(f["file"], []).append(f)

    constants_table = load_constants()
    symbol_table = load_symbols()
    inventory_lines: dict[str, list[int]] = {}
    for f in functions:
        if f["file"]:
            inventory_lines.setdefault(f["file"], []).append(f["line"])

    packets: list[dict] = []
    id_counts: dict[str, int] = {}
    for file, members in groups.items():
        chunks: list[list[dict]] = [[]]
        line_budget = 0
        source = asm_lines(file)
        siblings = inventory_lines[file]
        enriched = []
        for f in members:
            asm = slice_asm(source, f["line"], siblings)
            enriched.append((f, asm, asm.count("\n") + 1))
        for f, asm, n_lines in enriched:
            if chunks[-1] and (len(chunks[-1]) >= max_routines
                               or line_budget + n_lines > max_asm_lines):
                chunks.append([])
                line_budget = 0
            chunks[-1].append((f, asm))
            line_budget += n_lines

        basename = Path(file).stem
        for chunk in chunks:
            routines = []
            packet_asm = []
            for f, asm in chunk:
                packet_asm.append(asm)
                routines.append({
                    "name": f["name"],
                    "size": f["size"],
                    "line": f["line"],
                    "refs": f["refs"],
                    "asm": asm,
                    "callees": [],
                    "cascade": cascade_of(f["name"]),
                })
            packet = {
                "id": (basename if id_counts.get(basename, 0) == 0
                       else f"{basename}-{id_counts[basename]}"),
                "basename": basename,
                "file": file,
                "mode": "append" if (ROOT / "src/home" / f"{basename}.c").exists() else "create",
                "state": "pending",
                "rounds": 0,
                "reason": None,
                "routines": routines,
                "constants": constants_for("\n".join(packet_asm), constants_table),
                "symbols": symbols_for("\n".join(packet_asm), symbol_table),
                "example": pick_example("\n".join(packet_asm)),
                "existing": existing_context(basename),
                "bytes": sum(r["size"] for r in routines),
                "cascade": cascade(graph, dependents, {r["name"] for r in routines}),
            }
            packets.append(packet)
            id_counts[basename] = id_counts.get(basename, 0) + 1

    packets.sort(key=lambda p: (-p["cascade"], p["bytes"]))
    if limit:
        packets = packets[:limit]
    return packets


def attach_dependencies(packets: list[dict]) -> list[dict]:
    """Fill callee prototypes; drop routines whose callees cannot link.

    A callee that is a real code label but has no C prototype is unavailable:
    either scope-excluded with no C equivalent (``JumpToFunctionInTable``) or
    simply unported. The frontier counts excluded callees as satisfied, so it
    offers such routines even though they cannot link. Block them here.
    """
    inventory = json.loads((ROOT / "site/data/inventory.json").read_text())
    functions = inventory["functions"]
    graph, dependents = blocker_graph(compute_functions()[0])
    kept: list[dict] = []
    for packet in packets:
        usable = []
        for routine in packet["routines"]:
            info = functions.get(routine["name"], {})
            deps = list(info.get("deps", []))
            fallthrough = info.get("fallthrough")
            routine["fallthrough"] = fallthrough
            if fallthrough and fallthrough not in deps:
                deps.append(fallthrough)
            callees, unavailable = [], []
            for dep in sorted(set(deps)):
                proto = prototype_for(dep)
                if proto is None and dep in functions:
                    unavailable.append(dep)
                callees.append({
                    "name": dep,
                    "header": proto[0] if proto else None,
                    "c": proto[1] if proto else None,
                })
            routine["callees"] = callees
            if unavailable:
                block_routine(routine["name"],
                              f"callee has no C symbol: {', '.join(unavailable)}",
                              "port or transform the named callee")
                continue
            usable.append(routine)
        if not usable:
            continue
        packet["routines"] = usable
        packet["bytes"] = sum(r["size"] for r in usable)
        packet["cascade"] = cascade(graph, dependents, {r["name"] for r in usable})
        kept.append(packet)
    return kept


def cmd_chokepoints(limit: int) -> int:
    functions, _inventory = compute_functions()
    graph, dependents = blocker_graph(functions)
    by_name = {f["name"]: f for f in functions}
    onehop: dict[str, int] = {}
    for name, blockers in graph.items():
        for blocker in blockers:
            onehop[blocker] = onehop.get(blocker, 0) + 1
    todo_names = list(graph)
    scored = sorted(
        ((cascade(graph, dependents, {n}), n) for n in todo_names),
        reverse=True)
    print(f"{'cascade':>7} {'1hop':>5} {'size':>6} {'ready':>6}  name  blockers")
    for score, name in scored[:limit]:
        f = by_name[name]
        print(f"{score:7} {onehop.get(name, 0):5} {f['size']:5}b {str(f['ready']):>6}  "
              f"{name}  {f['blockers'][:4]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="emit packets from the current frontier")
    build.add_argument("--dir", help="pret path prefix filter, e.g. src/audio")
    build.add_argument("--max-routines", type=int, default=MAX_ROUTINES)
    build.add_argument("--max-asm-lines", type=int, default=MAX_ASM_LINES)
    build.add_argument("--limit", type=int, help="emit at most N packets")
    build.add_argument("--force", action="store_true",
                       help="overwrite queue entries that already exist")
    build.add_argument("--json", action="store_true", help="print packet ids as JSON")
    chokepoints = sub.add_parser(
        "chokepoints", help="rank todo routines by transitive cascade")
    chokepoints.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if args.command == "chokepoints":
        return cmd_chokepoints(args.limit)

    packets = build_packets(args.dir, args.max_routines, args.max_asm_lines, args.limit)
    packets = attach_dependencies(packets)
    written = []
    for packet in packets:
        path = QUEUE / f"{packet['id']}.json"
        if path.exists() and not args.force:
            existing = json.loads(path.read_text())
            if existing.get("state") not in (None, "pending"):
                continue
        write_json(path, packet)
        written.append(packet["id"])
    if args.json:
        print(json.dumps(written))
    else:
        for packet in packets:
            if packet["id"] in written:
                print(f"{packet['id']:32} {packet['mode']:6} routines={len(packet['routines'])} "
                      f"bytes={packet['bytes']} cascade={packet['cascade']}")
        print(f"packets: {len(written)} written, {len(packets) - len(written)} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
