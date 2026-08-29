#include "home/challenge_hall_entrance.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/scripting.h"
#define CHALLENGE_CUP_NOT_STARTED 0x00u
#define CHALLENGE_CUP_READY_TO_START 0x01u
#define CHALLENGE_CUP_OVER 0x07u
#define EVENT_CHALLENGE_CUP_1_STATE 0x3fu
#define EVENT_CHALLENGE_CUP_2_STATE 0x40u
#define EVENT_CHALLENGE_CUP_3_STATE 0x41u
#define EVENT_CHALLENGE_CUP_NUMBER 0x44u
#define EVENT_CHALLENGE_CUP_STARTING 0x42u
#define EVENT_MEDAL_COUNT 0x2eu
#define MUSIC_CHALLENGE_HALL 0x0bu
/* <<< factory statics */

/* >>> factory Preload_Clerk9 */
PreloadClerk9Result Preload_Clerk9(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	TryGiveMedalPCPacksResult given = TryGiveMedalPCPacks(b, c, d, e, hl);
	PreloadClerk9Result result = {
		.a = given.a,
		.f = given.f,
		.b = given.b,
		.c = given.c,
		.d = given.d,
		.e = given.e,
		.hl = given.hl,
	};
	uint8_t medals = GetEventValue(EVENT_MEDAL_COUNT);
	if (medals < 9u) {
		if (medals == 3u) {
			if (GetEventValue(EVENT_CHALLENGE_CUP_1_STATE) == CHALLENGE_CUP_NOT_STARTED) {
				result.c = CHALLENGE_CUP_READY_TO_START;
				SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_READY_TO_START);
			}
		} else if (medals == 5u) {
			if (GetEventValue(EVENT_CHALLENGE_CUP_2_STATE) == CHALLENGE_CUP_NOT_STARTED) {
				result.c = CHALLENGE_CUP_READY_TO_START;
				SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_READY_TO_START);
			} else {
				result.c = CHALLENGE_CUP_OVER;
				SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
			}
		} else if (medals == 4u) {
			result.c = CHALLENGE_CUP_OVER;
			SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		} else if (medals >= 6u) {
			result.c = CHALLENGE_CUP_OVER;
			SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
			result.c = CHALLENGE_CUP_OVER;
			SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		}
	}
	ZeroOutEventValue(EVENT_CHALLENGE_CUP_STARTING, 0u, 0u, 0u);
	uint8_t cup1 = GetEventValue(EVENT_CHALLENGE_CUP_1_STATE);
	if (cup1 != CHALLENGE_CUP_NOT_STARTED && cup1 != CHALLENGE_CUP_OVER) {
		result.c = 1u;
		SetEventValue(EVENT_CHALLENGE_CUP_NUMBER, 0u, 0u, result.c);
		MaxOutEventValue(EVENT_CHALLENGE_CUP_STARTING, 0u, 0u, 0u);
		result.a = MUSIC_CHALLENGE_HALL;
		wDefaultSong = result.a;
	} else {
		uint8_t cup2 = GetEventValue(EVENT_CHALLENGE_CUP_2_STATE);
		if (cup2 != CHALLENGE_CUP_NOT_STARTED && cup2 != CHALLENGE_CUP_OVER) {
			result.c = 2u;
			SetEventValue(EVENT_CHALLENGE_CUP_NUMBER, 0u, 0u, result.c);
			MaxOutEventValue(EVENT_CHALLENGE_CUP_STARTING, 0u, 0u, 0u);
			result.a = MUSIC_CHALLENGE_HALL;
			wDefaultSong = result.a;
		} else {
			uint8_t cup3 = GetEventValue(EVENT_CHALLENGE_CUP_3_STATE);
			if (cup3 != CHALLENGE_CUP_NOT_STARTED && cup3 != CHALLENGE_CUP_OVER) {
				result.c = 3u;
				SetEventValue(EVENT_CHALLENGE_CUP_NUMBER, 0u, 0u, result.c);
				MaxOutEventValue(EVENT_CHALLENGE_CUP_STARTING, 0u, 0u, 0u);
				result.a = MUSIC_CHALLENGE_HALL;
				wDefaultSong = result.a;
			}
		}
	}
	result.f = (uint8_t)((result.f & 0x80u) | 0x10u);
	result.hl = 0x6FE4u;
	return result;
}
/* <<< factory Preload_Clerk9 */
