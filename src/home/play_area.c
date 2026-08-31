#include "home/play_area.h"

#include "generated/wram.h"
#include "home/objects.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"
#include "home/random.h"
#include "home/sound.h"
#include "home/deck_check.h"
#include "home/objects.h"
#include "home/play_area.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define B_CURSOR_BLINK_PERIOD 0x04u
#define B_PAD_UP 6u
#define B_PAD_DOWN 7u
#define B_PAD_LEFT 5u
#define B_PAD_RIGHT 4u
#define PAD_A 0x01u
#define PAD_B 0x02u
#define CURSOR_BLINK_PERIOD_MASK 0x0fu
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define INPLAYAREA_OPP_BENCH_1 0x0bu
#define INPLAYAREA_OPP_DISCARD_PILE 0x0au
#define INPLAYAREA_OPP_PLAY_AREA 0x11u
#define INPLAYAREA_PLAYER_ACTIVE 0x05u
#define INPLAYAREA_PLAYER_PLAY_AREA 0x10u
#define MENU_CANCEL 0xffu
#define MENU_CONFIRM 0x01u
#define SFX_CURSOR 0x01u

#include "generated/wram.h"
#include "home/duel.h"
#include "home/card_data.h"
#include "home/core.h"
#define DUELVARS_ARENA_CARD 0xBBu
#define PLAY_AREA_ARENA 0x00u

#define INPLAYAREA_OPP_ACTIVE 0x08u
#define PLAY_AREA_BENCH_1 0x01u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/play_area.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/substatus.h"
#include "home/switch_rom.h"
#include "mem.h"

#define BANK_OPEN_IN_PLAY_AREA_SCREEN 0x06u
#define OPEN_IN_PLAY_AREA_TEXT_TABLE 0x42BBu
#define OPEN_IN_PLAY_AREA_TRANSITION_TABLE1 0x42DBu
#define OPEN_IN_PLAY_AREA_TRANSITION_TABLE2 0x434Bu
#define EMPTY_LINE_TEXT 0x0251u
#define HAND_TEXT_2 0x024Eu
#define PLAY_AREA_BENCH_5 0x05u
#define INPLAYAREA_PLAYER_HAND 0x06u
#define INPLAYAREA_OPP_HAND 0x09u
#define TRUE 0x01u

static void open_in_play_area_print_associated_text(uint8_t position)
{
	InitTextPrinting(1u, 17u);
	(void)ProcessTextFromID(EMPTY_LINE_TEXT);
	hffb0 = TRUE;
	(void)ProcessTextFromID(HAND_TEXT_2);
	hffb0 = 0u;
	InitTextPrinting(1u, 17u);

	uint16_t text_entry = (uint16_t)(OPEN_IN_PLAY_AREA_TEXT_TABLE +
		(uint16_t)position * 2u);
	uint16_t text = (uint16_t)(gb_read8(text_entry) |
		((uint16_t)gb_read8((uint16_t)(text_entry + 1u)) << 8));
	if ((text >> 8) != 0u || (uint8_t)text >= (uint8_t)(PLAY_AREA_BENCH_5 + 1u)) {
		if (position < INPLAYAREA_OPP_ACTIVE) {
			(void)PrintTextNoDelay(text, 1u, 17u);
		} else {
			SwapTurn();
			(void)PrintTextNoDelay(text, 1u, 17u);
			SwapTurn();
		}
		return;
	}

	uint8_t location = (uint8_t)text;
	DuelistVarResult duel;
	if (position < INPLAYAREA_PLAYER_HAND)
		duel = GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
	else
		duel = GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
	if (duel.a == 0xFFu)
		return;

	if (position >= INPLAYAREA_PLAYER_HAND)
		SwapTurn();
	uint16_t card_id = GetCardIDFromDeckIndex(duel.a);
	LoadCardDataToBuffer1_FromCardID((uint8_t)card_id);
	if (position >= INPLAYAREA_PLAYER_HAND)
		SwapTurn();
	(void)CopyCardNameAndLevel(18u, 0u, 0u, 0u, 0u);
	uint16_t default_text = wDefaultText_ADDR;
	ProcessText(&default_text);
}
/* <<< factory statics */

void ZeroObjectPositionsAndToggleOAMCopy_Bank6(void)
{
	ZeroObjectPositions();
	gb_write8(wVBlankOAMCopyToggle_ADDR, 1);
}

/* >>> factory OpenInPlayAreaScreen_HandleInput */
OpenInPlayAreaScreenHandleInputResult OpenInPlayAreaScreen_HandleInput(void)
{
	/* play_area.asm:376-685 */
	wMenuInputSFX = 0u;
	uint16_t table = (uint16_t)(wMenuInputTablePointer |
		((uint16_t)gb_read8((uint16_t)(wMenuInputTablePointer_ADDR + 1u)) << 8));

	uint8_t dpad = hDPadHeld;
	if (dpad != 0u) {
		uint8_t offset;
		if (dpad & (1u << B_PAD_UP))
			offset = 3u;
		else if (dpad & (1u << B_PAD_DOWN))
			offset = 4u;
		else if (dpad & (1u << B_PAD_RIGHT))
			offset = 5u;
		else if (dpad & (1u << B_PAD_LEFT))
			offset = 6u;
		else
			offset = 0xFFu;

		if (offset != 0xFFu) {
			uint16_t entry = (uint16_t)(table + HtimesL((uint16_t)(0x0700u | wInPlayAreaCurPosition)));
			uint8_t new_pos = gb_read8((uint16_t)(entry + offset));

			wInPlayAreaPreservedPosition = wInPlayAreaCurPosition;
			wInPlayAreaCurPosition = new_pos;

			if (new_pos < INPLAYAREA_PLAYER_ACTIVE) {
				uint8_t bench = (uint8_t)(GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a - 1u);
				if (bench == 0u) {
					wInPlayAreaCurPosition = INPLAYAREA_PLAYER_PLAY_AREA;
				} else if (wInPlayAreaCurPosition >= bench) {
					if (dpad & (1u << B_PAD_RIGHT))
						wInPlayAreaCurPosition = 0u;
					else
						wInPlayAreaCurPosition = (uint8_t)(bench - 1u);
				}
			} else if (new_pos >= INPLAYAREA_OPP_BENCH_1 && new_pos < INPLAYAREA_PLAYER_PLAY_AREA) {
				uint8_t bench = (uint8_t)(GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a - 1u);
				if (bench == 0u) {
					wInPlayAreaCurPosition = INPLAYAREA_OPP_PLAY_AREA;
				} else {
					uint8_t rel = (uint8_t)(wInPlayAreaCurPosition - INPLAYAREA_OPP_BENCH_1);
					if (rel >= bench) {
						if (dpad & (1u << B_PAD_LEFT))
							wInPlayAreaCurPosition = INPLAYAREA_OPP_BENCH_1;
						else
							wInPlayAreaCurPosition = (uint8_t)(bench + INPLAYAREA_OPP_DISCARD_PILE);
					}
				}
			}

			wMenuInputSFX = SFX_CURSOR;
			wCheckMenuCursorBlinkCounter = 0u;
		}
	}

	uint8_t keys = (uint8_t)(hKeysPressed & (PAD_A | PAD_B));
	if (keys != 0u) {
		if (keys & PAD_A) {
			ZeroObjectPositions();
			{
				uint16_t entry = (uint16_t)(table + HtimesL((uint16_t)(0x0700u | wInPlayAreaCurPosition)));
				uint8_t x = gb_read8(entry);
				uint8_t y = gb_read8((uint16_t)(entry + 1u));
				uint8_t attr = gb_read8((uint16_t)(entry + 2u));
				SetOneObjectAttributes(y, x, 0u, attr);
			}
			PlaySFXConfirmOrCancel(MENU_CONFIRM);
			return (OpenInPlayAreaScreenHandleInputResult){wInPlayAreaCurPosition, 0x10u};
		}
		PlaySFXConfirmOrCancel(MENU_CANCEL);
		return (OpenInPlayAreaScreenHandleInputResult){MENU_CANCEL, 0x10u};
	}

	uint8_t sfx = wMenuInputSFX;
	if (sfx != 0u)
		PlaySFX(sfx);

	uint8_t old_counter = wCheckMenuCursorBlinkCounter;
	wCheckMenuCursorBlinkCounter = (uint8_t)(old_counter + 1u);
	uint8_t masked = (uint8_t)(old_counter & CURSOR_BLINK_PERIOD_MASK);
	if (masked != 0u)
		return (OpenInPlayAreaScreenHandleInputResult){masked, 0x20u};

	if (wCheckMenuCursorBlinkCounter & (1u << B_CURSOR_BLINK_PERIOD)) {
		ZeroObjectPositionsAndToggleOAMCopy_Bank6();
		return (OpenInPlayAreaScreenHandleInputResult){0u, 0x00u};
	}

	ZeroObjectPositions();
	{
		uint16_t entry = (uint16_t)(table + HtimesL((uint16_t)(0x0700u | wInPlayAreaCurPosition)));
		uint8_t x = gb_read8(entry);
		uint8_t y = gb_read8((uint16_t)(entry + 1u));
		uint8_t attr = gb_read8((uint16_t)(entry + 2u));
		SetOneObjectAttributes(y, x, 0u, attr);
	}
	return (OpenInPlayAreaScreenHandleInputResult){0u, 0x00u};
}
/* <<< factory OpenInPlayAreaScreen_HandleInput */

/* >>> factory OpenInPlayAreaScreen_TurnHolderPlayArea */
void OpenInPlayAreaScreen_TurnHolderPlayArea(void)
{
	uint8_t slot = (uint8_t)(wInPlayAreaCurPosition + 1u);
	if (slot == (uint8_t)(INPLAYAREA_PLAYER_ACTIVE + 1u))
		slot = PLAY_AREA_ARENA;
	wCurPlayAreaSlot = slot;
	DuelistVarResult duel = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD));
	if (duel.a == 0xFFu)
		return;
	uint16_t card_id = GetCardIDFromDeckIndex(duel.a);
	LoadCardDataToBuffer1_FromCardID((uint8_t)card_id);
	wCurPlayAreaY = 0u;
	OpenCardPage_FromCheckPlayArea(0u, 0u, 0u, 0u, 0u, (uint8_t)card_id, card_id);
}
/* <<< factory OpenInPlayAreaScreen_TurnHolderPlayArea */

/* >>> factory OpenInPlayAreaScreen_NonTurnHolderPlayArea */
void OpenInPlayAreaScreen_NonTurnHolderPlayArea(void)
{
	uint8_t slot = (uint8_t)(wInPlayAreaCurPosition - INPLAYAREA_OPP_ACTIVE);
	if (slot != 0u)
		slot = (uint8_t)(slot - (INPLAYAREA_OPP_BENCH_1 - INPLAYAREA_OPP_ACTIVE - PLAY_AREA_BENCH_1));
	wCurPlayAreaSlot = slot;
	DuelistVarResult duel = GetNonTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD));
	if (duel.a == 0xFFu)
		return;
	SwapTurn();
	uint16_t card_id = GetCardIDFromDeckIndex(duel.a);
	LoadCardDataToBuffer1_FromCardID((uint8_t)card_id);
	wCurPlayAreaY = 0u;
	OpenCardPage_FromCheckPlayArea(0u, 0u, 0u, 0u, 0u, (uint8_t)card_id, card_id);
	SwapTurn();
}
/* <<< factory OpenInPlayAreaScreen_NonTurnHolderPlayArea */

/* >>> factory OpenInPlayAreaScreen_TurnHolderDiscardPile */
void OpenInPlayAreaScreen_TurnHolderDiscardPile(uint8_t c)
{
	uint8_t saved_hWhoseTurn = hWhoseTurn;
	(void)OpenTurnHolderDiscardPileScreen(c);
	hWhoseTurn = saved_hWhoseTurn;
}
/* <<< factory OpenInPlayAreaScreen_TurnHolderDiscardPile */

/* >>> factory OpenInPlayAreaScreen_NonTurnHolderDiscardPile */
/* play_area.asm:301-310 */
void OpenInPlayAreaScreen_NonTurnHolderDiscardPile(uint8_t c)
{
	uint8_t saved_hWhoseTurn = hWhoseTurn;
	(void)OpenNonTurnHolderDiscardPileScreen(c);
	hWhoseTurn = saved_hWhoseTurn;
}
/* <<< factory OpenInPlayAreaScreen_NonTurnHolderDiscardPile */

/* >>> factory OpenInPlayAreaScreen_NonTurnHolderHand */
void OpenInPlayAreaScreen_NonTurnHolderHand(void)
{
	uint8_t saved_hWhoseTurn = hWhoseTurn;
	(void)OpenNonTurnHolderHandScreen_Simple();
	hWhoseTurn = saved_hWhoseTurn;
}
/* <<< factory OpenInPlayAreaScreen_NonTurnHolderHand */

/* >>> factory OpenInPlayAreaScreen_TurnHolderHand */
uint8_t OpenInPlayAreaScreen_TurnHolderHand(void)
{
	uint8_t saved_hWhoseTurn = hWhoseTurn;
	(void)OpenTurnHolderHandScreen_Simple();
	hWhoseTurn = saved_hWhoseTurn;
	return saved_hWhoseTurn;
}
/* <<< factory OpenInPlayAreaScreen_TurnHolderHand */

/* >>> factory OpenInPlayAreaScreen */
void OpenInPlayAreaScreen(void)
{
	BankswitchROM(BANK_OPEN_IN_PLAY_AREA_SCREEN);
	wInPlayAreaCurPosition = INPLAYAREA_PLAYER_ACTIVE;

	for (;;) {
		wCheckMenuCursorBlinkCounter = 0u;
		DrawInPlayAreaScreen();
		EnableLCD();
		PkmnPowerCountResult clairvoyance = IsClairvoyanceActive();
		uint16_t transition_table = (clairvoyance.f & 0x10u) != 0u
			? OPEN_IN_PLAY_AREA_TRANSITION_TABLE2
			: OPEN_IN_PLAY_AREA_TRANSITION_TABLE1;
		wMenuInputTablePointer = (uint8_t)transition_table;
		gb_write8((uint16_t)(wMenuInputTablePointer_ADDR + 1u),
			(uint8_t)(transition_table >> 8));
		open_in_play_area_print_associated_text(wInPlayAreaCurPosition);

		for (;;) {
			wVBlankOAMCopyToggle = TRUE;
			DoFrame();
			uint8_t dpad = hDPadHeld;
			if ((dpad & 0x08u) != 0u)
				goto selection;
			if (wInPlayAreaFromSelectButton != 0u && (dpad & 0x04u) != 0u) {
				wCheckMenuCursorBlinkCounter = 9u;
				ZeroObjectPositionsAndToggleOAMCopy_Bank6();
				(void)SetupText(0x38u, 0x9Fu);
				return;
			}
			wInPlayAreaTemporaryPosition = wInPlayAreaCurPosition;
			OpenInPlayAreaScreenHandleInputResult input = OpenInPlayAreaScreen_HandleInput();
			if ((input.f & 0x10u) != 0u) {
				if (input.a == 0xFFu) {
					wCheckMenuCursorBlinkCounter = 9u;
					ZeroObjectPositionsAndToggleOAMCopy_Bank6();
					(void)SetupText(0x38u, 0x9Fu);
					return;
				}
				goto selection;
			}
			uint8_t position = wInPlayAreaCurPosition;
			if (position == INPLAYAREA_PLAYER_PLAY_AREA) {
				(void)SetupText(0x38u, 0x9Fu);
				uint8_t turn = hWhoseTurn;
				OpenTurnHolderPlayAreaScreen();
				hWhoseTurn = turn;
				wInPlayAreaCurPosition = wInPlayAreaPreservedPosition;
				break;
			}
			if (position == INPLAYAREA_OPP_PLAY_AREA) {
				(void)SetupText(0x38u, 0x9Fu);
				uint8_t turn = hWhoseTurn;
				OpenNonTurnHolderPlayAreaScreen();
				hWhoseTurn = turn;
				wInPlayAreaCurPosition = wInPlayAreaPreservedPosition;
				break;
			}
			if (position != wInPlayAreaTemporaryPosition)
				open_in_play_area_print_associated_text(position);
		}
		continue;

selection:
		ZeroObjectPositionsAndToggleOAMCopy_Bank6();
		(void)SetupText(0x38u, 0x9Fu);
		wInPlayAreaPreservedPosition = wInPlayAreaCurPosition;
		switch (wInPlayAreaCurPosition) {
		case 0u:
		case 1u:
		case 2u:
		case 3u:
		case 4u:
		case INPLAYAREA_PLAYER_ACTIVE:
			OpenInPlayAreaScreen_TurnHolderPlayArea();
			break;
		case INPLAYAREA_PLAYER_HAND:
			(void)OpenInPlayAreaScreen_TurnHolderHand();
			break;
		case 7u:
			OpenInPlayAreaScreen_TurnHolderDiscardPile(0u);
			break;
		case INPLAYAREA_OPP_ACTIVE:
			OpenInPlayAreaScreen_NonTurnHolderPlayArea();
			break;
		case INPLAYAREA_OPP_HAND:
			OpenInPlayAreaScreen_NonTurnHolderHand();
			break;
		case 0x0Au:
			OpenInPlayAreaScreen_NonTurnHolderDiscardPile(0u);
			break;
		default:
			OpenInPlayAreaScreen_NonTurnHolderPlayArea();
			break;
		}
		wInPlayAreaCurPosition = wInPlayAreaPreservedPosition;
	}
}
/* <<< factory OpenInPlayAreaScreen */
