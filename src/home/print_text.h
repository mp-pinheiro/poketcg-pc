#ifndef POKETCG_HOME_PRINT_TEXT_H
#define POKETCG_HOME_PRINT_TEXT_H

/* >>> part includes */
#include "home/process_text.h"
/* <<< part includes */

/* >>> factory GetTextOffsetFromTextID */
uint16_t GetTextOffsetFromTextID(uint16_t text_id);
/* <<< factory GetTextOffsetFromTextID */
/* >>> factory GetPointerToTextHeader */
uint16_t GetPointerToTextHeader(void);
/* <<< factory GetPointerToTextHeader */
/* >>> factory ReadTextHeader */
uint16_t ReadTextHeader(void);
/* <<< factory ReadTextHeader */
/* >>> part TextHeaderWrite */
/* WriteToTextHeader does `push hl / call GetPointerToTextHeader / pop bc`
 * (print_text.asm:180-182), so exit b/c are the entry pointer's halves. */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} TextHeaderWrite;
/* <<< part TextHeaderWrite */
/* >>> factory WriteToTextHeader */
TextHeaderWrite WriteToTextHeader(uint16_t text);
/* <<< factory WriteToTextHeader */
/* >>> factory WriteToTextHeader_MoveToNext */
TextHeaderWrite WriteToTextHeader_MoveToNext(uint16_t text);
/* <<< factory WriteToTextHeader_MoveToNext */
/* >>> factory ResetTxRam_WriteToTextHeader */
TextHeaderWrite ResetTxRam_WriteToTextHeader(uint16_t text);
/* <<< factory ResetTxRam_WriteToTextHeader */
/* >>> part LeadingZerosResult */
typedef struct {
	uint8_t c;
	uint16_t de;
	uint16_t hl;
} LeadingZerosResult;
/* <<< part LeadingZerosResult */
/* >>> factory TwoByteNumberToText_CountLeadingZeros */
LeadingZerosResult TwoByteNumberToText_CountLeadingZeros(uint16_t value, uint8_t c, uint16_t de);
/* <<< factory TwoByteNumberToText_CountLeadingZeros */
/* >>> factory CopyText */
CopyTextResult CopyText(uint16_t text_id, uint16_t de);
/* <<< factory CopyText */
/* >>> factory CountLinesOfTextFromID */
uint8_t CountLinesOfTextFromID(uint16_t text_id);
/* <<< factory CountLinesOfTextFromID */
/* >>> factory LoadTxRam2 */
void LoadTxRam2(uint16_t text_id);
/* <<< factory LoadTxRam2 */
/* >>> factory LoadTxRam3 */
void LoadTxRam3(uint16_t value);
/* <<< factory LoadTxRam3 */
/* >>> part ProcessTextHeaderResult */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} ProcessTextHeaderResult;
/* <<< part ProcessTextHeaderResult */

/* >>> factory ProcessTextHeader */
ProcessTextHeaderResult ProcessTextHeader(uint8_t d, uint8_t e);
/* <<< factory ProcessTextHeader */
/* >>> part TxRamSlot */
/* The tail is `ld a, [hli] / ld h, [hl] / ld l, a` (print_text.asm), so exit a is the
 * slot's low byte, and the index doubling leaves d = 0 with e = the byte offset. */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} TxRamSlot;
/* <<< part TxRamSlot */
/* >>> factory HandleTxRam2Or3 */
TxRamSlot HandleTxRam2Or3(uint16_t de, uint16_t hl);
/* <<< factory HandleTxRam2Or3 */
/* >>> factory CopyTextData_FromTextID */
CopyTextResult CopyTextData_FromTextID(uint8_t a, uint16_t hl, uint16_t de);
/* <<< factory CopyTextData_FromTextID */
/* >>> factory CopyPlayerNameOrTurnDuelistName */
CopyTextResult CopyPlayerNameOrTurnDuelistName(void);
/* <<< factory CopyPlayerNameOrTurnDuelistName */
/* >>> factory InitTextPrinting_ProcessTextFromID */
ProcessTextHeaderResult InitTextPrinting_ProcessTextFromID(uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory InitTextPrinting_ProcessTextFromID */
/* >>> factory InitTextPrinting_ProcessTextFromPointerToID */
ProcessTextHeaderResult InitTextPrinting_ProcessTextFromPointerToID(uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory InitTextPrinting_ProcessTextFromPointerToID */
/* >>> factory ProcessTextFromID */
ProcessTextHeaderResult ProcessTextFromID(uint16_t hl);
/* <<< factory ProcessTextFromID */
/* >>> factory ProcessTextFromPointerToID */
ProcessTextHeaderResult ProcessTextFromPointerToID(uint16_t hl);
/* <<< factory ProcessTextFromPointerToID */

/* >>> part TextResult */
typedef struct {
	uint8_t a, b, c, d, e;
	uint16_t hl;
} TextResult;
/* <<< part TextResult */

/* >>> factory PlaceTextItems */
TextResult PlaceTextItems(uint16_t hl);
/* <<< factory PlaceTextItems */
/* >>> factory PrintText */
TextResult PrintText(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory PrintText */
/* >>> factory PrintTextNoDelay */
TextResult PrintTextNoDelay(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory PrintTextNoDelay */
/* >>> part WaitResult */
typedef struct {
	uint8_t f;
	uint8_t a;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} WaitResult;
/* <<< part WaitResult */
/* >>> factory DrawTextReadyLabeledOrRegularTextBox */
TextResult DrawTextReadyLabeledOrRegularTextBox(uint16_t hl);
/* <<< factory DrawTextReadyLabeledOrRegularTextBox */
/* >>> factory WaitForPlayerToAdvanceText */
WaitResult WaitForPlayerToAdvanceText(void);
/* <<< factory WaitForPlayerToAdvanceText */
/* >>> factory PrintScrollableText */
TextResult PrintScrollableText(uint8_t a, uint16_t hl);
/* <<< factory PrintScrollableText */
/* >>> factory PrintScrollableText_NoTextBoxLabel */
WaitResult PrintScrollableText_NoTextBoxLabel(uint16_t hl);
/* <<< factory PrintScrollableText_NoTextBoxLabel */
/* >>> factory PrintScrollableText_WithTextBoxLabel_NoWait */
TextResult PrintScrollableText_WithTextBoxLabel_NoWait(uint16_t hl, uint16_t de);
/* <<< factory PrintScrollableText_WithTextBoxLabel_NoWait */
/* >>> factory PrintScrollableText_WithTextBoxLabel */
WaitResult PrintScrollableText_WithTextBoxLabel(uint16_t hl, uint16_t de);
/* <<< factory PrintScrollableText_WithTextBoxLabel */
#endif
