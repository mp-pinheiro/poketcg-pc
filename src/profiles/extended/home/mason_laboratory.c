/* >>> part includes */
#include "home/mason_laboratory.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "home/card_collection.h"
#define ENERGY_CARD_LIST EnergyCardList_ADDR
#define ENERGY_CARD_LIST_BANK 3u
#define ENERGY_CARD_LIST_LEN 6u

#include "home/grass_club_entrance.h"
#define MasonLaboratoryAfterDuelTable (MasonLaboratoryAfterDuel_ADDR + 0x06u)

#include "home/fire_club_lobby.h"
#include "home/map.h"
#include "home/overworld.h"
#include "home/scripting.h"
#include "home/map_events.h"
#define SCRIPT_ENTER_LAB_FIRST_TIME Script_EnterLabFirstTime_ADDR
#define CHALLENGE_MACHINE_OBJECT_TABLE ChallengeMachineObjectTable_ADDR
/* <<< factory statics */

/* >>> factory Func_d703 */
FuncD703Result Func_d703(void)
{
	uint8_t event = GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS);
	if (event == 0u)
		return (FuncD703Result){0u, 0x80u};
	return (FuncD703Result){SetOWMapEvent(MAP_EVENT_CHALLENGE_MACHINE), 0u};
}
/* <<< factory Func_d703 */

/* >>> factory Preload_DrMason */
PreloadDrMasonResult Preload_DrMason(void)
{
	if (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) != 0u)
		(void)SetOWMapEvent(MAP_EVENT_CHALLENGE_MACHINE);

	uint8_t state = GetEventValue(EVENT_MASON_LAB_STATE);
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

/* >>> factory Preload_Sam */
/* mason_laboratory.asm Preload_Sam: before the practice duel Sam stands at
 * the table, ($0a,$08) facing south; from MASON_LAB_IN_PRACTICE_DUEL on the
 * map data's own position stands. `cp 1` then `scf`: Z survives the scf, so f
 * is $90 exactly when the state is 1, and a is SOUTH on the moved branch. The
 * get_event_value macro is GetStackEventValue, which also parks the event's
 * mask in wLoadedEventBits through GetEventVar. */
PreloadSamResult Preload_Sam(void)
{
	uint8_t state = GetEventValue(EVENT_MASON_LAB_STATE);
	uint8_t a = state;
	uint8_t f = state == MASON_LAB_IN_PRACTICE_DUEL ? 0x90u : 0x10u;

	if (state < MASON_LAB_IN_PRACTICE_DUEL) {
		gb_write8(wLoadNPCXPos_ADDR, 0x0Au);
		gb_write8(wLoadNPCYPos_ADDR, 0x08u);
		gb_write8(wLoadNPCDirection_ADDR, SOUTH);
		a = SOUTH;
	}
	return (PreloadSamResult){a, f};
}
/* <<< factory Preload_Sam */

/* >>> factory Preload_Tech5 */
/* mason_laboratory.asm Preload_Tech5: once the legendary cards are received
 * the technician stands two tiles to the right. Z comes from `or a` on the
 * skip path and from the second `inc [hl]` on the moved one (an X of $FE
 * wraps to zero); `scf` then sets carry and leaves Z alone, with hl pointing
 * at wLoadNPCXPos on the moved branch. */
PreloadTech5Result Preload_Tech5(uint16_t hl)
{
	uint8_t value = GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS);
	uint8_t zero = value == 0u;

	if (value != 0u) {
		hl = wLoadNPCXPos_ADDR;
		uint8_t moved = (uint8_t)(gb_read8(hl) + 2u);
		gb_write8(hl, moved);
		zero = moved == 0u;
	}
	return (PreloadTech5Result){value, zero ? 0x90u : 0x10u, hl};
}
/* <<< factory Preload_Tech5 */

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

/* >>> factory MasonLabLoadMap */
/* mason_laboratory.asm:21-29. `ret nc` when the lab state has reached
 * MASON_LAB_RECEIVED_STARTER_DECK, otherwise Dr Mason is looked up and the
 * first-visit script is queued by a tail jump. No caller reads the exit
 * registers: the LOAD_MAP slot's flags reach LoadMap through Func_c17a, which
 * discards them. */
void MasonLabLoadMap(void)
{
	if (GetEventValue(EVENT_MASON_LAB_STATE) >= MASON_LAB_RECEIVED_STARTER_DECK)
		return;
	wTempNPC = NPC_DRMASON;
	(void)FindLoadedNPC();
	(void)SetNextNPCAndScript(SCRIPT_ENTER_LAB_FIRST_TIME, 0u);
}
/* <<< factory MasonLabLoadMap */

/* >>> factory MasonLabPressedA */
/* mason_laboratory.asm:31-37. `or a / ret z` exits with carry clear before the
 * legendary cards are received; afterwards the challenge machine's object table
 * is searched and that search's carry is the result, which FindNPCOrObject
 * reads to decide whether to enter script mode. */
MasonLabPressedAResult MasonLabPressedA(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	if (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) == 0u)
		return (MasonLabPressedAResult){hl, b, c, d, e, 0u};

	FindExtraInteractableObjectsResult found =
		FindExtraInteractableObjects(CHALLENGE_MACHINE_OBJECT_TABLE);

	return (MasonLabPressedAResult){found.hl, found.b, found.c, found.d,
					found.e, found.carry};
}
/* <<< factory MasonLabPressedA */

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
		const uint8_t *entry = rom_ptr(ENERGY_CARD_LIST_BANK, hl);
		CardId id = (CardId)(entry[0] | ((uint16_t)entry[1] << 8));
		hl = (uint16_t)(hl + 2u);
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
		const uint8_t *entry = rom_ptr(ENERGY_CARD_LIST_BANK, hl);
		CardId id = (CardId)(entry[0] | ((uint16_t)entry[1] << 8));
		hl = (uint16_t)(hl + 2u);
		a = (uint8_t)id;
		do {
			AddCardToCollection(id);
			b--;
		} while (b != 0u);
		c--;
	} while (c != 0u);
	return (ScriptTech1Result){a, b, c, hl};
}
/* <<< factory Script_Tech1 */
