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
/* >>> factory SetNPCOpponentNameAndPortrait */
void SetNPCOpponentNameAndPortrait(uint8_t a);
/* <<< factory SetNPCOpponentNameAndPortrait */
/* >>> factory GetNPCNameAndScript */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} GetNPCNameAndScriptResult;

GetNPCNameAndScriptResult GetNPCNameAndScript(uint8_t a);
/* <<< factory GetNPCNameAndScript */
#endif /* POKETCG_HOME_NPC_DATA_H */
