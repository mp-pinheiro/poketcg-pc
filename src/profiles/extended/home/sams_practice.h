#ifndef POKETCG_HOME_SAMS_PRACTICE_H
#define POKETCG_HOME_SAMS_PRACTICE_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part SamsPracticeResult */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
} SamsPracticeResult;
/* <<< part SamsPracticeResult */

/* >>> factory IsAIPracticeScriptedTurn */
SamsPracticeResult IsAIPracticeScriptedTurn(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory IsAIPracticeScriptedTurn */

/* >>> factory SetSamsStartingPlayArea */
SamsPracticeResult SetSamsStartingPlayArea(uint8_t a, uint8_t f, uint8_t b,
						uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory SetSamsStartingPlayArea */

/* >>> factory GetPlayAreaLocationOfRaticateOrRattata */
void GetPlayAreaLocationOfRaticateOrRattata(void);
/* <<< factory GetPlayAreaLocationOfRaticateOrRattata */
/* >>> factory AIPerformScriptedTurn */
SamsPracticeResult AIPerformScriptedTurn(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory AIPerformScriptedTurn */
#endif
