/* --- factory AIDecide_Defender_Phase14 */
/* --- factory PickPokedexCards_Unreferenced */
/* === factory AIPlay_Bill */
/* >>> part AIDecide_Defender1 */
static void adapt_AIDecide_Defender1(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_Defender1(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_Defender1 */
/* >>> part AIDecide_Defender2 */
static void adapt_AIDecide_Defender2(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_Defender2(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_Defender2 */
/* >>> part AIDecide_PlusPower1 */
static void adapt_AIDecide_PlusPower1(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_PlusPower1(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_PlusPower1 */
/* >>> part AIDecide_PlusPower2 */
static void adapt_AIDecide_PlusPower2(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_PlusPower2(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_PlusPower2 */
/* >>> part AIDecide_SuperPotion1 */
static void adapt_AIDecide_SuperPotion1(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_SuperPotion1(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_SuperPotion1 */
/* >>> part AIDecide_SuperPotion2 */
static void adapt_AIDecide_SuperPotion2(ProbeState *s)
{
	AIDecideParameterResult result = AIDecide_SuperPotion2(s->d);
	s->a = result.a;
	s->f = result.f;
	s->d = result.d;
}
/* <<< part AIDecide_SuperPotion2 */
/* --- factory AIDecide_PlusPower_Phase14 */
/* --- factory AIDecide_Defender_Phase13 */
/* --- factory AIDecide_PlusPower_Phase13 */
/* --- factory AIDecide_SuperPotion_Phase11 */
/* --- factory AIDecide_SuperPotion_Phase08 */
/* >>> part probe_entries_trainer_cards */
	{ "AIDecide_Defender1", adapt_AIDecide_Defender1 },
	{ "AIDecide_Defender2", adapt_AIDecide_Defender2 },
	{ "AIDecide_PlusPower1", adapt_AIDecide_PlusPower1 },
	{ "AIDecide_PlusPower2", adapt_AIDecide_PlusPower2 },
	{ "AIDecide_SuperPotion1", adapt_AIDecide_SuperPotion1 },
	{ "AIDecide_SuperPotion2", adapt_AIDecide_SuperPotion2 },
/* <<< part probe_entries_trainer_cards */
