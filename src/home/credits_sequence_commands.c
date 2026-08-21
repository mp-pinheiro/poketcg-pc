#include "home/credits_sequence_commands.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/credits_sequence_commands.h"
#include "home/color.h"
#include "home/lcd.h"

#include "generated/wram.h"
#include "home/credits.h"
#include "home/credits_sequence_commands.h"

#include "generated/wram.h"
#include "home/process_text.h"
#include "home/print_text.h"

#define SINGLE_SPACED 0x01u
/* <<< factory statics */

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

/* >>> factory AdvanceCreditsSequenceCmdPtrBy6 */
/* credits_sequence_commands.asm:57-59 */
void AdvanceCreditsSequenceCmdPtrBy6(void)
{
	AdvanceCreditsSequenceCmdPtr(6u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy6 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy4 */
/* credits_sequence_commands.asm:61-65 (fallthrough into AdvanceCreditsSequenceCmdPtr) */
void AdvanceCreditsSequenceCmdPtrBy4(void)
{
	AdvanceCreditsSequenceCmdPtr(4u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy4 */


/* >>> factory CreditsSequenceCmd_Wait */
/* credits_sequence_commands.asm:76-79. Consumes the frame count in c, stores it
 * as the sequence delay, then tail-jumps into AdvanceCreditsSequenceCmdPtrBy3.
 * Exit registers/flags belong to that callee (called as a plain C function here),
 * so no register outputs are claimed; the observable effect is the wSequenceDelay
 * store plus the callee's cmd-pointer advance. */
void CreditsSequenceCmd_Wait(uint8_t c)
{
	wSequenceDelay = c;
	AdvanceCreditsSequenceCmdPtrBy3();
}
/* <<< factory CreditsSequenceCmd_Wait */


/* >>> factory CreditsSequenceCmd_DisableLCD */
/* credits_sequence_commands.asm:298-300. Turns the LCD off, then tail-jumps into
 * AdvanceCreditsSequenceCmdPtrBy2. Exit registers/flags are the callee's, so none
 * are claimed; effects are the LCD write and the cmd-pointer advance. */
void CreditsSequenceCmd_DisableLCD(void)
{
	DisableLCD();
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory CreditsSequenceCmd_DisableLCD */

/* >>> factory CreditsSequenceCmd_TransformOverlay */
void CreditsSequenceCmd_TransformOverlay(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	uint8_t changed = 0;
	uint8_t value = wd647;
	if (value != 0xFFu && value != c) {
		changed = 1;
		value = (uint8_t)(value + (value < c ? 2u : (uint8_t)-2));
	}
	wd647 = value;
	value = wd648;
	if (value != 0xFFu && value != b) {
		changed = 1;
		value = (uint8_t)(value + (value < b ? 2u : (uint8_t)-2));
	}
	wd648 = value;
	value = wd649;
	if (value != 0xFFu && value != e) {
		changed = 1;
		value = (uint8_t)(value + (value < e ? 2u : (uint8_t)-2));
	}
	wd649 = value;
	value = wd64a;
	if (value != 0xFFu && value != d) {
		changed = 1;
		value = (uint8_t)(value + (value < d ? 2u : (uint8_t)-2));
	}
	wd64a = value;
	if (changed != 0) {
		wSequenceDelay = 1;
		return;
	}
	(void)Func_1d765();
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory CreditsSequenceCmd_TransformOverlay */

/* >>> factory CreditsSequenceCmd_FadeIn */
void CreditsSequenceCmd_FadeIn(void)
{
	DisableLCD();
	SetWindowOn();
	FadeScreenFromWhite();
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory CreditsSequenceCmd_FadeIn */

/* >>> factory CreditsSequenceCmd_PrintTextBox */
void CreditsSequenceCmd_PrintTextBox(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	wLineSeparation = SINGLE_SPACED;
	InitTextPrinting(c, b);
	(void)PrintTextNoDelay((uint16_t)(((uint16_t)d << 8) | e), c, b);
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory CreditsSequenceCmd_PrintTextBox */

/* >>> factory CreditsSequenceCmd_InitOverlay */
void CreditsSequenceCmd_InitOverlay(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	wd647 = c;
	wd648 = b;
	wd649 = e;
	wd64a = d;
	(void)Func_1d765();
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory CreditsSequenceCmd_InitOverlay */
