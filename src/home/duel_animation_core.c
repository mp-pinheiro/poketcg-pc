#include "home/duel_animation_core.h"
#include "generated/wram.h"
#include "home/sprite_animations.h"
#include "mem.h"

#define QUEUE_ADDR 0xd423u
#define QUEUE_LENGTH 7u
#define BUFFER_ADDR 0xd42cu
#define STRUCT_SIZE 8u
#define BUFFER_MASK 0x7fu
#define UPDATE_ADDR 0x4ac5u
#define DEFAULT_SCREEN_UPDATE_ADDR 0x4cbcu
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

DuelAnimationResetResult _ResetAnimationQueue(void)
{
    uint8_t lcdc = read(wLCDC_ADDR);
    write(wLCDC_ADDR, (uint8_t)(lcdc & (uint8_t)~0x04u));
    for (uint8_t i = 0; i < QUEUE_LENGTH; i++) write((uint16_t)(QUEUE_ADDR + i), 0xff);
    write(wActiveScreenAnim_ADDR, 0xff);
    write(wd4c0_ADDR, 0xff);
    write(wDuelAnimBufferCurPos_ADDR, 0);
    write(wDuelAnimBufferSize_ADDR, 0);
    write(wDuelAnimSetScreen_ADDR, 0);
    write(wScreenAnimUpdatePtr_ADDR, (uint8_t)DEFAULT_SCREEN_UPDATE_ADDR);
    write((uint16_t)(wScreenAnimUpdatePtr_ADDR + 1u),
          (uint8_t)(DEFAULT_SCREEN_UPDATE_ADDR >> 8));
    write(wDoFrameFunction_ADDR, (uint8_t)UPDATE_ADDR);
    write((uint16_t)(wDoFrameFunction_ADDR + 1u),
          (uint8_t)(UPDATE_ADDR >> 8));
    write(wAllSpriteAnimationsDisabled_ADDR, 0);
    write(wVBlankOAMCopyToggle_ADDR,
          (uint8_t)(read(wVBlankOAMCopyToggle_ADDR) + 1u));
    return (DuelAnimationResetResult){ .c = 0 };
}

void PlayLoadedDuelAnimation(void)
{
    uint8_t lo = read(wDoFrameFunction_ADDR);
    uint8_t hi = read((uint16_t)(wDoFrameFunction_ADDR + 1u));
    if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))
        return;
    write(wd4bf_ADDR, read(wTempAnimation_ADDR));
    if (read(wTempAnimation_ADDR) >= 0x96u)
        return;
    uint8_t animation = read(wTempAnimation_ADDR);
    if (animation == 0) return;
    uint8_t flags = read((uint16_t)(0xd42cu + 3u));
    if (read(wAnimationsDisabled_ADDR) && !(flags & SPRITE_UNSKIPPABLE))
        return;
    write(QUEUE_ADDR, read(wWhichSprite_ADDR));
    write(wAnimFlags_ADDR, flags);
    LoadAnimCoordsAndFlags(read(wWhichSprite_ADDR));
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

DuelAnimationUpdateResult _UpdateQueuedAnimations(void)
{
    uint8_t active = read(wActiveScreenAnim_ADDR);
    if (active != 0xff)
        return (DuelAnimationUpdateResult){active};
    uint8_t accumulator = read(wd4c0_ADDR);
    if (accumulator == 0x80) {
        write(wd4c0_ADDR, 0xff);
        return (DuelAnimationUpdateResult){0xff};
    }
    if (accumulator == 0)
        return (DuelAnimationUpdateResult){0};
    for (uint8_t i = 0; i < QUEUE_LENGTH; i++) {
        uint16_t queue_addr = (uint16_t)(QUEUE_ADDR + i);
        uint8_t sprite = read(queue_addr);
        if (sprite != 0xff) {
            uint16_t slot = (uint16_t)(wSpriteAnimBuffer_ADDR + (uint16_t)sprite * 16u);
            write(wWhichSprite_ADDR, sprite);
            if (read((uint16_t)(slot + 14u)) == 0xff) {
                if (read(wAllSpriteAnimationsDisabled_ADDR) == 0)
                    write(slot, 0);
                write(queue_addr, 0xff);
            }
        }
        accumulator &= read(queue_addr);
    }
    return (DuelAnimationUpdateResult){accumulator};
}

DuelAnimationResult ClearAndDisableQueuedAnimations(void)
{
    uint8_t lo = read(wDoFrameFunction_ADDR);
    uint8_t hi = read((uint16_t)(wDoFrameFunction_ADDR + 1u));
    if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))
        return (DuelAnimationResult){0, 0x10};
    write(wd4c0_ADDR, 0xff);
    for (uint8_t i = 0; i < QUEUE_LENGTH; i++) write((uint16_t)(QUEUE_ADDR + i), 0xff);
    write(wDuelAnimBufferCurPos_ADDR, 0);
    write(wDuelAnimBufferSize_ADDR, 0);
    return (DuelAnimationResult){0, 0};
}
