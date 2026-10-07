/* --- part TILESET_MINT */
/* --- part TILESET_MINT_SINGLE */
/* --- part SPRITE_OW_MINT */
/* --- part PALETTE_MINT */
/* --- part PALETTE_MINT_SINGLE */
/* --- part MINT_PALETTE_BYTES */
/* --- part MINT_SINGLE_PALETTE_OFFSET */
/* --- part MINT_SINGLE_PALETTE_BYTES */
/* --- part MINT_ASSET_ADDR */
/* --- part mint_tileset_bank */
/* === part TILE_SIZE */
/* >>> part GFX_TABLE_POINTERS_BANK */
#define GFX_TABLE_POINTERS_BANK GfxTablePointers_BANK
/* <<< part GFX_TABLE_POINTERS_BANK */
/* >>> part GFX_TABLE_POINTERS_ADDR */
#define GFX_TABLE_POINTERS_ADDR GfxTablePointers_ADDR
/* <<< part GFX_TABLE_POINTERS_ADDR */
/* >>> part PORTRAIT_TILE_COUNT */
#define PORTRAIT_TILE_COUNT 36u
/* <<< part PORTRAIT_TILE_COUNT */
/* >>> part TILEMAP_WIDTH */
#define TILEMAP_WIDTH 32u
/* <<< part TILEMAP_WIDTH */
/* >>> part VRAM_BANK_REGISTER */
#define VRAM_BANK_REGISTER 0xFF4Fu
/* <<< part VRAM_BANK_REGISTER */
/* >>> part PORTRAIT_PAL_BASE */
#define PORTRAIT_PAL_BASE 0x97u
/* <<< part PORTRAIT_PAL_BASE */
/* === part put16 */
/* >>> part extended_gfx_entry */
static uint16_t extended_gfx_entry(uint8_t table, uint8_t index)
{
	uint8_t saved_bank = hBankROM;
	uint16_t table_ptr;

	BankswitchROM(GFX_TABLE_POINTERS_BANK);
	table_ptr = (uint16_t)(gb_read8((uint16_t)(GFX_TABLE_POINTERS_ADDR + table)) |
		((uint16_t)gb_read8((uint16_t)(GFX_TABLE_POINTERS_ADDR + table + 1u)) << 8));
	BankswitchROM(saved_bank);
	return (uint16_t)(table_ptr + (uint16_t)index * 4u);
}
/* <<< part extended_gfx_entry */
/* >>> part load_extended_palette_data */
static void load_extended_palette_data(uint8_t palette)
{
	uint8_t saved_bank = hBankROM;
	BankswitchROM(GFX_TABLE_POINTERS_BANK);
	uint16_t entry = extended_gfx_entry(GFXTABLE_PALETTES, palette);
	LoadGraphicsPointerFromHL(&entry);
	uint8_t count = gb_read8(entry);
	BankswitchROM(saved_bank);
	CopyBankedDataToDE((uint16_t)((uint16_t)count * 8u + 1u), wLoadedPalData_ADDR);
}
/* <<< part load_extended_palette_data */
/* >>> factory _DrawPortrait */
void _DrawPortrait(uint8_t b, uint8_t c)
{
	uint16_t entry = extended_gfx_entry(GFXTABLE_PORTRAITS, wCurPortrait);
	LoadGraphicsPointerFromHL(&entry);

	uint16_t source = (uint16_t)(wTempPointer |
		((uint16_t)gb_read8((uint16_t)(wTempPointer_ADDR + 1u)) << 8));
	uint8_t emotion = wPortraitEmotion;
	uint16_t emotion_offset = emotion == 0u ? 0u :
		(emotion == 1u ? 0x0240u : 0x0480u);
	source = (uint16_t)(source + emotion_offset);

	uint8_t swapped_slot = (uint8_t)((wPortraitSlot << 4) | (wPortraitSlot >> 4));
	uint16_t destination = (uint16_t)(((uint16_t)(swapped_slot | 0x80u)) << 8);
	CopyGfxDataFromTempBank(&source, &destination, PORTRAIT_TILE_COUNT, TILE_SIZE);

	uint16_t bg_map = BCCoordToBGMap0Address(b, c);
	uint16_t row = bg_map;
	uint8_t tile = wPortraitSlot;
	for (uint8_t y = 0u; y < 6u; y++) {
		for (uint8_t x = 0u; x < 6u; x++) {
			gb_write8((uint16_t)(row + x), tile++);
		}
		row = (uint16_t)(row + TILEMAP_WIDTH);
	}

	uint16_t attr_source = (uint16_t)(wTempPointer |
		((uint16_t)gb_read8((uint16_t)(wTempPointer_ADDR + 1u)) << 8));
	attr_source = (uint16_t)(attr_source +
		(wCurPortrait == PORTRAIT_PLAYER ? PORTRAIT_TILE_COUNT * TILE_SIZE :
			PORTRAIT_TILE_COUNT * 3u * TILE_SIZE));
	InitDataDecompression(attr_source, (uint8_t)(wDecompressionSecondaryBuffer_ADDR >> 8));
	wBGMapCGBMode = 1u;
	wd291 = wPortraitSlot == PORTRAIT_SLOT_1 ? 2u : 5u;
	for (uint8_t i = 0u; i <= emotion; i++)
		DecompressDataFromBank(PORTRAIT_TILE_COUNT, wDecompressionBuffer_ADDR);
	FuncEightZeroOneFourEight(wDecompressionBuffer_ADDR, PORTRAIT_TILE_COUNT);

	hBankVRAM = 1u;
	gb_write8(VRAM_BANK_REGISTER, 1u);
	row = bg_map;
	uint16_t source_attr = wDecompressionBuffer_ADDR;
	for (uint8_t y = 0u; y < 6u; y++) {
		for (uint8_t x = 0u; x < 6u; x++) {
			gb_write8((uint16_t)(row + x), gb_read8(source_attr++));
		}
		row = (uint16_t)(row + TILEMAP_WIDTH);
	}
	hBankVRAM = 0u;
	gb_write8(VRAM_BANK_REGISTER, 0u);

	load_extended_palette_data((uint8_t)(PORTRAIT_PAL_BASE + wCurPortrait));
	LoadPaletteDataFromHL(wLoadedPalData_ADDR,
		wPortraitSlot == PORTRAIT_SLOT_1 ? 2u : 5u, 3u);
}
/* <<< factory _DrawPortrait */
/* >>> factory LoadTilemap_Decompress */
void LoadTilemap_Decompress(uint16_t *de)
{
	uint8_t width = wBGMapWidth;
	uint8_t rows = wBGMapHeight;
	uint8_t row_width = (uint8_t)(width << (wBGMapCGBMode != 0));
	uint8_t row;
	wDecompressionRowWidth = row_width;
	for (row = 0; row < 0x40u; row++)
		gb_write8((uint16_t)(wDecompressionBuffer_ADDR + row), 0);
	for (row = 0;; row++) {
		uint16_t row_source = wDecompressionBuffer_ADDR;
		uint16_t row_dest = *de;
		DecompressDataFromBank((uint16_t)row_width, row_source);
		CopyBGDataToVRAMOrSRAM(&row_source, &row_dest, width);
		switch_vram(1);
		row_source = (uint16_t)(wDecompressionBuffer_ADDR + width);
		row_dest = *de;
		FuncEightZeroOneFourEight(row_source, width);
		CopyBGDataToVRAMOrSRAM(&row_source, &row_dest, width);
		switch_vram(0);
		*de = (uint16_t)(*de + 32u);
		if ((uint8_t)(row + 1u) == rows)
			break;
	}
}
/* <<< factory LoadTilemap_Decompress */
/* >>> factory SafelyCopyBGMapFromSRAMToVRAM */
void SafelyCopyBGMapFromSRAMToVRAM(void)
{
	uint8_t saved = hBankSRAM;
	uint8_t row;
	BankswitchSRAM(1);
	for (row = 0; row < 32; row++) {
		uint16_t src = (uint16_t)(0xa000u + row * 32u);
		uint16_t dst = (uint16_t)(0x9800u + row * 32u);
		SafeCopyDataHLtoDE(&src, &dst, 0x20u);
		switch_vram(1);
		src = (uint16_t)(0xa400u + row * 32u);
		dst = (uint16_t)(0x9800u + row * 32u);
		SafeCopyDataHLtoDE(&src, &dst, 0x20u);
		switch_vram(0);
	}
	BankswitchSRAM(saved);
	DisableSRAM();
}
/* <<< factory SafelyCopyBGMapFromSRAMToVRAM */
/* >>> factory LoadSpriteGfx */
uint8_t LoadSpriteGfx(uint8_t a)
{
	uint8_t saved = hBankROM;
	BankswitchROM(GfxTablePointers_BANK);
	uint16_t hl = GetMapDataPointer(a, GFX_TABLE_SPRITES).hl;
	LoadGraphicsPointerFromHL(&hl);
	uint8_t total = gb_read8(hl);
	BankswitchROM(saved);
	wTotalNumTiles = total;
	wCurSpriteTileSize = TILE_SIZE;
	LoadGfxDataFromTempPointerToVRAMBank();
	return total;
}
/* <<< factory LoadSpriteGfx */
/* >>> factory LoadGfxDataFromTempPointer */
void LoadGfxDataFromTempPointer(void)
{
	uint16_t src = state16(wTempPointer_ADDR);
	uint16_t dst = state16(wVRAMPointer_ADDR);
	CopyGfxDataFromTempBank(&src, &dst, wTotalNumTiles, wCurSpriteTileSize);
	switch_vram(0);
}
/* <<< factory LoadGfxDataFromTempPointer */
/* >>> factory LoadTilesetGfx */
void LoadTilesetGfx(void)
{
	uint16_t hl = GetMapDataPointer(wCurTileset, GFX_TABLE_TILESETS).hl;
	LoadGraphicsPointerFromHL(&hl);
	LoadTilesetGfx_LoadTileGfx();
	switch_vram(0);
}
/* <<< factory LoadTilesetGfx */
/* --- factory Func_80238 */
/* >>> factory LoadTilesetGfx_LoadTileGfx */
void LoadTilesetGfx_LoadTileGfx(void)
{
	uint16_t hl = state16(wTempPointer_ADDR);
	uint8_t bank = wTempPointerBank;
	uint16_t total = (uint16_t)(GetFarByte(bank, hl)
			      | ((uint16_t)GetFarByte(bank, (uint16_t)(hl + 1u)) << 8));
	put16(wTotalNumTiles_ADDR, total);
	put16(wTempPointer_ADDR, (uint16_t)(hl + 2u));
	if (LoadTilesetGfx_CopyGfxData(0, 0).f & 0x80u)
		return;
	if (LoadTilesetGfx_CopyGfxData(0, 0x80u).f & 0x80u)
		return;
	if (LoadTilesetGfx_CopyGfxData(1, 0).f & 0x80u)
		return;
	(void)LoadTilesetGfx_CopyGfxData(1, 0x80u);
}
/* <<< factory LoadTilesetGfx_LoadTileGfx */
/* >>> factory LoadBGPalette */
void LoadBGPalette(uint8_t a)
{
	LoadPaletteDataToBuffer(a);
	uint8_t count = gb_read8(wLoadedPalData_ADDR);
	if (count != 0u)
		LoadPaletteDataFromHL((uint16_t)(wLoadedPalData_ADDR + 1u),
				      wWhichBGPalIndex, count);
}
/* <<< factory LoadBGPalette */
/* >>> factory LoadOBPalette */
void LoadOBPalette(uint8_t a)
{
	LoadPaletteDataToBuffer(a);
	uint8_t count = gb_read8(wLoadedPalData_ADDR);
	if (count != 0u)
		LoadPaletteDataFromHL((uint16_t)(wLoadedPalData_ADDR + 1u),
				      (uint8_t)(wWhichOBPalIndex | 8u), count);
}
/* <<< factory LoadOBPalette */
/* >>> factory LoadPaletteDataToBuffer */
void LoadPaletteDataToBuffer(uint8_t a)
{
	uint8_t saved = hBankROM;
	BankswitchROM(GfxTablePointers_BANK);
	uint16_t hl = GetMapDataPointer(a, GFX_TABLE_PALETTES).hl;
	uint8_t size;
	uint16_t count;
	uint16_t de = wLoadedPalData_ADDR;
	LoadGraphicsPointerFromHL(&hl);
	size = gb_read8(hl);
	count = (uint16_t)size * 8u + 1u;
	BankswitchROM(saved);
	BankswitchROM(wTempPointerBank);
	CopyBankedDataToDE(count, de);
	BankswitchROM(saved);
}
/* <<< factory LoadPaletteDataToBuffer */
/* === factory LoadGfxDataFromTempPointerToVRAMBank_Tiles0ToTiles2 */
/* === factory LoadTilemap */
