/* >>> part BANK_DRAW_PORTRAIT */
#define BANK_DRAW_PORTRAIT _DrawPortrait_BANK
/* <<< part BANK_DRAW_PORTRAIT */
/* --- part includes_MINT_PIC */
/* --- part MINT_PIC */
/* >>> part includes_BANK_LOAD_SCENE */
#include "generated/wram.h"

#include "generated/wram.h"

#include "home/animation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/palettes.h"
#include "home/scenes.h"
#include "home/switch_rom.h"
/* <<< part includes_BANK_LOAD_SCENE */
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
	wCurPortrait = PORTRAIT_PLAYER;
	wPortraitSlot = PORTRAIT_SLOT_1;
	DrawPortrait(EMOTION_NEUTRAL, b, c);
}
/* <<< factory DrawPlayerPortrait */
