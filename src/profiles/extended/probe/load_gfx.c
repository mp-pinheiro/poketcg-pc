/* === part includes */
/* >>> factory _DrawPortrait */
static void adapt__DrawPortrait(ProbeState *s)
{
	_DrawPortrait(s->b, s->c);
}
/* <<< factory _DrawPortrait */
/* --- factory Func_80238 */
/* --- part const */
/* >>> part probe_entries_load_gfx */
	{ "_DrawPortrait", adapt__DrawPortrait },
/* <<< part probe_entries_load_gfx */
