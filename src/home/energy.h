#ifndef POKETCG_HOME_ENERGY_H
#define POKETCG_HOME_ENERGY_H

#include <stdint.h>

/* >>> factory RetrievePlayAreaAIScoreFromBackup1 */
typedef struct { uint16_t de, hl; } Backup1Result;
Backup1Result RetrievePlayAreaAIScoreFromBackup1(void);
/* <<< factory RetrievePlayAreaAIScoreFromBackup1 */
/* >>> factory FindPlayAreaCardWithHighestAIScore */
typedef struct { uint8_t a, f, b, c, d, e; uint16_t hl; } AIScoreResult;
AIScoreResult FindPlayAreaCardWithHighestAIScore(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory FindPlayAreaCardWithHighestAIScore */
/* >>> factory CheckSpecificDecksToAttachDoubleColorless */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CheckSpecificDecksToAttachDoubleColorlessResult;
CheckSpecificDecksToAttachDoubleColorlessResult CheckSpecificDecksToAttachDoubleColorless(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckSpecificDecksToAttachDoubleColorless */
/* >>> factory GetEnergyCardForDiscardOrEnergyBoostAttack */
typedef struct { uint8_t a; uint8_t b; uint8_t c; uint8_t e; uint8_t f; } GetEnergyCardForDiscardOrEnergyBoostAttackResult;
GetEnergyCardForDiscardOrEnergyBoostAttackResult GetEnergyCardForDiscardOrEnergyBoostAttack(uint8_t c);
/* <<< factory GetEnergyCardForDiscardOrEnergyBoostAttack */
/* >>> factory CheckIfEvolutionNeedsEnergyForAttack */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CheckIfEvolutionNeedsEnergyForAttackResult;
CheckIfEvolutionNeedsEnergyForAttackResult CheckIfEvolutionNeedsEnergyForAttack(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckIfEvolutionNeedsEnergyForAttack */
/* >>> factory AITryToPlayEnergyCard */
uint8_t AITryToPlayEnergyCard(void);
/* <<< factory AITryToPlayEnergyCard */
/* >>> factory DetermineAIScoreOfAttackEnergyRequirement */
void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a);
/* <<< factory DetermineAIScoreOfAttackEnergyRequirement */
/* >>> factory AIProcessEnergyCards */
void AIProcessEnergyCards(void);
/* <<< factory AIProcessEnergyCards */
/* >>> factory AIProcessAndTryToPlayEnergy */
void AIProcessAndTryToPlayEnergy(void);
/* <<< factory AIProcessAndTryToPlayEnergy */
/* >>> factory AIProcessButDontPlayEnergy_SkipEvolution */
/* >>> factory AIProcessButDontPlayEnergy_SkipEvolution */
void AIProcessButDontPlayEnergy_SkipEvolution(void);
/* <<< factory AIProcessButDontPlayEnergy_SkipEvolution */
/* >>> factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena */
void AIProcessButDontPlayEnergy_SkipEvolutionAndArena(void);
/* <<< factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena */
/* >>> factory Func_16488 */
void Func_16488(void);
/* <<< factory Func_16488 */
#endif /* POKETCG_HOME_ENERGY_H */
