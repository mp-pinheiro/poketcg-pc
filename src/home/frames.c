#include "home/frames.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/input.h"
#include "home/intro_sequence_commands.h"
#include "home/load_animation.h"
#include "home/switch_rom.h"
#include "home/map.h"
#include "home/play_animation.h"
#include "mem.h"

#define PAD_CTRL_PAD 0xF0u
#define PAD_BUTTONS 0x0Fu

/* Registered targets of wDoFrameFunction that this tree has a C body for. */
#define DO_FRAME_UPDATE_QUEUED_ANIMATIONS 0x3BA2u
#define DO_FRAME_OVERWORLD 0x380Eu
#define INTRO_SEQUENCE_BANK 0x07u
#define DO_FRAME_FUNC_3E31 0x3E31u
#define DO_FRAME_ALL_SPRITE_ANIMATIONS 0x3CB4u

static FrameBoundaryHook g_frame_boundary_hook;
static void *g_frame_boundary_context;

void frame_boundary_install(FrameBoundaryHook hook, void *context)
{
	g_frame_boundary_hook = hook;
	g_frame_boundary_context = context;
}

void frame_boundary_reach(void)
{
	if (g_frame_boundary_hook)
		g_frame_boundary_hook(g_frame_boundary_context);
}

/* CallIndirect(wDoFrameFunction), poketcg/src/home/frames.asm:18-19 through
 * jumptable.asm:15-30: call the registered per-frame function unless the
 * pointer is NULL. CallIndirect reaches its target with `jp hl`, so the callee
 * sees hl holding its own address.
 *
 * Omitting this call made every native loop that waits for an animation spin
 * forever: ResetAnimationQueue registers UpdateQueuedAnimations here
 * (src/home/duel_animation_core.c), and without it CheckAnyAnimationPlaying
 * never stops reporting an animation in flight, so PlayDeckShuffleAnimation and
 * everything above it never returned under the probe.
 */
static void CallDoFrameFunction(void)
{
	uint16_t target = (uint16_t)(gb_read8(wDoFrameFunction_ADDR)
	                            | (uint16_t)gb_read8((uint16_t)(wDoFrameFunction_ADDR + 1u)) << 8);

	switch (target) {
	case DO_FRAME_UPDATE_QUEUED_ANIMATIONS:
		(void)UpdateQueuedAnimations(target);
		return;
	case DO_FRAME_ALL_SPRITE_ANIMATIONS:
		HandleAllSpriteAnimations();
		if (wSequenceCmdPtr != 0u ||
		    gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u)) != 0u) {
			uint8_t saved_bank = hBankROM;
			BankswitchROM(INTRO_SEQUENCE_BANK);
			(void)ExecuteIntroSequenceCmd();
			BankswitchROM(saved_bank);
		}
		return;
	case DO_FRAME_OVERWORLD:
		OverworldDoFrameFunction();
		return;
	case DO_FRAME_FUNC_3E31:
		Func_3e31();
		return;
	default:
		/* NULL, and any address whose routine is not ported yet: the asm
		 * returns immediately for NULL, and an unported target keeps the
		 * behaviour this port had before the dispatch existed. */
		return;
	}
}

void HandleDPadRepeat(void)
{
	uint8_t keys = gb_read8(hKeysHeld_ADDR);

	gb_write8(hDPadHeld_ADDR, keys);
	if (keys & PAD_CTRL_PAD) {
		if (gb_read8(hKeysPressed_ADDR) & PAD_CTRL_PAD) {
			gb_write8(hDPadRepeat_ADDR, 24);
			return;
		}
		uint8_t repeat = (uint8_t)(gb_read8(hDPadRepeat_ADDR) - 1u);

		gb_write8(hDPadRepeat_ADDR, repeat);
		if (repeat != 0)
			return;
		gb_write8(hDPadRepeat_ADDR, 6);
		return;
	}
	gb_write8(hDPadHeld_ADDR,
	          (uint8_t)(gb_read8(hKeysPressed_ADDR) & PAD_BUTTONS));
}

void DoFrame(void)
{
	CallDoFrameFunction();
	gb_write8(wVBlankCounter_ADDR,
	          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	ReadJoypad();
	HandleDPadRepeat();
	frame_boundary_reach();
}

void DoAFrames(uint8_t a)
{
	uint16_t count = a ? a : 0x100u;

	while (count--)
		DoFrame();
}
