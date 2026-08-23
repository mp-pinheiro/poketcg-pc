#include "home/pokemon_dome_entrance.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#define MAP_EVENT_POKEMON_DOME_DOOR 0x00u
/* <<< factory statics */

/* >>> factory PokemonDomeEntranceCloseTextBox */
void PokemonDomeEntranceCloseTextBox(void)
{
	ApplyOWMapEventChangeIfEventSet(MAP_EVENT_POKEMON_DOME_DOOR);
}
/* <<< factory PokemonDomeEntranceCloseTextBox */
