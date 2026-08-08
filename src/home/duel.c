#include "home/duel.h"

#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/print_text.h"
#include "home/switch_sram.h"
#include "mem.h"

/* HIGH(wOpponentDuelVariables), the value hWhoseTurn carries on the opponent's turn. */
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))
#define PLAYER_TURN ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))

/* duel.asm:1316-1323: [hWhoseTurn << 8 | a], the current turn holder's duelvar a. */
DuelistVarResult GetTurnDuelistVariable(uint8_t a)
{
	uint16_t address = (uint16_t)(((uint16_t)hWhoseTurn << 8) | a);
	return (DuelistVarResult){gb_read8(address), address};
}

/* duel.asm:1325-1337: the other player's duelvar a. */
DuelistVarResult GetNonTurnDuelistVariable(uint8_t a)
{
	uint8_t turn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;
	uint16_t address = (uint16_t)(((uint16_t)turn << 8) | a);
	return (DuelistVarResult){gb_read8(address), address};
}

/* duel.asm:2364-2371: the other player becomes the turn holder. */
void SwapTurn(void)
{
	hWhoseTurn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;
}

/* Text ID of the fallback opponent name. */
#define PLAYER2_TEXT_ID 0x0092u

/* CopyPlayerName's `.loop` tail. CopyOpponentName's name-buffer path jumps straight
 * into it, so the DisableSRAM runs on that path too even though it never enabled SRAM. */
static CopyTextResult copy_name_loop(uint16_t hl, uint16_t de)
{
	uint8_t a;

	do {
		a = gb_read8(hl++);
		gb_write8(de++, a);
	} while (a);
	de--;
	DisableSRAM();
	return (CopyTextResult){a, (uint8_t)(de >> 8), (uint8_t)de, hl};
}

CopyTextResult CopyPlayerName(uint16_t de)
{
	EnableSRAM();
	return copy_name_loop(sPlayerName_ADDR, de);
}

CopyTextResult CopyOpponentName(uint16_t de)
{
	uint16_t name = (uint16_t)(gb_read8(wOpponentName_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wOpponentName_ADDR + 1u)) << 8);

	if (name)
		return CopyText(name, de);
	if (gb_read8(wNameBuffer_ADDR))
		return copy_name_loop(wNameBuffer_ADDR, de);
	return CopyText(PLAYER2_TEXT_ID, de);
}
