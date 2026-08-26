#include "home/damage_calculation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_color.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "home/substatus.h"

#include <stdint.h>

#define DUELVARS_ARENA_CARD 0xBBu
#define DUELVARS_ARENA_CARD_CHANGED_WEAKNESS 0xE9u
#define DUELVARS_ARENA_CARD_CHANGED_RESISTANCE 0xEAu
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define CARD_LOCATION_ARENA 0x10u
#define UNAFFECTED_BY_WEAKNESS_RESISTANCE_F 7u
#define POISONED 0x80u
#define DOUBLE_POISONED 0xC0u
#define DUELVARS_ARENA_CARD_SUBSTATUS1 0xE7u
#define DUELVARS_ARENA_CARD_SUBSTATUS2 0xE8u
#define POKEMON_POWER 0x04u
#define EFFECTCMDTYPE_AI 0x09u


static DamageCalculationResult finish_damage(uint16_t out, uint16_t value)
{
    uint8_t a;
    uint8_t f;

    gb_write8(out, (uint8_t)value);
    if ((value >> 8) != 0) {
        a = 0xFFu;
        f = 0x00u;
        gb_write8(out, a);
    } else {
        a = 0;
        f = 0x80u;
    }
    return (DamageCalculationResult){a, f, (uint8_t)(value >> 8), (uint8_t)value, out};
}

static void load_attacker_and_defender(uint8_t location)
{
    uint8_t index;
    uint8_t id;

    index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
    id = LoadCardDataToBuffer2_FromDeckIndex(index);
    wTempTurnDuelistCardID = id;
    SwapTurn();
    index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
    id = LoadCardDataToBuffer2_FromDeckIndex(index);
    wTempNonTurnDuelistCardID = id;
    SwapTurn();
}

static uint16_t calculate_versus_one(uint16_t damage)
{
    NoDamageOrEffectResult blocked;
    uint8_t location = hTempPlayAreaLocation_ff9d;
    uint8_t b;
    uint8_t status;

    load_attacker_and_defender(location);
    blocked = HandleNoDamageOrEffectSubstatus((uint8_t)damage, 0);
    if (!(blocked.f & 0x10u)) {
        if (location == 0)
            damage = HandleDoubleDamageSubstatus(damage);
        if (!(damage & (1u << UNAFFECTED_BY_WEAKNESS_RESISTANCE_F))) {
            b = TranslateColorToWR(GetPlayAreaCardColor(location));
            SwapTurn();
            if (GetArenaCardWeakness() & b)
                damage = (uint16_t)(damage << 1);
            SwapTurn();
            if (GetArenaCardResistance() & b)
                damage = (uint16_t)(damage - 30u);
        }
        {
            PowerModifierResult r = ApplyAttachedPlusPower((uint8_t)(location + CARD_LOCATION_ARENA), damage);
            damage = r.de;
        }
        SwapTurn();
        {
            PowerModifierResult r = ApplyAttachedDefender(CARD_LOCATION_ARENA, damage);
            damage = r.de;
        }
        damage = HandleDamageReduction(damage);
        if (damage & 0x8000u)
            damage = 0;
        status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
        if (status & DOUBLE_POISONED)
            damage = (uint16_t)(damage + ((status & (DOUBLE_POISONED & (POISONED ^ 0xFFu))) ? 20u : 10u));
        SwapTurn();
    } else {
        damage = 0;
    }
    return damage;
}
static uint16_t calculate_from_one(uint16_t damage)
{
    uint8_t location = hTempPlayAreaLocation_ff9d;
    uint8_t b;
    uint8_t status;
    uint8_t changed;

    SwapTurn();
    {
        uint8_t index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
        wTempTurnDuelistCardID = LoadCardDataToBuffer2_FromDeckIndex(index);
    }
    SwapTurn();
    {
        uint8_t index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
        wTempNonTurnDuelistCardID = LoadCardDataToBuffer2_FromDeckIndex(index);
    }
    SwapTurn();
    damage = HandleDoubleDamageSubstatus(damage);
    b = TranslateColorToWR(GetArenaCardColor());
    SwapTurn();
    changed = location == 0 ? GetTurnDuelistVariable(DUELVARS_ARENA_CARD_CHANGED_WEAKNESS).a : 0;
    if (location != 0 || changed == 0) {
        uint8_t index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
        LoadCardDataToBuffer2_FromDeckIndex(index);
    }
    if (wLoadedCard2Weakness & b)
        damage = (uint16_t)(damage << 1);
    SwapTurn();
    changed = location == 0 ? GetTurnDuelistVariable(DUELVARS_ARENA_CARD_CHANGED_RESISTANCE).a : 0;
    if (location != 0 || changed == 0) {
        uint8_t index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
        LoadCardDataToBuffer2_FromDeckIndex(index);
    }
    if (wLoadedCard2Resistance & b)
        damage = (uint16_t)(damage - 30u);
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

DamageCalculationResult CalculateDamage_VersusDefendingPokemon(void)
{
    DamageCalculationResult result;
    result = finish_damage(wAIMinDamage_ADDR, calculate_versus_one(wAIMinDamage));
    result = finish_damage(wAIMaxDamage_ADDR, calculate_versus_one(wAIMaxDamage));
    result = finish_damage(wDamage_ADDR, calculate_versus_one(wDamage));
    return result;
}

DamageCalculationResult CalculateDamage_FromDefendingPokemon(void)
{
    DamageCalculationResult result;
    result = finish_damage(wAIMinDamage_ADDR, calculate_from_one(wAIMinDamage));
    result = finish_damage(wAIMaxDamage_ADDR, calculate_from_one(wAIMaxDamage));
    result = finish_damage(wDamage_ADDR, calculate_from_one(wDamage));
    return result;
}

/* >>> factory EstimateDamage_VersusDefendingCard */
/* damage_calculation.asm:6-84. Stores the estimated damage against the defending
 * Pokemon in wDamage/wAIMinDamage/wAIMaxDamage. A Pokemon Power zeroes all three
 * and returns d=e=0. Otherwise the attack's damage seeds the AI min/max, the
 * card's own EFFECTCMDTYPE_AI command may adjust them, and the calculation runs --
 * directly when the attacker is already active, otherwise with substatus1,
 * substatus2 and changed-resistance temporarily zeroed and then restored.
 * `ld l, DUELVARS_*` only replaces hl's low byte, so all three live on the page
 * GetTurnDuelistVariable returned. */
DamageCalculationResult EstimateDamage_VersusDefendingCard(uint8_t a)
{
	const uint8_t e_in = a;
	gb_write8(wSelectedAttack_ADDR, a);
	uint8_t location = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	DuelistVarResult arena =
		GetTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD));
	(void)CopyAttackDataAndDamage_FromDeckIndex(arena.a, e_in);

	if (gb_read8(wLoadedAttackCategory_ADDR) == POKEMON_POWER) {
		gb_write8(wDamage_ADDR, 0u);
		gb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);
		gb_write8(wAIMinDamage_ADDR, 0u);
		gb_write8(wAIMaxDamage_ADDR, 0u);
		return (DamageCalculationResult){0u, 0x80u, 0u, 0u,
			(uint16_t)(wDamage_ADDR + 1u)};
	}

	/* .is_attack */
	uint8_t damage = gb_read8(wDamage_ADDR);
	gb_write8(wAIMinDamage_ADDR, damage);
	gb_write8(wAIMaxDamage_ADDR, damage);
	(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI, 0u, 0u, 0u);
	if ((gb_read8(wAIMinDamage_ADDR) | gb_read8(wAIMaxDamage_ADDR)) == 0u) {
		damage = gb_read8(wDamage_ADDR);
		gb_write8(wAIMinDamage_ADDR, damage);
		gb_write8(wAIMaxDamage_ADDR, damage);
	}

	/* .calculation */
	if (gb_read8(hTempPlayAreaLocation_ff9d_ADDR) == 0u)
		return CalculateDamage_VersusDefendingPokemon();

	const uint16_t page = (uint16_t)(arena.hl & 0xFF00u);
	const uint16_t sub1 = (uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS1);
	const uint16_t sub2 = (uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS2);
	const uint16_t resist = (uint16_t)(page | DUELVARS_ARENA_CARD_CHANGED_RESISTANCE);
	DuelistVarResult saved1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	const uint8_t v1 = saved1.a;
	gb_write8(sub1, 0u);
	const uint8_t v2 = gb_read8(sub2);
	gb_write8(sub2, 0u);
	const uint8_t v3 = gb_read8(resist);
	gb_write8(resist, 0u);

	(void)CalculateDamage_VersusDefendingPokemon();

	gb_write8(resist, v3);
	gb_write8(sub2, v2);
	gb_write8(sub1, v1);
	return (DamageCalculationResult){v1, 0x00u, 0u, 0u, sub1};
}
/* <<< factory EstimateDamage_VersusDefendingCard */

/* >>> factory EstimateDamage_FromDefendingPokemon */
/* damage_calculation.asm:217-303. The mirror of the routine above: damage dealt
 * BY the defending Pokemon to the card at hTempPlayAreaLocation_ff9d. The attack
 * data is copied under SwapTurn (so it is the opponent's arena card), and the
 * EFFECTCMDTYPE_AI command likewise runs swapped with the location forced to
 * PLAY_AREA_ARENA and restored afterwards. `ld l, DUELVARS_*` replaces only hl's
 * low byte, so the substatus addresses stay on GetTurnDuelistVariable's page. */
DamageCalculationResult EstimateDamage_FromDefendingPokemon(uint8_t a)
{
	const uint8_t e_in = a;
	SwapTurn();
	gb_write8(wSelectedAttack_ADDR, a);
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	(void)CopyAttackDataAndDamage_FromDeckIndex(arena.a, e_in);
	SwapTurn();

	if (gb_read8(wLoadedAttackCategory_ADDR) == POKEMON_POWER) {
		gb_write8(wDamage_ADDR, 0u);
		gb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);
		gb_write8(wAIMinDamage_ADDR, 0u);
		gb_write8(wAIMaxDamage_ADDR, 0u);
		return (DamageCalculationResult){0u, 0x80u, 0u, 0u,
			(uint16_t)(wDamage_ADDR + 1u)};
	}

	/* .is_attack */
	uint8_t damage = gb_read8(wDamage_ADDR);
	gb_write8(wAIMinDamage_ADDR, damage);
	gb_write8(wAIMaxDamage_ADDR, damage);
	SwapTurn();
	const uint8_t saved_location = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	gb_write8(hTempPlayAreaLocation_ff9d_ADDR, 0u); /* PLAY_AREA_ARENA */
	(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI, 0u, 0u, 0u);
	gb_write8(hTempPlayAreaLocation_ff9d_ADDR, saved_location);
	SwapTurn();
	if ((gb_read8(wAIMinDamage_ADDR) | gb_read8(wAIMaxDamage_ADDR)) == 0u) {
		damage = gb_read8(wDamage_ADDR);
		gb_write8(wAIMinDamage_ADDR, damage);
		gb_write8(wAIMaxDamage_ADDR, damage);
	}

	/* .calculation */
	if (gb_read8(hTempPlayAreaLocation_ff9d_ADDR) == 0u)
		return CalculateDamage_FromDefendingPokemon();

	DuelistVarResult saved1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	const uint16_t page = (uint16_t)(saved1.hl & 0xFF00u);
	const uint16_t sub1 = (uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS1);
	const uint16_t sub2 = (uint16_t)(page | DUELVARS_ARENA_CARD_SUBSTATUS2);
	const uint16_t resist = (uint16_t)(page | DUELVARS_ARENA_CARD_CHANGED_RESISTANCE);
	const uint8_t v1 = saved1.a;
	gb_write8(sub1, 0u);
	const uint8_t v2 = gb_read8(sub2);
	gb_write8(sub2, 0u);
	const uint8_t v3 = gb_read8(resist);
	gb_write8(resist, 0u);

	(void)CalculateDamage_FromDefendingPokemon();

	gb_write8(resist, v3);
	gb_write8(sub2, v2);
	gb_write8(sub1, v1);
	return (DamageCalculationResult){v1, 0x00u, 0u, 0u, sub1};
}
/* <<< factory EstimateDamage_FromDefendingPokemon */
