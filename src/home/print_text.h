#ifndef POKETCG_HOME_PRINT_TEXT_H
#define POKETCG_HOME_PRINT_TEXT_H

#include <stdint.h>

uint16_t GetTextOffsetFromTextID(uint16_t text_id);
uint16_t GetPointerToTextHeader(void);
uint16_t ReadTextHeader(void);
uint16_t WriteToTextHeader(uint16_t text);
uint16_t WriteToTextHeader_MoveToNext(uint16_t text);
uint16_t ResetTxRam_WriteToTextHeader(uint16_t text);
uint8_t TwoByteNumberToText_CountLeadingZeros(uint16_t value, uint16_t *text);
uint16_t CopyText(uint16_t text_id, uint16_t *destination);
uint8_t CountLinesOfTextFromID(uint16_t text_id);
void LoadTxRam2(uint16_t text_id);
void LoadTxRam3(uint16_t value);

#endif
