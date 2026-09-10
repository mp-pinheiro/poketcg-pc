#!/usr/bin/env python3
"""The static map from card effects to the cards that carry them, and decks
built to make the ROM's AI play a chosen card.

cards.asm gives every attack, trainer and energy card its `EffectCommands`
table; effect_commands.asm gives every table its `EFFECTCMDTYPE_*` command
routines. Inverted, that names the cards a coverage target needs in play; a
deck of four copies of the carrier, its pre-evolutions, the attack's energy and
same-type basics is what `session.py ai-duel --cards` pokes into wPlayerDeck.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PRET = ROOT / "poketcg" / "src"
CARDS = PRET / "data" / "cards.asm"
COMMANDS = PRET / "engine" / "duel" / "effect_commands.asm"
CONSTANTS = PRET / "constants" / "card_constants.asm"
MAP_PATH = ROOT / "build" / "completion" / "effects.json"
DECK_SIZE = 60
COPIES = 4
ENERGY_CARDS = 24
ENERGY_BY_TYPE = {"GRASS": 1, "FIRE": 2, "WATER": 3, "LIGHTNING": 4, "FIGHTING": 5, "PSYCHIC": 6}
DOUBLE_COLORLESS = 7
LABEL = re.compile(r"^(\w+Card):")
COMMAND_LABEL = re.compile(r"^(\w+EffectCommands):")
COMMAND_ROW = re.compile(r"^\s*dbw\s+(EFFECTCMDTYPE_\w+)\s*,\s*(\w+)")


class EffectsError(RuntimeError):
    pass


def card_ids() -> dict[str, int]:
    ids: dict[str, int] = {}
    value = None
    for line in CONSTANTS.read_text().splitlines():
        text = line.split(";", 1)[0].strip()
        if text.startswith("const_def"):
            parts = text.split()
            value = int(parts[1]) if len(parts) > 1 else 0
        elif text.startswith("const ") and value is not None:
            ids[text.split()[1]] = value
            value += 1
    if not ids:
        raise EffectsError(f"no card constants in {CONSTANTS}")
    return ids


def parse_energy(text: str) -> dict[str, int]:
    parts = [part.strip() for part in text.split(None, 1)[1].split(",")] if " " in text else ["0"]
    if parts == ["0"]:
        return {}
    return {parts[index]: int(parts[index + 1]) for index in range(0, len(parts) - 1, 2)}


def parse_cards() -> list[dict[str, Any]]:
    """Every card block of cards.asm: type, id, stage, pre-evolution name and
    the effect table each attack (or the trainer/energy card) points at."""
    ids = card_ids()
    cards: list[dict[str, Any]] = []
    block: list[str] = []
    label = None

    def flush() -> None:
        if label is None or not block:
            return
        body = [line.split(";", 1)[0].strip() for line in block]
        body = [line for line in body if line]
        card: dict[str, Any] = {"label": label, "type": body[0].split()[1], "name": body[2].split()[1],
                                "id": ids[body[5].split()[1]], "id_name": body[5].split()[1]}
        if card["type"].startswith("TYPE_PKMN"):
            card["hp"] = int(body[6].split()[1])
            card["stage"] = body[7].split()[1]
            card["pre_evo"] = body[8].split()[1] if body[8].startswith("tx") else None
            attacks = []
            cursor = 9
            for slot in (1, 2):
                energy = parse_energy(body[cursor])
                name = body[cursor + 1].split()[1] if body[cursor + 1].startswith("tx") else None
                effect = body[cursor + 6].split()[1]
                attacks.append({"slot": slot, "energy": energy, "name": name,
                                "effect": None if effect == "NONE" else effect})
                cursor += 12
            card["attacks"] = attacks
        else:
            effect = body[6].split()[1]
            card["effect"] = None if effect == "NONE" else effect
        cards.append(card)

    for line in CARDS.read_text().splitlines():
        match = LABEL.match(line)
        if match:
            flush()
            label = match.group(1)
            block = []
        elif label is not None:
            block.append(line)
    flush()
    return cards


def parse_commands() -> dict[str, list[tuple[str, str]]]:
    """EffectCommands table -> [(EFFECTCMDTYPE_*, routine)]."""
    tables: dict[str, list[tuple[str, str]]] = {}
    current = None
    for line in COMMANDS.read_text().splitlines():
        match = COMMAND_LABEL.match(line)
        if match:
            current = match.group(1)
            tables[current] = []
            continue
        row = COMMAND_ROW.match(line)
        if row and current is not None:
            tables[current].append((row.group(1), row.group(2)))
    if not tables:
        raise EffectsError(f"no effect command tables in {COMMANDS}")
    return tables


def build_map() -> dict[str, Any]:
    cards = parse_cards()
    tables = parse_commands()
    routines: dict[str, list[dict[str, Any]]] = {}

    def add(table: str | None, card: dict[str, Any], slot: str, attack: str | None) -> None:
        if table is None:
            return
        for kind, routine in tables.get(table, []):
            routines.setdefault(routine, []).append({
                "card": card["id_name"], "id": card["id"], "slot": slot, "attack": attack,
                "table": table, "command": kind,
            })

    for card in cards:
        if card["type"].startswith("TYPE_PKMN"):
            for attack in card["attacks"]:
                add(attack["effect"], card, f"attack{attack['slot']}", attack["name"])
        else:
            add(card["effect"], card, "trainer" if card["type"] == "TYPE_TRAINER" else "energy", None)
    return {
        "schema": 1, "format": "card-effects-v1",
        "cards": len(cards), "tables": len(tables), "routines": len(routines),
        "by_routine": {name: rows for name, rows in sorted(routines.items())},
        "card_data": {card["id_name"]: card for card in cards},
    }


def load_map() -> dict[str, Any]:
    if MAP_PATH.is_file():
        data = json.loads(MAP_PATH.read_text())
        if data.get("format") == "card-effects-v1":
            return data
    data = build_map()
    MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    MAP_PATH.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
    return data


def evolution_chain(card: dict[str, Any], cards: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """The carrier's pre-evolutions, lowest stage first."""
    by_name: dict[str, list[dict[str, Any]]] = {}
    for other in cards.values():
        if other["type"].startswith("TYPE_PKMN"):
            by_name.setdefault(other["name"], []).append(other)
    chain: list[dict[str, Any]] = []
    current = card
    while current.get("pre_evo"):
        candidates = [c for c in by_name.get(current["pre_evo"], [])
                      if c["stage"] in ("BASIC", "STAGE1")]
        if not candidates:
            raise EffectsError(f"{card['id_name']}: no card named {current['pre_evo']} to evolve from")
        current = min(candidates, key=lambda c: (c["stage"] != "BASIC", c["id"]))
        chain.insert(0, current)
    return chain


def build_deck(card_name: str, *, attack_slot: int | None = None) -> list[int]:
    """Sixty card ids in draw order: the evolution chain interleaved with the
    attack's energy first (double colorless for colorless costs), so an
    arranged duel opens with the carrier's basic and powers it up, then the
    remaining copies, energy and same-type basics."""
    data = load_map()
    cards = data["card_data"]
    if card_name not in cards:
        raise EffectsError(f"{card_name} is not a card")
    card = cards[card_name]
    pokemon = card["type"].startswith("TYPE_PKMN")
    chain = (evolution_chain(card, cards) if pokemon else []) + [card]
    energy_types: dict[str, int] = {}
    if pokemon:
        for attack in card["attacks"]:
            if attack_slot is None or attack["slot"] == attack_slot:
                for kind, count in attack["energy"].items():
                    energy_types[kind] = energy_types.get(kind, 0) + count
    card_type = card["type"].removeprefix("TYPE_PKMN_") if pokemon else None
    basic_type = card_type if card_type in ENERGY_BY_TYPE else next(
        (kind for kind in energy_types if kind in ENERGY_BY_TYPE), "FIRE")
    typed = [kind for kind in energy_types if kind in ENERGY_BY_TYPE] or [basic_type]
    energies: list[int] = []
    if energy_types.get("COLORLESS", 0):
        energies += [DOUBLE_COLORLESS] * COPIES
    while len(energies) < ENERGY_CARDS:
        for kind in typed:
            if len(energies) < ENERGY_CARDS:
                energies.append(ENERGY_BY_TYPE[kind])
    fillers = sorted((c for c in cards.values()
                      if c["type"] == f"TYPE_PKMN_{basic_type}" and c["stage"] == "BASIC"
                      and c["id"] not in {stage["id"] for stage in chain}),
                     key=lambda c: (c["hp"], c["id"]))
    pending = list(energies)
    opening: list[int] = [chain[0]["id"]] if pokemon else [fillers[0]["id"], card["id"], card["id"]]
    for stage in chain[1:]:
        opening += [pending.pop(0), stage["id"]]
    while len(opening) < 7 and pending:
        opening.append(pending.pop(0))
    deck: list[int] = list(opening)
    if pokemon and fillers:
        deck.append(fillers[0]["id"])
    for stage in chain:
        for _ in range(COPIES - opening.count(stage["id"])):
            deck.append(stage["id"])
            if pending:
                deck.append(pending.pop(0))
    deck += pending
    for filler in fillers:
        if len(deck) >= DECK_SIZE:
            break
        deck += [filler["id"]] * min(COPIES - deck.count(filler["id"]), DECK_SIZE - len(deck))
    if len(deck) != DECK_SIZE:
        raise EffectsError(f"{card_name}: built {len(deck)} cards, not {DECK_SIZE}")
    return deck


def carriers(routine: str) -> list[dict[str, Any]]:
    data = load_map()
    rows = data["by_routine"].get(routine)
    if not rows:
        raise EffectsError(f"{routine} is not a card effect routine")
    cards = data["card_data"]
    ranked = sorted(rows, key=lambda row: (
        row["slot"] == "trainer", row["slot"] == "energy",
        cards[row["card"]].get("stage") != "BASIC",
        cards[row["card"]].get("hp", 0) * -1, row["id"]))
    return ranked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("map", help="rebuild build/completion/effects.json and print its totals")
    carriers_parser = sub.add_parser("carriers", help="the cards carrying an effect routine")
    carriers_parser.add_argument("routine")
    deck_parser = sub.add_parser("deck", help="write a 60-card deck file for a carrier card")
    deck_parser.add_argument("card", help="card constant, e.g. EKANS")
    deck_parser.add_argument("--attack", type=int, choices=(1, 2))
    deck_parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "map":
            MAP_PATH.unlink(missing_ok=True)
            data = load_map()
            print(f"EFFECTS cards={data['cards']} tables={data['tables']} routines={data['routines']} "
                  f"map={MAP_PATH.relative_to(ROOT)}")
            return 0
        if args.command == "carriers":
            for row in carriers(args.routine):
                print(f"CARRIER {row['card']} id={row['id']} slot={row['slot']} attack={row['attack']} "
                      f"command={row['command']}")
            return 0
        deck = build_deck(args.card, attack_slot=args.attack)
        text = "\n".join(str(card) for card in deck) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text)
            print(f"DECK {args.card} cards={len(deck)} out={args.out}")
        else:
            sys.stdout.write(text)
        return 0
    except (EffectsError, OSError, ValueError, KeyError, IndexError) as exc:
        print(json.dumps({"status": "FAIL", "detail": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
