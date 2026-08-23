#include "home/mason_laboratory.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define MASON_LAB_IN_PRACTICE_DUEL 0x01u
/* EVENT_MASON_LAB_STATE bitfield location (scripting.asm EventVarMasks): byte
 * wEventVars+0x0D, bits 1-3. */
#define EVENT_MASON_LAB_STATE_BYTE_OFFSET 0x0Du
#define EVENT_MASON_LAB_STATE_MASK 0x0Eu
#define EVENT_MASON_LAB_STATE_SHIFT 1u

#include "home/grass_club_entrance.h"
#define MasonLaboratoryAfterDuelTable 0x5542u
/* <<< factory statics */

/* >>> factory Preload_DrMason */
/* mason_laboratory.asm:276-287. Func_d703's SetOWMapEvent branch (unported;
 * map_events.asm) never affects this routine's a/f or wLoadNPCXPos/Y and is
 * not reproduced. */
PreloadDrMasonResult Preload_DrMason(void)
{
	uint8_t event_byte = gb_read8((uint16_t)(wEventVars_ADDR + EVENT_MASON_LAB_STATE_BYTE_OFFSET));
	uint8_t state = (uint8_t)((event_byte & EVENT_MASON_LAB_STATE_MASK) >> EVENT_MASON_LAB_STATE_SHIFT);
	uint8_t a = state;
	uint8_t f = 0x10u;

	if (state == MASON_LAB_IN_PRACTICE_DUEL) {
		gb_write8(wLoadNPCXPos_ADDR, 0x06u);
		gb_write8(wLoadNPCYPos_ADDR, 0x0Cu);
		a = 0x0Cu;
		f = 0x90u;
	}
	return (PreloadDrMasonResult){a, f};
}
/* <<< factory Preload_DrMason */

/* >>> factory MasonLaboratoryAfterDuel */
MasonLaboratoryAfterDuelResult MasonLaboratoryAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(MasonLaboratoryAfterDuelTable);
	return (MasonLaboratoryAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory MasonLaboratoryAfterDuel */
