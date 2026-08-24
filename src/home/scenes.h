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
/* >>> factory LoadScene_LoadCompressedSGBPacket */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} LoadScene_LoadCompressedSGBPacketResult;
LoadScene_LoadCompressedSGBPacketResult LoadScene_LoadCompressedSGBPacket(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory LoadScene_LoadCompressedSGBPacket */
/* >>> factory LoadScene_SetCardPopAttrBlk */
typedef struct { uint8_t a, f, b, c, d, e; uint16_t hl; } LoadScene_SetCardPopAttrBlkResult;
LoadScene_SetCardPopAttrBlkResult LoadScene_SetCardPopAttrBlk(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory LoadScene_SetCardPopAttrBlk */
/* >>> factory LoadScene_SetGameBoyPrinterAttrBlk */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} LoadScene_SetGameBoyPrinterAttrBlkResult;
LoadScene_SetGameBoyPrinterAttrBlkResult LoadScene_SetGameBoyPrinterAttrBlk(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory LoadScene_SetGameBoyPrinterAttrBlk */
/* >>> factory _LoadScene */
void _LoadScene(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory _LoadScene */
/* >>> factory LoadBoosterGfx */
uint8_t LoadBoosterGfx(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory LoadBoosterGfx */
#endif /* POKETCG_HOME_SCENES_H */
