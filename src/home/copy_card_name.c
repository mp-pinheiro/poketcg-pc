#include "home/copy_card_name.h"

#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "mem.h"
#define TYPE_ENERGY 0x08u
#define TX_END 0x00u
#include "home/print_text.h"
#include "home/process_text.h"
#define TX_HALFWIDTH 0x06u
#define TX_SYMBOL 0x05u
#define SYM_Lv 0x11u
#define SYM_0 0x20u
#define FULLWIDTH_SPACE 0x70u
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

/* >>> factory _CopyCardNameAndLevel */
static uint16_t loaded_card1_name(void)
{
	return (uint16_t)(gb_read8(wLoadedCard1Name_ADDR)
			  | (uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8);
}

CopyCardNameAndLevelResult _CopyCardNameAndLevel(uint8_t a, uint8_t b, uint8_t c,
						 uint8_t d, uint8_t e)
{
	/* push bc / push de: both pairs come back at whichever exit runs, and the
	 * halfwidth tail jump hands them to the label that pops them there. */
	uint16_t caller_bc = (uint16_t)((uint16_t)b << 8 | c);
	uint16_t caller_de = (uint16_t)((uint16_t)d << 8 | e);
	wCardNameLength = a;
	(void)CopyText(loaded_card1_name(), wDefaultText_ADDR);
	if (gb_read8(wDefaultText_ADDR) == TX_HALFWIDTH)
		return _CopyCardNameAndLevel_HalfwidthText(caller_bc, caller_de);

	/* The name did not start with TX_HALFWIDTH. pret notes this never happens
	 * unless a caller rewrites wLoadedCard1Name, but the branch is real code. */
	uint8_t tiles = wCardNameLength;
	if (wLoadedCard1Type < TYPE_ENERGY) {
		uint8_t level = wLoadedCard1Level;
		if (level != 0u) {
			tiles = (uint8_t)(tiles + 2u);
			if (level >= 10u)
				tiles++; /* second digit */
		}
	}

	CopyTextResult copied = CopyText(loaded_card1_name(), wDefaultText_ADDR);
	/* `ld e, c` before the call, and GetTextLengthInHalfTiles pushes de at its
	 * own entry, so the `add e` that follows still sees the tile count. */
	TextLength measured = GetTextLengthInTiles(wDefaultText_ADDR);
	tiles = (uint8_t)(measured.a + tiles);
	/* `pop hl` at asm 0x4049 restores the de CopyText left, pushed just before
	 * the length call: that is where the padding starts. */
	uint16_t hl = (uint16_t)((uint16_t)copied.d << 8 | copied.e);
	uint16_t resume = hl;
	do {
		gb_write8(hl, FULLWIDTH_SPACE);
		hl++;
		tiles--;
	} while (tiles != 0u);
	gb_write8(hl, TX_END);
	hl = resume;

	uint8_t type = wLoadedCard1Type;
	if (type >= TYPE_ENERGY) {
		/* `cp TYPE_ENERGY` then `jr nc`: carry clear, subtract set, and the
		 * half-carry follows the low nibble of the comparison. */
		uint8_t f = (uint8_t)(0x40u
				      | (type == TYPE_ENERGY ? 0x80u : 0x00u)
				      | ((type & 0x0Fu) < TYPE_ENERGY ? 0x20u : 0x00u));
		return (CopyCardNameAndLevelResult){
			type, f,
			(uint8_t)(caller_bc >> 8), (uint8_t)caller_bc,
			(uint8_t)(caller_de >> 8), (uint8_t)caller_de, hl,
		};
	}
	uint8_t level = wLoadedCard1Level;
	if (level == 0u)
		return (CopyCardNameAndLevelResult){
			0u, 0x80u, /* `or a` on zero */
			(uint8_t)(caller_bc >> 8), (uint8_t)caller_bc,
			(uint8_t)(caller_de >> 8), (uint8_t)caller_de, hl,
		};

	gb_write8(hl, TX_SYMBOL);
	hl++;
	gb_write8(hl, SYM_Lv);
	hl++;
	a = level;
	if (a >= 10u) {
		gb_write8(hl, TX_SYMBOL);
		hl++;
		uint8_t tens = (uint8_t)(SYM_0 - 1u);
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
	}
	gb_write8(hl, TX_SYMBOL);
	hl++;
	a = (uint8_t)(a + SYM_0);
	gb_write8(hl, a);
	hl++;
	/* `add SYM_0` over a digit below ten: no zero, no half-carry, no carry. */
	return (CopyCardNameAndLevelResult){
		a, 0x00u,
		(uint8_t)(caller_bc >> 8), (uint8_t)caller_bc,
		(uint8_t)(caller_de >> 8), (uint8_t)caller_de, hl,
	};
}
/* <<< factory _CopyCardNameAndLevel */
