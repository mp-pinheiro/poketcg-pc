/* --- part includes_MINT_PIC */
/* --- part MINT_PIC */
/* --- factory Func_3ddb */
/* --- factory Func_3de7 */
/* >>> factory DrawPortrait */
void DrawPortrait(uint8_t a, uint8_t b, uint8_t c)
{
	wPortraitEmotion = a;
	uint8_t saved = hBankROM;
	BankswitchROM(BANK_DRAW_PORTRAIT);
	_DrawPortrait(b, c);
	BankswitchROM(saved);
}
/* <<< factory DrawPortrait */
/* >>> factory DrawOpponentPortrait */
void DrawOpponentPortrait(uint8_t a, uint8_t b, uint8_t c, uint8_t e)
{
	wCurPortrait = a;
	wPortraitSlot = PORTRAIT_SLOT_2;
	DrawPortrait(e, b, c);
}
/* <<< factory DrawOpponentPortrait */
/* >>> factory DrawPlayerPortrait */
void DrawPlayerPortrait(uint8_t b, uint8_t c)
{
	wCurPortrait = runtime_player_gender() ? NUM_PORTRAITS : PORTRAIT_PLAYER;
	wPortraitSlot = PORTRAIT_SLOT_1;
	DrawPortrait(EMOTION_NEUTRAL, b, c);
}

void DrawPlayerChoicePortrait(uint8_t female, uint8_t b, uint8_t c)
{
	wCurPortrait = female ? NUM_PORTRAITS : PORTRAIT_PLAYER;
	wPortraitSlot = female ? PORTRAIT_SLOT_2 : PORTRAIT_SLOT_1;
	DrawPortrait(EMOTION_NEUTRAL, b, c);
}
/* <<< factory DrawPlayerPortrait */
