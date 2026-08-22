#include "home/play_animation.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "home/duel_animation_core.h"

#define DUEL_SPECIAL_ANIMS 0x61u
#define BANK_LOAD_DUEL_ANIM_BUFFER 7u

#include "home/load_animation.h"
#define BANK_UPDATE_QUEUED_ANIMATIONS 7u

#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#include "home/switch_rom.h"
#include "home/load_animation.h"
/* <<< factory statics */

#define ANIMATION_QUEUE_LENGTH 7u
#define rQUEUE 0xD423u

AnimationStatusResult CheckAnyAnimationPlaying(void)
{
	uint8_t value = (uint8_t)(gb_read8(wActiveScreenAnim_ADDR) & gb_read8(wd4c0_ADDR));
	for (uint8_t i = 0; i < ANIMATION_QUEUE_LENGTH; i++)
		value = (uint8_t)(value & gb_read8((uint16_t)(rQUEUE + i)));

	uint8_t flags = 0x40u;
	if (value == 0xffu)
		flags |= 0x80u;
	else {
		flags |= 0x10u;
		if ((value & 0x0fu) < 0x0fu)
			flags |= 0x20u;
	}
	return (AnimationStatusResult){value, flags};
}
FrameFunctionResult SetDoFrameFunction(uint16_t hl)
{
	gb_write8(wDoFrameFunction_ADDR, (uint8_t)hl);
	gb_write8(wDoFrameFunction_ADDR + 1u, (uint8_t)(hl >> 8));
	return (FrameFunctionResult){(uint8_t)(hl >> 8), (uint8_t)((hl >> 8) ? 0 : 0x80), hl};
}

FrameFunctionResult ResetDoFrameFunction(uint16_t hl)
{
	SetDoFrameFunction(0);
	return (FrameFunctionResult){0, 0x80, hl};
}

/* >>> factory PlayDuelAnimation */
/* play_animation.asm:26-62 */
PlayDuelAnimationResult PlayDuelAnimation(uint8_t a)
{
	gb_write8(wTempAnimation_ADDR, a);
	uint8_t saved = gb_read8(hBankROM_ADDR);
	gb_write8(wDuelAnimReturnBank_ADDR, saved);

	BankswitchROM(BANK_LOAD_DUEL_ANIM_BUFFER);
	if (a < DUEL_SPECIAL_ANIMS
	    && gb_read8(wDuelAnimBufferCurPos_ADDR) == gb_read8(wDuelAnimBufferSize_ADDR)
	    && !(CheckAnyAnimationPlaying().f & 0x10u)) {
		PlayLoadedDuelAnimation();
	} else {
		LoadDuelAnimationToBuffer();
	}

	BankswitchROM(saved);
	return (PlayDuelAnimationResult){saved};
}
/* <<< factory PlayDuelAnimation */

/* >>> factory UpdateQueuedAnimations */
/* play_animation.asm:64-73 */
UpdateQueuedAnimationsResult UpdateQueuedAnimations(uint16_t hl)
{
	uint8_t saved = gb_read8(hBankROM_ADDR);
	BankswitchROM(BANK_UPDATE_QUEUED_ANIMATIONS);
	DuelAnimationUpdateResult result = _UpdateQueuedAnimations(hl);
	HandleAllSpriteAnimations();
	BankswitchROM(saved);
	return (UpdateQueuedAnimationsResult){saved, result.hl};
}
/* <<< factory UpdateQueuedAnimations */

/* >>> factory Func_3bb5 */
void Func_3bb5(void)
{
	gb_write8(wd4c0_ADDR, 0x00u);
	uint8_t saved_bank = gb_read8(hBankROM_ADDR);
	BankswitchROM(gb_read8(wDuelAnimReturnBank_ADDR));
	HandleAllSpriteAnimations();
	BankswitchROM(saved_bank);
	gb_write8(wd4c0_ADDR, 0x80u);
}
/* <<< factory Func_3bb5 */
