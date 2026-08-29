#include "mem.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

uint8_t g_wram[0x2000];
uint8_t g_hram[0x80];
uint8_t g_sram[0x8000];
uint8_t g_vram[0x4000];
uint8_t g_oam[0xA0];
uint8_t g_io[0x80];
uint8_t g_pal[0x80];
uint8_t g_keys;
static uint16_t g_ir_read_count;
static uint16_t g_ir_write_count;
static uint8_t g_ir_mode;

/* Key timeline: entries[0..count-1], cycled per completed joypad poll. count <= 1
 * disarms the advance entirely, leaving g_keys exactly as seeded. */
static uint8_t g_key_entries[MEM_KEY_TIMELINE_MAX];
static uint8_t g_key_count;
static uint8_t g_key_index;
static uint16_t g_key_latch_addr;
static int g_key_latch_armed;

void gb_keys_arm_timeline(const uint8_t *entries, uint8_t count, uint16_t latch_addr)
{
	if (count > MEM_KEY_TIMELINE_MAX)
		count = MEM_KEY_TIMELINE_MAX;
	for (uint8_t i = 0; i < count; i++)
		g_key_entries[i] = entries[i];
	g_key_count = count;
	g_key_index = 0;
	g_key_latch_addr = latch_addr;
	g_key_latch_armed = count > 1;
	if (count)
		g_keys = entries[0];
}

uint8_t *g_rom = NULL;
size_t g_rom_size = 0;

uint8_t g_rom_bank = 1;
uint8_t g_sram_bank = 0;
uint8_t g_vram_bank = 0;
int g_sram_enabled = 0;

/* Out-of-image ROM reads and the unusable $FEA0-$FEFF hole, so gb_ptr stays total.
 * Writable through gb_write8, so the snapshot vector has to cover it. */
uint8_t g_scratch[MEM_SCRATCH_SIZE];

static ApuWrite g_apu_trace[APU_TRACE_CAPACITY];
static size_t g_apu_trace_count;
static uint32_t g_apu_trace_tick;

void apu_trace_clear(void)
{
	g_apu_trace_count = 0;
	g_apu_trace_tick = 0;
}

void apu_trace_set_tick(uint32_t tick)
{
	g_apu_trace_tick = tick;
}

size_t apu_trace_count(void)
{
	return g_apu_trace_count;
}

const ApuWrite *apu_trace_data(void)
{
	return g_apu_trace;
}

static void apu_trace_record(uint16_t addr, uint8_t value)
{
	if (!((addr >= 0xFF10u && addr <= 0xFF26u) ||
	      (addr >= 0xFF30u && addr <= 0xFF3Fu)))
		return;
	if (g_apu_trace_count < APU_TRACE_CAPACITY) {
		g_apu_trace[g_apu_trace_count++] = (ApuWrite){g_apu_trace_tick, addr, value};
	}
}

int rom_load(const char *path)
{
	FILE *f = fopen(path, "rb");
	if (!f)
		return -1;
	if (fseek(f, 0, SEEK_END) != 0) {
		fclose(f);
		return -1;
	}
	long n = ftell(f);
	if (n <= 0) {
		fclose(f);
		return -1;
	}
	rewind(f);

	uint8_t *buf = malloc((size_t)n);
	if (!buf) {
		fclose(f);
		return -1;
	}
	if (fread(buf, 1, (size_t)n, f) != (size_t)n) {
		free(buf);
		fclose(f);
		return -1;
	}
	fclose(f);

	free(g_rom);
	g_rom = buf;
	g_rom_size = (size_t)n;
	return 0;
}

void rom_free(void)
{
	free(g_rom);
	g_rom = NULL;
	g_rom_size = 0;
}

void mem_reset(void)
{
	memset(g_wram, 0, sizeof g_wram);
	memset(g_hram, 0, sizeof g_hram);
	memset(g_sram, 0, sizeof g_sram);
	memset(g_vram, 0, sizeof g_vram);
	memset(g_oam, 0, sizeof g_oam);
	memset(g_io, 0, sizeof g_io);
	memset(g_pal, 0, sizeof g_pal);
	g_keys = 0;
	g_ir_read_count = 0;
	g_ir_write_count = 0;
	g_ir_mode = 0;
	g_key_count = 0;
	g_key_index = 0;
	g_key_latch_addr = 0;
	memset(g_scratch, 0, sizeof g_scratch);
	g_rom_bank = 1;
	g_sram_bank = 0;
	g_vram_bank = 0;
	g_sram_enabled = 0;
	apu_trace_clear();
}

const uint8_t *rom_ptr(uint8_t bank, uint16_t addr)
{
	size_t off = addr < 0x4000 ? addr : (size_t)0x4000 * bank + (addr - 0x4000);
	if (!g_rom || off >= g_rom_size)
		return g_scratch;
	return g_rom + off;
}

uint8_t *gb_ptr(uint16_t addr)
{
	if (addr < 0x8000)
		return (uint8_t *)rom_ptr(addr < 0x4000 ? 0 : g_rom_bank, addr);
	if (addr < 0xA000)
		return g_vram + (size_t)(g_vram_bank & 1) * 0x2000 + (addr - 0x8000);
	if (addr < 0xC000)
		return g_sram + (size_t)(g_sram_bank & 3) * 0x2000 + (addr - 0xA000);
	if (addr < 0xE000)
		return g_wram + (addr - 0xC000);
	if (addr < 0xFE00)
		return g_wram + (addr - 0xE000); /* echo RAM */
	if (addr < 0xFEA0)
		return g_oam + (addr - 0xFE00);
	if (addr < 0xFF00)
		return g_scratch + (addr - 0xFEA0); /* unusable region */
	if (addr < 0xFF80)
		return g_io + (addr - 0xFF00);
	return g_hram + (addr - 0xFF80);
}

uint8_t gb_read8(uint16_t addr)
{
	if (addr >= 0xA000 && addr < 0xC000 && !g_sram_enabled)
		return 0xFF; /* open bus, as on hardware */
	/* STAT bit 7 is unused and reads back as 1 on real hardware, so a
	 * read-modify-write of $FF41 stores it too. PyBoy models this; without it
	 * every rSTAT diff is off by $80. */
	if (addr == 0xFF41u)
		return (uint8_t)(*gb_ptr(addr) | 0x80u);
	if (addr == 0xFF02u)
		return (uint8_t)(*gb_ptr(addr) | 0x7Cu);
	if (addr == 0xFF0Fu)
		return (uint8_t)(*gb_ptr(addr) | 0xE0u);
	if (addr == 0xFF4Fu)
		return (uint8_t)(0xFEu | g_vram_bank);
	if (addr == 0xFF4Du)
		return (uint8_t)(0x7Eu | (*gb_ptr(addr) & 0x80u));
	if (addr == 0xFF69u)
		return g_pal[g_io[0x68] & 0x3Fu];
	if (addr == 0xFF6Bu)
		return g_pal[0x40u + (g_io[0x6A] & 0x3Fu)];
	/* RP ($FF56): unused bits 2-5 float high (0x3C), bit 1 is the IR receive
	 * status (1 = no signal detected), bit 0 echoes the LED-control bit.
	 * Bits 6-7 are write-only enable bits and read back as 0. */
	if (addr == 0xFF56u) {
		if ((g_keys & 0x80u) != 0u) {
			uint16_t sample_total = g_ir_read_count++;
			uint16_t byte_index = sample_total / 81u;
			uint16_t sample = sample_total % 81u;
			uint8_t rx_byte;
			if (sample_total == 0u && g_ir_write_count > 1u)
				g_ir_mode = 1u;
			if (g_ir_write_count <= 1u) {
				rx_byte = byte_index == 0u ? 0xAAu
					: (byte_index == 1u ? 0x49u
					   : (byte_index == 2u ? 0x52u : 0x00u));
			} else if (byte_index == 0u) {
				rx_byte = 0x33u;
			} else if (byte_index == 1u) {
				rx_byte = 0xAAu;
			} else if (g_ir_mode != 0u && byte_index == 2u) {
				rx_byte = 0x33u;
			} else if (g_ir_mode == 0u && byte_index == 2u) {
				rx_byte = 0x49u;
			} else if (g_ir_mode == 0u && byte_index == 3u) {
				rx_byte = 0x52u;
			} else if (g_ir_mode == 0u && byte_index == 12u) {
				rx_byte = 0x01u;
			} else {
				rx_byte = 0x00u;
			}
			if (sample == 0u)
				return 0x3Cu;
			uint16_t bit = (uint16_t)((sample - 1u) / 10u);
			if (bit < 8u)
				return (rx_byte & (uint8_t)(1u << bit)) != 0u ? 0x3Eu : 0x3Cu;
			return 0x3Cu;
		}
		return (uint8_t)(0x3Eu | (*gb_ptr(addr) & 0x01u));
	}
	/* JOYP ($FF00): the stored byte only ever holds the two selection bits a
	 * routine wrote (P14/P15); the input nibble is synthesized from g_keys on
	 * every read, matching hardware's active-low matrix. Neither group
	 * selected (sel == $30) still floats the low nibble high, exactly like
	 * either group selected with no keys held -- PyBoy returns $FF there, not
	 * the raw select bits, and SGB detection protocols (DetectSGB) rely on
	 * that floating-high nibble while both P14/P15 sit deselected. */
	if (addr == 0xFF00u) {
		uint8_t sel = (uint8_t)(*gb_ptr(addr) & 0x30u);
		uint8_t low = 0x0Fu;
		if (!(sel & 0x10u)) /* P14 low: d-pad */
			low &= (uint8_t)~(g_keys >> 4);
		if (!(sel & 0x20u)) /* P15 low: buttons */
			low &= (uint8_t)~(g_keys & 0x0Fu);
		return (uint8_t)(0xC0u | sel | low);
	}
	return *gb_ptr(addr);
}

/* MBC5 register decode, mirroring PyBoy's MBC5.setitem exactly (PyBoy is the oracle).
 * RAMG is an exact byte compare, not a low-nibble mask: PyBoy checks the whole byte.
 * $3000-$3FFF (the ROM bank's 9th bit) and $6000-$7FFF are no-ops on this cart: it has
 * 64 banks, so (v & 1) << 8 always vanishes under the resulting modulo. */
void mbc5_write(uint16_t addr, uint8_t v)
{
	if (addr < 0x2000)
		g_sram_enabled = (v == 0x0A);
	else if (addr < 0x3000)
		g_rom_bank = v % 64;
	else if (addr >= 0x4000 && addr < 0x6000)
		g_sram_bank = (v & 0x0F) % 4;
}

void mbc5_conformance_vector(void)
{
	gb_write8(0xC000, gb_read8(0x0150));
	gb_write8(0xC001, gb_read8(0x4000));

	gb_write8(0x2000, 0x00);
	gb_write8(0xC002, gb_read8(0x4000));
	gb_write8(0x2000, 0x45);
	gb_write8(0xC003, gb_read8(0x4000));
	gb_write8(0x3000, 0x01);
	gb_write8(0xC004, gb_read8(0x4000));
	gb_write8(0x0000, 0x0A);
	gb_write8(0x4000, 0x03);
	gb_write8(0xA123, 0x33);
	gb_write8(0x4000, 0x04);
	gb_write8(0xA123, 0x44);
	gb_write8(0x4000, 0x03);
	gb_write8(0xC005, gb_read8(0xA123));
	gb_write8(0x4000, 0x04);
	gb_write8(0xC006, gb_read8(0xA123));

	gb_write8(0x0000, 0x1A);
	gb_write8(0xA123, 0x55);
	gb_write8(0xC007, gb_read8(0xA123));

	gb_write8(0x0000, 0x0A);
	gb_write8(0x4000, 0x00);
	gb_write8(0xC008, gb_read8(0xA123));

	gb_write8(0x0000, 0x00);
}

void gb_write8(uint16_t addr, uint8_t v)
{
	if (addr < 0x8000) {
		mbc5_write(addr, v);
		return;
	}
	if (addr >= 0xA000 && addr < 0xC000 && !g_sram_enabled)
		return;
	/* VBK: the low bit selects which 8 KiB half of g_vram the $8000-$9FFF window
	 * resolves to, so it has to latch before the store lands. */
	if (addr == 0xFF4F)
		g_vram_bank = v & 1;
	if (addr == 0xFF68u || addr == 0xFF6Au)
		v &= 0xBFu;
	if (addr == 0xFF69u || addr == 0xFF6Bu) {
		uint8_t *index = &g_io[addr == 0xFF69u ? 0x68u : 0x6Au];
		size_t offset = (addr == 0xFF69u ? 0u : 0x40u) + (*index & 0x3Fu);
		g_pal[offset] = v;
		if (*index & 0x80u)
			*index = (uint8_t)(0x80u | ((*index + 1u) & 0x3Fu));
	}
	if (addr == 0xFF56u && (g_keys & 0x80u) != 0u)
		g_ir_write_count++;
	/* A completed joypad poll is the native frame boundary: advance to the next
	 * timeline entry so the following poll sees a fresh press edge, exactly as a
	 * new reference frame does. Cycles modulo the entry count, matching
	 * runner.c. Disarmed unless the case declared more than one entry. */
	if (g_key_latch_armed && addr == g_key_latch_addr) {
		g_key_index = (uint8_t)((g_key_index + 1u) % g_key_count);
		g_keys = g_key_entries[g_key_index];
	}
	apu_trace_record(addr, v);
	*gb_ptr(addr) = v;
}
