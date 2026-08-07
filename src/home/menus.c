#include "home/menus.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#define SYM_0 0x20
#define SYM_SPACE 0x00
#define TYPE_ENERGY 0x08
#define TYPE_TRAINER 0x10
#define CARD_SYMBOL_TABLE 0x29dd

void InitializeCardListParameters(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl)
{
	wNumListItems = a;
	wListScrollOffset = d;
	wCurMenuItem = e;
	hCurMenuItem = (uint8_t)(e + d);
	wMenuCursorXOffset = gb_read8((*hl)++);
	wMenuCursorYOffset = gb_read8((*hl)++);
	wListItemXPosition = gb_read8((*hl)++);
	wListItemNameMaxLength = gb_read8((*hl)++);
	wNumMenuItems = gb_read8((*hl)++);
	wMenuVisibleCursorTile = gb_read8((*hl)++);
	wMenuInvisibleCursorTile = gb_read8((*hl)++);
	wListFunctionPointer = gb_read8((*hl)++);
	gb_write8((uint16_t)(wListFunctionPointer_ADDR + 1), gb_read8((*hl)++));
	wCursorBlinkCounter = 0;
	wMenuYSeparation = 1;
}

void InitializeMenuParameters(uint8_t a, uint16_t *hl)
{
	wCurMenuItem = a;
	hCurMenuItem = a;
	for (uint8_t i = 0; i < 8; i++)
		gb_write8((uint16_t)(wMenuCursorXOffset_ADDR + i), gb_read8((*hl)++));
	wCursorBlinkCounter = 0;
}

void SetMenuItem(uint8_t a)
{
	wCurMenuItem = a;
	hCurMenuItem = a;
	wCursorBlinkCounter = 0;
}

static TxSymbolResult tx_symbol_core(uint8_t a)
{
	uint8_t e = (uint8_t)(SYM_0 - 1);
	for (;;) {
		e++;
		a = (uint8_t)(a - 10);
		if (a >= 0xf6)
			break;
	}
	gb_write8(wDefaultText_ADDR, e);
	uint8_t ones = (uint8_t)(a + SYM_0 + 10);
	gb_write8((uint16_t)(wDefaultText_ADDR + 1), ones);
	gb_write8((uint16_t)(wDefaultText_ADDR + 2), SYM_SPACE);
	return (TxSymbolResult){ones, wDefaultText_ADDR};
}

TxSymbolResult OneByteNumberToTxSymbol(uint8_t a)
{
	return tx_symbol_core(a);
}

TxSymbolResult OneByteNumberToTxSymbol_PadSpace(uint8_t a)
{
	TxSymbolResult result = tx_symbol_core(a);
	uint8_t first = gb_read8(result.hl);
	if (first == SYM_0)
		gb_write8(result.hl, SYM_SPACE);
	result.a = first;
	return result;
}

TxSymbolResult OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign(uint8_t a)
{
	TxSymbolResult result = tx_symbol_core(a);
	uint16_t hl = (uint16_t)(result.hl + 1);
	uint8_t first = gb_read8(result.hl);
	if (first == SYM_0) {
		uint8_t second = gb_read8(hl);
		gb_write8(result.hl, second);
		gb_write8(hl, SYM_SPACE);
		result.a = second;
	} else {
		result.a = first;
	}
	result.hl = hl;
	return result;
}

uint8_t CardTypeToSymbolID(void)
{
	uint8_t type = wLoadedCard1Type;
	if (type >= TYPE_TRAINER)
		return 11;
	if (type >= TYPE_ENERGY)
		return (uint8_t)(type & 7);
	return (uint8_t)(wLoadedCard1Stage + 8);
}

uint8_t GetCardSymbolData(void)
{
	uint8_t id = CardTypeToSymbolID();
	uint16_t address = (uint16_t)(CARD_SYMBOL_TABLE + (uint16_t)id * 2);
	return gb_read8(address);
}
