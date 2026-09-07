#include "home/grass_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/grass_club.h"
#include "home/grass_club_entrance.h"
#include "home/scripting.h"
#include "generated/wram.h"
#define GrassClubAfterDuelTable 0x66eeu
#define ISHIHARAS_HOUSE 0x03u
#define NIKKI_IN_GRASS_CLUB 0x02u
/* <<< factory statics */

/* >>> factory GrassClubAfterDuel */
GrassClubAfterDuelResult GrassClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubAfterDuelTable);
	return (GrassClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory GrassClubAfterDuel */

/* >>> factory Script_Nikki */
static uint8_t nikki_cp_flags(uint8_t a, uint8_t n)
{
	return (uint8_t)(0x40u
		| ((a == n) ? 0x80u : 0u)
		| (((a & 0x0Fu) < (n & 0x0Fu)) ? 0x20u : 0u)
		| ((a < n) ? 0x10u : 0u));
}

ScriptNikkiResult Script_Nikki(void)
{
	uint8_t map = gb_read8(wCurMap_ADDR);
	return (ScriptNikkiResult){map, nikki_cp_flags(map, ISHIHARAS_HOUSE)};
}
/* <<< factory Script_Nikki */

/* >>> factory Preload_NikkiInGrassClub */
PreloadNikkiInGrassClubResult Preload_NikkiInGrassClub(void)
{
	uint8_t a = GetEventValue(0x35u);
	uint8_t f = (uint8_t)((a == NIKKI_IN_GRASS_CLUB) ? 0x80u : 0u);
	if (a < NIKKI_IN_GRASS_CLUB)
		f |= 0x10u;
	return (PreloadNikkiInGrassClubResult){a, (uint8_t)(f ^ 0x10u)};
}
/* <<< factory Preload_NikkiInGrassClub */
