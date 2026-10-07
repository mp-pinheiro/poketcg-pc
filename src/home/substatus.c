/* >>> part includes */
#include "home/substatus.h"

#include "generated/text_ids.h"
#include "generated/rom.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/coin_toss.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "home/menus.h"
#include "home/frames.h"
#include "home/print_text.h"
#include "mem.h"
#include "home/card_id_bus.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/substatus.h"

#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "mem.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/coin_toss.h"
#include "home/duel.h"
#include "home/menus.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/substatus.h"

#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "mem.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/coin_toss.h"
#include "home/duel.h"
#include "home/menus.h"
/* <<< part includes_2 */
/* >>> part DUELVARS_ARENA_CARD_STAGE */
#define DUELVARS_ARENA_CARD_STAGE 0xceu
/* <<< part DUELVARS_ARENA_CARD_STAGE */

/* >>> part includes_DUELVARS_ARENA_CARD_SUBSTATUS2 */
#include "generated/wram.h"
#include "home/coin_toss.h"
#include "home/substatus.h"

#include "generated/wram.h"
#include "home/coin_toss.h"
#include "home/menus.h"
#include "home/substatus.h"
/* <<< part includes_DUELVARS_ARENA_CARD_SUBSTATUS2 */

/* >>> part DUELVARS_ARENA_CARD_SUBSTATUS2 */
#define DUELVARS_ARENA_CARD_SUBSTATUS2 0xe8u
/* <<< part DUELVARS_ARENA_CARD_SUBSTATUS2 */
/* >>> part SAND_ATTACK_CHECK_TEXT */
#define SAND_ATTACK_CHECK_TEXT SandAttackCheckText
/* <<< part SAND_ATTACK_CHECK_TEXT */
/* >>> part SMOKESCREEN_CHECK_TEXT */
#define SMOKESCREEN_CHECK_TEXT SmokescreenCheckText
/* <<< part SMOKESCREEN_CHECK_TEXT */
/* >>> part DUELVARS_ARENA_CARD */
#define DUELVARS_ARENA_CARD 0xbbu
/* <<< part DUELVARS_ARENA_CARD */
/* >>> part DUELVARS_BENCH */
#define DUELVARS_BENCH 0xbcu
/* <<< part DUELVARS_BENCH */
/* >>> part DUELVARS_ARENA_CARD_STATUS */
#define DUELVARS_ARENA_CARD_STATUS 0xf0u
/* <<< part DUELVARS_ARENA_CARD_STATUS */
/* >>> part wTempPokemonID_ADDR */
#define wTempPokemonID_ADDR wTempPokemonID_ce7c_ADDR
/* <<< part wTempPokemonID_ADDR */

/* >>> factory CountTurnDuelistPokemonWithActivePkmnPower */
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
/* <<< factory CountTurnDuelistPokemonWithActivePkmnPower */

/* >>> factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
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
/* <<< factory CountPokemonWithActivePkmnPowerInBothPlayAreas */

/* >>> factory CheckSandAttackOrSmokescreenSubstatus */
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
/* <<< factory CheckSandAttackOrSmokescreenSubstatus */

/* >>> part DUELVARS_ARENA_CARD_SUBSTATUS1 */
#define DUELVARS_ARENA_CARD_SUBSTATUS1 0xe7u
/* <<< part DUELVARS_ARENA_CARD_SUBSTATUS1 */
/* >>> part DUELVARS_ARENA_CARD_SUBSTATUS3 */
#define DUELVARS_ARENA_CARD_SUBSTATUS3 0xebu
/* <<< part DUELVARS_ARENA_CARD_SUBSTATUS3 */
/* >>> part DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX */
#define DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX 0xf2u
/* <<< part DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX */
/* >>> part DUELVARS_ARENA_CARD_CHANGED_TYPE */
#define DUELVARS_ARENA_CARD_CHANGED_TYPE 0xd4u
/* <<< part DUELVARS_ARENA_CARD_CHANGED_TYPE */







/* >>> part CANNOT_USE_DUE_TO_STATUS_TEXT_ID */
/* ldtx's compile-time text ids, matching text_offsets.asm's index (the same
 * convention as duel.c's PLAYER2_TEXT_ID). */
#define CANNOT_USE_DUE_TO_STATUS_TEXT_ID CannotUseDueToStatusText
/* <<< part CANNOT_USE_DUE_TO_STATUS_TEXT_ID */
/* >>> part UNABLE_DUE_TO_TOXIC_GAS_TEXT_ID */
#define UNABLE_DUE_TO_TOXIC_GAS_TEXT_ID UnableDueToToxicGasText
/* <<< part UNABLE_DUE_TO_TOXIC_GAS_TEXT_ID */
/* >>> part UNABLE_TO_RETREAT_DUE_TO_ACID_TEXT_ID */
#define UNABLE_TO_RETREAT_DUE_TO_ACID_TEXT_ID UnableToRetreatDueToAcidText
/* <<< part UNABLE_TO_RETREAT_DUE_TO_ACID_TEXT_ID */
/* >>> part UNABLE_TO_USE_TRAINER_DUE_TO_HEADACHE_TEXT_ID */
#define UNABLE_TO_USE_TRAINER_DUE_TO_HEADACHE_TEXT_ID UnableToUseTrainerDueToHeadacheText
/* <<< part UNABLE_TO_USE_TRAINER_DUE_TO_HEADACHE_TEXT_ID */
/* >>> part UNABLE_TO_ATTACK_DUE_TO_TAIL_WAG_TEXT_ID */
#define UNABLE_TO_ATTACK_DUE_TO_TAIL_WAG_TEXT_ID UnableToAttackDueToTailWagText
/* <<< part UNABLE_TO_ATTACK_DUE_TO_TAIL_WAG_TEXT_ID */
/* >>> part UNABLE_TO_ATTACK_DUE_TO_LEER_TEXT_ID */
#define UNABLE_TO_ATTACK_DUE_TO_LEER_TEXT_ID UnableToAttackDueToLeerText
/* <<< part UNABLE_TO_ATTACK_DUE_TO_LEER_TEXT_ID */
/* >>> part UNABLE_TO_ATTACK_DUE_TO_BONE_ATTACK_TEXT_ID */
#define UNABLE_TO_ATTACK_DUE_TO_BONE_ATTACK_TEXT_ID UnableToAttackDueToBoneAttackText
/* <<< part UNABLE_TO_ATTACK_DUE_TO_BONE_ATTACK_TEXT_ID */
/* >>> part UNABLE_TO_USE_ATTACK_DUE_TO_AMNESIA_TEXT_ID */
#define UNABLE_TO_USE_ATTACK_DUE_TO_AMNESIA_TEXT_ID UnableToUseAttackDueToAmnesiaText
/* <<< part UNABLE_TO_USE_ATTACK_DUE_TO_AMNESIA_TEXT_ID */
/* >>> part UNABLE_TO_EVOLVE_DUE_TO_PREHISTORIC_POWER_TEXT_ID */
#define UNABLE_TO_EVOLVE_DUE_TO_PREHISTORIC_POWER_TEXT_ID UnableToEvolveDueToPrehistoricPowerText
/* <<< part UNABLE_TO_EVOLVE_DUE_TO_PREHISTORIC_POWER_TEXT_ID */
/* >>> part NO_DAMAGE_OR_EFFECT_DUE_TO_FLY_TEXT_ID */
#define NO_DAMAGE_OR_EFFECT_DUE_TO_FLY_TEXT_ID NoDamageOrEffectDueToFlyText
/* <<< part NO_DAMAGE_OR_EFFECT_DUE_TO_FLY_TEXT_ID */
/* >>> part NO_DAMAGE_OR_EFFECT_DUE_TO_BARRIER_TEXT_ID */
#define NO_DAMAGE_OR_EFFECT_DUE_TO_BARRIER_TEXT_ID NoDamageOrEffectDueToBarrierText
/* <<< part NO_DAMAGE_OR_EFFECT_DUE_TO_BARRIER_TEXT_ID */
/* >>> part NO_DAMAGE_OR_EFFECT_DUE_TO_AGILITY_TEXT_ID */
#define NO_DAMAGE_OR_EFFECT_DUE_TO_AGILITY_TEXT_ID NoDamageOrEffectDueToAgilityText
/* <<< part NO_DAMAGE_OR_EFFECT_DUE_TO_AGILITY_TEXT_ID */
/* >>> part NO_DAMAGE_OR_EFFECT_DUE_TO_NSHIELD_TEXT_ID */
#define NO_DAMAGE_OR_EFFECT_DUE_TO_NSHIELD_TEXT_ID NoDamageOrEffectDueToNShieldText
/* <<< part NO_DAMAGE_OR_EFFECT_DUE_TO_NSHIELD_TEXT_ID */

/* >>> part NO_DAMAGE_OR_EFFECT_TEXT_ID_TABLE_ADDR */
/* substatus.asm:476-481, ROM0 fixed bank (00:34d8 per poketcg.sym). */
#define NO_DAMAGE_OR_EFFECT_TEXT_ID_TABLE_ADDR NoDamageOrEffectTextIDTable_ADDR
/* <<< part NO_DAMAGE_OR_EFFECT_TEXT_ID_TABLE_ADDR */

/* >>> factory CheckIsIncapableOfUsingPkmnPower */
PkmnPowerIncapableResult CheckIsIncapableOfUsingPkmnPower(uint8_t a)
{
	if (a == PLAY_AREA_ARENA) {
		DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
		if (status.a & CNF_SLP_PRZ)
			return (PkmnPowerIncapableResult){(uint8_t)(status.a & CNF_SLP_PRZ), 0x10u, CANNOT_USE_DUE_TO_STATUS_TEXT_ID};
	}
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	return (PkmnPowerIncapableResult){muk.a, muk.f, UNABLE_DUE_TO_TOXIC_GAS_TEXT_ID};
}
/* <<< factory CheckIsIncapableOfUsingPkmnPower */

/* >>> factory CheckIsIncapableOfUsingPkmnPower_ArenaCard */
PkmnPowerIncapableResult CheckIsIncapableOfUsingPkmnPower_ArenaCard(void)
{
	return CheckIsIncapableOfUsingPkmnPower(PLAY_AREA_ARENA);
}
/* <<< factory CheckIsIncapableOfUsingPkmnPower_ArenaCard */

/* >>> factory HandleDoubleDamageSubstatus */
uint16_t HandleDoubleDamageSubstatus(uint16_t de)
{
	DuelistVarResult sub3 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS3);
	if ((sub3.a & (1u << SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F)) && de != 0)
		de = (uint16_t)(de << 1);
	return de;
}
/* <<< factory HandleDoubleDamageSubstatus */

/* >>> part reduce_by */
static uint16_t reduce_by(uint16_t de, uint16_t amount)
{
	return (uint16_t)(de + (uint16_t)(0u - amount));
}
/* <<< part reduce_by */

/* >>> part buggy_halve_damage */
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
/* <<< part buggy_halve_damage */

/* >>> factory HandleDamageReductionExceptSubstatus2 */
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
	return HandleDamageReductionExceptSubstatus2_PkmnPower(de);
}
/* <<< factory HandleDamageReductionExceptSubstatus2 */

/* >>> part HandleDamageReductionExceptSubstatus2_PkmnPower */
uint16_t HandleDamageReductionExceptSubstatus2_PkmnPower(uint16_t de)
{
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
/* <<< part HandleDamageReductionExceptSubstatus2_PkmnPower */

/* >>> factory HandleDamageReduction */
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
/* <<< factory HandleDamageReduction */

/* >>> factory HandleCantAttackSubstatus */
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
/* <<< factory HandleCantAttackSubstatus */

/* >>> factory HandleAmnesiaSubstatus */
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
/* <<< factory HandleAmnesiaSubstatus */

/* >>> factory HandleNoDamageOrEffectSubstatus */
NoDamageOrEffectResult HandleNoDamageOrEffectSubstatus(uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wNoDamageOrEffect_ADDR, 0);
	if (gb_read8(wLoadedAttackCategory_ADDR) == POKEMON_POWER)
		return (NoDamageOrEffectResult){0xC0u, d, e, hl};

	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);

	e = NO_DAMAGE_OR_EFFECT_FLY;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_FLY_TEXT_ID;
	if (sub1.a == SUBSTATUS1_FLY) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, d, e, hl};
	}

	e = NO_DAMAGE_OR_EFFECT_BARRIER;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_BARRIER_TEXT_ID;
	if (sub1.a == SUBSTATUS1_BARRIER) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, d, e, hl};
	}

	e = NO_DAMAGE_OR_EFFECT_AGILITY;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_AGILITY_TEXT_ID;
	if (sub1.a == SUBSTATUS1_AGILITY) {
		gb_write8(wNoDamageOrEffect_ADDR, e);
		return (NoDamageOrEffectResult){0x90u, d, e, hl};
	}

	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower_ArenaCard();
	hl = incapable.hl;
	if (incapable.f & 0x10u)
		return (NoDamageOrEffectResult){0x00u, d, e, hl};
	return HandleNoDamageOrEffectSubstatus_PkmnPower(d, e, hl);
}
/* <<< factory HandleNoDamageOrEffectSubstatus */

/* >>> part HandleNoDamageOrEffectSubstatus_PkmnPower */
NoDamageOrEffectResult HandleNoDamageOrEffectSubstatus_PkmnPower(uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t defender = gb_read8(wTempNonTurnDuelistCardID_ADDR);
	if (defender != MEW_LV8)
		return (NoDamageOrEffectResult){defender == 0 ? 0x80u : 0x00u, d, e, hl};

	if (gb_read8(wIsDamageToSelf_ADDR) != 0)
		return (NoDamageOrEffectResult){0x00u, d, e, hl};

	/* `ld e, a; ld d, $0`: the card id is loaded through de. */
	e = gb_read8(wTempTurnDuelistCardID_ADDR);
	d = 0u;
	LoadCardDataToBuffer2_FromCardID(e);
	if (gb_read8(wLoadedCard2Stage_ADDR) == 0)
		return (NoDamageOrEffectResult){0x80u, d, e, hl};

	e = NO_DAMAGE_OR_EFFECT_NSHIELD;
	hl = NO_DAMAGE_OR_EFFECT_DUE_TO_NSHIELD_TEXT_ID;
	gb_write8(wNoDamageOrEffect_ADDR, e);
	return (NoDamageOrEffectResult){0x10u, d, e, hl};
}
/* <<< part HandleNoDamageOrEffectSubstatus_PkmnPower */

/* >>> factory CheckNoDamageOrEffect */
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
/* <<< factory CheckNoDamageOrEffect */

/* >>> factory IsClairvoyanceActive */
PkmnPowerCountResult IsClairvoyanceActive(void)
{
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (muk.f & 0x10u)
		return (PkmnPowerCountResult){muk.a, 0x00u};
	return CountTurnDuelistPokemonWithActivePkmnPower(OMANYTE);
}
/* <<< factory IsClairvoyanceActive */

/* >>> factory GetLoadedCard1RetreatCost */
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
/* <<< factory GetLoadedCard1RetreatCost */

/* >>> factory CheckUnableToRetreatDueToEffect */
RetreatEffectResult CheckUnableToRetreatDueToEffect(void)
{
	DuelistVarResult sub2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS2);
	if (sub2.a == 0)
		return (RetreatEffectResult){0x80u, sub2.hl};
	if (sub2.a != SUBSTATUS2_ACID)
		return (RetreatEffectResult){0x00u, sub2.hl};
	return (RetreatEffectResult){0x90u, UNABLE_TO_RETREAT_DUE_TO_ACID_TEXT_ID};
}
/* <<< factory CheckUnableToRetreatDueToEffect */

/* >>> factory CheckCantUseTrainerDueToEffect */
TrainerEffectResult CheckCantUseTrainerDueToEffect(void)
{
	DuelistVarResult sub3 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS3);
	if (!(sub3.a & (1u << SUBSTATUS3_HEADACHE_F)))
		return (TrainerEffectResult){0xA0u, sub3.hl};
	return (TrainerEffectResult){0x10u, UNABLE_TO_USE_TRAINER_DUE_TO_HEADACHE_TEXT_ID};
}
/* <<< factory CheckCantUseTrainerDueToEffect */

/* >>> factory IsPrehistoricPowerActive */
PrehistoricPowerResult IsPrehistoricPowerActive(uint16_t hl)
{
	PkmnPowerCountResult aero = CountPokemonWithActivePkmnPowerInBothPlayAreas(AERODACTYL);
	if (!(aero.f & 0x10u))
		return (PrehistoricPowerResult){aero.a, aero.f, hl};
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	uint8_t f = (muk.f & 0x10u) ? 0x00u : 0x90u;
	return (PrehistoricPowerResult){muk.a, f, UNABLE_TO_EVOLVE_DUE_TO_PREHISTORIC_POWER_TEXT_ID};
}
/* <<< factory IsPrehistoricPowerActive */

/* >>> factory ClearDamageReductionSubstatus2 */
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
/* <<< factory ClearDamageReductionSubstatus2 */

/* >>> factory UpdateSubstatusConditions_StartOfTurn */
void UpdateSubstatusConditions_StartOfTurn(void)
{
	DuelistVarResult sub1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	gb_write8(sub1.hl, 0);
	if (sub1.a != SUBSTATUS1_NEXT_TURN_DOUBLE_DAMAGE)
		return;
	DuelistVarResult sub3 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS3);
	gb_write8(sub3.hl, (uint8_t)(sub3.a | (1u << SUBSTATUS3_THIS_TURN_DOUBLE_DAMAGE_F)));
}
/* <<< factory UpdateSubstatusConditions_StartOfTurn */

/* >>> factory UpdateSubstatusConditions_EndOfTurn */
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
/* <<< factory UpdateSubstatusConditions_EndOfTurn */

/* >>> factory IsRainDanceActive */
PkmnPowerCountResult IsRainDanceActive(void)
{
	PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
	if (!(blastoise.f & 0x10u))
		return blastoise;
	PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	uint8_t f = (muk.f & 0x10u) ? 0x00u : 0x90u;
	return (PkmnPowerCountResult){muk.a, f};
}
/* <<< factory IsRainDanceActive */

/* >>> part zero_changed_type_run */
static void zero_changed_type_run(void)
{
	uint16_t addr = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_CHANGED_TYPE).hl;
	for (uint8_t i = 0; i < MAX_PLAY_AREA_POKEMON; i++)
		gb_write8(addr++, 0);
}
/* <<< part zero_changed_type_run */

/* >>> factory ClearChangedTypesIfMuk */
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
/* <<< factory ClearChangedTypesIfMuk */



/* >>> factory CheckRainDanceScenario */
RainDanceResult CheckRainDanceScenario(void)
{
	uint8_t card_idx = hTempCardIndex_ff98;
	uint16_t card_id = GetCardIDFromDeckIndex(card_idx);
	uint8_t card_type = GetCardType(card_id);
	if (card_type != TYPE_ENERGY_WATER)
		return (RainDanceResult){card_type, 0x00u};
	uint8_t color = GetPlayAreaCardColor(hTempPlayAreaLocation_ff9d);
	if (color != TYPE_PKMN_WATER)
		return (RainDanceResult){color, 0x00u};
	return (RainDanceResult){TYPE_PKMN_WATER, 0x90u};
}
/* <<< factory CheckRainDanceScenario */

/* >>> part MACHAMP_ID */
#define MACHAMP_ID 0x7Fu
/* <<< part MACHAMP_ID */
/* >>> part MUK_ID */
#define MUK_ID     0x27u
/* <<< part MUK_ID */
/* >>> part DUELVARS_ARENA_CARD_HP */
#define DUELVARS_ARENA_CARD_HP 0xc8u
/* <<< part DUELVARS_ARENA_CARD_HP */
/* >>> part RECEIVES_DAMAGE_DUE_TO_STRIKES_BACK_TEXT */
#define RECEIVES_DAMAGE_DUE_TO_STRIKES_BACK_TEXT ReceivesDamageDueToStrikesBackText
/* <<< part RECEIVES_DAMAGE_DUE_TO_STRIKES_BACK_TEXT */
/* >>> part f_or */
static uint8_t f_or(uint8_t result) { return (uint8_t)(result ? 0x00u : 0x80u); }
/* <<< part f_or */
/* >>> part f_cp */
static uint8_t f_cp(uint8_t a, uint8_t val)
{
	uint8_t f = 0x40u;
	if (a == val) f |= 0x80u;
	if ((a & 0x0Fu) < (val & 0x0Fu)) f |= 0x20u;
	if (a < val) f |= 0x10u;
	return f;
}
/* <<< part f_cp */

/* >>> factory HandleStrikesBack_AgainstDamagingAttack */
StrikesBackResult HandleStrikesBack_AgainstDamagingAttack(uint16_t de)
{
	uint8_t a;
	if (!de) {
		a = (uint8_t)de;
		return (StrikesBackResult){a, f_or(a)};
	}
	a = wIsDamageToSelf;
	if (a)
		return (StrikesBackResult){a, f_or(a)};
	a = wTempNonTurnDuelistCardID;
	if (a != MACHAMP_ID)
		return (StrikesBackResult){a, f_cp(a, MACHAMP_ID)};
	PkmnPowerCountResult count = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK_ID);
	if (count.f & 0x10u)
		return (StrikesBackResult){count.a, count.f};
	a = wLoadedAttackCategory;
	if (a == 0x04u)
		return (StrikesBackResult){a, f_cp(a, 0x04u)};
	if (!wTempPlayAreaLocation_cceb) {
		uint8_t inc_f = CheckIsIncapableOfUsingPkmnPower_ArenaCard().f;
		if (inc_f & 0x10u)
			return (StrikesBackResult){a, inc_f};
	}
	SwapTurn();
	uint8_t deck_idx = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	LoadCardDataToBuffer2_FromDeckIndex(deck_idx);
	DuelistVarResult hp_var = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t hp = hp_var.a;
	(void)SubtractHP(hp_var.hl, 10);
	wTempNonTurnDuelistCardID = wLoadedCard2ID;
	LoadTxRam3(10);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard2Name_ADDR)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	DrawWideTextBox_WaitForInput(RECEIVES_DAMAGE_DUE_TO_STRIKES_BACK_TEXT);
	if (hp)
		PrintPlayAreaCardKnockedOutIfNoHP(0);
	SwapTurn();
	return (StrikesBackResult){0, 0x10u};
}
/* <<< factory HandleStrikesBack_AgainstDamagingAttack */
/* >>> factory ApplyStrikesBack_AgainstResidualAttack */
ApplyStrikesBackResult ApplyStrikesBack_AgainstResidualAttack(uint16_t hl)
{
	LoadTxRam3(hl);
	uint8_t card_id = wTempTurnDuelistCardID;
	LoadCardDataToBuffer2_FromCardID(card_id);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard2Name_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	DuelistVarResult hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	SubtractHPResult subtracted = SubtractHP(hp.hl, hl);
	(void)DrawWideTextBox_PrintText(ReceivesDamageDueToStrikesBackText);
	if (subtracted.a == 0)
		return (ApplyStrikesBackResult){0, 0x80u};
	(void)WaitForWideTextBoxInput();
	(void)PrintPlayAreaCardKnockedOutIfNoHP(PLAY_AREA_ARENA);
	DrawDuelHUDs();
	return (ApplyStrikesBackResult){0, 0x10u};
}
/* <<< factory ApplyStrikesBack_AgainstResidualAttack */

/* >>> factory HandleStrikesBack_AgainstResidualAttack */
HandleStrikesBackResidualResult HandleStrikesBack_AgainstResidualAttack(void)
{
	uint8_t card_id = wTempNonTurnDuelistCardID;
	if (card_id != MACHAMP) {
		/* substatus.asm:788-790 `cp MACHAMP / ret`: N, and H or C as the
		 * compare borrows; the carry is not implied. */
		uint8_t f = 0x40u;
		if ((card_id & 0x0Fu) < (MACHAMP & 0x0Fu))
			f |= 0x20u;
		if (card_id < MACHAMP)
			f |= 0x10u;
		return (HandleStrikesBackResidualResult){card_id, f};
	}
	uint8_t category = wLoadedAttackCategory;
	uint8_t residual = (uint8_t)(category & RESIDUAL);
	if (residual)
		return (HandleStrikesBackResidualResult){residual, 0x20u};
	uint8_t damage = wDealtDamage;
	if (!damage)
		return (HandleStrikesBackResidualResult){0x00u, 0x80u};
	SwapTurn();
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower_ArenaCard();
	SwapTurn();
	if (incapable.f & 0x10u)
		return (HandleStrikesBackResidualResult){0x00u, incapable.f};
	ApplyStrikesBackResult applied = ApplyStrikesBack_AgainstResidualAttack(10u);
	if (!(applied.f & 0x10u)) {
		WaitResult waited = WaitForWideTextBoxInput();
		return (HandleStrikesBackResidualResult){applied.a, waited.f};
	}
	return (HandleStrikesBackResidualResult){applied.a, applied.f};
}
/* <<< factory HandleStrikesBack_AgainstResidualAttack */

/* >>> factory HandleDestinyBondSubstatus */
/* substatus.asm:746-809. Destiny Bond: when the defending (non-turn) arena
 * Pokemon carries the substatus and has just been knocked out, the attacking
 * (turn holder's) arena Pokemon is knocked out with it. Neither duelvar helper
 * pushes hl, so every early exit reports the address its own lookup left
 * behind, with the flags of the test that took that exit. */
DestinyBondResult HandleDestinyBondSubstatus(void)
{
	DuelistVarResult substatus = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_SUBSTATUS1);
	if (substatus.a != SUBSTATUS1_DESTINY_BOND)
		return (DestinyBondResult){substatus.a,
			f_cp(substatus.a, SUBSTATUS1_DESTINY_BOND), substatus.hl};

	/* `cp -1`: an empty arena slot means there is nothing to bond with. */
	DuelistVarResult defending = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (defending.a == 0xFFu)
		return (DestinyBondResult){defending.a, f_cp(defending.a, 0xFFu), defending.hl};

	DuelistVarResult defending_hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	if (defending_hp.a != 0u)
		return (DestinyBondResult){defending_hp.a, f_or(defending_hp.a), defending_hp.hl};

	DuelistVarResult attacking_hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	if (attacking_hp.a == 0u)
		return (DestinyBondResult){attacking_hp.a, f_or(attacking_hp.a), attacking_hp.hl};

	gb_write8(attacking_hp.hl, 0u);
	DrawDuelMainScene();
	DrawDuelHUDs();
	/* `pop hl` restores the HP duelvar and `ld l, DUELVARS_ARENA_CARD` rewrites
	 * only the low byte, so this stays on the turn holder's duelvar page. */
	uint16_t attacking_card = (uint16_t)((attacking_hp.hl & 0xFF00u) | DUELVARS_ARENA_CARD);
	(void)LoadCardDataToBuffer2_FromDeckIndex(gb_read8(attacking_card));
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard2Name_ADDR)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard2Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	WaitResult waited = DrawWideTextBox_WaitForInput(KnockedOutDueToDestinyBondText);
	/* The text-box wait clobbers a and hl in the ROM; the ported WaitResult
	 * carries only f, so this exit reports the last hl this routine loads. */
	return (DestinyBondResult){0u, waited.f, KnockedOutDueToDestinyBondText};
}
/* <<< factory HandleDestinyBondSubstatus */

/* >>> factory HandleNShieldAndTransparency */
HandleNShieldAndTransparencyResult HandleNShieldAndTransparency(uint16_t de)
{
	uint8_t e = (uint8_t)de;
	DuelistVarResult arena = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e));
	uint8_t card = GetCardIDFromDeckIndex(arena.a);
	if (card == MEW_LV8) {
		DuelistVarResult stage = GetNonTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_STAGE + e));
		if (stage.a != 0u) {
			gb_write8(wNoDamageOrEffect_ADDR, NO_DAMAGE_OR_EFFECT_NSHIELD);
			(void)DrawWideTextBox_WaitForInput(NoDamageOrEffectDueToNShieldText);
			return (HandleNShieldAndTransparencyResult){0u, 0x90u, (uint8_t)(de >> 8), e, NoDamageOrEffectDueToNShieldText};
		}
		return (HandleNShieldAndTransparencyResult){stage.a, stage.a ? 0u : 0x80u, (uint8_t)(de >> 8), e, stage.hl};
	}
	if (card == HAUNTER_LV17) {
		wDuelDisplayedScreen = 0u;
		TossCoinRoutineResult toss = TossCoin(TransparencyCheckText, arena.hl);
		if (toss.f & 0x10u) {
			gb_write8(wNoDamageOrEffect_ADDR, NO_DAMAGE_OR_EFFECT_TRANSPARENCY);
			(void)DrawWideTextBox_WaitForInput(NoDamageOrEffectDueToTransparencyText);
			return (HandleNShieldAndTransparencyResult){0u, 0x90u, (uint8_t)(de >> 8), e, NoDamageOrEffectDueToTransparencyText};
		}
		return (HandleNShieldAndTransparencyResult){toss.a, toss.a ? 0u : 0x80u, (uint8_t)(de >> 8), e, toss.hl};
	}
	return (HandleNShieldAndTransparencyResult){card, card ? 0u : 0x80u, (uint8_t)(de >> 8), e, arena.hl};
}
/* <<< factory HandleNShieldAndTransparency */

/* >>> factory HandleTransparency */
HandleTransparencyResult HandleTransparency(uint16_t hl)
{
	uint8_t card = wTempNonTurnDuelistCardID;
	if (card != HAUNTER_LV17)
		return (HandleTransparencyResult){card, card ? 0u : 0x80u, hl};

	uint8_t category = wLoadedAttackCategory;
	if (category == POKEMON_POWER) {
		return (HandleTransparencyResult){category, category ? 0u : 0x80u, hl};
	}

	uint8_t location = wTempPlayAreaLocation_cceb;
	PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(location);
	if (incapable.f & 0x10u)
		return (HandleTransparencyResult){location, location ? 0u : 0x80u, incapable.hl};

	wDuelDisplayedScreen = 0u;
	TossCoinRoutineResult toss = TossCoin(TransparencyCheckText, hl);
	if (!(toss.f & 0x10u))
		return (HandleTransparencyResult){toss.a, toss.f, toss.hl};

	wNoDamageOrEffect = NO_DAMAGE_OR_EFFECT_TRANSPARENCY;
	return (HandleTransparencyResult){NO_DAMAGE_OR_EFFECT_TRANSPARENCY, 0x10u, NoDamageOrEffectDueToTransparencyText};
}
/* <<< factory HandleTransparency */

/* >>> factory HandleDamageReductionOrNoDamageFromPkmnPowerEffects */
HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult HandleDamageReductionOrNoDamageFromPkmnPowerEffects(uint16_t de, uint16_t hl)
{
	uint8_t category = wLoadedAttackCategory;
	if (category == POKEMON_POWER)
		return (HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult){0xC0u, de, hl};

	PkmnPowerCountResult powers = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
	if (powers.f & 0x10u)
		return (HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult){powers.f, de, hl};

	uint8_t location = wTempPlayAreaLocation_cceb;
	if (location != 0)
		de = HandleDamageReductionExceptSubstatus2_PkmnPower(de);

	uint16_t damage = de;
	NoDamageOrEffectResult no_damage = HandleNoDamageOrEffectSubstatus_PkmnPower((uint8_t)(de >> 8), location, hl);
	uint8_t f = no_damage.f;
	hl = no_damage.hl;
	if (!(f & 0x10u)) {
		HandleTransparencyResult transparency = HandleTransparency(hl);
		f = transparency.f;
		hl = transparency.hl;
		if (f & 0x10u)
			damage = 0;
	} else {
		damage = 0;
	}
	return (HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult){f, damage, hl};
}
/* <<< factory HandleDamageReductionOrNoDamageFromPkmnPowerEffects */

/* >>> factory HandleSandAttackOrSmokescreenSubstatus */
HandleSandAttackOrSmokescreenSubstatusResult HandleSandAttackOrSmokescreenSubstatus(uint16_t de, uint16_t hl)
{
	(void)hl;
	SandAttackCheckResult check = CheckSandAttackOrSmokescreenSubstatus(de);
	if ((check.f & 0x10u) == 0u)
		return (HandleSandAttackOrSmokescreenSubstatusResult){check.a, check.f, check.de, check.hl, 0u};
	TossCoinRoutineResult toss = TossCoin(check.de, check.hl);
	wGotHeadsFromSandAttackOrSmokescreenCheck = toss.a;
	if ((toss.f & 0x10u) != 0u)
		return (HandleSandAttackOrSmokescreenSubstatusResult){toss.a, (uint8_t)(toss.f & 0x80u), check.de, toss.hl, 0u};
	WaitResult wait = DrawWideTextBox_WaitForInput(AttackUnsuccessfulText);
	return (HandleSandAttackOrSmokescreenSubstatusResult){wait.a, (uint8_t)((wait.f & 0x80u) | 0x10u),
		(uint16_t)((uint16_t)wait.d << 8 | wait.e), wait.hl,
		(uint16_t)((uint16_t)wait.b << 8 | wait.c)};
}
/* <<< factory HandleSandAttackOrSmokescreenSubstatus */
