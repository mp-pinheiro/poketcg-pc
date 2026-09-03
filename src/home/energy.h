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
/* energy.asm relative :61-159. Five exits, every one derivable: the two
 * `ret nc` paths take their callee's a/f, `.play_energy_card` takes
 * AIMakeDecision's a with the trailing `scf`, and the two `or a` exits
 * leave the wTempAI and wSelectedAttack bytes they tested. */
typedef struct { uint8_t a; uint8_t f; } AITryToPlayEnergyCardResult;
AITryToPlayEnergyCardResult AITryToPlayEnergyCard(void);
/* <<< factory AITryToPlayEnergyCard */
/* >>> factory DetermineAIScoreOfAttackEnergyRequirement */
void DetermineAIScoreOfAttackEnergyRequirement(uint8_t a);
/* <<< factory DetermineAIScoreOfAttackEnergyRequirement */
/* >>> factory AIProcessEnergyCards */
/* energy.asm:265-285. Only `f` is modelled: the carry is set on the
 * `.play_energy_card` tail and clear on every other exit, and `a` at exit
 * differs per path with no consumer. */
/* `a` is the wAIEnergyAttachLogicFlags byte the `or a` tests read -- zero on
 * the no-flags exit -- or AITryToPlayEnergyCard's on the play path. */
typedef struct { uint8_t a; uint8_t f; } AIEnergyResult;
AIEnergyResult AIProcessEnergyCards(void);
/* <<< factory AIProcessEnergyCards */
/* >>> factory AIProcessAndTryToPlayEnergy */
void AIProcessAndTryToPlayEnergy(void);
/* <<< factory AIProcessAndTryToPlayEnergy */
/* >>> factory AIProcessButDontPlayEnergy_SkipEvolution */
AIEnergyResult AIProcessButDontPlayEnergy_SkipEvolution(void);
/* <<< factory AIProcessButDontPlayEnergy_SkipEvolution */
/* >>> factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena */
AIEnergyResult AIProcessButDontPlayEnergy_SkipEvolutionAndArena(void);
/* <<< factory AIProcessButDontPlayEnergy_SkipEvolutionAndArena */
/* >>> factory Func_16488 */
void Func_16488(void);
/* <<< factory Func_16488 */
#endif /* POKETCG_HOME_ENERGY_H */
