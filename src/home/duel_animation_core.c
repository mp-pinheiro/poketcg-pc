#include "home/duel_animation_core.h"
#include "generated/wram.h"
#include "home/sprite_animations.h"
#include "home/load_gfx.h"
#include "home/sound.h"
#include "home/play_animation.h"
#include "mem.h"
#include "home/lcd.h"

#define QUEUE_ADDR 0xd423u
#define QUEUE_LENGTH 7u
#define BUFFER_ADDR 0xd42cu
#define STRUCT_SIZE 8u
#define BUFFER_MASK 0x7fu
#define UPDATE_ADDR 0x3BA2u
#define DEFAULT_SCREEN_UPDATE_ADDR 0x4cbcu
#define ANIMATIONS_BANK 7u
#define ANIMATIONS_ADDR 0x4E32u
#define ANIM_ENTRY_SIZE 6u
#define SPRITE_UNSKIPPABLE 0x80u
#define SPRITE_CENTERED 0x04u
#define SPRITE_X_FLIP 0x01u
#define SPRITE_Y_FLIP 0x02u
#define SPRITE_X_INVERTED 0x10u
#define SPRITE_Y_INVERTED 0x20u

static uint8_t read(uint16_t addr) { return gb_read8(addr); }
static void write(uint16_t addr, uint8_t value) { gb_write8(addr, value); }

static uint8_t coord_index(void)
{
    uint8_t flags = read(wAnimFlags_ADDR);
    if (flags & SPRITE_CENTERED)
        return 0;
    uint8_t c = (uint8_t)(read(wDuelAnimationScreen_ADDR) * 12u);
    if (read(wDuelAnimDuelistSide_ADDR) != (uint8_t)(wPlayerDuelVariables_ADDR >> 8))
        c = (uint8_t)(c + 6u);
    return (uint8_t)(c + read(wDuelAnimLocationParam_ADDR));
}

static void GetAnimCoordsAndFlags(uint8_t *flags, uint8_t *x, uint8_t *y)
{
    static const uint8_t coords[][3] = {
        {88, 88, 4}, {40, 80, 0}, {136, 48, 0x33},
        {88, 72, 0}, {24, 96, 0}, {56, 96, 0}, {88, 96, 0},
        {120, 96, 0}, {152, 96, 0}, {88, 80, 0}, {152, 40, 0},
        {120, 40, 0}, {88, 40, 0}, {56, 40, 0}, {24, 40, 0}
    };
    uint8_t index = coord_index();
    if (index > 14u) index = 0;
    *x = coords[index][0];
    *y = coords[index][1];
    *flags = (uint8_t)(read(wAnimFlags_ADDR) & coords[index][2]);
}

static void LoadAnimCoordsAndFlags(uint8_t slot)
{
    uint16_t addr = (uint16_t)(wSpriteAnimBuffer_ADDR + (uint16_t)slot * 16u);
    uint8_t flags, x, y;
    GetAnimCoordsAndFlags(&flags, &x, &y);
    write((uint16_t)(addr + 1u), (uint8_t)(flags | (read((uint16_t)(addr + 1u)) & (SPRITE_X_FLIP | SPRITE_Y_FLIP))));
    write((uint16_t)(addr + 2u), x);
    write((uint16_t)(addr + 3u), y);
    write((uint16_t)(addr + 15u), (uint8_t)(flags | (read((uint16_t)(addr + 15u)) & (SPRITE_X_INVERTED | SPRITE_Y_INVERTED))));
}
static void DefaultScreenAnimationUpdate(void)
{
    write(wActiveScreenAnim_ADDR, 0xff);
    write(wScreenAnimUpdatePtr_ADDR, (uint8_t)DEFAULT_SCREEN_UPDATE_ADDR);
    write((uint16_t)(wScreenAnimUpdatePtr_ADDR + 1u),
          (uint8_t)(DEFAULT_SCREEN_UPDATE_ADDR >> 8));
}

static void EnableAndClearSpriteAnimations(void)
{
    write(wAllSpriteAnimationsDisabled_ADDR, 0);
    _ClearSpriteAnimations();
}


void _ResetAnimationQueue(void)
{
    Set_OBJ_8x8();
    write(wDoFrameFunction_ADDR, (uint8_t)UPDATE_ADDR);
    write((uint16_t)(wDoFrameFunction_ADDR + 1u),
          (uint8_t)(UPDATE_ADDR >> 8));
    for (uint8_t i = 0; i < QUEUE_LENGTH; i++)
        write((uint16_t)(QUEUE_ADDR + i), 0xff);
    write(wActiveScreenAnim_ADDR, 0xff);
    write(wd4c0_ADDR, 0xff);
    write(wDuelAnimBufferCurPos_ADDR, 0);
    write(wDuelAnimBufferSize_ADDR, 0);
    write(wDuelAnimSetScreen_ADDR, 0);
    DefaultScreenAnimationUpdate();
    EnableAndClearSpriteAnimations();
    return;
}

void PlayLoadedDuelAnimation(void)
{
    uint8_t lo = read(wDoFrameFunction_ADDR);
    uint8_t hi = read((uint16_t)(wDoFrameFunction_ADDR + 1u));
    if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))
        return;
    uint8_t animation = read(wTempAnimation_ADDR);
    write(wd4bf_ADDR, animation);
    if (animation >= 0x96u) return;
    if (animation == 0) return;
    const uint8_t *anim = rom_ptr(ANIMATIONS_BANK, ANIMATIONS_ADDR) + (uint16_t)animation * ANIM_ENTRY_SIZE;
    uint8_t sprite_id  = anim[0];
    uint8_t palette_id = anim[1];
    uint8_t anim_id    = anim[2];
    uint8_t flags      = anim[3];
    uint8_t sfx_id     = anim[4];
    if (!sprite_id || !palette_id || !anim_id) return;
    if (read(wAnimationsDisabled_ADDR) && !(flags & SPRITE_UNSKIPPABLE))
        return;
    if (sfx_id) PlaySFX(sfx_id);
    CreateSpriteAndAnimBufferEntry(sprite_id, 0);
    write(QUEUE_ADDR, read(wWhichSprite_ADDR));
    write(wWhichOBP_ADDR, 0);
    write(wWhichOBPalIndex_ADDR, 0);
    LoadOBPalette(palette_id);
    write(wAnimFlags_ADDR, flags);
    LoadAnimCoordsAndFlags(read(wWhichSprite_ADDR));
    StartNewSpriteAnimation(anim_id);
}

uint8_t LoadDuelAnimationToBuffer(void)
{
    uint8_t cur = read(wDuelAnimBufferCurPos_ADDR);
    uint8_t size = read(wDuelAnimBufferSize_ADDR);
    uint8_t next = (uint8_t)((size + STRUCT_SIZE) & BUFFER_MASK);
    if (next != cur) {
        write(wDuelAnimBufferSize_ADDR, next);
        uint16_t dst = (uint16_t)(BUFFER_ADDR + size);
        write(dst++, read(wTempAnimation_ADDR));
        write(dst++, read(wDuelAnimationScreen_ADDR));
        write(dst++, read(wDuelAnimDuelistSide_ADDR));
        write(dst++, read(wDuelAnimLocationParam_ADDR));
        write(dst++, read(wDuelAnimDamage_ADDR));
        write(dst++, read((uint16_t)(wDuelAnimDamage_ADDR + 1u)));
        write(dst++, read(wDuelAnimSetScreen_ADDR));
        write(dst, read(wDuelAnimReturnBank_ADDR));
    }
    return read(wDuelAnimReturnBank_ADDR);
}
static uint8_t play_buffered_duel_animations(void)
{
    for (;;) {
        uint8_t cur  = read(wDuelAnimBufferCurPos_ADDR);
        uint8_t size = read(wDuelAnimBufferSize_ADDR);
        if (cur == size) break;
        uint16_t src = (uint16_t)(BUFFER_ADDR + cur);
        write(wTempAnimation_ADDR, read(src));
        write(wDuelAnimationScreen_ADDR, read((uint16_t)(src + 1u)));
        write(wDuelAnimDuelistSide_ADDR, read((uint16_t)(src + 2u)));
        write(wDuelAnimLocationParam_ADDR, read((uint16_t)(src + 3u)));
        write(wDuelAnimDamage_ADDR, read((uint16_t)(src + 4u)));
        write((uint16_t)(wDuelAnimDamage_ADDR + 1u), read((uint16_t)(src + 5u)));
        write(wDuelAnimSetScreen_ADDR, read((uint16_t)(src + 6u)));
        write(wDuelAnimReturnBank_ADDR, read((uint16_t)(src + 7u)));
        write(wDuelAnimBufferCurPos_ADDR, (uint8_t)((cur + STRUCT_SIZE) & BUFFER_MASK));
        PlayLoadedDuelAnimation();
        if (CheckAnyAnimationPlaying().f & 0x10u) break;
    }
    return read(wDuelAnimBufferCurPos_ADDR);
}

DuelAnimationUpdateResult _UpdateQueuedAnimations(uint16_t entry_hl)
{
    uint8_t active = read(wActiveScreenAnim_ADDR);
    if (active != 0xff)
        return (DuelAnimationUpdateResult){active, entry_hl};
    uint8_t accumulator = read(wd4c0_ADDR);
    if (accumulator == 0x80) {
        write(wd4c0_ADDR, 0xff);
        uint8_t a = play_buffered_duel_animations();
        return (DuelAnimationUpdateResult){a, entry_hl};
    }
    if (accumulator == 0)
        return (DuelAnimationUpdateResult){0, entry_hl};
    for (uint8_t i = 0; i < QUEUE_LENGTH; i++) {
        uint16_t queue_addr = (uint16_t)(QUEUE_ADDR + i);
        uint8_t sprite = read(queue_addr);
        if (sprite != 0xff) {
            write(wWhichSprite_ADDR, sprite);
            if (GetSpriteAnimCounter() == 0xff) {
                DisableCurSpriteAnim();
                write(queue_addr, 0xff);
            }
        }
        accumulator &= read(queue_addr);
    }
    if (accumulator == 0xff)
        accumulator = play_buffered_duel_animations();
    return (DuelAnimationUpdateResult){accumulator, (uint16_t)(QUEUE_ADDR + QUEUE_LENGTH)};
}

DuelAnimationResult ClearAndDisableQueuedAnimations(void)
{
    uint8_t lo = read(wDoFrameFunction_ADDR);
    uint8_t hi = read((uint16_t)(wDoFrameFunction_ADDR + 1u));
    if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))
        return (DuelAnimationResult){0, 0x10};
    write(wd4c0_ADDR, 0xff);
    for (uint8_t i = 0; i < QUEUE_LENGTH; i++) {
        uint16_t queue_addr = (uint16_t)(QUEUE_ADDR + i);
        uint8_t sprite = read(queue_addr);
        if (sprite != 0xff) {
            write(wWhichSprite_ADDR, sprite);
            DisableCurSpriteAnim();
            write(queue_addr, 0xff);
        }
    }
    write(wDuelAnimBufferCurPos_ADDR, 0);
    write(wDuelAnimBufferSize_ADDR, 0);
    return (DuelAnimationResult){0, 0};
}
