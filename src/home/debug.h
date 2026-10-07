#ifndef POKETCG_HOME_DEBUG_H
#define POKETCG_HOME_DEBUG_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part DebugSGBFrameResult */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} DebugSGBFrameResult;
/* <<< part DebugSGBFrameResult */

/* >>> part DebugStandardBGCharacterResult */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t d;
	uint8_t e;
} DebugStandardBGCharacterResult;
/* <<< part DebugStandardBGCharacterResult */

/* >>> part DebugQuitResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} DebugQuitResult;
/* <<< part DebugQuitResult */

/* >>> factory DebugSGBFrame */
DebugSGBFrameResult DebugSGBFrame(uint8_t b, uint8_t c, uint8_t d,
	uint8_t e, uint16_t hl);
/* <<< factory DebugSGBFrame */
/* >>> factory DebugStandardBGCharacter */
DebugStandardBGCharacterResult DebugStandardBGCharacter(uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DebugStandardBGCharacter */
/* >>> factory DebugQuit */
DebugQuitResult DebugQuit(uint8_t a, uint8_t f);
/* <<< factory DebugQuit */

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
/* >>> factory Func_80c64 */
void Func_80c64(void);
/* <<< factory Func_80c64 */
/* >>> factory DebugVEffect */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} DebugVEffectResult;

DebugVEffectResult DebugVEffect(uint8_t a, uint8_t f, uint8_t b,
	uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DebugVEffect */
/* >>> factory DebugCGBTest */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} DebugCGBTestResult;

DebugCGBTestResult DebugCGBTest(uint8_t a, uint8_t f, uint8_t b,
	uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DebugCGBTest */
/* >>> factory DebugCreateBoosterPack */
void DebugCreateBoosterPack(void);
/* <<< factory DebugCreateBoosterPack */
/* >>> factory DebugCredits */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } DebugCreditsResult;
DebugCreditsResult DebugCredits(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DebugCredits */
/* >>> factory _DebugLookAtSprite */
void _DebugLookAtSprite(void);
/* <<< factory _DebugLookAtSprite */
/* >>> factory DebugLookAtSprite */
void DebugLookAtSprite(void);
/* <<< factory DebugLookAtSprite */
/* >>> factory DebugDuelMode */
typedef struct {
	uint8_t a;
	uint8_t f;
} DebugDuelModeResult;

DebugDuelModeResult DebugDuelMode(void);
/* <<< factory DebugDuelMode */
#endif
