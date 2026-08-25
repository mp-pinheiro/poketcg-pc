
#ifndef POKETCG_HOME_EFFECT_FUNCTIONS_H
#define POKETCG_HOME_EFFECT_FUNCTIONS_H

#include "home/print_text.h"

/* >>> factory UpdateExpectedAIDamage */
void UpdateExpectedAIDamage(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory UpdateExpectedAIDamage */
/* >>> factory SetExpectedAIDamage */
void SetExpectedAIDamage(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory SetExpectedAIDamage */
/* >>> factory IsPlayerTurn */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } IsPlayerTurnResult;
IsPlayerTurnResult IsPlayerTurn(void);
/* <<< factory IsPlayerTurn */
/* >>> factory UpdateExpectedAIDamage_AccountForPoison */
void UpdateExpectedAIDamage_AccountForPoison(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory UpdateExpectedAIDamage_AccountForPoison */
/* >>> factory ApplySubstatus1ToAttackingCard */
uint16_t ApplySubstatus1ToAttackingCard(uint8_t a);
/* <<< factory ApplySubstatus1ToAttackingCard */
/* >>> factory SetNoEffectFromStatus */
void SetNoEffectFromStatus(void);
/* <<< factory SetNoEffectFromStatus */
/* >>> factory SetDefiniteAIDamage */
void SetDefiniteAIDamage(void);
/* <<< factory SetDefiniteAIDamage */
/* >>> factory PickRandomPlayAreaCard */
typedef struct { uint8_t a; uint8_t f; } PickRandomPlayAreaCardResult;
PickRandomPlayAreaCardResult PickRandomPlayAreaCard(void);
/* <<< factory PickRandomPlayAreaCard */
/* >>> factory SetDefiniteDamage */
void SetDefiniteDamage(uint8_t a);
/* <<< factory SetDefiniteDamage */
/* >>> factory GetNextPositionInTempList */
uint16_t GetNextPositionInTempList(void);
/* <<< factory GetNextPositionInTempList */
/* >>> factory QueueStatusCondition */
typedef struct { uint8_t f; } QueueStatusConditionResult;
QueueStatusConditionResult QueueStatusCondition(uint8_t b, uint8_t c);
/* <<< factory QueueStatusCondition */
/* >>> factory SleepEffect */
QueueStatusConditionResult SleepEffect(void);
/* <<< factory SleepEffect */
/* >>> factory CommentedOut_2c086 */
uint8_t CommentedOut_2c086(uint8_t a);
/* <<< factory CommentedOut_2c086 */
/* >>> factory SetWasUnsuccessful */
void SetWasUnsuccessful(void);
/* <<< factory SetWasUnsuccessful */
/* >>> factory Teleport_SwitchEffect */
/* >>> factory Teleport_SwitchEffect */
void Teleport_SwitchEffect(void);
/* <<< factory Teleport_SwitchEffect */
/* >>> factory SetDamageToATimes20 */
/* >>> factory SetDamageToATimes20 */
void SetDamageToATimes20(uint8_t a);
/* <<< factory SetDamageToATimes20 */
/* >>> factory CreateTrainerCardListFromDiscardPile */
typedef struct { uint16_t hl; uint8_t f; } CreateTrainerCardListFromDiscardPileResult;
CreateTrainerCardListFromDiscardPileResult CreateTrainerCardListFromDiscardPile(void);
/* <<< factory CreateTrainerCardListFromDiscardPile */
/* >>> factory CreateEnergyCardListFromDiscardPile */
typedef struct { uint16_t hl; uint8_t f; } CreateEnergyCardListFromDiscardPileResult;
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile(uint8_t c);
/* <<< factory CreateEnergyCardListFromDiscardPile */
/* >>> factory GetAttackName */
uint16_t GetAttackName(uint8_t d, uint8_t e);
/* <<< factory GetAttackName */
/* >>> factory ClefableMinimizeEffect */
uint16_t ClefableMinimizeEffect(void);
/* <<< factory ClefableMinimizeEffect */
/* >>> factory HandleAIMetronomeEffect */
void HandleAIMetronomeEffect(void);
/* <<< factory HandleAIMetronomeEffect */
/* >>> factory ParalysisEffect */
QueueStatusConditionResult ParalysisEffect(void);
/* <<< factory ParalysisEffect */
/* >>> factory ConfusionEffect */
QueueStatusConditionResult ConfusionEffect(void);
/* <<< factory ConfusionEffect */
/* >>> factory InvisibleWallEffect */
uint8_t InvisibleWallEffect(uint8_t f);
/* <<< factory InvisibleWallEffect */
/* >>> factory CheckIfDefendingPokemonHasAnyAttack */
typedef struct { uint8_t f; } CheckAttackResult;
CheckAttackResult CheckIfDefendingPokemonHasAnyAttack(void);
/* <<< factory CheckIfDefendingPokemonHasAnyAttack */
/* >>> factory UpdateDevolvedCardHPAndStage */
void UpdateDevolvedCardHPAndStage(uint8_t a);
/* <<< factory UpdateDevolvedCardHPAndStage */
/* >>> factory DodrioRage_DamageBoostEffect */
void DodrioRage_DamageBoostEffect(void);
/* <<< factory DodrioRage_DamageBoostEffect */
/* >>> factory DragonairSlam_AIEffect */
void DragonairSlam_AIEffect(void);
/* <<< factory DragonairSlam_AIEffect */
/* >>> factory CheckIfPlayAreaHasAnyDamage */
typedef struct { uint8_t f; uint16_t hl; } CheckIfPlayAreaHasAnyDamageResult;
CheckIfPlayAreaHasAnyDamageResult CheckIfPlayAreaHasAnyDamage(void);
/* <<< factory CheckIfPlayAreaHasAnyDamage */
/* >>> factory CreateEnergyCardListFromDiscardPile_OnlyBasic */
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile_OnlyBasic(void);
/* <<< factory CreateEnergyCardListFromDiscardPile_OnlyBasic */
/* >>> factory KabutoArmorEffect */
uint8_t KabutoArmorEffect(uint8_t f);
/* <<< factory KabutoArmorEffect */
/* >>> factory CuboneRage_DamageBoostEffect */
void CuboneRage_DamageBoostEffect(void);
/* <<< factory CuboneRage_DamageBoostEffect */
/* >>> factory PoisonEffect */
QueueStatusConditionResult PoisonEffect(void);
/* <<< factory PoisonEffect */
/* >>> factory DoublePoisonEffect */
QueueStatusConditionResult DoublePoisonEffect(void);
/* <<< factory DoublePoisonEffect */
/* >>> factory LoadCardNameAndInputColor */
void LoadCardNameAndInputColor(uint8_t a, uint8_t d, uint8_t e);
/* <<< factory LoadCardNameAndInputColor */
/* >>> factory AIPickEnergyCardToDiscardFromDefendingPokemon */
typedef struct { uint8_t a; } AIPickEnergyCardToDiscardResult;
AIPickEnergyCardToDiscardResult AIPickEnergyCardToDiscardFromDefendingPokemon(void);
/* <<< factory AIPickEnergyCardToDiscardFromDefendingPokemon */
/* >>> factory AIFindTargetForBenchAttack */
typedef struct { uint8_t a; } AIFindTargetForBenchAttackResult;
AIFindTargetForBenchAttackResult AIFindTargetForBenchAttack(void);
/* <<< factory AIFindTargetForBenchAttack */
/* >>> factory ApplyExtraWaterEnergyDamageBonus */
void ApplyExtraWaterEnergyDamageBonus(uint8_t b, uint8_t c);
/* <<< factory ApplyExtraWaterEnergyDamageBonus */
/* >>> factory OmastarSpikeCannon_AIEffect */
void OmastarSpikeCannon_AIEffect(void);
/* <<< factory OmastarSpikeCannon_AIEffect */
/* >>> factory ClairvoyanceEffect */
uint8_t ClairvoyanceEffect(uint8_t f);
/* <<< factory ClairvoyanceEffect */
/* >>> factory KrabbyCallForFamily_AISelectEffect */
void KrabbyCallForFamily_AISelectEffect(uint8_t c, uint16_t de);
/* <<< factory KrabbyCallForFamily_AISelectEffect */
/* >>> factory CreateListOfEnergyAttachedToArena */
typedef struct { uint8_t a; uint8_t c; uint16_t hl; uint8_t f; } CreateListOfEnergyAttachedToArenaResult;
CreateListOfEnergyAttachedToArenaResult CreateListOfEnergyAttachedToArena(uint8_t a);
/* <<< factory CreateListOfEnergyAttachedToArena */
/* >>> factory HandleNoDamageOrEffect */
typedef struct { uint8_t f; uint16_t hl; } HandleNoDamageOrEffectResult;
HandleNoDamageOrEffectResult HandleNoDamageOrEffect(uint16_t hl);
/* <<< factory HandleNoDamageOrEffect */
/* >>> factory ArcanineFlamethrower_CheckEnergy */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t e;
	uint16_t hl;
} ArcanineFlamethrowerCheckEnergyResult;
ArcanineFlamethrowerCheckEnergyResult ArcanineFlamethrower_CheckEnergy(void);
/* <<< factory ArcanineFlamethrower_CheckEnergy */
/* >>> factory ArcanineFlamethrower_DiscardEffect */
uint8_t ArcanineFlamethrower_DiscardEffect(void);
/* <<< factory ArcanineFlamethrower_DiscardEffect */
/* >>> factory PoisonWhip_AIEffect */
void PoisonWhip_AIEffect(void);
/* <<< factory PoisonWhip_AIEffect */
/* >>> factory SolarPower_CheckUse */
typedef struct { uint8_t f; uint16_t hl; } SolarPowerCheckUseResult;
SolarPowerCheckUseResult SolarPower_CheckUse(void);
/* <<< factory SolarPower_CheckUse */
/* >>> factory DevolutionBeam_LoadAnimation */
void DevolutionBeam_LoadAnimation(void);
/* <<< factory DevolutionBeam_LoadAnimation */
/* >>> factory CheckIfTurnDuelistHasEvolvedCards */
CheckAttackResult CheckIfTurnDuelistHasEvolvedCards(void);
/* <<< factory CheckIfTurnDuelistHasEvolvedCards */
/* >>> factory FindFirstNonBasicCardInPlayArea */
typedef struct { uint8_t a; uint8_t f; } FindFirstNonBasicCardInPlayAreaResult;
FindFirstNonBasicCardInPlayAreaResult FindFirstNonBasicCardInPlayArea(void);
/* <<< factory FindFirstNonBasicCardInPlayArea */
/* >>> factory Wildfire_AISelectEffect */
typedef struct { uint8_t a; uint8_t f; } WildfireAISelectEffectResult;
WildfireAISelectEffectResult Wildfire_AISelectEffect(void);
/* <<< factory Wildfire_AISelectEffect */
/* >>> factory FireBlast_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } FireBlastCheckEnergyResult;
FireBlastCheckEnergyResult FireBlast_CheckEnergy(void);
/* <<< factory FireBlast_CheckEnergy */
/* >>> factory BigEggsplosion_AIEffect */
void BigEggsplosion_AIEffect(void);
/* <<< factory BigEggsplosion_AIEffect */
/* >>> factory Thrash_AIEffect */
void Thrash_AIEffect(void);
/* <<< factory Thrash_AIEffect */
/* >>> factory Prophecy_CheckDeck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } ProphecyCheckDeckResult;
ProphecyCheckDeckResult Prophecy_CheckDeck(void);
/* <<< factory Prophecy_CheckDeck */
/* >>> factory TryGiveDamageCounter_DamageSwap */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} TryGiveDamageCounter_DamageSwapResult;
TryGiveDamageCounter_DamageSwapResult TryGiveDamageCounter_DamageSwap(void);
/* <<< factory TryGiveDamageCounter_DamageSwap */
/* >>> factory TransparencyEffect */
uint8_t TransparencyEffect(void);
/* <<< factory TransparencyEffect */
/* >>> factory Barrier_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } BarrierCheckEnergyResult;
BarrierCheckEnergyResult Barrier_CheckEnergy(void);
/* <<< factory Barrier_CheckEnergy */
/* >>> factory ResetDevolvedCardStatus */
uint8_t ResetDevolvedCardStatus(void);
/* <<< factory ResetDevolvedCardStatus */
/* >>> factory EeveeQuickAttack_AIEffect */
void EeveeQuickAttack_AIEffect(void);
/* <<< factory EeveeQuickAttack_AIEffect */
/* >>> factory MirrorMove_AIEffect */
void MirrorMove_AIEffect(void);
/* <<< factory MirrorMove_AIEffect */
/* >>> factory MirrorMove_InitialEffect1 */
typedef struct { uint8_t f; uint16_t hl; } MirrorMoveInitialEffect1Result;
MirrorMoveInitialEffect1Result MirrorMove_InitialEffect1(void);
/* <<< factory MirrorMove_InitialEffect1 */
/* >>> factory FuryAttack_AIEffect */
void FuryAttack_AIEffect(void);
/* <<< factory FuryAttack_AIEffect */
/* >>> factory RetreatAidEffect */
uint8_t RetreatAidEffect(uint8_t f);
/* <<< factory RetreatAidEffect */
/* >>> factory FriendshipSong_BenchCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } FriendshipSongBenchCheckResult;
FriendshipSongBenchCheckResult FriendshipSong_BenchCheck(void);
/* <<< factory FriendshipSong_BenchCheck */
/* >>> factory ExpandEffect */
void ExpandEffect(void);
/* <<< factory ExpandEffect */
/* >>> factory CheckIfThereAreAnyEnergyCardsAttached */
typedef struct { uint8_t f; } CheckIfThereAreAnyEnergyCardsAttachedResult;
CheckIfThereAreAnyEnergyCardsAttachedResult CheckIfThereAreAnyEnergyCardsAttached(void);
/* <<< factory CheckIfThereAreAnyEnergyCardsAttached */
/* >>> factory PokeBall_DeckCheck */
typedef struct { uint8_t a; uint16_t hl; uint8_t f; } PokeBall_DeckCheckResult;
PokeBall_DeckCheckResult PokeBall_DeckCheck(void);
/* <<< factory PokeBall_DeckCheck */
/* >>> factory Recycle_DiscardPileCheck */
typedef struct { uint16_t hl; uint8_t f; } Recycle_DiscardPileCheckResult;
Recycle_DiscardPileCheckResult Recycle_DiscardPileCheck(void);
/* <<< factory Recycle_DiscardPileCheck */
/* >>> factory CreateBasicPokemonCardListFromDiscardPile */
typedef struct { uint8_t f; } CreateBasicPokemonCardListFromDiscardPileResult;
CreateBasicPokemonCardListFromDiscardPileResult CreateBasicPokemonCardListFromDiscardPile(void);
/* <<< factory CreateBasicPokemonCardListFromDiscardPile */
/* >>> factory CreatePokemonCardListFromHand */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint8_t d; uint8_t e; } CreatePokemonCardListFromHandResult;
CreatePokemonCardListFromHandResult CreatePokemonCardListFromHand(void);
/* <<< factory CreatePokemonCardListFromHand */
/* >>> factory Pokedex_DeckCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } PokedexDeckCheckResult;
PokedexDeckCheckResult Pokedex_DeckCheck(void);
/* <<< factory Pokedex_DeckCheck */
/* >>> factory Pokedex_OrderDeckCardsEffect */
typedef struct { uint8_t a; uint8_t c; uint8_t f; uint16_t hl; } PokedexOrderDeckCardsEffectResult;
PokedexOrderDeckCardsEffectResult Pokedex_OrderDeckCardsEffect(void);
/* <<< factory Pokedex_OrderDeckCardsEffect */
/* >>> factory Maintenance_HandCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } MaintenanceHandCheckResult;
MaintenanceHandCheckResult Maintenance_HandCheck(void);
/* <<< factory Maintenance_HandCheck */
/* >>> factory DevolutionSpray_PlayAreaEvolutionCheck */
typedef struct { uint16_t hl; uint8_t f; } DevolutionSprayPlayAreaEvolutionCheckResult;
DevolutionSprayPlayAreaEvolutionCheckResult DevolutionSpray_PlayAreaEvolutionCheck(void);
/* <<< factory DevolutionSpray_PlayAreaEvolutionCheck */
/* >>> factory SpitPoison_AIEffect */
void SpitPoison_AIEffect(void);
/* <<< factory SpitPoison_AIEffect */
/* >>> factory GloomPoisonPowder_AIEffect */
void GloomPoisonPowder_AIEffect(void);
/* <<< factory GloomPoisonPowder_AIEffect */
/* >>> factory FoulOdorEffect */
QueueStatusConditionResult FoulOdorEffect(void);
/* <<< factory FoulOdorEffect */
/* >>> factory KakunaPoisonPowder_AIEffect */
void KakunaPoisonPowder_AIEffect(void);
/* <<< factory KakunaPoisonPowder_AIEffect */
/* >>> factory SwordsDanceEffect */
uint16_t SwordsDanceEffect(void);
/* <<< factory SwordsDanceEffect */
/* >>> factory Twineedle_AIEffect */
void Twineedle_AIEffect(void);
/* <<< factory Twineedle_AIEffect */
/* >>> factory BeedrillPoisonSting_AIEffect */
void BeedrillPoisonSting_AIEffect(void);
/* <<< factory BeedrillPoisonSting_AIEffect */
/* >>> factory FoulGas_AIEffect */
void FoulGas_AIEffect(void);
/* <<< factory FoulGas_AIEffect */
/* >>> factory Sprout_AISelectEffect */
void Sprout_AISelectEffect(uint8_t c, uint16_t de);
/* <<< factory Sprout_AISelectEffect */
/* >>> factory Teleport_CheckBench */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } TeleportCheckBenchResult;
TeleportCheckBenchResult Teleport_CheckBench(void);
/* <<< factory Teleport_CheckBench */
/* >>> factory Teleport_AISelectEffect */
typedef struct { uint8_t a; uint16_t hl; } TeleportAISelectEffectResult;
TeleportAISelectEffectResult Teleport_AISelectEffect(void);
/* <<< factory Teleport_AISelectEffect */
/* >>> factory HornHazard_AIEffect */
void HornHazard_AIEffect(void);
/* <<< factory HornHazard_AIEffect */
/* >>> factory NidorinaDoubleKick_AIEffect */
void NidorinaDoubleKick_AIEffect(void);
/* <<< factory NidorinaDoubleKick_AIEffect */
/* >>> factory NidorinoDoubleKick_AIEffect */
void NidorinoDoubleKick_AIEffect(void);
/* <<< factory NidorinoDoubleKick_AIEffect */
/* >>> factory WeedlePoisonSting_AIEffect */
void WeedlePoisonSting_AIEffect(void);
/* <<< factory WeedlePoisonSting_AIEffect */
/* >>> factory BellsproutCallForFamily_AISelectEffect */
void BellsproutCallForFamily_AISelectEffect(uint8_t c, uint16_t de);
/* <<< factory BellsproutCallForFamily_AISelectEffect */
/* >>> factory WeezingSmog_AIEffect */
void WeezingSmog_AIEffect(void);
/* <<< factory WeezingSmog_AIEffect */
/* >>> factory NidoranFFurySwipes_AIEffect */
void NidoranFFurySwipes_AIEffect(void);
/* <<< factory NidoranFFurySwipes_AIEffect */
/* >>> factory NidoranFCallForFamily_AISelectEffect */
void NidoranFCallForFamily_AISelectEffect(uint8_t c, uint16_t de);
/* <<< factory NidoranFCallForFamily_AISelectEffect */
/* >>> factory ToxicGasEffect */
uint8_t ToxicGasEffect(uint8_t f);
/* <<< factory ToxicGasEffect */
/* >>> factory Sludge_AIEffect */
void Sludge_AIEffect(void);
/* <<< factory Sludge_AIEffect */
/* >>> factory KadabraRecover_DiscardEffect */
uint8_t KadabraRecover_DiscardEffect(void);
/* <<< factory KadabraRecover_DiscardEffect */
/* >>> factory PrimeapeFurySwipes_AIEffect */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; } PrimeapeFurySwipesAIResult;
PrimeapeFurySwipesAIResult PrimeapeFurySwipes_AIEffect(void);
/* <<< factory PrimeapeFurySwipes_AIEffect */
/* >>> factory StretchKick_CheckBench */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } StretchKickCheckBenchResult;
StretchKickCheckBenchResult StretchKick_CheckBench(void);
/* <<< factory StretchKick_CheckBench */
/* >>> factory LightScreenEffect */
uint16_t LightScreenEffect(void);
/* <<< factory LightScreenEffect */
/* >>> factory StarmieRecover_CheckEnergyHP */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint8_t checked_damage; uint16_t hl; } StarmieRecoverCheckEnergyHPResult;
StarmieRecoverCheckEnergyHPResult StarmieRecover_CheckEnergyHP(void);
/* <<< factory StarmieRecover_CheckEnergyHP */
/* >>> factory StarmieRecover_DiscardEffect */
uint8_t StarmieRecover_DiscardEffect(void);
/* <<< factory StarmieRecover_DiscardEffect */
/* >>> factory Cowardice_CheckUseAndBench */
typedef struct { uint8_t f; uint16_t hl; } CowardiceCheckUseAndBenchResult;
CowardiceCheckUseAndBenchResult Cowardice_CheckUseAndBench(void);
/* <<< factory Cowardice_CheckUseAndBench */
/* >>> factory Cowardice_ReturnToHandEffect */
void Cowardice_ReturnToHandEffect(void);
/* <<< factory Cowardice_ReturnToHandEffect */

/* >>> factory CheckIfCardHasGrassEnergyAttached */
typedef struct { uint8_t a; uint8_t f; uint8_t e; uint16_t hl; } CheckIfCardHasGrassEnergyAttachedResult;
CheckIfCardHasGrassEnergyAttachedResult CheckIfCardHasGrassEnergyAttached(uint8_t a);
/* <<< factory CheckIfCardHasGrassEnergyAttached */
/* >>> factory GrimerMinimizeEffect */
uint16_t GrimerMinimizeEffect(void);
/* <<< factory GrimerMinimizeEffect */
/* >>> factory Quickfreeze_InitialEffect */
uint8_t Quickfreeze_InitialEffect(uint8_t f);
/* <<< factory Quickfreeze_InitialEffect */
/* >>> factory FocusEnergyEffect */
void FocusEnergyEffect(void);
/* <<< factory FocusEnergyEffect */
/* >>> factory MagnetonSonicboom_UnaffectedByColorEffect */
void MagnetonSonicboom_UnaffectedByColorEffect(void);
/* <<< factory MagnetonSonicboom_UnaffectedByColorEffect */
/* >>> factory MagnetonSonicboom_NullEffect */
void MagnetonSonicboom_NullEffect(void);
/* <<< factory MagnetonSonicboom_NullEffect */
/* >>> factory ElectrodeSonicboom_UnaffectedByColorEffect */
uint16_t ElectrodeSonicboom_UnaffectedByColorEffect(void);
/* <<< factory ElectrodeSonicboom_UnaffectedByColorEffect */
/* >>> factory EnergySpike_AISelectEffect */
void EnergySpike_AISelectEffect(void);
/* <<< factory EnergySpike_AISelectEffect */
/* >>> factory CometPunch_AIEffect */
void CometPunch_AIEffect(void);
/* <<< factory CometPunch_AIEffect */
/* >>> factory Conversion1_WeaknessCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } Conversion1WeaknessCheckResult;
Conversion1WeaknessCheckResult Conversion1_WeaknessCheck(void);
/* <<< factory Conversion1_WeaknessCheck */
/* >>> factory Conversion2_ResistanceCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } Conversion2ResistanceCheckResult;
Conversion2ResistanceCheckResult Conversion2_ResistanceCheck(void);
/* <<< factory Conversion2_ResistanceCheck */
/* >>> factory ElectrodeSonicboom_NullEffect */
void ElectrodeSonicboom_NullEffect(void);
/* <<< factory ElectrodeSonicboom_NullEffect */
/* >>> factory FirstAid_DamageCheck */
typedef struct { uint16_t hl; uint8_t f; } FirstAidDamageCheckResult;
FirstAidDamageCheckResult FirstAid_DamageCheck(void);
/* <<< factory FirstAid_DamageCheck */
/* >>> factory DoTheWaveEffect */
void DoTheWaveEffect(void);
/* <<< factory DoTheWaveEffect */
/* >>> factory FullHeal_StatusCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } FullHealStatusCheckResult;
FullHealStatusCheckResult FullHeal_StatusCheck(void);
/* <<< factory FullHeal_StatusCheck */
/* >>> factory PoisonFang_AIEffect */
void PoisonFang_AIEffect(void);
/* <<< factory PoisonFang_AIEffect */
/* >>> factory WeepinbellPoisonPowder_AIEffect */
void WeepinbellPoisonPowder_AIEffect(void);
/* <<< factory WeepinbellPoisonPowder_AIEffect */
/* >>> factory Toxic_AIEffect */
void Toxic_AIEffect(void);
/* <<< factory Toxic_AIEffect */
/* >>> factory BoyfriendsEffect */
void BoyfriendsEffect(void);
/* <<< factory BoyfriendsEffect */
/* >>> factory IvysaurPoisonPowder_AIEffect */
void IvysaurPoisonPowder_AIEffect(void);
/* <<< factory IvysaurPoisonPowder_AIEffect */
/* >>> factory EnergyTrans_CheckPlayArea */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; uint16_t de; } EnergyTransCheckPlayAreaResult;
EnergyTransCheckPlayAreaResult EnergyTrans_CheckPlayArea(void);
/* <<< factory EnergyTrans_CheckPlayArea */
/* >>> factory Firegiver_InitialEffect */
uint8_t Firegiver_InitialEffect(uint8_t f);
/* <<< factory Firegiver_InitialEffect */
/* >>> factory MoltresLv37DiveBomb_AIEffect */
void MoltresLv37DiveBomb_AIEffect(void);
/* <<< factory MoltresLv37DiveBomb_AIEffect */
/* >>> factory GetEnergyAttachedMultiplierDamage */
uint16_t GetEnergyAttachedMultiplierDamage(void);
/* <<< factory GetEnergyAttachedMultiplierDamage */
/* >>> factory Fly_AIEffect */
void Fly_AIEffect(void);
/* <<< factory Fly_AIEffect */
/* >>> factory Gigashock_AISelectEffect */
void Gigashock_AISelectEffect(void);
/* <<< factory Gigashock_AISelectEffect */
/* >>> factory Wildfire_DiscardDeckEffect */
void Wildfire_DiscardDeckEffect(void);
/* <<< factory Wildfire_DiscardDeckEffect */
/* >>> factory MoltresLv35DiveBomb_AIEffect */
void MoltresLv35DiveBomb_AIEffect(void);
/* <<< factory MoltresLv35DiveBomb_AIEffect */
/* >>> factory ClefairyDoll_BenchCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } ClefairyDollBenchCheckResult;
ClefairyDollBenchCheckResult ClefairyDoll_BenchCheck(void);
/* <<< factory ClefairyDoll_BenchCheck */
/* >>> factory ClefairyDoll_PlaceInPlayAreaEffect */
void ClefairyDoll_PlaceInPlayAreaEffect(void);
/* <<< factory ClefairyDoll_PlaceInPlayAreaEffect */
/* >>> factory EnergyBurnCheck_Unreferenced */
typedef struct { uint8_t a; uint8_t f; } EnergyBurnCheckResult;
EnergyBurnCheckResult EnergyBurnCheck_Unreferenced(void);
/* <<< factory EnergyBurnCheck_Unreferenced */
/* >>> factory FlareonRage_DamageBoostEffect */
void FlareonRage_DamageBoostEffect(void);
/* <<< factory FlareonRage_DamageBoostEffect */
/* >>> factory Shift_OncePerTurnCheck */
typedef struct { uint8_t f; uint16_t hl; } ShiftOncePerTurnCheckResult;
ShiftOncePerTurnCheckResult Shift_OncePerTurnCheck(void);
/* <<< factory Shift_OncePerTurnCheck */
/* >>> factory VenomPowder_AIEffect */
void VenomPowder_AIEffect(void);
/* <<< factory VenomPowder_AIEffect */
/* >>> factory TangelaPoisonPowder_AIEffect */
void TangelaPoisonPowder_AIEffect(void);
/* <<< factory TangelaPoisonPowder_AIEffect */
/* >>> factory PetalDance_AIEffect */
void PetalDance_AIEffect(void);
/* <<< factory PetalDance_AIEffect */
/* >>> factory RainDanceEffect */
uint8_t RainDanceEffect(uint8_t f);
/* <<< factory RainDanceEffect */
/* >>> factory PsyduckFurySwipes_AIEffect */
void PsyduckFurySwipes_AIEffect(void);
/* <<< factory PsyduckFurySwipes_AIEffect */
/* >>> factory VaporeonQuickAttack_AIEffect */
void VaporeonQuickAttack_AIEffect(void);
/* <<< factory VaporeonQuickAttack_AIEffect */
/* >>> factory JellyfishSting_AIEffect */
void JellyfishSting_AIEffect(void);
/* <<< factory JellyfishSting_AIEffect */
/* >>> factory PoliwhirlAmnesia_CheckAttacks */
typedef struct { uint8_t f; uint16_t hl; } PoliwhirlAmnesiaCheckAttacksResult;
PoliwhirlAmnesiaCheckAttacksResult PoliwhirlAmnesia_CheckAttacks(void);
/* <<< factory PoliwhirlAmnesia_CheckAttacks */
/* >>> factory HeadacheEffect */
void HeadacheEffect(void);
/* <<< factory HeadacheEffect */
/* >>> factory ArcanineQuickAttack_AIEffect */
void ArcanineQuickAttack_AIEffect(void);
/* <<< factory ArcanineQuickAttack_AIEffect */
/* >>> factory FlamesOfRage_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint8_t e; uint16_t hl; } FlamesOfRageCheckEnergyResult;
FlamesOfRageCheckEnergyResult FlamesOfRage_CheckEnergy(void);
/* <<< factory FlamesOfRage_CheckEnergy */
/* >>> factory MagmarFlamethrower_DiscardEffect */
uint8_t MagmarFlamethrower_DiscardEffect(void);
/* <<< factory MagmarFlamethrower_DiscardEffect */
/* >>> factory MagmarSmog_AIEffect */
void MagmarSmog_AIEffect(void);
/* <<< factory MagmarSmog_AIEffect */
/* >>> factory Wildfire_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint8_t e; uint16_t hl; } WildfireCheckEnergyResult;
WildfireCheckEnergyResult Wildfire_CheckEnergy(void);
/* <<< factory Wildfire_CheckEnergy */
/* >>> factory MrMimeMeditate_DamageBoostEffect */
void MrMimeMeditate_DamageBoostEffect(void);
/* <<< factory MrMimeMeditate_DamageBoostEffect */
/* >>> factory DancingEmbers_AIEffect */
void DancingEmbers_AIEffect(void);
/* <<< factory DancingEmbers_AIEffect */
/* >>> factory FlareonFlamethrower_DiscardEffect */
uint8_t FlareonFlamethrower_DiscardEffect(void);
/* <<< factory FlareonFlamethrower_DiscardEffect */
/* >>> factory MagmarFlamethrower_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } MagmarFlamethrowerCheckEnergyResult;
MagmarFlamethrowerCheckEnergyResult MagmarFlamethrower_CheckEnergy(void);
/* <<< factory MagmarFlamethrower_CheckEnergy */
/* >>> factory FlamesOfRage_DiscardEffect */
void FlamesOfRage_DiscardEffect(void);
/* <<< factory FlamesOfRage_DiscardEffect */
/* >>> factory FlamesOfRage_DamageBoostEffect */
void FlamesOfRage_DamageBoostEffect(void);
/* <<< factory FlamesOfRage_DamageBoostEffect */
/* >>> factory CharmeleonFlamethrower_CheckEnergy */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t e;
	uint16_t hl;
} CharmeleonFlamethrowerCheckEnergyResult;
CharmeleonFlamethrowerCheckEnergyResult CharmeleonFlamethrower_CheckEnergy(void);
/* <<< factory CharmeleonFlamethrower_CheckEnergy */
/* >>> factory CharmeleonFlamethrower_DiscardEffect */
uint8_t CharmeleonFlamethrower_DiscardEffect(void);
/* <<< factory CharmeleonFlamethrower_DiscardEffect */
/* >>> factory EnergyBurnEffect */
typedef struct { uint8_t f; } EnergyBurnEffectResult;
EnergyBurnEffectResult EnergyBurnEffect(uint8_t f);
/* <<< factory EnergyBurnEffect */
/* >>> factory FireSpin_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } FireSpinCheckEnergyResult;
FireSpinCheckEnergyResult FireSpin_CheckEnergy(void);
/* <<< factory FireSpin_CheckEnergy */
/* >>> factory FlareonQuickAttack_AIEffect */
void FlareonQuickAttack_AIEffect(void);
/* <<< factory FlareonQuickAttack_AIEffect */
/* >>> factory FlareonFlamethrower_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint8_t e; uint16_t hl; } FlareonFlamethrowerCheckEnergyResult;
FlareonFlamethrowerCheckEnergyResult FlareonFlamethrower_CheckEnergy(void);
/* <<< factory FlareonFlamethrower_CheckEnergy */
/* >>> factory Prophecy_AISelectEffect */
typedef struct { uint8_t a; } ProphecyAISelectEffectResult;
ProphecyAISelectEffectResult Prophecy_AISelectEffect(void);
/* <<< factory Prophecy_AISelectEffect */
/* >>> factory Prophecy_ReorderDeckEffect */
typedef struct { uint8_t a; uint8_t c; uint8_t f; uint16_t hl; } ProphecyReorderDeckEffectResult;
ProphecyReorderDeckEffectResult Prophecy_ReorderDeckEffect(void);
/* <<< factory Prophecy_ReorderDeckEffect */
/* >>> factory SuperEnergyRetrieval_HandEnergyCheck */
typedef struct { uint16_t hl; uint8_t f; } SuperEnergyRetrievalHandEnergyCheckResult;
SuperEnergyRetrievalHandEnergyCheckResult SuperEnergyRetrieval_HandEnergyCheck(void);
/* <<< factory SuperEnergyRetrieval_HandEnergyCheck */
/* >>> factory GetNextPositionInTempList_TrainerEffects */
uint16_t GetNextPositionInTempList_TrainerEffects(void);
/* <<< factory GetNextPositionInTempList_TrainerEffects */
/* >>> factory NinetalesLure_AISelectEffect */
uint8_t NinetalesLure_AISelectEffect(void);
/* <<< factory NinetalesLure_AISelectEffect */
/* >>> factory Ember_CheckEnergy */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } EmberCheckEnergyResult;
EmberCheckEnergyResult Ember_CheckEnergy(void);
/* <<< factory Ember_CheckEnergy */
/* >>> factory DestinyBond_CheckEnergy */
IsPlayerTurnResult DestinyBond_CheckEnergy(void);
/* <<< factory DestinyBond_CheckEnergy */
/* >>> factory ComputerSearch_HandDeckCheck */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} ComputerSearchHandDeckCheckResult;
ComputerSearchHandDeckCheckResult ComputerSearch_HandDeckCheck(void);
/* <<< factory ComputerSearch_HandDeckCheck */
/* >>> factory MrFuji_BenchCheck */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} MrFujiBenchCheckResult;
MrFujiBenchCheckResult MrFuji_BenchCheck(void);
/* <<< factory MrFuji_BenchCheck */
/* >>> factory DreamEaterEffect */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } DreamEaterEffectResult;
DreamEaterEffectResult DreamEaterEffect(void);
/* <<< factory DreamEaterEffect */
/* >>> factory JynxMeditate_DamageBoostEffect */
void JynxMeditate_DamageBoostEffect(void);
/* <<< factory JynxMeditate_DamageBoostEffect */
/* >>> factory KadabraRecover_CheckEnergyHP */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint8_t checked_damage; uint16_t hl; } KadabraRecoverCheckEnergyHPResult;
KadabraRecoverCheckEnergyHPResult KadabraRecover_CheckEnergyHP(void);
/* <<< factory KadabraRecover_CheckEnergyHP */
/* >>> factory MewtwoAltEnergyAbsorption_AddToHandEffect */
void MewtwoAltEnergyAbsorption_AddToHandEffect(void);
/* <<< factory MewtwoAltEnergyAbsorption_AddToHandEffect */
/* >>> factory MewtwoEnergyAbsorption_AddToHandEffect */
void MewtwoEnergyAbsorption_AddToHandEffect(void);
/* <<< factory MewtwoEnergyAbsorption_AddToHandEffect */
/* >>> factory NeutralizingShieldEffect */
uint8_t NeutralizingShieldEffect(void);
/* <<< factory NeutralizingShieldEffect */
/* >>> factory PealOfThunder_InitialEffect */
uint8_t PealOfThunder_InitialEffect(void);
/* <<< factory PealOfThunder_InitialEffect */
/* >>> factory PrehistoricPowerEffect */
uint8_t PrehistoricPowerEffect(void);
/* <<< factory PrehistoricPowerEffect */
/* >>> factory Scavenge_DiscardEffect */
uint8_t Scavenge_DiscardEffect(void);
/* <<< factory Scavenge_DiscardEffect */
/* >>> factory Peek_OncePerTurnCheck */
/* >>> factory StepIn_BenchCheck */
SolarPowerCheckUseResult StepIn_BenchCheck(void);
/* <<< factory StepIn_BenchCheck */
SolarPowerCheckUseResult Peek_OncePerTurnCheck(void);
/* <<< factory Peek_OncePerTurnCheck */
/* >>> factory Wail_BenchCheck */
MrFujiBenchCheckResult Wail_BenchCheck(void);
/* <<< factory Wail_BenchCheck */
/* >>> factory StepIn_SwitchEffect */
void StepIn_SwitchEffect(void);
/* <<< factory StepIn_SwitchEffect */
/* >>> factory ThickSkinnedEffect */
uint8_t ThickSkinnedEffect(uint8_t f);
/* <<< factory ThickSkinnedEffect */
/* >>> factory HealingWind_InitialEffect */
uint8_t HealingWind_InitialEffect(uint8_t f);
/* <<< factory HealingWind_InitialEffect */
/* >>> factory PickRandomBasicCardFromDeck */
uint8_t PickRandomBasicCardFromDeck(void);
/* <<< factory PickRandomBasicCardFromDeck */
/* >>> factory GustOfWind_BenchCheck */
IsPlayerTurnResult GustOfWind_BenchCheck(void);
/* <<< factory GustOfWind_BenchCheck */
/* >>> factory DrawSymbolOnPlayAreaCursor */
void DrawSymbolOnPlayAreaCursor(uint8_t a, uint8_t b);
/* <<< factory DrawSymbolOnPlayAreaCursor */
/* >>> factory Func_2c6d9 */
WaitResult Func_2c6d9(void);
/* <<< factory Func_2c6d9 */

/* >>> factory MarowakCallForFamily_AISelectEffect */
void MarowakCallForFamily_AISelectEffect(void);
/* <<< factory MarowakCallForFamily_AISelectEffect */
/* >>> factory CreateListOfFireEnergyAttachedToArena */
CreateListOfEnergyAttachedToArenaResult CreateListOfFireEnergyAttachedToArena(void);
/* <<< factory CreateListOfFireEnergyAttachedToArena */
/* >>> factory CreateEnergyCardListFromDiscardPile_AllEnergy */
CreateEnergyCardListFromDiscardPileResult CreateEnergyCardListFromDiscardPile_AllEnergy(void);
/* <<< factory CreateEnergyCardListFromDiscardPile_AllEnergy */
/* >>> factory CheckIfDeckIsEmpty */
typedef struct { uint8_t a; uint16_t hl; uint8_t f; } CheckIfDeckIsEmptyResult;
CheckIfDeckIsEmptyResult CheckIfDeckIsEmpty(void);
/* <<< factory CheckIfDeckIsEmpty */
/* >>> factory VictreebelLure_AssertPokemonInBench */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } VictreebelLureAssertPokemonInBenchResult;
VictreebelLureAssertPokemonInBenchResult VictreebelLure_AssertPokemonInBench(void);
/* <<< factory VictreebelLure_AssertPokemonInBench */
/* >>> factory NinetalesLure_CheckBench */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } NinetalesLureCheckBenchResult;
NinetalesLureCheckBenchResult NinetalesLure_CheckBench(void);
/* <<< factory NinetalesLure_CheckBench */
/* >>> factory ThunderboltEffect */
void ThunderboltEffect(void);
/* <<< factory ThunderboltEffect */
/* >>> factory TrainerCardAsPokemon_BenchCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } TrainerCardAsPokemonBenchCheckResult;
TrainerCardAsPokemonBenchCheckResult TrainerCardAsPokemon_BenchCheck(void);
/* <<< factory TrainerCardAsPokemon_BenchCheck */
/* >>> factory TrainerCardAsPokemon_DiscardEffect */
void TrainerCardAsPokemon_DiscardEffect(void);
/* <<< factory TrainerCardAsPokemon_DiscardEffect */
/* >>> factory MysteriousFossil_BenchCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } MysteriousFossilBenchCheckResult;
MysteriousFossilBenchCheckResult MysteriousFossil_BenchCheck(void);
/* <<< factory MysteriousFossil_BenchCheck */
/* >>> factory MysteriousFossil_PlaceInPlayAreaEffect */
void MysteriousFossil_PlaceInPlayAreaEffect(void);
/* <<< factory MysteriousFossil_PlaceInPlayAreaEffect */
/* >>> factory ScoopUp_BenchCheck */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } ScoopUpBenchCheckResult;
ScoopUpBenchCheckResult ScoopUp_BenchCheck(void);
/* <<< factory ScoopUp_BenchCheck */
/* >>> factory Toxic_DoublePoisonEffect */
QueueStatusConditionResult Toxic_DoublePoisonEffect(void);
/* >>> factory LeekSlap_OncePerDuelCheck */
uint8_t LeekSlap_OncePerDuelCheck(void);
/* <<< factory LeekSlap_OncePerDuelCheck */
/* >>> factory LeekSlap_SetUsedThisDuelFlag */
void LeekSlap_SetUsedThisDuelFlag(void);
/* <<< factory LeekSlap_SetUsedThisDuelFlag */
/* >>> factory PlusPowerEffect */
void PlusPowerEffect(void);
/* <<< factory PlusPowerEffect */
/* >>> factory StrikesBackEffect */
uint8_t StrikesBackEffect(void);
/* <<< factory StrikesBackEffect */
/* >>> factory Switch_BenchCheck */
MrFujiBenchCheckResult Switch_BenchCheck(void);
/* <<< factory Switch_BenchCheck */
/* >>> factory Switch_SwitchEffect */
void Switch_SwitchEffect(void);
/* <<< factory Switch_SwitchEffect */
/* >>> factory TryGiveDamageCounter_StrangeBehavior */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} TryGiveDamageCounter_StrangeBehaviorResult;
TryGiveDamageCounter_StrangeBehaviorResult TryGiveDamageCounter_StrangeBehavior(void);
/* <<< factory TryGiveDamageCounter_StrangeBehavior */
/* >>> factory SpacingOut_CheckDamage */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint8_t e; uint16_t hl; } SpacingOutCheckDamageResult;
SpacingOutCheckDamageResult SpacingOut_CheckDamage(void);
/* <<< factory SpacingOut_CheckDamage */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; uint8_t update_hl; } SpacingOutHealEffectResult;
SpacingOutHealEffectResult SpacingOut_HealEffect(void);
/* <<< factory SpacingOut_HealEffect */
/* >>> factory CopyPlayAreaHPToBackup_Unreferenced */
void CopyPlayAreaHPToBackup_Unreferenced(void);
/* <<< factory CopyPlayAreaHPToBackup_Unreferenced */
/* >>> factory CopyPlayAreaHPFromBackup_Unreferenced */
void CopyPlayAreaHPFromBackup_Unreferenced(void);
/* <<< factory CopyPlayAreaHPFromBackup_Unreferenced */
/* >>> factory Gale_LoadAnimation */
void Gale_LoadAnimation(void);
/* <<< factory Gale_LoadAnimation */
/* >>> factory EnergySearch_DeckCheck */
uint8_t EnergySearch_DeckCheck(void);
/* <<< factory EnergySearch_DeckCheck */
/* >>> factory CheckIfCardIsBasicEnergy */
uint8_t CheckIfCardIsBasicEnergy(uint8_t a);
/* <<< factory CheckIfCardIsBasicEnergy */
/* >>> factory CreatePlayableStage2PokemonCardListFromHand */
uint8_t CreatePlayableStage2PokemonCardListFromHand(void);
/* <<< factory CreatePlayableStage2PokemonCardListFromHand */
/* >>> factory PidgeottoMirrorMove_InitialEffect1 */
MirrorMoveInitialEffect1Result PidgeottoMirrorMove_InitialEffect1(void);
/* <<< factory PidgeottoMirrorMove_InitialEffect1 */
/* >>> factory ClefairyMetronome_CheckAttacks */
typedef struct { uint8_t f; uint16_t hl; } ClefairyMetronomeCheckAttacksResult;
ClefairyMetronomeCheckAttacksResult ClefairyMetronome_CheckAttacks(void);
/* <<< factory ClefairyMetronome_CheckAttacks */
/* >>> factory Psychic_DamageBoostEffect */
void Psychic_DamageBoostEffect(void);
/* <<< factory Psychic_DamageBoostEffect */
/* >>> factory Barrier_AISelectEffect */
void Barrier_AISelectEffect(void);
/* <<< factory Barrier_AISelectEffect */
/* >>> factory Whirlpool_AISelectEffect */
uint8_t Whirlpool_AISelectEffect(void);
/* <<< factory Whirlpool_AISelectEffect */
/* >>> factory Whirlpool_DiscardEffect */
uint16_t Whirlpool_DiscardEffect(uint16_t hl);
/* <<< factory Whirlpool_DiscardEffect */
/* >>> factory EnergyRemoval_EnergyCheck */
typedef struct { uint8_t f; uint16_t hl; } EnergyRemovalEnergyCheckResult;
EnergyRemovalEnergyCheckResult EnergyRemoval_EnergyCheck(void);
/* <<< factory EnergyRemoval_EnergyCheck */
/* >>> factory EnergyRemoval_AISelection */
uint8_t EnergyRemoval_AISelection(void);
/* <<< factory EnergyRemoval_AISelection */
/* >>> factory EnergyRetrieval_HandEnergyCheck */
typedef struct { uint16_t hl; uint8_t f; } EnergyRetrievalHandEnergyCheckResult;
EnergyRetrievalHandEnergyCheckResult EnergyRetrieval_HandEnergyCheck(void);
/* <<< factory EnergyRetrieval_HandEnergyCheck */
/* >>> factory MrMimeMeditate_AIEffect */
void MrMimeMeditate_AIEffect(void);
/* <<< factory MrMimeMeditate_AIEffect */
/* >>> factory PsywaveEffect */
uint16_t PsywaveEffect(void);
/* <<< factory PsywaveEffect */
/* >>> factory PokemonCenter_DamageCheck */
typedef struct { uint8_t f; uint16_t hl; } PokemonCenterDamageCheckResult;
PokemonCenterDamageCheckResult PokemonCenter_DamageCheck(void);
/* <<< factory PokemonCenter_DamageCheck */
/* >>> factory PokemonBreeder_HandPlayAreaCheck */
typedef struct { uint8_t f; uint16_t hl; } PokemonBreederHandPlayAreaCheckResult;
PokemonBreederHandPlayAreaCheckResult PokemonBreeder_HandPlayAreaCheck(uint16_t hl);
/* <<< factory PokemonBreeder_HandPlayAreaCheck */
/* >>> factory PokemonTrader_HandDeckCheck */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
	uint8_t update_cde;
} PokemonTraderHandDeckCheckResult;
PokemonTraderHandDeckCheckResult PokemonTrader_HandDeckCheck(void);
/* <<< factory PokemonTrader_HandDeckCheck */
/* >>> factory VictreebelLure_GetBenchPokemonWithLowestHP */
void VictreebelLure_GetBenchPokemonWithLowestHP(void);
/* <<< factory VictreebelLure_GetBenchPokemonWithLowestHP */
/* >>> factory Sprout_CheckDeckAndPlayArea */
CheckIfDeckIsEmptyResult Sprout_CheckDeckAndPlayArea(void);
/* <<< factory Sprout_CheckDeckAndPlayArea */
/* >>> factory NidoranFCallForFamily_CheckDeckAndPlayArea */
CheckIfDeckIsEmptyResult NidoranFCallForFamily_CheckDeckAndPlayArea(void);
/* <<< factory NidoranFCallForFamily_CheckDeckAndPlayArea */
/* >>> factory DragonairHyperBeam_AISelectEffect */
void DragonairHyperBeam_AISelectEffect(void);
/* <<< factory DragonairHyperBeam_AISelectEffect */
/* >>> factory ClefableMetronome_CheckAttacks */
typedef struct { uint8_t f; uint16_t hl; } ClefableMetronomeCheckAttacksResult;
ClefableMetronomeCheckAttacksResult ClefableMetronome_CheckAttacks(void);
/* <<< factory ClefableMetronome_CheckAttacks */
/* >>> factory Scavenge_CheckDiscardPile */
typedef struct { uint16_t hl; uint8_t f; } ScavengeCheckDiscardPileResult;
ScavengeCheckDiscardPileResult Scavenge_CheckDiscardPile(void);
/* <<< factory Scavenge_CheckDiscardPile */
/* >>> factory Scavenge_AISelectEffect */
void Scavenge_AISelectEffect(void);
/* <<< factory Scavenge_AISelectEffect */
/* >>> factory SlowpokeAmnesia_CheckAttacks */
typedef struct { uint8_t f; uint16_t hl; } SlowpokeAmnesiaCheckAttacksResult;
SlowpokeAmnesiaCheckAttacksResult SlowpokeAmnesia_CheckAttacks(void);
/* <<< factory SlowpokeAmnesia_CheckAttacks */
/* >>> factory DevolutionBeam_CheckPlayArea */
typedef struct { uint8_t f; uint8_t d; uint8_t e; uint16_t hl; } DevolutionBeamCheckPlayAreaResult;
DevolutionBeamCheckPlayAreaResult DevolutionBeam_CheckPlayArea(void);
/* <<< factory DevolutionBeam_CheckPlayArea */
/* >>> factory DevolutionBeam_AISelectEffect */
void DevolutionBeam_AISelectEffect(void);
/* <<< factory DevolutionBeam_AISelectEffect */
/* >>> factory MewtwoAltEnergyAbsorption_CheckDiscardPile */
CreateEnergyCardListFromDiscardPileResult MewtwoAltEnergyAbsorption_CheckDiscardPile(void);
/* <<< factory MewtwoAltEnergyAbsorption_CheckDiscardPile */
/* >>> factory MewtwoAltEnergyAbsorption_AISelectEffect */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t de; uint16_t hl; } MewtwoAltEnergyAbsorptionAISelectEffectResult;
MewtwoAltEnergyAbsorptionAISelectEffectResult MewtwoAltEnergyAbsorption_AISelectEffect(void);
/* <<< factory MewtwoAltEnergyAbsorption_AISelectEffect */
/* >>> factory MewtwoEnergyAbsorption_CheckDiscardPile */
typedef struct { uint16_t hl; uint8_t f; uint8_t b; uint8_t c; uint16_t de; } MewtwoEnergyAbsorptionCheckDiscardPileResult;
MewtwoEnergyAbsorptionCheckDiscardPileResult MewtwoEnergyAbsorption_CheckDiscardPile(void);
/* <<< factory MewtwoEnergyAbsorption_CheckDiscardPile */
/* >>> factory MewtwoEnergyAbsorption_AISelectEffect */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t de; uint16_t hl; } MewtwoEnergyAbsorptionAISelectEffectResult;
MewtwoEnergyAbsorptionAISelectEffectResult MewtwoEnergyAbsorption_AISelectEffect(void);
/* <<< factory MewtwoEnergyAbsorption_AISelectEffect */
/* >>> factory JynxMeditate_AIEffect */
void JynxMeditate_AIEffect(void);
/* <<< factory JynxMeditate_AIEffect */
/* >>> factory MysteryAttack_RandomEffect */
void MysteryAttack_RandomEffect(void);
/* <<< factory MysteryAttack_RandomEffect */
/* >>> factory MarowakCallForFamily_CheckDeckAndPlayArea */
CheckIfDeckIsEmptyResult MarowakCallForFamily_CheckDeckAndPlayArea(void);
/* <<< factory MarowakCallForFamily_CheckDeckAndPlayArea */
/* >>> factory IceBreath_ZeroDamage */
uint8_t IceBreath_ZeroDamage(void);
/* <<< factory IceBreath_ZeroDamage */
/* >>> factory AIPickFireEnergyCardToDiscard */
void AIPickFireEnergyCardToDiscard(void);
/* <<< factory AIPickFireEnergyCardToDiscard */
/* >>> factory FlamesOfRage_AIEffect */
void FlamesOfRage_AIEffect(void);
/* <<< factory FlamesOfRage_AIEffect */
/* >>> factory ArcanineFlamethrower_AISelectEffect */
void ArcanineFlamethrower_AISelectEffect(void);
/* <<< factory ArcanineFlamethrower_AISelectEffect */
/* >>> factory FlamesOfRage_AISelectEffect */
void FlamesOfRage_AISelectEffect(void);
/* <<< factory FlamesOfRage_AISelectEffect */
/* >>> factory FireBlast_AISelectEffect */
void FireBlast_AISelectEffect(void);
/* <<< factory FireBlast_AISelectEffect */
/* >>> factory EnergyConversion_CheckEnergy */
typedef struct { uint16_t hl; uint8_t f; } EnergyConversionCheckEnergyResult;
EnergyConversionCheckEnergyResult EnergyConversion_CheckEnergy(void);
/* <<< factory EnergyConversion_CheckEnergy */
/* >>> factory EnergyConversion_AISelectEffect */
void EnergyConversion_AISelectEffect(void);
/* <<< factory EnergyConversion_AISelectEffect */
/* >>> factory HypnoDarkMind_AISelectEffect */
void HypnoDarkMind_AISelectEffect(void);
/* <<< factory HypnoDarkMind_AISelectEffect */
/* >>> factory AIPickAttackForAmnesia */
uint8_t AIPickAttackForAmnesia(void);
/* <<< factory AIPickAttackForAmnesia */
/* >>> factory MirrorMove_AISelection */
void MirrorMove_AISelection(void);
/* <<< factory MirrorMove_AISelection */
/* >>> factory KinglerFlail_HPCheck */
void KinglerFlail_HPCheck(void);
/* <<< factory KinglerFlail_HPCheck */
/* >>> factory MagikarpFlail_HPCheck */
void MagikarpFlail_HPCheck(void);
/* <<< factory MagikarpFlail_HPCheck */
/* >>> factory SuperFang_HalfHPEffect */
void SuperFang_HalfHPEffect(void);
/* <<< factory SuperFang_HalfHPEffect */
/* >>> factory KarateChop_DamageSubtractionEffect */
void KarateChop_DamageSubtractionEffect(void);
/* <<< factory KarateChop_DamageSubtractionEffect */
/* >>> factory SpearowMirrorMove_AISelection */
void SpearowMirrorMove_AISelection(void);
/* <<< factory SpearowMirrorMove_AISelection */
/* >>> factory CharmeleonFlamethrower_AISelectEffect */
/* poketcg/src/engine/duel/effect_functions.asm */

void AIPickFireEnergyCardToDiscard(void);
void CharmeleonFlamethrower_AISelectEffect(void);
/* <<< factory CharmeleonFlamethrower_AISelectEffect */
/* >>> factory ClefableMetronome_AISelectEffect */
void ClefableMetronome_AISelectEffect(void);
/* <<< factory ClefableMetronome_AISelectEffect */
/* >>> factory Ember_AISelectEffect */
/* poketcg/src/engine/duel/effect_functions.asm */

void AIPickFireEnergyCardToDiscard(void);
void Ember_AISelectEffect(void);
/* <<< factory Ember_AISelectEffect */
/* >>> factory FlareonFlamethrower_AISelectEffect */
/* poketcg/src/engine/duel/effect_functions.asm */

void AIPickFireEnergyCardToDiscard(void);
void FlareonFlamethrower_AISelectEffect(void);
/* <<< factory FlareonFlamethrower_AISelectEffect */
/* >>> factory DestinyBond_DestinyBondEffect */
uint16_t DestinyBond_DestinyBondEffect(void);
/* <<< factory DestinyBond_DestinyBondEffect */
/* >>> factory FlareonRage_AIEffect */
void FlareonRage_AIEffect(void);
/* <<< factory FlareonRage_AIEffect */
/* >>> factory GolduckHyperBeam_AISelectEffect */
void GolduckHyperBeam_AISelectEffect(void);
/* <<< factory GolduckHyperBeam_AISelectEffect */
/* >>> factory OnixHardenEffect */
uint16_t OnixHardenEffect(void);
/* <<< factory OnixHardenEffect */
/* >>> factory PoliwhirlAmnesia_AISelectEffect */
void PoliwhirlAmnesia_AISelectEffect(void);
/* <<< factory PoliwhirlAmnesia_AISelectEffect */
/* >>> factory StretchKick_AISelectEffect */
void StretchKick_AISelectEffect(void);
/* <<< factory StretchKick_AISelectEffect */
/* >>> factory VaporeonWaterGunEffect */
void VaporeonWaterGunEffect(void);
/* <<< factory VaporeonWaterGunEffect */
/* >>> factory Potion_DamageCheck */
typedef struct { uint8_t f; uint16_t hl; } PotionDamageCheckResult;
PotionDamageCheckResult Potion_DamageCheck(void);
/* <<< factory Potion_DamageCheck */
/* >>> factory CloysterSpikeCannon_AIEffect */
void CloysterSpikeCannon_AIEffect(void);
/* <<< factory CloysterSpikeCannon_AIEffect */
/* >>> factory JolteonDoubleKick_AIEffect */
void JolteonDoubleKick_AIEffect(void);
/* <<< factory JolteonDoubleKick_AIEffect */
/* >>> factory RapidashStomp_AIEffect */
void RapidashStomp_AIEffect(void);
/* <<< factory RapidashStomp_AIEffect */
/* >>> factory StoneBarrage_AIEffect */
void StoneBarrage_AIEffect(void);
/* <<< factory StoneBarrage_AIEffect */
/* >>> factory DestinyBond_AISelectEffect */
void DestinyBond_AISelectEffect(void);
/* <<< factory DestinyBond_AISelectEffect */
/* >>> factory Rampage_AIEffect */
void Rampage_AIEffect(void);
/* <<< factory Rampage_AIEffect */
/* >>> factory SuperPotion_DamageEnergyCheck */
typedef struct { uint8_t f; uint16_t hl; } SuperPotionDamageEnergyCheckResult;
SuperPotionDamageEnergyCheckResult SuperPotion_DamageEnergyCheck(void);
/* <<< factory SuperPotion_DamageEnergyCheck */
/* >>> factory KrabbyCallForFamily_CheckDeckAndPlayArea */
CheckIfDeckIsEmptyResult KrabbyCallForFamily_CheckDeckAndPlayArea(void);
/* <<< factory KrabbyCallForFamily_CheckDeckAndPlayArea */
/* >>> factory Revive_BenchCheck */
typedef struct { uint8_t f; uint16_t hl; } ReviveBenchCheckResult;
ReviveBenchCheckResult Revive_BenchCheck(void);
/* <<< factory Revive_BenchCheck */
/* >>> factory DragonairHyperBeam_DiscardEffect */
uint16_t DragonairHyperBeam_DiscardEffect(uint16_t hl);
/* <<< factory DragonairHyperBeam_DiscardEffect */
/* >>> factory MirrorMove_ExecuteStatusEffect */
typedef struct { uint8_t f; } MirrorMoveExecuteStatusEffectResult;
MirrorMoveExecuteStatusEffectResult MirrorMove_ExecuteStatusEffect(uint8_t a);
/* <<< factory MirrorMove_ExecuteStatusEffect */
/* >>> factory Curse_CheckDamageAndBench */
typedef struct { uint8_t f; uint16_t hl; } CurseCheckDamageAndBenchResult;
CurseCheckDamageAndBenchResult Curse_CheckDamageAndBench(void);
/* <<< factory Curse_CheckDamageAndBench */
/* >>> factory SpearowMirrorMove_AIEffect */
void SpearowMirrorMove_AIEffect(void);
/* <<< factory SpearowMirrorMove_AIEffect */
/* >>> factory SpearowMirrorMove_InitialEffect1 */
MirrorMoveInitialEffect1Result SpearowMirrorMove_InitialEffect1(void);
/* <<< factory SpearowMirrorMove_InitialEffect1 */
/* >>> factory PidgeottoMirrorMove_AIEffect */
void PidgeottoMirrorMove_AIEffect(void);
/* <<< factory PidgeottoMirrorMove_AIEffect */
/* >>> factory PidgeottoMirrorMove_AISelection */
void PidgeottoMirrorMove_AISelection(void);
/* <<< factory PidgeottoMirrorMove_AISelection */
/* >>> factory ClefairyMetronome_AISelectEffect */
void ClefairyMetronome_AISelectEffect(void);
/* <<< factory ClefairyMetronome_AISelectEffect */
/* >>> factory EnergySpike_DeckCheck */
CheckIfDeckIsEmptyResult EnergySpike_DeckCheck(void);
/* <<< factory EnergySpike_DeckCheck */
/* >>> factory MagmarFlamethrower_AISelectEffect */
/* poketcg/src/engine/duel/effect_functions.asm */

void AIPickFireEnergyCardToDiscard(void);
void MagmarFlamethrower_AISelectEffect(void);
/* <<< factory MagmarFlamethrower_AISelectEffect */
/* >>> factory OmastarWaterGunEffect */
void OmastarWaterGunEffect(void);
/* <<< factory OmastarWaterGunEffect */
/* >>> factory CuboneRage_AIEffect */
void CuboneRage_AIEffect(void);
/* <<< factory CuboneRage_AIEffect */
/* >>> factory GravelerHardenEffect */
uint16_t GravelerHardenEffect(void);
/* <<< factory GravelerHardenEffect */
/* >>> factory KarateChop_AIEffect */
void KarateChop_AIEffect(void);
/* <<< factory KarateChop_AIEffect */
/* >>> factory LaprasWaterGunEffect */
void LaprasWaterGunEffect(void);
/* <<< factory LaprasWaterGunEffect */
/* >>> factory OmanyteWaterGunEffect */
void OmanyteWaterGunEffect(void);
/* <<< factory OmanyteWaterGunEffect */
/* >>> factory PoliwrathWaterGunEffect */
void PoliwrathWaterGunEffect(void);
/* <<< factory PoliwrathWaterGunEffect */
/* >>> factory SeadraWaterGunEffect */
void SeadraWaterGunEffect(void);
/* <<< factory SeadraWaterGunEffect */
/* >>> factory SuperFang_AIEffect */
void SuperFang_AIEffect(void);
/* <<< factory SuperFang_AIEffect */
/* >>> factory DragoniteLv41Slam_AIEffect */
void DragoniteLv41Slam_AIEffect(void);
/* <<< factory DragoniteLv41Slam_AIEffect */
/* >>> factory ElectabuzzQuickAttack_AIEffect */
void ElectabuzzQuickAttack_AIEffect(void);
/* <<< factory ElectabuzzQuickAttack_AIEffect */
/* >>> factory JolteonQuickAttack_AIEffect */
void JolteonQuickAttack_AIEffect(void);
/* <<< factory JolteonQuickAttack_AIEffect */
/* >>> factory LeekSlap_AIEffect */
void LeekSlap_AIEffect(void);
/* <<< factory LeekSlap_AIEffect */
/* >>> factory PinMissile_AIEffect */
void PinMissile_AIEffect(void);
/* <<< factory PinMissile_AIEffect */
/* >>> factory SandslashFurySwipes_AIEffect */
void SandslashFurySwipes_AIEffect(void);
/* <<< factory SandslashFurySwipes_AIEffect */
/* >>> factory Thunderpunch_AIEffect */
void Thunderpunch_AIEffect(void);
/* <<< factory Thunderpunch_AIEffect */
/* >>> factory StarmieRecover_AISelectEffect */
typedef struct { uint8_t a; uint8_t f; } StarmieRecoverAISelectEffectResult;
StarmieRecoverAISelectEffectResult StarmieRecover_AISelectEffect(void);
/* <<< factory StarmieRecover_AISelectEffect */
/* >>> factory BellsproutCallForFamily_CheckDeckAndPlayArea */
typedef struct { uint8_t a; uint16_t hl; uint8_t f; } BellsproutCallForFamilyCheckDeckAndPlayAreaResult;
BellsproutCallForFamilyCheckDeckAndPlayAreaResult BellsproutCallForFamily_CheckDeckAndPlayArea(void);
/* <<< factory BellsproutCallForFamily_CheckDeckAndPlayArea */
/* >>> factory Spark_AISelectEffect */
typedef struct { uint8_t a; } SparkAISelectEffectResult;
SparkAISelectEffectResult Spark_AISelectEffect(void);
/* <<< factory Spark_AISelectEffect */
/* >>> factory DamageSwap_CheckDamage */
typedef struct { uint8_t f; uint16_t hl; } DamageSwapCheckDamageResult;
DamageSwapCheckDamageResult DamageSwap_CheckDamage(void);
/* <<< factory DamageSwap_CheckDamage */
/* >>> factory PokemonFlute_BenchCheck */
typedef struct { uint8_t f; uint16_t hl; } PokemonFluteBenchCheckResult;
PokemonFluteBenchCheckResult PokemonFlute_BenchCheck(void);
/* <<< factory PokemonFlute_BenchCheck */
/* >>> factory Heal_OncePerTurnCheck */
typedef struct { uint8_t f; uint16_t hl; } HealOncePerTurnCheckResult;
HealOncePerTurnCheckResult Heal_OncePerTurnCheck(void);
/* <<< factory Heal_OncePerTurnCheck */
/* >>> factory Shift_ChangeColorEffect */
typedef struct { uint8_t f; } Shift_ChangeColorEffectResult;
Shift_ChangeColorEffectResult Shift_ChangeColorEffect(uint8_t d, uint8_t e);
/* <<< factory Shift_ChangeColorEffect */
/* >>> factory MagikarpFlail_AIEffect */
void MagikarpFlail_AIEffect(void);
/* <<< factory MagikarpFlail_AIEffect */
/* >>> factory PoliwagWaterGunEffect */
void PoliwagWaterGunEffect(void);
/* <<< factory PoliwagWaterGunEffect */
/* >>> factory TaurosStomp_AIEffect */
void TaurosStomp_AIEffect(void);
/* <<< factory TaurosStomp_AIEffect */
/* >>> factory DodrioRage_AIEffect */
void DodrioRage_AIEffect(void);
/* <<< factory DodrioRage_AIEffect */
/* >>> factory DragoniteLv45Slam_AIEffect */
void DragoniteLv45Slam_AIEffect(void);
/* <<< factory DragoniteLv45Slam_AIEffect */
/* >>> factory GengarDarkMind_AISelectEffect */
void GengarDarkMind_AISelectEffect(void);
/* <<< factory GengarDarkMind_AISelectEffect */
/* >>> factory PoliwhirlDoubleslap_AIEffect */
void PoliwhirlDoubleslap_AIEffect(void);
/* <<< factory PoliwhirlDoubleslap_AIEffect */
/* >>> factory KinglerFlail_AIEffect */
void KinglerFlail_AIEffect(void);
/* <<< factory KinglerFlail_AIEffect */
/* >>> factory JynxDoubleslap_AIEffect */
void JynxDoubleslap_AIEffect(void);
/* <<< factory JynxDoubleslap_AIEffect */
/* >>> factory Bonemerang_AIEffect */
void Bonemerang_AIEffect(void);
/* <<< factory Bonemerang_AIEffect */
/* >>> factory Barrier_BarrierEffect */
void Barrier_BarrierEffect(void);
/* <<< factory Barrier_BarrierEffect */
/* >>> factory HydroPumpEffect */
void HydroPumpEffect(void);
/* <<< factory HydroPumpEffect */
/* >>> factory MysteryAttack_AIEffect */
void MysteryAttack_AIEffect(void);
/* <<< factory MysteryAttack_AIEffect */
/* >>> factory HurricaneEffect */
QueueStatusConditionResult HurricaneEffect(uint16_t hl);
/* <<< factory HurricaneEffect */
/* >>> factory Psychic_AIEffect */
void Psychic_AIEffect(void);
/* <<< factory Psychic_AIEffect */
/* >>> factory SlowpokeAmnesia_AISelectEffect */
void SlowpokeAmnesia_AISelectEffect(void);
/* <<< factory SlowpokeAmnesia_AISelectEffect */
/* >>> factory KadabraRecover_AISelectEffect */
void KadabraRecover_AISelectEffect(void);
/* <<< factory KadabraRecover_AISelectEffect */
/* >>> factory GolduckHyperBeam_DiscardEffect */
uint16_t GolduckHyperBeam_DiscardEffect(uint16_t hl);
/* <<< factory GolduckHyperBeam_DiscardEffect */
/* >>> factory StrangeBehavior_CheckDamage */
typedef struct { uint8_t f; uint16_t hl; } StrangeBehavior_CheckDamageResult;
StrangeBehavior_CheckDamageResult StrangeBehavior_CheckDamage(void);
/* <<< factory StrangeBehavior_CheckDamage */
/* >>> factory EnergyTrans_PrintProcedure */
void EnergyTrans_PrintProcedure(void);
/* <<< factory EnergyTrans_PrintProcedure */
/* >>> factory ItemFinder_HandDiscardPileCheck */
typedef struct { uint8_t f; uint16_t hl; } ItemFinder_HandDiscardPileCheckResult;
ItemFinder_HandDiscardPileCheckResult ItemFinder_HandDiscardPileCheck(void);
/* <<< factory ItemFinder_HandDiscardPileCheck */
/* >>> factory Wildfire_DiscardEnergyEffect */
void Wildfire_DiscardEnergyEffect(void);
/* <<< factory Wildfire_DiscardEnergyEffect */
/* >>> factory SuperEnergyRemoval_EnergyCheck */
typedef struct { uint8_t f; uint16_t hl; } SuperEnergyRemoval_EnergyCheckResult;
SuperEnergyRemoval_EnergyCheckResult SuperEnergyRemoval_EnergyCheck(void);
/* <<< factory SuperEnergyRemoval_EnergyCheck */
/* >>> factory MorphEffect */
void MorphEffect(void);
/* <<< factory MorphEffect */
/* >>> factory AISelectConversionColor */
void AISelectConversionColor(void);
/* <<< factory AISelectConversionColor */
/* >>> factory PrintArenaCardNameAndColorText */
TextResult PrintArenaCardNameAndColorText(uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PrintArenaCardNameAndColorText */
/* >>> factory Conversion1_AISelectEffect */
void Conversion1_AISelectEffect(void);
/* <<< factory Conversion1_AISelectEffect */
/* >>> factory Conversion2_ChangeResistanceEffect */
TextResult Conversion2_ChangeResistanceEffect(uint8_t d, uint8_t e);
/* <<< factory Conversion2_ChangeResistanceEffect */
/* >>> factory Conversion2_AISelectEffect */
void Conversion2_AISelectEffect(void);
/* <<< factory Conversion2_AISelectEffect */
/* >>> factory MirrorMove_AfterDamage */
TextResult MirrorMove_AfterDamage(uint8_t d, uint8_t e, uint16_t hl_in);
/* <<< factory MirrorMove_AfterDamage */
/* >>> factory PidgeottoMirrorMove_AfterDamage */
TextResult PidgeottoMirrorMove_AfterDamage(uint8_t d, uint8_t e, uint16_t hl_in);
/* <<< factory PidgeottoMirrorMove_AfterDamage */
/* >>> factory SpearowMirrorMove_AfterDamage */
TextResult SpearowMirrorMove_AfterDamage(uint8_t d, uint8_t e, uint16_t hl_in);
/* <<< factory SpearowMirrorMove_AfterDamage */
/* >>> factory Func_2c0a8 */
uint8_t Func_2c0a8(void);
/* <<< factory Func_2c0a8 */
/* >>> factory ShuffleCardsInDeck */
typedef struct { uint8_t a; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint8_t f; uint16_t hl; } ShuffleCardsInDeckResult;
ShuffleCardsInDeckResult ShuffleCardsInDeck(uint8_t b, uint8_t c, uint16_t de, uint16_t hl);
/* <<< factory ShuffleCardsInDeck */
/* >>> factory DrawPlayAreaScreenToShowChanges */
void DrawPlayAreaScreenToShowChanges(uint8_t a);
/* <<< factory DrawPlayAreaScreenToShowChanges */
/* >>> factory EnergyRemoval_DiscardEffect */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } EnergyRemovalDiscardEffectResult;
EnergyRemovalDiscardEffectResult EnergyRemoval_DiscardEffect(void);
/* <<< factory EnergyRemoval_DiscardEffect */
/* >>> factory SuperEnergyRemoval_DiscardEffect */
void SuperEnergyRemoval_DiscardEffect(void);
/* <<< factory SuperEnergyRemoval_DiscardEffect */
/* >>> factory EnergyTrans_AIEffect */
void EnergyTrans_AIEffect(void);
/* <<< factory EnergyTrans_AIEffect */
/* >>> factory StrangeBehavior_SwapEffect */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } StrangeBehaviorSwapEffectResult;
StrangeBehaviorSwapEffectResult StrangeBehavior_SwapEffect(void);
/* <<< factory StrangeBehavior_SwapEffect */
/* >>> factory Defender_AttachDefenderEffect */
typedef struct { uint8_t f; } DefenderAttachDefenderEffectResult;
DefenderAttachDefenderEffectResult Defender_AttachDefenderEffect(void);
/* <<< factory Defender_AttachDefenderEffect */
/* >>> factory DamageSwap_SwapEffect */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } DamageSwap_SwapEffectResult;
DamageSwap_SwapEffectResult DamageSwap_SwapEffect(void);
/* <<< factory DamageSwap_SwapEffect */
/* >>> factory PrintDevolvedCardNameAndLevelText */
void PrintDevolvedCardNameAndLevelText(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory PrintDevolvedCardNameAndLevelText */
/* >>> factory ApplySubstatus2ToDefendingCard */
uint16_t ApplySubstatus2ToDefendingCard(uint8_t a, uint16_t hl);
/* <<< factory ApplySubstatus2ToDefendingCard */
/* >>> factory ApplyAmnesiaToAttack */
void ApplyAmnesiaToAttack(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory ApplyAmnesiaToAttack */
/* >>> factory MirrorMove_BeforeDamage */
void MirrorMove_BeforeDamage(void);
/* <<< factory MirrorMove_BeforeDamage */
/* >>> factory SpearowMirrorMove_BeforeDamage */
void SpearowMirrorMove_BeforeDamage(void);
/* <<< factory SpearowMirrorMove_BeforeDamage */
/* >>> factory PidgeottoMirrorMove_BeforeDamage */
void PidgeottoMirrorMove_BeforeDamage(void);
/* <<< factory PidgeottoMirrorMove_BeforeDamage */
#endif /* POKETCG_HOME_EFFECT_FUNCTIONS_H */
/* >>> factory Barrier_DiscardEffect */
uint8_t Barrier_DiscardEffect(void);
/* <<< factory Barrier_DiscardEffect */
/* >>> factory DestinyBond_DiscardEffect */
void DestinyBond_DiscardEffect(void);
/* <<< factory DestinyBond_DiscardEffect */
/* >>> factory Ember_DiscardEffect */
void Ember_DiscardEffect(void);
/* <<< factory Ember_DiscardEffect */
/* >>> factory FireBlast_DiscardEffect */
void FireBlast_DiscardEffect(void);
/* <<< factory FireBlast_DiscardEffect */
/* >>> factory FireSpin_AISelectEffect */
void FireSpin_AISelectEffect(void);
/* <<< factory FireSpin_AISelectEffect */
/* >>> factory FireSpin_DiscardEffect */
void FireSpin_DiscardEffect(void);
/* <<< factory FireSpin_DiscardEffect */