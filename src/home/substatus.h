#ifndef POKETCG_HOME_SUBSTATUS_H
#define POKETCG_HOME_SUBSTATUS_H

#include <stdint.h>

/* poketcg/src/home/substatus.asm */

typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t de;
	uint16_t hl;
} SandAttackCheckResult;

SandAttackCheckResult CheckSandAttackOrSmokescreenSubstatus(uint16_t de);

/* Pkmn-power counters (substatus.asm:495-590). Count cards of the given id in
 * the play areas, skipping status-incapable arena cards. Exit a = the count;
 * carry is set iff at least one was found ($10 found / $80 none, per the
 * `or a / scf / jr nz / or a` tail). All other registers restored. */
typedef struct {
	uint8_t a;
	uint8_t f;
} PkmnPowerCountResult;
PkmnPowerCountResult CountTurnDuelistPokemonWithActivePkmnPower(uint8_t a);
PkmnPowerCountResult CountPokemonWithActivePkmnPowerInBothPlayAreas(uint8_t a);

/* substatus.asm:495-516. hl is the text id shown; `a` is scratch, never a
 * documented output. b/c/d/e preserved. */
typedef struct {
	uint8_t f;
	uint16_t hl;
} PkmnPowerIncapableResult;
PkmnPowerIncapableResult CheckIsIncapableOfUsingPkmnPower(uint8_t a);
PkmnPowerIncapableResult CheckIsIncapableOfUsingPkmnPower_ArenaCard(void);

/* substatus.asm:1-27. The SUBSTATUS1/SUBSTATUS2 reads that follow the double
 * are dead: `call nz, .retN` into a bare `.retN: ret` just pops its own
 * return address, so they are not reproduced. */
uint16_t HandleDoubleDamageSubstatus(uint16_t de);

/* substatus.asm:60-159. Bug-compatible: SUBSTATUS1_HALVE_DAMAGE and Kabuto
 * Armor use `sla d` where the source comment says it should be `sra d` --
 * doubling the high byte instead of halving it -- and the result sticks even
 * when the parity check afterward takes the early return. */
uint16_t HandleDamageReductionExceptSubstatus2(uint16_t de);

uint16_t HandleDamageReduction(uint16_t de);

/* substatus.asm:284-304. GetTurnDuelistVariable has no push/pop, so hl is
 * always left at the SUBSTATUS2 duelvar's address unless a match overwrites
 * it with the text id; there is no caller-hl passthrough. b/c/d/e preserved. */
typedef struct {
	uint8_t f;
	uint16_t hl;
} CantAttackResult;
CantAttackResult HandleCantAttackSubstatus(void);

/* substatus.asm:306-328. Same as HandleCantAttackSubstatus: hl always ends at
 * the SUBSTATUS2 (or disabled-attack) duelvar's address, or the text id on a
 * match. d/e are never touched by the asm at all. */
typedef struct {
	uint8_t f;
	uint16_t hl;
} AmnesiaResult;
AmnesiaResult HandleAmnesiaSubstatus(void);

/* substatus.asm:367-418. e/hl pass through untouched only on the
 * POKEMON_POWER early exit (before any duelvar read); the `cp` that decides
 * it sets N, so that exit's f is $C0, not $80. Past the FLY/BARRIER/AGILITY
 * checks, hl is clobbered again by CheckIsIncapableOfUsingPkmnPower_ArenaCard
 * (no push/pop there either) before the Neutralizing Shield check, and only
 * NShield's own ldtx overwrites it again. e ends up holding
 * wTempTurnDuelistCardID's raw value on the Neutralizing Shield path (not a
 * NO_DAMAGE_OR_EFFECT_* constant), because that path reuses e for the
 * LoadCardDataToBuffer2_FromCardID call. */
typedef struct {
	uint8_t f;
	uint8_t e;
	uint16_t hl;
} NoDamageOrEffectResult;
NoDamageOrEffectResult HandleNoDamageOrEffectSubstatus(uint8_t e, uint16_t hl);

/* substatus.asm:448-474. Carry is always set on this path. hl is the resolved
 * id from NoDamageOrEffectTextIDTable, $0000 if bit 7 already marked the text
 * shown, or passed through untouched when wNoDamageOrEffect is 0. Sets bit 7
 * of wNoDamageOrEffect as a side effect the first time through. b/c preserved. */
typedef struct {
	uint8_t f;
	uint16_t hl;
} NoDamageOrEffectCheckResult;
NoDamageOrEffectCheckResult CheckNoDamageOrEffect(uint16_t hl);

/* substatus.asm:483-491. a is 0 when Muk's Toxic Gas blocks the check outright,
 * else the matching Omanyte count. b/c/d/e/hl preserved. */
PkmnPowerCountResult IsClairvoyanceActive(void);

uint8_t GetLoadedCard1RetreatCost(void);

/* substatus.asm:624-637. hl always ends at the SUBSTATUS2 duelvar's address,
 * or the text id on a match; no caller-hl passthrough. b/c/d/e preserved. */
typedef struct {
	uint8_t f;
	uint16_t hl;
} RetreatEffectResult;
RetreatEffectResult CheckUnableToRetreatDueToEffect(void);

/* substatus.asm:639-648. $A0 rather than $80 on the clear path: `bit` always
 * sets H, and only the set path's `scf` clears it back. b/c/d/e preserved. */
typedef struct {
	uint8_t f;
	uint16_t hl;
} TrainerEffectResult;
TrainerEffectResult CheckCantUseTrainerDueToEffect(void);

/* substatus.asm:650-659. a/hl pass through untouched from the Aerodactyl
 * check until the Muk check runs. b/c/d/e preserved. */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} PrehistoricPowerResult;
PrehistoricPowerResult IsPrehistoricPowerActive(uint16_t hl);

void ClearDamageReductionSubstatus2(void);

void UpdateSubstatusConditions_StartOfTurn(void);

void UpdateSubstatusConditions_EndOfTurn(void);

PkmnPowerCountResult IsRainDanceActive(void);

/* substatus.asm:838-857. The asm calls its zeroing subroutine once explicitly
 * (post-SwapTurn) then falls into it a second time (post-SwapTurn-back), so
 * both duelists' CHANGED_TYPE runs get cleared, not just one. */
void ClearChangedTypesIfMuk(uint8_t a);

typedef struct { uint8_t a, f; } RainDanceResult;
RainDanceResult CheckRainDanceScenario(void);

typedef struct { uint8_t a, f; } StrikesBackResult;
StrikesBackResult HandleStrikesBack_AgainstDamagingAttack(uint16_t de);


/* >>> factory ApplyStrikesBack_AgainstResidualAttack */
typedef struct { uint8_t a, f; } ApplyStrikesBackResult;
ApplyStrikesBackResult ApplyStrikesBack_AgainstResidualAttack(uint16_t hl);
/* <<< factory ApplyStrikesBack_AgainstResidualAttack */
/* >>> factory HandleStrikesBack_AgainstResidualAttack */
typedef struct { uint8_t a, f; } HandleStrikesBackResidualResult;
HandleStrikesBackResidualResult HandleStrikesBack_AgainstResidualAttack(void);
/* <<< factory HandleStrikesBack_AgainstResidualAttack */
/* >>> factory HandleDestinyBondSubstatus */
/* substatus.asm:746-809. a/f are the register state of the test that returned;
 * hl is the duelvar address the last lookup left in it, since nothing on the
 * early-exit paths preserves hl. b/c/d/e are never observed. */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} DestinyBondResult;
DestinyBondResult HandleDestinyBondSubstatus(void);
/* <<< factory HandleDestinyBondSubstatus */
#endif