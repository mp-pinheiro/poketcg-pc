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

#include "home/duel.h"
#include "mem.h"
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

/* >>> factory FindPlayAreaCardWithHighestAIScore */
/* energy.asm:596-675 */
AIScoreResult FindPlayAreaCardWithHighestAIScore(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	if (wAIEnergyAttachLogicFlags & AI_ENERGY_FLAG_SKIP_ARENA_CARD) {
		uint8_t cnt = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t n = (uint8_t)(cnt - 1u);
		if (n == 0u) {
			AIScoreResult r = {0u, 0x80u, b, c, d, e, hl};
			return r;
		}
		e = 0u;
		c = PLAY_AREA_BENCH_1;
		d = c;
		hl = (uint16_t)(wPlayAreaAIScore_ADDR + 1u);
		for (uint8_t i = 0u; i < n; i++) {
			uint8_t v = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			if (v > e) {
				e = v;
				d = c;
			}
			c = (uint8_t)(c + 1u);
		}
		hTempPlayAreaLocation_ff9d = d;
		AIScoreResult r = {d, 0x90u, 0u, c, d, e, hl};
		return r;
	}

	uint8_t cnt = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint32_t n = cnt ? (uint32_t)cnt : 0x100u;
	e = 0u;
	c = PLAY_AREA_ARENA;
	d = c;
	hl = wPlayAreaAIScore_ADDR;
	for (uint32_t i = 0u; i < n; i++) {
		uint8_t v = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (v > e) {
			e = v;
			d = c;
		}
		c = (uint8_t)(c + 1u);
	}
	if (e < 0x85u) {
		AIScoreResult r = {e, (uint8_t)(e == 0u ? 0x80u : 0x00u), 0u, c, d, e, hl};
		return r;
	}
	hTempPlayAreaLocation_ff9d = d;
	AIScoreResult r = {d, (uint8_t)(0x10u | (e == 0x85u ? 0x80u : 0x00u)), 0u, c, d, e, hl};
	return r;
}
/* <<< factory FindPlayAreaCardWithHighestAIScore */
