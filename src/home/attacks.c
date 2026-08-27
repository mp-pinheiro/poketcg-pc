#include "home/attacks.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/hram.h"
#include "home/core.h"
/* <<< factory statics */

/* engine/duel/ai/attacks.asm:26-41 */
void RetrievePlayAreaAIScoreFromBackup2(void)
{
	for (uint8_t i = 0; i < 6; i++)
		gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + i),
			  gb_read8((uint16_t)(wTempPlayAreaAIScore_ADDR + i)));
	gb_write8(wAIScore_ADDR, gb_read8(wTempAIScore_ADDR));
}

/* >>> factory GetAIScoreOfAttack */
void GetAIScoreOfAttack(uint8_t a)
{
	wSelectedAttack = a;
	wAIScore = 0x50u;
	hTempPlayAreaLocation_ff9d = 0u;
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((unusable.f & 0x10u) != 0u)
		wAIScore = 0u;
}
/* <<< factory GetAIScoreOfAttack */
