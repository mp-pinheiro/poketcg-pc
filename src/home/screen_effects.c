#include "home/screen_effects.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "mem.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/scroll.h"
#include "mem.h"

#define rSCX 0xFF43u
#define DEFAULT_SCREEN_ANIMATION_UPDATE_ADDR 0x4CBCu

#include "generated/wram.h"

#include "home/screen_effects.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#define SHAKE_SCREEN_X_UPDATE_FUNC_ADDR 0x4CFFu

#include "generated/wram.h"
#include "home/play_animation.h"
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

/* >>> factory DefaultScreenAnimationUpdate */
void DefaultScreenAnimationUpdate(void)
{
	gb_write8(wActiveScreenAnim_ADDR, 0xffu);
	DisableInt_LYCoincidence();
	gb_write8(hSCX_ADDR, 0u);
	gb_write8(rSCX, 0u);
	gb_write8(hSCY_ADDR, 0u);
	gb_write8(wScreenAnimUpdatePtr_ADDR,
	          (uint8_t)DEFAULT_SCREEN_ANIMATION_UPDATE_ADDR);
	gb_write8((uint16_t)(wScreenAnimUpdatePtr_ADDR + 1u),
	          (uint8_t)(DEFAULT_SCREEN_ANIMATION_UPDATE_ADDR >> 8));
}
/* <<< factory DefaultScreenAnimationUpdate */

/* >>> factory DoScreenAnimationUpdate */
void DoScreenAnimationUpdate(void)
{
	wScreenAnimDuration = 1u;
	DefaultScreenAnimationUpdate();
}
/* <<< factory DoScreenAnimationUpdate */

/* >>> factory LoadDefaultScreenAnimationUpdateWhenFinished */
void LoadDefaultScreenAnimationUpdateWhenFinished(void)
{
	if (wScreenAnimDuration != 0u)
		return;
	DefaultScreenAnimationUpdate();
}
/* <<< factory LoadDefaultScreenAnimationUpdateWhenFinished */

/* >>> factory ShakeScreenX */
void ShakeScreenX(uint16_t hl)
{
	gb_write8(wScreenShakeOffsetsPtr_ADDR, (uint8_t)hl);
	gb_write8((uint16_t)(wScreenShakeOffsetsPtr_ADDR + 1u), (uint8_t)(hl >> 8));
	gb_write8(wScreenAnimUpdatePtr_ADDR, (uint8_t)SHAKE_SCREEN_X_UPDATE_FUNC_ADDR);
	gb_write8((uint16_t)(wScreenAnimUpdatePtr_ADDR + 1u),
	          (uint8_t)(SHAKE_SCREEN_X_UPDATE_FUNC_ADDR >> 8));
}
/* <<< factory ShakeScreenX */

/* >>> factory Func_1ce03 */
void Func_1ce03(uint8_t a)
{
	uint16_t hl;
	if (a == 0x9eu) {
		hl = (uint16_t)(wDuelAnimDamage | ((uint16_t)gb_read8((uint16_t)(wDuelAnimDamage_ADDR + 1u)) << 8));
	} else {
		hl = 0u;
	}
	(void)hl;
	Func_3bb5();
}
/* <<< factory Func_1ce03 */
