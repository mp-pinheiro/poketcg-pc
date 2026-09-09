#ifndef POKETCG_HOME_VBLANK_H
#define POKETCG_HOME_VBLANK_H

/* Host counterpart of the ROM's VBlankHandler (poketcg/src/home/vblank.asm):
 * the runtime loop calls it once per frame, after DoFrame returns and before
 * the PPU samples the IO image. */
void RuntimeVBlankHandler(void);

/* The LCDC (STAT) interrupt: home.asm:34-36 `call wLCDCFunctionTrampoline`
 * whenever LY reaches rLYC with the coincidence interrupt armed
 * (EnableInt_LYCoincidence). The runtime loop calls it once per VBlank
 * service, before the handler, for the frame that just ended: line 0 for
 * ApplyBackgroundScroll, which then owns lines 0-$5F and rearms LYC=0; a
 * walking LYC for the credits' Func_3e44, which rearms at the next table
 * line until the table wraps. Every rearm forward within the frame is
 * followed, so the per-frame handler count matches the ROM's. */
void RuntimeLCDCHandler(void);
int RuntimeLCDCHandlerOnce(void);

#endif
