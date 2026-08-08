#include "home/menus.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/random.h"
#include "home/text_box.h"
#include "mem.h"

#define SYM_0 0x20
#define SYM_SPACE 0x00
#define TYPE_ENERGY 0x08
#define TYPE_TRAINER 0x10
#define CARD_SYMBOL_TABLE 0x29dd
#define CONSOLE_CGB 0x02
#define YES_OR_NO_TEXT_ID 0x2f

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

CursorTileResult SetCursorParametersForTextBox(uint8_t d, uint8_t e, uint8_t b, uint8_t c)
{
	gb_write8(wCurMenuItem_ADDR, 0);
	gb_write8(wMenuCursorXOffset_ADDR, d);
	gb_write8(wMenuCursorYOffset_ADDR, e);
	gb_write8(wMenuYSeparation_ADDR, 0);
	gb_write8(wNumMenuItems_ADDR, 1);
	gb_write8(wMenuVisibleCursorTile_ADDR, b);
	gb_write8(wMenuInvisibleCursorTile_ADDR, c);
	gb_write8(wCursorBlinkCounter_ADDR, 0);
	return (CursorTileResult){b, c, wMenuInvisibleCursorTile_ADDR};
}

CursorTileResult SetCursorParametersForTextBox_Default(uint8_t d, uint8_t e)
{
	return SetCursorParametersForTextBox(d, e, 0x0f, 0x00);
}

void DrawCursor(uint8_t a)
{
	uint16_t product = HtimesL((uint16_t)((uint16_t)wCurMenuItem << 8 | wMenuYSeparation));
	uint8_t d = wMenuCursorXOffset;
	uint8_t e = (uint8_t)((uint8_t)product + wMenuCursorYOffset);

	AdjustCoordinatesForBGScroll(&d, &e);
	WriteByteToBGMap0(a, d, e);
}

void EraseCursor(void)
{
	DrawCursor(wMenuInvisibleCursorTile);
}

void DrawCursor2(void)
{
	DrawCursor(wMenuVisibleCursorTile);
}

void RefreshMenuCursor(void)
{
	uint8_t old = wCursorBlinkCounter;

	wCursorBlinkCounter = (uint8_t)(old + 1);
	if (old & 0x0f)
		return;
	if (!(wCursorBlinkCounter & 0x10))
		DrawCursor(wMenuVisibleCursorTile);
	else
		EraseCursor();
}

/* menus.asm:654-683 always fills a fixed 2x2 block (`lb bc, 2, 2`). Not using
 * the shared FillRectangle: its hl split is backwards vs hardware (H is the
 * per-column step, L the per-row step -- verified against the oracle here;
 * FillRectangle has them swapped), so this unrolls the two writes directly. */
static void fill_symbol_2x2(uint8_t tile, uint8_t x, uint8_t y, uint8_t col_step, uint8_t row_step)
{
	for (uint8_t row = 0; row < 2; row++) {
		uint16_t pos = DECoordToBGMap0Address(x, (uint8_t)(y + row));
		uint8_t t = (uint8_t)(tile + row_step * row);

		gb_write8(pos, t);
		gb_write8((uint16_t)(pos + 1), (uint8_t)(t + col_step));
	}
}

void DrawCardSymbol(uint8_t d, uint8_t e)
{
	uint8_t id = CardTypeToSymbolID();
	uint16_t entry = (uint16_t)(CARD_SYMBOL_TABLE + (uint16_t)id * 2);
	uint8_t tile = gb_read8(entry);
	uint8_t x = (uint8_t)(d - 2);
	uint8_t y = (uint8_t)(e - 1);

	if (wConsole == CONSOLE_CGB) {
		uint8_t attr = gb_read8((uint16_t)(entry + 1));

		hBankVRAM = 1;
		gb_write8(0xff4f, 1);
		fill_symbol_2x2(attr, x, y, 0, 0);
		hBankVRAM = 0;
		gb_write8(0xff4f, 0);
	}
	fill_symbol_2x2(tile, x, y, 1, 2);
}

uint16_t DrawNarrowTextBox(void)
{
	uint8_t d = 0, e = 12;
	uint16_t hl = 0;

	AdjustCoordinatesForBGScroll(&d, &e);
	DrawRegularTextBox(&hl, 0, 12, 6, d, e);
	return hl;
}

uint16_t DrawWideTextBox(void)
{
	uint8_t d = 0, e = 12;
	uint16_t hl = 0;

	AdjustCoordinatesForBGScroll(&d, &e);
	DrawRegularTextBox(&hl, 0, 20, 6, d, e);
	return hl;
}

/* menus.asm:775-784 is only ever reached by fallthrough from the two callers
 * below, both of which `push hl` first; a synthesized direct call has no such
 * value on the stack, so `pop hl` there grabs the return address and the
 * routine never reaches the oracle's sentinel (times out at MAX_FRAMES). Not
 * independently oracle-testable -- exercised transitively through both callers. */
static TextResult DrawTextBox_PrintTextNoDelay(uint8_t a, uint16_t hl)
{
	uint8_t d = 1, e = 14;

	AdjustCoordinatesForBGScroll(&d, &e);
	InitTextPrintingInTextbox(a, d, e);
	if (hl)
		return PrintTextNoDelay(hl, d, e);

	uint16_t ptr = wDefaultText_ADDR;
	ProcessText(&ptr);
	return (TextResult){0, 0, 0, d, e, ptr};
}

TextResult DrawNarrowTextBox_PrintTextNoDelay(uint16_t hl)
{
	DrawNarrowTextBox();
	return DrawTextBox_PrintTextNoDelay(11, hl);
}

TextResult DrawWideTextBox_PrintTextNoDelay(uint16_t hl)
{
	DrawWideTextBox();
	return DrawTextBox_PrintTextNoDelay(19, hl);
}

TextResult DrawWideTextBox_PrintText(uint16_t hl)
{
	uint8_t d = 1, e = 14;

	DrawWideTextBox();
	AdjustCoordinatesForBGScroll(&d, &e);
	InitTextPrintingInTextbox(19, d, e);
	EnableLCD();
	return PrintText(hl, d, e);
}

ProcessTextHeaderResult PrintYesOrNoItems(uint8_t d, uint8_t e)
{
	AdjustCoordinatesForBGScroll(&d, &e);
	return InitTextPrinting_ProcessTextFromID(d, e, YES_OR_NO_TEXT_ID);
}

#define PAD_A        0x01u
#define PAD_B        0x02u
#define NTBM_PARAMS  0x2a96u
#define WTBM_PARAMS  0x2ac8u

WaitResult WaitForButtonAorB(void)
{
	for (;;) {
		DoFrame();
		RefreshMenuCursor();
		uint8_t keys = gb_read8(hKeysPressed_ADDR);
		if (keys & PAD_A) {
			EraseCursor();
			return (WaitResult){0x00u};
		}
		if (keys & PAD_B) {
			EraseCursor();
			return (WaitResult){0x10u};
		}
	}
}

void DrawWideTextBox_PrintTextNoDelay_Wait(uint16_t hl)
{
	(void)DrawWideTextBox_PrintTextNoDelay(hl);
	WaitForWideTextBoxInput();
}

void DrawNarrowTextBox_WaitForInput(uint16_t hl)
{
	(void)DrawNarrowTextBox_PrintTextNoDelay(hl);
	uint16_t params = NTBM_PARAMS;
	InitializeMenuParameters(0, &params);
	EnableLCD();
	for (;;) {
		DoFrame();
		RefreshMenuCursor();
		uint8_t keys = gb_read8(hKeysPressed_ADDR);
		if (keys & (PAD_A | PAD_B))
			break;
	}
}

void DrawWideTextBox_WaitForInput(uint16_t hl)
{
	(void)DrawWideTextBox_PrintText(hl);
	WaitForWideTextBoxInput();
}

void WaitForWideTextBoxInput(void)
{
	uint16_t params = WTBM_PARAMS;
	InitializeMenuParameters(0, &params);
	EnableLCD();
	for (;;) {
		DoFrame();
		RefreshMenuCursor();
		uint8_t keys = gb_read8(hKeysPressed_ADDR);
		if (keys & (PAD_A | PAD_B))
			break;
	}
	EraseCursor();
}
