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
