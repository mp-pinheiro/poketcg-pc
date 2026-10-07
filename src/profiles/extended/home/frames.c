/* >>> part includes */
#include "home/frames.h"
#include "serial_track.h"
#include "isr.h"
#include "home/music.h"

#include "generated/hram.h"
#include "generated/rom.h"
#include "generated/wram.h"
#include "home/indirect_dispatch.h"
#include "home/input.h"
#include "home/load_animation.h"
#include "home/map.h"
#include "home/play_animation.h"
#include "mem.h"
/* <<< part includes */
/* --- part DO_FRAME_LINK_OPPONENT_TURN */
/* >>> part CallDoFrameFunction */
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
/* <<< part CallDoFrameFunction */
/* --- factory DoAFrames */
