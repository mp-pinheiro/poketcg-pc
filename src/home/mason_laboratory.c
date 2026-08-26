#include "home/mason_laboratory.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/card_collection.h"
#define ENERGY_CARD_LIST 0x55C4u
#define ENERGY_CARD_LIST_BANK 3u
#define ENERGY_CARD_LIST_LEN 6u
#define MASON_LAB_IN_PRACTICE_DUEL 0x01u
/* EVENT_MASON_LAB_STATE bitfield location (scripting.asm EventVarMasks): byte
 * wEventVars+0x0D, bits 1-3. */
#define EVENT_MASON_LAB_STATE_BYTE_OFFSET 0x0Du
#define EVENT_MASON_LAB_STATE_MASK 0x0Eu
#define EVENT_MASON_LAB_STATE_SHIFT 1u

#include "home/grass_club_entrance.h"
#define MasonLaboratoryAfterDuelTable 0x5542u

#define MAP_EVENT_CHALLENGE_MACHINE 0x0au
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

/* >>> factory MasonLabCloseTextBox */
void MasonLabCloseTextBox(void)
{
	ApplyOWMapEventChangeIfEventSet(MAP_EVENT_CHALLENGE_MACHINE);
}
/* <<< factory MasonLabCloseTextBox */

/* >>> factory Script_Tech1 */
/* mason_laboratory.asm:58-90. Two paths, each ending in its own `rst $20`:
 *   total >= 10 -> the `start_script` rst at $5597
 *   total <  10 -> .low_on_energies adds 10 of each of the six energy cards,
 *                  then reaches the rst at $55B5
 * The cases declare one completion pc each. Both paths are implemented here --
 * verifying only the counting prefix would be a simplification, not a port.
 *
 * EnergyCardList (03:55C4, six bytes 01..06) is walked by `ld a, [hli]`, so hl
 * ends at EnergyCardList.end = $55CA on both paths. The count loop keeps the
 * running total in b (`add b` / `ld b, a`) and is a do/while: `dec c` / `jr nz`
 * sits at the bottom, and c starts at 6.
 *
 * On the low path `push af` / `pop af` around AddCardToCollection restores the
 * card id every iteration, so `a` ends holding the LAST card id (6), while both
 * loop counters land on zero. */
ScriptTech1Result Script_Tech1(void)
{
	uint8_t b = 0u;
	uint8_t c = ENERGY_CARD_LIST_LEN;
	uint16_t hl = ENERGY_CARD_LIST;
	uint8_t a;

	do {
		uint8_t id = rom_ptr(ENERGY_CARD_LIST_BANK, hl)[0];
		hl = (uint16_t)(hl + 1u);
		a = GetCardCountInCollection(id).a;
		a = (uint8_t)(a + b);
		b = a;
		c--;
	} while (c != 0u);

	a = b;
	if (a >= 10u)
		return (ScriptTech1Result){a, b, c, hl};

	c = ENERGY_CARD_LIST_LEN;
	hl = ENERGY_CARD_LIST;
	do {
		b = 10u;
		a = rom_ptr(ENERGY_CARD_LIST_BANK, hl)[0];
		hl = (uint16_t)(hl + 1u);
		do {
			AddCardToCollection(a);
			b--;
		} while (b != 0u);
		c--;
	} while (c != 0u);
	return (ScriptTech1Result){a, b, c, hl};
}
/* <<< factory Script_Tech1 */
