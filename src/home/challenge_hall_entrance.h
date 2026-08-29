#ifndef POKETCG_HOME_CHALLENGE_HALL_ENTRANCE_H
#define POKETCG_HOME_CHALLENGE_HALL_ENTRANCE_H

#include <stdint.h>

/* >>> factory Preload_Clerk9 */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} PreloadClerk9Result;

PreloadClerk9Result Preload_Clerk9(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory Preload_Clerk9 */
#endif /* POKETCG_HOME_CHALLENGE_HALL_ENTRANCE_H */
