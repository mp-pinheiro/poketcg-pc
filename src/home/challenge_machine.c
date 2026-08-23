#include "home/challenge_machine.h"

#include "generated/sram.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "mem.h"
/* >>> factory statics */
#include "home/challenge_machine.h"
#include "home/random.h"
#include "home/switch_sram.h"
#include "generated/sram.h"
#include "mem.h"

#define CLUB_MASTERS_START 0x18u
#define GRAND_MASTERS_START 0x20u
#define NUM_CHALLENGE_MACHINE_OPPONENTS 0x05u

/* challenge_machine.asm:781-789 ChallengeMachine_FinalOpponentProbabilities.
 * Pairs of (probability weight, opponent id); the last weight is a catch-all. */
static const uint8_t ChallengeMachine_FinalOpponentProbabilities[16] = {
	56u, (uint8_t)(GRAND_MASTERS_START + 0u),
	56u, (uint8_t)(GRAND_MASTERS_START + 1u),
	56u, (uint8_t)(GRAND_MASTERS_START + 2u),
	56u, (uint8_t)(GRAND_MASTERS_START + 3u),
	8u, (uint8_t)(GRAND_MASTERS_START + 4u),
	8u, (uint8_t)(GRAND_MASTERS_START + 5u),
	8u, (uint8_t)(GRAND_MASTERS_START + 6u),
	255u, (uint8_t)(GRAND_MASTERS_START + 7u),
};

#include "home/copy.h"
#include "home/switch_sram.h"
#include "mem.h"

#define NAME_BUFFER_LENGTH 0x10u
#define TRUE_VALUE 0x01u
#define WIN_CAP_HIGH 0x03u
#define WIN_CAP_LOW 0xE7u

/* wChallengeMachineOpponent is not exposed by generated/wram.h in this build. */
#define wChallengeMachineOpponent_ADDR 0xD692u

#include "generated/sram.h"
#include "generated/wram.h"
#include "home/switch_sram.h"

#include "home/challenge_machine.h"
#include "generated/sram.h"
#include "home/switch_sram.h"
#include "mem.h"

#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#define sPlayerInChallengeMachine_ADDR 0xBA44u
#define sTotalChallengeMachineWins_ADDR 0xBA45u
#define sPresentConsecutiveWins_ADDR 0xBA47u
#define sPresentConsecutiveWinsBackup_ADDR 0xBA49u

#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "generated/sram.h"
#define ConsecutiveWinsEndedAtText 0x07e2u

#include "home/challenge_machine.h"
#include "home/switch_sram.h"
#include "home/sound.h"
#include "home/play_song.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "generated/sram.h"
#define MUSIC_MEDAL 0x1du
#define ConsecutiveWinRecordIncreasedText 0x07e8u
#define sConsecutiveWinRecordIncreased_ADDR 0xBA68u
#define sMaximumConsecutiveWins_ADDR 0xBA56u
/* <<< factory statics */

ChallengeMachineCheckResult ChallengeMachine_CheckIfOpponentAlreadySelected(uint8_t a, uint8_t c)
{
	uint16_t hl = sChallengeMachineOpponents_ADDR;
	uint16_t n = c ? c : 0x100u;
	while (n--) {
		if (a == gb_read8(hl))
			return (ChallengeMachineCheckResult){hl, 0x90u};
		hl = (uint16_t)(hl + 1u);
	}
	return (ChallengeMachineCheckResult){hl, a ? 0x00u : 0x80u};
}

ChallengeMachinePrintResult ChallengeMachine_PrintText(uint16_t hl, uint8_t b, uint8_t c)
{
	uint16_t text = (uint16_t)(gb_read8(hl) | ((uint16_t)gb_read8((uint16_t)(hl + 1u)) << 8));
	InitTextPrinting(b, c);
	TextResult result = PrintTextNoDelay(text, b, c);
	return (ChallengeMachinePrintResult){result.hl, b, c};
}

/* >>> factory ChallengeMachine_PickOpponentSequence */
/* challenge_machine.asm:697-779. No arguments and no register outputs: a/f are
 * whatever DisableSRAM leaves, hl is loop residue ($BA55), c is 0 after the
 * clear loop. The whole contract is the SRAM image. */
void ChallengeMachine_PickOpponentSequence(void)
{
	EnableSRAM();

	/* first opponent: any club member */
	gb_write8(sChallengeMachineOpponents_ADDR, Random(CLUB_MASTERS_START));

	/* second opponent: reroll while it duplicates the first */
	for (;;) {
		uint8_t a = Random(CLUB_MASTERS_START);
		ChallengeMachineCheckResult r =
			ChallengeMachine_CheckIfOpponentAlreadySelected(a, 1u);
		if (!(r.f & 0x10u)) {
			gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 1u), a);
			break;
		}
	}

	/* third opponent: reroll while it duplicates either earlier pick */
	for (;;) {
		uint8_t a = Random(CLUB_MASTERS_START);
		ChallengeMachineCheckResult r =
			ChallengeMachine_CheckIfOpponentAlreadySelected(a, 2u);
		if (!(r.f & 0x10u)) {
			gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 2u), a);
			break;
		}
	}

	/* fourth opponent: a club master, no duplicate check */
	{
		uint8_t a = Random((uint8_t)(GRAND_MASTERS_START - CLUB_MASTERS_START));
		a = (uint8_t)(a + CLUB_MASTERS_START);
		gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 3u), a);
	}

	/* fifth opponent: weighted pick from the probability table */
	{
		uint8_t a = UpdateRNGSources();
		uint8_t i = 0;
		while (a >= ChallengeMachine_FinalOpponentProbabilities[i]) {
			a = (uint8_t)(a - ChallengeMachine_FinalOpponentProbabilities[i]);
			i = (uint8_t)(i + 2u);
		}
		gb_write8((uint16_t)(sChallengeMachineOpponents_ADDR + 4u),
			ChallengeMachine_FinalOpponentProbabilities[i + 1u]);
	}

	gb_write8(sChallengeMachineOpponentNumber_ADDR, 0u);
	gb_write8(sConsecutiveWinRecordIncreased_ADDR, 0u);
	for (uint8_t i = 0; i < NUM_CHALLENGE_MACHINE_OPPONENTS; i++)
		gb_write8((uint16_t)(sChallengeMachineDuelResults_ADDR + i), 0u);

	gb_write8(sPresentConsecutiveWins_ADDR,
		gb_read8(sPresentConsecutiveWinsBackup_ADDR));
	gb_write8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u),
		gb_read8((uint16_t)(sPresentConsecutiveWinsBackup_ADDR + 1u)));

	DisableSRAM();
}
/* <<< factory ChallengeMachine_PickOpponentSequence */

/* >>> factory ChallengeMachine_GetCurrentOpponent */
/* challenge_machine.asm:152-162 */
ChallengeMachineOpponentResult ChallengeMachine_GetCurrentOpponent(void)
{
	EnableSRAM();
	uint8_t e = gb_read8(sChallengeMachineOpponentNumber_ADDR);
	uint16_t hl = (uint16_t)(sChallengeMachineOpponents_ADDR + e);
	uint8_t a = gb_read8(hl);
	gb_write8(wChallengeMachineOpponent_ADDR, a);
	DisableSRAM();
	return (ChallengeMachineOpponentResult){ .hl = hl, .d = 0, .e = e };
}
/* <<< factory ChallengeMachine_GetCurrentOpponent */

/* >>> factory ChallengeMachine_IncrementHLMax999 */
/* challenge_machine.asm:239-256. hl points at a little-endian 16-bit counter.
 * The value is incremented unless it is already 999; hl exits advanced to the
 * high byte on the increment path and left on the low byte on the skip path. */
uint16_t ChallengeMachine_IncrementHLMax999(uint16_t hl)
{
	EnableSRAM();
	uint8_t high = gb_read8((uint16_t)(hl + 1));
	if (high == WIN_CAP_HIGH && gb_read8(hl) == WIN_CAP_LOW) {
		DisableSRAM();
		return hl;
	}
	uint8_t low = gb_read8(hl);
	uint8_t sum = (uint8_t)(low + 1u);
	gb_write8(hl, sum);
	hl = (uint16_t)(hl + 1);
	uint8_t carry = (uint8_t)(sum < low ? 1u : 0u);
	gb_write8(hl, (uint8_t)(gb_read8(hl) + carry));
	DisableSRAM();
	return hl;
}
/* <<< factory ChallengeMachine_IncrementHLMax999 */

/* >>> factory ChallengeMachine_CheckForNewRecord */
/* challenge_machine.asm:260-286. No register inputs are consumed; on the
 * no-record path hl exits at sMaximumConsecutiveWins+1 when the high bytes
 * differ and at sMaximumConsecutiveWins when they match, and bc/de pass
 * through. On the new-record path the copy setup leaves hl=sPlayerName,
 * de=sChallengeMachineRecordHolderName and bc=NAME_BUFFER_LENGTH, all of which
 * CopyDataHLtoDE_SaveRegisters restores. */
ChallengeMachineRecordResult ChallengeMachine_CheckForNewRecord(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	EnableSRAM();
	uint8_t max_high = gb_read8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1));
	uint8_t present_high = gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1));
	uint16_t hl = (uint16_t)(sMaximumConsecutiveWins_ADDR + 1);
	int new_record;
	if (present_high != max_high) {
		new_record = present_high > max_high;
	} else {
		hl = sMaximumConsecutiveWins_ADDR;
		uint8_t max_low = gb_read8(hl);
		uint8_t present_low = gb_read8(sPresentConsecutiveWins_ADDR);
		new_record = present_low > max_low;
	}
	if (new_record) {
		uint8_t low = gb_read8(sPresentConsecutiveWins_ADDR);
		gb_write8(sMaximumConsecutiveWins_ADDR, low);
		gb_write8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1),
			gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1)));
		hl = sPlayerName_ADDR;
		uint16_t de = sChallengeMachineRecordHolderName_ADDR;
		CopyDataHLtoDE_SaveRegisters(hl, de, NAME_BUFFER_LENGTH);
		gb_write8(sConsecutiveWinRecordIncreased_ADDR, TRUE_VALUE);
		b = (uint8_t)(NAME_BUFFER_LENGTH >> 8);
		c = (uint8_t)NAME_BUFFER_LENGTH;
		d = (uint8_t)(de >> 8);
		e = (uint8_t)de;
	}
	DisableSRAM();
	return (ChallengeMachineRecordResult){ .hl = hl, .b = b, .c = c, .d = d, .e = e };
}
/* <<< factory ChallengeMachine_CheckForNewRecord */

/* >>> factory ChallengeMachine_RecordDuelResult */
void ChallengeMachine_RecordDuelResult(void)
{
	EnableSRAM();
	uint8_t opponent = gb_read8(sChallengeMachineOpponentNumber_ADDR);
	uint16_t result_address = (uint16_t)(sChallengeMachineDuelResults_ADDR + opponent);
	uint8_t result = gb_read8(wDuelResult_ADDR);
	if (result == 0u) {
		gb_write8(result_address, 1u);
		DisableSRAM();
		(void)ChallengeMachine_IncrementHLMax999(sPresentConsecutiveWins_ADDR);
		return;
	}
	gb_write8(result_address, 2u);
	DisableSRAM();
}
/* <<< factory ChallengeMachine_RecordDuelResult */

/* >>> factory ChallengeMachine_Initialize */
ChallengeMachineInitializeResult ChallengeMachine_Initialize(void)
{
	EnableSRAM();
	uint8_t initialized = 0u;
	if (gb_read8(sChallengeMachineMagic_ADDR) == 0xE3u &&
		gb_read8((uint16_t)(sChallengeMachineMagic_ADDR + 1u)) == 0x95u) {
		initialized = 1u;
	} else {
		uint16_t hl = sChallengeMachineMagic_ADDR;
		uint8_t c = (uint8_t)(sChallengeMachineEnd_ADDR - sChallengeMachineStart_ADDR);
		gb_write8(hl++, 0xE3u);
		gb_write8(hl++, 0x95u);
		while (c != 0u) {
			gb_write8(hl++, 0u);
			c--;
		}
		const uint8_t *text = rom_ptr(0x04u, 0x7674u);
		for (uint8_t i = 0u; i < NAME_BUFFER_LENGTH; i++)
			gb_write8((uint16_t)(sChallengeMachineRecordHolderName_ADDR + i), text[i]);
		gb_write8(sMaximumConsecutiveWins_ADDR, 1u);
		gb_write8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1u), 0u);
	}
	uint8_t a = gb_read8(sPlayerInChallengeMachine_ADDR);
	DisableSRAM();
	return (ChallengeMachineInitializeResult){.a = a, .f = initialized ? 0xC0u : 0x80u};
}
/* <<< factory ChallengeMachine_Initialize */

/* >>> factory ChallengeMachine_Reset */
void ChallengeMachine_Reset(void)
{
	(void)ChallengeMachine_Initialize();
	EnableSRAM();
	gb_write8(sTotalChallengeMachineWins_ADDR, 0u);
	gb_write8((uint16_t)(sTotalChallengeMachineWins_ADDR + 1u), 0u);
	gb_write8(sPresentConsecutiveWins_ADDR, 0u);
	gb_write8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u), 0u);
	gb_write8(sPresentConsecutiveWinsBackup_ADDR, 0u);
	gb_write8((uint16_t)(sPresentConsecutiveWinsBackup_ADDR + 1u), 0u);
	gb_write8(sPlayerInChallengeMachine_ADDR, 0u);
	DisableSRAM();
}
/* <<< factory ChallengeMachine_Reset */

/* >>> factory ChallengeMachine_PrintFinalConsecutiveWinStreak */
ChallengeMachinePrintFinalConsecutiveWinStreakResult ChallengeMachine_PrintFinalConsecutiveWinStreak(uint16_t hl)
{
	EnableSRAM();
	uint8_t low = gb_read8(sPresentConsecutiveWins_ADDR);
	gb_write8(wTxRam3_ADDR, low);
	uint8_t high = gb_read8((uint16_t)(sPresentConsecutiveWins_ADDR + 1u));
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), high);
	if (high == 0u && low < 2u) {
		DisableSRAM();
		return (ChallengeMachinePrintFinalConsecutiveWinStreakResult){0x70u, hl};
	}
	WaitResult printed = PrintScrollableText_NoTextBoxLabel(ConsecutiveWinsEndedAtText);
	DisableSRAM();
	return (ChallengeMachinePrintFinalConsecutiveWinStreakResult){printed.f, ConsecutiveWinsEndedAtText};
}
/* <<< factory ChallengeMachine_PrintFinalConsecutiveWinStreak */

/* >>> factory ChallengeMachine_ShowNewRecord */
ChallengeMachineShowNewRecordResult ChallengeMachine_ShowNewRecord(uint16_t hl)
{
	EnableSRAM();
	uint8_t increased = gb_read8(sConsecutiveWinRecordIncreased_ADDR);
	if (increased == 0u)
		return (ChallengeMachineShowNewRecordResult){0u, 0x80u, hl};

	uint8_t low = gb_read8(sMaximumConsecutiveWins_ADDR);
	gb_write8(wTxRam3_ADDR, low);
	uint8_t high = gb_read8((uint16_t)(sMaximumConsecutiveWins_ADDR + 1u));
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), high);
	DisableSRAM();
	PauseSong();
	PlaySong(MUSIC_MEDAL);
	(void)PrintScrollableText_NoTextBoxLabel(ConsecutiveWinRecordIncreasedText);
	WaitForSongToFinish();
	ResumeSong();
	return (ChallengeMachineShowNewRecordResult){0u, 0u, hl};
}
/* <<< factory ChallengeMachine_ShowNewRecord */
