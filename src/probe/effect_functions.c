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
/* >>> factory SetDefiniteDamage */
static void adapt_SetDefiniteDamage(ProbeState *s)
{
	SetDefiniteDamage(s->a);
}
/* <<< factory SetDefiniteDamage */


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
/* >>> factory SleepEffect */
static void adapt_SleepEffect(ProbeState *s)
{
	QueueStatusConditionResult r = SleepEffect();
	s->f = r.f;
}
/* <<< factory SleepEffect */


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
	ApplyExtraWaterEnergyDamageBonus(s->b, s->c);
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

/* >>> factory NidoranFFurySwipes_AIEffect */
static void adapt_NidoranFFurySwipes_AIEffect(ProbeState *s)
{
	(void)s;
	NidoranFFurySwipes_AIEffect();
}
/* <<< factory NidoranFFurySwipes_AIEffect */


/* >>> factory NidoranFCallForFamily_AISelectEffect */
static void adapt_NidoranFCallForFamily_AISelectEffect(ProbeState *s)
{
	NidoranFCallForFamily_AISelectEffect(s->c, (uint16_t)(s->d << 8 | s->e));
}
/* <<< factory NidoranFCallForFamily_AISelectEffect */


/* >>> factory ToxicGasEffect */
static void adapt_ToxicGasEffect(ProbeState *s)
{
	s->f = ToxicGasEffect(s->f);
}
/* <<< factory ToxicGasEffect */


/* >>> factory Sludge_AIEffect */
static void adapt_Sludge_AIEffect(ProbeState *s)
{
	Sludge_AIEffect();
	s->hl = wDamage_ADDR;
}
/* <<< factory Sludge_AIEffect */


/* >>> factory KadabraRecover_DiscardEffect */
static void adapt_KadabraRecover_DiscardEffect(ProbeState *s)
{
	s->a = KadabraRecover_DiscardEffect();
}
/* <<< factory KadabraRecover_DiscardEffect */

/* >>> factory PrimeapeFurySwipes_AIEffect */
static void adapt_PrimeapeFurySwipes_AIEffect(ProbeState *s)
{
	PrimeapeFurySwipesAIResult r = PrimeapeFurySwipes_AIEffect();
	s->a = r.a;
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
}
/* <<< factory PrimeapeFurySwipes_AIEffect */

/* >>> factory StretchKick_CheckBench */
static void adapt_StretchKick_CheckBench(ProbeState *s)
{
	StretchKickCheckBenchResult r = StretchKick_CheckBench();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory StretchKick_CheckBench */
/* >>> factory Cowardice_CheckUseAndBench */
static void adapt_Cowardice_CheckUseAndBench(ProbeState *s)
{
	CowardiceCheckUseAndBenchResult r = Cowardice_CheckUseAndBench();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Cowardice_CheckUseAndBench */



/* >>> factory Cowardice_ReturnToHandEffect */
static void adapt_Cowardice_ReturnToHandEffect(ProbeState *s)
{
	Cowardice_ReturnToHandEffect();
	s->a = gb_read8(wDuelDisplayedScreen_ADDR);
}
/* <<< factory Cowardice_ReturnToHandEffect */




/* >>> factory LightScreenEffect */
static void adapt_LightScreenEffect(ProbeState *s)
{
	s->hl = LightScreenEffect();
}
/* <<< factory LightScreenEffect */


/* >>> factory StarmieRecover_CheckEnergyHP */
static void adapt_StarmieRecover_CheckEnergyHP(ProbeState *s)
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
static void adapt_StarmieRecover_DiscardEffect(ProbeState *s)
{
	s->a = StarmieRecover_DiscardEffect();
}
/* <<< factory StarmieRecover_DiscardEffect */


/* >>> factory CheckIfCardHasGrassEnergyAttached */
static void adapt_CheckIfCardHasGrassEnergyAttached(ProbeState *s)
{
	CheckIfCardHasGrassEnergyAttachedResult r = CheckIfCardHasGrassEnergyAttached(s->a);
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CheckIfCardHasGrassEnergyAttached */

/* >>> factory GrimerMinimizeEffect */
static void adapt_GrimerMinimizeEffect(ProbeState *s)
{
	s->a = 0x13u;
	s->hl = GrimerMinimizeEffect();
}
/* <<< factory GrimerMinimizeEffect */

/* >>> factory Quickfreeze_InitialEffect */
static void adapt_Quickfreeze_InitialEffect(ProbeState *s)
{
	s->f = Quickfreeze_InitialEffect(s->f);
}
/* <<< factory Quickfreeze_InitialEffect */


/* >>> factory FocusEnergyEffect */
static void adapt_FocusEnergyEffect(ProbeState *s)
{
	FocusEnergyEffect();
}
/* <<< factory FocusEnergyEffect */


/* >>> factory MagnetonSonicboom_UnaffectedByColorEffect */
static void adapt_MagnetonSonicboom_UnaffectedByColorEffect(ProbeState *s)
{
	MagnetonSonicboom_UnaffectedByColorEffect();
}
/* <<< factory MagnetonSonicboom_UnaffectedByColorEffect */

/* >>> factory MagnetonSonicboom_NullEffect */
static void adapt_MagnetonSonicboom_NullEffect(ProbeState *s)
{
	MagnetonSonicboom_NullEffect();
}
/* <<< factory MagnetonSonicboom_NullEffect */

/* >>> factory ElectrodeSonicboom_UnaffectedByColorEffect */
static void adapt_ElectrodeSonicboom_UnaffectedByColorEffect(ProbeState *s)
{
	s->hl = ElectrodeSonicboom_UnaffectedByColorEffect();
}
/* <<< factory ElectrodeSonicboom_UnaffectedByColorEffect */

/* >>> factory EnergySpike_AISelectEffect */
static void adapt_EnergySpike_AISelectEffect(ProbeState *s)
{
	EnergySpike_AISelectEffect();
	s->a = 0xffu;
}
/* <<< factory EnergySpike_AISelectEffect */

/* >>> factory CometPunch_AIEffect */
static void adapt_CometPunch_AIEffect(ProbeState *s)
{
	CometPunch_AIEffect();
}
/* <<< factory CometPunch_AIEffect */

/* >>> factory Conversion1_WeaknessCheck */
static void adapt_Conversion1_WeaknessCheck(ProbeState *s)
{
	Conversion1WeaknessCheckResult result = Conversion1_WeaknessCheck();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Conversion1_WeaknessCheck */

/* >>> factory Conversion2_ResistanceCheck */
static void adapt_Conversion2_ResistanceCheck(ProbeState *s)
{
	Conversion2ResistanceCheckResult result = Conversion2_ResistanceCheck();
	s->a = result.a;
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Conversion2_ResistanceCheck */

/* >>> factory ElectrodeSonicboom_NullEffect */
static void adapt_ElectrodeSonicboom_NullEffect(ProbeState *s)
{
	ElectrodeSonicboom_NullEffect();
}
/* <<< factory ElectrodeSonicboom_NullEffect */

/* >>> factory FirstAid_DamageCheck */
static void adapt_FirstAid_DamageCheck(ProbeState *s)
{
	FirstAidDamageCheckResult r = FirstAid_DamageCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory FirstAid_DamageCheck */

/* >>> factory DoTheWaveEffect */
static void adapt_DoTheWaveEffect(ProbeState *s)
{
	DoTheWaveEffect();
}
/* <<< factory DoTheWaveEffect */

/* >>> factory FullHeal_StatusCheck */
static void adapt_FullHeal_StatusCheck(ProbeState *s)
{
	FullHealStatusCheckResult r = FullHeal_StatusCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FullHeal_StatusCheck */

/* >>> factory PoisonFang_AIEffect */
static void adapt_PoisonFang_AIEffect(ProbeState *s)
{
	(void)s;
	PoisonFang_AIEffect();
}
/* <<< factory PoisonFang_AIEffect */

/* >>> factory WeepinbellPoisonPowder_AIEffect */
static void adapt_WeepinbellPoisonPowder_AIEffect(ProbeState *s)
{
	(void)s;
	WeepinbellPoisonPowder_AIEffect();
}
/* <<< factory WeepinbellPoisonPowder_AIEffect */

/* >>> factory Toxic_AIEffect */
static void adapt_Toxic_AIEffect(ProbeState *s)
{
	(void)s;
	Toxic_AIEffect();
}
/* <<< factory Toxic_AIEffect */

/* >>> factory BoyfriendsEffect */
static void adapt_BoyfriendsEffect(ProbeState *s)
{
	(void)s;
	BoyfriendsEffect();
}
/* <<< factory BoyfriendsEffect */

/* >>> factory IvysaurPoisonPowder_AIEffect */
static void adapt_IvysaurPoisonPowder_AIEffect(ProbeState *s)
{
	(void)s;
	IvysaurPoisonPowder_AIEffect();
}
/* <<< factory IvysaurPoisonPowder_AIEffect */

/* >>> factory EnergyTrans_CheckPlayArea */
static void adapt_EnergyTrans_CheckPlayArea(ProbeState *s)
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
static void adapt_Firegiver_InitialEffect(ProbeState *s)
{
	s->f = Firegiver_InitialEffect(s->f);
}
/* <<< factory Firegiver_InitialEffect */


/* >>> factory MoltresLv37DiveBomb_AIEffect */
static void adapt_MoltresLv37DiveBomb_AIEffect(ProbeState *s)
{
	MoltresLv37DiveBomb_AIEffect();
}
/* <<< factory MoltresLv37DiveBomb_AIEffect */


/* >>> factory GetEnergyAttachedMultiplierDamage */
static void adapt_GetEnergyAttachedMultiplierDamage(ProbeState *s)
{
	uint16_t r = GetEnergyAttachedMultiplierDamage();
	s->d = (uint8_t)(r >> 8);
	s->e = (uint8_t)r;
}
/* <<< factory GetEnergyAttachedMultiplierDamage */

/* >>> factory Fly_AIEffect */
static void adapt_Fly_AIEffect(ProbeState *s)
{
	(void)s;
	Fly_AIEffect();
}
/* <<< factory Fly_AIEffect */
/* >>> factory Gigashock_AISelectEffect */
static void adapt_Gigashock_AISelectEffect(ProbeState *s)
{
	(void)s;
	Gigashock_AISelectEffect();
}
/* <<< factory Gigashock_AISelectEffect */

/* >>> factory Wildfire_DiscardDeckEffect */
static void adapt_Wildfire_DiscardDeckEffect(ProbeState *s)
{
	(void)s;
	Wildfire_DiscardDeckEffect();
}
/* <<< factory Wildfire_DiscardDeckEffect */

/* >>> factory MoltresLv35DiveBomb_AIEffect */
static void adapt_MoltresLv35DiveBomb_AIEffect(ProbeState *s)
{
	(void)s;
	MoltresLv35DiveBomb_AIEffect();
}
/* <<< factory MoltresLv35DiveBomb_AIEffect */

/* >>> factory ClefairyDoll_BenchCheck */
static void adapt_ClefairyDoll_BenchCheck(ProbeState *s)
{
	ClefairyDollBenchCheckResult r = ClefairyDoll_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ClefairyDoll_BenchCheck */

/* >>> factory ClefairyDoll_PlaceInPlayAreaEffect */
static void adapt_ClefairyDoll_PlaceInPlayAreaEffect(ProbeState *s)
{
	ClefairyDoll_PlaceInPlayAreaEffect();
}
/* <<< factory ClefairyDoll_PlaceInPlayAreaEffect */

/* >>> factory EnergyBurnCheck_Unreferenced */
static void adapt_EnergyBurnCheck_Unreferenced(ProbeState *s)
{
    EnergyBurnCheckResult r = EnergyBurnCheck_Unreferenced();
    s->a = r.a;
    s->f = r.f;
}
/* <<< factory EnergyBurnCheck_Unreferenced */

/* >>> factory FlareonRage_DamageBoostEffect */
static void adapt_FlareonRage_DamageBoostEffect(ProbeState *s)
{
    (void)s;
    FlareonRage_DamageBoostEffect();
}
/* <<< factory FlareonRage_DamageBoostEffect */

/* >>> factory Shift_OncePerTurnCheck */
static void adapt_Shift_OncePerTurnCheck(ProbeState *s)
{
	ShiftOncePerTurnCheckResult r = Shift_OncePerTurnCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Shift_OncePerTurnCheck */

/* >>> factory VenomPowder_AIEffect */
static void adapt_VenomPowder_AIEffect(ProbeState *s)
{
	(void)s;
	VenomPowder_AIEffect();
}
/* <<< factory VenomPowder_AIEffect */

/* >>> factory TangelaPoisonPowder_AIEffect */
static void adapt_TangelaPoisonPowder_AIEffect(ProbeState *s)
{
	(void)s;
	TangelaPoisonPowder_AIEffect();
}
/* <<< factory TangelaPoisonPowder_AIEffect */

/* >>> factory PetalDance_AIEffect */
static void adapt_PetalDance_AIEffect(ProbeState *s)
{
	(void)s;
	PetalDance_AIEffect();
}
/* <<< factory PetalDance_AIEffect */

/* >>> factory RainDanceEffect */
static void adapt_RainDanceEffect(ProbeState *s)
{
	s->f = RainDanceEffect(s->f);
}
/* <<< factory RainDanceEffect */

/* >>> factory PsyduckFurySwipes_AIEffect */
static void adapt_PsyduckFurySwipes_AIEffect(ProbeState *s)
{
	(void)s;
	PsyduckFurySwipes_AIEffect();
}
/* <<< factory PsyduckFurySwipes_AIEffect */

/* >>> factory VaporeonQuickAttack_AIEffect */
static void adapt_VaporeonQuickAttack_AIEffect(ProbeState *s)
{
	(void)s;
	VaporeonQuickAttack_AIEffect();
}
/* <<< factory VaporeonQuickAttack_AIEffect */

/* >>> factory JellyfishSting_AIEffect */
static void adapt_JellyfishSting_AIEffect(ProbeState *s)
{
	(void)s;
	JellyfishSting_AIEffect();
}
/* <<< factory JellyfishSting_AIEffect */

/* >>> factory PoliwhirlAmnesia_CheckAttacks */
static void adapt_PoliwhirlAmnesia_CheckAttacks(ProbeState *s)
{
	PoliwhirlAmnesiaCheckAttacksResult r = PoliwhirlAmnesia_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PoliwhirlAmnesia_CheckAttacks */

/* >>> factory HeadacheEffect */
static void adapt_HeadacheEffect(ProbeState *s)
{
	(void)s;
	HeadacheEffect();
}
/* <<< factory HeadacheEffect */

/* >>> factory ArcanineQuickAttack_AIEffect */
static void adapt_ArcanineQuickAttack_AIEffect(ProbeState *s)
{
	(void)s;
	ArcanineQuickAttack_AIEffect();
}
/* <<< factory ArcanineQuickAttack_AIEffect */

/* >>> factory FlamesOfRage_CheckEnergy */
static void adapt_FlamesOfRage_CheckEnergy(ProbeState *s)
{
	FlamesOfRageCheckEnergyResult r = FlamesOfRage_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FlamesOfRage_CheckEnergy */

/* >>> factory MagmarFlamethrower_DiscardEffect */
static void adapt_MagmarFlamethrower_DiscardEffect(ProbeState *s)
{
	s->a = MagmarFlamethrower_DiscardEffect();
}
/* <<< factory MagmarFlamethrower_DiscardEffect */

/* >>> factory MagmarSmog_AIEffect */
static void adapt_MagmarSmog_AIEffect(ProbeState *s)
{
	(void)s;
	MagmarSmog_AIEffect();
}
/* <<< factory MagmarSmog_AIEffect */

/* >>> factory Wildfire_CheckEnergy */
static void adapt_Wildfire_CheckEnergy(ProbeState *s)
{
	WildfireCheckEnergyResult r = Wildfire_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory Wildfire_CheckEnergy */

/* >>> factory MrMimeMeditate_DamageBoostEffect */
static void adapt_MrMimeMeditate_DamageBoostEffect(ProbeState *s)
{
	(void)s;
	MrMimeMeditate_DamageBoostEffect();
}
/* <<< factory MrMimeMeditate_DamageBoostEffect */

/* >>> factory DancingEmbers_AIEffect */
static void adapt_DancingEmbers_AIEffect(ProbeState *s)
{
	(void)s;
	DancingEmbers_AIEffect();
}
/* <<< factory DancingEmbers_AIEffect */

/* >>> factory FlareonFlamethrower_DiscardEffect */
static void adapt_FlareonFlamethrower_DiscardEffect(ProbeState *s)
{
	s->a = FlareonFlamethrower_DiscardEffect();
}
/* <<< factory FlareonFlamethrower_DiscardEffect */

/* >>> factory MagmarFlamethrower_CheckEnergy */
static void adapt_MagmarFlamethrower_CheckEnergy(ProbeState *s)
{
	MagmarFlamethrowerCheckEnergyResult r = MagmarFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MagmarFlamethrower_CheckEnergy */

/* >>> factory FlamesOfRage_DiscardEffect */
static void adapt_FlamesOfRage_DiscardEffect(ProbeState *s)
{
	(void)s;
	FlamesOfRage_DiscardEffect();
}
/* <<< factory FlamesOfRage_DiscardEffect */

/* >>> factory FlamesOfRage_DamageBoostEffect */
static void adapt_FlamesOfRage_DamageBoostEffect(ProbeState *s)
{
	(void)s;
	FlamesOfRage_DamageBoostEffect();
}
/* <<< factory FlamesOfRage_DamageBoostEffect */

/* >>> factory CharmeleonFlamethrower_CheckEnergy */
static void adapt_CharmeleonFlamethrower_CheckEnergy(ProbeState *s)
{
	CharmeleonFlamethrowerCheckEnergyResult r = CharmeleonFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory CharmeleonFlamethrower_CheckEnergy */

/* >>> factory CharmeleonFlamethrower_DiscardEffect */
static void adapt_CharmeleonFlamethrower_DiscardEffect(ProbeState *s)
{
	s->a = CharmeleonFlamethrower_DiscardEffect();
}
/* <<< factory CharmeleonFlamethrower_DiscardEffect */

/* >>> factory EnergyBurnEffect */
static void adapt_EnergyBurnEffect(ProbeState *s)
{
	EnergyBurnEffectResult r = EnergyBurnEffect(s->f);
	s->f = r.f;
}
/* <<< factory EnergyBurnEffect */

/* >>> factory FireSpin_CheckEnergy */
static void adapt_FireSpin_CheckEnergy(ProbeState *s)
{
	FireSpinCheckEnergyResult r = FireSpin_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory FireSpin_CheckEnergy */

/* >>> factory FlareonQuickAttack_AIEffect */
static void adapt_FlareonQuickAttack_AIEffect(ProbeState *s)
{
	(void)s;
	FlareonQuickAttack_AIEffect();
}
/* <<< factory FlareonQuickAttack_AIEffect */

/* >>> factory FlareonFlamethrower_CheckEnergy */
static void adapt_FlareonFlamethrower_CheckEnergy(ProbeState *s)
{
	FlareonFlamethrowerCheckEnergyResult r = FlareonFlamethrower_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory FlareonFlamethrower_CheckEnergy */

/* >>> factory Prophecy_AISelectEffect */
static void adapt_Prophecy_AISelectEffect(ProbeState *s)
{
	ProphecyAISelectEffectResult r = Prophecy_AISelectEffect();
	s->a = r.a;
}
/* <<< factory Prophecy_AISelectEffect */

/* >>> factory Prophecy_ReorderDeckEffect */
static void adapt_Prophecy_ReorderDeckEffect(ProbeState *s)
{
	ProphecyReorderDeckEffectResult r = Prophecy_ReorderDeckEffect();
	s->a = r.a;
	s->c = r.c;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Prophecy_ReorderDeckEffect */

/* >>> factory SuperEnergyRetrieval_HandEnergyCheck */
static void adapt_SuperEnergyRetrieval_HandEnergyCheck(ProbeState *s)
{
	SuperEnergyRetrievalHandEnergyCheckResult r =
		SuperEnergyRetrieval_HandEnergyCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory SuperEnergyRetrieval_HandEnergyCheck */

/* >>> factory GetNextPositionInTempList_TrainerEffects */
static void adapt_GetNextPositionInTempList_TrainerEffects(ProbeState *s)
{
	s->hl = GetNextPositionInTempList_TrainerEffects();
}
/* <<< factory GetNextPositionInTempList_TrainerEffects */

/* >>> factory NinetalesLure_AISelectEffect */
static void adapt_NinetalesLure_AISelectEffect(ProbeState *s)
{
	s->a = NinetalesLure_AISelectEffect();
}
/* <<< factory NinetalesLure_AISelectEffect */

/* >>> factory Ember_CheckEnergy */
static void adapt_Ember_CheckEnergy(ProbeState *s)
{
	EmberCheckEnergyResult r = Ember_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Ember_CheckEnergy */

/* >>> factory DestinyBond_CheckEnergy */
static void adapt_DestinyBond_CheckEnergy(ProbeState *s)
{
	IsPlayerTurnResult r = DestinyBond_CheckEnergy();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DestinyBond_CheckEnergy */

/* >>> factory ComputerSearch_HandDeckCheck */
static void adapt_ComputerSearch_HandDeckCheck(ProbeState *s)
{
	ComputerSearchHandDeckCheckResult r = ComputerSearch_HandDeckCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ComputerSearch_HandDeckCheck */

/* >>> factory MrFuji_BenchCheck */
static void adapt_MrFuji_BenchCheck(ProbeState *s)
{
	MrFujiBenchCheckResult r = MrFuji_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MrFuji_BenchCheck */

/* >>> factory DreamEaterEffect */
static void adapt_DreamEaterEffect(ProbeState *s)
{
	DreamEaterEffectResult r = DreamEaterEffect();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DreamEaterEffect */

/* >>> factory JynxMeditate_DamageBoostEffect */
static void adapt_JynxMeditate_DamageBoostEffect(ProbeState *s)
{
	JynxMeditate_DamageBoostEffect();
}
/* <<< factory JynxMeditate_DamageBoostEffect */
/* >>> factory KadabraRecover_CheckEnergyHP */
static void adapt_KadabraRecover_CheckEnergyHP(ProbeState *s)
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
static void adapt_MewtwoAltEnergyAbsorption_AddToHandEffect(ProbeState *s)
{
	MewtwoAltEnergyAbsorption_AddToHandEffect();
}
/* <<< factory MewtwoAltEnergyAbsorption_AddToHandEffect */
/* >>> factory MewtwoEnergyAbsorption_AddToHandEffect */
static void adapt_MewtwoEnergyAbsorption_AddToHandEffect(ProbeState *s)
{
	MewtwoEnergyAbsorption_AddToHandEffect();
}
/* <<< factory MewtwoEnergyAbsorption_AddToHandEffect */
/* >>> factory NeutralizingShieldEffect */
static void adapt_NeutralizingShieldEffect(ProbeState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | NeutralizingShieldEffect());
}
/* <<< factory NeutralizingShieldEffect */
/* >>> factory PealOfThunder_InitialEffect */
static void adapt_PealOfThunder_InitialEffect(ProbeState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | PealOfThunder_InitialEffect());
}
/* <<< factory PealOfThunder_InitialEffect */
/* >>> factory PrehistoricPowerEffect */
static void adapt_PrehistoricPowerEffect(ProbeState *s)
{
	s->f = (uint8_t)((s->f & 0x80u) | PrehistoricPowerEffect());
}
/* <<< factory PrehistoricPowerEffect */
/* >>> factory Scavenge_DiscardEffect */
static void adapt_Scavenge_DiscardEffect(ProbeState *s)
{
	s->a = Scavenge_DiscardEffect();
}
/* <<< factory Scavenge_DiscardEffect */

/* >>> factory StepIn_BenchCheck */
static void adapt_StepIn_BenchCheck(ProbeState *s) { SolarPowerCheckUseResult r = StepIn_BenchCheck(); s->f = r.f; s->hl = r.hl; }
/* <<< factory StepIn_BenchCheck */
/* >>> factory Peek_OncePerTurnCheck */
static void adapt_Peek_OncePerTurnCheck(ProbeState *s)
{
	SolarPowerCheckUseResult r = Peek_OncePerTurnCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Peek_OncePerTurnCheck */
/* >>> factory Wail_BenchCheck */
static void adapt_Wail_BenchCheck(ProbeState *s)
{
	MrFujiBenchCheckResult r = Wail_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Wail_BenchCheck */
/* >>> factory StepIn_SwitchEffect */
static void adapt_StepIn_SwitchEffect(ProbeState *s) { StepIn_SwitchEffect(); }
/* <<< factory StepIn_SwitchEffect */
/* >>> factory ThickSkinnedEffect */
static void adapt_ThickSkinnedEffect(ProbeState *s) { s->f = ThickSkinnedEffect(s->f); }
/* <<< factory ThickSkinnedEffect */
/* >>> factory HealingWind_InitialEffect */
static void adapt_HealingWind_InitialEffect(ProbeState *s) { s->f = HealingWind_InitialEffect(s->f); }
/* <<< factory HealingWind_InitialEffect */
/* >>> factory PickRandomBasicCardFromDeck */
static void adapt_PickRandomBasicCardFromDeck(ProbeState *s) { s->a = PickRandomBasicCardFromDeck(); s->f = s->a == 0xFFu ? 0x90u : (s->a == 0u ? 0x80u : 0u); }
/* <<< factory PickRandomBasicCardFromDeck */

/* >>> factory GustOfWind_BenchCheck */
static void adapt_GustOfWind_BenchCheck(ProbeState *s)
{
	IsPlayerTurnResult r = GustOfWind_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory GustOfWind_BenchCheck */

/* >>> factory DrawSymbolOnPlayAreaCursor */
static void adapt_DrawSymbolOnPlayAreaCursor(ProbeState *s)
{
	DrawSymbolOnPlayAreaCursor(s->a, s->b);
}
/* <<< factory DrawSymbolOnPlayAreaCursor */
/* >>> factory Func_2c6d9 */
static void adapt_Func_2c6d9(ProbeState *s)
{
	WaitResult r = Func_2c6d9();
	s->f = r.f;
}
/* <<< factory Func_2c6d9 */


/* >>> factory MarowakCallForFamily_AISelectEffect */
static void adapt_MarowakCallForFamily_AISelectEffect(ProbeState *s)
{
	MarowakCallForFamily_AISelectEffect();
}
/* <<< factory MarowakCallForFamily_AISelectEffect */

/* >>> factory CreateListOfFireEnergyAttachedToArena */
static void adapt_CreateListOfFireEnergyAttachedToArena(ProbeState *s)
{
	CreateListOfEnergyAttachedToArenaResult r = CreateListOfFireEnergyAttachedToArena();
	s->a = r.a;
	s->c = r.c;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateListOfFireEnergyAttachedToArena */
/* >>> factory CreateEnergyCardListFromDiscardPile_AllEnergy */
static void adapt_CreateEnergyCardListFromDiscardPile_AllEnergy(ProbeState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = CreateEnergyCardListFromDiscardPile_AllEnergy();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CreateEnergyCardListFromDiscardPile_AllEnergy */
/* >>> factory CheckIfDeckIsEmpty */
static void adapt_CheckIfDeckIsEmpty(ProbeState *s)
{
	CheckIfDeckIsEmptyResult r = CheckIfDeckIsEmpty();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory CheckIfDeckIsEmpty */
/* >>> factory VictreebelLure_AssertPokemonInBench */
static void adapt_VictreebelLure_AssertPokemonInBench(ProbeState *s)
{
	VictreebelLureAssertPokemonInBenchResult r = VictreebelLure_AssertPokemonInBench();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory VictreebelLure_AssertPokemonInBench */
/* >>> factory NinetalesLure_CheckBench */
static void adapt_NinetalesLure_CheckBench(ProbeState *s)
{
	NinetalesLureCheckBenchResult r = NinetalesLure_CheckBench();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory NinetalesLure_CheckBench */
/* >>> factory ThunderboltEffect */
static void adapt_ThunderboltEffect(ProbeState *s)
{
	ThunderboltEffect();
}
/* <<< factory ThunderboltEffect */
/* >>> factory TrainerCardAsPokemon_BenchCheck */
static void adapt_TrainerCardAsPokemon_BenchCheck(ProbeState *s)
{
	TrainerCardAsPokemonBenchCheckResult r = TrainerCardAsPokemon_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory TrainerCardAsPokemon_BenchCheck */
/* >>> factory TrainerCardAsPokemon_DiscardEffect */
static void adapt_TrainerCardAsPokemon_DiscardEffect(ProbeState *s)
{
	TrainerCardAsPokemon_DiscardEffect();
}
/* <<< factory TrainerCardAsPokemon_DiscardEffect */
/* >>> factory MysteriousFossil_BenchCheck */
static void adapt_MysteriousFossil_BenchCheck(ProbeState *s)
{
	MysteriousFossilBenchCheckResult r = MysteriousFossil_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MysteriousFossil_BenchCheck */
/* >>> factory MysteriousFossil_PlaceInPlayAreaEffect */
static void adapt_MysteriousFossil_PlaceInPlayAreaEffect(ProbeState *s)
{
	MysteriousFossil_PlaceInPlayAreaEffect();
}
/* <<< factory MysteriousFossil_PlaceInPlayAreaEffect */
/* >>> factory ScoopUp_BenchCheck */
static void adapt_ScoopUp_BenchCheck(ProbeState *s)
{
	ScoopUpBenchCheckResult r = ScoopUp_BenchCheck();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ScoopUp_BenchCheck */
/* >>> factory Toxic_DoublePoisonEffect */
static void adapt_Toxic_DoublePoisonEffect(ProbeState *s)
{
	QueueStatusConditionResult r = Toxic_DoublePoisonEffect();
	s->f = r.f;
}
/* <<< factory Toxic_DoublePoisonEffect */

/* >>> factory TryGiveDamageCounter_StrangeBehavior */
static void adapt_TryGiveDamageCounter_StrangeBehavior(ProbeState *s)
{
	TryGiveDamageCounter_StrangeBehaviorResult r =
		TryGiveDamageCounter_StrangeBehavior();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory TryGiveDamageCounter_StrangeBehavior */
/* >>> factory SpacingOut_CheckDamage */
static void adapt_SpacingOut_CheckDamage(ProbeState *s)
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
static void adapt_SpacingOut_HealEffect(ProbeState *s)
{
	SpacingOutHealEffectResult r = SpacingOut_HealEffect();
	s->a = r.a;
	s->f = r.f;
	if (r.update_hl)
		s->hl = r.hl;
}
/* <<< factory SpacingOut_HealEffect */

/* >>> factory LeekSlap_OncePerDuelCheck */
static void adapt_LeekSlap_OncePerDuelCheck(ProbeState *s) { s->f = (uint8_t)(LeekSlap_OncePerDuelCheck() | (s->f & 0x00u)); }
/* <<< factory LeekSlap_OncePerDuelCheck */
/* >>> factory LeekSlap_SetUsedThisDuelFlag */
static void adapt_LeekSlap_SetUsedThisDuelFlag(ProbeState *s) { LeekSlap_SetUsedThisDuelFlag(); }
/* <<< factory LeekSlap_SetUsedThisDuelFlag */
/* >>> factory PlusPowerEffect */
static void adapt_PlusPowerEffect(ProbeState *s) { PlusPowerEffect(); }
/* <<< factory PlusPowerEffect */
/* >>> factory StrikesBackEffect */
static void adapt_StrikesBackEffect(ProbeState *s) { s->f = (uint8_t)((s->f & 0x80u) | StrikesBackEffect()); }
/* <<< factory StrikesBackEffect */
/* >>> factory Switch_BenchCheck */
static void adapt_Switch_BenchCheck(ProbeState *s) { MrFujiBenchCheckResult r = Switch_BenchCheck(); s->a = r.a; s->f = r.f; s->hl = r.hl; }
/* <<< factory Switch_BenchCheck */
/* >>> factory Switch_SwitchEffect */
static void adapt_Switch_SwitchEffect(ProbeState *s) { Switch_SwitchEffect(); }
/* <<< factory Switch_SwitchEffect */

/* >>> factory CopyPlayAreaHPToBackup_Unreferenced */
static void adapt_CopyPlayAreaHPToBackup_Unreferenced(ProbeState *s) { (void)s; CopyPlayAreaHPToBackup_Unreferenced(); }
/* <<< factory CopyPlayAreaHPToBackup_Unreferenced */
/* >>> factory CopyPlayAreaHPFromBackup_Unreferenced */
static void adapt_CopyPlayAreaHPFromBackup_Unreferenced(ProbeState *s) { (void)s; CopyPlayAreaHPFromBackup_Unreferenced(); }
/* <<< factory CopyPlayAreaHPFromBackup_Unreferenced */
/* >>> factory Gale_LoadAnimation */
static void adapt_Gale_LoadAnimation(ProbeState *s) { (void)s; Gale_LoadAnimation(); }
/* <<< factory Gale_LoadAnimation */
/* >>> factory EnergySearch_DeckCheck */
static void adapt_EnergySearch_DeckCheck(ProbeState *s) { s->f = EnergySearch_DeckCheck(); }
/* <<< factory EnergySearch_DeckCheck */
/* >>> factory CheckIfCardIsBasicEnergy */
static void adapt_CheckIfCardIsBasicEnergy(ProbeState *s) { s->f = CheckIfCardIsBasicEnergy(s->a); }
/* <<< factory CheckIfCardIsBasicEnergy */
/* >>> factory CreatePlayableStage2PokemonCardListFromHand */
static void adapt_CreatePlayableStage2PokemonCardListFromHand(ProbeState *s) { s->f = (uint8_t)((s->f & 0x80u) | CreatePlayableStage2PokemonCardListFromHand()); }
/* <<< factory CreatePlayableStage2PokemonCardListFromHand */
/* >>> factory Barrier_DiscardEffect */
static void adapt_Barrier_DiscardEffect(ProbeState *s)
{
	s->a = Barrier_DiscardEffect();
}
/* <<< factory Barrier_DiscardEffect */

/* >>> factory DestinyBond_DiscardEffect */
static void adapt_DestinyBond_DiscardEffect(ProbeState *s) { DestinyBond_DiscardEffect(); }
/* <<< factory DestinyBond_DiscardEffect */
static void adapt_Ember_DiscardEffect(ProbeState *s) { Ember_DiscardEffect(); }
/* <<< factory Ember_DiscardEffect */
/* >>> factory FireBlast_DiscardEffect */
static void adapt_FireBlast_DiscardEffect(ProbeState *s) { FireBlast_DiscardEffect(); }
/* <<< factory FireBlast_DiscardEffect */
/* >>> factory FireSpin_AISelectEffect */
static void adapt_FireSpin_AISelectEffect(ProbeState *s) { FireSpin_AISelectEffect(); }
/* <<< factory FireSpin_AISelectEffect */
/* >>> factory FireSpin_DiscardEffect */
static void adapt_FireSpin_DiscardEffect(ProbeState *s) { FireSpin_DiscardEffect(); }
/* <<< factory FireSpin_DiscardEffect */
/* >>> factory PidgeottoMirrorMove_InitialEffect1 */
static void adapt_PidgeottoMirrorMove_InitialEffect1(ProbeState *s)
{
	MirrorMoveInitialEffect1Result r = PidgeottoMirrorMove_InitialEffect1();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PidgeottoMirrorMove_InitialEffect1 */

/* >>> factory ClefairyMetronome_CheckAttacks */
static void adapt_ClefairyMetronome_CheckAttacks(ProbeState *s)
{
	ClefairyMetronomeCheckAttacksResult r = ClefairyMetronome_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ClefairyMetronome_CheckAttacks */

/* >>> factory Psychic_DamageBoostEffect */
static void adapt_Psychic_DamageBoostEffect(ProbeState *s)
{
	Psychic_DamageBoostEffect();
}
/* <<< factory Psychic_DamageBoostEffect */

/* >>> factory Barrier_AISelectEffect */
static void adapt_Barrier_AISelectEffect(ProbeState *s)
{
	Barrier_AISelectEffect();
}
/* <<< factory Barrier_AISelectEffect */

/* >>> factory Whirlpool_AISelectEffect */
static void adapt_Whirlpool_AISelectEffect(ProbeState *s)
{
	s->a = Whirlpool_AISelectEffect();
}
/* <<< factory Whirlpool_AISelectEffect */

/* >>> factory Whirlpool_DiscardEffect */
static void adapt_Whirlpool_DiscardEffect(ProbeState *s)
{
	s->hl = Whirlpool_DiscardEffect(s->hl);
}
/* <<< factory Whirlpool_DiscardEffect */

/* >>> factory EnergyRemoval_EnergyCheck */
static void adapt_EnergyRemoval_EnergyCheck(ProbeState *s)
{
	EnergyRemovalEnergyCheckResult r = EnergyRemoval_EnergyCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory EnergyRemoval_EnergyCheck */

/* >>> factory EnergyRemoval_AISelection */
static void adapt_EnergyRemoval_AISelection(ProbeState *s)
{
	s->a = EnergyRemoval_AISelection();
}
/* <<< factory EnergyRemoval_AISelection */

/* >>> factory EnergyRetrieval_HandEnergyCheck */
static void adapt_EnergyRetrieval_HandEnergyCheck(ProbeState *s)
{
	EnergyRetrievalHandEnergyCheckResult r = EnergyRetrieval_HandEnergyCheck();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory EnergyRetrieval_HandEnergyCheck */

/* >>> factory MrMimeMeditate_AIEffect */
static void adapt_MrMimeMeditate_AIEffect(ProbeState *s)
{
	MrMimeMeditate_AIEffect();
}
/* <<< factory MrMimeMeditate_AIEffect */

/* >>> factory PsywaveEffect */
static void adapt_PsywaveEffect(ProbeState *s)
{
	s->hl = PsywaveEffect();
}
/* <<< factory PsywaveEffect */

/* >>> factory PokemonCenter_DamageCheck */
static void adapt_PokemonCenter_DamageCheck(ProbeState *s)
{
	PokemonCenterDamageCheckResult r = PokemonCenter_DamageCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokemonCenter_DamageCheck */

/* >>> factory PokemonBreeder_HandPlayAreaCheck */
static void adapt_PokemonBreeder_HandPlayAreaCheck(ProbeState *s)
{
	PokemonBreederHandPlayAreaCheckResult r = PokemonBreeder_HandPlayAreaCheck(s->hl);
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokemonBreeder_HandPlayAreaCheck */

/* >>> factory PokemonTrader_HandDeckCheck */
static void adapt_PokemonTrader_HandDeckCheck(ProbeState *s)
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
static void adapt_VictreebelLure_GetBenchPokemonWithLowestHP(ProbeState *s)
{
	VictreebelLure_GetBenchPokemonWithLowestHP();
}
/* <<< factory VictreebelLure_GetBenchPokemonWithLowestHP */

/* >>> factory Sprout_CheckDeckAndPlayArea */
static void adapt_Sprout_CheckDeckAndPlayArea(ProbeState *s)
{
	CheckIfDeckIsEmptyResult r = Sprout_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory Sprout_CheckDeckAndPlayArea */

/* >>> factory NidoranFCallForFamily_CheckDeckAndPlayArea */
static void adapt_NidoranFCallForFamily_CheckDeckAndPlayArea(ProbeState *s)
{
	CheckIfDeckIsEmptyResult r = NidoranFCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory NidoranFCallForFamily_CheckDeckAndPlayArea */

/* >>> factory DragonairHyperBeam_AISelectEffect */
static void adapt_DragonairHyperBeam_AISelectEffect(ProbeState *s)
{
	(void)s;
	DragonairHyperBeam_AISelectEffect();
}
/* <<< factory DragonairHyperBeam_AISelectEffect */

/* >>> factory ClefableMetronome_CheckAttacks */
static void adapt_ClefableMetronome_CheckAttacks(ProbeState *s)
{
	ClefableMetronomeCheckAttacksResult r = ClefableMetronome_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory ClefableMetronome_CheckAttacks */

/* >>> factory Scavenge_CheckDiscardPile */
static void adapt_Scavenge_CheckDiscardPile(ProbeState *s)
{
	ScavengeCheckDiscardPileResult r = Scavenge_CheckDiscardPile();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory Scavenge_CheckDiscardPile */

/* >>> factory Scavenge_AISelectEffect */
static void adapt_Scavenge_AISelectEffect(ProbeState *s)
{
	Scavenge_AISelectEffect();
}
/* <<< factory Scavenge_AISelectEffect */

/* >>> factory SlowpokeAmnesia_CheckAttacks */
static void adapt_SlowpokeAmnesia_CheckAttacks(ProbeState *s)
{
	SlowpokeAmnesiaCheckAttacksResult r = SlowpokeAmnesia_CheckAttacks();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SlowpokeAmnesia_CheckAttacks */

/* >>> factory DevolutionBeam_CheckPlayArea */
static void adapt_DevolutionBeam_CheckPlayArea(ProbeState *s)
{
	DevolutionBeamCheckPlayAreaResult r = DevolutionBeam_CheckPlayArea();
	s->f = r.f;
	s->d = r.d;
	s->e = r.e;
	s->hl = r.hl;
}
/* <<< factory DevolutionBeam_CheckPlayArea */

/* >>> factory DevolutionBeam_AISelectEffect */
static void adapt_DevolutionBeam_AISelectEffect(ProbeState *s)
{
	DevolutionBeam_AISelectEffect();
}
/* <<< factory DevolutionBeam_AISelectEffect */

/* >>> factory MewtwoAltEnergyAbsorption_CheckDiscardPile */
static void adapt_MewtwoAltEnergyAbsorption_CheckDiscardPile(ProbeState *s)
{
	CreateEnergyCardListFromDiscardPileResult r = MewtwoAltEnergyAbsorption_CheckDiscardPile();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory MewtwoAltEnergyAbsorption_CheckDiscardPile */

/* >>> factory MewtwoAltEnergyAbsorption_AISelectEffect */
static void adapt_MewtwoAltEnergyAbsorption_AISelectEffect(ProbeState *s)
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
static void adapt_MewtwoEnergyAbsorption_CheckDiscardPile(ProbeState *s)
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
static void adapt_MewtwoEnergyAbsorption_AISelectEffect(ProbeState *s)
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
static void adapt_JynxMeditate_AIEffect(ProbeState *s)
{
	JynxMeditate_AIEffect();
}
/* <<< factory JynxMeditate_AIEffect */

/* >>> factory MysteryAttack_RandomEffect */
static void adapt_MysteryAttack_RandomEffect(ProbeState *s)
{
	MysteryAttack_RandomEffect();
}
/* <<< factory MysteryAttack_RandomEffect */

/* >>> factory MarowakCallForFamily_CheckDeckAndPlayArea */
static void adapt_MarowakCallForFamily_CheckDeckAndPlayArea(ProbeState *s)
{
	CheckIfDeckIsEmptyResult r = MarowakCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory MarowakCallForFamily_CheckDeckAndPlayArea */

/* >>> factory IceBreath_ZeroDamage */
static void adapt_IceBreath_ZeroDamage(ProbeState *s)
{
	s->a = IceBreath_ZeroDamage();
}
/* <<< factory IceBreath_ZeroDamage */

/* >>> factory AIPickFireEnergyCardToDiscard */
static void adapt_AIPickFireEnergyCardToDiscard(ProbeState *s)
{
	(void)s;
	AIPickFireEnergyCardToDiscard();
}
/* <<< factory AIPickFireEnergyCardToDiscard */

/* >>> factory FlamesOfRage_AIEffect */
static void adapt_FlamesOfRage_AIEffect(ProbeState *s)
{
	(void)s;
	FlamesOfRage_AIEffect();
}
/* <<< factory FlamesOfRage_AIEffect */

/* >>> factory ArcanineFlamethrower_AISelectEffect */
static void adapt_ArcanineFlamethrower_AISelectEffect(ProbeState *s)
{
	ArcanineFlamethrower_AISelectEffect();
}
/* <<< factory ArcanineFlamethrower_AISelectEffect */

/* >>> factory FlamesOfRage_AISelectEffect */
static void adapt_FlamesOfRage_AISelectEffect(ProbeState *s)
{
	FlamesOfRage_AISelectEffect();
}
/* <<< factory FlamesOfRage_AISelectEffect */

/* >>> factory FireBlast_AISelectEffect */
static void adapt_FireBlast_AISelectEffect(ProbeState *s)
{
	FireBlast_AISelectEffect();
}
/* <<< factory FireBlast_AISelectEffect */

/* >>> factory EnergyConversion_CheckEnergy */
static void adapt_EnergyConversion_CheckEnergy(ProbeState *s)
{
	EnergyConversionCheckEnergyResult r = EnergyConversion_CheckEnergy();
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory EnergyConversion_CheckEnergy */

/* >>> factory EnergyConversion_AISelectEffect */
static void adapt_EnergyConversion_AISelectEffect(ProbeState *s)
{
	EnergyConversion_AISelectEffect();
}
/* <<< factory EnergyConversion_AISelectEffect */

/* >>> factory HypnoDarkMind_AISelectEffect */
static void adapt_HypnoDarkMind_AISelectEffect(ProbeState *s)
{
	HypnoDarkMind_AISelectEffect();
}
/* <<< factory HypnoDarkMind_AISelectEffect */

/* >>> factory AIPickAttackForAmnesia */
static void adapt_AIPickAttackForAmnesia(ProbeState *s)
{
	s->a = AIPickAttackForAmnesia();
}
/* <<< factory AIPickAttackForAmnesia */

/* >>> factory MirrorMove_AISelection */
static void adapt_MirrorMove_AISelection(ProbeState *s)
{
	(void)s;
	MirrorMove_AISelection();
}
/* <<< factory MirrorMove_AISelection */

/* >>> factory KinglerFlail_HPCheck */
static void adapt_KinglerFlail_HPCheck(ProbeState *s)
{
	KinglerFlail_HPCheck();
}
/* <<< factory KinglerFlail_HPCheck */

/* >>> factory MagikarpFlail_HPCheck */
static void adapt_MagikarpFlail_HPCheck(ProbeState *s)
{
	MagikarpFlail_HPCheck();
}
/* <<< factory MagikarpFlail_HPCheck */

/* >>> factory SuperFang_HalfHPEffect */
static void adapt_SuperFang_HalfHPEffect(ProbeState *s)
{
	SuperFang_HalfHPEffect();
}
/* <<< factory SuperFang_HalfHPEffect */

/* >>> factory KarateChop_DamageSubtractionEffect */
static void adapt_KarateChop_DamageSubtractionEffect(ProbeState *s)
{
	(void)s;
	KarateChop_DamageSubtractionEffect();
}
/* <<< factory KarateChop_DamageSubtractionEffect */

/* >>> factory SpearowMirrorMove_AISelection */
static void adapt_SpearowMirrorMove_AISelection(ProbeState *s)
{
	(void)s;
	SpearowMirrorMove_AISelection();
}
/* <<< factory SpearowMirrorMove_AISelection */

/* >>> factory CharmeleonFlamethrower_AISelectEffect */
static void adapt_CharmeleonFlamethrower_AISelectEffect(ProbeState *s)
{
	(void)s;
	CharmeleonFlamethrower_AISelectEffect();
}
/* <<< factory CharmeleonFlamethrower_AISelectEffect */

/* >>> factory ClefableMetronome_AISelectEffect */
static void adapt_ClefableMetronome_AISelectEffect(ProbeState *s)
{
	(void)s;
	ClefableMetronome_AISelectEffect();
}
/* <<< factory ClefableMetronome_AISelectEffect */

/* >>> factory Ember_AISelectEffect */
static void adapt_Ember_AISelectEffect(ProbeState *s)
{
	(void)s;
	Ember_AISelectEffect();
}
/* <<< factory Ember_AISelectEffect */

/* >>> factory FlareonFlamethrower_AISelectEffect */
static void adapt_FlareonFlamethrower_AISelectEffect(ProbeState *s)
{
	(void)s;
	FlareonFlamethrower_AISelectEffect();
}
/* <<< factory FlareonFlamethrower_AISelectEffect */

/* >>> factory DestinyBond_DestinyBondEffect */
static void adapt_DestinyBond_DestinyBondEffect(ProbeState *s)
{
	s->hl = DestinyBond_DestinyBondEffect();
}
/* <<< factory DestinyBond_DestinyBondEffect */

/* >>> factory FlareonRage_AIEffect */
static void adapt_FlareonRage_AIEffect(ProbeState *s)
{
	FlareonRage_AIEffect();
}
/* <<< factory FlareonRage_AIEffect */

/* >>> factory GolduckHyperBeam_AISelectEffect */
static void adapt_GolduckHyperBeam_AISelectEffect(ProbeState *s)
{
	GolduckHyperBeam_AISelectEffect();
	(void)s;
}
/* <<< factory GolduckHyperBeam_AISelectEffect */

/* >>> factory OnixHardenEffect */
static void adapt_OnixHardenEffect(ProbeState *s)
{
	s->hl = OnixHardenEffect();
}
/* <<< factory OnixHardenEffect */

/* >>> factory PoliwhirlAmnesia_AISelectEffect */
static void adapt_PoliwhirlAmnesia_AISelectEffect(ProbeState *s)
{
	PoliwhirlAmnesia_AISelectEffect();
	(void)s;
}
/* <<< factory PoliwhirlAmnesia_AISelectEffect */

/* >>> factory StretchKick_AISelectEffect */
static void adapt_StretchKick_AISelectEffect(ProbeState *s)
{
	StretchKick_AISelectEffect();
	(void)s;
}
/* <<< factory StretchKick_AISelectEffect */

/* >>> factory VaporeonWaterGunEffect */
static void adapt_VaporeonWaterGunEffect(ProbeState *s)
{
	(void)s;
	VaporeonWaterGunEffect();
}
/* <<< factory VaporeonWaterGunEffect */

/* >>> factory Potion_DamageCheck */
static void adapt_Potion_DamageCheck(ProbeState *s)
{
	PotionDamageCheckResult r = Potion_DamageCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Potion_DamageCheck */

/* >>> factory CloysterSpikeCannon_AIEffect */
static void adapt_CloysterSpikeCannon_AIEffect(ProbeState *s)
{
	(void)s;
	CloysterSpikeCannon_AIEffect();
}
/* <<< factory CloysterSpikeCannon_AIEffect */

/* >>> factory JolteonDoubleKick_AIEffect */
static void adapt_JolteonDoubleKick_AIEffect(ProbeState *s)
{
	(void)s;
	JolteonDoubleKick_AIEffect();
}
/* <<< factory JolteonDoubleKick_AIEffect */

/* >>> factory RapidashStomp_AIEffect */
static void adapt_RapidashStomp_AIEffect(ProbeState *s)
{
	RapidashStomp_AIEffect();
}
/* <<< factory RapidashStomp_AIEffect */

/* >>> factory StoneBarrage_AIEffect */
static void adapt_StoneBarrage_AIEffect(ProbeState *s)
{
	(void)s;
	StoneBarrage_AIEffect();
}
/* <<< factory StoneBarrage_AIEffect */

/* >>> factory DestinyBond_AISelectEffect */
static void adapt_DestinyBond_AISelectEffect(ProbeState *s)
{
	(void)s;
	DestinyBond_AISelectEffect();
}
/* <<< factory DestinyBond_AISelectEffect */

/* >>> factory Rampage_AIEffect */
static void adapt_Rampage_AIEffect(ProbeState *s)
{
	(void)s;
	Rampage_AIEffect();
}
/* <<< factory Rampage_AIEffect */

/* >>> factory SuperPotion_DamageEnergyCheck */
static void adapt_SuperPotion_DamageEnergyCheck(ProbeState *s)
{
	SuperPotionDamageEnergyCheckResult r = SuperPotion_DamageEnergyCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SuperPotion_DamageEnergyCheck */

/* >>> factory KrabbyCallForFamily_CheckDeckAndPlayArea */
static void adapt_KrabbyCallForFamily_CheckDeckAndPlayArea(ProbeState *s)
{
	CheckIfDeckIsEmptyResult r = KrabbyCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory KrabbyCallForFamily_CheckDeckAndPlayArea */

/* >>> factory Revive_BenchCheck */
static void adapt_Revive_BenchCheck(ProbeState *s)
{
	ReviveBenchCheckResult r = Revive_BenchCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Revive_BenchCheck */

/* >>> factory DragonairHyperBeam_DiscardEffect */
static void adapt_DragonairHyperBeam_DiscardEffect(ProbeState *s)
{
	s->hl = DragonairHyperBeam_DiscardEffect(s->hl);
}
/* <<< factory DragonairHyperBeam_DiscardEffect */

/* >>> factory MirrorMove_ExecuteStatusEffect */
static void adapt_MirrorMove_ExecuteStatusEffect(ProbeState *s)
{
	MirrorMoveExecuteStatusEffectResult r = MirrorMove_ExecuteStatusEffect(s->a);
	s->f = r.f;
}
/* <<< factory MirrorMove_ExecuteStatusEffect */

/* >>> factory Curse_CheckDamageAndBench */
static void adapt_Curse_CheckDamageAndBench(ProbeState *s)
{
	CurseCheckDamageAndBenchResult result = Curse_CheckDamageAndBench();
	s->f = result.f;
	s->hl = result.hl;
}
/* <<< factory Curse_CheckDamageAndBench */

/* >>> factory SpearowMirrorMove_AIEffect */
static void adapt_SpearowMirrorMove_AIEffect(ProbeState *s)
{
	SpearowMirrorMove_AIEffect();
	(void)s;
}
/* <<< factory SpearowMirrorMove_AIEffect */

/* >>> factory SpearowMirrorMove_InitialEffect1 */
static void adapt_SpearowMirrorMove_InitialEffect1(ProbeState *s)
{
	MirrorMoveInitialEffect1Result r = SpearowMirrorMove_InitialEffect1();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory SpearowMirrorMove_InitialEffect1 */

/* >>> factory PidgeottoMirrorMove_AIEffect */
static void adapt_PidgeottoMirrorMove_AIEffect(ProbeState *s)
{
	PidgeottoMirrorMove_AIEffect();
	(void)s;
}
/* <<< factory PidgeottoMirrorMove_AIEffect */

/* >>> factory PidgeottoMirrorMove_AISelection */
static void adapt_PidgeottoMirrorMove_AISelection(ProbeState *s)
{
	PidgeottoMirrorMove_AISelection();
}
/* <<< factory PidgeottoMirrorMove_AISelection */

/* >>> factory ClefairyMetronome_AISelectEffect */
static void adapt_ClefairyMetronome_AISelectEffect(ProbeState *s)
{
	(void)s;
	ClefairyMetronome_AISelectEffect();
}
/* <<< factory ClefairyMetronome_AISelectEffect */

/* >>> factory EnergySpike_DeckCheck */
static void adapt_EnergySpike_DeckCheck(ProbeState *s)
{
	CheckIfDeckIsEmptyResult result = EnergySpike_DeckCheck();
	s->a = result.a;
	s->hl = result.hl;
	s->f = result.f;
}
/* <<< factory EnergySpike_DeckCheck */

/* >>> factory MagmarFlamethrower_AISelectEffect */
static void adapt_MagmarFlamethrower_AISelectEffect(ProbeState *s)
{
	(void)s;
	MagmarFlamethrower_AISelectEffect();
}
/* <<< factory MagmarFlamethrower_AISelectEffect */

/* >>> factory OmastarWaterGunEffect */
static void adapt_OmastarWaterGunEffect(ProbeState *s)
{
	(void)s;
	OmastarWaterGunEffect();
}
/* <<< factory OmastarWaterGunEffect */

/* >>> factory CuboneRage_AIEffect */
static void adapt_CuboneRage_AIEffect(ProbeState *s)
{
	(void)s;
	CuboneRage_AIEffect();
}
/* <<< factory CuboneRage_AIEffect */

/* >>> factory GravelerHardenEffect */
static void adapt_GravelerHardenEffect(ProbeState *s)
{
	s->hl = GravelerHardenEffect();
}
/* <<< factory GravelerHardenEffect */

/* >>> factory KarateChop_AIEffect */
static void adapt_KarateChop_AIEffect(ProbeState *s)
{
	(void)s;
	KarateChop_AIEffect();
}
/* <<< factory KarateChop_AIEffect */

/* >>> factory LaprasWaterGunEffect */
static void adapt_LaprasWaterGunEffect(ProbeState *s)
{
	(void)s;
	LaprasWaterGunEffect();
}
/* <<< factory LaprasWaterGunEffect */

/* >>> factory OmanyteWaterGunEffect */
static void adapt_OmanyteWaterGunEffect(ProbeState *s)
{
	(void)s;
	OmanyteWaterGunEffect();
}
/* <<< factory OmanyteWaterGunEffect */

/* >>> factory PoliwrathWaterGunEffect */
static void adapt_PoliwrathWaterGunEffect(ProbeState *s)
{
	(void)s;
	PoliwrathWaterGunEffect();
}
/* <<< factory PoliwrathWaterGunEffect */

/* >>> factory SeadraWaterGunEffect */
static void adapt_SeadraWaterGunEffect(ProbeState *s)
{
	(void)s;
	SeadraWaterGunEffect();
}
/* <<< factory SeadraWaterGunEffect */

/* >>> factory SuperFang_AIEffect */
static void adapt_SuperFang_AIEffect(ProbeState *s)
{
	(void)s;
	SuperFang_AIEffect();
}
/* <<< factory SuperFang_AIEffect */

/* >>> factory DragoniteLv41Slam_AIEffect */
static void adapt_DragoniteLv41Slam_AIEffect(ProbeState *s)
{
	(void)s;
	DragoniteLv41Slam_AIEffect();
}
/* <<< factory DragoniteLv41Slam_AIEffect */

/* >>> factory ElectabuzzQuickAttack_AIEffect */
static void adapt_ElectabuzzQuickAttack_AIEffect(ProbeState *s)
{
	(void)s;
	ElectabuzzQuickAttack_AIEffect();
}
/* <<< factory ElectabuzzQuickAttack_AIEffect */

/* >>> factory JolteonQuickAttack_AIEffect */
static void adapt_JolteonQuickAttack_AIEffect(ProbeState *s)
{
	(void)s;
	JolteonQuickAttack_AIEffect();
}
/* <<< factory JolteonQuickAttack_AIEffect */

/* >>> factory LeekSlap_AIEffect */
static void adapt_LeekSlap_AIEffect(ProbeState *s)
{
	(void)s;
	LeekSlap_AIEffect();
}
/* <<< factory LeekSlap_AIEffect */

/* >>> factory PinMissile_AIEffect */
static void adapt_PinMissile_AIEffect(ProbeState *s)
{
	(void)s;
	PinMissile_AIEffect();
}
/* <<< factory PinMissile_AIEffect */

/* >>> factory SandslashFurySwipes_AIEffect */
static void adapt_SandslashFurySwipes_AIEffect(ProbeState *s)
{
	(void)s;
	SandslashFurySwipes_AIEffect();
}
/* <<< factory SandslashFurySwipes_AIEffect */

/* >>> factory Thunderpunch_AIEffect */
static void adapt_Thunderpunch_AIEffect(ProbeState *s)
{
	(void)s;
	Thunderpunch_AIEffect();
}
/* <<< factory Thunderpunch_AIEffect */

/* >>> factory StarmieRecover_AISelectEffect */
static void adapt_StarmieRecover_AISelectEffect(ProbeState *s)
{
	StarmieRecoverAISelectEffectResult r = StarmieRecover_AISelectEffect();
	s->a = r.a;
	s->f = r.f;
}
/* <<< factory StarmieRecover_AISelectEffect */

/* >>> factory BellsproutCallForFamily_CheckDeckAndPlayArea */
static void adapt_BellsproutCallForFamily_CheckDeckAndPlayArea(ProbeState *s)
{
	BellsproutCallForFamilyCheckDeckAndPlayAreaResult r = BellsproutCallForFamily_CheckDeckAndPlayArea();
	s->a = r.a;
	s->hl = r.hl;
	s->f = r.f;
}
/* <<< factory BellsproutCallForFamily_CheckDeckAndPlayArea */

/* >>> factory Spark_AISelectEffect */
static void adapt_Spark_AISelectEffect(ProbeState *s)
{
	s->a = Spark_AISelectEffect().a;
}
/* <<< factory Spark_AISelectEffect */

/* >>> factory DamageSwap_CheckDamage */
static void adapt_DamageSwap_CheckDamage(ProbeState *s)
{
	DamageSwapCheckDamageResult r = DamageSwap_CheckDamage();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory DamageSwap_CheckDamage */

/* >>> factory PokemonFlute_BenchCheck */
static void adapt_PokemonFlute_BenchCheck(ProbeState *s)
{
	PokemonFluteBenchCheckResult r = PokemonFlute_BenchCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory PokemonFlute_BenchCheck */

/* >>> factory Heal_OncePerTurnCheck */
static void adapt_Heal_OncePerTurnCheck(ProbeState *s)
{
	HealOncePerTurnCheckResult r = Heal_OncePerTurnCheck();
	s->f = r.f;
	s->hl = r.hl;
}
/* <<< factory Heal_OncePerTurnCheck */

/* >>> factory Shift_ChangeColorEffect */
static void adapt_Shift_ChangeColorEffect(ProbeState *s)
{
	Shift_ChangeColorEffectResult r = Shift_ChangeColorEffect(s->d, s->e);
	s->f = r.f;
}
/* <<< factory Shift_ChangeColorEffect */

/* >>> factory MagikarpFlail_AIEffect */
static void adapt_MagikarpFlail_AIEffect(ProbeState *s)
{
	(void)s;
	MagikarpFlail_AIEffect();
}
/* <<< factory MagikarpFlail_AIEffect */

/* >>> factory PoliwagWaterGunEffect */
static void adapt_PoliwagWaterGunEffect(ProbeState *s)
{
	(void)s;
	PoliwagWaterGunEffect();
}
/* <<< factory PoliwagWaterGunEffect */

/* >>> factory DodrioRage_AIEffect */
static void adapt_DodrioRage_AIEffect(ProbeState *s)
{
	(void)s;
	DodrioRage_AIEffect();
}
/* <<< factory DodrioRage_AIEffect */

const ProbeEntry probe_entries_effect_functions[] = {
	{ "LeekSlap_OncePerDuelCheck", adapt_LeekSlap_OncePerDuelCheck },
	{ "LeekSlap_SetUsedThisDuelFlag", adapt_LeekSlap_SetUsedThisDuelFlag },
	{ "PlusPowerEffect", adapt_PlusPowerEffect },
	{ "StrikesBackEffect", adapt_StrikesBackEffect },
	{ "Switch_BenchCheck", adapt_Switch_BenchCheck },
	{ "Switch_SwitchEffect", adapt_Switch_SwitchEffect },
	{ "UpdateExpectedAIDamage", adapt_UpdateExpectedAIDamage },
	{ "SetExpectedAIDamage", adapt_SetExpectedAIDamage },
	{ "UpdateExpectedAIDamage_AccountForPoison", adapt_UpdateExpectedAIDamage_AccountForPoison },
	{ "IsPlayerTurn", adapt_IsPlayerTurn },
	{ "ApplySubstatus1ToAttackingCard", adapt_ApplySubstatus1ToAttackingCard },
	{ "SetNoEffectFromStatus", adapt_SetNoEffectFromStatus },
	{ "SetDefiniteAIDamage", adapt_SetDefiniteAIDamage },
	{ "SetDefiniteDamage", adapt_SetDefiniteDamage },
	{ "PickRandomPlayAreaCard", adapt_PickRandomPlayAreaCard },
	{ "GetNextPositionInTempList", adapt_GetNextPositionInTempList },
	{ "QueueStatusCondition", adapt_QueueStatusCondition },
	{ "SleepEffect", adapt_SleepEffect },
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
	{ "Func_2c6d9", adapt_Func_2c6d9 },

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
	{ "KrabbyCallForFamily_AISelectEffect", adapt_KrabbyCallForFamily_AISelectEffect },
	{ "ArcanineFlamethrower_CheckEnergy", adapt_ArcanineFlamethrower_CheckEnergy },
	{ "ArcanineFlamethrower_DiscardEffect", adapt_ArcanineFlamethrower_DiscardEffect },
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
	{ "NidorinoDoubleKick_AIEffect", adapt_NidorinoDoubleKick_AIEffect },
	{ "WeedlePoisonSting_AIEffect", adapt_WeedlePoisonSting_AIEffect },
	{ "BellsproutCallForFamily_AISelectEffect", adapt_BellsproutCallForFamily_AISelectEffect },
	{ "WeezingSmog_AIEffect", adapt_WeezingSmog_AIEffect },
	{ "KadabraRecover_DiscardEffect", adapt_KadabraRecover_DiscardEffect },
	{ "PrimeapeFurySwipes_AIEffect", adapt_PrimeapeFurySwipes_AIEffect },
	{ "StretchKick_CheckBench", adapt_StretchKick_CheckBench },
	{ "LightScreenEffect", adapt_LightScreenEffect },
	{ "CheckIfCardHasGrassEnergyAttached", adapt_CheckIfCardHasGrassEnergyAttached },
	{ "GrimerMinimizeEffect", adapt_GrimerMinimizeEffect },
	{ "MagnetonSonicboom_UnaffectedByColorEffect", adapt_MagnetonSonicboom_UnaffectedByColorEffect },
	{ "MagnetonSonicboom_NullEffect", adapt_MagnetonSonicboom_NullEffect },
	{ "ElectrodeSonicboom_UnaffectedByColorEffect", adapt_ElectrodeSonicboom_UnaffectedByColorEffect },
	{ "EnergySpike_AISelectEffect", adapt_EnergySpike_AISelectEffect },
	{ "CometPunch_AIEffect", adapt_CometPunch_AIEffect },
	{ "Conversion1_WeaknessCheck", adapt_Conversion1_WeaknessCheck },
	{ "Conversion2_ResistanceCheck", adapt_Conversion2_ResistanceCheck },
	{ "ElectrodeSonicboom_NullEffect", adapt_ElectrodeSonicboom_NullEffect },
	{ "FirstAid_DamageCheck", adapt_FirstAid_DamageCheck },
	{ "DoTheWaveEffect", adapt_DoTheWaveEffect },
	{ "FullHeal_StatusCheck", adapt_FullHeal_StatusCheck },
	{ "AIPickEnergyCardToDiscardFromDefendingPokemon", adapt_AIPickEnergyCardToDiscardFromDefendingPokemon },
	{ "AIFindTargetForBenchAttack", adapt_AIFindTargetForBenchAttack },
	{ "LoadCardNameAndInputColor", adapt_LoadCardNameAndInputColor },
	{ "Quickfreeze_InitialEffect", adapt_Quickfreeze_InitialEffect },
	{ "FocusEnergyEffect", adapt_FocusEnergyEffect },
	{ "Teleport_CheckBench", adapt_Teleport_CheckBench },
	{ "Teleport_AISelectEffect", adapt_Teleport_AISelectEffect },
	{ "ToxicGasEffect", adapt_ToxicGasEffect },
	{ "Sludge_AIEffect", adapt_Sludge_AIEffect },
	{ "PoisonWhip_AIEffect", adapt_PoisonWhip_AIEffect },
	{ "SolarPower_CheckUse", adapt_SolarPower_CheckUse },
	{ "Cowardice_CheckUseAndBench", adapt_Cowardice_CheckUseAndBench },
	{ "Cowardice_ReturnToHandEffect", adapt_Cowardice_ReturnToHandEffect },
	{ "PoisonFang_AIEffect", adapt_PoisonFang_AIEffect },
	{ "WeepinbellPoisonPowder_AIEffect", adapt_WeepinbellPoisonPowder_AIEffect },
	{ "Twineedle_AIEffect", adapt_Twineedle_AIEffect },
	{ "BeedrillPoisonSting_AIEffect", adapt_BeedrillPoisonSting_AIEffect },
	{ "FoulGas_AIEffect", adapt_FoulGas_AIEffect },
	{ "Sprout_AISelectEffect", adapt_Sprout_AISelectEffect },
	{ "NidoranFFurySwipes_AIEffect", adapt_NidoranFFurySwipes_AIEffect },
	{ "NidoranFCallForFamily_AISelectEffect", adapt_NidoranFCallForFamily_AISelectEffect },
	{ "HornHazard_AIEffect", adapt_HornHazard_AIEffect },
	{ "NidorinaDoubleKick_AIEffect", adapt_NidorinaDoubleKick_AIEffect },
	{ "ApplyExtraWaterEnergyDamageBonus", adapt_ApplyExtraWaterEnergyDamageBonus },
	{ "KakunaPoisonPowder_AIEffect", adapt_KakunaPoisonPowder_AIEffect },
	{ "SwordsDanceEffect", adapt_SwordsDanceEffect },
	{ "Toxic_AIEffect", adapt_Toxic_AIEffect },
	{ "BoyfriendsEffect", adapt_BoyfriendsEffect },
	{ "IvysaurPoisonPowder_AIEffect", adapt_IvysaurPoisonPowder_AIEffect },
	{ "EnergyTrans_CheckPlayArea", adapt_EnergyTrans_CheckPlayArea },
	{ "Fly_AIEffect", adapt_Fly_AIEffect },
	{ "Gigashock_AISelectEffect", adapt_Gigashock_AISelectEffect },
	{ "Wildfire_DiscardDeckEffect", adapt_Wildfire_DiscardDeckEffect },
	{ "MoltresLv35DiveBomb_AIEffect", adapt_MoltresLv35DiveBomb_AIEffect },
	{ "ClefairyDoll_BenchCheck", adapt_ClefairyDoll_BenchCheck },
	{ "ClefairyDoll_PlaceInPlayAreaEffect", adapt_ClefairyDoll_PlaceInPlayAreaEffect },
	{ "EnergyBurnCheck_Unreferenced", adapt_EnergyBurnCheck_Unreferenced },
	{ "FlareonRage_DamageBoostEffect", adapt_FlareonRage_DamageBoostEffect },
	{ "Shift_OncePerTurnCheck", adapt_Shift_OncePerTurnCheck },
	{ "VenomPowder_AIEffect", adapt_VenomPowder_AIEffect },
	{ "TangelaPoisonPowder_AIEffect", adapt_TangelaPoisonPowder_AIEffect },
	{ "PetalDance_AIEffect", adapt_PetalDance_AIEffect },
	{ "ClairvoyanceEffect", adapt_ClairvoyanceEffect },
	{ "RainDanceEffect", adapt_RainDanceEffect },
	{ "PsyduckFurySwipes_AIEffect", adapt_PsyduckFurySwipes_AIEffect },
	{ "VaporeonQuickAttack_AIEffect", adapt_VaporeonQuickAttack_AIEffect },
	{ "JellyfishSting_AIEffect", adapt_JellyfishSting_AIEffect },
	{ "PoliwhirlAmnesia_CheckAttacks", adapt_PoliwhirlAmnesia_CheckAttacks },
	{ "OmastarSpikeCannon_AIEffect", adapt_OmastarSpikeCannon_AIEffect },
	{ "HeadacheEffect", adapt_HeadacheEffect },
	{ "ArcanineQuickAttack_AIEffect", adapt_ArcanineQuickAttack_AIEffect },
	{ "FlamesOfRage_CheckEnergy", adapt_FlamesOfRage_CheckEnergy },
	{ "MoltresLv37DiveBomb_AIEffect", adapt_MoltresLv37DiveBomb_AIEffect },
	{ "GetEnergyAttachedMultiplierDamage", adapt_GetEnergyAttachedMultiplierDamage },
	{ "MagmarFlamethrower_DiscardEffect", adapt_MagmarFlamethrower_DiscardEffect },
	{ "MagmarSmog_AIEffect", adapt_MagmarSmog_AIEffect },
	{ "CheckIfTurnDuelistHasEvolvedCards", adapt_CheckIfTurnDuelistHasEvolvedCards },
	{ "FindFirstNonBasicCardInPlayArea", adapt_FindFirstNonBasicCardInPlayArea },
	{ "Wildfire_CheckEnergy", adapt_Wildfire_CheckEnergy },
	{ "MrMimeMeditate_DamageBoostEffect", adapt_MrMimeMeditate_DamageBoostEffect },
	{ "DancingEmbers_AIEffect", adapt_DancingEmbers_AIEffect },
	{ "Firegiver_InitialEffect", adapt_Firegiver_InitialEffect },
	{ "FlareonFlamethrower_DiscardEffect", adapt_FlareonFlamethrower_DiscardEffect },
	{ "MagmarFlamethrower_CheckEnergy", adapt_MagmarFlamethrower_CheckEnergy },
	{ "FlamesOfRage_DiscardEffect", adapt_FlamesOfRage_DiscardEffect },
	{ "FlamesOfRage_DamageBoostEffect", adapt_FlamesOfRage_DamageBoostEffect },
	{ "CharmeleonFlamethrower_CheckEnergy", adapt_CharmeleonFlamethrower_CheckEnergy },
	{ "CharmeleonFlamethrower_DiscardEffect", adapt_CharmeleonFlamethrower_DiscardEffect },
	{ "EnergyBurnEffect", adapt_EnergyBurnEffect },
	{ "FireSpin_CheckEnergy", adapt_FireSpin_CheckEnergy },
	{ "FlareonQuickAttack_AIEffect", adapt_FlareonQuickAttack_AIEffect },
	{ "FlareonFlamethrower_CheckEnergy", adapt_FlareonFlamethrower_CheckEnergy },
	{ "StarmieRecover_CheckEnergyHP", adapt_StarmieRecover_CheckEnergyHP },
	{ "StarmieRecover_DiscardEffect", adapt_StarmieRecover_DiscardEffect },
	{ "Prophecy_AISelectEffect", adapt_Prophecy_AISelectEffect },
	{ "Prophecy_ReorderDeckEffect", adapt_Prophecy_ReorderDeckEffect },
	{ "SuperEnergyRetrieval_HandEnergyCheck", adapt_SuperEnergyRetrieval_HandEnergyCheck },
	{ "GetNextPositionInTempList_TrainerEffects", adapt_GetNextPositionInTempList_TrainerEffects },
	{ "NinetalesLure_AISelectEffect", adapt_NinetalesLure_AISelectEffect },
	{ "Ember_CheckEnergy", adapt_Ember_CheckEnergy },
	{ "DestinyBond_CheckEnergy", adapt_DestinyBond_CheckEnergy },
	{ "ComputerSearch_HandDeckCheck", adapt_ComputerSearch_HandDeckCheck },
	{ "MrFuji_BenchCheck", adapt_MrFuji_BenchCheck },
	{ "Peek_OncePerTurnCheck", adapt_Peek_OncePerTurnCheck },
	{ "StepIn_BenchCheck", adapt_StepIn_BenchCheck },
	{ "Wail_BenchCheck", adapt_Wail_BenchCheck },
	{ "StepIn_SwitchEffect", adapt_StepIn_SwitchEffect },
	{ "ThickSkinnedEffect", adapt_ThickSkinnedEffect },
	{ "HealingWind_InitialEffect", adapt_HealingWind_InitialEffect },
	{ "PickRandomBasicCardFromDeck", adapt_PickRandomBasicCardFromDeck },
	{ "JynxMeditate_DamageBoostEffect", adapt_JynxMeditate_DamageBoostEffect },
	{ "KadabraRecover_CheckEnergyHP", adapt_KadabraRecover_CheckEnergyHP },
	{ "MewtwoAltEnergyAbsorption_AddToHandEffect", adapt_MewtwoAltEnergyAbsorption_AddToHandEffect },
	{ "MewtwoEnergyAbsorption_AddToHandEffect", adapt_MewtwoEnergyAbsorption_AddToHandEffect },
	{ "NeutralizingShieldEffect", adapt_NeutralizingShieldEffect },
	{ "PealOfThunder_InitialEffect", adapt_PealOfThunder_InitialEffect },
	{ "PrehistoricPowerEffect", adapt_PrehistoricPowerEffect },
	{ "Scavenge_DiscardEffect", adapt_Scavenge_DiscardEffect },
	{ "GustOfWind_BenchCheck", adapt_GustOfWind_BenchCheck },
	{ "DrawSymbolOnPlayAreaCursor", adapt_DrawSymbolOnPlayAreaCursor },
	{ "MarowakCallForFamily_AISelectEffect", adapt_MarowakCallForFamily_AISelectEffect },
	{ "CreateListOfFireEnergyAttachedToArena", adapt_CreateListOfFireEnergyAttachedToArena },
	{ "CreateEnergyCardListFromDiscardPile_AllEnergy", adapt_CreateEnergyCardListFromDiscardPile_AllEnergy },
	{ "CheckIfDeckIsEmpty", adapt_CheckIfDeckIsEmpty },
	{ "VictreebelLure_AssertPokemonInBench", adapt_VictreebelLure_AssertPokemonInBench },
	{ "NinetalesLure_CheckBench", adapt_NinetalesLure_CheckBench },
	{ "ThunderboltEffect", adapt_ThunderboltEffect },
	{ "TrainerCardAsPokemon_BenchCheck", adapt_TrainerCardAsPokemon_BenchCheck },
	{ "TrainerCardAsPokemon_DiscardEffect", adapt_TrainerCardAsPokemon_DiscardEffect },
	{ "MysteriousFossil_BenchCheck", adapt_MysteriousFossil_BenchCheck },
	{ "MysteriousFossil_PlaceInPlayAreaEffect", adapt_MysteriousFossil_PlaceInPlayAreaEffect },
	{ "ScoopUp_BenchCheck", adapt_ScoopUp_BenchCheck },
	{ "Toxic_DoublePoisonEffect", adapt_Toxic_DoublePoisonEffect },
	{ "TryGiveDamageCounter_StrangeBehavior", adapt_TryGiveDamageCounter_StrangeBehavior },
	{ "SpacingOut_CheckDamage", adapt_SpacingOut_CheckDamage },
	{ "SpacingOut_HealEffect", adapt_SpacingOut_HealEffect },
	{ "CopyPlayAreaHPToBackup_Unreferenced", adapt_CopyPlayAreaHPToBackup_Unreferenced },
	{ "CopyPlayAreaHPFromBackup_Unreferenced", adapt_CopyPlayAreaHPFromBackup_Unreferenced },
	{ "Gale_LoadAnimation", adapt_Gale_LoadAnimation },
	{ "EnergySearch_DeckCheck", adapt_EnergySearch_DeckCheck },
	{ "CheckIfCardIsBasicEnergy", adapt_CheckIfCardIsBasicEnergy },
	{ "CreatePlayableStage2PokemonCardListFromHand", adapt_CreatePlayableStage2PokemonCardListFromHand },
	{ "DestinyBond_DiscardEffect", adapt_DestinyBond_DiscardEffect },
	{ "Ember_DiscardEffect", adapt_Ember_DiscardEffect },
	{ "FireBlast_DiscardEffect", adapt_FireBlast_DiscardEffect },
	{ "FireSpin_AISelectEffect", adapt_FireSpin_AISelectEffect },
	{ "FireSpin_DiscardEffect", adapt_FireSpin_DiscardEffect },
	{ "PidgeottoMirrorMove_InitialEffect1", adapt_PidgeottoMirrorMove_InitialEffect1 },
	{ "ClefairyMetronome_CheckAttacks", adapt_ClefairyMetronome_CheckAttacks },
	{ "Psychic_DamageBoostEffect", adapt_Psychic_DamageBoostEffect },
	{ "Barrier_AISelectEffect", adapt_Barrier_AISelectEffect },
	{ "Whirlpool_AISelectEffect", adapt_Whirlpool_AISelectEffect },
	{ "Whirlpool_DiscardEffect", adapt_Whirlpool_DiscardEffect },
	{ "EnergyRemoval_EnergyCheck", adapt_EnergyRemoval_EnergyCheck },
	{ "EnergyRemoval_AISelection", adapt_EnergyRemoval_AISelection },
	{ "EnergyRetrieval_HandEnergyCheck", adapt_EnergyRetrieval_HandEnergyCheck },
	{ "MrMimeMeditate_AIEffect", adapt_MrMimeMeditate_AIEffect },
	{ "PsywaveEffect", adapt_PsywaveEffect },
	{ "PokemonCenter_DamageCheck", adapt_PokemonCenter_DamageCheck },
	{ "PokemonBreeder_HandPlayAreaCheck", adapt_PokemonBreeder_HandPlayAreaCheck },
	{ "PokemonTrader_HandDeckCheck", adapt_PokemonTrader_HandDeckCheck },
	{ "VictreebelLure_GetBenchPokemonWithLowestHP", adapt_VictreebelLure_GetBenchPokemonWithLowestHP },
	{ "Sprout_CheckDeckAndPlayArea", adapt_Sprout_CheckDeckAndPlayArea },
	{ "NidoranFCallForFamily_CheckDeckAndPlayArea", adapt_NidoranFCallForFamily_CheckDeckAndPlayArea },
	{ "DragonairHyperBeam_AISelectEffect", adapt_DragonairHyperBeam_AISelectEffect },
	{ "ClefableMetronome_CheckAttacks", adapt_ClefableMetronome_CheckAttacks },
	{ "Scavenge_CheckDiscardPile", adapt_Scavenge_CheckDiscardPile },
	{ "Scavenge_AISelectEffect", adapt_Scavenge_AISelectEffect },
	{ "SlowpokeAmnesia_CheckAttacks", adapt_SlowpokeAmnesia_CheckAttacks },
	{ "DevolutionBeam_CheckPlayArea", adapt_DevolutionBeam_CheckPlayArea },
	{ "DevolutionBeam_AISelectEffect", adapt_DevolutionBeam_AISelectEffect },
	{ "MewtwoAltEnergyAbsorption_CheckDiscardPile", adapt_MewtwoAltEnergyAbsorption_CheckDiscardPile },
	{ "MewtwoAltEnergyAbsorption_AISelectEffect", adapt_MewtwoAltEnergyAbsorption_AISelectEffect },
	{ "MewtwoEnergyAbsorption_CheckDiscardPile", adapt_MewtwoEnergyAbsorption_CheckDiscardPile },
	{ "MewtwoEnergyAbsorption_AISelectEffect", adapt_MewtwoEnergyAbsorption_AISelectEffect },
	{ "JynxMeditate_AIEffect", adapt_JynxMeditate_AIEffect },
	{ "MysteryAttack_RandomEffect", adapt_MysteryAttack_RandomEffect },
	{ "MarowakCallForFamily_CheckDeckAndPlayArea", adapt_MarowakCallForFamily_CheckDeckAndPlayArea },
	{ "IceBreath_ZeroDamage", adapt_IceBreath_ZeroDamage },
	{ "AIPickFireEnergyCardToDiscard", adapt_AIPickFireEnergyCardToDiscard },
	{ "FlamesOfRage_AIEffect", adapt_FlamesOfRage_AIEffect },
	{ "ArcanineFlamethrower_AISelectEffect", adapt_ArcanineFlamethrower_AISelectEffect },
	{ "FlamesOfRage_AISelectEffect", adapt_FlamesOfRage_AISelectEffect },
	{ "FireBlast_AISelectEffect", adapt_FireBlast_AISelectEffect },
	{ "EnergyConversion_CheckEnergy", adapt_EnergyConversion_CheckEnergy },
	{ "EnergyConversion_AISelectEffect", adapt_EnergyConversion_AISelectEffect },
	{ "HypnoDarkMind_AISelectEffect", adapt_HypnoDarkMind_AISelectEffect },
	{ "DreamEaterEffect", adapt_DreamEaterEffect },
	{ "Barrier_DiscardEffect", adapt_Barrier_DiscardEffect },
	{ "AIPickAttackForAmnesia", adapt_AIPickAttackForAmnesia },
	{ "MirrorMove_AISelection", adapt_MirrorMove_AISelection },
	{ "KinglerFlail_HPCheck", adapt_KinglerFlail_HPCheck },
	{ "MagikarpFlail_HPCheck", adapt_MagikarpFlail_HPCheck },
	{ "SuperFang_HalfHPEffect", adapt_SuperFang_HalfHPEffect },
	{ "KarateChop_DamageSubtractionEffect", adapt_KarateChop_DamageSubtractionEffect },
	{ "SpearowMirrorMove_AISelection", adapt_SpearowMirrorMove_AISelection },
	{ "CharmeleonFlamethrower_AISelectEffect", adapt_CharmeleonFlamethrower_AISelectEffect },
	{ "ClefableMetronome_AISelectEffect", adapt_ClefableMetronome_AISelectEffect },
	{ "Ember_AISelectEffect", adapt_Ember_AISelectEffect },
	{ "FlareonFlamethrower_AISelectEffect", adapt_FlareonFlamethrower_AISelectEffect },
	{ "DestinyBond_DestinyBondEffect", adapt_DestinyBond_DestinyBondEffect },
	{ "FlareonRage_AIEffect", adapt_FlareonRage_AIEffect },
	{ "GolduckHyperBeam_AISelectEffect", adapt_GolduckHyperBeam_AISelectEffect },
	{ "OnixHardenEffect", adapt_OnixHardenEffect },
	{ "PoliwhirlAmnesia_AISelectEffect", adapt_PoliwhirlAmnesia_AISelectEffect },
	{ "StretchKick_AISelectEffect", adapt_StretchKick_AISelectEffect },
	{ "VaporeonWaterGunEffect", adapt_VaporeonWaterGunEffect },
	{ "Potion_DamageCheck", adapt_Potion_DamageCheck },
	{ "CloysterSpikeCannon_AIEffect", adapt_CloysterSpikeCannon_AIEffect },
	{ "JolteonDoubleKick_AIEffect", adapt_JolteonDoubleKick_AIEffect },
	{ "RapidashStomp_AIEffect", adapt_RapidashStomp_AIEffect },
	{ "StoneBarrage_AIEffect", adapt_StoneBarrage_AIEffect },
	{ "DestinyBond_AISelectEffect", adapt_DestinyBond_AISelectEffect },
	{ "Rampage_AIEffect", adapt_Rampage_AIEffect },
	{ "SuperPotion_DamageEnergyCheck", adapt_SuperPotion_DamageEnergyCheck },
	{ "KrabbyCallForFamily_CheckDeckAndPlayArea", adapt_KrabbyCallForFamily_CheckDeckAndPlayArea },
	{ "Revive_BenchCheck", adapt_Revive_BenchCheck },
	{ "DragonairHyperBeam_DiscardEffect", adapt_DragonairHyperBeam_DiscardEffect },
	{ "MirrorMove_ExecuteStatusEffect", adapt_MirrorMove_ExecuteStatusEffect },
	{ "Curse_CheckDamageAndBench", adapt_Curse_CheckDamageAndBench },
	{ "SpearowMirrorMove_AIEffect", adapt_SpearowMirrorMove_AIEffect },
	{ "SpearowMirrorMove_InitialEffect1", adapt_SpearowMirrorMove_InitialEffect1 },
	{ "PidgeottoMirrorMove_AIEffect", adapt_PidgeottoMirrorMove_AIEffect },
	{ "PidgeottoMirrorMove_AISelection", adapt_PidgeottoMirrorMove_AISelection },
	{ "ClefairyMetronome_AISelectEffect", adapt_ClefairyMetronome_AISelectEffect },
	{ "EnergySpike_DeckCheck", adapt_EnergySpike_DeckCheck },
	{ "MagmarFlamethrower_AISelectEffect", adapt_MagmarFlamethrower_AISelectEffect },
	{ "OmastarWaterGunEffect", adapt_OmastarWaterGunEffect },
	{ "CuboneRage_AIEffect", adapt_CuboneRage_AIEffect },
	{ "GravelerHardenEffect", adapt_GravelerHardenEffect },
	{ "KarateChop_AIEffect", adapt_KarateChop_AIEffect },
	{ "LaprasWaterGunEffect", adapt_LaprasWaterGunEffect },
	{ "OmanyteWaterGunEffect", adapt_OmanyteWaterGunEffect },
	{ "PoliwrathWaterGunEffect", adapt_PoliwrathWaterGunEffect },
	{ "SeadraWaterGunEffect", adapt_SeadraWaterGunEffect },
	{ "SuperFang_AIEffect", adapt_SuperFang_AIEffect },
	{ "DragoniteLv41Slam_AIEffect", adapt_DragoniteLv41Slam_AIEffect },
	{ "ElectabuzzQuickAttack_AIEffect", adapt_ElectabuzzQuickAttack_AIEffect },
	{ "JolteonQuickAttack_AIEffect", adapt_JolteonQuickAttack_AIEffect },
	{ "LeekSlap_AIEffect", adapt_LeekSlap_AIEffect },
	{ "PinMissile_AIEffect", adapt_PinMissile_AIEffect },
	{ "SandslashFurySwipes_AIEffect", adapt_SandslashFurySwipes_AIEffect },
	{ "Thunderpunch_AIEffect", adapt_Thunderpunch_AIEffect },
	{ "StarmieRecover_AISelectEffect", adapt_StarmieRecover_AISelectEffect },
	{ "BellsproutCallForFamily_CheckDeckAndPlayArea", adapt_BellsproutCallForFamily_CheckDeckAndPlayArea },
	{ "Spark_AISelectEffect", adapt_Spark_AISelectEffect },
	{ "DamageSwap_CheckDamage", adapt_DamageSwap_CheckDamage },
	{ "PokemonFlute_BenchCheck", adapt_PokemonFlute_BenchCheck },
	{ "Heal_OncePerTurnCheck", adapt_Heal_OncePerTurnCheck },
	{ "Shift_ChangeColorEffect", adapt_Shift_ChangeColorEffect },
	{ "MagikarpFlail_AIEffect", adapt_MagikarpFlail_AIEffect },
	{ "PoliwagWaterGunEffect", adapt_PoliwagWaterGunEffect },
	{ "DodrioRage_AIEffect", adapt_DodrioRage_AIEffect },
	{ NULL, NULL },
};
