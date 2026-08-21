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
#endif
