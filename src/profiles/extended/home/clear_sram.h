#ifndef POKETCG_HOME_CLEAR_SRAM_H
#define POKETCG_HOME_CLEAR_SRAM_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part ClearSRAMResult */
/* poketcg/src/home/clear_sram.asm */

typedef struct {
	uint8_t a, f, b, c;
	uint16_t hl;
} ClearSRAMResult;
/* <<< part ClearSRAMResult */

/* >>> factory ClearSRAMBank */
ClearSRAMResult ClearSRAMBank(uint8_t bank, uint8_t f);
/* <<< factory ClearSRAMBank */
/* >>> factory RestartSRAM */
ClearSRAMResult RestartSRAM(void);
/* <<< factory RestartSRAM */

/* >>> factory ValidateSRAM */
void ValidateSRAM(void);
/* <<< factory ValidateSRAM */
#endif /* POKETCG_HOME_CLEAR_SRAM_H */
