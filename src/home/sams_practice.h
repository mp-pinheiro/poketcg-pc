#ifndef POKETCG_HOME_SAMS_PRACTICE_H
#define POKETCG_HOME_SAMS_PRACTICE_H

#include <stdint.h>

typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
} SamsPracticeResult;

SamsPracticeResult IsAIPracticeScriptedTurn(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl);

SamsPracticeResult SetSamsStartingPlayArea(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl);

/* >>> factory GetPlayAreaLocationOfRaticateOrRattata */
void GetPlayAreaLocationOfRaticateOrRattata(void);
/* <<< factory GetPlayAreaLocationOfRaticateOrRattata */
#endif
