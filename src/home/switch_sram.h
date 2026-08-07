#ifndef POKETCG_HOME_SWITCH_SRAM_H
#define POKETCG_HOME_SWITCH_SRAM_H

#include <stdint.h>

void BankswitchSRAM(uint8_t bank);
void DisableSRAM(void);
void EnableSRAM(void);

#endif /* POKETCG_HOME_SWITCH_SRAM_H */
