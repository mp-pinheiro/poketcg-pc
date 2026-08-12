#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory SetLineSeparation */
static void adapt_SetLineSeparation(ProbeState *s)
{
	SetLineSeparation(s->a);
}
/* <<< factory SetLineSeparation */

/* >>> factory PlayAreaScreenMenuFunction */
static void adapt_PlayAreaScreenMenuFunction(ProbeState *s)
{
	s->f = PlayAreaScreenMenuFunction();
}
/* <<< factory PlayAreaScreenMenuFunction */

/* >>> factory SwitchAttackPage */
static void adapt_SwitchAttackPage(ProbeState *s)
{
	(void)s;
	SwitchAttackPage();
}
/* <<< factory SwitchAttackPage */

/* >>> factory CopyCGBCardPalette */
static void adapt_CopyCGBCardPalette(ProbeState *s)
{
	CopyCGBCardPalette(s->a);
}
/* <<< factory CopyCGBCardPalette */

/* >>> factory CreateCardAttrBlkPacket_DataSet */
static void adapt_CreateCardAttrBlkPacket_DataSet(ProbeState *s)
{
	s->hl = CreateCardAttrBlkPacket_DataSet(s->hl, s->a, s->d, s->e);
}
/* <<< factory CreateCardAttrBlkPacket_DataSet */

/* >>> factory SaveDuelDataToDE */
static void adapt_SaveDuelDataToDE(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	SaveDuelDataToDE(de);
}
/* <<< factory SaveDuelDataToDE */

/* >>> factory LoadSavedDuelDataFromDE */
static void adapt_LoadSavedDuelDataFromDE(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	LoadSavedDuelDataFromDE(de);
}
/* <<< factory LoadSavedDuelDataFromDE */

/* >>> factory SetBGP7OrSGB2ToCardPalette */
static void adapt_SetBGP7OrSGB2ToCardPalette(ProbeState *s)
{
	(void)s;
	SetBGP7OrSGB2ToCardPalette();
}
/* <<< factory SetBGP7OrSGB2ToCardPalette */

/* >>> factory JPWriteByteToBGMap0 */
static void adapt_JPWriteByteToBGMap0(ProbeState *s)
{
	JPWriteByteToBGMap0(s->a, s->b, s->c);
}
/* <<< factory JPWriteByteToBGMap0 */

/* >>> factory ZeroObjectPositionsAndToggleOAMCopy */
static void adapt_ZeroObjectPositionsAndToggleOAMCopy(ProbeState *s)
{
	(void)s;
	ZeroObjectPositionsAndToggleOAMCopy();
}
/* <<< factory ZeroObjectPositionsAndToggleOAMCopy */

/* >>> factory LoadPlayerDeck */
static void adapt_LoadPlayerDeck(ProbeState *s)
{
	(void)s;
	LoadPlayerDeck();
}
/* <<< factory LoadPlayerDeck */

/* >>> factory PrintPracticeDuelDrMasonInstructions */
static void adapt_PrintPracticeDuelDrMasonInstructions(ProbeState *s)
{
	PrintPracticeDuelDrMasonInstructions(s->hl);
}
/* <<< factory PrintPracticeDuelDrMasonInstructions */

/* >>> factory PrintPracticeDuelInstructionsTextBoxLabel */
static void adapt_PrintPracticeDuelInstructionsTextBoxLabel(ProbeState *s)
{
	(void)s;
	PrintPracticeDuelInstructionsTextBoxLabel();
}
/* <<< factory PrintPracticeDuelInstructionsTextBoxLabel */

/* >>> factory SwitchCardPage */
static void adapt_SwitchCardPage(ProbeState *s)
{
	CardPageResult r = SwitchCardPage(s->a);
	s->a = r.a;
}
/* <<< factory SwitchCardPage */

/* >>> factory CardPageSwitch_00 */
static void adapt_CardPageSwitch_00(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_00();
	s->a = r.a;
}
/* <<< factory CardPageSwitch_00 */

/* >>> factory LoadLoaded1CardGfx */
static void adapt_LoadLoaded1CardGfx(ProbeState *s)
{
	LoadLoaded1CardGfx((uint16_t)(s->d << 8 | s->e));
}
/* <<< factory LoadLoaded1CardGfx */

/* >>> factory SetSGB3ToCardPalette */
static void adapt_SetSGB3ToCardPalette(ProbeState *s)
{
	(void)s;
	SetSGB3ToCardPalette();
}
/* <<< factory SetSGB3ToCardPalette */

/* >>> factory LookForCardIDInPlayArea_Bank5 */
static void adapt_LookForCardIDInPlayArea_Bank5(ProbeState *s)
{
	LookResult r = LookForCardIDInPlayArea_Bank5(s->a, s->b);
	s->a = r.a;
	s->b = r.b;
	s->f = r.f;
}
/* <<< factory LookForCardIDInPlayArea_Bank5 */

/* >>> factory ClearMemory_Bank5 */
static void adapt_ClearMemory_Bank5(ProbeState *s)
{
	ClearMemory_Bank5(s->a, s->hl);
}
/* <<< factory ClearMemory_Bank5 */

/* >>> factory CheckCardPageExists */
static void adapt_CheckCardPageExists(ProbeState *s)
{
	CardPageExistsResult r = CheckCardPageExists(&s->hl);
	s->a = r.a;
	s->f = r.zero ? (uint8_t)0x80u : (uint8_t)0x00u;
}
/* <<< factory CheckCardPageExists */

/* >>> factory CardPageSwitch_PokemonEnd */
static void adapt_CardPageSwitch_PokemonEnd(ProbeState *s)
{
	CardPageResult r = CardPageSwitch_PokemonEnd();
	s->a = r.a;
	s->f = (uint8_t)((s->f & 0x80u) | (r.carry ? 0x10u : 0u));
}
/* <<< factory CardPageSwitch_PokemonEnd */

/* >>> factory SetCardListInfoBoxText */
static void adapt_SetCardListInfoBoxText(ProbeState *s)
{
	SetCardListInfoBoxText(s->hl);
}
/* <<< factory SetCardListInfoBoxText */

/* >>> factory LoadCardNameToTxRam2 */
static void adapt_LoadCardNameToTxRam2(ProbeState *s)
{
	LoadCardNameToTxRam2(s->a);
}
/* <<< factory LoadCardNameToTxRam2 */

/* >>> factory LoadCardNameToTxRam2_b */
static void adapt_LoadCardNameToTxRam2_b(ProbeState *s)
{
	LoadCardNameToTxRam2_b(s->a);
}
/* <<< factory LoadCardNameToTxRam2_b */

const ProbeEntry probe_entries_core[] = {
	{ "SetLineSeparation", adapt_SetLineSeparation },
	{ "PlayAreaScreenMenuFunction", adapt_PlayAreaScreenMenuFunction },
	{ "SwitchAttackPage", adapt_SwitchAttackPage },
	{ "CopyCGBCardPalette", adapt_CopyCGBCardPalette },
	{ "CreateCardAttrBlkPacket_DataSet", adapt_CreateCardAttrBlkPacket_DataSet },
	{ "SaveDuelDataToDE", adapt_SaveDuelDataToDE },
	{ "LoadSavedDuelDataFromDE", adapt_LoadSavedDuelDataFromDE },
	{ "SetBGP7OrSGB2ToCardPalette", adapt_SetBGP7OrSGB2ToCardPalette },
	{ "JPWriteByteToBGMap0", adapt_JPWriteByteToBGMap0 },
	{ "ZeroObjectPositionsAndToggleOAMCopy", adapt_ZeroObjectPositionsAndToggleOAMCopy },
	{ "LoadPlayerDeck", adapt_LoadPlayerDeck },
	{ "PrintPracticeDuelDrMasonInstructions", adapt_PrintPracticeDuelDrMasonInstructions },
	{ "PrintPracticeDuelInstructionsTextBoxLabel", adapt_PrintPracticeDuelInstructionsTextBoxLabel },
	{ "SwitchCardPage", adapt_SwitchCardPage },
	{ "CardPageSwitch_00", adapt_CardPageSwitch_00 },
	{ "LoadLoaded1CardGfx", adapt_LoadLoaded1CardGfx },
	{ "SetSGB3ToCardPalette", adapt_SetSGB3ToCardPalette },
	{ "LookForCardIDInPlayArea_Bank5", adapt_LookForCardIDInPlayArea_Bank5 },
	{ "ClearMemory_Bank5", adapt_ClearMemory_Bank5 },
	{ "CheckCardPageExists", adapt_CheckCardPageExists },
	{ "CardPageSwitch_PokemonEnd", adapt_CardPageSwitch_PokemonEnd },
	{ "SetCardListInfoBoxText", adapt_SetCardListInfoBoxText },
	{ "LoadCardNameToTxRam2", adapt_LoadCardNameToTxRam2 },
	{ "LoadCardNameToTxRam2_b", adapt_LoadCardNameToTxRam2_b },
	{ NULL, NULL },
};
