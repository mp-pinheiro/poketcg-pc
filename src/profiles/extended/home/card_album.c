/* === part includes */
/* >>> part MENU_CONFIRM */
#define MENU_CONFIRM 0x01u
/* <<< part MENU_CONFIRM */
/* --- part includes_tail */
/* >>> part includes_tail */
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes_tail */
/* === part PAD_BUTTONS */
/* >>> part includes_tail_2 */
#include "home/deck_configuration.h"
#include "home/card_album.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#include "generated/sram.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
/* <<< part includes_tail_2 */
/* >>> factory PrintCardSetListEntries */
/* card_album.asm:270-460. The list index goes into wCurDeckName after the
 * set's two-byte prefix; the energy rows print from that offset, the others
 * from the prefix. Fullwidth "E" is $03,$34 and "×" is $6c in this charmap. */
#define CARD_ALBUM_INDEX_E_HI 0x03u
#define CARD_ALBUM_INDEX_E_LO 0x34u
#define CARD_ALBUM_INDEX_PHANTOM 0x6Cu
#define CARD_ALBUM_EMPTY_SLOT_DASH 0x6Bu
#define CARD_ALBUM_EMPTY_SLOT_DASHES 13u

static uint16_t card_album_append_list_index(uint16_t index, uint8_t b)
{
	uint16_t card_addr = (uint16_t)(wFilteredCardList_ADDR + (index - 1u) * 2u);
	CardId card = card_id_read_at(card_addr);
	uint16_t hl = (uint16_t)(wCurDeckName_ADDR + 2u);
	if (card <= DOUBLE_COLORLESS_ENERGY) {
		CalculateOnesAndTensDigits(card);
		uint8_t ones = gb_read8(wDecimalDigitsSymbols_ADDR);
		gb_write8(hl++, CARD_ALBUM_INDEX_E_HI);
		gb_write8(hl++, CARD_ALBUM_INDEX_E_LO);
		gb_write8(hl++, TX_SYMBOL);
		gb_write8(hl++, SYM_0);
		gb_write8(hl++, TX_SYMBOL);
		gb_write8(hl++, ones);
		gb_write8(hl++, TX_SYMBOL);
		gb_write8(hl++, SYM_SPACE);
		gb_write8(hl, SYM_SPACE);
		return (uint16_t)(wCurDeckName_ADDR + 2u);
	}
	if (card == VENUSAUR_LV64 || card == MEW_LV15) {
		gb_write8(hl++, CARD_ALBUM_INDEX_PHANTOM);
		gb_write8(hl++, CARD_ALBUM_INDEX_PHANTOM);
		gb_write8(hl++, TX_SYMBOL);
		gb_write8(hl++, SYM_SPACE);
		gb_write8(hl, SYM_SPACE);
		return wCurDeckName_ADDR;
	}
	uint8_t position = (uint8_t)(wNumVisibleCardListEntries - b + wCardListVisibleOffset + 1u);
	CalculateOnesAndTensDigits(position);
	uint8_t ones = gb_read8(wDecimalDigitsSymbols_ADDR);
	uint8_t tens = gb_read8((uint16_t)(wDecimalDigitsSymbols_ADDR + 1u));
	if (tens == 0u)
		tens = SYM_0;
	gb_write8(hl++, TX_SYMBOL);
	gb_write8(hl++, tens);
	gb_write8(hl++, TX_SYMBOL);
	gb_write8(hl++, ones);
	gb_write8(hl++, TX_SYMBOL);
	gb_write8(hl++, SYM_SPACE);
	gb_write8(hl, SYM_SPACE);
	return wCurDeckName_ADDR;
}

PrintCardSetListEntriesResult PrintCardSetListEntries(void)
{
	uint8_t y = gb_read8(wCardListCoords_ADDR);
	uint8_t x = gb_read8((uint16_t)(wCardListCoords_ADDR + 1u));
	uint16_t index = wCardListVisibleOffset;
	uint8_t b = wNumVisibleCardListEntries;
	(void)WriteByteToBGMap0(
		index != 0u ? SYM_CURSOR_U : SYM_BOX_TOP_R, 19u, (uint8_t)(y - 2u));
	for (;;) {
		if (b == 0u) {
			uint16_t hl = (uint16_t)(wFilteredCardList_ADDR + index * 2u);
			uint8_t low = gb_read8(hl++);
			uint8_t high = gb_read8(hl);
			wUnableToScrollDown = (uint8_t)((low | high) == 0u);
			(void)WriteByteToBGMap0(
				wUnableToScrollDown ? SYM_BOX_BTM_R : SYM_CURSOR_D, 19u, 17u);
			return (PrintCardSetListEntriesResult){ .hl = hl };
		}
		uint16_t list_addr =
			(uint16_t)(wFilteredCardList_ADDR + index * 2u);
		CardId card = card_id_read_at(list_addr);
		index++;
		if (card == 0u) {
			wUnableToScrollDown = TRUE;
			(void)WriteByteToBGMap0(SYM_BOX_BTM_R, 19u, 17u);
			return (PrintCardSetListEntriesResult){
				.hl = (uint16_t)(wFilteredCardList_ADDR + index * 2u + 1u)};
		}
		AddCardIDToVisibleList(b, card);
		LoadCardDataToBuffer1_FromCardID(card);
		if (gb_read8((uint16_t)(wOwnedCardsCountList_ADDR + index - 1u))
			== CARD_NOT_OWNED) {
			uint16_t de = wDefaultText_ADDR;
			for (uint8_t i = 0; i < CARD_ALBUM_EMPTY_SLOT_DASHES; i++)
				gb_write8(de++, CARD_ALBUM_EMPTY_SLOT_DASH);
			gb_write8(de, TX_END);
		} else {
			(void)CopyCardNameAndLevel(13u, b, (uint8_t)index, x, (uint8_t)card);
		}
		InitTextPrinting(x, y);
		uint16_t text = card_album_append_list_index(index, b);
		ProcessText(&text);
		text = wDefaultText_ADDR;
		ProcessText(&text);
		b--;
		y = (uint8_t)(y + 2u);
	}
}
/* <<< factory PrintCardSetListEntries */
/* >>> factory CreateCardSetList */
void CreateCardSetList(uint8_t a)
{
	uint8_t set = a;
	ClearMemory_Bank2((uint8_t)((MAX_NUM_CARDS_PER_TYPE + 1u) * 2u),
		wFilteredCardList_ADDR);
	ClearMemory_Bank2(DECK_SIZE, wOwnedCardsCountList_ADDR);
	wOwnedPhantomCardFlags = 0u;

	uint16_t list_index = 0u;
	for (CardId card_id = 1u; card_id <= NUM_CARDS; card_id++) {
		LoadCardDataToBuffer1_FromCardID(card_id);
		if (((uint8_t)(wLoadedCard1Set & 0xF0u) >> 4) != set)
			continue;
		if (card_id == VENUSAUR_LV64) {
			if (gb_read8((uint16_t)(wTempCardCollection_ADDR + card_id))
				!= CARD_NOT_OWNED)
				wOwnedPhantomCardFlags |= 0x01u;
			continue;
		}
		if (card_id == MEW_LV15) {
			if (gb_read8((uint16_t)(wTempCardCollection_ADDR + card_id))
				!= CARD_NOT_OWNED)
				wOwnedPhantomCardFlags |= 0x02u;
			continue;
		}
		uint16_t list_addr = (uint16_t)(wFilteredCardList_ADDR + list_index * 2u);
		gb_write8(list_addr, (uint8_t)card_id);
		gb_write8((uint16_t)(list_addr + 1u), (uint8_t)(card_id >> 8));
		gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + list_index),
			gb_read8((uint16_t)(wTempCardCollection_ADDR + card_id)));
		list_index++;
	}

	if (set == 0u) {
		for (CardId card_id = 1u; card_id < 7u; card_id++) {
			uint16_t list_addr =
				(uint16_t)(wFilteredCardList_ADDR + list_index * 2u);
			gb_write8(list_addr, (uint8_t)card_id);
			gb_write8((uint16_t)(list_addr + 1u), (uint8_t)(card_id >> 8));
			gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + list_index),
				gb_read8((uint16_t)(wTempCardCollection_ADDR + card_id)));
			list_index++;
		}
	} else if (set == CARD_SET_MYSTERY) {
		CardId card_id = DOUBLE_COLORLESS_ENERGY;
		uint16_t list_addr =
			(uint16_t)(wFilteredCardList_ADDR + list_index * 2u);
		gb_write8(list_addr, (uint8_t)card_id);
		gb_write8((uint16_t)(list_addr + 1u), (uint8_t)(card_id >> 8));
		gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + list_index),
			gb_read8((uint16_t)(wTempCardCollection_ADDR + card_id)));
		list_index++;
	}

	uint8_t c = (uint8_t)(list_index - 1u);
	while (gb_read8((uint16_t)(wOwnedCardsCountList_ADDR + c))
		== CARD_NOT_OWNED)
		c--;
	c++;
	wNumEntriesInCurFilter = c;
	gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + c), 0xFFu);
	uint16_t terminator = (uint16_t)(wFilteredCardList_ADDR + (uint16_t)c * 2u);
	gb_write8(terminator, 0u);
	gb_write8((uint16_t)(terminator + 1u), 0u);
}
/* <<< factory CreateCardSetList */
/* === factory CreateCardSetListAndInitListCoords */
/* === factory HandleCardAlbumCardPage */
/* === factory CardAlbum */
