#ifndef POKETCG_HOME_PRINT_TEXT_H
#define POKETCG_HOME_PRINT_TEXT_H

#include "home/process_text.h"

uint16_t GetTextOffsetFromTextID(uint16_t text_id);
uint16_t GetPointerToTextHeader(void);
uint16_t ReadTextHeader(void);
/* WriteToTextHeader does `push hl / call GetPointerToTextHeader / pop bc`
 * (print_text.asm:180-182), so exit b/c are the entry pointer's halves. */
typedef struct {
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} TextHeaderWrite;
TextHeaderWrite WriteToTextHeader(uint16_t text);
TextHeaderWrite WriteToTextHeader_MoveToNext(uint16_t text);
TextHeaderWrite ResetTxRam_WriteToTextHeader(uint16_t text);
typedef struct {
	uint8_t c;
	uint16_t de;
	uint16_t hl;
} LeadingZerosResult;
LeadingZerosResult TwoByteNumberToText_CountLeadingZeros(uint16_t value, uint8_t c, uint16_t de);
CopyTextResult CopyText(uint16_t text_id, uint16_t de);
uint8_t CountLinesOfTextFromID(uint16_t text_id);
void LoadTxRam2(uint16_t text_id);
void LoadTxRam3(uint16_t value);
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint8_t f;
	uint16_t hl;
} ProcessTextHeaderResult;

ProcessTextHeaderResult ProcessTextHeader(uint8_t d, uint8_t e);
/* The tail is `ld a, [hli] / ld h, [hl] / ld l, a` (print_text.asm), so exit a is the
 * slot's low byte, and the index doubling leaves d = 0 with e = the byte offset. */
typedef struct {
	uint8_t a;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} TxRamSlot;
TxRamSlot HandleTxRam2Or3(uint16_t de, uint16_t hl);
CopyTextResult CopyTextData_FromTextID(uint8_t a, uint16_t hl, uint16_t de);
CopyTextResult CopyPlayerNameOrTurnDuelistName(void);
ProcessTextHeaderResult InitTextPrinting_ProcessTextFromID(uint8_t d, uint8_t e, uint16_t hl);
ProcessTextHeaderResult InitTextPrinting_ProcessTextFromPointerToID(uint8_t d, uint8_t e, uint16_t hl);
ProcessTextHeaderResult ProcessTextFromID(uint16_t hl);
ProcessTextHeaderResult ProcessTextFromPointerToID(uint16_t hl);

typedef struct {
	uint8_t a, b, c, d, e;
	uint16_t hl;
} TextResult;

TextResult PlaceTextItems(uint16_t hl);
TextResult PrintText(uint16_t hl, uint8_t d, uint8_t e);
TextResult PrintTextNoDelay(uint16_t hl, uint8_t d, uint8_t e);
typedef struct {
	uint8_t f;
} WaitResult;
TextResult DrawTextReadyLabeledOrRegularTextBox(uint16_t hl);
WaitResult WaitForPlayerToAdvanceText(void);
TextResult PrintScrollableText(uint8_t a, uint16_t hl);
WaitResult PrintScrollableText_NoTextBoxLabel(uint16_t hl);
TextResult PrintScrollableText_WithTextBoxLabel_NoWait(uint16_t hl, uint16_t de);
WaitResult PrintScrollableText_WithTextBoxLabel(uint16_t hl, uint16_t de);
#endif
