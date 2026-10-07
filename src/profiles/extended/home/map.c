/* >>> part includes_tail */
#include "generated/sram.h"
#include "home/scripting.h"
#include "home/switch_sram.h"

#include "home/map.h"
#include "home/switch_rom.h"
#include "home/animation.h"
#include "home/overworld.h"
#include "home/npc_core.h"
#include "home/load_animation.h"
#include "home/random.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#include "generated/wram.h"
#include "generated/sram.h"
#include "home/switch_sram.h"
#include "home/save.h"
#include "home/core.h"

#include "home/map.h"
#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#include "generated/sram.h"


#include "home/map.h"
#include "home/challenge_machine.h"
#include "home/core.h"
#include "home/switch_sram.h"
#include "generated/wram.h"
#include "generated/sram.h"

#include "home/map.h"
#include "generated/wram.h"

#include "home/map.h"
#include "home/overworld.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_tail */
/* --- factory GameEvent_GiftCenter */
/* --- factory GameEvent_BattleCenter */
/* >>> factory _ExecuteGameEvent */
uint8_t _ExecuteGameEvent(void)
{
	uint8_t event = wGameEvent;
	if (event >= NUM_GAME_EVENTS)
		event = GAME_EVENT_CHALLENGE_MACHINE;
	switch (event) {
	case 0u:
		return GameEvent_Overworld(0u);
	case 1u:
		return GameEvent_Duel();
	case 2u:
		GameEvent_Credits();
		return 0x80u;
	case 3u: {
		SongResult result = GameEvent_ContinueDuel();
		return result.f;
	}
	case GAME_EVENT_CHALLENGE_MACHINE:
		return GameEvent_ChallengeMachine();
	default:
		return GameEvent_Overworld(0u);
	}
}
/* <<< factory _ExecuteGameEvent */
