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

/* duel.asm:2011-2030. `sub e` then `sbc d` borrows the high byte; `and $80` on the
 * 8-bit result is the sign of the 16-bit subtraction, so a set sign means the
 * damage exceeded the HP and it clamps to zero. The tail is `or a / jr z / scf`,
 * so carry is set exactly when HP remains non-zero. */
SubtractHPResult SubtractHP(uint16_t hl, uint16_t de)
{
	uint8_t hp = gb_read8(hl);
	uint16_t damage = de;
	uint8_t remaining;
	if ((uint16_t)hp >= damage) {
		remaining = (uint8_t)(hp - damage);
	} else {
		remaining = 0;
	}
	gb_write8(hl, remaining);
	/* `or a` sets Z on zero; `scf` then sets C on non-zero. */
	uint8_t f = remaining ? 0x10u : 0x80u;
	return (SubtractHPResult){remaining, f};
}

#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xbau
#define DUELVARS_DECK_CARDS 0x7eu
#define DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE 0xedu
#define DECK_SIZE 60u

/* duel.asm:398-431. Copies DECK_SIZE - n remaining deck ids into wDuelTempList.
 * The `or a; ret` tail leaves carry clear on the non-empty path, so the exit is
 * Z-only; the empty path is `scf`. Exit hl is page + $BA on both paths (the
 * GetTurnDuelistVariable residue equals where the copy loop ends). */
CardListResult CreateDeckCardList(uint8_t c, uint16_t de)
{
	DuelistVarResult not_in_deck = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (not_in_deck.a >= DECK_SIZE) {
		/* b/c/de are never touched on this path. The `cp DECK_SIZE` above left Z
		 * set iff n == 60 exactly, and `scf` preserves it. */
		gb_write8(wDuelTempList_ADDR, 0xFF);
		uint8_t f = (uint8_t)(0x10u | (not_in_deck.a == DECK_SIZE ? 0x80u : 0x00u));
		return (CardListResult){0xFF, 0, c, (uint8_t)(de >> 8), (uint8_t)de, f,
					not_in_deck.hl};
	}
	uint8_t count = (uint8_t)(DECK_SIZE - not_in_deck.a);
	uint16_t src = (uint16_t)(((uint16_t)hWhoseTurn << 8) |
				  (DUELVARS_DECK_CARDS + not_in_deck.a));
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++)
		gb_write8((uint16_t)(dst + i), gb_read8((uint16_t)(src + i)));
	gb_write8((uint16_t)(dst + count), 0xFF);
	/* `dec b / jr nz` leaves b = 0; c is the count it was loaded with. */
	return (CardListResult){count, 0, count, (uint8_t)((dst + count) >> 8),
				(uint8_t)(dst + count), 0x00u, not_in_deck.hl};
}

/* duel.asm:713-746. `ld a, b / or a / jr nz / scf` sets carry iff the compacted
 * list is empty; every other register is pushed and popped, so a is the only
 * remaining output besides the flag. */
TempListResult RemoveCardFromDuelTempList(uint8_t a)
{
	uint16_t src = wDuelTempList_ADDR;
	uint16_t dst = wDuelTempList_ADDR;
	uint8_t count = 0;
	for (;;) {
		uint8_t entry = gb_read8(src++);
		if (entry == 0xFF)
			break;
		if (entry != a) {
			gb_write8(dst++, entry);
			count++;
		}
	}
	gb_write8(dst, 0xFF);
	/* `or a` set Z on the empty exit, then `scf` keeps it: Z+C. */
	return (TempListResult){count, count ? 0x00u : 0x90u};
}

/* duel.asm:747-761. The terminator `cp $ff` on the $FF byte leaves Z+N ($C0);
 * only a carries the count. */
TempListResult CountCardsInDuelTempList(void)
{
	uint8_t count = 0;
	while (gb_read8((uint16_t)(wDuelTempList_ADDR + count)) != 0xFF)
		count++;
	return (TempListResult){count, 0xC0u};
}

/* duel.asm:369-397. Reads the discard pile backward into wDuelTempList; carry is
 * set iff the pile is empty (`or a / ret nz / scf`, so the empty exit is Z+C).
 * `inc b / dec b` leaves b = 0 on both paths; c is never touched. */
CardListResult CreateDiscardPileCardList(uint8_t c)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE).a;
	uint16_t src = (uint16_t)(((uint16_t)hWhoseTurn << 8) | (DUELVARS_DECK_CARDS - 1u) + count);
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++)
		gb_write8((uint16_t)(dst + i), gb_read8((uint16_t)(src - i)));
	gb_write8((uint16_t)(dst + count), 0xFF);
	uint8_t f = count ? 0x00u : 0x90u;
	return (CardListResult){count, 0, c, (uint8_t)((dst + count) >> 8),
				(uint8_t)(dst + count), f,
				(uint16_t)(((uint16_t)hWhoseTurn << 8) |
					      DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE)};
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
