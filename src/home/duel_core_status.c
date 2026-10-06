#include "home/duel_core_status.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "mem.h"

#define DUELVARS_ARENA_CARD_ATTACHED_DEFENDER 0xdau
#define DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER 0xe0u
#define DUELVARS_ARENA_CARD_STATUS 0xf0u

DuelCoreStatusResult IsArenaPokemonAsleepOrPoisoned(void)
{
	DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	uint8_t value = status.a;
	uint8_t low;

	if (value == 0)
		return (DuelCoreStatusResult){0, status.hl, 0x80u};
	value &= (POISONED | DOUBLE_POISONED);
	if (value != 0)
		return (DuelCoreStatusResult){value, status.hl, 0x10u};
	low = gb_read8(status.hl) & CNF_SLP_PRZ;
	if (low == ASLEEP)
		return (DuelCoreStatusResult){low, status.hl, 0x90u};
	return (DuelCoreStatusResult){low, status.hl, low == 0 ? 0x80u : 0x00u};
}

static DuelCoreStatusDiscardResult discard_attached(uint8_t offset, uint8_t card)
{
	DuelistVarResult attached = GetTurnDuelistVariable(offset);
	uint16_t page = (uint16_t)(attached.hl >> 8);
	DuelCoreStatusDiscardResult result;

	for (uint8_t i = 0; i < MAX_PLAY_AREA_POKEMON; i++)
		gb_write8((uint16_t)(attached.hl + i), 0);
	{
		DiscardIfInPlayResult moved = MoveCardToDiscardPileIfInPlayArea(card, (uint8_t)page);
		result.a = moved.a;
		result.b = moved.b;
		result.c = moved.c;
		result.hl = moved.hl;
		result.f = moved.f;
	}
	return result;
}

DuelCoreStatusDiscardResult DiscardAttachedPlusPowers(void)
{
	return discard_attached(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER, PLUSPOWER);
}

DuelCoreStatusDiscardResult DiscardAttachedDefenders(void)
{
	return discard_attached(DUELVARS_ARENA_CARD_ATTACHED_DEFENDER, DEFENDER);
}
