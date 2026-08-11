#ifndef POKETCG_HOME_RETREAT_H
#define POKETCG_HOME_RETREAT_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} SetAIRetreatFlagsResult;

SetAIRetreatFlagsResult SetAIRetreatFlags(void);

#endif /* POKETCG_HOME_RETREAT_H */
