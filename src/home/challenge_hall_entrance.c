/* >>> part includes */
#include "home/challenge_hall_entrance.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "generated/wram.h"
#include "home/scripting.h"
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
	/* `ld hl, .jump_table` then JumpToFunctionInTable leaves hl on the entry
	 * jumped to; the event helpers keep hl, so it is the exit value. A count
	 * of nine or more skips the table and keeps the table's own address. */
	static const uint16_t jump_table[9] = {
		(Preload_Clerk9__less_than_three_medals_ADDR), (Preload_Clerk9__less_than_three_medals_ADDR), (Preload_Clerk9__less_than_three_medals_ADDR), (Preload_Clerk9__three_medals_ADDR), (Preload_Clerk9__four_medals_ADDR), (Preload_Clerk9__five_medals_ADDR), (Preload_Clerk9__more_than_five_medals_ADDR), (Preload_Clerk9__more_than_five_medals_ADDR), (Preload_Clerk9__more_than_five_medals_ADDR),
	};
	result.hl = medals < 9u ? jump_table[medals] : (Preload_Clerk9__jump_table_ADDR);
	if (medals < 9u) {
		if (medals == 3u) {
			if (GetEventValue(EVENT_CHALLENGE_CUP_1_STATE) == CHALLENGE_CUP_NOT_STARTED) {
				result.c = CHALLENGE_CUP_READY_TO_START;
				SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_READY_TO_START);
			}
		} else if (medals == 5u) {
			/* challenge_hall_entrance.asm .five_medals: a not-yet-started cup 2
			 * becomes ready, and both paths continue into .four_medals, which
			 * closes cup 1. */
			if (GetEventValue(EVENT_CHALLENGE_CUP_2_STATE) == CHALLENGE_CUP_NOT_STARTED) {
				result.c = CHALLENGE_CUP_READY_TO_START;
				SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_READY_TO_START);
			}
			result.c = CHALLENGE_CUP_OVER;
			SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
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
	/* .less_than_three_medals: the first cup neither unstarted nor over is the
	 * one starting; the `cp` that sends a state to the next check leaves Z set
	 * under the exit's `scf`, and a started cup exits with MaxOutEventValue's
	 * flags and the hall's song in a. */
	uint8_t cup1 = GetEventValue(EVENT_CHALLENGE_CUP_1_STATE);
	result.a = cup1;
	uint8_t cup_number = 0u;
	if (cup1 != CHALLENGE_CUP_NOT_STARTED && cup1 != CHALLENGE_CUP_OVER) {
		cup_number = 1u;
	} else {
		uint8_t cup2 = GetEventValue(EVENT_CHALLENGE_CUP_2_STATE);
		result.a = cup2;
		if (cup2 != CHALLENGE_CUP_NOT_STARTED && cup2 != CHALLENGE_CUP_OVER) {
			cup_number = 2u;
		} else {
			uint8_t cup3 = GetEventValue(EVENT_CHALLENGE_CUP_3_STATE);
			result.a = cup3;
			if (cup3 != CHALLENGE_CUP_NOT_STARTED && cup3 != CHALLENGE_CUP_OVER)
				cup_number = 3u;
		}
	}
	if (cup_number == 0u) {
		result.f = 0x90u;
		return result;
	}
	result.c = cup_number;
	SetEventValue(EVENT_CHALLENGE_CUP_NUMBER, 0u, 0u, result.c);
	SetEventValueResult started = MaxOutEventValue(EVENT_CHALLENGE_CUP_STARTING, 0u, 0u, 0u);
	result.a = MUSIC_CHALLENGE_HALL;
	wDefaultSong = result.a;
	result.f = (uint8_t)((started.f & 0x80u) | 0x10u);
	return result;
}
/* <<< factory Preload_Clerk9 */
