#include "home/psychic_club.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/psychic_club.h"
#include "home/grass_club_entrance.h"
#include "generated/wram.h"
#define PsychicClubAfterDuelTable 0x6a4du

#include "home/scripting.h"
#include "mem.h"
#define EVENT_MEDAL_COUNT_530 0x2Eu

#include "home/psychic_club.h"
#include "mem.h"
/* <<< factory statics */

/* >>> factory PsychicClubAfterDuel */
PsychicClubAfterDuelResult PsychicClubAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(PsychicClubAfterDuelTable);
	return (PsychicClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory PsychicClubAfterDuel */

/* >>> factory Preload_Murray2 */
Preload_Murray2Result Preload_Murray2(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)TryGiveMedalPCPacks(b, c, d, e, hl);
	uint8_t a = GetEventValue(EVENT_MEDAL_COUNT_530);
	uint8_t f = 0x40u;
	if (a == 4u)
		f |= 0x80u;
	if ((a & 0x0Fu) < 4u)
		f |= 0x20u;
	if (a < 4u)
		f |= 0x10u;
	return (Preload_Murray2Result){a, f};
}
/* <<< factory Preload_Murray2 */

/* >>> factory Preload_Murray1 */
Preload_Murray2Result Preload_Murray1(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	Preload_Murray2Result r = Preload_Murray2(b, c, d, e, hl);
	uint8_t old_c = (uint8_t)(r.f & 0x10u);
	uint8_t new_f = (uint8_t)((r.f & 0x80u) | (old_c ? 0u : 0x10u));
	return (Preload_Murray2Result){r.a, new_f};
}
/* <<< factory Preload_Murray1 */
