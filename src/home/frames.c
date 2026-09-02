#include "home/frames.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/indirect_dispatch.h"
#include "home/input.h"
#include "home/load_animation.h"
#include "home/map.h"
#include "home/play_animation.h"
#include "home/serial.h"
#include "mem.h"

#define PAD_CTRL_PAD 0xF0u
#define PAD_BUTTONS 0x0Fu
#define PAD_SELECT 0x04u

/* Registered targets of wDoFrameFunction that this tree has a C body for. */
#define DO_FRAME_UPDATE_QUEUED_ANIMATIONS 0x3BA2u
#define DO_FRAME_OVERWORLD 0x380Eu
#define DO_FRAME_FUNC_3E31 0x3E31u
#define DO_FRAME_ALL_SPRITE_ANIMATIONS 0x3CB4u
#define DO_FRAME_LINK_OPPONENT_TURN 0x0F1Du
#define DO_FRAME_NOOP 0x0348u

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

int frame_boundary_is_installed(void)
{
	return g_frame_boundary_hook != NULL;
}

/* CallIndirect(wDoFrameFunction), poketcg/src/home/frames.asm:18-19 through
 * jumptable.asm:15-30: call the registered per-frame function unless the
 * pointer is NULL (DispatchIndirect treats zero as a no-op, matching
 * CallIndirect). Every non-NULL address stored anywhere in the asm is
 * registered below; an unregistered nonzero target fails loud.
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
		return;
	case DO_FRAME_OVERWORLD:
		OverworldDoFrameFunction();
		return;
	case DO_FRAME_FUNC_3E31:
		Func_3e31();
		return;
	case DO_FRAME_LINK_OPPONENT_TURN:
		/* engine/duel/core.asm:6405-6409 stores this target for the link
		 * opponent's turn (serial.asm:504-521). The asm's decided path
		 * reloads sp from wLinkOpponentTurnReturnAddress -- not expressible
		 * in C -- so the port models it as bank switch + carry inside the
		 * callee; the frame hook observes the serial-poll side effects. */
		(void)LinkOpponentTurnFrameFunction();
		return;
	case DO_FRAME_NOOP:
		/* home/jumptable.asm CallIndirect guard: NoOp ($0348) is the asm's
		 * canonical do-nothing per-frame function; several probe cases seed
		 * it explicitly. */
		return;
	default:
		DispatchIndirect("wDoFrameFunction", target);
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

/* frames.asm:23-39: when wDebugPauseAllowed is set, pressing SELECT freezes
 * the game inside DoFrame until SELECT is pressed again. Each paused
 * iteration repeats DoFrame's vblank tail (WaitForVBlank, ReadJoypad,
 * HandleDPadRepeat) -- WaitForVBlank is the halt point, so it also keeps the
 * frame boundary reachable: the host keeps granting frames and pumping while
 * the game is paused. */
static void DoFrameDebugPause(void)
{
	for (;;) {
		gb_write8(wVBlankCounter_ADDR,
		          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
		ReadJoypad();
		HandleDPadRepeat();
		frame_boundary_reach();
		if ((gb_read8(hKeysPressed_ADDR) & PAD_SELECT) != 0u)
			return;
	}
}

void DoFrame(void)
{
	CallDoFrameFunction();
	gb_write8(wVBlankCounter_ADDR,
	          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	ReadJoypad();
	HandleDPadRepeat();
	if (gb_read8(wDebugPauseAllowed_ADDR) != 0u &&
	    (gb_read8(hKeysPressed_ADDR) & PAD_SELECT) != 0u)
		DoFrameDebugPause();
	frame_boundary_reach();
}

void DoAFrames(uint8_t a)
{
	uint16_t count = a ? a : 0x100u;

	while (count--)
		DoFrame();
}
