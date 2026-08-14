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
	if (((EVENT_VAR_MASKS & 0x0FFFu) + (bc & 0x0FFFu)) > 0x0FFFu)
		flags |= 0x20u;
	if ((uint32_t)EVENT_VAR_MASKS + bc > 0xFFFFu)
		flags |= 0x10u;

	gb_write8(wLoadedEventBits_ADDR, entry[1]);
	return (GetEventVarResult){entry[1], flags, b, c,
	                           (uint16_t)(wEventVars_ADDR + entry[0])};
}
/* <<< factory GetEventVar */
