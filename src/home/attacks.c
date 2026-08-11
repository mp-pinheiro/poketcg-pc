#include "home/attacks.h"

#include "generated/wram.h"
#include "mem.h"

/* engine/duel/ai/attacks.asm:26-41 */
void RetrievePlayAreaAIScoreFromBackup2(void)
{
	for (uint8_t i = 0; i < 6; i++)
		gb_write8((uint16_t)(wPlayAreaAIScore_ADDR + i),
			  gb_read8((uint16_t)(wTempPlayAreaAIScore_ADDR + i)));
	gb_write8(wAIScore_ADDR, gb_read8(wTempAIScore_ADDR));
}
