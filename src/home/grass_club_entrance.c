#include "home/grass_club_entrance.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/grass_club_entrance.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define DUEL_WIN 0x00u
#define PUPIL_DEFEATED 0x08u
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

/* >>> factory Preload_MichaelInGrassClubEntrance */
PreloadMichaelInGrassClubEntranceResult Preload_MichaelInGrassClubEntrance(void)
{
	uint8_t a = GetEventValue(0x11u);
	if (a == 0u)
		return (PreloadMichaelInGrassClubEntranceResult){a, 0x80u};
	uint8_t f = (uint8_t)(0x40u | ((a == PUPIL_DEFEATED) ? 0x80u : 0u)
		| (((a & 0x0Fu) < (PUPIL_DEFEATED & 0x0Fu)) ? 0x20u : 0u)
		| ((a < PUPIL_DEFEATED) ? 0x10u : 0u));
	return (PreloadMichaelInGrassClubEntranceResult){a, f};
}
/* <<< factory Preload_MichaelInGrassClubEntrance */
