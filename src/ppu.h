#ifndef POKETCG_PPU_H
#define POKETCG_PPU_H

#include <stdint.h>

#ifndef SCREEN_W
#define SCREEN_W 160
#endif
#ifndef SCREEN_H
#define SCREEN_H 144
#endif
#ifndef TILEMAP_W
#define TILEMAP_W 32
#endif
#ifndef TILEMAP_H
#define TILEMAP_H 32
#endif

/* scroll.asm and credits.asm rewrite SCX/SCY mid-frame via LYC, so the
 * rasteriser reads scroll/window position per scanline instead of once per
 * frame; the eventual interrupt layer overwrites individual entries. */
typedef struct { uint8_t scx, scy; } BgOffset;
typedef struct { uint8_t wx, wy; } WinOffset;

typedef struct {
	BgOffset bg[SCREEN_H];
	WinOffset win[SCREEN_H];
	int win_line;
} Ppu;

void ppu_init_offsets(Ppu *p);
void ppu_render_scanline(Ppu *p, int ly, uint16_t *fb);
/* fb is SCREEN_W*SCREEN_H pixels of BGR555 (R:0-4, G:5-9, B:10-14). */
void ppu_render_frame(Ppu *p, uint16_t *fb);

#endif /* POKETCG_PPU_H */
