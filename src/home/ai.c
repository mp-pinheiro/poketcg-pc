#include "home/ai.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/load_deck.h"
#include "mem.h"

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
