"""Oracle-diff cases for poketcg/src/engine/save.asm (the WRAMToSRAMMapper walkers
and the SRAM<->SRAM2 backup copiers)."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

hBankSRAM = 0xFF81
wNumSRAMValidationErrors = 0xD3C7
wAnimationsDisabled = 0xD421
wTextSpeed = 0xCE47
wEventVars = 0xD3D2
wGeneralSaveDataCheckSum = 0xD3C5
wTempPointer = 0xD4C4
wGeneralSaveDataByteCount = 0xD4C8

# Both walkers keep the running count and checksum in WRAM, not in registers, and
# ValidateGeneralSaveDataFromDE's final header test ORs them straight back out of
# WRAM (save.asm:307-315). wTempPointer is the walk's own source cursor, and the save
# walker deliberately leaves it at $0000 (it stores the terminator word before
# testing it). All three are outputs, so every image case reads them back.
ACCUMULATORS = {wGeneralSaveDataByteCount: 2, wGeneralSaveDataCheckSum: 2,
                wTempPointer: 2}

# wPlayTimeHourMinutes ($D3C8, 3 bytes), wCurOverworldMap ($D3CB) and wMedalCount
# ($D3CC) are contiguous. save.asm:325-341 copies all five out of the payload after the
# error counting, with no branch on the error count.
PLAYTIME_OUT = {0xD3C8: 5}

sGeneralSaveData = 0xB800
sCardCollection = 0xA100
sCardAndDeckSaveDataEnd = 0xB707
sGeneralSaveDataEnd = 0xB900

hBankROM = 0xFF80
sAlbumProgress = 0xB8FE
sBackupGeneralSaveData = 0xB800  # bank 2, same GB address as sGeneralSaveData
wTotalNumCardsCollected = 0xD3CD
wTotalNumCardsToCollect = 0xD3CE
wLoadedEventBits = 0xD3D1
wPCPacks = 0xD11E
wMedalCount = 0xD3CC
wCurOverworldMap = 0xD3CB
wOverworldMapSelection = 0xD32E
wCurMap = 0xD32F
wPlayerXCoord = 0xD330
wPlayerYCoord = 0xD331
wPlayerDirection = 0xD334
wTempMap = 0xD0BB
wTempPlayerXCoord = 0xD0BC
wTempPlayerYCoord = 0xD0BD
wTempPlayerDirection = 0xD0BE
sReceivedLegendaryCards = 0xA00A

ROM_SLOT = 0x556C  # WRAMToSRAMMapper.EmptySRAMSlot, ROM bank 4: always reads 0

# WRAMToSRAMMapper (save.asm:461-497), 35 entries in table order: (WRAM/ROM address,
# byte count, min, max). Cross-checked against the shipped ROM: entry 22's payload
# offset (36) lands exactly on sPCPackSelection ($B82C = $B800 + 8 + 36), and the
# four ROM_SLOT entries' payload offsets land exactly on $B827/$B84C/$B85B/$B86B.
MAPPER = [
    (0xD3CC, 1, 0, 255), (0xD3CB, 1, 0, 255), (0xCAC5, 1, 0, 255), (0xCAC6, 1, 0, 255),
    (0xCAC7, 1, 0, 255), (0xCAC8, 2, 0, 255), (0xD32E, 1, 0, 255), (0xD0BB, 1, 0, 255),
    (0xD0BC, 1, 0, 255), (0xD0BD, 1, 0, 255), (0xD0BE, 1, 0, 255), (0xD0C2, 1, 0, 255),
    (0xD0C3, 1, 0, 255), (0xD0C4, 1, 0, 255), (0xD696, 1, 0, 255), (0xD698, 4, 0, 255),
    (0xD323, 11, 0, 255), (ROM_SLOT, 1, 0, 255), (0xD0B8, 1, 0, 255), (0xD0B9, 1, 0, 255),
    (0xD11B, 1, 0, 255), (0xD0BA, 1, 0, 255), (0xD11D, 1, 0, 14), (0xD11E, 15, 0, 255),
    (0xD111, 1, 0, 255), (0xCAD5, 1, 0, 255), (0xD3B8, 1, 0, 255), (0xD3BB, 10, 0, 255),
    (0xD0C5, 1, 0, 255), (0xD695, 1, 0, 255), (0xD10E, 1, 0, 255), (ROM_SLOT, 15, 0, 255),
    (ROM_SLOT, 16, 0, 255), (ROM_SLOT, 16, 0, 255), (0xD3D2, 64, 0, 255),
]
assert sum(n for _, n, _, _ in MAPPER) == 0xB3

_OFFSETS = []
_o = 0
for _addr, _n, _lo, _hi in MAPPER:
    _OFFSETS.append(_o)
    _o += _n
PAYLOAD_LEN = _o  # 179


def poison_wram(seed=11):
    """Deterministic, distinct, in-range byte(s) per WRAM mapper slot."""
    return {addr: bytes(lo + ((seed + i * 13 + k * 7) % (hi - lo + 1)) for k in range(n))
            for i, (addr, n, lo, hi) in enumerate(MAPPER) if addr != ROM_SLOT}


def payload_from_wram(wram):
    """The 179-byte payload the mapper walk produces from a poison_wram() dict."""
    out = bytearray()
    for addr, n, _lo, _hi in MAPPER:
        out += bytes(n) if addr == ROM_SLOT else bytes(wram[addr])
    return bytes(out)


def header_for(payload):
    checksum = sum(payload) & 0xFFFF
    return bytes([0x08, 0x00, len(payload) & 0xFF, len(payload) >> 8,
                  checksum & 0xFF, checksum >> 8])


def build_image(payload):
    """Header + the 2 never-written/never-checked filler bytes + payload, i.e. the
    full $B800-$B8BA span CopyGeneralSaveDataToSRAM/ValidateGeneralSaveDataFromDE use."""
    return header_for(payload) + b"\x00\x00" + payload


def medal_bits(count):
	return (0xFF << (8 - count) & 0xFF) if count else 0


def event_vars_for(medal_count, ishihara_mentioned=False, legendary=False):
	ev = bytearray((i * 7 + 3) & 0xFF or 1 for i in range(64))
	ev[0] = medal_bits(medal_count)
	if ishihara_mentioned:
		ev[5] |= 0x10
	if legendary:
		ev[6] |= 0x02
	return bytes(ev)


_BASE_WRAM = poison_wram()
_BASE_PAYLOAD = payload_from_wram(_BASE_WRAM)
_VALID_IMAGE = build_image(_BASE_PAYLOAD)

_BAD_CHECKSUM_PAYLOAD = bytearray(_BASE_PAYLOAD)
_BAD_CHECKSUM_PAYLOAD[0] = (_BAD_CHECKSUM_PAYLOAD[0] + 1) & 0xFF  # wMedalCount slot, full 0-255 range
_BAD_CHECKSUM_IMAGE = header_for(_BASE_PAYLOAD) + b"\x00\x00" + bytes(_BAD_CHECKSUM_PAYLOAD)

_PCPACKSEL_OFFSET = _OFFSETS[22]  # wPCPackSelection, min 0 max 14
_BAD_RANGE_PAYLOAD = bytearray(_BASE_PAYLOAD)
_BAD_RANGE_PAYLOAD[_PCPACKSEL_OFFSET] = 15  # one past max; checksum recomputed to stay self-consistent
_BAD_RANGE_IMAGE = build_image(bytes(_BAD_RANGE_PAYLOAD))

# wPCPackSelection set to exactly its max of 14. The max compare exits through
# `jr z, .next_byte`, so equality is not an error; no other image reaches 14.
_AT_MAX_PAYLOAD = bytearray(_BASE_PAYLOAD)
_AT_MAX_PAYLOAD[_PCPACKSEL_OFFSET] = 14
_AT_MAX_IMAGE = build_image(bytes(_AT_MAX_PAYLOAD))

# Header count one short of the 179 the mapper actually walks, leaving a non-zero
# byte-count residue for the header test to OR in.
_BAD_COUNT_IMAGE = (bytes([0x08, 0x00, 178, 0x00]) + header_for(_BASE_PAYLOAD)[4:]
                    + b"\x00\x00" + _BASE_PAYLOAD)

# $556C quirk image: non-zero bytes across all four ROM_SLOT-destined spans (the
# 4 mapper entries whose destination is .EmptySRAMSlot, $556C - inside the MBC5
# RAM-bank-select window). wEventVars (the final entry) is seeded distinctly in
# every SRAM bank, so its post-call WRAM content pins whichever bank the $556C
# writes actually left selected - matching real hardware only if gb_write8 below
# $8000 decodes as an MBC5 register write instead of being dropped.
_QUIRK_PAYLOAD = bytearray(_BASE_PAYLOAD)
_rom_slot_indices = [i for i, (a, n, lo, hi) in enumerate(MAPPER) if a == ROM_SLOT]
for k, idx in enumerate(_rom_slot_indices):
    n = MAPPER[idx][1]
    off = _OFFSETS[idx]
    _QUIRK_PAYLOAD[off:off + n] = bytes(((k + 1) * 17 + j) & 0xFF or 1 for j in range(n))
_QUIRK_IMAGE = build_image(bytes(_QUIRK_PAYLOAD))
_WEVENT_ADDR = sGeneralSaveData + 8 + _OFFSETS[34]
_WEVENT_BANK_PATTERNS = {
    0: bytes((0x10 + k) & 0xFF for k in range(64)),
    1: bytes((0x40 + k * 3) & 0xFF for k in range(64)),
    2: bytes((0x80 + k * 5) & 0xFF for k in range(64)),
    3: bytes((0xC0 + k * 7) & 0xFF for k in range(64)),
}

_CARD_PATTERN = bytes((i * 17 + 3) & 0xFF for i in range(5639))

# Same-shape image for sBackupGeneralSaveData (bank 2, GB address $B800 too), used
# by the two validators' bank-selection and error-count coverage.
_VALID_BACKUP_IMAGE = _VALID_IMAGE
_INVALID_HEADER_BACKUP_IMAGE = bytes([0x08 ^ 0xFF, 0x00 ^ 0xFF]) + _VALID_IMAGE[2:]

# 2 errors: header checksum/count from the base payload paired with the
# out-of-range payload, so both the residue check (mismatched checksum) and the
# explicit wPCPackSelection range check fire.
_MULTI_ERROR_IMAGE = header_for(_BASE_PAYLOAD) + b"\x00\x00" + bytes(_BAD_RANGE_PAYLOAD)

_P0_COLLECTION = bytes((i * 3 + 5) & 0xFF for i in range(256))
_P2_COLLECTION = bytes((i * 7 + 11) & 0xFF for i in range(256))

CONTRACT = {
    # Preserved per save.asm:94-96/133/146-148 (push hl,bc,de,de.../pop hl,de,bc,hl);
    # a/f are scratch throughout with no top-level push af, so excluded.
    "CopyGeneralSaveDataToSRAM": ("b", "c", "d", "e", "hl"),
    # Preserved per save.asm:219-221/324/342-343 (push hl,bc,de.../pop de,bc,hl); a/f scratch.
    "ValidateGeneralSaveDataFromDE": ("b", "c", "d", "e", "hl"),
    # Preserved per save.asm:381-382 (outer) and 391-393/445-447 (inner .LoadData); a/f scratch.
    "LoadGeneralSaveDataFromDE": ("b", "c", "d", "e", "hl"),
    # hl/bc are consumed inputs, not preserved outputs; de is never touched at all.
    "WriteDataToBackup": ("d", "e"),
    "LoadDataFromBackup": ("d", "e"),
    "WriteBackupGeneralSaveData": ("d", "e"),
    "WriteBackupCardAndDeckSaveData": ("d", "e"),
    "LoadBackupGeneralSaveData": ("d", "e"),
    "LoadBackupCardAndDeckSaveData": ("d", "e"),
    # hl is explicitly push/pop-preserved (save.asm:5,24); a/f are scratch, no top pop af.
    "InvalidateSaveData": ("hl",),
    # de/hl are the de argument and hl, both push/pop-preserved around the whole body
    # (save.asm:74-75/79/87-88); a/f scratch.
    "UpdateAlbumProgress": ("d", "e", "hl"),
    # de push/pop-preserved (save.asm:347/353); hl never touched.
    "LoadAlbumProgressFromSRAM": ("d", "e"),
    # de/hl push/pop-preserved (save.asm:359-360/368-369); a/f scratch.
    "LoadBackupSaveData": ("d", "e", "hl"),
    # de push/pop-preserved (save.asm:373/376); hl never touched.
    "_LoadGeneralSaveData": ("d", "e"),
    # b,c,d,e,hl push/pop-preserved (save.asm:531-533/552-554); a is a consumed input,
    # not an output (both passes reload it from wCardToAddToCollection); f scratch.
    "_AddCardToCollectionAndUpdateAlbumProgress": ("b", "c", "d", "e", "hl"),
    # de push/pop-preserved (save.asm:184/196); a/f are the real outputs of the
    # trailing `ld a,[wNumSRAMValidationErrors] / cp 1`.
    "ValidateBackupGeneralSaveData": ("a", "f", "d", "e"),
    "_ValidateGeneralSaveData": ("a", "f", "d", "e"),
    # push hl/bc + de saved/restored across the farcalls and CopyGeneralSaveDataToSRAM
    # (save.asm:53-54/56/61-64/66-67); a/f scratch, set by the farcalls then clobbered.
    "SaveGeneralSaveDataFromDE": ("b", "c", "d", "e", "hl"),
    # de push/pop-preserved (save.asm:42/48); a/b/c/hl/f all clobbered by the callees.
    "_SaveGeneralSaveData": ("d", "e"),
    # de push/pop-preserved (save.asm:31/38); a/b/c/hl/f clobbered by the callees.
    "SaveAndBackupData": ("d", "e"),
    # de preserved through SaveAndBackupData (save.asm:526); c is the consumed branch
    # input (save.asm:507-509). a/b/c/hl/f clobbered.
    "_SaveGame": ("d", "e"),
    # Same trampoline shape as SaveGeneralSaveData; identical contract to the callee.
    "SaveGeneralSaveData": ("d", "e"),
    "LoadGeneralSaveData": ("d", "e"),
    "ValidateGeneralSaveData": ("a", "f", "d", "e"),
    "AddCardToCollectionAndUpdateAlbumProgress": ("b", "c", "d", "e", "hl"),
    # push af/bc/de/hl wraps the farcall (save.asm:20-29), so every entry register
    # is restored regardless of what _SaveGame(0) does internally.
    "SaveGame": ("a", "f", "b", "c", "d", "e", "hl"),
}

CASES = {
    "CopyGeneralSaveDataToSRAM": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        # Round trip half 1: poisoned WRAM sources -> full $B800-$B8BA span.
        {"d": 0xB8, "e": 0x00,
         "wram": {a: d for a, d in _BASE_WRAM.items()},
         "sram": {0: {sGeneralSaveData: bytes(187)}},
         "read": {sGeneralSaveData: 187, **ACCUMULATORS}},
    ],
    "ValidateGeneralSaveDataFromDE": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        # Checksum is actually checked: valid image -> 0 errors, one flipped payload
        # byte (still in-range) -> exactly 1 error.
        {"d": 0xB8, "e": 0x00,
         "sram": {0: {sGeneralSaveData: _VALID_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1, **ACCUMULATORS, **PLAYTIME_OUT}},
        {"d": 0xB8, "e": 0x00,
         "sram": {0: {sGeneralSaveData: _BAD_CHECKSUM_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1, **ACCUMULATORS, **PLAYTIME_OUT}},
        # Range check is actually reached: wPCPackSelection pushed to 15 (max is 14),
        # checksum kept self-consistent so this is the *only* violation. The play-time,
        # medal and map copies are read back here too: the asm makes them
        # unconditionally, after the error counting, so they must land even at errors>0.
        {"d": 0xB8, "e": 0x00,
         "sram": {0: {sGeneralSaveData: _BAD_RANGE_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1, **ACCUMULATORS, **PLAYTIME_OUT}},
        # `jr z, .next_byte` on the max compare means v == max is NOT an error. The
        # base payload puts 12 in wPCPackSelection and the range case puts 15, so
        # without exactly 14 the asm's z-branch is never taken.
        {"d": 0xB8, "e": 0x00,
         "sram": {0: {sGeneralSaveData: _AT_MAX_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1, **ACCUMULATORS, **PLAYTIME_OUT}},
        # Every image above carries the true count 179, so the byte-count residue is 0
        # and its two OR terms in the header test are dead. A header claiming 178
        # leaves a non-zero residue and is the only case that exercises them.
        {"d": 0xB8, "e": 0x00,
         "sram": {0: {sGeneralSaveData: _BAD_COUNT_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1, **ACCUMULATORS, **PLAYTIME_OUT}},
    ],
    "LoadGeneralSaveDataFromDE": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        # Round trip half 2: an image built from the same poisoned WRAM sources
        # loads back to all 31 distinct WRAM targets plus the two settings bytes.
        {"d": 0xB8, "e": 0x00,
         "sram": {0: {sGeneralSaveData: build_image(_BASE_PAYLOAD)}},
         "read": {**{a: n for a, n, _lo, _hi in MAPPER if a != ROM_SLOT},
                  wAnimationsDisabled: 1, wTextSpeed: 1, wTempPointer: 2}},
        # The $556C quirk: non-zero EmptySRAMSlot-destined bytes retarget the MBC5
        # RAM bank mid-walk, so wEventVars (the trailing entry) is read out of
        # whichever bank that left selected - each bank seeded with a distinct,
        # oracle-verifiable pattern.
        {"d": 0xB8, "e": 0x00,
         "sram": {3: {_WEVENT_ADDR: _WEVENT_BANK_PATTERNS[3]},
                  2: {_WEVENT_ADDR: _WEVENT_BANK_PATTERNS[2]},
                  1: {_WEVENT_ADDR: _WEVENT_BANK_PATTERNS[1]},
                  0: {sGeneralSaveData: _QUIRK_IMAGE, **{_WEVENT_ADDR: _WEVENT_BANK_PATTERNS[0]}}},
         "read": {wEventVars: 64}},
    ],
    "WriteDataToBackup": [
        # hl=bc=0: the post-test loop's zero-means-65536-iterations boundary. This
        # exceeds the oracle's 240-frame budget (two BankswitchSRAM calls per
        # iteration), so it is proven against the C alone. hBankSRAM is seeded to 2
        # (not the default 0/2 either side already uses) so BankswitchSRAM(saved)
        # at the end leaves bank 2 selected; a plain post-call read at the seeded
        # SRAM address then observes bank 2's mirrored content without needing
        # `sread`, proving the sweep actually ran rather than no-op'd on bc=0.
        {"wram": {hBankSRAM: b"\x02"},
         "sram": {0: {0xA100: b"\xde\xad\xbe\xef"}},
         "oracle": False,
         "why": "bc=0 is 65536 iterations (two SRAM bank switches each), which "
                "exceeds the oracle's 240-frame synthesized-call-frame budget.",
         "expect_sram": {0: {0xA100: b"\xde\xad\xbe\xef"}}},
        dict(POISON, hl=0xA100, b=0x00, c=0x04,
             sram={0: {0xA100: b"\xde\xad\xbe\xef"}},
             sread={2: {0xA100: 4}}),
        {"hl": 0xA100, "b": 0x00, "c": 0x01,
         "sram": {0: {0xA100: b"\x42"}}, "sread": {2: {0xA100: 1}}},
        {"hl": 0xA100, "b": 0x01, "c": 0x00,
         "sram": {0: {0xA100: bytes(range(256))}}, "sread": {2: {0xA100: 256}}},
        {"hl": 0xA100, "b": 0x01, "c": 0x01,
         "sram": {0: {0xA100: bytes(range(256)) + b"\xaa"}}, "sread": {2: {0xA100: 257}}},
    ],
    "LoadDataFromBackup": [
        # Mirror of WriteDataToBackup's bc=0 case: hBankSRAM defaults to 0, which
        # BankswitchSRAM(saved) restores at the end, so a plain post-call read at
        # the seeded address observes bank 0's mirrored content (from bank 2).
        {"sram": {2: {0xA100: b"\xde\xad\xbe\xef"}},
         "oracle": False,
         "why": "bc=0 is 65536 iterations (two SRAM bank switches each), which "
                "exceeds the oracle's 240-frame synthesized-call-frame budget.",
         "expect_sram": {2: {0xA100: b"\xde\xad\xbe\xef"}}},
        dict(POISON, hl=0xA100, b=0x00, c=0x04,
             sram={2: {0xA100: b"\xde\xad\xbe\xef"}},
             sread={0: {0xA100: 4}}),
        {"hl": 0xA100, "b": 0x00, "c": 0x01,
         "sram": {2: {0xA100: b"\x42"}}, "sread": {0: {0xA100: 1}}},
        {"hl": 0xA100, "b": 0x01, "c": 0x00,
         "sram": {2: {0xA100: bytes(range(256))}}, "sread": {0: {0xA100: 256}}},
        {"hl": 0xA100, "b": 0x01, "c": 0x01,
         "sram": {2: {0xA100: bytes(range(256)) + b"\xaa"}}, "sread": {0: {0xA100: 257}}},
    ],
    "WriteBackupGeneralSaveData": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        # Cross-bank mirroring: poison bank 0's whole $B800-$B8FF, confirm bank 2
        # matches and bank 0 is untouched; hBankSRAM (seeded away from 0/2) pins the
        # per-byte flip actually restoring the entry bank rather than leaking it.
        {"wram": {hBankSRAM: b"\x03"},
         "sram": {0: {sGeneralSaveData: bytes((i * 31 + 7) & 0xFF for i in range(256))}},
         "sread": {0: {sGeneralSaveData: 256}, 2: {sGeneralSaveData: 256}},
         "read": {hBankSRAM: 1}},
    ],
    "WriteBackupCardAndDeckSaveData": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        # 5639 bytes exceeds both the 4096-byte sread cap and the probe's per-span
        # hex-string buffer (8192 hex chars = 4096 bytes exactly overflows it), so
        # both the seed and the readback split into two sub-4096-byte spans.
        {"wram": {hBankSRAM: b"\x03"},
         "sram": {0: {sCardCollection: _CARD_PATTERN[:4000],
                      sCardCollection + 4000: _CARD_PATTERN[4000:]}},
         "sread": {0: {sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000},
                   2: {sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000}},
         "read": {hBankSRAM: 1}},
    ],
    "LoadBackupGeneralSaveData": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        {"wram": {hBankSRAM: b"\x03"},
         "sram": {2: {sGeneralSaveData: bytes((i * 31 + 7) & 0xFF for i in range(256))}},
         "sread": {2: {sGeneralSaveData: 256}, 0: {sGeneralSaveData: 256}},
         "read": {hBankSRAM: 1}},
    ],
    "LoadBackupCardAndDeckSaveData": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        {"wram": {hBankSRAM: b"\x03"},
         "sram": {2: {sCardCollection: _CARD_PATTERN[:4000],
                      sCardCollection + 4000: _CARD_PATTERN[4000:]}},
         "sread": {2: {sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000},
                   0: {sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000}},
         "read": {hBankSRAM: 1}},
    ],
    "InvalidateSaveData": [
        {"wram": {hBankROM: b"\x04"}},
        dict(POISON, wram={hBankROM: b"\x04"}),
        # Header magic: bank 2's header bytes become the complement of $08/$00;
        # bank 0 at the same address is untouched, and hBankSRAM is restored.
        {"wram": {hBankROM: b"\x04", hBankSRAM: b"\x03"},
         "sram": {2: {sBackupGeneralSaveData: _VALID_BACKUP_IMAGE[:2]},
                  0: {sGeneralSaveData: bytes([0x11, 0x22])}},
         "sread": {2: {sBackupGeneralSaveData: 2}, 0: {sGeneralSaveData: 2}},
         "read": {hBankSRAM: 1}},
    ],
    "UpdateAlbumProgress": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        # No bank switch: writes land in whichever bank is selected at entry, never
        # bank 2 unless bank 2 is the one selected.
        {"d": 0xB8, "e": 0xFE, "sram": {1: {}},
         "sread": {1: {sAlbumProgress: 2}, 2: {sAlbumProgress: 2}},
         "read": {wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1}},
        {"d": 0xB8, "e": 0xFE, "sram": {3: {}},
         "sread": {3: {sAlbumProgress: 2}, 2: {sAlbumProgress: 2}},
         "read": {wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1}},
    ],
    "LoadAlbumProgressFromSRAM": [
        {},
        dict(POISON, d=0xDD, e=0xEE),
        {"d": 0xB8, "e": 0xFE, "sram": {0: {sAlbumProgress: b"\x2a\x37"}},
         "read": {wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1}},
        # de+1 wraps $FFFF -> $0000: a real 16-bit address wraparound, not a no-op.
        {"d": 0xFF, "e": 0xFF,
         "read": {wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1}},
    ],
    "ValidateBackupGeneralSaveData": [
        {},
        POISON,
        {"wram": {hBankSRAM: b"\x03"},
         "sram": {2: {sBackupGeneralSaveData: _VALID_BACKUP_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1, hBankSRAM: 1}},
        # Header magic outcome: InvalidateSaveData's complemented header, error count
        # rises from 0 (above) to 1.
        {"sram": {2: {sBackupGeneralSaveData: _INVALID_HEADER_BACKUP_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        {"sram": {2: {sBackupGeneralSaveData: _MULTI_ERROR_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        # Bank asymmetry: this validator switches to bank 2 explicitly, so it reads
        # sAlbumProgress from bank 2 regardless of the entry-selected bank (here 0).
        {"sram": {0: {sAlbumProgress: b"\x99\x88"},
                  2: {sBackupGeneralSaveData: _VALID_BACKUP_IMAGE, sAlbumProgress: b"\x2a\x37"}},
         "read": {wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1}},
    ],
    "_ValidateGeneralSaveData": [
        {},
        POISON,
        {"sram": {0: {sGeneralSaveData: _VALID_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        {"sram": {0: {sGeneralSaveData: _BAD_CHECKSUM_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        {"sram": {0: {sGeneralSaveData: _MULTI_ERROR_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        # Bank asymmetry: no bank switch here, so it reads sAlbumProgress out of
        # whichever bank ends up selected (bank 0, the normal-path default), never
        # bank 2's real value.
        {"sram": {2: {sAlbumProgress: b"\x99\x88"},
                  0: {sGeneralSaveData: _VALID_IMAGE, sAlbumProgress: b"\x2a\x37"}},
         "read": {wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1}},
    ],
    "LoadBackupSaveData": [
        {"wram": {hBankROM: b"\x04"}},
        dict(POISON, wram={hBankROM: b"\x04"}),
        # Round trip: backup bank 2 mirrors into bank 0 (LoadBackupGeneralSaveData),
        # which then loads into WRAM through the mapper walk.
        {"wram": {hBankROM: b"\x04"},
         "sram": {2: {sGeneralSaveData: build_image(_BASE_PAYLOAD)}},
         "read": {MAPPER[0][0]: 1, wEventVars: 64}},
    ],
    "_LoadGeneralSaveData": [
        {},
        POISON,
        {"sram": {0: {sGeneralSaveData: build_image(_BASE_PAYLOAD)}},
         "read": {MAPPER[0][0]: 1, wEventVars: 64}},
    ],
    "_AddCardToCollectionAndUpdateAlbumProgress": [
        {},
        POISON,
        # Double-run quirk: the second pass runs under the restored (bank 0) bank
        # with a distinct collection, so both banks' sAlbumProgress must diverge.
        {"a": 0x10,
         "sram": {2: {sCardCollection: _P2_COLLECTION}, 0: {sCardCollection: _P0_COLLECTION}},
         "sread": {2: {sAlbumProgress: 2}, 0: {sAlbumProgress: 2}}},
    ],
    # These four reach TryGiveMedalPCPacks / OverworldMap_GetOWMapID / BackupPlayerPosition
    # via farcall, whose return restores the ROM bank from hBankROM ($FF80). The oracle's
    # synthesized frame selects the entry bank in the MBC but never sets hBankROM, so each
    # case seeds it to bank 4 (this file's home) -- the same trick LoadBackupSaveData uses
    # for its bank1call. Without it the first farcall restores bank 0 mid-routine and the
    # oracle blocks (a single tick hangs on the corrupted path); with it the farcall
    # round-trip is symmetric and the routine returns cleanly.
    "SaveGeneralSaveDataFromDE": [
        {"d": 0xB8, "e": 0x00, "wram": {hBankROM: b"\x04"},
         "sram": {0: {sGeneralSaveData: bytes(187)}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187}}},
        dict(POISON, d=0xB8, e=0x00, wram={hBankROM: b"\x04"}),
        {"d": 0xB8, "e": 0x00,
         "wram": {hBankROM: b"\x04", **poison_wram(seed=7), wEventVars: event_vars_for(3),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x05"},
         "sram": {0: {sGeneralSaveData: bytes(187)}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187}}},
        {"d": 0xB8, "e": 0x00,
         "wram": {hBankROM: b"\x04", **poison_wram(seed=9), wEventVars: event_vars_for(8),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x06"},
         "sram": {0: {sGeneralSaveData: bytes(187)}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187}}},
        {"d": 0xB8, "e": 0x00,
         "wram": {hBankROM: b"\x04", **poison_wram(seed=11), wEventVars: event_vars_for(2),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x02"},
         "sram": {0: {sGeneralSaveData: bytes(187)}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187}}},
    ],
    "_SaveGeneralSaveData": [
        {"wram": {hBankROM: b"\x04"},
         "sram": {0: {sGeneralSaveData: bytes(187)}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187}}},
        dict(POISON, wram={hBankROM: b"\x04"}),
        {"wram": {hBankROM: b"\x04", **poison_wram(seed=14),
                  wEventVars: event_vars_for(4, True, True),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x02"},
         "sram": {0: {sGeneralSaveData: bytes(187), sCardCollection: _CARD_PATTERN[:256]}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15,
                  wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187, sAlbumProgress: 2,
                       sReceivedLegendaryCards: 1}}},
    ],
    "SaveAndBackupData": [
        {"wram": {hBankROM: b"\x04"},
         "sram": {0: {sGeneralSaveData: bytes(256)}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187, sAlbumProgress: 2}}},
        dict(POISON, wram={hBankROM: b"\x04"}),
        {"wram": {hBankROM: b"\x04", **poison_wram(seed=13), wEventVars: event_vars_for(5),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x03"},
         "sram": {0: {sGeneralSaveData: bytes(256),
                      sCardCollection: _CARD_PATTERN[:4000],
                      sCardCollection + 4000: _CARD_PATTERN[4000:5639]}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15,
                  wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187, sAlbumProgress: 2},
                   2: {sGeneralSaveData: 187, sAlbumProgress: 2,
                       sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000}}},
    ],
    "_SaveGame": [
        {"c": 0x00,
         "wram": {hBankROM: b"\x04", **poison_wram(seed=15), wEventVars: event_vars_for(6),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x04",
                  wCurMap: b"\x07", wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x34",
                  wPlayerDirection: b"\x01"},
         "sram": {0: {sGeneralSaveData: bytes(256),
                      sCardCollection: _CARD_PATTERN[:4000],
                      sCardCollection + 4000: _CARD_PATTERN[4000:5639]}},
         "read": {wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1,
                  wTempPlayerDirection: 1, wMedalCount: 1, wCurOverworldMap: 1,
                  wLoadedEventBits: 1, wEventVars: 64, wPCPacks: 15,
                  wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187, sAlbumProgress: 2},
                   2: {sGeneralSaveData: 187, sAlbumProgress: 2,
                       sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000}}},
        {"c": 0x01,
         "wram": {hBankROM: b"\x04", **poison_wram(seed=16), wEventVars: event_vars_for(7),
                  wPCPacks: bytes(15)},
         "sram": {0: {sGeneralSaveData: bytes(256),
                      sCardCollection: _CARD_PATTERN[:4000],
                      sCardCollection + 4000: _CARD_PATTERN[4000:5639]}},
         "read": {wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1,
                  wTempPlayerDirection: 1, wOverworldMapSelection: 1,
                  wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15,
                  wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187, sAlbumProgress: 2},
                   2: {sGeneralSaveData: 187, sAlbumProgress: 2,
                       sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000}}},
        dict(POISON, c=0x01, wram={hBankROM: b"\x04"}),
    ],
    "SaveGeneralSaveData": [
        {"wram": {hBankROM: b"\x04"},
         "sram": {0: {sGeneralSaveData: bytes(187)}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187}}},
        dict(POISON, wram={hBankROM: b"\x04"}),
        {"wram": {hBankROM: b"\x04", **poison_wram(seed=14),
                  wEventVars: event_vars_for(4, True, True),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x02"},
         "sram": {0: {sGeneralSaveData: bytes(187), sCardCollection: _CARD_PATTERN[:256]}},
         "read": {wMedalCount: 1, wCurOverworldMap: 1, wLoadedEventBits: 1,
                  wEventVars: 64, wPCPacks: 15,
                  wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187, sAlbumProgress: 2,
                       sReceivedLegendaryCards: 1}}},
    ],
    "LoadGeneralSaveData": [
        {},
        POISON,
        {"sram": {0: {sGeneralSaveData: build_image(_BASE_PAYLOAD)}},
         "read": {MAPPER[0][0]: 1, wEventVars: 64}},
    ],
    "ValidateGeneralSaveData": [
        {},
        POISON,
        {"sram": {0: {sGeneralSaveData: _VALID_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        {"sram": {0: {sGeneralSaveData: _BAD_CHECKSUM_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        {"sram": {0: {sGeneralSaveData: _MULTI_ERROR_IMAGE}},
         "read": {wNumSRAMValidationErrors: 1}},
        {"sram": {2: {sAlbumProgress: b"\x99\x88"},
                  0: {sGeneralSaveData: _VALID_IMAGE, sAlbumProgress: b"\x2a\x37"}},
         "read": {wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1}},
    ],
    "AddCardToCollectionAndUpdateAlbumProgress": [
        {},
        POISON,
        {"a": 0x10,
         "sram": {2: {sCardCollection: _P2_COLLECTION}, 0: {sCardCollection: _P0_COLLECTION}},
         "sread": {2: {sAlbumProgress: 2}, 0: {sAlbumProgress: 2}}},
    ],
    # SaveGame always calls _SaveGame(0) -- save.asm:24 hardcodes c before the
    # farcall, so the caller's c is dead despite being preserved back out. Both
    # cases seed the same wCurMap/wPlayer* source data that the c==0 branch reads,
    # then case 2's poisoned c=0xCC (rather than 0) proves the branch taken is
    # still "current position", not the "force Mason lab" branch: a c-pass-through
    # bug would report wTempPlayerDirection=$02 (DIR_SOUTH) and wTempMap=MAP_MASON
    # instead of the seeded $01/$07.
    "SaveGame": [
        {"wram": {hBankROM: b"\x04", **poison_wram(seed=15), wEventVars: event_vars_for(6),
                  wPCPacks: bytes(15), wOverworldMapSelection: b"\x04",
                  wCurMap: b"\x07", wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x34",
                  wPlayerDirection: b"\x01"},
         "sram": {0: {sGeneralSaveData: bytes(256),
                      sCardCollection: _CARD_PATTERN[:4000],
                      sCardCollection + 4000: _CARD_PATTERN[4000:5639]}},
         "read": {wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1,
                  wTempPlayerDirection: 1, wMedalCount: 1, wCurOverworldMap: 1,
                  wLoadedEventBits: 1, wEventVars: 64, wPCPacks: 15,
                  wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1, **ACCUMULATORS},
         "sread": {0: {sGeneralSaveData: 187, sAlbumProgress: 2},
                   2: {sGeneralSaveData: 187, sAlbumProgress: 2,
                       sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000}}},
        dict(POISON,
             wram={hBankROM: b"\x04", **poison_wram(seed=15), wEventVars: event_vars_for(6),
                   wPCPacks: bytes(15), wOverworldMapSelection: b"\x04",
                   wCurMap: b"\x07", wPlayerXCoord: b"\x12", wPlayerYCoord: b"\x34",
                   wPlayerDirection: b"\x01"},
             sram={0: {sGeneralSaveData: bytes(256),
                       sCardCollection: _CARD_PATTERN[:4000],
                       sCardCollection + 4000: _CARD_PATTERN[4000:5639]}},
             read={wTempMap: 1, wTempPlayerXCoord: 1, wTempPlayerYCoord: 1,
                   wTempPlayerDirection: 1, wMedalCount: 1, wCurOverworldMap: 1,
                   wLoadedEventBits: 1, wEventVars: 64, wPCPacks: 15,
                   wTotalNumCardsCollected: 1, wTotalNumCardsToCollect: 1, **ACCUMULATORS},
             sread={0: {sGeneralSaveData: 187, sAlbumProgress: 2},
                    2: {sGeneralSaveData: 187, sAlbumProgress: 2,
                        sCardCollection: 4000, sCardCollection + 4000: 5639 - 4000}}),
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
