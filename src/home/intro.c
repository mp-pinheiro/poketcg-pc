#include "home/intro.h"
#include "generated/wram.h"
#include "home/load_animation.h"
#include "home/load_gfx.h"
#include "home/sprite_animations.h"
#include "mem.h"
/* >>> factory statics */
#include "home/color.h"
#include "home/init_menu.h"
#include "home/lcd.h"
#include "home/play_animation.h"
#define HANDLE_ALL_SPRITE_ANIMATIONS 0x3CB4u
#define INTRO_SEQUENCE 0x559Du
/* <<< factory statics */

#define PALETTE_TITLE_SCREEN_ORBS 0x1eu
#define SPRITE_ANIM_ATTRIBUTES 1u

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
}
/* <<< factory PlayIntroSequence */
