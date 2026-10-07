/* >>> factory _GetCardIDFromDeckIndex */
static void adapt__GetCardIDFromDeckIndex(ProbeState *s)
{
	DeckCardResult r = _GetCardIDFromDeckIndex(s->a);
	s->a = r.a;
	s->d = (uint8_t)(r.id >> 8);
	s->e = (uint8_t)r.id;
	s->hl = r.hl;

}
/* <<< factory _GetCardIDFromDeckIndex */
/* >>> factory GetCardIDFromDeckIndex_bc */
static void adapt_GetCardIDFromDeckIndex_bc(ProbeState *s)
{
	DeckCardResult r = GetCardIDFromDeckIndex_bc(s->a, s->hl);
	s->a = r.a;
	s->b = (uint8_t)(r.id >> 8);
	s->c = (uint8_t)r.id;
	s->hl = r.hl;
}
/* <<< factory GetCardIDFromDeckIndex_bc */
/* >>> factory CountCardIDInLocation */
static void adapt_CountCardIDInLocation(ProbeState *s)
{
	CardLocationCountResult r = CountCardIDInLocation(s->b, pair(s->d, s->e), s->hl);
	s->a = r.a;
	s->hl = r.hl;
}
/* <<< factory CountCardIDInLocation */
/* --- factory CheckPrizeTaken */
/* >>> factory CopyAttackDataAndDamage_FromCardID */
static void adapt_CopyAttackDataAndDamage_FromCardID(ProbeState *s)
{
	AttackCopyResult r = CopyAttackDataAndDamage_FromCardID(s->b, s->c, pair(s->d, s->e));
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory CopyAttackDataAndDamage_FromCardID */
/* --- factory Func_8bf2 */
/* --- factory SendAttackDataToLinkOpponent */
/* --- factory _DrawPlayersPrizeAndBenchCards */
/* >>> factory DrawYourOrOppPlayArea_ActiveCardGfx */
static void adapt_DrawYourOrOppPlayArea_ActiveCardGfx(ProbeState *s)
{
	uint16_t de = (uint16_t)((uint16_t)s->d << 8 | s->e);
	de = DrawYourOrOppPlayArea_ActiveCardGfx(de);
	s->d = (uint8_t)(de >> 8);
	s->e = (uint8_t)de;
}
/* <<< factory DrawYourOrOppPlayArea_ActiveCardGfx */
/* --- factory Func_17ed */
/* >>> part probe_entries_duel */
/* <<< part probe_entries_duel */
