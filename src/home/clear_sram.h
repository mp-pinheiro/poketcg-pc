#ifndef POKETCG_HOME_CLEAR_SRAM_H
#define POKETCG_HOME_CLEAR_SRAM_H

#include <stdint.h>

/* poketcg/src/home/clear_sram.asm */

typedef struct {
	uint8_t a, f, b, c;
	uint16_t hl;
} ClearSRAMResult;

ClearSRAMResult ClearSRAMBank(uint8_t bank, uint8_t f);
ClearSRAMResult RestartSRAM(void);

#endif /* POKETCG_HOME_CLEAR_SRAM_H */
