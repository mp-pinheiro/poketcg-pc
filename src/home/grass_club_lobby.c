/* >>> part includes */
#include "home/grass_club_lobby.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/grass_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
/* <<< part includes_2 */
/* >>> part GrassClubLobbyAfterDuelTable */
#define GrassClubLobbyAfterDuelTable (GrassClubLobbyAfterDuel__after_duel_table_ADDR)
/* <<< part GrassClubLobbyAfterDuelTable */
/* >>> part includes_TRUE */
#include "home/scripting.h"
/* <<< part includes_TRUE */
/* >>> part TRUE */
#define TRUE 0x01u
/* <<< part TRUE */

/* >>> factory GrassClubLobbyAfterDuel */
GrassClubLobbyAfterDuelResult GrassClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, GrassClubLobbyAfterDuel__after_duel_table_BANK);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(GrassClubLobbyAfterDuelTable);
	return (GrassClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory GrassClubLobbyAfterDuel */

/* >>> factory Preload_Gal2 */
/* grass_club_lobby.asm:133-136: `cp TRUE` on the event value; carry loads the NPC. */
PreloadGal2Result Preload_Gal2(void)
{
	uint8_t a = GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS);
	uint8_t f = 0x40u;
	if (a == TRUE)
		f |= 0x80u;
	if ((a & 0x0Fu) < (TRUE & 0x0Fu))
		f |= 0x20u;
	if (a < TRUE)
		f |= 0x10u;
	return (PreloadGal2Result){a, f};
}
/* <<< factory Preload_Gal2 */
