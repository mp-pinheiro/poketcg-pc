#ifndef HOME_ATTACKS_H
#define HOME_ATTACKS_H

void RetrievePlayAreaAIScoreFromBackup2(void);

/* >>> factory GetAIScoreOfAttack */
void GetAIScoreOfAttack(unsigned char a);
/* <<< factory GetAIScoreOfAttack */
/* >>> factory AIProcessAttacks */
/* ai/attacks.asm:52-116. `a` is the wAIExecuteProcessedAttack byte the two
 * flag tests read -- zero on the failed exit -- or AITryUseAttack's on the
 * use-attack exit. */
typedef struct { unsigned char a; unsigned char f; } AIProcessAttacksResult;
AIProcessAttacksResult AIProcessAttacks(void);
/* <<< factory AIProcessAttacks */
/* >>> factory AIProcessAndTryToUseAttack */
/* >>> factory AIProcessAndTryToUseAttack */
AIProcessAttacksResult AIProcessAndTryToUseAttack(void);
/* <<< factory AIProcessAndTryToUseAttack */
/* >>> factory AIProcessButDontUseAttack */
AIProcessAttacksResult AIProcessButDontUseAttack(void);
/* <<< factory AIProcessButDontUseAttack */
#endif
