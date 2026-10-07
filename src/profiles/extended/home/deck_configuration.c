/* >>> part includes */
#include "home/deck_configuration.h"

#include <stdio.h>
#include <stdlib.h>

#include "generated/text_ids.h"
#include "generated/constants.h"
/* <<< part includes */
/* >>> part MENU_CONFIRM */
#define MENU_CONFIRM 0x01u
/* <<< part MENU_CONFIRM */
/* >>> part CURSOR_BLINK_PERIOD_MASK */
#define CURSOR_BLINK_PERIOD_MASK 0x0Fu
/* <<< part CURSOR_BLINK_PERIOD_MASK */
/* >>> part B_CURSOR_BLINK_PERIOD */
#define B_CURSOR_BLINK_PERIOD 4u
/* <<< part B_CURSOR_BLINK_PERIOD */
/* >>> part includes_tail */
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes_tail */
/* >>> part HFFB3 */
#define HFFB3 0xffb3u
/* <<< part HFFB3 */
/* >>> part includes_SYM_SPACE */
#include "home/deck_configuration.h"

#include "home/deck_selection.h"
#include "home/switch_sram.h"


#include "home/tiles.h"

#include "generated/wram.h"
#include "home/switch_sram.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_id_bus.h"
#include "home/load_deck.h"
#include "home/deck_configuration.h"
#include "home/switch_sram.h"


#include "generated/wram.h"

#include "home/switch_sram.h"
#include "mem.h"

#include "home/empty_screen.h"
#include "home/deck_configuration.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/deck_configuration.h"
#include "home/process_text.h"
/* <<< part includes_SYM_SPACE */
/* >>> part CARD_LIST_MISSING_CARDS_ADDR */
#define CARD_LIST_MISSING_CARDS_ADDR (HandleDeckMissingCardsList__DeckConfirmationCardSelectionParams_ADDR)
/* <<< part CARD_LIST_MISSING_CARDS_ADDR */
/* --- part CARD_LIST_SHOW_RECEIVED_ADDR */
/* --- part SEND_DECK_CONFIGURATION_MENU_HANDLER */
/* --- part includes_HANDLE_SEND_DECK_CONFIGURATION_MENU_DATA_ADDR */
/* --- part HANDLE_SEND_DECK_CONFIGURATION_MENU_DATA_ADDR */
/* --- part DATA_B04A_ADDR */
/* --- part CANCEL_SEND_DECK_CONFIGURATION_ADDR */
/* >>> part includes_PREPARE_TO_BUILD_DECK_TEXT_ADDR */
#include "home/card_album.h"
#include "home/deck_configuration.h"
#include "home/deck_machine.h"
#include "home/indirect_dispatch.h"
#include "home/duel.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "home/text_box.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/deck_configuration.h"
#include "home/deck_selection.h"
#include "generated/wram.h"
/* <<< part includes_PREPARE_TO_BUILD_DECK_TEXT_ADDR */
/* >>> factory DecrementDeckCardsInCollection */
/* deck_configuration.asm:4-21 */
uint16_t DecrementDeckCardsInCollection(uint16_t hl)
{
	uint16_t p = hl;
	for (uint8_t d = 0u; d < DECK_SIZE; d++) {
		CardId id = card_id_read(&p);
		if (id == 0u)
			break;
		uint16_t addr = (uint16_t)(sCardCollection_ADDR + id);
		gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));
	}
	return hl;
}
/* <<< factory DecrementDeckCardsInCollection */
/* >>> factory AddDeckToCollection */
/* deck_configuration.asm:74-91 */
uint16_t AddDeckToCollection(uint16_t hl)
{
	uint16_t source = hl;
	uint8_t remaining = DECK_SIZE;
	while (remaining != 0u) {
		uint8_t command = gb_read8(source++);
		for (uint8_t bit = 0u; bit < 8u && remaining != 0u; bit++) {
			CardId id = gb_read8(source++);
			if ((command & 0x80u) != 0u)
				id = (CardId)(id | 0x0100u);
			uint16_t addr = (uint16_t)(sCardCollection_ADDR + id);
			gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
			command = (uint8_t)(command << 1);
			remaining = (uint8_t)(remaining - 1u);
		}
	}
	return hl;
}
/* <<< factory AddDeckToCollection */
/* === factory CalculateOnesAndTensDigits */
/* >>> factory CalculateOnesAndTensDigits_Long */
void CalculateOnesAndTensDigits_Long(uint16_t hl)
{
	const uint16_t places[5] = {10000u, 1000u, 100u, 10u, 1u};
	uint16_t output = wDecimalDigitsSymbols_ADDR;
	for (uint8_t i = 0u; i < 5u; i++) {
		uint8_t digit = 0u;
		while (hl >= places[i]) {
			hl = (uint16_t)(hl - places[i]);
			digit = (uint8_t)(digit + 1u);
		}
		gb_write8(output++, (uint8_t)(SYM_0 + digit));
	}
}
/* <<< factory CalculateOnesAndTensDigits_Long */
/* >>> factory CountNumberOfCardsOfType */
uint8_t CountNumberOfCardsOfType(uint8_t a)
{
	uint8_t input_type = a;
	uint8_t count = 0u;
	for (uint8_t index = 0u; index < DECK_SIZE; index++) {
		CardId card = card_id_read_at(card_id_index_address(wCurDeckCards_ADDR,
			index));
		if (card == 0u)
			break;
		uint8_t card_type = GetCardType(card);
		if ((input_type & FILTER_ENERGY) == FILTER_ENERGY) {
			if ((card_type & TYPE_ENERGY) != TYPE_ENERGY)
				continue;
		} else if (card_type != input_type) {
			continue;
		}
		count = (uint8_t)(count + 1u);
	}
	return count;
}
/* <<< factory CountNumberOfCardsOfType */
/* === factory CopyNBytesFromHLToDE */
/* >>> factory CopyNBytesFromHLToDE_Long */
CopyNBytesFromHLToDELongResult CopyNBytesFromHLToDE_Long(
	uint16_t *hl, uint16_t *de, uint16_t bc)
{
	uint16_t src = *hl;
	uint16_t dst = *de;
	uint32_t n = bc ? bc : 0x10000u;
	do {
		gb_write8(dst++, gb_read8(src++));
	} while (--n);
	*hl = src;
	*de = dst;
	return (CopyNBytesFromHLToDELongResult){0u, 0x80u, 0u, 0u, src, dst};
}
/* <<< factory CopyNBytesFromHLToDE_Long */
/* >>> factory IncrementDeckCardsInTempCollection */
void IncrementDeckCardsInTempCollection(uint16_t de)
{
	EnableSRAM();
	uint8_t remaining = DECK_SIZE;
	while (remaining != 0u) {
		uint8_t command = gb_read8(de++);
		for (uint8_t bit = 0u; bit < 8u && remaining != 0u; bit++) {
			CardId id = (CardId)gb_read8(de++);
			if ((command & 0x80u) != 0u)
				id = (CardId)(id | 0x0100u);
			command = (uint8_t)(command << 1);
			uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + id);
			gb_write8(slot, (uint8_t)(gb_read8(slot) + 1u));
			remaining = (uint8_t)(remaining - 1u);
			wDecompSavedDeckCount = remaining;
		}
	}
	DisableSRAM();
}
/* <<< factory IncrementDeckCardsInTempCollection */
/* >>> factory CreateCardCollectionListWithDeckCards */
void CreateCardCollectionListWithDeckCards(uint8_t a)
{
	gb_write8(hffb5_ADDR, a);
	uint16_t hl = sCardCollection_ADDR;
	uint16_t de = wTempCardCollection_ADDR;
	EnableSRAM();
	CopyNBytesFromHLToDE_Long(&hl, &de, (uint16_t)(CARD_COLLECTION_SIZE - 2u));
	DisableSRAM();
	uint8_t flags = gb_read8(hffb5_ADDR);
	if ((flags & (uint8_t)(1u << DECK_1_F)) != 0u)
		IncrementDeckCardsInTempCollection(sDeck1Cards_ADDR);
	if ((flags & (uint8_t)(1u << DECK_2_F)) != 0u)
		IncrementDeckCardsInTempCollection(sDeck2Cards_ADDR);
	if ((flags & (uint8_t)(1u << DECK_3_F)) != 0u)
		IncrementDeckCardsInTempCollection(sDeck3Cards_ADDR);
	if ((flags & (uint8_t)(1u << DECK_4_F)) != 0u)
		IncrementDeckCardsInTempCollection(sDeck4Cards_ADDR);
}
/* <<< factory CreateCardCollectionListWithDeckCards */
/* >>> factory GetSelectedVisibleCardID */
GetSelectedVisibleCardIDResult GetSelectedVisibleCardID(void)
{
	uint8_t cursor = wCardListCursorPos;
	uint8_t offset = (uint8_t)(cursor << 1);
	uint8_t f = (uint8_t)((offset == 0u ? 0x80u : 0u) |
		((cursor & 0x80u) != 0u ? 0x10u : 0u));
	uint16_t hl = (uint16_t)(wVisibleListCardIDs_ADDR + offset);
	uint8_t low = gb_read8(hl);
	uint8_t high = gb_read8((uint16_t)(hl + 1u));
	return (GetSelectedVisibleCardIDResult){
		(CardId)(((uint16_t)high << 8) | low), offset, f,
		(uint16_t)(hl + 1u)};
}
/* <<< factory GetSelectedVisibleCardID */
/* >>> factory CheckIfDeckHasCards */
uint8_t CheckIfDeckHasCards(uint16_t hl)
{
	hl = (uint16_t)(hl + DECK_NAME_SIZE);
	EnableSRAM();
	CardId id = card_id_read_at(hl);
	DisableSRAM();
	return id == 0u ? 0x90u : 0x00u;
}
/* <<< factory CheckIfDeckHasCards */
/* >>> factory FillBGMapLineWithA */
void FillBGMapLineWithA(uint8_t a, uint8_t b, uint8_t c)
{
	uint16_t de = BCCoordToBGMap0Address(b, c);
	FillDEWithA(a, 20u, de);
	hBankVRAM = 1u;
	gb_write8(0xFF4Fu, 1u);
	FillDEWithA(0x01u, 20u, de);
	hBankVRAM = 0u;
	gb_write8(0xFF4Fu, 0u);
}
/* <<< factory FillBGMapLineWithA */
/* >>> factory OpenDeckConfigurationMenu */
DeckBuildScreenResult OpenDeckConfigurationMenu(void)
{
	gb_write8(wYourOrOppPlayAreaCurPosition_ADDR, 0u);
	uint16_t de = wDeckConfigurationMenuTransitionTable_ADDR;
	uint16_t hl = wMenuInputTablePointer_ADDR;
	gb_write8(hl++, gb_read8(de++));
	gb_write8(hl, gb_read8(de));
	gb_write8(wDuelInitialPrizesUpperBitsSet_ADDR, 0xffu);
	return OpenDeckConfigurationMenu_SkipInit();
}

DeckBuildScreenResult OpenDeckConfigurationMenu_SkipInit(void)
{
	gb_write8(wCheckMenuCursorBlinkCounter_ADDR, 0u);
	uint16_t handler = (uint16_t)(gb_read8(wDeckConfigurationMenuHandlerFunction_ADDR)
	                              | (gb_read8((uint16_t)(wDeckConfigurationMenuHandlerFunction_ADDR + 1u)) << 8));
	switch (handler) {
	case DECK_CONFIGURATION_MENU_HANDLER:
		return HandleDeckConfigurationMenu();
	default:
		fprintf(stderr, "wDeckConfigurationMenuHandlerFunction is $%04X\n", (unsigned)handler);
		abort();
	}
}
/* <<< factory OpenDeckConfigurationMenu */
/* >>> factory GetCountOfCardInCurDeck */
GetCountOfCardInCurDeckResult GetCountOfCardInCurDeck(CardId id)
{
	uint8_t count = 0u;
	uint16_t cards = wCurDeckCards_ADDR;
	for (uint8_t i = 0u; i < DECK_SIZE; i++) {
		CardId card = card_id_read(&cards);
		if (card == 0u)
			break;
		if (card == id)
			count = (uint8_t)(count + 1u);
	}
	return (GetCountOfCardInCurDeckResult){count, 0x80u, (uint8_t)(id >> 8)};
}
/* <<< factory GetCountOfCardInCurDeck */
/* >>> factory IsCardInAnyDeck */
/* deck_configuration.asm:1133-1190 */
IsCardInAnyDeckResult IsCardInAnyDeck(uint8_t a, uint8_t f, CardId id)
{
	const uint16_t decks[] = {
		sDeck1Cards_ADDR,
		sDeck2Cards_ADDR,
		sDeck3Cards_ADDR,
		sDeck4Cards_ADDR,
	};
	uint8_t final_bits = 5u;
	for (uint8_t deck = 0u; deck < 4u; deck++) {
		EnableSRAM();
		uint16_t address = decks[deck];
		uint8_t remaining = DECK_SIZE;
		while (remaining != 0u) {
			uint8_t command = gb_read8(address++);
			uint8_t bits = 8u;
			while (bits != 0u) {
				uint8_t low = gb_read8(address++);
				CardId card = (CardId)low;
				if ((command & 0x80u) != 0u)
					card = (CardId)(card | 0x0100u);
				command = (uint8_t)(command << 1);
				if (card == id) {
					DisableSRAM();
					return (IsCardInAnyDeckResult){
						(a == 0u) ? 0x80u : 0x00u, remaining, bits
					};
				}
				remaining = (uint8_t)(remaining - 1u);
				if (remaining == 0u) {
					final_bits = bits;
					break;
				}
				bits = (uint8_t)(bits - 1u);
			}
		}
		DisableSRAM();
	}
	return (IsCardInAnyDeckResult){(f & 0x80u) | 0x10u, 0u, final_bits};
}
/* <<< factory IsCardInAnyDeck */
/* >>> factory GetOwnedCardCount */
GetOwnedCardCountResult GetOwnedCardCount(CardId id)
{
	uint16_t hl = wFilteredCardList_ADDR;
	uint8_t index = 0u;
	for (;;) {
		CardId card = card_id_read(&hl);
		if (card == 0u)
			return (GetOwnedCardCountResult){0u, (uint8_t)(id >> 8)};
		if (card == id) {
			uint8_t count = gb_read8((uint16_t)(wOwnedCardsCountList_ADDR + index));
			return (GetOwnedCardCountResult){count, (uint8_t)(id >> 8)};
		}
		index = (uint8_t)(index + 1u);
	}
}
/* <<< factory GetOwnedCardCount */
/* >>> factory RemoveCardFromDeck */
RemoveCardFromDeckResult RemoveCardFromDeck(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	CardId id = (CardId)(((uint16_t)d << 8) | e);
	GetCountOfCardInCurDeckResult r = GetCountOfCardInCurDeck(id);
	if (r.a == 0u)
		return (RemoveCardFromDeckResult){0u, 0x80u, b, c, d, e, hl};
	PlaySFX(SFX_CURSOR);
	uint16_t source = wCurDeckCards_ADDR;
	for (;;) {
		CardId card = card_id_read(&source);
		if (card == id)
			break;
	}
	uint16_t dst = (uint16_t)(source - 2u);
	for (;;) {
		CardId card = card_id_read(&source);
		if (card == 0u) {
			card_id_write(&dst, 0u);
			break;
		}
		card_id_write(&dst, card);
	}
	uint8_t filter = wCurCardTypeFilter;
	uint16_t faddr = (uint16_t)(wCardFilterCounts_ADDR + filter);
	gb_write8(faddr, (uint8_t)(gb_read8(faddr) - 1u));
	uint16_t bc = (uint16_t)(dst - 1u);
	return (RemoveCardFromDeckResult){
		0u, 0x10u, (uint8_t)(bc >> 8), (uint8_t)bc, d, e,
		(uint16_t)(source - 2u)
	};
}
/* <<< factory RemoveCardFromDeck */
/* >>> factory CheckIfCurrentDeckWasChanged */
CheckIfCurrentDeckWasChangedResult CheckIfCurrentDeckWasChanged(void)
{
	uint8_t total = wTotalCardCount;
	if (total != 0u && total != DECK_SIZE) {
		DisableSRAM();
		return (CheckIfCurrentDeckWasChangedResult){total, 0x10u};
	}
	uint16_t source = GetPointerToDeckCards();
	EnableSRAM();
	DecompressSRAMDeck(source, wCurDeckCardChanges_ADDR);
	DisableSRAM();
	gb_write8((uint16_t)(wCurDeckCardChanges_ADDR + DECK_SIZE * 2u), 0xFFu);
	gb_write8((uint16_t)(wCurDeckCardChanges_ADDR + DECK_SIZE * 2u + 1u),
		0xFFu);
	uint16_t current = wCurDeckCards_ADDR;
	for (;;) {
		CardId card = card_id_read(&current);
		if (card == 0u)
			break;
		uint16_t scan = wCurDeckCardChanges_ADDR;
		for (;;) {
			CardId value = card_id_read(&scan);
			if (value == 0xFFFFu)
				break;
			if (value == card) {
				uint16_t zero = (uint16_t)(scan - 2u);
				card_id_write(&zero, 0u);
				break;
			}
		}
	}
	uint16_t scan = wCurDeckCardChanges_ADDR;
	for (;;) {
		CardId value = card_id_read(&scan);
		if (value == 0xFFFFu)
			break;
		if (value != 0u) {
			DisableSRAM();
			return (CheckIfCurrentDeckWasChangedResult){
				(uint8_t)value, 0x10u
			};
		}
	}
	uint16_t name = GetPointerToDeckName();
	uint16_t current_name = wCurDeckName_ADDR;
	EnableSRAM();
	for (;;) {
		uint8_t left = gb_read8(current_name);
		uint8_t right = gb_read8(name);
		if (left != right) {
			DisableSRAM();
			return (CheckIfCurrentDeckWasChangedResult){left, 0x10u};
		}
		current_name = (uint16_t)(current_name + 1u);
		name = (uint16_t)(name + 1u);
		if (left == 0u)
			break;
	}
	DisableSRAM();
	return (CheckIfCurrentDeckWasChangedResult){0u, 0x80u};
}
/* <<< factory CheckIfCurrentDeckWasChanged */
/* >>> factory CreateFilteredCardList */
CreateFilteredCardListResult CreateFilteredCardList(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t filter = a;
	ClearMemory_Bank2(DECK_SIZE, wOwnedCardsCountList_ADDR);
	ClearMemory_Bank2((uint8_t)((MAX_NUM_CARDS_PER_TYPE + 1u) * 2u),
		wFilteredCardList_ADDR);
	uint8_t out_index = 0u;
	for (CardId id = 1u; id <= CARD_ID_MAX; id++) {
		CardPtrResult ptr = GetCardPointer(id);
		if (ptr.carry)
			break;
		uint8_t card_type = GetCardType(id);
		uint8_t add = 0u;
		if (filter == 0xFFu)
			add = 1u;
		else if ((filter & FILTER_ENERGY) == FILTER_ENERGY)
			add = (uint8_t)((card_type & TYPE_ENERGY) == TYPE_ENERGY);
		else
			add = (uint8_t)(card_type == filter);
		if (!add)
			continue;
		uint16_t list = (uint16_t)(wFilteredCardList_ADDR +
			(uint16_t)out_index * 2u);
		card_id_write(&list, id);
		uint8_t owned = gb_read8((uint16_t)(wTempCardCollection_ADDR + id));
		if (owned == CARD_NOT_OWNED)
			continue;
		if (owned == 0u) {
			IsCardInAnyDeckResult r = IsCardInAnyDeck(0u, 0x80u, id);
			if ((r.f & 0x10u) != 0u)
				continue;
		}
		gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + out_index), owned);
		out_index = (uint8_t)(out_index + 1u);
	}
	gb_write8(wNumEntriesInCurFilter_ADDR, out_index);
	uint16_t terminator = (uint16_t)(wFilteredCardList_ADDR +
		(uint16_t)out_index * 2u);
	gb_write8(terminator++, 0u);
	gb_write8(terminator, 0u);
	gb_write8((uint16_t)(wOwnedCardsCountList_ADDR + out_index), 0xFFu);
	return (CreateFilteredCardListResult){a, f, b, c, d, e, hl};
}
/* <<< factory CreateFilteredCardList */
/* >>> factory AddCardIDToVisibleList */
void AddCardIDToVisibleList(uint8_t b, CardId id)
{
	uint8_t num_entries = wNumVisibleCardListEntries;
	uint8_t offset = (uint8_t)(num_entries - b);
	uint16_t address = (uint16_t)(wVisibleListCardIDs_ADDR +
		(uint16_t)offset * 2u);
	card_id_write(&address, id);
}
/* <<< factory AddCardIDToVisibleList */
/* >>> factory HandleCardSelectionInput */
HandleCardSelectionInputResult HandleCardSelectionInput(void)
{
	gb_write8(wMenuInputSFX_ADDR, FALSE);
	uint8_t dpad = gb_read8(hDPadHeld_ADDR);
	if (dpad != 0u) {
		uint8_t num_positions = gb_read8(wCardListNumCursorPositions_ADDR);
		uint8_t pos = gb_read8(wCardListCursorPos_ADDR);
		uint8_t handled = 1u;
		if ((dpad & (1u << B_PAD_LEFT)) != 0u) {
			pos = (uint8_t)(pos - 1u);
			if ((pos & 0x80u) != 0u)
				pos = (uint8_t)(num_positions - 1u);
		} else if ((dpad & (1u << B_PAD_RIGHT)) != 0u) {
			pos = (uint8_t)(pos + 1u);
			if (pos >= num_positions)
				pos = 0u;
		} else {
			handled = 0u;
		}
		if (handled) {
			gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR);
			(void)DrawHorizontalListCursor_Invisible();
			gb_write8(wCardListCursorPos_ADDR, pos);
			gb_write8(wCheckMenuCursorBlinkCounter_ADDR, 0u);
		}
	}

	gb_write8(0xFFB3u, gb_read8(wCardListCursorPos_ADDR));
	uint8_t keys = gb_read8(hKeysPressed_ADDR);
	if ((keys & (PAD_A | PAD_B)) == 0u) {
		DrawHorizontalListCursorResult r = HandleCardSelectionCursorBlink();
		return (HandleCardSelectionInputResult){0u, 0u, r.b, r.c, 0};
	}
	if ((keys & PAD_A) != 0u) {
		ConfirmSelectionAndReturnCarryResult r = ConfirmSelectionAndReturnCarry();
		return (HandleCardSelectionInputResult){r.a, r.e, 0u, 0u, 1};
	}
	gb_write8(0xFFB3u, MENU_CANCEL);
	PlaySFXConfirmOrCancel(MENU_CANCEL);
	return (HandleCardSelectionInputResult){MENU_CANCEL, 0u, 0u, 0u, 1};
}
/* <<< factory HandleCardSelectionInput */
/* >>> part DispatchCardListUpdateFunction */
/* CallIndirect(wCardListUpdateFunction), deck_configuration.asm:1823-1824,
 * 1849-1850, 2483-2484, 2532-2533: the card-list input handlers fire the
 * redraw routine armed by whichever card-list screen is active. Every bank-2
 * address the asm stores into wCardListUpdateFunction is registered below;
 * DispatchIndirect no-ops on the cleared pointer and fails loud on any
 * nonzero target without a C body. */
static void DispatchCardListUpdateFunction(void)
{
	uint16_t target = (uint16_t)(gb_read8(wCardListUpdateFunction_ADDR)
	                            | (uint16_t)gb_read8((uint16_t)(wCardListUpdateFunction_ADDR + 1u)) << 8);

	switch (target) {
	case HANDLE_SELECT_PRINT_DECK_BUILDING_ADDR:
		PrintDeckBuildingCardList();
		return;
	case HANDLE_SELECT_UPDATE_CONFIRM_ADDR:
		UpdateConfirmationCardScreen();
		return;
		/* 02:642d PrintCardSelectionList, armed by deck_configuration.asm
		 * 3155-3158 and printer.asm:62-65. */
	case HANDLE_SELECT_PRINT_CARD_ADDR:
		PrintCardSelectionList();
		return;
		/* 02:66fa PrintCardSetListEntries, armed by card_album.asm:685-688. */
	case CARD_LIST_PRINT_CARD_SET_ADDR:
		(void)PrintCardSetListEntries();
		return;
		/* 02:6e9a HandleDeckMissingCardsList.CardListUpdateFunction,
		 * armed by deck_machine.asm:49-52. */
	case CARD_LIST_MISSING_CARDS_ADDR:
		HandleDeckMissingCardsList_CardListUpdateFunction();
		return;
		/* 02:73fe, armed by deck_machine.asm:1899-1902; the callee ignores
		 * its f input (see the port in deck_machine.c). */
	case CARD_LIST_UPDATE_MACHINE_ARROWS_ADDR:
		UpdateDeckMachineScrollArrowsAndEntries(0u);
		return;
		/* 02:7403, armed by deck_machine.asm:638-641. */
	case CARD_LIST_DRAW_MACHINE_SCREEN_ADDR:
		(void)DrawDeckMachineScreen();
		return;
	default:
		DispatchIndirect("wCardListUpdateFunction", target);
		return;
	}
}
/* <<< part DispatchCardListUpdateFunction */
/* --- factory AddGiftCenterDeckCardsToCollection */
/* >>> factory AppendOwnedCardCountNumber */
void AppendOwnedCardCountNumber(uint16_t hl, CardId id)
{
	uint16_t walk = hl;
	while (gb_read8(walk) != 0u)
		walk = (uint16_t)(walk + 1u);
	GetOwnedCardCountResult r1 = GetOwnedCardCount(id);
	ConvertToNumericalDigitsResult r2 = ConvertToNumericalDigits(r1.a, walk);
	gb_write8(r2.hl, 0u);
}
/* <<< factory AppendOwnedCardCountNumber */
/* >>> factory AppendOwnedCardCountAndStorageCountNumbers */
void AppendOwnedCardCountAndStorageCountNumbers(uint16_t hl, CardId id)
{
	uint16_t walk = hl;
	while (gb_read8(walk) != 0u)
		walk = (uint16_t)(walk + 1u);
	GetCountOfCardInCurDeckResult r1 = GetCountOfCardInCurDeck(id);
	ConvertToNumericalDigitsResult r2 = ConvertToNumericalDigits(r1.a, walk);
	walk = r2.hl;
	gb_write8(walk++, TX_SYMBOL);
	gb_write8(walk++, SYM_SLASH);
	GetOwnedCardCountResult r3 = GetOwnedCardCount(id);
	ConvertToNumericalDigitsResult r4 = ConvertToNumericalDigits(r3.a, walk);
	gb_write8(r4.hl, TX_END);
}
/* <<< factory AppendOwnedCardCountAndStorageCountNumbers */
/* >>> factory PrintCardSelectionList */
void PrintCardSelectionList(void)
{
	uint8_t e = wCardListCoords;
	uint8_t d = gb_read8((uint16_t)(wCardListCoords_ADDR + 1u));
	uint8_t tile;
	if (wCardListVisibleOffset != 0u) {
		tile = SYM_CURSOR_U;
	} else {
		tile = wCursorAlternateTile;
	}
	WriteByteToBGMap0(tile, 19u, e);

	uint8_t offset = wCardListVisibleOffset;
	uint8_t c = offset;
	uint16_t hl = (uint16_t)(wFilteredCardList_ADDR +
		(uint16_t)offset * 2u);
	uint8_t count = wNumVisibleCardListEntries;
	while (count != 0u) {
		CardId card_id = card_id_read(&hl);
		if (card_id != 0u) {
			uint8_t b = count;
			AddCardIDToVisibleList(b, card_id);
			LoadCardDataToBuffer1_FromCardID(card_id);
			CopyCardNameAndLevelResult name = CopyCardNameAndLevel(14u, b, c, d,
				(uint8_t)card_id);
			AppendOwnedCardCountNumber(name.hl, card_id);
			InitTextPrinting(d, e);
			uint16_t text = wDefaultText_ADDR;
			ProcessText(&text);
		} else {
			InitTextPrinting(d, e);
			uint16_t text = Text_9a36;
			ProcessText(&text);
		}
		--count;
		e = (uint8_t)(e + 2u);
	}
	if (card_id_read_at(hl) != 0u) {
		wUnableToScrollDown = FALSE;
		tile = SYM_CURSOR_D;
	} else {
		wUnableToScrollDown = TRUE;
		tile = wCursorAlternateTile;
	}
	WriteByteToBGMap0(tile, 19u, (uint8_t)(e - 2u));
}
/* <<< factory PrintCardSelectionList */
/* >>> factory PrintDeckBuildingCardList */
void PrintDeckBuildingCardList(void)
{
	uint8_t e = wCardListCoords;
	uint8_t d = gb_read8((uint16_t)(wCardListCoords_ADDR + 1u));
	uint8_t tile = (wCardListVisibleOffset != 0u) ? SYM_CURSOR_U : SYM_SPACE;
	WriteByteToBGMap0(tile, 19u, (uint8_t)(e - 1u));

	uint8_t offset = wCardListVisibleOffset;
	uint16_t hl = (uint16_t)(wFilteredCardList_ADDR +
		(uint16_t)offset * 2u);
	uint8_t count = wNumVisibleCardListEntries;
	while (count != 0u) {
		uint8_t b = count;
		CardId card_id = card_id_read(&hl);
		if (card_id != 0u) {
			AddCardIDToVisibleList(b, card_id);
			LoadCardDataToBuffer1_FromCardID(card_id);
			CopyCardNameAndLevelResult name = CopyCardNameAndLevel(13u, b, offset,
				d, (uint8_t)card_id);
			AppendOwnedCardCountAndStorageCountNumbers(name.hl, card_id);
			InitTextPrinting(d, e);
			uint16_t text = wDefaultText_ADDR;
			ProcessText(&text);
		} else {
			InitTextPrinting(d, e);
			uint16_t text = Text_9a30;
			ProcessText(&text);
		}
		count = (uint8_t)(count - 1u);
		e = (uint8_t)(e + 2u);
	}
	if (card_id_read_at(hl) != 0u) {
		wUnableToScrollDown = FALSE;
		tile = SYM_CURSOR_D;
	} else {
		wUnableToScrollDown = TRUE;
		tile = SYM_SPACE;
	}
	WriteByteToBGMap0(tile, 19u, (uint8_t)(e - 2u));
}
/* <<< factory PrintDeckBuildingCardList */
/* >>> factory PrintFilteredCardList */
PrintFilteredCardListResult PrintFilteredCardList(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_a = a;
	uint8_t saved_f = f;
	/* deck_configuration.asm:1469-1479 CardTypeFilters, verbatim: grass $01,
	 * fire $00, water $03, lightning $02, fighting $04, psychic $05,
	 * colorless $06, trainer $10, energy $20. */
	static const uint8_t card_type_filters[] = {0x01u, 0x00u, 0x03u, 0x02u, 0x04u,
	                                            0x05u, 0x06u, FILTER_TRAINER, FILTER_ENERGY};
	uint8_t filter = (a < 9u) ? card_type_filters[a] : 0xFFu;
	uint16_t src = sCardCollection_ADDR;
	uint16_t dst = wTempCardCollection_ADDR;
	EnableSRAM();
	CopyNBytesFromHLToDE_Long(&src, &dst, (uint16_t)(CARD_COLLECTION_SIZE - 2u));
	DisableSRAM();
	b = 0u;
	c = 0u;
	if (gb_read8(wIncludeCardsInDeck_ADDR) != 0u) {
		dst = GetPointerToDeckCards();
		IncrementDeckCardsInTempCollection(dst);
		b = (uint8_t)(wTempCardCollection_ADDR >> 8);
	}
	CreateFilteredCardListResult filtered = CreateFilteredCardList(filter, saved_f, b, c, (uint8_t)(dst >> 8), (uint8_t)dst, src);
	a = filtered.a;
	f = filtered.f;
	b = filtered.b;
	c = filtered.c;
	d = filtered.d;
	e = filtered.e;
	hl = filtered.hl;
	gb_write8(wNumVisibleCardListEntries_ADDR, NUM_FILTERED_LIST_VISIBLE_CARDS);
	e = 0x13u;
	d = 0x01u;
	gb_write8(wCardListCoords_ADDR, 0x07u);
	gb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x01u);
	hl = (uint16_t)(wFilteredCardList_ADDR + 0x0Du);
	PrintDeckBuildingCardList();
	return (PrintFilteredCardListResult){saved_a, saved_f, b, c, d, e, hl};
}
/* <<< factory PrintFilteredCardList */
/* --- factory Func_9ced */
/* >>> factory OpenCardPageFromCardList */
void OpenCardPageFromCardList(void)
{
restart:
	uint16_t list_ptr = (uint16_t)gb_read8(wCurCardListPtr_ADDR);
	list_ptr |= (uint16_t)((uint16_t)gb_read8((uint16_t)(wCurCardListPtr_ADDR + 1u)) << 8);
	uint8_t cursor = gb_read8(wCardListCursorPos_ADDR);
	uint8_t visible = gb_read8(wCardListVisibleOffset_ADDR);
	list_ptr = (uint16_t)(list_ptr +
		((uint16_t)cursor + visible) * 2u);
	CardId card_id = card_id_read_at(list_ptr);
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint16_t text_hl = SetupText(0x38u, 0x9Fu);
	OpenCardPage_FromCheckHandOrDiscardPile(0u, 0u, 0u, 0u, 0x38u, 0x9Fu, text_hl);

handle_input:
	uint8_t held = gb_read8(hDPadHeld_ADDR);
	uint8_t b = held;
	uint8_t offset;
	if ((held & (PAD_A | PAD_B | PAD_SELECT | PAD_START)) != 0u)
		goto exit;

	gb_write8(wMenuInputSFX_ADDR, FALSE);
	uint8_t count = gb_read8(wCardListNumCursorPositions_ADDR);
	cursor = gb_read8(wCardListCursorPos_ADDR);
	if ((b & (uint8_t)(1u << B_PAD_UP)) != 0u) {
		gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR);
		cursor = (uint8_t)(cursor - 1u);
		if ((cursor & 0x80u) == 0u)
			goto reopen_card_page;
		offset = gb_read8(wCardListVisibleOffset_ADDR);
		if (offset != 0u) {
			offset = (uint8_t)(offset - 1u);
			gb_write8(wCardListVisibleOffset_ADDR, offset);
			cursor = 0u;
			goto reopen_card_page;
		}
		goto handle_regular_card_page_input;
	}
	if ((b & (uint8_t)(1u << B_PAD_DOWN)) != 0u) {
		gb_write8(wMenuInputSFX_ADDR, SFX_CURSOR);
		cursor = (uint8_t)(cursor + 1u);
		if (cursor < count)
			goto reopen_card_page;
		uint16_t probe = (uint16_t)gb_read8(wCurCardListPtr_ADDR);
		probe |= (uint16_t)((uint16_t)gb_read8((uint16_t)(wCurCardListPtr_ADDR + 1u)) << 8);
		probe = (uint16_t)(probe +
			((uint16_t)gb_read8(wCardListCursorPos_ADDR) + offset) * 2u);
		if (card_id_read_at(probe) != 0u) {
			gb_write8(wCardListVisibleOffset_ADDR, offset);
			cursor = (uint8_t)(cursor - 1u);
			goto reopen_card_page;
		}
	}

handle_regular_card_page_input:
	{
		uint8_t saved = hBankROM;

		BankswitchROM(OpenCardPage__input_loop_BANK);
		OpenCardPage_input_loop(0u);
		BankswitchROM(saved);
	}
	goto handle_input;

reopen_card_page:
	gb_write8(wCardListCursorPos_ADDR, cursor);
	if (gb_read8(wMenuInputSFX_ADDR) == 0u)
		goto restart;
	PlaySFX(gb_read8(wMenuInputSFX_ADDR));
	goto restart;

exit:
	gb_write8(wVBlankOAMCopyToggle_ADDR, TRUE);
	cursor = gb_read8(wCardListCursorPos_ADDR);
	wTempCardListCursorPos = cursor;
}
/* <<< factory OpenCardPageFromCardList */
/* >>> factory CheckIfThereAreAnyBasicCardsInDeck */
CheckIfThereAreAnyBasicCardsInDeckResult CheckIfThereAreAnyBasicCardsInDeck(void)
{
	uint16_t hl = wCurDeckCards_ADDR;
	for (uint8_t i = 0u; i < DECK_SIZE; i++) {
		CardId card = card_id_read(&hl);
		if (card == 0u)
			return (CheckIfThereAreAnyBasicCardsInDeckResult){0u, 0x80u, 0u, hl};
		LoadCardDataToBuffer1_FromCardID(card);
		if ((wLoadedCard1Type & TYPE_ENERGY) != 0u)
			continue;
		if (wLoadedCard1Stage != 0u)
			continue;
		return (CheckIfThereAreAnyBasicCardsInDeckResult){
			0u, 0x90u, (uint8_t)card, hl
		};
	}
	return (CheckIfThereAreAnyBasicCardsInDeckResult){0u, 0x80u, 0u, hl};
}
/* <<< factory CheckIfThereAreAnyBasicCardsInDeck */
/* >>> factory SortCurDeckCardsByID */
SortCurDeckCardsByIDResult SortCurDeckCardsByID(void)
{
	uint16_t src = wCurDeckCards_ADDR;
	uint16_t dst = wOpponentDeck_ADDR;
	uint16_t list = wDuelTempList_ADDR;
	uint8_t index = 0u;
	for (uint8_t i = 0u; i < DECK_SIZE; i++) {
		CardId card = card_id_read(&src);
		card_id_write(&dst, card);
		if (card == 0u) {
			gb_write8(list, 0xFFu);
			break;
		}
		gb_write8(list++, index++);
	}
	uint8_t saved_turn = hWhoseTurn;
	hWhoseTurn = OPPONENT_TURN;
	(void)SortCardsInDuelTempListByID((uint8_t)(list >> 8),
		(uint8_t)list, dst);
	hWhoseTurn = saved_turn;
	uint16_t out = wCurDeckCards_ADDR;
	uint16_t order = wDuelTempList_ADDR;
	for (;;) {
		uint8_t entry = gb_read8(order++);
		if (entry == 0xFFu)
			break;
		uint16_t card = (uint16_t)(wOpponentDeck_ADDR + (uint16_t)entry * 2u);
		CardId id = card_id_read_at(card);
		card_id_write(&out, id);
	}
	gb_write8(out++, 0u);
	gb_write8(out, 0u);
	return (SortCurDeckCardsByIDResult){(uint8_t)(order - 1u)};
}
/* <<< factory SortCurDeckCardsByID */
/* >>> factory GetCardTypeIconPalette */
GetCardTypeIconPaletteResult GetCardTypeIconPalette(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t palette = 0xffu;
	f = 0x80u;
	if (a == 0xe0u) {
		palette = 2u;
		f = 0xc0u;
	} else if (a == 0xe4u) {
		palette = 3u;
		f = 0xc0u;
	} else if (a == 0xe8u) {
		palette = 2u;
		f = 0xc0u;
	} else if (a == 0xecu) {
		palette = 3u;
		f = 0xc0u;
	} else if (a == 0xf0u) {
		palette = 4u;
		f = 0xc0u;
	} else if (a == 0xf4u) {
		palette = 4u;
		f = 0xc0u;
	} else if (a == 0xf8u) {
		palette = 0u;
		f = 0xc0u;
	} else if (a == 0xfcu || a == 0xd0u || a == 0xd4u || a == 0xd8u || a == 0xdcu) {
		palette = (a == 0xd8u) ? 2u : 3u;
		f = 0xc0u;
	}
	return (GetCardTypeIconPaletteResult){palette, f, b, c, d, e, hl};
}
/* <<< factory GetCardTypeIconPalette */
/* >>> factory PrintConfirmationCardList */
void PrintConfirmationCardList(uint8_t a, uint8_t d, uint8_t e, uint16_t *hl)
{
	uint8_t row = wCardListCoords;
	uint8_t align = gb_read8((uint16_t)(wCardListCoords_ADDR + 1u));
	uint8_t tile = wCardListVisibleOffset ? SYM_CURSOR_U : SYM_SPACE;
	WriteByteToBGMap0(tile, 19u, (uint8_t)(row - 1u));
	uint8_t offset = wCardListVisibleOffset;
	uint16_t list = (uint16_t)(wUniqueDeckCardList_ADDR +
		(uint16_t)offset * 2u);
	uint8_t remaining = wNumVisibleCardListEntries;
	while (remaining != 0u) {
		uint8_t index = remaining;
		CardId card = card_id_read(&list);
		if (card == 0u)
			break;
		AddCardIDToVisibleList(index, card);
		LoadCardDataToBuffer1_FromCardID(card);
		CopyCardNameAndLevelResult name = CopyCardNameAndLevel(13u, index, align,
			row, (uint8_t)card);
		uint16_t text = name.hl;
		while (gb_read8(text) != 0u)
			text++;
		GetCountOfCardInCurDeckResult count = GetCountOfCardInCurDeck(card);
		gb_write8(text++, TX_SYMBOL);
		gb_write8(text++, SYM_CROSS);
		ConvertToNumericalDigitsResult digits = ConvertToNumericalDigits(count.a, text);
		gb_write8(digits.hl, TX_END);
		uint8_t icon;
		if (wLoadedCard1Type < TYPE_ENERGY)
			icon = (uint8_t)(ICON_TILE_BASIC_POKEMON + (uint8_t)(wLoadedCard1Stage * 4u));
		else if (wLoadedCard1Type < TYPE_TRAINER)
			icon = (uint8_t)(ICON_TILE_FIRE +
				(uint8_t)((wLoadedCard1Type - TYPE_ENERGY) * 4u));
		else
			icon = ICON_TILE_TRAINER;
		uint16_t de = (uint16_t)((uint16_t)(align - 2u) << 8 |
			(uint8_t)(row - 1u));
		FillRectangle(icon, 2u, 2u, de, 0x0102u);
		GetCardTypeIconPaletteResult palette =
			GetCardTypeIconPalette(icon, 0u, 0u, 0u, 0u, 0u, de);
		hBankVRAM = 1u;
		gb_write8(0xFF4Fu, 1u);
		FillRectangle(palette.a, 2u, 2u, de, 0x0000u);
		hBankVRAM = 0u;
		gb_write8(0xFF4Fu, 0u);
		InitTextPrinting(align, row);
		uint16_t text_ptr = wDefaultText_ADDR;
		ProcessText(&text_ptr);
		remaining = (uint8_t)(index - 1u);
		row = (uint8_t)(row + 2u);
	}
	if (card_id_read_at(list) == 0u) {
		wUnableToScrollDown = 1u;
		tile = SYM_SPACE;
	} else {
		wUnableToScrollDown = 0u;
		tile = SYM_CURSOR_D;
	}
	WriteByteToBGMap0(tile, 19u, (uint8_t)(row - 2u));
	(void)a; (void)d; (void)e; (void)hl;
}
/* <<< factory PrintConfirmationCardList */
/* >>> factory CreateCurDeckUniqueCardList */
CreateCurDeckUniqueCardListResult CreateCurDeckUniqueCardList(void)
{
	uint8_t count = 0u;
	CardId previous = 0u;
	uint16_t hl = wCurDeckCards_ADDR;
	uint16_t de = wUniqueDeckCardList_ADDR;
	for (;;) {
		CardId card = card_id_read(&hl);
		if (card == previous)
			continue;
		previous = card;
		card_id_write(&de, card);
		if (card == 0u)
			break;
		count = (uint8_t)(count + 1u);
	}
	wNumUniqueCards = count;
	return (CreateCurDeckUniqueCardListResult){
		0u, 0x80u, 0u, 0u, (uint8_t)(de >> 8), (uint8_t)de, hl
	};
}
/* <<< factory CreateCurDeckUniqueCardList */
/* >>> factory TryAddCardToDeck */
TryAddCardToDeckResult TryAddCardToDeck(CardId id)
{
	uint8_t max_cards = wMaxNumCardsAllowed;
	if (wTotalCardCount == max_cards)
		return (TryAddCardToDeckResult){wTotalCardCount, 0x90u};
	LoadCardDataToBuffer1_FromCardID(id);
	if (wLoadedCard1Type != TYPE_ENERGY_DOUBLE_COLORLESS &&
		(wLoadedCard1Type & TYPE_ENERGY) != TYPE_ENERGY) {
		uint16_t name = (uint16_t)(wLoadedCard1Name |
			(uint16_t)wLoadedCard1Name_PTR[1] << 8);
		uint8_t same = 0u;
		uint16_t cards = wCurDeckCards_ADDR;
		for (;;) {
			CardId card = card_id_read(&cards);
			if (card == 0u)
				break;
			if (GetCardName(card) == name) {
				same = (uint8_t)(same + 1u);
				if (same == wSameNameCardsLimit)
					return (TryAddCardToDeckResult){0u, 0x10u};
			}
		}
	}
	GetCountOfCardInCurDeckResult count = GetCountOfCardInCurDeck(id);
	uint16_t owned_address = (uint16_t)(wOwnedCardsCountList_ADDR +
		wCardListVisibleOffset + wCardListCursorPos);
	uint8_t owned = gb_read8(owned_address);
	if (count.a == owned)
		return (TryAddCardToDeckResult){count.a, 0x90u};
	PlaySFX(SFX_CURSOR);
	uint16_t slot = wCurDeckCards_ADDR;
	for (uint8_t i = 0u; i < DECK_SIZE; i++) {
		if (card_id_read_at(slot) == 0u)
			break;
		slot = (uint16_t)(slot + 2u);
	}
	card_id_write(&slot, id);
	card_id_write(&slot, 0u);
	uint8_t filter = wCurCardTypeFilter;
	uint16_t filter_address = (uint16_t)(wCardFilterCounts_ADDR + filter);
	gb_write8(filter_address, (uint8_t)(gb_read8(filter_address) + 1u));
	return (TryAddCardToDeckResult){0u, 0u};
}
/* <<< factory TryAddCardToDeck */
/* >>> factory AddCardToDeckAndUpdateCount */
AddCardToDeckAndUpdateCountResult AddCardToDeckAndUpdateCount(CardId id)
{
	TryAddCardToDeckResult r = TryAddCardToDeck(id);
	if (r.f & 0x10u)
		return (AddCardToDeckAndUpdateCountResult){r.a, r.f, (uint8_t)id};
	PrintCardTypeCounts();
	PrintTotalCardCount(15u, 0u);
	GetCountOfCardInCurDeckResult r2 = GetCountOfCardInCurDeck(id);
	PrintNumberValueInCursorYPos(r2.a);
	return (AddCardToDeckAndUpdateCountResult){r2.a, r2.f, (uint8_t)id};
}
/* <<< factory AddCardToDeckAndUpdateCount */
/* >>> factory HandleDeckCardSelectionList */
HandleDeckCardSelectionListResult HandleDeckCardSelectionList(void)
{
	wMenuInputSFX = FALSE;
	uint8_t dpad = hDPadHeld;
	uint8_t cursor = wCardListCursorPos;
	uint8_t a = cursor;
	HandleDeckCardSelectionListResult out = {0u, 0u, 0u, 0u, 0u, 0u, 0u};
	if (dpad != 0u) {
		uint8_t count = wCardListNumCursorPositions;
		if ((dpad & (1u << B_PAD_UP)) != 0u) {
			wMenuInputSFX = SFX_CURSOR; a = (uint8_t)(cursor - 1u);
			if ((a & 0x80u) != 0u) {
				if (wCardListVisibleOffset == 0u) { wMenuInputSFX = FALSE; }
				else { --wCardListVisibleOffset; DispatchCardListUpdateFunction(); }
				a = 0u;
			}
			(void)DrawListCursor_Invisible(); wCardListCursorPos = a; wCheckMenuCursorBlinkCounter = 0u;
		} else if ((dpad & (1u << B_PAD_DOWN)) != 0u) {
			wMenuInputSFX = SFX_CURSOR; a = (uint8_t)(cursor + 1u);
			if (a >= count) { if (wUnableToScrollDown == 0u) { ++wCardListVisibleOffset; DispatchCardListUpdateFunction(); --a; } else { --a; wMenuInputSFX = FALSE; } }
			(void)DrawListCursor_Invisible(); wCardListCursorPos = a; wCheckMenuCursorBlinkCounter = 0u;
		} else if (wced2 != 0u) {
			if ((dpad & (1u << B_PAD_LEFT)) != 0u) {
				GetSelectedVisibleCardIDResult selected =
					GetSelectedVisibleCardID();
				RemoveCardFromDeckAndUpdateCount(out.b, out.c,
					(uint8_t)(selected.id >> 8), (uint8_t)selected.id, out.hl);
			} else if ((dpad & (1u << B_PAD_RIGHT)) != 0u) {
				GetSelectedVisibleCardIDResult selected =
					GetSelectedVisibleCardID();
				AddCardToDeckAndUpdateCount(selected.id);
			}
		}
	}
	hffb3 = wCardListCursorPos;
	if (wCardListHandlerFunction != 0u) {
		DrawListCursor_Visible(); PlaySFXConfirmOrCancel(MENU_CONFIRM); out.a = MENU_CONFIRM; out.f = 0x10u; out.e = wCardListCursorPos; return out;
	}
	uint8_t keys = hKeysPressed;
	if ((keys & (PAD_A | PAD_B)) != 0u) {
		if ((keys & PAD_A) != 0u) { DrawListCursor_Visible(); PlaySFXConfirmOrCancel(MENU_CONFIRM); out.a = MENU_CONFIRM; out.f = 0x10u; out.e = wCardListCursorPos; return out; }
		hffb3 = MENU_CANCEL; PlaySFXConfirmOrCancel(MENU_CANCEL); out.a = MENU_CANCEL; out.f = 0x10u; return out;
	}
	if (wMenuInputSFX != 0u) PlaySFX(wMenuInputSFX);
	/* deck_configuration.asm:1927-1935: the period test reads the counter
	 * before the increment, the phase bit after it. */
	uint8_t before = wCheckMenuCursorBlinkCounter;
	uint8_t counter = (uint8_t)(before + 1u); wCheckMenuCursorBlinkCounter = counter;
	if ((before & CURSOR_BLINK_PERIOD_MASK) == 0u) { if ((counter & (1u << B_CURSOR_BLINK_PERIOD)) == 0u) DrawListCursor(wVisibleCursorTile); else DrawListCursor_Invisible(); }
	return out;
}
/* <<< factory HandleDeckCardSelectionList */
/* >>> factory DismantleDeck */
/* deck_configuration.asm:684-716 */
DismantleDeckResult DismantleDeck(uint16_t w0)
{
	/* Entered through JumpToFunctionInTable, so the word at sp is the return
	 * address back into HandleDeckConfigurationMenu; the `add sp, $2` on the
	 * .Dismantle exit discards it to return one frame further out and never
	 * reads it. Only `a` is modelled: that exit leaves the flags produced by
	 * `add sp, $2`, which depend on the runtime sp. */
	(void)w0;

	HandleYesOrNoMenuResult confirm = YesOrNoMenuWithText(DismantleThisDeckText);
	if ((confirm.f & 0x10u) != 0u) {
		/* jr c, SaveDeckConfiguration.go_back */
		DrawCardTypeIconsAndPrintCardCounts();
		PrintDeckBuildingCardList();
		uint8_t back = wced6;
		wCardListCursorPos = back;
		return (DismantleDeckResult){back, 0u};
	}

	if ((CheckIfHasOtherValidDecks() & 0x10u) != 0u) {
		/* carry: this is the only deck with cards, so it cannot be dismantled */
		(void)DrawWideTextBox_WaitForInput(ThereIsOnly1DeckSoCannotBeDismantledText);
		EmptyScreen();
		uint16_t params = FILTERS_CARD_SELECTION_PARAMS_ADDR;
		(void)InitCardSelectionParams(0u, &params);
		/* wTempCardTypeFilter and wCardListCursorPos are the same byte ($CEA4);
		 * the filter store happens first, exactly as in the asm. */
		wTempCardTypeFilter = wCurCardTypeFilter;
		(void)DrawHorizontalListCursor_Visible();
		PrintDeckBuildingCardList();
		EnableLCD();
		uint8_t cursor = wced6;
		wCardListCursorPos = cursor;
		return (DismantleDeckResult){cursor, 0u};
	}

	/* .Dismantle */
	EnableSRAM();
	uint16_t name = GetPointerToDeckName();
	uint8_t a = gb_read8(name);
	if (a != 0u) {
		ClearMemory_Bank2(NAME_BUFFER_LENGTH, name);
		uint16_t cards = GetPointerToDeckCards();
		(void)AddDeckToCollection(cards);
		a = DECK_COMPRESSED_SIZE;
		ClearMemory_Bank2(DECK_COMPRESSED_SIZE, cards);
	}
	DisableSRAM();
	return (DismantleDeckResult){a, 1u};
}
/* <<< factory DismantleDeck */
/* --- factory HandleSendDeckConfigurationMenu */
/* --- factory PrepareToBuildDeckConfigurationToSend */
/* === factory CheckIfHasOtherValidDecks */
/* === factory DrawCardTypeIcons */
/* === factory HandleCardSelectionCursorBlink */
/* === factory PrintTotalNumberOfCardsInCollection */
