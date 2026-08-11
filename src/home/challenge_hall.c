#include "home/challenge_hall.h"

#include "generated/sram.h"
#include "mem.h"

void Func_f5db(void)
{
	gb_write8(sb818_ADDR, 0x00);
	gb_write8((uint16_t)(sb818_ADDR + 1u), 0x00);
	gb_write8((uint16_t)(sb818_ADDR + 2u), 0x00);
	gb_write8((uint16_t)(sb818_ADDR + 3u), 0x00);
}

FuncF5E9Result Func_f5e9(uint8_t c)
{
	uint16_t hl = sb818_ADDR;
	uint8_t offset = c;
	while (offset >= 8u) {
		offset = (uint8_t)(offset - 8u);
		hl++;
	}
	uint8_t b = 0x80u;
	while (offset != 0u) {
		b >>= 1;
		offset = (uint8_t)(offset - 1u);
	}
	return (FuncF5E9Result){hl, b};
}

void Script_Host(void)
{
}
