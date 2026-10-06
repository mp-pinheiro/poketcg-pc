#include "home/battle_center.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/battle_center.h"
#include "home/scripting.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< factory statics */

/* >>> factory Func_fc2b */
void Func_fc2b(void)
{
	uint8_t a = wDuelResult;
	if (a >= (DUEL_LOSS + 1u))
		a = 2u;
	uint16_t bc;
	if (a == 0u)
		bc = Script_fc64_ADDR;
	else if (a == 1u)
		bc = Script_fc68_ADDR;
	else
		bc = Script_fc60_ADDR;
	wCurrentNPCNameTx = (uint8_t)(0x03B0u & 0xFFu);
	gb_write8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u), (uint8_t)(0x03B0u >> 8));
	SetNextScript(bc);
}
/* <<< factory Func_fc2b */
