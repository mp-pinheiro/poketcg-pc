#!/usr/bin/env python3
"""Turn a scenario census into one self-contained fix packet per owning basename."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream

INVENTORY = ROOT / "site" / "data" / "inventory.json"
CASES_DIR = ROOT / "tests" / "cases"
DISASM = ROOT / "poketcg"
FIELD_BASE = {
    "wram": 0xC000,
    "hram": 0xFF80,
    "io": 0xFF00,
    "oam": 0xFE00,
    "sram_bank_0": 0xA000,
    "sram_bank_1": 0xA000,
    "sram_bank_2": 0xA000,
    "sram_bank_3": 0xA000,
    "save": 0xA000,
}


def load_inventory() -> dict[str, dict[str, Any]]:
    return json.loads(INVENTORY.read_text())["functions"]


def routine_basenames() -> dict[str, str]:
    """routine -> pret basename, from the CONTRACT of each case module."""
    import importlib.util

    mapping: dict[str, str] = {}
    for path in sorted(CASES_DIR.glob("*.py")):
        if path.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"case_{path.stem}", path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except (ImportError, SyntaxError, AttributeError, NameError, TypeError, ValueError) as exc:
            print(f"skipped {path.name}: {exc}", file=sys.stderr)
            continue
        for name in getattr(module, "CONTRACT", {}):
            mapping.setdefault(name, path.stem)
    return mapping


def asm_slice(routine: str, inventory: dict[str, dict[str, Any]]) -> str:
    entry = inventory.get(routine)
    if entry is None:
        return ""
    source = DISASM / entry["file"]
    if not source.is_file():
        return ""
    lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
    start = int(entry["line"])
    end = start
    while end < len(lines):
        text = lines[end]
        if text and not text[0].isspace() and not text.lstrip().startswith(";") and "::" in text:
            break
        end += 1
    return "\n".join(f"{entry['file']}:{start + i}: {line}" for i, line in enumerate(lines[start - 1 : end]))


def divergent_addresses(census: dict[str, Any]) -> list[tuple[str, int, int]]:
    """(field, field offset, absolute address) for every census byte."""
    rows = []
    for region in census.get("top_regions", []):
        field = region["field"]
        base = FIELD_BASE.get(field)
        if base is None:
            continue
        for offset in region["offsets"]:
            rows.append((field, offset, base + offset))
    return rows


def build_packets(
    evidence: Path, frames: int, scenario: str, out: Path
) -> dict[str, Any]:
    evidence = evidence if evidence.is_absolute() else (ROOT / evidence).resolve()
    out = out if out.is_absolute() else (ROOT / out).resolve()
    artifact = json.loads(evidence.read_text())
    census = artifact["comparison"]["census"]
    rows = divergent_addresses(census)
    if not rows:
        return {"status": "PASS", "detail": "census is empty", "packets": []}
    addresses = sorted({address for _field, _offset, address in rows})
    attribution = {
        int(entry["address"], 16): entry["writers"]
        for entry in refstream.writers(scenario, frames, addresses)
    }
    basenames = routine_basenames()
    inventory = load_inventory()

    grouped: dict[str, list[dict[str, Any]]] = {}
    for field, offset, address in rows:
        writers = attribution.get(address, [])
        top = writers[0] if writers else None
        routine = top["routine"] if top else None
        owner = basenames.get(routine or "", "unattributed")
        symbol, _base = refstream.resolve_region(field, offset)
        grouped.setdefault(owner, []).append(
            {
                "field": field,
                "offset": offset,
                "address": f"0x{address:04X}",
                "symbol": symbol,
                "writer": top,
                "other_writers": writers[1:3],
                "routine": routine,
            }
        )

    out.mkdir(parents=True, exist_ok=True)
    packets = []
    for owner, entries in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        routines = sorted({row["routine"] for row in entries if row["routine"]})
        body = [
            f"# Divergence packet: {owner} ({len(entries)} byte(s))",
            "",
            f"Scenario `{scenario}`, evidence `{evidence.relative_to(ROOT)}`.",
            "The reference is the real ROM under Gambatte; the native port is this tree.",
            "Every row below is a byte whose value differs at the scenario's terminal frame.",
            "",
            "## Divergent bytes and the reference routine that wrote each",
            "",
            "| field | address | symbol | reference writer | pc |",
            "|---|---|---|---|---|",
        ]
        for row in entries:
            writer = row["writer"] or {}
            label = writer.get("label", "-")
            offset_text = f"+{writer['label_offset']}" if writer.get("label_offset") else ""
            body.append(
                f"| {row['field']} | {row['address']} | {row['symbol']} | "
                f"`{label}{offset_text}` | {writer.get('pc', '-')} |"
            )
        body += [
            "",
            "## Owned files",
            "",
            f"- `src/home/{owner}.c`, `src/home/{owner}.h`, `src/probe/{owner}.c`, `tests/cases/{owner}.py`",
            "",
            "Touch nothing outside those four files. Another agent owns every other basename.",
            "",
            "## Reference assembly for the writer routines",
            "",
        ]
        for routine in routines:
            listing = asm_slice(routine, inventory)
            if not listing:
                continue
            body += [f"### {routine}", "", "```", listing, "```", ""]
        body += [
            "## Acceptance",
            "",
            "- `just oracle-diff <Fn>` prints PASS for every routine you change.",
            "- Do not run the central gate, a formatter, or the full suite.",
            "- Report the routine names you changed and the asm line that justified each change.",
            "- If a byte is unreproducible by construction rather than a port bug, say so with the",
            "  asm citation instead of changing code; do not widen the comparator exclusion ledger",
            "  yourself.",
            "",
        ]
        path = out / f"{owner}.md"
        path.write_text("\n".join(body))
        packets.append(
            {
                "basename": owner,
                "bytes": len(entries),
                "routines": routines,
                "prompt": str(path.relative_to(ROOT)),
            }
        )
    summary = {
        "status": "OK",
        "scenario": scenario,
        "census_total_bytes": census["total_bytes"],
        "census_regions": census["regions"],
        "packets": packets,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--scenario", default="boot-title")
    parser.add_argument("--frames", type=int, default=2400)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    summary = build_packets(
        Path(args.evidence), args.frames, args.scenario, Path(args.out)
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
