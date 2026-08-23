#include "home/challenge_hall_lobby.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/challenge_hall_lobby.h"
#include "home/scripting.h"
#include "mem.h"
#define EVENT_RONALD_CHALLENGE_HALL_LOBBY_STATE 0x58u
/* <<< factory statics */

#define EVENT_CHALLENGE_CUP_STARTING_OFFSET 0x10u
#define EVENT_CHALLENGE_CUP_STARTING_MASK 0x80u
#define MUSIC_CHALLENGE_HALL 0x0Bu
#define W_DEFAULT_SONG_ADDR 0xD111u

ChallengeHallLobbyResult Preload_ChallengeHallNPCs2(void)
{
	uint8_t event_byte = gb_read8((uint16_t)(wEventVars_ADDR + EVENT_CHALLENGE_CUP_STARTING_OFFSET));
	gb_write8(wLoadedEventBits_ADDR, EVENT_CHALLENGE_CUP_STARTING_MASK);
	if ((event_byte & EVENT_CHALLENGE_CUP_STARTING_MASK) == 0)
		return (ChallengeHallLobbyResult){0, 0x90u};
	gb_write8(W_DEFAULT_SONG_ADDR, MUSIC_CHALLENGE_HALL);
	return (ChallengeHallLobbyResult){MUSIC_CHALLENGE_HALL, 0};
}

/* >>> factory SetRonaldChallengeHallLobbyState */
SetRonaldChallengeHallLobbyStateResult SetRonaldChallengeHallLobbyState(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t a = 0u;
	for (uint8_t c = 4u; c != 0u; c--) {
		a = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (a != e) {
			hl = (uint16_t)(hl + 3u);
			continue;
		}
		a = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (a != d) {
			hl = (uint16_t)(hl + 2u);
			continue;
		}
		a = gb_read8(hl);
		uint8_t current = GetEventValue(a);
		if (current != 0u) {
			hl = (uint16_t)(hl + 2u);
			continue;
		}
		(void)MaxOutEventValue(a, 0u, 0u, 0u);
		hl = (uint16_t)(hl + 1u);
		uint8_t convo = gb_read8(hl);
		SetEventValueResult setResult = SetEventValue(EVENT_RONALD_CHALLENGE_HALL_LOBBY_STATE, 0u, 0u, convo);
		uint8_t final_f = (uint8_t)((setResult.f & 0x80u) | 0x10u);
		return (SetRonaldChallengeHallLobbyStateResult){setResult.a, final_f, hl};
	}
	uint8_t f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
	return (SetRonaldChallengeHallLobbyStateResult){a, f, hl};
}
/* <<< factory SetRonaldChallengeHallLobbyState */
