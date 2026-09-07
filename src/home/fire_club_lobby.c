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

#include "home/grass_club_entrance.h"
#include "mem.h"
#define AFTER_DUEL_TABLE_830 0x6D50u
#define EVENT_LAD2_STATE 0x21u
#define LAD2_SLOWPOKE_AVAILABLE 0x01u
#define EVENT_PUPIL_JESSICA_STATE 0x20u
#define PUPIL_DEFEATED 0x08u
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
FireClubLobbyAfterDuelResult FireClubLobbyAfterDuel(void)
{
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(AFTER_DUEL_TABLE_830);
	return (FireClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory FireClubLobbyAfterDuel */

/* >>> factory Preload_Lad2 */
/* fire_club_lobby.asm:150-153: `cp LAD2_SLOWPOKE_AVAILABLE` on the event value; carry loads the NPC. */
PreloadLad2Result Preload_Lad2(void)
{
	uint8_t a = GetEventValue(EVENT_LAD2_STATE);
	uint8_t f = 0x40u;
	if (a == LAD2_SLOWPOKE_AVAILABLE)
		f |= 0x80u;
	if ((a & 0x0Fu) < (LAD2_SLOWPOKE_AVAILABLE & 0x0Fu))
		f |= 0x20u;
	if (a < LAD2_SLOWPOKE_AVAILABLE)
		f |= 0x10u;
	return (PreloadLad2Result){a, f};
}
/* <<< factory Preload_Lad2 */

/* >>> factory Preload_JessicaInFireClubLobby */
/* fire_club_lobby.asm:58-63: `or a` returns an inactive pupil with Z; otherwise
 * `cp PUPIL_DEFEATED`, whose carry -- not yet defeated -- loads the pupil. */
PreloadJessicaInFireClubLobbyResult Preload_JessicaInFireClubLobby(void)
{
	uint8_t a = GetEventValue(EVENT_PUPIL_JESSICA_STATE);
	if (a == 0u)
		return (PreloadJessicaInFireClubLobbyResult){a, 0x80u};
	uint8_t f = 0x40u;
	if (a == PUPIL_DEFEATED)
		f |= 0x80u;
	if ((a & 0x0Fu) < (PUPIL_DEFEATED & 0x0Fu))
		f |= 0x20u;
	if (a < PUPIL_DEFEATED)
		f |= 0x10u;
	return (PreloadJessicaInFireClubLobbyResult){a, f};
}
/* <<< factory Preload_JessicaInFireClubLobby */
