#include "ppu.h"

#include "mem.h"

enum {
	IO_LCDC = 0x40,
	IO_SCY  = 0x42,
	IO_SCX  = 0x43,
	IO_WY   = 0x4A,
	IO_WX   = 0x4B,
};

#define VRAM(bank, off) g_vram[(size_t)(bank) * 0x2000 + (size_t)(off)]

#define BG_MAP0 0x1800u
#define BG_MAP1 (BG_MAP0 + (TILEMAP_W * TILEMAP_H))

enum { COL0 = 0x01, BG_PRI = 0x02 };

static uint16_t pal_bg(int palette, int color)
{
	int i = palette * 8 + color * 2;
	return (uint16_t)((g_pal[i] | (g_pal[i + 1] << 8)) & 0x7FFF);
}

static uint16_t pal_obj(int palette, int color)
{
	int i = 0x40 + palette * 8 + color * 2;
	return (uint16_t)((g_pal[i] | (g_pal[i + 1] << 8)) & 0x7FFF);
}

static int fetch_bgwin_pixel(int mapx, int mapy, uint16_t map_base, uint8_t lcdc,
			     int *palette, int *bprio)
{
	int col = mapx & 7;
	int row = mapy & 7;
	int tile_addr = (int)map_base + ((mapy >> 3) % TILEMAP_H) * TILEMAP_W + (mapx >> 3) % TILEMAP_W;

	uint8_t tnum = VRAM(0, tile_addr);
	/* tiledata_select=0 selects the signed $8800 base; remap to the unsigned
	 * index over the 384-tile array. */
	int ti = (lcdc & 0x10) ? tnum : (tnum ^ 0x80) + 0x80;

	uint8_t attr = VRAM(1, tile_addr);
	int vbank = (attr >> 3) & 1;
	int hflip = (attr >> 5) & 1;
	int vflip = (attr >> 6) & 1;
	*palette = attr & 7;
	*bprio = (attr >> 7) & 1;

	int rr = vflip ? 7 - row : row;
	int cc = hflip ? 7 - col : col;
	int bit = 7 - cc;
	uint8_t b1 = VRAM(vbank, ti * 16 + rr * 2);
	uint8_t b2 = VRAM(vbank, ti * 16 + rr * 2 + 1);
	return ((b1 >> bit) & 1) | (((b2 >> bit) & 1) << 1);
}

static void render_sprites(int ly, uint8_t lcdc, uint16_t *fb, const uint8_t *ab)
{
	if (!(lcdc & 0x02))
		return;

	int sheight = (lcdc & 0x04) ? 16 : 8;
	int master = lcdc & 0x01;
	int idx = ly * SCREEN_W;

	int found[10];
	int nf = 0;
	for (int n = 0; n < 40; n++) {
		int sy = (int)g_oam[n * 4] - 16;
		if (sy <= ly && ly < sy + sheight) {
			found[nf++] = n;
			if (nf == 10)
				break;
		}
	}

	/* CGB priority is OAM order, lowest index on top; drawing highest index
	 * first makes the lowest-index sprite land last and win. */
	for (int k = nf - 1; k >= 0; k--) {
		int n = found[k];
		int sy = (int)g_oam[n * 4] - 16;
		int sx = (int)g_oam[n * 4 + 1] - 8;
		int tnum = g_oam[n * 4 + 2];
		if (sheight == 16)
			tnum &= 0xFE; /* 8x16 ignores the tile low bit */
		uint8_t attr = g_oam[n * 4 + 3];
		int xflip = attr & 0x20;
		int yflip = attr & 0x40;
		int sprio = attr & 0x80;
		int palette = attr & 0x07;
		int vbank = (attr >> 3) & 1;

		int dy = ly - sy;
		int yy = yflip ? sheight - dy - 1 : dy;
		uint8_t b1 = VRAM(vbank, tnum * 16 + yy * 2);
		uint8_t b2 = VRAM(vbank, tnum * 16 + yy * 2 + 1);

		for (int dx = 0; dx < 8; dx++) {
			int px = sx + dx;
			if (px < 0 || px >= SCREEN_W)
				continue;
			int color = ((b1 >> (7 - (xflip ? 7 - dx : dx))) & 1) |
				    (((b2 >> (7 - (xflip ? 7 - dx : dx))) & 1) << 1);
			if (color == 0)
				continue;

			uint8_t ba = ab[px];
			int draw;
			if (!master)
				draw = 1;
			else if (ba & BG_PRI)
				draw = (ba & COL0) != 0;
			else if (sprio)
				draw = (ba & COL0) != 0;
			else
				draw = 1;
			if (draw)
				fb[idx + px] = pal_obj(palette, color);
		}
	}
}

void ppu_render_scanline(Ppu *p, int ly, uint16_t *fb)
{
	uint8_t lcdc = g_io[IO_LCDC];
	int idx = ly * SCREEN_W;

	if (!(lcdc & 0x80)) {
		for (int x = 0; x < SCREEN_W; x++)
			fb[idx + x] = 0x7FFF;
		return;
	}

	uint8_t scx = p->bg[ly].scx;
	uint8_t scy = p->bg[ly].scy;
	int wx = (int)p->win[ly].wx - 7;
	int wy = p->win[ly].wy;
	int win_active = (lcdc & 0x20) && wy <= ly && wx < SCREEN_W;
	uint16_t bgmap = (lcdc & 0x08) ? BG_MAP1 : BG_MAP0;
	uint16_t winmap = (lcdc & 0x40) ? BG_MAP1 : BG_MAP0;

	uint8_t ab[SCREEN_W];

	if (win_active) {
		/* The window keeps its own line counter, advanced only on lines it
		 * actually draws; reset to -1 at the frame start so the first
		 * window line is row 0. */
		int wl = ++p->win_line;
		int pre = wx > 0 ? wx : 0;
		for (int x = 0; x < pre; x++) {
			int pal, bprio;
			int c = fetch_bgwin_pixel(x + scx, ly + scy, bgmap, lcdc, &pal, &bprio);
			fb[idx + x] = pal_bg(pal, c);
			ab[x] = (uint8_t)((bprio ? BG_PRI : 0) | (c == 0 ? COL0 : 0));
		}
		for (int x = pre; x < SCREEN_W; x++) {
			int pal, bprio;
			int c = fetch_bgwin_pixel(x - wx, wl, winmap, lcdc, &pal, &bprio);
			fb[idx + x] = pal_bg(pal, c);
			ab[x] = (uint8_t)((bprio ? BG_PRI : 0) | (c == 0 ? COL0 : 0));
		}
	} else {
		for (int x = 0; x < SCREEN_W; x++) {
			int pal, bprio;
			int c = fetch_bgwin_pixel(x + scx, ly + scy, bgmap, lcdc, &pal, &bprio);
			fb[idx + x] = pal_bg(pal, c);
			ab[x] = (uint8_t)((bprio ? BG_PRI : 0) | (c == 0 ? COL0 : 0));
		}
	}

	render_sprites(ly, lcdc, fb, ab);
}

void ppu_init_offsets(Ppu *p)
{
	uint8_t scx = g_io[IO_SCX];
	uint8_t scy = g_io[IO_SCY];
	uint8_t wx = g_io[IO_WX];
	uint8_t wy = g_io[IO_WY];
	for (int i = 0; i < SCREEN_H; i++) {
		p->bg[i].scx = scx;
		p->bg[i].scy = scy;
		p->win[i].wx = wx;
		p->win[i].wy = wy;
	}
	p->win_line = -1;
}

void ppu_render_frame(Ppu *p, uint16_t *fb)
{
	p->win_line = -1;
	for (int ly = 0; ly < SCREEN_H; ly++)
		ppu_render_scanline(p, ly, fb);
}
