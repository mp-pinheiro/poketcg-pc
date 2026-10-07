/* >>> part includes */
#include "home/fire_club_lobby.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "home/scripting.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/fire_club_lobby.h"
#include "generated/wram.h"
#include "mem.h"
#define SLOWPOKE_PAINTING_OBJECT_TABLE_ADDR_520 SlowpokePaintingObjectTable_ADDR

#include "home/grass_club_entrance.h"
#include "mem.h"
#define AFTER_DUEL_TABLE_830 (FireClubLobbyAfterDuel_ADDR + 0x06u)
/* <<< factory statics */

/* >>> factory FindExtraInteractableObjects */
FindExtraInteractableObjectsResult FindExtraInteractableObjects(uint16_t hl)
{
	uint16_t de = 6u;
	for (;;) {
		uint8_t a = gb_read8(hl);
		if (a == 0u)
			return (FindExtraInteractableObjectsResult){
				hl, 0u, 0u, (uint8_t)(de >> 8), (uint8_t)de, 0u};
		uint16_t entry_start = hl;
		if (gb_read8(wPlayerXCoord_ADDR) != gb_read8(hl))
			goto next;
		hl = (uint16_t)(hl + 1u);
		if (gb_read8(wPlayerYCoord_ADDR) != gb_read8(hl))
			goto next;
		hl = (uint16_t)(hl + 1u);
		if (gb_read8(wPlayerDirection_ADDR) != gb_read8(hl))
			goto next;
		hl = (uint16_t)(hl + 1u);
		uint8_t c = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t b = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t bank = gb_read8(hl);
		uint16_t next_hl = SetNextScript(bank, (uint16_t)(((uint16_t)b << 8) | c));
		return (FindExtraInteractableObjectsResult){
			next_hl, b, c, (uint8_t)(de >> 8), (uint8_t)de, 1u};
	next:
		hl = (uint16_t)(entry_start + de);
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
