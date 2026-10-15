/* >>> part includes */
#include "home/duel_animation_core.h"
#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/wram.h"
#include "home/load_animation.h"
#include "home/core.h"
#include "home/screen_effects.h"
#include "home/sprite_animations.h"
#include "home/load_gfx.h"
#include "home/sound.h"
#include "home/play_animation.h"
#include "mem.h"

#include "home/lcd.h"
/* <<< part includes */

/* >>> part QUEUE_ADDR */
#define QUEUE_ADDR wAnimationQueue_ADDR
/* <<< part QUEUE_ADDR */
/* >>> part QUEUE_LENGTH */
#define QUEUE_LENGTH 7u
/* <<< part QUEUE_LENGTH */
/* >>> part BUFFER_ADDR */
#define BUFFER_ADDR wDuelAnim1ID_ADDR
/* <<< part BUFFER_ADDR */
/* >>> part STRUCT_SIZE */
#define STRUCT_SIZE 8u
/* <<< part STRUCT_SIZE */
/* >>> part BUFFER_MASK */
#define BUFFER_MASK 0x7fu
/* <<< part BUFFER_MASK */
/* >>> part UPDATE_ADDR */
#define UPDATE_ADDR UpdateQueuedAnimations_ADDR
/* <<< part UPDATE_ADDR */
/* >>> part ANIMATIONS_BANK */
#define ANIMATIONS_BANK Animations_BANK
/* <<< part ANIMATIONS_BANK */
/* >>> part ANIMATIONS_ADDR */
#define ANIMATIONS_ADDR Animations_ADDR
/* <<< part ANIMATIONS_ADDR */
/* >>> part ANIM_ENTRY_SIZE */
#define ANIM_ENTRY_SIZE 6u
/* <<< part ANIM_ENTRY_SIZE */
/* >>> part SPRITE_UNSKIPPABLE */
#define SPRITE_UNSKIPPABLE 0x80u
/* <<< part SPRITE_UNSKIPPABLE */

/* >>> part read */
static uint8_t read(uint16_t addr) { return gb_read8(addr); }
/* <<< part read */
/* >>> part write */
static void write(uint16_t addr, uint8_t value) { gb_write8(addr, value); }
/* <<< part write */

/* >>> factory _ResetAnimationQueue */
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
/* <<< factory _ResetAnimationQueue */

/* >>> factory PlayLoadedDuelAnimation */
void PlayLoadedDuelAnimation(void)
{
    uint8_t lo = read(wDoFrameFunction_ADDR);
    uint8_t hi = read((uint16_t)(wDoFrameFunction_ADDR + 1u));
    if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))
        return;
    uint8_t animation = read(wTempAnimation_ADDR);
    write(wd4bf_ADDR, animation);
    /* core.asm:42-43: everything from DUEL_SPECIAL_ANIMS up -- the screen
     * shakes and distortions, the damage HUD, and the $96+ screen effects --
     * is handled by Func_1cb5e, not the sprite animation table. */
    if (animation >= DUEL_SPECIAL_ANIMS) {
        Func_1cb5e(animation);
        return;
    }
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
    LoadAnimCoordsAndFlags();
    StartNewSpriteAnimation(anim_id);
}
/* <<< factory PlayLoadedDuelAnimation */

/* >>> factory LoadDuelAnimationToBuffer */
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
/* <<< factory LoadDuelAnimationToBuffer */
/* >>> part play_buffered_duel_animations */
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
        AnimationStatusResult status = CheckAnyAnimationPlaying();
        if (status.f & 0x10u) return status.a;
    }
    return read(wDuelAnimBufferCurPos_ADDR);
}
/* <<< part play_buffered_duel_animations */

/* >>> factory _UpdateQueuedAnimations */
DuelAnimationUpdateResult _UpdateQueuedAnimations(uint8_t entry_c, uint16_t entry_hl)
{
    uint8_t active = read(wActiveScreenAnim_ADDR);
    if (active != 0xff) {
        /* core.asm:416-421: tick the screen animation; when it just ended,
         * the buffered animations resume this same frame. */
        uint16_t hl = CallScreenAnimationUpdate();
        active = read(wActiveScreenAnim_ADDR);
        if (active == 0xff)
            active = play_buffered_duel_animations();
        return (DuelAnimationUpdateResult){active, entry_c, hl};
    }
    uint8_t accumulator = read(wd4c0_ADDR);
    if (accumulator == 0x80) {
        write(wd4c0_ADDR, 0xff);
        uint8_t a = play_buffered_duel_animations();
        return (DuelAnimationUpdateResult){a, entry_c, entry_hl};
    }
    if (accumulator == 0)
        return (DuelAnimationUpdateResult){0, entry_c, entry_hl};
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
    return (DuelAnimationUpdateResult){accumulator, 0u, (uint16_t)(QUEUE_ADDR + QUEUE_LENGTH)};
}
/* <<< factory _UpdateQueuedAnimations */

/* >>> factory ClearAndDisableQueuedAnimations */
DuelAnimationResult ClearAndDisableQueuedAnimations(void)
{
    uint8_t lo = read(wDoFrameFunction_ADDR);
    uint8_t hi = read((uint16_t)(wDoFrameFunction_ADDR + 1u));
    if (lo != (uint8_t)UPDATE_ADDR || hi != (uint8_t)(UPDATE_ADDR >> 8))
        return (DuelAnimationResult){0, 0x10};
    write(wd4c0_ADDR, 0xff);
    if (read(wActiveScreenAnim_ADDR) != 0xff)
        DoScreenAnimationUpdate();
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
/* <<< factory ClearAndDisableQueuedAnimations */
