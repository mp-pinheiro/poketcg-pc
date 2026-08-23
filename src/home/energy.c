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

#include "home/duel.h"
#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define CHARMANDER 0x30u
#define COLORLESS 0x06u
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define DRATINI 0xbfu
#define DUELVARS_ARENA_CARD 0xbbu
#define GROWLITHE 0x36u
#define LEGENDARY_DRAGONITE_DECK_ID 0x0fu
#define FIRE_CHARGE_DECK_ID 0x17u
#define LEGENDARY_RONALD_DECK_ID 0x1bu
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

/* >>> factory CheckSpecificDecksToAttachDoubleColorless */
static uint8_t CheckSpecificDecksToAttachDoubleColorless_GetID(void)
{
	uint8_t loc = hTempPlayAreaLocation_ff9d;
	DuelistVarResult v = GetTurnDuelistVariable((uint8_t)(loc + DUELVARS_ARENA_CARD));
	uint16_t id16 = GetCardIDFromDeckIndex(v.a);
	return (uint8_t)id16;
}

CheckSpecificDecksToAttachDoubleColorlessResult CheckSpecificDecksToAttachDoubleColorless(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t deck_id = wOpponentDeckID;
	uint8_t a = deck_id;
	uint8_t check_colorless = 0u;

	if (deck_id == LEGENDARY_DRAGONITE_DECK_ID) {
		a = CheckSpecificDecksToAttachDoubleColorless_GetID();
		if (a == CHARMANDER || a == DRATINI)
			check_colorless = 1u;
	} else if (deck_id == FIRE_CHARGE_DECK_ID) {
		a = CheckSpecificDecksToAttachDoubleColorless_GetID();
		if (a == GROWLITHE)
			check_colorless = 1u;
	} else if (deck_id == LEGENDARY_RONALD_DECK_ID) {
		a = CheckSpecificDecksToAttachDoubleColorless_GetID();
		if (a == DRATINI)
			check_colorless = 1u;
	}

	if (check_colorless) {
		uint8_t loc = hTempPlayAreaLocation_ff9d;
		(void)GetPlayAreaCardAttachedEnergies(loc);
		a = gb_read8((uint16_t)(wAttachedEnergies_ADDR + COLORLESS));
		if (a == 0u) {
			CoreCardListResult r = LookForCardIDInHand(DOUBLE_COLORLESS_ENERGY);
			if (!(r.f & 0x10u)) {
				hTemp_ffa0 = r.a;
				return (CheckSpecificDecksToAttachDoubleColorlessResult){r.a, 0x10u, b, c, d, e, hl};
			}
			a = r.a;
		}
	}
	return (CheckSpecificDecksToAttachDoubleColorlessResult){a, (uint8_t)(a == 0u ? 0x80u : 0u), b, c, d, e, hl};
}
/* <<< factory CheckSpecificDecksToAttachDoubleColorless */
