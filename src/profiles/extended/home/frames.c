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

/* >>> part PAD_CTRL_PAD */
#define PAD_CTRL_PAD 0xF0u
#define PAD_BUTTONS 0x0Fu
#define PAD_SELECT 0x04u

/* Registered targets of wDoFrameFunction that this tree has a C body for. */
#define DO_FRAME_UPDATE_QUEUED_ANIMATIONS UpdateQueuedAnimations_ADDR
#define DO_FRAME_OVERWORLD OverworldDoFrameFunction_ADDR
#define DO_FRAME_FUNC_3E31 Func_3e31_ADDR
#define DO_FRAME_ALL_SPRITE_ANIMATIONS HandleAllSpriteAnimations_ADDR
#define DO_FRAME_NOOP NoOp_ADDR
/* <<< part PAD_CTRL_PAD */

/* >>> part g_frame_boundary_hook */
static FrameBoundaryHook g_frame_boundary_hook;
/* <<< part g_frame_boundary_hook */
/* >>> part g_frame_boundary_context */
static void *g_frame_boundary_context;
/* <<< part g_frame_boundary_context */
/* >>> part g_frame_watchdog */
static FrameBoundaryHook g_frame_watchdog;
/* <<< part g_frame_watchdog */
/* >>> part g_frame_watchdog_context */
static void *g_frame_watchdog_context;
/* <<< part g_frame_watchdog_context */
/* >>> part g_frame_anchor */
static FrameBoundaryHook g_frame_anchor;
/* <<< part g_frame_anchor */
/* >>> part g_frame_anchor_context */
static void *g_frame_anchor_context;
/* <<< part g_frame_anchor_context */
/* >>> part g_doframe_ordinal */
static uint32_t g_doframe_ordinal;
/* <<< part g_doframe_ordinal */
/* >>> part g_pending_service_passes */
static uint8_t g_pending_service_passes;
/* <<< part g_pending_service_passes */

/* >>> part frame_boundary_take_service_pass */
uint8_t frame_boundary_take_service_pass(void)
{
	uint8_t pending = g_pending_service_passes;

	if (pending != 0u)
		g_pending_service_passes = (uint8_t)(pending - 1u);
	return pending;
}
/* <<< part frame_boundary_take_service_pass */

/* >>> part frame_boundary_install */
void frame_boundary_install(FrameBoundaryHook hook, void *context)
{
	g_frame_boundary_hook = hook;
	g_frame_boundary_context = context;
}
/* <<< part frame_boundary_install */

/* >>> part frame_boundary_install_watchdog */
void frame_boundary_install_watchdog(FrameBoundaryHook hook, void *context)
{
	g_frame_watchdog = hook;
	g_frame_watchdog_context = context;
}
/* <<< part frame_boundary_install_watchdog */

/* >>> part frame_boundary_reach */
void frame_boundary_reach(void)
{
	if (g_frame_boundary_hook)
		g_frame_boundary_hook(g_frame_boundary_context);
	if (g_frame_watchdog)
		g_frame_watchdog(g_frame_watchdog_context);
}
/* <<< part frame_boundary_reach */
/* >>> part g_services_from_track */
/* Models VBlank services the reference delivers while game code is still
 * running, so no DoFrame completes around them: each count entry runs one
 * host SERVICE pass (ISR-equivalent work only -- RuntimeVBlankHandler; no
 * input re-sample, no frame counter, no timer/clock aging, no render) and
 * then bumps wVBlankCounter for the service itself (vblank.asm:35), with no
 * RNG advance. No-op in the probe world. The per-boot sites are annotated
 * where they call this. */
static int g_services_from_track;
/* <<< part g_services_from_track */
/* >>> part g_doframe_pass */
static int g_doframe_pass;
/* <<< part g_doframe_pass */

/* >>> part frame_boundary_pass_is_doframe */
int frame_boundary_pass_is_doframe(void)
{
	return g_doframe_pass;
}
/* <<< part frame_boundary_pass_is_doframe */

/* >>> part frame_boundary_services_from_track */
void frame_boundary_services_from_track(int enable)
{
	g_services_from_track = enable;
}
/* <<< part frame_boundary_services_from_track */

/* >>> part frame_boundary_consume_services */
void frame_boundary_consume_services(uint8_t count)
{
	if (!g_frame_boundary_hook || g_services_from_track)
		return;
	g_pending_service_passes = count;
	for (uint8_t i = 0; i < count; i++) {
		frame_boundary_reach();
		gb_write8(wVBlankCounter_ADDR,
		          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	}
	g_pending_service_passes = 0;
}
/* <<< part frame_boundary_consume_services */


/* >>> part frame_boundary_is_installed */
int frame_boundary_is_installed(void)
{
	return g_frame_boundary_hook != NULL;
}
/* <<< part frame_boundary_is_installed */

/* >>> part frame_boundary_doframe_ordinal */
uint32_t frame_boundary_doframe_ordinal(void)
{
	return g_doframe_ordinal;
}
/* <<< part frame_boundary_doframe_ordinal */

/* >>> part frame_boundary_reset_ordinal */
void frame_boundary_reset_ordinal(void)
{
	g_doframe_ordinal = 0;
}
/* <<< part frame_boundary_reset_ordinal */

/* >>> part frame_boundary_install_anchor */
void frame_boundary_install_anchor(FrameBoundaryHook hook, void *context)
{
	g_frame_anchor = hook;
	g_frame_anchor_context = context;
}
/* <<< part frame_boundary_install_anchor */

/* >>> part g_overread_hook */
static FrameOverreadHook g_overread_hook;
/* <<< part g_overread_hook */
/* >>> part g_overread_context */
static void *g_overread_context;
/* <<< part g_overread_context */

/* >>> part frame_boundary_install_overread */
void frame_boundary_install_overread(FrameOverreadHook hook, void *context)
{
	g_overread_hook = hook;
	g_overread_context = context;
}
/* <<< part frame_boundary_install_overread */

/* >>> part frame_boundary_overread */
int frame_boundary_overread(uint8_t *out, size_t length)
{
	if (!g_overread_hook)
		return 0;
	return g_overread_hook(g_overread_context, g_doframe_ordinal, out, length);
}
/* <<< part frame_boundary_overread */

/* >>> part g_timer_sync_hook */
static FrameBoundaryHook g_timer_sync_hook;
/* <<< part g_timer_sync_hook */
/* >>> part g_timer_sync_context */
static void *g_timer_sync_context;
/* <<< part g_timer_sync_context */

/* >>> part frame_boundary_install_timer_sync */
void frame_boundary_install_timer_sync(FrameBoundaryHook hook, void *context)
{
	g_timer_sync_hook = hook;
	g_timer_sync_context = context;
}
/* <<< part frame_boundary_install_timer_sync */

/* >>> part frame_boundary_timer_sync */
void frame_boundary_timer_sync(void)
{
	if (g_timer_sync_hook)
		g_timer_sync_hook(g_timer_sync_context);
}
/* <<< part frame_boundary_timer_sync */

/* >>> part g_busy_wait_hook */
static FrameBoundaryHook g_busy_wait_hook;
/* <<< part g_busy_wait_hook */
/* >>> part g_busy_wait_context */
static void *g_busy_wait_context;
/* <<< part g_busy_wait_context */

/* >>> part frame_boundary_install_busy_wait */
void frame_boundary_install_busy_wait(FrameBoundaryHook hook, void *context)
{
	g_busy_wait_hook = hook;
	g_busy_wait_context = context;
}
/* <<< part frame_boundary_install_busy_wait */

/* >>> part frame_boundary_busy_wait */
void frame_boundary_busy_wait(void)
{
	if (g_busy_wait_hook)
		g_busy_wait_hook(g_busy_wait_context);
	else
		SoundTimerHandler();
}
/* <<< part frame_boundary_busy_wait */

/* >>> part frame_boundary_isr_site */
void frame_boundary_isr_site(unsigned site)
{
	isr_on_site(site);
}
/* <<< part frame_boundary_isr_site */

/* >>> part g_vblank_sync_hook */
static FrameBoundaryHook g_vblank_sync_hook;
/* <<< part g_vblank_sync_hook */
/* >>> part g_vblank_sync_context */
static void *g_vblank_sync_context;
/* <<< part g_vblank_sync_context */

/* >>> part frame_boundary_install_vblank_sync */
void frame_boundary_install_vblank_sync(FrameBoundaryHook hook, void *context)
{
	g_vblank_sync_hook = hook;
	g_vblank_sync_context = context;
}
/* <<< part frame_boundary_install_vblank_sync */

/* >>> part frame_boundary_vblank_sync */
void frame_boundary_vblank_sync(void)
{
	if (g_vblank_sync_hook)
		g_vblank_sync_hook(g_vblank_sync_context);
}
/* <<< part frame_boundary_vblank_sync */

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

/* >>> factory HandleDPadRepeat */
/* frames.asm:45-65. hDPadHeld carries the d-pad only on the frame a
 * direction is pressed and on every frame the repeat counter runs out (24,
 * then 6); on the frames in between the `jr nz, .done` masks it back to the
 * newly pressed buttons, which is what makes a held direction step a menu
 * cursor at the repeat rate instead of every frame. */
uint16_t HandleDPadRepeat(uint16_t hl)
{
	uint8_t keys = gb_read8(hKeysHeld_ADDR);

	gb_write8(hDPadHeld_ADDR, keys);
	if (keys & PAD_CTRL_PAD) {
		hl = hDPadRepeat_ADDR;
		if (gb_read8(hKeysPressed_ADDR) & PAD_CTRL_PAD) {
			gb_write8(hDPadRepeat_ADDR, 24);
			return hl;
		}
		uint8_t repeat = (uint8_t)(gb_read8(hDPadRepeat_ADDR) - 1u);

		gb_write8(hDPadRepeat_ADDR, repeat);
		if (repeat == 0) {
			gb_write8(hDPadRepeat_ADDR, 6);
			return hl;
		}
	}
	gb_write8(hDPadHeld_ADDR,
	          (uint8_t)(gb_read8(hKeysPressed_ADDR) & PAD_BUTTONS));
	return hl;
}
/* <<< factory HandleDPadRepeat */

/* >>> part DoFrameDebugPause */
/* frames.asm:23-39: when wDebugPauseAllowed is set, pressing SELECT freezes
 * the game inside DoFrame until SELECT is pressed again. Each paused
 * iteration repeats DoFrame's vblank tail (WaitForVBlank, ReadJoypad,
 * HandleDPadRepeat) -- WaitForVBlank is the halt point, so it also keeps the
 * frame boundary reachable: the host keeps granting frames and pumping while
 * the game is paused. */
static void DoFrameDebugPause(void)
{
	for (;;) {
		g_doframe_pass = 1;
		frame_boundary_reach();
		g_doframe_pass = 0;
		if (!frame_boundary_is_installed())
			gb_write8(wVBlankCounter_ADDR,
			          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
		ReadJoypad();
		(void)HandleDPadRepeat(0u);
		if ((gb_read8(hKeysPressed_ADDR) & PAD_SELECT) != 0u)
			return;
	}
}
/* <<< part DoFrameDebugPause */

/* >>> factory DoFrame */
void DoFrame(void)
{
	CallDoFrameFunction();
	if (gb_read8(wDebugPauseAllowed_ADDR) != 0u &&
	    (gb_read8(hKeysPressed_ADDR) & PAD_SELECT) != 0u)
		DoFrameDebugPause();
	/* frames.asm:20-26 order: the body runs, then the halt waits out the
	 * VBlank -- whose ISR increments wVBlankCounter (vblank.asm:35) and
	 * services DMA/flushes (the host boundary pass) -- and only then does
	 * the tail (ReadJoypad, HandleDPadRepeat) poll the lines as of this
	 * vblank. */
	g_doframe_pass = 1;
	frame_boundary_reach();
	g_doframe_pass = 0;
	/* lcd.asm:2-16 WaitForVBlank: with wLCDC's enable bit clear there is
	 * no wait and no VBlank ISR, so the counter stands (PrintText's
	 * per-character DoFrames under a disabled LCD complete instantly on
	 * the ROM); the tail still polls the lines and the anchor still counts.
	 * Under a host the boundary pass is the ISR and keeps the counter
	 * (src/runtime.c vblank_service); the probe world has no ISR to run. */
	if (!frame_boundary_is_installed() && (gb_read8(wLCDC_ADDR) & 0x80u) != 0u)
		gb_write8(wVBlankCounter_ADDR,
		          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	ReadJoypad();
	(void)HandleDPadRepeat(0u);
	/* frames.asm $0552: the reference anchors its per-DoFrame state here. */
	serial_track_anchor();
	g_doframe_ordinal++;
	if (g_frame_anchor)
		g_frame_anchor(g_frame_anchor_context);
}
/* <<< factory DoFrame */

/* >>> part DoAFrames */
void DoAFrames(uint8_t a)
{
	uint16_t count = a ? a : 0x100u;

	while (count--)
		DoFrame();
}
/* <<< part DoAFrames */
