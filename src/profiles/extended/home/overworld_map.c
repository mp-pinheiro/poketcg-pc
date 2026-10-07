/* >>> factory OverworldMap_InitVolcanoSprite */
void OverworldMap_InitVolcanoSprite(uint8_t f)
{
	(void)CreateSpriteAndAnimBufferEntry(SPRITE_OW_MAP_OAM, f);
	uint16_t coords = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	gb_write8(coords, 0x80u);
	gb_write8((uint16_t)(coords + 1u), 0x10u);
	StartNewSpriteAnimation(SPRITE_ANIM_VOLCANO_SMOKE);
}
/* <<< factory OverworldMap_InitVolcanoSprite */
/* >>> factory OverworldMap_InitCursorSprite */
void OverworldMap_InitCursorSprite(void)
{
	wOverworldMapStartingPosition = wOverworldMapSelection;
	wOverworldMapPlayerAnimationState = 0u;
	(void)CreateSpriteAndAnimBufferEntry(SPRITE_OW_MAP_OAM, 0x80u);
	wOverworldMapCursorSprite = wWhichSprite;
	wOverworldMapCursorAnimation = SPRITE_ANIM_OWMAP_CURSOR;
	StartNewSpriteAnimation(SPRITE_ANIM_OWMAP_CURSOR);
	if (GetEventValue(EVENT_MASON_LAB_STATE) == 0u) {
		uint16_t flags = GetSpriteAnimBufferProperty(SPRITE_ANIM_FLAGS);
		gb_write8(flags, (uint8_t)(gb_read8(flags) | (uint8_t)(1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)));
	}
}
/* <<< factory OverworldMap_InitCursorSprite */
/* >>> factory OverworldMap_PrintMapName */
void OverworldMap_PrintMapName(void)
{
	InitTextPrinting(1u, 1u);
	const uint8_t *entry = rom_ptr(OverworldMapNames_BANK,
	                               (uint16_t)(OverworldMapNames_ADDR + (uint16_t)OverworldMap_GetOWMapID() * 2u));
	(void)ProcessTextFromID((uint16_t)(entry[0] | (uint16_t)entry[1] << 8));
}
/* <<< factory OverworldMap_PrintMapName */
