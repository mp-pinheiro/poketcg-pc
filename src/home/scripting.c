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
