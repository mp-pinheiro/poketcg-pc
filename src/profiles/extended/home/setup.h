#ifndef POKETCG_SETUP_H
#define POKETCG_SETUP_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part DetectConsoleResult */
typedef struct {
	uint8_t a;
	uint8_t b;
} DetectConsoleResult;
/* <<< part DetectConsoleResult */

/* >>> part SetupPalettesResult */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} SetupPalettesResult;
/* <<< part SetupPalettesResult */

/* >>> part ZeroRAMResult */
typedef struct {
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} ZeroRAMResult;
/* <<< part ZeroRAMResult */

/* >>> factory NoOp */
void NoOp(void);
/* <<< factory NoOp */
/* >>> factory DetectConsole */
DetectConsoleResult DetectConsole(uint8_t a);
/* <<< factory DetectConsole */
/* >>> factory SetupPalettes */
SetupPalettesResult SetupPalettes(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory SetupPalettes */
/* >>> factory FillTileMap */
uint16_t FillTileMap(void);
/* <<< factory FillTileMap */
/* >>> factory SetupVRAM */
uint16_t SetupVRAM(void);
/* <<< factory SetupVRAM */
/* >>> factory SetupRegisters */
uint16_t SetupRegisters(void);
/* <<< factory SetupRegisters */
/* >>> factory ZeroRAM */
ZeroRAMResult ZeroRAM(void);
/* <<< factory ZeroRAM */

#endif /* POKETCG_SETUP_H */
