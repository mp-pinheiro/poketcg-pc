#include "home/sgb.h"

uint8_t Wait(uint16_t bc, uint16_t *de)
{
	uint32_t outer = bc != 0 ? bc : 0x10000u;

	while (outer-- != 0) {
		uint16_t inner = 1750;
		while (inner-- != 0)
			;
	}
	*de = 0;
	return 0;
}
