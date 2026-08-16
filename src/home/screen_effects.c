#include "home/screen_effects.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "mem.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "mem.h"
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

/* >>> factory UpdateShakeOffset */
/* screen_effects.asm:144-168 */
UpdateShakeOffsetResult UpdateShakeOffset(void)
{
	uint16_t ptr = (uint16_t)(gb_read8(wScreenShakeOffsetsPtr_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wScreenShakeOffsetsPtr_ADDR + 1u)) << 8));
	uint8_t duration = wScreenAnimDuration;
	uint8_t timer = gb_read8(ptr);

	if (duration >= timer) {
		uint8_t flags = 0x40u;
		if (duration == timer)
			flags |= 0x80u;
		if ((duration & 0x0fu) < (timer & 0x0fu))
			flags |= 0x20u;
		return (UpdateShakeOffsetResult){duration, flags, ptr};
	}

	uint16_t offset = (uint16_t)(ptr + 1u);
	uint16_t next = (uint16_t)(ptr + 2u);
	gb_write8(wScreenShakeOffsetsPtr_ADDR, (uint8_t)next);
	gb_write8((uint16_t)(wScreenShakeOffsetsPtr_ADDR + 1u), (uint8_t)(next >> 8));
	return (UpdateShakeOffsetResult){(uint8_t)(next >> 8), 0x10u, offset};
}
/* <<< factory UpdateShakeOffset */
