#ifndef POKETCG_HOME_INIT_MENU_H
#define POKETCG_HOME_INIT_MENU_H
#include <stdint.h>

typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} InitMenuRegs;

InitMenuRegs InitMenuScreen(void);
InitMenuRegs FlashWhiteScreen(void);

#endif
