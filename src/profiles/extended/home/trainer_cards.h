/* >>> part includes */
#include <stdint.h>
#include "home/card_id.h"

/* Callee result types used by this file's declarations live in core.h
 * (AIMakeDecisionResult and friends). Packets tell a generator to "include
 * their header", but `statics` lands in the .c only, so a header fragment
 * naming a core.h type could not compile and cost four AIPlay_* attempts one
 * generation each on 2026-08-28. */
#include "home/core.h"
/* <<< part includes */
/* --- factory AIDecide_Defender_Phase14 */
/* --- factory PickPokedexCards_Unreferenced */
/* --- factory AIDecide_PlusPower_Phase14 */
/* --- factory AIDecide_Defender_Phase13 */
/* === factory AIDecide_GustOfWind */
/* >>> part AIDecide_Defender1 */
AIDecideParameterResult AIDecide_Defender1(uint8_t d);
/* <<< part AIDecide_Defender1 */
/* >>> part AIDecide_Defender2 */
AIDecideParameterResult AIDecide_Defender2(uint8_t d);
/* <<< part AIDecide_Defender2 */
/* >>> part AIDecide_PlusPower1 */
AIDecideParameterResult AIDecide_PlusPower1(uint8_t d);
/* <<< part AIDecide_PlusPower1 */
/* >>> part AIDecide_PlusPower2 */
AIDecideParameterResult AIDecide_PlusPower2(uint8_t d);
/* <<< part AIDecide_PlusPower2 */
/* >>> part AIDecide_SuperPotion1 */
AIDecideParameterResult AIDecide_SuperPotion1(uint8_t d);
/* <<< part AIDecide_SuperPotion1 */
/* >>> part AIDecide_SuperPotion2 */
AIDecideParameterResult AIDecide_SuperPotion2(uint8_t d);
/* <<< part AIDecide_SuperPotion2 */
/* --- factory AIDecide_PlusPower_Phase13 */
/* --- factory AIDecide_SuperPotion_Phase11 */
/* --- factory AIDecide_SuperPotion_Phase08 */
