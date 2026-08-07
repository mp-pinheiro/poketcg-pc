#ifndef POKETCG_MEM_H
#define POKETCG_MEM_H

#include <stddef.h>
#include <stdint.h>

/* Game Boy address space, one array per region the ported routines touch.
 * The generated layout headers in include/generated/ index straight into these. */
extern uint8_t g_wram[0x2000]; /* $C000-$DFFF; every rgbds section is WRAM0 */
extern uint8_t g_hram[0x80];   /* $FF80-$FFFF */
extern uint8_t g_sram[0x8000]; /* 4 banks x 8 KiB, windowed at $A000-$BFFF */
extern uint8_t g_vram[0x4000]; /* 2 banks x 8 KiB, windowed at $8000-$9FFF (CGB) */
extern uint8_t g_oam[0xA0];    /* $FE00-$FE9F */
extern uint8_t g_io[0x80];     /* $FF00-$FF7F */
extern uint8_t g_pal[0x80];    /* CGB palette RAM; reached through $FF68-$FF6B, not mapped */

/* $FEA0-$FEFF, the unusable hole, plus the landing page for out-of-image ROM reads.
 * Writable through the bus, so it belongs in any full-state snapshot. */
#define MEM_SCRATCH_SIZE 0x100
extern uint8_t g_scratch[MEM_SCRATCH_SIZE];

/* ROM image, loaded from $POKETCG_ROM. Only exists because three ported routines
 * read banked ROM (GetFarByte, DecompressDataFromBank, CopyBankedDataToDE); the
 * data-extraction phase replaces those reads with generated C arrays. */
extern uint8_t *g_rom;
extern size_t g_rom_size;

/* MBC5 latches, written only through mbc5_write() -- the single decoder for every
 * register write below $8000, so the port has exactly one MBC5 model. */
extern uint8_t g_rom_bank;
extern uint8_t g_sram_bank;
extern int g_sram_enabled;

/* VBK ($FF4F) low bit: which half of g_vram the $8000-$9FFF window resolves to. */
extern uint8_t g_vram_bank;
typedef struct {
	uint32_t tick;
	uint16_t address;
	uint8_t value;
} ApuWrite;

#define APU_TRACE_CAPACITY 65536u
void apu_trace_clear(void);
void apu_trace_set_tick(uint32_t tick);
size_t apu_trace_count(void);
const ApuWrite *apu_trace_data(void);


int rom_load(const char *path); /* 0 on success, -1 with errno set */
void rom_free(void);

/* bank:addr -> ROM image. addr < $4000 ignores bank, as on hardware. Out-of-image
 * offsets resolve to the open-bus scratch page rather than reading past g_rom. */
const uint8_t *rom_ptr(uint8_t bank, uint16_t addr);

/* Whole-address-space access, needed by routines whose state is GB-address-shaped
 * (the decompressor keeps its source and buffer pointers in WRAM as raw addresses).
 * Total by design: it never returns NULL, because several ported routines walk the
 * whole 64 KiB when a count is zero. Only $FEA0-$FEFF, the unusable hole, is scratch. */
uint8_t *gb_ptr(uint16_t addr);
uint8_t gb_read8(uint16_t addr);
void gb_write8(uint16_t addr, uint8_t v); /* writes below $8000 decode as MBC5 registers */
void mbc5_write(uint16_t addr, uint8_t v); /* MBC5 register decode; mirrors PyBoy's MBC5.setitem */

/* Reset every region and both bank latches to power-on state. Leaves g_rom alone. */
void mem_reset(void);

#endif /* POKETCG_MEM_H */
