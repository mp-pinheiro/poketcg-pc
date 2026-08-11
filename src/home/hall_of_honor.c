#include "home/hall_of_honor.h"

#include "home/sound.h"

#define SFX_LEGENDARY_CARDS 0x10u

void HallOfHonorLoadMap(void)
{
	PlaySFX(SFX_LEGENDARY_CARDS);
}
