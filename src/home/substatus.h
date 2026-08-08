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

#endif
