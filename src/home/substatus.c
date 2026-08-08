#include "home/substatus.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/coin_toss.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "mem.h"

#define DUELVARS_ARENA_CARD_SUBSTATUS2 0xe8u
#define SUBSTATUS2_SMOKESCREEN 0x01u
#define SUBSTATUS2_SAND_ATTACK 0x02u
#define SAND_ATTACK_CHECK_TEXT 0x00deu
#define SMOKESCREEN_CHECK_TEXT 0x00dfu
#define DUELVARS_ARENA_CARD 0xbbu
#define DUELVARS_BENCH 0xbcu
#define DUELVARS_ARENA_CARD_STATUS 0xf0u
#define CNF_SLP_PRZ 0x0fu
#define wTempPokemonID_ADDR 0xce7cu

/* substatus.asm:544-590. Counts arena (if not status-incapable) plus bench
 * slots matching the target id. The bench walk ends at its $FF terminator. */
PkmnPowerCountResult CountTurnDuelistPokemonWithActivePkmnPower(uint8_t a)
{
	gb_write8(wTempPokemonID_ADDR, a);
	uint8_t count = 0;
	uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	if (arena != 0xFF) {
		uint16_t arena_id = GetCardIDFromDeckIndex(arena);
		if ((uint8_t)arena_id == gb_read8(wTempPokemonID_ADDR)) {
			uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
			if (!(status & CNF_SLP_PRZ))
				count++;
		}
	}
	uint16_t bench = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
	while (gb_read8(bench) != 0xFF) {
		uint16_t slot_id = GetCardIDFromDeckIndex(gb_read8(bench));
		if ((uint8_t)slot_id == gb_read8(wTempPokemonID_ADDR))
			count++;
		bench++;
	}
	/* `or a / scf / jr nz / or a`: found = Z clear + C set. */
	return (PkmnPowerCountResult){count, count ? 0x10u : 0x80u};
}

/* substatus.asm:522-543: both duelists' play areas. */
PkmnPowerCountResult CountPokemonWithActivePkmnPowerInBothPlayAreas(uint8_t a)
{
	gb_write8(wTempPokemonID_ADDR, a);
	uint8_t count = CountTurnDuelistPokemonWithActivePkmnPower(a).a;
	SwapTurn();
	count = (uint8_t)(count + CountTurnDuelistPokemonWithActivePkmnPower(a).a);
	SwapTurn();
	return (PkmnPowerCountResult){count, count ? 0x10u : 0x80u};
}

/* substatus.asm:346-366. Returns carry iff the turn holder's arena card has the
 * sand-attack or smokescreen substatus active AND the coin toss came up tails.
 *
 * The ldtx flow is fall-through, not branch-scoped: `ldtx de, SandAttackCheckText`
 * runs for ANY non-zero substatus, then `ldtx de, SmokescreenCheckText` replaces it
 * whenever the value is not sand attack. So the unrelated-value exit carries
 * de = $00DF. GetTurnDuelistVariable leaves hl = the duelvar address and nothing
 * restores it, so exit hl is $C2E8/$C3E8 on every path. */
SandAttackCheckResult CheckSandAttackOrSmokescreenSubstatus(uint16_t de)
{
	DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (status.a == 0)
		return (SandAttackCheckResult){0, 0x80u, de, status.hl};

	de = SAND_ATTACK_CHECK_TEXT;
	if (status.a != SUBSTATUS2_SAND_ATTACK) {
		de = SMOKESCREEN_CHECK_TEXT;
		if (status.a != SUBSTATUS2_SMOKESCREEN)
			return (SandAttackCheckResult){status.a, 0x00u, de, status.hl};
	}

	uint8_t heads = gb_read8(wGotHeadsFromSandAttackOrSmokescreenCheck_ADDR);
	if (heads != 0)
		return (SandAttackCheckResult){heads, 0x00u, de, status.hl};
	/* `or a` set Z, then `scf` keeps it: the tails exit is Z+C. */
	return (SandAttackCheckResult){0, 0x90u, de, status.hl};
}

#define DUELVARS_ARENA_CARD_SUBSTATUS1 0xe7u
#define DUELVARS_ARENA_CARD_SUBSTATUS3 0xebu
#define DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX 0xf2u
#define DUELVARS_ARENA_CARD_CHANGED_TYPE 0xd4u
#define MAX_PLAY_AREA_POKEMON 6u
#define PLAY_AREA_ARENA 0x00u

#define SUBSTATUS1_AGILITY 0x0cu
#define SUBSTATUS1_FLY 0x0du
#define SUBSTATUS1_PREVENT_LESS_THAN_40 0x0eu
#define SUBSTATUS1_NO_DAMAGE_STIFFEN 0x0fu
#define SUBSTATUS1_NO_DAMAGE_WITHDRAW 0x10u
#define SUBSTATUS1_NO_DAMAGE_HIDE_IN_SHELL 0x11u
#define SUBSTATUS1_REDUCE_BY_20 0x13u
#define SUBSTATUS1_BARRIER 0x14u
#define SUBSTATUS1_HALVE_DAMAGE 0x15u
#define SUBSTATUS1_NO_DAMAGE_SCRUNCH 0x17u
#define SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE 0x19u
#define SUBSTATUS1_REDUCE_BY_10 0x1eu

#define SUBSTATUS2_REDUCE_BY_20 0x03u
#define SUBSTATUS2_AMNESIA 0x04u
#define SUBSTATUS2_TAIL_WAG 0x05u
#define SUBSTATUS2_LEER 0x06u
#define SUBSTATUS2_POUNCE 0x07u
#define SUBSTATUS2_ACID 0x09u
#define SUBSTATUS2_BONE_ATTACK 0x0bu
#define SUBSTATUS2_GROWL 0x12u

#define SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F 0u
#define SUBSTATUS3_HEADACHE_F 1u

#define NO_DAMAGE_OR_EFFECT_AGILITY 0x01u
#define NO_DAMAGE_OR_EFFECT_BARRIER 0x02u
#define NO_DAMAGE_OR_EFFECT_FLY 0x03u
#define NO_DAMAGE_OR_EFFECT_NSHIELD 0x05u

#define POKEMON_POWER 0x04u

#define MUK 0x27u
#define OMANYTE 0x5cu
#define BLASTOISE 0x43u
#define AERODACTYL 0x8du
#define DODRIO 0xb6u
#define MR_MIME 0x9bu
#define KABUTO 0x8bu
#define MEW_LV8 0xa0u

/* ldtx's compile-time text ids, matching text_offsets.asm's index (the same
 * convention as duel.c's PLAYER2_TEXT_ID). */
#define CANNOT_USE_DUE_TO_STATUS_TEXT_ID 0x00cbu
#define UNABLE_DUE_TO_TOXIC_GAS_TEXT_ID 0x00d4u
#define UNABLE_TO_RETREAT_DUE_TO_ACID_TEXT_ID 0x00feu
#define UNABLE_TO_USE_TRAINER_DUE_TO_HEADACHE_TEXT_ID 0x00ffu
#define UNABLE_TO_ATTACK_DUE_TO_TAIL_WAG_TEXT_ID 0x0100u
#define UNABLE_TO_ATTACK_DUE_TO_LEER_TEXT_ID 0x0101u
#define UNABLE_TO_ATTACK_DUE_TO_BONE_ATTACK_TEXT_ID 0x0102u
#define UNABLE_TO_USE_ATTACK_DUE_TO_AMNESIA_TEXT_ID 0x0103u
#define UNABLE_TO_EVOLVE_DUE_TO_PREHISTORIC_POWER_TEXT_ID 0x0106u
#define NO_DAMAGE_OR_EFFECT_DUE_TO_FLY_TEXT_ID 0x0107u
#define NO_DAMAGE_OR_EFFECT_DUE_TO_BARRIER_TEXT_ID 0x0108u
#define NO_DAMAGE_OR_EFFECT_DUE_TO_AGILITY_TEXT_ID 0x0109u
#define NO_DAMAGE_OR_EFFECT_DUE_TO_NSHIELD_TEXT_ID 0x010bu

/* substatus.asm:476-481, ROM0 fixed bank (00:34d8 per poketcg.sym). */
#define NO_DAMAGE_OR_EFFECT_TEXT_ID_TABLE_ADDR 0x34d8u

PkmnPowerIncapableResult CheckIsIncapableOfUsingPkmnPower(uint8_t a)
{
	if (a == PLAY_AREA_ARENA) {
		DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
		if (status.a & CNF_SLP_PRZ)
			return (PkmnPowerIncapableResult){0x10u, CANNOT_USE_DUE_TO_STATUS_TEXT_ID};
	}
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	return (PkmnPowerIncapableResult){muk.f, UNABLE_DUE_TO_TOXIC_GAS_TEXT_ID};
}

PkmnPowerIncapableResult CheckIsIncapableOfUsingPkmnPower_ArenaCard(void)
{
	return CheckIsIncapableOfUsingPkmnPower(PLAY_AREA_ARENA);
}

uint16_t HandleDoubleDamageSubstatus(uint16_t de)
{
	DuelistVarResult sub3 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS3);
	if ((sub3.a & (1u << SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F)) && de != 0)
		de = (uint16_t)(de << 1);
	return de;
}

static uint16_t reduce_by(uint16_t de, uint16_t amount)
{
	return (uint16_t)(de + (uint16_t)(0u - amount));
}

static uint16_t buggy_halve_damage(uint16_t de)
{
	uint8_t d = (uint8_t)(de >> 8);
	uint8_t e = (uint8_t)de;
	uint8_t sla_carry = (uint8_t)(d >> 7);
	d = (uint8_t)(d << 1);
	e = (uint8_t)((sla_carry << 7) | (e >> 1));
	de = (uint16_t)((uint16_t)d << 8 | e);
	if (!(e & 1u))
		return de;
	return reduce_by(de, 5);
}

uint16_t HandleDamageReductionExceptSubstatus2(uint16_t de)
{
	if (gb_read8(wNoDamageOrEffect_ADDR) != 0)
		return 0;

	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	if (sub1.a != 0) {
		if (sub1.a == SUBSTATUS1_NO_DAMAGE_STIFFEN || sub1.a == SUBSTATUS1_NO_DAMAGE_WITHDRAW ||
		    sub1.a == SUBSTATUS1_NO_DAMAGE_HIDE_IN_SHELL || sub1.a == SUBSTATUS1_NO_DAMAGE_SCRUNCH)
			return 0;
		if (sub1.a == SUBSTATUS1_REDUCE_BY_10)
			return reduce_by(de, 10);
		if (sub1.a == SUBSTATUS1_REDUCE_BY_20)
			return reduce_by(de, 20);
		if (sub1.a == SUBSTATUS1_PREVENT_LESS_THAN_40) {
			if (CompareDEtoBC((uint8_t)(de >> 8), (uint8_t)de, 0, 40) & 0x10u)
				return 0;
			return de;
		}
		if (sub1.a == SUBSTATUS1_HALVE_DAMAGE)
			return buggy_halve_damage(de);
	}

	if (CheckIsIncapableOfUsingPkmnPower_ArenaCard().f & 0x10u)
		return de;
	if (gb_read8(wLoadedAttackCategory_ADDR) == POKEMON_POWER)
		return de;
	uint8_t defender = gb_read8(wTempNonTurnDuelistCardID_ADDR);
	if (defender == MR_MIME) {
		if (CompareDEtoBC((uint8_t)(de >> 8), (uint8_t)de, 0, 30) & 0x10u)
			return de;
		return 0;
	}
	if (defender == KABUTO)
		return buggy_halve_damage(de);
	return de;
}

uint16_t HandleDamageReduction(uint16_t de)
{
	de = HandleDamageReductionExceptSubstatus2(de);
	DuelistVarResult sub2 = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (sub2.a == 0)
		return de;
	if (sub2.a == SUBSTATUS2_REDUCE_BY_20)
		return reduce_by(de, 20);
	if (sub2.a == SUBSTATUS2_POUNCE || sub2.a == SUBSTATUS2_GROWL)
		return reduce_by(de, 10);
	return de;
}

CantAttackResult HandleCantAttackSubstatus(void)
{
	DuelistVarResult sub2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (sub2.a == 0)
		return (CantAttackResult){0x80u, sub2.hl};
	if (sub2.a == SUBSTATUS2_TAIL_WAG)
		return (CantAttackResult){0x90u, UNABLE_TO_ATTACK_DUE_TO_TAIL_WAG_TEXT_ID};
	if (sub2.a == SUBSTATUS2_LEER)
		return (CantAttackResult){0x90u, UNABLE_TO_ATTACK_DUE_TO_LEER_TEXT_ID};
	if (sub2.a == SUBSTATUS2_BONE_ATTACK)
		return (CantAttackResult){0x90u, UNABLE_TO_ATTACK_DUE_TO_BONE_ATTACK_TEXT_ID};
	return (CantAttackResult){0x00u, UNABLE_TO_ATTACK_DUE_TO_BONE_ATTACK_TEXT_ID};
}

AmnesiaResult HandleAmnesiaSubstatus(void)
{
	DuelistVarResult sub2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (sub2.a == 0)
		return (AmnesiaResult){0x80u, sub2.hl};
	if (sub2.a != SUBSTATUS2_AMNESIA)
		return (AmnesiaResult){0x00u, sub2.hl};
	DuelistVarResult disabled = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX);
	uint8_t selected = gb_read8(wSelectedAttack_ADDR);
	if (selected != disabled.a)
		return (AmnesiaResult){selected == 0 ? 0x80u : 0x00u, disabled.hl};
	return (AmnesiaResult){0x90u, UNABLE_TO_USE_ATTACK_DUE_TO_AMNESIA_TEXT_ID};
}

NoDamageOrEffectResult HandleNoDamageOrEffectSubstatus(uint8_t e, uint16_t hl)
{
	gb_write8(wNoDamageOrEffect_ADDR, 0);
	if (gb_read8(wLoadedAttackCategory_ADDR) == POKEMON_POWER)
		return (NoDamageOrEffectResult){0xC0u, e, hl};

	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);

	e = NO_DAMAGE_OR_EFFECT_FLY;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_FLY_TEXT_ID;
	if (sub1.a == SUBSTATUS1_FLY) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, e, hl};
	}

	e = NO_DAMAGE_OR_EFFECT_BARRIER;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_BARRIER_TEXT_ID;
	if (sub1.a == SUBSTATUS1_BARRIER) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, e, hl};
	}

	e = NO_DAMAGE_OR_EFFECT_AGILITY;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_AGILITY_TEXT_ID;
	if (sub1.a == SUBSTATUS1_AGILITY) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, e, hl};
	}

	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower_ArenaCard();
	hl = incapable.hl;
	if (incapable.f & 0x10u)
		return (NoDamageOrEffectResult){0x00u, e, hl};

	uint8_t defender = gb_read8(wTempNonTurnDuelistCardID_ADDR);
	if (defender != MEW_LV8)
		return (NoDamageOrEffectResult){defender == 0 ? 0x80u : 0x00u, e, hl};

	if (gb_read8(wIsDamageToSelf_ADDR) != 0)
		return (NoDamageOrEffectResult){0x00u, e, hl};

	e = gb_read8(wTempTurnDuelistCardID_ADDR);
	LoadCardDataToBuffer2_FromCardID(e);
	if (gb_read8(wLoadedCard2Stage_ADDR) == 0)
		return (NoDamageOrEffectResult){0x80u, e, hl};

	e = NO_DAMAGE_OR_EFFECT_NSHIELD;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_NSHIELD_TEXT_ID;
	gb_write8(wNoDamageOrEffect_ADDR, e);
	return (NoDamageOrEffectResult){0x10u, e, hl};
}

NoDamageOrEffectCheckResult CheckNoDamageOrEffect(uint16_t hl)
{
	uint8_t val = gb_read8(wNoDamageOrEffect_ADDR);
	if (val == 0)
		return (NoDamageOrEffectCheckResult){0x80u, hl};
	if (val & 0x80u)
		return (NoDamageOrEffectCheckResult){0x10u, 0x0000u};

	gb_write8(wNoDamageOrEffect_ADDR, (uint8_t)(val | 0x80u));
	uint8_t offset = (uint8_t)((val - 1u) * 2u);
	const uint8_t *entry = rom_ptr(0u, (uint16_t)(NO_DAMAGE_OR_EFFECT_TEXT_ID_TABLE_ADDR + offset));
	uint16_t id = (uint16_t)(entry[0] | (uint16_t)entry[1] << 8);
	return (NoDamageOrEffectCheckResult){offset == 0 ? 0x90u : 0x10u, id};
}

PkmnPowerCountResult IsClairvoyanceActive(void)
{
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (muk.f & 0x10u)
		return (PkmnPowerCountResult){muk.a, 0x00u};
	return CountTurnDuelistPokemonWithActivePkmnPower(OMANYTE);
}

uint8_t GetLoadedCard1RetreatCost(void)
{
	uint8_t dodrio_count = 0;
	uint16_t bench = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
	while (gb_read8(bench) != 0xFFu) {
		uint16_t id = GetCardIDFromDeckIndex(gb_read8(bench));
		if ((uint8_t)id == DODRIO)
			dodrio_count++;
		bench++;
	}

	uint8_t regular_cost = gb_read8(wLoadedCard1RetreatCost_ADDR);
	if (dodrio_count == 0)
		return regular_cost;

	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (muk.f & 0x10u)
		return regular_cost;

	if (regular_cost >= dodrio_count)
		return (uint8_t)(regular_cost - dodrio_count);
	return 0;
}

RetreatEffectResult CheckUnableToRetreatDueToEffect(void)
{
	DuelistVarResult sub2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (sub2.a == 0)
		return (RetreatEffectResult){0x80u, sub2.hl};
	if (sub2.a != SUBSTATUS2_ACID)
		return (RetreatEffectResult){0x00u, sub2.hl};
	return (RetreatEffectResult){0x90u, UNABLE_TO_RETREAT_DUE_TO_ACID_TEXT_ID};
}

TrainerEffectResult CheckCantUseTrainerDueToEffect(void)
{
	DuelistVarResult sub3 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS3);
	if (!(sub3.a & (1u << SUBSTATUS3_HEADACHE_F)))
		return (TrainerEffectResult){0xA0u, sub3.hl};
	return (TrainerEffectResult){0x10u, UNABLE_TO_USE_TRAINER_DUE_TO_HEADACHE_TEXT_ID};
}

PrehistoricPowerResult IsPrehistoricPowerActive(uint16_t hl)
{
	PkmnPowerCountResult aero = CountPokemonWithActivePkmnPowerInBothPlayAreas(AERODACTYL);
	if (!(aero.f & 0x10u))
		return (PrehistoricPowerResult){aero.a, aero.f, hl};
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	uint8_t f = (muk.f & 0x10u) ? 0x00u : 0x90u;
	return (PrehistoricPowerResult){muk.a, f, UNABLE_TO_EVOLVE_DUE_TO_PREHISTORIC_POWER_TEXT_ID};
}

void ClearDamageReductionSubstatus2(void)
{
	DuelistVarResult sub2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (sub2.a == 0)
		return;
	if (sub2.a == SUBSTATUS2_REDUCE_BY_20 || sub2.a == SUBSTATUS2_POUNCE ||
	    sub2.a == SUBSTATUS2_GROWL || sub2.a == SUBSTATUS2_TAIL_WAG ||
	    sub2.a == SUBSTATUS2_LEER)
		gb_write8(sub2.hl, 0);
}

void UpdateSubstatusConditions_StartOfTurn(void)
{
	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	gb_write8(sub1.hl, 0);
	if (sub1.a != SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE)
		return;
	DuelistVarResult sub3 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS3);
	gb_write8(sub3.hl, (uint8_t)(sub3.a | (1u << SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F)));
}

void UpdateSubstatusConditions_EndOfTurn(void)
{
	DuelistVarResult sub3 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS3);
	gb_write8(sub3.hl, (uint8_t)(sub3.a & (uint8_t)~(1u << SUBSTATUS3_HEADACHE_F)));

	DuelistVarResult sub2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	gb_write8(sub2.hl, 0);

	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	if (sub1.a == SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE)
		return;

	uint8_t sub3_now = gb_read8(sub3.hl);
	gb_write8(sub3.hl, (uint8_t)(sub3_now & (uint8_t)~(1u << SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F)));
}

PkmnPowerCountResult IsRainDanceActive(void)
{
	PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
	if (!(blastoise.f & 0x10u))
		return blastoise;
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	uint8_t f = (muk.f & 0x10u) ? 0x00u : 0x90u;
	return (PkmnPowerCountResult){muk.a, f};
}

static void zero_changed_type_run(void)
{
	uint16_t addr = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_CHANGED_TYPE).hl;
	for (uint8_t i = 0; i < MAX_PLAY_AREA_POKEMON; i++)
		gb_write8(addr++, 0);
}

void ClearChangedTypesIfMuk(uint8_t a)
{
	uint16_t id = GetCardIDFromDeckIndex(a);
	if ((uint8_t)id != MUK)
		return;
	SwapTurn();
	zero_changed_type_run();
	SwapTurn();
	zero_changed_type_run();
}


#define TYPE_ENERGY_WATER 0x0Bu
#define TYPE_PKMN_WATER   0x03u

RainDanceResult CheckRainDanceScenario(void)
{
	uint8_t card_idx = hTempCardIndex_ff98;
	uint16_t card_id = GetCardIDFromDeckIndex(card_idx);
	uint8_t card_type = GetCardType((uint8_t)card_id);
	if (card_type != TYPE_ENERGY_WATER)
		return (RainDanceResult){card_type, 0x00u};
	uint8_t color = GetPlayAreaCardColor(hTempPlayAreaLocation_ff9d);
	if (color != TYPE_PKMN_WATER)
		return (RainDanceResult){color, 0x00u};
	return (RainDanceResult){TYPE_PKMN_WATER, 0x90u};
}