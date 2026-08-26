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

#include "generated/wram.h"

#include "generated/wram.h"
#define EVENT_VAR_BYTES 0x40u

#include "home/mail.h"

#include "home/scripting.h"
#include "home/npc_core.h"
#include "generated/wram.h"

#include "home/scripting.h"
#include "home/card_collection.h"

#include "home/scripting.h"
#include "home/card_collection.h"
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define GRASS_ENERGY 0x01u

#include "home/card_collection.h"
#include "home/scripting.h"

#include "home/scripting.h"
#include "generated/wram.h"
#define EVENT_PUPIL_CHRIS_STATE 0x17u
#define EVENT_PUPIL_JESSICA_STATE 0x20u
#define EVENT_PUPIL_MICHAEL_STATE 0x11u
#define PUPIL_DEFEATED 0x08u
#define PUPIL_INACTIVE 0x00u

#include "generated/wram.h"
#include "mem.h"

#include "home/scripting.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "home/npc_core.h"

#include "home/map.h"
#include "home/npc_core.h"
#include "home/scripting.h"
#include "generated/wram.h"

#include "home/scripting.h"
#include "home/npc_core.h"
#include "home/lcd_enable_frame.h"

#include "home/scripting.h"
#include "home/npc_core.h"

#include "home/save.h"
#include "home/scripting.h"

#include "home/scripting.h"
#include "home/map.h"
#include "generated/wram.h"
#define GAME_EVENT_CREDITS 0x04u

#include "home/scripting.h"
#include "home/random.h"
#include "home/challenge_hall.h"
#include "generated/wram.h"
#include "mem.h"
#define EVENT_CHALLENGE_CUP_NUMBER 0x44u
#define EVENT_CHALLENGE_CUP_OPPONENT_NUMBER 0x45u
#define NPC_RONALD1 0x02u
#define CHALLENGE_HALL_NPC_COUNT 25u
#define CHALLENGE_HALL_NPCS_BANK 3u
#define CHALLENGE_HALL_NPCS_ADDR 0x75B3u

#include "home/scripting.h"
#include "home/card_data.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/scripting.h"
#include "generated/wram.h"
#define NPC_AMY 0x22u

#include "home/scripting.h"
#include "home/random.h"
#include "generated/wram.h"
#define EVENT_IMAKUNI_ROOM 0x34u
#define EVENT_IMAKUNI_STATE 0x13u
#define FIGHTING_CLUB_LOBBY 0x05u
#define IMAKUNI_FIGHTING_CLUB 0x00u
#define IMAKUNI_TALKED 0x02u
#define LIGHTNING_CLUB_LOBBY 0x0eu
#define SCIENCE_CLUB_LOBBY 0x17u
#define WATER_CLUB_LOBBY 0x0bu

#include "home/overworld.h"

#include "home/scripting.h"
#include "home/map.h"
#include "generated/wram.h"

#include "home/scripting.h"
#include "generated/wram.h"
#define CHALLENGE_CUP_NOT_STARTED 0x00u
#define CHALLENGE_CUP_READY_TO_START 0x01u
#define CHALLENGE_CUP_WON 0x02u
#define CHALLENGE_CUP_OVER 0x07u
#define EVENT_RECEIVED_LEGENDARY_CARDS 0x22u
#define EVENT_CHALLENGE_CUP_1_STATE 0x3fu
#define EVENT_CHALLENGE_CUP_2_STATE 0x40u
#define EVENT_CHALLENGE_CUP_3_STATE 0x41u
#define OWMAP_CHALLENGE_HALL 0x0bu

#include "home/scripting.h"
#include "generated/wram.h"

#include "home/scripting.h"
#include "home/npc_core.h"
#include "home/npc_data.h"
#include "generated/wram.h"
#define SOUTH 0x02u

#include "home/scripting.h"
#define EVENT_MASON_LAB_STATE 0x3eu
#define EVENT_PLAYER_ENTERED_CHALLENGE_CUP 0x59u
#define EVENT_CHALLENGE_CUP_OPPONENT_CHOSEN 0x46u
#define Script_BeginGame 0x552eu

#include "home/scripting.h"
#include "home/mail.h"
#include "generated/wram.h"
#include "mem.h"
#define EVENT_BEAT_NIKKI 0x08u
#define EVENT_BEAT_RICK 0x09u
#define EVENT_BEAT_KEN 0x0Au
#define EVENT_BEAT_AMY 0x0Bu
#define EVENT_BEAT_ISAAC 0x0Cu
#define EVENT_BEAT_MURRAY 0x0Du
#define EVENT_BEAT_GENE 0x0Eu
#define EVENT_BEAT_MITCH 0x0Fu
#define EVENT_MEDAL_COUNT 0x2Eu

#include "home/scripting.h"
#include "mem.h"

#include "home/scripting.h"
#include "home/npc_data.h"
#include "mem.h"

#include "home/scripting.h"
#include "home/npc_data.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/npc_core.h"
#include "home/map.h"
#include "home/npc_data.h"
#include "generated/wram.h"
#include "mem.h"
#define GAME_EVENT_DUEL 0x01u
#define LOADED_NPC_ID 0x00u
static const uint8_t sAaronDeckIDs[] = {0x00u, 0x01u, 0x02u, 0x03u};

#include "home/scripting.h"
#include "home/npc_data.h"
#include "home/npc_core.h"
#include "generated/wram.h"
#include "mem.h"
#define MUSIC_MATCH_START_2 0x16u

#include "home/overworld.h"
#include "home/scripting.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "generated/wram.h"
#include "home/map.h"
#include "home/script.h"
#define MAP_SCRIPT_AFTER_DUEL 0x0Au

#include "generated/wram.h"
#include "home/map.h"
#include "home/script.h"

#include "home/scripting.h"
#define MAP_SCRIPT_LOAD_MAP 0x08u

#define MAP_SCRIPT_MOVED_PLAYER 0x0cu

#include "generated/wram.h"
#include "home/overworld.h"

#include "home/scripting.h"
#include "home/gift_center.h"
#include "generated/wram.h"
#define EVENT_GIFT_CENTER_MENU_CHOICE 0x72u
#define GAME_EVENT_GIFT_CENTER 0x03u
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

/* >>> factory GetScriptArgs1AfterPointer */
/* scripting.asm:615-618 */
GetScriptArgsAfterPointerResult GetScriptArgs1AfterPointer(void)
{
	GetScriptArgsAfterPointerResult r = GetScriptArgsAfterPointer(1u);
	return r;
}
/* <<< factory GetScriptArgs1AfterPointer */

/* >>> factory SetNextScript */
void SetNextScript(uint16_t bc)
{
	wNextScript = (uint8_t)bc;
	wNextScript_PTR[1] = (uint8_t)(bc >> 8);
	wOverworldMode = 0x03u;
}
/* <<< factory SetNextScript */

/* >>> factory SetEventValue */
SetEventValueResult SetEventValue(uint8_t a, uint8_t f, uint8_t b, uint8_t c)
{
	GetEventVarResult event = GetEventVar(a, f, b, c);
	uint16_t addr = event.hl;
	uint8_t mask = gb_read8(wLoadedEventBits_ADDR);
	uint8_t value = c;
	while ((mask & 1u) == 0) {
		mask = (uint8_t)(mask >> 1);
		value = (uint8_t)(value << 1);
	}
	uint8_t loaded = gb_read8(wLoadedEventBits_ADDR);
	uint8_t selected = (uint8_t)(loaded & value);
	uint8_t result = (uint8_t)((gb_read8(addr) & (uint8_t)~loaded) | selected);
	gb_write8(addr, result);
	return (SetEventValueResult){result, result == 0 ? 0x80u : 0u};
}
/* <<< factory SetEventValue */

/* >>> factory MaxOutEventValue */
SetEventValueResult MaxOutEventValue(uint8_t a, uint8_t f, uint8_t b, uint8_t c)
{
	return SetEventValue(a, f, b, 0xffu);
}
/* <<< factory MaxOutEventValue */

/* >>> factory ZeroOutEventValue */
SetEventValueResult ZeroOutEventValue(uint8_t a, uint8_t f, uint8_t b, uint8_t c)
{
	return SetEventValue(a, f, b, 0u);
}
/* <<< factory ZeroOutEventValue */

/* >>> factory ClearEvents */
void ClearEvents(void)
{
	for (uint16_t i = 0; i < EVENT_VAR_BYTES; ++i) {
		gb_write8((uint16_t)(wEventVars_ADDR + i), 0u);
	}
}
/* <<< factory ClearEvents */

/* >>> factory ScriptCommand_Jump */
ScriptCommand_JumpResult ScriptCommand_Jump(void)
{
	GetScriptArgsAfterPointerResult args = GetScriptArgs1AfterPointer();
	uint16_t target = (uint16_t)(((uint16_t)args.b << 8) | args.c);
	uint16_t hl = SetScriptPointer(target);
	return (ScriptCommand_JumpResult){args.a, args.f, args.b, args.c, hl};
}
/* <<< factory ScriptCommand_Jump */

/* >>> factory ScriptCommand_MaxOutEventValue */
IncreaseScriptPointerResult ScriptCommand_MaxOutEventValue(uint8_t f, uint8_t b, uint8_t c)
{
	(void)MaxOutEventValue(c, f, b, c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_MaxOutEventValue */

/* >>> factory ScriptCommand_ZeroOutEventValue */
IncreaseScriptPointerResult ScriptCommand_ZeroOutEventValue(uint8_t f, uint8_t b, uint8_t c)
{
	(void)ZeroOutEventValue(c, f, b, c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_ZeroOutEventValue */

/* >>> factory ScriptCommand_SetEventValue */
IncreaseScriptPointerResult ScriptCommand_SetEventValue(uint8_t f, uint8_t b, uint8_t c)
{
	(void)SetEventValue(c, f, b, c);
	return IncreaseScriptPointerBy3();
}
/* <<< factory ScriptCommand_SetEventValue */

/* >>> factory ScriptCommand_TryGivePCPack */
IncreaseScriptPointerResult ScriptCommand_TryGivePCPack(uint8_t c)
{
	TryGivePCPack(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_TryGivePCPack */

/* >>> factory ScriptCommand_SetActiveNPCCoords */
IncreaseScriptPointerResultWithB ScriptCommand_SetActiveNPCCoords(uint8_t b, uint8_t c)
{
	wLoadedNPCTempIndex = wScriptNPC;
	(void)SetNPCPosition(c, b);
	IncreaseScriptPointerResult pointer = IncreaseScriptPointerBy3();
	return (IncreaseScriptPointerResultWithB){pointer.a, pointer.f, c, pointer.c};
}
/* <<< factory ScriptCommand_SetActiveNPCCoords */

/* >>> factory ScriptCommand_JumpIfEnoughCardsOwned */
JumpIfCardInCollectionResult ScriptCommand_JumpIfEnoughCardsOwned(uint8_t b, uint8_t c)
{
	IncreaseScriptPointerBy1();
	uint16_t owned = GetAmountOfCardsOwned();
	uint16_t target = (uint16_t)(((uint16_t)b << 8) | c);
	if (owned >= target) {
		SetScriptControlBytePass();
		GetScriptArgsAfterPointerResult args = GetScriptArgs2AfterPointer();
		if (args.f & 0x80u) {
			IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
			return (JumpIfCardInCollectionResult){r.a, r.f, args.b, r.c};
		}
		(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
		return (JumpIfCardInCollectionResult){args.a, args.f, args.b, args.c};
	}
	SetScriptControlByteFail();
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
	return (JumpIfCardInCollectionResult){r.a, r.f, b, r.c};
}
/* <<< factory ScriptCommand_JumpIfEnoughCardsOwned */

/* >>> factory ScriptCommand_RemoveAllEnergyCardsFromCollection */
IncreaseScriptPointerResult ScriptCommand_RemoveAllEnergyCardsFromCollection(void)
{
	uint8_t card = 1u;
	for (;;) {
		CardCountResult count = GetCardCountInCollection(card);
		if ((count.f & 0x10u) == 0u) {
			uint8_t remaining = count.a;
			while (remaining != 0u) {
				RemoveCardFromCollection(card);
				--remaining;
			}
		}
		card = (uint8_t)(card + 1u);
		if (card < (uint8_t)(DOUBLE_COLORLESS_ENERGY + 1u))
			continue;
		return IncreaseScriptPointerBy1();
	}
}
/* <<< factory ScriptCommand_RemoveAllEnergyCardsFromCollection */

/* >>> factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */
ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult ScriptCommand_JumpIfAnyEnergyCardsInCollection(void)
{
	uint8_t total = 0u;
	for (uint8_t card = GRASS_ENERGY; card <= DOUBLE_COLORLESS_ENERGY; ++card) {
		CardCountResult count = GetCardCountInCollection(card);
		total = (uint8_t)(total + count.a);
	}
	if (total == 0u) {
		SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult){r.a, r.f, total, r.c};
	}
	SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs1AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy3();
		return (ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult){r.a, r.f, args.b, r.c};
	}
	(void)SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfAnyEnergyCardsInCollectionResult){args.a, args.f, args.b, args.c};
}
/* <<< factory ScriptCommand_JumpIfAnyEnergyCardsInCollection */

/* >>> factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
/* >>> factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
ScriptCommand_JumpBasedOnFightingClubPupilStatusResult ScriptCommand_JumpBasedOnFightingClubPupilStatus(void)
{
	GetEventVarResult michael_event = GetEventVar(EVENT_PUPIL_MICHAEL_STATE, 0u, 0u, 0u);
	uint8_t michael_mask = michael_event.a;
	uint8_t michael = gb_read8(michael_event.hl);
	while ((michael_mask & 1u) == 0u) {
		michael_mask = (uint8_t)(michael_mask >> 1);
		michael = (uint8_t)(michael >> 1);
	}
	michael = (uint8_t)(michael & michael_mask);
	if (michael == PUPIL_INACTIVE) {
		GetScriptArgsAfterPointerResult args = GetScriptArgs1AfterPointer();
		uint16_t target = (uint16_t)(((uint16_t)args.b << 8) | args.c);
		uint16_t hl = SetScriptPointer(target);
		return (ScriptCommand_JumpBasedOnFightingClubPupilStatusResult){args.a, args.f, args.b, args.c, hl};
	}

	uint8_t count = 0u;
	if (michael >= PUPIL_DEFEATED)
		++count;

	GetEventVarResult chris_event = GetEventVar(EVENT_PUPIL_CHRIS_STATE, 0u, 0u, 0u);
	uint8_t chris_mask = chris_event.a;
	uint8_t chris = gb_read8(chris_event.hl);
	while ((chris_mask & 1u) == 0u) {
		chris_mask = (uint8_t)(chris_mask >> 1);
		chris = (uint8_t)(chris >> 1);
	}
	chris = (uint8_t)(chris & chris_mask);
	if (chris >= PUPIL_DEFEATED)
		++count;

	GetEventVarResult jessica_event = GetEventVar(EVENT_PUPIL_JESSICA_STATE, 0u, 0u, 0u);
	uint8_t jessica_mask = jessica_event.a;
	uint8_t jessica = gb_read8(jessica_event.hl);
	while ((jessica_mask & 1u) == 0u) {
		jessica_mask = (uint8_t)(jessica_mask >> 1);
		jessica = (uint8_t)(jessica >> 1);
	}
	jessica = (uint8_t)(jessica & jessica_mask);
	if (jessica >= PUPIL_DEFEATED)
		++count;

	uint8_t offset = (uint8_t)((count << 1) + 3u);
	GetScriptArgsAfterPointerResult args = GetScriptArgsAfterPointer(offset);
	uint16_t target = (uint16_t)(((uint16_t)args.b << 8) | args.c);
	uint16_t hl = SetScriptPointer(target);
	return (ScriptCommand_JumpBasedOnFightingClubPupilStatusResult){args.a, args.f, args.b, args.c, hl};
}
/* <<< factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */
/* <<< factory ScriptCommand_JumpBasedOnFightingClubPupilStatus */

/* >>> factory GetEventValue */
uint8_t GetEventValue(uint8_t a)
{
	GetEventVarResult event = GetEventVar(a, 0u, 0u, 0u);
	uint8_t value = gb_read8(event.hl);
	uint8_t mask = wLoadedEventBits;
	while ((mask & 1u) == 0u) {
		mask = (uint8_t)(mask >> 1);
		value = (uint8_t)(value >> 1);
	}
	return (uint8_t)(mask & value);
}
/* <<< factory GetEventValue */

/* >>> factory GetEventValueBC */
GetEventValueBCResult GetEventValueBC(uint8_t b, uint8_t c)
{
	uint8_t value = GetEventValue(c);
	uint8_t f = value == 0u ? 0x80u : 0u;
	return (GetEventValueBCResult){value, f, b};
}
/* <<< factory GetEventValueBC */

/* >>> factory ScriptCommand_JumpIfEventEqual */
ScriptCommand_JumpIfEventEqualResult ScriptCommand_JumpIfEventEqual(uint8_t b, uint8_t c, uint16_t hl)
{
	GetEventValueBCResult event = GetEventValueBC(b, c);
	/* before */
	if (event.a != event.c) {
		(void)SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventEqualResult){r.a, r.f, event.c, r.c, hl};
	}
	(void)SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventEqualResult){r.a, r.f, args.b, r.c, hl};
	}
	uint16_t next_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfEventEqualResult){args.a, args.f, args.b, args.c, next_hl};
}
/* <<< factory ScriptCommand_JumpIfEventEqual */

/* >>> factory ScriptCommand_JumpIfEventZero */
ScriptCommand_JumpIfEventZeroResult ScriptCommand_JumpIfEventZero(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t event = GetEventValue(c);
	if (event == 0u) {
		/* before */
		(void)SetScriptControlBytePass();
		GetScriptArgsAfterPointerResult args = GetScriptArgs2AfterPointer();
		if (args.f & 0x80u) {
			IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
			return (ScriptCommand_JumpIfEventZeroResult){r.a, r.f, args.b, r.c, hl};
		}
		uint16_t next_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
		return (ScriptCommand_JumpIfEventZeroResult){args.a, args.f, args.b, args.c, next_hl};
	}
	(void)SetScriptControlByteFail();
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
	return (ScriptCommand_JumpIfEventZeroResult){r.a, r.f, b, r.c, hl};
}
/* <<< factory ScriptCommand_JumpIfEventZero */

/* >>> factory ScriptCommand_JumpIfEventGreaterOrEqual */
ScriptCommand_JumpIfEventGreaterOrEqualResult ScriptCommand_JumpIfEventGreaterOrEqual(uint8_t b, uint8_t c, uint16_t hl)
{
	GetEventValueBCResult event = GetEventValueBC(b, c);
	/* before */
	if (event.a < event.c) {
		(void)SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventGreaterOrEqualResult){r.a, r.f, event.c, r.c, hl};
	}
	(void)SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventGreaterOrEqualResult){r.a, r.f, args.b, r.c, hl};
	}
	uint16_t next_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfEventGreaterOrEqualResult){args.a, args.f, args.b, args.c, next_hl};
}
/* <<< factory ScriptCommand_JumpIfEventGreaterOrEqual */

/* >>> factory ScriptCommand_JumpIfEventLessThan */
ScriptCommand_JumpIfEventLessThanResult ScriptCommand_JumpIfEventLessThan(uint8_t b, uint8_t c, uint16_t hl)
{
	GetEventValueBCResult event = GetEventValueBC(b, c);
	/* before */
	if (event.a >= event.c) {
		(void)SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventLessThanResult){r.a, r.f, event.c, r.c, hl};
	}
	(void)SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventLessThanResult){r.a, r.f, args.b, r.c, hl};
	}
	uint16_t next_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfEventLessThanResult){args.a, args.f, args.b, args.c, next_hl};
}
/* <<< factory ScriptCommand_JumpIfEventLessThan */

/* >>> factory ScriptCommand_JumpIfEventNotEqual */
ScriptCommand_JumpIfEventNotEqualResult ScriptCommand_JumpIfEventNotEqual(uint8_t b, uint8_t c, uint16_t hl)
{
	GetEventValueBCResult event = GetEventValueBC(b, c);
	/* before */
	if (event.a == event.c) {
		(void)SetScriptControlByteFail();
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventNotEqualResult){r.a, r.f, event.c, r.c, hl};
	}
	(void)SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfEventNotEqualResult){r.a, r.f, args.b, r.c, hl};
	}
	uint16_t next_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfEventNotEqualResult){args.a, args.f, args.b, args.c, next_hl};
}
/* <<< factory ScriptCommand_JumpIfEventNotEqual */

/* >>> factory ScriptCommand_JumpIfEventNonzero */
ScriptCommand_JumpIfEventZeroResult ScriptCommand_JumpIfEventNonzero(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t event = GetEventValue(c);
	if (event != 0u) {
		/* before */
		(void)SetScriptControlBytePass();
		GetScriptArgsAfterPointerResult args = GetScriptArgs2AfterPointer();
		if (args.f & 0x80u) {
			IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
			return (ScriptCommand_JumpIfEventZeroResult){r.a, r.f, args.b, r.c, hl};
		}
		uint16_t next_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
		return (ScriptCommand_JumpIfEventZeroResult){args.a, args.f, args.b, args.c, next_hl};
	}
	(void)SetScriptControlByteFail();
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
	return (ScriptCommand_JumpIfEventZeroResult){r.a, r.f, b, r.c, hl};
}
/* <<< factory ScriptCommand_JumpIfEventNonzero */

/* >>> factory ScriptCommand_JumpIfEventTrue */
/* scripting.asm:1990-2012. The pair jumps into each other's sub-labels rather
 * than calling each other's entry points, so the two shared blocks are static
 * helpers here and each entry point selects between them. */
static ScriptCommand_JumpIfEventTrueResult script_jump_event_pass(uint16_t hl)
{
	(void)SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs2AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
		return (ScriptCommand_JumpIfEventTrueResult){r.a, r.f, args.b, r.c, hl};
	}
	uint16_t next_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfEventTrueResult){args.a, args.f, args.b, args.c, next_hl};
}

static ScriptCommand_JumpIfEventTrueResult script_jump_event_fail(uint8_t b, uint16_t hl)
{
	(void)SetScriptControlByteFail();
	IncreaseScriptPointerResult r = IncreaseScriptPointerBy4();
	return (ScriptCommand_JumpIfEventTrueResult){r.a, r.f, b, r.c, hl};
}

ScriptCommand_JumpIfEventTrueResult ScriptCommand_JumpIfEventTrue(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t event = GetEventValue(c);
	if (event == 0u) return script_jump_event_fail(b, hl);
	return script_jump_event_pass(hl);
}
/* <<< factory ScriptCommand_JumpIfEventTrue */

/* >>> factory ScriptCommand_JumpIfEventFalse */
ScriptCommand_JumpIfEventTrueResult ScriptCommand_JumpIfEventFalse(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t event = GetEventValue(c);
	if (event == 0u) return script_jump_event_pass(hl);
	return script_jump_event_fail(b, hl);
}
/* <<< factory ScriptCommand_JumpIfEventFalse */

#include "home/lcd_enable_frame.h"
#include "home/overworld_map.h"

/* >>> factory ScriptCommand_WalkPlayerToMasonLaboratory */
#define OWMAP_MASON_LABORATORY 0x01u

/* scripting.asm:1830-1841. Drives the player's walk to the Mason Laboratory: the
 * loop runs a frame and advances the walking animation until
 * wOverworldMapPlayerAnimationState reaches 2. Bounded by the animation itself,
 * not by a counter -- the reference needs ~11.5M instructions, so a case must
 * declare a large budget. */
IncreaseScriptPointerResult ScriptCommand_WalkPlayerToMasonLaboratory(void)
{
	gb_write8(wOverworldMapSelection_ADDR, OWMAP_MASON_LABORATORY);
	OverworldMap_BeginPlayerMovement();
	do {
		DoFrameIfLCDEnabled();
		OverworldMap_UpdatePlayerWalkingAnimation();
	} while (gb_read8(wOverworldMapPlayerAnimationState_ADDR) != 2u);
	OverworldMap_PrintMapName();
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_WalkPlayerToMasonLaboratory */



/* >>> factory ScriptCommand_IncrementEventValue */
IncreaseScriptPointerResult ScriptCommand_IncrementEventValue(uint8_t f, uint8_t b, uint8_t c)
{
	uint8_t value = (uint8_t)(GetEventValue(c) + 1u);
	(void)SetEventValue(c, f, b, value);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_IncrementEventValue */

/* >>> factory ScriptCommand_JumpIfPlayerCoordsMatch */
ScriptCommand_JumpIfPlayerCoordsMatchResult ScriptCommand_JumpIfPlayerCoordsMatch(uint8_t b, uint8_t c, uint16_t hl)
{
	/* before */
	if (wPlayerXCoord != c) {
		(void)SetScriptControlByteFail();
		IncreaseScriptPointerResult pointer = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfPlayerCoordsMatchResult){pointer.a, pointer.f, b, pointer.c, hl};
	}
	if (wPlayerYCoord != b) {
		(void)SetScriptControlByteFail();
		IncreaseScriptPointerResult pointer = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfPlayerCoordsMatchResult){pointer.a, pointer.f, b, pointer.c, hl};
	}
	(void)SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if ((args.f & 0x80u) != 0u) {
		IncreaseScriptPointerResult pointer = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfPlayerCoordsMatchResult){pointer.a, pointer.f, args.b, pointer.c, hl};
	}
	uint16_t new_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfPlayerCoordsMatchResult){args.a, args.f, args.b, args.c, new_hl};
}
/* <<< factory ScriptCommand_JumpIfPlayerCoordsMatch */

/* >>> factory ScriptCommand_JumpIfActiveNPCCoordsMatch */
/* before */
ScriptCommand_JumpIfActiveNPCCoordsMatchResult ScriptCommand_JumpIfActiveNPCCoordsMatch(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t d = c;
	uint8_t e = b;
	wLoadedNPCTempIndex = wScriptNPC;
	NPCPositionResult position = GetNPCPosition();
	if (e != position.c || d != position.b) {
		ScriptCommand_JumpIfEventEqualResult result = ScriptCommand_JumpIfEventEqual(b, c, hl);
		return (ScriptCommand_JumpIfActiveNPCCoordsMatchResult){result.a, result.f, position.b, result.c, d, e, result.hl};
	}
	(void)SetScriptControlBytePass();
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult pointer = IncreaseScriptPointerBy5();
		return (ScriptCommand_JumpIfActiveNPCCoordsMatchResult){pointer.a, pointer.f, 0u, pointer.c, d, e, hl};
	}
	uint16_t new_hl = SetScriptPointer((uint16_t)(((uint16_t)args.b << 8) | args.c));
	return (ScriptCommand_JumpIfActiveNPCCoordsMatchResult){args.a, args.f, 0u, args.c, d, e, new_hl};
}
/* <<< factory ScriptCommand_JumpIfActiveNPCCoordsMatch */

/* >>> factory SetNextNPCAndScript */
SetNextNPCAndScriptResult SetNextNPCAndScript(uint16_t bc, uint16_t hl)
{
	(void)FindLoadedNPC();
	wScriptNPC = wLoadedNPCTempIndex;
	SetNewScriptNPCResult npc = SetNewScriptNPC(hl);
	SetNextScript(bc);
	return (SetNextNPCAndScriptResult){npc.a, npc.f, (uint8_t)(bc >> 8), (uint8_t)bc, npc.hl};
}
/* <<< factory SetNextNPCAndScript */

/* >>> factory ExecuteNPCMovement */
ExecuteNPCMovementResult ExecuteNPCMovement(uint16_t bc)
{
	uint16_t movement_script = bc;
	(void)StartNPCMovement(&movement_script);
	for (;;) {
		DoFrameIfLCDEnabled();
		CheckIsAnNPCMovingResult moving = CheckIsAnNPCMoving();
		if (moving.a == 0u)
			break;
	}
	IncreaseScriptPointerResult pointer = IncreaseScriptPointerBy3();
	return (ExecuteNPCMovementResult){pointer.a, pointer.f, (uint8_t)(movement_script >> 8), pointer.c};
}
/* <<< factory ExecuteNPCMovement */

/* >>> factory Func_cdd1 */
IncreaseScriptPointerResult Func_cdd1(void)
{
	(void)UnloadNPC();
	IncreaseScriptPointerResult result = IncreaseScriptPointerBy1();
	return result;
}
/* <<< factory Func_cdd1 */

/* >>> factory ScriptCommand_JumpIfCardOwned */
JumpIfCardInCollectionResult ScriptCommand_JumpIfCardOwned(uint8_t b, uint8_t c)
{
	CardCountResult cnt = GetCardCountInCollectionAndDecks(c);
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
/* <<< factory ScriptCommand_JumpIfCardOwned */

/* >>> factory ScriptCommand_WaitForSongToFinish */
IncreaseScriptPointerResult ScriptCommand_WaitForSongToFinish(void)
{
	WaitForSongToFinish();
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_WaitForSongToFinish */

/* >>> factory ScriptCommand_SaveGame */
IncreaseScriptPointerResult ScriptCommand_SaveGame(uint8_t c)
{
	_SaveGame(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_SaveGame */

/* >>> factory ScriptCommand_MoveActiveNPC */
ExecuteNPCMovementResult ScriptCommand_MoveActiveNPC(uint16_t bc)
{
	wLoadedNPCTempIndex = wScriptNPC;
	return ExecuteNPCMovement(bc);
}
/* <<< factory ScriptCommand_MoveActiveNPC */

/* >>> factory ScriptCommand_SetNextNPCAndScript */
IncreaseScriptPointerResult ScriptCommand_SetNextNPCAndScript(uint8_t c, uint16_t hl)
{
	wTempNPC = c;
	GetScriptArgsAfterPointerResult args = GetScriptArgs2AfterPointer();
	(void)SetNextNPCAndScript((uint16_t)(((uint16_t)args.b << 8) | args.c), hl);
	return IncreaseScriptPointerBy4();
}
/* <<< factory ScriptCommand_SetNextNPCAndScript */

/* >>> factory ScriptCommand_SetActiveNPCDirection */
IncreaseScriptPointerResult ScriptCommand_SetActiveNPCDirection(uint8_t c)
{
	wLoadedNPCTempIndex = wScriptNPC;
	(void)Func_1c52e(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_SetActiveNPCDirection */

/* >>> factory ScriptCommand_PlayCredits */
IncreaseScriptPointerResult ScriptCommand_PlayCredits(void)
{
	(void)GetReceivedLegendaryCards();
	wGameEvent = GAME_EVENT_CREDITS;
	wOverworldTransition |= 0x40u;
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_PlayCredits */

/* >>> factory ScriptCommand_PickChallengeHallOpponent */
IncreaseScriptPointerResult ScriptCommand_PickChallengeHallOpponent(void)
{
	/* Func_f580 (challenge_hall.asm:458-487) inlined: not independently
	 * ported, and this is its only caller. wTempNPC is pushed/popped by the
	 * real asm around the whole call, so its net effect here is zero. */
	uint8_t cup_number = GetEventValue(EVENT_CHALLENGE_CUP_NUMBER);
	uint8_t opponent_number = GetEventValue(EVENT_CHALLENGE_CUP_OPPONENT_NUMBER);
	uint8_t new_opponent_number = (uint8_t)(opponent_number + 1u);
	(void)SetEventValue(EVENT_CHALLENGE_CUP_OPPONENT_NUMBER, 0u, 0u, new_opponent_number);

	uint8_t picked;
	if (cup_number != 3u && new_opponent_number == 3u) {
		picked = NPC_RONALD1;
	} else {
		uint8_t d = (cup_number == 3u) ? CHALLENGE_HALL_NPC_COUNT : (uint8_t)(CHALLENGE_HALL_NPC_COUNT - 1u);
		uint8_t c;
		for (;;) {
			c = Random(d);
			ChallengeHallTestBitResult tested = Func_f5cc(c);
			if (!(tested.f & 0x10u))
				break;
		}
		(void)Func_f5d4(c);
		const uint8_t *entry = rom_ptr(CHALLENGE_HALL_NPCS_BANK, (uint16_t)(CHALLENGE_HALL_NPCS_ADDR + c));
		picked = entry[0];
	}
	wChallengeHallNPC = picked;
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_PickChallengeHallOpponent */

/* >>> factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */
IncreaseScriptPointerResult ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot(uint8_t c)
{
	uint8_t shifted = (uint8_t)(c << 1);
	uint16_t addr = (uint16_t)(wTxRam2_ADDR + shifted);
	uint8_t event = GetEventValue(EVENT_MAN1_REQUESTED_CARD_ID);
	uint16_t name = GetCardName(event);
	gb_write8(addr, (uint8_t)(name & 0xFFu));
	gb_write8((uint16_t)(addr + 1u), (uint8_t)(name >> 8));
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_LoadMan1RequestedCardIntoTxRamSlot */

/* >>> factory Func_c998 */
Func_c998Result Func_c998(void)
{
	uint8_t npc = wTempNPC;
	if (npc != NPC_AMY) {
		uint8_t f = (uint8_t)(0x40u
			| ((npc == NPC_AMY) ? 0x80u : 0u)
			| (((npc & 0x0Fu) < (NPC_AMY & 0x0Fu)) ? 0x20u : 0u)
			| ((npc < NPC_AMY) ? 0x10u : 0u));
		return (Func_c998Result){npc, f};
	}
	if (wd3d0 == 0u)
		return (Func_c998Result){0u, 0x80u};
	uint8_t console = wConsole;
	uint8_t anim = (console == CONSOLE_CGB) ? 14u : 4u;
	wNPCAnim = anim;
	wNPCAnimFlags = 0u;
	uint8_t f = (uint8_t)(0x40u
		| ((console == CONSOLE_CGB) ? 0x80u : 0u)
		| (((console & 0x0Fu) < (CONSOLE_CGB & 0x0Fu)) ? 0x20u : 0u)
		| ((console < CONSOLE_CGB) ? 0x10u : 0u));
	return (Func_c998Result){0u, f};
}
/* <<< factory Func_c998 */

/* >>> factory DetermineImakuniRoom */
SetEventValueResult DetermineImakuniRoom(void)
{
	const uint8_t rooms[4] = {FIGHTING_CLUB_LOBBY, SCIENCE_CLUB_LOBBY, LIGHTNING_CLUB_LOBBY, WATER_CLUB_LOBBY};
	uint8_t picked = IMAKUNI_FIGHTING_CLUB;
	uint8_t state = GetEventValue(EVENT_IMAKUNI_STATE);
	if (state >= IMAKUNI_TALKED) {
		do {
			picked = (uint8_t)(UpdateRNGSources() & 0x03u);
		} while (gb_read8(wTempMap) == rooms[picked]);
	}
	return SetEventValue(EVENT_IMAKUNI_ROOM, 0u, 0u, picked);
}
/* <<< factory DetermineImakuniRoom */

/* >>> factory ScriptCommand_SetPlayerDirection */
IncreaseScriptPointerResult ScriptCommand_SetPlayerDirection(uint8_t c)
{
	UpdatePlayerDirection(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_SetPlayerDirection */

/* >>> factory ScriptCommand_UnloadActiveNPC */
IncreaseScriptPointerResult ScriptCommand_UnloadActiveNPC(void)
{
	wLoadedNPCTempIndex = wScriptNPC;
	return Func_cdd1();
}
/* <<< factory ScriptCommand_UnloadActiveNPC */

/* >>> factory ScriptCommand_ReplaceMapBlocks */
IncreaseScriptPointerResult ScriptCommand_ReplaceMapBlocks(uint8_t c)
{
	SetOWMapEvent(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_ReplaceMapBlocks */

/* >>> factory ScriptCommand_GiveStarterDeck */
IncreaseScriptPointerResult ScriptCommand_GiveStarterDeck(void)
{
	AddStarterDeck(wStarterDeckChoice);
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_GiveStarterDeck */

/* >>> factory ScriptCommand_FlashScreen */
IncreaseScriptPointerResult ScriptCommand_FlashScreen(uint8_t c)
{
	FlashScreenToWhite(c);
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_FlashScreen */

/* >>> factory ScriptCommand_MoveActiveNPCByDirection */
ExecuteNPCMovementResult ScriptCommand_MoveActiveNPCByDirection(uint8_t b, uint8_t c)
{
	uint8_t npc = wScriptNPC;
	wLoadedNPCTempIndex = npc;
	uint8_t dir = GetNPCDirection();
	uint8_t rotated = (uint8_t)((dir << 1) | (dir >> 7));
	uint16_t sum = (uint16_t)(c + rotated);
	uint8_t l = (uint8_t)sum;
	uint8_t carry = (uint8_t)(sum >> 8);
	uint8_t h = (uint8_t)(b + carry);
	uint16_t hl = (uint16_t)(((uint16_t)h << 8) | l);
	uint8_t new_c = gb_read8(hl);
	hl++;
	uint8_t new_b = gb_read8(hl);
	uint16_t bc = (uint16_t)(((uint16_t)new_b << 8) | new_c);
	return ExecuteNPCMovement(bc);
}
/* <<< factory ScriptCommand_MoveActiveNPCByDirection */

/* >>> factory ScriptCommand_UnloadChallengeHallNPC */
void ScriptCommand_UnloadChallengeHallNPC(void)
{
	uint8_t saved_index = wLoadedNPCTempIndex;
	uint8_t saved_temp_npc = wTempNPC;
	wTempNPC = wChallengeHallNPC;
	(void)FindLoadedNPC();
	(void)Func_cdd1();
	wTempNPC = saved_temp_npc;
	wLoadedNPCTempIndex = saved_index;
}
/* <<< factory ScriptCommand_UnloadChallengeHallNPC */

/* >>> factory DetermineChallengeHallEvent */
void DetermineChallengeHallEvent(void)
{
	if (wOverworldMapSelection == OWMAP_CHALLENGE_HALL)
		return;

	if (GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS) != 0u) {
		uint8_t c3 = ((UpdateRNGSources() & 0x03u) == 0u) ? CHALLENGE_CUP_READY_TO_START : CHALLENGE_CUP_NOT_STARTED;
		(void)SetEventValue(EVENT_CHALLENGE_CUP_3_STATE, 0u, 0u, c3);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		return;
	}

	uint8_t state2 = GetEventValue(EVENT_CHALLENGE_CUP_2_STATE);
	if (state2 == CHALLENGE_CUP_OVER)
		return;

	if (state2 == CHALLENGE_CUP_NOT_STARTED) {
		uint8_t state1 = GetEventValue(EVENT_CHALLENGE_CUP_1_STATE);
		if (state1 == CHALLENGE_CUP_OVER || state1 == CHALLENGE_CUP_NOT_STARTED || state1 == CHALLENGE_CUP_WON)
			return;
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_READY_TO_START);
		return;
	}

	if (state2 != CHALLENGE_CUP_WON)
		(void)SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_READY_TO_START);

	(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
}
/* <<< factory DetermineChallengeHallEvent */

/* >>> factory DetermineImakuniAndChallengeHall */
void DetermineImakuniAndChallengeHall(void)
{
	gb_write8((uint16_t)(wEventVars_ADDR + EVENT_VAR_BYTES - 1u), 0u);
	(void)DetermineImakuniRoom();
	DetermineChallengeHallEvent();
}
/* <<< factory DetermineImakuniAndChallengeHall */

/* >>> factory ScriptCommand_SetChallengeHallNPCCoords */
IncreaseScriptPointerResult ScriptCommand_SetChallengeHallNPCCoords(uint8_t b, uint8_t c)
{
	uint8_t saved_index = wLoadedNPCTempIndex;
	uint8_t saved_temp_npc = wTempNPC;
	wTempNPC = wChallengeHallNPC;
	wLoadNPCXPos = c;
	wLoadNPCYPos = b;
	wLoadNPCDirection = SOUTH;
	uint8_t npc_id = wTempNPC;
	(void)LoadNPCSpriteData(npc_id, 0u, 0u, 0u, 0u, 0u);
	(void)LoadNPC();
	wTempNPC = saved_temp_npc;
	wLoadedNPCTempIndex = saved_index;
	return IncreaseScriptPointerBy3();
}
/* <<< factory ScriptCommand_SetChallengeHallNPCCoords */

/* >>> factory LoadOverworld */
void LoadOverworld(void)
{
	(void)ZeroOutEventValue(EVENT_PLAYER_ENTERED_CHALLENGE_CUP, 0u, 0u, 0u);
	(void)ZeroOutEventValue(EVENT_CHALLENGE_CUP_OPPONENT_CHOSEN, 0u, 0u, 0u);

	if (GetEventValue(EVENT_CHALLENGE_CUP_1_STATE) == CHALLENGE_CUP_WON) {
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
	} else if (GetEventValue(EVENT_CHALLENGE_CUP_2_STATE) == CHALLENGE_CUP_WON) {
		(void)SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
	} else if (GetEventValue(EVENT_CHALLENGE_CUP_3_STATE) == CHALLENGE_CUP_WON) {
		(void)SetEventValue(EVENT_CHALLENGE_CUP_3_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_2_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
		(void)SetEventValue(EVENT_CHALLENGE_CUP_1_STATE, 0u, 0u, CHALLENGE_CUP_OVER);
	}

	if (GetEventValue(EVENT_MASON_LAB_STATE) != 0u)
		return;
	SetNextScript(Script_BeginGame);
}
/* <<< factory LoadOverworld */

/* >>> factory TryGiveMedalPCPacks */
TryGiveMedalPCPacksResult TryGiveMedalPCPacks(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	static const uint8_t medal_events[8] = {
		EVENT_BEAT_NIKKI, EVENT_BEAT_RICK, EVENT_BEAT_KEN, EVENT_BEAT_AMY,
		EVENT_BEAT_ISAAC, EVENT_BEAT_MURRAY, EVENT_BEAT_GENE, EVENT_BEAT_MITCH,
	};
	uint8_t medal_count = 0u;
	for (uint8_t i = 0u; i < 8u; i++) {
		if (GetEventValue(medal_events[i]) != 0u)
			medal_count = (uint8_t)(medal_count + 1u);
	}
	SetEventValueResult sev = SetEventValue(EVENT_MEDAL_COUNT, 0u, 0u, medal_count);
	uint8_t saved_a = medal_count;
	uint8_t saved_f = sev.f;
	if (medal_count >= 8u) {
		TryGivePCPack(0xCu);
		TryGivePCPack(0xBu);
		TryGivePCPack(0xAu);
	} else if (medal_count >= 7u) {
		TryGivePCPack(0xBu);
		TryGivePCPack(0xAu);
	} else if (medal_count >= 3u) {
		TryGivePCPack(0xAu);
	}
	return (TryGiveMedalPCPacksResult){saved_a, saved_f, b, c, d, e, hl};
}
/* <<< factory TryGiveMedalPCPacks */

/* >>> factory GetByteAfterCall */
/* scripting.asm:273-286. `ld hl, sp+4` reads the caller's caller's return
 * address (the byte after that call site's own `call` instruction), an
 * explicit stand-in per Func_2057's established sp-relative-as-parameter
 * convention: hl carries that address value. The routine's only real
 * effect other than reading it (advancing the stack-resident copy by one)
 * lands in the harness's own reserved $CF00-$CFFF call frame and is not
 * independently observable; future callers derive the advanced pointer
 * as hl+1 inline. */
uint8_t GetByteAfterCall(uint16_t hl)
{
	return gb_read8(hl);
}
/* <<< factory GetByteAfterCall */

/* >>> factory ScriptCommand_TryGiveMedalPCPacks */
ScriptCommand_TryGiveMedalPCPacksResult ScriptCommand_TryGiveMedalPCPacks(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	TryGiveMedalPCPacksResult r1 = TryGiveMedalPCPacks(b, c, d, e, hl);
	IncreaseScriptPointerResult r2 = IncreaseScriptPointerBy1();
	return (ScriptCommand_TryGiveMedalPCPacksResult){r2.a, r2.f, r1.b, r2.c, r1.d, r1.e, r1.hl};
}
/* <<< factory ScriptCommand_TryGiveMedalPCPacks */

/* >>> factory ScriptCommand_SetDialogNPC */
ScriptCommand_SetDialogNPCResult ScriptCommand_SetDialogNPC(uint8_t f, uint8_t b, uint8_t c, uint16_t hl)
{
	SetNPCDialogNameResult r1 = SetNPCDialogName(c, f, b, c, hl);
	IncreaseScriptPointerResult r2 = IncreaseScriptPointerBy2();
	return (ScriptCommand_SetDialogNPCResult){r2.a, r2.f, r1.b, r2.c, r1.hl};
}
/* <<< factory ScriptCommand_SetDialogNPC */

/* >>> factory ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot */
IncreaseScriptPointerResult ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot(uint8_t c)
{
	uint8_t saved_e = gb_read8(wCurrentNPCNameTx_ADDR);
	uint8_t saved_d = gb_read8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u));

	uint8_t slot_c = (uint8_t)(c << 1);
	uint16_t slot_hl = (uint16_t)(wTxRam2_ADDR + slot_c);

	uint8_t a = wChallengeHallNPC;
	(void)SetNPCDialogName(a, 0u, 0u, slot_c, slot_hl);

	uint8_t name_lo = gb_read8(wCurrentNPCNameTx_ADDR);
	gb_write8(slot_hl, name_lo);
	uint8_t name_hi = gb_read8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u));
	gb_write8((uint16_t)(slot_hl + 1u), name_hi);

	gb_write8(wCurrentNPCNameTx_ADDR, saved_e);
	gb_write8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u), saved_d);

	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_LoadChallengeHallNPCIntoTxRamSlot */

/* >>> factory ScriptCommand_StartDuel */
IncreaseScriptPointerResult ScriptCommand_StartDuel(uint8_t b, uint8_t c)
{
	SetNPCDuelParamsResult params = SetNPCDuelParams(b, c);
	PermissionResult item = GetItemInLoadedNPCIndex(wScriptNPC, LOADED_NPC_ID);
	uint8_t npc = gb_read8(item.hl);
	SetNPCMatchStartThemeResult theme = SetNPCMatchStartTheme(npc, params.f, params.b, params.c, 0, 0, 0);
	(void)theme;
	if (wNPCDuelDeckID == 0xFFu) {
		uint8_t choice = wMultichoiceTextboxResult_ChooseDeckToDuelAgainst;
		wNPCDuelDeckID = sAaronDeckIDs[choice & 0x03u];
	}
	item = GetItemInLoadedNPCIndex(wScriptNPC, LOADED_NPC_ID);
	npc = gb_read8(item.hl);
	wNPCDuelist = npc;
	wNPCDuelistCopy = npc;
	wNPCDuelistDirection = Func_1c557(npc);
	SetNPCOpponentNameAndPortrait(npc);
	wGameEvent = GAME_EVENT_DUEL;
	wOverworldTransition |= 0x40u;
	return IncreaseScriptPointerBy4();
}
/* <<< factory ScriptCommand_StartDuel */

/* >>> factory ScriptCommand_StartChallengeHallDuel */
IncreaseScriptPointerResult ScriptCommand_StartChallengeHallDuel(uint8_t b, uint8_t c)
{
	(void)SetNPCDuelParams(b, c);
	uint8_t npc = gb_read8(wChallengeHallNPC_ADDR);
	(void)SetNPCDeckIDAndDuelTheme(npc);
	gb_write8(wMatchStartTheme_ADDR, MUSIC_MATCH_START_2);
	npc = gb_read8(wChallengeHallNPC_ADDR);
	wNPCDuelist = npc;
	wNPCDuelistCopy = npc;
	wNPCDuelistDirection = Func_1c557(npc);
	SetNPCOpponentNameAndPortrait(npc);
	wGameEvent = GAME_EVENT_DUEL;
	wOverworldTransition = (uint8_t)(wOverworldTransition | 0x40u);
	return IncreaseScriptPointerBy4();
}
/* <<< factory ScriptCommand_StartChallengeHallDuel */

/* >>> factory ScriptCommand_AskQuestionJump */
ScriptCommand_AskQuestionJumpResult ScriptCommand_AskQuestionJump(uint8_t b, uint8_t c)
{
	FuncC8edResult r = Func_c8ed((uint16_t)(((uint16_t)b << 8) | c));
	wScriptControlByte = hCurMenuItem;
	if (r.f & 0x10u) {
		IncreaseScriptPointerResult inc = IncreaseScriptPointerBy5();
		return (ScriptCommand_AskQuestionJumpResult){inc.a, inc.f, b, inc.c, 0u};
	}
	GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
	if (args.f & 0x80u) {
		IncreaseScriptPointerResult inc = IncreaseScriptPointerBy5();
		return (ScriptCommand_AskQuestionJumpResult){inc.a, inc.f, args.b, inc.c, 0u};
	}
	uint16_t target = (uint16_t)(((uint16_t)args.b << 8) | args.c);
	uint16_t hl = SetScriptPointer(target);
	return (ScriptCommand_AskQuestionJumpResult){args.a, args.f, args.b, args.c, hl};
}
/* <<< factory ScriptCommand_AskQuestionJump */

/* >>> factory ScriptCommand_AskQuestionJumpDefaultYes */
ScriptCommand_AskQuestionJumpResult ScriptCommand_AskQuestionJumpDefaultYes(uint8_t b, uint8_t c)
{
	wDefaultYesOrNo = 1u;
	return ScriptCommand_AskQuestionJump(b, c);
}
/* <<< factory ScriptCommand_AskQuestionJumpDefaultYes */

/* >>> factory ScriptCommand_JumpIfNPCLoaded */
ScriptCommand_JumpIfNPCLoadedResult ScriptCommand_JumpIfNPCLoaded(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_loaded = wLoadedNPCTempIndex;
	uint8_t saved_temp = wTempNPC;
	wTempNPC = c;
	NPCSearchResult search = FindLoadedNPC();
	ScriptCommand_JumpIfEventTrueResult result;
	if (search.f & 0x10u)
		result = script_jump_event_fail(b, hl);
	else
		result = script_jump_event_pass(hl);
	wTempNPC = saved_temp;
	wLoadedNPCTempIndex = saved_loaded;
	return (ScriptCommand_JumpIfNPCLoadedResult){saved_loaded, f, result.b, result.c, d, e, result.hl};
}
/* <<< factory ScriptCommand_JumpIfNPCLoaded */

/* >>> factory CallMapScriptPointerIfExists */
/* scripting.asm:98-101 -- five bytes:
 *   call GetMapScriptPointer / ret nc / jp hl
 * Two exits, and they need DIFFERENT completion modes, which is why the cases
 * mix them:
 *   no script for this map slot (carry clear) -> `ret nc`, an ordinary return
 *   script found (carry set)                  -> `jp hl` transfers to the map
 *      script's own entry, so the case declares pre-ret at that address
 *
 * Neither `ret nc` nor `jp hl` touches a register, so both exits observe exactly
 * what GetMapScriptPointer produced -- and because `hl` IS the jump target,
 * comparing hl is what verifies the transfer. The target is ordinary script code,
 * not a `rst $20`, so no bytecode interpreter is involved on this boundary. */
CallMapScriptResult CallMapScriptPointerIfExists(uint8_t l)
{
	MapScriptResult r = GetMapScriptPointer(l);
	return (CallMapScriptResult){r.a, r.f, r.hl};
}
/* <<< factory CallMapScriptPointerIfExists */

/* >>> factory Func_c9bc */
/* scripting.asm:91-93 -- four bytes:
 *   ld l, MAP_SCRIPT_AFTER_DUEL / jr CallMapScriptPointerIfExists
 * A tail call, so the exits are the callee's: an ordinary return when the map
 * has no AFTER_DUEL script, or `jp hl` into the script entry when it does. The
 * cases mix completion modes accordingly. Nothing between here and there touches
 * a register, so the result is exactly the callee's. */
CallMapScriptResult Func_c9bc(void)
{
	return CallMapScriptPointerIfExists(MAP_SCRIPT_AFTER_DUEL);
}
/* <<< factory Func_c9bc */

/* >>> factory Func_c9c7 */
CallMapScriptResult Func_c9c7(void)
{
	return CallMapScriptPointerIfExists(0x0eu);
}
/* <<< factory Func_c9c7 */

/* >>> factory Func_c9b8 */
CallMapScriptResult Func_c9b8(void)
{
	return CallMapScriptPointerIfExists(MAP_SCRIPT_LOAD_MAP);
}
/* <<< factory Func_c9b8 */

/* >>> factory ScriptCommand_CloseTextBox */
IncreaseScriptPointerResult ScriptCommand_CloseTextBox(void)
{
	CloseTextBox();
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_CloseTextBox */

/* >>> factory ScriptCommand_PrintText */
/* scripting.asm:674-681 */
IncreaseScriptPointerResult ScriptCommand_PrintText(uint8_t b, uint8_t c)
{
	uint16_t text_pointer = (uint16_t)(((uint16_t)b << 8) | c);
	Func_c891(text_pointer);
	return IncreaseScriptPointerBy3();
}
/* <<< factory ScriptCommand_PrintText */

/* >>> factory Func_c9c0 */
CallMapScriptResult Func_c9c0(void)
{
	return CallMapScriptPointerIfExists(MAP_SCRIPT_MOVED_PLAYER);
}
/* <<< factory Func_c9c0 */

/* >>> factory Func_cc32 */
void Func_cc32(uint16_t hl)
{
	uint16_t de = (uint16_t)wCurrentNPCNameTx |
		(uint16_t)((uint16_t)gb_read8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u)) << 8);
	Func_c8ba(hl, de);
}
/* <<< factory Func_cc32 */

/* >>> factory Script_LegendaryCardRightSpark */
void Script_LegendaryCardRightSpark(void)
{
	CloseAdvancedDialogueBox();
}
/* <<< factory Script_LegendaryCardRightSpark */

/* >>> factory ScriptCommand_PrintNPCText */
IncreaseScriptPointerResult ScriptCommand_PrintNPCText(uint8_t b, uint8_t c)
{
	uint16_t text_pointer = (uint16_t)(((uint16_t)b << 8) | c);
	Func_cc32(text_pointer);
	return IncreaseScriptPointerBy3();
}
/* <<< factory ScriptCommand_PrintNPCText */

/* >>> factory ScriptCommand_CloseAdvancedTextBox */
IncreaseScriptPointerResult ScriptCommand_CloseAdvancedTextBox(void)
{
	CloseAdvancedDialogueBox();
	return IncreaseScriptPointerBy1();
}
/* <<< factory ScriptCommand_CloseAdvancedTextBox */

/* >>> factory ScriptCommand_PrintVariableNPCText */
IncreaseScriptPointerResult ScriptCommand_PrintVariableNPCText(uint8_t b, uint8_t c)
{
	uint16_t text_pointer = (uint16_t)(((uint16_t)b << 8) | c);
	if (wScriptControlByte == 0u) {
		GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
		text_pointer = (uint16_t)(((uint16_t)args.b << 8) | args.c);
	}
	Func_cc32(text_pointer);
	return IncreaseScriptPointerBy5();
}
/* <<< factory ScriptCommand_PrintVariableNPCText */

/* >>> factory ScriptCommand_PrintVariableText */
/* scripting.asm:794-810 */
IncreaseScriptPointerResult ScriptCommand_PrintVariableText(uint8_t b, uint8_t c)
{
	uint16_t text_pointer = (uint16_t)(((uint16_t)b << 8) | c);
	if (wScriptControlByte == 0u) {
		GetScriptArgsAfterPointerResult args = GetScriptArgs3AfterPointer();
		text_pointer = (uint16_t)(((uint16_t)args.b << 8) | args.c);
	}
	Func_c891(text_pointer);
	return IncreaseScriptPointerBy5();
}
/* <<< factory ScriptCommand_PrintVariableText */

/* >>> factory ScriptCommand_GiftCenter */
/* scripting.asm:1788-1805. `ld a, c` / `or a` picks the arm. c == 0 shows the
 * gift-center menu and feeds the returned choice to set_event_value
 * EVENT_GIFT_CENTER_MENU_CHOICE (SetStackEventValue reads the db'd event byte
 * and falls through to SetEventValue, which preserves bc and hl); any other c
 * takes .load_gift_center, which stores GAME_EVENT_GIFT_CENTER in wGameEvent
 * and ORs bit 6 into wOverworldTransition -- `set 6, [hl]` leaves the other
 * flags alone. Both arms join at .done and tail-jump to
 * IncreaseScriptPointerBy2, so its exit (a = the new wScriptPointer high byte,
 * f = the adc flags, c = 2) is the whole contract; the menu arm additionally
 * clobbers b, d, e and hl inside GiftCenterMenu, which is why they are not
 * reported. */
IncreaseScriptPointerResult ScriptCommand_GiftCenter(uint8_t c)
{
	if (c == 0u) {
		GiftCenterMenuResult menu = GiftCenterMenu();
		(void)SetEventValue(EVENT_GIFT_CENTER_MENU_CHOICE, 0u, 0u, menu.a);
	} else {
		wGameEvent = GAME_EVENT_GIFT_CENTER;
		wOverworldTransition |= 0x40u;
	}
	return IncreaseScriptPointerBy2();
}
/* <<< factory ScriptCommand_GiftCenter */

/* >>> factory ScriptCommand_PrintTextQuitFully */
/* scripting.asm:806-823 */
ScriptCommand_PrintTextQuitFullyResult ScriptCommand_PrintTextQuitFully(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t saved_hl)
{
	Func_cc32((uint16_t)(((uint16_t)b << 8) | c));
	CloseAdvancedDialogueBox();
	wBreakScriptLoop = 0x01u;
	IncreaseScriptPointerResult pointer = IncreaseScriptPointerBy3();
	return (ScriptCommand_PrintTextQuitFullyResult){pointer.a, pointer.f, 0u, pointer.c, 0x12u, 0x11u, saved_hl};
}
/* <<< factory ScriptCommand_PrintTextQuitFully */

/* >>> factory ScriptCommand_QuitScriptFully */
ScriptCommand_QuitScriptFullyResult ScriptCommand_QuitScriptFully(uint16_t caller_hl)
{
	(void)ScriptCommand_CloseAdvancedTextBox();
	IncreaseScriptPointerResult end = ScriptCommand_EndScript();
	return (ScriptCommand_QuitScriptFullyResult){end.a, end.f, end.c, caller_hl};
}
/* <<< factory ScriptCommand_QuitScriptFully */
