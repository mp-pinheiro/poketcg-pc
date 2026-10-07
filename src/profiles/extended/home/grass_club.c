/* >>> factory Preload_NikkiInGrassClub */
PreloadNikkiInGrassClubResult Preload_NikkiInGrassClub(void)
{
	uint8_t a = GetEventValue(EVENT_NIKKI_STATE);
	uint8_t f = (uint8_t)(a >= NIKKI_IN_GRASS_CLUB ? 0x10u : 0u);
	if (a == NIKKI_IN_GRASS_CLUB)
		f |= 0x80u;
	return (PreloadNikkiInGrassClubResult){a, f};
}
/* <<< factory Preload_NikkiInGrassClub */
