/* >>> part includes */
#include "home/damage_calculation.h"
#include "home/card_id_bus.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_color.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "home/substatus.h"

#include <stdint.h>
/* <<< part includes */
/* >>> part load_attacker_and_defender */
static void load_attacker_and_defender(uint8_t location)
{
	uint8_t index;
	CardId id;
	uint16_t temp;

	index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
	LoadCardDataToBuffer2_FromDeckIndex(index);
	id = card_id_read_at(wLoadedCard2ID_ADDR);
	temp = wTempTurnDuelistCardID_ADDR;
	card_id_write(&temp, id);
	SwapTurn();
	index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	LoadCardDataToBuffer2_FromDeckIndex(index);
	id = card_id_read_at(wLoadedCard2ID_ADDR);
	temp = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp, id);
	SwapTurn();
}
/* <<< part load_attacker_and_defender */
/* >>> part calculate_from_one */
static uint16_t calculate_from_one(uint16_t damage)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	uint8_t b;
	uint8_t status;

	SwapTurn();
	{
		uint8_t index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
		LoadCardDataToBuffer2_FromDeckIndex(index);
		CardId id = card_id_read_at(wLoadedCard2ID_ADDR);
		uint16_t temp = wTempTurnDuelistCardID_ADDR;
		card_id_write(&temp, id);
	}
	SwapTurn();
	{
		uint8_t index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
		LoadCardDataToBuffer2_FromDeckIndex(index);
		CardId id = card_id_read_at(wLoadedCard2ID_ADDR);
		uint16_t temp = wTempNonTurnDuelistCardID_ADDR;
		card_id_write(&temp, id);
	}
    /* damage_calculation.asm:347-407. The weakness and resistance checks both
     * run on the defending side (no swap between them), and an attack flagged
     * UNAFFECTED_BY_WEAKNESS_RESISTANCE skips them; PlusPower is the
     * attacker's, Defender the defender's. */
    SwapTurn();
    damage = HandleDoubleDamageSubstatus(damage);
    if (damage & (1u << (UNAFFECTED_BY_WEAKNESS_RESISTANCE_F + 8u))) {
        damage = (uint16_t)(damage & ~(uint16_t)(1u << (UNAFFECTED_BY_WEAKNESS_RESISTANCE_F + 8u)));
    } else {
        b = TranslateColorToWR(GetArenaCardColor());
        SwapTurn();
        /* damage_calculation.asm .unchanged_weak/.unchanged_res: an arena card
         * with a changed weakness or resistance uses that value, not its own. */
        uint8_t weakness = location == 0u ? GetTurnDuelistVariable(DUELVARS_ARENA_CARD_CHANGED_WEAKNESS).a : 0u;
        if (weakness == 0u) {
            uint8_t index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
            LoadCardDataToBuffer2_FromDeckIndex(index);
            weakness = wLoadedCard2Weakness;
        }
        if (weakness & b)
            damage = (uint16_t)(damage << 1);
        uint8_t resistance = location == 0u ? GetTurnDuelistVariable(DUELVARS_ARENA_CARD_CHANGED_RESISTANCE).a : 0u;
        if (resistance == 0u) {
            uint8_t index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
            LoadCardDataToBuffer2_FromDeckIndex(index);
            resistance = wLoadedCard2Resistance;
        }
        if (resistance & b)
            damage = (uint16_t)(damage - 30u);
        SwapTurn();
    }
    {
        PowerModifierResult r = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, damage);
        damage = r.de;
    }
    SwapTurn();
    {
        PowerModifierResult r = ApplyAttachedDefender((uint8_t)(location + CARD_LOCATION_ARENA), damage);
        damage = r.de;
    }
    if (location == 0)
        damage = HandleDamageReduction(damage);
    if (damage & 0x8000u)
        damage = 0;
    if (location == 0) {
        status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
        if (status & DOUBLE_POISONED)
            damage = (uint16_t)(damage + ((status & (DOUBLE_POISONED & (POISONED ^ 0xFFu))) ? 40u : 20u));
    }
    return damage;
}
/* <<< part calculate_from_one */
/* === factory CalculateDamage_FromDefendingPokemon */
/* === factory CalculateDamage_VersusDefendingPokemon */
