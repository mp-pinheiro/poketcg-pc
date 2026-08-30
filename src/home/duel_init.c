#include "home/duel_init.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
/* <<< factory statics */

/* >>> factory Duel_Init */
DuelInitResult Duel_Init(uint8_t f)
{
	uint8_t saved_d291 = wd291;
	wTextBoxFrameType = 4u;
	wLCDC = 0x80u;
	return (DuelInitResult){saved_d291, f};
}
/* <<< factory Duel_Init */
