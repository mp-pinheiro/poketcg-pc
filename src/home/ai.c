#include "home/ai.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/load_deck.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/overworld.h"
#include "home/retreat.h"
#include "home/sams_practice.h"
#include "mem.h"

#define BANK_DECK_AI_POINTER_TABLE 5u
#define DECK_AI_POINTER_TABLE_ADDR 0x4000u
#define AI_ACTION_TABLE_SAM_PRACTICE_ADDR 0x47BDu
#define AI_ACTION_TABLE_SAM_FORCED_SWITCH_ADDR 0x47DAu
#define AI_ACTION_TABLE_SAM_KO_SWITCH_ADDR 0x47E7u

#define AIACTION_KO_SWITCH 0x04u
/* <<< factory statics */

#define SAMS_PRACTICE_DECK_ID 0u
#define SAMS_NORMAL_DECK_ID 2u
#define PRACTICE_PLAYER_DECK_ID 1u
#define PRACTICE_PLAYER_DECK 3u
#define NUM_DECK_IDS 53u
#define DUELIST_TYPE_AI_OPP 0x80u
#define DUELVARS_DUELIST_TYPE 0xF1u

/* ai.asm:1-46. Sam paths (deck id 0 or 2) force PRACTICE_PLAYER_DECK onto the
 * OTHER duelist (swap in, load, swap back) and reseed the RNG to $57/$57/$57;
 * every path then loads the (possibly Sam-forced) deck for the current turn
 * holder and clamps wOpponentDeckID to PRACTICE_PLAYER_DECK_ID if it is past
 * NUM_DECK_IDS. Exit a/hl are the final duelist-type write, the only
 * deterministic register outputs -- everything else is LoadDeck/SwapTurn
 * clobber the asm never saves. */
DeckLoadResult LoadOpponentDeck(void)
{
	wIsPracticeDuel = 0;
	uint8_t deck_id = wOpponentDeckID;
	uint8_t load_arg;

	if (deck_id == SAMS_NORMAL_DECK_ID || deck_id == SAMS_PRACTICE_DECK_ID) {
		if (deck_id == SAMS_PRACTICE_DECK_ID)
			wIsPracticeDuel = 1;
		wOpponentDeckID = 0;
		SwapTurn();
		(void)LoadDeck(PRACTICE_PLAYER_DECK);
		SwapTurn();
		wRNG1 = 0x57;
		wRNG2 = 0x57;
		wRNGCounter = 0x57;
		load_arg = 2;
	} else {
		load_arg = (uint8_t)(deck_id + 2u);
	}

	(void)LoadDeck(load_arg);
	if (wOpponentDeckID >= NUM_DECK_IDS + 1u)
		wOpponentDeckID = PRACTICE_PLAYER_DECK_ID;

	DuelistVarResult dv = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	uint8_t v = (uint8_t)(wOpponentDeckID | DUELIST_TYPE_AI_OPP);
	gb_write8(dv.hl, v);
	return (DeckLoadResult){v, dv.hl};
}

/* >>> factory AIDoAction */
uint8_t AIDoAction(uint8_t a)
{
	uint8_t action = a;
	uint8_t saved_bank = hBankROM;

	BankswitchROM(BANK_DECK_AI_POINTER_TABLE);
	const uint8_t *deck_entry = rom_ptr(
		BANK_DECK_AI_POINTER_TABLE,
		(uint16_t)(DECK_AI_POINTER_TABLE_ADDR +
			(uint16_t)wOpponentDeckID * 2u));
	uint16_t action_table = (uint16_t)(deck_entry[0] |
		((uint16_t)deck_entry[1] << 8));

	if (action == 0u) {
		const uint8_t *deck_data = rom_ptr(BANK_DECK_AI_POINTER_TABLE, action_table);
		uint16_t deck_pointer = (uint16_t)(deck_data[0] |
			((uint16_t)deck_data[1] << 8));
		CardListResult copied = CopyDeckData(deck_pointer);
		action = copied.a;
	} else {
		const uint8_t *target_entry = rom_ptr(
			BANK_DECK_AI_POINTER_TABLE,
			(uint16_t)(action_table + (uint16_t)action * 2u));
		uint16_t target = (uint16_t)(target_entry[0] |
			((uint16_t)target_entry[1] << 8));

		if (action == 3u || action == 4u) {
			if (target == AI_ACTION_TABLE_SAM_FORCED_SWITCH_ADDR ||
				target == AI_ACTION_TABLE_SAM_KO_SWITCH_ADDR) {
				SamsPracticeResult scripted = IsAIPracticeScriptedTurn(
					0u, 0u, 0u, 0u, 0u, 0u, 0u);
				if ((scripted.f & 0x10u) != 0u) {
					AIDecideBenchPokemonToSwitchToResult bench =
						AIDecideBenchPokemonToSwitchTo();
					action = bench.a;
				} else if (action == 3u) {
					action = PickRandomBenchPokemon();
				} else {
					GetPlayAreaLocationOfRaticateOrRattata();
					action = hTempPlayAreaLocation_ff9d;
				}
			} else {
				AIDecideBenchPokemonToSwitchToResult bench =
					AIDecideBenchPokemonToSwitchTo();
				action = bench.a;
			}
		}
	}

	BankswitchROM(saved_bank);
	return action;
}
/* <<< factory AIDoAction */

/* >>> factory AIDoAction_ForcedSwitch */
uint8_t AIDoAction_ForcedSwitch(void)
{
	uint8_t result = AIDoAction(0x03u);
	hTempPlayAreaLocation_ff9d = result;
	return result;
}
/* <<< factory AIDoAction_ForcedSwitch */

/* >>> factory AIDoAction_KOSwitch */
uint8_t AIDoAction_KOSwitch(void)
{
	uint8_t result = AIDoAction(AIACTION_KO_SWITCH);
	hTemp_ffa0 = result;
	return result;
}
/* <<< factory AIDoAction_KOSwitch */
