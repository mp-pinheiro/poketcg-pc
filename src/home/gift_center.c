#include "home/gift_center.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define CONSOLE_CGB 0x02u
#define NORTH 0x00u
/* <<< factory statics */

/* >>> factory Preload_GiftCenterClerk */
PreloadGiftCenterClerkResult Preload_GiftCenterClerk(void)
{
	uint8_t console = gb_read8(wConsole_ADDR);

	if (console == CONSOLE_CGB)
		return (PreloadGiftCenterClerkResult){console, 0x90u};

	gb_write8(wLoadNPCDirection_ADDR, NORTH);
	return (PreloadGiftCenterClerkResult){NORTH, 0x10u};
}
/* <<< factory Preload_GiftCenterClerk */

/* >>> factory Func_fc7a */
/* gift_center.asm:13-16 -- the routine's entire CODE portion, 8 bytes:
 *   ld a, [wConsole] / ld c, a / set_event_value <event>
 * The macro is `call SetStackEventValue` + `db`; the callee consumes the db via
 * GetByteAfterCall and returns PAST it, to the `rst $20` at $7C82 that begins
 * the script bytecode. The cases declare completion pre-ret there.
 *
 * SetEventValue writes (~mask & [hl]) | ((c << tz(mask)) & mask), with
 * (offset, mask) read from EventVarMasks[id*2]. Verified against the ROM
 * 2026-08-26: offset 0x1B, mask 0xFF, shift-alignment loop runs 0 times.
 * A 0xFF mask replaces the whole byte. */
Func_fc7aResult Func_fc7a(void)
{
	uint8_t value = gb_read8(wConsole_ADDR);
	uint16_t event_addr = (uint16_t)(wEventVars_ADDR + 0x1Bu);
	uint8_t event = gb_read8(event_addr);
	uint8_t written;
	gb_write8(wLoadedEventBits_ADDR, 0xFFu);
	written = (uint8_t)((event & (uint8_t)~0xFFu) | (value & 0xFFu));
	gb_write8(event_addr, written);
	return (Func_fc7aResult){written, value};
}
/* <<< factory Func_fc7a */

/* >>> factory Func_fcad */
/* gift_center.asm:38-41 -- the routine's entire CODE portion, 8 bytes:
 *   ld a, [wGiftCenterChoice] / ld c, a / set_event_value <event>
 * The macro is `call SetStackEventValue` + `db`; the callee consumes the db via
 * GetByteAfterCall and returns PAST it, to the `rst $20` at $7CB5 that begins
 * the script bytecode. The cases declare completion pre-ret there.
 *
 * SetEventValue writes (~mask & [hl]) | ((c << tz(mask)) & mask), with
 * (offset, mask) read from EventVarMasks[id*2]. Verified against the ROM
 * 2026-08-26: offset 0x1A, mask 0xFC, shift-alignment loop runs 2 times.
 * `sla c` is an 8-bit shift, so the aligned value truncates to 8 bits before
 * the mask applies. This event shares event-var byte 0x1A with
 * EVENT_AARON_BOOSTER_REWARD (mask 0x03), which owns the low bits. */
Func_fcadResult Func_fcad(void)
{
	uint8_t value = gb_read8(wGiftCenterChoice_ADDR);
	uint16_t event_addr = (uint16_t)(wEventVars_ADDR + 0x1Au);
	uint8_t event = gb_read8(event_addr);
	uint8_t written;
	gb_write8(wLoadedEventBits_ADDR, 0xFCu);
	written = (uint8_t)((event & (uint8_t)~0xFCu) | ((uint8_t)(value << 2u) & 0xFCu));
	gb_write8(event_addr, written);
	return (Func_fcadResult){written, value};
}
/* <<< factory Func_fcad */
