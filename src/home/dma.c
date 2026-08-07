#include "home/dma.h"

#include "generated/wram.h"
#include "mem.h"

void DMA(void)
{
	for (uint8_t i = 0; i < 0xA0u; i++)
		gb_write8((uint16_t)(0xFE00u + i),
			  gb_read8((uint16_t)(wOAM_ADDR + i)));
}
