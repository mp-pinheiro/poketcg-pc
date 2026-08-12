#include "home/intro.h"
#include "generated/wram.h"
#include "home/load_animation.h"
#include "home/load_gfx.h"
#include "home/sprite_animations.h"
#include "mem.h"

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
