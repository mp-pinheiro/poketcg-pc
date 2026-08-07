#include "mem.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

uint8_t g_wram[0x2000];
uint8_t g_hram[0x80];
uint8_t g_sram[0x8000];

uint8_t *g_rom = NULL;
size_t g_rom_size = 0;

uint8_t g_rom_bank = 1;
uint8_t g_sram_bank = 0;
int g_sram_enabled = 0;

/* Backs VRAM/OAM/IO and out-of-image ROM reads. Not a PPU: plain scratch bytes so
 * the bus is total and a stray access cannot run off an array. */
static uint8_t g_scratch[0x2000];

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
	memset(g_scratch, 0, sizeof g_scratch);
	g_rom_bank = 1;
	g_sram_bank = 0;
	g_sram_enabled = 0;
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
		return g_scratch + (addr - 0x8000);
	if (addr < 0xC000)
		return g_sram + (size_t)(g_sram_bank & 3) * 0x2000 + (addr - 0xA000);
	if (addr < 0xE000)
		return g_wram + (addr - 0xC000);
	if (addr < 0xFE00)
		return g_wram + (addr - 0xE000); /* echo RAM */
	if (addr < 0xFF80)
		return g_scratch + (addr - 0xFE00);
	return g_hram + (addr - 0xFF80);
}

uint8_t gb_read8(uint16_t addr)
{
	if (addr >= 0xA000 && addr < 0xC000 && !g_sram_enabled)
		return 0xFF; /* open bus, as on hardware */
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

void gb_write8(uint16_t addr, uint8_t v)
{
	if (addr < 0x8000) {
		mbc5_write(addr, v);
		return;
	}
	if (addr >= 0xA000 && addr < 0xC000 && !g_sram_enabled)
		return;
	*gb_ptr(addr) = v;
}
