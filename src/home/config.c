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

#define SYM_SPACE 0x00u

#include "home/sound.h"

#define SFX_CURSOR 0x01u

#include "generated/hram.h"
#include "home/overworld.h"

#define PAD_CTRL_PAD 0xF0u

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/config.h"
#include "home/lcd_enable_frame.h"
#include "home/text_box.h"
#include "home/init_menu.h"
#include "home/sound.h"
#include "home/labels.h"
#include "mem.h"
#define SFX_CONFIRM 0x02u
#define SINGLE_SPACED 0x01u
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

/* >>> factory HideConfigMenuCursor */
HideConfigMenuCursorResult HideConfigMenuCursor(uint8_t a, uint8_t b, uint8_t c)
{
	DrawConfigMenuCursor(SYM_SPACE, a);
	return (HideConfigMenuCursorResult){b, c};
}
/* <<< factory HideConfigMenuCursor */

/* >>> factory ConfigScreenDPadLeft */
void ConfigScreenDPadLeft(void)
{
	static const uint16_t kAddrs[3] = {
		wConfigMessageSpeedCursorPos_ADDR,
		wConfigDuelAnimationCursorPos_ADDR,
		wConfigExitSettingsCursorPos_ADDR,
	};
	static const uint8_t kMaxes[3] = {4u, 2u, 0u};
	uint8_t row = gb_read8(wConfigCursorYPos_ADDR);
	(void)HideConfigMenuCursor(row, 0u, 0u);
	uint16_t addr = kAddrs[row];
	uint8_t max = kMaxes[row];
	uint8_t current = gb_read8(addr);
	uint8_t new_val = (uint8_t)(current - 1u);
	if (new_val > max) {
		if (new_val < 0x80u)
			new_val = 0u;
		else
			new_val = max;
	}
	gb_write8(addr, new_val);
	if (max != 0u)
		PlaySFX(SFX_CURSOR);
	(void)ShowConfigMenuCursor(row, 0u, 0u);
	gb_write8(wCursorBlinkTimer_ADDR, 0u);
}
/* <<< factory ConfigScreenDPadLeft */

/* >>> factory ConfigScreenDPadRight */
void ConfigScreenDPadRight(void)
{
	static const uint16_t kAddrs[3] = {
		wConfigMessageSpeedCursorPos_ADDR,
		wConfigDuelAnimationCursorPos_ADDR,
		wConfigExitSettingsCursorPos_ADDR,
	};
	static const uint8_t kMaxes[3] = {4u, 2u, 0u};
	uint8_t row = gb_read8(wConfigCursorYPos_ADDR);
	(void)HideConfigMenuCursor(row, 0u, 0u);
	uint16_t addr = kAddrs[row];
	uint8_t max = kMaxes[row];
	uint8_t current = gb_read8(addr);
	uint8_t new_val = (uint8_t)(current + 1u);
	if (new_val > max) {
		if (new_val < 0x80u)
			new_val = 0u;
		else
			new_val = max;
	}
	gb_write8(addr, new_val);
	if (max != 0u)
		PlaySFX(SFX_CURSOR);
	(void)ShowConfigMenuCursor(row, 0u, 0u);
	gb_write8(wCursorBlinkTimer_ADDR, 0u);
}
/* <<< factory ConfigScreenDPadRight */

/* >>> factory UpdateConfigMenuCursor */
UpdateConfigMenuCursorResult UpdateConfigMenuCursor(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t timer = gb_read8(wCursorBlinkTimer_ADDR);
	if (timer & 0x10u) {
		HideConfigMenuCursorResult r = HideConfigMenuCursor(a, b, c);
		return (UpdateConfigMenuCursorResult){r.b, r.c};
	}
	ShowConfigMenuCursorResult r = ShowConfigMenuCursor(a, b, c);
	return (UpdateConfigMenuCursorResult){r.b, r.c};
}
/* <<< factory UpdateConfigMenuCursor */

/* >>> factory ConfigScreenDPadDown */
void ConfigScreenDPadDown(void)
{
	static const uint8_t kInitTimer[3] = {0x18u, 0x18u, 0x08u};
	uint8_t direction = 1u;
	uint8_t old_row = gb_read8(wConfigCursorYPos_ADDR);
	if (old_row == 2u)
		(void)HideConfigMenuCursor(old_row, 0u, 0u);
	else
		(void)ShowConfigMenuCursor(old_row, 0u, 0u);
	uint8_t new_row_candidate = (uint8_t)(direction + old_row);
	uint8_t new_row;
	if (new_row_candidate < 3u)
		new_row = new_row_candidate;
	else if (new_row_candidate == 3u)
		new_row = 0u;
	else
		new_row = 2u;
	gb_write8(wConfigCursorYPos_ADDR, new_row);
	uint8_t timer = kInitTimer[new_row];
	gb_write8(wCursorBlinkTimer_ADDR, timer);
	(void)UpdateConfigMenuCursor(new_row, 0u, 0u);
	PlaySFX(SFX_CURSOR);
}
/* <<< factory ConfigScreenDPadDown */

/* >>> factory ConfigScreenDPadUp */
void ConfigScreenDPadUp(void)
{
	static const uint8_t kInitTimer[3] = {0x18u, 0x18u, 0x08u};
	uint8_t direction = 0xFFu;
	uint8_t old_row = gb_read8(wConfigCursorYPos_ADDR);
	if (old_row == 2u)
		(void)HideConfigMenuCursor(old_row, 0u, 0u);
	else
		(void)ShowConfigMenuCursor(old_row, 0u, 0u);
	uint8_t new_row_candidate = (uint8_t)(direction + old_row);
	uint8_t new_row;
	if (new_row_candidate < 3u)
		new_row = new_row_candidate;
	else if (new_row_candidate == 3u)
		new_row = 0u;
	else
		new_row = 2u;
	gb_write8(wConfigCursorYPos_ADDR, new_row);
	uint8_t timer = kInitTimer[new_row];
	gb_write8(wCursorBlinkTimer_ADDR, timer);
	(void)UpdateConfigMenuCursor(new_row, 0u, 0u);
	PlaySFX(SFX_CURSOR);
}
/* <<< factory ConfigScreenDPadUp */

/* >>> factory ConfigScreenHandleDPadInput */
void ConfigScreenHandleDPadInput(void)
{
	if ((gb_read8(hDPadHeld_ADDR) & PAD_CTRL_PAD) == 0u)
		return;
	GetDirectionFromDPadResult direction = GetDirectionFromDPad(gb_read8(hDPadHeld_ADDR));
	switch (direction.a) {
	case 0u:
		ConfigScreenDPadUp();
		break;
	case 1u:
		ConfigScreenDPadRight();
		break;
	case 2u:
		ConfigScreenDPadDown();
		break;
	default:
		ConfigScreenDPadLeft();
		break;
	}
}
/* <<< factory ConfigScreenHandleDPadInput */

/* >>> factory _PauseMenu_Config */
void _PauseMenu_Config(void)
{
	uint8_t saved_wd291 = wd291;
	uint8_t saved_line_separation = wLineSeparation;
	uint16_t box_hl = 0;

	wConfigExitSettingsCursorPos = 0;
	wLineSeparation = SINGLE_SPACED;
	(void)InitMenuScreen();
	DrawRegularTextBox(&box_hl, 1, 20, 5, 0, 3);
	DrawRegularTextBox(&box_hl, 1, 20, 5, 0, 9);
	(void)PrintLabels(0, 0, 0);
	GetConfigCursorPositions();
	(void)ShowConfigMenuCursor(0, 0, 0);
	(void)ShowConfigMenuCursor(1, 0, 1);
	wCursorBlinkTimer = 0;
	(void)FlashWhiteScreen();

	for (;;) {
		uint8_t keys;

		DoFrameIfLCDEnabled();
		(void)UpdateConfigMenuCursor(wConfigCursorYPos, 0, 0);
		++wCursorBlinkTimer;
		ConfigScreenHandleDPadInput();
		keys = hKeysPressed;
		if (keys & 0x0Au)
			break;
		if (wConfigCursorYPos != 2u)
			continue;
		if (!(keys & 0x01u))
			continue;
		break;
	}

	PlaySFX(SFX_CONFIRM);
	SaveConfigSettings();
	wLineSeparation = saved_line_separation;
	wd291 = saved_wd291;
}
/* <<< factory _PauseMenu_Config */
