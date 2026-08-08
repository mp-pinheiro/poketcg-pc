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

#define DUELVARS_HAND 0x42u
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xeeu
#define DUELVARS_CARD_LOCATIONS 0x00u
#define CARD_LOCATION_JUST_DRAWN 0x40u
#define TYPE_ENERGY_F 3u
#define PLAY_AREA_MASK 0x10u

/* duel.asm:526-533: b = hand count, hl = page + $41 + count, de = wDuelTempList. */
HandListResult FindLastCardInHand(uint8_t c)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	return (HandListResult){(uint8_t)(DUELVARS_HAND - 1u + count), count, c,
				(uint8_t)(wDuelTempList_ADDR >> 8), (uint8_t)wDuelTempList_ADDR,
				0x00u, (uint16_t)(((uint16_t)hWhoseTurn << 8) |
						  (DUELVARS_HAND - 1u + count))};
}

/* duel.asm:473-500. Walks the hand backward from the last card, skipping
 * just-drawn cards. Exit a = hand count, carry iff the hand is empty. */
HandListResult CreateHandCardList(uint8_t c)
{
	HandListResult last = FindLastCardInHand(c);
	uint8_t count = last.b;
	uint16_t src = last.hl;
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t deck_index = gb_read8(src--);
		uint8_t location = gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | deck_index));
		if (!(location & CARD_LOCATION_JUST_DRAWN))
			gb_write8(dst++, deck_index);
	}
	gb_write8(dst, 0xFF);
	uint8_t hand_count = gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) |
						   DUELVARS_NUMBER_OF_CARDS_IN_HAND));
	uint8_t f = hand_count ? 0x00u : 0x90u;
	return (HandListResult){hand_count, 0, c, (uint8_t)(dst >> 8), (uint8_t)dst, f,
				(uint16_t)(((uint16_t)hWhoseTurn << 8) |
					   DUELVARS_NUMBER_OF_CARDS_IN_HAND)};
}

/* duel.asm:435-470. Location-masked scan of the 60 card locations; energies of the
 * requested play-area location go into wDuelTempList. Exit a = the first entry,
 * carry iff the list is empty. */
HandListResult CreateArenaOrBenchEnergyCardList(uint8_t a)
{
	uint8_t location_mask = (uint8_t)(a | PLAY_AREA_MASK);
	uint16_t dst = wDuelTempList_ADDR;
	uint8_t first = 0xFF;
	for (uint8_t i = 0; i < DECK_SIZE; i++) {
		if (gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | i)) != location_mask)
			continue;
		(void)LoadCardDataToBuffer2_FromDeckIndex(i);
		if (!(gb_read8(wLoadedCard2Type_ADDR) & (uint8_t)(1u << TYPE_ENERGY_F)))
			continue;
		gb_write8(dst++, i);
		if (first == 0xFF)
			first = i;
	}
	gb_write8(dst, 0xFF);
	uint8_t f;
	if (first == 0xFF)
		f = 0x90u; /* `cp $ff` set Z, `scf` kept it */
	else
		f = first ? 0x00u : 0x80u; /* `or a` on the first entry */
	return (HandListResult){first, 0, location_mask, (uint8_t)(dst >> 8), (uint8_t)dst,
				f, (uint16_t)(((uint16_t)hWhoseTurn << 8) + DECK_SIZE)};
}

#include "home/random.h"

/* duel.asm:541-563. `or a / ret z` on entry; otherwise swap each of the first a
 * deck bytes with [de + Random(c)], where de starts at hl. Exit a is the byte
 * swapped into the last position; the tail pops restore every other register. */
ShuffleCardsResult ShuffleCards(uint8_t a, uint16_t hl)
{
	if (!a)
		return (ShuffleCardsResult){0, 0x80u};
	uint8_t c = a;
	uint16_t de = hl;
	uint8_t last = 0;
	for (uint8_t i = 0; i < a; i++) {
		uint16_t target = (uint16_t)(de + Random(c));
		uint8_t swap = gb_read8(target);
		uint8_t moving = gb_read8((uint16_t)(hl + i));
		gb_write8((uint16_t)(hl + i), swap);
		gb_write8(target, moving);
		last = moving;
	}
	/* The final `dec b` from 1 leaves Z+N on the way out. */
	return (ShuffleCardsResult){last, 0xC0u};
}

#define HTEMP_LIST_PTR 0xFF99u
#define HTEMP_CARD_ID 0xFF9Bu

static uint16_t list_ptr(void)
{
	return (uint16_t)(gb_read8(HTEMP_LIST_PTR) |
			  (uint16_t)gb_read8((uint16_t)(HTEMP_LIST_PTR + 1u)) << 8);
}

static void list_set_ptr(uint16_t ptr)
{
	gb_write8(HTEMP_LIST_PTR, (uint8_t)ptr);
	gb_write8((uint16_t)(HTEMP_LIST_PTR + 1u), (uint8_t)(ptr >> 8));
}

/* duel.asm:589-648. The terminator is $FF, whose bit 7 is the loop-exit test. Each
 * pass finds the lowest-ID card in the remaining span and swaps it to the front,
 * then advances the pointer; the final `bit 7, [hl]` on the terminator leaves
 * Z clear and H set. */
SortResult SortCardsInListByID(uint8_t b, uint8_t c, uint16_t de)
{
	for (;;) {
		uint16_t ptr = list_ptr();
		if (gb_read8(ptr) & 0x80u) {
			/* `bit 7, [hl]` on the $FF terminator: Z clear, H set. */
			return (SortResult){(uint8_t)ptr, b, c, (uint8_t)(de >> 8), (uint8_t)de,
						0x20u, ptr};
		}
		uint16_t lowest_pos = ptr;
		uint16_t lowest_id = GetCardIDFromDeckIndex_bc(gb_read8(ptr), 0).a;
		uint16_t scan = (uint16_t)(ptr + 1u);
		while (!(gb_read8(scan) & 0x80u)) {
			uint16_t candidate = GetCardIDFromDeckIndex_bc(gb_read8(scan), 0).a;
			/* The asm's `cp / jr c, .not_lower_id` updates the slot on EQUAL ids
			 * too (only a strictly smaller current-lowest keeps the slot), so the
			 * sort is unstable: the last equal card moves to the front. */
			if (candidate <= lowest_id) {
				lowest_id = candidate;
				lowest_pos = scan;
			}
			scan++;
		}
		uint8_t front = gb_read8(ptr);
		gb_write8(ptr, gb_read8(lowest_pos));
		gb_write8(lowest_pos, front);
		/* Every pass ends with b = 0 (GetCardIDFromDeckIndex_bc's `ld b, $0`),
		 * c = the swapped-out front, de = the lowest-card position. */
		b = 0;
		c = front;
		de = lowest_pos;
		list_set_ptr((uint16_t)(ptr + 1u));
	}
}

/* duel.asm:578-587. Point the list pointer at wDuelTempList and sort it. On an
 * empty list the first terminator check returns with the entry registers intact. */
SortResult SortCardsInDuelTempListByID(uint8_t b, uint8_t c, uint16_t de)
{
	list_set_ptr(wDuelTempList_ADDR);
	return SortCardsInListByID(b, c, de);
}

/* duel.asm:502-525. Copies the hand (newest last) into wDuelTempList, sorts it,
 * then writes it back from the last hand position down, so the lowest id lands at
 * the newest slot. The trailing `dec b` leaves Z+N and a = the last copied value;
 * hl ends one before the first hand card (page + $41). */
HandSortResult SortHandCardsByID(void)
{
	HandListResult last = FindLastCardInHand(0);
	uint8_t count = last.b;
	uint16_t src = last.hl;
	uint16_t dst = wDuelTempList_ADDR;
	for (uint8_t i = 0; i < count; i++)
		gb_write8(dst++, gb_read8(src--));
	gb_write8(dst, 0xFF);
	/* The sort's exit c (its last swap front) survives to the routine's exit. */
	SortResult sorted = SortCardsInDuelTempListByID(0, 0, wDuelTempList_ADDR);
	dst = wDuelTempList_ADDR;
	uint16_t hand = (uint16_t)(((uint16_t)hWhoseTurn << 8) | (DUELVARS_HAND - 1u + count));
	uint8_t last_card = 0;
	for (uint8_t i = 0; i < count; i++) {
		last_card = gb_read8(dst++);
		gb_write8(hand--, last_card);
	}
	return (HandSortResult){last_card, 0, sorted.c, (uint8_t)(dst >> 8), (uint8_t)dst,
				0xC0u, (uint16_t)(((uint16_t)hWhoseTurn << 8) + DUELVARS_HAND - 1u)};
}

/* duel.asm:1915-1922. The table is `db $80, $40, $20, $10, $08, $04, $02, $01`
 * (InvertedPowersOf2, 00:1A1A). Entry a is a color index; all other registers
 * are preserved. */
uint8_t TranslateColorToWR(uint8_t a)
{
	return rom_ptr(0u, 0x1A1Au)[a];
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
