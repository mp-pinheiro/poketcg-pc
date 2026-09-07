#!/usr/bin/env python3
"""Report the bytes a routine writes that none of its cases observe.

`just oracle-diff <Fn>` only compares what a case names: its `compare`
registers, seeded WRAM/SRAM, and `read`/`sread`/`vread` spans. A routine that
draws a screen, sorts a list into HRAM scratch or fills a text buffer can be
wrong in every byte it produces and still print PASS, because nothing looked.
That is the shape of every divergence the TAS loop has bisected to a routine
whose oracle was green: `PrintPlayAreaCardInformation` wrote the wrong symbol
tile, `DrawDuelHUD` drew the HP bar one row off, `SortCardsInListByID` left
HRAM scratch unmirrored.

This audit runs each case on the PyBoy reference, diffs RAM between the
routine's entry and its completion, and subtracts every span the routine's
cases observe. What is left is the routine's blind spot: bytes the ROM wrote
that the oracle never checks. The report groups them by symbol so the fix is
mechanical -- add the span to `read`/`sread`/`vread` (or the register to
`compare`) and re-run the oracle.

The synthesized call frame (stack, sentinel, spin) and the hardware counters
the reference advances on its own (`wVBlankCounter`, DIV/TIMA/LY/STAT/IF) are
excluded. A byte a *setup* routine writes is part of the entry state and is not
reported.

Usage:
    blind_spots.py --fn DrawDuelHUD            one routine
    blind_spots.py --all [--json out.json]     every routine with cases
    blind_spots.py --from-list reached.txt     routines named one per line
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
sys.path.insert(0, str(ROOT / "tools" / "oracle"))
sys.path.insert(0, str(ROOT / "tools" / "completion"))

import refstream
from pyboy_oracle import (
    HRAM_BASE, OAM_BASE, RESERVED, SRAM_BASE, VRAM_BASE, WRAM_BASE, Oracle, OracleError,
)
from test_leaves import (
    AUTO_OBSERVE_IGNORED as IGNORED, key_timeline, load_cases, merged_spans, pyboy_frames,
)

RESERVED_ADDRESSES = {address for block in RESERVED for address in block}


def observed_addresses(fn: str, cases: list[dict]) -> set[tuple[str, int, int]]:
    """(field, bank, address) every case of the routine compares."""
    seen: set[tuple[str, int, int]] = set()
    for case in cases:
        if not case.get("oracle", True):
            continue
        reads, sreads, vreads = merged_spans(case)
        for address, size in reads.items():
            field = "hram" if address >= HRAM_BASE else "oam" if address >= OAM_BASE else "wram"
            for offset in range(size):
                seen.add((field, 0, address + offset))
        for bank, spans in sreads.items():
            for address, size in spans.items():
                for offset in range(size):
                    seen.add(("sram", bank, address + offset))
        for bank, spans in vreads.items():
            for address, size in spans.items():
                for offset in range(size):
                    seen.add(("vram", bank, address + offset))
    return seen


def written_addresses(oracle: Oracle, fn: str, case: dict) -> set[tuple[str, int, int]]:
    completion = case.get("_completion", {"mode": "return"})
    stop = completion.get("mode") in ("pre-ret", "entry")
    result = oracle.call(
        fn, a=case.get("a", 0), f=case.get("f", 0), b=case.get("b", 0),
        c=case.get("c", 0), d=case.get("d", 0), e=case.get("e", 0),
        hl=case.get("hl", 0), wram=case.get("wram"), sram=case.get("sram"),
        ramg=case.get("ramg"), setup=case.get("setup"), keys=key_timeline(case),
        stop_pc=completion.get("pc") if stop else None,
        stop_bank=completion.get("bank") if stop else None,
        stack=case.get("stack"), hbank_rom=case.get("hbank_rom"),
        post_call_byte=case.get("post_call_byte"), entry_sp=case.get("entry_sp"),
        frames=pyboy_frames(case),
    )
    entry = oracle.entry_state
    assert entry is not None
    written: set[tuple[str, int, int]] = set()

    def diff(field: str, bank: int, base: int, before: bytes, after: bytes) -> None:
        for offset, (old, new) in enumerate(zip(before, after)):
            if old != new:
                address = base + offset
                if address in RESERVED_ADDRESSES or address in IGNORED:
                    continue
                written.add((field, bank, address))

    diff("wram", 0, WRAM_BASE, entry.wram, result.wram)
    diff("hram", 0, HRAM_BASE, entry.hram, result.hram)
    diff("oam", 0, OAM_BASE, entry.oam, result.oam)
    for bank in range(4):
        diff("sram", bank, SRAM_BASE, entry.sram_banks[bank], result.sram_banks[bank])
    for bank in range(2):
        diff("vram", bank, VRAM_BASE, entry.vram_banks[bank], result.vram_banks[bank])
    return written


def field_name(field: str, bank: int) -> str:
    if field in ("sram", "vram"):
        return f"{field}_bank_{bank}"
    return field


def report(fn: str, blind: set[tuple[str, int, int]]) -> list[dict]:
    rows: list[dict] = []
    by_field: dict[tuple[str, int], list[int]] = {}
    for field, bank, address in blind:
        by_field.setdefault((field, bank), []).append(address)
    for (field, bank), addresses in sorted(by_field.items()):
        window = refstream.FIELD_WINDOWS[field_name(field, bank)][0]
        offsets = sorted(address - window for address in addresses)
        for row in refstream.group_by_symbol(field_name(field, bank), offsets):
            first = min(offsets[i] for i in range(len(offsets)) if offsets[i] >= row["field_offset"])
            rows.append({
                "fn": fn, "field": field, "bank": bank, "symbol": row["symbol"],
                "address": f"0x{window + first:04X}", "count": row["count"],
            })
    rows.sort(key=lambda row: (-row["count"], row["address"]))
    return rows


def audit(oracle: Oracle, fn: str, cases: list[dict]) -> tuple[list[dict], int, str | None]:
    live = [case for case in cases if case.get("oracle", True)]
    written: set[tuple[str, int, int]] = set()
    for case in live:
        try:
            written |= written_addresses(oracle, fn, case)
        except OracleError as exc:
            return [], 0, str(exc)
    blind = written - observed_addresses(fn, cases)
    return report(fn, blind), len(written), None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fn", help="one routine")
    group.add_argument("--all", action="store_true", help="every routine with cases")
    group.add_argument("--from-list", type=Path, help="file naming routines, one per line")
    parser.add_argument("--json", type=Path, help="write the full report here")
    parser.add_argument("--rom", default=os.environ.get("POKETCG_ROM", str(ROOT / "poketcg" / "poketcg.gbc")))
    args = parser.parse_args(argv)

    cases, _contracts = load_cases()
    if args.fn:
        names = [args.fn]
    elif args.from_list:
        names = [line.strip() for line in args.from_list.read_text().splitlines() if line.strip()]
    else:
        names = sorted(cases)
    missing = [name for name in names if name not in cases]
    if missing:
        raise SystemExit(f"no cases for: {', '.join(missing[:10])}")

    results: list[dict] = []
    with Oracle(args.rom) as oracle:
        for name in names:
            rows, written, error = audit(oracle, name, cases[name])
            blind = sum(row["count"] for row in rows)
            results.append({"fn": name, "written": written, "blind": blind,
                            "error": error, "rows": rows})
            if error:
                print(f"ERROR {name}: {error}")
                continue
            if rows:
                print(f"BLIND {name}: {blind}/{written} written bytes unobserved")
                for row in rows[:12]:
                    print(f"    {row['field']}{row['bank'] if row['field'] in ('sram', 'vram') else ''}"
                          f" {row['symbol']} {row['address']} x{row['count']}")
            else:
                print(f"CLEAN {name}: {written} written bytes, all observed")
    if args.json:
        args.json.write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    blind_total = sum(1 for result in results if result["blind"])
    print(f"blind-spots: {len(results)} routines, {blind_total} with unobserved writes",
          file=sys.stderr)
    return 1 if blind_total else 0


if __name__ == "__main__":
    sys.exit(main())
