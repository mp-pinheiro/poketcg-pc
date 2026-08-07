#include "home/card_color.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "mem.h"

/* card_color.asm's duel-variable and deck-index helpers (duel.asm:1316, 762) reduce to
 * WRAM reads keyed by hWhoseTurn. ConvertSpecialTrainerCardToPokemon is a no-op for the
 * pokemon cards these routines query, so LoadCardDataToBuffer2_FromCardID alone matches. */
#define PLAYER_TURN                       ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))
#define DUELVARS_ARENA_CARD               0xBBu
#define DUELVARS_ARENA_CARD_CHANGED_WEAKNESS   0xE9u
#define DUELVARS_ARENA_CARD_CHANGED_RESISTANCE 0xEAu

static uint8_t turn_duel_var(uint8_t off)
{
	return gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) + off));
}

static uint8_t deck_card_id(uint8_t idx)
{
	uint16_t base = (hWhoseTurn == PLAYER_TURN) ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	return gb_read8((uint16_t)(base + idx));
}

static uint8_t card_weakness_of(uint8_t duelvar_off)
{
	uint8_t idx = turn_duel_var(duelvar_off);
	LoadCardDataToBuffer2_FromCardID(deck_card_id(idx));
	return wLoadedCard2Weakness;
}

static uint8_t card_resistance_of(uint8_t duelvar_off)
{
	uint8_t idx = turn_duel_var(duelvar_off);
	LoadCardDataToBuffer2_FromCardID(deck_card_id(idx));
	return wLoadedCard2Resistance;
}

uint8_t GetCardWeakness(uint8_t a)
{
	return card_weakness_of(a);
}

/* card_color.asm:52-64 */
uint8_t GetArenaCardWeakness(void)
{
	uint8_t changed = turn_duel_var(DUELVARS_ARENA_CARD_CHANGED_WEAKNESS);
	if (changed != 0)
		return changed;
	return card_weakness_of(DUELVARS_ARENA_CARD);
}

/* card_color.asm:44-48 */
uint8_t GetPlayAreaCardWeakness(uint8_t a)
{
	if (a == 0)
		return GetArenaCardWeakness();
	return card_weakness_of((uint8_t)(a + DUELVARS_ARENA_CARD));
}

uint8_t GetCardResistance(uint8_t a)
{
	return card_resistance_of(a);
}

/* card_color.asm:77-89 */
uint8_t GetArenaCardResistance(void)
{
	uint8_t changed = turn_duel_var(DUELVARS_ARENA_CARD_CHANGED_RESISTANCE);
	if (changed != 0)
		return changed;
	return card_resistance_of(DUELVARS_ARENA_CARD);
}

/* card_color.asm:69-73 */
uint8_t GetPlayAreaCardResistance(uint8_t a)
{
	if (a == 0)
		return GetArenaCardResistance();
	return card_resistance_of((uint8_t)(a + DUELVARS_ARENA_CARD));
}
