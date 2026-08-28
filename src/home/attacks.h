#ifndef HOME_ATTACKS_H
#define HOME_ATTACKS_H

void RetrievePlayAreaAIScoreFromBackup2(void);

/* >>> factory GetAIScoreOfAttack */
void GetAIScoreOfAttack(unsigned char a);
/* <<< factory GetAIScoreOfAttack */
/* >>> factory AIProcessAttacks */
typedef struct { unsigned char f; } AIProcessAttacksResult;
AIProcessAttacksResult AIProcessAttacks(void);
/* <<< factory AIProcessAttacks */
/* >>> factory AIProcessAndTryToUseAttack */
/* >>> factory AIProcessAndTryToUseAttack */
AIProcessAttacksResult AIProcessAndTryToUseAttack(void);
/* <<< factory AIProcessAndTryToUseAttack */
#endif
