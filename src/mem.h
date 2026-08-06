#ifndef POKETCG_MEM_H
#define POKETCG_MEM_H

#include <stddef.h>
#include <stdint.h>

/* Game Boy address space, one array per region the ported routines touch.
 * The generated layout headers in include/generated/ index straight into these. */
extern uint8_t g_wram[0x2000]; /* $C000-$DFFF; every rgbds section is WRAM0 */
extern uint8_t g_hram[0x80];   /* $FF80-$FFFF */
extern uint8_t g_sram[0x8000]; /* 4 banks x 8 KiB, windowed at $A000-$BFFF. Always
                                * readable: the MBC5 SRAM-enable latch is not modelled,
                                * so a read before enabling returns 0 here and $FF on
                                * hardware. */

/* ROM image, loaded from $POKETCG_ROM. Only exists because three ported routines
 * read banked ROM (GetFarByte, DecompressDataFromBank, CopyBankedDataToDE); the
 * data-extraction phase replaces those reads with generated C arrays. */
extern uint8_t *g_rom;
extern size_t g_rom_size;

/* MBC5 latches. BankswitchROM() writes g_rom_bank; hBankSRAM writes g_sram_bank. */
extern uint8_t g_rom_bank;
extern uint8_t g_sram_bank;

int rom_load(const char *path); /* 0 on success, -1 with errno set */
void rom_free(void);

/* bank:addr -> ROM image. addr < $4000 ignores bank, as on hardware. Out-of-image
 * offsets resolve to the open-bus scratch page rather than reading past g_rom. */
const uint8_t *rom_ptr(uint8_t bank, uint16_t addr);

/* Whole-address-space access, needed by routines whose state is GB-address-shaped
 * (the decompressor keeps its source and buffer pointers in WRAM as raw addresses).
 * $8000-$9FFF and $FE00-$FF7F resolve to a shared scratch page: this slice has no
 * PPU, so VRAM/OAM/IO are plain read-write bytes with no side effects. */
uint8_t *gb_ptr(uint16_t addr);
uint8_t gb_read8(uint16_t addr);
void gb_write8(uint16_t addr, uint8_t v); /* writes below $8000 are discarded */

/* Reset every region and both bank latches to power-on state. Leaves g_rom alone. */
void mem_reset(void);

#endif /* POKETCG_MEM_H */
