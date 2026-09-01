#ifndef POKETCG_HOME_VBLANK_H
#define POKETCG_HOME_VBLANK_H

/* Host counterpart of the ROM's VBlankHandler (poketcg/src/home/vblank.asm):
 * the runtime loop calls it once per frame, after DoFrame returns and before
 * the PPU samples the IO image. */
void RuntimeVBlankHandler(void);

#endif
