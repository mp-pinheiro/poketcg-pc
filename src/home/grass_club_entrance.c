#include "home/grass_club_entrance.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/grass_club_entrance.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define DUEL_WIN 0x00u

#define GrassClubEntranceAfterDuelTable 0x6553u
/* <<< factory statics */

/* >>> factory FindEndOfDuelScript */
FindEndOfDuelScriptResult FindEndOfDuelScript(uint16_t hl)
{
	uint8_t c = 0u;
	if (wDuelResult != DUEL_WIN)
		c = 2u;
	uint8_t b = wNPCDuelist;
	uint8_t a;
	for (;;) {
		a = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (a == 0u)
			return (FindEndOfDuelScriptResult){0u, 0x80u, b, c, 0u, 5u, hl};
		if (a == b)
			break;
		hl = (uint16_t)(hl + 5u);
	}
	a = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	wTempNPC = a;
	hl = (uint16_t)(hl + c);
	uint8_t lo = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint8_t hi = gb_read8(hl);
	SetNextNPCAndScriptResult r = SetNextNPCAndScript((uint16_t)((uint16_t)hi << 8 | lo), hl);
	return (FindEndOfDuelScriptResult){r.a, r.f, r.b, r.c, 0u, 5u, r.hl};
}
/* <<< factory FindEndOfDuelScript */

/* >>> factory GrassClubEntranceAfterDuel */
FindEndOfDuelScriptResult GrassClubEntranceAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	return FindEndOfDuelScript(GrassClubEntranceAfterDuelTable);
}
/* <<< factory GrassClubEntranceAfterDuel */
