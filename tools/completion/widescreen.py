#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import struct
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import refstream
import session
import witness

SCREEN_W = 160
SCREEN_H = 144
WIDE_EXTRA = 48
SPRITES_PER_LINE = 10
SPRITES_MAX = 40
OVERWORLD_DO_FRAME = 0x380E
OVERWORLD_MAP = 0x00
LCD_OFF_COLOR = 0x7FFF
BG_MAP0 = 0x1800
BG_MAP1 = 0x1C00
DO_FRAME = witness.wram_offset("wDoFrameFunction")
CUR_MAP = witness.wram_offset("wCurMap")
MAP_WIDTH = witness.wram_offset("wBGMapWidth")


class WidescreenError(RuntimeError):
    pass


@dataclass(frozen=True)
class Scenario:
    sessions: tuple[str, ...]
    fields: tuple[str, ...]
    terminal: str
    sprite_limit: int = SPRITES_PER_LINE
    need: tuple[str, ...] = ()
    samples: int = 48


def corpus_sessions() -> tuple[str, ...]:
    names: list[str] = []
    for spec in witness.SPECS.values():
        for name in spec.sessions:
            if name not in names:
                names.append(name)
    return tuple(names)


SCENARIOS: dict[str, Scenario] = {
    "span-widening": Scenario(
        sessions=("seed-deck-machines", "challenge-machine", "boot-menu"),
        fields=("framebuffer",),
        terminal="WIDE_SPAN_CLOSED",
        need=("widened",),
    ),
    "viewport-rect": Scenario(
        sessions=("seed-deck-machines", "challenge-machine"),
        fields=("wram", "framebuffer"),
        terminal="VIEWPORT_RECT_CLOSED",
        need=("rooms", "clamped"),
    ),
    "wide-layouts": Scenario(
        sessions=("boot-menu", "seed-packs", "effect-item-finder"),
        fields=("wram", "framebuffer"),
        terminal="WIDE_UI_CLOSED",
        need=("layouts",),
    ),
    "render-only": Scenario(
        sessions=("seed-deck-machines", "effect-item-finder", "boot-menu"),
        fields=("wram", "framebuffer"),
        terminal="RENDER_ONLY_CLOSED",
        sprite_limit=SPRITES_MAX,
    ),
    "widescreen-corpus": Scenario(
        sessions=corpus_sessions(),
        fields=("wram", "framebuffer", "save", "rng"),
        terminal="WIDESCREEN_CORPUS_CLOSED",
        samples=12,
    ),
}


def color(palette: bytes, index: int) -> int:
    return (palette[index] | (palette[index + 1] << 8)) & 0x7FFF


def fetch(vram: bytes, mapx: int, mapy: int, base: int, lcdc: int) -> tuple[int, int, int]:
    tile = base + ((mapy >> 3) % 32) * 32 + (mapx >> 3) % 32
    number = vram[tile]
    index = number if lcdc & 0x10 else (number ^ 0x80) + 0x80
    attr = vram[0x2000 + tile]
    bank = (attr >> 3) & 1
    row = 7 - (mapy & 7) if attr & 0x40 else mapy & 7
    column = 7 - (mapx & 7) if attr & 0x20 else mapx & 7
    offset = bank * 0x2000 + index * 16 + row * 2
    bit = 7 - column
    value = ((vram[offset] >> bit) & 1) | (((vram[offset + 1] >> bit) & 1) << 1)
    return value, attr & 7, (attr >> 7) & 1


def render(state: dict[str, Any], extra: int, limit: int) -> list[int]:
    vram, oam, palette, io = state["vram"], state["oam"], state["palette_ram"], state["io"]
    width = SCREEN_W + 2 * extra
    lcdc = io[0x40]
    if not lcdc & 0x80:
        return [LCD_OFF_COLOR] * (width * SCREEN_H)
    scx, scy, wx, wy = io[0x43], io[0x42], io[0x4B] - 7, io[0x4A]
    bgmap = BG_MAP1 if lcdc & 0x08 else BG_MAP0
    winmap = BG_MAP1 if lcdc & 0x40 else BG_MAP0
    height = 16 if lcdc & 0x04 else 8
    frame: list[int] = []
    window_line = -1
    for ly in range(SCREEN_H):
        active = bool(lcdc & 0x20) and wy <= ly and wx < SCREEN_W
        start = max(0, wx) if active else SCREEN_W
        if active:
            window_line += 1
        row: list[int] = []
        flags: list[int] = []
        for x in range(-extra, SCREEN_W + extra):
            if start <= x < SCREEN_W:
                value, pal, priority = fetch(vram, x - wx, window_line, winmap, lcdc)
            else:
                value, pal, priority = fetch(vram, (x + scx) & 0xFF, ly + scy, bgmap, lcdc)
            row.append(color(palette, pal * 8 + value * 2))
            flags.append((2 if priority else 0) | (1 if value == 0 else 0))
        if lcdc & 0x02:
            found = [n for n in range(40) if oam[n * 4] - 16 <= ly < oam[n * 4] - 16 + height][:limit]
            for n in reversed(found):
                sy, sx = oam[n * 4] - 16, oam[n * 4 + 1] - 8
                tile = oam[n * 4 + 2] & (0xFE if height == 16 else 0xFF)
                attr = oam[n * 4 + 3]
                dy = ly - sy
                yy = height - dy - 1 if attr & 0x40 else dy
                offset = ((attr >> 3) & 1) * 0x2000 + tile * 16 + yy * 2
                for dx in range(8):
                    px = sx + dx
                    if px < -extra or px >= SCREEN_W + extra:
                        continue
                    bit = 7 - (7 - dx if attr & 0x20 else dx)
                    value = ((vram[offset] >> bit) & 1) | (((vram[offset + 1] >> bit) & 1) << 1)
                    if value == 0:
                        continue
                    flag = flags[px + extra]
                    if not lcdc & 0x01:
                        draw = True
                    elif flag & 2 or attr & 0x80:
                        draw = bool(flag & 1)
                    else:
                        draw = True
                    if draw:
                        row[px + extra] = color(palette, 0x40 + (attr & 7) * 8 + value * 2)
        frame.extend(row)
    return frame


def viewport(state: dict[str, Any], extra: int) -> tuple[int, int, bool]:
    wram, io = state["wram"], state["io"]
    frame_function = wram[DO_FRAME] | (wram[DO_FRAME + 1] << 8)
    if not (io[0x40] & 0x80 and frame_function == OVERWORLD_DO_FRAME and wram[CUR_MAP] != OVERWORLD_MAP):
        return 0, SCREEN_W, False
    scx = io[0x43]
    left = max(-extra, -scx)
    right = min(SCREEN_W + extra, wram[MAP_WIDTH] * 8 - scx)
    return min(left, 0), max(right, SCREEN_W), True


def present(state: dict[str, Any], extra: int, limit: int) -> tuple[list[int], tuple[int, int, bool]]:
    frame = render(state, extra, limit)
    left, right, room = viewport(state, extra)
    if not state["io"][0x40] & 0x80:
        return frame, (left, right, room)
    fill = color(state["palette_ram"], 0)
    width = SCREEN_W + 2 * extra
    for ly in range(SCREEN_H):
        base = ly * width + extra
        for x in range(-extra, left):
            frame[base + x] = fill
        for x in range(right, SCREEN_W + extra):
            frame[base + x] = fill
    return frame, (left, right, room)


def center(frame: list[int], extra: int) -> list[int]:
    width = SCREEN_W + 2 * extra
    return [frame[ly * width + extra + x] for ly in range(SCREEN_H) for x in range(SCREEN_W)]


CONTINUOUS_LIMIT = 60000


def reference_states(name: str, masks: list[int], meta: dict[str, Any], frames: int,
                     anchors: list[int]) -> dict[int, dict[str, Any]]:
    padded = (list(masks) + [0] * max(0, frames - len(masks)))[:frames]
    wanted = set(anchors)
    watch = wanted | {a - 1 for a in anchors} | {a + 1 for a in anchors}
    states: dict[int, dict[str, Any]] = {}
    shots: dict[int, bytes] = {}
    link = meta.get("link")
    if link:
        side = int(link["side"])
        members = (name, link["peer"]) if side == 0 else (link["peer"], name)
        cores, pair, _masks = session.linked_pair(members, frames)
        core = cores[side]
    else:
        cores = [refstream.Core(padded, pokes=meta["pokes"], save=meta["save"], printer=meta["printer"])]
        pair = None
        core = cores[0]
    hits = 0

    def on_exec(address: int, _cycle: int) -> None:
        nonlocal hits
        if address != refstream.DOFRAME_ANCHOR:
            return
        hits += 1
        if hits in watch:
            shots[hits] = bytes(core._framebuffer)
        if hits in wanted:
            regions = session.reference_regions(core)
            states[hits] = {
                "wram": regions["wram"], "vram": regions["vram"], "oam": regions["oam"],
                "io": core.io_block(), "palette_ram": core.palette_block(),
            }

    try:
        core.input_axis = "ordinal"
        core.install_exec(on_exec)
        if pair is not None:
            stop = max(anchors) + 1
            session.run_linked(pair, lambda: hits >= stop, frames * refstream.SAMPLES_PER_FRAME)
        else:
            checkpoints = session.checkpoint_directory(name, masks, frames, meta["pokes"], meta["save"],
                                                       meta["printer"])
            spans = [anchors] if len(masks) <= CONTINUOUS_LIMIT else [[a] for a in anchors]
            for span in spans:
                hits = core.seek(checkpoints, min(span) - 1)
                stop = max(span) + 1
                core.run(frames, stop=lambda: hits >= stop)
    finally:
        for member in cores:
            member.close()
    missing = wanted - set(states)
    if missing:
        raise WidescreenError(f"reference never reached ordinals {sorted(missing)[:4]} of {name}")
    for ordinal in anchors:
        state = states[ordinal]
        frame = shots.get(ordinal)
        state["framebuffer"] = frame
        state["stable"] = frame is not None and shots.get(ordinal - 1) == frame and shots.get(ordinal + 1) == frame
    return states


def reference_frame_pixels(raw: bytes) -> list[int]:
    return [value & 0x7FFF for value in struct.unpack(f"<{SCREEN_W * SCREEN_H}I", raw)]


def native_pass(name: str, count: int, anchors: list[int], lag_path: Path, lane: Path,
                extra: list[str], printer: bool) -> tuple[dict[int, dict[str, Any]], bytes, str]:
    mask_path = lane / "mask.txt"
    mask_path.write_text(session.mask_text())
    digest_path = lane / "native.bin"
    state_path, failure, _off = session.run_native(
        lane, session.session_dir(name) / "input.txt", count, lag_path=lag_path,
        digest_out=digest_path, mask_path=mask_path, dump_ordinals=anchors, extra=extra,
        printer_dir=lane / "printer" if printer else None)
    dumps: dict[int, dict[str, Any]] = {}
    for ordinal in anchors:
        path = state_path.with_name(f"{state_path.stem}-f{ordinal}.json")
        if not path.is_file():
            raise WidescreenError(f"native dump missing at ordinal {ordinal} for {name}: {failure[-300:]}")
        dumps[ordinal] = json.loads(path.read_text(encoding="utf-8"))
    return dumps, digest_path.read_bytes() if digest_path.is_file() else b"", failure


def session_row(name: str, scenario: Scenario) -> dict[str, Any]:
    masks, meta = session.load_session(name)
    count = len(masks)
    frames = session.reference_frames(masks, meta)
    report = witness.verify_report(name)
    row: dict[str, Any] = {
        "name": name,
        "ordinals": count,
        "verify": {key: report.get(key) for key in ("status", "confirmed", "schedule_mismatches")},
    }
    failures: list[str] = []
    if report.get("status") != "clean" or report.get("confirmed") != count or report.get("schedule_mismatches"):
        row["status"] = "FAIL"
        row["failures"] = ["4:3 replay is not clean"]
        return row
    anchors = witness.sample_anchors(count, scenario.samples)
    anchors = [a for a in anchors if a < count] or [max(1, count - 1)]
    ref_meta = session.build_reference(name, masks, frames, pokes=meta["pokes"], save=meta["save"],
                                       printer=meta["printer"])
    reference_digests = session.load_reference(ref_meta)
    lag_path = ROOT / ref_meta["directory"] / "lag.txt"
    extra = ["--widescreen", str(WIDE_EXTRA)]
    if scenario.sprite_limit != SPRITES_PER_LINE:
        extra.append("--no-sprite-limits")
    with tempfile.TemporaryDirectory(prefix=f"widescreen-{name}-") as directory:
        lane = Path(directory)
        wide_dir = lane / "wide"
        wide_dir.mkdir()
        dumps, native_digests, failure = native_pass(name, count, anchors + [count], lag_path, wide_dir, extra,
                                                     meta["printer"])
        faithful_save = None
        if "save" in scenario.fields:
            plain_dir = lane / "plain"
            plain_dir.mkdir()
            plain, _digests, _failure = native_pass(name, count, [count], lag_path, plain_dir, [], meta["printer"])
            faithful_save = plain[count].get("save")
    ordinal, reached, regions, _audio = session.first_divergence(reference_digests, native_digests)
    ref_count = len(reference_digests) // session.REFERENCE_RECORD.size
    row["digests"] = {"compared": reached, "reference": ref_count,
                      "first_divergence": ordinal, "regions": regions}
    if ordinal is not None or reached < min(count, ref_count):
        failures.append(f"feature run left the replay at ordinal {ordinal} ({regions}); {failure[-200:]}")
    states = reference_states(name, masks, meta, frames, anchors)
    census = {"anchors": 0, "wide_mismatch": 0, "center_mismatch": 0, "renderer_mismatch": 0,
              "stable": 0, "rooms": 0, "widened": 0, "clamped": 0, "layouts": 0, "rect_mismatch": 0,
              "feature_changed": 0}
    for ordinal in anchors:
        state = states[ordinal]
        dump = dumps[ordinal]
        census["anchors"] += 1
        expected, (left, right, room) = present(state, WIDE_EXTRA, scenario.sprite_limit)
        wide = dump.get("framebuffer_wide")
        if not isinstance(wide, list) or dump.get("wide_width") != SCREEN_W + 2 * WIDE_EXTRA:
            census["wide_mismatch"] += 1
            continue
        if [value & 0x7FFF for value in wide] != expected:
            census["wide_mismatch"] += 1
        if scenario.sprite_limit != SPRITES_PER_LINE and render(state, WIDE_EXTRA, SPRITES_PER_LINE) != render(
                state, WIDE_EXTRA, scenario.sprite_limit):
            census["feature_changed"] += 1
        if list(dump.get("wide_viewport") or []) != [left, right] or bool(dump.get("wide_room")) != room:
            census["rect_mismatch"] += 1
        if scenario.sprite_limit == SPRITES_PER_LINE and center(wide, WIDE_EXTRA) != [v & 0x7FFF for v in dump["framebuffer"]]:
            census["center_mismatch"] += 1
        if state["io"][0x40] & 0x80:
            if room:
                census["rooms"] += 1
                if left < 0 or right > SCREEN_W:
                    census["widened"] += 1
                if left > -WIDE_EXTRA or right < SCREEN_W + WIDE_EXTRA:
                    census["clamped"] += 1
            else:
                census["layouts"] += 1
        if state["stable"] and state["framebuffer"] is not None:
            census["stable"] += 1
            if center(render(state, 0, SPRITES_PER_LINE), 0) != reference_frame_pixels(state["framebuffer"]):
                census["renderer_mismatch"] += 1
    if "save" in scenario.fields:
        wide_save = dumps[count].get("save")
        row["save"] = {"compared": wide_save is not None and faithful_save is not None,
                       "equal": wide_save == faithful_save}
        if wide_save is None or wide_save != faithful_save:
            failures.append("save differs between the 4:3 and the widescreen run")
    for key in ("wide_mismatch", "center_mismatch", "renderer_mismatch", "rect_mismatch"):
        if census[key]:
            failures.append(f"{key}: {census[key]} of {census['anchors']} anchors")
    if not census["stable"]:
        failures.append("no stable anchor to check the renderer against the reference frame")
    runtime = dumps[count].get("runtime", {})
    row["events"] = {"count": int(runtime.get("events", 0)),
                     "observed": witness.event_names(int(runtime.get("event_mask", 0)))}
    row["frames"] = int(runtime.get("frames", 0))
    row["anchors"] = anchors
    row["census"] = census
    row["status"] = "PASS" if not failures else "FAIL"
    if failures:
        row["failures"] = failures
    return row


def run(name: str) -> dict[str, Any]:
    scenario = SCENARIOS[name]
    rows = [session_row(member, scenario) for member in scenario.sessions]
    totals = {key: sum(row.get("census", {}).get(key, 0) for row in rows)
              for key in ("rooms", "widened", "clamped", "layouts")}
    missing = [key for key in scenario.need if not totals.get(key)]
    passed = all(row["status"] == "PASS" for row in rows) and not missing
    fragment: dict[str, Any] = {
        "oracles": ["gambatte", "native"],
        "state_fields": list(scenario.fields),
        "frames": sum(row.get("frames", 0) for row in rows),
        "events": sum(row.get("events", {}).get("count", 0) for row in rows),
        "comparison": {
            "status": "PASS" if passed else "FAIL",
            "axis": "doframe-ordinal",
            "wide_extra": WIDE_EXTRA,
            "sprite_limit": scenario.sprite_limit,
            "totals": totals,
            "sessions": rows,
        },
        "session_sha256": hashlib.sha256(
            json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
    }
    if passed:
        fragment["status"] = "PASS"
        fragment["terminal_event"] = scenario.terminal
    else:
        fragment["status"] = "FAIL"
        fragment["failure"] = "WIDESCREEN_MISMATCH"
        fragment["detail"] = "; ".join(
            [f"{row['name']}: " + "; ".join(row.get("failures") or []) for row in rows if row["status"] != "PASS"]
            + [f"no anchor showed {key}" for key in missing]
        )
    return fragment


def corpus(name: str) -> list[dict[str, str]]:
    return witness.corpus_for(SCENARIOS[name].sessions)


if __name__ == "__main__":
    result = run(sys.argv[1])
    print(json.dumps({key: result[key] for key in ("status", "comparison") if key in result},
                     indent=1, default=str)[:20000])
