/* >>> factory CountTurnDuelistPokemonWithActivePkmnPower */
static void adapt_CountTurnDuelistPokemonWithActivePkmnPower(ProbeState *s)
{
	CardId target = (CardId)(((uint16_t)s->d << 8) | s->e);
	PkmnPowerCountResult r = CountTurnDuelistPokemonWithActivePkmnPower(target);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory CountTurnDuelistPokemonWithActivePkmnPower */
/* >>> factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
static void adapt_CountPokemonWithActivePkmnPowerInBothPlayAreas(ProbeState *s)
{
	CardId target = (CardId)(((uint16_t)s->d << 8) | s->e);
	PkmnPowerCountResult r = CountPokemonWithActivePkmnPowerInBothPlayAreas(target);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
/* >>> factory IsClairvoyanceActive */
static void adapt_IsClairvoyanceActive(ProbeState *s)
{
	PkmnPowerCountResult r = IsClairvoyanceActive();
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory IsClairvoyanceActive */
/* >>> factory IsPrehistoricPowerActive */
static void adapt_IsPrehistoricPowerActive(ProbeState *s)
{
	PrehistoricPowerResult r = IsPrehistoricPowerActive(s->hl);
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory IsPrehistoricPowerActive */
/* >>> factory IsRainDanceActive */
static void adapt_IsRainDanceActive(ProbeState *s)
{
	PkmnPowerCountResult r = IsRainDanceActive();
	s->a = r.a;
	s->f = r.f;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory IsRainDanceActive */
/* >>> factory HandleStrikesBack_AgainstDamagingAttack */
static void adapt_HandleStrikesBack_AgainstDamagingAttack(ProbeState *s)
{
	uint16_t de = (uint16_t)(s->d << 8 | s->e);
	StrikesBackResult r = HandleStrikesBack_AgainstDamagingAttack(de, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory HandleStrikesBack_AgainstDamagingAttack */
