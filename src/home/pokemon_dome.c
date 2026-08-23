#include "home/pokemon_dome.h"

#include "mem.h"
/* >>> factory statics */
#define MAP_EVENT_HALL_OF_HONOR_DOOR 0x01u
/* <<< factory statics */

#define W_LOAD_NPC_X_POS_ADDR 0xD3ACu
#define W_LOAD_NPC_Y_POS_ADDR 0xD3ADu
#define W_LOAD_NPC_DIRECTION_ADDR 0xD3AEu
#define WEST 0x03u

static uint8_t carry_flags(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}

PokemonDomeResult Func_f762(void)
{
	uint8_t y = (uint8_t)(gb_read8(W_LOAD_NPC_Y_POS_ADDR) + 2u);
	gb_write8(W_LOAD_NPC_Y_POS_ADDR, y);
	return (PokemonDomeResult){y, (uint8_t)((y == 0 ? 0x80u : 0x00u) | 0x10u)};
}

PokemonDomeResult Func_f782(uint8_t b, uint8_t c, uint8_t f)
{
	gb_write8(W_LOAD_NPC_X_POS_ADDR, b);
	gb_write8(W_LOAD_NPC_Y_POS_ADDR, c);
	return (PokemonDomeResult){c, carry_flags(f)};
}

PokemonDomeResult PlacePokemonDomeOpponentAtDuelTable(uint8_t f)
{
	gb_write8(W_LOAD_NPC_X_POS_ADDR, 0x12u);
	gb_write8(W_LOAD_NPC_Y_POS_ADDR, 0x0Eu);
	gb_write8(W_LOAD_NPC_DIRECTION_ADDR, WEST);
	return (PokemonDomeResult){WEST, carry_flags(f)};
}

/* >>> factory Func_f77d */
/* pokemon_dome.asm:114-116 (falls through into Func_f782) */
PokemonDomeResult Func_f77d(uint8_t b, uint8_t c, uint8_t f)
{
	gb_write8(W_LOAD_NPC_DIRECTION_ADDR, WEST);
	return Func_f782(b, c, f);
}
/* <<< factory Func_f77d */

/* >>> factory PokemonDomeCloseTextBox */
void PokemonDomeCloseTextBox(void)
{
	ApplyOWMapEventChangeIfEventSet(MAP_EVENT_HALL_OF_HONOR_DOOR);
}
/* <<< factory PokemonDomeCloseTextBox */
