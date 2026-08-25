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

/* Held-button state a case seeds via the "keys" probe key, laid out exactly like
 * hKeysHeld (src/constants/hardware.inc): bit0 A, 1 B, 2 SELECT, 3 START, 4 RIGHT,
 * 5 LEFT, 6 UP, 7 DOWN. 1 = pressed. gb_read8($FF00) resolves the joypad matrix
 * against it so ReadJoypad (and anything that waits on it) can observe input. */
extern uint8_t g_keys;

/* Per-poll key timeline, the native mirror of the reference's per-frame
 * `input_events` cycle (tools/oracle/gbref/runner.c: input_index advances on each
 * frame boundary, modulo the entry count, and only when more than one entry
 * exists). The native probe renders no frames, so the faithful analogue of a
 * frame boundary is a completed joypad poll: ReadJoypad ends by having
 * SaveButtonsHeld store hKeysHeld, the only write to that address in the tree.
 * gb_keys_arm_timeline() registers that latch address and the cycle; every write
 * to it advances g_keys to the next entry.
 *
 * With zero or one entry the index never leaves 0 and g_keys is exactly the
 * single seeded value, so an armed timeline is inert for every case that does not
 * declare a multi-frame one. That is what keeps a held `keys` scalar -- newly
 * pressed exactly once -- unchanged.
 */
#define MEM_KEY_TIMELINE_MAX 16
void gb_keys_arm_timeline(const uint8_t *entries, uint8_t count, uint16_t latch_addr);

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
void mbc5_conformance_vector(void);

/* Reset every region and both bank latches to power-on state. Leaves g_rom alone. */
void mem_reset(void);

#endif /* POKETCG_MEM_H */
