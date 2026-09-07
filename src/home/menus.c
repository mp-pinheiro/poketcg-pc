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
/* >>> factory statics */
#include "home/menus.h"
#include "home/sound.h"
#include "generated/wram.h"

#define SFX_CANCEL 0x03u
#define SFX_CONFIRM 0x02u
/* Function pointers the asm installs in RAM: menus.asm:322 CardListMenuFunction
 * into wMenuUpdateFunc; duel/core.asm:5030/5038 PlayAreaScreenMenuFunction
 * ($01:60CE) into wMenuUpdateFunc; core.asm:3395 CardListFunction ($01:5719)
 * into wListFunctionPointer. */
#define CARD_LIST_MENU_FUNCTION 0x283Fu
#define PLAY_AREA_SCREEN_MENU_FUNCTION 0x60CEu
#define CARD_LIST_FUNCTION 0x5719u
#include "home/core.h"
#include "home/indirect_dispatch.h"

#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/sound.h"
#include "generated/hram.h"
#include "generated/wram.h"

#define SYM_CURSOR_R 0x0Fu
#define SYM_SPACE 0x00u
#define PAD_A 0x01u
#define PAD_RIGHT 0x10u
#define PAD_LEFT 0x20u
#define SFX_CURSOR 0x01u

#define SYM_CURSOR_U 0x0Cu
#define SYM_CURSOR_D 0x2Fu
#include "generated/wram.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/duel.h"
#include "home/bg_map.h"

#include "generated/hram.h"
#include "mem.h"
#include "home/menus.h"

#include "generated/wram.h"
#include "home/menus.h"

#include "home/menus.h"
#include "home/bg_map.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define PAD_UP 0x40u
#define PAD_DOWN 0x80u
#define SYM_SLASH 0x2Eu

#define PAD_B 0x02u

#include "home/menus.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "generated/hram.h"

#include "home/overworld.h"
#include "home/core.h"
#define CONTINUE_DUEL_BANK 0x01u
/* <<< factory statics */

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
	return (CursorTileResult){.b = b, .c = c, .hl = wMenuInvisibleCursorTile_ADDR};
}

CursorTileResult SetCursorParametersForTextBox_Default(uint8_t d, uint8_t e)
{
	CursorTileResult result = SetCursorParametersForTextBox(d, e, 0x0f, 0x00);
	result.f = WaitForButtonAorB().f;
	return result;
}

/* menus.asm:190-210's tail (`or a; ret`) reloads the tile into a before the
 * write, so DrawCursor's exit a/e/f are fully determined by the tile and the
 * computed BG coordinate -- not garbage. HandleMenuInput's tail jumps into
 * RefreshMenuCursor_CheckPlaySFX (menus.asm:122,135) need that exit state,
 * so it is kept here instead of discarded. */
static HandleMenuInputResult DrawCursorRegs(uint8_t tile)
{
	uint16_t product = HtimesL((uint16_t)((uint16_t)wCurMenuItem << 8 | wMenuYSeparation));
	uint8_t d = wMenuCursorXOffset;
	uint8_t e = (uint8_t)((uint8_t)product + wMenuCursorYOffset);

	AdjustCoordinatesForBGScroll(&d, &e);
	WriteByteToBGMap0(tile, d, e);
	/* menus.asm DrawCursor ends `or a` on what WriteByteToBGMap0 leaves:
	 * the tile with the LCD off, and rSTAT's mode bits -- 0, HBlank asserted --
	 * after HblankCopyDataHLtoDE with it on (bg_map.asm:52-88, hblank.asm:12-14). */
	uint8_t a = (wLCDC & 0x80u) != 0u ? 0u : tile;
	return (HandleMenuInputResult){a, e, (a == 0u) ? 0x80u : 0x00u};
}

void DrawCursor(uint8_t a)
{
	(void)DrawCursorRegs(a);
}

void EraseCursor(void)
{
	DrawCursor(wMenuInvisibleCursorTile);
}

void DrawCursor2(void)
{
	DrawCursor(wMenuVisibleCursorTile);
}

/* menus.asm:173-184. `and $f; ret nz` (:178-179) only fires when the
 * pre-increment counter's low nibble is non-zero; e is left untouched by it.
 * RefreshMenuCursor_CheckPlaySFX is only ever reached with carry already
 * clear (menus.asm:122 `jr nc`, :135 `jr z`), so every HandleMenuInput
 * caller takes the "no selection" branch and never reads a/e here -- e has
 * no defined value on this path (dead register, not a callable output), so
 * 0 stands in for it. When the counter is on a 16-frame boundary, execution
 * falls through into DrawCursor/EraseCursor instead, whose exit state is
 * fully defined and reused verbatim. */
static HandleMenuInputResult RefreshMenuCursorRegs(void)
{
	uint8_t old = wCursorBlinkCounter;

	wCursorBlinkCounter = (uint8_t)(old + 1);
	if ((old & 0x0fu) != 0u)
		return (HandleMenuInputResult){(uint8_t)(old & 0x0fu), 0u, 0x20u};
	if ((wCursorBlinkCounter & 0x10u) == 0u)
		return DrawCursorRegs(wMenuVisibleCursorTile);
	return DrawCursorRegs(wMenuInvisibleCursorTile);
}

void RefreshMenuCursor(void)
{
	(void)RefreshMenuCursorRegs();
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

/* >>> factory DrawTextBox_PrintTextNoDelay */
/* menus.asm:775-784. Reached by fallthrough from the two callers below, both of
 * which `push hl` first, so the `pop hl` consumes a caller-pushed value rather
 * than the return address. A probed call models that with the case's `stack`
 * field, exactly as the music command handlers do for their stream pointer. */
TextResult DrawTextBox_PrintTextNoDelay(uint8_t a, uint16_t hl)
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
/* <<< factory DrawTextBox_PrintTextNoDelay */

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
		uint8_t zero = (gb_read8(wLCDC_ADDR) & 0x80u) != 0u
			|| gb_read8(wMenuInvisibleCursorTile_ADDR) == 0u ? 0x80u : 0x00u;
		if (keys & PAD_A) {
			EraseCursor();
			return (WaitResult){zero};
		}
		if (keys & PAD_B) {
			EraseCursor();
			return (WaitResult){(uint8_t)(zero | 0x10u)};
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

WaitResult DrawWideTextBox_WaitForInput(uint16_t hl)
{
	(void)DrawWideTextBox_PrintText(hl);
	return WaitForWideTextBoxInput();
}

WaitResult WaitForWideTextBoxInput(void)
{
	uint16_t params = WTBM_PARAMS;
	InitializeMenuParameters(0, &params);
	EnableLCD();
	for (;;) {
		DoFrame();
		RefreshMenuCursor();
		uint8_t keys = gb_read8(hKeysPressed_ADDR);
		if (keys & (PAD_A | PAD_B)) {
			EraseCursor();
			return (WaitResult){0x80u};
		}
	}
}

/* HandleMenuInput's two callers of RefreshMenuCursor_CheckPlaySFX are tail
 * jumps in the real asm (menus.asm:122 `jr nc`, :135 `jr z` -- not `call`),
 * so the a/e/f state it exits with is exactly what HandleMenuInput itself
 * returns on those paths. */
static HandleMenuInputResult RefreshMenuCursor_CheckPlaySFXRegs(void)
{
	uint8_t a = wRefreshMenuCursorSFX;
	if (a != 0u)
		PlaySFX(a);
	return RefreshMenuCursorRegs();
}

/* >>> factory RefreshMenuCursor_CheckPlaySFX */
void RefreshMenuCursor_CheckPlaySFX(void)
{
	(void)RefreshMenuCursor_CheckPlaySFXRegs();
}
/* <<< factory RefreshMenuCursor_CheckPlaySFX */

/* >>> factory PlayOpenOrExitScreenSFX */
PlayOpenOrExitScreenSFXResult PlayOpenOrExitScreenSFX(uint8_t a, uint8_t f)
{
	uint8_t item = hCurMenuItem;
	if ((uint8_t)(item + 1u) == 0u)
		PlaySFX(SFX_CANCEL);
	else
		PlaySFX(SFX_CONFIRM);
	return (PlayOpenOrExitScreenSFXResult){a, f};
}
/* <<< factory PlayOpenOrExitScreenSFX */

/* >>> factory HandleYesOrNoMenu */
HandleYesOrNoMenuResult HandleYesOrNoMenu(uint8_t d, uint8_t e, uint8_t b, uint8_t c)
{
	wLeftmostItemCursorX = d;
	(void)SetCursorParametersForTextBox(d, e, SYM_CURSOR_R, SYM_SPACE);
	uint8_t selected = (uint8_t)(wDefaultYesOrNo ^ 1u);
	wCurMenuItem = (uint8_t)(wDefaultYesOrNo ^ 1u);
	EnableLCD();
	wMenuCursorXOffset = (uint8_t)(wCurMenuItem * 4u + wLeftmostItemCursorX);
	wCursorBlinkCounter = 0u;
	for (;;) {
		DoFrame();
		RefreshMenuCursor();
		if ((hKeysPressed & PAD_A) != 0u) {
			hCurMenuItem = wCurMenuItem;
			if (wCurMenuItem == 0u) {
				wDefaultYesOrNo = 0u;
				return (HandleYesOrNoMenuResult){0u, 0x80u};
			}
			wDefaultYesOrNo = 0u;
			hCurMenuItem = 1u;
			return (HandleYesOrNoMenuResult){1u, 0x90u};
		}
		if ((hDPadHeld & (PAD_RIGHT | PAD_LEFT)) == 0u)
			continue;
		PlaySFX(SFX_CURSOR);
		EraseCursor();
		wCurMenuItem = (uint8_t)(wCurMenuItem ^ 1u);
		wMenuCursorXOffset = (uint8_t)(wCurMenuItem * 4u + wLeftmostItemCursorX);
		wCursorBlinkCounter = 0u;
	}
}
/* <<< factory HandleYesOrNoMenu */

/* >>> factory CopyCardNameAndLevel */
CopyCardNameAndLevelResult CopyCardNameAndLevel(uint8_t a, uint8_t b, uint8_t c,
						uint8_t d, uint8_t e)
{
	return _CopyCardNameAndLevel(a, b, c, d, e);
}
/* <<< factory CopyCardNameAndLevel */

/* >>> factory ReloadCardListItems */
void ReloadCardListItems(void)
{
	uint8_t e = SYM_SPACE;
	uint8_t scroll = wListScrollOffset;
	uint8_t c = (uint8_t)(wMenuCursorYOffset - 1u);
	uint8_t up = SYM_SPACE;
	if (scroll != 0u)
		up = SYM_CURSOR_U;
	WriteByteToBGMap0(up, 18u, c);

	if ((uint8_t)(scroll + wNumMenuItems) < wNumListItems)
		e = SYM_CURSOR_D;
	uint8_t down_row = (uint8_t)((uint8_t)(wNumMenuItems + wNumMenuItems) + c - 1u);
	WriteByteToBGMap0(e, 18u, down_row);

	uint16_t hl = (uint16_t)(wDuelTempList_ADDR + scroll);
	uint8_t b = wNumMenuItems;
	uint8_t d = wListItemXPosition;
	e = wMenuCursorYOffset;
	c = 0u;
	while (b != 0u) {
		uint8_t a = gb_read8(hl);
		if (a == 0xFFu)
			break;
		uint8_t saved_b = b;
		uint8_t saved_c = c;
		uint8_t saved_d = d;
		uint8_t saved_e = e;
		(void)LoadCardDataToBuffer1_FromDeckIndex(a);
		DrawCardSymbol(saved_d, saved_e);
		InitTextPrinting(saved_d, saved_e);
		(void)CopyCardNameAndLevel(wListItemNameMaxLength, saved_b, saved_c, saved_d, saved_e);
		uint16_t text_hl = wDefaultText_ADDR;
		ProcessText(&text_hl);
		b = saved_b;
		c = saved_c;
		d = saved_d;
		e = saved_e;
		hl = (uint16_t)(hl + 1u);
		c = (uint8_t)(c + 1u);
		if (c >= wNumListItems)
			break;
		e = (uint8_t)(e + 2u);
		b = (uint8_t)(b - 1u);
	}
}
/* <<< factory ReloadCardListItems */

/* >>> factory Func_2827 */
void Func_2827(void)
{
	gb_write8(hffb0_ADDR, 0x01u);
	ReloadCardListItems();
	gb_write8(hffb0_ADDR, 0x00u);
}
/* <<< factory Func_2827 */

/* >>> factory PrintCardListItems */
void PrintCardListItems(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl)
{
	InitializeCardListParameters(a, d, e, hl);
	gb_write8(wMenuUpdateFunc_ADDR, (uint8_t)CARD_LIST_MENU_FUNCTION);
	gb_write8((uint16_t)(wMenuUpdateFunc_ADDR + 1u), (uint8_t)(CARD_LIST_MENU_FUNCTION >> 8));
	wMenuYSeparation = 2u;
	wCardListIndicatorYPosition = 1u;
	ReloadCardListItems();
}
/* <<< factory PrintCardListItems */

/* >>> factory CardListMenuFunction */
CardListMenuFunctionResult CardListMenuFunction(void)
{
	uint8_t keys = hDPadHeld;
	uint8_t count = (uint8_t)(wNumMenuItems - 1u);
	uint8_t cur = wCurMenuItem;
	/* menus.asm:436-481. `.no_more_items` -- the page cannot scroll past
	 * either end -- clears wRefreshMenuCursorSFX, so the buffered cursor
	 * SFX HandleMenuInput armed for the wrap stays silent. */
	if ((keys & PAD_UP) != 0u) {
		if (cur == count) {
			wCurMenuItem = 0u;
			if (wListScrollOffset != 0u) {
				wListScrollOffset = (uint8_t)(wListScrollOffset - 1u);
				ReloadCardListItems();
			} else {
				wRefreshMenuCursorSFX = 0u;
			}
		}
	} else if ((keys & PAD_DOWN) != 0u) {
		if (cur == 0u) {
			wCurMenuItem = count;
			if ((uint8_t)(wListScrollOffset + count + 1u) != wNumListItems) {
				wListScrollOffset = (uint8_t)(wListScrollOffset + 1u);
				ReloadCardListItems();
			} else {
				wRefreshMenuCursorSFX = 0u;
			}
		} else if ((uint8_t)(cur + wListScrollOffset) >= wNumListItems) {
			wCurMenuItem = (uint8_t)(cur - 1u);
			wRefreshMenuCursorSFX = 0u;
		}
	} else if ((keys & 0x20u) != 0u) {
		if (wListScrollOffset != 0u) {
			uint8_t next = (uint8_t)(wListScrollOffset - wNumMenuItems);
			if (wListScrollOffset >= wNumMenuItems) {
				wListScrollOffset = next;
				ReloadCardListItems();
			} else {
				/* menus.asm:495-508 .top_of_page_reached: the cursor
				 * keeps its absolute item, less one page if that item
				 * is beyond the first page (`sub [hl] / jr nc`). */
				uint8_t absolute = (uint8_t)(wListScrollOffset + cur);

				EraseCursor();
				wCurMenuItem = absolute >= wNumMenuItems
					? (uint8_t)(absolute - wNumMenuItems) : absolute;
				wListScrollOffset = 0u;
				wRefreshMenuCursorSFX = 0u;
				ReloadCardListItems();
			}
		}
	} else if ((keys & 0x10u) != 0u) {
		if (wNumMenuItems < wNumListItems) {
			uint8_t next = (uint8_t)(wListScrollOffset + wNumMenuItems);
			if ((uint8_t)(next + wNumMenuItems - 1u) < wNumListItems) {
				wListScrollOffset = next;
				ReloadCardListItems();
			} else {
				/* menus.asm:530-546 .asm_28f9: the last page; the
				 * cursor keeps its absolute item relative to the new
				 * scroll, plus one page when that goes negative. */
				uint8_t absolute = (uint8_t)(wListScrollOffset + cur);
				uint8_t relative;

				EraseCursor();
				wListScrollOffset = (uint8_t)(wNumListItems - wNumMenuItems);
				relative = (uint8_t)(absolute - wListScrollOffset);
				if (absolute < wListScrollOffset)
					relative = (uint8_t)(relative + wNumMenuItems);
				wCurMenuItem = relative;
				ReloadCardListItems();
			}
		}
	}
	uint8_t selected = (uint8_t)(wListScrollOffset + wCurMenuItem);
	hCurMenuItem = selected;
	if (wCardListIndicatorYPosition != 0xFFu) {
		uint8_t y = wCardListIndicatorYPosition;
		TxSymbolResult first = OneByteNumberToTxSymbol_PadSpace((uint8_t)(selected + 1u));
		uint16_t first_hl = first.hl;
		uint16_t first_de = 0u;
		CopyDataToBGMap0(2u, &first_hl, &first_de, 13u, y);
		WriteByteToBGMap0(SYM_SLASH, 15u, y);
		TxSymbolResult total = OneByteNumberToTxSymbol_PadSpace(wNumListItems);
		uint16_t total_hl = total.hl;
		uint16_t total_de = 0u;
		CopyDataToBGMap0(2u, &total_hl, &total_de, 16u, y);
	}
	/* menus.asm:573-581 `jp hl` on wListFunctionPointer with a = hCurMenuItem:
	 * the function's own exit is this one's. CardListFunction ($01:5719,
	 * CardListParameters) is the only list function the asm installs. */
	uint16_t list_fn = (uint16_t)(wListFunctionPointer |
	                              ((uint16_t)gb_read8((uint16_t)(wListFunctionPointer_ADDR + 1u)) << 8));
	if (list_fn == CARD_LIST_FUNCTION) {
		CardListFunctionResult r = CardListFunction();
		return (CardListMenuFunctionResult){r.a, r.f};
	}
	if (list_fn != 0u) {
		DispatchIndirect("wListFunctionPointer", list_fn);
		return (CardListMenuFunctionResult){0u, 0x00u};
	}
	uint8_t pressed = (uint8_t)(hKeysPressed & (PAD_A | PAD_B));
	if (pressed == 0u)
		return (CardListMenuFunctionResult){0u, 0xA0u};
	if ((pressed & PAD_B) != 0u) {
		hCurMenuItem = 0xFFu;
		return (CardListMenuFunctionResult){0xFFu, 0x10u};
	}
	return (CardListMenuFunctionResult){0u, 0x10u};
}
/* <<< factory CardListMenuFunction */

/* >>> factory HandleMenuInput */
HandleMenuInputResult HandleMenuInput(void)
{
	wRefreshMenuCursorSFX = 0u;
	uint8_t dpad = hDPadHeld;
	if (dpad != 0u) {
		uint8_t count = wNumMenuItems;
		uint8_t item = wCurMenuItem;
		if ((dpad & PAD_UP) != 0u) {
			item = (uint8_t)(item - 1u);
			if ((item & 0x80u) != 0u)
				item = (uint8_t)(wNumMenuItems - 1u);
			wRefreshMenuCursorSFX = 1u;
			EraseCursor();
			wCurMenuItem = item;
			wCursorBlinkCounter = 0u;
		} else if ((dpad & PAD_DOWN) != 0u) {
			item = (uint8_t)(item + 1u);
			if (item >= count)
				item = 0u;
			wRefreshMenuCursorSFX = 1u;
			EraseCursor();
			wCurMenuItem = item;
			wCursorBlinkCounter = 0u;
		}
	}
	hCurMenuItem = wCurMenuItem;

	/* menus.asm:113-122 `call CallHL` on wMenuUpdateFunc: the two functions
	 * ever installed are CardListMenuFunction (home, by PrintCardListItems)
	 * and PlayAreaScreenMenuFunction ($01:60CE, by the play area screen's
	 * menu parameter blocks). Carry from either takes the A-pressed exit;
	 * anything else registered is an unported target. */
	uint16_t update = (uint16_t)(wMenuUpdateFunc |
	                             ((uint16_t)gb_read8((uint16_t)(wMenuUpdateFunc_ADDR + 1u)) << 8));
	if (update != 0u) {
		uint8_t update_a, update_f;
		if (update == CARD_LIST_MENU_FUNCTION) {
			CardListMenuFunctionResult r = CardListMenuFunction();
			update_a = r.a;
			update_f = r.f;
		} else if (update == PLAY_AREA_SCREEN_MENU_FUNCTION) {
			update_f = PlayAreaScreenMenuFunction();
			update_a = hCurMenuItem;
		} else {
			DispatchIndirect("wMenuUpdateFunc", update);
			update_a = 0u;
			update_f = 0u;
		}
		if ((update_f & 0x10u) == 0u)
			return RefreshMenuCursor_CheckPlaySFXRegs();
		DrawCursor2();
		uint8_t drawn_tile = wMenuVisibleCursorTile;
		uint8_t z_bit = (drawn_tile == 0u) ? 0x80u : 0u;
		(void)PlayOpenOrExitScreenSFX(update_a, (uint8_t)(z_bit));
		uint8_t e2 = wCurMenuItem;
		uint8_t a2 = hCurMenuItem;
		return (HandleMenuInputResult){a2, e2, (uint8_t)(0x10u | z_bit)};
	}

	uint8_t pressed = (uint8_t)(hKeysPressed & (PAD_A | PAD_B));
	if (pressed == 0u)
		return RefreshMenuCursor_CheckPlaySFXRegs();
	if ((pressed & PAD_A) != 0u) {
		DrawCursor2();
		uint8_t drawn_tile = wMenuVisibleCursorTile;
		uint8_t z_bit = (drawn_tile == 0u) ? 0x80u : 0u;
		(void)PlayOpenOrExitScreenSFX(0u, z_bit);
		uint8_t e2 = wCurMenuItem;
		uint8_t a2 = hCurMenuItem;
		return (HandleMenuInputResult){a2, e2, (uint8_t)(0x10u | z_bit)};
	}
	uint8_t e2 = wCurMenuItem;
	hCurMenuItem = 0xFFu;
	(void)PlayOpenOrExitScreenSFX(0u, 0x80u);
	return (HandleMenuInputResult){0xFFu, e2, 0x90u};
}
/* <<< factory HandleMenuInput */

/* >>> factory HandleCardListInput */
HandleCardListInputResult HandleCardListInput(void)
{
	HandleMenuInputResult input = HandleMenuInput();
	HandleCardListInputResult result = {input.a, 0u, input.e, input.f};
	if ((input.f & 0x10u) == 0u)
		return result;
	result.d = wListScrollOffset;
	result.e = wCurMenuItem;
	result.a = hCurMenuItem;
	return result;
}
/* <<< factory HandleCardListInput */

/* >>> factory HandleDuelMenuInput */
HandleMenuInputResult HandleDuelMenuInput(uint8_t e)
{
	static const uint8_t coords[12] = {2u,14u, 2u,16u, 8u,14u, 8u,16u, 14u,14u, 14u,16u};
	uint8_t dpad = hDPadHeld;
	if (dpad != 0u) {
		uint8_t b = dpad;
		uint8_t item = wCurMenuItem;
		uint8_t moved = 1u;
		if ((b & (PAD_UP | PAD_DOWN)) != 0u) {
			item = (uint8_t)(item ^ 1u);
		} else if ((b & PAD_LEFT) != 0u) {
			if (item >= 2u)
				item = (uint8_t)(item - 2u);
			else
				item = (uint8_t)((item & 1u) + 4u);
		} else if ((b & PAD_RIGHT) != 0u) {
			item = (uint8_t)(item + 2u);
			if (item >= 6u)
				item = (uint8_t)(item & 1u);
		} else {
			moved = 0u;
			if ((b & PAD_A) != 0u) {
				(void)PlayOpenOrExitScreenSFX(0u, 0x00u);
				uint8_t e2 = wCurMenuItem;
				uint8_t a2 = hCurMenuItem;
				return (HandleMenuInputResult){a2, e2, 0x10u};
			}
		}
		if (moved != 0u) {
			PlaySFX(SFX_CURSOR);
			uint8_t old_item = wCurMenuItem;
			WriteByteToBGMap0(SYM_SPACE, coords[(uint8_t)(old_item * 2u)], coords[(uint8_t)(old_item * 2u + 1u)]);
			wCurMenuItem = item;
			hCurMenuItem = item;
			wCursorBlinkCounter = 0u;
		}
	}
	uint8_t counter = wCursorBlinkCounter;
	wCursorBlinkCounter = (uint8_t)(counter + 1u);
	uint8_t masked = (uint8_t)(counter & 0x0Fu);
	if (masked != 0u)
		return (HandleMenuInputResult){masked, e, 0x20u};
	uint8_t item2 = wCurMenuItem;
	uint8_t tile = ((wCursorBlinkCounter & 0x10u) != 0u) ? SYM_SPACE : SYM_CURSOR_R;
	WriteByteToBGMap0(tile, coords[(uint8_t)(item2 * 2u)], coords[(uint8_t)(item2 * 2u + 1u)]);
	return (HandleMenuInputResult){item2, item2, (item2 == 0u) ? 0x80u : 0x00u};
}
/* <<< factory HandleDuelMenuInput */

/* >>> factory YesOrNoMenuWithText_LeftAligned */
HandleYesOrNoMenuResult YesOrNoMenuWithText_LeftAligned(uint16_t hl, uint8_t b, uint8_t c)
{
	(void)DrawNarrowTextBox_PrintTextNoDelay(hl);
	(void)PrintYesOrNoItems(3u, 16u);
	return HandleYesOrNoMenu(2u, 16u, b, c);
}
/* <<< factory YesOrNoMenuWithText_LeftAligned */

/* >>> factory TwoItemHorizontalMenu */
HandleYesOrNoMenuResult TwoItemHorizontalMenu(uint16_t hl)
{
	(void)DrawWideTextBox_PrintText(hl);
	wLeftmostItemCursorX = 6u;
	(void)SetCursorParametersForTextBox(6u, 16u, SYM_CURSOR_R, SYM_SPACE);
	wCurMenuItem = 1u;
	EnableLCD();
	/* jp target lands inside .refresh_menu, whose own xor $1 flips */
	/* wCurMenuItem unconditionally before the wait loop begins. */
	wCurMenuItem = (uint8_t)(wCurMenuItem ^ 1u);
	wMenuCursorXOffset = (uint8_t)(wCurMenuItem * 4u + wLeftmostItemCursorX);
	wCursorBlinkCounter = 0u;
	for (;;) {
		DoFrame();
		RefreshMenuCursor();
		if ((hKeysPressed & PAD_A) != 0u) {
			hCurMenuItem = wCurMenuItem;
			if (wCurMenuItem == 0u) {
				wDefaultYesOrNo = 0u;
				return (HandleYesOrNoMenuResult){0u, 0x80u};
			}
			wDefaultYesOrNo = 0u;
			hCurMenuItem = 1u;
			return (HandleYesOrNoMenuResult){1u, 0x90u};
		}
		if ((hDPadHeld & (PAD_RIGHT | PAD_LEFT)) == 0u)
			continue;
		PlaySFX(SFX_CURSOR);
		EraseCursor();
		wCurMenuItem = (uint8_t)(wCurMenuItem ^ 1u);
		wMenuCursorXOffset = (uint8_t)(wCurMenuItem * 4u + wLeftmostItemCursorX);
		wCursorBlinkCounter = 0u;
	}
}
/* <<< factory TwoItemHorizontalMenu */

/* >>> factory YesOrNoMenu */
HandleYesOrNoMenuResult YesOrNoMenu(void)
{
	(void)PrintYesOrNoItems(7u, 16u);
	return HandleYesOrNoMenu(6u, 16u, 0u, 0u);
}
/* <<< factory YesOrNoMenu */

/* >>> factory YesOrNoMenuWithText */
HandleYesOrNoMenuResult YesOrNoMenuWithText(uint16_t hl)
{
	(void)DrawWideTextBox_PrintText(hl);
	return YesOrNoMenu();
}
/* <<< factory YesOrNoMenuWithText */

/* >>> factory YesOrNoMenuWithText_SetCursorToYes */
HandleYesOrNoMenuResult YesOrNoMenuWithText_SetCursorToYes(uint16_t hl)
{
	wDefaultYesOrNo = 1u;
	return YesOrNoMenuWithText(hl);
}
/* <<< factory YesOrNoMenuWithText_SetCursorToYes */

/* >>> factory ContinueDuel */
void ContinueDuel(void)
{
	BankswitchROM(CONTINUE_DUEL_BANK);
	_ContinueDuel();
}
/* <<< factory ContinueDuel */
