POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC,
          "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hWhoseTurn = 0xFF97
CARD = 0xC100  # stand-in for wLoadedCard1
LOCATION = 0xC200  # player duel variables page

wAttackAnimationIsPlaying = 0xCE7E
wUnused_DefendingPkmnStatus = 0xCCC5
wDefendingWasForcedToSwitch = 0xCCEF
wDealtDamage = 0xCCBF
wNoEffectFromWhichStatus = 0xCCF1
wLoadedAttackName = 0xCCAA
wTxRam2 = 0xCE3F
wLoadedAttackAnimation = 0xCCB8

PLAYER_ARENA = 0xC200
OPP_ARENA  = 0xC300
wPlayerArenaCardLastTurnStatus = 0xC2F5
wOpponentArenaCardLastTurnStatus = 0xC3F5
wWhoseTurn = 0xCC05
wStatusConditionQueueIndex = 0xCCCD
wStatusConditionQueue = 0xCCCE
wNoDamageOrEffect = 0xCCC7
wIsDamageToSelf = 0xCCE6
wPlayerArenaCardStatus = 0xC2F0
wOpponentArenaCardStatus = 0xC3F0
hTempPlayAreaLocation_ff9d = 0xFF9D
wPlayerDeck = 0xC400
wOpponentDeck = 0xC480
wPlayerArenaCard = 0xC2BB
wOpponentArenaCard = 0xC3BB
wPlayerArenaCardStage = 0xC2CE
wOpponentArenaCardStage = 0xC3CE
wAllStagesIndices = 0xCCCA
wLoadedCard2 = 0xCC65
wLoadedCard2Type = 0xCC65
wLoadedCard2Stage = 0xCC6E
hBankROM = 0xFF80




CONTRACT = {
    "ConvertSpecialTrainerCardToPokemon": ("a", "b", "c", "d", "e", "hl"),
    "ResetAttackAnimationIsPlaying": ("b", "c", "d", "e", "hl"),
    "ClearNonTurnTemporaryDuelvars": ("b", "c", "d", "e"),
    "ClearNonTurnTemporaryDuelvars_CopyStatus": ("b", "c", "d", "e"),
    "UpdateArenaCardLastTurnDamage": ("b", "c", "d", "e"),
    "PrintThereWasNoEffectFromStatusText": ("b", "d", "e", "hl"),
    "WaitAttackAnimation": ("b", "c", "d", "e", "hl"),
    "ApplyStatusConditionQueue": ("f",),
    "GetCardOneStageBelow": ("a", "d", "e", "hl", "f"),
}

CASES = {
    "ConvertSpecialTrainerCardToPokemon": [
        {"a": 0, "hl": CARD, "d": 0, "e": 0,
         "wram": {CARD: b"\x06", hWhoseTurn: b"\xC2"},
         "read": {CARD: 1}},
        {"a": 1, "hl": CARD, "d": 0, "e": 0,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 1: b"\x00"},
         "read": {CARD: 1}},
        {"a": 1, "hl": CARD, "d": 0x01, "e": 0x02,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 1: b"\x10"},
         "read": {CARD: 1}},
        {"a": 2, "hl": CARD, "d": 0x00, "e": 0xCC,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 2: b"\x10"},
         "read": {CARD: 64}},
        {"a": 3, "hl": CARD, "d": 0x00, "e": 0xCB,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 3: b"\x10"},
         "read": {CARD: 64}},
        {"a": 4, "hl": CARD, "d": 0x02, "e": 0xCC,
         "wram": {CARD: b"\x10", hWhoseTurn: b"\xC2", LOCATION + 4: b"\x10"},
         "read": {CARD: 1}},
        dict(POISON, a=0, hl=CARD, d=0x00, e=0x01,
             wram={CARD: b"\x06", hWhoseTurn: b"\xC2"}, read={CARD: 1}),
    ],

    "ResetAttackAnimationIsPlaying": [
        # all-zero: verify wAttackAnimationIsPlaying is zeroed
        {"wram": {wAttackAnimationIsPlaying: b"\xFF"},
         "read": {wAttackAnimationIsPlaying: 1}},
        # poisoned: hWhoseTurn=PLAYER (C2) for bank setup
        dict(POISON,
             wram={wAttackAnimationIsPlaying: b"\x01", hWhoseTurn: b"\xC2"},
             read={wAttackAnimationIsPlaying: 1}),
    ],

    "ClearNonTurnTemporaryDuelvars": [
        # all-zero: non-turn(O2) = OPP(C3), 8 bytes at C3F2 are zeroed
        {"wram": {hWhoseTurn: b"\xC2",
                  OPP_ARENA + 0xF2: b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"},
         "read": {OPP_ARENA + 0xF2: 8}},
        # poisoned: non-turn(O2) = PLAYER(C2) since hWhoseTurn=OPP
        dict(POISON,
             wram={hWhoseTurn: b"\xC3",
                   PLAYER_ARENA + 0xF2: b"\x01\x02\x03\x04\x05\x06\x07\x08"},
             read={PLAYER_ARENA + 0xF2: 8}),
    ],

    "ClearNonTurnTemporaryDuelvars_CopyStatus": [
        # all-zero: non-turn OPP, status F0 is read then 8 bytes at F2 cleared
        {"wram": {hWhoseTurn: b"\xC2",
                  OPP_ARENA + 0xF0: b"\xAB",
                  OPP_ARENA + 0xF2: b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"},
         "read": {wUnused_DefendingPkmnStatus: 1, OPP_ARENA + 0xF2: 8}},
        # poisoned: non-turn PLAYER since hWhoseTurn=OPP
        dict(POISON,
             wram={hWhoseTurn: b"\xC3",
                   PLAYER_ARENA + 0xF0: b"\xCD",
                   PLAYER_ARENA + 0xF2: b"\x01\x02\x03\x04\x05\x06\x07\x08"},
             read={wUnused_DefendingPkmnStatus: 1, PLAYER_ARENA + 0xF2: 8}),
    ],

    "UpdateArenaCardLastTurnDamage": [
        # wDefendingWasForcedToSwitch==0: writes wDealtDamage to OPP F3-F4
        {"wram": {hWhoseTurn: b"\xC2",
                  wDefendingWasForcedToSwitch: b"\x00",
                  wDealtDamage: b"\x34\x12",  # little-endian: 0x1234
                  OPP_ARENA + 0xF3: b"\xFF\xFF"},
         "read": {OPP_ARENA + 0xF3: 2}},
        # wDefendingWasForcedToSwitch!=0: writes 0,0 to PLAYER F3-F4
        {"wram": {hWhoseTurn: b"\xC3",
                  wDefendingWasForcedToSwitch: b"\x01",
                  wDealtDamage: b"\xAB\xCD",
                  PLAYER_ARENA + 0xF3: b"\xFF\xFF"},
         "read": {PLAYER_ARENA + 0xF3: 2}},
        # poisoned: wDefendingWasForcedToSwitch==0, damage is zero
        dict(POISON,
             wram={hWhoseTurn: b"\xC2",
                   wDefendingWasForcedToSwitch: b"\x00",
                   wDealtDamage: b"\x00\x00",
                   OPP_ARENA + 0xF3: b"\xFF\xFF"},
             read={OPP_ARENA + 0xF3: 2}),
    ],

    "PrintThereWasNoEffectFromStatusText": [
        # status==0: loads attack name, returns TX_RAM2 text, writes to wTxRam2
        {"wram": {wNoEffectFromWhichStatus: b"\x00",
                  wLoadedAttackName: b"\x34\x12",  # name id 0x1234
                  wTxRam2: b"\xFF\xFF"},
         "read": {wTxRam2: 2}},
        # status==POISONED|CONFUSED (0x81): poison/confusion text
        {"wram": {wNoEffectFromWhichStatus: b"\x81"},
         "read": {}},
        # status==POISONED (0x80): poison text
        {"wram": {wNoEffectFromWhichStatus: b"\x80"},
         "read": {}},
        # status==DOUBLE_POISONED (0xC0): toxic text
        {"wram": {wNoEffectFromWhichStatus: b"\xC0"},
         "read": {}},
        # status==PARALYZED (0x03): paralysis text
        {"wram": {wNoEffectFromWhichStatus: b"\x03"},
         "read": {}},
        # status==ASLEEP (0x02): sleep text
        {"wram": {wNoEffectFromWhichStatus: b"\x02"},
         "read": {}},
        # status==CONFUSED (0x01): confusion text
        {"wram": {wNoEffectFromWhichStatus: b"\x01"},
         "read": {}},
        # poisoned: POISONED|CONFUSED
        dict(POISON,
             wram={wNoEffectFromWhichStatus: b"\x81"},
             read={}),
    ],
    "ApplyStatusConditionQueue": [
        {
            "name": "empty queue clears last-turn statuses",
            "wram": {
                wPlayerArenaCardLastTurnStatus: b"\xff",
                wOpponentArenaCardLastTurnStatus: b"\xff",
                wStatusConditionQueueIndex: b"\x00",
            },
            "read": {
                wPlayerArenaCardLastTurnStatus: 1,
                wOpponentArenaCardLastTurnStatus: 1,
            },
            "expect_regs": {"f": 0x80},
        },
        {
            "name": "poisoned apply-one-record sets carry",
            **POISON,
            "wram": {
                wStatusConditionQueueIndex: b"\x03",
                wStatusConditionQueue: b"\xc2\x00\x02",
                wPlayerArenaCardStatus: b"\xf1",
                wPlayerArenaCardLastTurnStatus: b"\xff",
                wOpponentArenaCardLastTurnStatus: b"\xff",
            },
            "read": {
                wStatusConditionQueue + 3: 1,
                wPlayerArenaCardStatus: 1,
                wPlayerArenaCardLastTurnStatus: 1,
                wOpponentArenaCardLastTurnStatus: 1,
            },
            "expect_regs": {"f": 0x90},
        },
        {
            "name": "no-damage-or-effect applies only own side",
            "wram": {
                wNoDamageOrEffect: b"\x80",
                wWhoseTurn: b"\xc2",
                wStatusConditionQueueIndex: b"\x06",
                wStatusConditionQueue: b"\xc2\x00\x04" + b"\xc3\x00\x08",
                wPlayerArenaCardStatus: b"\xf1",
                wOpponentArenaCardStatus: b"\xe2",
                wPlayerArenaCardLastTurnStatus: b"\xff",
                wOpponentArenaCardLastTurnStatus: b"\xff",
            },
            "read": {
                wPlayerArenaCardStatus: 1,
                wOpponentArenaCardStatus: 1,
                wPlayerArenaCardLastTurnStatus: 1,
                wOpponentArenaCardLastTurnStatus: 1,
                wNoDamageOrEffect: 1,
                wStatusConditionQueue + 6: 1,
            },
            "expect_regs": {"f": 0x80},
        },
        {
            "name": "maximum queue all eight records applied",
            "wram": {
                wStatusConditionQueueIndex: b"\x18",
                wStatusConditionQueue:
                    b"\xc2\x00\x01"
                    + b"\xc3\x00\x02"
                    + b"\xc2\x00\x04"
                    + b"\xc3\x00\x08"
                    + b"\xc2\x00\x10"
                    + b"\xc3\x00\x20"
                    + b"\xc2\x00\x40"
                    + b"\xc3\x00\x80",
                wPlayerArenaCardStatus: b"\x00",
                wOpponentArenaCardStatus: b"\x00",
                wPlayerArenaCardLastTurnStatus: b"\xff",
                wOpponentArenaCardLastTurnStatus: b"\xff",
            },
            "read": {
                wStatusConditionQueue: 24,
                wIsDamageToSelf: 1,
            },
            "expect_regs": {"f": 0x90},
        },
    ],

}

CASES["GetCardOneStageBelow"] = [
    {
        "name": "all-zero basic card returns early with carry",
        "a": 0, "d": 0, "e": 0, "hl": 0, "f": 0,
        "wram": {
            hBankROM: b"\x01",
            hWhoseTurn: b"\xC2",
            hTempPlayAreaLocation_ff9d: b"\x00",
            wPlayerArenaCard: b"\x00",
            LOCATION: b"\x10",
            wPlayerDeck: b"\x08",
        },
        "read": {
            wLoadedCard2Stage: 1,
        },
    },
    {
        "name": "poisoned stage-1 card returns basic index",
        **POISON,
        "wram": {
            hBankROM: b"\x01",
            hWhoseTurn: b"\xC2",
            hTempPlayAreaLocation_ff9d: b"\x00",
            wPlayerArenaCard: b"\x01",
            wPlayerArenaCardStage: b"\x01",
            LOCATION: b"\x10\x10",
            wPlayerDeck: b"\x08\x09",
        },
        "read": {
            wLoadedCard2: 64,
            wAllStagesIndices: 3,
        },
    },
    {
        "name": "stage-2 filters energy and returns stage-1",
        "a": 0, "d": 0, "e": 0, "hl": 0, "f": 0,
        "wram": {
            hBankROM: b"\x01",
            hWhoseTurn: b"\xC2",
            hTempPlayAreaLocation_ff9d: b"\x00",
            wPlayerArenaCard: b"\x02",
            wPlayerArenaCardStage: b"\x02",
            LOCATION: b"\x10\x10\x10\x10",
            wPlayerDeck: b"\x08\x09\x0a\x01",
        },
        "read": {
            wLoadedCard2: 64,
            wAllStagesIndices: 3,
        },
    },
    {
        "name": "stage-2 without stage-1 returns 0xFF",
        "a": 0, "d": 0, "e": 0, "hl": 0, "f": 0,
        "wram": {
            hBankROM: b"\x01",
            hWhoseTurn: b"\xC2",
            hTempPlayAreaLocation_ff9d: b"\x00",
            wPlayerArenaCard: b"\x01",
            wPlayerArenaCardStage: b"\x02",
            LOCATION: b"\x10\x10",
            wPlayerDeck: b"\x08\x0a",
        },
        "read": {
            wLoadedCard2: 64,
            wAllStagesIndices: 3,
        },
    },
    {
        "name": "opponent page stage-1 card",
        **POISON,
        "wram": {
            hBankROM: b"\x01",
            hWhoseTurn: b"\xC3",
            hTempPlayAreaLocation_ff9d: b"\x00",
            wOpponentArenaCard: b"\x01",
            wOpponentArenaCardStage: b"\x01",
            OPP_ARENA: b"\x10\x10",
            wOpponentDeck: b"\x08\x09",
        },
        "read": {
            wLoadedCard2: 64,
            wAllStagesIndices: 3,
        },
    },
    {
        "name": "60-entry scan finds card at last index",
        "a": 0, "d": 0, "e": 0, "hl": 0, "f": 0,
        "wram": {
            hBankROM: b"\x01",
            hWhoseTurn: b"\xC2",
            hTempPlayAreaLocation_ff9d: b"\x00",
            wPlayerArenaCard: b"\x3B",
            wPlayerArenaCardStage: b"\x01",
            LOCATION: b"\x00" * 59 + b"\x10",
            wPlayerDeck: b"\x00" * 59 + b"\x09",
        },
        "read": {
            wLoadedCard2: 64,
            wAllStagesIndices: 3,
        },
    },
]


ACTIVE_ANIM = 0xD42A
WD4C0_ANIM = 0xD4C0
QUEUE_ANIM = 0xD423
ALL_FF_ANIM = {ACTIVE_ANIM: b"\xff", WD4C0_ANIM: b"\xff", QUEUE_ANIM: b"\xff" * 7}
HPAD_REPEAT = 0xFF8D

CASES["WaitAttackAnimation"] = [
    {"wram": {wLoadedAttackAnimation: b"\x00"}},
    dict(POISON, wram={wLoadedAttackAnimation: b"\x00"}),
    dict(POISON,
         wram={wLoadedAttackAnimation: b"\x01",
               **ALL_FF_ANIM,
               HPAD_REPEAT: b"\x00\x00\x00\x00\x00"},
         keys=0x01,
         read={HPAD_REPEAT: 5, ACTIVE_ANIM: 1, WD4C0_ANIM: 1, QUEUE_ANIM: 7}),
]
