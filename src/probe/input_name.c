#include "home/input_name.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"

/* >>> factory DeckNamingScreen_GetCharInfoFromPos */
static void adapt_DeckNamingScreen_GetCharInfoFromPos(ProbeState *s)
{
	s->hl = DeckNamingScreen_GetCharInfoFromPos(s->hl);
}
/* <<< factory DeckNamingScreen_GetCharInfoFromPos */

/* >>> factory ClearMemory_Bank6 */
static void adapt_ClearMemory_Bank6(ProbeState *s)
{
	ClearMemory_Bank6(s->a, s->hl);
}
/* <<< factory ClearMemory_Bank6 */

/* >>> factory DrawTextboxForKeyboard */
static void adapt_DrawTextboxForKeyboard(ProbeState *s)
{
	DrawTextboxForKeyboard(&s->hl, s->a);
}
/* <<< factory DrawTextboxForKeyboard */

/* >>> factory TransformCharacter */
static void adapt_TransformCharacter(ProbeState *s)
{
	TransformCharacterResult r = TransformCharacter(s->hl, s->d, s->e);
	s->hl = r.hl;
	s->d = r.d;
	s->e = r.e;
	s->f = r.f;
}
/* <<< factory TransformCharacter */

/* >>> factory PlayerNamingScreen_GetCharInfoFromPos */
static void adapt_PlayerNamingScreen_GetCharInfoFromPos(ProbeState *s)
{
	s->hl = PlayerNamingScreen_GetCharInfoFromPos(s->hl);
}
/* <<< factory PlayerNamingScreen_GetCharInfoFromPos */

/* >>> factory PlaySFXConfirmOrCancel_Bank6 */
static void adapt_PlaySFXConfirmOrCancel_Bank6(ProbeState *s)
{
	PlaySFXConfirmOrCancel_Bank6(s->a);
}
/* <<< factory PlaySFXConfirmOrCancel_Bank6 */

/* >>> factory PlayerNamingScreen_AdjustCursorPosition */
static void adapt_PlayerNamingScreen_AdjustCursorPosition(ProbeState *s)
{
	PlayerNamingScreen_AdjustCursorPosition(s->a);
}
/* <<< factory PlayerNamingScreen_AdjustCursorPosition */

/* >>> factory DeckNamingScreen_AdjustCursorPosition */
static void adapt_DeckNamingScreen_AdjustCursorPosition(ProbeState *s)
{
	DeckNamingScreen_AdjustCursorPosition(s->a);
}
/* <<< factory DeckNamingScreen_AdjustCursorPosition */

/* >>> factory PlayerNamingScreen_DrawCursor */
static void adapt_PlayerNamingScreen_DrawCursor(ProbeState *s)
{
	PlayerNamingScreen_DrawCursorResult r = PlayerNamingScreen_DrawCursor(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory PlayerNamingScreen_DrawCursor */

/* >>> factory DeckNamingScreen_DrawCursor */
static void adapt_DeckNamingScreen_DrawCursor(ProbeState *s)
{
	DeckNamingScreen_DrawCursorResult r = DeckNamingScreen_DrawCursor(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory DeckNamingScreen_DrawCursor */

/* >>> factory DeckNamingScreen_DrawInvisibleCursor */
static void adapt_DeckNamingScreen_DrawInvisibleCursor(ProbeState *s)
{
	DeckNamingScreen_DrawCursorResult r = DeckNamingScreen_DrawInvisibleCursor(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DeckNamingScreen_DrawInvisibleCursor */

/* >>> factory DeckNamingScreen_DrawVisibleCursor */
static void adapt_DeckNamingScreen_DrawVisibleCursor(ProbeState *s)
{
	DeckNamingScreen_DrawCursorResult r = DeckNamingScreen_DrawVisibleCursor(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DeckNamingScreen_DrawVisibleCursor */

/* >>> factory PlayerNamingScreen_DrawInvisibleCursor */
static void adapt_PlayerNamingScreen_DrawInvisibleCursor(ProbeState *s)
{
	PlayerNamingScreen_DrawCursorResult r = PlayerNamingScreen_DrawInvisibleCursor(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PlayerNamingScreen_DrawInvisibleCursor */

/* >>> factory PlayerNamingScreen_DrawVisibleCursor */
static void adapt_PlayerNamingScreen_DrawVisibleCursor(ProbeState *s)
{
	PlayerNamingScreen_DrawCursorResult r = PlayerNamingScreen_DrawVisibleCursor(s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PlayerNamingScreen_DrawVisibleCursor */

/* >>> factory PlayerNamingScreen_CheckButtonState */
static void adapt_PlayerNamingScreen_CheckButtonState(ProbeState *s)
{
	PlayerNamingScreen_DrawCursorResult r = PlayerNamingScreen_CheckButtonState();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PlayerNamingScreen_CheckButtonState */

/* >>> factory PrintPlayerNameFromInput */
static void adapt_PrintPlayerNameFromInput(ProbeState *s)
{
	PrintPlayerNameFromInput();
}
/* <<< factory PrintPlayerNameFromInput */

/* >>> factory DrawPlayerNamingScreenBG */
static void adapt_DrawPlayerNamingScreenBG(ProbeState *s)
{
	DrawPlayerNamingScreenBG();
}
/* <<< factory DrawPlayerNamingScreenBG */

/* >>> factory PlayerNamingScreen_ProcessInput */
static void adapt_PlayerNamingScreen_ProcessInput(ProbeState *s)
{
	PlayerNamingScreen_ProcessInputResult r = PlayerNamingScreen_ProcessInput();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PlayerNamingScreen_ProcessInput */

/* >>> factory LoadTextCursorTile */
static void adapt_LoadTextCursorTile(ProbeState *s)
{
	LoadTextCursorTile();
}
/* <<< factory LoadTextCursorTile */

/* >>> factory LoadHalfWidthTextCursorTile */
static void adapt_LoadHalfWidthTextCursorTile(ProbeState *s)
{
	LoadHalfWidthTextCursorTileResult r = LoadHalfWidthTextCursorTile(s->c);
	s->b = r.b;
	s->c = r.c;
}
/* <<< factory LoadHalfWidthTextCursorTile */

/* >>> factory PrintDeckNameFromInput */
static void adapt_PrintDeckNameFromInput(ProbeState *s)
{
	PrintDeckNameFromInput();
}
/* <<< factory PrintDeckNameFromInput */

/* >>> factory DrawDeckNamingScreenBG */
static void adapt_DrawDeckNamingScreenBG(ProbeState *s)
{
	DrawDeckNamingScreenBG();
}
/* <<< factory DrawDeckNamingScreenBG */

/* >>> factory DeckNamingScreen_ProcessInput */
static void adapt_DeckNamingScreen_ProcessInput(ProbeState *s)
{
	DeckNamingScreen_ProcessInputResult r = DeckNamingScreen_ProcessInput();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory DeckNamingScreen_ProcessInput */

const ProbeEntry probe_entries_input_name[] = {
	{ "DeckNamingScreen_GetCharInfoFromPos", adapt_DeckNamingScreen_GetCharInfoFromPos },
	{ "ClearMemory_Bank6", adapt_ClearMemory_Bank6 },
	{ "DrawTextboxForKeyboard", adapt_DrawTextboxForKeyboard },
	{ "TransformCharacter", adapt_TransformCharacter },
	{ "PlayerNamingScreen_GetCharInfoFromPos", adapt_PlayerNamingScreen_GetCharInfoFromPos },
	{ "PlaySFXConfirmOrCancel_Bank6", adapt_PlaySFXConfirmOrCancel_Bank6 },
	{ "PlayerNamingScreen_AdjustCursorPosition", adapt_PlayerNamingScreen_AdjustCursorPosition },
	{ "DeckNamingScreen_AdjustCursorPosition", adapt_DeckNamingScreen_AdjustCursorPosition },
	{ "PlayerNamingScreen_DrawCursor", adapt_PlayerNamingScreen_DrawCursor },
	{ "DeckNamingScreen_DrawCursor", adapt_DeckNamingScreen_DrawCursor },
	{ "DeckNamingScreen_DrawInvisibleCursor", adapt_DeckNamingScreen_DrawInvisibleCursor },
	{ "DeckNamingScreen_DrawVisibleCursor", adapt_DeckNamingScreen_DrawVisibleCursor },
	{ "PlayerNamingScreen_DrawInvisibleCursor", adapt_PlayerNamingScreen_DrawInvisibleCursor },
	{ "PlayerNamingScreen_DrawVisibleCursor", adapt_PlayerNamingScreen_DrawVisibleCursor },
	{ "PlayerNamingScreen_CheckButtonState", adapt_PlayerNamingScreen_CheckButtonState },
	{ "PrintPlayerNameFromInput", adapt_PrintPlayerNameFromInput },
	{ "DrawPlayerNamingScreenBG", adapt_DrawPlayerNamingScreenBG },
	{ "PlayerNamingScreen_ProcessInput", adapt_PlayerNamingScreen_ProcessInput },
	{ "LoadTextCursorTile", adapt_LoadTextCursorTile },
	{ "LoadHalfWidthTextCursorTile", adapt_LoadHalfWidthTextCursorTile },
	{ "PrintDeckNameFromInput", adapt_PrintDeckNameFromInput },
	{ "DrawDeckNamingScreenBG", adapt_DrawDeckNamingScreenBG },
	{ "DeckNamingScreen_ProcessInput", adapt_DeckNamingScreen_ProcessInput },
	{ NULL, NULL },
};
