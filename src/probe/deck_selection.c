#include "home/deck_selection.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory GetPointerToDeckCards */
static void adapt_GetPointerToDeckCards(ProbeState *s)
{
	s->hl = GetPointerToDeckCards();
}
/* <<< factory GetPointerToDeckCards */

/* >>> factory ResetCheckMenuCursorPositionAndBlink */
static void adapt_ResetCheckMenuCursorPositionAndBlink(ProbeState *s)
{
	ResetCheckMenuCursorPositionAndBlinkResult r = ResetCheckMenuCursorPositionAndBlink();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ResetCheckMenuCursorPositionAndBlink */

/* >>> factory GetPointerToDeckName */
static void adapt_GetPointerToDeckName(ProbeState *s)
{
	s->a = 0;
	s->f = 0x80;
	s->hl = GetPointerToDeckName();
}
/* <<< factory GetPointerToDeckName */

/* >>> factory InitDeckBuildingParams */
static void adapt_InitDeckBuildingParams(ProbeState *s)
{
	InitDeckBuildingParamsResult r = InitDeckBuildingParams(&s->hl, s->f);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory InitDeckBuildingParams */

/* >>> factory CheckIfCurDeckIsValid */
static void adapt_CheckIfCurDeckIsValid(ProbeState *s)
{
	CheckIfCurDeckIsValidResult result = CheckIfCurDeckIsValid();
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->hl = result.hl;
}
/* <<< factory CheckIfCurDeckIsValid */

/* >>> factory CancelDeckSelectionSubMenu */
static void adapt_CancelDeckSelectionSubMenu(ProbeState *s)
{
	(void)s;
	CancelDeckSelectionSubMenu();
}
/* <<< factory CancelDeckSelectionSubMenu */

/* >>> factory CopyDeckFromSRAM */
static void adapt_CopyDeckFromSRAM(ProbeState *s)
{
	CopyDeckFromSRAMResult r = CopyDeckFromSRAM((uint16_t)(((uint16_t)s->d << 8) | s->e), s->hl);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory CopyDeckFromSRAM */

/* >>> factory Func_9001 */
static void adapt_Func_9001(ProbeState *s)
{
	Func_9001Result r = Func_9001(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory Func_9001 */

/* >>> factory LoadHandCardsIcon */
static void adapt_LoadHandCardsIcon(ProbeState *s)
{
	LoadHandCardsIconResult r = LoadHandCardsIcon();
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory LoadHandCardsIcon */

/* >>> factory InitPromotionalCardAndDeckCounterSaveData */
static void adapt_InitPromotionalCardAndDeckCounterSaveData(ProbeState *s)
{
	LoadHandCardsIconResult r = InitPromotionalCardAndDeckCounterSaveData();
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory InitPromotionalCardAndDeckCounterSaveData */

/* >>> factory PrepareMenuGraphics */
static void adapt_PrepareMenuGraphics(ProbeState *s)
{
	(void)s;
	PrepareMenuGraphics();
}
/* <<< factory PrepareMenuGraphics */

/* >>> factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */
static void adapt_EmptyScreenAndLoadFontDuelAndHandCardsIcons(ProbeState *s)
{
	(void)s;
	EmptyScreenAndLoadFontDuelAndHandCardsIcons();
}
/* <<< factory EmptyScreenAndLoadFontDuelAndHandCardsIcons */

const ProbeEntry probe_entries_deck_selection[] = {
	{ "GetPointerToDeckCards", adapt_GetPointerToDeckCards },
	{ "ResetCheckMenuCursorPositionAndBlink", adapt_ResetCheckMenuCursorPositionAndBlink },
	{ "GetPointerToDeckName", adapt_GetPointerToDeckName },
	{ "InitDeckBuildingParams", adapt_InitDeckBuildingParams },
	{ "CheckIfCurDeckIsValid", adapt_CheckIfCurDeckIsValid },
	{ "CancelDeckSelectionSubMenu", adapt_CancelDeckSelectionSubMenu },
	{ "CopyDeckFromSRAM", adapt_CopyDeckFromSRAM },
	{ "Func_9001", adapt_Func_9001 },
	{ "LoadHandCardsIcon", adapt_LoadHandCardsIcon },
	{ "InitPromotionalCardAndDeckCounterSaveData", adapt_InitPromotionalCardAndDeckCounterSaveData },
	{ "PrepareMenuGraphics", adapt_PrepareMenuGraphics },
	{ "EmptyScreenAndLoadFontDuelAndHandCardsIcons", adapt_EmptyScreenAndLoadFontDuelAndHandCardsIcons },
	{ NULL, NULL },
};
