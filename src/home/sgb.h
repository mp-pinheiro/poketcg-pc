#ifndef POKETCG_HOME_SGB_H
#define POKETCG_HOME_SGB_H

#include <stdint.h>

typedef struct {
	uint8_t a, f, b, c, d, e;
} SGBWaitResult;

SGBWaitResult Wait(uint16_t bc);

/* >>> factory SendSGB */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
} SendSGBResult;

SendSGBResult SendSGB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory SendSGB */
/* >>> factory InitSGB */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
} InitSGBResult;

InitSGBResult InitSGB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory InitSGB */
/* >>> factory DetectSGB */
typedef struct {
	uint8_t a, f, b, c, d, e;
	uint16_t hl;
} DetectSGBResult;

DetectSGBResult DetectSGB(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DetectSGB */
#endif /* POKETCG_HOME_SGB_H */
