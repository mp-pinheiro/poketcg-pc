/* >>> factory LoadOWMapForCreditsSequence */
void LoadOWMapForCreditsSequence(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	(void)d;
	EmptyScreen();
	hSCX = c;
	hSCY = b;
	wCurMap = e;
	LoadMapTilesAndPals();
	(void)Func_c9c7();
	SafelyCopyBGMapFromSRAMToVRAM();
	DoMapOWFrame();
	wWhichOBP = 0;
	wWhichOBPalIndex = 0;
	LoadOBPalette(PALETTE_29);
}
/* <<< factory LoadOWMapForCreditsSequence */
