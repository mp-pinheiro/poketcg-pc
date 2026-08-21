#ifndef POKETCG_HOME_SWITCH_ROM_H
#define POKETCG_HOME_SWITCH_ROM_H

#include <stdint.h>

/* poketcg/src/home/switch_rom.asm:90 */
void BankswitchROM(uint8_t bank);

/* >>> factory BankpushROM */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} BankpushROMResult;
BankpushROMResult BankpushROM(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory BankpushROM */
#endif /* POKETCG_HOME_SWITCH_ROM_H */
