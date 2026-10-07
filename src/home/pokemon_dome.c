/* >>> part includes */
#include "home/pokemon_dome.h"

#include "home/map_events.h"
#include "mem.h"
/* <<< part includes */

/* >>> part includes_2 */
#include "home/pokemon_dome.h"
#include "home/scripting.h"
#include "mem.h"
#include "home/mail.h"
#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/wram.h"
#include "home/fire_club_lobby.h"
#include "home/grass_club_entrance.h"
/* <<< part includes_2 */
/* >>> part PokemonDomeAfterDuelTable */
#define PokemonDomeAfterDuelTable (PokemonDomeAfterDuel__after_duel_table_ADDR)
/* <<< part PokemonDomeAfterDuelTable */

/* >>> part preload_grand_master */
static PokemonDomeResult preload_grand_master(uint8_t event, uint8_t x, uint8_t y,
	uint8_t challenged, uint8_t defeated)
{
	uint8_t a = GetEventValue(event);
	if (a == challenged)
		return PlacePokemonDomeOpponentAtDuelTable(0x80u);
	if (a == defeated)
		return Func_f77d(x, y, 0x80u);
	if (GetEventValue(EVENT_CHALLENGED_GRAND_MASTERS) != 0u)
		return Func_f762();
	return (PokemonDomeResult){a, 0x90u};
}
/* <<< part preload_grand_master */

/* >>> part W_LOAD_NPC_X_POS_ADDR */
#define W_LOAD_NPC_X_POS_ADDR wLoadNPCXPos_ADDR
/* <<< part W_LOAD_NPC_X_POS_ADDR */
/* >>> part W_LOAD_NPC_Y_POS_ADDR */
#define W_LOAD_NPC_Y_POS_ADDR wLoadNPCYPos_ADDR
/* <<< part W_LOAD_NPC_Y_POS_ADDR */
/* >>> part W_LOAD_NPC_DIRECTION_ADDR */
#define W_LOAD_NPC_DIRECTION_ADDR wLoadNPCDirection_ADDR
/* <<< part W_LOAD_NPC_DIRECTION_ADDR */

/* >>> part carry_flags */
static uint8_t carry_flags(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< part carry_flags */

/* >>> factory Func_f762 */
PokemonDomeResult Func_f762(void)
{
	uint8_t y = (uint8_t)(gb_read8(W_LOAD_NPC_Y_POS_ADDR) + 2u);
	gb_write8(W_LOAD_NPC_Y_POS_ADDR, y);
	return (PokemonDomeResult){y, (uint8_t)((y == 0 ? 0x80u : 0x00u) | 0x10u)};
}
/* <<< factory Func_f762 */

/* >>> factory Func_f782 */
PokemonDomeResult Func_f782(uint8_t b, uint8_t c, uint8_t f)
{
	gb_write8(W_LOAD_NPC_X_POS_ADDR, b);
	gb_write8(W_LOAD_NPC_Y_POS_ADDR, c);
	return (PokemonDomeResult){c, carry_flags(f)};
}
/* <<< factory Func_f782 */

/* >>> factory PlacePokemonDomeOpponentAtDuelTable */
PokemonDomeResult PlacePokemonDomeOpponentAtDuelTable(uint8_t f)
{
	gb_write8(W_LOAD_NPC_X_POS_ADDR, 0x12u);
	gb_write8(W_LOAD_NPC_Y_POS_ADDR, 0x0Eu);
	gb_write8(W_LOAD_NPC_DIRECTION_ADDR, WEST);
	return (PokemonDomeResult){WEST, carry_flags(f)};
}
/* <<< factory PlacePokemonDomeOpponentAtDuelTable */

/* >>> factory Func_f77d */
/* pokemon_dome.asm:114-116 (falls through into Func_f782) */
PokemonDomeResult Func_f77d(uint8_t b, uint8_t c, uint8_t f)
{
	gb_write8(W_LOAD_NPC_DIRECTION_ADDR, WEST);
	return Func_f782(b, c, f);
}
/* <<< factory Func_f77d */
/* >>> factory Preload_Courtney */
/* pokemon_dome.asm:85-95 */
PokemonDomeResult Preload_Courtney(void)
{
	return preload_grand_master(EVENT_COURTNEY_STATE, 0x16u, 0x0Cu,
		COURTNEY_CHALLENGED, COURTNEY_DEFEATED);
}
/* <<< factory Preload_Courtney */

/* >>> factory Preload_Steve */
/* pokemon_dome.asm:125-135 */
PokemonDomeResult Preload_Steve(void)
{
	return preload_grand_master(EVENT_STEVE_STATE, 0x16u, 0x0Eu,
		STEVE_CHALLENGED, STEVE_DEFEATED);
}
/* <<< factory Preload_Steve */

/* >>> factory Preload_Jack */
/* pokemon_dome.asm:137-147 */
PokemonDomeResult Preload_Jack(void)
{
	return preload_grand_master(EVENT_JACK_STATE, 0x14u, 0x0Au,
		JACK_CHALLENGED, JACK_DEFEATED);
}
/* <<< factory Preload_Jack */

/* >>> factory Preload_Rod */
/* pokemon_dome.asm:149-161 */
PokemonDomeResult Preload_Rod(void)
{
	uint8_t a = GetEventValue(EVENT_ROD_STATE);
	if (a == ROD_CHALLENGED)
		return PlacePokemonDomeOpponentAtDuelTable(0x80u);
	a = GetEventValue(EVENT_POKEMON_DOME_STATE);
	if (a == POKEMON_DOME_DEFEATED)
		return Func_f782(0x10u, 0x0Au, 0x80u);
	if (a == POKEMON_DOME_CHALLENGED)
		return Func_f782(0x0Eu, 0x0Au, 0x80u);
	return (PokemonDomeResult){a, 0x10u};
}
/* <<< factory Preload_Rod */

/* >>> factory Preload_Ronald1InPokemonDome */
/* pokemon_dome.asm:163-175 */
PokemonDomeResult Preload_Ronald1InPokemonDome(void)
{
	uint8_t a = GetEventValue(EVENT_RONALD_POKEMON_DOME_STATE);
	if (a >= RONALD_DEFEATED) {
		uint8_t f = 0x40u;
		if (a == RONALD_DEFEATED)
			f |= 0x80u;
		return (PokemonDomeResult){a, f};
	}
	a = GetEventValue(EVENT_RONALD_POKEMON_DOME_STATE);
	if (a != 0u) {
		wDefaultSong = MUSIC_RONALD;
		return PlacePokemonDomeOpponentAtDuelTable(0u);
	}
	return (PokemonDomeResult){a, 0x90u};
}
/* <<< factory Preload_Ronald1InPokemonDome */

/* >>> factory PokemonDomeCloseTextBox */
void PokemonDomeCloseTextBox(void)
{
	ApplyOWMapEventChangeIfEventSet(MAP_EVENT_HALL_OF_HONOR_DOOR);
}
/* <<< factory PokemonDomeCloseTextBox */

/* >>> factory PokemonDomeMovePlayer */
void PokemonDomeMovePlayer(void)
{
	if (gb_read8(wPlayerYCoord_ADDR) != 0x16u)
		return;
	uint8_t x = gb_read8(wPlayerXCoord_ADDR);
	if (x < 0x0Eu)
		return;
	if (x >= 0x11u)
		return;
	gb_write8(wTempNPC_ADDR, 0x3Au);
	(void)SetNextNPCAndScript(Script_f84c_ADDR, PokemonDomeMovePlayer_ADDR);
}
/* <<< factory PokemonDomeMovePlayer */

/* >>> factory PokemonDomeLoadMap */
void PokemonDomeLoadMap(void)
{
	TryGivePCPack(0x0Du);
	/* pokemon_dome.asm PokemonDomeLoadMap: `get_event_value` goes through
	 * GetEventVar, which leaves the event's mask in wLoadedEventBits. */
	if (GetEventValue(EVENT_POKEMON_DOME_IN_MENU) == 0u)
		return;
	SetNextScript(Script_f80b_ADDR);
}
/* <<< factory PokemonDomeLoadMap */

/* >>> factory PokemonDomeAfterDuel */
PokemonDomeAfterDuelResult PokemonDomeAfterDuel(void)
{
	gb_write8(0x2000u, PokemonDomeAfterDuel__after_duel_table_BANK);
	/* pokemon_dome.asm PokemonDomeAfterDuel: the table lookup and `ret`; the
	 * map's load-map script is not part of it. */
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(PokemonDomeAfterDuelTable);
	return (PokemonDomeAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory PokemonDomeAfterDuel */
