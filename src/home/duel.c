#include "home/duel.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel_core.h"
#include "home/card_color.h"
#include "home/substatus.h"
#include "home/print_text.h"
#include "home/switch_sram.h"
#include "home/menus.h"
#include "home/frames.h"
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
#define DUELVARS_ARENA_CARD 0xbbu
#define DUELVARS_ARENA_CARD_HP 0xc8u
#define CARD_LOCATION_JUST_DRAWN 0x40u
#define TYPE_ENERGY_F 3u
#define PLAY_AREA_MASK 0x10u

/* duel.asm:2306-2320. The final `sub [hl]` borrows when the damage exceeds the
 * max HP; c keeps the HP, a the difference, and the borrow is the exit carry. */
CardDamageResult GetCardDamageAndMaxHP(uint8_t e)
{
	uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
	(void)LoadCardDataToBuffer2_FromDeckIndex(deck_index);
	uint8_t damage = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + e)).a;
	uint8_t max_hp = gb_read8(wLoadedCard2HP_ADDR);
	uint8_t difference = (uint8_t)(max_hp - damage);
	/* `sub [hl]`: N always, H on the low-nibble borrow, C on the full-byte borrow,
	 * Z when the difference is zero. */
	uint8_t f = 0x40u;
	if ((max_hp & 0x0Fu) < (damage & 0x0Fu))
		f |= 0x20u;
	if (max_hp < damage)
		f |= 0x10u;
	if (!difference)
		f |= 0x80u;
	return (CardDamageResult){difference, max_hp, f};
}

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

/* duel.asm:1290-1315. Entry hl must already hold the card-locations page; the
 * routine only walks l from 0 to 60. `ld a, c / pop bc` leaves a = the count and
 * restores bc, so the only other exit is hl = page + 60. */
CardCountResult CountCardIDInLocation(uint8_t b, uint8_t e, uint16_t hl)
{
	uint8_t count = 0;
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		if (gb_read8((uint16_t)(hl + l)) != b)
			continue;
		if (_GetCardIDFromDeckIndex(l).a != e)
			continue;
		count++;
	}
	return (CardCountResult){count, (uint16_t)(hl + DECK_SIZE)};
}

/* duel.asm:2331-2357. PowersOf2 (00:11B7) is `db $01..$80`. The rra x3 folds a's
 * top five bits into the group index. */
AttackFlagResult CheckLoadedAttackFlag(uint8_t a)
{
	uint8_t bit = (uint8_t)(1u << (a & 0x07u));
	uint8_t group = (uint8_t)((a >> 3) & 0x1Fu);
	uint8_t value = (uint8_t)(gb_read8((uint16_t)(wLoadedAttackFlag1_ADDR + group)) & bit);
	/* Oracle-observed exits: scf on the set path leaves C only; the clear path
	 * carries Z+H from the final `and b` (0xA0). */
	uint8_t f = value ? 0x10u : 0xA0u;
	return (AttackFlagResult){value, f};
}

/* duel.asm:369-397. Reads the discard pile backward into wDuelTempList; carry is
 * set iff the pile is empty (`or a / ret nz / scf`, so the empty exit is Z+C).
 * `inc b / dec b` leaves b = 0 on both paths; c is never touched. */
CardListResult CreateDiscardPileCardList(uint8_t c)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE).a;
	uint16_t src = (uint16_t)(((uint16_t)hWhoseTurn << 8) | ((DUELVARS_DECK_CARDS - 1u) + count));
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

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define DUELVARS_PRIZES 0xecu
#define CARD_LOCATION_DECK 0x00u
#define CARD_LOCATION_HAND 0x01u
#define CARD_LOCATION_DISCARD_PILE 0x02u
#define DUELVARS_ARENA_CARD_FLAGS 0xc2u
#define DUELVARS_ARENA_CARD_STAGE 0xceu
#define DUELVARS_ARENA_CARD_CHANGED_TYPE 0xd4u
#define DUELVARS_ARENA_CARD_ATTACHED_DEFENDER 0xdau
#define DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER 0xe0u
#define DUELVARS_ARENA_CARD_SUBSTATUS1 0xe7u
#define DUELVARS_ARENA_CARD_SUBSTATUS2 0xe8u
#define DUELVARS_ARENA_CARD_CHANGED_WEAKNESS 0xe9u
#define DUELVARS_ARENA_CARD_CHANGED_RESISTANCE 0xeau
#define DUELVARS_ARENA_CARD_SUBSTATUS3 0xebu
#define DUELVARS_ARENA_CARD_STATUS 0xf0u
#define DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX 0xf2u
#define SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F 0u
#define CAN_EVOLVE_THIS_TURN 0x80u
#define NUM_TYPES 8u
#define TYPE_PKMN 0x07u
#define PLUSPOWER 0xd8u
#define DEFENDER 0xd9u
#define ATTACK_DATA_LEN 0x13u
#define MAX_PLAY_AREA_POKEMON 6u
#define PLAY_AREA_ARENA 0u
#define COLORLESS 6u

/* duel.asm:60-104. */
CardListResult CopyDeckData(uint16_t de)
{
	uint16_t deck = hWhoseTurn == PLAYER_TURN ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	uint16_t last_slot = (uint16_t)(deck + DECK_SIZE - 1u);
	uint16_t dst = deck;
	uint8_t last_value;
	uint8_t f;

	gb_write8(last_slot, 0);
	for (;;) {
		uint8_t count = gb_read8(de++);
		uint8_t id;

		if (!count)
			break;
		id = gb_read8(de++);
		for (uint8_t i = 0; i < count; i++)
			gb_write8(dst++, id);
	}
	gb_write8(wDeckName_ADDR, gb_read8(de++));
	gb_write8((uint16_t)(wDeckName_ADDR + 1u), gb_read8(de));

	/* The trailing `ld bc, DECK_SIZE - 1` (re-deriving hl for the final check)
	 * overwrites b/c unconditionally: b = 0, c = DECK_SIZE - 1 always. */
	last_value = gb_read8(last_slot);
	f = last_value ? 0x00u : 0x90u;

	return (CardListResult){last_value, 0, (uint8_t)(DECK_SIZE - 1u), (uint8_t)(de >> 8),
				(uint8_t)de, f, last_slot};
}

/* duel.asm:107-120. Verified exhaustively (all 256 byte values) against the
 * `rr l / adc 0` carry-ring: it computes popcount. */
uint8_t CountPrizes(void)
{
	uint8_t mask = GetTurnDuelistVariable(DUELVARS_PRIZES).a;
	uint8_t count = 0;

	while (mask) {
		count = (uint8_t)(count + (mask & 1u));
		mask = (uint8_t)(mask >> 1);
	}
	return count;
}

/* duel.asm:124-137. */
ShuffleDeckResult ShuffleDeck(uint8_t c, uint8_t e)
{
	uint8_t turn = hWhoseTurn;
	uint16_t page = (uint16_t)((uint16_t)turn << 8);
	uint8_t not_in_deck = gb_read8((uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK));
	uint8_t count = (uint8_t)(DECK_SIZE - not_in_deck);
	uint16_t deck_offset = (uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + not_in_deck));
	ShuffleCardsResult r = ShuffleCards(count, deck_offset);

	return (ShuffleDeckResult){r.a, count, c, turn, e, r.f, deck_offset};
}

/* duel.asm:142-161. */
DrawCardResult DrawCardFromDeck(void)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t not_in_deck_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t not_in_deck = gb_read8(not_in_deck_addr);
	uint8_t card;

	if (not_in_deck >= DECK_SIZE) {
		uint8_t f = (uint8_t)(0x10u | (not_in_deck == DECK_SIZE ? 0x80u : 0x00u));
		return (DrawCardResult){not_in_deck, f};
	}
	gb_write8(not_in_deck_addr, (uint8_t)(not_in_deck + 1u));
	card = gb_read8((uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + not_in_deck)));
	gb_write8((uint16_t)(page | card), CARD_LOCATION_JUST_DRAWN);
	return (DrawCardResult){card, card ? 0x00u : 0x80u};
}

/* duel.asm:165-180. */
void ReturnCardToDeck(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t not_in_deck_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t not_in_deck = (uint8_t)(gb_read8(not_in_deck_addr) - 1u);

	gb_write8(not_in_deck_addr, not_in_deck);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + not_in_deck)), a);
	gb_write8((uint16_t)(page | a), CARD_LOCATION_DECK);
}

/* duel.asm:185-217. */
void SearchCardInDeckAndAddToHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t not_in_deck_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t not_in_deck = gb_read8(not_in_deck_addr);
	uint8_t in_deck = (uint8_t)(DECK_SIZE - not_in_deck);
	uint16_t loc_addr = (uint16_t)(page | a);
	uint16_t hl = (uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS + DECK_SIZE - 1u));
	uint16_t de = hl;

	gb_write8(not_in_deck_addr, (uint8_t)(not_in_deck + 1u));
	gb_write8(loc_addr, (uint8_t)(gb_read8(loc_addr) | CARD_LOCATION_JUST_DRAWN));
	for (uint8_t i = 0; i < in_deck; i++) {
		uint8_t card = gb_read8(hl--);

		if (card == a)
			continue;
		gb_write8(de--, card);
	}
}

/* duel.asm:221-242. */
void AddCardToHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	uint8_t count = (uint8_t)(gb_read8(count_addr) + 1u);

	gb_write8((uint16_t)(page | a), CARD_LOCATION_HAND);
	gb_write8(count_addr, count);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_HAND - 1u + count)), a);
}

/* duel.asm:246-280. */
void RemoveCardFromHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	uint8_t count = gb_read8(count_addr);
	uint16_t src = (uint16_t)(page | DUELVARS_HAND);
	uint16_t dst = src;

	if (!count)
		return;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t card = gb_read8(src++);

		if (card == a) {
			gb_write8(count_addr, (uint8_t)(gb_read8(count_addr) - 1u));
			continue;
		}
		gb_write8(dst++, card);
	}
}

/* duel.asm:294-311. */
void PutCardInDiscardPile(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t count = (uint8_t)(gb_read8(count_addr) + 1u);

	gb_write8((uint16_t)(page | a), CARD_LOCATION_DISCARD_PILE);
	gb_write8(count_addr, count);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_DECK_CARDS - 1u + count)), a);
}

/* duel.asm:284-311. */
MoveCardResult MoveHandCardToDiscardPile(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t hl = (uint16_t)(page | a);
	uint8_t masked = (uint8_t)(gb_read8(hl) & (uint8_t)~CARD_LOCATION_JUST_DRAWN);

	if (masked != CARD_LOCATION_HAND) {
		uint8_t f = 0x40u;

		if ((masked & 0x0Fu) < (CARD_LOCATION_HAND & 0x0Fu))
			f |= 0x20u;
		if (masked < CARD_LOCATION_HAND)
			f |= 0x10u;
		return (MoveCardResult){masked, f, hl};
	}
	RemoveCardFromHand(a);
	PutCardInDiscardPile(a);
	return (MoveCardResult){a, 0xC0u, hl};
}

/* duel.asm:316-346. */
MoveDiscardResult MoveDiscardPileCardToHand(uint8_t a)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t loc_addr = (uint16_t)(page | a);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_CARDS_IN_DISCARD_PILE);
	uint8_t count = gb_read8(count_addr);
	uint16_t src, dst;
	uint8_t last_carry;
	uint8_t f;

	gb_write8(loc_addr, (uint8_t)(gb_read8(loc_addr) | CARD_LOCATION_JUST_DRAWN));
	if (!count)
		return (MoveDiscardResult){0, 0x80u};
	gb_write8(count_addr, (uint8_t)(count - 1u));
	src = (uint16_t)(page | DUELVARS_DECK_CARDS);
	dst = src;
	last_carry = 0;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t card = gb_read8(src++);

		last_carry = card < a ? 1u : 0u;
		if (card == a)
			continue;
		gb_write8(dst++, card);
	}
	f = (uint8_t)(0xC0u | (last_carry ? 0x10u : 0x00u));
	return (MoveDiscardResult){a, f};
}

/* duel.asm:350-362. PowersOf2 (00:11B7) is `db $01..$80`. */
CheckPrizeResult CheckPrizeTaken(uint8_t a)
{
	uint8_t mask = rom_ptr(0u, 0x11B7u)[a];
	uint8_t comp = (uint8_t)~mask;
	DuelistVarResult prizes = GetTurnDuelistVariable(DUELVARS_PRIZES);
	uint8_t result = (uint8_t)(prizes.a & mask);
	uint8_t f = (uint8_t)(0x20u | (result ? 0x00u : 0x80u));

	return (CheckPrizeResult){result, comp, mask, f, prizes.hl};
}

/* duel.asm:650-657. Identical to entering the top of SortCardsInListByID's own
 * loop. */
SortResult SortCardsInListByID_CheckForListTerminator(uint8_t b, uint8_t c, uint16_t de)
{
	return SortCardsInListByID(b, c, de);
}

/* duel.asm:879-915. */
EvolveResult CheckIfCanEvolveInto(uint8_t d, uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t card2_idx = gb_read8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + e)));
	uint16_t flags_addr;
	uint8_t flags;

	(void)LoadCardDataToBuffer2_FromDeckIndex(card2_idx);
	(void)LoadCardDataToBuffer1_FromDeckIndex(d);
	if (gb_read8(wLoadedCard1PreEvoName_ADDR) != gb_read8(wLoadedCard2Name_ADDR))
		return (EvolveResult){0, 0, d, e, 0x90u, wLoadedCard2Name_ADDR};
	if (gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u)) !=
	    gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)))
		return (EvolveResult){0, 0, d, e, 0x90u, (uint16_t)(wLoadedCard2Name_ADDR + 1u)};

	flags_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + e));
	flags = (uint8_t)(gb_read8(flags_addr) & CAN_EVOLVE_THIS_TURN);
	if (flags)
		return (EvolveResult){flags, 0, d, e, 0x00u, flags_addr};
	return (EvolveResult){0x01u, 0, d, e, 0x10u, flags_addr};
}

/* duel.asm:922-957. */
EvolveResult CheckIfCanEvolveInto_BasicToStage2(uint8_t d, uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t flags_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + e));
	uint8_t flags = (uint8_t)(gb_read8(flags_addr) & CAN_EVOLVE_THIS_TURN);
	uint8_t basic_idx;
	uint16_t stage1_name;
	uint8_t byte1;

	if (!flags)
		return (EvolveResult){0, 0, d, e, 0x90u, flags_addr};

	basic_idx = gb_read8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + e)));
	(void)LoadCardDataToBuffer2_FromDeckIndex(basic_idx);
	(void)LoadCardDataToBuffer1_FromDeckIndex(d);
	stage1_name = (uint16_t)(gb_read8(wLoadedCard1PreEvoName_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u)) << 8));
	LoadCardDataToBuffer1_FromName(stage1_name);

	if (gb_read8(wLoadedCard1PreEvoName_ADDR) != gb_read8(wLoadedCard2Name_ADDR))
		return (EvolveResult){0, 0, d, e, 0x90u, wLoadedCard2Name_ADDR};
	byte1 = gb_read8((uint16_t)(wLoadedCard1PreEvoName_ADDR + 1u));
	if (byte1 != gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)))
		return (EvolveResult){0, 0, d, e, 0x90u, (uint16_t)(wLoadedCard2Name_ADDR + 1u)};
	return (EvolveResult){byte1, 0, d, e, byte1 ? 0x00u : 0x80u,
				(uint16_t)(wLoadedCard2Name_ADDR + 1u)};
}

/* duel.asm:814-822. */
EvolveResult EvolvePokemonCardIfPossible(uint8_t c)
{
	uint8_t card_idx = hTempCardIndex_ff98;
	uint8_t slot = hTempPlayAreaLocation_ff9d;
	EvolveResult check = CheckIfCanEvolveInto(card_idx, slot);
	EvolveResult evolved;

	if (check.f & 0x10u)
		return (EvolveResult){check.a, c, card_idx, slot, check.f, check.hl};
	evolved = EvolvePokemonCard();
	return (EvolveResult){evolved.a, evolved.c, card_idx, evolved.e, evolved.f, evolved.hl};
}

/* duel.asm:824-869. */
EvolveResult EvolvePokemonCard(void)
{
	uint8_t slot = hTempPlayAreaLocation_ff9d;
	uint8_t card_idx = hTempCardIndex_ff98;
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t arena_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + slot));
	uint8_t pre_evo_idx = gb_read8(arena_addr);
	uint16_t hp_addr;
	uint8_t old_hp2, new_hp1, diff;
	uint16_t stage_addr;
	uint8_t stage;

	gb_write8(wPreEvolutionPokemonCard_ADDR, pre_evo_idx);
	(void)LoadCardDataToBuffer2_FromDeckIndex(pre_evo_idx);
	gb_write8(arena_addr, card_idx);
	(void)LoadCardDataToBuffer1_FromDeckIndex(card_idx);

	hp_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_HP + slot));
	old_hp2 = gb_read8(wLoadedCard2HP_ADDR);
	new_hp1 = gb_read8(wLoadedCard1HP_ADDR);
	diff = (uint8_t)(new_hp1 - old_hp2);
	gb_write8(hp_addr, (uint8_t)(diff + gb_read8(hp_addr)));

	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_CHANGED_TYPE + slot)), 0);
	if (slot == 0)
		ClearAllStatusConditions();

	stage_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_STAGE + slot));
	stage = gb_read8(wLoadedCard1Stage_ADDR);
	gb_write8(stage_addr, stage);
	return (EvolveResult){stage, old_hp2, 0, slot, stage ? 0x00u : 0x80u, stage_addr};
}

/* duel.asm:962-989. a/f are always 0/$80 (the entry `xor a`, untouched
 * afterward) and omitted from CONTRACT, matching SwapTurn's precedent. */
void ClearAllStatusConditions(void)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t sub3_addr = (uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS3);
	uint16_t addr = (uint16_t)(page | DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX);

	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_STATUS), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS1), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS2), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_CHANGED_WEAKNESS), 0);
	gb_write8((uint16_t)(page | DUELVARS_ARENA_CARD_CHANGED_RESISTANCE), 0);
	gb_write8(sub3_addr, (uint8_t)(gb_read8(sub3_addr) &
				       (uint8_t)~(1u << SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F)));
	for (int i = 0; i < 8; i++)
		gb_write8((uint16_t)(addr + i), 0);
}

/* duel.asm:1058-1064. */
PutHandResult PutHandCardInPlayArea(uint8_t a, uint8_t e)
{
	uint16_t hl = (uint16_t)(((uint16_t)hWhoseTurn << 8) | a);
	uint8_t result = (uint8_t)(e | PLAY_AREA_MASK);

	RemoveCardFromHand(a);
	gb_write8(hl, result);
	return (PutHandResult){result, hl};
}

/* duel.asm:996-1049. */
PutHandPokemonResult PutHandPokemonCardInPlayArea(uint8_t a, uint8_t f)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint16_t page;
	uint8_t slot;
	uint16_t arena_addr, stage_addr;

	if (count.a >= MAX_PLAY_AREA_POKEMON) {
		/* `pop af` restores the caller's entry flags before `scf` forces C;
		 * Z (and a itself) come from the caller, not from this `cp`. */
		uint8_t exit_f = (uint8_t)((f & 0x80u) | 0x10u);
		return (PutHandPokemonResult){a, exit_f, count.hl};
	}
	gb_write8(count.hl, (uint8_t)(count.a + 1u));
	slot = count.a;
	page = (uint16_t)((uint16_t)hWhoseTurn << 8);

	(void)PutHandCardInPlayArea(a, slot);
	arena_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + slot));
	gb_write8(arena_addr, a);
	(void)LoadCardDataToBuffer2_FromDeckIndex(a);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_HP + slot)),
		 gb_read8(wLoadedCard2HP_ADDR));
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_FLAGS + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_CHANGED_TYPE + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER + slot)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_DEFENDER + slot)), 0);
	stage_addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_STAGE + slot));
	gb_write8(stage_addr, gb_read8(wLoadedCard2Stage_ADDR));
	if (slot == 0)
		ClearAllStatusConditions();
	return (PutHandPokemonResult){slot, slot ? 0x00u : 0x80u, stage_addr};
}

/* duel.asm:1091-1111. */
EmptySlotResult EmptyPlayAreaSlot(uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t last;
	uint16_t last_addr;
	uint8_t f;

	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + e)), 0xFFu);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_HP + e)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_STAGE + e)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_CHANGED_TYPE + e)), 0);
	gb_write8((uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_DEFENDER + e)), 0);
	last = (uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER + e);
	last_addr = (uint16_t)(page | last);
	gb_write8(last_addr, 0);

	f = last ? 0x00u : 0x80u;
	if ((uint8_t)(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER & 0x0Fu) + (e & 0x0Fu) > 0x0Fu)
		f |= 0x20u;
	if ((uint32_t)DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER + e > 0xFFu)
		f |= 0x10u;
	return (EmptySlotResult){last, 0, f, last_addr};
}

/* duel.asm:1068-1087. */
MoveAreaResult MovePlayAreaCardToDiscardPile(uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint16_t count_addr = (uint16_t)(page | DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t location = (uint8_t)(e | PLAY_AREA_MASK);

	(void)EmptyPlayAreaSlot(e);
	gb_write8(count_addr, (uint8_t)(gb_read8(count_addr) - 1u));
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint16_t addr = (uint16_t)(page | l);

		if (gb_read8(addr) == location)
			PutCardInDiscardPile(l);
	}
	/* EmptyPlayAreaSlot's `ld d, 0` (before its 2nd-6th writes) survives
	 * unmodified to this exit. */
	return (MoveAreaResult){DECK_SIZE, 0, 0xC0u, (uint16_t)(page | DECK_SIZE)};
}

/* duel.asm:1148-1215 / 1143-1146. */
SwapAreaResult SwapPlayAreaPokemon(uint8_t d, uint8_t e)
{
	if (e == d)
		return (SwapAreaResult){e, d, 0xC0u};

	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	static const uint8_t fields[7] = {
		DUELVARS_ARENA_CARD, DUELVARS_ARENA_CARD_HP, DUELVARS_ARENA_CARD_FLAGS,
		DUELVARS_ARENA_CARD_STAGE, DUELVARS_ARENA_CARD_CHANGED_TYPE,
		DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER, DUELVARS_ARENA_CARD_ATTACHED_DEFENDER,
	};
	uint8_t marked_d, marked_e;

	for (int i = 0; i < 7; i++) {
		uint16_t addr_e = (uint16_t)(page | (uint8_t)(fields[i] + e));
		uint16_t addr_d = (uint16_t)(page | (uint8_t)(fields[i] + d));
		uint8_t tmp = gb_read8(addr_d);

		gb_write8(addr_d, gb_read8(addr_e));
		gb_write8(addr_e, tmp);
	}
	marked_d = (uint8_t)(d | PLAY_AREA_MASK);
	marked_e = (uint8_t)(e | PLAY_AREA_MASK);
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint16_t addr = (uint16_t)(page | l);
		uint8_t loc = gb_read8(addr);

		if (loc == marked_e)
			gb_write8(addr, marked_d);
		else if (loc == marked_d)
			gb_write8(addr, marked_e);
	}
	return (SwapAreaResult){DECK_SIZE, d, 0xC0u};
}

SwapAreaResult SwapArenaWithBenchPokemon(uint8_t e)
{
	ClearAllStatusConditions();
	return SwapPlayAreaPokemon(PLAY_AREA_ARENA, e);
}

/* duel.asm:1122-1137. */
ShiftResult ShiftTurnPokemonToFirstPlayAreaSlots(void)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t write_slot = PLAY_AREA_ARENA;
	uint16_t hl;

	for (uint8_t scan_slot = PLAY_AREA_ARENA; scan_slot < MAX_PLAY_AREA_POKEMON; scan_slot++) {
		uint16_t addr = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + scan_slot));

		if (!(gb_read8(addr) & 0x80u)) {
			(void)SwapPlayAreaPokemon(scan_slot, write_slot);
			write_slot++;
		}
	}
	hl = (uint16_t)(page | (uint8_t)(DUELVARS_ARENA_CARD + MAX_PLAY_AREA_POKEMON));
	return (ShiftResult){MAX_PLAY_AREA_POKEMON, MAX_PLAY_AREA_POKEMON, write_slot, 0xC0u, hl};
}

/* duel.asm:1114-1119. */
ShiftResult ShiftAllPokemonToFirstPlayAreaSlots(void)
{
	ShiftResult r;

	(void)ShiftTurnPokemonToFirstPlayAreaSlots();
	SwapTurn();
	r = ShiftTurnPokemonToFirstPlayAreaSlots();
	SwapTurn();
	return r;
}

/* duel.asm:1221-1284. */
EnergiesResult GetPlayAreaCardAttachedEnergies(uint8_t e)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t location = (uint8_t)(PLAY_AREA_MASK | e);
	uint8_t sum;

	for (uint8_t t = 0; t < NUM_TYPES; t++)
		gb_write8((uint16_t)(wAttachedEnergies_ADDR + t), 0);
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint8_t type, color;
		uint16_t addr;

		if (gb_read8((uint16_t)(page | l)) != location)
			continue;
		(void)LoadCardDataToBuffer2_FromDeckIndex(l);
		type = gb_read8(wLoadedCard2Type_ADDR);
		if (!(type & (1u << TYPE_ENERGY_F)))
			continue;
		color = (uint8_t)(type & TYPE_PKMN);
		addr = (uint16_t)(wAttachedEnergies_ADDR + color);
		gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
		if (color == COLORLESS)
			gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
	}
	sum = 0;
	for (uint8_t t = 0; t < NUM_TYPES; t++)
		sum = (uint8_t)(sum + gb_read8((uint16_t)(wAttachedEnergies_ADDR + t)));
	gb_write8(wTotalAttachedEnergies_ADDR, sum);
	return (EnergiesResult){sum, 0xC0u};
}

/* duel.asm:1442-1467. */
AttackCopyResult CopyAttackDataAndDamage(uint8_t e)
{
	uint8_t card_id = gb_read8(wLoadedCard1ID_ADDR);
	uint16_t src = (e == 1) ? wLoadedCard1Atk2_ADDR : wLoadedCard1Atk1_ADDR;
	uint16_t dst = wLoadedAttack_ADDR;
	uint8_t damage;

	gb_write8(wTempCardID_ccc2_ADDR, card_id);
	for (uint8_t i = 0; i < ATTACK_DATA_LEN; i++)
		gb_write8(dst++, gb_read8(src++));
	damage = gb_read8(wLoadedAttackDamage_ADDR);
	gb_write8(wDamage_ADDR, damage);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), 0);
	gb_write8(wNoDamageOrEffect_ADDR, 0);
	gb_write8(wDealtDamage_ADDR, 0);
	gb_write8((uint16_t)(wDealtDamage_ADDR + 1u), 0);
	return (AttackCopyResult){0, 0, 0x80u, (uint16_t)(wDealtDamage_ADDR + 1u), dst};
}

/* duel.asm:1434-1440. */
AttackCopyResult CopyAttackDataAndDamage_FromDeckIndex(uint8_t d, uint8_t e)
{
	gb_write8(wSelectedAttack_ADDR, e);
	hTempCardIndex_ff9f = d;
	(void)LoadCardDataToBuffer1_FromDeckIndex(d);
	return CopyAttackDataAndDamage(e);
}

/* duel.asm:1415-1427. */
AttackCopyResult CopyAttackDataAndDamage_FromCardID(uint8_t a, uint8_t d, uint8_t e)
{
	gb_write8(wSelectedAttack_ADDR, e);
	hTempCardIndex_ff9f = d;
	LoadCardDataToBuffer1_FromCardID(a);
	return CopyAttackDataAndDamage(e);
}

/* duel.asm:1621-1623. `scf` sets C, clears N/H, leaves Z untouched. */
uint8_t ReturnCarry(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}

/* duel.asm:1793-1803. f omitted: its last flag-setting instruction is inside
 * the opaque LoadCardDataToBuffer1_FromDeckIndex call. */
LoadEffectResult LoadNonPokemonCardEffectCommands(void)
{
	uint8_t idx = hTempCardIndex_ff9f;
	uint8_t b0, b1;

	(void)LoadCardDataToBuffer1_FromDeckIndex(idx);
	b0 = gb_read8(wLoadedCard1EffectCommands_ADDR);
	b1 = gb_read8((uint16_t)(wLoadedCard1EffectCommands_ADDR + 1u));
	gb_write8(wLoadedAttackEffectCommands_ADDR, b0);
	gb_write8((uint16_t)(wLoadedAttackEffectCommands_ADDR + 1u), b1);
	return (LoadEffectResult){b1, (uint16_t)(wLoadedCard1EffectCommands_ADDR + 1u),
				  (uint16_t)(wLoadedAttackEffectCommands_ADDR + 1u)};
}

/* duel.asm:1976-1988 / 1991-2006. a/f flow through the opaque HtimesL leaf and
 * are omitted. */
PowerModifierResult ApplyAttachedPlusPower(uint8_t b, uint16_t de)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t count = CountCardIDInLocation(b, PLUSPOWER, page).a;
	uint16_t sum = (uint16_t)(de + (uint16_t)(count * 10u));

	return (PowerModifierResult){sum, sum};
}

PowerModifierResult ApplyAttachedDefender(uint8_t b, uint16_t de)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t count = CountCardIDInLocation(b, DEFENDER, page).a;
	uint16_t product = (uint16_t)(count * 20u);

	return (PowerModifierResult){product, (uint16_t)(de - product)};
}

/* duel.asm:2273-2298. Exit d/e are genuine unpredictable loop residue
 * (clobbered by GetCardIDFromDeckIndex on every match) and omitted. */
DiscardIfInPlayResult MoveCardToDiscardPileIfInPlayArea(uint16_t de, uint8_t page)
{
	uint8_t c = (uint8_t)de;
	uint8_t b = (uint8_t)(de >> 8);

	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		uint16_t loc_addr = (uint16_t)(((uint16_t)page << 8) | l);
		uint16_t id;

		if (!(gb_read8(loc_addr) & PLAY_AREA_MASK))
			continue;
		id = GetCardIDFromDeckIndex(l);
		if ((uint8_t)id != c)
			continue;
		if ((uint8_t)(id >> 8) != b)
			continue;
		PutCardInDiscardPile(l);
	}
	return (DiscardIfInPlayResult){DECK_SIZE, b, c, 0xC0u,
				       (uint16_t)(((uint16_t)page << 8) | DECK_SIZE)};
}

#define CARD_LOCATION_ARENA 0x10u
#define WEAKNESS  (1u << 1)
#define RESISTANCE (1u << 2)

uint16_t ApplyDamageModifiers_DamageToTarget(void)
{
	gb_write8(wDamageEffectiveness_ADDR, 0);

	uint8_t lo = gb_read8(wDamage_ADDR);
	uint8_t hi_byte = gb_read8((uint16_t)(wDamage_ADDR + 1u));
	if (!(hi_byte | lo))
		return 0;

	hTempPlayAreaLocation_ff9d = 0;
	uint16_t de = (uint16_t)((uint16_t)hi_byte << 8 | lo);

	if (hi_byte & 0x80u) {
		de &= (uint16_t)~0x8000u;
		gb_write8(wDamageEffectiveness_ADDR, 0);
		de = HandleDoubleDamageSubstatus(de);
	} else {
		de = HandleDoubleDamageSubstatus(de);
		if (!de)
			return 0;

		uint8_t color = GetPlayAreaCardColor(hTempPlayAreaLocation_ff9d);
		uint8_t wr = TranslateColorToWR(color);

		SwapTurn();
		uint8_t weakness = GetArenaCardWeakness();
		SwapTurn();
		if (weakness & wr) {
			de <<= 1;
			gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | WEAKNESS));
		}

		SwapTurn();
		uint8_t resistance = GetArenaCardResistance();
		SwapTurn();
		if (resistance & wr) {
			de = (uint16_t)(de - 30u);
			gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | RESISTANCE));
		}
	}

	{
		PowerModifierResult r = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	SwapTurn();
	{
		PowerModifierResult r = ApplyAttachedDefender(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	de = HandleDamageReduction(de);
	if (de & 0x8000u)
		de = 0;
	SwapTurn();
	return de;
}

uint16_t ApplyDamageModifiers_DamageToSelf(void)
{
	gb_write8(wDamageEffectiveness_ADDR, 0);

	uint8_t lo = gb_read8(wDamage_ADDR);
	uint8_t hi_byte = gb_read8((uint16_t)(wDamage_ADDR + 1u));
	uint8_t nonzero = (uint8_t)(hi_byte | lo);
	if (!nonzero)
		return 0;

	uint16_t de = (uint16_t)((uint16_t)hi_byte << 8 | lo);
	uint8_t color = GetArenaCardColor();
	uint8_t wr = TranslateColorToWR(color);

	uint8_t weakness = GetArenaCardWeakness();
	if (weakness & wr) {
		de <<= 1;
		gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | WEAKNESS));
	}
	uint8_t resistance = GetArenaCardResistance();
	if (resistance & wr) {
		de = (uint16_t)(de - 30u);
		gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | RESISTANCE));
	}

	{
		PowerModifierResult r = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	{
		PowerModifierResult r = ApplyAttachedDefender(CARD_LOCATION_ARENA, de);
		de = r.de;
	}


	if (de & 0x8000u)
		return 0;
	return de;
}
uint8_t GetPlayAreaCardRetreatCost(void)
{
	uint8_t slot = hTempPlayAreaLocation_ff9d;
	uint8_t deck_idx = GetTurnDuelistVariable((uint8_t)(slot + 0xBBu)).a;
	LoadCardDataToBuffer1_FromDeckIndex(deck_idx);
	return GetLoadedCard1RetreatCost();
}

#define WAS_KNOCKED_OUT_TEXT 0x0081u

uint8_t DrawWideTextBox_WaitForInput_ReturnCarry(uint16_t hl)
{
	DrawWideTextBox_WaitForInput(hl);
	return 0x10u;
}

uint8_t PrintKnockedOut(void)
{
	uint8_t card_id = wTempNonTurnDuelistCardID;
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	DrawWideTextBox_PrintText(WAS_KNOCKED_OUT_TEXT);
	DoAFrames(40);
	return 0x10u;
}
KnockoutCheckResult PrintPlayAreaCardKnockedOutIfNoHP(uint8_t a)
{
	uint8_t e_val = a;
	uint8_t hp = GetTurnDuelistVariable((uint8_t)(a + DUELVARS_ARENA_CARD_HP)).a;
	if (hp)
		return (KnockoutCheckResult){hp, 0x00u};
	uint8_t saved = wTempNonTurnDuelistCardID;
	uint8_t deck_idx = GetTurnDuelistVariable((uint8_t)(e_val + DUELVARS_ARENA_CARD)).a;
	LoadCardDataToBuffer1_FromDeckIndex(deck_idx);
	wTempNonTurnDuelistCardID = wLoadedCard1ID;
	PrintKnockedOut();
	wTempNonTurnDuelistCardID = saved;
	return (KnockoutCheckResult){saved, 0x10u};
}
