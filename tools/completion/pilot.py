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
    peek               print the player's tile, facing and map, and every loaded
                       NPC's tile, so a walk can be aimed instead of guessed
    duel               play the player's side of the current duel from WRAM until
                       it ends: attach an energy the active Pokemon's first attack
                       needs, attack with the first affordable attack, otherwise
                       end the turn; text boxes, knockouts and the bench prompt are
                       answered from the routine the ROM is waiting in

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
from bisect import bisect_right
import ctypes
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
        elif verb == "peek" and len(parts) == 1:
            steps.append(("peek", 0, ""))
        elif verb == "duel" and len(parts) == 1:
            steps.append(("duel", 0, ""))
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


# wram.asm: wPlayerXCoord/wPlayerYCoord ($D330/$D331, in tiles), wPlayerDirection
# ($D334, NORTH..WEST), wCurMap ($D32F), wLoadedNPCs ($D34A: 8 entries of 12
# bytes, id at +0, x/y tiles at +2/+3, direction at +4).
DIRECTIONS = ("north", "east", "south", "west")


def peek(core: refstream.Core) -> str:
    read = core.library.gambatte_cpuread
    at = lambda address: read(core.core, address)  # noqa: E731
    facing = DIRECTIONS[at(0xD334) & 3]
    lines = [f"player x={at(0xD330)} y={at(0xD331)} facing={facing} map={at(0xD32F)}"]
    for slot in range(8):
        base = 0xD34A + slot * 12
        npc = at(base)
        if npc == 0:
            continue
        lines.append(f"npc[{slot}] id={npc} x={at(base + 2)} y={at(base + 3)} facing={DIRECTIONS[at(base + 4) & 3]}")
    return "\n".join(lines)


# The duel, read straight from WRAM (wram.asm `duel_vars`, constants/duel_constants.asm
# and card_data_constants.asm). Card data comes from the ROM's CardPointers table.
PLAYER_VARS = 0xC200
CARD_LOCATIONS, HAND, ARENA_CARD, ARENA_CARD_HP = 0x00, 0x42, 0xBB, 0xC8
NUMBER_OF_CARDS_IN_HAND, NUMBER_OF_POKEMON_IN_PLAY_AREA = 0xEE, 0xEF
LOCATION_HAND, LOCATION_ARENA = 0x01, 0x10
PLAYER_DECK = 0xC400
DUEL_FINISHED, ALREADY_PLAYED_ENERGY, CUR_MENU_ITEM, DUEL_TURNS = 0xCC07, 0xCC0B, 0xCD10, 0xCC06
WHOSE_TURN, BANK_ROM = 0xFF97, 0xFF80
CARD_POINTERS_BANK, CARD_POINTERS = 0x0C, 0x4C5C
CARD_TYPE, ATTACK1_COST, ATTACK1_DAMAGE, ATTACK2_COST, ATTACK2_DAMAGE = 0x00, 0x0C, 0x16, 0x1F, 0x29
TYPE_ENERGY_FIRE, TYPE_ENERGY_DOUBLE_COLORLESS, TYPE_TRAINER = 0x08, 0x0E, 0x10
COLORS = ("fire", "grass", "lightning", "water", "fighting", "psychic")
# Where the ROM is when it waits for the player, by the routine that called
# DoFrame (poketcg.sym), and what the policy presses there.
PROMPTS = {
    "PrintDuelMenuAndHandleInput": "menu",
    "DisplayCardList": "hand",
    "HandleDuelMenuInput": "hand",
    "DisplayPlayAreaScreen": "play-area",
    "SelectAttackFromMenu": "attack",
    "WaitForWideTextBoxInput": "text",
    "DrawWideTextBox_WaitForInput": "text",
    "WaitForButtonAorB": "text",
    "HandleYesOrNoMenu": "yes-no",
    "YesOrNoMenuWithText": "yes-no",
    "DisplayDrawNCardsScreen": "text",
    "DuelMainInterface": "text",
    "MainDuelLoop": "text",
}


class DuelReader:
    def __init__(self, core: refstream.Core) -> None:
        self.core = core
        self.read = core.library.gambatte_cpuread
        self.rom = bytes(core._rom_buffer)
        labels = [(bank, address, name) for bank, address, name in refstream.load_labels()
                  if "." not in name]
        self.labels = {}
        for bank, address, name in labels:
            self.labels.setdefault(bank, []).append((address, name))
        for rows in self.labels.values():
            rows.sort()
        self.registers = (ctypes.c_int * 10)()

    def at(self, address: int) -> int:
        return self.read(self.core.core, address)

    def var(self, offset: int) -> int:
        return self.at(PLAYER_VARS + offset)

    def rom_byte(self, bank: int, address: int) -> int:
        return self.rom[bank * 0x4000 + (address - 0x4000)]

    def card(self, card_id: int) -> dict:
        entry = CARD_POINTERS + 2 * card_id
        pointer = self.rom_byte(CARD_POINTERS_BANK, entry) | (self.rom_byte(CARD_POINTERS_BANK, entry + 1) << 8)
        data = lambda offset: self.rom_byte(CARD_POINTERS_BANK, pointer + offset)  # noqa: E731
        kind = data(CARD_TYPE)
        attacks = []
        if kind < TYPE_ENERGY_FIRE:
            for cost, damage in ((ATTACK1_COST, ATTACK1_DAMAGE), (ATTACK2_COST, ATTACK2_DAMAGE)):
                packed = [data(cost + i) for i in range(4)]
                need = {"fire": packed[0] >> 4, "grass": packed[0] & 15, "lightning": packed[1] >> 4,
                        "water": packed[1] & 15, "fighting": packed[2] >> 4, "psychic": packed[2] & 15,
                        "colorless": packed[3] >> 4}
                if any(need.values()):
                    attacks.append({"need": need, "damage": data(damage)})
        return {"id": card_id, "type": kind, "attacks": attacks}

    def temp_list(self) -> list[int]:
        """wDuelTempList: the deck indices a card list screen shows, in order."""
        listed = []
        for offset in range(60):
            index = self.at(0xC510 + offset)
            if index == 0xFF:
                break
            listed.append(index)
        return listed

    def hand(self) -> list[int]:
        count = self.var(NUMBER_OF_CARDS_IN_HAND)
        return [self.var(HAND + i) for i in range(count)]

    def attached(self, location: int) -> dict:
        energy = {color: 0 for color in COLORS}
        energy["colorless"] = 0
        for index in range(60):
            if self.var(CARD_LOCATIONS + index) != LOCATION_ARENA + location:
                continue
            kind = self.card(self.at(PLAYER_DECK + index))["type"]
            if TYPE_ENERGY_FIRE <= kind < TYPE_ENERGY_DOUBLE_COLORLESS:
                energy[COLORS[kind - TYPE_ENERGY_FIRE]] += 1
            elif kind == TYPE_ENERGY_DOUBLE_COLORLESS:
                energy["colorless"] += 2
        return energy

    @staticmethod
    def affordable(need: dict, have: dict) -> bool:
        spare = 0
        for color in COLORS:
            if have[color] < need[color]:
                return False
            spare += have[color] - need[color]
        return spare + have["colorless"] >= need["colorless"]

    def waiting_in(self) -> str:
        """The routine that called DoFrame: the first ROM return address above
        DoFrame's four pushes, resolved through the mapped bank."""
        self.core.library.gambatte_getregs(self.core.core, self.registers)
        sp = self.registers[1] & 0xFFFF
        bank = self.at(BANK_ROM)
        for offset in range(8, 40, 2):
            address = self.at(sp + offset) | (self.at(sp + offset + 1) << 8)
            if 0x0150 <= address < 0x8000:
                rows = self.labels.get(0 if address < 0x4000 else bank, [])
                index = bisect_right(rows, (address, "\uffff")) - 1
                if index >= 0:
                    return rows[index][1]
        return "?"

    def describe(self, waiting: str) -> str:
        turn = "player" if self.at(WHOSE_TURN) == 0xC2 else "opponent"
        lines = [f"duel turn={self.at(DUEL_TURNS)} whose={turn} finished={self.at(DUEL_FINISHED)} "
                 f"energy_played={self.at(ALREADY_PLAYED_ENERGY)} waiting_in={waiting}"]
        for slot in range(self.var(NUMBER_OF_POKEMON_IN_PLAY_AREA)):
            index = self.var(ARENA_CARD + slot)
            card = self.card(self.at(PLAYER_DECK + index))
            have = self.attached(slot)
            costs = " ".join(f"atk{n}={a['damage']}:{sum(a['need'].values())}" for n, a in enumerate(card["attacks"], 1))
            lines.append(f"slot{slot} deck={index} card={card['id']:#04x} hp={self.var(ARENA_CARD_HP + slot)} "
                         f"energy={sum(have.values())} {costs}")
        hand = " ".join(f"{index}:{self.card(self.at(PLAYER_DECK + index))['id']:#04x}" for index in self.hand())
        lines.append(f"hand deck:card = {hand}")
        return "\n".join(lines)


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
        self.reader: DuelReader | None = None
        self.waiting = "?"
        self.core.install_exec(self._on_exec)
        self.reader = DuelReader(self.core)
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
            # The CPU is inside DoFrame right now; by the frame's end it is not.
            self.waiting = self.reader.waiting_in() if self.reader is not None else "?"
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


A, B, RIGHT, LEFT, UP, DOWN = 0x10, 0x20, 0x01, 0x02, 0x04, 0x08
# wCurrentDuelMenuItem: 0 HAND, 2 CHECK, 4 RETREAT on the top row; 1 ATTACK,
# 3 PKMN POWER, 5 DONE below (core.asm DuelMenuFunctionTable; up/down flips the
# low bit, left/right steps by two).
MENU_HAND, MENU_ATTACK, MENU_DONE = 0, 1, 5
CURRENT_DUEL_MENU_ITEM, LIST_SCROLL_OFFSET = 0xCBC6, 0xCD19
TEXT_PROMPTS = {"WaitForWideTextBoxInput", "DrawWideTextBox_WaitForInput", "WaitForButtonAorB",
                "DisplayDrawNCardsScreen", "DuelMainInterface", "MainDuelLoop", "DoFrameIfLCDEnabled"}
YES_NO_PROMPTS = {"HandleYesOrNoMenu", "YesOrNoMenuWithText"}


def menu_press(current: int, target: int) -> int:
    """One d-pad press toward `target` on the duel menu, or A when there."""
    if current == target:
        return A
    if (current & 1) != (target & 1):
        return DOWN
    return RIGHT if (target >> 1) > (current >> 1) else LEFT


def play_duel(driver: "Driver", max_actions: int = 1200) -> None:
    """Drive the player's side of the duel from WRAM until wDuelFinished. One
    press per DoFrame prompt; the goal for the turn is re-read from the state
    each time the duel menu comes back."""
    reader = driver.reader
    goal: tuple | None = None
    failed_attaches: set[int] = set()
    seen: dict[str, int] = {}
    for _ in range(max_actions):
        if reader.at(DUEL_FINISHED) != 0:
            print(f"duel: finished at ordinal {len(driver.masks)} turns={reader.at(DUEL_TURNS)}")
            return
        driver.idle()
        where = driver.waiting
        key = (f"{where}:{reader.describe(where)}:{goal}:"
               f"{reader.at(CUR_MENU_ITEM)}:{reader.at(LIST_SCROLL_OFFSET)}:{reader.at(CURRENT_DUEL_MENU_ITEM)}")
        seen[key] = seen.get(key, 0) + 1
        if seen[key] >= 4:
            screenshot(driver.core, SHOTS / "duel-stuck.png")
            raise SystemExit(f"duel: the same prompt four times in {where} (goal {goal}); "
                             f"see build/completion/pilot/duel-stuck.png\n{reader.describe(where)}")
        press = A
        if reader.at(WHOSE_TURN) != 0xC2:
            goal = None
        elif where == "PrintDuelMenuAndHandleInput":
            if goal is not None and goal[0] == "attach":
                if reader.at(ALREADY_PLAYED_ENERGY) == 0:
                    failed_attaches.add(goal[1])
                goal = None
            if goal is None:
                goal = decide_turn(reader, failed_attaches)
                print(f"duel: ordinal {len(driver.masks)} turn {reader.at(DUEL_TURNS)} goal {goal}")
            target = {"attach": MENU_HAND, "attack": MENU_ATTACK, "done": MENU_DONE}[goal[0]]
            press = menu_press(reader.at(CURRENT_DUEL_MENU_ITEM), target)
        elif where == "DisplayCardList":
            # The list shows wDuelTempList's order, which is the hand sorted by
            # id when the player turned sorting on; the goal names the card.
            listed = reader.temp_list()
            if goal is None or goal[0] != "attach" or goal[1] not in listed:
                press = B
            else:
                wanted = listed.index(goal[1])
                current = reader.at(LIST_SCROLL_OFFSET) + reader.at(CUR_MENU_ITEM)
                press = A if current == wanted else (DOWN if current < wanted else UP)
        elif where == "CardListItemSelectionMenu":
            press = A if goal is not None and goal[0] == "attach" else B
        elif where == "DisplayPlayAreaScreen":
            press = A
        elif where == "DuelMenu_Attack":
            if goal is None or goal[0] != "attack":
                press = B
            else:
                current = reader.at(CUR_MENU_ITEM)
                press = A if current == goal[1] else (DOWN if current < goal[1] else UP)
                if press == A:
                    goal = ("attacked",)
        elif where in YES_NO_PROMPTS:
            press = LEFT if reader.at(CUR_MENU_ITEM) != 0 else A
        elif where in TEXT_PROMPTS:
            press = A
        else:
            print(f"duel: ordinal {len(driver.masks)} unknown prompt in {where}, pressing A")
        driver.step(press)
        driver.step(0)
    raise SystemExit(f"duel: {max_actions} actions without the duel ending")


def decide_turn(reader: DuelReader, failed_attaches: set[int]) -> tuple:
    """An energy the active's first attack still needs, else the first
    affordable attack, else DONE."""
    if reader.var(NUMBER_OF_POKEMON_IN_PLAY_AREA) == 0:
        return ("done",)
    active = reader.card(reader.at(PLAYER_DECK + reader.var(ARENA_CARD)))
    have = reader.attached(0)
    for number, attack in enumerate(active["attacks"]):
        if reader.affordable(attack["need"], have):
            return ("attack", number)
    if reader.at(ALREADY_PLAYED_ENERGY) == 0 and active["attacks"]:
        need = active["attacks"][0]["need"]
        for index in reader.hand():
            if index in failed_attaches:
                continue
            kind = reader.card(reader.at(PLAYER_DECK + index))["type"]
            if not TYPE_ENERGY_FIRE <= kind <= TYPE_ENERGY_DOUBLE_COLORLESS:
                continue
            color = COLORS[kind - TYPE_ENERGY_FIRE] if kind < TYPE_ENERGY_DOUBLE_COLORLESS else "colorless"
            if color == "colorless" or need[color] > have[color] or need["colorless"] > 0:
                return ("attach", index)
    return ("done",)


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
            elif verb == "peek":
                print(f"peek: ordinal {len(driver.masks)}\n{peek(driver.core)}")
                print(driver.reader.describe(driver.waiting))
            elif verb == "duel":
                play_duel(driver)
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
