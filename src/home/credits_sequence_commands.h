#ifndef HOME_CREDITS_SEQUENCE_COMMANDS_H
#define HOME_CREDITS_SEQUENCE_COMMANDS_H

#include <stdint.h>

void SetCreditsSequenceCmdPtr(void);
void ExecuteCreditsSequenceCmd(void);
void AdvanceCreditsSequenceCmdPtr(uint8_t a);

/* >>> factory AdvanceCreditsSequenceCmdPtrBy2 */
void AdvanceCreditsSequenceCmdPtrBy2(void);
/* <<< factory AdvanceCreditsSequenceCmdPtrBy2 */
/* >>> factory AdvanceCreditsSequenceCmdPtrBy3 */
void AdvanceCreditsSequenceCmdPtrBy3(void);
/* <<< factory AdvanceCreditsSequenceCmdPtrBy3 */
/* >>> factory AdvanceCreditsSequenceCmdPtrBy5 */
void AdvanceCreditsSequenceCmdPtrBy5(void);
/* <<< factory AdvanceCreditsSequenceCmdPtrBy5 */
/* >>> factory AdvanceCreditsSequenceCmdPtrBy6 */
void AdvanceCreditsSequenceCmdPtrBy6(void);
/* <<< factory AdvanceCreditsSequenceCmdPtrBy6 */
/* >>> factory AdvanceCreditsSequenceCmdPtrBy4 */
void AdvanceCreditsSequenceCmdPtrBy4(void);
/* <<< factory AdvanceCreditsSequenceCmdPtrBy4 */
/* >>> factory CreditsSequenceCmd_Wait */
void CreditsSequenceCmd_Wait(uint8_t c);
/* <<< factory CreditsSequenceCmd_Wait */
/* >>> factory CreditsSequenceCmd_DisableLCD */
void CreditsSequenceCmd_DisableLCD(void);
/* <<< factory CreditsSequenceCmd_DisableLCD */
/* >>> factory CreditsSequenceCmd_TransformOverlay */
void CreditsSequenceCmd_TransformOverlay(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory CreditsSequenceCmd_TransformOverlay */
/* >>> factory CreditsSequenceCmd_FadeIn */
void CreditsSequenceCmd_FadeIn(void);
/* <<< factory CreditsSequenceCmd_FadeIn */
/* >>> factory CreditsSequenceCmd_PrintTextBox */
void CreditsSequenceCmd_PrintTextBox(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory CreditsSequenceCmd_PrintTextBox */
/* >>> factory CreditsSequenceCmd_InitOverlay */
void CreditsSequenceCmd_InitOverlay(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory CreditsSequenceCmd_InitOverlay */
/* >>> factory CreditsSequenceCmd_InitVolcanoSprite */
/* poketcg/src/engine/sequences/credits_sequence_commands.asm:412 */
void CreditsSequenceCmd_InitVolcanoSprite(uint8_t f);
/* <<< factory CreditsSequenceCmd_InitVolcanoSprite */
/* >>> factory CreditsSequenceCmd_DrawRectangle */
typedef struct { uint8_t a; uint8_t f; } CreditsSequenceCmdDrawRectangleResult;
CreditsSequenceCmdDrawRectangleResult CreditsSequenceCmd_DrawRectangle(uint8_t b, uint8_t c);
/* <<< factory CreditsSequenceCmd_DrawRectangle */
/* >>> factory CreditsSequenceCmd_PrintText */
void CreditsSequenceCmd_PrintText(uint8_t b, uint8_t c, uint16_t de);
/* <<< factory CreditsSequenceCmd_PrintText */
/* >>> factory CreditsSequenceCmd_LoadBooster */
void CreditsSequenceCmd_LoadBooster(uint8_t b, uint8_t c, uint8_t d, uint8_t e);

void AdvanceCreditsSequenceCmdPtrBy5(void);
void ClearNumLoadedFramesetSubgroups(void);
void EmptyScreen(void);
uint8_t LoadBoosterGfx(uint8_t a, uint8_t b, uint8_t c);
void SetDefaultPalettes(void);
/* <<< factory CreditsSequenceCmd_LoadBooster */
/* >>> factory CreditsSequenceCmd_FadeOut */
void CreditsSequenceCmd_FadeOut(void);
/* <<< factory CreditsSequenceCmd_FadeOut */
/* >>> factory CreditsSequenceCmd_LoadScene */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; } CreditsSequenceCmdLoadSceneResult;
CreditsSequenceCmdLoadSceneResult CreditsSequenceCmd_LoadScene(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CreditsSequenceCmd_LoadScene */
/* >>> factory LoadOWMapForCreditsSequence */
void LoadOWMapForCreditsSequence(uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory LoadOWMapForCreditsSequence */
#endif
