#include "home/credits_sequence_commands.h"

#include "generated/wram.h"
#include "mem.h"

#define CREDITS_SEQUENCE_ADDR 0x5AEFu

void SetCreditsSequenceCmdPtr(void)
{
	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)CREDITS_SEQUENCE_ADDR);
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u),
	          (uint8_t)(CREDITS_SEQUENCE_ADDR >> 8));
	gb_write8(wSequenceDelay_ADDR, 0);
}

void ExecuteCreditsSequenceCmd(void)
{
	uint8_t delay = gb_read8(wSequenceDelay_ADDR);
	if (delay == 0 || delay == 0xFFu)
		return;
	gb_write8(wSequenceDelay_ADDR, (uint8_t)(delay - 1u));
}

void AdvanceCreditsSequenceCmdPtr(uint8_t a)
{
	uint16_t ptr = (uint16_t)(gb_read8(wSequenceCmdPtr_ADDR) |
	                          ((uint16_t)gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u)) << 8));
	ptr = (uint16_t)(ptr + a);
	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)ptr);
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u), (uint8_t)(ptr >> 8));
}

/* >>> factory AdvanceCreditsSequenceCmdPtrBy2 */
/* credits_sequence_commands.asm:45-47 */
void AdvanceCreditsSequenceCmdPtrBy2(void)
{
	AdvanceCreditsSequenceCmdPtr(2u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy2 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy3 */
/* credits_sequence_commands.asm:49-51 */
void AdvanceCreditsSequenceCmdPtrBy3(void)
{
	AdvanceCreditsSequenceCmdPtr(3u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy3 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy5 */
/* credits_sequence_commands.asm:53-55 */
void AdvanceCreditsSequenceCmdPtrBy5(void)
{
	AdvanceCreditsSequenceCmdPtr(5u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy5 */
