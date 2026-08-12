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
	{ NULL, NULL },
};
