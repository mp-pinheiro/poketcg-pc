#include "home/screen_effects.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "mem.h"
#include "generated/wram.h"
/* <<< factory statics */

/* >>> factory DecrementScreenAnimDuration */
/* screen_effects.asm:183-186
 * dec [hl] on wScreenAnimDuration; hl is left holding wScreenAnimDuration.
 * Z/N/H are the dec flags; carry is the one flag dec does not touch, so the
 * entry f (its C bit) is passed through to the exit byte. */
DecrementDurResult DecrementScreenAnimDuration(uint8_t f)
{
	uint8_t old = wScreenAnimDuration;
	uint8_t v = (uint8_t)(old - 1u);
	wScreenAnimDuration = v;
	uint8_t nf = (uint8_t)((f & 0x10u) | 0x40u |
	                       (v == 0u ? 0x80u : 0u) |
	                       ((old & 0x0fu) == 0u ? 0x20u : 0u));
	return (DecrementDurResult){(uint16_t)wScreenAnimDuration_ADDR, nf};
}
/* <<< factory DecrementScreenAnimDuration */
