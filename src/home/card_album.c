#include "home/card_album.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define CARD_NOT_OWNED 0x80u

#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/card_data.h"
#include "home/deck_configuration.h"
#include "home/menus.h"
#include "home/process_text.h"
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define FALSE 0x00u
#define MEW_LV15 0xA1u
#define TRUE 0x01u
#define TX_SYMBOL 0x05u
#define VENUSAUR_LV64 0x0Au
#define SYM_BOX_TOP_R 0x19u
#define SYM_BOX_BTM_R 0x1Bu
#define SYM_CURSOR_U 0x0Cu
#define SYM_CURSOR_D 0x2Fu
#define SYM_0 0x20u
#define SYM_SPACE 0x00u
#define TX_END 0x00u

#include "home/deck_configuration.h"
#include "home/card_data.h"
#include "mem.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/deck_configuration.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/sound.h"
#include "mem.h"
/* hardware.inc:88-106 -- this game uses the swapped-nybble combined input byte,
 * so the Control Pad lives in the HIGH nybble and PAD_BUTTONS is $0F, not $F0. */
#define PAD_A       0x01u
#define PAD_START   0x08u
#define PAD_RIGHT   0x10u
#define PAD_LEFT    0x20u
#define PAD_UP      0x40u
#define PAD_DOWN    0x80u
#define PAD_BUTTONS 0x0Fu
#define SFX_CURSOR  0x01u

#include "home/deck_configuration.h"
#include "home/card_album.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#include "generated/sram.h"
#define CARD_COLLECTION_SIZE 0x100u
#define CARD_SET_EVOLUTION 0x01u
#define CARD_SET_LABORATORY 0x03u
#define CARD_SET_MYSTERY 0x02u
#define CARD_SET_PROMOTIONAL 0x04u
#define NUM_CARD_ALBUM_VISIBLE_CARDS 0x07u

#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
/* <<< factory statics */

/* >>> factory GetFirstOwnedCardIndex */
/* card_album.asm:612-624. Scans wOwnedCardsCountList for the first entry
 * that is not CARD_NOT_OWNED; no bound check, so it relies on the caller
 * guaranteeing at least one owned entry (card_album.asm:660-662,717-719).
 * hl exits one past the byte that ended the scan (post-increment ld a,[hli]
 * on every iteration, including the last). */
GetFirstOwnedCardIndexResult GetFirstOwnedCardIndex(void)
{
	uint16_t hl = wOwnedCardsCountList_ADDR;
	uint8_t index = 0;

	for (;;) {
		uint8_t card = gb_read8(hl++);
		if (card != CARD_NOT_OWNED)
			break;
		index++;
	}
	gb_write8(wFirstOwnedCardIndex_ADDR, index);
	return (GetFirstOwnedCardIndexResult){ .a = index, .b = index, .hl = hl };
}
/* <<< factory GetFirstOwnedCardIndex */

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
	uint8_t card = gb_read8((uint16_t)(wFilteredCardList_ADDR + index - 1u));
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
	uint8_t visible_offset = wCardListVisibleOffset;
	(void)WriteByteToBGMap0(visible_offset != 0u ? SYM_CURSOR_U : SYM_BOX_TOP_R, 19u, (uint8_t)(y - 2u));
	uint16_t index = visible_offset;
	uint8_t b = wNumVisibleCardListEntries;
	uint8_t tile;
	for (;;) {
		if (b == 0u) {
			uint16_t hl = (uint16_t)(wFilteredCardList_ADDR + index);
			if (gb_read8(hl) == 0u) {
				wUnableToScrollDown = TRUE;
				tile = SYM_BOX_BTM_R;
			} else {
				wUnableToScrollDown = FALSE;
				tile = SYM_CURSOR_D;
			}
			(void)WriteByteToBGMap0(tile, 19u, 17u);
			return (PrintCardSetListEntriesResult){ .hl = hl };
		}
		uint8_t card = gb_read8((uint16_t)(wFilteredCardList_ADDR + index));
		index = (uint16_t)((index & 0xff00u) | ((index + 1u) & 0xffu));
		if (card == 0u) {
			wUnableToScrollDown = TRUE;
			(void)WriteByteToBGMap0(SYM_BOX_BTM_R, 19u, 17u);
			return (PrintCardSetListEntriesResult){ .hl = index };
		}
		AddCardIDToVisibleList(b, card);
		LoadCardDataToBuffer1_FromCardID(card);
		if (gb_read8((uint16_t)(wOwnedCardsCountList_ADDR + index - 1u)) == CARD_NOT_OWNED) {
			uint16_t de = wDefaultText_ADDR;
			for (uint8_t i = 0; i < CARD_ALBUM_EMPTY_SLOT_DASHES; i++)
				gb_write8(de++, CARD_ALBUM_EMPTY_SLOT_DASH);
			gb_write8(de, TX_END);
		} else {
			(void)CopyCardNameAndLevel(13u, b, (uint8_t)index, x, card);
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
	uint8_t l = 0;

	ClearMemory_Bank2(0x3cu, 0xCEDAu);
	ClearMemory_Bank2(0x3cu, 0xCF68u);
	gb_write8(0xCFE2u, 0);

	for (uint16_t card_id = 1; card_id <= 0xE4u; ++card_id) {
		uint8_t e = (uint8_t)card_id;
		LoadCardDataToBuffer1_FromCardID(e);
		if (((gb_read8(0xCC2Au) & 0xF0u) >> 4) != set)
			continue;

		if (e == 0x0Au || e == 0xA1u) {
			uint8_t bit = (e == 0x0Au) ? 0x01u : 0x02u;
			if (gb_read8(0xC000u + e) != 0x80u) {
				uint8_t flags = gb_read8(0xCFE2u);
				gb_write8(0xCFE2u, (uint8_t)(flags | bit));
			}
			continue;
		}

		gb_write8(0xCEDAu + l, e);
		gb_write8(0xCF68u + l, gb_read8(0xC000u + e));
		++l;
	}

	if (set == 0u) {
		for (uint8_t e = 1; e < 7u; ++e) {
			gb_write8(0xCEDAu + l, e);
			gb_write8(0xCF68u + l, gb_read8(0xC000u + e));
			++l;
		}
	} else if (set == 0x02u) {
		uint8_t e = 7u;
		gb_write8(0xCEDAu + l, e);
		gb_write8(0xCF68u + l, gb_read8(0xC000u + e));
		++l;
	}

	uint8_t flags = gb_read8(0xCFE2u);
	if (flags & 0x01u) {
		gb_write8(0xCEDAu + l, 0x0Au);
		gb_write8(0xCF68u + l, 1u);
		++l;
	}
	if (flags & 0x02u) {
		gb_write8(0xCEDAu + l, 0xA1u);
		gb_write8(0xCF68u + l, 1u);
		++l;
	}

	uint8_t c = (uint8_t)(l - 1u);
	while (gb_read8(0xCF68u + c) == 0x80u)
		--c;
	++c;
	gb_write8(0xCEAEu, c);
	gb_write8(0xCEDAu + c, 0);
	gb_write8(0xCF68u + c, 0xFFu);
}
/* <<< factory CreateCardSetList */

/* >>> factory HandleCardAlbumCardPage */
/* card_album.asm:476-604. Card Album card-page viewer. Opens the card page
 * for the list entry under the cursor when that entry is owned, then loops on
 * the D-pad: PAD_UP/PAD_DOWN scroll the list and jump back to the top of the
 * routine, PAD_LEFT/PAD_RIGHT edit the deck when wced2 is set, and any of
 * PAD_BUTTONS ($0F in this game's swapped-nybble pad byte) exits.
 *
 * `jp HandleCardAlbumCardPage` is a tail jump, not a call, so the restart is
 * the enclosing for(;;) and the frame never grows.
 *
 * `bank1call OpenCardPage.input_loop` re-enters OpenCardPage past its scene
 * setup. That label has no exported C symbol, so core.asm:3512-3529 is inlined
 * below; it reloads b from hDPadHeld before any use, so the incoming b is dead.
 *
 * The `call TryAddCardToDeck` path falls through into `.open_card_page_pop_af_2`
 * with no matching `push af`, so the real ROM pops its own return address into
 * af there. Both halves are overwritten before their next read, so the C body
 * just drops the word; the GB-side stack damage has no C analogue.
 *
 * One exit only. `and PAD_BUTTONS` / `jp nz` leaves Z=0 N=0 H=1 C=0 and nothing
 * after it touches flags, so f is always $20 and a is always the byte reloaded
 * from wCardListCursorPos. */
HandleCardAlbumCardPageResult HandleCardAlbumCardPage(uint8_t d, uint8_t e)
{
	uint8_t a = 0u;
	uint8_t b = 0u;
	uint8_t c = 0u;
	uint8_t saved_a = 0u;
	uint16_t hl = 0u;

	for (;;) {
		b = wCardListCursorPos;
		c = (uint8_t)(wCardListVisibleOffset + b);
		b = 0u;
		hl = (uint16_t)(wOwnedCardsCountList_ADDR + c);
		if (gb_read8(hl) != CARD_NOT_OWNED) {
			hl = (uint16_t)(gb_read8(wCurCardListPtr_ADDR) |
					((uint16_t)gb_read8((uint16_t)(wCurCardListPtr_ADDR + 1u)) << 8));
			hl = (uint16_t)(hl + c);
			e = gb_read8(hl);
			d = 0u;
			/* push de: the pair below is what the matching pop restores,
			 * so the $38/$9f handed to SetupText and the card page is a
			 * separate de that never reaches the input handler. */
			LoadCardDataToBuffer1_FromCardID(e);
			hl = SetupText(0x38u, 0x9Fu);
			OpenCardPage_FromCheckHandOrDiscardPile(0u, 0u, 0u, 0u, 0x38u, 0x9Fu, hl);
		}

	handle_input:
		b = hDPadHeld;
		if ((uint8_t)(b & PAD_BUTTONS) != 0u)
			break;
		wMenuInputSFX = FALSE;
		c = wCardListNumCursorPositions;
		a = wCardListCursorPos;

		if ((b & PAD_UP) != 0u) {
			saved_a = a;
			wMenuInputSFX = SFX_CURSOR;
			a = (uint8_t)(wCardListCursorPos + wCardListVisibleOffset);
			if (a == wFirstOwnedCardIndex) {
				a = saved_a;
				goto open_card_page;
			}
			a = (uint8_t)(saved_a - 1u);
			if ((a & 0x80u) == 0u)
				goto got_new_pos;
			a = wCardListVisibleOffset;
			if (a == 0u)
				goto open_card_page;
			wCardListVisibleOffset = (uint8_t)(a - 1u);
			a = 0u;
			goto got_new_pos;
		}

		if ((b & PAD_DOWN) != 0u) {
			wMenuInputSFX = SFX_CURSOR;
			a = (uint8_t)(a + 1u);
			if (a < c)
				goto got_new_pos;
			saved_a = a;
			hl = (uint16_t)(gb_read8(wCurCardListPtr_ADDR) |
					((uint16_t)gb_read8((uint16_t)(wCurCardListPtr_ADDR + 1u)) << 8));
			c = wCardListCursorPos;
			b = 0u;
			hl = (uint16_t)(hl + c);
			c = (uint8_t)(wCardListVisibleOffset + 1u);
			b = 0u;
			hl = (uint16_t)(hl + c);
			if (gb_read8(hl) == 0u) {
				a = saved_a;
				goto open_card_page;
			}
			wCardListVisibleOffset = (uint8_t)(wCardListVisibleOffset + 1u);
			a = (uint8_t)(saved_a - 1u);
			goto got_new_pos;
		}

		a = wced2;
		if (a == 0u)
			goto open_card_page;
		if ((b & PAD_LEFT) != 0u) {
			RemoveCardFromDeckResult removed =
				RemoveCardFromDeck(b, c, d, e, hl);
			/* Only de outlives the call: .open_card_page pushes and pops
			 * it, while a, b, c and hl are rewritten before their next
			 * read at .handle_input and in the inlined input loop. */
			d = removed.d;
			e = removed.e;
			goto open_card_page;
		}
		if ((b & PAD_RIGHT) == 0u)
			goto open_card_page;
		(void)TryAddCardToDeck(e);
		goto open_card_page;

	got_new_pos:
		wCardListCursorPos = a;
		a = wMenuInputSFX;
		if (a != 0u)
			PlaySFX(a);
		continue;

	open_card_page:
		for (;;) {
			DoFrame();
			b = hDPadHeld;
			if ((uint8_t)(wCardPageExitKeys & b) != 0u)
				break;
			a = (uint8_t)(hKeysPressed & (PAD_START | PAD_A));
			if (a != 0u) {
				CardPageNavigationResult page =
					DisplayFirstOrNextCardPage(b);
				if ((page.f & 0x10u) != 0u)
					break;
				EnableLCD();
				continue;
			}
			a = (uint8_t)(hKeysPressed & (PAD_RIGHT | PAD_LEFT));
			if (a != 0u)
				DisplayCardPageOnLeftOrRightPressed(a);
		}
		goto handle_input;
	}

	wVBlankOAMCopyToggle = TRUE;
	a = wCardListCursorPos;
	wTempCardListCursorPos = a;
	return (HandleCardAlbumCardPageResult){ .a = a, .f = 0x20u };
}
/* <<< factory HandleCardAlbumCardPage */

/* >>> factory CreateCardSetListAndInitListCoords */
void CreateCardSetListAndInitListCoords(uint8_t a)
{
	uint16_t hl = sCardCollection_ADDR;
	uint16_t de = wTempCardCollection_ADDR;
	EnableSRAM();
	CopyNBytesFromHLToDE(&hl, &de, (uint8_t)(CARD_COLLECTION_SIZE - 1u));
	DisableSRAM();

	uint8_t prefix = 0x30u;
	if (a == CARD_SET_EVOLUTION)
		prefix = 0x31u;
	else if (a == CARD_SET_MYSTERY)
		prefix = 0x32u;
	else if (a == CARD_SET_LABORATORY)
		prefix = 0x33u;
	else if (a == CARD_SET_PROMOTIONAL)
		prefix = 0x3Fu;
	gb_write8(wCurDeckName_ADDR, 0x03u);
	gb_write8((uint16_t)(wCurDeckName_ADDR + 1u), prefix);

	CreateCardSetList(a);
	wNumVisibleCardListEntries = NUM_CARD_ALBUM_VISIBLE_CARDS;
	gb_write8(wCardListCoords_ADDR, 0x04u);
	gb_write8((uint16_t)(wCardListCoords_ADDR + 1u), 0x02u);
}
/* <<< factory CreateCardSetListAndInitListCoords */

#include "home/credits_sequence_commands.h"
#include "home/deck_check.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "home/empty_screen.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/objects.h"
#include "home/print_text.h"
#include "home/switch_sram.h"
#include "home/text_box.h"
#include "home/tiles.h"
/* card_album.asm:685-688 parks PrintCardSetListEntries (02:66fa) in
 * wCardListUpdateFunction; deck_configuration.c's CallIndirect registry
 * dispatches it. */
#define PRINT_CARD_SET_LIST_ENTRIES 0x66FAu
/* >>> factory CardAlbum */
#define CARD_ALBUM_BOOSTER_PACK_MENU_PARAMS 0x6A02u
#define CARD_ALBUM_BOOSTER_PACK_CARDS_MENU_PARAMS 0x6A0Au
#define CARD_ALBUM_BOOSTER_PACKS_MENU_DATA 0x6B62u
#define MENU_CANCEL 0xFFu
#define MENU_CONFIRM 0x01u
#define PAD_B 0x02u
#define PAD_START 0x08u
#define NUM_CARD_SETS 0x05u
#define NUM_CARDS_COLOSSEUM 0x38u
#define NUM_CARDS_EVOLUTION 0x32u
#define NUM_CARDS_MYSTERY 0x33u
#define NUM_CARDS_LABORATORY 0x33u
#define NUM_CARDS_PROMOTIONAL 0x14u
#define VENUSAUR_OWNED_PHANTOM_F 0x00u
#define MEW_OWNED_PHANTOM_F 0x01u
#define SYM_SLASH 0x2Eu
#define BoosterPackTitleText 0x0252u
#define Item1ColosseumText 0x0253u
#define Item2EvolutionText 0x0254u
#define Item3MysteryText 0x0255u
#define Item4LaboratoryText 0x0256u
#define Item5PromotionalCardText 0x0257u
#define ViewWhichCardFileText 0x0258u
#define EmptyPromotionalCardText 0x0259u

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
			(void)InitCardSelectionParams(0u, &list_params);
			wCardListNumCursorPositions = wTempCardListNumCursorPositions;
			wCardListCursorPos = wTempCardListCursorPos;
		}
		cursor = hCurMenuItem;
	}
}
/* <<< factory CardAlbum */
