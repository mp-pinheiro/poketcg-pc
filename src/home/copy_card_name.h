#ifndef POKETCG_HOME_COPY_CARD_NAME_H
#define POKETCG_HOME_COPY_CARD_NAME_H

#include <stdint.h>

/* >>> factory _CopyCardNameAndLevel_HalfwidthText */
/* copy_card_name.asm:93. Reached only by `jp z` from inside _CopyCardNameAndLevel
 * (same file, line 17), which pushed bc then de at its own entry. This label's
 * epilogue (`pop hl; pop de; pop bc; ret`) therefore pops saves its caller made,
 * two frames up. Those two words are the explicit caller_bc/caller_de parameters
 * here, and a case declares them with the `stack` knob so the reference oracles
 * build the same frame; every other register is dead on entry. */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CopyCardNameAndLevelResult;

CopyCardNameAndLevelResult _CopyCardNameAndLevel_HalfwidthText(uint16_t caller_bc,
							       uint16_t caller_de);
/* <<< factory _CopyCardNameAndLevel_HalfwidthText */
#endif
