#include "home/water_club.h"

#include "mem.h"

#define W_ACTIVE_GAME_EVENT_ADDR 0xD0C2u
#define W_PLAYER_X_COORD_ADDR 0xD330u
#define W_PLAYER_Y_COORD_ADDR 0xD331u
#define W_LOAD_NPC_X_POS_ADDR 0xD3ACu
#define W_D3D0_ADDR 0xD3D0u

PreloadAmyResult Preload_Amy(void)
{
	uint8_t event = gb_read8(W_ACTIVE_GAME_EVENT_ADDR);
	uint8_t x = gb_read8(W_PLAYER_X_COORD_ADDR);
	uint8_t y = gb_read8(W_PLAYER_Y_COORD_ADDR);
	uint8_t a = 0;
	uint8_t f = 0x90u;

	gb_write8(W_D3D0_ADDR, 0);
	if (event != 0) {
		f = 0x10u;
		if (x == 0x14u) {
			if (y == 0x06u) {
				gb_write8(W_LOAD_NPC_X_POS_ADDR, 0x14u);
				gb_write8(W_D3D0_ADDR, 1);
				a = 1;
				f = 0x90u;
			} else {
				a = y;
			}
		} else {
			a = x;
		}
	}
	return (PreloadAmyResult){a, f};
}
