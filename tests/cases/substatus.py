POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hTempCardIndex_ff98_ADDR = 0xFF98
hTempPlayAreaLocation_ff9d_ADDR = 0xFF9D
hWhoseTurn = 0xFF97
wGotHeads = 0xCC0A
ARENA_SUBSTATUS2 = 0xC200 + 0xE8  # player page, duelvar $E8
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480

ARENA_SUBSTATUS1 = 0xC200 + 0xE7
ARENA_SUBSTATUS3 = 0xC200 + 0xEB
ARENA_STATUS = 0xC200 + 0xF0
ARENA_DISABLED_ATK = 0xC200 + 0xF2
ARENA_CARD = 0xC200 + 0xBB
BENCH = 0xC200 + 0xBC
ARENA_CHANGED_TYPE = 0xC200 + 0xD4
OPP_SUBSTATUS2 = 0xC300 + 0xE8
OPP_ARENA_CARD = 0xC300 + 0xBB
OPP_BENCH = 0xC300 + 0xBC
OPP_CHANGED_TYPE = 0xC300 + 0xD4

wNoDamageOrEffect = 0xCCC7
wLoadedAttackCategory = 0xCCB1
wTempNonTurnDuelistCardID = 0xCCC4
wTempTurnDuelistCardID = 0xCCC3
wIsDamageToSelf = 0xCCE6
wSelectedAttack = 0xCCC6
wLoadedCard1RetreatCost = 0xCC56

POKEMON_POWER = 0x04
MUK = 0x27
DODRIO = 0xB6
OMANYTE = 0x5C
BLASTOISE = 0x43
AERODACTYL = 0x8D
MR_MIME = 0x9B
KABUTO = 0x8B
MEW_LV8 = 0xA0
GRIMER = 0x26  # a real Basic (stage 0) card, for the Neutralizing Shield check

PLAYER_TURN = {hWhoseTurn: b"\xC2"}
BENCH_DONE = {BENCH: b"\xff", OPP_BENCH: b"\xff"}


def mw(*dicts):
    out = {}
    for d in dicts:
        out.update(d)
    return out


CONTRACT = {
    "CheckSandAttackOrSmokescreenSubstatus": {
        "compare": ("a", "b", "c", "d", "e", "f", "hl"),
        "preserve": ("b", "c"),
    },
    "CountTurnDuelistPokemonWithActivePkmnPower": {
        "compare": ("a", "b", "c", "d", "e", "f", "hl"),
        "preserve": (),
    },
    "CountPokemonWithActivePkmnPowerInBothPlayAreas": {
        "compare": ("a", "b", "c", "d", "e", "f", "hl"),
        "preserve": (),
    },
    "CheckIsIncapableOfUsingPkmnPower": {
        "compare": ("f", "hl", "b", "c", "d", "e"),
        "preserve": (),
    },
    "CheckIsIncapableOfUsingPkmnPower_ArenaCard": {
        "compare": ("f", "hl", "b", "c", "d", "e"),
        "preserve": (),
    },
    "HandleDoubleDamageSubstatus": {
        "compare": ("b", "c", "d", "e"),
        "preserve": ("b", "c"),
    },
    "HandleDamageReductionExceptSubstatus2": {
        "compare": ("d", "e"),
        "preserve": (),
    },
    "HandleDamageReduction": {
        "compare": ("d", "e"),
        "preserve": (),
    },
    "HandleCantAttackSubstatus": {
        "compare": ("f", "hl", "b", "c", "d", "e"),
        "preserve": ("b", "c", "d", "e"),
    },
    "HandleAmnesiaSubstatus": {
        "compare": ("f", "hl", "b", "c", "d", "e"),
        "preserve": ("b", "c", "d", "e"),
    },
    "HandleNoDamageOrEffectSubstatus": {
        "compare": ("f", "e", "hl", "b", "c"),
        "preserve": (),
    },
    "CheckNoDamageOrEffect": {
        "compare": ("f", "hl", "b", "c"),
        "preserve": ("b", "c"),
    },
    "IsClairvoyanceActive": {
        "compare": ("a", "f", "b", "c", "d", "e", "hl"),
        "preserve": (),
    },
    "GetLoadedCard1RetreatCost": {
        "compare": ("a",),
        "preserve": (),
    },
    "CheckUnableToRetreatDueToEffect": {
        "compare": ("f", "hl", "b", "c", "d", "e"),
        "preserve": ("b", "c", "d", "e"),
    },
    "CheckCantUseTrainerDueToEffect": {
        "compare": ("f", "hl", "b", "c", "d", "e"),
        "preserve": ("b", "c", "d", "e"),
    },
    "IsPrehistoricPowerActive": {
        "compare": ("a", "f", "hl", "b", "c", "d", "e"),
        "preserve": (),
    },
    "ClearDamageReductionSubstatus2": {
        "compare": (),
        "preserve": (),
    },
    "UpdateSubstatusConditions_StartOfTurn": {
        "compare": (),
        "preserve": (),
    },
    "UpdateSubstatusConditions_EndOfTurn": {
        "compare": (),
        "preserve": (),
    },
    "IsRainDanceActive": {
        "compare": ("a", "f", "b", "c", "d", "e"),
        "preserve": (),
    },
    "CheckRainDanceScenario": {
        "compare": ("a", "f"),
        "preserve": (),
    },
    "ClearChangedTypesIfMuk": {
        "compare": (),
        "preserve": (),
    },
    "HandleStrikesBack_AgainstDamagingAttack": {
        "compare": ("a", "b", "c", "d", "e", "f", "hl"),
        "preserve": (),
    },
}

CASES = {
    "CheckSandAttackOrSmokescreenSubstatus": [
        # No substatus: a = 0, Z set, de untouched.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x00"}},
        # Sand attack, got tails: carry set, a = 0, de = $00DE.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x02", wGotHeads: b"\x00"}},
        # Sand attack, got heads: a = heads, no carry, de = $00DE.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x02", wGotHeads: b"\x01"}},
        # Smokescreen, got tails: carry set, de = $00DF.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x01", wGotHeads: b"\x00"}},
        # Smokescreen, got heads: a = heads, de = $00DF.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x01", wGotHeads: b"\x01"}},
        # Unrelated substatus value: a = it, no carry, de untouched.
        {"wram": {hWhoseTurn: b"\xC2", ARENA_SUBSTATUS2: b"\x03"}},
        # Poisoned: opponent's turn reads the $C3 page.
        dict(POISON, wram={hWhoseTurn: b"\xC3", 0xC300 + 0xE8: b"\x00"}),
    ],
    # Count id $01 across arena ($C2BB) and bench ($C2BC+): MUK = $C3, DODRIO = $C5.
    "CountTurnDuelistPokemonWithActivePkmnPower": [
        # Arena only, no status: 1 found.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
        # Arena + two bench slots: 3 found.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             wPlayerDeck: b"\x01",
                             0xC2BC: b"\x00\x00\xff"},
         "read": {0xCE7C: 1}},
        # Arena asleep (status $01): skipped.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2F0: b"\x01",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
        # Arena paralyzed (status $08): skipped too.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC2F0: b"\x08",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
        # No match: 0 found, no carry.
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff"}},
    ],
    "CountPokemonWithActivePkmnPowerInBothPlayAreas": [
        # Player arena has 1; opponent arena has 1 (opponent deck $C480): total 2.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00",
                             0xC3BB: b"\x00",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff",
                             0xC480: b"\x01", 0xC3BC: b"\xff"}},
        # Player only: total 1. Opponent bench terminated.
        {"a": 0x01, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\x00", 0xC3BB: b"\xff",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff",
                             0xC480: b"\x01", 0xC3BC: b"\xff"},
         "read": {0xCE7C: 1}},
        # Neither: 0. Both benches terminated.
        {"a": 0x02, "wram": {hWhoseTurn: b"\xC2", 0xC2BB: b"\xff", 0xC3BB: b"\xff",
                             wPlayerDeck: b"\x01", 0xC2BC: b"\xff",
                             0xC480: b"\x01", 0xC3BC: b"\xff"},
         "read": {0xCE7C: 1}},
    ],
    "CheckIsIncapableOfUsingPkmnPower": [
        # a=0 (arena), status confused ($01, in CNF_SLP_PRZ): incapable via status.
        {"a": 0x00, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_STATUS: b"\x01"})},
        # a=0, status clear, no Muk anywhere: capable.
        {"a": 0x00, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_STATUS: b"\x00"})},
        # a=0, status clear, Muk on the turn holder's own arena.
        {"a": 0x00, "wram": mw(PLAYER_TURN, BENCH_DONE,
                               {ARENA_CARD: b"\x00", wPlayerDeck: bytes([MUK])})},
        # a=1 (bench slot): the status check is skipped even though status is set.
        {"a": 0x01, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_STATUS: b"\x01"})},
        # a=1, Muk on the opponent's arena.
        {"a": 0x01, "wram": mw(PLAYER_TURN, BENCH_DONE,
                               {OPP_ARENA_CARD: b"\x00", wOpponentDeck: bytes([MUK])})},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "CheckIsIncapableOfUsingPkmnPower_ArenaCard": [
        {"wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_STATUS: b"\x08"})},  # paralyzed
        {"wram": mw(PLAYER_TURN, BENCH_DONE)},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "HandleDoubleDamageSubstatus": [
        # Flag set, de = 0: `ret z` skips the shift, de stays 0.
        {"d": 0x00, "e": 0x00, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: b"\x01"})},
        # Flag set, de != 0: doubled.
        {"d": 0x12, "e": 0x34, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: b"\x01"})},
        # Flag clear: unchanged regardless of de.
        {"d": 0x12, "e": 0x34, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: b"\x00"})},
        # Boundary: doubling $8000 wraps to $0000.
        {"d": 0x80, "e": 0x00, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: b"\x01"})},
        dict(POISON, wram=mw(PLAYER_TURN, {ARENA_SUBSTATUS3: b"\x01"})),
    ],
    "HandleDamageReductionExceptSubstatus2": [
        # wNoDamageOrEffect set: zeroed unconditionally.
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {wNoDamageOrEffect: b"\x01"})},
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x0f])})},  # NO_DAMAGE_STIFFEN
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x1e])})},  # REDUCE_BY_10
        # Boundary: damage below the subtracted amount wraps (bug-compatible with real hardware).
        {"d": 0x00, "e": 0x05, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x1e])})},
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x13])})},  # REDUCE_BY_20
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x0e])})},  # PREVENT_LESS_THAN_40, >= 40
        {"d": 0x00, "e": 0x27, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x0e])})},  # 39 -> zeroed
        {"d": 0x00, "e": 0x28, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x0e])})},  # 40 -> unchanged
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x15])})},  # HALVE_DAMAGE, odd
        {"d": 0x00, "e": 0x02, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x15])})},  # HALVE_DAMAGE, even
        # No SUBSTATUS1, incapable of Pkmn Power: unchanged.
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_STATUS: b"\x01"})},
        # No SUBSTATUS1, capable, attack is itself a Pkmn Power: unchanged.
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {wLoadedAttackCategory: bytes([POKEMON_POWER])})},
        # Defender MR_MIME, damage < 30: unchanged.
        {"d": 0x00, "e": 0x0a, "wram": mw(PLAYER_TURN, BENCH_DONE, {wTempNonTurnDuelistCardID: bytes([MR_MIME])})},
        # Defender MR_MIME, damage == 30 (boundary): zeroed.
        {"d": 0x00, "e": 0x1e, "wram": mw(PLAYER_TURN, BENCH_DONE, {wTempNonTurnDuelistCardID: bytes([MR_MIME])})},
        # Defender KABUTO: same buggy halve as SUBSTATUS1_HALVE_DAMAGE.
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {wTempNonTurnDuelistCardID: bytes([KABUTO])})},
        # Defender is neither: unchanged.
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {wTempNonTurnDuelistCardID: bytes([0x01])})},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "HandleDamageReduction": [
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {OPP_SUBSTATUS2: b"\x00"})},
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {OPP_SUBSTATUS2: bytes([0x03])})},  # REDUCE_BY_20
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {OPP_SUBSTATUS2: bytes([0x07])})},  # POUNCE
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {OPP_SUBSTATUS2: bytes([0x12])})},  # GROWL
        {"d": 0x00, "e": 0x64, "wram": mw(PLAYER_TURN, BENCH_DONE, {OPP_SUBSTATUS2: bytes([0x01])})},  # unrelated
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "HandleCantAttackSubstatus": [
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: b"\x00"})},
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x05])})},  # TAIL_WAG
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x06])})},  # LEER
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x0b])})},  # BONE_ATTACK
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x01])})},  # unrelated
        dict(POISON, wram=PLAYER_TURN),
    ],
    "HandleAmnesiaSubstatus": [
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: b"\x00"})},
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x01])})},  # not Amnesia
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x04]),
                                                 ARENA_DISABLED_ATK: bytes([0x02]),
                                                 wSelectedAttack: bytes([0x02])})},  # match
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x04]),
                                                 ARENA_DISABLED_ATK: bytes([0x02]),
                                                 wSelectedAttack: b"\x00"})},  # mismatch, selected = 0
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x04]),
                                                 ARENA_DISABLED_ATK: bytes([0x02]),
                                                 wSelectedAttack: bytes([0x03])})},  # mismatch, selected != 0
        dict(POISON, wram=PLAYER_TURN),
    ],
    "HandleNoDamageOrEffectSubstatus": [
        # Attack is itself a Pkmn Power: e/hl pass through, wNoDamageOrEffect forced to 0.
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE,
             {wLoadedAttackCategory: bytes([POKEMON_POWER]), wNoDamageOrEffect: b"\x03"})},
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x0d])})},  # FLY
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x14])})},  # BARRIER
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_SUBSTATUS1: bytes([0x0c])})},  # AGILITY
        # None of the three, incapable of Pkmn Power: e/hl left at the Agility leftover.
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_STATUS: b"\x01"})},
        # Capable, defender id 0 (boundary: the `or a` sets Z).
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE, {wTempNonTurnDuelistCardID: b"\x00"})},
        # Capable, defender != MEW_LV8, nonzero id.
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE, {wTempNonTurnDuelistCardID: bytes([0x01])})},
        # Capable, defender MEW_LV8, damage to self: no shield.
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE,
             {wTempNonTurnDuelistCardID: bytes([MEW_LV8]), wIsDamageToSelf: b"\x01"})},
        # Capable, defender MEW_LV8, attacker is Basic (stage 0): no shield.
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE,
             {wTempNonTurnDuelistCardID: bytes([MEW_LV8]), wTempTurnDuelistCardID: bytes([GRIMER])})},
        # Capable, defender MEW_LV8, attacker is non-Basic (stage 1): Neutralizing Shield triggers.
        {"e": 0x99, "hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE,
             {wTempNonTurnDuelistCardID: bytes([MEW_LV8]), wTempTurnDuelistCardID: bytes([MUK])})},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "CheckNoDamageOrEffect": [
        {"hl": 0x1234, "wram": {wNoDamageOrEffect: b"\x00"}},
        {"hl": 0x1234, "wram": {wNoDamageOrEffect: b"\x81"}},  # bit 7 already set: no text, hl = 0
        {"hl": 0x1234, "wram": {wNoDamageOrEffect: b"\x01"}},  # Agility, doubled offset 0
        {"hl": 0x1234, "wram": {wNoDamageOrEffect: b"\x05"}},  # NShield, table's last entry
        {"hl": 0x1234, "wram": {wNoDamageOrEffect: b"\x03"}},  # Fly, a middle entry
        dict(POISON, wram={wNoDamageOrEffect: b"\x02"}),
    ],
    "IsClairvoyanceActive": [
        {"wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_CARD: b"\x00", wPlayerDeck: bytes([OMANYTE])})},
        {"wram": mw(PLAYER_TURN, BENCH_DONE)},
        {"wram": mw(PLAYER_TURN, BENCH_DONE, {OPP_ARENA_CARD: b"\x00", wOpponentDeck: bytes([MUK])})},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "GetLoadedCard1RetreatCost": [
        {"wram": mw(PLAYER_TURN, BENCH_DONE, {wLoadedCard1RetreatCost: b"\x03"})},
        {"wram": mw(PLAYER_TURN, BENCH_DONE,
                    {BENCH: b"\x00\xff", wPlayerDeck: bytes([DODRIO]), wLoadedCard1RetreatCost: b"\x03"})},
        {"wram": mw(PLAYER_TURN, BENCH_DONE,
                    {BENCH: b"\x00\x00\xff", wPlayerDeck: bytes([DODRIO]), wLoadedCard1RetreatCost: b"\x03"})},
        # Boundary: cost < Dodrio count clamps to 0, no borrow wraparound.
        {"wram": mw(PLAYER_TURN, BENCH_DONE,
                    {BENCH: b"\x00\x00\xff", wPlayerDeck: bytes([DODRIO]), wLoadedCard1RetreatCost: b"\x01"})},
        # Dodrio present but Muk blocks every Pkmn Power: cost unchanged.
        {"wram": mw(PLAYER_TURN, BENCH_DONE,
                    {BENCH: b"\x00\xff", wPlayerDeck: bytes([DODRIO]), wLoadedCard1RetreatCost: b"\x03",
                     OPP_ARENA_CARD: b"\x00", wOpponentDeck: bytes([MUK])})},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE, {wLoadedCard1RetreatCost: b"\x05"})),
    ],
    "CheckUnableToRetreatDueToEffect": [
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: b"\x00"})},
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x09])})},  # ACID
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x01])})},  # unrelated
        dict(POISON, wram=PLAYER_TURN),
    ],
    "CheckCantUseTrainerDueToEffect": [
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: b"\x00"})},
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: bytes([0x02])})},  # Headache bit (bit 1) set
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: bytes([0x01])})},  # a different bit set, Headache clear
        dict(POISON, wram=PLAYER_TURN),
    ],
    "IsPrehistoricPowerActive": [
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE)},
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_CARD: b"\x00", wPlayerDeck: bytes([AERODACTYL])})},
        {"hl": 0x1234, "wram": mw(PLAYER_TURN, BENCH_DONE,
             {ARENA_CARD: b"\x00", wPlayerDeck: bytes([AERODACTYL])},
             {OPP_ARENA_CARD: b"\x00", wOpponentDeck: bytes([MUK])})},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "ClearDamageReductionSubstatus2": [
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x03])})},  # REDUCE_BY_20 -> cleared
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x05])})},  # TAIL_WAG -> cleared
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x06])})},  # LEER -> cleared
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x07])})},  # POUNCE -> cleared
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x12])})},  # GROWL -> cleared
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x01])})},  # unrelated -> left alone
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS2: b"\x00"})},
        dict(POISON, wram=mw(PLAYER_TURN, {ARENA_SUBSTATUS2: bytes([0x05])})),
    ],
    "UpdateSubstatusConditions_StartOfTurn": [
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS1: bytes([0x19]), ARENA_SUBSTATUS3: b"\x00"})},
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS1: bytes([0x0c]), ARENA_SUBSTATUS3: b"\x00"})},
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS1: b"\x00", ARENA_SUBSTATUS3: bytes([0x02])})},
        # substatus3 already has another bit set: the OR must not clobber it.
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS1: bytes([0x19]), ARENA_SUBSTATUS3: bytes([0x02])})},
        dict(POISON, wram=mw(PLAYER_TURN, {ARENA_SUBSTATUS1: bytes([0x19]), ARENA_SUBSTATUS3: b"\x00"})),
    ],
    "UpdateSubstatusConditions_EndOfTurn": [
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: bytes([0x03]), ARENA_SUBSTATUS2: bytes([0x05]),
                                   ARENA_SUBSTATUS1: b"\x00"})},
        # substatus1 is NEXT_TURN_DOUBLE_DAMAGE: this-turn-double-damage bit is left alone.
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: bytes([0x03]), ARENA_SUBSTATUS2: bytes([0x05]),
                                   ARENA_SUBSTATUS1: bytes([0x19])})},
        {"wram": mw(PLAYER_TURN, {ARENA_SUBSTATUS3: b"\x00", ARENA_SUBSTATUS2: b"\x00",
                                   ARENA_SUBSTATUS1: b"\x00"})},
        dict(POISON, wram=mw(PLAYER_TURN, {ARENA_SUBSTATUS3: bytes([0x03]), ARENA_SUBSTATUS2: bytes([0x05]),
                                            ARENA_SUBSTATUS1: b"\x00"})),
    ],
    "IsRainDanceActive": [
        {"wram": mw(PLAYER_TURN, BENCH_DONE)},
        {"wram": mw(PLAYER_TURN, BENCH_DONE, {ARENA_CARD: b"\x00", wPlayerDeck: bytes([BLASTOISE])})},
        {"wram": mw(PLAYER_TURN, BENCH_DONE,
             {ARENA_CARD: b"\x00", wPlayerDeck: bytes([BLASTOISE])},
             {OPP_ARENA_CARD: b"\x00", wOpponentDeck: bytes([MUK])})},
        dict(POISON, wram=mw(PLAYER_TURN, BENCH_DONE)),
    ],
    "ClearChangedTypesIfMuk": [
        {"a": 0x00, "wram": mw(PLAYER_TURN,
             {wPlayerDeck: bytes([MUK]), ARENA_CHANGED_TYPE: b"\x01\x02\x03\x04\x05\x06",
              OPP_CHANGED_TYPE: b"\x07\x08\x09\x0a\x0b\x0c"})},
        {"a": 0x00, "wram": mw(PLAYER_TURN,
             {wPlayerDeck: bytes([0x01]), ARENA_CHANGED_TYPE: b"\x01\x02\x03\x04\x05\x06",
              OPP_CHANGED_TYPE: b"\x07\x08\x09\x0a\x0b\x0c"})},
        dict(POISON, wram=mw(PLAYER_TURN,
             {wPlayerDeck: bytes([MUK]), ARENA_CHANGED_TYPE: b"\x01\x02\x03\x04\x05\x06",
              OPP_CHANGED_TYPE: b"\x07\x08\x09\x0a\x0b\x0c"})),
    ],
    "CheckRainDanceScenario": [
        {"wram": {hWhoseTurn: bytes((0xC2,)), 0xFF98: b"\x00",
                  wPlayerDeck + 0: b"\x08",
                  0xFF9D: b"\x00",
                  0xC2BB: b"\x00", 0xC2D4: b"\x00"}},
        {"wram": {hWhoseTurn: bytes((0xC2,)), 0xFF98: b"\x00",
                  wPlayerDeck + 0: b"\x03",
                  0xFF9D: b"\x00",
                  0xC2BB: b"\x01", wPlayerDeck + 1: b"\x08", 0xC2D4: b"\x00"}},
        {"wram": {hWhoseTurn: bytes((0xC2,)), 0xFF98: b"\x00",
                  wPlayerDeck + 0: b"\x03",
                  0xFF9D: b"\x00",
                  0xC2BB: b"\x01", wPlayerDeck + 1: b"\x43", 0xC2D4: b"\x00"}},
        dict(POISON, wram={hWhoseTurn: bytes((0xC2,)), 0xFF98: b"\x00",
                           wPlayerDeck + 0: b"\x03",
                           0xFF9D: b"\x00",
                           0xC2BB: b"\x01", wPlayerDeck + 1: b"\x43", 0xC2D4: b"\x00"}),
    ],
}

STRIKES_WRAM = {
    hWhoseTurn: bytes((0xC2,)),
    0xC2BC: b"\xFF",
    0xC3BC: b"\xFF",
    0xCCC4: bytes((0x7F,)),
}
CASES.update({
    "HandleStrikesBack_AgainstDamagingAttack": [
        # de=0 → immediate return, no carry
        {"d": 0, "e": 0, "wram": STRIKES_WRAM},
        # damage to self → return, no carry
        {"d": 0, "e": 10, "wram": {**STRIKES_WRAM, 0xCCE6: b"\x01"}},
        # not MACHAMP → return, no carry
        {"d": 0, "e": 10, "wram": {hWhoseTurn: bytes((0xC2,)), 0xCCC4: b"\x01"}},
        # POKEMON_POWER category → return, no carry
        {"d": 0, "e": 10, "wram": {**STRIKES_WRAM, 0xCCB1: b"\x04"}},
        dict(POISON, d=0, e=0, wram=STRIKES_WRAM),
    ],
})
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)

MUTATIONS = {
    "HandleDoubleDamageSubstatus": {
        "source_symbol": "HandleDoubleDamageSubstatus",
        "before": "de = (uint16_t)(de << 1);",
        "after": "de = (uint16_t)(de >> 1);",
        "case_ids": ["HandleDoubleDamageSubstatus-0", "HandleDoubleDamageSubstatus-1", "HandleDoubleDamageSubstatus-2", "HandleDoubleDamageSubstatus-3", "HandleDoubleDamageSubstatus-4"],
    },
}
