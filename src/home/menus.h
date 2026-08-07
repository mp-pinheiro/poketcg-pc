#ifndef POKETCG_HOME_MENUS_H
#define POKETCG_HOME_MENUS_H

#include <stdint.h>
typedef struct {
	uint8_t a;
	uint16_t hl;
} TxSymbolResult;

void InitializeCardListParameters(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl);
void InitializeMenuParameters(uint8_t a, uint16_t *hl);
void SetMenuItem(uint8_t a);
TxSymbolResult OneByteNumberToTxSymbol(uint8_t a);
TxSymbolResult OneByteNumberToTxSymbol_PadSpace(uint8_t a);
TxSymbolResult OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign(uint8_t a);
uint8_t CardTypeToSymbolID(void);
uint8_t GetCardSymbolData(void);
typedef struct {
	uint8_t b;
	uint8_t c;
	uint16_t hl;
} CursorTileResult;
CursorTileResult SetCursorParametersForTextBox(uint8_t d, uint8_t e, uint8_t b, uint8_t c);
CursorTileResult SetCursorParametersForTextBox_Default(uint8_t d, uint8_t e);

#endif
