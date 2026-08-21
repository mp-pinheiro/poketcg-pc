#ifndef POKETCG_HOME_SCENES_H
#define POKETCG_HOME_SCENES_H

#include <stdint.h>

/* >>> factory SetBoosterLogoOAM */
void SetBoosterLogoOAM(void);
/* <<< factory SetBoosterLogoOAM */
/* >>> factory _DrawPortrait */
void _DrawPortrait(void);
/* <<< factory _DrawPortrait */
/* >>> factory LoadScene_LoadSGBPacket */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} LoadScene_LoadSGBPacketResult;
LoadScene_LoadSGBPacketResult LoadScene_LoadSGBPacket(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory LoadScene_LoadSGBPacket */
#endif /* POKETCG_HOME_SCENES_H */
