/* --- factory Func_3ddb */
/* --- factory Func_3de7 */
/* >>> factory DrawOpponentPortrait */
static void adapt_DrawOpponentPortrait(ProbeState *s)
{
	DrawOpponentPortrait(s->a, s->b, s->c, s->e);
}
/* <<< factory DrawOpponentPortrait */
/* >>> part probe_entries_load_animation */
const ProbeEntry probe_entries_load_animation[] = {
	{ "GetFirstSpriteAnimBufferProperty", adapt_GetFirstSpriteAnimBufferProperty },
	{ "GetSpriteAnimBufferProperty", adapt_GetSpriteAnimBufferProperty },
	{ "GetSpriteAnimBufferProperty_SpriteInA", adapt_GetSpriteAnimBufferProperty_SpriteInA },
	{ "DrawSpriteAnimationFrame", adapt_DrawSpriteAnimationFrame },
	{ "GetAnimationFramePointer", adapt_GetAnimationFramePointer },
	{ "ClearSpriteAnimations", adapt_ClearSpriteAnimations },
	{ "HandleAllSpriteAnimations", adapt_HandleAllSpriteAnimations },
	{ "EnableAndClearSpriteAnimations", adapt_EnableAndClearSpriteAnimations },
	{ "DrawPortrait", adapt_DrawPortrait },
	{ "DrawOpponentPortrait", adapt_DrawOpponentPortrait },
	{ "DrawPlayerPortrait", adapt_DrawPlayerPortrait },
	{ "Func_3e31", adapt_Func_3e31 },
	{ "LoadScene", adapt_LoadScene },
	{ NULL, NULL },
};
/* <<< part probe_entries_load_animation */
