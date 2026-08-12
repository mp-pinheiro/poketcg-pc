#include "home/challenge_machine.h"

#include "generated/sram.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "mem.h"

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
