#include "home/copy_card_name.h"

#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "mem.h"
#define TYPE_ENERGY 0x08u
#define TX_END 0x00u
/* <<< factory statics */

/* >>> factory _CopyCardNameAndLevel_HalfwidthText */
CopyCardNameAndLevelResult _CopyCardNameAndLevel_HalfwidthText(uint16_t caller_bc,
							       uint16_t caller_de)
{
	/* b counts the tiles still to pad: 2 * (wCardNameLength + 1). */
	uint8_t b = (uint8_t)((uint8_t)(wCardNameLength + 1u) << 1);
	uint16_t hl = wDefaultText_ADDR;
	uint8_t a;
	do {
		b--;
		a = gb_read8(hl);
		hl++;
	} while (a != 0u);
	hl--; /* land on the TX_END the name copy left behind */

	uint8_t c = 0u;
	uint8_t level = 0u;
	int append_level = 0;
	if (wLoadedCard1Type < TYPE_ENERGY) {
		level = wLoadedCard1Level;
		append_level = level != 0u;
	}
	if (append_level) {
		c = level;
		gb_write8(hl, (uint8_t)' ');
		hl++;
		b--;
		gb_write8(hl, (uint8_t)'L');
		hl++;
		b--;
		gb_write8(hl, (uint8_t)'v');
		hl++;
		b--;
		a = c;
		if (a >= 10u) {
			/* `ld b, '0' - 1` / inc-and-subtract: b becomes the tens
			 * digit, a the remainder. The real code brackets this in
			 * push bc / pop bc, so the pad counter survives it. */
			uint8_t tens = (uint8_t)('0' - 1u);
			for (;;) {
				tens++;
				uint8_t previous = a;
				a = (uint8_t)(a - 10u);
				if (previous < 10u)
					break;
			}
			a = (uint8_t)(a + 10u);
			gb_write8(hl, tens);
			hl++;
			c = a;
			b--;
		}
		a = (uint8_t)(c + (uint8_t)'0');
		gb_write8(hl, a);
		hl++;
		b--;
	}

	uint16_t resume = hl;
	a = (uint8_t)' ';
	do {
		gb_write8(hl, a);
		hl++;
		b--;
	} while (b != 0u);
	gb_write8(hl, TX_END);
	hl = resume;

	/* The loop above can only exit through `dec b` reaching zero, so Z and the
	 * subtract flag are set and the half-carry is clear. Carry is untouched by
	 * dec/inc, and every path into the loop leaves it clear: the energy exit
	 * took `jr nc`, the level-zero exit ran `or a`, and both digit paths end on
	 * `add '0'` over a value below ten. */
	uint8_t f = 0xC0u;
	return (CopyCardNameAndLevelResult){
		a, f,
		(uint8_t)(caller_bc >> 8), (uint8_t)caller_bc,
		(uint8_t)(caller_de >> 8), (uint8_t)caller_de,
		hl,
	};
}
/* <<< factory _CopyCardNameAndLevel_HalfwidthText */
