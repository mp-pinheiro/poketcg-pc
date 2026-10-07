#ifndef POKETCG_HOME_DECK_CHECK_H
#define POKETCG_HOME_DECK_CHECK_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part DrawCheckMenuCursorResult */
typedef struct {
	uint8_t a;
	uint8_t e;
	uint8_t f;
} DrawCheckMenuCursorResult;
/* <<< part DrawCheckMenuCursorResult */

/* >>> factory DrawCheckMenuCursor */
DrawCheckMenuCursorResult DrawCheckMenuCursor(uint8_t a);
/* <<< factory DrawCheckMenuCursor */
/* >>> factory PlaySFXConfirmOrCancel */
void PlaySFXConfirmOrCancel(uint8_t a);
/* <<< factory PlaySFXConfirmOrCancel */

/* >>> factory EraseCheckMenuCursor */
DrawCheckMenuCursorResult EraseCheckMenuCursor(void);
/* <<< factory EraseCheckMenuCursor */
/* >>> factory DisplayCheckMenuCursor */
DrawCheckMenuCursorResult DisplayCheckMenuCursor(void);
/* <<< factory DisplayCheckMenuCursor */
/* >>> factory HandleCheckMenuInput */
typedef struct { uint8_t a; uint8_t f; } HandleCheckMenuInputResult;
HandleCheckMenuInputResult HandleCheckMenuInput(void);
/* <<< factory HandleCheckMenuInput */
#endif
