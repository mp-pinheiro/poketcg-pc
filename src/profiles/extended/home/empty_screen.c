/* --- part ATTR_BLK_PACKET_EMPTY_SCREEN */
/* >>> factory EmptyScreen */
/* empty_screen.asm:2-14. DisableLCD first: it is what turns wLCDC's enable
 * bit off, so every WriteByteToBGMap0 until the next EnableLCD takes the
 * direct path (no wTempByte staging) and DoFrameIfLCDEnabled skips its
 * DoFrame, as on the ROM. FillTileMap is the home routine, not a copy. */
void EmptyScreen(void)
{
	DisableLCD();
	(void)FillTileMap();
	wDuelDisplayedScreen = 0;
}
/* <<< factory EmptyScreen */
