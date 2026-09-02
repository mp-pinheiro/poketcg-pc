#!/usr/bin/env python3
"""Coverage-guided input search: drive the ROM into unvisited code and emit the script."""

from __future__ import annotations

import argparse
import ctypes
import heapq
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream

# JOYP nibble order, the same encoding scenario.boot_input emits and the native
# --input flag consumes: low nibble dpad, high nibble buttons.
BUTTON = {
    "A": 0x10, "B": 0x20, "SELECT": 0x40, "START": 0x80,
    "RIGHT": 0x01, "LEFT": 0x02, "UP": 0x04, "DOWN": 0x08,
}

PRESS_FRAMES = 4
SETTLE_FRAMES = 20
WAIT_FRAMES = 90
# Repeat counts exist because menu progress needs long uniform chains: the
# overworld entry sits 35 consecutive A presses past the naming screen, which a
# branching search over single presses cannot assemble.
REPEATS = (1, 5, 20)


class ExploreError(RuntimeError):
    pass


def actions() -> list[tuple[str, int, int, int, int]]:
    """(label, mask, press frames, settle frames, repeats)."""
    rows = [("WAIT", 0, 0, WAIT_FRAMES, 1), ("WAIT5", 0, 0, WAIT_FRAMES, 5)]
    for name, mask in BUTTON.items():
        for repeat in REPEATS:
            label = name if repeat == 1 else f"{name}x{repeat}"
            rows.append((label, mask, PRESS_FRAMES, SETTLE_FRAMES, repeat))
    return rows


def path_to_masks(path: list[str], seed_masks: list[int]) -> list[int]:
    """Replayable per-frame mask timeline for an action path, in the same
    encoding scenario.boot_input emits and the native --input flag consumes."""
    table = {label: (mask, press, settle, repeats)
             for label, mask, press, settle, repeats in actions()}
    masks = list(seed_masks)
    for label in path:
        mask, press, settle, repeats = table[label]
        for _ in range(repeats):
            masks.extend([mask] * press)
            masks.extend([0] * settle)
    return masks


class Explorer:
    def __init__(self, budget: int, seed_masks: list[int], seed: int = 20260902,
                 checkpoint_dir: Path | None = None) -> None:
        self.rng = random.Random(seed)
        self.checkpoint_dir = checkpoint_dir
        if checkpoint_dir is not None:
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.core = refstream.Core(seed_masks)
        library = self.core.library
        library.gambatte_newstatesave.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
        library.gambatte_newstatesave.restype = ctypes.c_int
        library.gambatte_newstateload.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
        library.gambatte_newstateload.restype = ctypes.c_int
        self.candidates, self.by_bank_address = refstream.routine_entry_addresses()
        self.seen: set[str] = set()
        self.hits: set[str] = set()
        self.budget = budget
        self.expansions = 0
        self.core.install_exec(self._on_exec)
        self._state_len = library.gambatte_newstatelen(self.core.core)
        if self._state_len <= 0:
            raise ExploreError("gambatte_newstatelen returned no length")

    def _on_exec(self, address: int, _cycle: int) -> None:
        if address not in self.candidates:
            return
        bank = 0 if address < 0x4000 else self.core.bank_of(address)
        name = self.by_bank_address.get((bank, address))
        if name is not None:
            self.hits.add(name)

    def snapshot(self) -> bytes:
        buffer = ctypes.create_string_buffer(self._state_len)
        if not self.core.library.gambatte_newstatesave(self.core.core, buffer, self._state_len):
            raise ExploreError("gambatte_newstatesave failed")
        return buffer.raw

    def restore(self, blob: bytes) -> None:
        if not self.core.library.gambatte_newstateload(self.core.core, blob, len(blob)):
            raise ExploreError("gambatte_newstateload failed")

    def domains(self) -> dict[str, Any]:
        """Checkpoint memory in the native --dump-state schema, so the port can
        be started from a reference state instead of having to reach it."""
        vram = self.core.area("VRAM")
        registers = self.core.io_block()
        return {
            "schema": 1,
            "format": "reference-checkpoint-v1",
            "wram": list(self.core.area("WRAM")[:0x2000]),
            "hram": list(self.core.hram_block()),
            "io": list(registers),
            "oam": list(self.core.area("OAM")[:0xA0]),
            "palette_ram": list(self.core.palette_block()),
            "vram_bank_0": list(vram[:0x2000]),
            "vram_bank_1": list(vram[0x2000:0x4000]),
            "sram": list(self.core.area("CartRAM")[:0x8000]),
            "mapper_state": {
                "rom_bank": self.core.bank_of(0x4000),
                "vram_bank": registers[0x4F] & 0x01,
            },
        }

    def advance(self, mask: int, press: int, settle: int, repeats: int = 1) -> set[str]:
        """Run one action, repeated, and return the routines it newly reached."""
        self.hits = set()
        for _ in range(repeats):
            if press:
                self.core.hold(mask)
                for _ in range(press):
                    self.core.step_frame()
            self.core.hold(0)
            for _ in range(settle):
                self.core.step_frame()
        return self.hits - self.seen

    def seed(self, masks: list[int]) -> tuple[bytes, int]:
        """Replay a known-good prefix so the search starts past the intro."""
        self.hits = set()
        self.core.hold(None)
        self.core.run(len(masks))
        self.seen |= self.hits
        return self.snapshot(), len(masks)

    def search(self, seed_masks: list[int], report_every: int, frontier_cap: int) -> dict[str, Any]:
        start = time.perf_counter()
        blob, frames = self.seed(seed_masks)
        # Every reachable state stays in the frontier, prioritised by what its
        # action just discovered. Dropping zero-gain children starves the search
        # immediately: navigating a menu needs a DOWN that reveals nothing
        # before the A that does.
        frontier: list[tuple[int, int, float, bytes, list[str]]] = []
        visited: set[int] = set()
        heapq.heappush(frontier, (0, -frames, self.rng.random(), blob, []))
        best_path: list[str] = []
        timeline: list[dict[str, Any]] = []
        while frontier and self.expansions < self.budget:
            # A deterministic tie-break dives the first action forever: with
            # every sibling at equal depth and zero discovery it walked a
            # 31,000-frame chain of WAITs. Random tie-breaks plus occasional
            # uniform restarts keep the search moving across screens.
            if self.rng.random() < 0.2 and len(frontier) > 1:
                index = self.rng.randrange(len(frontier))
                frontier[index], frontier[-1] = frontier[-1], frontier[index]
                _score, negative_depth, _seq, blob, path = frontier.pop()
                heapq.heapify(frontier)
            else:
                _score, negative_depth, _seq, blob, path = heapq.heappop(frontier)
            depth = -negative_depth
            for label, mask, press, settle, repeats in actions():
                if self.expansions >= self.budget:
                    break
                self.restore(blob)
                found = self.advance(mask, press, settle, repeats)
                self.expansions += 1
                child_blob = self.snapshot()
                digest = hash(child_blob)
                if digest in visited:
                    continue
                visited.add(digest)
                child_depth = depth + (press + settle) * repeats
                if found:
                    self.seen |= found
                    entry = {
                        "action": label, "new_routines": len(found),
                        "total": len(self.seen), "depth": child_depth,
                        "path": path + [label],
                    }
                    if self.checkpoint_dir is not None:
                        stem = f"ck{len(timeline):04d}-{label}-{len(found)}"
                        (self.checkpoint_dir / f"{stem}.gbs").write_bytes(child_blob)
                        (self.checkpoint_dir / f"{stem}.json").write_text(
                            json.dumps(self.domains(), separators=(",", ":")) + "\n")
                        entry["checkpoint"] = f"{stem}.gbs"
                        entry["state"] = f"{stem}.json"
                    timeline.append(entry)
                child = path + [label]
                # The random key stops equal-scoring siblings from being
                # explored in a fixed order, which collapsed the search into a
                # single 31,000-frame chain of WAITs.
                heapq.heappush(
                    frontier,
                    (-len(found), -child_depth, self.rng.random(), child_blob, child),
                )
                if len(child) > len(best_path):
                    best_path = child
            if len(frontier) > frontier_cap:
                frontier = heapq.nsmallest(frontier_cap, frontier)
                heapq.heapify(frontier)
            if report_every and self.expansions % report_every == 0:
                print(
                    f"  expansions={self.expansions} covered={len(self.seen)} "
                    f"frontier={len(frontier)} depth={depth}",
                    file=sys.stderr,
                )
        return {
            "expansions": self.expansions,
            "covered": len(self.seen),
            "seconds": round(time.perf_counter() - start, 2),
            "discoveries": timeline,
            "deepest_path": best_path,
        }

    def close(self) -> None:
        self.core.close()


def subsystem_report(covered: set[str]) -> dict[str, dict[str, int]]:
    inventory = json.loads((ROOT / "site" / "data" / "inventory.json").read_text())["functions"]

    def group(path: str) -> str:
        parts = path.replace("src/", "").split("/")
        return f"engine/{parts[1]}" if parts[0] == "engine" and len(parts) > 1 else parts[0]

    totals: dict[str, int] = {}
    hit: dict[str, int] = {}
    for name, info in inventory.items():
        key = group(info["file"])
        totals[key] = totals.get(key, 0) + 1
        if name in covered:
            hit[key] = hit.get(key, 0) + 1
    return {
        key: {"executed": hit.get(key, 0), "total": totals[key]}
        for key in sorted(totals, key=lambda k: -totals[k])
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--budget", type=int, default=400, help="action expansions")
    parser.add_argument("--seed-frames", type=int, default=1300,
                        help="boot-title prefix replayed before searching")
    parser.add_argument("--report-every", type=int, default=50)
    parser.add_argument("--frontier-cap", type=int, default=4000)
    parser.add_argument("--json")
    parser.add_argument("--corpus", help="directory for checkpoints and replay scripts")
    args = parser.parse_args(argv)

    import scenario as scenario_module

    seed_masks = scenario_module.boot_input(args.seed_frames)
    corpus = Path(args.corpus) if args.corpus else None
    if corpus is not None and not corpus.is_absolute():
        corpus = ROOT / corpus
    explorer = Explorer(args.budget, seed_masks,
                        checkpoint_dir=(corpus / "checkpoints") if corpus else None)
    try:
        result = explorer.search(seed_masks, args.report_every, args.frontier_cap)
        result["subsystems"] = subsystem_report(explorer.seen)
        result["covered_routines"] = sorted(explorer.seen)
    finally:
        explorer.close()
    if corpus is not None:
        scripts = corpus / "scripts"
        scripts.mkdir(parents=True, exist_ok=True)
        # Replay scripts are emitted for the discoveries that unlocked the most
        # routines, because a path is only worth replaying on the native lane if
        # it reaches code the shorter paths never do.
        ranked = sorted(result["discoveries"], key=lambda row: -row["new_routines"])
        index = []
        for position, row in enumerate(ranked[:32]):
            masks = path_to_masks(row["path"], seed_masks)
            name = f"s{position:02d}-{row['action']}-{row['new_routines']}.txt"
            (scripts / name).write_text(",".join(str(v) for v in masks) + "\n")
            index.append({
                "script": f"scripts/{name}", "frames": len(masks),
                "new_routines": row["new_routines"], "action": row["action"],
                "checkpoint": row.get("checkpoint"), "path": row["path"],
            })
        (corpus / "corpus.json").write_text(
            json.dumps({"schema": 1, "format": "input-corpus-v1",
                        "covered": result["covered"], "entries": index},
                       indent=2, sort_keys=True) + "\n")
        result["corpus"] = str(corpus.relative_to(ROOT))
        result["corpus_entries"] = len(index)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json:
        Path(args.json).write_text(text + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("discoveries", "covered_routines")},
                     indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
