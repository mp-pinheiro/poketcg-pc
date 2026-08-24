#include "home/fire_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/scripting.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/fire_club_lobby.h"
#include "generated/wram.h"
#include "mem.h"
#define SLOWPOKE_PAINTING_OBJECT_TABLE_ADDR_520 0x6D5Eu

#include "mem.h"
#define AFTER_DUEL_TABLE_830 0x6D50u
/* <<< factory statics */

/* >>> factory FindExtraInteractableObjects */
FindExtraInteractableObjectsResult FindExtraInteractableObjects(uint16_t hl)
{
	for (;;) {
		uint8_t a = gb_read8(hl);
		if (a == 0u)
			return (FindExtraInteractableObjectsResult){hl, 0u, 0u, 0u, 5u, 0u};
		uint16_t entry_start = hl;
		uint16_t cursor = hl;
		if (gb_read8(wPlayerXCoord_ADDR) == gb_read8(cursor)) {
			cursor = (uint16_t)(cursor + 1u);
			if (gb_read8(wPlayerYCoord_ADDR) == gb_read8(cursor)) {
				cursor = (uint16_t)(cursor + 1u);
				if (gb_read8(wPlayerDirection_ADDR) == gb_read8(cursor)) {
					cursor = (uint16_t)(cursor + 1u);
					uint8_t c = gb_read8(cursor);
					cursor = (uint16_t)(cursor + 1u);
					uint8_t b = gb_read8(cursor);
					uint16_t bc = (uint16_t)(c | ((uint16_t)b << 8));
					SetNextScript(bc);
					return (FindExtraInteractableObjectsResult){entry_start, b, c, 0u, 5u, 1u};
				}
			}
		}
		hl = (uint16_t)(entry_start + 5u);
	}
}
/* <<< factory FindExtraInteractableObjects */

/* >>> factory FireClubPressedA */
FireClubPressedAResult FireClubPressedA(void)
{
	FindExtraInteractableObjectsResult r = FindExtraInteractableObjects(SLOWPOKE_PAINTING_OBJECT_TABLE_ADDR_520);
	return (FireClubPressedAResult){r.hl, r.b, r.c, r.d, r.e, r.carry};
}
/* <<< factory FireClubPressedA */

/* >>> factory FireClubLobbyAfterDuel */
FindEndOfDuelScriptResult FireClubLobbyAfterDuel(void)
{
	return FindEndOfDuelScript(AFTER_DUEL_TABLE_830);
}
/* <<< factory FireClubLobbyAfterDuel */
