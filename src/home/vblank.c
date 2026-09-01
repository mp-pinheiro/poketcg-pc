#include "home/vblank.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/dma.h"
#include "home/indirect_dispatch.h"
#include "home/load_animation.h"
#include "home/palettes.h"
#include "home/setup.h"
#include "mem.h"

#define rLCDC 0xFF40u
#define rSCY  0xFF42u
#define rSCX  0xFF43u
#define rWY   0xFF4Au
#define rWX   0xFF4Bu

/* poketcg.sym (bank 0): the two targets the wVBlankFunctionTrampoline `jp`
 * carries — NoOp from SetupRegisters (src/home/setup.c) and
 * HandleAllSpriteAnimations from SetSpriteAnimationsAsVBlankFunction
 * (src/home/sprite_vblank.c). Anything else aborts through DispatchIndirect. */
#define TRAMPOLINE_NOOP 0x0348u
#define TRAMPOLINE_ALL_SPRITE_ANIMATIONS 0x3CB4u

/* poketcg/src/home/vblank.asm:2-38: the VBlankHandler body between the
 * register save/restore. The native host calls it once per frame from the
 * runtime loop (src/runtime.c) after DoFrame returns, so its work is visible
 * to game code exactly like the ROM's halt-return boundary. The
 * wReentrancyFlag guard (vblank.asm:9-12,37-38) protects against nested
 * interrupts, which the frame-batched host loop cannot produce, and the
 * wVBlankCounter++ stays in DoFrame (src/home/frames.c). */
void RuntimeVBlankHandler(void)
{
	/* vblank.asm:13-18: a nonzero wVBlankOAMCopyToggle requests one OAM
	 * copy through the HRAM DMA stub. The request is consumed by resetting
	 * the toggle to 0, not counted down — writers either store TRUE or inc
	 * it (sprite_animations.asm:32,171). */
	if (gb_read8(wVBlankOAMCopyToggle_ADDR) != 0u) {
		DMA();
		gb_write8(wVBlankOAMCopyToggle_ADDR, 0u);
	}

	/* vblank.asm:20-28: flush scaling/windowing parameters. */
	gb_write8(rSCX, gb_read8(hSCX_ADDR));
	gb_write8(rSCY, gb_read8(hSCY_ADDR));
	gb_write8(rWX, gb_read8(hWX_ADDR));
	gb_write8(rWY, gb_read8(hWY_ADDR));

	/* vblank.asm:29-31: flush LCDC. */
	gb_write8(rLCDC, gb_read8(wLCDC_ADDR));

	/* vblank.asm:33: `call wVBlankFunctionTrampoline` — a `jp nn` stub in
	 * WRAM whose target games rewrite (setup.asm:20-24, sprite_vblank.asm). */
	uint16_t target =
		(uint16_t)(gb_read8((uint16_t)(wVBlankFunctionTrampoline_ADDR + 1u)) |
			   (uint16_t)gb_read8((uint16_t)(wVBlankFunctionTrampoline_ADDR + 2u))
				   << 8);

	switch (target) {
	case TRAMPOLINE_NOOP:
		NoOp();
		return;
	case TRAMPOLINE_ALL_SPRITE_ANIMATIONS:
		HandleAllSpriteAnimations();
		return;
	default:
		DispatchIndirect("wVBlankFunction", target);
	}

	/* vblank.asm:34. */
	FlushPalettesIfRequested();
}
