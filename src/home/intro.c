#include "home/intro.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/load_animation.h"
#include "home/frames.h"
#include "home/intro_sequence_commands.h"
#include "home/load_gfx.h"
#include "home/sprite_animations.h"
#include "home/switch_rom.h"
#include "home/scenes.h"
#include "home/lcd_enable_frame.h"
#include "home/random.h"
#include "mem.h"
/* >>> factory statics */
#include "home/color.h"
#include "home/init_menu.h"
#include "home/lcd.h"
#include "home/sound.h"
#include "home/play_animation.h"
#define HANDLE_ALL_SPRITE_ANIMATIONS 0x3CB4u
#define INTRO_SEQUENCE 0x559Du
#define SCENE_TITLE_SCREEN 0x00u
#define MUSIC_TITLESCREEN 0x01u
#define PAD_A 0x01u
#define PAD_START 0x08u
/* <<< factory statics */

#define PALETTE_TITLE_SCREEN_ORBS 0x1eu
#define SPRITE_ANIM_ATTRIBUTES 1u
#define SPRITE_ANIM_COORD_X 2u
#define SPRITE_PRESS_START 0x6au
#define SPRITE_ANIM_190 0xbeu
#define SPRITE_ANIM_191 0xbfu
#define CONSOLE_CGB 0x02u

void LoadTitleScreenSprites(void)
{
    static const uint8_t sprites[] = {0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70, 0x71};
    uint16_t destination = wTitleScreenSprites_ADDR;

    gb_write8(wWhichOBP_ADDR, 0);
    gb_write8(wWhichOBPalIndex_ADDR, 0);
    LoadOBPalette(PALETTE_TITLE_SCREEN_ORBS);

    for (uint8_t index = 0; index < sizeof(sprites); index++) {
        CreateSpriteAndAnimBufferEntry(sprites[index], 0);
        gb_write8(destination, gb_read8(wWhichSprite_ADDR));
        destination++;
        uint16_t property = GetFirstSpriteAnimBufferProperty();
        property++;
        gb_write8(property, (uint8_t)(gb_read8(property) | index));
    }
}

/* intro.asm:55-73 .ShowPressStart */
static void ShowPressStart(void)
{
	CreateSpriteAndAnimBufferEntry(SPRITE_PRESS_START, 0u);
	uint16_t property = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	gb_write8(property, 48u);         /* x */
	gb_write8((uint16_t)(property + 1u), 112u); /* y */
	uint8_t anim = SPRITE_ANIM_190;
	if (wConsole == CONSOLE_CGB)
		anim = SPRITE_ANIM_191;
	Func_12ac9(anim, 60u); /* bc = 60 */
}


/* >>> factory PlayIntroSequence */
void PlayIntroSequence(void)
{
	DisableLCD();
	LoadConsolePaletteData();
	(void)InitMenuScreen();
	EnableAndClearSpriteAnimations();
	(void)SetDoFrameFunction(HANDLE_ALL_SPRITE_ANIMATIONS);
	LoadTitleScreenSprites();

	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)(INTRO_SEQUENCE & 0xffu));
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u), (uint8_t)(INTRO_SEQUENCE >> 8));
	wd317 = 0u;
	wIntroSequencePalsNeedUpdate = 0u;
	wSequenceDelay = 0u;
	(void)FlashWhiteScreen();
	if (!frame_boundary_is_installed()) {
		EnableLCD();
		return;
	}

	for (;;) {
		DoFrameIfLCDEnabled();
		(void)UpdateRNGSources();
		if ((hKeysPressed & (PAD_A | PAD_START)) != 0u) {
			if (AssertSongFinished() == 0u) {
				DisableLCD();
				PlaySong(MUSIC_TITLESCREEN);
				LoadOpeningScene(SCENE_TITLE_SCREEN, 0u, 0u);
				IntroSequenceEmptyFunc();
			}
			break;
		}
		if (wIntroSequencePalsNeedUpdate != 0u)
			Func_10d74();
		uint8_t saved_bank = hBankROM;
		BankswitchROM(7u);
		(void)ExecuteIntroSequenceCmd();
		BankswitchROM(saved_bank);
		if (wSequenceDelay == 0xFFu)
			break;
	}
	EnableAndClearSpriteAnimations();
	ShowPressStart(); /* intro.asm:51 .ShowPressStart */
	EnableLCD();
}
/* <<< factory PlayIntroSequence */

