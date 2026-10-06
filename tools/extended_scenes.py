#!/usr/bin/env python3
"""Derive animation and SFX scenes from verified Extended sessions.

Replays each Extended session on the reference core and records, per DoFrame
ordinal, the attack animation loaded in wLoadedAttackAnimation and every SFX
id written to wCurSfxID. A manifest entry gets a scene when a session plays
it; the scene passes when the session's confirmed ordinal (the native port
matched the reference byte for byte that far) covers the ordinals it played
on, so the scene is the evidence that the native rendering, palettes, OAM,
state and audio of that animation agree with the reference.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("POKETCG_PROFILE", "extended")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "completion"))

import refstream
import session as session_tool
from gen_constants import constant_names, evaluate
from tools.profiles import get_profile, symbol_address

PROFILE = get_profile("extended", ROOT)
SCENES_DIR = ROOT / "tests" / "profiles" / "extended" / "scenes"
RATCHET = ROOT / "tools" / "completion" / "session_ratchet_extended.json"


def manifest_values(manifest: dict[str, object]) -> dict[str, tuple[str, int]]:
    disasm = PROFILE.source_path(ROOT)
    values = evaluate(disasm, constant_names(disasm))
    result: dict[str, tuple[str, int]] = {}
    for entry in manifest["entries"]:
        name = entry["name"]
        if name not in values:
            raise SystemExit(f"manifest constant {name} is not defined by the Extended constants")
        result[name] = ("animation" if name.startswith("ATK_ANIM_") else "sfx", values[name])
    return result


def confirmed_ordinal(name: str) -> int:
    if not RATCHET.is_file():
        return 0
    return int(json.loads(RATCHET.read_text()).get(name, {}).get("confirmed_ordinal", 0))


def replay(name: str) -> tuple[dict[int, list[tuple[int, int]]], dict[int, list[tuple[int, int]]]]:
    masks, meta = session_tool.load_session(name)
    frames = session_tool.reference_frames(masks, meta)
    anim_addr = symbol_address(PROFILE, "wLoadedAttackAnimation", ROOT)[1]
    sfx_addr = symbol_address(PROFILE, "wCurSfxID", ROOT)[1]
    animations: dict[int, list[tuple[int, int]]] = {}
    sfx: dict[int, list[tuple[int, int]]] = {}
    with refstream.Core(masks, pokes=meta["pokes"], save=meta["save"]) as core:
        core.input_axis = "ordinal"
        current = {"anim": None}

        def on_write(address: int, _cycle: int) -> None:
            if address == sfx_addr:
                value = core.library.gambatte_cpuread(core.core, address) & 0x7F
                if value not in (0, 0x00):
                    spans = sfx.setdefault(value, [])
                    if not spans or spans[-1][1] < core.ordinal - 1:
                        spans.append((core.ordinal, core.ordinal))
                    else:
                        spans[-1] = (spans[-1][0], core.ordinal)

        def on_exec(address: int, _cycle: int) -> None:
            if address != refstream.DOFRAME_ANCHOR:
                return
            value = core.library.gambatte_cpuread(core.core, anim_addr)
            if value == 0:
                current["anim"] = None
                return
            spans = animations.setdefault(value, [])
            if current["anim"] == value and spans and spans[-1][1] >= core.ordinal - 1:
                spans[-1] = (spans[-1][0], core.ordinal)
            else:
                spans.append((core.ordinal, core.ordinal))
            current["anim"] = value

        core.library.gambatte_cpuread.restype = __import__("ctypes").c_ubyte
        core.on_write(on_write)
        core.install_exec(on_exec)
        core.run(frames, stop=lambda: core.ordinal > len(masks))
    return animations, sfx


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", type=Path,
                        default=ROOT / "build-extended" / "completion" / "extended-animation-manifest.json")
    parser.add_argument("sessions", nargs="*", help="Extended session names (default: all)")
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    wanted = manifest_values(manifest)
    by_value = {(kind, value): name for name, (kind, value) in wanted.items()}
    names = args.sessions or sorted(path.name for path in PROFILE.session_path(ROOT).iterdir()
                                    if (path / "input.txt").is_file())
    found: dict[str, dict[str, object]] = {}
    for session_name in names:
        animations, sfx = replay(session_name)
        confirmed = confirmed_ordinal(session_name)
        for kind, table in (("animation", animations), ("sfx", sfx)):
            for value, spans in table.items():
                name = by_value.get((kind, value))
                if name is None:
                    continue
                first, last = spans[0]
                record = {
                    "name": name,
                    "kind": kind,
                    "value": value,
                    "session": session_name,
                    "first_ordinal": first,
                    "last_ordinal": last,
                    "confirmed_ordinal": confirmed,
                    "status": "pass" if confirmed >= last else "fail",
                }
                previous = found.get(name)
                if previous is None or (record["status"] == "pass" and previous["status"] != "pass"):
                    found[name] = record
        print(f"{session_name}: animations={sorted(animations)} sfx={sorted(sfx)} confirmed={confirmed}")
    SCENES_DIR.mkdir(parents=True, exist_ok=True)
    for name, record in found.items():
        (SCENES_DIR / f"{name}.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    missing = sorted(set(wanted) - set(found))
    passing = sum(1 for record in found.values() if record["status"] == "pass")
    print(f"scenes: manifest={len(wanted)} found={len(found)} passing={passing} missing={len(missing)}")
    for name in missing:
        print(f"  missing {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
