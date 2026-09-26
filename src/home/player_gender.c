#include "home/player_gender.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/init_menu.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/process_text.h"
#include "home/random.h"
#include "home/sound.h"
#include "home/text_box.h"
#include "runtime.h"

#define PLAYER_PIC 0x01u
#define MINT_PIC 0x2Bu
#define TILEMAP_PLAYER 0x62u
#define TILEMAP_OPPONENT 0x63u
#define SYM_CURSOR_R 0x0Fu
#define SYM_SPACE 0x00u
#define PAD_A 0x01u
#define PAD_LEFT 0x20u
#define PAD_RIGHT 0x10u
#define SFX_CURSOR 0x01u
#define SFX_CONFIRM 0x02u

static void print_host_text(const char *text, uint8_t d, uint8_t e)
{
	uint16_t ptr = wDefaultText_ADDR;
	gb_write8(ptr++, 0x06u);
	while (*text)
		gb_write8(ptr++, (uint8_t)*text++);
	gb_write8(ptr, 0u);
	InitTextPrinting(d, e);
	ptr = wDefaultText_ADDR;
	(void)ProcessText(&ptr);
}

static void draw_cursor(uint8_t x)
{
	(void)WriteByteToBGMap0(SYM_CURSOR_R, x, 3u);
}

void PlayerGenderSelection(void)
{
	uint16_t box = 0u;
	uint8_t selected = 0u;
	DisableLCD();
	(void)InitMenuScreen();
	EnableAndClearSpriteAnimations();
	(void)SetupText(0x38u, 0xBFu);
	DrawRegularTextBox(&box, 0u, 20u, 18u, 0u, 0u);
	print_host_text("ARE YOU A BOY OR A GIRL?", 2u, 1u);
	print_host_text("BOY", 4u, 3u);
	print_host_text("GIRL", 14u, 3u);
	wCurPortrait = PLAYER_PIC;
	DrawPortrait(TILEMAP_PLAYER, 2u, 5u);
	wCurPortrait = MINT_PIC;
	DrawPortrait(TILEMAP_OPPONENT, 12u, 5u);
	draw_cursor(3u);
	(void)FlashWhiteScreen();
	for (;;) {
		DoFrameIfLCDEnabled();
		(void)UpdateRNGSources();
		uint8_t held = hDPadHeld;
		if ((hKeysPressed & PAD_A) != 0u) {
			PlaySFX(SFX_CONFIRM);
			runtime_set_player_gender(selected != 0u);
			return;
		}
		if ((held & (PAD_LEFT | PAD_RIGHT)) == 0u)
			continue;
		selected ^= 1u;
		(void)WriteByteToBGMap0(SYM_SPACE, selected ? 3u : 13u, 3u);
		draw_cursor(selected ? 13u : 3u);
		PlaySFX(SFX_CURSOR);
	}
}
