#ifndef POKETCG_HOME_EFFECT_FUNCTIONS_H
#define POKETCG_HOME_EFFECT_FUNCTIONS_H

#include <stdint.h>

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
/* >>> factory GetNextPositionInTempList */
uint16_t GetNextPositionInTempList(void);
/* <<< factory GetNextPositionInTempList */
/* >>> factory QueueStatusCondition */
typedef struct { uint8_t f; } QueueStatusConditionResult;
QueueStatusConditionResult QueueStatusCondition(uint8_t b, uint8_t c);
/* <<< factory QueueStatusCondition */
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
void ApplyExtraWaterEnergyDamageBonus(void);
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
#endif /* POKETCG_HOME_EFFECT_FUNCTIONS_H */
