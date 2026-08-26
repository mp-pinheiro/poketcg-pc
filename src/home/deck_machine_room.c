#include "home/deck_machine_room.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define MAP_EVENT_FIGHTING_DECK_MACHINE 0x02u
#define MAP_EVENT_FIRE_DECK_MACHINE 0x09u

#include "home/grass_club_entrance.h"

#define DeckMachineRoomAfterDuelTable 0x58a6u

#include "generated/wram.h"
#define PKMN_CARD_DATA_LENGTH 0x41u

#include "home/deck_machine_room.h"
#include "home/scripting.h"
#include "home/map_events.h"
#include "generated/wram.h"
#include "mem.h"
#define EVENT_BEAT_NIKKI 0x08u
#define EVENT_GRASS_DECK_MACHINE_ACTIVE 0x5eu
#define MAP_EVENT_GRASS_DECK_MACHINE 0x06u

#include "home/deck_machine_room.h"
#include "home/scripting.h"
#include "home/print_text.h"
#include "home/menus.h"
#include "home/map_events.h"
#include "home/sound.h"
#include "generated/wram.h"
#include "mem.h"
#define EVENT_BEAT_AMY 0x0bu
#define EVENT_WATER_DECK_MACHINE_ACTIVE 0x5cu
#define MAP_EVENT_WATER_DECK_MACHINE 0x04u
#define SFX_INTRO_ORB_TITLE 0x5au

#define EVENT_BEAT_ISAAC 0x0cu
#define EVENT_LIGHTNING_DECK_MACHINE_ACTIVE 0x5du
#define MAP_EVENT_LIGHTNING_DECK_MACHINE 0x05u
/* <<< factory statics */
#define CLUB_MAP_NAMES 0x5985u
#define CLUB_MAP_NAMES_BANK 3u
#define EVENT_AARON_BOOSTER_REWARD_OFFSET 0x1Au
#define EVENT_AARON_BOOSTER_REWARD_MASK 0x03u
FuncD96cResult Func_d96c(uint8_t a){uint8_t offset=(uint8_t)((uint8_t)(a-2u)<<1);uint16_t hl=(uint16_t)(CLUB_MAP_NAMES+offset);const uint8_t *entry=rom_ptr(CLUB_MAP_NAMES_BANK,hl);uint8_t lo=entry[0],hi=entry[1];gb_write8(wTxRam2_ADDR,lo);gb_write8(wTxRam2_b_ADDR,lo);gb_write8((uint16_t)(wTxRam2_ADDR+1u),hi);return (FuncD96cResult){hi,0,offset,(uint16_t)(hl+1u)};}
/* >>> factory Script_BeatAaron */
/* deck_machine_room.asm:62-65 -- the routine's entire CODE portion, 8 bytes:
 *   ld a, [wMultichoiceTextboxResult_ChooseDeckToDuelAgainst] / ld c, a
 *   set_event_value EVENT_AARON_BOOSTER_REWARD
 * The macro is `call SetStackEventValue` + `db $73`; SetStackEventValue consumes
 * the db via GetByteAfterCall and returns PAST it, to the `rst $20` at $590B that
 * begins the script bytecode. So $590B is the end of this routine's code, and the
 * case declares completion pre-ret there. Full-script behaviour past the rst is
 * scene-level replay territory, not a per-routine port.
 *
 * SetEventValue computes [hl] = (~mask & [hl]) | ((c << tz(mask)) & mask) after
 * GetEventVar loads (offset, mask) from EventVarMasks[id*2]. Verified against the
 * ROM 2026-08-26: EventVarMasks[0x73] = (0x1A, 0x03); mask 0x03 has bit 0 set, so
 * the shift-alignment loop runs zero times and the value needs no shifting.
 * `a` holds the byte written, `c` the value read (push/pop bc restores `ld c, a`);
 * b, d, e and hl are preserved across the callee's push/pop pairs. */
ScriptBeatAaronResult Script_BeatAaron(void)
{
	uint8_t value = gb_read8(wMultichoiceTextboxResult_ChooseDeckToDuelAgainst_ADDR);
	uint16_t event_addr = (uint16_t)(wEventVars_ADDR + EVENT_AARON_BOOSTER_REWARD_OFFSET);
	uint8_t event = gb_read8(event_addr);
	uint8_t written;
	gb_write8(wLoadedEventBits_ADDR, EVENT_AARON_BOOSTER_REWARD_MASK);
	written = (uint8_t)((event & (uint8_t)~EVENT_AARON_BOOSTER_REWARD_MASK)
	                    | (value & EVENT_AARON_BOOSTER_REWARD_MASK));
	gb_write8(event_addr, written);
	return (ScriptBeatAaronResult){written, value};
}
/* <<< factory Script_BeatAaron */

/* >>> factory Script_d93f */
/* deck_machine_room.asm:97-99 -- the routine's entire CODE portion, 5 bytes:
 * `ld a, $02` / `call Func_d96c`. The `start_script` macro assembles to
 * `rst $20` at $5944: that is where the code ends and the script bytecode
 * begins, so the cases declare completion pre-ret there. RST20 pops its own
 * return address as a bytecode pointer and interprets the data that follows,
 * which needs ambient scene state a probed per-routine call cannot supply.
 * Func_d96c is already verified; this routine contributes the argument and the
 * call, and the pre-ret split is what makes those observable at all. Its outputs
 * are exactly Func_d96c's, so it reuses that result type rather than declaring an
 * identical one. */
FuncD96cResult Script_d93f(void)
{
	return Func_d96c(0x02u);
}
/* <<< factory Script_d93f */

/* >>> factory Script_d995 */
/* deck_machine_room.asm:150-152 -- the routine's entire CODE portion, 5 bytes:
 * `ld a, $03` / `call Func_d96c`. The `start_script` macro assembles to
 * `rst $20` at $599A: that is where the code ends and the script bytecode
 * begins, so the cases declare completion pre-ret there. RST20 pops its own
 * return address as a bytecode pointer and interprets the data that follows,
 * which needs ambient scene state a probed per-routine call cannot supply.
 * Func_d96c is already verified; this routine contributes the argument and the
 * call, and the pre-ret split is what makes those observable at all. Its outputs
 * are exactly Func_d96c's, so it reuses that result type rather than declaring an
 * identical one. */
FuncD96cResult Script_d995(void)
{
	return Func_d96c(0x03u);
}
/* <<< factory Script_d995 */

/* >>> factory Script_da49 */
/* deck_machine_room.asm:262-264 -- the routine's entire CODE portion, 5 bytes:
 * `ld a, $07` / `call Func_d96c`. The `start_script` macro assembles to
 * `rst $20` at $5A4E: that is where the code ends and the script bytecode
 * begins, so the cases declare completion pre-ret there. RST20 pops its own
 * return address as a bytecode pointer and interprets the data that follows,
 * which needs ambient scene state a probed per-routine call cannot supply.
 * Func_d96c is already verified; this routine contributes the argument and the
 * call, and the pre-ret split is what makes those observable at all. Its outputs
 * are exactly Func_d96c's, so it reuses that result type rather than declaring an
 * identical one. */
FuncD96cResult Script_da49(void)
{
	return Func_d96c(0x07u);
}
/* <<< factory Script_da49 */

/* >>> factory Script_daa3 */
/* deck_machine_room.asm:318-320 -- the routine's entire CODE portion, 5 bytes:
 * `ld a, $09` / `call Func_d96c`. The `start_script` macro assembles to
 * `rst $20` at $5AA8: that is where the code ends and the script bytecode
 * begins, so the cases declare completion pre-ret there. RST20 pops its own
 * return address as a bytecode pointer and interprets the data that follows,
 * which needs ambient scene state a probed per-routine call cannot supply.
 * Func_d96c is already verified; this routine contributes the argument and the
 * call, and the pre-ret split is what makes those observable at all. Its outputs
 * are exactly Func_d96c's, so it reuses that result type rather than declaring an
 * identical one. */
FuncD96cResult Script_daa3(void)
{
	return Func_d96c(0x09u);
}
/* <<< factory Script_daa3 */

/* >>> factory DeckMachineRoomCloseTextBox */
void DeckMachineRoomCloseTextBox(void)
{
	/* rebuild after probe reformat */
	for (uint8_t a = MAP_EVENT_FIGHTING_DECK_MACHINE; a <= MAP_EVENT_FIRE_DECK_MACHINE; a++)
		ApplyOWMapEventChangeIfEventSet(a);
}
/* <<< factory DeckMachineRoomCloseTextBox */

/* >>> factory DeckMachineRoomAfterDuel */
DeckMachineRoomAfterDuelResult DeckMachineRoomAfterDuel(void)
{
	gb_write8(0x2000u, 0x03u);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(DeckMachineRoomAfterDuelTable);
	return (DeckMachineRoomAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory DeckMachineRoomAfterDuel */

/* >>> factory Script_da76 */
void Script_da76(void)
{
	(void)Func_d96c(0x08u);
	uint8_t copy_length = PKMN_CARD_DATA_LENGTH;
	gb_write8(wLCDC_ADDR, (uint8_t)(0x80u | (uint8_t)(copy_length == PKMN_CARD_DATA_LENGTH ? 0u : 1u)));
}
/* <<< factory Script_da76 */

/* >>> factory Script_da1c */
void Script_da1c(void)
{
	FuncD96cResult result = Func_d96c(0x06u);
	if (GetEventValue(EVENT_GRASS_DECK_MACHINE_ACTIVE) == 0u &&
	    GetEventValue(EVENT_BEAT_NIKKI) != 0u) {
		(void)MaxOutEventValue(EVENT_GRASS_DECK_MACHINE_ACTIVE, 0u, 0u, 0u);
		ApplyOWMapEventChangeIfEventSet(MAP_EVENT_GRASS_DECK_MACHINE);
	}
	wLCDC = 0x80u;
	gb_write8(0xff40u, 0x80u);
	(void)result;
}
/* <<< factory Script_da1c */

/* >>> factory Script_d9c2 */
void Script_d9c2(void)
{
	FuncD96cResult card = Func_d96c(4u);
	(void)card;
	(void)PrintScrollableText_NoTextBoxLabel(0x0607u);
	if (GetEventValue(EVENT_WATER_DECK_MACHINE_ACTIVE) == 0u) {
		(void)PrintScrollableText_NoTextBoxLabel(0x0608u);
		if (GetEventValue(EVENT_BEAT_AMY) == 0u)
			return;
		HandleYesOrNoMenuResult first = YesOrNoMenuWithText(0x0609u);
		if ((first.f & 0x10u) != 0u)
			return;
		(void)MaxOutEventValue(EVENT_WATER_DECK_MACHINE_ACTIVE, 0u, 0u, 0u);
		SetOWMapEvent(MAP_EVENT_WATER_DECK_MACHINE);
		(void)PrintScrollableText_NoTextBoxLabel(0x060au);
	}
	HandleYesOrNoMenuResult second = YesOrNoMenuWithText(0x060bu);
	if ((second.f & 0x10u) != 0u)
		return;
	PlaySFX(SFX_INTRO_ORB_TITLE);
	gb_write8(wLCDC_ADDR, 0x80u);
}
/* <<< factory Script_d9c2 */

/* >>> factory Script_d9ef */
void Script_d9ef(void)
{
	FuncD96cResult card = Func_d96c(5u);
	(void)card;
	(void)PrintScrollableText_NoTextBoxLabel(0x0607u);
	if (GetEventValue(EVENT_LIGHTNING_DECK_MACHINE_ACTIVE) == 0u) {
		(void)PrintScrollableText_NoTextBoxLabel(0x0608u);
		if (GetEventValue(EVENT_BEAT_ISAAC) == 0u)
			return;
		HandleYesOrNoMenuResult first = YesOrNoMenuWithText(0x0609u);
		if ((first.f & 0x10u) != 0u)
			return;
		(void)MaxOutEventValue(EVENT_LIGHTNING_DECK_MACHINE_ACTIVE, 0u, 0u, 0u);
		SetOWMapEvent(MAP_EVENT_LIGHTNING_DECK_MACHINE);
		(void)PrintScrollableText_NoTextBoxLabel(0x060au);
	}
	HandleYesOrNoMenuResult second = YesOrNoMenuWithText(0x060bu);
	if ((second.f & 0x10u) != 0u)
		return;
	PlaySFX(SFX_INTRO_ORB_TITLE);
	gb_write8(wLCDC_ADDR, 0x80u);
}
/* <<< factory Script_d9ef */
