/* >>> part includes */
#include "home/duel_core_state.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel.h"
/* <<< part includes */

/* >>> part DUELVARS_PRIZE_CARDS */
#define DUELVARS_PRIZE_CARDS 0x3cu
/* <<< part DUELVARS_PRIZE_CARDS */
/* >>> part DUELVARS_PRIZES */
#define DUELVARS_PRIZES 0xecu
/* <<< part DUELVARS_PRIZES */
/* >>> part DUELVARS_ARENA_CARD */
#define DUELVARS_ARENA_CARD 0xbbu
/* <<< part DUELVARS_ARENA_CARD */
/* >>> part DUELVARS_ARENA_CARD_HP */
#define DUELVARS_ARENA_CARD_HP 0xc8u
/* <<< part DUELVARS_ARENA_CARD_HP */
/* >>> part DUELVARS_ARENA_CARD_FLAGS */
#define DUELVARS_ARENA_CARD_FLAGS 0xc2u
/* <<< part DUELVARS_ARENA_CARD_FLAGS */
/* >>> part DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA */
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
/* <<< part DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA */

/* >>> part duelvar_addr */
static uint16_t duelvar_addr(uint8_t offset)
{
	return (uint16_t)(((uint16_t)hWhoseTurn << 8) | offset);
}
/* <<< part duelvar_addr */

/* >>> factory InitVariablesToBeginTurn */
DuelCoreStateResult InitVariablesToBeginTurn(void)
{
	wAlreadyPlayedEnergy = 0;
	wConfusionRetreatCheckWasUnsuccessful = 0;
	wGotHeadsFromSandAttackOrSmokescreenCheck = 0;
	wWhoseTurn = hWhoseTurn;
	return (DuelCoreStateResult){hWhoseTurn, 0, 0, 0, 0x80};
}
/* <<< factory InitVariablesToBeginTurn */

/* >>> factory SetAllPlayAreaPokemonCanEvolve */
DuelCoreStateResult SetAllPlayAreaPokemonCanEvolve(void)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint16_t flags = duelvar_addr(DUELVARS_ARENA_CARD_FLAGS);
	uint8_t a = count;
	do {
		uint8_t flags_value = gb_read8(flags);
		flags_value &= (uint8_t)~USED_PKMN_POWER_THIS_TURN;
		flags_value |= CAN_EVOLVE_THIS_TURN;
		gb_write8(flags, flags_value);
		flags = (uint16_t)((flags & 0xff00u) | (uint8_t)(flags + 1u));
		count--;
	} while (count != 0);
	return (DuelCoreStateResult){a, 0, count, flags, 0x80};
}
/* <<< factory SetAllPlayAreaPokemonCanEvolve */

/* >>> factory InitializeDuelVariables */
DuelCoreStateWideResult InitializeDuelVariables(void)
{
	uint8_t page = hWhoseTurn;
	uint16_t type_addr = (uint16_t)(((uint16_t)page << 8) | 0xf1);
	uint8_t type = gb_read8(type_addr);
	for (uint16_t i = 0; i != 0x100; i++)
		gb_write8((uint16_t)(((uint16_t)page << 8) | i), 0);
	gb_write8(type_addr, type);
	uint8_t b = 0;
	uint8_t c = 60;
	uint8_t deck_index = 0x7e;
	do {
		gb_write8((uint16_t)(((uint16_t)page << 8) | deck_index), b);
		gb_write8((uint16_t)(((uint16_t)page << 8) | b), 0);
		deck_index++;
		b++;
		c--;
	} while (c != 0);
	c = 7;
	uint8_t l = DUELVARS_ARENA_CARD;
	do {
		gb_write8((uint16_t)(((uint16_t)page << 8) | l), 0xff);
		l++;
		c--;
	} while (c != 0);
	return (DuelCoreStateWideResult){type, b, c, 0, 0,
		(uint16_t)(((uint16_t)page << 8) | l), 0x80};
}
/* <<< factory InitializeDuelVariables */

/* >>> factory InitTurnDuelistPrizes */
DuelCoreStateWideResult InitTurnDuelistPrizes(void)
{
	uint8_t page = hWhoseTurn;
	uint8_t count = wDuelInitialPrizes;
	uint8_t b = 0;
	uint8_t e = DUELVARS_PRIZE_CARDS;
	uint8_t a;
	do {
		DrawCardResult draw = DrawCardFromDeck();
		a = draw.a;
		gb_write8((uint16_t)(((uint16_t)page << 8) | e), a);
		e++;
		gb_write8((uint16_t)(((uint16_t)page << 8) | a), CARD_LOCATION_PRIZE);
		b++;
	} while (b != count);
	static const uint8_t prize_masks[] = {0, 1, 3, 7, 15, 31, 63};
	a = prize_masks[count <= 6 ? count : 6];
	gb_write8((uint16_t)(((uint16_t)page << 8) | DUELVARS_PRIZES), a);
	return (DuelCoreStateWideResult){a, b, count, 0, count,
		(uint16_t)(((uint16_t)page << 8) | DUELVARS_PRIZES), 0x80};
}
/* <<< factory InitTurnDuelistPrizes */

/* >>> factory TakeAPrizes */
DuelCoreStateResult TakeAPrizes(uint8_t a)
{
	if (a == 0)
		return (DuelCoreStateResult){0, 0, 0, 0, 0x80};
	uint8_t c = a;
	uint8_t available = CountPrizes();
	uint8_t remaining = available;
	if (remaining < c)
		remaining = 0;
	else
		remaining = (uint8_t)(remaining - c);
	static const uint8_t prize_masks[] = {0, 1, 3, 7, 15, 31, 63};
	uint8_t mask = prize_masks[remaining <= 6 ? remaining : 6];
	DuelistVarResult prizes = GetTurnDuelistVariable(DUELVARS_PRIZES);
	gb_write8(prizes.hl, mask);
	return (DuelCoreStateResult){prizes.a, mask, remaining, prizes.hl, 0};
}
/* <<< factory TakeAPrizes */

/* >>> factory CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut */
DuelCoreStateResult CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut(void)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint16_t hp = duelvar_addr(DUELVARS_ARENA_CARD_HP);
	uint8_t a;
	do {
		a = gb_read8(hp);
		hp++;
		if (a != 0)
			return (DuelCoreStateResult){a, 0, count, hp, 0};
		count--;
	} while (count != 0);
	return (DuelCoreStateResult){0, 0, count, hp, 0x90};
}
/* <<< factory CheckIfTurnDuelistPlayAreaPokemonAreAllKnockedOut */

/* >>> factory CountKnockedOutPokemon */
DuelCoreStateWideResult CountKnockedOutPokemon(void)
{
	uint16_t hp = duelvar_addr(DUELVARS_ARENA_CARD_HP);
	uint16_t cards = duelvar_addr(DUELVARS_ARENA_CARD);
	uint8_t b = 0;
	uint8_t c = 6;
	uint8_t d = hWhoseTurn;
	uint8_t e = DUELVARS_ARENA_CARD;
	do {
		uint8_t index = gb_read8(cards);
		if (index != 0xff && gb_read8(hp) == 0) {
			uint8_t id = GetCardIDFromDeckIndex(index);
			if (GetCardType(id) != TYPE_TRAINER)
				b++;
		}
		hp++;
		cards++;
		e++;
		c--;
	} while (c != 0);
	wNumberPrizeCardsToTake = b;
	return (DuelCoreStateWideResult){b, b, c, d, e, hp, b == 0 ? 0x80 : 0x10};
}
/* <<< factory CountKnockedOutPokemon */
