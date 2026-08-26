#ifndef POKETCG_HOME_RETREAT_H
#define POKETCG_HOME_RETREAT_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} SetAIRetreatFlagsResult;

SetAIRetreatFlagsResult SetAIRetreatFlags(void);

/* >>> factory AITryToRetreat */
/* engine/duel/ai/retreat.asm:775-1012. a/f only: b, c, d, e and hl are list-walk
 * residue on every path that reaches the energy-discard loops. */
typedef struct {
	uint8_t a;
	uint8_t f;
} AITryToRetreatResult;
AITryToRetreatResult AITryToRetreat(uint8_t entry_a, uint8_t entry_f);
/* <<< factory AITryToRetreat */
#endif /* POKETCG_HOME_RETREAT_H */
