#include "home/challenge_hall.h"

#include "generated/wram.h"
#include "mem.h"
#include "home/scripting.h"
#include "home/map.h"
#include "home/random.h"
#include "generated/wram.h"
#include "mem.h"
#define DUEL_WIN 0x00u
#define NPC_HOST 0x4Au
#define NPC_RONALD1 0x02u
#define CHALLENGE_HALL_BANK 3u
#define ChallengeHallAfterDuelTable_ADDR 0x7254u
#define EVENT_CHALLENGE_CUP_IN_MENU 0x47u
#define EVENT_CHALLENGE_CUP_STARTING 0x42u
#define EVENT_CHALLENGE_CUP_OPPONENT_CHOSEN 0x46u
#define EVENT_CHALLENGE_CUP_OPPONENT_NUMBER 0x45u
#define EVENT_CHALLENGE_CUP_NUMBER 0x44u
#define CHALLENGE_HALL_NPC_COUNT 25u
#define CHALLENGE_HALL_NPCS_ADDR 0x75B3u
#define CHALLENGE_HALL_SCRIPT_F433 0x7433u
/* <<< factory statics */

/* >>> factory ChallengeHallLoadMap */
/* challenge_hall.asm:22-30 */
ChallengeHallLoadMapResult ChallengeHallLoadMap(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t event = GetEventValue(EVENT_CHALLENGE_CUP_IN_MENU);
	if (event == 0u)
		return (ChallengeHallLoadMapResult){0u, 0x80u, b, c, hl};
	wTempNPC = NPC_HOST;
	(void)FindLoadedNPC();
	SetNextNPCAndScriptResult r = SetNextNPCAndScript(CHALLENGE_HALL_SCRIPT_F433, hl);
	return (ChallengeHallLoadMapResult){r.a, r.f, r.b, r.c, r.hl};
}
/* <<< factory ChallengeHallLoadMap */

/* >>> factory Preload_Guide */
/* challenge_hall.asm:36-46 */
PreloadGuideResult Preload_Guide(void)
{
	uint8_t event = GetEventValue(EVENT_CHALLENGE_CUP_STARTING);
	if (event != 0u) {
		wLoadNPCXPos = 0x1Cu;
		wLoadNPCYPos = 0x02u;
	}
	return (PreloadGuideResult){event != 0u ? 0x02u : 0u,
		event != 0u ? 0x10u : 0x90u};
}
/* <<< factory Preload_Guide */

/* >>> factory Preload_ChallengeHallOpponent */
/* challenge_hall.asm:437-456 */
PreloadChallengeHallOpponentResult Preload_ChallengeHallOpponent(void)
{
	uint8_t starting = GetEventValue(EVENT_CHALLENGE_CUP_STARTING);
	if (starting == 0u)
		return (PreloadChallengeHallOpponentResult){0u, 0x80u};
	uint8_t chosen = GetEventValue(EVENT_CHALLENGE_CUP_OPPONENT_CHOSEN);
	if (chosen != 0u) {
		wTempNPC = wChallengeHallNPC;
		return (PreloadChallengeHallOpponentResult){wTempNPC, 0x10u};
	}
	(void)Func_f5db();
	uint8_t opponent_number = (uint8_t)(GetEventValue(EVENT_CHALLENGE_CUP_OPPONENT_NUMBER) + 1u);
	(void)SetEventValue(EVENT_CHALLENGE_CUP_OPPONENT_NUMBER, 0u, 0u, opponent_number);
	uint8_t cup_number = GetEventValue(EVENT_CHALLENGE_CUP_NUMBER);
	uint8_t picked;
	if (cup_number != 3u && opponent_number == 3u) {
		picked = NPC_RONALD1;
	} else {
		uint8_t count = (cup_number == 3u) ? 25u : 24u;
		uint8_t index;
		do {
			index = Random(count);
		} while ((Func_f5cc(index).f & 0x10u) != 0u);
		(void)Func_f5d4(index);
		picked = gb_read8((uint16_t)(0x75B3u + index));
	}
	wTempNPC = picked;
	wChallengeHallNPC = picked;
	SetEventValueResult max = MaxOutEventValue(EVENT_CHALLENGE_CUP_OPPONENT_CHOSEN, 0u, 0u, 0u);
	return (PreloadChallengeHallOpponentResult){max.a, 0x10u};
}
/* <<< factory Preload_ChallengeHallOpponent */

ChallengeHallClearResult Func_f5db(void)
{
	gb_write8(wd698_ADDR + 0u, 0);
	gb_write8(wd698_ADDR + 1u, 0);
	gb_write8(wd698_ADDR + 2u, 0);
	gb_write8(wd698_ADDR + 3u, 0);
	return (ChallengeHallClearResult){0, 0x80u};
}

ChallengeHallBitResult Func_f5e9(uint8_t c)
{
	uint16_t hl = (uint16_t)(wd698_ADDR + (uint16_t)(c / 8u));
	uint8_t b = (uint8_t)(0x80u >> (c & 7u));
	return (ChallengeHallBitResult){b, hl};
}

void Script_Host(void)
{
}

/* >>> factory Func_f5cc */
/* challenge_hall.asm:517-523 */
ChallengeHallTestBitResult Func_f5cc(uint8_t c)
{
	ChallengeHallBitResult bit = Func_f5e9(c);
	uint8_t a = (uint8_t)(gb_read8(bit.hl) & bit.b);
	uint8_t f = a ? 0x10u : 0xA0u;
	return (ChallengeHallTestBitResult){a, f};
}
/* <<< factory Func_f5cc */

/* >>> factory Func_f5d4 */
/* challenge_hall.asm:525-530 */
ChallengeHallSetBitResult Func_f5d4(uint8_t c)
{
	ChallengeHallBitResult bit = Func_f5e9(c);
	uint8_t a = (uint8_t)(gb_read8(bit.hl) | bit.b);
	gb_write8(bit.hl, a);
	uint8_t f = a ? 0x00u : 0x80u;
	return (ChallengeHallSetBitResult){a, f};
}
/* <<< factory Func_f5d4 */

/* >>> factory ChallengeHallAfterDuel */
ChallengeHallAfterDuelResult ChallengeHallAfterDuel(void)
{
	uint8_t c = (wDuelResult == DUEL_WIN) ? 0u : 2u;
	const uint8_t *entry = rom_ptr(CHALLENGE_HALL_BANK, (uint16_t)(ChallengeHallAfterDuelTable_ADDR + c));
	uint16_t bc = (uint16_t)(entry[0] | ((uint16_t)entry[1] << 8));
	uint16_t hl = (uint16_t)(ChallengeHallAfterDuelTable_ADDR + c + 1u);
	wTempNPC = NPC_HOST;
	SetNextNPCAndScriptResult r = SetNextNPCAndScript(bc, hl);
	return (ChallengeHallAfterDuelResult){r.a, r.f, r.b, r.c, r.hl};
}
/* <<< factory ChallengeHallAfterDuel */
