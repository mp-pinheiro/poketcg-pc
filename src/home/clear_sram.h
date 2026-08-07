#ifndef POKETCG_HOME_CLEAR_SRAM_H
#define POKETCG_HOME_CLEAR_SRAM_H

#include <stdint.h>

/* poketcg/src/home/clear_sram.asm */

void ClearSRAMBank(uint8_t bank);
void RestartSRAM(void);

#endif /* POKETCG_HOME_CLEAR_SRAM_H */
