/* >>> part kMedalCoordsAndTilemaps */
static const uint8_t kMedalCoordsAndTilemaps[24] = {
	 1u, 10u, TILEMAP_GRASS_MEDAL,
	 6u, 10u, TILEMAP_SCIENCE_MEDAL,
	11u, 10u, TILEMAP_FIRE_MEDAL,
	16u, 10u, TILEMAP_WATER_MEDAL,
	 1u, 14u, TILEMAP_LIGHTNING_MEDAL,
	 6u, 14u, TILEMAP_PSYCHIC_MEDAL,
	11u, 14u, TILEMAP_ROCK_MEDAL,
	16u, 14u, TILEMAP_FIGHTING_MEDAL,
};
/* <<< part kMedalCoordsAndTilemaps */
/* >>> factory PrintAlbumProgress_SkipGetProgress */
void PrintAlbumProgress_SkipGetProgress(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)ConvertWordToNumericalDigits((uint16_t)(((uint16_t)d << 8) | e));
	uint16_t dest1 = BCCoordToBGMap0Address(b, c);
	uint16_t src1 = wDecimalChars_ADDR;
	SafeCopyDataHLtoDE(&src1, &dest1, 3u);

	(void)ConvertWordToNumericalDigits(hl);
	uint8_t b2 = (uint8_t)(b + 4u);
	uint16_t dest2 = BCCoordToBGMap0Address(b2, c);
	uint16_t src2 = wDecimalChars_ADDR;
	SafeCopyDataHLtoDE(&src2, &dest2, 3u);
}
/* <<< factory PrintAlbumProgress_SkipGetProgress */
/* >>> factory PrintAlbumProgress */
void PrintAlbumProgress(uint8_t b, uint8_t c)
{
	AlbumProgress prog = GetCardAlbumProgress();
	PrintAlbumProgress_SkipGetProgress(b, c, prog.d, prog.e,
		(uint16_t)(((uint16_t)prog.b << 8) | prog.c));
}
/* <<< factory PrintAlbumProgress */
/* --- factory DrawCollectedMedals */
/* === factory LoadCollectedMedalTilemaps */
