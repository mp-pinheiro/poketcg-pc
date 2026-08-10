"""Oracle-diff cases for ClearSavedDuel (engine/duel/core.asm:6183-6191)."""

POISON = {"a": 0xAA, "f": 0xF0, "b": 0xBB, "c": 0xCC, "d": 0xDD, "e": 0xEE, "hl": 0x1234}

sCurrentDuelValid = 0xBC00
sCurrentDuelChecksum = 0xBC01
GUARD_LOW = 0xBBFF        # byte just below sCurrentDuelValid
GUARD_HIGH = 0xBC03       # sCurrentDuelType, the byte just past the checksum
hBankSRAM = 0xFF81

CONTRACT = {
    # b/c/d/e are never referenced by the asm, so they are preserved. a, f and hl are
    # deliberately absent: their exit values ($00, $80, $BC02) are constants of the
    # instruction sequence that none of the four callsites reads (challenge_machine.asm:72,
    # save.asm:22, save.asm:362, overworld/overworld.asm:4 -- each overwrites or discards
    # a/f/hl before use), so naming them would force a hardcoded value into the adapter
    # rather than test anything.
    "ClearSavedDuel": ("b", "c", "d", "e"),
}

CASES = {
    "ClearSavedDuel": [
        # All-zero baseline.
        {"sread": {0: {sCurrentDuelValid: 3}}},
        # Poisoned registers: none are consumed by the routine. hBankSRAM is seeded
        # away from the 0/2 both sides default to and read back, which is the only
        # thing pinning the asm's guarantee that it never bank-switches: a port using
        # BankswitchSRAM(g_sram_bank) to enable SRAM re-selects the same bank and
        # would diff clean everywhere else.
        dict(POISON,
             wram={hBankSRAM: b"\x03"},
             sram={0: {sCurrentDuelValid: b"\xaa\xbb\xcc"}},
             read={hBankSRAM: 1}),
        # Guard bytes on both sides of the 3-byte target prove the clear is exactly
        # $BC00-$BC02 wide.
        {"sram": {0: {GUARD_LOW: b"\x11", sCurrentDuelValid: b"\xaa\xbb\xcc",
                      GUARD_HIGH: b"\x22"}}},
        # Bank 2 seeded last is live at entry, so the routine must clear bank 2 and
        # leave bank 0's distinct bytes at the same address untouched.
        {"sram": {0: {sCurrentDuelValid: b"\x44\x55\x66"},
                  2: {sCurrentDuelValid: b"\xaa\xbb\xcc"}}},
        # The routine's own EnableSRAM is only observable when the latch is OFF at
        # entry with non-zero bytes in the target. Seeding SRAM turns the latch on as
        # a side effect, so `ramg: False` forces it back off after the seed; without
        # the enable, gb_write8 drops all three stores and the seeded bytes survive.
        {"sram": {0: {sCurrentDuelValid: b"\xaa\xbb\xcc"}}, "ramg": False},
    ],
}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
