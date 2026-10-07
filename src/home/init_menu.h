#ifndef POKETCG_HOME_INIT_MENU_H
#define POKETCG_HOME_INIT_MENU_H
/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part InitMenuRegs */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} InitMenuRegs;
/* <<< part InitMenuRegs */

/* >>> factory InitMenuScreen */
InitMenuRegs InitMenuScreen(void);
/* <<< factory InitMenuScreen */
/* >>> factory FlashWhiteScreen */
InitMenuRegs FlashWhiteScreen(void);
/* <<< factory FlashWhiteScreen */

#endif
