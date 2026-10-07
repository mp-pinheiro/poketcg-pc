/* >>> part includes */
#include <stdint.h>
#include "home/card_id.h"
/* <<< part includes */
/* >>> part PkmnPowerCountResult */
/* Pkmn-power counters (substatus.asm:495-590). Count cards of the given id in
 * the play areas, skipping status-incapable arena cards. Exit a = the count;
 * carry is set iff at least one was found ($10 found / $80 none, per the
 * `or a / scf / jr nz / or a` tail). All other registers restored. */
typedef struct {
	uint8_t a;
	uint8_t f;
	CardId de;
} PkmnPowerCountResult;
/* <<< part PkmnPowerCountResult */
/* >>> factory CountTurnDuelistPokemonWithActivePkmnPower */
PkmnPowerCountResult CountTurnDuelistPokemonWithActivePkmnPower(CardId target);
/* <<< factory CountTurnDuelistPokemonWithActivePkmnPower */
/* >>> factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
PkmnPowerCountResult CountPokemonWithActivePkmnPowerInBothPlayAreas(CardId target);
/* <<< factory CountPokemonWithActivePkmnPowerInBothPlayAreas */
/* >>> factory HandleDamageReductionExceptSubstatus2 */
uint16_t HandleDamageReductionExceptSubstatus2(uint16_t de);
/* <<< factory HandleDamageReductionExceptSubstatus2 */
/* >>> part PrehistoricPowerResult */
/* substatus.asm:650-659. a/hl pass through untouched from the Aerodactyl
 * check until the Muk check runs. b/c/d/e preserved. */
typedef struct {
	uint8_t a;
	uint8_t f;
	CardId de;
	uint16_t hl;
} PrehistoricPowerResult;
/* <<< part PrehistoricPowerResult */
/* >>> part StrikesBackResult */
typedef struct { uint8_t a, f, d, e; uint16_t hl; } StrikesBackResult;
/* <<< part StrikesBackResult */
/* >>> factory HandleStrikesBack_AgainstDamagingAttack */
StrikesBackResult HandleStrikesBack_AgainstDamagingAttack(uint16_t de, uint16_t hl);
/* <<< factory HandleStrikesBack_AgainstDamagingAttack */
