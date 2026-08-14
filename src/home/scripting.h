#ifndef POKETCG_HOME_SCRIPTING_H
#define POKETCG_HOME_SCRIPTING_H

#include <stdint.h>

/* >>> factory IncreaseScriptPointer */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t c;
} IncreaseScriptPointerResult;

IncreaseScriptPointerResult IncreaseScriptPointer(uint8_t a);
/* <<< factory IncreaseScriptPointer */

/* >>> factory SetScriptPointer */
uint16_t SetScriptPointer(uint16_t bc);
/* <<< factory SetScriptPointer */

/* >>> factory GetScriptArgsAfterPointer */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} GetScriptArgsAfterPointerResult;

GetScriptArgsAfterPointerResult GetScriptArgsAfterPointer(uint8_t a);
/* <<< factory GetScriptArgsAfterPointer */

/* >>> factory GetEventVar */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} GetEventVarResult;

GetEventVarResult GetEventVar(uint8_t a, uint8_t f, uint8_t b, uint8_t c);
/* <<< factory GetEventVar */

#endif
