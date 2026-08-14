#include "home/credits.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define R_STAT        0xFF41u
#define R_IE          0xFFFFu
#define STAT_LYC_MASK 0x40u
#define IE_STAT_MASK  0x02u
/* <<< factory statics */

/* >>> factory Func_1d758 */
/* credits.asm:79-86 */
void Func_1d758(void)
{
	gb_write8(R_STAT, (uint8_t)(gb_read8(R_STAT) & (uint8_t)~STAT_LYC_MASK));
	gb_write8(R_IE, (uint8_t)(gb_read8(R_IE) & (uint8_t)~IE_STAT_MASK));
}
/* <<< factory Func_1d758 */
