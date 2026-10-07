#include "home/memory.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/decompress.h"
#include "home/switch_rom.h"
#include "mem.h"

/* DecompressDataFromBank:: poketcg/src/home/memory.asm:6-14 */
void DecompressDataFromBank(uint16_t bc, uint16_t de)
{
	uint8_t saved = hBankROM;

	BankswitchROM(wTempPointerBank);
	DecompressData(bc, de);
	BankswitchROM(saved);
}

/* CopyBankedDataToDE:: poketcg/src/home/memory.asm:17-31 */
void CopyBankedDataToDE(uint16_t bc, uint16_t de)
{
	uint8_t saved = hBankROM;

	BankswitchROM(wTempPointerBank);
	CopyDataHLtoDE_SaveRegisters(
		(uint16_t)(wTempPointer_PTR[0] | wTempPointer_PTR[1] << 8), de, bc);
	BankswitchROM(saved);
}

/* FillMemoryWithA:: poketcg/src/home/memory.asm:34-49. Post-test loop: bc==0 fills
 * 65536 bytes. */
void FillMemoryWithA(uint16_t hl, uint16_t bc, uint8_t a)
{
	uint32_t n = bc ? bc : 0x10000;

	while (n--)
		gb_write8(hl++, a);
}

/* FillMemoryWithDE:: poketcg/src/home/memory.asm:52-66. bc counts pairs, so bc==0
 * writes 131072 bytes and wraps the address space twice. */
void FillMemoryWithDE(uint16_t hl, uint16_t bc, uint8_t d, uint8_t e)
{
	uint32_t n = bc ? bc : 0x10000;

	while (n--) {
		gb_write8(hl++, e);
		gb_write8(hl++, d);
	}
}

/* memory.asm:79 `ld a, [hl]` is a bus read under the switched bank, not a ROM read:
 * an address at or above $8000 reaches VRAM/SRAM/WRAM/HRAM. */
uint8_t GetFarByte(uint8_t bank, uint16_t addr)
{
	uint8_t saved = hBankROM;
	uint8_t v;

	BankswitchROM(bank);
	v = gb_read8(addr);
	BankswitchROM(saved);
	return v;
}
