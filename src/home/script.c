#include "home/script.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "home/switch_rom.h"
#include "home/duel_animation_core.h"
#include "home/objects.h"

#define TRUE 1u
#define BANK_ANIMATION_CORE 0x07u
/* <<< factory statics */

#define MAP_SCRIPTS_BANK 4u
#define MAP_SCRIPTS 0x562Au

/* script.asm:62-95. Entry l = script selector; the entry is
 * MapScripts + wCurMap * 16 + l in bank 4. The pointer is read there and the
 * routine's bank is restored, so the returned value is a plain address.
 * Exit carry is set iff the pointer is non-zero (`scf / ccf` double-negation),
 * and a is lo | hi of the pointer. */
MapScriptResult GetMapScriptPointer(uint8_t l)
{
	uint16_t entry = (uint16_t)(MAP_SCRIPTS + (uint16_t)wCurMap * 16u + l);
	const uint8_t *p = rom_ptr(MAP_SCRIPTS_BANK, entry);
	uint16_t ptr = (uint16_t)(p[0] | (uint16_t)p[1] << 8);

	uint8_t a = (uint8_t)((uint8_t)ptr | (uint8_t)(ptr >> 8));
	uint8_t f = 0x10u; /* carry set when found */
	if (a == 0)
		f = 0x80u; /* `or h` set Z, `scf`+`ccf` left carry clear */
	return (MapScriptResult){a, f, ptr};
}

/* >>> factory ResetAnimationQueue */
/* script.asm:145-153. Wraps _ResetAnimationQueue (duel_animation_core.asm,
 * bank 7) with a bankswitch, restoring the caller's ROM bank afterward. No
 * registers are read or produced: the asm never pushes bc/de/hl and the
 * final `pop af / call BankswitchROM / ret` only restores the bank latch. */
void ResetAnimationQueue(void)
{
	uint8_t bank = gb_read8(hBankROM_ADDR);
	BankswitchROM(BANK_ANIMATION_CORE);
	_ResetAnimationQueue();
	BankswitchROM(bank);
}
/* <<< factory ResetAnimationQueue */

/* >>> factory FinishQueuedAnimations */
/* script.asm:155-171. ClearAndDisableQueuedAnimations's exit carry (f&0x10)
 * means wDoFrameFunction did not hold the update handler; the asm's
 * `jr c, .skip_clear_frame_func` then leaves wDoFrameFunction untouched.
 * ZeroObjectPositions runs while still bankswitched to bank 7 in the asm
 * (it is a fixed-bank-0 routine, so that is safe) before the bank restore. */
void FinishQueuedAnimations(void)
{
	uint8_t bank = gb_read8(hBankROM_ADDR);
	BankswitchROM(BANK_ANIMATION_CORE);
	DuelAnimationResult r = ClearAndDisableQueuedAnimations();
	if (!(r.f & 0x10u)) {
		gb_write8(wDoFrameFunction_ADDR, 0u);
		gb_write8((uint16_t)(wDoFrameFunction_ADDR + 1u), 0u);
	}
	ZeroObjectPositions();
	gb_write8(wVBlankOAMCopyToggle_ADDR, TRUE);
	BankswitchROM(bank);
}
/* <<< factory FinishQueuedAnimations */
