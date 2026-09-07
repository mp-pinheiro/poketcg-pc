#!/usr/bin/env python3
"""Extend a session by playing the reference from a script.

A session is one input byte per DoFrame. The movie sessions are exhausted (the
5530S route ends in the Duel Escape glitch) and a human recording needs a
human, so this drives the reference core itself: it replays an existing
session's input, then appends steps from a script, and writes the new
session's `input.txt` plus a screenshot at every step so the route can be
checked by eye before the port is asked to follow it.

Script lines, one step each (`#` comments allowed):

    press A            press A for one DoFrame, then release for one
    hold DOWN 12       hold DOWN for 12 DoFrames
    wait 30            release everything for 30 DoFrames
    idle               release everything until the ROM has been waiting for
                       input: 150 DoFrames in a row whose WRAM, under the session
                       mask plus the cursor-blink counters, did not change
    shot name          write build/completion/pilot/<name>.png of the screen now

`idle` is what makes a route robust: a text box that prints for 70 frames and a
menu that opens in 3 both settle before the next press, so the script names
presses, not frame counts.

Buttons: A B SELECT START RIGHT LEFT UP DOWN, joined with `+` (`B+LEFT`).
Masks are the session byte layout (hKeysHeld nibble-swapped).

    pilot.py --from first-duel --script route.txt --out tests/sessions/lab-pc

The script is kept next to the session it produced (`route.txt`) so the route
can be re-derived or extended.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "completion"))

import refstream
import session

BUTTONS = {"A": 0x10, "B": 0x20, "SELECT": 0x40, "START": 0x80,
           "RIGHT": 0x01, "LEFT": 0x02, "UP": 0x04, "DOWN": 0x08}
SHOTS = ROOT / "build" / "completion" / "pilot"


def parse_mask(text: str) -> int:
    mask = 0
    for name in text.upper().split("+"):
        if name not in BUTTONS:
            raise SystemExit(f"unknown button {name!r}")
        mask |= BUTTONS[name]
    return mask


def parse_script(path: Path) -> list[tuple[str, int, str]]:
    steps: list[tuple[str, int, str]] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        verb = parts[0].lower()
        if verb == "press" and len(parts) == 2:
            steps.append(("hold", parse_mask(parts[1]), ""))
            steps.append(("wait", 1, ""))
        elif verb == "hold" and len(parts) == 3:
            steps.append(("hold", parse_mask(parts[1]), parts[2]))
        elif verb == "wait" and len(parts) == 2:
            steps.append(("wait", int(parts[1]), ""))
        elif verb == "shot" and len(parts) == 2:
            steps.append(("shot", 0, parts[1]))
        elif verb == "idle" and len(parts) == 1:
            steps.append(("idle", 0, ""))
        else:
            raise SystemExit(f"{path}:{number}: cannot parse {raw!r}")
    return steps


IDLE_RUN = 150
# WRAM that moves while the ROM waits for a press, on top of the session
# mask: the OAM shadow, VBlank/timer/play-time counters and the RNG
# ($CAB8-$CACD), the three cursor-blink counters, and the overworld's sprite
# animation state and decompression scratch ($D200-$D560).
IDLE_EXTRA_MASK = ((0xCA00, 0xCAA0), (0xCAB8, 0xCACE), (0xCD04, 0xCD05), (0xCD0F, 0xCD10),
                   (0xCEA3, 0xCEA4), (0xD200, 0xD560))


def write_png(path: Path, pixels: bytes, width: int, height: int) -> None:
    raw = b"".join(b"\x00" + pixels[y * width * 3:(y + 1) * width * 3] for y in range(height))

    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body) & 0xFFFFFFFF)

    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def screenshot(core: refstream.Core, path: Path) -> None:
    frame = bytes(core._framebuffer)  # the core exposes no reader
    rgb = bytearray()
    for index in range(refstream.WIDTH * refstream.HEIGHT):
        pixel = int.from_bytes(frame[index * 4:index * 4 + 4], "little")
        rgb += bytes(((pixel >> 16) & 0xFF, (pixel >> 8) & 0xFF, pixel & 0xFF))
    path.parent.mkdir(parents=True, exist_ok=True)
    write_png(path, bytes(rgb), refstream.WIDTH, refstream.HEIGHT)


class Driver:
    """Runs the reference one DoFrame at a time under script control."""

    def __init__(self, base_masks: list[int], budget: int) -> None:
        self.masks = list(base_masks)
        self.core = refstream.Core([0] * budget)
        self.core.input_axis = "ordinal"
        self.core.override_mask = 0
        self.budget = budget
        self.frame = 0
        self.pending: dict[int, str] = {}
        self.taken: dict[int, str] = {}
        self._anchor = False
        self.core.install_exec(self._on_exec)
        table = bytearray(0x2000)
        for start, end in session.mask_ranges()["wram"]:
            for index in range(max(0, start), min(0x2000, end)):
                table[index] = 1
        for start, end in IDLE_EXTRA_MASK:
            for index in range(start - 0xC000, end - 0xC000):
                table[index] = 1
        self.keep = bytes(1 - b for b in table)

    def _on_exec(self, address: int, _cycle: int) -> None:
        if address == refstream.DOFRAME_ANCHOR:
            self._anchor = True
            name = self.pending.pop(self.core.ordinal, None)
            if name is not None:
                screenshot(self.core, SHOTS / f"{name}.png")
                self.taken[self.core.ordinal] = name

    def step(self, mask: int) -> None:
        """Advance to the next DoFrame anchor with `mask` held."""
        self.core.override_mask = mask
        self.masks.append(mask)
        self._anchor = False
        while not self._anchor:
            if self.frame >= self.budget:
                raise SystemExit(f"the reference stopped polling after {self.core.ordinal} DoFrames")
            self.core.frame = self.frame
            self.core.step_frame()
            self.frame += 1

    def replay(self, masks: list[int]) -> None:
        for mask in masks:
            self.step(mask)

    def digest(self) -> bytes:
        wram = self.core.area("WRAM")[:0x2000]
        return bytes(a & k for a, k in zip(wram, self.keep))

    def idle(self) -> int:
        last = self.digest()
        stable = 0
        waited = 0
        while stable < IDLE_RUN:
            self.step(0)
            waited += 1
            current = self.digest()
            stable = stable + 1 if current == last else 0
            last = current
            if waited > 4000:
                raise SystemExit(f"never idle after {waited} DoFrames at ordinal {self.core.ordinal}")
        return waited

    def close(self) -> None:
        self.core.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="base", required=True, help="session to extend")
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="new session directory")
    parser.add_argument("--goal", default="")
    parser.add_argument("--base-ordinals", type=int, help="use only the first N inputs of the base session")
    args = parser.parse_args(argv)

    base_masks, _meta = session.load_session(args.base)
    if args.base_ordinals is not None:
        base_masks = base_masks[:args.base_ordinals]
    steps = parse_script(args.script)
    driver = Driver([], budget=(len(base_masks) + 80000) * 2 + 400)
    try:
        driver.replay(base_masks)
        start = len(driver.masks)
        for verb, value, extra in steps:
            if verb == "hold":
                for _ in range(int(extra) if extra else 1):
                    driver.step(value)
            elif verb == "wait":
                for _ in range(value):
                    driver.step(0)
            elif verb == "idle":
                waited = driver.idle()
                print(f"idle: {waited} DoFrames, now at ordinal {len(driver.masks)}")
            elif verb == "shot":
                screenshot(driver.core, SHOTS / f"{extra}.png")
                print(f"shot {extra}: ordinal {len(driver.masks)} -> {SHOTS / (extra + '.png')}")
        masks = driver.masks
    finally:
        driver.close()
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "input.txt").write_text("\n".join(str(m) for m in masks) + "\n", encoding="utf-8")
    print(f"wrote {args.out / 'input.txt'}: {len(masks)} DoFrames ({len(masks) - start} new)")
    if args.goal:
        session.record_meta(args.out.name, args.goal)
    return 0


if __name__ == "__main__":
    sys.exit(main())
