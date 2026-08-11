#include "home/challenge_hall_lobby.h"

#include "generated/wram.h"
#include "mem.h"

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
