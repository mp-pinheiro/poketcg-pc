/* --- part includes_MINT_PIC */
/* --- part MINT_PIC */
/* --- part TILESET_MINT */
/* --- part TILESET_MINT_SINGLE */
/* --- part PALETTE_MINT */
/* --- part PALETTE_MINT_SINGLE */
/* --- part MINT_PALETTE_BASE */
/* --- part MINT_ATTRIBUTE_OFFSET */
/* --- part rVBK */
/* --- part g_mint_single_palette */
/* --- part SetMintSinglePalette */
/* --- part write_mint_attributes */
/* --- part includes_SCENE_POINTERS_BANK */
/* --- part SCENE_POINTERS_BANK */
/* --- part SCENE_POINTERS_ADDR */
/* --- part includes_tail */
/* >>> factory SetBoosterLogoOAM */
/* scenes.asm:135-181 */
void SetBoosterLogoOAM(void)
{
	uint8_t i;
	uint8_t count = booster_logo_oam[0];

	wWhichVRAMBank = 0u;
	wVRAMTileOffset = 0u;
	(void)LoadSpriteGfx(SPRITE_BOOSTER_PACK_OAM);
	ZeroObjectPositions();

	for (i = 0u; i < count; i++) {
		const uint8_t *entry = &booster_logo_oam[1u + (uint8_t)(i * 4u)];
		uint8_t e = (uint8_t)(wSceneBaseY - hSCY + entry[0]);
		uint8_t d = (uint8_t)(wSceneBaseX - hSCX + entry[1]);
		uint8_t c = (uint8_t)(wd61f + entry[2]);
		uint8_t b = entry[3];

		SetOneObjectAttributes(e, d, c, b);
	}

	wVBlankOAMCopyToggle = (uint8_t)(wVBlankOAMCopyToggle + 1u);
}
/* <<< factory SetBoosterLogoOAM */
/* --- factory _DrawPortrait */
/* --- factory LoadScene_LoadSGBPacket */
/* --- factory LoadScene_LoadCompressedSGBPacket */
/* --- factory LoadScene_SetCardPopAttrBlk */
/* --- factory LoadScene_SetGameBoyPrinterAttrBlk */
/* >>> factory _LoadScene */
void _LoadScene(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t saved_tilemap = gb_read8(wCurTilemap_ADDR);
	uint8_t saved_d291 = gb_read8(wd291_ADDR);
	uint8_t base_x = (uint8_t)((uint8_t)(b << 3) + 0x08u);
	uint8_t base_y = (uint8_t)((uint8_t)(c << 3) + 0x10u);

	gb_write8(wSceneBaseX_ADDR, base_x);
	gb_write8(wSceneBaseY_ADDR, base_y);

	const uint8_t *ptr_entry = rom_ptr(ScenePointers_BANK,
		(uint16_t)(ScenePointers_ADDR + (uint16_t)a * 2u));
	uint16_t scene_ptr = (uint16_t)(ptr_entry[0] |
		((uint16_t)ptr_entry[1] << 8));
	const uint8_t *scene = rom_ptr(ScenePointers_BANK, scene_ptr);
	uint16_t index = 0u;

	uint8_t palette = scene[index++];
	wWhichOBP = 0u;
	wWhichBGPalIndex = scene[index];
	wd291 = scene[index++];
	LoadBGPalette(palette);

	wCurTilemap = scene[index++];
	LoadTilemap_ToVRAM(b, c);

	wVRAMTileOffset = scene[index++];
	wWhichVRAMBank = scene[index++];
	LoadTilesetGfx();

	for (;;) {
		uint8_t sprite = scene[index++];
		if (sprite == 0u)
			break;
		wSceneSprite = sprite;
		uint8_t sprite_palette = scene[index++];
		wWhichOBP = 0u;
		wWhichOBPalIndex = scene[index++];
		LoadOBPalette(sprite_palette);

		for (;;) {
			uint8_t animation = scene[index++];
			if (animation == 0u)
				break;
			wSceneSpriteAnimation = animation;
			(void)CreateSpriteAndAnimBufferEntry(wSceneSprite, 0u);
			wSceneSpriteIndex = wWhichSprite;
			uint16_t coords = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
			gb_write8(coords, (uint8_t)(wSceneBaseX + scene[index++]));
			gb_write8((uint16_t)(coords + 1u),
				(uint8_t)(wSceneBaseY + scene[index++]));
			if (wSceneSpriteAnimation != 0xFFu)
				StartSpriteAnimation(wSceneSpriteAnimation);
		}
	}

	wd291 = saved_d291;
	wCurTilemap = saved_tilemap;
}
/* <<< factory _LoadScene */
