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
/* >>> factory CardAlbum */
#define CARD_ALBUM_BOOSTER_PACK_MENU_PARAMS (CardAlbum_ADDR + 0xEDu)
#define CARD_ALBUM_BOOSTER_PACK_CARDS_MENU_PARAMS (CardAlbum_ADDR + 0xF5u)
#define CARD_ALBUM_BOOSTER_PACKS_MENU_DATA (CardAlbum_ADDR + 0x24Au)
#define MENU_CANCEL 0xFFu
#define PAD_B 0x02u
#define PAD_START 0x08u
#define SYM_SLASH 0x2Eu

static uint8_t card_album_num_card_entries(void)
{
	uint8_t count = 0u;
	for (uint16_t hl = wFilteredCardList_ADDR; gb_read8(hl) != 0u; hl++)
		count++;
	wNumCardListEntries = count;
	return count;
}

static void card_album_count_owned_cards_in_set(void)
{
	uint8_t count = 0u;
	for (uint16_t hl = wOwnedCardsCountList_ADDR;; hl++) {
		uint8_t entry = gb_read8(hl);
		if (entry == 0xffu)
			break;
		if (entry != CARD_NOT_OWNED)
			count++;
	}
	wNumOwnedCardsInSet = count;
}

static void card_album_load_screen_tiles(void)
{
	wVBlankOAMCopyToggle = TRUE;
	LoadCursorTile();
	(void)LoadSymbolsFont();
	(void)LoadDuelCardSymbolTiles();
	SetDefaultConsolePalettes();
	(void)SetupText(0x3cu, 0xffu);
}

static void card_album_print_card_count(void)
{
	Set_OBJ_8x8();
	wTileMapFill = 0u;
	ZeroObjectPositions();
	EmptyScreen();
	card_album_load_screen_tiles();
	InitTextPrinting(1u, 1u);
	uint16_t title;
	uint8_t total;
	switch (wSelectedCardSet) {
	case CARD_SET_PROMOTIONAL:
		title = Item5PromotionalCardText;
		total = NUM_CARDS_PROMOTIONAL - 2u;
		if ((wOwnedPhantomCardFlags & (1u << VENUSAUR_OWNED_PHANTOM_F)) != 0u)
			total++;
		if ((wOwnedPhantomCardFlags & (1u << MEW_OWNED_PHANTOM_F)) != 0u)
			total++;
		break;
	case CARD_SET_LABORATORY:
		title = Item4LaboratoryText;
		total = NUM_CARDS_LABORATORY;
		break;
	case CARD_SET_MYSTERY:
		title = Item3MysteryText;
		total = NUM_CARDS_MYSTERY;
		break;
	case CARD_SET_EVOLUTION:
		title = Item2EvolutionText;
		total = NUM_CARDS_EVOLUTION;
		break;
	default:
		title = Item1ColosseumText;
		total = NUM_CARDS_COLOSSEUM;
		break;
	}
	(void)ProcessTextFromID(title);
	card_album_count_owned_cards_in_set();
	InitTextPrinting(14u, 1u);
	ConvertToNumericalDigitsResult digits = ConvertToNumericalDigits(wNumOwnedCardsInSet, wDefaultText_ADDR);
	CalculateOnesAndTensDigits(digits.a);
	uint16_t hl = digits.hl;
	gb_write8(hl++, TX_SYMBOL);
	gb_write8(hl++, SYM_SLASH);
	digits = ConvertToNumericalDigits(total, hl);
	gb_write8(digits.hl, TX_END);
	uint16_t text = wDefaultText_ADDR;
	ProcessText(&text);
	uint16_t box = 0u;
	DrawRegularTextBox(&box, 0u, 20u, 16u, 0u, 2u);
	EnableLCD();
}

static void card_album_show_booster_pack_menu(void)
{
	wTileMapFill = 0u;
	EmptyScreen();
	if (hffb4 == 1u) {
		hffb4 = 0u;
		Set_OBJ_8x8();
		ZeroObjectPositions();
		card_album_load_screen_tiles();
	}
	uint16_t box = 0u;
	DrawRegularTextBox(&box, 0u, 20u, 13u, 0u, 0u);
	(void)PlaceTextItems(CARD_ALBUM_BOOSTER_PACKS_MENU_DATA);
	ClearMemory_Bank2(NUM_CARD_SETS, wUnavailableAlbumCardSets_ADDR);
	EnableSRAM();
	uint8_t has_promotional = sHasPromotionalCards;
	DisableSRAM();
	if (has_promotional == 0u) {
		CreateCardSetListAndInitListCoords(CARD_SET_PROMOTIONAL);
		if (gb_read8(wFilteredCardList_ADDR) != 0u) {
			EnableSRAM();
			sHasPromotionalCards = TRUE;
			DisableSRAM();
		} else {
			gb_write8((uint16_t)(wUnavailableAlbumCardSets_ADDR + CARD_SET_PROMOTIONAL), TRUE);
			InitTextPrinting(5u, 11u);
			(void)ProcessTextFromID(EmptyPromotionalCardText);
		}
	}
	(void)DrawWideTextBox_PrintText(ViewWhichCardFileText);
	EnableLCD();
}

void CardAlbum(void)
{
	hffb4 = 1u;
	uint8_t cursor = 0u;
	for (;;) { /* .booster_pack_menu */
		uint16_t params = CARD_ALBUM_BOOSTER_PACK_MENU_PARAMS;
		InitializeMenuParameters(cursor, &params);
		card_album_show_booster_pack_menu();
		uint8_t set;
		for (;;) { /* .loop_input_1 */
			DoFrame();
			if ((HandleMenuInput().f & 0x10u) == 0u)
				continue;
			set = hCurMenuItem;
			if (set == MENU_CANCEL)
				return;
			if (gb_read8((uint16_t)(wUnavailableAlbumCardSets_ADDR + set)) == 0u)
				break;
		}
		wSelectedCardSet = set;
		CreateCardSetListAndInitListCoords(set);
		card_album_print_card_count();
		wCardListVisibleOffset = 0u;
		(void)PrintCardSetListEntries();
		EnableLCD();
		if (wNumEntriesInCurFilter == 0u) {
			do { /* .loop_input_2 */
				DoFrame();
			} while ((hKeysPressed & PAD_B) == 0u);
			PlaySFXConfirmOrCancel(MENU_CANCEL);
			cursor = hCurMenuItem;
			continue;
		}
		(void)card_album_num_card_entries();
		uint16_t list_params = CARD_ALBUM_BOOSTER_PACK_CARDS_MENU_PARAMS;
		(void)InitCardSelectionParams(0u, &list_params);
		if (wNumEntriesInCurFilter < wNumVisibleCardListEntries)
			wCardListNumCursorPositions = wNumEntriesInCurFilter;
		gb_write8(wCardListUpdateFunction_ADDR, (uint8_t)PRINT_CARD_SET_LIST_ENTRIES);
		gb_write8((uint16_t)(wCardListUpdateFunction_ADDR + 1u), (uint8_t)(PRINT_CARD_SET_LIST_ENTRIES >> 8));
		wced2 = 0u;
		for (;;) { /* .loop_input_3 */
			DoFrame();
			HandleDeckCardSelectionListResult selection = HandleDeckCardSelectionList();
			if ((selection.f & 0x10u) != 0u) {
				(void)DrawListCursor_Invisible();
				wTempCardListCursorPos = wCardListCursorPos;
				if (hffb3 == MENU_CANCEL)
					break;
			} else {
				if ((HandleLeftRightInCardList().f & 0x10u) != 0u)
					continue;
				if ((hDPadHeld & PAD_START) == 0u)
					continue;
			}
			/* .open_card_page */
			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			wTempCardListNumCursorPositions = wCardListNumCursorPositions;
			wTempCardListCursorPos = wCardListCursorPos;
			uint8_t index = (uint8_t)(wCardListVisibleOffset + wCardListCursorPos);
			if (gb_read8((uint16_t)(wOwnedCardsCountList_ADDR + index)) == CARD_NOT_OWNED)
				continue;
			gb_write8(wCurCardListPtr_ADDR, (uint8_t)wFilteredCardList_ADDR);
			gb_write8((uint16_t)(wCurCardListPtr_ADDR + 1u), (uint8_t)(wFilteredCardList_ADDR >> 8));
			(void)GetFirstOwnedCardIndex();
			(void)HandleCardAlbumCardPage((uint8_t)(wFilteredCardList_ADDR >> 8), (uint8_t)wFilteredCardList_ADDR);
			card_album_print_card_count();
			(void)PrintCardSetListEntries();
			EnableLCD();
			list_params = CARD_ALBUM_BOOSTER_PACK_CARDS_MENU_PARAMS;
			/* card_album.asm:721-722 passes EnableLCD's a, the wLCDC value, as the
			 * cursor position; the real position is restored below but hffb3 keeps it. */
			(void)InitCardSelectionParams(wLCDC, &list_params);
			wCardListNumCursorPositions = wTempCardListNumCursorPositions;
			wCardListCursorPos = wTempCardListCursorPos;
		}
		cursor = hCurMenuItem;
	}
}
/* <<< factory CardAlbum */
/* === factory CreateCardSetListAndInitListCoords */
/* === factory HandleCardAlbumCardPage */
