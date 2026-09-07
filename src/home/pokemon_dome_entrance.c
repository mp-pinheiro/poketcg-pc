#include "home/pokemon_dome_entrance.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/scripting.h"
#include "home/map_events.h"
#define MAP_EVENT_POKEMON_DOME_DOOR 0x00u
#define EVENT_HALL_OF_HONOR_DOORS_OPEN 0x63u
#define EVENT_POKEMON_DOME_STATE 0x65u
#define EVENT_COURTNEY_STATE 0x68u
#define EVENT_STEVE_STATE 0x69u
#define EVENT_JACK_STATE 0x6Au
#define EVENT_ROD_STATE 0x6Bu
#define EVENT_RECEIVED_LEGENDARY_CARDS 0x22u
#define EVENT_RONALD_POKEMON_DOME_STATE 0x6Cu
/* <<< factory statics */

/* >>> factory PokemonDomeEntranceLoadMap */
/* pokemon_dome_entrance.asm:1-12 */
PokemonDomeEntranceLoadMapResult PokemonDomeEntranceLoadMap(void)
{
	(void)ZeroOutEventValue(EVENT_HALL_OF_HONOR_DOORS_OPEN, 0u, 0u, 0u);
	(void)ZeroOutEventValue(EVENT_POKEMON_DOME_STATE, 0u, 0u, 0u);
	(void)ZeroOutEventValue(EVENT_COURTNEY_STATE, 0u, 0u, 0u);
	(void)ZeroOutEventValue(EVENT_STEVE_STATE, 0u, 0u, 0u);
	(void)ZeroOutEventValue(EVENT_JACK_STATE, 0u, 0u, 0u);
	(void)ZeroOutEventValue(EVENT_ROD_STATE, 0u, 0u, 0u);
	uint8_t a = GetEventValue(EVENT_RECEIVED_LEGENDARY_CARDS);
	if (a != 0u)
		return (PokemonDomeEntranceLoadMapResult){a, 0u};
	SetEventValueResult r = ZeroOutEventValue(EVENT_RONALD_POKEMON_DOME_STATE, 0u, 0u, 0u);
	return (PokemonDomeEntranceLoadMapResult){r.a, r.f};
}
/* <<< factory PokemonDomeEntranceLoadMap */

/* >>> factory PokemonDomeEntranceCloseTextBox */
void PokemonDomeEntranceCloseTextBox(void)
{
	ApplyOWMapEventChangeIfEventSet(MAP_EVENT_POKEMON_DOME_DOOR);
}
/* <<< factory PokemonDomeEntranceCloseTextBox */
