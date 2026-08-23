#include "home/battle_center.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/battle_center.h"
#include "home/scripting.h"
#include "generated/wram.h"
#include "mem.h"
#define DUEL_LOSS 0x01u
/* <<< factory statics */

/* >>> factory Func_fc2b */
void Func_fc2b(void)
{
	uint8_t a = wDuelResult;
	if (a >= (DUEL_LOSS + 1u))
		a = 2u;
	uint16_t bc;
	if (a == 0u)
		bc = 0x7C64u;
	else if (a == 1u)
		bc = 0x7C68u;
	else
		bc = 0x7C60u;
	wCurrentNPCNameTx = (uint8_t)(0x03B0u & 0xFFu);
	gb_write8((uint16_t)(wCurrentNPCNameTx_ADDR + 1u), (uint8_t)(0x03B0u >> 8));
	SetNextScript(bc);
}
/* <<< factory Func_fc2b */
