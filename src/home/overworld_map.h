#ifndef POKETCG_HOME_OVERWORLD_MAP_H
#define POKETCG_HOME_OVERWORLD_MAP_H

#include <stdint.h>

/* >>> factory OverworldMap_ContinuePlayerWalkingAnimation */
void OverworldMap_ContinuePlayerWalkingAnimation(void);
/* <<< factory OverworldMap_ContinuePlayerWalkingAnimation */
/* >>> factory OverworldMap_NegateBC */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} OverworldMapNegateBCResult;
OverworldMapNegateBCResult OverworldMap_NegateBC(uint8_t b, uint8_t c);
/* <<< factory OverworldMap_NegateBC */
#endif /* POKETCG_HOME_OVERWORLD_MAP_H */
