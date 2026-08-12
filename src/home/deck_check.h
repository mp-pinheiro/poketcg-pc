#ifndef POKETCG_HOME_DECK_CHECK_H
#define POKETCG_HOME_DECK_CHECK_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t e;
	uint8_t f;
} DrawCheckMenuCursorResult;

DrawCheckMenuCursorResult DrawCheckMenuCursor(uint8_t a);
void PlaySFXConfirmOrCancel(uint8_t a);

/* >>> factory EraseCheckMenuCursor */
DrawCheckMenuCursorResult EraseCheckMenuCursor(void);
/* <<< factory EraseCheckMenuCursor */
/* >>> factory DisplayCheckMenuCursor */
DrawCheckMenuCursorResult DisplayCheckMenuCursor(void);
/* <<< factory DisplayCheckMenuCursor */
#endif
