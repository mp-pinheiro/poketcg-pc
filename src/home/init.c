#include "home/init.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/core.h"

#include "home/common.h"
#include "home/duel.h"
#include "generated/wram.h"

#define AI_MEWTWO_MILL_F 0x07u
#define AI_MEWTWO_MILL (1u << AI_MEWTWO_MILL_F)
#define DUELVARS_ARENA_CARD 0xbbu
#define MEWTWO_LV53 0x9du
/* <<< factory statics */

/* >>> factory InitAIDuelVars */
/* init.asm:1-9 */
void InitAIDuelVars(void)
{
	ClearMemory_Bank5((uint8_t)(wAIDuelVarsEnd_ADDR - wAIDuelVars_ADDR), wAIDuelVars_ADDR);
	wAIPokedexCounter = 5u;
	wAIPeekedPrizes = 0xFFu;
}
/* <<< factory InitAIDuelVars */

/* >>> factory InitAITurnVars */
void InitAITurnVars(void)
{
	wAIPokedexCounter = (uint8_t)(wAIPokedexCounter + 1u);

	wPreviousAIFlags = 0u;
	wAITriedAttack = 0u;
	wUnused_cddc = 0u;
	wAIRetreatedThisTurn = 0u;

	uint8_t barrier_flag_set = 0u;
	if (wPlayerAttackingAttackIndex != 0xFFu && wPlayerAttackingAttackIndex != 0u &&
	    wPlayerAttackingCardIndex != 0xFFu) {
		SwapTurn();
		uint16_t id = GetCardIDFromDeckIndex(wPlayerAttackingCardIndex);
		SwapTurn();
		if ((uint8_t)id == MEWTWO_LV53) {
			if (wAIBarrierFlagCounter & AI_MEWTWO_MILL) {
				barrier_flag_set = 1u;
			} else {
				uint8_t counter = (uint8_t)(wAIBarrierFlagCounter + 1u);
				wAIBarrierFlagCounter = counter;
				if (counter >= 3u) {
					DuelistVarResult arena = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
					SwapTurn();
					uint16_t id2 = GetCardIDFromDeckIndex(arena.a);
					SwapTurn();
					if ((uint8_t)id2 == MEWTWO_LV53) {
						CheckIfPlayerHasPokemonOtherThanMewtwoLv53Result r =
							CheckIfPlayerHasPokemonOtherThanMewtwoLv53(0u, 0u, 0u, 0u);
						if (!(r.f & 0x10u))
							barrier_flag_set = 1u;
						else
							wAIBarrierFlagCounter = 0u;
					} else {
						wAIBarrierFlagCounter = 0u;
					}
				}
			}
			if (barrier_flag_set)
				wAIBarrierFlagCounter = AI_MEWTWO_MILL;
			return;
		}
	}

	if (wAIBarrierFlagCounter & AI_MEWTWO_MILL)
		wAIBarrierFlagCounter = (uint8_t)(wAIBarrierFlagCounter + 1u);
	else
		wAIBarrierFlagCounter = 0u;
}
/* <<< factory InitAITurnVars */
