#include "home/energy.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define AI_ENERGY_FLAG_SKIP_ARENA_CARD 0x80u
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define MAX_PLAY_AREA_POKEMON 0x06u
#define PLAY_AREA_ARENA 0x00u
#define PLAY_AREA_BENCH_1 0x01u
/* <<< factory statics */

/* >>> factory RetrievePlayAreaAIScoreFromBackup1 */
/* energy.asm:71-84 */
Backup1Result RetrievePlayAreaAIScoreFromBackup1(void)
{
	uint16_t de = wPlayAreaAIScore_ADDR;
	uint16_t hl = wTempPlayAreaAIScore_ADDR;
	for (uint8_t b = MAX_PLAY_AREA_POKEMON; b != 0u; b--) {
		gb_write8(de, gb_read8(hl));
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(de + 1u);
	}
	wAIScore = gb_read8(hl);
	return (Backup1Result){de, hl};
}
/* <<< factory RetrievePlayAreaAIScoreFromBackup1 */
