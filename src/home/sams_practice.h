#ifndef POKETCG_HOME_SAMS_PRACTICE_H
#define POKETCG_HOME_SAMS_PRACTICE_H

#include <stdint.h>

typedef struct {
	uint8_t a, b, c, d, e, f;
	uint16_t hl;
} SamsPracticeResult;

typedef struct {
	uint8_t a, f;
} IsAIPracticeScriptedTurnResult;

IsAIPracticeScriptedTurnResult IsAIPracticeScriptedTurn(void);
SamsPracticeResult SetSamsStartingPlayArea(uint8_t c, uint8_t b, uint8_t d,
                                           uint8_t e, uint16_t hl);

#endif
