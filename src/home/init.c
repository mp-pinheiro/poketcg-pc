#include "home/init.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/core.h"
/* <<< factory statics */

/* >>> factory InitAIDuelVars */
/* init.asm:1-9 */
void InitAIDuelVars(void)
{
	ClearMemory_Bank5((uint8_t)(wAIDuelVarsEnd_ADDR - wAIDuelVars_ADDR), wAIDuelVars_ADDR);
	wAIPokedexCounter = 5u;
	wAIPeekedPrizes = 0xFFu;
}
/* <<< factory InitAIDuelVars */
