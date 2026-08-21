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
#endif /* POKETCG_HOME_INPUT_NAME_H */
