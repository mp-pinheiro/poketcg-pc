#ifndef POKETCG_HOME_SWITCH_SRAM_H
#define POKETCG_HOME_SWITCH_SRAM_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory BankswitchSRAM */
void BankswitchSRAM(uint8_t bank);
/* <<< factory BankswitchSRAM */
/* >>> part DisableSRAM */
void DisableSRAM(void);
/* <<< part DisableSRAM */
/* >>> part EnableSRAM */
void EnableSRAM(void);
/* <<< part EnableSRAM */

#endif /* POKETCG_HOME_SWITCH_SRAM_H */
