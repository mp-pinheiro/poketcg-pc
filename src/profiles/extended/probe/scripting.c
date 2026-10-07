/* --- factory GetScriptArgs5AfterPointer */
/* >>> factory ScriptCommand_JumpIfCardInCollection */
static void adapt_ScriptCommand_JumpIfCardInCollection(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfCardInCollection(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfCardInCollection */
/* >>> factory ScriptCommand_GiveCard */
static void adapt_ScriptCommand_GiveCard(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_GiveCard(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_GiveCard */
/* >>> factory ScriptCommand_TakeCard */
static void adapt_ScriptCommand_TakeCard(ProbeState *s)
{
	IncreaseScriptPointerResult r = ScriptCommand_TakeCard(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_TakeCard */
/* >>> factory ScriptCommand_SetSpriteAttributes */
static void adapt_ScriptCommand_SetSpriteAttributes(ProbeState *s)
{
	SetSpriteAttributesResult r = ScriptCommand_SetSpriteAttributes(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
}
/* <<< factory ScriptCommand_SetSpriteAttributes */
/* --- factory ScriptCommand_BattleCenter */
/* >>> factory SetNextScript */
static void adapt_SetNextScript(ProbeState *s)
{
	s->hl = SetNextScript(s->a, (uint16_t)(((uint16_t)s->b << 8) | s->c));
}
/* <<< factory SetNextScript */
/* >>> factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
static void adapt_ScriptCommand_RemoveAllEnergyCardsFromCollection(ProbeState *s)
{
	ScriptCommand_RemoveAllEnergyCardsResult r =
		ScriptCommand_RemoveAllEnergyCardsFromCollection(s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
/* >>> factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
static void adapt_ScriptCommand_JumpIfAnyEnergyCardsInCollection(ProbeState *s)
{
	ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult r =
		ScriptCommand_JumpIfAnyEnergyCardsInCollection();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
/* >>> factory ScriptCommand_JumpIfCardOwned */
static void adapt_ScriptCommand_JumpIfCardOwned(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfCardOwned(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfCardOwned */
/* --- factory Func_c998 */
/* --- factory ScriptCommand_GiftCenter */
/* >>> factory ScriptCommand_ShowCardReceivedScreen */
static void adapt_ScriptCommand_ShowCardReceivedScreen(ProbeState *s)
{
	IncreaseScriptPointerResult result = ScriptCommand_ShowCardReceivedScreen(s->b, s->c);
	s->a = result.a;
	s->f = result.f;
	s->c = result.c;
}
/* <<< factory ScriptCommand_ShowCardReceivedScreen */
/* --- factory Script_GiftCenterClerk */
/* >>> factory ScriptCommand_JumpIfMan1RequestedCardOwned */
static void adapt_ScriptCommand_JumpIfMan1RequestedCardOwned(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfMan1RequestedCardOwned(s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfMan1RequestedCardOwned */
/* >>> factory ScriptCommand_JumpIfMan1RequestedCardInCollection */
static void adapt_ScriptCommand_JumpIfMan1RequestedCardInCollection(ProbeState *s)
{
	JumpIfCardInCollectionResult r = ScriptCommand_JumpIfMan1RequestedCardInCollection(s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory ScriptCommand_JumpIfMan1RequestedCardInCollection */
/* >>> part probe_entries_scripting */
/* <<< part probe_entries_scripting */
