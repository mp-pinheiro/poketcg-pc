#include "home/damage_calculation.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_color.h"
#include "home/duel.h"
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

