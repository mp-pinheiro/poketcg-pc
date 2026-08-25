#include "home/pokemon_dome.h"

#include "mem.h"
/* >>> factory statics */
#define MAP_EVENT_HALL_OF_HONOR_DOOR 0x01u

#include "home/pokemon_dome.h"
#include "home/scripting.h"
#include "mem.h"

#include "home/scripting.h"
#include "home/mail.h"
#include "generated/wram.h"
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

/* >>> factory PokemonDomeMovePlayer */
void PokemonDomeMovePlayer(void)
{
	if (gb_read8(0xD331u) != 0x16u)
		return;
	uint8_t x = gb_read8(0xD330u);
	if (x < 0x0Eu)
		return;
	if (x >= 0x11u)
		return;
	gb_write8(0xD3ABu, 0x3Au);
	(void)SetNextNPCAndScript(0x784Cu, 0x76C6u);
}
/* <<< factory PokemonDomeMovePlayer */

/* >>> factory PokemonDomeLoadMap */
void PokemonDomeLoadMap(void)
{
	TryGivePCPack(0x0Du);
	uint8_t value = (uint8_t)((gb_read8(0xD3E9u) & 0x08u) >> 3);
	if (value == 0u)
		return;
	SetNextScript(0x780Bu);
}
/* <<< factory PokemonDomeLoadMap */
