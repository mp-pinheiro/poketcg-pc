#ifndef POKETCG_HOME_DEBUG_H
#define POKETCG_HOME_DEBUG_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} DebugSGBFrameResult;

typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t d;
	uint8_t e;
} DebugStandardBGCharacterResult;

typedef struct {
	uint8_t a;
	uint8_t f;
} DebugQuitResult;

DebugSGBFrameResult DebugSGBFrame(uint8_t b, uint8_t c, uint8_t d,
	uint8_t e, uint16_t hl);
DebugStandardBGCharacterResult DebugStandardBGCharacter(uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl);
DebugQuitResult DebugQuit(uint8_t a, uint8_t f);

/* >>> factory UnreferencedFillVRAMWithRandomData */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} UnreferencedFillVRAMWithRandomDataResult;

UnreferencedFillVRAMWithRandomDataResult UnreferencedFillVRAMWithRandomData(void);
/* <<< factory UnreferencedFillVRAMWithRandomData */
/* >>> factory _DebugVEffect */
void _DebugVEffect(void);
/* <<< factory _DebugVEffect */
#endif
