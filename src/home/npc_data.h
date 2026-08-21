#ifndef POKETCG_HOME_NPC_DATA_H
#define POKETCG_HOME_NPC_DATA_H

#include <stdint.h>

/* >>> factory GetNPCHeaderPointer */
typedef struct {
	uint16_t hl;
	uint8_t a;
	uint8_t f;
} GetNPCHeaderPointerResult;

GetNPCHeaderPointerResult GetNPCHeaderPointer(uint8_t a);
/* <<< factory GetNPCHeaderPointer */
#endif /* POKETCG_HOME_NPC_DATA_H */
