#include "home/duel.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel_core.h"
#include "home/print_text.h"
#include "home/switch_sram.h"
#include "mem.h"

/* HIGH(wOpponentDuelVariables), the value hWhoseTurn carries on the opponent's turn. */
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))
#define PLAYER_TURN ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))

/* duel.asm:1316-1323: [hWhoseTurn << 8 | a], the current turn holder's duelvar a. */
DuelistVarResult GetTurnDuelistVariable(uint8_t a)
{
	uint16_t address = (uint16_t)(((uint16_t)hWhoseTurn << 8) | a);
	return (DuelistVarResult){gb_read8(address), address};
}

/* duel.asm:1325-1337: the other player's duelvar a. */
DuelistVarResult GetNonTurnDuelistVariable(uint8_t a)
{
	uint8_t turn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;
	uint16_t address = (uint16_t)(((uint16_t)turn << 8) | a);
	return (DuelistVarResult){gb_read8(address), address};
}

/* duel.asm:2364-2371: the other player becomes the turn holder. */
void SwapTurn(void)
{
	hWhoseTurn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;
}

/* duel.asm:762-777: deck index -> card id, from the turn holder's deck.
 * `ld hl, wPlayerDeck / add hl, de / ld a, [hl]` leaves hl = deck + a. */
DeckCardResult _GetCardIDFromDeckIndex(uint8_t a)
{
	uint16_t deck = hWhoseTurn == PLAYER_TURN ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	return (DeckCardResult){gb_read8((uint16_t)(deck + a)), (uint16_t)(deck + a)};
}

/* duel.asm:701-711: id in de, af and hl preserved (both pushed and popped). */
uint16_t GetCardIDFromDeckIndex(uint8_t a)
{
	return _GetCardIDFromDeckIndex(a).a;
}

/* duel.asm:661-668: id in a and c, b = 0, hl preserved. */
DeckCardResult GetCardIDFromDeckIndex_bc(uint8_t a, uint16_t hl)
{
	return (DeckCardResult){_GetCardIDFromDeckIndex(a).a, hl};
}

/* duel.asm:670-684: the temp-list entry in a, shadowed in hTempCardIndex_ff98,
 * hl and de preserved. */
DeckCardResult GetCardInDuelTempList_OnlyDeckIndex(uint8_t a, uint16_t hl)
{
	uint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + a));
	hTempCardIndex_ff98 = entry;
	return (DeckCardResult){entry, hl};
}

/* duel.asm:686-699: entry in a (reloaded after the call), id in de, hl preserved. */
DeckEntryResult GetCardInDuelTempList(uint8_t a, uint16_t hl)
{
	uint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + a));
	hTempCardIndex_ff98 = entry;
	uint16_t id = GetCardIDFromDeckIndex(entry);
	return (DeckEntryResult){entry, (uint8_t)(id >> 8), (uint8_t)id, hl};
}

/* duel.asm:778-812. `push af` keeps the deck index for the trainer conversion;
 * de carries the card id through both calls, so the final `ld a, e` is the id's
 * low byte. Every other register is restored by the pops. */
static uint8_t load_card_data_from_deck_index(uint8_t a, uint16_t buffer, void (*load)(uint8_t))
{
	uint16_t id = GetCardIDFromDeckIndex(a);
	load((uint8_t)id);
	(void)ConvertSpecialTrainerCardToPokemon(a, buffer, id);
	return (uint8_t)id;
}

uint8_t LoadCardDataToBuffer1_FromDeckIndex(uint8_t a)
{
	return load_card_data_from_deck_index(a, wLoadedCard1_ADDR,
					      LoadCardDataToBuffer1_FromCardID);
}

uint8_t LoadCardDataToBuffer2_FromDeckIndex(uint8_t a)
{
	return load_card_data_from_deck_index(a, wLoadedCard2_ADDR,
					      LoadCardDataToBuffer2_FromCardID);
}

/* Text ID of the fallback opponent name. */
#define PLAYER2_TEXT_ID 0x0092u

/* CopyPlayerName's `.loop` tail. CopyOpponentName's name-buffer path jumps straight
 * into it, so the DisableSRAM runs on that path too even though it never enabled SRAM. */
static CopyTextResult copy_name_loop(uint16_t hl, uint16_t de)
{
	uint8_t a;

	do {
		a = gb_read8(hl++);
		gb_write8(de++, a);
	} while (a);
	de--;
	DisableSRAM();
	return (CopyTextResult){a, (uint8_t)(de >> 8), (uint8_t)de, hl};
}

CopyTextResult CopyPlayerName(uint16_t de)
{
	EnableSRAM();
	return copy_name_loop(sPlayerName_ADDR, de);
}

CopyTextResult CopyOpponentName(uint16_t de)
{
	uint16_t name = (uint16_t)(gb_read8(wOpponentName_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wOpponentName_ADDR + 1u)) << 8);

	if (name)
		return CopyText(name, de);
	if (gb_read8(wNameBuffer_ADDR))
		return copy_name_loop(wNameBuffer_ADDR, de);
	return CopyText(PLAYER2_TEXT_ID, de);
}
