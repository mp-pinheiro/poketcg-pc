#ifndef POKETCG_SETUP_H
#define POKETCG_SETUP_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t b;
} DetectConsoleResult;

typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} SetupPalettesResult;

typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ZeroRAMResult;

void NoOp(void);
DetectConsoleResult DetectConsole(uint8_t a);
SetupPalettesResult SetupPalettes(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
uint16_t FillTileMap(void);
uint16_t SetupVRAM(void);
uint16_t SetupRegisters(void);
ZeroRAMResult ZeroRAM(void);

#endif /* POKETCG_SETUP_H */
