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
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common  # noqa: E402
from common import (  # noqa: E402
    BUNDLES, FACTORY, QUEUE, ROOT, block_routine, blocked_routines,
    issue_records, read_json, write_json,
)

PRET = ROOT / "poketcg"
MAX_ROUTINES = 8
MAX_ASM_LINES = 300
BACKUPS = FACTORY / "backups"
ACTIVE_CLAIM_STATES = {"pending", "translating", "translated", "verifying", "repair", "green"}


def _positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def select_pending_packets(limit: int | None) -> list[dict]:
    packets = sorted(
        common.list_packets(("pending",)),
        key=lambda packet: (
            packet.get("updated_at") if isinstance(packet.get("updated_at"), int) else 0,
            packet["id"],
        ),
    )
    return packets if limit is None else packets[:limit]


def plan_work_id_migration(
    packets: list[dict],
    managed_issues: dict[str, dict],
) -> tuple[list[dict], dict[str, int]]:
    """Validate and backfill queue identity without mutating the inputs."""
    migrated = []
    changed_packets = 0
    changed_routines = 0
    for packet in packets:
        packet_id = packet.get("id")
        if not isinstance(packet_id, str) or not packet_id:
            raise ValueError("queue packet has no non-empty id")
        source = packet.get("file")
        if not isinstance(source, str) or not source:
            raise ValueError(f"packet {packet_id} has no non-empty file")
        routines = packet.get("routines")
        if not isinstance(routines, list):
            raise ValueError(f"packet {packet_id} has no routine list")
        updated = copy.deepcopy(packet)
        packet_changed = False
        for index, routine in enumerate(updated["routines"]):
            name = routine.get("name")
            if not isinstance(name, str) or not name:
                raise ValueError(
                    f"packet {packet_id} routine {index} has no non-empty name"
                )
            work_id = f"port:v1:{source}:{name}"
            issue = managed_issues.get(work_id)
            if issue is None:
                raise ValueError(
                    f"packet {packet_id} routine {name} has unresolved work ID "
                    f"{work_id}"
                )
            if "issue_number" not in issue:
                raise ValueError(f"issue record {work_id} has no issue number")
            routine_changed = False
            for field, expected in (
                ("work_id", work_id),
                ("issue_number", issue["issue_number"]),
            ):
                if field in routine:
                    if routine[field] != expected:
                        raise ValueError(
                            f"packet {packet_id} routine {name} has mismatched "
                            f"{field}: {routine[field]!r} != {expected!r}"
                        )
                else:
                    routine[field] = expected
                    routine_changed = True
            if routine_changed:
                packet_changed = True
                changed_routines += 1
        if packet_changed:
            changed_packets += 1
        migrated.append(updated)

    active_claims: dict[str, str] = {}
    for packet in migrated:
        if packet.get("state") not in ACTIVE_CLAIM_STATES:
            continue
        for routine in packet["routines"]:
            work_id = routine["work_id"]
            owner = active_claims.get(work_id)
            if owner is not None and owner != packet["id"]:
                raise ValueError(
                    f"work ID {work_id} claimed by active packets {owner} and "
                    f"{packet['id']}"
                )
            active_claims[work_id] = packet["id"]
    return migrated, {
        "packets": len(migrated),
        "routines": sum(len(packet["routines"]) for packet in migrated),
        "changed_packets": changed_packets,
        "changed_routines": changed_routines,
    }


def _plan_bundle_metadata(packets: list[dict]) -> dict:
    by_id = {packet["id"]: packet for packet in packets}
    entries = []
    missing = []
    existing = []
    if not BUNDLES.is_dir():
        return {
            "bundles": 0,
            "changed_bundle_metadata": 0,
            "entries": entries,
            "missing": missing,
            "existing": existing,
        }
    for bundle in sorted(path for path in BUNDLES.iterdir() if path.is_dir()):
        packet = by_id.get(bundle.name)
        if packet is None:
            raise ValueError(f"orphan bundle directory: {bundle}")
        expected = common.packet_identity(packet)
        metadata = bundle / "packet.json"
        if metadata.exists():
            raw = metadata.read_bytes()
            existing_identity = json.loads(raw)
            if existing_identity != expected:
                raise ValueError(f"bundle identity mismatch: {metadata}")
            existing.append((metadata, raw))
        else:
            missing.append((metadata, expected))
        entries.append((metadata, expected))
    return {
        "bundles": len(entries),
        "changed_bundle_metadata": len(missing),
        "entries": entries,
        "missing": missing,
        "existing": existing,
    }


def _migration_preflight() -> dict:
    packets = []
    queue_entries = []
    if QUEUE.is_dir():
        for path in sorted(QUEUE.glob("*.json")):
            raw = path.read_bytes()
            packet = json.loads(raw)
            if path.stem != packet.get("id"):
                raise ValueError(f"queue filename does not match packet id: {path}")
            queue_entries.append((path, raw, packet))
    managed_issues = issue_records(required=True)
    packets = [packet for _path, _raw, packet in queue_entries]
    migrated, counts = plan_work_id_migration(packets, managed_issues)
    planned_queue = []
    for (path, raw, original), updated in zip(queue_entries, migrated):
        planned_queue.append((path, raw, original, updated))
    bundle_plan = _plan_bundle_metadata(migrated)
    counts.update({
        "bundles": bundle_plan["bundles"],
        "changed_bundle_metadata": bundle_plan["changed_bundle_metadata"],
    })
    return {
        "counts": counts,
        "queue": planned_queue,
        "bundles": bundle_plan,
    }


def _restore_bytes(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=f".{path.stem}.", suffix=".restore",
                                dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def _create_migration_backup(preflight: dict) -> Path:
    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
    backup = BACKUPS / f"work-id-migration-{stamp}-{time.time_ns() % 1000000:06d}"
    backup.mkdir()
    queue_files = []
    for path, _raw, original, updated in preflight["queue"]:
        if original == updated:
            continue
        destination = backup / "queue" / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        queue_files.append(str(destination.relative_to(backup)))
    bundle_files = []
    for path, raw in preflight["bundles"]["existing"]:
        destination = backup / "bundles" / path.parent.name / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        bundle_files.append(str(destination.relative_to(backup)))
    absent = [
        str(path.relative_to(BUNDLES))
        for path, _expected in preflight["bundles"]["missing"]
    ]
    write_json(backup / "manifest.json", {
        "queue": queue_files,
        "bundle_metadata": bundle_files,
        "absent_bundle_metadata": absent,
    })
    return backup


def _restore_migration(preflight: dict) -> None:
    for path, raw, original, updated in preflight["queue"]:
        if original != updated:
            _restore_bytes(path, raw)
    for path, raw in preflight["bundles"]["existing"]:
        _restore_bytes(path, raw)
    for path, _expected in preflight["bundles"]["missing"]:
        if path.exists():
            path.unlink()


def apply_work_id_migration(preflight: dict) -> dict:
    """Apply a completed preflight with a backup and atomic rollback."""
    counts = dict(preflight["counts"])
    if not counts["changed_packets"] and not counts["changed_bundle_metadata"]:
        counts["backup"] = None
        return counts
    backup = _create_migration_backup(preflight)
    try:
        for path, _raw, original, updated in preflight["queue"]:
            if original != updated:
                write_json(path, updated)
        for path, expected in preflight["bundles"]["missing"]:
            write_json(path, expected)
        for path, _raw, original, updated in preflight["queue"]:
            if original != updated and read_json(path) != updated:
                raise RuntimeError(f"queue readback mismatch: {path}")
        for path, expected in preflight["bundles"]["missing"]:
            if read_json(path) != expected:
                raise RuntimeError(f"bundle metadata readback mismatch: {path}")
    except Exception as exc:
        try:
            _restore_migration(preflight)
        except Exception as restore_exc:
            raise RuntimeError(
                f"migration failed; backup at {backup}; rollback failed: "
                f"{restore_exc}"
            ) from exc
        raise RuntimeError(
            f"migration failed and was restored; backup at {backup}: {exc}"
        ) from exc
    counts["backup"] = str(backup)
    return counts


def run_work_id_migration(*, apply: bool = False) -> dict:
    preflight = _migration_preflight()
    if apply:
        return apply_work_id_migration(preflight)
    return dict(preflight["counts"], backup=None)



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
    computed = report.compute(inventory, routines, gate)
    by_name = {record["name"]: record for record in computed["work_records"]}
    functions = []
    for function in computed["functions"]:
        enriched = dict(function)
        work = by_name.get(function["name"])
        if work:
            enriched["work_id"] = work["work_id"]
            enriched["tier"] = work["tier"]
        functions.append(enriched)
    return functions, inventory


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


_NUMERIC_EXPR = re.compile(r"^[0-9A-Fa-fxX+\-*/()\s]+$")


def _eval_const(text: str, numeric: dict[str, int]) -> int | None:
    """Best-effort numeric value of a pret constant expression.

    Handles ``$1f`` / ``0x1f`` / decimal literals and arithmetic over
    already-known constant names (``TYPE_PKMN_UNUSED + 1 - TYPE_PKMN_FIRE``).
    Returns None when a name is still unknown or the text is not arithmetic —
    callers fall back to storing the raw text.
    """
    expr = text.strip()
    if not expr:
        return None
    expr = re.sub(r"\$([0-9A-Fa-f]+)", r"0x\1", expr)
    expr = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*)\b",
                  lambda m: str(numeric[m.group(1)]) if m.group(1) in numeric else m.group(0),
                  expr)
    if not _NUMERIC_EXPR.match(expr):
        return None
    try:
        return int(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307 - arithmetic only
    except Exception:
        return None


def load_constants() -> dict[str, str]:
    """NAME -> value text for every pret constant (EQU, EQUS, const_def).

    Two classes were silently missing before, and both produced invented
    constants downstream:
    - ``DEF X EQUS "LOW(wSym)"`` (every ``DUELVARS_*``) — resolved here against
      the generated RAM symbol table.
    - ``const_def <expression>`` — an unparsed expression left the whole
      following ``const`` block offset (``TYPE_TRAINER`` resolved to $08
      instead of $10).
    """
    table: dict[str, str] = {}
    numeric: dict[str, int] = {}
    symbols = {name: int(addr, 16) for name, addr in load_symbols().items()}
    equ = re.compile(r"^\s*(?:DEF\s+)?([A-Za-z_][A-Za-z0-9_]*)\s+EQU\s+(.+?)\s*$")
    equs_byte = re.compile(
        r"^\s*(?:DEF\s+)?([A-Za-z_][A-Za-z0-9_]*)\s+EQUS\s+\"(LOW|HIGH)\(([A-Za-z_][A-Za-z0-9_]*)\)\"")
    const_def = re.compile(r"^\s*const_def(?:\s+([^,]+?))?(?:\s*,\s*(\S+))?\s*$")
    const_line = re.compile(r"^\s*const\s+([A-Za-z_][A-Za-z0-9_]*)")
    const_skip = re.compile(r"^\s*const_skip(?:\s+(\S+))?")

    def record(name: str, value: int | None, text: str) -> None:
        if name in table:
            return
        table[name] = f"${value:02x}" if value is not None else text
        if value is not None:
            numeric[name] = value

    for path in sorted((PRET / "src" / "constants").rglob("*.asm")):
        current, step = 0, 1
        for raw in path.read_text(errors="replace").splitlines():
            line = raw.split(";", 1)[0]
            numeric["const_value"] = current  # rgbasm's running const counter
            match = const_def.match(line)
            if match:
                start = _eval_const(match.group(1) or "0", numeric)
                current = start if start is not None else 0
                step = _eval_const(match.group(2) or "1", numeric) or 1
                continue
            match = const_skip.match(line)
            if match:
                current += step * (_eval_const(match.group(1) or "1", numeric) or 1)
                continue
            match = const_line.match(line)
            if match:
                record(match.group(1), current, f"${current:02x}")
                current += step
                continue
            match = equs_byte.match(line)
            if match:
                name, half, symbol = match.groups()
                addr = symbols.get(symbol)
                if addr is not None:
                    record(name, addr & 0xFF if half == "LOW" else (addr >> 8) & 0xFF, "")
                continue
            match = equ.match(line)
            if match:
                record(match.group(1), _eval_const(match.group(2), numeric), match.group(2))
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


LDTX_TOKEN = re.compile(r"\bldtx\s+\w+,\s*(\w+)")
TEXTPOINTER = re.compile(r"^\ttextpointer\s+(\w+)(?:\s*;\s*(0x[0-9A-Fa-f]+))?")


def load_text_ids() -> dict[str, str]:
    """pret text label -> numeric id, from TextOffsets:: ordinal position.

    `ldtx hl, FooText` loads hl with the label's 1-based index in
    src/text/text_offsets.asm (entry 0 is the null dwb). The trailing
    `; 0xNNNN` comment column, where present, must agree with the computed
    ordinal — a mismatch means the table drifted and the parse is wrong.
    """
    path = PRET / "src" / "text" / "text_offsets.asm"
    table: dict[str, str] = {}
    index = 0
    for line in path.read_text().splitlines():
        match = TEXTPOINTER.match(line)
        if not match:
            continue
        index += 1
        name, comment = match.groups()
        if comment is not None and int(comment, 16) != index:
            raise RuntimeError(
                f"text_offsets.asm ordinal drift at {name}: computed "
                f"{index:#06x}, comment says {comment}")
        table[name] = f"0x{index:04x}u"
    return table


def text_ids_for(asm: str, table: dict[str, str]) -> dict[str, str]:
    found = {}
    for token in LDTX_TOKEN.findall(asm):
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
    if result is None:
        alias = _probe_alias(routine)
        if alias and alias != routine:
            result = prototype_for(alias)
    _PROTO_CACHE[routine] = result
    return result


PROBE_ROW = re.compile(r'\{\s*"([A-Za-z_]\w*)"\s*,\s*adapt_([A-Za-z_]\w*)\s*\}')


def _probe_alias(routine: str) -> str | None:
    """C routine an alias-registered pret symbol actually resolves to.

    Some pret symbols are trampolines the port maps onto an existing C
    function instead of duplicating it: the probe row reads
    ``{ "JPHblankCopyDataHLtoDE", adapt_SafeCopyDataHLtoDE }``. Without this,
    a caller of such a symbol looks like it has an unported callee and gets
    blocked, even though the callee is fully available under another name.
    """
    for probe in sorted((ROOT / "src" / "probe").glob("*.c")):
        for name, adapter in PROBE_ROW.findall(probe.read_text()):
            if name == routine:
                return adapter
    return None


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
    graph, dependents = blocker_graph(functions)
    cascade_cache: dict[str, int] = {}
    def cascade_of(name: str) -> int:
        if name not in cascade_cache:
            cascade_cache[name] = cascade(graph, dependents, {name})
        return cascade_cache[name]

    managed_issues = issue_records(required=True)
    missing = [
        f["name"] for f in functions
        if f["status"] == "todo"
        and f.get("work_id") not in managed_issues
    ]
    if missing:
        raise RuntimeError(
            "Forgejo issue missing for todo routines: "
            + ", ".join(sorted(missing))
        )
    ready = [
        f for f in functions
        if f["status"] == "todo"
        and f["ready"]
        and f["name"] not in blocked
        and managed_issues[f["work_id"]]["state"] == "open"
        and "port-ready" in managed_issues[f["work_id"]]["labels"]
    ]
    held = set()
    for path in QUEUE.glob("*.json"):
        entry = json.loads(path.read_text())
        held.update(r["work_id"] for r in entry.get("routines", [])
                    if r.get("work_id"))
    ready = [f for f in ready if f["work_id"] not in held]
    if dir_filter:
        ready = [f for f in ready if (f["file"] or "").startswith(dir_filter)]

    groups: dict[str, list[dict]] = {}
    for f in sorted(ready, key=lambda f: f["line"]):
        groups.setdefault(f["file"], []).append(f)

    constants_table = load_constants()
    symbol_table = load_symbols()
    text_table = load_text_ids()
    inventory_lines: dict[str, list[int]] = {}
    for f in functions:
        if f["file"]:
            inventory_lines.setdefault(f["file"], []).append(f["line"])

    packets: list[dict] = []
    built_at = int(time.time())

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
            work_ids = sorted(f["work_id"] for f, _asm in chunk)
            digest = hashlib.sha256("\0".join(work_ids).encode()).hexdigest()[:10]
            routines = []
            packet_asm = []
            for f, asm in chunk:
                packet_asm.append(asm)
                issue = managed_issues.get(f["work_id"])
                routines.append({
                    "name": f["name"],
                    "work_id": f["work_id"],
                    "issue_number": issue["issue_number"] if issue else None,
                    "size": f["size"],
                    "line": f["line"],
                    "refs": f["refs"],
                    "asm": asm,
                    "callees": [],
                    "cascade": cascade_of(f["name"]),
                })
            packet = {
                "id": f"{basename}--{digest}",
                "basename": basename,
                "file": file,
                "routines": routines,
                "mode": "append" if (ROOT / "src/home" / f"{basename}.c").exists() else "create",
                "state": "pending",
                "rounds": 0,
                "format_retry_used": False,
                "updated_at": built_at,
                "reason": None,
                "constants": constants_for("\n".join(packet_asm), constants_table),
                "symbols": symbols_for("\n".join(packet_asm), symbol_table),
                "text_ids": text_ids_for("\n".join(packet_asm), text_table),
                "example": pick_example("\n".join(packet_asm)),
                "existing": existing_context(basename),
                "bytes": sum(r["size"] for r in routines),
                "cascade": cascade(graph, dependents, {r["name"] for r in routines}),
            }
            packets.append(packet)

    packets.sort(key=lambda p: (-p["cascade"], p["bytes"]))
    if limit:
        packets = packets[:limit]
    return packets


def drop_claimed(packets: list[dict]) -> list[dict]:
    """Reject duplicate non-terminal work claims instead of silently merging."""
    claims: dict[str, str] = {}
    kept: list[dict] = []
    for path in QUEUE.glob("*.json"):
        entry = json.loads(path.read_text())
        if entry.get("state") not in ACTIVE_CLAIM_STATES:
            continue
        for routine in entry.get("routines", []):
            if "work_id" not in routine or not routine["work_id"]:
                raise RuntimeError(
                    f"active packet {entry['id']} routine {routine.get('name')!r} "
                    "lacks work ID"
                )
            work_id = routine["work_id"]
            owner = claims.get(work_id)
            if owner and owner != entry["id"]:
                raise RuntimeError(
                    f"work ID {work_id} claimed by active packets {owner} and "
                    f"{entry['id']}"
                )
            claims[work_id] = entry["id"]
    for packet in packets:
        for routine in packet["routines"]:
            work_id = routine["work_id"]
            owner = claims.get(work_id)
            if owner and owner != packet["id"]:
                raise RuntimeError(
                    f"work ID {work_id} already claimed by non-terminal packet {owner}"
                )
        claims.update({r["work_id"]: packet["id"] for r in packet["routines"]})
        kept.append(packet)
    return kept


def dissolved_symbols() -> set[str]:
    """pret symbols the port will never contain, per tools/progress/scope.toml.

    Phase-1 dissolves whole files (``vram.asm``, ``double_speed.asm``,
    ``jumptable.asm``, ``call_regs.asm``, ...). A caller of one of those does
    not need a C symbol for it — the call simply disappears in the port, or
    becomes a direct call / function-pointer table. Treating them as
    "unported callee" wrongly blocks perfectly portable routines.
    """
    import tomllib
    path = ROOT / "tools" / "progress" / "scope.toml"
    if not path.exists():
        return set()
    spec = tomllib.load(open(path, "rb"))
    files = set()
    names: set[str] = set()
    for entry in spec.get("exclude", []):
        files.update(entry.get("files", []))
        names.update(entry.get("symbols", []))
    inventory = json.loads((ROOT / "site/data/inventory.json").read_text())
    for name, info in inventory["functions"].items():
        if info.get("file") in files:
            names.add(name)
    return names


def attach_dependencies(packets: list[dict]) -> list[dict]:
    """Fill callee prototypes; drop routines whose callees cannot link.

    A callee with no C prototype blocks its callers — unless it is dissolved
    by the Phase-1 transform, in which case the port omits the call and the
    caller is perfectly portable. Only genuinely unported, in-scope callees
    block.
    """
    inventory = json.loads((ROOT / "site/data/inventory.json").read_text())
    functions = inventory["functions"]
    dissolved = dissolved_symbols()
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
                if proto is None and dep in functions and dep not in dissolved:
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
    build.add_argument("--limit", type=_positive_int, help="emit at most N packets")
    build.add_argument("--force", action="store_true",
                       help="overwrite queue entries that already exist")
    build.add_argument("--json", action="store_true", help="print packet ids as JSON")
    chokepoints = sub.add_parser(
        "chokepoints", help="rank todo routines by transitive cascade")
    chokepoints.add_argument("--limit", type=int, default=20)
    migrate = sub.add_parser(
        "migrate-work-ids",
        help="backfill queue and bundle work identity from the issue cache",
    )
    migrate.add_argument(
        "--apply", action="store_true",
        help="write the validated migration and create a backup",
    )
    args = parser.parse_args()

    if args.command == "migrate-work-ids":
        try:
            counts = run_work_id_migration(apply=args.apply)
        except (OSError, RuntimeError, ValueError) as exc:
            print(f"migration aborted: {exc}", file=sys.stderr)
            return 1
        print(
            "packets={packets} routines={routines} "
            "changed_packets={changed_packets} changed_routines={changed_routines} "
            "bundles={bundles} "
            "changed_bundle_metadata={changed_bundle_metadata}".format(**counts)
        )
        if counts["backup"] is None:
            print("no files written; no backup created")
        else:
            print(f"migration applied; backup: {counts['backup']}")
        return 0

    if args.command == "chokepoints":
        return cmd_chokepoints(args.limit)

    selected_pending = select_pending_packets(args.limit)
    capacity = None if args.limit is None else args.limit - len(selected_pending)
    fresh = []
    if capacity is None or capacity > 0:
        fresh = build_packets(
            args.dir, args.max_routines, args.max_asm_lines, capacity,
        )
        if not args.force:
            fresh = drop_claimed(fresh)
        fresh = attach_dependencies(fresh)
    built_at = int(time.time())
    written = []
    for packet in fresh:
        packet.update({
            "updated_at": built_at,
            "rounds": 0,
            "format_retry_used": False,
        })
        path = QUEUE / f"{packet['id']}.json"
        if path.exists() and not args.force:
            existing = json.loads(path.read_text())
            if existing.get("state") not in (None, "pending"):
                continue
        write_json(path, packet)
        written.append(packet["id"])
    selected_ids = [packet["id"] for packet in selected_pending]
    result_ids = selected_ids + written
    if args.json:
        print(json.dumps(result_ids))
    else:
        for packet in fresh:
            if packet["id"] in written:
                print(f"{packet['id']:32} {packet['mode']:6} routines={len(packet['routines'])} "
                      f"bytes={packet['bytes']} cascade={packet['cascade']}")
        print(f"packets: {len(result_ids)} written, {len(fresh) - len(written)} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
