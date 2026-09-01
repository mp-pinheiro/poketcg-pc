#include "home/dma.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
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
	/* home/dma.asm:15-22 DMA, bytes $05A1-$05AA: `ld a,HIGH(wOAM);
	 * ldh [rDMA],a; ld a,40; dec a; jr nz,-3; ret`. Literal bytes so the
	 * product build never depends on a data-pack span for bank 0. */
	static const uint8_t dma_stub[] = {0x3E, 0xCA, 0xE0, 0x46, 0x3E,
					   0x28, 0x3D, 0x20, 0xFD, 0xC9};
	for (uint8_t i = 0u; i < DMA_COPY_LENGTH; i++)
		gb_write8((uint16_t)(hDMAFunction_ADDR + i), dma_stub[i]);
}
/* <<< factory CopyDMAFunction */
