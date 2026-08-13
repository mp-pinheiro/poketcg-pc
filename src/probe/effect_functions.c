#include "home/effect_functions.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "probe.h"




/* >>> factory UpdateExpectedAIDamage */
static void adapt_UpdateExpectedAIDamage(ProbeState *s)
{
	UpdateExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory UpdateExpectedAIDamage */


/* >>> factory SetExpectedAIDamage */
static void adapt_SetExpectedAIDamage(ProbeState *s)
{
	SetExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory SetExpectedAIDamage */


/* >>> factory IsPlayerTurn */
static void adapt_IsPlayerTurn(ProbeState *s)
{
	IsPlayerTurnResult r = IsPlayerTurn();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory IsPlayerTurn */


/* >>> factory UpdateExpectedAIDamage_AccountForPoison */
static void adapt_UpdateExpectedAIDamage_AccountForPoison(ProbeState *s)
{
	UpdateExpectedAIDamage_AccountForPoison(s->a, s->d, s->e);
}
/* <<< factory UpdateExpectedAIDamage_AccountForPoison */

/* >>> factory ApplySubstatus1ToAttackingCard */
static void adapt_ApplySubstatus1ToAttackingCard(ProbeState *s)
{
	s->hl = ApplySubstatus1ToAttackingCard(s->a);
}
/* <<< factory ApplySubstatus1ToAttackingCard */


/* >>> factory SetNoEffectFromStatus */
static void adapt_SetNoEffectFromStatus(ProbeState *s)
{
	(void)s;
	SetNoEffectFromStatus();
}
/* <<< factory SetNoEffectFromStatus */

/* >>> factory SetDefiniteAIDamage */
static void adapt_SetDefiniteAIDamage(ProbeState *s)
{
	(void)s;
	SetDefiniteAIDamage();
}
/* <<< factory SetDefiniteAIDamage */

/* >>> factory PickRandomPlayAreaCard */
static void adapt_PickRandomPlayAreaCard(ProbeState *s)
{
	PickRandomPlayAreaCardResult r = PickRandomPlayAreaCard();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PickRandomPlayAreaCard */

/* >>> factory GetNextPositionInTempList */
static void adapt_GetNextPositionInTempList(ProbeState *s)
{
	s->hl = GetNextPositionInTempList();
}
/* <<< factory GetNextPositionInTempList */

/* >>> factory QueueStatusCondition */
static void adapt_QueueStatusCondition(ProbeState *s)
{
	QueueStatusConditionResult r = QueueStatusCondition(s->b, s->c);
	s->f = r.f;
}
/* <<< factory QueueStatusCondition */

/* >>> factory CommentedOut_2c086 */
static void adapt_CommentedOut_2c086(ProbeState *s)
{
	s->a = CommentedOut_2c086(s->a);
}
/* <<< factory CommentedOut_2c086 */

/* >>> factory SetWasUnsuccessful */
static void adapt_SetWasUnsuccessful(ProbeState *s)
{
	(void)s;
	SetWasUnsuccessful();
}
/* <<< factory SetWasUnsuccessful */

/* >>> factory Teleport_SwitchEffect */
static void adapt_Teleport_SwitchEffect(ProbeState *s)
{
	Teleport_SwitchEffect();
}
/* <<< factory Teleport_SwitchEffect */

/* >>> factory SetDamageToATimes20 */
static void adapt_SetDamageToATimes20(ProbeState *s)
{
	SetDamageToATimes20(s->a);
}
/* <<< factory SetDamageToATimes20 */

/* >>> factory CreateTrainerCardListFromDiscardPile */
static void adapt_CreateTrainerCardListFromDiscardPile(ProbeState *s)
{
	CreateTrainerCardListFromDiscardPileResult r = CreateTrainerCardListFromDiscardPile();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateTrainerCardListFromDiscardPile */

/* >>> factory CreateEnergyCardListFromDiscardPile */
static void adapt_CreateEnergyCardListFromDiscardPile(ProbeState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile(s->c);
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateEnergyCardListFromDiscardPile */

/* >>> factory GetAttackName */
static void adapt_GetAttackName(ProbeState *s)
{
	uint16_t hl = GetAttackName(s->d, s->e);
	s->hl = hl;
}
/* <<< factory GetAttackName */


/* >>> factory ClefableMinimizeEffect */
static void adapt_ClefableMinimizeEffect(ProbeState *s)
{
	s->hl = ClefableMinimizeEffect();
}
/* <<< factory ClefableMinimizeEffect */


/* >>> factory HandleAIMetronomeEffect */
static void adapt_HandleAIMetronomeEffect(ProbeState *s)
{
	(void)s;
	HandleAIMetronomeEffect();
}
/* <<< factory HandleAIMetronomeEffect */

/* >>> factory ParalysisEffect */
static void adapt_ParalysisEffect(ProbeState *s)
{
	QueueStatusConditionResult r = ParalysisEffect();
	s->f = r.f;
}
/* <<< factory ParalysisEffect */

/* >>> factory ConfusionEffect */
static void adapt_ConfusionEffect(ProbeState *s)
{
	QueueStatusConditionResult r = ConfusionEffect();
	s->f = r.f;
}
/* <<< factory ConfusionEffect */

/* >>> factory InvisibleWallEffect */
static void adapt_InvisibleWallEffect(ProbeState *s)
{
	s->f = InvisibleWallEffect(s->f);
}
/* <<< factory InvisibleWallEffect */

/* >>> factory CheckIfDefendingPokemonHasAnyAttack */
static void adapt_CheckIfDefendingPokemonHasAnyAttack(ProbeState *s)
{
	CheckAttackResult r = CheckIfDefendingPokemonHasAnyAttack();
	s->f = r.f;
}
/* <<< factory CheckIfDefendingPokemonHasAnyAttack */

/* >>> factory UpdateDevolvedCardHPAndStage */
static void adapt_UpdateDevolvedCardHPAndStage(ProbeState *s)
{
	UpdateDevolvedCardHPAndStage(s->a);
}
/* <<< factory UpdateDevolvedCardHPAndStage */

/* >>> factory DodrioRage_DamageBoostEffect */
static void adapt_DodrioRage_DamageBoostEffect(ProbeState *s)
{
	(void)s;
	DodrioRage_DamageBoostEffect();
}
/* <<< factory DodrioRage_DamageBoostEffect */


/* >>> factory DragonairSlam_AIEffect */
static void adapt_DragonairSlam_AIEffect(ProbeState *s)
{
	(void)s;
	DragonairSlam_AIEffect();
}
/* <<< factory DragonairSlam_AIEffect */

/* >>> factory CheckIfPlayAreaHasAnyDamage */
static void adapt_CheckIfPlayAreaHasAnyDamage(ProbeState *s)
{
	CheckIfPlayAreaHasAnyDamageResult r = CheckIfPlayAreaHasAnyDamage();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckIfPlayAreaHasAnyDamage */



/* >>> factory CreateEnergyCardListFromDiscardPile_OnlyBasic */
static void adapt_CreateEnergyCardListFromDiscardPile_OnlyBasic(ProbeState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile_OnlyBasic();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateEnergyCardListFromDiscardPile_OnlyBasic */

/* >>> factory KabutoArmorEffect */
static void adapt_KabutoArmorEffect(ProbeState *s)
{
	s->f = KabutoArmorEffect(s->f);
}
/* <<< factory KabutoArmorEffect */

/* >>> factory CuboneRage_DamageBoostEffect */
static void adapt_CuboneRage_DamageBoostEffect(ProbeState *s)
{
	(void)s;
	CuboneRage_DamageBoostEffect();
}
/* <<< factory CuboneRage_DamageBoostEffect */

/* >>> factory PoisonEffect */
static void adapt_PoisonEffect(ProbeState *s)
{
	QueueStatusConditionResult r = PoisonEffect();
	s->f = r.f;
}
/* <<< factory PoisonEffect */

/* >>> factory DoublePoisonEffect */
static void adapt_DoublePoisonEffect(ProbeState *s)
{
	QueueStatusConditionResult r = DoublePoisonEffect();
	s->f = r.f;
}
/* <<< factory DoublePoisonEffect */

/* >>> factory LoadCardNameAndInputColor */
static void adapt_LoadCardNameAndInputColor(ProbeState *s)
{
	LoadCardNameAndInputColor(s->a, s->d, s->e);
}
/* <<< factory LoadCardNameAndInputColor */



/* >>> factory AIPickEnergyCardToDiscardFromDefendingPokemon */
static void adapt_AIPickEnergyCardToDiscardFromDefendingPokemon(ProbeState *s)
{
	AIPickEnergyCardToDiscardResult r =
		AIPickEnergyCardToDiscardFromDefendingPokemon();
	s->a = r.a;
}
/* <<< factory AIPickEnergyCardToDiscardFromDefendingPokemon */



/* >>> factory AIFindTargetForBenchAttack */
static void adapt_AIFindTargetForBenchAttack(ProbeState *s)
{
	AIFindTargetForBenchAttackResult r = AIFindTargetForBenchAttack();
	s->a = r.a;
}
/* <<< factory AIFindTargetForBenchAttack */



/* >>> factory ApplyExtraWaterEnergyDamageBonus */
static void adapt_ApplyExtraWaterEnergyDamageBonus(ProbeState *s)
{
	(void)s;
	ApplyExtraWaterEnergyDamageBonus();
}
/* <<< factory ApplyExtraWaterEnergyDamageBonus */


/* >>> factory OmastarSpikeCannon_AIEffect */
static void adapt_OmastarSpikeCannon_AIEffect(ProbeState *s)
{
	OmastarSpikeCannon_AIEffect();
	s->a = gb_read8(wAIMaxDamage_ADDR);
}
/* <<< factory OmastarSpikeCannon_AIEffect */

/* >>> factory ClairvoyanceEffect */
static void adapt_ClairvoyanceEffect(ProbeState *s)
{
	s->f = ClairvoyanceEffect(s->f);
}
/* <<< factory ClairvoyanceEffect */

/* >>> factory KrabbyCallForFamily_AISelectEffect */
static void adapt_KrabbyCallForFamily_AISelectEffect(ProbeState *s)
{
	KrabbyCallForFamily_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory KrabbyCallForFamily_AISelectEffect */

/* >>> factory CreateListOfEnergyAttachedToArena */
static void adapt_CreateListOfEnergyAttachedToArena(ProbeState *s)
{
	CreateListOfEnergyAttachedToArenaResult r = CreateListOfEnergyAttachedToArena(s->a);
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateListOfEnergyAttachedToArena */


/* >>> factory HandleNoDamageOrEffect */
static void adapt_HandleNoDamageOrEffect(ProbeState *s)
{
	HandleNoDamageOrEffectResult r = HandleNoDamageOrEffect(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory HandleNoDamageOrEffect */


/* >>> factory ArcanineFlamethrower_CheckEnergy */
static void adapt_ArcanineFlamethrower_CheckEnergy(ProbeState *s)
{
	ArcanineFlamethrowerCheckEnergyResult r = ArcanineFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ArcanineFlamethrower_CheckEnergy */

/* >>> factory ArcanineFlamethrower_DiscardEffect */
static void adapt_ArcanineFlamethrower_DiscardEffect(ProbeState *s)
{
	s->a = ArcanineFlamethrower_DiscardEffect();
}
/* <<< factory ArcanineFlamethrower_DiscardEffect */

/* >>> factory PoisonWhip_AIEffect */
static void adapt_PoisonWhip_AIEffect(ProbeState *s)
{
	(void)s;
	PoisonWhip_AIEffect();
}
/* <<< factory PoisonWhip_AIEffect */

/* >>> factory SolarPower_CheckUse */
static void adapt_SolarPower_CheckUse(ProbeState *s)
{
	SolarPowerCheckUseResult r = SolarPower_CheckUse();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SolarPower_CheckUse */

/* >>> factory DevolutionBeam_LoadAnimation */
static void adapt_DevolutionBeam_LoadAnimation(ProbeState *s)
{
	DevolutionBeam_LoadAnimation();
}
/* <<< factory DevolutionBeam_LoadAnimation */


/* >>> factory CheckIfTurnDuelistHasEvolvedCards */
static void adapt_CheckIfTurnDuelistHasEvolvedCards(ProbeState *s)
{
	CheckAttackResult r = CheckIfTurnDuelistHasEvolvedCards();
	s->f = r.f;
}
/* <<< factory CheckIfTurnDuelistHasEvolvedCards */

/* >>> factory FindFirstNonBasicCardInPlayArea */
static void adapt_FindFirstNonBasicCardInPlayArea(ProbeState *s)
{
	FindFirstNonBasicCardInPlayAreaResult r = FindFirstNonBasicCardInPlayArea();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory FindFirstNonBasicCardInPlayArea */

/* >>> factory Wildfire_AISelectEffect */
static void adapt_Wildfire_AISelectEffect(ProbeState *s)
{
	WildfireAISelectEffectResult r = Wildfire_AISelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Wildfire_AISelectEffect */

/* >>> factory FireBlast_CheckEnergy */
static void adapt_FireBlast_CheckEnergy(ProbeState *s)
{
	FireBlastCheckEnergyResult r = FireBlast_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FireBlast_CheckEnergy */

/* >>> factory BigEggsplosion_AIEffect */
static void adapt_BigEggsplosion_AIEffect(ProbeState *s)
{
	BigEggsplosion_AIEffect();
}
/* <<< factory BigEggsplosion_AIEffect */

/* >>> factory Thrash_AIEffect */
static void adapt_Thrash_AIEffect(ProbeState *s)
{
	Thrash_AIEffect();
}
/* <<< factory Thrash_AIEffect */

/* >>> factory Prophecy_CheckDeck */
static void adapt_Prophecy_CheckDeck(ProbeState *s)
{
	ProphecyCheckDeckResult r = Prophecy_CheckDeck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Prophecy_CheckDeck */

/* >>> factory TryGiveDamageCounter_DamageSwap */
static void adapt_TryGiveDamageCounter_DamageSwap(ProbeState *s)
{
	TryGiveDamageCounter_DamageSwapResult r = TryGiveDamageCounter_DamageSwap();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory TryGiveDamageCounter_DamageSwap */

/* >>> factory TransparencyEffect */
static void adapt_TransparencyEffect(ProbeState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | TransparencyEffect());
}
/* <<< factory TransparencyEffect */

/* >>> factory Barrier_CheckEnergy */
static void adapt_Barrier_CheckEnergy(ProbeState *s)
{
	BarrierCheckEnergyResult r = Barrier_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Barrier_CheckEnergy */

/* >>> factory ResetDevolvedCardStatus */
static void adapt_ResetDevolvedCardStatus(ProbeState *s)
{
	s->a = ResetDevolvedCardStatus();
}
/* <<< factory ResetDevolvedCardStatus */

/* >>> factory EeveeQuickAttack_AIEffect */
static void adapt_EeveeQuickAttack_AIEffect(ProbeState *s)
{
	(void)s;
	EeveeQuickAttack_AIEffect();
}
/* <<< factory EeveeQuickAttack_AIEffect */

/* >>> factory MirrorMove_AIEffect */
static void adapt_MirrorMove_AIEffect(ProbeState *s)
{
	(void)s;
	MirrorMove_AIEffect();
}
/* <<< factory MirrorMove_AIEffect */

/* >>> factory MirrorMove_InitialEffect1 */
static void adapt_MirrorMove_InitialEffect1(ProbeState *s)
{
	MirrorMoveInitialEffect1Result r = MirrorMove_InitialEffect1();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MirrorMove_InitialEffect1 */

/* >>> factory FuryAttack_AIEffect */
static void adapt_FuryAttack_AIEffect(ProbeState *s)
{
	(void)s;
	FuryAttack_AIEffect();
}
/* <<< factory FuryAttack_AIEffect */

/* >>> factory RetreatAidEffect */
static void adapt_RetreatAidEffect(ProbeState *s)
{
	s->f = RetreatAidEffect(s->f);
}
/* <<< factory RetreatAidEffect */

/* >>> factory FriendshipSong_BenchCheck */
static void adapt_FriendshipSong_BenchCheck(ProbeState *s)
{
	FriendshipSongBenchCheckResult r = FriendshipSong_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FriendshipSong_BenchCheck */

/* >>> factory ExpandEffect */
static void adapt_ExpandEffect(ProbeState *s)
{
	(void)s;
	ExpandEffect();
}
/* <<< factory ExpandEffect */

/* >>> factory CheckIfThereAreAnyEnergyCardsAttached */
static void adapt_CheckIfThereAreAnyEnergyCardsAttached(ProbeState *s)
{
	CheckIfThereAreAnyEnergyCardsAttachedResult r = CheckIfThereAreAnyEnergyCardsAttached();
	s->f = r.f;
}
/* <<< factory CheckIfThereAreAnyEnergyCardsAttached */

/* >>> factory PokeBall_DeckCheck */
static void adapt_PokeBall_DeckCheck(ProbeState *s)
{
	PokeBall_DeckCheckResult r = PokeBall_DeckCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokeBall_DeckCheck */

/* >>> factory Recycle_DiscardPileCheck */
static void adapt_Recycle_DiscardPileCheck(ProbeState *s)
{
	Recycle_DiscardPileCheckResult r = Recycle_DiscardPileCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory Recycle_DiscardPileCheck */

/* >>> factory CreateBasicPokemonCardListFromDiscardPile */
static void adapt_CreateBasicPokemonCardListFromDiscardPile(ProbeState *s)
{
	CreateBasicPokemonCardListFromDiscardPileResult r = CreateBasicPokemonCardListFromDiscardPile();
	s->f = r.f;
}
/* <<< factory CreateBasicPokemonCardListFromDiscardPile */


/* >>> factory CreatePokemonCardListFromHand */
static void adapt_CreatePokemonCardListFromHand(ProbeState *s)
{
	CreatePokemonCardListFromHandResult r = CreatePokemonCardListFromHand();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory CreatePokemonCardListFromHand */

/* >>> factory Pokedex_DeckCheck */
static void adapt_Pokedex_DeckCheck(ProbeState *s)
{
	PokedexDeckCheckResult r = Pokedex_DeckCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Pokedex_DeckCheck */

/* >>> factory Pokedex_OrderDeckCardsEffect */
static void adapt_Pokedex_OrderDeckCardsEffect(ProbeState *s)
{
	PokedexOrderDeckCardsEffectResult r = Pokedex_OrderDeckCardsEffect();
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Pokedex_OrderDeckCardsEffect */

/* >>> factory Maintenance_HandCheck */
static void adapt_Maintenance_HandCheck(ProbeState *s)
{
	MaintenanceHandCheckResult r = Maintenance_HandCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Maintenance_HandCheck */

/* >>> factory DevolutionSpray_PlayAreaEvolutionCheck */
static void adapt_DevolutionSpray_PlayAreaEvolutionCheck(ProbeState *s)
{
	DevolutionSprayPlayAreaEvolutionCheckResult r = DevolutionSpray_PlayAreaEvolutionCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory DevolutionSpray_PlayAreaEvolutionCheck */

/* >>> factory SpitPoison_AIEffect */
static void adapt_SpitPoison_AIEffect(ProbeState *s)
{
	(void)s;
	SpitPoison_AIEffect();
}
/* <<< factory SpitPoison_AIEffect */

/* >>> factory GloomPoisonPowder_AIEffect */
static void adapt_GloomPoisonPowder_AIEffect(ProbeState *s)
{
	(void)s;
	GloomPoisonPowder_AIEffect();
}
/* <<< factory GloomPoisonPowder_AIEffect */

/* >>> factory FoulOdorEffect */
static void adapt_FoulOdorEffect(ProbeState *s)
{
	s->f = FoulOdorEffect().f;
}
/* <<< factory FoulOdorEffect */

/* >>> factory KakunaPoisonPowder_AIEffect */
static void adapt_KakunaPoisonPowder_AIEffect(ProbeState *s)
{
	KakunaPoisonPowder_AIEffect();
	s->hl = wDamage_ADDR;
}
/* <<< factory KakunaPoisonPowder_AIEffect */

/* >>> factory SwordsDanceEffect */
static void adapt_SwordsDanceEffect(ProbeState *s)
{
	s->hl = SwordsDanceEffect();
}
/* <<< factory SwordsDanceEffect */

/* >>> factory Twineedle_AIEffect */
static void adapt_Twineedle_AIEffect(ProbeState *s)
{
	(void)s;
	Twineedle_AIEffect();
}
/* <<< factory Twineedle_AIEffect */

/* >>> factory BeedrillPoisonSting_AIEffect */
static void adapt_BeedrillPoisonSting_AIEffect(ProbeState *s)
{
	(void)s;
	BeedrillPoisonSting_AIEffect();
}
/* <<< factory BeedrillPoisonSting_AIEffect */

/* >>> factory FoulGas_AIEffect */
static void adapt_FoulGas_AIEffect(ProbeState *s)
{
	FoulGas_AIEffect();
}
/* <<< factory FoulGas_AIEffect */

/* >>> factory Sprout_AISelectEffect */
static void adapt_Sprout_AISelectEffect(ProbeState *s)
{
	Sprout_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory Sprout_AISelectEffect */

/* >>> factory Teleport_CheckBench */
static void adapt_Teleport_CheckBench(ProbeState *s)
{
    TeleportCheckBenchResult r = Teleport_CheckBench();
    s->a = r.a; s->f = r.f; s->hl = r.hl;
}
/* <<< factory Teleport_CheckBench */

/* >>> factory Teleport_AISelectEffect */
static void adapt_Teleport_AISelectEffect(ProbeState *s)
{
    TeleportAISelectEffectResult r = Teleport_AISelectEffect();
    s->a = r.a;
    s->hl = r.hl;
}
/* <<< factory Teleport_AISelectEffect */

/* >>> factory HornHazard_AIEffect */
static void adapt_HornHazard_AIEffect(ProbeState *s)
{
	(void)s;
	HornHazard_AIEffect();
}
/* <<< factory HornHazard_AIEffect */

/* >>> factory NidorinaDoubleKick_AIEffect */
static void adapt_NidorinaDoubleKick_AIEffect(ProbeState *s)
{
	(void)s;
	NidorinaDoubleKick_AIEffect();
}
/* <<< factory NidorinaDoubleKick_AIEffect */

/* >>> factory NidorinoDoubleKick_AIEffect */
static void adapt_NidorinoDoubleKick_AIEffect(ProbeState *s)
{
	NidorinoDoubleKick_AIEffect();
}
/* <<< factory NidorinoDoubleKick_AIEffect */

/* >>> factory WeedlePoisonSting_AIEffect */
static void adapt_WeedlePoisonSting_AIEffect(ProbeState *s)
{
	WeedlePoisonSting_AIEffect();
}
/* <<< factory WeedlePoisonSting_AIEffect */

/* >>> factory BellsproutCallForFamily_AISelectEffect */
static void adapt_BellsproutCallForFamily_AISelectEffect(ProbeState *s)
{
	BellsproutCallForFamily_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory BellsproutCallForFamily_AISelectEffect */

/* >>> factory WeezingSmog_AIEffect */
static void adapt_WeezingSmog_AIEffect(ProbeState *s)
{
	WeezingSmog_AIEffect();
}
/* <<< factory WeezingSmog_AIEffect */

const ProbeEntry probe_entries_effect_functions[] = {
	{ "UpdateExpectedAIDamage", adapt_UpdateExpectedAIDamage },
	{ "SetExpectedAIDamage", adapt_SetExpectedAIDamage },
	{ "UpdateExpectedAIDamage_AccountForPoison", adapt_UpdateExpectedAIDamage_AccountForPoison },
	{ "IsPlayerTurn", adapt_IsPlayerTurn },
	{ "ApplySubstatus1ToAttackingCard", adapt_ApplySubstatus1ToAttackingCard },
	{ "SetNoEffectFromStatus", adapt_SetNoEffectFromStatus },
	{ "SetDefiniteAIDamage", adapt_SetDefiniteAIDamage },
	{ "PickRandomPlayAreaCard", adapt_PickRandomPlayAreaCard },
	{ "GetNextPositionInTempList", adapt_GetNextPositionInTempList },
	{ "QueueStatusCondition", adapt_QueueStatusCondition },
	{ "CommentedOut_2c086", adapt_CommentedOut_2c086 },
	{ "SetWasUnsuccessful", adapt_SetWasUnsuccessful },
	{ "Teleport_SwitchEffect", adapt_Teleport_SwitchEffect },
	{ "SetDamageToATimes20", adapt_SetDamageToATimes20 },
	{ "CreateTrainerCardListFromDiscardPile", adapt_CreateTrainerCardListFromDiscardPile },
	{ "CreateEnergyCardListFromDiscardPile", adapt_CreateEnergyCardListFromDiscardPile },
	{ "HandleAIMetronomeEffect", adapt_HandleAIMetronomeEffect },
	{ "ParalysisEffect", adapt_ParalysisEffect },
	{ "ConfusionEffect", adapt_ConfusionEffect },
	{ "InvisibleWallEffect", adapt_InvisibleWallEffect },
	{ "GetAttackName", adapt_GetAttackName },
	{ "CheckIfDefendingPokemonHasAnyAttack", adapt_CheckIfDefendingPokemonHasAnyAttack },
	{ "UpdateDevolvedCardHPAndStage", adapt_UpdateDevolvedCardHPAndStage },
	{ "DragonairSlam_AIEffect", adapt_DragonairSlam_AIEffect },
	{ "ClefableMinimizeEffect", adapt_ClefableMinimizeEffect },
	{ "CreateEnergyCardListFromDiscardPile_OnlyBasic", adapt_CreateEnergyCardListFromDiscardPile_OnlyBasic },
	{ "KabutoArmorEffect", adapt_KabutoArmorEffect },
	{ "CuboneRage_DamageBoostEffect", adapt_CuboneRage_DamageBoostEffect },
	{ "PoisonEffect", adapt_PoisonEffect },
	{ "DoublePoisonEffect", adapt_DoublePoisonEffect },
	{ "LoadCardNameAndInputColor", adapt_LoadCardNameAndInputColor },
	{ "OmastarSpikeCannon_AIEffect", adapt_OmastarSpikeCannon_AIEffect },
	{ "ClairvoyanceEffect", adapt_ClairvoyanceEffect },
	{ "KrabbyCallForFamily_AISelectEffect", adapt_KrabbyCallForFamily_AISelectEffect },
	{ "ArcanineFlamethrower_CheckEnergy", adapt_ArcanineFlamethrower_CheckEnergy },
	{ "ArcanineFlamethrower_DiscardEffect", adapt_ArcanineFlamethrower_DiscardEffect },
	{ "PoisonWhip_AIEffect", adapt_PoisonWhip_AIEffect },
	{ "SolarPower_CheckUse", adapt_SolarPower_CheckUse },
	{ "ApplyExtraWaterEnergyDamageBonus", adapt_ApplyExtraWaterEnergyDamageBonus },
	{ "CheckIfTurnDuelistHasEvolvedCards", adapt_CheckIfTurnDuelistHasEvolvedCards },
	{ "FindFirstNonBasicCardInPlayArea", adapt_FindFirstNonBasicCardInPlayArea },
	{ "CreateListOfEnergyAttachedToArena", adapt_CreateListOfEnergyAttachedToArena },
	{ "HandleNoDamageOrEffect", adapt_HandleNoDamageOrEffect },
	{ "CheckIfPlayAreaHasAnyDamage", adapt_CheckIfPlayAreaHasAnyDamage },
	{ "Wildfire_AISelectEffect", adapt_Wildfire_AISelectEffect },
	{ "FireBlast_CheckEnergy", adapt_FireBlast_CheckEnergy },
	{ "BigEggsplosion_AIEffect", adapt_BigEggsplosion_AIEffect },
	{ "Thrash_AIEffect", adapt_Thrash_AIEffect },
	{ "Prophecy_CheckDeck", adapt_Prophecy_CheckDeck },
	{ "TryGiveDamageCounter_DamageSwap", adapt_TryGiveDamageCounter_DamageSwap },
	{ "DevolutionBeam_LoadAnimation", adapt_DevolutionBeam_LoadAnimation },
	{ "TransparencyEffect", adapt_TransparencyEffect },
	{ "Barrier_CheckEnergy", adapt_Barrier_CheckEnergy },
	{ "ResetDevolvedCardStatus", adapt_ResetDevolvedCardStatus },
	{ "AIPickEnergyCardToDiscardFromDefendingPokemon", adapt_AIPickEnergyCardToDiscardFromDefendingPokemon },
	{ "AIFindTargetForBenchAttack", adapt_AIFindTargetForBenchAttack },
	{ "EeveeQuickAttack_AIEffect", adapt_EeveeQuickAttack_AIEffect },
	{ "MirrorMove_AIEffect", adapt_MirrorMove_AIEffect },
	{ "MirrorMove_InitialEffect1", adapt_MirrorMove_InitialEffect1 },
	{ "FuryAttack_AIEffect", adapt_FuryAttack_AIEffect },
	{ "RetreatAidEffect", adapt_RetreatAidEffect },
	{ "DodrioRage_DamageBoostEffect", adapt_DodrioRage_DamageBoostEffect },
	{ "FriendshipSong_BenchCheck", adapt_FriendshipSong_BenchCheck },
	{ "ExpandEffect", adapt_ExpandEffect },
	{ "CheckIfThereAreAnyEnergyCardsAttached", adapt_CheckIfThereAreAnyEnergyCardsAttached },
	{ "PokeBall_DeckCheck", adapt_PokeBall_DeckCheck },
	{ "Recycle_DiscardPileCheck", adapt_Recycle_DiscardPileCheck },
	{ "CreatePokemonCardListFromHand", adapt_CreatePokemonCardListFromHand },
	{ "Pokedex_DeckCheck", adapt_Pokedex_DeckCheck },
	{ "Pokedex_OrderDeckCardsEffect", adapt_Pokedex_OrderDeckCardsEffect },
	{ "Maintenance_HandCheck", adapt_Maintenance_HandCheck },
	{ "CreateBasicPokemonCardListFromDiscardPile", adapt_CreateBasicPokemonCardListFromDiscardPile },
	{ "DevolutionSpray_PlayAreaEvolutionCheck", adapt_DevolutionSpray_PlayAreaEvolutionCheck },
	{ "SpitPoison_AIEffect", adapt_SpitPoison_AIEffect },
	{ "GloomPoisonPowder_AIEffect", adapt_GloomPoisonPowder_AIEffect },
	{ "FoulOdorEffect", adapt_FoulOdorEffect },
	{ "KakunaPoisonPowder_AIEffect", adapt_KakunaPoisonPowder_AIEffect },
	{ "SwordsDanceEffect", adapt_SwordsDanceEffect },
	{ "Twineedle_AIEffect", adapt_Twineedle_AIEffect },
	{ "BeedrillPoisonSting_AIEffect", adapt_BeedrillPoisonSting_AIEffect },
	{ "FoulGas_AIEffect", adapt_FoulGas_AIEffect },
	{ "Sprout_AISelectEffect", adapt_Sprout_AISelectEffect },
	{ "Teleport_CheckBench", adapt_Teleport_CheckBench },
	{ "Teleport_AISelectEffect", adapt_Teleport_AISelectEffect },
	{ "HornHazard_AIEffect", adapt_HornHazard_AIEffect },
	{ "NidorinaDoubleKick_AIEffect", adapt_NidorinaDoubleKick_AIEffect },
	{ "NidorinoDoubleKick_AIEffect", adapt_NidorinoDoubleKick_AIEffect },
	{ "WeedlePoisonSting_AIEffect", adapt_WeedlePoisonSting_AIEffect },
	{ "BellsproutCallForFamily_AISelectEffect", adapt_BellsproutCallForFamily_AISelectEffect },
	{ "WeezingSmog_AIEffect", adapt_WeezingSmog_AIEffect },
	{ NULL, NULL },
};
