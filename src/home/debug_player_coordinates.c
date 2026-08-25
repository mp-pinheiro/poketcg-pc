#include "home/debug_player_coordinates.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/debug_player_coordinates.h"
#include "home/load_animation.h"
#include "home/lcd.h"
#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define PAD_A 0x01u
#define PAD_B 0x02u
#define OWMODE_START_SCRIPT 0x02u
#define SCENE_COLOR_PALETTE 0x1Bu
#define WX_OFS 0x07u
/* <<< factory statics */

#define LCDC_WIN_ON 0x20u

void JumpSetWindowOff(void)
{
	gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_WIN_ON));
}

/* >>> factory Func_1c003 */
void Func_1c003(void)
{
	uint8_t held = wCurMap;
	if (held == 0u) {
		JumpSetWindowOff();
		return;
	}
	if (wOverworldMode >= OWMODE_START_SCRIPT) {
		JumpSetWindowOff();
		return;
	}
	held = hKeysHeld;
	uint8_t ab = (uint8_t)(held & (PAD_A | PAD_B));
	if (ab != held || (ab & PAD_B) == 0u) {
		JumpSetWindowOff();
		return;
	}
	uint8_t a = wPlayerXCoord;
	WriteOneByteNumberInTxSymbol_PadSpace(a, 0u, 0x20u, 0u, 0u, 0u);
	a = wPlayerYCoord;
	WriteOneByteNumberInTxSymbol_PadSpace(a, 0x03u, 0x20u, 0u, 0u, 0u);
	hWX = (uint8_t)(112u + WX_OFS);
	hWY = 136u;
	if ((hKeysPressed & PAD_A) != 0u) {
		(void)LoadScene(SCENE_COLOR_PALETTE, 0u, 33u, 0u, 0u, 0u, 0u);
	}
	if ((hKeysHeld & PAD_A) != 0u) {
		hWX = (uint8_t)(96u + WX_OFS);
		hWY = 104u;
	}
	SetWindowOn();
}
/* <<< factory Func_1c003 */
