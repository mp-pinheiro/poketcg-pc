#include "home/dma.h"

#include "generated/wram.h"
#include "mem.h"

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
