#include "home/dma.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#define DMA_ROM_ADDR 0x05A1u
#define DMA_COPY_LENGTH 10u
/* <<< factory statics */

void DMA(void)
{
	const uint8_t source_page = (uint8_t)(wOAM_ADDR >> 8);
	const uint16_t source = (uint16_t)source_page << 8;

	/* DMA starts when rDMA is written; retain the latched page in the IO image. */
	gb_write8(0xFF46u, source_page);
	for (uint16_t i = 0; i < 0xA0u; i++)
		gb_write8((uint16_t)(0xFE00u + i),
			  gb_read8((uint16_t)(source + i)));
}

/* >>> factory CopyDMAFunction */
void CopyDMAFunction(void)
{
	const uint8_t *stub = rom_ptr(0u, DMA_ROM_ADDR);
	for (uint8_t i = 0u; i < DMA_COPY_LENGTH; i++)
		gb_write8((uint16_t)(hDMAFunction_ADDR + i), stub[i]);
}
/* <<< factory CopyDMAFunction */
