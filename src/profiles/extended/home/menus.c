/* --- part includes_CONTINUE_DUEL_BANK */
/* --- part CONTINUE_DUEL_BANK */
/* === part SYM_SLASH */
/* >>> part includes_SYM_0 */
#include "home/menus.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "generated/hram.h"
/* <<< part includes_SYM_0 */
/* >>> part CARD_SYMBOL_TABLE */
#define CARD_SYMBOL_TABLE 0x20C5u
/* <<< part CARD_SYMBOL_TABLE */
/* --- factory OneByteNumberToTxSymbol_PadSpace */
/* --- factory OneByteNumberToTxSymbol_TrimLeadingZeroAndAlign */
/* === factory OneByteNumberToTxSymbol */
/* >>> factory OneByteNumberToTxSymbol_TrimLeadingZeros */
TxSymbolResult OneByteNumberToTxSymbol_TrimLeadingZeros(uint8_t a)
{
	TxSymbolResult result = tx_symbol_core(a);
	uint8_t first = gb_read8(result.hl);
	if (first == SYM_0)
		gb_write8(result.hl, SYM_SPACE);
	result.a = first;
	return result;
}
/* <<< factory OneByteNumberToTxSymbol_TrimLeadingZeros */
/* >>> factory DrawCardSymbol */
void DrawCardSymbol(uint8_t d, uint8_t e)
{
	uint8_t id = CardTypeToSymbolID();
	uint16_t entry = (uint16_t)(CARD_SYMBOL_TABLE + (uint16_t)id * 2);
	uint8_t tile = gb_read8(entry);
	uint8_t x = (uint8_t)(d - 2);
	uint8_t y = (uint8_t)(e - 1);

	uint8_t attr = gb_read8((uint16_t)(entry + 1));
	hBankVRAM = 1;
	gb_write8(0xff4f, 1);
	fill_symbol_2x2(attr, x, y, 0, 0);
	hBankVRAM = 0;
	gb_write8(0xff4f, 0);
	fill_symbol_2x2(tile, x, y, 1, 2);
}
/* <<< factory DrawCardSymbol */
/* --- part NTBM_PARAMS */
/* --- part DrawNarrowTextBox_WaitForInput */
/* --- factory Func_2827 */
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
		TxSymbolResult first = OneByteNumberToTxSymbol_TrimLeadingZeros((uint8_t)(selected + 1u));
		uint16_t first_hl = first.hl;
		uint16_t first_de = 0u;
		CopyDataToBGMap0(2u, &first_hl, &first_de, 13u, y);
		WriteByteToBGMap0(SYM_SLASH, 15u, y);
		TxSymbolResult total = OneByteNumberToTxSymbol_TrimLeadingZeros(wNumListItems);
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
/* --- factory ContinueDuel */
/* --- part DrawWideTextBox_PrintTextNoDelay_Wait */
