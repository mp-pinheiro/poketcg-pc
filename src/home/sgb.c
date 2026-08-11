#include "home/sgb.h"

/* sgb.asm:258-274. The delay loop has no observable effects beyond its
 * register residue: DE and A end at zero, and the final OR leaves Z set. */
SGBWaitResult Wait(uint16_t bc)
{
	uint32_t count = bc ? bc : 0x10000u;

	while (count--) {
		uint16_t de = 1750u;
		do {
			de--;
		} while (de != 0);
	}

	return (SGBWaitResult){0, 0x80u, 0, 0, 0, 0};
}
