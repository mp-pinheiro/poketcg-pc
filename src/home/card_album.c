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
#define SYM_BOX_BTM_R 0x1Du
#define SYM_CURSOR_U 0x0Cu
#define SYM_CURSOR_D 0x2Fu

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
PrintCardSetListEntriesResult PrintCardSetListEntries(void)
{
	uint16_t hl = wCardListCoords_ADDR;
	uint8_t e = gb_read8(hl++);
	uint8_t d = gb_read8(hl);
	uint8_t visible_offset = wCardListVisibleOffset;
	uint8_t tile = visible_offset ? SYM_CURSOR_U : SYM_BOX_TOP_R;
	WriteByteToBGMap0(tile, d, (uint8_t)(e - 2u));
	hl = visible_offset;
	uint8_t count = wNumVisibleCardListEntries;
	while (count != 0u) {
		uint8_t card = gb_read8((uint16_t)(wFilteredCardList_ADDR + hl));
		hl = (uint16_t)(hl + 1u);
		if (card == 0u) break;
		--count;
	}
	hl = (uint16_t)(wFilteredCardList_ADDR + hl);
	if (gb_read8(hl) == 0u) {
		gb_write8(wUnableToScrollDown_ADDR, TRUE);
		tile = SYM_BOX_BTM_R;
	} else {
		gb_write8(wUnableToScrollDown_ADDR, FALSE);
		tile = SYM_CURSOR_D;
	}
	WriteByteToBGMap0(tile, 19u, 17u);
	return (PrintCardSetListEntriesResult){ .hl = hl };
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
