#include "home/grass_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/grass_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define GrassClubAfterDuelTable 0x66eeu
#define ISHIHARAS_HOUSE 0x03u
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
/* grass_club.asm:95-98 -- the routine's entire CODE portion, 8 bytes:
 *   ld a, [wCurMap] / cp ISHIHARAS_HOUSE / jp z, Script_NikkiInIshiharasHouse
 * Both exits enter script bytecode through a `rst $20`, so the routine has TWO
 * completion points and the cases declare one each:
 *   not taken -> the `start_script` rst at $67A6
 *   taken     -> Script_NikkiInIshiharasHouse, whose first byte is the rst
 *                at $5AE9
 * The routine's only real effect is choosing between them, which a per-routine
 * port cannot express as control flow -- so the decision is carried in `f`: Z
 * set means the jump is taken. Comparing `f` is therefore what verifies the
 * branch at all, and `cp_flags` models the full cp result (N always set, H and
 * C from the nibble/byte borrow), not just Z. */
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
