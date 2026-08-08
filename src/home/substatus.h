#ifndef POKETCG_HOME_SUBSTATUS_H
#define POKETCG_HOME_SUBSTATUS_H

#include <stdint.h>

/* poketcg/src/home/substatus.asm */

typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t de;
	uint16_t hl;
} SandAttackCheckResult;

SandAttackCheckResult CheckSandAttackOrSmokescreenSubstatus(uint16_t de);

#endif
