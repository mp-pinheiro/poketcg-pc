#include "home/config.h"

#include "generated/wram.h"

#include "home/bg_map.h"
/* >>> factory statics */
#include "home/switch_sram.h"
#include "home/config.h"

#define SYM_CURSOR_R 0x01u
#define sTextSpeed_ADDR_L 0xA006u
#define sAnimationsDisabled_ADDR_L 0xA007u
#define sSkipDelayAllowed_ADDR_L 0xA009u

/* config.asm:158-161 TextDelaySettings (TEXT_SPEED_1..TEXT_SPEED_5) */
static const uint8_t kTextDelaySettings[5] = { 0x06u, 0x04u, 0x02u, 0x01u, 0x00u };

/* config.asm:99-104 DuelAnimationSettingsIndices */
static const uint8_t kDuelAnimationSettingsIndices[4] = { 0u, 0u, 1u, 2u };

/* config.asm:150-155 DuelAnimationSettings: animations disabled, skip delay allowed */
static const uint8_t kDuelAnimationSettings[8] = {
	0x00u, 0x00u, 0x00u, 0x01u, 0x01u, 0x01u, 0x00u, 0x00u
};

#include "home/config.h"
/* <<< factory statics */

void DrawConfigMenuCursor(uint8_t a, uint8_t c)
{
	uint8_t cursor;
	uint8_t x;
	uint8_t y;

	switch (c) {
	case 0:
		cursor = wConfigMessageSpeedCursorPos;
		x = (uint8_t)(5u + (uint8_t)(cursor << 1));
		y = 6;
		break;
	case 1:
		cursor = wConfigDuelAnimationCursorPos;
		if (cursor == 0)
			x = 1;
		else if (cursor == 1)
			x = 7;
		else
			x = 15;
		y = 12;
		break;
	default:
		cursor = wConfigExitSettingsCursorPos;
		x = 1;
		y = 16;
		break;
	}
	WriteByteToBGMap0(a, x, y);
}

/* >>> factory GetConfigCursorPositions */
/* config.asm:71-97 */
void GetConfigCursorPositions(void)
{
	EnableSRAM();
	uint8_t c = 0;
	while (gb_read8(sTextSpeed_ADDR_L) < kTextDelaySettings[c]) {
		c++;
		if (c >= 4u)
			break;
	}
	wConfigMessageSpeedCursorPos = c;
	uint8_t idx = (uint8_t)(((gb_read8(sSkipDelayAllowed_ADDR_L) & 0x01u) << 1)
		| (uint8_t)(wAnimationsDisabled & 0x01u));
	wConfigDuelAnimationCursorPos = kDuelAnimationSettingsIndices[idx];
	DisableSRAM();
}
/* <<< factory GetConfigCursorPositions */

/* >>> factory SaveConfigSettings */
/* config.asm:113-148 */
void SaveConfigSettings(void)
{
	EnableSRAM();
	uint8_t c = (uint8_t)((wConfigDuelAnimationCursorPos & 0x03u) << 1);
	uint8_t anim = kDuelAnimationSettings[c];
	wAnimationsDisabled = anim;
	gb_write8(sAnimationsDisabled_ADDR_L, anim);
	gb_write8(sSkipDelayAllowed_ADDR_L, kDuelAnimationSettings[c + 1u]);
	DisableSRAM();
	uint8_t speed = kTextDelaySettings[wConfigMessageSpeedCursorPos & 0x07u];
	EnableSRAM();
	gb_write8(sTextSpeed_ADDR_L, speed);
	wTextSpeed = speed;
	DisableSRAM();
}
/* <<< factory SaveConfigSettings */

/* >>> factory ShowConfigMenuCursor */
ShowConfigMenuCursorResult ShowConfigMenuCursor(uint8_t a, uint8_t b, uint8_t c)
{
	DrawConfigMenuCursor(SYM_CURSOR_R, a);
	return (ShowConfigMenuCursorResult){b, c};
}
/* <<< factory ShowConfigMenuCursor */
