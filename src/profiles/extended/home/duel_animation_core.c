/* >>> part BUFFER_ADDR */
#define BUFFER_ADDR wDuelAnimBuffer_ADDR
/* <<< part BUFFER_ADDR */
/* >>> part ANIMATIONS_BANK */
#define ANIMATIONS_BANK Animations_BANK
/* <<< part ANIMATIONS_BANK */
/* >>> part ANIM_ENTRY_SIZE */
#define ANIM_ENTRY_SIZE 5u
/* <<< part ANIM_ENTRY_SIZE */
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
    ClearSpriteVRAMBuffer();
    ZeroObjectPositions();
    write(wVBlankOAMCopyToggle_ADDR, 1u);
    const uint8_t *anim = rom_ptr(ANIMATIONS_BANK, (uint16_t)(ANIMATIONS_ADDR + (uint16_t)animation * ANIM_ENTRY_SIZE));
    uint8_t sprite_id  = anim[0];
    uint8_t palette_id = anim[1];
    uint8_t anim_id    = anim[2];
    uint8_t flags      = anim[3];
    uint8_t sfx_id     = anim[4];
    if (read(wAnimationsDisabled_ADDR) && !(flags & SPRITE_UNSKIPPABLE))
        return;
    if (sfx_id) PlaySFX(sfx_id);
    if (!sprite_id || !palette_id || !anim_id) return;
    CreateSpriteAndAnimBufferEntry(sprite_id, 0);
    write(QUEUE_ADDR, read(wWhichSprite_ADDR));
    write(wWhichOBP_ADDR, 0);
    write(wWhichOBPalIndex_ADDR, 0);
    LoadOBPalette(palette_id);
    write(wAnimFlags_ADDR, flags);
    if (flags & SPRITE_ANIM_FLAG_8x16)
        Set_OBJ_8x16();
    LoadAnimCoordsAndFlags();
    StartNewSpriteAnimation(anim_id);
}
/* <<< factory PlayLoadedDuelAnimation */
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
        Set_OBJ_8x8();
        PlayLoadedDuelAnimation();
        if (CheckAnyAnimationPlaying().f & 0x10u) break;
    }
    return read(wDuelAnimBufferCurPos_ADDR);
}
/* <<< part play_buffered_duel_animations */
/* === factory _UpdateQueuedAnimations */
