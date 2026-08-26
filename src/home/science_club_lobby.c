#include "home/science_club_lobby.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define DATA_EBE7 0x6BE7u
#define DATA_EBE7_BANK 3u
#include "home/science_club_lobby.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define ScienceClubLobbyAfterDuelTable 0x6b5eu
/* <<< factory statics */

/* >>> factory ScienceClubLobbyAfterDuel */
ScienceClubLobbyAfterDuelResult ScienceClubLobbyAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(ScienceClubLobbyAfterDuelTable);
	return (ScienceClubLobbyAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory ScienceClubLobbyAfterDuel */

/* >>> factory Script_Specs2 */
/* science_club_lobby.asm:68-81 -- the routine's entire CODE portion, 24 bytes,
 * straight-line with a single exit. The `start_script` macro assembles to
 * `rst $20` at $6BDD, where the code ends and the script bytecode begins, so
 * the cases declare completion pre-ret there.
 *
 * `and %11` keeps the low two bits of UpdateRNGSources' return, indexing a
 * four-entry card-id table at Data_ebe7 (03:6BE7). GetCardName returns the new
 * `de`, which is stored little-endian to wTxRam2 by `ld [hli],a` / `ld [hl],d`,
 * leaving hl at wTxRam2+1. `d` is zeroed before the call, so only `e` carries
 * the table byte in. */
ScriptSpecs2Result Script_Specs2(void)
{
	uint8_t rng = UpdateRNGSources();
	uint8_t c = (uint8_t)(rng & 0x03u);
	uint16_t hl = (uint16_t)(DATA_EBE7 + c);
	uint8_t e = rom_ptr(DATA_EBE7_BANK, hl)[0];
	uint16_t de = GetCardName(e);
	hl = wTxRam2_ADDR;
	gb_write8(hl, (uint8_t)(de & 0xFFu));
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, (uint8_t)(de >> 8));
	return (ScriptSpecs2Result){(uint8_t)(de & 0xFFu), 0u, c,
	                            (uint8_t)(de >> 8), (uint8_t)(de & 0xFFu), hl};
}
/* <<< factory Script_Specs2 */
