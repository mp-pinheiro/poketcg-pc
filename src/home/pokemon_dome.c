#include "home/pokemon_dome.h"

#include "generated/wram.h"

static uint8_t set_carry(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}

uint8_t Func_f762(uint8_t f)
{
	wLoadNPCYPos = (uint8_t)(wLoadNPCYPos + 2u);
	return set_carry(f);
}

uint8_t PlacePokemonDomeOpponentAtDuelTable(uint8_t f)
{
	wLoadNPCXPos = 0x12;
	wLoadNPCYPos = 0x0E;
	wLoadNPCDirection = 0x03;
	return set_carry(f);
}

uint8_t Func_f782(uint8_t b, uint8_t c, uint8_t f)
{
	wLoadNPCXPos = b;
	wLoadNPCYPos = c;
	return set_carry(f);
}
