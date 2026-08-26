#include "home/effect_functions.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/effect_dispatch.h"

#include <string.h>




/* >>> factory UpdateExpectedAIDamage */
static void adapt_UpdateExpectedAIDamage(EffectDispatchState *s)
{
	UpdateExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory UpdateExpectedAIDamage */


/* >>> factory SetExpectedAIDamage */
static void adapt_SetExpectedAIDamage(EffectDispatchState *s)
{
	SetExpectedAIDamage(s->a, s->d, s->e);
}
/* <<< factory SetExpectedAIDamage */


/* >>> factory IsPlayerTurn */
static void adapt_IsPlayerTurn(EffectDispatchState *s)
{
	IsPlayerTurnResult r = IsPlayerTurn();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory IsPlayerTurn */


/* >>> factory UpdateExpectedAIDamage_AccountForPoison */
static void adapt_UpdateExpectedAIDamage_AccountForPoison(EffectDispatchState *s)
{
	UpdateExpectedAIDamage_AccountForPoison(s->a, s->d, s->e);
}
/* <<< factory UpdateExpectedAIDamage_AccountForPoison */

/* >>> factory ApplySubstatus1ToAttackingCard */
static void adapt_ApplySubstatus1ToAttackingCard(EffectDispatchState *s)
{
	s->hl = ApplySubstatus1ToAttackingCard(s->a);
}
/* <<< factory ApplySubstatus1ToAttackingCard */


/* >>> factory SetNoEffectFromStatus */
static void adapt_SetNoEffectFromStatus(EffectDispatchState *s)
{
	(void)s;
	SetNoEffectFromStatus();
}
/* <<< factory SetNoEffectFromStatus */

/* >>> factory SetDefiniteAIDamage */
static void adapt_SetDefiniteAIDamage(EffectDispatchState *s)
{
	(void)s;
	SetDefiniteAIDamage();
}
/* <<< factory SetDefiniteAIDamage */
/* >>> factory SetDefiniteDamage */
static void adapt_SetDefiniteDamage(EffectDispatchState *s)
{
	SetDefiniteDamage(s->a);
}
/* <<< factory SetDefiniteDamage */


/* >>> factory PickRandomPlayAreaCard */
static void adapt_PickRandomPlayAreaCard(EffectDispatchState *s)
{
	PickRandomPlayAreaCardResult r = PickRandomPlayAreaCard();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PickRandomPlayAreaCard */

/* >>> factory GetNextPositionInTempList */
static void adapt_GetNextPositionInTempList(EffectDispatchState *s)
{
	s->hl = GetNextPositionInTempList();
}
/* <<< factory GetNextPositionInTempList */

/* >>> factory QueueStatusCondition */
static void adapt_QueueStatusCondition(EffectDispatchState *s)
{
	QueueStatusConditionResult r = QueueStatusCondition(s->b, s->c);
	s->f = r.f;
}
/* <<< factory QueueStatusCondition */
/* >>> factory SleepEffect */
static void adapt_SleepEffect(EffectDispatchState *s)
{
	QueueStatusConditionResult r = SleepEffect();
	s->f = r.f;
}
/* <<< factory SleepEffect */


/* >>> factory CommentedOut_2c086 */
static void adapt_CommentedOut_2c086(EffectDispatchState *s)
{
	s->a = CommentedOut_2c086(s->a);
}
/* <<< factory CommentedOut_2c086 */

/* >>> factory SetWasUnsuccessful */
static void adapt_SetWasUnsuccessful(EffectDispatchState *s)
{
	(void)s;
	SetWasUnsuccessful();
}
/* <<< factory SetWasUnsuccessful */

/* >>> factory Teleport_SwitchEffect */
static void adapt_Teleport_SwitchEffect(EffectDispatchState *s)
{
	Teleport_SwitchEffect();
}
/* <<< factory Teleport_SwitchEffect */

/* >>> factory SetDamageToATimes20 */
static void adapt_SetDamageToATimes20(EffectDispatchState *s)
{
	SetDamageToATimes20(s->a);
}
/* <<< factory SetDamageToATimes20 */

/* >>> factory CreateTrainerCardListFromDiscardPile */
static void adapt_CreateTrainerCardListFromDiscardPile(EffectDispatchState *s)
{
	CreateTrainerCardListFromDiscardPileResult r = CreateTrainerCardListFromDiscardPile();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateTrainerCardListFromDiscardPile */

/* >>> factory CreateEnergyCardListFromDiscardPile */
static void adapt_CreateEnergyCardListFromDiscardPile(EffectDispatchState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile(s->c);
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateEnergyCardListFromDiscardPile */

/* >>> factory GetAttackName */
static void adapt_GetAttackName(EffectDispatchState *s)
{
	uint16_t hl = GetAttackName(s->d, s->e);
	s->hl = hl;
}
/* <<< factory GetAttackName */


/* >>> factory ClefableMinimizeEffect */
static void adapt_ClefableMinimizeEffect(EffectDispatchState *s)
{
	s->hl = ClefableMinimizeEffect();
}
/* <<< factory ClefableMinimizeEffect */


/* >>> factory HandleAIMetronomeEffect */
static void adapt_HandleAIMetronomeEffect(EffectDispatchState *s)
{
	(void)s;
	HandleAIMetronomeEffect();
}
/* <<< factory HandleAIMetronomeEffect */

/* >>> factory ParalysisEffect */
static void adapt_ParalysisEffect(EffectDispatchState *s)
{
	QueueStatusConditionResult r = ParalysisEffect();
	s->f = r.f;
}
/* <<< factory ParalysisEffect */

/* >>> factory ConfusionEffect */
static void adapt_ConfusionEffect(EffectDispatchState *s)
{
	QueueStatusConditionResult r = ConfusionEffect();
	s->f = r.f;
}
/* <<< factory ConfusionEffect */

/* >>> factory InvisibleWallEffect */
static void adapt_InvisibleWallEffect(EffectDispatchState *s)
{
	s->f = InvisibleWallEffect(s->f);
}
/* <<< factory InvisibleWallEffect */

/* >>> factory CheckIfDefendingPokemonHasAnyAttack */
static void adapt_CheckIfDefendingPokemonHasAnyAttack(EffectDispatchState *s)
{
	CheckAttackResult r = CheckIfDefendingPokemonHasAnyAttack();
	s->f = r.f;
}
/* <<< factory CheckIfDefendingPokemonHasAnyAttack */

/* >>> factory UpdateDevolvedCardHPAndStage */
static void adapt_UpdateDevolvedCardHPAndStage(EffectDispatchState *s)
{
	UpdateDevolvedCardHPAndStage(s->a);
}
/* <<< factory UpdateDevolvedCardHPAndStage */

/* >>> factory DodrioRage_DamageBoostEffect */
static void adapt_DodrioRage_DamageBoostEffect(EffectDispatchState *s)
{
	(void)s;
	DodrioRage_DamageBoostEffect();
}
/* <<< factory DodrioRage_DamageBoostEffect */


/* >>> factory DragonairSlam_AIEffect */
static void adapt_DragonairSlam_AIEffect(EffectDispatchState *s)
{
	(void)s;
	DragonairSlam_AIEffect();
}
/* <<< factory DragonairSlam_AIEffect */

/* >>> factory CheckIfPlayAreaHasAnyDamage */
static void adapt_CheckIfPlayAreaHasAnyDamage(EffectDispatchState *s)
{
	CheckIfPlayAreaHasAnyDamageResult r = CheckIfPlayAreaHasAnyDamage();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory CheckIfPlayAreaHasAnyDamage */



/* >>> factory CreateEnergyCardListFromDiscardPile_OnlyBasic */
static void adapt_CreateEnergyCardListFromDiscardPile_OnlyBasic(EffectDispatchState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile_OnlyBasic();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateEnergyCardListFromDiscardPile_OnlyBasic */

/* >>> factory KabutoArmorEffect */
static void adapt_KabutoArmorEffect(EffectDispatchState *s)
{
	s->f = KabutoArmorEffect(s->f);
}
/* <<< factory KabutoArmorEffect */

/* >>> factory CuboneRage_DamageBoostEffect */
static void adapt_CuboneRage_DamageBoostEffect(EffectDispatchState *s)
{
	(void)s;
	CuboneRage_DamageBoostEffect();
}
/* <<< factory CuboneRage_DamageBoostEffect */

/* >>> factory PoisonEffect */
static void adapt_PoisonEffect(EffectDispatchState *s)
{
	QueueStatusConditionResult r = PoisonEffect();
	s->f = r.f;
}
/* <<< factory PoisonEffect */

/* >>> factory DoublePoisonEffect */
static void adapt_DoublePoisonEffect(EffectDispatchState *s)
{
	QueueStatusConditionResult r = DoublePoisonEffect();
	s->f = r.f;
}
/* <<< factory DoublePoisonEffect */

/* >>> factory LoadCardNameAndInputColor */
static void adapt_LoadCardNameAndInputColor(EffectDispatchState *s)
{
	LoadCardNameAndInputColor(s->a, s->d, s->e);
}
/* <<< factory LoadCardNameAndInputColor */




/* >>> factory AIPickEnergyCardToDiscardFromDefendingPokemon */
static void adapt_AIPickEnergyCardToDiscardFromDefendingPokemon(EffectDispatchState *s)
{
	AIPickEnergyCardToDiscardResult r =
		AIPickEnergyCardToDiscardFromDefendingPokemon();
	s->a = r.a;
}
/* <<< factory AIPickEnergyCardToDiscardFromDefendingPokemon */




/* >>> factory AIFindTargetForBenchAttack */
static void adapt_AIFindTargetForBenchAttack(EffectDispatchState *s)
{
	AIFindTargetForBenchAttackResult r = AIFindTargetForBenchAttack();
	s->a = r.a;
}
/* <<< factory AIFindTargetForBenchAttack */




/* >>> factory ApplyExtraWaterEnergyDamageBonus */
static void adapt_ApplyExtraWaterEnergyDamageBonus(EffectDispatchState *s)
{
	ApplyExtraWaterEnergyDamageBonus(s->b, s->c);
}
/* <<< factory ApplyExtraWaterEnergyDamageBonus */




/* >>> factory OmastarSpikeCannon_AIEffect */
static void adapt_OmastarSpikeCannon_AIEffect(EffectDispatchState *s)
{
	OmastarSpikeCannon_AIEffect();
	s->a = gb_read8(wAIMaxDamage_ADDR);
}
/* <<< factory OmastarSpikeCannon_AIEffect */



/* >>> factory ClairvoyanceEffect */
static void adapt_ClairvoyanceEffect(EffectDispatchState *s)
{
	s->f = ClairvoyanceEffect(s->f);
}
/* <<< factory ClairvoyanceEffect */



/* >>> factory KrabbyCallForFamily_AISelectEffect */
static void adapt_KrabbyCallForFamily_AISelectEffect(EffectDispatchState *s)
{
	KrabbyCallForFamily_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory KrabbyCallForFamily_AISelectEffect */

/* >>> factory CreateListOfEnergyAttachedToArena */
static void adapt_CreateListOfEnergyAttachedToArena(EffectDispatchState *s)
{
	CreateListOfEnergyAttachedToArenaResult r = CreateListOfEnergyAttachedToArena(s->a);
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateListOfEnergyAttachedToArena */


/* >>> factory HandleNoDamageOrEffect */
static void adapt_HandleNoDamageOrEffect(EffectDispatchState *s)
{
	HandleNoDamageOrEffectResult r = HandleNoDamageOrEffect(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory HandleNoDamageOrEffect */


/* >>> factory ArcanineFlamethrower_CheckEnergy */
static void adapt_ArcanineFlamethrower_CheckEnergy(EffectDispatchState *s)
{
	ArcanineFlamethrowerCheckEnergyResult r = ArcanineFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory ArcanineFlamethrower_CheckEnergy */

/* >>> factory ArcanineFlamethrower_DiscardEffect */
static void adapt_ArcanineFlamethrower_DiscardEffect(EffectDispatchState *s)
{
	s->a = ArcanineFlamethrower_DiscardEffect();
}
/* <<< factory ArcanineFlamethrower_DiscardEffect */

/* >>> factory PoisonWhip_AIEffect */
static void adapt_PoisonWhip_AIEffect(EffectDispatchState *s)
{
	(void)s;
	PoisonWhip_AIEffect();
}
/* <<< factory PoisonWhip_AIEffect */


/* >>> factory SolarPower_CheckUse */
static void adapt_SolarPower_CheckUse(EffectDispatchState *s)
{
	SolarPowerCheckUseResult r = SolarPower_CheckUse();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SolarPower_CheckUse */


/* >>> factory DevolutionBeam_LoadAnimation */
static void adapt_DevolutionBeam_LoadAnimation(EffectDispatchState *s)
{
	DevolutionBeam_LoadAnimation();
}
/* <<< factory DevolutionBeam_LoadAnimation */


/* >>> factory CheckIfTurnDuelistHasEvolvedCards */
static void adapt_CheckIfTurnDuelistHasEvolvedCards(EffectDispatchState *s)
{
	CheckAttackResult r = CheckIfTurnDuelistHasEvolvedCards();
	s->f = r.f;
}
/* <<< factory CheckIfTurnDuelistHasEvolvedCards */


/* >>> factory FindFirstNonBasicCardInPlayArea */
static void adapt_FindFirstNonBasicCardInPlayArea(EffectDispatchState *s)
{
	FindFirstNonBasicCardInPlayAreaResult r = FindFirstNonBasicCardInPlayArea();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory FindFirstNonBasicCardInPlayArea */


/* >>> factory Wildfire_AISelectEffect */
static void adapt_Wildfire_AISelectEffect(EffectDispatchState *s)
{
	WildfireAISelectEffectResult r = Wildfire_AISelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Wildfire_AISelectEffect */

/* >>> factory FireBlast_CheckEnergy */
static void adapt_FireBlast_CheckEnergy(EffectDispatchState *s)
{
	FireBlastCheckEnergyResult r = FireBlast_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FireBlast_CheckEnergy */

/* >>> factory BigEggsplosion_AIEffect */
static void adapt_BigEggsplosion_AIEffect(EffectDispatchState *s)
{
	BigEggsplosion_AIEffect();
}
/* <<< factory BigEggsplosion_AIEffect */

/* >>> factory Thrash_AIEffect */
static void adapt_Thrash_AIEffect(EffectDispatchState *s)
{
	Thrash_AIEffect();
}
/* <<< factory Thrash_AIEffect */

/* >>> factory Prophecy_CheckDeck */
static void adapt_Prophecy_CheckDeck(EffectDispatchState *s)
{
	ProphecyCheckDeckResult r = Prophecy_CheckDeck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Prophecy_CheckDeck */

/* >>> factory TryGiveDamageCounter_DamageSwap */
static void adapt_TryGiveDamageCounter_DamageSwap(EffectDispatchState *s)
{
	TryGiveDamageCounter_DamageSwapResult r = TryGiveDamageCounter_DamageSwap();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory TryGiveDamageCounter_DamageSwap */

/* >>> factory TransparencyEffect */
static void adapt_TransparencyEffect(EffectDispatchState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | TransparencyEffect());
}
/* <<< factory TransparencyEffect */

/* >>> factory Barrier_CheckEnergy */
static void adapt_Barrier_CheckEnergy(EffectDispatchState *s)
{
	BarrierCheckEnergyResult r = Barrier_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Barrier_CheckEnergy */

/* >>> factory ResetDevolvedCardStatus */
static void adapt_ResetDevolvedCardStatus(EffectDispatchState *s)
{
	s->a = ResetDevolvedCardStatus();
}
/* <<< factory ResetDevolvedCardStatus */

/* >>> factory EeveeQuickAttack_AIEffect */
static void adapt_EeveeQuickAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	EeveeQuickAttack_AIEffect();
}
/* <<< factory EeveeQuickAttack_AIEffect */

/* >>> factory MirrorMove_AIEffect */
static void adapt_MirrorMove_AIEffect(EffectDispatchState *s)
{
	(void)s;
	MirrorMove_AIEffect();
}
/* <<< factory MirrorMove_AIEffect */

/* >>> factory MirrorMove_InitialEffect1 */
static void adapt_MirrorMove_InitialEffect1(EffectDispatchState *s)
{
	MirrorMoveInitialEffect1Result r = MirrorMove_InitialEffect1();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MirrorMove_InitialEffect1 */

/* >>> factory FuryAttack_AIEffect */
static void adapt_FuryAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	FuryAttack_AIEffect();
}
/* <<< factory FuryAttack_AIEffect */

/* >>> factory RetreatAidEffect */
static void adapt_RetreatAidEffect(EffectDispatchState *s)
{
	s->f = RetreatAidEffect(s->f);
}
/* <<< factory RetreatAidEffect */

/* >>> factory FriendshipSong_BenchCheck */
static void adapt_FriendshipSong_BenchCheck(EffectDispatchState *s)
{
	FriendshipSongBenchCheckResult r = FriendshipSong_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FriendshipSong_BenchCheck */

/* >>> factory ExpandEffect */
static void adapt_ExpandEffect(EffectDispatchState *s)
{
	(void)s;
	ExpandEffect();
}
/* <<< factory ExpandEffect */

/* >>> factory CheckIfThereAreAnyEnergyCardsAttached */
static void adapt_CheckIfThereAreAnyEnergyCardsAttached(EffectDispatchState *s)
{
	CheckIfThereAreAnyEnergyCardsAttachedResult r = CheckIfThereAreAnyEnergyCardsAttached();
	s->f = r.f;
}
/* <<< factory CheckIfThereAreAnyEnergyCardsAttached */

/* >>> factory PokeBall_DeckCheck */
static void adapt_PokeBall_DeckCheck(EffectDispatchState *s)
{
	PokeBall_DeckCheckResult r = PokeBall_DeckCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokeBall_DeckCheck */

/* >>> factory Recycle_DiscardPileCheck */
static void adapt_Recycle_DiscardPileCheck(EffectDispatchState *s)
{
	Recycle_DiscardPileCheckResult r = Recycle_DiscardPileCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory Recycle_DiscardPileCheck */

/* >>> factory CreateBasicPokemonCardListFromDiscardPile */
static void adapt_CreateBasicPokemonCardListFromDiscardPile(EffectDispatchState *s)
{
	CreateBasicPokemonCardListFromDiscardPileResult r = CreateBasicPokemonCardListFromDiscardPile();
	s->f = r.f;
}
/* <<< factory CreateBasicPokemonCardListFromDiscardPile */


/* >>> factory CreatePokemonCardListFromHand */
static void adapt_CreatePokemonCardListFromHand(EffectDispatchState *s)
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
static void adapt_Pokedex_DeckCheck(EffectDispatchState *s)
{
	PokedexDeckCheckResult r = Pokedex_DeckCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Pokedex_DeckCheck */

/* >>> factory Pokedex_OrderDeckCardsEffect */
static void adapt_Pokedex_OrderDeckCardsEffect(EffectDispatchState *s)
{
	PokedexOrderDeckCardsEffectResult r = Pokedex_OrderDeckCardsEffect();
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Pokedex_OrderDeckCardsEffect */

/* >>> factory Maintenance_HandCheck */
static void adapt_Maintenance_HandCheck(EffectDispatchState *s)
{
	MaintenanceHandCheckResult r = Maintenance_HandCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Maintenance_HandCheck */

/* >>> factory DevolutionSpray_PlayAreaEvolutionCheck */
static void adapt_DevolutionSpray_PlayAreaEvolutionCheck(EffectDispatchState *s)
{
	DevolutionSprayPlayAreaEvolutionCheckResult r = DevolutionSpray_PlayAreaEvolutionCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory DevolutionSpray_PlayAreaEvolutionCheck */

/* >>> factory SpitPoison_AIEffect */
static void adapt_SpitPoison_AIEffect(EffectDispatchState *s)
{
	(void)s;
	SpitPoison_AIEffect();
}
/* <<< factory SpitPoison_AIEffect */

/* >>> factory GloomPoisonPowder_AIEffect */
static void adapt_GloomPoisonPowder_AIEffect(EffectDispatchState *s)
{
	(void)s;
	GloomPoisonPowder_AIEffect();
}
/* <<< factory GloomPoisonPowder_AIEffect */

/* >>> factory FoulOdorEffect */
static void adapt_FoulOdorEffect(EffectDispatchState *s)
{
	s->f = FoulOdorEffect().f;
}
/* <<< factory FoulOdorEffect */

/* >>> factory KakunaPoisonPowder_AIEffect */
static void adapt_KakunaPoisonPowder_AIEffect(EffectDispatchState *s)
{
	KakunaPoisonPowder_AIEffect();
	s->hl = wDamage_ADDR;
}
/* <<< factory KakunaPoisonPowder_AIEffect */


/* >>> factory SwordsDanceEffect */
static void adapt_SwordsDanceEffect(EffectDispatchState *s)
{
	s->hl = SwordsDanceEffect();
}
/* <<< factory SwordsDanceEffect */


/* >>> factory Twineedle_AIEffect */
static void adapt_Twineedle_AIEffect(EffectDispatchState *s)
{
	(void)s;
	Twineedle_AIEffect();
}
/* <<< factory Twineedle_AIEffect */


/* >>> factory BeedrillPoisonSting_AIEffect */
static void adapt_BeedrillPoisonSting_AIEffect(EffectDispatchState *s)
{
	(void)s;
	BeedrillPoisonSting_AIEffect();
}
/* <<< factory BeedrillPoisonSting_AIEffect */


/* >>> factory FoulGas_AIEffect */
static void adapt_FoulGas_AIEffect(EffectDispatchState *s)
{
	FoulGas_AIEffect();
}
/* <<< factory FoulGas_AIEffect */


/* >>> factory Sprout_AISelectEffect */
static void adapt_Sprout_AISelectEffect(EffectDispatchState *s)
{
	Sprout_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory Sprout_AISelectEffect */


/* >>> factory Teleport_CheckBench */
static void adapt_Teleport_CheckBench(EffectDispatchState *s)
{
    TeleportCheckBenchResult r = Teleport_CheckBench();
    s->a = r.a; s->f = r.f; s->hl = r.hl;
}
/* <<< factory Teleport_CheckBench */


/* >>> factory Teleport_AISelectEffect */
static void adapt_Teleport_AISelectEffect(EffectDispatchState *s)
{
    TeleportAISelectEffectResult r = Teleport_AISelectEffect();
    s->a = r.a;
    s->hl = r.hl;
}
/* <<< factory Teleport_AISelectEffect */


/* >>> factory HornHazard_AIEffect */
static void adapt_HornHazard_AIEffect(EffectDispatchState *s)
{
	(void)s;
	HornHazard_AIEffect();
}
/* <<< factory HornHazard_AIEffect */


/* >>> factory NidorinaDoubleKick_AIEffect */
static void adapt_NidorinaDoubleKick_AIEffect(EffectDispatchState *s)
{
	(void)s;
	NidorinaDoubleKick_AIEffect();
}
/* <<< factory NidorinaDoubleKick_AIEffect */


/* >>> factory NidorinoDoubleKick_AIEffect */
static void adapt_NidorinoDoubleKick_AIEffect(EffectDispatchState *s)
{
	NidorinoDoubleKick_AIEffect();
}
/* <<< factory NidorinoDoubleKick_AIEffect */

/* >>> factory WeedlePoisonSting_AIEffect */
static void adapt_WeedlePoisonSting_AIEffect(EffectDispatchState *s)
{
	WeedlePoisonSting_AIEffect();
}
/* <<< factory WeedlePoisonSting_AIEffect */

/* >>> factory BellsproutCallForFamily_AISelectEffect */
static void adapt_BellsproutCallForFamily_AISelectEffect(EffectDispatchState *s)
{
	BellsproutCallForFamily_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory BellsproutCallForFamily_AISelectEffect */

/* >>> factory WeezingSmog_AIEffect */
static void adapt_WeezingSmog_AIEffect(EffectDispatchState *s)
{
	WeezingSmog_AIEffect();
}
/* <<< factory WeezingSmog_AIEffect */

/* >>> factory NidoranFFurySwipes_AIEffect */
static void adapt_NidoranFFurySwipes_AIEffect(EffectDispatchState *s)
{
	(void)s;
	NidoranFFurySwipes_AIEffect();
}
/* <<< factory NidoranFFurySwipes_AIEffect */


/* >>> factory NidoranFCallForFamily_AISelectEffect */
static void adapt_NidoranFCallForFamily_AISelectEffect(EffectDispatchState *s)
{
	NidoranFCallForFamily_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory NidoranFCallForFamily_AISelectEffect */


/* >>> factory ToxicGasEffect */
static void adapt_ToxicGasEffect(EffectDispatchState *s)
{
	s->f = ToxicGasEffect(s->f);
}
/* <<< factory ToxicGasEffect */


/* >>> factory Sludge_AIEffect */
static void adapt_Sludge_AIEffect(EffectDispatchState *s)
{
	Sludge_AIEffect();
	s->hl = wDamage_ADDR;
}
/* <<< factory Sludge_AIEffect */


/* >>> factory KadabraRecover_DiscardEffect */
static void adapt_KadabraRecover_DiscardEffect(EffectDispatchState *s)
{
	s->a = KadabraRecover_DiscardEffect();
}
/* <<< factory KadabraRecover_DiscardEffect */

/* >>> factory PrimeapeFurySwipes_AIEffect */
static void adapt_PrimeapeFurySwipes_AIEffect(EffectDispatchState *s)
{
	PrimeapeFurySwipesAIResult r = PrimeapeFurySwipes_AIEffect();
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory PrimeapeFurySwipes_AIEffect */

/* >>> factory StretchKick_CheckBench */
static void adapt_StretchKick_CheckBench(EffectDispatchState *s)
{
	StretchKickCheckBenchResult r = StretchKick_CheckBench();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory StretchKick_CheckBench */
/* >>> factory Cowardice_CheckUseAndBench */
static void adapt_Cowardice_CheckUseAndBench(EffectDispatchState *s)
{
	CowardiceCheckUseAndBenchResult r = Cowardice_CheckUseAndBench();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Cowardice_CheckUseAndBench */



/* >>> factory Cowardice_ReturnToHandEffect */
static void adapt_Cowardice_ReturnToHandEffect(EffectDispatchState *s)
{
	Cowardice_ReturnToHandEffect();
	s->a = gb_read8(wDuelDisplayedScreen_ADDR);
}
/* <<< factory Cowardice_ReturnToHandEffect */




/* >>> factory LightScreenEffect */
static void adapt_LightScreenEffect(EffectDispatchState *s)
{
	s->hl = LightScreenEffect();
}
/* <<< factory LightScreenEffect */


/* >>> factory StarmieRecover_CheckEnergyHP */
static void adapt_StarmieRecover_CheckEnergyHP(EffectDispatchState *s)
{
	uint8_t b = s->b;
	uint8_t c = s->c;
	uint8_t d = s->d;
	StarmieRecoverCheckEnergyHPResult r = StarmieRecover_CheckEnergyHP();
	s->a = r.a;
	s->f = r.f;
	s->b = b;
	s->c = r.checked_damage ? r.c : c;
	s->d = d;
	s->e = 0u;
	s->hl = r.hl;
}
/* <<< factory StarmieRecover_CheckEnergyHP */


/* >>> factory StarmieRecover_DiscardEffect */
static void adapt_StarmieRecover_DiscardEffect(EffectDispatchState *s)
{
	s->a = StarmieRecover_DiscardEffect();
}
/* <<< factory StarmieRecover_DiscardEffect */


/* >>> factory CheckIfCardHasGrassEnergyAttached */
static void adapt_CheckIfCardHasGrassEnergyAttached(EffectDispatchState *s)
{
	CheckIfCardHasGrassEnergyAttachedResult r = CheckIfCardHasGrassEnergyAttached(s->a);
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CheckIfCardHasGrassEnergyAttached */

/* >>> factory GrimerMinimizeEffect */
static void adapt_GrimerMinimizeEffect(EffectDispatchState *s)
{
	s->a = 0x13u;
	s->hl = GrimerMinimizeEffect();
}
/* <<< factory GrimerMinimizeEffect */

/* >>> factory Quickfreeze_InitialEffect */
static void adapt_Quickfreeze_InitialEffect(EffectDispatchState *s)
{
	s->f = Quickfreeze_InitialEffect(s->f);
}
/* <<< factory Quickfreeze_InitialEffect */


/* >>> factory FocusEnergyEffect */
static void adapt_FocusEnergyEffect(EffectDispatchState *s)
{
	FocusEnergyEffect();
}
/* <<< factory FocusEnergyEffect */


/* >>> factory MagnetonSonicboom_UnaffectedByColorEffect */
static void adapt_MagnetonSonicboom_UnaffectedByColorEffect(EffectDispatchState *s)
{
	MagnetonSonicboom_UnaffectedByColorEffect();
}
/* <<< factory MagnetonSonicboom_UnaffectedByColorEffect */

/* >>> factory MagnetonSonicboom_NullEffect */
static void adapt_MagnetonSonicboom_NullEffect(EffectDispatchState *s)
{
	MagnetonSonicboom_NullEffect();
}
/* <<< factory MagnetonSonicboom_NullEffect */

/* >>> factory ElectrodeSonicboom_UnaffectedByColorEffect */
static void adapt_ElectrodeSonicboom_UnaffectedByColorEffect(EffectDispatchState *s)
{
	s->hl = ElectrodeSonicboom_UnaffectedByColorEffect();
}
/* <<< factory ElectrodeSonicboom_UnaffectedByColorEffect */

/* >>> factory EnergySpike_AISelectEffect */
static void adapt_EnergySpike_AISelectEffect(EffectDispatchState *s)
{
	EnergySpike_AISelectEffect();
	s->a = 0xffu;
}
/* <<< factory EnergySpike_AISelectEffect */

/* >>> factory CometPunch_AIEffect */
static void adapt_CometPunch_AIEffect(EffectDispatchState *s)
{
	CometPunch_AIEffect();
}
/* <<< factory CometPunch_AIEffect */

/* >>> factory Conversion1_WeaknessCheck */
static void adapt_Conversion1_WeaknessCheck(EffectDispatchState *s)
{
	Conversion1WeaknessCheckResult result = Conversion1_WeaknessCheck();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Conversion1_WeaknessCheck */

/* >>> factory Conversion2_ResistanceCheck */
static void adapt_Conversion2_ResistanceCheck(EffectDispatchState *s)
{
	Conversion2ResistanceCheckResult result = Conversion2_ResistanceCheck();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Conversion2_ResistanceCheck */

/* >>> factory ElectrodeSonicboom_NullEffect */
static void adapt_ElectrodeSonicboom_NullEffect(EffectDispatchState *s)
{
	ElectrodeSonicboom_NullEffect();
}
/* <<< factory ElectrodeSonicboom_NullEffect */

/* >>> factory FirstAid_DamageCheck */
static void adapt_FirstAid_DamageCheck(EffectDispatchState *s)
{
	FirstAidDamageCheckResult r = FirstAid_DamageCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory FirstAid_DamageCheck */

/* >>> factory DoTheWaveEffect */
static void adapt_DoTheWaveEffect(EffectDispatchState *s)
{
	DoTheWaveEffect();
}
/* <<< factory DoTheWaveEffect */

/* >>> factory FullHeal_StatusCheck */
static void adapt_FullHeal_StatusCheck(EffectDispatchState *s)
{
	FullHealStatusCheckResult r = FullHeal_StatusCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FullHeal_StatusCheck */

/* >>> factory PoisonFang_AIEffect */
static void adapt_PoisonFang_AIEffect(EffectDispatchState *s)
{
	(void)s;
	PoisonFang_AIEffect();
}
/* <<< factory PoisonFang_AIEffect */

/* >>> factory WeepinbellPoisonPowder_AIEffect */
static void adapt_WeepinbellPoisonPowder_AIEffect(EffectDispatchState *s)
{
	(void)s;
	WeepinbellPoisonPowder_AIEffect();
}
/* <<< factory WeepinbellPoisonPowder_AIEffect */

/* >>> factory Toxic_AIEffect */
static void adapt_Toxic_AIEffect(EffectDispatchState *s)
{
	(void)s;
	Toxic_AIEffect();
}
/* <<< factory Toxic_AIEffect */

/* >>> factory BoyfriendsEffect */
static void adapt_BoyfriendsEffect(EffectDispatchState *s)
{
	(void)s;
	BoyfriendsEffect();
}
/* <<< factory BoyfriendsEffect */

/* >>> factory IvysaurPoisonPowder_AIEffect */
static void adapt_IvysaurPoisonPowder_AIEffect(EffectDispatchState *s)
{
	(void)s;
	IvysaurPoisonPowder_AIEffect();
}
/* <<< factory IvysaurPoisonPowder_AIEffect */

/* >>> factory EnergyTrans_CheckPlayArea */
static void adapt_EnergyTrans_CheckPlayArea(EffectDispatchState *s)
{
	EnergyTransCheckPlayAreaResult r = EnergyTrans_CheckPlayArea();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
}
/* <<< factory EnergyTrans_CheckPlayArea */

/* >>> factory Firegiver_InitialEffect */
static void adapt_Firegiver_InitialEffect(EffectDispatchState *s)
{
	s->f = Firegiver_InitialEffect(s->f);
}
/* <<< factory Firegiver_InitialEffect */


/* >>> factory MoltresLv37DiveBomb_AIEffect */
static void adapt_MoltresLv37DiveBomb_AIEffect(EffectDispatchState *s)
{
	MoltresLv37DiveBomb_AIEffect();
}
/* <<< factory MoltresLv37DiveBomb_AIEffect */


/* >>> factory GetEnergyAttachedMultiplierDamage */
static void adapt_GetEnergyAttachedMultiplierDamage(EffectDispatchState *s)
{
	uint16_t r = GetEnergyAttachedMultiplierDamage();
	s->d = (uint8_t)(r >> 8);
	s->e = (uint8_t)r;
}
/* <<< factory GetEnergyAttachedMultiplierDamage */

/* >>> factory Fly_AIEffect */
static void adapt_Fly_AIEffect(EffectDispatchState *s)
{
	(void)s;
	Fly_AIEffect();
}
/* <<< factory Fly_AIEffect */
/* >>> factory Gigashock_AISelectEffect */
static void adapt_Gigashock_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	Gigashock_AISelectEffect();
}
/* <<< factory Gigashock_AISelectEffect */

/* >>> factory Wildfire_DiscardDeckEffect */
static void adapt_Wildfire_DiscardDeckEffect(EffectDispatchState *s)
{
	(void)s;
	Wildfire_DiscardDeckEffect();
}
/* <<< factory Wildfire_DiscardDeckEffect */

/* >>> factory MoltresLv35DiveBomb_AIEffect */
static void adapt_MoltresLv35DiveBomb_AIEffect(EffectDispatchState *s)
{
	(void)s;
	MoltresLv35DiveBomb_AIEffect();
}
/* <<< factory MoltresLv35DiveBomb_AIEffect */

/* >>> factory ClefairyDoll_BenchCheck */
static void adapt_ClefairyDoll_BenchCheck(EffectDispatchState *s)
{
	ClefairyDollBenchCheckResult r = ClefairyDoll_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ClefairyDoll_BenchCheck */

/* >>> factory ClefairyDoll_PlaceInPlayAreaEffect */
static void adapt_ClefairyDoll_PlaceInPlayAreaEffect(EffectDispatchState *s)
{
	ClefairyDoll_PlaceInPlayAreaEffect();
}
/* <<< factory ClefairyDoll_PlaceInPlayAreaEffect */

/* >>> factory EnergyBurnCheck_Unreferenced */
static void adapt_EnergyBurnCheck_Unreferenced(EffectDispatchState *s)
{
    EnergyBurnCheckResult r = EnergyBurnCheck_Unreferenced();
    s->a = r.a;
    s->f = r.f;
}
/* <<< factory EnergyBurnCheck_Unreferenced */

/* >>> factory FlareonRage_DamageBoostEffect */
static void adapt_FlareonRage_DamageBoostEffect(EffectDispatchState *s)
{
    (void)s;
    FlareonRage_DamageBoostEffect();
}
/* <<< factory FlareonRage_DamageBoostEffect */

/* >>> factory Shift_OncePerTurnCheck */
static void adapt_Shift_OncePerTurnCheck(EffectDispatchState *s)
{
	ShiftOncePerTurnCheckResult r = Shift_OncePerTurnCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Shift_OncePerTurnCheck */

/* >>> factory VenomPowder_AIEffect */
static void adapt_VenomPowder_AIEffect(EffectDispatchState *s)
{
	(void)s;
	VenomPowder_AIEffect();
}
/* <<< factory VenomPowder_AIEffect */

/* >>> factory TangelaPoisonPowder_AIEffect */
static void adapt_TangelaPoisonPowder_AIEffect(EffectDispatchState *s)
{
	(void)s;
	TangelaPoisonPowder_AIEffect();
}
/* <<< factory TangelaPoisonPowder_AIEffect */

/* >>> factory PetalDance_AIEffect */
static void adapt_PetalDance_AIEffect(EffectDispatchState *s)
{
	(void)s;
	PetalDance_AIEffect();
}
/* <<< factory PetalDance_AIEffect */

/* >>> factory RainDanceEffect */
static void adapt_RainDanceEffect(EffectDispatchState *s)
{
	s->f = RainDanceEffect(s->f);
}
/* <<< factory RainDanceEffect */

/* >>> factory PsyduckFurySwipes_AIEffect */
static void adapt_PsyduckFurySwipes_AIEffect(EffectDispatchState *s)
{
	(void)s;
	PsyduckFurySwipes_AIEffect();
}
/* <<< factory PsyduckFurySwipes_AIEffect */

/* >>> factory VaporeonQuickAttack_AIEffect */
static void adapt_VaporeonQuickAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	VaporeonQuickAttack_AIEffect();
}
/* <<< factory VaporeonQuickAttack_AIEffect */

/* >>> factory JellyfishSting_AIEffect */
static void adapt_JellyfishSting_AIEffect(EffectDispatchState *s)
{
	(void)s;
	JellyfishSting_AIEffect();
}
/* <<< factory JellyfishSting_AIEffect */

/* >>> factory PoliwhirlAmnesia_CheckAttacks */
static void adapt_PoliwhirlAmnesia_CheckAttacks(EffectDispatchState *s)
{
	PoliwhirlAmnesiaCheckAttacksResult r = PoliwhirlAmnesia_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PoliwhirlAmnesia_CheckAttacks */

/* >>> factory HeadacheEffect */
static void adapt_HeadacheEffect(EffectDispatchState *s)
{
	(void)s;
	HeadacheEffect();
}
/* <<< factory HeadacheEffect */

/* >>> factory ArcanineQuickAttack_AIEffect */
static void adapt_ArcanineQuickAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	ArcanineQuickAttack_AIEffect();
}
/* <<< factory ArcanineQuickAttack_AIEffect */

/* >>> factory FlamesOfRage_CheckEnergy */
static void adapt_FlamesOfRage_CheckEnergy(EffectDispatchState *s)
{
	FlamesOfRageCheckEnergyResult r = FlamesOfRage_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FlamesOfRage_CheckEnergy */

/* >>> factory MagmarFlamethrower_DiscardEffect */
static void adapt_MagmarFlamethrower_DiscardEffect(EffectDispatchState *s)
{
	s->a = MagmarFlamethrower_DiscardEffect();
}
/* <<< factory MagmarFlamethrower_DiscardEffect */

/* >>> factory MagmarSmog_AIEffect */
static void adapt_MagmarSmog_AIEffect(EffectDispatchState *s)
{
	(void)s;
	MagmarSmog_AIEffect();
}
/* <<< factory MagmarSmog_AIEffect */

/* >>> factory Wildfire_CheckEnergy */
static void adapt_Wildfire_CheckEnergy(EffectDispatchState *s)
{
	WildfireCheckEnergyResult r = Wildfire_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory Wildfire_CheckEnergy */

/* >>> factory MrMimeMeditate_DamageBoostEffect */
static void adapt_MrMimeMeditate_DamageBoostEffect(EffectDispatchState *s)
{
	(void)s;
	MrMimeMeditate_DamageBoostEffect();
}
/* <<< factory MrMimeMeditate_DamageBoostEffect */

/* >>> factory DancingEmbers_AIEffect */
static void adapt_DancingEmbers_AIEffect(EffectDispatchState *s)
{
	(void)s;
	DancingEmbers_AIEffect();
}
/* <<< factory DancingEmbers_AIEffect */

/* >>> factory FlareonFlamethrower_DiscardEffect */
static void adapt_FlareonFlamethrower_DiscardEffect(EffectDispatchState *s)
{
	s->a = FlareonFlamethrower_DiscardEffect();
}
/* <<< factory FlareonFlamethrower_DiscardEffect */

/* >>> factory MagmarFlamethrower_CheckEnergy */
static void adapt_MagmarFlamethrower_CheckEnergy(EffectDispatchState *s)
{
	MagmarFlamethrowerCheckEnergyResult r = MagmarFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MagmarFlamethrower_CheckEnergy */

/* >>> factory FlamesOfRage_DiscardEffect */
static void adapt_FlamesOfRage_DiscardEffect(EffectDispatchState *s)
{
	(void)s;
	FlamesOfRage_DiscardEffect();
}
/* <<< factory FlamesOfRage_DiscardEffect */

/* >>> factory FlamesOfRage_DamageBoostEffect */
static void adapt_FlamesOfRage_DamageBoostEffect(EffectDispatchState *s)
{
	(void)s;
	FlamesOfRage_DamageBoostEffect();
}
/* <<< factory FlamesOfRage_DamageBoostEffect */

/* >>> factory CharmeleonFlamethrower_CheckEnergy */
static void adapt_CharmeleonFlamethrower_CheckEnergy(EffectDispatchState *s)
{
	CharmeleonFlamethrowerCheckEnergyResult r = CharmeleonFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CharmeleonFlamethrower_CheckEnergy */

/* >>> factory CharmeleonFlamethrower_DiscardEffect */
static void adapt_CharmeleonFlamethrower_DiscardEffect(EffectDispatchState *s)
{
	s->a = CharmeleonFlamethrower_DiscardEffect();
}
/* <<< factory CharmeleonFlamethrower_DiscardEffect */

/* >>> factory EnergyBurnEffect */
static void adapt_EnergyBurnEffect(EffectDispatchState *s)
{
	EnergyBurnEffectResult r = EnergyBurnEffect(s->f);
	s->f = r.f;
}
/* <<< factory EnergyBurnEffect */

/* >>> factory FireSpin_CheckEnergy */
static void adapt_FireSpin_CheckEnergy(EffectDispatchState *s)
{
	FireSpinCheckEnergyResult r = FireSpin_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FireSpin_CheckEnergy */

/* >>> factory FlareonQuickAttack_AIEffect */
static void adapt_FlareonQuickAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	FlareonQuickAttack_AIEffect();
}
/* <<< factory FlareonQuickAttack_AIEffect */

/* >>> factory FlareonFlamethrower_CheckEnergy */
static void adapt_FlareonFlamethrower_CheckEnergy(EffectDispatchState *s)
{
	FlareonFlamethrowerCheckEnergyResult r = FlareonFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FlareonFlamethrower_CheckEnergy */

/* >>> factory Prophecy_AISelectEffect */
static void adapt_Prophecy_AISelectEffect(EffectDispatchState *s)
{
	ProphecyAISelectEffectResult r = Prophecy_AISelectEffect();
	s->a = r.a;
}
/* <<< factory Prophecy_AISelectEffect */

/* >>> factory Prophecy_ReorderDeckEffect */
static void adapt_Prophecy_ReorderDeckEffect(EffectDispatchState *s)
{
	ProphecyReorderDeckEffectResult r = Prophecy_ReorderDeckEffect();
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Prophecy_ReorderDeckEffect */

/* >>> factory SuperEnergyRetrieval_HandEnergyCheck */
static void adapt_SuperEnergyRetrieval_HandEnergyCheck(EffectDispatchState *s)
{
	SuperEnergyRetrievalHandEnergyCheckResult r =
		SuperEnergyRetrieval_HandEnergyCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory SuperEnergyRetrieval_HandEnergyCheck */

/* >>> factory GetNextPositionInTempList_TrainerEffects */
static void adapt_GetNextPositionInTempList_TrainerEffects(EffectDispatchState *s)
{
	s->hl = GetNextPositionInTempList_TrainerEffects();
}
/* <<< factory GetNextPositionInTempList_TrainerEffects */

/* >>> factory NinetalesLure_AISelectEffect */
static void adapt_NinetalesLure_AISelectEffect(EffectDispatchState *s)
{
	s->a = NinetalesLure_AISelectEffect();
}
/* <<< factory NinetalesLure_AISelectEffect */

/* >>> factory Ember_CheckEnergy */
static void adapt_Ember_CheckEnergy(EffectDispatchState *s)
{
	EmberCheckEnergyResult r = Ember_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Ember_CheckEnergy */

/* >>> factory DestinyBond_CheckEnergy */
static void adapt_DestinyBond_CheckEnergy(EffectDispatchState *s)
{
	IsPlayerTurnResult r = DestinyBond_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DestinyBond_CheckEnergy */

/* >>> factory ComputerSearch_HandDeckCheck */
static void adapt_ComputerSearch_HandDeckCheck(EffectDispatchState *s)
{
	ComputerSearchHandDeckCheckResult r = ComputerSearch_HandDeckCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ComputerSearch_HandDeckCheck */

/* >>> factory MrFuji_BenchCheck */
static void adapt_MrFuji_BenchCheck(EffectDispatchState *s)
{
	MrFujiBenchCheckResult r = MrFuji_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MrFuji_BenchCheck */

/* >>> factory DreamEaterEffect */
static void adapt_DreamEaterEffect(EffectDispatchState *s)
{
	DreamEaterEffectResult r = DreamEaterEffect();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DreamEaterEffect */

/* >>> factory JynxMeditate_DamageBoostEffect */
static void adapt_JynxMeditate_DamageBoostEffect(EffectDispatchState *s)
{
	JynxMeditate_DamageBoostEffect();
}
/* <<< factory JynxMeditate_DamageBoostEffect */
/* >>> factory KadabraRecover_CheckEnergyHP */
static void adapt_KadabraRecover_CheckEnergyHP(EffectDispatchState *s)
{
	uint8_t b = s->b, d = s->d;
	KadabraRecoverCheckEnergyHPResult r = KadabraRecover_CheckEnergyHP();
	s->a = r.a;
	s->f = r.f;
	s->c = r.checked_damage ? r.c : s->c;
	s->d = d;
	s->e = 0u;
	s->hl = r.hl;
	(void)b;
}
/* <<< factory KadabraRecover_CheckEnergyHP */
/* >>> factory MewtwoAltEnergyAbsorption_AddToHandEffect */
static void adapt_MewtwoAltEnergyAbsorption_AddToHandEffect(EffectDispatchState *s)
{
	MewtwoAltEnergyAbsorption_AddToHandEffect();
}
/* <<< factory MewtwoAltEnergyAbsorption_AddToHandEffect */
/* >>> factory MewtwoEnergyAbsorption_AddToHandEffect */
static void adapt_MewtwoEnergyAbsorption_AddToHandEffect(EffectDispatchState *s)
{
	MewtwoEnergyAbsorption_AddToHandEffect();
}
/* <<< factory MewtwoEnergyAbsorption_AddToHandEffect */
/* >>> factory NeutralizingShieldEffect */
static void adapt_NeutralizingShieldEffect(EffectDispatchState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | NeutralizingShieldEffect());
}
/* <<< factory NeutralizingShieldEffect */
/* >>> factory PealOfThunder_InitialEffect */
static void adapt_PealOfThunder_InitialEffect(EffectDispatchState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | PealOfThunder_InitialEffect());
}
/* <<< factory PealOfThunder_InitialEffect */
/* >>> factory PrehistoricPowerEffect */
static void adapt_PrehistoricPowerEffect(EffectDispatchState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | PrehistoricPowerEffect());
}
/* <<< factory PrehistoricPowerEffect */
/* >>> factory Scavenge_DiscardEffect */
static void adapt_Scavenge_DiscardEffect(EffectDispatchState *s)
{
	s->a = Scavenge_DiscardEffect();
}
/* <<< factory Scavenge_DiscardEffect */

/* >>> factory StepIn_BenchCheck */
static void adapt_StepIn_BenchCheck(EffectDispatchState *s) { SolarPowerCheckUseResult r = StepIn_BenchCheck(); s->f = r.f; s->hl = r.hl; }
/* <<< factory StepIn_BenchCheck */
/* >>> factory Peek_OncePerTurnCheck */
static void adapt_Peek_OncePerTurnCheck(EffectDispatchState *s)
{
	SolarPowerCheckUseResult r = Peek_OncePerTurnCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Peek_OncePerTurnCheck */
/* >>> factory Wail_BenchCheck */
static void adapt_Wail_BenchCheck(EffectDispatchState *s)
{
	MrFujiBenchCheckResult r = Wail_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Wail_BenchCheck */
/* >>> factory StepIn_SwitchEffect */
static void adapt_StepIn_SwitchEffect(EffectDispatchState *s) { StepIn_SwitchEffect(); }
/* <<< factory StepIn_SwitchEffect */
/* >>> factory ThickSkinnedEffect */
static void adapt_ThickSkinnedEffect(EffectDispatchState *s) { s->f = ThickSkinnedEffect(s->f); }
/* <<< factory ThickSkinnedEffect */
/* >>> factory HealingWind_InitialEffect */
static void adapt_HealingWind_InitialEffect(EffectDispatchState *s) { s->f = HealingWind_InitialEffect(s->f); }
/* <<< factory HealingWind_InitialEffect */
/* >>> factory PickRandomBasicCardFromDeck */
static void adapt_PickRandomBasicCardFromDeck(EffectDispatchState *s) { s->a = PickRandomBasicCardFromDeck(); s->f = s->a == 0xFFu ? 0x90u : (s->a == 0u ? 0x80u : 0u); }
/* <<< factory PickRandomBasicCardFromDeck */

/* >>> factory GustOfWind_BenchCheck */
static void adapt_GustOfWind_BenchCheck(EffectDispatchState *s)
{
	IsPlayerTurnResult r = GustOfWind_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory GustOfWind_BenchCheck */

/* >>> factory DrawSymbolOnPlayAreaCursor */
static void adapt_DrawSymbolOnPlayAreaCursor(EffectDispatchState *s)
{
	DrawSymbolOnPlayAreaCursor(s->a, s->b);
}
/* <<< factory DrawSymbolOnPlayAreaCursor */
/* >>> factory Func_2c6d9 */
static void adapt_Func_2c6d9(EffectDispatchState *s)
{
	WaitResult r = Func_2c6d9();
	s->f = r.f;
}
/* <<< factory Func_2c6d9 */


/* >>> factory MarowakCallForFamily_AISelectEffect */
static void adapt_MarowakCallForFamily_AISelectEffect(EffectDispatchState *s)
{
	MarowakCallForFamily_AISelectEffect();
}
/* <<< factory MarowakCallForFamily_AISelectEffect */

/* >>> factory CreateListOfFireEnergyAttachedToArena */
static void adapt_CreateListOfFireEnergyAttachedToArena(EffectDispatchState *s)
{
	CreateListOfEnergyAttachedToArenaResult r = CreateListOfFireEnergyAttachedToArena();
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateListOfFireEnergyAttachedToArena */
/* >>> factory CreateEnergyCardListFromDiscardPile_AllEnergy */
static void adapt_CreateEnergyCardListFromDiscardPile_AllEnergy(EffectDispatchState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile_AllEnergy();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateEnergyCardListFromDiscardPile_AllEnergy */
/* >>> factory CheckIfDeckIsEmpty */
static void adapt_CheckIfDeckIsEmpty(EffectDispatchState *s)
{
	CheckIfDeckIsEmptyResult r = CheckIfDeckIsEmpty();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CheckIfDeckIsEmpty */
/* >>> factory VictreebelLure_AssertPokemonInBench */
static void adapt_VictreebelLure_AssertPokemonInBench(EffectDispatchState *s)
{
	VictreebelLureAssertPokemonInBenchResult r = VictreebelLure_AssertPokemonInBench();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory VictreebelLure_AssertPokemonInBench */
/* >>> factory NinetalesLure_CheckBench */
static void adapt_NinetalesLure_CheckBench(EffectDispatchState *s)
{
	NinetalesLureCheckBenchResult r = NinetalesLure_CheckBench();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory NinetalesLure_CheckBench */
/* >>> factory ThunderboltEffect */
static void adapt_ThunderboltEffect(EffectDispatchState *s)
{
	ThunderboltEffect();
}
/* <<< factory ThunderboltEffect */
/* >>> factory TrainerCardAsPokemon_BenchCheck */
static void adapt_TrainerCardAsPokemon_BenchCheck(EffectDispatchState *s)
{
	TrainerCardAsPokemonBenchCheckResult r = TrainerCardAsPokemon_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory TrainerCardAsPokemon_BenchCheck */
/* >>> factory TrainerCardAsPokemon_DiscardEffect */
static void adapt_TrainerCardAsPokemon_DiscardEffect(EffectDispatchState *s)
{
	TrainerCardAsPokemon_DiscardEffect();
}
/* <<< factory TrainerCardAsPokemon_DiscardEffect */
/* >>> factory MysteriousFossil_BenchCheck */
static void adapt_MysteriousFossil_BenchCheck(EffectDispatchState *s)
{
	MysteriousFossilBenchCheckResult r = MysteriousFossil_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MysteriousFossil_BenchCheck */
/* >>> factory MysteriousFossil_PlaceInPlayAreaEffect */
static void adapt_MysteriousFossil_PlaceInPlayAreaEffect(EffectDispatchState *s)
{
	MysteriousFossil_PlaceInPlayAreaEffect();
}
/* <<< factory MysteriousFossil_PlaceInPlayAreaEffect */
/* >>> factory ScoopUp_BenchCheck */
static void adapt_ScoopUp_BenchCheck(EffectDispatchState *s)
{
	ScoopUpBenchCheckResult r = ScoopUp_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ScoopUp_BenchCheck */
/* >>> factory Toxic_DoublePoisonEffect */
static void adapt_Toxic_DoublePoisonEffect(EffectDispatchState *s)
{
	QueueStatusConditionResult r = Toxic_DoublePoisonEffect();
	s->f = r.f;
}
/* <<< factory Toxic_DoublePoisonEffect */

/* >>> factory TryGiveDamageCounter_StrangeBehavior */
static void adapt_TryGiveDamageCounter_StrangeBehavior(EffectDispatchState *s)
{
	TryGiveDamageCounter_StrangeBehaviorResult r =
		TryGiveDamageCounter_StrangeBehavior();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory TryGiveDamageCounter_StrangeBehavior */
/* >>> factory SpacingOut_CheckDamage */
static void adapt_SpacingOut_CheckDamage(EffectDispatchState *s)
{
	SpacingOutCheckDamageResult r = SpacingOut_CheckDamage();
	s->a = r.a;
	s->f = r.f;
	s->c = r.c;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SpacingOut_CheckDamage */
/* >>> factory SpacingOut_HealEffect */
static void adapt_SpacingOut_HealEffect(EffectDispatchState *s)
{
	SpacingOutHealEffectResult r = SpacingOut_HealEffect();
	s->a = r.a;
	s->f = r.f;
	if (r.update_hl)
		s->hl = r.hl;
}
/* <<< factory SpacingOut_HealEffect */

/* >>> factory LeekSlap_OncePerDuelCheck */
static void adapt_LeekSlap_OncePerDuelCheck(EffectDispatchState *s) { s->f = (uint8_t)(LeekSlap_OncePerDuelCheck() | (s->f & 0x00u)); }
/* <<< factory LeekSlap_OncePerDuelCheck */
/* >>> factory LeekSlap_SetUsedThisDuelFlag */
static void adapt_LeekSlap_SetUsedThisDuelFlag(EffectDispatchState *s) { LeekSlap_SetUsedThisDuelFlag(); }
/* <<< factory LeekSlap_SetUsedThisDuelFlag */
/* >>> factory PlusPowerEffect */
static void adapt_PlusPowerEffect(EffectDispatchState *s) { PlusPowerEffect(); }
/* <<< factory PlusPowerEffect */
/* >>> factory StrikesBackEffect */
static void adapt_StrikesBackEffect(EffectDispatchState *s) { s->f = (uint8_t)((s->f & 0x80u) | StrikesBackEffect()); }
/* <<< factory StrikesBackEffect */
/* >>> factory Switch_BenchCheck */
static void adapt_Switch_BenchCheck(EffectDispatchState *s) { MrFujiBenchCheckResult r = Switch_BenchCheck(); s->a = r.a; s->f = r.f; s->hl = r.hl; }
/* <<< factory Switch_BenchCheck */
/* >>> factory Switch_SwitchEffect */
static void adapt_Switch_SwitchEffect(EffectDispatchState *s) { Switch_SwitchEffect(); }
/* <<< factory Switch_SwitchEffect */

/* >>> factory CopyPlayAreaHPToBackup_Unreferenced */
static void adapt_CopyPlayAreaHPToBackup_Unreferenced(EffectDispatchState *s) { (void)s; CopyPlayAreaHPToBackup_Unreferenced(); }
/* <<< factory CopyPlayAreaHPToBackup_Unreferenced */
/* >>> factory CopyPlayAreaHPFromBackup_Unreferenced */
static void adapt_CopyPlayAreaHPFromBackup_Unreferenced(EffectDispatchState *s) { (void)s; CopyPlayAreaHPFromBackup_Unreferenced(); }
/* <<< factory CopyPlayAreaHPFromBackup_Unreferenced */
/* >>> factory Gale_LoadAnimation */
static void adapt_Gale_LoadAnimation(EffectDispatchState *s) { (void)s; Gale_LoadAnimation(); }
/* <<< factory Gale_LoadAnimation */
/* >>> factory EnergySearch_DeckCheck */
static void adapt_EnergySearch_DeckCheck(EffectDispatchState *s) { s->f = EnergySearch_DeckCheck(); }
/* <<< factory EnergySearch_DeckCheck */
/* >>> factory CheckIfCardIsBasicEnergy */
static void adapt_CheckIfCardIsBasicEnergy(EffectDispatchState *s) { s->f = CheckIfCardIsBasicEnergy(s->a); }
/* <<< factory CheckIfCardIsBasicEnergy */
/* >>> factory CreatePlayableStage2PokemonCardListFromHand */
static void adapt_CreatePlayableStage2PokemonCardListFromHand(EffectDispatchState *s) { s->f = (uint8_t)((s->f & 0x80u) | CreatePlayableStage2PokemonCardListFromHand()); }
/* <<< factory CreatePlayableStage2PokemonCardListFromHand */
/* >>> factory Barrier_DiscardEffect */
static void adapt_Barrier_DiscardEffect(EffectDispatchState *s)
{
	s->a = Barrier_DiscardEffect();
}
/* <<< factory Barrier_DiscardEffect */

/* >>> factory DestinyBond_DiscardEffect */
static void adapt_DestinyBond_DiscardEffect(EffectDispatchState *s) { DestinyBond_DiscardEffect(); }
/* <<< factory DestinyBond_DiscardEffect */
static void adapt_Ember_DiscardEffect(EffectDispatchState *s) { Ember_DiscardEffect(); }
/* <<< factory Ember_DiscardEffect */
/* >>> factory FireBlast_DiscardEffect */
static void adapt_FireBlast_DiscardEffect(EffectDispatchState *s) { FireBlast_DiscardEffect(); }
/* <<< factory FireBlast_DiscardEffect */
/* >>> factory FireSpin_AISelectEffect */
static void adapt_FireSpin_AISelectEffect(EffectDispatchState *s) { FireSpin_AISelectEffect(); }
/* <<< factory FireSpin_AISelectEffect */
/* >>> factory FireSpin_DiscardEffect */
static void adapt_FireSpin_DiscardEffect(EffectDispatchState *s) { FireSpin_DiscardEffect(); }
/* <<< factory FireSpin_DiscardEffect */
/* >>> factory PidgeottoMirrorMove_InitialEffect1 */
static void adapt_PidgeottoMirrorMove_InitialEffect1(EffectDispatchState *s)
{
	MirrorMoveInitialEffect1Result r = PidgeottoMirrorMove_InitialEffect1();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PidgeottoMirrorMove_InitialEffect1 */

/* >>> factory ClefairyMetronome_CheckAttacks */
static void adapt_ClefairyMetronome_CheckAttacks(EffectDispatchState *s)
{
	ClefairyMetronomeCheckAttacksResult r = ClefairyMetronome_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ClefairyMetronome_CheckAttacks */

/* >>> factory Psychic_DamageBoostEffect */
static void adapt_Psychic_DamageBoostEffect(EffectDispatchState *s)
{
	Psychic_DamageBoostEffect();
}
/* <<< factory Psychic_DamageBoostEffect */

/* >>> factory Barrier_AISelectEffect */
static void adapt_Barrier_AISelectEffect(EffectDispatchState *s)
{
	Barrier_AISelectEffect();
}
/* <<< factory Barrier_AISelectEffect */

/* >>> factory Whirlpool_AISelectEffect */
static void adapt_Whirlpool_AISelectEffect(EffectDispatchState *s)
{
	s->a = Whirlpool_AISelectEffect();
}
/* <<< factory Whirlpool_AISelectEffect */

/* >>> factory Whirlpool_DiscardEffect */
static void adapt_Whirlpool_DiscardEffect(EffectDispatchState *s)
{
	s->hl = Whirlpool_DiscardEffect(s->hl);
}
/* <<< factory Whirlpool_DiscardEffect */

/* >>> factory EnergyRemoval_EnergyCheck */
static void adapt_EnergyRemoval_EnergyCheck(EffectDispatchState *s)
{
	EnergyRemovalEnergyCheckResult r = EnergyRemoval_EnergyCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory EnergyRemoval_EnergyCheck */

/* >>> factory EnergyRemoval_AISelection */
static void adapt_EnergyRemoval_AISelection(EffectDispatchState *s)
{
	s->a = EnergyRemoval_AISelection();
}
/* <<< factory EnergyRemoval_AISelection */

/* >>> factory EnergyRetrieval_HandEnergyCheck */
static void adapt_EnergyRetrieval_HandEnergyCheck(EffectDispatchState *s)
{
	EnergyRetrievalHandEnergyCheckResult r = EnergyRetrieval_HandEnergyCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory EnergyRetrieval_HandEnergyCheck */

/* >>> factory MrMimeMeditate_AIEffect */
static void adapt_MrMimeMeditate_AIEffect(EffectDispatchState *s)
{
	MrMimeMeditate_AIEffect();
}
/* <<< factory MrMimeMeditate_AIEffect */

/* >>> factory PsywaveEffect */
static void adapt_PsywaveEffect(EffectDispatchState *s)
{
	s->hl = PsywaveEffect();
}
/* <<< factory PsywaveEffect */

/* >>> factory PokemonCenter_DamageCheck */
static void adapt_PokemonCenter_DamageCheck(EffectDispatchState *s)
{
	PokemonCenterDamageCheckResult r = PokemonCenter_DamageCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokemonCenter_DamageCheck */

/* >>> factory PokemonBreeder_HandPlayAreaCheck */
static void adapt_PokemonBreeder_HandPlayAreaCheck(EffectDispatchState *s)
{
	PokemonBreederHandPlayAreaCheckResult r = PokemonBreeder_HandPlayAreaCheck(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokemonBreeder_HandPlayAreaCheck */

/* >>> factory PokemonTrader_HandDeckCheck */
static void adapt_PokemonTrader_HandDeckCheck(EffectDispatchState *s)
{
	PokemonTraderHandDeckCheckResult r = PokemonTrader_HandDeckCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
	if (r.update_cde) {
		s->c = r.c;
		s->d = r.d;
		s->e = r.e;
	}
}
/* <<< factory PokemonTrader_HandDeckCheck */

/* >>> factory VictreebelLure_GetBenchPokemonWithLowestHP */
static void adapt_VictreebelLure_GetBenchPokemonWithLowestHP(EffectDispatchState *s)
{
	VictreebelLure_GetBenchPokemonWithLowestHP();
}
/* <<< factory VictreebelLure_GetBenchPokemonWithLowestHP */

/* >>> factory Sprout_CheckDeckAndPlayArea */
static void adapt_Sprout_CheckDeckAndPlayArea(EffectDispatchState *s)
{
	CheckIfDeckIsEmptyResult r = Sprout_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory Sprout_CheckDeckAndPlayArea */

/* >>> factory NidoranFCallForFamily_CheckDeckAndPlayArea */
static void adapt_NidoranFCallForFamily_CheckDeckAndPlayArea(EffectDispatchState *s)
{
	CheckIfDeckIsEmptyResult r = NidoranFCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory NidoranFCallForFamily_CheckDeckAndPlayArea */

/* >>> factory DragonairHyperBeam_AISelectEffect */
static void adapt_DragonairHyperBeam_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	DragonairHyperBeam_AISelectEffect();
}
/* <<< factory DragonairHyperBeam_AISelectEffect */

/* >>> factory ClefableMetronome_CheckAttacks */
static void adapt_ClefableMetronome_CheckAttacks(EffectDispatchState *s)
{
	ClefableMetronomeCheckAttacksResult r = ClefableMetronome_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ClefableMetronome_CheckAttacks */

/* >>> factory Scavenge_CheckDiscardPile */
static void adapt_Scavenge_CheckDiscardPile(EffectDispatchState *s)
{
	ScavengeCheckDiscardPileResult r = Scavenge_CheckDiscardPile();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory Scavenge_CheckDiscardPile */

/* >>> factory Scavenge_AISelectEffect */
static void adapt_Scavenge_AISelectEffect(EffectDispatchState *s)
{
	Scavenge_AISelectEffect();
}
/* <<< factory Scavenge_AISelectEffect */

/* >>> factory SlowpokeAmnesia_CheckAttacks */
static void adapt_SlowpokeAmnesia_CheckAttacks(EffectDispatchState *s)
{
	SlowpokeAmnesiaCheckAttacksResult r = SlowpokeAmnesia_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SlowpokeAmnesia_CheckAttacks */

/* >>> factory DevolutionBeam_CheckPlayArea */
static void adapt_DevolutionBeam_CheckPlayArea(EffectDispatchState *s)
{
	DevolutionBeamCheckPlayAreaResult r = DevolutionBeam_CheckPlayArea();
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DevolutionBeam_CheckPlayArea */

/* >>> factory DevolutionBeam_AISelectEffect */
static void adapt_DevolutionBeam_AISelectEffect(EffectDispatchState *s)
{
	DevolutionBeam_AISelectEffect();
}
/* <<< factory DevolutionBeam_AISelectEffect */

/* >>> factory MewtwoAltEnergyAbsorption_CheckDiscardPile */
static void adapt_MewtwoAltEnergyAbsorption_CheckDiscardPile(EffectDispatchState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = MewtwoAltEnergyAbsorption_CheckDiscardPile();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory MewtwoAltEnergyAbsorption_CheckDiscardPile */

/* >>> factory MewtwoAltEnergyAbsorption_AISelectEffect */
static void adapt_MewtwoAltEnergyAbsorption_AISelectEffect(EffectDispatchState *s)
{
	MewtwoAltEnergyAbsorptionAISelectEffectResult r = MewtwoAltEnergyAbsorption_AISelectEffect();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory MewtwoAltEnergyAbsorption_AISelectEffect */

/* >>> factory MewtwoEnergyAbsorption_CheckDiscardPile */
static void adapt_MewtwoEnergyAbsorption_CheckDiscardPile(EffectDispatchState *s)
{
	MewtwoEnergyAbsorptionCheckDiscardPileResult r = MewtwoEnergyAbsorption_CheckDiscardPile();
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory MewtwoEnergyAbsorption_CheckDiscardPile */

/* >>> factory MewtwoEnergyAbsorption_AISelectEffect */
static void adapt_MewtwoEnergyAbsorption_AISelectEffect(EffectDispatchState *s)
{
	MewtwoEnergyAbsorptionAISelectEffectResult r = MewtwoEnergyAbsorption_AISelectEffect();
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = (uint8_t)(r.de >> 8);
	s->e = (uint8_t)r.de;
	s->hl = r.hl;
}
/* <<< factory MewtwoEnergyAbsorption_AISelectEffect */

/* >>> factory JynxMeditate_AIEffect */
static void adapt_JynxMeditate_AIEffect(EffectDispatchState *s)
{
	JynxMeditate_AIEffect();
}
/* <<< factory JynxMeditate_AIEffect */

/* >>> factory MysteryAttack_RandomEffect */
static void adapt_MysteryAttack_RandomEffect(EffectDispatchState *s)
{
	MysteryAttack_RandomEffect();
}
/* <<< factory MysteryAttack_RandomEffect */

/* >>> factory MarowakCallForFamily_CheckDeckAndPlayArea */
static void adapt_MarowakCallForFamily_CheckDeckAndPlayArea(EffectDispatchState *s)
{
	CheckIfDeckIsEmptyResult r = MarowakCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MarowakCallForFamily_CheckDeckAndPlayArea */

/* >>> factory IceBreath_ZeroDamage */
static void adapt_IceBreath_ZeroDamage(EffectDispatchState *s)
{
	s->a = IceBreath_ZeroDamage();
}
/* <<< factory IceBreath_ZeroDamage */

/* >>> factory AIPickFireEnergyCardToDiscard */
static void adapt_AIPickFireEnergyCardToDiscard(EffectDispatchState *s)
{
	(void)s;
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory AIPickFireEnergyCardToDiscard */

/* >>> factory FlamesOfRage_AIEffect */
static void adapt_FlamesOfRage_AIEffect(EffectDispatchState *s)
{
	(void)s;
	FlamesOfRage_AIEffect();
}
/* <<< factory FlamesOfRage_AIEffect */

/* >>> factory ArcanineFlamethrower_AISelectEffect */
static void adapt_ArcanineFlamethrower_AISelectEffect(EffectDispatchState *s)
{
	ArcanineFlamethrower_AISelectEffect();
}
/* <<< factory ArcanineFlamethrower_AISelectEffect */

/* >>> factory FlamesOfRage_AISelectEffect */
static void adapt_FlamesOfRage_AISelectEffect(EffectDispatchState *s)
{
	FlamesOfRage_AISelectEffect();
}
/* <<< factory FlamesOfRage_AISelectEffect */

/* >>> factory FireBlast_AISelectEffect */
static void adapt_FireBlast_AISelectEffect(EffectDispatchState *s)
{
	FireBlast_AISelectEffect();
}
/* <<< factory FireBlast_AISelectEffect */

/* >>> factory EnergyConversion_CheckEnergy */
static void adapt_EnergyConversion_CheckEnergy(EffectDispatchState *s)
{
	EnergyConversionCheckEnergyResult r = EnergyConversion_CheckEnergy();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory EnergyConversion_CheckEnergy */

/* >>> factory EnergyConversion_AISelectEffect */
static void adapt_EnergyConversion_AISelectEffect(EffectDispatchState *s)
{
	EnergyConversion_AISelectEffect();
}
/* <<< factory EnergyConversion_AISelectEffect */

/* >>> factory HypnoDarkMind_AISelectEffect */
static void adapt_HypnoDarkMind_AISelectEffect(EffectDispatchState *s)
{
	HypnoDarkMind_AISelectEffect();
}
/* <<< factory HypnoDarkMind_AISelectEffect */

/* >>> factory AIPickAttackForAmnesia */
static void adapt_AIPickAttackForAmnesia(EffectDispatchState *s)
{
	s->a = AIPickAttackForAmnesia();
}
/* <<< factory AIPickAttackForAmnesia */

/* >>> factory MirrorMove_AISelection */
static void adapt_MirrorMove_AISelection(EffectDispatchState *s)
{
	(void)s;
	MirrorMove_AISelection();
}
/* <<< factory MirrorMove_AISelection */

/* >>> factory KinglerFlail_HPCheck */
static void adapt_KinglerFlail_HPCheck(EffectDispatchState *s)
{
	KinglerFlail_HPCheck();
}
/* <<< factory KinglerFlail_HPCheck */

/* >>> factory MagikarpFlail_HPCheck */
static void adapt_MagikarpFlail_HPCheck(EffectDispatchState *s)
{
	MagikarpFlail_HPCheck();
}
/* <<< factory MagikarpFlail_HPCheck */

/* >>> factory SuperFang_HalfHPEffect */
static void adapt_SuperFang_HalfHPEffect(EffectDispatchState *s)
{
	SuperFang_HalfHPEffect();
}
/* <<< factory SuperFang_HalfHPEffect */

/* >>> factory KarateChop_DamageSubtractionEffect */
static void adapt_KarateChop_DamageSubtractionEffect(EffectDispatchState *s)
{
	(void)s;
	KarateChop_DamageSubtractionEffect();
}
/* <<< factory KarateChop_DamageSubtractionEffect */

/* >>> factory SpearowMirrorMove_AISelection */
static void adapt_SpearowMirrorMove_AISelection(EffectDispatchState *s)
{
	(void)s;
	SpearowMirrorMove_AISelection();
}
/* <<< factory SpearowMirrorMove_AISelection */

/* >>> factory CharmeleonFlamethrower_AISelectEffect */
static void adapt_CharmeleonFlamethrower_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	CharmeleonFlamethrower_AISelectEffect();
}
/* <<< factory CharmeleonFlamethrower_AISelectEffect */

/* >>> factory ClefableMetronome_AISelectEffect */
static void adapt_ClefableMetronome_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	ClefableMetronome_AISelectEffect();
}
/* <<< factory ClefableMetronome_AISelectEffect */

/* >>> factory Ember_AISelectEffect */
static void adapt_Ember_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	Ember_AISelectEffect();
}
/* <<< factory Ember_AISelectEffect */

/* >>> factory FlareonFlamethrower_AISelectEffect */
static void adapt_FlareonFlamethrower_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	FlareonFlamethrower_AISelectEffect();
}
/* <<< factory FlareonFlamethrower_AISelectEffect */

/* >>> factory DestinyBond_DestinyBondEffect */
static void adapt_DestinyBond_DestinyBondEffect(EffectDispatchState *s)
{
	s->hl = DestinyBond_DestinyBondEffect();
}
/* <<< factory DestinyBond_DestinyBondEffect */

/* >>> factory FlareonRage_AIEffect */
static void adapt_FlareonRage_AIEffect(EffectDispatchState *s)
{
	FlareonRage_AIEffect();
}
/* <<< factory FlareonRage_AIEffect */

/* >>> factory GolduckHyperBeam_AISelectEffect */
static void adapt_GolduckHyperBeam_AISelectEffect(EffectDispatchState *s)
{
	GolduckHyperBeam_AISelectEffect();
	(void)s;
}
/* <<< factory GolduckHyperBeam_AISelectEffect */

/* >>> factory OnixHardenEffect */
static void adapt_OnixHardenEffect(EffectDispatchState *s)
{
	s->hl = OnixHardenEffect();
}
/* <<< factory OnixHardenEffect */

/* >>> factory PoliwhirlAmnesia_AISelectEffect */
static void adapt_PoliwhirlAmnesia_AISelectEffect(EffectDispatchState *s)
{
	PoliwhirlAmnesia_AISelectEffect();
	(void)s;
}
/* <<< factory PoliwhirlAmnesia_AISelectEffect */

/* >>> factory StretchKick_AISelectEffect */
static void adapt_StretchKick_AISelectEffect(EffectDispatchState *s)
{
	StretchKick_AISelectEffect();
	(void)s;
}
/* <<< factory StretchKick_AISelectEffect */

/* >>> factory VaporeonWaterGunEffect */
static void adapt_VaporeonWaterGunEffect(EffectDispatchState *s)
{
	(void)s;
	VaporeonWaterGunEffect();
}
/* <<< factory VaporeonWaterGunEffect */

/* >>> factory Potion_DamageCheck */
static void adapt_Potion_DamageCheck(EffectDispatchState *s)
{
	PotionDamageCheckResult r = Potion_DamageCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Potion_DamageCheck */

/* >>> factory CloysterSpikeCannon_AIEffect */
static void adapt_CloysterSpikeCannon_AIEffect(EffectDispatchState *s)
{
	(void)s;
	CloysterSpikeCannon_AIEffect();
}
/* <<< factory CloysterSpikeCannon_AIEffect */

/* >>> factory JolteonDoubleKick_AIEffect */
static void adapt_JolteonDoubleKick_AIEffect(EffectDispatchState *s)
{
	(void)s;
	JolteonDoubleKick_AIEffect();
}
/* <<< factory JolteonDoubleKick_AIEffect */

/* >>> factory RapidashStomp_AIEffect */
static void adapt_RapidashStomp_AIEffect(EffectDispatchState *s)
{
	RapidashStomp_AIEffect();
}
/* <<< factory RapidashStomp_AIEffect */

/* >>> factory StoneBarrage_AIEffect */
static void adapt_StoneBarrage_AIEffect(EffectDispatchState *s)
{
	(void)s;
	StoneBarrage_AIEffect();
}
/* <<< factory StoneBarrage_AIEffect */

/* >>> factory DestinyBond_AISelectEffect */
static void adapt_DestinyBond_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	DestinyBond_AISelectEffect();
}
/* <<< factory DestinyBond_AISelectEffect */

/* >>> factory Rampage_AIEffect */
static void adapt_Rampage_AIEffect(EffectDispatchState *s)
{
	(void)s;
	Rampage_AIEffect();
}
/* <<< factory Rampage_AIEffect */

/* >>> factory SuperPotion_DamageEnergyCheck */
static void adapt_SuperPotion_DamageEnergyCheck(EffectDispatchState *s)
{
	SuperPotionDamageEnergyCheckResult r = SuperPotion_DamageEnergyCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SuperPotion_DamageEnergyCheck */

/* >>> factory KrabbyCallForFamily_CheckDeckAndPlayArea */
static void adapt_KrabbyCallForFamily_CheckDeckAndPlayArea(EffectDispatchState *s)
{
	CheckIfDeckIsEmptyResult r = KrabbyCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory KrabbyCallForFamily_CheckDeckAndPlayArea */

/* >>> factory Revive_BenchCheck */
static void adapt_Revive_BenchCheck(EffectDispatchState *s)
{
	ReviveBenchCheckResult r = Revive_BenchCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Revive_BenchCheck */

/* >>> factory DragonairHyperBeam_DiscardEffect */
static void adapt_DragonairHyperBeam_DiscardEffect(EffectDispatchState *s)
{
	s->hl = DragonairHyperBeam_DiscardEffect(s->hl);
}
/* <<< factory DragonairHyperBeam_DiscardEffect */

/* >>> factory MirrorMove_ExecuteStatusEffect */
static void adapt_MirrorMove_ExecuteStatusEffect(EffectDispatchState *s)
{
	MirrorMoveExecuteStatusEffectResult r = MirrorMove_ExecuteStatusEffect(s->a);
	s->f = r.f;
}
/* <<< factory MirrorMove_ExecuteStatusEffect */

/* >>> factory Curse_CheckDamageAndBench */
static void adapt_Curse_CheckDamageAndBench(EffectDispatchState *s)
{
	CurseCheckDamageAndBenchResult result = Curse_CheckDamageAndBench();
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Curse_CheckDamageAndBench */

/* >>> factory SpearowMirrorMove_AIEffect */
static void adapt_SpearowMirrorMove_AIEffect(EffectDispatchState *s)
{
	SpearowMirrorMove_AIEffect();
	(void)s;
}
/* <<< factory SpearowMirrorMove_AIEffect */

/* >>> factory SpearowMirrorMove_InitialEffect1 */
static void adapt_SpearowMirrorMove_InitialEffect1(EffectDispatchState *s)
{
	MirrorMoveInitialEffect1Result r = SpearowMirrorMove_InitialEffect1();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SpearowMirrorMove_InitialEffect1 */

/* >>> factory PidgeottoMirrorMove_AIEffect */
static void adapt_PidgeottoMirrorMove_AIEffect(EffectDispatchState *s)
{
	PidgeottoMirrorMove_AIEffect();
	(void)s;
}
/* <<< factory PidgeottoMirrorMove_AIEffect */

/* >>> factory PidgeottoMirrorMove_AISelection */
static void adapt_PidgeottoMirrorMove_AISelection(EffectDispatchState *s)
{
	PidgeottoMirrorMove_AISelection();
}
/* <<< factory PidgeottoMirrorMove_AISelection */

/* >>> factory ClefairyMetronome_AISelectEffect */
static void adapt_ClefairyMetronome_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	ClefairyMetronome_AISelectEffect();
}
/* <<< factory ClefairyMetronome_AISelectEffect */

/* >>> factory EnergySpike_DeckCheck */
static void adapt_EnergySpike_DeckCheck(EffectDispatchState *s)
{
	CheckIfDeckIsEmptyResult result = EnergySpike_DeckCheck();
	s->a = result.a;
	s->hl = result.hl;
	s->f = result.f;
}
/* <<< factory EnergySpike_DeckCheck */

/* >>> factory MagmarFlamethrower_AISelectEffect */
static void adapt_MagmarFlamethrower_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	MagmarFlamethrower_AISelectEffect();
}
/* <<< factory MagmarFlamethrower_AISelectEffect */

/* >>> factory OmastarWaterGunEffect */
static void adapt_OmastarWaterGunEffect(EffectDispatchState *s)
{
	(void)s;
	OmastarWaterGunEffect();
}
/* <<< factory OmastarWaterGunEffect */

/* >>> factory CuboneRage_AIEffect */
static void adapt_CuboneRage_AIEffect(EffectDispatchState *s)
{
	(void)s;
	CuboneRage_AIEffect();
}
/* <<< factory CuboneRage_AIEffect */

/* >>> factory GravelerHardenEffect */
static void adapt_GravelerHardenEffect(EffectDispatchState *s)
{
	s->hl = GravelerHardenEffect();
}
/* <<< factory GravelerHardenEffect */

/* >>> factory KarateChop_AIEffect */
static void adapt_KarateChop_AIEffect(EffectDispatchState *s)
{
	(void)s;
	KarateChop_AIEffect();
}
/* <<< factory KarateChop_AIEffect */

/* >>> factory LaprasWaterGunEffect */
static void adapt_LaprasWaterGunEffect(EffectDispatchState *s)
{
	(void)s;
	LaprasWaterGunEffect();
}
/* <<< factory LaprasWaterGunEffect */

/* >>> factory OmanyteWaterGunEffect */
static void adapt_OmanyteWaterGunEffect(EffectDispatchState *s)
{
	(void)s;
	OmanyteWaterGunEffect();
}
/* <<< factory OmanyteWaterGunEffect */

/* >>> factory PoliwrathWaterGunEffect */
static void adapt_PoliwrathWaterGunEffect(EffectDispatchState *s)
{
	(void)s;
	PoliwrathWaterGunEffect();
}
/* <<< factory PoliwrathWaterGunEffect */

/* >>> factory SeadraWaterGunEffect */
static void adapt_SeadraWaterGunEffect(EffectDispatchState *s)
{
	(void)s;
	SeadraWaterGunEffect();
}
/* <<< factory SeadraWaterGunEffect */

/* >>> factory SuperFang_AIEffect */
static void adapt_SuperFang_AIEffect(EffectDispatchState *s)
{
	(void)s;
	SuperFang_AIEffect();
}
/* <<< factory SuperFang_AIEffect */

/* >>> factory DragoniteLv41Slam_AIEffect */
static void adapt_DragoniteLv41Slam_AIEffect(EffectDispatchState *s)
{
	(void)s;
	DragoniteLv41Slam_AIEffect();
}
/* <<< factory DragoniteLv41Slam_AIEffect */

/* >>> factory ElectabuzzQuickAttack_AIEffect */
static void adapt_ElectabuzzQuickAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	ElectabuzzQuickAttack_AIEffect();
}
/* <<< factory ElectabuzzQuickAttack_AIEffect */

/* >>> factory JolteonQuickAttack_AIEffect */
static void adapt_JolteonQuickAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	JolteonQuickAttack_AIEffect();
}
/* <<< factory JolteonQuickAttack_AIEffect */

/* >>> factory LeekSlap_AIEffect */
static void adapt_LeekSlap_AIEffect(EffectDispatchState *s)
{
	(void)s;
	LeekSlap_AIEffect();
}
/* <<< factory LeekSlap_AIEffect */

/* >>> factory PinMissile_AIEffect */
static void adapt_PinMissile_AIEffect(EffectDispatchState *s)
{
	(void)s;
	PinMissile_AIEffect();
}
/* <<< factory PinMissile_AIEffect */

/* >>> factory SandslashFurySwipes_AIEffect */
static void adapt_SandslashFurySwipes_AIEffect(EffectDispatchState *s)
{
	(void)s;
	SandslashFurySwipes_AIEffect();
}
/* <<< factory SandslashFurySwipes_AIEffect */

/* >>> factory Thunderpunch_AIEffect */
static void adapt_Thunderpunch_AIEffect(EffectDispatchState *s)
{
	(void)s;
	Thunderpunch_AIEffect();
}
/* <<< factory Thunderpunch_AIEffect */

/* >>> factory StarmieRecover_AISelectEffect */
static void adapt_StarmieRecover_AISelectEffect(EffectDispatchState *s)
{
	StarmieRecoverAISelectEffectResult r = StarmieRecover_AISelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory StarmieRecover_AISelectEffect */

/* >>> factory BellsproutCallForFamily_CheckDeckAndPlayArea */
static void adapt_BellsproutCallForFamily_CheckDeckAndPlayArea(EffectDispatchState *s)
{
	BellsproutCallForFamilyCheckDeckAndPlayAreaResult r = BellsproutCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory BellsproutCallForFamily_CheckDeckAndPlayArea */

/* >>> factory Spark_AISelectEffect */
static void adapt_Spark_AISelectEffect(EffectDispatchState *s)
{
	s->a = Spark_AISelectEffect().a;
}
/* <<< factory Spark_AISelectEffect */

/* >>> factory DamageSwap_CheckDamage */
static void adapt_DamageSwap_CheckDamage(EffectDispatchState *s)
{
	DamageSwapCheckDamageResult r = DamageSwap_CheckDamage();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DamageSwap_CheckDamage */

/* >>> factory PokemonFlute_BenchCheck */
static void adapt_PokemonFlute_BenchCheck(EffectDispatchState *s)
{
	PokemonFluteBenchCheckResult r = PokemonFlute_BenchCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokemonFlute_BenchCheck */

/* >>> factory Heal_OncePerTurnCheck */
static void adapt_Heal_OncePerTurnCheck(EffectDispatchState *s)
{
	HealOncePerTurnCheckResult r = Heal_OncePerTurnCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Heal_OncePerTurnCheck */

/* >>> factory Shift_ChangeColorEffect */
static void adapt_Shift_ChangeColorEffect(EffectDispatchState *s)
{
	Shift_ChangeColorEffectResult r = Shift_ChangeColorEffect(s->d, s->e);
	s->f = r.f;
}
/* <<< factory Shift_ChangeColorEffect */

/* >>> factory MagikarpFlail_AIEffect */
static void adapt_MagikarpFlail_AIEffect(EffectDispatchState *s)
{
	(void)s;
	MagikarpFlail_AIEffect();
}
/* <<< factory MagikarpFlail_AIEffect */

/* >>> factory PoliwagWaterGunEffect */
static void adapt_PoliwagWaterGunEffect(EffectDispatchState *s)
{
	(void)s;
	PoliwagWaterGunEffect();
}
/* <<< factory PoliwagWaterGunEffect */

/* >>> factory TaurosStomp_AIEffect */
static void adapt_TaurosStomp_AIEffect(EffectDispatchState *s)
{
	(void)s;
	TaurosStomp_AIEffect();
}
/* <<< factory TaurosStomp_AIEffect */

/* >>> factory DodrioRage_AIEffect */
static void adapt_DodrioRage_AIEffect(EffectDispatchState *s)
{
	(void)s;
	DodrioRage_AIEffect();
}
/* <<< factory DodrioRage_AIEffect */

/* >>> factory DragoniteLv45Slam_AIEffect */
static void adapt_DragoniteLv45Slam_AIEffect(EffectDispatchState *s)
{
	(void)s;
	DragoniteLv45Slam_AIEffect();
}
/* <<< factory DragoniteLv45Slam_AIEffect */

/* >>> factory GengarDarkMind_AISelectEffect */
static void adapt_GengarDarkMind_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	GengarDarkMind_AISelectEffect();
}
/* <<< factory GengarDarkMind_AISelectEffect */

/* >>> factory PoliwhirlDoubleslap_AIEffect */
static void adapt_PoliwhirlDoubleslap_AIEffect(EffectDispatchState *s)
{
	(void)s;
	PoliwhirlDoubleslap_AIEffect();
}
/* <<< factory PoliwhirlDoubleslap_AIEffect */

/* >>> factory KinglerFlail_AIEffect */
static void adapt_KinglerFlail_AIEffect(EffectDispatchState *s)
{
	(void)s;
	KinglerFlail_AIEffect();
}
/* <<< factory KinglerFlail_AIEffect */

/* >>> factory JynxDoubleslap_AIEffect */
static void adapt_JynxDoubleslap_AIEffect(EffectDispatchState *s)
{
	(void)s;
	JynxDoubleslap_AIEffect();
}
/* <<< factory JynxDoubleslap_AIEffect */

/* >>> factory Bonemerang_AIEffect */
static void adapt_Bonemerang_AIEffect(EffectDispatchState *s)
{
	(void)s;
	Bonemerang_AIEffect();
}
/* <<< factory Bonemerang_AIEffect */

/* >>> factory Barrier_BarrierEffect */
static void adapt_Barrier_BarrierEffect(EffectDispatchState *s)
{
	(void)s;
	Barrier_BarrierEffect();
}
/* <<< factory Barrier_BarrierEffect */

/* >>> factory HydroPumpEffect */
static void adapt_HydroPumpEffect(EffectDispatchState *s)
{
	(void)s;
	HydroPumpEffect();
}
/* <<< factory HydroPumpEffect */

/* >>> factory MysteryAttack_AIEffect */
static void adapt_MysteryAttack_AIEffect(EffectDispatchState *s)
{
	(void)s;
	MysteryAttack_AIEffect();
}
/* <<< factory MysteryAttack_AIEffect */

/* >>> factory HurricaneEffect */
static void adapt_HurricaneEffect(EffectDispatchState *s)
{
	QueueStatusConditionResult r = HurricaneEffect(s->hl);
	s->f = r.f;
}
/* <<< factory HurricaneEffect */

/* >>> factory Psychic_AIEffect */
static void adapt_Psychic_AIEffect(EffectDispatchState *s)
{
	(void)s;
	Psychic_AIEffect();
}
/* <<< factory Psychic_AIEffect */

/* >>> factory SlowpokeAmnesia_AISelectEffect */
static void adapt_SlowpokeAmnesia_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	SlowpokeAmnesia_AISelectEffect();
}
/* <<< factory SlowpokeAmnesia_AISelectEffect */

/* >>> factory KadabraRecover_AISelectEffect */
static void adapt_KadabraRecover_AISelectEffect(EffectDispatchState *s)
{
	(void)s;
	KadabraRecover_AISelectEffect();
}
/* <<< factory KadabraRecover_AISelectEffect */

/* >>> factory GolduckHyperBeam_DiscardEffect */
static void adapt_GolduckHyperBeam_DiscardEffect(EffectDispatchState *s)
{
	s->hl = GolduckHyperBeam_DiscardEffect(s->hl);
}
/* <<< factory GolduckHyperBeam_DiscardEffect */

/* >>> factory StrangeBehavior_CheckDamage */
static void adapt_StrangeBehavior_CheckDamage(EffectDispatchState *s)
{
	StrangeBehavior_CheckDamageResult r = StrangeBehavior_CheckDamage();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory StrangeBehavior_CheckDamage */

/* >>> factory EnergyTrans_PrintProcedure */
static void adapt_EnergyTrans_PrintProcedure(EffectDispatchState *s)
{
	(void)s;
	EnergyTrans_PrintProcedure();
}
/* <<< factory EnergyTrans_PrintProcedure */

/* >>> factory ItemFinder_HandDiscardPileCheck */
static void adapt_ItemFinder_HandDiscardPileCheck(EffectDispatchState *s)
{
	ItemFinder_HandDiscardPileCheckResult r = ItemFinder_HandDiscardPileCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ItemFinder_HandDiscardPileCheck */

/* >>> factory Wildfire_DiscardEnergyEffect */
static void adapt_Wildfire_DiscardEnergyEffect(EffectDispatchState *s)
{
	(void)s;
	Wildfire_DiscardEnergyEffect();
}
/* <<< factory Wildfire_DiscardEnergyEffect */

/* >>> factory SuperEnergyRemoval_EnergyCheck */
static void adapt_SuperEnergyRemoval_EnergyCheck(EffectDispatchState *s)
{
	SuperEnergyRemoval_EnergyCheckResult r = SuperEnergyRemoval_EnergyCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SuperEnergyRemoval_EnergyCheck */

/* >>> factory MorphEffect */
static void adapt_MorphEffect(EffectDispatchState *s)
{
	(void)s;
	MorphEffect();
}
/* <<< factory MorphEffect */

/* >>> factory AISelectConversionColor */
static void adapt_AISelectConversionColor(EffectDispatchState *s)
{
	AISelectConversionColor();
}
/* <<< factory AISelectConversionColor */

/* >>> factory PrintArenaCardNameAndColorText */
static void adapt_PrintArenaCardNameAndColorText(EffectDispatchState *s)
{
	TextResult r = PrintArenaCardNameAndColorText(s->d, s->e, s->hl);
	s->a = r.a; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory PrintArenaCardNameAndColorText */

/* >>> factory Conversion1_AISelectEffect */
static void adapt_Conversion1_AISelectEffect(EffectDispatchState *s)
{
	Conversion1_AISelectEffect();
}
/* <<< factory Conversion1_AISelectEffect */

/* >>> factory Conversion2_ChangeResistanceEffect */
static void adapt_Conversion2_ChangeResistanceEffect(EffectDispatchState *s)
{
	TextResult r = Conversion2_ChangeResistanceEffect(s->d, s->e);
	s->hl = r.hl;
}
/* <<< factory Conversion2_ChangeResistanceEffect */

/* >>> factory Conversion2_AISelectEffect */
static void adapt_Conversion2_AISelectEffect(EffectDispatchState *s)
{
	Conversion2_AISelectEffect();
}
/* <<< factory Conversion2_AISelectEffect */

/* >>> factory MirrorMove_AfterDamage */
static void adapt_MirrorMove_AfterDamage(EffectDispatchState *s)
{
	TextResult r = MirrorMove_AfterDamage(s->d, s->e, s->hl);
	s->a = r.a; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory MirrorMove_AfterDamage */

/* >>> factory PidgeottoMirrorMove_AfterDamage */
static void adapt_PidgeottoMirrorMove_AfterDamage(EffectDispatchState *s)
{
	TextResult r = PidgeottoMirrorMove_AfterDamage(s->d, s->e, s->hl);
	s->a = r.a; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory PidgeottoMirrorMove_AfterDamage */

/* >>> factory SpearowMirrorMove_AfterDamage */
static void adapt_SpearowMirrorMove_AfterDamage(EffectDispatchState *s)
{
	TextResult r = SpearowMirrorMove_AfterDamage(s->d, s->e, s->hl);
	s->a = r.a; s->d = r.d; s->e = r.e; s->hl = r.hl;
}
/* <<< factory SpearowMirrorMove_AfterDamage */

/* >>> factory Func_2c0a8 */
static void adapt_Func_2c0a8(EffectDispatchState *s)
{
	s->a = Func_2c0a8();
}
/* <<< factory Func_2c0a8 */

/* >>> factory ShuffleCardsInDeck */
static void adapt_ShuffleCardsInDeck(EffectDispatchState *s)
{
	uint16_t de = (uint16_t)(((uint16_t)s->d << 8) | s->e);
	ShuffleCardsInDeckResult r = ShuffleCardsInDeck(s->b, s->c, de, s->hl);
	s->a = r.a; s->b = r.b; s->c = r.c; s->d = r.d; s->e = r.e; s->f = r.f; s->hl = r.hl;
}
/* <<< factory ShuffleCardsInDeck */

/* >>> factory DrawPlayAreaScreenToShowChanges */
static void adapt_DrawPlayAreaScreenToShowChanges(EffectDispatchState *s)
{
	DrawPlayAreaScreenToShowChanges(s->a);
}
/* <<< factory DrawPlayAreaScreenToShowChanges */

/* >>> factory EnergyRemoval_DiscardEffect */
static void adapt_EnergyRemoval_DiscardEffect(EffectDispatchState *s)
{
	EnergyRemovalDiscardEffectResult r = EnergyRemoval_DiscardEffect();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory EnergyRemoval_DiscardEffect */

/* >>> factory SuperEnergyRemoval_DiscardEffect */
static void adapt_SuperEnergyRemoval_DiscardEffect(EffectDispatchState *s)
{
	(void)s;
	SuperEnergyRemoval_DiscardEffect();
}
/* <<< factory SuperEnergyRemoval_DiscardEffect */

/* >>> factory EnergyTrans_AIEffect */
static void adapt_EnergyTrans_AIEffect(EffectDispatchState *s)
{
	(void)s;
	EnergyTrans_AIEffect();
}
/* <<< factory EnergyTrans_AIEffect */

/* >>> factory StrangeBehavior_SwapEffect */
static void adapt_StrangeBehavior_SwapEffect(EffectDispatchState *s)
{
	StrangeBehaviorSwapEffectResult result = StrangeBehavior_SwapEffect();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory StrangeBehavior_SwapEffect */

/* >>> factory Defender_AttachDefenderEffect */
static void adapt_Defender_AttachDefenderEffect(EffectDispatchState *s)
{
	DefenderAttachDefenderEffectResult r = Defender_AttachDefenderEffect();
	s->f = r.f;
}
/* <<< factory Defender_AttachDefenderEffect */

/* >>> factory DamageSwap_SwapEffect */
static void adapt_DamageSwap_SwapEffect(EffectDispatchState *s)
{
	DamageSwap_SwapEffectResult result = DamageSwap_SwapEffect();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory DamageSwap_SwapEffect */

/* >>> factory PrintDevolvedCardNameAndLevelText */
static void adapt_PrintDevolvedCardNameAndLevelText(EffectDispatchState *s)
{
	PrintDevolvedCardNameAndLevelText(s->b, s->c, s->d, s->e);
}
/* <<< factory PrintDevolvedCardNameAndLevelText */

/* >>> factory ApplySubstatus2ToDefendingCard */
static void adapt_ApplySubstatus2ToDefendingCard(EffectDispatchState *s)
{
	s->hl = ApplySubstatus2ToDefendingCard(s->a, s->hl);
}
/* <<< factory ApplySubstatus2ToDefendingCard */

/* >>> factory ApplyAmnesiaToAttack */
static void adapt_ApplyAmnesiaToAttack(EffectDispatchState *s)
{
	ApplyAmnesiaToAttack(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory ApplyAmnesiaToAttack */

/* >>> factory MirrorMove_BeforeDamage */
static void adapt_MirrorMove_BeforeDamage(EffectDispatchState *s)
{
	(void)s;
	MirrorMove_BeforeDamage();
}
/* <<< factory MirrorMove_BeforeDamage */

/* >>> factory SpearowMirrorMove_BeforeDamage */
static void adapt_SpearowMirrorMove_BeforeDamage(EffectDispatchState *s)
{
	(void)s;
	SpearowMirrorMove_BeforeDamage();
}
/* <<< factory SpearowMirrorMove_BeforeDamage */

/* >>> factory PidgeottoMirrorMove_BeforeDamage */
static void adapt_PidgeottoMirrorMove_BeforeDamage(EffectDispatchState *s)
{
	(void)s;
	PidgeottoMirrorMove_BeforeDamage();
}
/* <<< factory PidgeottoMirrorMove_BeforeDamage */

/* >>> factory PoliwhirlAmnesia_DisableEffect */
static void adapt_PoliwhirlAmnesia_DisableEffect(EffectDispatchState *s)
{
	PoliwhirlAmnesia_DisableEffect(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory PoliwhirlAmnesia_DisableEffect */

/* >>> factory SlowpokeAmnesia_DisableEffect */
static void adapt_SlowpokeAmnesia_DisableEffect(EffectDispatchState *s)
{
	SlowpokeAmnesia_DisableEffect(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory SlowpokeAmnesia_DisableEffect */

/* >>> factory HorseaSmokescreenEffect */
static void adapt_HorseaSmokescreenEffect(EffectDispatchState *s)
{
	s->a = 0x01u;
	s->hl = HorseaSmokescreenEffect(s->hl);
}
/* <<< factory HorseaSmokescreenEffect */

/* >>> factory PikachuAltLv16GrowlEffect */
static void adapt_PikachuAltLv16GrowlEffect(EffectDispatchState *s)
{
	s->a = 0x12u;
	s->hl = PikachuAltLv16GrowlEffect(s->hl);
}
/* <<< factory PikachuAltLv16GrowlEffect */

/* >>> factory MagmarSmokescreenEffect */
static void adapt_MagmarSmokescreenEffect(EffectDispatchState *s)
{
	s->a = 0x01u;
	s->hl = MagmarSmokescreenEffect(s->hl);
}
/* <<< factory MagmarSmokescreenEffect */

/* >>> factory PikachuLv16GrowlEffect */
static void adapt_PikachuLv16GrowlEffect(EffectDispatchState *s)
{
	s->a = 0x12u;
	s->hl = PikachuLv16GrowlEffect(s->hl);
}
/* <<< factory PikachuLv16GrowlEffect */

/* >>> factory PounceEffect */
static void adapt_PounceEffect(EffectDispatchState *s)
{
	s->a = 0x07u;
	s->hl = PounceEffect(s->hl);
}
/* <<< factory PounceEffect */

/* >>> factory SandAttackEffect */
static void adapt_SandAttackEffect(EffectDispatchState *s)
{
	s->a = 0x02u;
	s->hl = SandAttackEffect(s->hl);
}
/* <<< factory SandAttackEffect */

/* >>> factory SnivelEffect */
static void adapt_SnivelEffect(EffectDispatchState *s)
{
	s->a = 0x03u;
	s->hl = SnivelEffect(s->hl);
}
/* <<< factory SnivelEffect */

/* >>> factory Conversion1_ChangeWeaknessEffect */
static void adapt_Conversion1_ChangeWeaknessEffect(EffectDispatchState *s)
{
	s->hl = Conversion1_ChangeWeaknessEffect(s->d, s->e, s->hl);
}
/* <<< factory Conversion1_ChangeWeaknessEffect */

/* >>> factory EnergyRetrieval_DiscardAndAddToHandEffect */
static void adapt_EnergyRetrieval_DiscardAndAddToHandEffect(EffectDispatchState *s)
{
	(void)s;
	EnergyRetrieval_DiscardAndAddToHandEffect();
}
/* <<< factory EnergyRetrieval_DiscardAndAddToHandEffect */

/* >>> factory SuperEnergyRetrieval_DiscardAndAddToHandEffect */
static void adapt_SuperEnergyRetrieval_DiscardAndAddToHandEffect(EffectDispatchState *s)
{
	SuperEnergyRetrievalDiscardAndAddToHandEffectResult r = SuperEnergyRetrieval_DiscardAndAddToHandEffect(s->b, s->c);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory SuperEnergyRetrieval_DiscardAndAddToHandEffect */

/* >>> factory HandleDefendingPokemonAttackSelection */
static void adapt_HandleDefendingPokemonAttackSelection(EffectDispatchState *s)
{
	HandleDefendingPokemonAttackSelectionResult r = HandleDefendingPokemonAttackSelection();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory HandleDefendingPokemonAttackSelection */

/* >>> factory HandleEnergyDiscardEffectSelection */
static void adapt_HandleEnergyDiscardEffectSelection(EffectDispatchState *s)
{
	(void)s;
	HandleEnergyDiscardEffectSelection();
}
/* <<< factory HandleEnergyDiscardEffectSelection */

/* >>> factory DragonairHyperBeam_PlayerSelectEffect */
static void adapt_DragonairHyperBeam_PlayerSelectEffect(EffectDispatchState *s)
{
	(void)s;
	DragonairHyperBeam_PlayerSelectEffect();
}
/* <<< factory DragonairHyperBeam_PlayerSelectEffect */

/* >>> factory GolduckHyperBeam_PlayerSelectEffect */
static void adapt_GolduckHyperBeam_PlayerSelectEffect(EffectDispatchState *s)
{
	(void)s;
	GolduckHyperBeam_PlayerSelectEffect();
}
/* <<< factory GolduckHyperBeam_PlayerSelectEffect */

/* >>> factory MirrorMove_PlayerSelection */
static void adapt_MirrorMove_PlayerSelection(EffectDispatchState *s)
{
	(void)s;
	MirrorMove_PlayerSelection();
}
/* <<< factory MirrorMove_PlayerSelection */

/* >>> factory SpearowMirrorMove_PlayerSelection */
static void adapt_SpearowMirrorMove_PlayerSelection(EffectDispatchState *s)
{
	(void)s;
	SpearowMirrorMove_PlayerSelection();
}
/* <<< factory SpearowMirrorMove_PlayerSelection */

/* >>> factory StrangeBehavior_SelectAndSwapEffect */
static void adapt_StrangeBehavior_SelectAndSwapEffect(EffectDispatchState *s)
{
	(void)s;
	StrangeBehavior_SelectAndSwapEffect();
}
/* <<< factory StrangeBehavior_SelectAndSwapEffect */

/* >>> factory PidgeottoMirrorMove_PlayerSelection */
static void adapt_PidgeottoMirrorMove_PlayerSelection(EffectDispatchState *s)
{
	(void)s;
	PidgeottoMirrorMove_PlayerSelection();
}
/* <<< factory PidgeottoMirrorMove_PlayerSelection */

/* >>> factory LookForCardsInDeck */
static void adapt_LookForCardsInDeck(EffectDispatchState *s)
{
	LookForCardsInDeckResult result = LookForCardsInDeck(s->a, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory LookForCardsInDeck */

/* >>> factory KadabraRecover_PlayerSelectEffect */
static void adapt_KadabraRecover_PlayerSelectEffect(EffectDispatchState *s)
{
	KadabraRecover_PlayerSelectEffectResult r = KadabraRecover_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory KadabraRecover_PlayerSelectEffect */

/* >>> factory Scavenge_PlayerSelectEnergyEffect */
static void adapt_Scavenge_PlayerSelectEnergyEffect(EffectDispatchState *s)
{
	Scavenge_PlayerSelectEnergyEffectResult r = Scavenge_PlayerSelectEnergyEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Scavenge_PlayerSelectEnergyEffect */

/* >>> factory PlayerPickFireEnergyCardToDiscard */
static void adapt_PlayerPickFireEnergyCardToDiscard(EffectDispatchState *s)
{
	PlayerPickFireEnergyCardToDiscardResult r = PlayerPickFireEnergyCardToDiscard();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PlayerPickFireEnergyCardToDiscard */

/* >>> factory ArcanineFlamethrower_PlayerSelectEffect */
static void adapt_ArcanineFlamethrower_PlayerSelectEffect(EffectDispatchState *s)
{
	PlayerPickFireEnergyCardToDiscardResult r = ArcanineFlamethrower_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ArcanineFlamethrower_PlayerSelectEffect */

/* >>> factory CharmeleonFlamethrower_PlayerSelectEffect */
static void adapt_CharmeleonFlamethrower_PlayerSelectEffect(EffectDispatchState *s)
{
	PlayerPickFireEnergyCardToDiscardResult r = CharmeleonFlamethrower_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory CharmeleonFlamethrower_PlayerSelectEffect */

/* >>> factory Barrier_PlayerSelectEffect */
static void adapt_Barrier_PlayerSelectEffect(EffectDispatchState *s)
{
	Barrier_PlayerSelectEffectResult result = Barrier_PlayerSelectEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Barrier_PlayerSelectEffect */

/* >>> factory StarmieRecover_PlayerSelectEffect */
static void adapt_StarmieRecover_PlayerSelectEffect(EffectDispatchState *s)
{
	StarmieRecover_PlayerSelectEffectResult r = StarmieRecover_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory StarmieRecover_PlayerSelectEffect */

/* >>> factory DestinyBond_PlayerSelectEffect */
static void adapt_DestinyBond_PlayerSelectEffect(EffectDispatchState *s)
{
	DestinyBond_PlayerSelectEffectResult result = DestinyBond_PlayerSelectEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory DestinyBond_PlayerSelectEffect */

/* >>> factory FlamesOfRage_PlayerSelectEffect */
static void adapt_FlamesOfRage_PlayerSelectEffect(EffectDispatchState *s)
{
	(void)s;
	FlamesOfRage_PlayerSelectEffect();
}
/* <<< factory FlamesOfRage_PlayerSelectEffect */

/* >>> factory HandleColorChangeScreen */
static void adapt_HandleColorChangeScreen(EffectDispatchState *s)
{
	HandleColorChangeScreenResult r = HandleColorChangeScreen(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a; s->f = r.f;
}
/* <<< factory HandleColorChangeScreen */

/* >>> factory Ember_PlayerSelectEffect */
static void adapt_Ember_PlayerSelectEffect(EffectDispatchState *s)
{
	PlayerPickFireEnergyCardToDiscardResult r = Ember_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Ember_PlayerSelectEffect */

/* >>> factory FireBlast_PlayerSelectEffect */
static void adapt_FireBlast_PlayerSelectEffect(EffectDispatchState *s)
{
	PlayerPickFireEnergyCardToDiscardResult r = FireBlast_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory FireBlast_PlayerSelectEffect */

/* >>> factory MagmarFlamethrower_PlayerSelectEffect */
static void adapt_MagmarFlamethrower_PlayerSelectEffect(EffectDispatchState *s)
{
	PlayerPickFireEnergyCardToDiscardResult result = MagmarFlamethrower_PlayerSelectEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory MagmarFlamethrower_PlayerSelectEffect */

/* >>> factory FlareonFlamethrower_PlayerSelectEffect */
static void adapt_FlareonFlamethrower_PlayerSelectEffect(EffectDispatchState *s)
{
	PlayerPickFireEnergyCardToDiscardResult r = FlareonFlamethrower_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory FlareonFlamethrower_PlayerSelectEffect */

/* >>> factory Conversion1_PlayerSelectEffect */
static void adapt_Conversion1_PlayerSelectEffect(EffectDispatchState *s)
{
	HandleColorChangeScreenResult r = Conversion1_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Conversion1_PlayerSelectEffect */

/* >>> factory Conversion2_PlayerSelectEffect */
static void adapt_Conversion2_PlayerSelectEffect(EffectDispatchState *s)
{
	HandleColorChangeScreenResult r = Conversion2_PlayerSelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Conversion2_PlayerSelectEffect */

/* >>> factory AskWhetherToQuitSelectingCards */
static void adapt_AskWhetherToQuitSelectingCards(EffectDispatchState *s)
{
	AskWhetherToQuitSelectingCardsResult result = AskWhetherToQuitSelectingCards(s->a);
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory AskWhetherToQuitSelectingCards */

/* >>> factory Scavenge_AddToHandEffect */
static void adapt_Scavenge_AddToHandEffect(EffectDispatchState *s)
{
	Scavenge_AddToHandEffectResult r = Scavenge_AddToHandEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Scavenge_AddToHandEffect */

/* >>> factory Recycle_AddToHandEffect */
static void adapt_Recycle_AddToHandEffect(EffectDispatchState *s)
{
	Recycle_AddToHandEffectResult r = Recycle_AddToHandEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Recycle_AddToHandEffect */

/* >>> factory PokemonBreeder_EvolveEffect */
static void adapt_PokemonBreeder_EvolveEffect(EffectDispatchState *s)
{
	PokemonBreederEvolveEffectResult r = PokemonBreeder_EvolveEffect(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory PokemonBreeder_EvolveEffect */

/* >>> factory Sprout_PutInPlayAreaEffect */
static void adapt_Sprout_PutInPlayAreaEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult r = Sprout_PutInPlayAreaEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->hl = r.hl;
}
/* <<< factory Sprout_PutInPlayAreaEffect */

/* >>> factory NidoranFCallForFamily_PutInPlayAreaEffect */
static void adapt_NidoranFCallForFamily_PutInPlayAreaEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult r = NidoranFCallForFamily_PutInPlayAreaEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->hl = r.hl;
}
/* <<< factory NidoranFCallForFamily_PutInPlayAreaEffect */

/* >>> factory MarowakCallForFamily_PutInPlayAreaEffect */
static void adapt_MarowakCallForFamily_PutInPlayAreaEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult r = MarowakCallForFamily_PutInPlayAreaEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->hl = r.hl;
}
/* <<< factory MarowakCallForFamily_PutInPlayAreaEffect */

/* >>> factory KrabbyCallForFamily_PutInPlayAreaEffect */
static void adapt_KrabbyCallForFamily_PutInPlayAreaEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult r = KrabbyCallForFamily_PutInPlayAreaEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->hl = r.hl;
}
/* <<< factory KrabbyCallForFamily_PutInPlayAreaEffect */

/* >>> factory PokemonFlute_PlaceInPlayAreaText */
static void adapt_PokemonFlute_PlaceInPlayAreaText(EffectDispatchState *s)
{
	(void)s;
	PokemonFlute_PlaceInPlayAreaText();
}
/* <<< factory PokemonFlute_PlaceInPlayAreaText */

/* >>> factory Revive_PlaceInPlayAreaEffect */
static void adapt_Revive_PlaceInPlayAreaEffect(EffectDispatchState *s)
{
	Revive_PlaceInPlayAreaEffectResult r = Revive_PlaceInPlayAreaEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory Revive_PlaceInPlayAreaEffect */

/* >>> factory ItemFinder_DiscardAddToHandEffect */
static void adapt_ItemFinder_DiscardAddToHandEffect(EffectDispatchState *s)
{
	ItemFinder_DiscardAddToHandEffectResult r = ItemFinder_DiscardAddToHandEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory ItemFinder_DiscardAddToHandEffect */

/* >>> factory BellsproutCallForFamily_PutInPlayAreaEffect */
static void adapt_BellsproutCallForFamily_PutInPlayAreaEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult r = BellsproutCallForFamily_PutInPlayAreaEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->hl = r.hl;
}
/* <<< factory BellsproutCallForFamily_PutInPlayAreaEffect */

/* >>> factory Wildfire_PlayerSelectEffect */
static void adapt_Wildfire_PlayerSelectEffect(EffectDispatchState *s)
{
	Wildfire_PlayerSelectEffectResult result = Wildfire_PlayerSelectEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Wildfire_PlayerSelectEffect */

/* >>> factory Whirlpool_PlayerSelectEffect */
static void adapt_Whirlpool_PlayerSelectEffect(EffectDispatchState *s)
{
	Whirlpool_PlayerSelectEffect();
	s->a = 0xffu;
	s->f = 0x90u;
}
/* <<< factory Whirlpool_PlayerSelectEffect */

/* >>> factory FireSpin_PlayerSelectEffect */
static void adapt_FireSpin_PlayerSelectEffect(EffectDispatchState *s)
{
	(void)s;
	FireSpin_PlayerSelectEffect();
}
/* <<< factory FireSpin_PlayerSelectEffect */

/* >>> factory EnergySpike_AttachEnergyEffect */
static void adapt_EnergySpike_AttachEnergyEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult r = EnergySpike_AttachEnergyEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory EnergySpike_AttachEnergyEffect */

/* >>> factory ScoopUp_ReturnToHandEffect */
static void adapt_ScoopUp_ReturnToHandEffect(EffectDispatchState *s)
{
	(void)s;
	ScoopUp_ReturnToHandEffect();
}
/* <<< factory ScoopUp_ReturnToHandEffect */

/* >>> factory EnergyTrans_TransferEffect */
static void adapt_EnergyTrans_TransferEffect(EffectDispatchState *s)
{
	s->a = EnergyTrans_TransferEffect();
}
/* <<< factory EnergyTrans_TransferEffect */

/* >>> factory DamageSwap_SelectAndSwapEffect */
static void adapt_DamageSwap_SelectAndSwapEffect(EffectDispatchState *s)
{
	(void)s;
	DamageSwap_SelectAndSwapEffect();
}
/* <<< factory DamageSwap_SelectAndSwapEffect */

/* >>> factory Gigashock_PlayerSelectEffect */
static void adapt_Gigashock_PlayerSelectEffect(EffectDispatchState *s)
{
	Gigashock_PlayerSelectEffect();
}
/* <<< factory Gigashock_PlayerSelectEffect */

/* >>> factory HandleSwitchDefendingPokemonEffect */
static void adapt_HandleSwitchDefendingPokemonEffect(EffectDispatchState *s)
{
	HandleSwitchDefendingPokemonEffectResult r = HandleSwitchDefendingPokemonEffect(s->a);
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory HandleSwitchDefendingPokemonEffect */

/* >>> factory PidgeottoWhirlwind_SwitchEffect */
static void adapt_PidgeottoWhirlwind_SwitchEffect(EffectDispatchState *s)
{
	HandleSwitchDefendingPokemonEffectResult r = PidgeottoWhirlwind_SwitchEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory PidgeottoWhirlwind_SwitchEffect */

/* >>> factory ButterfreeWhirlwind_SwitchEffect */
static void adapt_ButterfreeWhirlwind_SwitchEffect(EffectDispatchState *s)
{
	ButterfreeWhirlwind_SwitchEffectResult result = ButterfreeWhirlwind_SwitchEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory ButterfreeWhirlwind_SwitchEffect */

/* >>> factory PidgeyWhirlwind_SwitchEffect */
static void adapt_PidgeyWhirlwind_SwitchEffect(EffectDispatchState *s)
{
	HandleSwitchDefendingPokemonEffectResult result = PidgeyWhirlwind_SwitchEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory PidgeyWhirlwind_SwitchEffect */

/* >>> factory TerrorStrike_SwitchDefendingPokemon */
static void adapt_TerrorStrike_SwitchDefendingPokemon(EffectDispatchState *s)
{
	HandleSwitchDefendingPokemonEffectResult r = TerrorStrike_SwitchDefendingPokemon();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory TerrorStrike_SwitchDefendingPokemon */

/* >>> factory Gale_SwitchEffect */
static void adapt_Gale_SwitchEffect(EffectDispatchState *s)
{
	GaleSwitchEffectResult result = Gale_SwitchEffect(s->hl);
	s->f = result.f;
}
/* <<< factory Gale_SwitchEffect */

/* >>> factory Shift_PlayerSelectEffect */
static void adapt_Shift_PlayerSelectEffect(EffectDispatchState *s)
{
	HandleColorChangeScreenResult result = Shift_PlayerSelectEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Shift_PlayerSelectEffect */

/* >>> factory HandlePlayerMetronomeEffect */
static void adapt_HandlePlayerMetronomeEffect(EffectDispatchState *s)
{
	s->f = HandlePlayerMetronomeEffect(s->a);
}
/* <<< factory HandlePlayerMetronomeEffect */

/* >>> factory ClefairyMetronome_UseAttackEffect */
static void adapt_ClefairyMetronome_UseAttackEffect(EffectDispatchState *s)
{
	s->f = ClefairyMetronome_UseAttackEffect();
}
/* <<< factory ClefairyMetronome_UseAttackEffect */

/* >>> factory ClefableMetronome_UseAttackEffect */
static void adapt_ClefableMetronome_UseAttackEffect(EffectDispatchState *s)
{
	s->f = ClefableMetronome_UseAttackEffect();
}
/* <<< factory ClefableMetronome_UseAttackEffect */

/* >>> factory Curse_PlayerSelectEffect */
static void adapt_Curse_PlayerSelectEffect(EffectDispatchState *s)
{
	Curse_PlayerSelectEffectResult result = Curse_PlayerSelectEffect();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory Curse_PlayerSelectEffect */

/* >>> factory MrFuji_ReturnToDeckEffect */
static void adapt_MrFuji_ReturnToDeckEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult result = MrFuji_ReturnToDeckEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory MrFuji_ReturnToDeckEffect */

/* >>> factory Serial_TossCoinATimes */
static void adapt_Serial_TossCoinATimes(EffectDispatchState *s)
{
	SerialTossCoinATimesResult result = Serial_TossCoinATimes(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Serial_TossCoinATimes */

/* >>> factory TossCoinATimes_BankB */
static void adapt_TossCoinATimes_BankB(EffectDispatchState *s)
{
	TossCoinATimes_BankBResult result = TossCoinATimes_BankB(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory TossCoinATimes_BankB */

/* >>> factory Serial_TossZeroCoins */
static void adapt_Serial_TossZeroCoins(EffectDispatchState *s)
{
	SerialTossCoinATimesResult result = Serial_TossZeroCoins(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Serial_TossZeroCoins */

/* >>> factory Serial_TossCoin */
static void adapt_Serial_TossCoin(EffectDispatchState *s)
{
	SerialTossCoinATimesResult result = Serial_TossCoin(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Serial_TossCoin */

/* >>> factory NinetalesLure_SwitchEffect */
static void adapt_NinetalesLure_SwitchEffect(EffectDispatchState *s)
{
	(void)s;
	NinetalesLure_SwitchEffect();
}
/* <<< factory NinetalesLure_SwitchEffect */

/* >>> factory VictreebelLure_SwitchDefendingPokemon */
static void adapt_VictreebelLure_SwitchDefendingPokemon(EffectDispatchState *s)
{
	(void)s;
	VictreebelLure_SwitchDefendingPokemon();
}
/* <<< factory VictreebelLure_SwitchDefendingPokemon */

/* >>> factory DancingEmbers_MultiplierEffect */
static void adapt_DancingEmbers_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	DancingEmbers_MultiplierEffect();
}
/* <<< factory DancingEmbers_MultiplierEffect */

/* >>> factory NidoranFFurySwipes_MultiplierEffect */
static void adapt_NidoranFFurySwipes_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	NidoranFFurySwipes_MultiplierEffect();
}
/* <<< factory NidoranFFurySwipes_MultiplierEffect */

/* >>> factory PsyduckFurySwipes_MultiplierEffect */
static void adapt_PsyduckFurySwipes_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	PsyduckFurySwipes_MultiplierEffect();
}
/* <<< factory PsyduckFurySwipes_MultiplierEffect */

/* >>> factory JolteonDoubleKick_MultiplierEffect */
static void adapt_JolteonDoubleKick_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	JolteonDoubleKick_MultiplierEffect();
}
/* <<< factory JolteonDoubleKick_MultiplierEffect */

/* >>> factory CometPunch_MultiplierEffect */
static void adapt_CometPunch_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	CometPunch_MultiplierEffect();
}
/* <<< factory CometPunch_MultiplierEffect */

/* >>> factory PinMissile_MultiplierEffect */
static void adapt_PinMissile_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	PinMissile_MultiplierEffect();
}
/* <<< factory PinMissile_MultiplierEffect */

/* >>> factory PrimeapeFurySwipes_MultiplierEffect */
static void adapt_PrimeapeFurySwipes_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	PrimeapeFurySwipes_MultiplierEffect();
}
/* <<< factory PrimeapeFurySwipes_MultiplierEffect */

/* >>> factory SandslashFurySwipes_MultiplierEffect */
static void adapt_SandslashFurySwipes_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	SandslashFurySwipes_MultiplierEffect();
}
/* <<< factory SandslashFurySwipes_MultiplierEffect */

/* >>> factory DragoniteLv45Slam_MultiplierEffect */
static void adapt_DragoniteLv45Slam_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	DragoniteLv45Slam_MultiplierEffect();
}
/* <<< factory DragoniteLv45Slam_MultiplierEffect */

/* >>> factory FuryAttack_MultiplierEffect */
static void adapt_FuryAttack_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	FuryAttack_MultiplierEffect();
}
/* <<< factory FuryAttack_MultiplierEffect */

/* >>> factory Bonemerang_MultiplierEffect */
static void adapt_Bonemerang_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	Bonemerang_MultiplierEffect();
}
/* <<< factory Bonemerang_MultiplierEffect */

/* >>> factory CloysterSpikeCannon_MultiplierEffect */
static void adapt_CloysterSpikeCannon_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	CloysterSpikeCannon_MultiplierEffect();
}
/* <<< factory CloysterSpikeCannon_MultiplierEffect */

/* >>> factory NidorinaDoubleKick_MultiplierEffect */
static void adapt_NidorinaDoubleKick_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	NidorinaDoubleKick_MultiplierEffect();
}
/* <<< factory NidorinaDoubleKick_MultiplierEffect */

/* >>> factory DragoniteLv41Slam_MultiplierEffect */
static void adapt_DragoniteLv41Slam_MultiplierEffect(EffectDispatchState *s)
{
	DragoniteLv41Slam_MultiplierEffect();
}
/* <<< factory DragoniteLv41Slam_MultiplierEffect */

/* >>> factory NidorinoDoubleKick_MultiplierEffect */
static void adapt_NidorinoDoubleKick_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	NidorinoDoubleKick_MultiplierEffect();
}
/* <<< factory NidorinoDoubleKick_MultiplierEffect */

/* >>> factory OmastarSpikeCannon_MultiplierEffect */
static void adapt_OmastarSpikeCannon_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	OmastarSpikeCannon_MultiplierEffect();
}
/* <<< factory OmastarSpikeCannon_MultiplierEffect */

/* >>> factory JynxDoubleslap_MultiplierEffect */
static void adapt_JynxDoubleslap_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	JynxDoubleslap_MultiplierEffect();
}
/* <<< factory JynxDoubleslap_MultiplierEffect */

/* >>> factory PoliwhirlDoubleslap_MultiplierEffect */
static void adapt_PoliwhirlDoubleslap_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	PoliwhirlDoubleslap_MultiplierEffect();
}
/* <<< factory PoliwhirlDoubleslap_MultiplierEffect */

/* >>> factory Twineedle_MultiplierEffect */
static void adapt_Twineedle_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	Twineedle_MultiplierEffect();
}
/* <<< factory Twineedle_MultiplierEffect */

/* >>> factory DragonairSlam_MultiplierEffect */
static void adapt_DragonairSlam_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	DragonairSlam_MultiplierEffect();
}
/* <<< factory DragonairSlam_MultiplierEffect */

/* >>> factory PetalDance_MultiplierEffect */
static void adapt_PetalDance_MultiplierEffect(EffectDispatchState *s)
{
	(void)s;
	PetalDance_MultiplierEffect();
}
/* <<< factory PetalDance_MultiplierEffect */

/* >>> factory PlayTrainerEffectAnimation */
static void adapt_PlayTrainerEffectAnimation(EffectDispatchState *s)
{
	PlayTrainerEffectAnimation(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory PlayTrainerEffectAnimation */

/* >>> factory StretchKick_BenchDamageEffect */
static void adapt_StretchKick_BenchDamageEffect(EffectDispatchState *s)
{
	StretchKick_BenchDamageEffectResult result =
		StretchKick_BenchDamageEffect(s->b, s->c, s->d, s->e, s->hl);
	s->a = result.a;
	s->f = result.f;
	s->b = result.b;
	s->c = result.c;
	s->d = result.d;
	s->e = result.e;
	s->hl = result.hl;
}
/* <<< factory StretchKick_BenchDamageEffect */

/* >>> factory IceBreath_RandomPokemonDamageEffect */
static void adapt_IceBreath_RandomPokemonDamageEffect(EffectDispatchState *s)
{
	IceBreath_RandomPokemonDamageEffect();
}
/* <<< factory IceBreath_RandomPokemonDamageEffect */

/* >>> factory HypnoDarkMind_DamageBenchEffect */
static void adapt_HypnoDarkMind_DamageBenchEffect(EffectDispatchState *s)
{
	HypnoDarkMind_DamageBenchEffect(s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory HypnoDarkMind_DamageBenchEffect */

/* >>> factory GengarDarkMind_DamageBenchEffect */
static void adapt_GengarDarkMind_DamageBenchEffect(EffectDispatchState *s)
{
	GengarDarkMind_DamageBenchEffect(s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory GengarDarkMind_DamageBenchEffect */

/* >>> factory Spark_BenchDamageEffect */
static void adapt_Spark_BenchDamageEffect(EffectDispatchState *s)
{
	Spark_BenchDamageEffect(s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory Spark_BenchDamageEffect */

/* >>> factory CatPunchEffect */
static void adapt_CatPunchEffect(EffectDispatchState *s)
{
	(void)s;
	CatPunchEffect();
}
/* <<< factory CatPunchEffect */

/* >>> factory Gigashock_BenchDamageEffect */
static void adapt_Gigashock_BenchDamageEffect(EffectDispatchState *s)
{
	Gigashock_BenchDamageEffect();
}
/* <<< factory Gigashock_BenchDamageEffect */

/* >>> factory ChainLightningEffect */
static void adapt_ChainLightningEffect(EffectDispatchState *s)
{
	(void)s;
	ChainLightningEffect();
}
/* <<< factory ChainLightningEffect */

/* >>> factory Firegiver_AddToHandEffect */
static void adapt_Firegiver_AddToHandEffect(EffectDispatchState *s)
{
	ShuffleCardsInDeckResult r = Firegiver_AddToHandEffect(s->b);
	s->a = r.a;
	s->f = r.f;
	s->b = r.b;
	s->c = r.c;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory Firegiver_AddToHandEffect */

/* >>> factory PlayAttackAnimationOverAttackingPokemon */
static void adapt_PlayAttackAnimationOverAttackingPokemon(EffectDispatchState *s)
{
	PlayAttackAnimationOverAttackingPokemon(s->a, s->f, s->b, s->c, s->d, s->e, s->hl);
}
/* <<< factory PlayAttackAnimationOverAttackingPokemon */

/* >>> factory PokemonTrader_PlayerHandSelection */
static void adapt_PokemonTrader_PlayerHandSelection(EffectDispatchState *s)
{
	(void)s;
	PokemonTrader_PlayerHandSelection();
}
/* <<< factory PokemonTrader_PlayerHandSelection */

/* >>> factory EnergyRetrieval_PlayerDiscardPileSelection */
static void adapt_EnergyRetrieval_PlayerDiscardPileSelection(EffectDispatchState *s)
{
	EnergyRetrieval_PlayerDiscardPileSelectionResult result = EnergyRetrieval_PlayerDiscardPileSelection();
	s->a = result.a;
	s->f = result.f;
}
/* <<< factory EnergyRetrieval_PlayerDiscardPileSelection */

/* >>> factory EnergyRetrieval_PlayerHandSelection */
static void adapt_EnergyRetrieval_PlayerHandSelection(EffectDispatchState *s)
{
	(void)s;
	EnergyRetrieval_PlayerHandSelection();
}
/* <<< factory EnergyRetrieval_PlayerHandSelection */

/* >>> factory HandleEnergyCardsInDiscardPileSelection */
static void adapt_HandleEnergyCardsInDiscardPileSelection(EffectDispatchState *s)
{
	HandleEnergyCardsInDiscardPileSelectionResult result =
		HandleEnergyCardsInDiscardPileSelection(s->hl);
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory HandleEnergyCardsInDiscardPileSelection */

static const EffectDispatchEntry kEffectDispatchEntries[] = {
	{ "PoisonEffect", 0x4007u, adapt_PoisonEffect },
	{ "DoublePoisonEffect", 0x400Cu, adapt_DoublePoisonEffect },
	{ "ParalysisEffect", 0x4018u, adapt_ParalysisEffect },
	{ "ConfusionEffect", 0x4024u, adapt_ConfusionEffect },
	{ "SleepEffect", 0x4030u, adapt_SleepEffect },
	{ "QueueStatusCondition", 0x4035u, adapt_QueueStatusCondition },
	{ "TossCoinATimes_BankB", 0x4082u, adapt_TossCoinATimes_BankB },
	{ "CommentedOut_2c086", 0x4086u, adapt_CommentedOut_2c086 },
	{ "Serial_TossZeroCoins", 0x4087u, adapt_Serial_TossZeroCoins },
	{ "Serial_TossCoin", 0x408Au, adapt_Serial_TossCoin },
	{ "Serial_TossCoinATimes", 0x408Cu, adapt_Serial_TossCoinATimes },
	{ "SetNoEffectFromStatus", 0x409Cu, adapt_SetNoEffectFromStatus },
	{ "SetWasUnsuccessful", 0x40A2u, adapt_SetWasUnsuccessful },
	{ "Func_2c0a8", 0x40A8u, adapt_Func_2c0a8 },
	{ "ShuffleCardsInDeck", 0x40BDu, adapt_ShuffleCardsInDeck },
	{ "IsPlayerTurn", 0x40C7u, adapt_IsPlayerTurn },
	{ "UpdateExpectedAIDamage_AccountForPoison", 0x40D4u, adapt_UpdateExpectedAIDamage_AccountForPoison },
	{ "UpdateExpectedAIDamage", 0x40E9u, adapt_UpdateExpectedAIDamage },
	{ "SetExpectedAIDamage", 0x40FBu, adapt_SetExpectedAIDamage },
	{ "DrawPlayAreaScreenToShowChanges", 0x410Bu, adapt_DrawPlayAreaScreenToShowChanges },
	{ "PlayAttackAnimationOverAttackingPokemon", 0x412Eu, adapt_PlayAttackAnimationOverAttackingPokemon },
	{ "ApplySubstatus1ToAttackingCard", 0x4140u, adapt_ApplySubstatus1ToAttackingCard },
	{ "ApplySubstatus2ToDefendingCard", 0x4149u, adapt_ApplySubstatus2ToDefendingCard },
	{ "SetDefiniteDamage", 0x4166u, adapt_SetDefiniteDamage },
	{ "SetDefiniteAIDamage", 0x4174u, adapt_SetDefiniteAIDamage },
	{ "PickRandomPlayAreaCard", 0x417Eu, adapt_PickRandomPlayAreaCard },
	{ "GetNextPositionInTempList", 0x4188u, adapt_GetNextPositionInTempList },
	{ "CreateListOfFireEnergyAttachedToArena", 0x4197u, adapt_CreateListOfFireEnergyAttachedToArena },
	{ "CreateListOfEnergyAttachedToArena", 0x4199u, adapt_CreateListOfEnergyAttachedToArena },
	{ "PrintDevolvedCardNameAndLevelText", 0x41C4u, adapt_PrintDevolvedCardNameAndLevelText },
	{ "HandleSwitchDefendingPokemonEffect", 0x41ECu, adapt_HandleSwitchDefendingPokemonEffect },
	{ "HandleNoDamageOrEffect", 0x4216u, adapt_HandleNoDamageOrEffect },
	{ "CheckIfPlayAreaHasAnyDamage", 0x425Bu, adapt_CheckIfPlayAreaHasAnyDamage },
	{ "CreateTrainerCardListFromDiscardPile", 0x426Eu, adapt_CreateTrainerCardListFromDiscardPile },
	{ "CreateEnergyCardListFromDiscardPile_OnlyBasic", 0x42A0u, adapt_CreateEnergyCardListFromDiscardPile_OnlyBasic },
	{ "CreateEnergyCardListFromDiscardPile_AllEnergy", 0x42A4u, adapt_CreateEnergyCardListFromDiscardPile_AllEnergy },
	{ "CreateEnergyCardListFromDiscardPile", 0x42A6u, adapt_CreateEnergyCardListFromDiscardPile },
	{ "CheckIfDeckIsEmpty", 0x42E0u, adapt_CheckIfDeckIsEmpty },
	{ "LookForCardsInDeck", 0x42ECu, adapt_LookForCardsInDeck },
	{ "HandleDefendingPokemonAttackSelection", 0x4391u, adapt_HandleDefendingPokemonAttackSelection },
	{ "GetAttackName", 0x43FCu, adapt_GetAttackName },
	{ "CheckIfDefendingPokemonHasAnyAttack", 0x440Eu, adapt_CheckIfDefendingPokemonHasAnyAttack },
	{ "UpdateDevolvedCardHPAndStage", 0x4431u, adapt_UpdateDevolvedCardHPAndStage },
	{ "ResetDevolvedCardStatus", 0x445Du, adapt_ResetDevolvedCardStatus },
	{ "AskWhetherToQuitSelectingCards", 0x4476u, adapt_AskWhetherToQuitSelectingCards },
	{ "AIPickEnergyCardToDiscardFromDefendingPokemon", 0x44DAu, adapt_AIPickEnergyCardToDiscardFromDefendingPokemon },
	{ "AIPickAttackForAmnesia", 0x4532u, adapt_AIPickAttackForAmnesia },
	{ "AIFindTargetForBenchAttack", 0x4564u, adapt_AIFindTargetForBenchAttack },
	{ "HandleColorChangeScreen", 0x4588u, adapt_HandleColorChangeScreen },
	{ "LoadCardNameAndInputColor", 0x4686u, adapt_LoadCardNameAndInputColor },
	{ "DrawSymbolOnPlayAreaCursor", 0x46CCu, adapt_DrawSymbolOnPlayAreaCursor },
	{ "Func_2c6d9", 0x46D9u, adapt_Func_2c6d9 },
	{ "SpitPoison_AIEffect", 0x46F0u, adapt_SpitPoison_AIEffect },
	{ "TerrorStrike_SwitchDefendingPokemon", 0x4726u, adapt_TerrorStrike_SwitchDefendingPokemon },
	{ "PoisonFang_AIEffect", 0x4730u, adapt_PoisonFang_AIEffect },
	{ "WeepinbellPoisonPowder_AIEffect", 0x4738u, adapt_WeepinbellPoisonPowder_AIEffect },
	{ "VictreebelLure_AssertPokemonInBench", 0x4740u, adapt_VictreebelLure_AssertPokemonInBench },
	{ "VictreebelLure_GetBenchPokemonWithLowestHP", 0x4764u, adapt_VictreebelLure_GetBenchPokemonWithLowestHP },
	{ "VictreebelLure_SwitchDefendingPokemon", 0x476Au, adapt_VictreebelLure_SwitchDefendingPokemon },
	{ "GloomPoisonPowder_AIEffect", 0x478Bu, adapt_GloomPoisonPowder_AIEffect },
	{ "FoulOdorEffect", 0x4793u, adapt_FoulOdorEffect },
	{ "KakunaPoisonPowder_AIEffect", 0x47B4u, adapt_KakunaPoisonPowder_AIEffect },
	{ "SwordsDanceEffect", 0x47D0u, adapt_SwordsDanceEffect },
	{ "Twineedle_AIEffect", 0x47EDu, adapt_Twineedle_AIEffect },
	{ "Twineedle_MultiplierEffect", 0x47F5u, adapt_Twineedle_MultiplierEffect },
	{ "BeedrillPoisonSting_AIEffect", 0x480Du, adapt_BeedrillPoisonSting_AIEffect },
	{ "FoulGas_AIEffect", 0x4822u, adapt_FoulGas_AIEffect },
	{ "Sprout_CheckDeckAndPlayArea", 0x484Au, adapt_Sprout_CheckDeckAndPlayArea },
	{ "Sprout_AISelectEffect", 0x48B7u, adapt_Sprout_AISelectEffect },
	{ "Sprout_PutInPlayAreaEffect", 0x48CCu, adapt_Sprout_PutInPlayAreaEffect },
	{ "Teleport_CheckBench", 0x48ECu, adapt_Teleport_CheckBench },
	{ "Teleport_AISelectEffect", 0x490Fu, adapt_Teleport_AISelectEffect },
	{ "Teleport_SwitchEffect", 0x491Au, adapt_Teleport_SwitchEffect },
	{ "BigEggsplosion_AIEffect", 0x4925u, adapt_BigEggsplosion_AIEffect },
	{ "SetDamageToATimes20", 0x4958u, adapt_SetDamageToATimes20 },
	{ "Thrash_AIEffect", 0x496Bu, adapt_Thrash_AIEffect },
	{ "Toxic_AIEffect", 0x498Cu, adapt_Toxic_AIEffect },
	{ "Toxic_DoublePoisonEffect", 0x4994u, adapt_Toxic_DoublePoisonEffect },
	{ "BoyfriendsEffect", 0x4998u, adapt_BoyfriendsEffect },
	{ "NidoranFFurySwipes_AIEffect", 0x49BEu, adapt_NidoranFFurySwipes_AIEffect },
	{ "NidoranFFurySwipes_MultiplierEffect", 0x49C6u, adapt_NidoranFFurySwipes_MultiplierEffect },
	{ "NidoranFCallForFamily_CheckDeckAndPlayArea", 0x49DBu, adapt_NidoranFCallForFamily_CheckDeckAndPlayArea },
	{ "NidoranFCallForFamily_AISelectEffect", 0x4A55u, adapt_NidoranFCallForFamily_AISelectEffect },
	{ "NidoranFCallForFamily_PutInPlayAreaEffect", 0x4A6Eu, adapt_NidoranFCallForFamily_PutInPlayAreaEffect },
	{ "HornHazard_AIEffect", 0x4A8Eu, adapt_HornHazard_AIEffect },
	{ "NidorinaDoubleKick_AIEffect", 0x4AB3u, adapt_NidorinaDoubleKick_AIEffect },
	{ "NidorinaDoubleKick_MultiplierEffect", 0x4ABBu, adapt_NidorinaDoubleKick_MultiplierEffect },
	{ "NidorinoDoubleKick_AIEffect", 0x4AD3u, adapt_NidorinoDoubleKick_AIEffect },
	{ "NidorinoDoubleKick_MultiplierEffect", 0x4ADBu, adapt_NidorinoDoubleKick_MultiplierEffect },
	{ "ButterfreeWhirlwind_SwitchEffect", 0x4B09u, adapt_ButterfreeWhirlwind_SwitchEffect },
	{ "WeedlePoisonSting_AIEffect", 0x4B27u, adapt_WeedlePoisonSting_AIEffect },
	{ "IvysaurPoisonPowder_AIEffect", 0x4B2Fu, adapt_IvysaurPoisonPowder_AIEffect },
	{ "EnergyTrans_CheckPlayArea", 0x4B44u, adapt_EnergyTrans_CheckPlayArea },
	{ "EnergyTrans_PrintProcedure", 0x4B6Fu, adapt_EnergyTrans_PrintProcedure },
	{ "EnergyTrans_TransferEffect", 0x4B77u, adapt_EnergyTrans_TransferEffect },
	{ "EnergyTrans_AIEffect", 0x4BFBu, adapt_EnergyTrans_AIEffect },
	{ "CheckIfCardHasGrassEnergyAttached", 0x4C0Au, adapt_CheckIfCardHasGrassEnergyAttached },
	{ "GrimerMinimizeEffect", 0x4C30u, adapt_GrimerMinimizeEffect },
	{ "ToxicGasEffect", 0x4C36u, adapt_ToxicGasEffect },
	{ "Sludge_AIEffect", 0x4C38u, adapt_Sludge_AIEffect },
	{ "BellsproutCallForFamily_CheckDeckAndPlayArea", 0x4C40u, adapt_BellsproutCallForFamily_CheckDeckAndPlayArea },
	{ "BellsproutCallForFamily_AISelectEffect", 0x4CADu, adapt_BellsproutCallForFamily_AISelectEffect },
	{ "BellsproutCallForFamily_PutInPlayAreaEffect", 0x4CC2u, adapt_BellsproutCallForFamily_PutInPlayAreaEffect },
	{ "WeezingSmog_AIEffect", 0x4CE2u, adapt_WeezingSmog_AIEffect },
	{ "Shift_OncePerTurnCheck", 0x4D09u, adapt_Shift_OncePerTurnCheck },
	{ "Shift_PlayerSelectEffect", 0x4D21u, adapt_Shift_PlayerSelectEffect },
	{ "Shift_ChangeColorEffect", 0x4D5Du, adapt_Shift_ChangeColorEffect },
	{ "VenomPowder_AIEffect", 0x4D84u, adapt_VenomPowder_AIEffect },
	{ "TangelaPoisonPowder_AIEffect", 0x4DA0u, adapt_TangelaPoisonPowder_AIEffect },
	{ "Heal_OncePerTurnCheck", 0x4DA8u, adapt_Heal_OncePerTurnCheck },
	{ "PetalDance_AIEffect", 0x4E23u, adapt_PetalDance_AIEffect },
	{ "PetalDance_MultiplierEffect", 0x4E2Bu, adapt_PetalDance_MultiplierEffect },
	{ "PoisonWhip_AIEffect", 0x4E4Bu, adapt_PoisonWhip_AIEffect },
	{ "SolarPower_CheckUse", 0x4E53u, adapt_SolarPower_CheckUse },
	{ "ApplyExtraWaterEnergyDamageBonus", 0x4EC8u, adapt_ApplyExtraWaterEnergyDamageBonus },
	{ "OmastarWaterGunEffect", 0x4F05u, adapt_OmastarWaterGunEffect },
	{ "OmastarSpikeCannon_AIEffect", 0x4F0Au, adapt_OmastarSpikeCannon_AIEffect },
	{ "OmastarSpikeCannon_MultiplierEffect", 0x4F12u, adapt_OmastarSpikeCannon_MultiplierEffect },
	{ "ClairvoyanceEffect", 0x4F2Au, adapt_ClairvoyanceEffect },
	{ "OmanyteWaterGunEffect", 0x4F2Cu, adapt_OmanyteWaterGunEffect },
	{ "RainDanceEffect", 0x4F46u, adapt_RainDanceEffect },
	{ "HydroPumpEffect", 0x4F48u, adapt_HydroPumpEffect },
	{ "KinglerFlail_AIEffect", 0x4F4Eu, adapt_KinglerFlail_AIEffect },
	{ "KinglerFlail_HPCheck", 0x4F54u, adapt_KinglerFlail_HPCheck },
	{ "KrabbyCallForFamily_CheckDeckAndPlayArea", 0x4F5Du, adapt_KrabbyCallForFamily_CheckDeckAndPlayArea },
	{ "KrabbyCallForFamily_AISelectEffect", 0x4FCAu, adapt_KrabbyCallForFamily_AISelectEffect },
	{ "KrabbyCallForFamily_PutInPlayAreaEffect", 0x4FDFu, adapt_KrabbyCallForFamily_PutInPlayAreaEffect },
	{ "MagikarpFlail_AIEffect", 0x4FFFu, adapt_MagikarpFlail_AIEffect },
	{ "MagikarpFlail_HPCheck", 0x5005u, adapt_MagikarpFlail_HPCheck },
	{ "HeadacheEffect", 0x500Eu, adapt_HeadacheEffect },
	{ "PsyduckFurySwipes_AIEffect", 0x5016u, adapt_PsyduckFurySwipes_AIEffect },
	{ "PsyduckFurySwipes_MultiplierEffect", 0x501Eu, adapt_PsyduckFurySwipes_MultiplierEffect },
	{ "GolduckHyperBeam_PlayerSelectEffect", 0x5033u, adapt_GolduckHyperBeam_PlayerSelectEffect },
	{ "GolduckHyperBeam_AISelectEffect", 0x5065u, adapt_GolduckHyperBeam_AISelectEffect },
	{ "GolduckHyperBeam_DiscardEffect", 0x506Bu, adapt_GolduckHyperBeam_DiscardEffect },
	{ "SeadraWaterGunEffect", 0x5085u, adapt_SeadraWaterGunEffect },
	{ "VaporeonQuickAttack_AIEffect", 0x50B8u, adapt_VaporeonQuickAttack_AIEffect },
	{ "VaporeonWaterGunEffect", 0x50D3u, adapt_VaporeonWaterGunEffect },
	{ "StarmieRecover_CheckEnergyHP", 0x50D9u, adapt_StarmieRecover_CheckEnergyHP },
	{ "StarmieRecover_PlayerSelectEffect", 0x50F0u, adapt_StarmieRecover_PlayerSelectEffect },
	{ "StarmieRecover_AISelectEffect", 0x5103u, adapt_StarmieRecover_AISelectEffect },
	{ "StarmieRecover_DiscardEffect", 0x510Eu, adapt_StarmieRecover_DiscardEffect },
	{ "HorseaSmokescreenEffect", 0x5134u, adapt_HorseaSmokescreenEffect },
	{ "JellyfishSting_AIEffect", 0x5141u, adapt_JellyfishSting_AIEffect },
	{ "PoliwhirlAmnesia_CheckAttacks", 0x5149u, adapt_PoliwhirlAmnesia_CheckAttacks },
	{ "PoliwhirlAmnesia_AISelectEffect", 0x5173u, adapt_PoliwhirlAmnesia_AISelectEffect },
	{ "PoliwhirlAmnesia_DisableEffect", 0x5179u, adapt_PoliwhirlAmnesia_DisableEffect },
	{ "ApplyAmnesiaToAttack", 0x518Au, adapt_ApplyAmnesiaToAttack },
	{ "PoliwhirlDoubleslap_AIEffect", 0x51C0u, adapt_PoliwhirlDoubleslap_AIEffect },
	{ "PoliwhirlDoubleslap_MultiplierEffect", 0x51C8u, adapt_PoliwhirlDoubleslap_MultiplierEffect },
	{ "PoliwrathWaterGunEffect", 0x51E0u, adapt_PoliwrathWaterGunEffect },
	{ "Whirlpool_PlayerSelectEffect", 0x51E6u, adapt_Whirlpool_PlayerSelectEffect },
	{ "Whirlpool_AISelectEffect", 0x520Eu, adapt_Whirlpool_AISelectEffect },
	{ "Whirlpool_DiscardEffect", 0x5214u, adapt_Whirlpool_DiscardEffect },
	{ "PoliwagWaterGunEffect", 0x5227u, adapt_PoliwagWaterGunEffect },
	{ "CloysterSpikeCannon_AIEffect", 0x5246u, adapt_CloysterSpikeCannon_AIEffect },
	{ "CloysterSpikeCannon_MultiplierEffect", 0x524Eu, adapt_CloysterSpikeCannon_MultiplierEffect },
	{ "Cowardice_CheckUseAndBench", 0x528Bu, adapt_Cowardice_CheckUseAndBench },
	{ "Cowardice_ReturnToHandEffect", 0x52C3u, adapt_Cowardice_ReturnToHandEffect },
	{ "LaprasWaterGunEffect", 0x52EBu, adapt_LaprasWaterGunEffect },
	{ "Quickfreeze_InitialEffect", 0x52F1u, adapt_Quickfreeze_InitialEffect },
	{ "IceBreath_ZeroDamage", 0x5329u, adapt_IceBreath_ZeroDamage },
	{ "IceBreath_RandomPokemonDamageEffect", 0x532Eu, adapt_IceBreath_RandomPokemonDamageEffect },
	{ "FocusEnergyEffect", 0x533Fu, adapt_FocusEnergyEffect },
	{ "PlayerPickFireEnergyCardToDiscard", 0x534Bu, adapt_PlayerPickFireEnergyCardToDiscard },
	{ "AIPickFireEnergyCardToDiscard", 0x535Au, adapt_AIPickFireEnergyCardToDiscard },
	{ "ArcanineFlamethrower_CheckEnergy", 0x5363u, adapt_ArcanineFlamethrower_CheckEnergy },
	{ "ArcanineFlamethrower_PlayerSelectEffect", 0x5371u, adapt_ArcanineFlamethrower_PlayerSelectEffect },
	{ "ArcanineFlamethrower_AISelectEffect", 0x5375u, adapt_ArcanineFlamethrower_AISelectEffect },
	{ "ArcanineFlamethrower_DiscardEffect", 0x5379u, adapt_ArcanineFlamethrower_DiscardEffect },
	{ "ArcanineQuickAttack_AIEffect", 0x5385u, adapt_ArcanineQuickAttack_AIEffect },
	{ "FlamesOfRage_CheckEnergy", 0x53A0u, adapt_FlamesOfRage_CheckEnergy },
	{ "FlamesOfRage_PlayerSelectEffect", 0x53AEu, adapt_FlamesOfRage_PlayerSelectEffect },
	{ "FlamesOfRage_AISelectEffect", 0x53D5u, adapt_FlamesOfRage_AISelectEffect },
	{ "FlamesOfRage_DiscardEffect", 0x53DEu, adapt_FlamesOfRage_DiscardEffect },
	{ "FlamesOfRage_AIEffect", 0x53E9u, adapt_FlamesOfRage_AIEffect },
	{ "FlamesOfRage_DamageBoostEffect", 0x53EFu, adapt_FlamesOfRage_DamageBoostEffect },
	{ "RapidashStomp_AIEffect", 0x53F8u, adapt_RapidashStomp_AIEffect },
	{ "NinetalesLure_CheckBench", 0x5425u, adapt_NinetalesLure_CheckBench },
	{ "NinetalesLure_AISelectEffect", 0x5449u, adapt_NinetalesLure_AISelectEffect },
	{ "NinetalesLure_SwitchEffect", 0x544Fu, adapt_NinetalesLure_SwitchEffect },
	{ "FireBlast_CheckEnergy", 0x5463u, adapt_FireBlast_CheckEnergy },
	{ "FireBlast_PlayerSelectEffect", 0x5471u, adapt_FireBlast_PlayerSelectEffect },
	{ "FireBlast_AISelectEffect", 0x5475u, adapt_FireBlast_AISelectEffect },
	{ "FireBlast_DiscardEffect", 0x5479u, adapt_FireBlast_DiscardEffect },
	{ "Ember_CheckEnergy", 0x547Fu, adapt_Ember_CheckEnergy },
	{ "Ember_PlayerSelectEffect", 0x548Du, adapt_Ember_PlayerSelectEffect },
	{ "Ember_AISelectEffect", 0x5491u, adapt_Ember_AISelectEffect },
	{ "Ember_DiscardEffect", 0x5495u, adapt_Ember_DiscardEffect },
	{ "Wildfire_CheckEnergy", 0x549Bu, adapt_Wildfire_CheckEnergy },
	{ "Wildfire_PlayerSelectEffect", 0x54A9u, adapt_Wildfire_PlayerSelectEffect },
	{ "Wildfire_AISelectEffect", 0x54DDu, adapt_Wildfire_AISelectEffect },
	{ "Wildfire_DiscardEnergyEffect", 0x54E1u, adapt_Wildfire_DiscardEnergyEffect },
	{ "Wildfire_DiscardDeckEffect", 0x54F4u, adapt_Wildfire_DiscardDeckEffect },
	{ "MoltresLv35DiveBomb_AIEffect", 0x5523u, adapt_MoltresLv35DiveBomb_AIEffect },
	{ "FlareonQuickAttack_AIEffect", 0x5541u, adapt_FlareonQuickAttack_AIEffect },
	{ "FlareonFlamethrower_CheckEnergy", 0x555Cu, adapt_FlareonFlamethrower_CheckEnergy },
	{ "FlareonFlamethrower_PlayerSelectEffect", 0x556Au, adapt_FlareonFlamethrower_PlayerSelectEffect },
	{ "FlareonFlamethrower_AISelectEffect", 0x556Eu, adapt_FlareonFlamethrower_AISelectEffect },
	{ "FlareonFlamethrower_DiscardEffect", 0x5572u, adapt_FlareonFlamethrower_DiscardEffect },
	{ "MagmarFlamethrower_CheckEnergy", 0x5578u, adapt_MagmarFlamethrower_CheckEnergy },
	{ "MagmarFlamethrower_PlayerSelectEffect", 0x5586u, adapt_MagmarFlamethrower_PlayerSelectEffect },
	{ "MagmarFlamethrower_AISelectEffect", 0x558Au, adapt_MagmarFlamethrower_AISelectEffect },
	{ "MagmarFlamethrower_DiscardEffect", 0x558Eu, adapt_MagmarFlamethrower_DiscardEffect },
	{ "MagmarSmokescreenEffect", 0x5594u, adapt_MagmarSmokescreenEffect },
	{ "MagmarSmog_AIEffect", 0x559Au, adapt_MagmarSmog_AIEffect },
	{ "CharmeleonFlamethrower_CheckEnergy", 0x55A2u, adapt_CharmeleonFlamethrower_CheckEnergy },
	{ "CharmeleonFlamethrower_PlayerSelectEffect", 0x55B0u, adapt_CharmeleonFlamethrower_PlayerSelectEffect },
	{ "CharmeleonFlamethrower_AISelectEffect", 0x55B4u, adapt_CharmeleonFlamethrower_AISelectEffect },
	{ "CharmeleonFlamethrower_DiscardEffect", 0x55B8u, adapt_CharmeleonFlamethrower_DiscardEffect },
	{ "EnergyBurnEffect", 0x55BEu, adapt_EnergyBurnEffect },
	{ "FireSpin_CheckEnergy", 0x55C0u, adapt_FireSpin_CheckEnergy },
	{ "FireSpin_PlayerSelectEffect", 0x55CDu, adapt_FireSpin_PlayerSelectEffect },
	{ "FireSpin_AISelectEffect", 0x5606u, adapt_FireSpin_AISelectEffect },
	{ "FireSpin_DiscardEffect", 0x5614u, adapt_FireSpin_DiscardEffect },
	{ "EnergyBurnCheck_Unreferenced", 0x5620u, adapt_EnergyBurnCheck_Unreferenced },
	{ "FlareonRage_AIEffect", 0x5638u, adapt_FlareonRage_AIEffect },
	{ "FlareonRage_DamageBoostEffect", 0x563Eu, adapt_FlareonRage_DamageBoostEffect },
	{ "DancingEmbers_AIEffect", 0x56A3u, adapt_DancingEmbers_AIEffect },
	{ "DancingEmbers_MultiplierEffect", 0x56ABu, adapt_DancingEmbers_MultiplierEffect },
	{ "Firegiver_InitialEffect", 0x56C0u, adapt_Firegiver_InitialEffect },
	{ "Firegiver_AddToHandEffect", 0x56C2u, adapt_Firegiver_AddToHandEffect },
	{ "MoltresLv37DiveBomb_AIEffect", 0x576Eu, adapt_MoltresLv37DiveBomb_AIEffect },
	{ "GetEnergyAttachedMultiplierDamage", 0x578Cu, adapt_GetEnergyAttachedMultiplierDamage },
	{ "HandleEnergyCardsInDiscardPileSelection", 0x57BCu, adapt_HandleEnergyCardsInDiscardPileSelection },
	{ "Curse_CheckDamageAndBench", 0x57FCu, adapt_Curse_CheckDamageAndBench },
	{ "Curse_PlayerSelectEffect", 0x5834u, adapt_Curse_PlayerSelectEffect },
	{ "GengarDarkMind_AISelectEffect", 0x592Au, adapt_GengarDarkMind_AISelectEffect },
	{ "GengarDarkMind_DamageBenchEffect", 0x593Cu, adapt_GengarDarkMind_DamageBenchEffect },
	{ "DestinyBond_CheckEnergy", 0x5956u, adapt_DestinyBond_CheckEnergy },
	{ "DestinyBond_PlayerSelectEffect", 0x5964u, adapt_DestinyBond_PlayerSelectEffect },
	{ "DestinyBond_AISelectEffect", 0x5976u, adapt_DestinyBond_AISelectEffect },
	{ "DestinyBond_DiscardEffect", 0x5981u, adapt_DestinyBond_DiscardEffect },
	{ "DestinyBond_DestinyBondEffect", 0x5987u, adapt_DestinyBond_DestinyBondEffect },
	{ "EnergyConversion_CheckEnergy", 0x598Du, adapt_EnergyConversion_CheckEnergy },
	{ "EnergyConversion_AISelectEffect", 0x599Bu, adapt_EnergyConversion_AISelectEffect },
	{ "DreamEaterEffect", 0x59D6u, adapt_DreamEaterEffect },
	{ "TransparencyEffect", 0x59E5u, adapt_TransparencyEffect },
	{ "Prophecy_CheckDeck", 0x59E7u, adapt_Prophecy_CheckDeck },
	{ "Prophecy_AISelectEffect", 0x5A3Cu, adapt_Prophecy_AISelectEffect },
	{ "Prophecy_ReorderDeckEffect", 0x5A41u, adapt_Prophecy_ReorderDeckEffect },
	{ "HypnoDarkMind_AISelectEffect", 0x5B52u, adapt_HypnoDarkMind_AISelectEffect },
	{ "HypnoDarkMind_DamageBenchEffect", 0x5B64u, adapt_HypnoDarkMind_DamageBenchEffect },
	{ "InvisibleWallEffect", 0x5B77u, adapt_InvisibleWallEffect },
	{ "MrMimeMeditate_AIEffect", 0x5B79u, adapt_MrMimeMeditate_AIEffect },
	{ "MrMimeMeditate_DamageBoostEffect", 0x5B7Fu, adapt_MrMimeMeditate_DamageBoostEffect },
	{ "DamageSwap_CheckDamage", 0x5B8Eu, adapt_DamageSwap_CheckDamage },
	{ "DamageSwap_SelectAndSwapEffect", 0x5BA2u, adapt_DamageSwap_SelectAndSwapEffect },
	{ "DamageSwap_SwapEffect", 0x5C27u, adapt_DamageSwap_SwapEffect },
	{ "TryGiveDamageCounter_DamageSwap", 0x5C30u, adapt_TryGiveDamageCounter_DamageSwap },
	{ "PsywaveEffect", 0x5C49u, adapt_PsywaveEffect },
	{ "DevolutionBeam_CheckPlayArea", 0x5C53u, adapt_DevolutionBeam_CheckPlayArea },
	{ "DevolutionBeam_AISelectEffect", 0x5C9Eu, adapt_DevolutionBeam_AISelectEffect },
	{ "DevolutionBeam_LoadAnimation", 0x5CB6u, adapt_DevolutionBeam_LoadAnimation },
	{ "CheckIfTurnDuelistHasEvolvedCards", 0x5D3Bu, adapt_CheckIfTurnDuelistHasEvolvedCards },
	{ "FindFirstNonBasicCardInPlayArea", 0x5D62u, adapt_FindFirstNonBasicCardInPlayArea },
	{ "NeutralizingShieldEffect", 0x5D79u, adapt_NeutralizingShieldEffect },
	{ "Psychic_AIEffect", 0x5D7Bu, adapt_Psychic_AIEffect },
	{ "Psychic_DamageBoostEffect", 0x5D81u, adapt_Psychic_DamageBoostEffect },
	{ "Barrier_CheckEnergy", 0x5D8Eu, adapt_Barrier_CheckEnergy },
	{ "Barrier_PlayerSelectEffect", 0x5D9Cu, adapt_Barrier_PlayerSelectEffect },
	{ "Barrier_AISelectEffect", 0x5DAEu, adapt_Barrier_AISelectEffect },
	{ "Barrier_DiscardEffect", 0x5DB9u, adapt_Barrier_DiscardEffect },
	{ "Barrier_BarrierEffect", 0x5DBFu, adapt_Barrier_BarrierEffect },
	{ "MewtwoAltEnergyAbsorption_CheckDiscardPile", 0x5DC5u, adapt_MewtwoAltEnergyAbsorption_CheckDiscardPile },
	{ "MewtwoAltEnergyAbsorption_AISelectEffect", 0x5DD3u, adapt_MewtwoAltEnergyAbsorption_AISelectEffect },
	{ "MewtwoAltEnergyAbsorption_AddToHandEffect", 0x5DECu, adapt_MewtwoAltEnergyAbsorption_AddToHandEffect },
	{ "MewtwoEnergyAbsorption_CheckDiscardPile", 0x5DFFu, adapt_MewtwoEnergyAbsorption_CheckDiscardPile },
	{ "MewtwoEnergyAbsorption_AISelectEffect", 0x5E0Du, adapt_MewtwoEnergyAbsorption_AISelectEffect },
	{ "MewtwoEnergyAbsorption_AddToHandEffect", 0x5E26u, adapt_MewtwoEnergyAbsorption_AddToHandEffect },
	{ "StrangeBehavior_CheckDamage", 0x5E39u, adapt_StrangeBehavior_CheckDamage },
	{ "StrangeBehavior_SelectAndSwapEffect", 0x5E5Bu, adapt_StrangeBehavior_SelectAndSwapEffect },
	{ "StrangeBehavior_SwapEffect", 0x5EB3u, adapt_StrangeBehavior_SwapEffect },
	{ "TryGiveDamageCounter_StrangeBehavior", 0x5EBCu, adapt_TryGiveDamageCounter_StrangeBehavior },
	{ "SpacingOut_CheckDamage", 0x5ED5u, adapt_SpacingOut_CheckDamage },
	{ "SpacingOut_HealEffect", 0x5EF1u, adapt_SpacingOut_HealEffect },
	{ "Scavenge_CheckDiscardPile", 0x5F05u, adapt_Scavenge_CheckDiscardPile },
	{ "Scavenge_PlayerSelectEnergyEffect", 0x5F1Au, adapt_Scavenge_PlayerSelectEnergyEffect },
	{ "Scavenge_AISelectEffect", 0x5F2Du, adapt_Scavenge_AISelectEffect },
	{ "Scavenge_DiscardEffect", 0x5F40u, adapt_Scavenge_DiscardEffect },
	{ "Scavenge_AddToHandEffect", 0x5F5Fu, adapt_Scavenge_AddToHandEffect },
	{ "SlowpokeAmnesia_CheckAttacks", 0x5F74u, adapt_SlowpokeAmnesia_CheckAttacks },
	{ "SlowpokeAmnesia_AISelectEffect", 0x5F7Fu, adapt_SlowpokeAmnesia_AISelectEffect },
	{ "SlowpokeAmnesia_DisableEffect", 0x5F85u, adapt_SlowpokeAmnesia_DisableEffect },
	{ "KadabraRecover_CheckEnergyHP", 0x5F89u, adapt_KadabraRecover_CheckEnergyHP },
	{ "KadabraRecover_PlayerSelectEffect", 0x5FA0u, adapt_KadabraRecover_PlayerSelectEffect },
	{ "KadabraRecover_AISelectEffect", 0x5FB2u, adapt_KadabraRecover_AISelectEffect },
	{ "KadabraRecover_DiscardEffect", 0x5FBDu, adapt_KadabraRecover_DiscardEffect },
	{ "JynxDoubleslap_AIEffect", 0x5FCFu, adapt_JynxDoubleslap_AIEffect },
	{ "JynxDoubleslap_MultiplierEffect", 0x5FD7u, adapt_JynxDoubleslap_MultiplierEffect },
	{ "JynxMeditate_AIEffect", 0x5FECu, adapt_JynxMeditate_AIEffect },
	{ "JynxMeditate_DamageBoostEffect", 0x5FF2u, adapt_JynxMeditate_DamageBoostEffect },
	{ "MysteryAttack_AIEffect", 0x6001u, adapt_MysteryAttack_AIEffect },
	{ "MysteryAttack_RandomEffect", 0x6009u, adapt_MysteryAttack_RandomEffect },
	{ "StoneBarrage_AIEffect", 0x604Au, adapt_StoneBarrage_AIEffect },
	{ "OnixHardenEffect", 0x6075u, adapt_OnixHardenEffect },
	{ "PrimeapeFurySwipes_AIEffect", 0x607Bu, adapt_PrimeapeFurySwipes_AIEffect },
	{ "PrimeapeFurySwipes_MultiplierEffect", 0x6083u, adapt_PrimeapeFurySwipes_MultiplierEffect },
	{ "StrikesBackEffect", 0x60AFu, adapt_StrikesBackEffect },
	{ "KabutoArmorEffect", 0x60B1u, adapt_KabutoArmorEffect },
	{ "SnivelEffect", 0x60CBu, adapt_SnivelEffect },
	{ "CuboneRage_AIEffect", 0x60D1u, adapt_CuboneRage_AIEffect },
	{ "CuboneRage_DamageBoostEffect", 0x60D7u, adapt_CuboneRage_DamageBoostEffect },
	{ "Bonemerang_AIEffect", 0x60E0u, adapt_Bonemerang_AIEffect },
	{ "Bonemerang_MultiplierEffect", 0x60E8u, adapt_Bonemerang_MultiplierEffect },
	{ "MarowakCallForFamily_CheckDeckAndPlayArea", 0x6100u, adapt_MarowakCallForFamily_CheckDeckAndPlayArea },
	{ "MarowakCallForFamily_AISelectEffect", 0x6177u, adapt_MarowakCallForFamily_AISelectEffect },
	{ "MarowakCallForFamily_PutInPlayAreaEffect", 0x6194u, adapt_MarowakCallForFamily_PutInPlayAreaEffect },
	{ "KarateChop_AIEffect", 0x61B4u, adapt_KarateChop_AIEffect },
	{ "KarateChop_DamageSubtractionEffect", 0x61BAu, adapt_KarateChop_DamageSubtractionEffect },
	{ "GravelerHardenEffect", 0x61F6u, adapt_GravelerHardenEffect },
	{ "StretchKick_CheckBench", 0x6231u, adapt_StretchKick_CheckBench },
	{ "StretchKick_AISelectEffect", 0x6255u, adapt_StretchKick_AISelectEffect },
	{ "StretchKick_BenchDamageEffect", 0x625Bu, adapt_StretchKick_BenchDamageEffect },
	{ "SandAttackEffect", 0x626Bu, adapt_SandAttackEffect },
	{ "SandslashFurySwipes_AIEffect", 0x6271u, adapt_SandslashFurySwipes_AIEffect },
	{ "SandslashFurySwipes_MultiplierEffect", 0x6279u, adapt_SandslashFurySwipes_MultiplierEffect },
	{ "PrehistoricPowerEffect", 0x629Au, adapt_PrehistoricPowerEffect },
	{ "Peek_OncePerTurnCheck", 0x629Cu, adapt_Peek_OncePerTurnCheck },
	{ "Wail_BenchCheck", 0x631Cu, adapt_Wail_BenchCheck },
	{ "Thunderpunch_AIEffect", 0x6399u, adapt_Thunderpunch_AIEffect },
	{ "LightScreenEffect", 0x63BAu, adapt_LightScreenEffect },
	{ "ElectabuzzQuickAttack_AIEffect", 0x63C0u, adapt_ElectabuzzQuickAttack_AIEffect },
	{ "ThunderboltEffect", 0x6419u, adapt_ThunderboltEffect },
	{ "JolteonQuickAttack_AIEffect", 0x64BBu, adapt_JolteonQuickAttack_AIEffect },
	{ "PinMissile_AIEffect", 0x64D6u, adapt_PinMissile_AIEffect },
	{ "PinMissile_MultiplierEffect", 0x64DEu, adapt_PinMissile_MultiplierEffect },
	{ "Fly_AIEffect", 0x64F4u, adapt_Fly_AIEffect },
	{ "Spark_AISelectEffect", 0x6562u, adapt_Spark_AISelectEffect },
	{ "Spark_BenchDamageEffect", 0x6574u, adapt_Spark_BenchDamageEffect },
	{ "PikachuLv16GrowlEffect", 0x6589u, adapt_PikachuLv16GrowlEffect },
	{ "PikachuAltLv16GrowlEffect", 0x658Fu, adapt_PikachuAltLv16GrowlEffect },
	{ "ChainLightningEffect", 0x6595u, adapt_ChainLightningEffect },
	{ "Gigashock_PlayerSelectEffect", 0x660Du, adapt_Gigashock_PlayerSelectEffect },
	{ "Gigashock_AISelectEffect", 0x66C3u, adapt_Gigashock_AISelectEffect },
	{ "Gigashock_BenchDamageEffect", 0x671Fu, adapt_Gigashock_BenchDamageEffect },
	{ "MagnetonSonicboom_UnaffectedByColorEffect", 0x6758u, adapt_MagnetonSonicboom_UnaffectedByColorEffect },
	{ "MagnetonSonicboom_NullEffect", 0x675Eu, adapt_MagnetonSonicboom_NullEffect },
	{ "PealOfThunder_InitialEffect", 0x677Eu, adapt_PealOfThunder_InitialEffect },
	{ "ElectrodeSonicboom_UnaffectedByColorEffect", 0x6870u, adapt_ElectrodeSonicboom_UnaffectedByColorEffect },
	{ "ElectrodeSonicboom_NullEffect", 0x6876u, adapt_ElectrodeSonicboom_NullEffect },
	{ "EnergySpike_DeckCheck", 0x6877u, adapt_EnergySpike_DeckCheck },
	{ "EnergySpike_AISelectEffect", 0x68F1u, adapt_EnergySpike_AISelectEffect },
	{ "EnergySpike_AttachEnergyEffect", 0x68F6u, adapt_EnergySpike_AttachEnergyEffect },
	{ "JolteonDoubleKick_AIEffect", 0x6930u, adapt_JolteonDoubleKick_AIEffect },
	{ "JolteonDoubleKick_MultiplierEffect", 0x6938u, adapt_JolteonDoubleKick_MultiplierEffect },
	{ "EeveeQuickAttack_AIEffect", 0x6962u, adapt_EeveeQuickAttack_AIEffect },
	{ "SpearowMirrorMove_AIEffect", 0x697Du, adapt_SpearowMirrorMove_AIEffect },
	{ "SpearowMirrorMove_InitialEffect1", 0x697Fu, adapt_SpearowMirrorMove_InitialEffect1 },
	{ "SpearowMirrorMove_PlayerSelection", 0x6983u, adapt_SpearowMirrorMove_PlayerSelection },
	{ "SpearowMirrorMove_AISelection", 0x6985u, adapt_SpearowMirrorMove_AISelection },
	{ "SpearowMirrorMove_BeforeDamage", 0x6987u, adapt_SpearowMirrorMove_BeforeDamage },
	{ "SpearowMirrorMove_AfterDamage", 0x6989u, adapt_SpearowMirrorMove_AfterDamage },
	{ "MirrorMove_AIEffect", 0x698Cu, adapt_MirrorMove_AIEffect },
	{ "MirrorMove_InitialEffect1", 0x6999u, adapt_MirrorMove_InitialEffect1 },
	{ "MirrorMove_PlayerSelection", 0x69BEu, adapt_MirrorMove_PlayerSelection },
	{ "MirrorMove_AISelection", 0x69CBu, adapt_MirrorMove_AISelection },
	{ "MirrorMove_BeforeDamage", 0x69EBu, adapt_MirrorMove_BeforeDamage },
	{ "MirrorMove_AfterDamage", 0x6A28u, adapt_MirrorMove_AfterDamage },
	{ "MirrorMove_ExecuteStatusEffect", 0x6A8Fu, adapt_MirrorMove_ExecuteStatusEffect },
	{ "StepIn_BenchCheck", 0x6ACAu, adapt_StepIn_BenchCheck },
	{ "StepIn_SwitchEffect", 0x6AE8u, adapt_StepIn_SwitchEffect },
	{ "DragoniteLv45Slam_AIEffect", 0x6AF6u, adapt_DragoniteLv45Slam_AIEffect },
	{ "DragoniteLv45Slam_MultiplierEffect", 0x6AFEu, adapt_DragoniteLv45Slam_MultiplierEffect },
	{ "ThickSkinnedEffect", 0x6B15u, adapt_ThickSkinnedEffect },
	{ "LeekSlap_AIEffect", 0x6B17u, adapt_LeekSlap_AIEffect },
	{ "LeekSlap_OncePerDuelCheck", 0x6B1Fu, adapt_LeekSlap_OncePerDuelCheck },
	{ "LeekSlap_SetUsedThisDuelFlag", 0x6B2Cu, adapt_LeekSlap_SetUsedThisDuelFlag },
	{ "CometPunch_AIEffect", 0x6B5Du, adapt_CometPunch_AIEffect },
	{ "CometPunch_MultiplierEffect", 0x6B65u, adapt_CometPunch_MultiplierEffect },
	{ "TaurosStomp_AIEffect", 0x6B7Bu, adapt_TaurosStomp_AIEffect },
	{ "Rampage_AIEffect", 0x6B96u, adapt_Rampage_AIEffect },
	{ "FuryAttack_AIEffect", 0x6BBAu, adapt_FuryAttack_AIEffect },
	{ "FuryAttack_MultiplierEffect", 0x6BC2u, adapt_FuryAttack_MultiplierEffect },
	{ "RetreatAidEffect", 0x6BD7u, adapt_RetreatAidEffect },
	{ "DodrioRage_AIEffect", 0x6BD9u, adapt_DodrioRage_AIEffect },
	{ "DodrioRage_DamageBoostEffect", 0x6BDFu, adapt_DodrioRage_DamageBoostEffect },
	{ "DragonairSlam_AIEffect", 0x6C0Cu, adapt_DragonairSlam_AIEffect },
	{ "DragonairSlam_MultiplierEffect", 0x6C14u, adapt_DragonairSlam_MultiplierEffect },
	{ "DragonairHyperBeam_PlayerSelectEffect", 0x6C2Cu, adapt_DragonairHyperBeam_PlayerSelectEffect },
	{ "DragonairHyperBeam_AISelectEffect", 0x6C2Fu, adapt_DragonairHyperBeam_AISelectEffect },
	{ "DragonairHyperBeam_DiscardEffect", 0x6C35u, adapt_DragonairHyperBeam_DiscardEffect },
	{ "HandleEnergyDiscardEffectSelection", 0x6C4Fu, adapt_HandleEnergyDiscardEffectSelection },
	{ "ClefableMetronome_CheckAttacks", 0x6C77u, adapt_ClefableMetronome_CheckAttacks },
	{ "ClefableMetronome_AISelectEffect", 0x6C7Eu, adapt_ClefableMetronome_AISelectEffect },
	{ "ClefableMetronome_UseAttackEffect", 0x6C82u, adapt_ClefableMetronome_UseAttackEffect },
	{ "ClefableMinimizeEffect", 0x6C88u, adapt_ClefableMinimizeEffect },
	{ "HurricaneEffect", 0x6C8Eu, adapt_HurricaneEffect },
	{ "PidgeottoWhirlwind_SwitchEffect", 0x6CE9u, adapt_PidgeottoWhirlwind_SwitchEffect },
	{ "PidgeottoMirrorMove_AIEffect", 0x6CEFu, adapt_PidgeottoMirrorMove_AIEffect },
	{ "PidgeottoMirrorMove_InitialEffect1", 0x6CF2u, adapt_PidgeottoMirrorMove_InitialEffect1 },
	{ "PidgeottoMirrorMove_PlayerSelection", 0x6CF8u, adapt_PidgeottoMirrorMove_PlayerSelection },
	{ "PidgeottoMirrorMove_AISelection", 0x6CFBu, adapt_PidgeottoMirrorMove_AISelection },
	{ "PidgeottoMirrorMove_BeforeDamage", 0x6CFEu, adapt_PidgeottoMirrorMove_BeforeDamage },
	{ "PidgeottoMirrorMove_AfterDamage", 0x6D01u, adapt_PidgeottoMirrorMove_AfterDamage },
	{ "ClefairyMetronome_CheckAttacks", 0x6D0Bu, adapt_ClefairyMetronome_CheckAttacks },
	{ "ClefairyMetronome_AISelectEffect", 0x6D12u, adapt_ClefairyMetronome_AISelectEffect },
	{ "ClefairyMetronome_UseAttackEffect", 0x6D16u, adapt_ClefairyMetronome_UseAttackEffect },
	{ "HandlePlayerMetronomeEffect", 0x6D18u, adapt_HandlePlayerMetronomeEffect },
	{ "HandleAIMetronomeEffect", 0x6D86u, adapt_HandleAIMetronomeEffect },
	{ "DoTheWaveEffect", 0x6D87u, adapt_DoTheWaveEffect },
	{ "FirstAid_DamageCheck", 0x6D94u, adapt_FirstAid_DamageCheck },
	{ "PounceEffect", 0x6DACu, adapt_PounceEffect },
	{ "PidgeyWhirlwind_SwitchEffect", 0x6DCFu, adapt_PidgeyWhirlwind_SwitchEffect },
	{ "Conversion1_WeaknessCheck", 0x6DD5u, adapt_Conversion1_WeaknessCheck },
	{ "Conversion1_PlayerSelectEffect", 0x6DEDu, adapt_Conversion1_PlayerSelectEffect },
	{ "Conversion1_AISelectEffect", 0x6DF7u, adapt_Conversion1_AISelectEffect },
	{ "Conversion1_ChangeWeaknessEffect", 0x6DFBu, adapt_Conversion1_ChangeWeaknessEffect },
	{ "Conversion2_ResistanceCheck", 0x6E1Fu, adapt_Conversion2_ResistanceCheck },
	{ "Conversion2_PlayerSelectEffect", 0x6E31u, adapt_Conversion2_PlayerSelectEffect },
	{ "Conversion2_AISelectEffect", 0x6E3Cu, adapt_Conversion2_AISelectEffect },
	{ "Conversion2_ChangeResistanceEffect", 0x6E5Eu, adapt_Conversion2_ChangeResistanceEffect },
	{ "PrintArenaCardNameAndColorText", 0x6E6Cu, adapt_PrintArenaCardNameAndColorText },
	{ "AISelectConversionColor", 0x6E7Fu, adapt_AISelectConversionColor },
	{ "SuperFang_AIEffect", 0x6F01u, adapt_SuperFang_AIEffect },
	{ "SuperFang_HalfHPEffect", 0x6F07u, adapt_SuperFang_HalfHPEffect },
	{ "TrainerCardAsPokemon_BenchCheck", 0x6F18u, adapt_TrainerCardAsPokemon_BenchCheck },
	{ "TrainerCardAsPokemon_DiscardEffect", 0x6F3Cu, adapt_TrainerCardAsPokemon_DiscardEffect },
	{ "HealingWind_InitialEffect", 0x6F51u, adapt_HealingWind_InitialEffect },
	{ "DragoniteLv41Slam_AIEffect", 0x6F9Cu, adapt_DragoniteLv41Slam_AIEffect },
	{ "DragoniteLv41Slam_MultiplierEffect", 0x6FA4u, adapt_DragoniteLv41Slam_MultiplierEffect },
	{ "CopyPlayAreaHPToBackup_Unreferenced", 0x6FBCu, adapt_CopyPlayAreaHPToBackup_Unreferenced },
	{ "CopyPlayAreaHPFromBackup_Unreferenced", 0x6FCEu, adapt_CopyPlayAreaHPFromBackup_Unreferenced },
	{ "CatPunchEffect", 0x6FE0u, adapt_CatPunchEffect },
	{ "MorphEffect", 0x6FF6u, adapt_MorphEffect },
	{ "PickRandomBasicCardFromDeck", 0x7098u, adapt_PickRandomBasicCardFromDeck },
	{ "Gale_LoadAnimation", 0x70D0u, adapt_Gale_LoadAnimation },
	{ "Gale_SwitchEffect", 0x70D6u, adapt_Gale_SwitchEffect },
	{ "FriendshipSong_BenchCheck", 0x710Du, adapt_FriendshipSong_BenchCheck },
	{ "ExpandEffect", 0x7153u, adapt_ExpandEffect },
	{ "SuperPotion_DamageEnergyCheck", 0x7159u, adapt_SuperPotion_DamageEnergyCheck },
	{ "CheckIfThereAreAnyEnergyCardsAttached", 0x71C4u, adapt_CheckIfThereAreAnyEnergyCardsAttached },
	{ "EnergyRemoval_EnergyCheck", 0x7252u, adapt_EnergyRemoval_EnergyCheck },
	{ "EnergyRemoval_AISelection", 0x726Fu, adapt_EnergyRemoval_AISelection },
	{ "EnergyRemoval_DiscardEffect", 0x7273u, adapt_EnergyRemoval_DiscardEffect },
	{ "EnergyRetrieval_HandEnergyCheck", 0x728Eu, adapt_EnergyRetrieval_HandEnergyCheck },
	{ "EnergyRetrieval_PlayerHandSelection", 0x72A0u, adapt_EnergyRetrieval_PlayerHandSelection },
	{ "EnergyRetrieval_PlayerDiscardPileSelection", 0x72B9u, adapt_EnergyRetrieval_PlayerDiscardPileSelection },
	{ "EnergyRetrieval_DiscardAndAddToHandEffect", 0x72F8u, adapt_EnergyRetrieval_DiscardAndAddToHandEffect },
	{ "EnergySearch_DeckCheck", 0x731Cu, adapt_EnergySearch_DeckCheck },
	{ "CheckIfCardIsBasicEnergy", 0x738Fu, adapt_CheckIfCardIsBasicEnergy },
	{ "Potion_DamageCheck", 0x73CAu, adapt_Potion_DamageCheck },
	{ "ItemFinder_HandDiscardPileCheck", 0x743Bu, adapt_ItemFinder_HandDiscardPileCheck },
	{ "ItemFinder_DiscardAddToHandEffect", 0x7463u, adapt_ItemFinder_DiscardAddToHandEffect },
	{ "Defender_AttachDefenderEffect", 0x7499u, adapt_Defender_AttachDefenderEffect },
	{ "MysteriousFossil_BenchCheck", 0x74B3u, adapt_MysteriousFossil_BenchCheck },
	{ "MysteriousFossil_PlaceInPlayAreaEffect", 0x74BFu, adapt_MysteriousFossil_PlaceInPlayAreaEffect },
	{ "FullHeal_StatusCheck", 0x74C5u, adapt_FullHeal_StatusCheck },
	{ "ComputerSearch_HandDeckCheck", 0x7513u, adapt_ComputerSearch_HandDeckCheck },
	{ "ClefairyDoll_BenchCheck", 0x7561u, adapt_ClefairyDoll_BenchCheck },
	{ "ClefairyDoll_PlaceInPlayAreaEffect", 0x756Du, adapt_ClefairyDoll_PlaceInPlayAreaEffect },
	{ "MrFuji_BenchCheck", 0x7573u, adapt_MrFuji_BenchCheck },
	{ "MrFuji_ReturnToDeckEffect", 0x758Fu, adapt_MrFuji_ReturnToDeckEffect },
	{ "PlusPowerEffect", 0x75E0u, adapt_PlusPowerEffect },
	{ "Switch_BenchCheck", 0x75EEu, adapt_Switch_BenchCheck },
	{ "Switch_SwitchEffect", 0x760Au, adapt_Switch_SwitchEffect },
	{ "PokemonCenter_DamageCheck", 0x7611u, adapt_PokemonCenter_DamageCheck },
	{ "PokemonFlute_BenchCheck", 0x7659u, adapt_PokemonFlute_BenchCheck },
	{ "PokemonFlute_PlaceInPlayAreaText", 0x768Fu, adapt_PokemonFlute_PlaceInPlayAreaText },
	{ "PokemonBreeder_HandPlayAreaCheck", 0x76B3u, adapt_PokemonBreeder_HandPlayAreaCheck },
	{ "PokemonBreeder_EvolveEffect", 0x76F4u, adapt_PokemonBreeder_EvolveEffect },
	{ "CreatePlayableStage2PokemonCardListFromHand", 0x773Eu, adapt_CreatePlayableStage2PokemonCardListFromHand },
	{ "ScoopUp_BenchCheck", 0x7795u, adapt_ScoopUp_BenchCheck },
	{ "ScoopUp_ReturnToHandEffect", 0x77C3u, adapt_ScoopUp_ReturnToHandEffect },
	{ "PokemonTrader_HandDeckCheck", 0x7826u, adapt_PokemonTrader_HandDeckCheck },
	{ "PokemonTrader_PlayerHandSelection", 0x7838u, adapt_PokemonTrader_PlayerHandSelection },
	{ "CreatePokemonCardListFromHand", 0x78B6u, adapt_CreatePokemonCardListFromHand },
	{ "Pokedex_DeckCheck", 0x78E1u, adapt_Pokedex_DeckCheck },
	{ "Pokedex_OrderDeckCardsEffect", 0x79AAu, adapt_Pokedex_OrderDeckCardsEffect },
	{ "Maintenance_HandCheck", 0x7A70u, adapt_Maintenance_HandCheck },
	{ "PokeBall_DeckCheck", 0x7AADu, adapt_PokeBall_DeckCheck },
	{ "Recycle_DiscardPileCheck", 0x7B36u, adapt_Recycle_DiscardPileCheck },
	{ "Recycle_AddToHandEffect", 0x7B68u, adapt_Recycle_AddToHandEffect },
	{ "Revive_BenchCheck", 0x7B80u, adapt_Revive_BenchCheck },
	{ "Revive_PlaceInPlayAreaEffect", 0x7BB0u, adapt_Revive_PlaceInPlayAreaEffect },
	{ "CreateBasicPokemonCardListFromDiscardPile", 0x7BD6u, adapt_CreateBasicPokemonCardListFromDiscardPile },
	{ "DevolutionSpray_PlayAreaEvolutionCheck", 0x7C0Bu, adapt_DevolutionSpray_PlayAreaEvolutionCheck },
	{ "SuperEnergyRemoval_EnergyCheck", 0x7CD0u, adapt_SuperEnergyRemoval_EnergyCheck },
	{ "SuperEnergyRemoval_DiscardEffect", 0x7D73u, adapt_SuperEnergyRemoval_DiscardEffect },
	{ "SuperEnergyRetrieval_HandEnergyCheck", 0x7DA4u, adapt_SuperEnergyRetrieval_HandEnergyCheck },
	{ "SuperEnergyRetrieval_DiscardAndAddToHandEffect", 0x7DFAu, adapt_SuperEnergyRetrieval_DiscardAndAddToHandEffect },
	{ "GetNextPositionInTempList_TrainerEffects", 0x7E25u, adapt_GetNextPositionInTempList_TrainerEffects },
	{ "GustOfWind_BenchCheck", 0x7E6Eu, adapt_GustOfWind_BenchCheck },
	{ "PlayTrainerEffectAnimation", 0x7EA9u, adapt_PlayTrainerEffectAnimation },
};

EffectDispatchFn EffectDispatchLookupName(const char *name)
{
	for (uint16_t i = 0u; i < (uint16_t)(sizeof(kEffectDispatchEntries) / sizeof(kEffectDispatchEntries[0])); i++)
		if (strcmp(kEffectDispatchEntries[i].name, name) == 0)
			return kEffectDispatchEntries[i].function;
	return NULL;
}

EffectDispatchFn EffectDispatchLookupAddress(uint16_t address)
{
	uint16_t low = 0u;
	uint16_t high = (uint16_t)(sizeof(kEffectDispatchEntries) / sizeof(kEffectDispatchEntries[0]));
	while (low < high) {
		uint16_t middle = (uint16_t)(low + (uint16_t)((high - low) / 2u));
		if (kEffectDispatchEntries[middle].address < address)
			low = (uint16_t)(middle + 1u);
		else
			high = middle;
	}
	if (low < (uint16_t)(sizeof(kEffectDispatchEntries) / sizeof(kEffectDispatchEntries[0])) &&
	    kEffectDispatchEntries[low].address == address)
		return kEffectDispatchEntries[low].function;
	return NULL;
}
