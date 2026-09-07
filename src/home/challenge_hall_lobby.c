#include "home/challenge_hall_lobby.h"

#include "generated/wram.h"
#include "mem.h"
#include "home/challenge_hall_lobby.h"
#include "home/map.h"
#include "home/scripting.h"
#include "generated/wram.h"
#include "mem.h"
#define EVENT_RONALD_CHALLENGE_HALL_LOBBY_STATE 0x58u
#define EVENT_RECEIVED_LEGENDARY_CARDS 0x22u
#define EVENT_PLAYER_ENTERED_CHALLENGE_CUP 0x59u
#define EVENT_CHALLENGE_CUP_2_STATE 0x40u
#define EVENT_CHALLENGE_CUP_2_RESULT 0x49u
#define EVENT_CHALLENGE_CUP_1_STATE 0x3Fu
#define EVENT_CHALLENGE_CUP_1_RESULT 0x48u
#define EVENT_CHALLENGE_CUP_STARTING 0x42u
#define EVENT_CHALLENGE_CUP_NOT_STARTED 0u
#define EVENT_CHALLENGE_CUP_READY_TO_START 1u
#define EVENT_CHALLENGE_CUP_LOST 2u
#define EVENT_CHALLENGE_CUP_OVER 3u
#define NPC_RONALD1 0x02u
#define SCRIPT_F166 0x7166u
#define CUP1_TABLE 0x7146u
#define EVENT_CHALLENGE_CUP_STARTING_OFFSET 0x10u
#define EVENT_CHALLENGE_CUP_STARTING_MASK 0x80u
#define MUSIC_CHALLENGE_HALL 0x0Bu
#define W_DEFAULT_SONG_ADDR 0xD111u
#define CUP2_TABLE 0x7156u

/* >>> factory Preload_ChallengeHallNPCs1 */
/* challenge_hall_lobby.asm:6-14 */
PreloadChallengeHallNPCs1Result Preload_ChallengeHallNPCs1(void)
{
	uint8_t event = GetEventValue(EVENT_CHALLENGE_CUP_STARTING);
	if (event == 0u)
		return (PreloadChallengeHallNPCs1Result){0u, 0x80u};
	gb_write8(W_DEFAULT_SONG_ADDR, MUSIC_CHALLENGE_HALL);
	return (PreloadChallengeHallNPCs1Result){MUSIC_CHALLENGE_HALL, 0x10u};
}
/* <<< factory Preload_ChallengeHallNPCs1 */

/* >>> factory ChallengeHallLobbyLoadMap */
/* challenge_hall_lobby.asm:16-24 */
ChallengeHallLobbyLoadMapResult ChallengeHallLobbyLoadMap(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t event = GetEventValue(EVENT_RONALD_CHALLENGE_HALL_LOBBY_STATE);
	if (event == 0u)
		return (ChallengeHallLobbyLoadMapResult){0u, 0x80u, b, c, hl};
	wTempNPC = NPC_RONALD1;
	(void)FindLoadedNPC();
	SetNextNPCAndScriptResult r = SetNextNPCAndScript(SCRIPT_F166, hl);
	return (ChallengeHallLobbyLoadMapResult){r.a, r.f, r.b, r.c, r.hl};
}
/* <<< factory ChallengeHallLobbyLoadMap */

ChallengeHallLobbyResult Preload_ChallengeHallNPCs2(void)
{
	uint8_t event_byte = gb_read8((uint16_t)(wEventVars_ADDR + EVENT_CHALLENGE_CUP_STARTING_OFFSET));
	gb_write8(wLoadedEventBits_ADDR, EVENT_CHALLENGE_CUP_STARTING_MASK);
	if ((event_byte & EVENT_CHALLENGE_CUP_STARTING_MASK) == 0)
		return (ChallengeHallLobbyResult){0, 0x90u};
	gb_write8(W_DEFAULT_SONG_ADDR, MUSIC_CHALLENGE_HALL);
	return (ChallengeHallLobbyResult){MUSIC_CHALLENGE_HALL, 0};
}

/* >>> factory Preload_ChallengeHallLobbyRonald1 */
/* challenge_hall_lobby.asm:50-97 */
PreloadChallengeHallLobbyRonald1Result Preload_ChallengeHallLobbyRonald1(void)
{
	(void)SetEventValue(EVENT_RONALD_CHALLENGE_HALL_LOBBY_STATE, 0u, 0u, 0u);
	if (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) != 0u) {
		for (uint8_t event = 0x50u; event <= 0x57u; event++)
			(void)MaxOutEventValue(event, 0u, 0u, 0u);
		for (uint8_t event = 0x50u; event <= 0x53u; event++)
			(void)MaxOutEventValue(event, 0u, 0u, 0u);
		return (PreloadChallengeHallLobbyRonald1Result){7u, 0u, 0u, 0u, 0u, 0u, 0u};
	}
	if (GetEventValue(EVENT_PLAYER_ENTERED_CHALLENGE_CUP) != 0u)
		return (PreloadChallengeHallLobbyRonald1Result){1u, 0u, 0u, 0u, 0u, 0u, 0u};
	uint8_t cup_state = GetEventValue(EVENT_CHALLENGE_CUP_2_STATE);
	if (cup_state != EVENT_CHALLENGE_CUP_NOT_STARTED) {
		for (uint8_t event = 0x50u; event <= 0x53u; event++)
			(void)MaxOutEventValue(event, 0u, 0u, 0u);
		uint8_t d = GetEventValue(EVENT_CHALLENGE_CUP_2_RESULT);
		SetRonaldChallengeHallLobbyStateResult r = SetRonaldChallengeHallLobbyState(CUP2_TABLE, d, cup_state);
		if ((r.f & 0x10u) == 0u)
			return (PreloadChallengeHallLobbyRonald1Result){r.a, r.f, 0u, 0u, d, cup_state, r.hl};
		wLoadNPCYPos = wPlayerYCoord;
		return (PreloadChallengeHallLobbyRonald1Result){wLoadNPCYPos, 0x10u, 0u, 4u, d, cup_state, r.hl};
	}
	uint8_t e = GetEventValue(EVENT_CHALLENGE_CUP_1_STATE);
	uint8_t d = GetEventValue(EVENT_CHALLENGE_CUP_1_RESULT);
	SetRonaldChallengeHallLobbyStateResult r = SetRonaldChallengeHallLobbyState(CUP1_TABLE, d, e);
	if ((r.f & 0x10u) == 0u)
		return (PreloadChallengeHallLobbyRonald1Result){r.a, r.f, 0u, 0u, d, e, r.hl};
	wLoadNPCYPos = wPlayerYCoord;
	return (PreloadChallengeHallLobbyRonald1Result){wLoadNPCYPos, 0x10u, 0u, 4u, d, e, r.hl};
}
/* <<< factory Preload_ChallengeHallLobbyRonald1 */

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
