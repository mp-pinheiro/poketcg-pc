#include "home/scripting.h"

#include "generated/wram.h"
#include "mem.h"

/* >>> factory statics */
#define EVENT_VAR_MASKS_BANK 3u
#define EVENT_VAR_MASKS 0x4B37u

static uint8_t adc_zero_flags(uint8_t old, uint8_t result, uint8_t carry)
{
	uint8_t flags = result == 0 ? 0x80u : 0u;
	if (((old & 0x0Fu) + carry) > 0x0Fu)
		flags |= 0x20u;
	if ((uint16_t)old + carry > 0xFFu)
		flags |= 0x10u;
	return flags;
}

#include "home/scripting.h"

#include "home/card_collection.h"
#include "home/scripting.h"

#include "home/card_collection.h"

#include "home/play_song.h"

#include "home/scripting.h"
#include "home/sound.h"

#include "home/masters_beaten_list.h"
#include "home/scripting.h"

#define GAME_EVENT_CHALLENGE_MACHINE 0x06u

#include "home/map.h"
#include "home/play_song.h"
#include "home/sound.h"

#include "generated/wram.h"
#include "home/card_data.h"
#include "home/lcd_enable_frame.h"
#include "home/map.h"
#include "home/npc_core.h"
#include "mem.h"

#define CONSOLE_CGB                  0x02u
#define EVENT_MAN1_REQUESTED_CARD_ID 0x2bu
#define LOADED_NPC_FLAGS             0x05u
#define NPC_FLAG_DIRECTIONLESS_F     0x04u

#define TRUE                     0x01u
#define GAME_EVENT_BATTLE_CENTER 0x02u

#include "home/scripting.h"
#include "generated/wram.h"
#include "mem.h"

/* scripting.asm:1400. MapNames is a table of 12 tx (2-byte) name pointers
 * sitting right after ScriptCommand_LoadCurrentMapNameIntoTxRamSlot in the
 * overworld script bank. The routine does not switch banks itself, so the
 * table is reached through ordinary bus reads at this $4000-$7fff window
 * offset. */
#define MAP_NAMES 0x7080u
/* <<< factory statics */


/* >>> factory IncreaseScriptPointer */
/* scripting.asm:594-602 */
IncreaseScriptPointerResult IncreaseScriptPointer(uint8_t a)
{
	uint8_t low = gb_read8(wScriptPointer_ADDR);
	uint8_t high = gb_read8((uint16_t)(wScriptPointer_ADDR + 1u));
	uint16_t low_sum = (uint16_t)low + a;
	uint8_t carry = (uint8_t)(low_sum > 0xFFu);
	uint8_t new_low = (uint8_t)low_sum;
	uint8_t new_high = (uint8_t)(high + carry);

	gb_write8(wScriptPointer_ADDR, new_low);
	gb_write8((uint16_t)(wScriptPointer_ADDR + 1u), new_high);
	return (IncreaseScriptPointerResult){new_high,
	                                     adc_zero_flags(high, new_high, carry), a};
}
/* <<< factory IncreaseScriptPointer */


/* >>> factory SetScriptPointer */
/* scripting.asm:604-609 */
uint16_t SetScriptPointer(uint16_t bc)
{
	gb_write8(wScriptPointer_ADDR, (uint8_t)bc);
	gb_write8((uint16_t)(wScriptPointer_ADDR + 1u), (uint8_t)(bc >> 8));
	return (uint16_t)(wScriptPointer_ADDR + 1u);
}
/* <<< factory SetScriptPointer */


/* >>> factory GetScriptArgsAfterPointer */
/* scripting.asm:625-639 */
GetScriptArgsAfterPointerResult GetScriptArgsAfterPointer(uint8_t a)
{
	uint16_t pointer = (uint16_t)(gb_read8(wScriptPointer_ADDR) |
	                             ((uint16_t)gb_read8((uint16_t)(wScriptPointer_ADDR + 1u)) << 8));
	uint16_t target = (uint16_t)(pointer + a);
	uint8_t low = gb_read8(target);
	uint8_t high = gb_read8((uint16_t)(target + 1u));
	uint8_t value = (uint8_t)(low | high);
	return (GetScriptArgsAfterPointerResult){value, value == 0 ? 0x80u : 0u,
	                                         high, low};
}
/* <<< factory GetScriptArgsAfterPointer */


/* >>> factory GetEventVar */
/* scripting.asm:366-382 */
GetEventVarResult GetEventVar(uint8_t a, uint8_t f, uint8_t b, uint8_t c)
{
	(void)f;
	uint16_t bc = (uint16_t)a * 2u;
	uint16_t table_addr = (uint16_t)(EVENT_VAR_MASKS + bc);
	const uint8_t *entry = rom_ptr(EVENT_VAR_MASKS_BANK, table_addr);
	uint8_t flags = (bc & 0xFF00u) == 0 ? 0x80u : 0u;
	uint8_t offset = entry[0];
	if (((wEventVars_ADDR & 0x0FFFu) + (offset & 0x0FFFu)) > 0x0FFFu)
		flags |= 0x20u;
	if ((uint32_t)wEventVars_ADDR + offset > 0xFFFFu)
		flags |= 0x10u;

	gb_write8(wLoadedEventBits_ADDR, entry[1]);
	return (GetEventVarResult){entry[1], flags, b, c,
	                           (uint16_t)(wEventVars_ADDR + entry[0])};
}
/* <<< factory GetEventVar */

/* >>> factory IncreaseScriptPointerBy1 */
/* scripting.asm:568-570 */
IncreaseScriptPointerResult IncreaseScriptPointerBy1(void)
{
	return IncreaseScriptPointer(1u);
}
/* <<< factory IncreaseScriptPointerBy1 */

/* >>> factory IncreaseScriptPointerBy2 */
/* scripting.asm:572-574 */
IncreaseScriptPointerResult IncreaseScriptPointerBy2(void)
{
	return IncreaseScriptPointer(2u);
}
/* <<< factory IncreaseScriptPointerBy2 */

/* >>> factory IncreaseScriptPointerBy4 */
/* scripting.asm:576-578 */
IncreaseScriptPointerResult IncreaseScriptPointerBy4(void)
{
	return IncreaseScriptPointer(4u);
}
/* <<< factory IncreaseScriptPointerBy4 */

/* >>> factory IncreaseScriptPointerBy3 */
/* scripting.asm:592-593. ld a,3 then fallthrough into IncreaseScriptPointer. */
IncreaseScriptPointerResult IncreaseScriptPointerBy3(void)
{
	return IncreaseScriptPointer(3u);
}
/* <<< factory IncreaseScriptPointerBy3 */

/* >>> factory GetScriptArgs5AfterPointer */
/* scripting.asm:611-613. Tail-jump wrapper: `ld a, 5` then `jr` into
 * GetScriptArgsAfterPointer, so it fixes the arg offset to 5 and shares the
 * callee's entire exit contract (a, f, b, c; d, e, hl preserved). Modeled
 * as a plain call to the already-ported callee. */
GetScriptArgsAfterPointerResult GetScriptArgs5AfterPointer(void)
{
	return GetScriptArgsAfterPointer(5u);
}
/* <<< factory GetScriptArgs5AfterPointer */

/* >>> factory SetScriptControlByteFail */
/* scripting.asm:646-649. xor a yields a=$00 with Z set and N/H/C clear
 * (f=$80 exactly, independent of the entry flags); the store to
 * wScriptControlByte does not affect flags. */
SetScriptControlByteFailResult SetScriptControlByteFail(void)
{
	wScriptControlByte = 0x00u;
	return (SetScriptControlByteFailResult){0x00u, 0x80u};
}
/* <<< factory SetScriptControlByteFail */

/* >>> factory IncreaseScriptPointerBy5 */
/* scripting.asm:580-582. Tail-jumps into IncreaseScriptPointer with a = 5, so the
 * caller observes IncreaseScriptPointer's exit registers (a, f, c) directly. */
IncreaseScriptPointerResult IncreaseScriptPointerBy5(void)
{
	return IncreaseScriptPointer(5u);
}
/* <<< factory IncreaseScriptPointerBy5 */

/* >>> factory IncreaseScriptPointerBy6 */
/* scripting.asm:584-586. Tail-jumps into IncreaseScriptPointer with a = 6, so the
 * caller observes IncreaseScriptPointer's exit registers (a, f, c) directly. */
IncreaseScriptPointerResult IncreaseScriptPointerBy6(void)
{
	return IncreaseScriptPointer(6u);
}
/* <<< factory IncreaseScriptPointerBy6 */

/* >>> factory IncreaseScriptPointerBy7 */
/* scripting.asm:588-590. Tail-jumps into IncreaseScriptPointer with a = 7, so the
 * caller observes IncreaseScriptPointer's exit registers (a, f, c) directly. */
IncreaseScriptPointerResult IncreaseScriptPointerBy7(void)
{
	return IncreaseScriptPointer(7u);
}
/* <<< factory IncreaseScriptPointerBy7 */

/* >>> factory GetScriptArgs2AfterPointer */
/* scripting.asm:619-621 */
GetScriptArgsAfterPointerResult GetScriptArgs2AfterPointer(void)
{
	return GetScriptArgsAfterPointer(2u);
}
/* <<< factory GetScriptArgs2AfterPointer */

/* >>> factory GetScriptArgs3AfterPointer */
/* scripting.asm:623-624 */
GetScriptArgsAfterPointerResult GetScriptArgs3AfterPointer(void)
{
	return GetScriptArgsAfterPointer(3u);
}
/* <<< factory GetScriptArgs3AfterPointer */

/* >>> factory SetScriptControlBytePass */
/* scripting.asm:641-645 */
uint8_t SetScriptControlBytePass(void)
{
	wScriptControlByte = 0xffu;
	return 0xffu;
}
/* <<< factory SetScriptControlBytePass */

/* >>> factory ScriptCommand_JumpIfCardInCollection */
/* scripting.asm:1019-1036 */
JumpIfCardInCollectionResult ScriptCommand_JumpIfCardInCollection(uint8_t b, uint8_t c)
{
	CardCountResult cnt = GetCardCountInCollection(c);
	if (cnt.a == 0) {
		SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
		return (JumpIfCardInCollectionResult){r.a, r.f, b, r.c};
	}
	SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs2AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
		return (JumpIfCardInCollectionResult){r.a, r.f, args.b, r.c};
	}
	(void)SetScriptPointer((uint16_t)(args.b << 8 | args.c));
	return (JumpIfCardInCollectionResult){args.a, args.f, args.b, args.c};
}
/* <<< factory ScriptCommand_JumpIfCardInCollection */

/* >>> factory ScriptCommand_GiveCard */
/* scripting.asm:1056-1063 */
IncreaseScriptPointerResult ScriptCommand_GiveCard(uint8_t c)
{
	uint8_t a = c;
	if (a == 0)
		a = wCardReceived;
	AddCardToCollection(a);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_GiveCard */

/* >>> factory ScriptCommand_TakeCard */
/* scripting.asm:1066-1069 */
IncreaseScriptPointerResult ScriptCommand_TakeCard(uint8_t c)
{
	RemoveCardFromCollection(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_TakeCard */

/* >>> factory ScriptCommand_PauseSong */
/* scripting.asm:1868-1870 */
IncreaseScriptPointerResult ScriptCommand_PauseSong(void)
{
	PauseSong();
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy1();
	return r;
}
/* <<< factory ScriptCommand_PauseSong */

/* >>> factory ScriptCommand_ResumeSong */
/* scripting.asm:1872-1874 */
IncreaseScriptPointerResult ScriptCommand_ResumeSong(void)
{
	ResumeSong();
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy1();
	return r;
}
/* <<< factory ScriptCommand_ResumeSong */

/* >>> factory ScriptCommand_nop */
/* scripting.asm:1819-1820. Pure tail jump: the command behaves exactly like
 * IncreaseScriptPointerBy1 on the caller's registers. */
IncreaseScriptPointerResult ScriptCommand_nop(void)
{
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_nop */

/* >>> factory ScriptCommand_OverrideSong */
/* scripting.asm:1843-1847. The override byte is stored before PlaySong runs
 * (PlaySong takes the song id in a and may consult the override itself). */
IncreaseScriptPointerResult ScriptCommand_OverrideSong(uint8_t c)
{
	wSongOverride = c;
	PlaySong(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_OverrideSong */

/* >>> factory ScriptCommand_SetDefaultSong */
/* scripting.asm:1849-1852 */
IncreaseScriptPointerResult ScriptCommand_SetDefaultSong(uint8_t c)
{
	wDefaultSong = c;
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_SetDefaultSong */

/* >>> factory ScriptCommand_RecordMasterWin */
/* scripting.asm:1880-1883. Marks the master whose id is in c as beaten, then
 * tail-jumps to IncreaseScriptPointerBy2. The farcall's a/f results are dead
 * (the tail jump recomputes both); only its memory effect matters. */
IncreaseScriptPointerResult ScriptCommand_RecordMasterWin(uint8_t c)
{
	uint8_t f;
	AddMasterBeatenToList(c, &f);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_RecordMasterWin */

/* >>> factory ScriptCommand_ChallengeMachine */
/* scripting.asm:1885-1890. Triggers the challenge-machine event: stores
 * GAME_EVENT_CHALLENGE_MACHINE in wGameEvent and sets bit 6 of
 * wOverworldTransition (`set` preserves the other bits), then tail-jumps to
 * IncreaseScriptPointerBy1, whose exit state (a, f, c) is the contract. */
IncreaseScriptPointerResult ScriptCommand_ChallengeMachine(void)
{
	wGameEvent = GAME_EVENT_CHALLENGE_MACHINE;
	wOverworldTransition |= 0x40u;
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_ChallengeMachine */

/* >>> factory ScriptCommand_PlaySong */
/* scripting.asm:1854-1857. c is the song id passed to ScriptPlaySong; the
 * tail jp means the composite's exit registers are exactly
 * IncreaseScriptPointerBy2's ({a, f, c}). */
IncreaseScriptPointerResult ScriptCommand_PlaySong(uint8_t c)
{
	ScriptPlaySong(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_PlaySong */

/* >>> factory ScriptCommand_PlaySFX */
/* scripting.asm:1859-1862. c is the SFX id passed to PlaySFX; the tail jp
 * makes the composite's exit registers exactly IncreaseScriptPointerBy2's
 * ({a, f, c}). */
IncreaseScriptPointerResult ScriptCommand_PlaySFX(uint8_t c)
{
	PlaySFX(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_PlaySFX */

/* >>> factory ScriptCommand_PlayDefaultSong */
/* scripting.asm:1864-1866. PlayDefaultSong consumes no registers and its
 * {a, f} exit is fully overwritten by the IncreaseScriptPointerBy1 tail, so
 * the composite's exits are exactly IncreaseScriptPointerBy1's ({a, f, c}). */
IncreaseScriptPointerResult ScriptCommand_PlayDefaultSong(void)
{
	PlayDefaultSong();
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_PlayDefaultSong */

/* >>> factory ScriptCommand_SetSpriteAttributes */
/* scripting.asm:1276-1306. Records the current NPC in wLoadedNPCTempIndex,
 * reads 3 script bytes, clears the directionless bit in that NPC's flags
 * item and ORs the third script byte into it, then restarts the NPC
 * animation with b on CGB or c on DMG. Entry bc is only consumed after the
 * push/pop pair restores it. */
SetSpriteAttributesResult ScriptCommand_SetSpriteAttributes(uint8_t b, uint8_t c)
{
	wLoadedNPCTempIndex = wScriptNPC;
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	PermissionResult item = GetItemInLoadedNPCIndex(wScriptNPC, LOADED_NPC_FLAGS);
	uint8_t flags = (uint8_t)(gb_read8(item.hl) & (uint8_t)~(1u << NPC_FLAG_DIRECTIONLESS_F));
	gb_write8(item.hl, flags); /* res NPC_FLAG_DIRECTIONLESS_F, [hl] */
	flags = (uint8_t)(gb_read8(item.hl) | args.c); /* ld a, [hl]; or c */
	gb_write8(item.hl, flags); /* ld [hl], a */
	uint8_t e = c; /* ld e, c */
	if (wConsole == CONSOLE_CGB) /* cp CONSOLE_CGB; jr nz, .not_cgb */
		e = b; /* ld e, b */
	(void)SetNPCAnimation(e); /* ld a, e; farcall SetNPCAnimation */
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
	return (SetSpriteAttributesResult){r.a, r.f, r.c, e};
}
/* <<< factory ScriptCommand_SetSpriteAttributes */

/* >>> factory ScriptCommand_DoFrames */
/* scripting.asm:1308-1318. Runs DoFrameIfLCDEnabled c times -- the loop is
 * post-test, so a count of 0 wraps to 256 frames -- then advances the
 * script pointer by 2. The push/pop pair keeps b intact across the frames. */
IncreaseScriptPointerResult ScriptCommand_DoFrames(uint8_t c)
{
	uint32_t n = c ? c : 0x100u;
	for (uint32_t i = 0; i < n; i++)
		DoFrameIfLCDEnabled();
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_DoFrames */

/* >>> factory ScriptCommand_EndScript */
/* scripting.asm:652-655. Stores TRUE to wBreakScriptLoop, then tail-jumps into
 * IncreaseScriptPointerBy1, so the exit a/f/c are that helper's outputs and
 * b/d/e/hl pass through untouched. */
IncreaseScriptPointerResult ScriptCommand_EndScript(void)
{
	wBreakScriptLoop = TRUE;
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_EndScript */

/* >>> factory SetNPCDuelParams */
/* scripting.asm:753-761. Stores the prize count and deck id, then reads the
 * duel theme from the script args. The trailing `ld a, c` refreshes Z/N/H from
 * the final c while the carry bit survives from GetScriptArgs3AfterPointer's
 * exit flags; b/c/d/e/hl at ret are that helper's exit state (d/e/hl kept). */
SetNPCDuelParamsResult SetNPCDuelParams(uint8_t b, uint8_t c)
{
	wNPCDuelPrizes = c;
	wNPCDuelDeckID = b;
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	wDuelTheme = args.c;
	uint8_t f = args.f & 0x10u; /* ld a, c : carry unchanged */
	if (args.c == 0)
		f |= 0x80u; /* Z set when the theme byte is zero */
	return (SetNPCDuelParamsResult){args.c, f, args.b, args.c};
}
/* <<< factory SetNPCDuelParams */

/* >>> factory ScriptCommand_BattleCenter */
/* scripting.asm:763-768. Stores the Battle Center game event, sets bit 6 of
 * wOverworldTransition, then tail-jumps into IncreaseScriptPointerBy1 -- the
 * callee's a/f/c exit state becomes this routine's exit state. */
IncreaseScriptPointerResult ScriptCommand_BattleCenter(void)
{
	wGameEvent = GAME_EVENT_BATTLE_CENTER;
	wOverworldTransition |= 0x40u;
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_BattleCenter */

/* >>> factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot */
/* scripting.asm:1370-1398. sla c doubles the slot index into a byte offset
 * (bc = c*2 & $ff, b cleared); wTxRam2+bc receives the 2-byte tx pointer for
 * the map selected by wOverworldMapSelection (rlca doubles the selection
 * into the table index, base MapNames-2). Then tail-jumps
 * IncreaseScriptPointerBy2, so a/f/c at ret come from that callee while b
 * holds the 0 produced by the body (d/e/hl hold body residue the callee
 * preserves but no caller consumes). */
ScriptCommand_LoadCurrentMapNameIntoTxRamSlotResult ScriptCommand_LoadCurrentMapNameIntoTxRamSlot(uint8_t c)
{
	uint16_t dest = (uint16_t)(wTxRam2_ADDR + (uint8_t)(c << 1));
	uint8_t sel = wOverworldMapSelection;
	uint8_t idx = (uint8_t)((sel << 1) | (sel >> 7));
	uint16_t src = (uint16_t)(MAP_NAMES - 2u + idx);
	uint8_t lo = gb_read8(src);
	uint8_t hi = gb_read8((uint16_t)(src + 1u));
	gb_write8(dest, lo);
	gb_write8((uint16_t)(dest + 1u), hi);
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy2();
	return (ScriptCommand_LoadCurrentMapNameIntoTxRamSlotResult){r.a, r.f, 0x00u, r.c};
}
/* <<< factory ScriptCommand_LoadCurrentMapNameIntoTxRamSlot */

/* >>> factory ScriptCommand_EnterMap */
/* scripting.asm:1761-1774. Builds hl from wScriptPointer, skips the command
 * byte and the first argument byte (read but discarded), then stores the next
 * four bytes into wTempMap / wTempPlayerXCoord / wTempPlayerYCoord /
 * wTempPlayerDirection, sets bit 4 of wOverworldTransition, and tail-jumps
 * IncreaseScriptPointerBy6. All argument fetches are bus reads: the script
 * data lives wherever the caller banked it; 16-bit hl arithmetic wraps. */
IncreaseScriptPointerResult ScriptCommand_EnterMap(void)
{
	uint16_t hl = (uint16_t)(gb_read8(wScriptPointer_ADDR) | (uint16_t)gb_read8(wScriptPointer_ADDR + 1u) << 8);
	hl++;
	gb_read8(hl++);
	gb_write8(wTempMap_ADDR, gb_read8(hl++));
	gb_write8(wTempPlayerXCoord_ADDR, gb_read8(hl++));
	gb_write8(wTempPlayerYCoord_ADDR, gb_read8(hl++));
	gb_write8(wTempPlayerDirection_ADDR, gb_read8(hl++));
	wOverworldTransition |= 0x10u;
	return IncreaseScriptPointerBy6();
}
/* <<< factory ScriptCommand_EnterMap */
