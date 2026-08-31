#!/usr/bin/env python3
"""Build site/data/inventory.json: byte-weighted code/data labels from the
bootstrapped pret/poketcg checkout (poketcg.map sizes, asm source classification).

Run only when the pret pin in tools/oracle/artifacts.json moves (see just
progress-inventory). Requires `just bootstrap` to have populated poketcg/.
"""
from __future__ import annotations

import glob
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PRET = ROOT / "poketcg"
MAP_FILE = PRET / "poketcg.map"
SRC_DIR = PRET / "src"
OUT_FILE = ROOT / "site" / "data" / "inventory.json"

BANK_RE = re.compile(r'^(ROM0|ROMX|SRAM|WRAM0|WRAM|HRAM|VRAM|OAM) bank #(\d+):$')
SEC_RE = re.compile(r'^\tSECTION: \$([0-9a-f]{4})-\$([0-9a-f]{4}) \(\$([0-9a-f]{4}) bytes\) \["(.*)"\]$')
SYM_RE = re.compile(r'^\t {9}\$([0-9a-f]{4}) = (\S+)$')
LAB_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_#@]*):{1,2}\s*$')
CALL_RE = re.compile(r'^\s*(?:call|jp|jr|farcall|bank1call|homecall|callab|callba)\b(.*)$', re.I)
TERM_RE = re.compile(r'^(ret|reti)\b(?!\s*,)|^(jp|jr)\s+(?!(z|nz|c|nc)\s*,)', re.I)
TOKEN_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
DW_RE = re.compile(r'^\s*dw\s+([A-Za-z_][A-Za-z0-9_.]*)')
DATA_RE = re.compile(r'^\s*(?:dw|db|dn|table_width|dr|ds)\b', re.I)

INSTR = set("""adc add and bit call ccf cp cpl daa dec di ei halt inc jp jr ld ldh ldi ldd
nop or pop push res ret reti rl rla rlc rlca rr rra rrc rrca rst sbc scf set sla sra srl
stop sub swap xor""".split())
CODE_MACROS = {"farcall", "bank1call", "homecall", "callab", "callba", "ldtx", "lb",
               "jumptable", "fallthrough", "jp_hl", "debug_ret", "rst",
               "handle_dmg_or_cgb", "sgb_command"}
SKIP_TOKENS = {"SECTION", "INCLUDE", "ENDC", "IF", "ELSE", "ENDM", "MACRO", "REPT",
               "ENDR", "ASSERT", "UNION", "NEXTU", "ENDU", "DEF", "CHARMAP", "PUSHS",
               "POPS", "RSSET", "EXPORT"}
COND = {"z", "nz", "c", "nc"}
ROM_BANK_TYPES = ("ROM0", "ROMX")


def fail(msg: str) -> None:
    print(f"inventory: {msg}", file=sys.stderr)
    raise SystemExit(2)


def parent_name(name: str) -> str:
    return name.split(".", 1)[0]


def classify_line(stripped: str) -> str | None:
    first = stripped.split()[0].lower()
    if first in INSTR or first in CODE_MACROS:
        return "code"
    return "data"


def extract_callee(line_stripped: str, code_names: set[str], cur_parent: str) -> str | None:
    m = CALL_RE.match(line_stripped)
    if not m:
        return None
    operand = m.group(1).strip()
    if not operand:
        return None
    parts = [p.strip() for p in operand.split(",")]
    target = parts[-1] if (len(parts) > 1 and parts[0].lower() in COND) else parts[0]
    target = target.split(";")[0].strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?", target):
        return None
    p = parent_name(target)
    if p == cur_parent or p not in code_names:
        return None
    return p


def rom_offset(bank_type: str, bank: int, address: int) -> int:
    if bank_type == "ROM0":
        return address
    return bank * 0x4000 + address - 0x4000


def parse_map() -> tuple[dict[str, dict], int, list[dict]]:
    if not MAP_FILE.exists():
        fail("run just bootstrap first")
    labels: dict[str, dict] = {}
    sections: list[dict] = []
    bank_type = None
    bank_num = None
    sec_start = sec_end = None
    sec_name = None
    sec_syms: list[tuple[int, str]] = []

    def flush_section():
        if bank_type not in ROM_BANK_TYPES or sec_start is None:
            return
        top = [(a, n) for a, n in sec_syms if "." not in n]
        sections.append({
            "bank_type": bank_type,
            "bank": bank_num,
            "address": sec_start,
            "length": sec_end - sec_start + 1,
            "end": sec_end,
            "section": sec_name,
            "symbols": [{"address": a, "name": n} for a, n in top],
        })
        for i, (addr, name) in enumerate(top):
            next_addr = top[i + 1][0] if i + 1 < len(top) else sec_end + 1
            size = next_addr - addr
            if name not in labels:
                labels[name] = {
                    "addr": addr, "size": size, "bank": bank_num, "section": sec_name,
                }

    for raw in MAP_FILE.read_text().splitlines():
        m = BANK_RE.match(raw)
        if m:
            flush_section()
            bank_type, bank_num = m.group(1), int(m.group(2))
            sec_start = None
            continue
        m = SEC_RE.match(raw)
        if m:
            flush_section()
            sec_start = int(m.group(1), 16)
            sec_end = int(m.group(2), 16)
            sec_name = m.group(4)
            sec_syms = []
            continue
        m = SYM_RE.match(raw)
        if m:
            sec_syms.append((int(m.group(1), 16), m.group(2)))
    flush_section()

    text = MAP_FILE.read_text()
    rm = re.search(r"ROM0: (\d+) bytes used.*?ROMX: (\d+) bytes used", text, re.S)
    rom_bytes = int(rm.group(1)) + int(rm.group(2)) if rm else None

    return labels, rom_bytes, sections


def process_asm_files(map_labels: dict[str, dict]) -> tuple[dict[str, dict], dict[str, int], list[str]]:
    files = sorted(glob.glob(str(SRC_DIR / "**" / "*.asm"), recursive=True))
    if not files:
        fail("no .asm sources found under poketcg/src")

    defs: dict[str, dict] = {}
    refs: Counter[str] = Counter()

    for fp in files:
        rel = str(Path(fp).relative_to(PRET))
        text = Path(fp).read_text(errors="replace")
        lines = text.splitlines()

        for line in lines:
            cstripped = line.split(";", 1)[0].rstrip("\n")
            if cstripped.strip():
                refs.update(TOKEN_RE.findall(cstripped.strip()))

        pending_labels: list[tuple[str, int]] = []
        cur_top: str | None = None
        last_body: str | None = None
        prev_kind: str | None = None

        for lineno, raw in enumerate(lines, start=1):
            stripped = raw.split(";", 1)[0].strip()
            if not stripped:
                continue
            if stripped.startswith("."):
                continue
            m = LAB_RE.match(stripped)
            if m:
                name = m.group(1)
                if "." not in name:
                    # `prev_kind` describes the FIRST body line, so a routine that
                    # ends in a data table (`tx`/`db`/`dw`/`assert_table_length`)
                    # still looked like code falling through into its neighbour.
                    # Data is never executed, so require the LAST line to be code
                    # too -- otherwise the phantom dep can close a dependency
                    # cycle and starve both routines out of the frontier forever
                    # (measured on GetPCPackNameTextID -> PrintPCPackName).
                    if (cur_top and last_body is not None and prev_kind == "code"
                            and classify_line(last_body) == "code"):
                        if not TERM_RE.match(last_body):
                            if cur_top in defs:
                                defs[cur_top]["fallthrough"] = name
                    pending_labels.append((name, lineno))
                else:
                    pending_labels.append((name, lineno))
                continue
            first_tok = stripped.split()[0].upper()
            if first_tok in SKIP_TOKENS:
                if first_tok == "SECTION":
                    pending_labels = []
                    cur_top = None
                    last_body = None
                    prev_kind = None
                continue
            if pending_labels:
                kind = classify_line(stripped)
                for lab_name, lab_line in pending_labels:
                    if lab_name not in defs:
                        defs[lab_name] = {
                            "file": rel, "line": lab_line, "kind": kind,
                            "deps": set(), "fallthrough": None,
                        }
                cur_top = parent_name(pending_labels[-1][0])
                prev_kind = kind
                pending_labels = []
            else:
                kind = classify_line(stripped)
            callee = extract_callee(stripped, set(), cur_top or "")
            if callee and cur_top and cur_top in defs:
                defs[cur_top]["deps"].add(callee)
            last_body = stripped

        if cur_top and last_body is not None and prev_kind == "code":
            if not TERM_RE.match(last_body):
                pass

    code_names = {n for n, d in defs.items() if n in map_labels and d["kind"] == "code"}

    for fp in files:
        text = Path(fp).read_text(errors="replace")
        lines = text.splitlines()
        pending_labels: list[tuple[str, int]] = []
        cur_top: str | None = None

        for lineno, raw in enumerate(lines, start=1):
            stripped = raw.split(";", 1)[0].strip()
            if not stripped:
                continue
            if stripped.startswith("."):
                continue
            m = LAB_RE.match(stripped)
            if m:
                name = m.group(1)
                if "." not in name:
                    pending_labels = [(name, lineno)]
                else:
                    pending_labels.append((name, lineno))
                continue
            first_tok = stripped.split()[0].upper()
            if first_tok in SKIP_TOKENS:
                if first_tok == "SECTION":
                    pending_labels = []
                    cur_top = None
                continue
            if pending_labels:
                cur_top = parent_name(pending_labels[-1][0])
                pending_labels = []
            callee = extract_callee(stripped, code_names, cur_top or "")
            if callee and cur_top and cur_top in defs:
                defs[cur_top]["deps"].add(callee)

    # Indirect dispatch. A body that reaches its callees through a `dw` pointer
    # table (JumpToFunctionInTable, the `jumptable` macro, or hand-rolled
    # LOW/HIGH pointer arithmetic) has real control-flow edges that `call`/`jp`
    # scanning cannot see, so the routine would otherwise report ready with no
    # blockers while its targets have no C body -- and a candidate issued for it
    # can only compile by stubbing the table. Two sources count: a table under
    # one of the routine's own sub-labels, and a top-level table the routine
    # names. A table that merely *follows* a routine is not attributed to it.
    table_cache: dict[str, set[str]] = {}

    def table_targets(label: str) -> set[str]:
        if label in table_cache:
            return table_cache[label]
        table_cache[label] = set()
        entry = defs.get(label)
        if not entry or not entry.get("file") or not entry.get("line"):
            return table_cache[label]
        lines_ = Path(PRET / entry["file"]).read_text(errors="replace").splitlines()
        found: set[str] = set()
        for raw in lines_[entry["line"]:]:
            body = raw.split(";", 1)[0]
            if not body.strip():
                continue
            if body[0] not in " \t." and LAB_RE.match(body.strip()):
                break
            m = DW_RE.match(body)
            if m:
                found.add(parent_name(m.group(1)))
                continue
            if not DATA_RE.match(body):
                break
        table_cache[label] = found
        return found

    for fp in files:
        rel = str(Path(fp).relative_to(PRET))
        lines = Path(fp).read_text(errors="replace").splitlines()
        cur_top = None
        for raw in lines:
            body = raw.split(";", 1)[0]
            if not body.strip():
                continue
            if body[0] not in " \t.":
                m = LAB_RE.match(body.strip())
                cur_top = m.group(1) if m else None
                continue
            if cur_top is None or cur_top not in defs:
                continue
            targets: set[str] = set()
            m = DW_RE.match(body)
            if m:
                targets.add(parent_name(m.group(1)))
            for token in TOKEN_RE.findall(body):
                if token in defs and token != cur_top:
                    targets |= table_targets(token)
            for target in targets:
                if target in code_names and target != cur_top:
                    defs[cur_top]["deps"].add(target)

    unknown = sorted(n for n in map_labels if n not in defs)
    for n in unknown:
        defs[n] = {"file": None, "line": None, "kind": "unknown", "deps": set(),
                    "fallthrough": None}

    ref_map = {}
    for name in defs:
        r = refs.get(name, 0)
        if "." not in name:
            def_lines = 1
        else:
            def_lines = 0
        ref_map[name] = max(r - def_lines, 0)

    return defs, ref_map, unknown
def build_spans(sections: list[dict], defs: dict[str, dict]) -> list[dict]:
    spans: list[dict] = []
    for section in sections:
        bank_type = section["bank_type"]
        bank = section["bank"]
        section_start = section["address"]
        section_end = section["end"] + 1
        if bank_type == "ROM0":
            base_offset = section_start
        else:
            base_offset = bank * 0x4000 + section_start - 0x4000
        by_address: dict[int, str] = {}
        for symbol in section["symbols"]:
            by_address.setdefault(symbol["address"], symbol["name"])
        addresses = sorted(by_address.items())
        cursor = section_start
        for index, (address, name) in enumerate(addresses):
            if address > cursor:
                spans.append({
                    "kind": "unclassified",
                    "source": "mapped-gap",
                    "bank_type": bank_type,
                    "bank": bank,
                    "address": cursor,
                    "length": address - cursor,
                    "offset": base_offset + cursor - section_start,
                    "section": section["section"],
                })
            end = addresses[index + 1][0] if index + 1 < len(addresses) else section_end
            definition = defs.get(name, {})
            kind = definition.get("kind")
            if kind not in {"code", "data"}:
                kind = "unclassified"
            if section["section"].casefold() == "romheader":
                kind = "header/metadata"
            spans.append({
                "kind": kind,
                "source": "mapped-symbol",
                "bank_type": bank_type,
                "bank": bank,
                "address": address,
                "length": end - address,
                "offset": base_offset + address - section_start,
                "section": section["section"],
                "symbol": name,
            })
            cursor = end
        if cursor < section_end:
            spans.append({
                "kind": "unclassified",
                "source": "mapped-gap",
                "bank_type": bank_type,
                "bank": bank,
                "address": cursor,
                "length": section_end - cursor,
                "offset": base_offset + cursor - section_start,
                "section": section["section"],
            })
    return sorted(spans, key=lambda span: span["offset"])


def main() -> int:
    map_labels, rom_bytes, sections = parse_map()
    defs, refs_map, unknown = process_asm_files(map_labels)
    spans = build_spans(sections, defs)

    functions = {}
    data_labels = 0
    data_bytes = 0
    for name, info in map_labels.items():
        d = defs.get(name)
        if d is None:
            continue
        if d["kind"] == "data":
            data_labels += 1
            data_bytes += info["size"]
            continue
        if d["kind"] != "code":
            continue
        dep_set = set(d["deps"])
        if d.get("fallthrough"):
            dep_set.add(d["fallthrough"])
        functions[name] = {
            "file": d["file"], "line": d["line"], "bank": info["bank"],
            "addr": info["addr"], "size": info["size"],
            "deps": sorted(dep_set),
            "fallthrough": d.get("fallthrough"),
            "refs": refs_map.get(name, 0),
        }

    for n in unknown:
        print(f"inventory: unknown label with no asm definition: {n}", file=sys.stderr)

    pret_commit = subprocess.run(
        ["git", "-C", str(PRET), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()

    mapped_bytes = sum(span["length"] for span in spans)
    unclassified_bytes = sum(
        span["length"] for span in spans if span["kind"] == "unclassified"
    )
    out = {
        "schema": 2,
        "pret_commit": pret_commit,
        "rom_bytes": rom_bytes,
        "mapped_sections": len(sections),
        "mapped_bytes": mapped_bytes,
        "unclassified_bytes": unclassified_bytes,
        "totals": {
            "code_functions": len(functions),
            "code_bytes": sum(f["size"] for f in functions.values()),
            "data_labels": data_labels,
            "data_bytes": data_bytes,
        },
        "unknown_labels": unknown,
        "functions": functions,
        "spans": spans,
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(out, sort_keys=True, separators=(",", ":")))
    print(f"inventory: code_functions={out['totals']['code_functions']}, "
          f"code_bytes={out['totals']['code_bytes']}, "
          f"data_labels={out['totals']['data_labels']}, "
          f"data_bytes={out['totals']['data_bytes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
