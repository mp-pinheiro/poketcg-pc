#ifndef POKETCG_HOME_INPUT_NAME_H
#define POKETCG_HOME_INPUT_NAME_H

#include <stdint.h>

/* >>> factory DeckNamingScreen_GetCharInfoFromPos */
/* poketcg/src/engine/input_name.asm */
uint16_t DeckNamingScreen_GetCharInfoFromPos(uint16_t hl);
/* <<< factory DeckNamingScreen_GetCharInfoFromPos */
/* >>> factory ClearMemory_Bank6 */
void ClearMemory_Bank6(uint8_t a, uint16_t hl);
/* <<< factory ClearMemory_Bank6 */
/* >>> factory DrawTextboxForKeyboard */
void DrawTextboxForKeyboard(uint16_t *hl, uint8_t a);
/* <<< factory DrawTextboxForKeyboard */
/* >>> factory TransformCharacter */
typedef struct { uint16_t hl; uint8_t d, e, f; } TransformCharacterResult;
TransformCharacterResult TransformCharacter(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory TransformCharacter */
/* >>> factory PlayerNamingScreen_GetCharInfoFromPos */
uint16_t PlayerNamingScreen_GetCharInfoFromPos(uint16_t hl);
/* <<< factory PlayerNamingScreen_GetCharInfoFromPos */
/* >>> factory PlaySFXConfirmOrCancel_Bank6 */
void PlaySFXConfirmOrCancel_Bank6(uint8_t a);
/* <<< factory PlaySFXConfirmOrCancel_Bank6 */
/* >>> factory PlayerNamingScreen_AdjustCursorPosition */
void PlayerNamingScreen_AdjustCursorPosition(uint8_t a);
/* <<< factory PlayerNamingScreen_AdjustCursorPosition */
/* >>> factory DeckNamingScreen_AdjustCursorPosition */
/* poketcg/src/engine/input_name.asm */

void DeckNamingScreen_AdjustCursorPosition(uint8_t a);
/* <<< factory DeckNamingScreen_AdjustCursorPosition */
/* >>> factory PlayerNamingScreen_DrawCursor */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } PlayerNamingScreen_DrawCursorResult;
PlayerNamingScreen_DrawCursorResult PlayerNamingScreen_DrawCursor(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PlayerNamingScreen_DrawCursor */
/* >>> factory DeckNamingScreen_DrawCursor */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } DeckNamingScreen_DrawCursorResult;
DeckNamingScreen_DrawCursorResult DeckNamingScreen_DrawCursor(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DeckNamingScreen_DrawCursor */
/* >>> factory DeckNamingScreen_DrawInvisibleCursor */
DeckNamingScreen_DrawCursorResult DeckNamingScreen_DrawInvisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DeckNamingScreen_DrawInvisibleCursor */
/* >>> factory DeckNamingScreen_DrawVisibleCursor */
DeckNamingScreen_DrawCursorResult DeckNamingScreen_DrawVisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory DeckNamingScreen_DrawVisibleCursor */
/* >>> factory PlayerNamingScreen_DrawInvisibleCursor */
PlayerNamingScreen_DrawCursorResult PlayerNamingScreen_DrawInvisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PlayerNamingScreen_DrawInvisibleCursor */
/* >>> factory PlayerNamingScreen_DrawVisibleCursor */
PlayerNamingScreen_DrawCursorResult PlayerNamingScreen_DrawVisibleCursor(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PlayerNamingScreen_DrawVisibleCursor */
#endif /* POKETCG_HOME_INPUT_NAME_H */
