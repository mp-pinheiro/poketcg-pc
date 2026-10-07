/* >>> part includes */
#include "home/water_club.h"

#include "mem.h"
/* <<< part includes */
/* >>> part includes_2 */
#include "home/scripting.h"
#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/wram.h"

#include "home/grass_club_entrance.h"
/* <<< part includes_2 */
/* >>> part WaterClubAfterDuelTable */
#define WaterClubAfterDuelTable (WaterClubAfterDuel__after_duel_table_ADDR)
/* <<< part WaterClubAfterDuelTable */

/* >>> part W_ACTIVE_GAME_EVENT_ADDR */
#define W_ACTIVE_GAME_EVENT_ADDR wActiveGameEvent_ADDR
/* <<< part W_ACTIVE_GAME_EVENT_ADDR */
/* >>> part W_PLAYER_X_COORD_ADDR */
#define W_PLAYER_X_COORD_ADDR wPlayerXCoord_ADDR
/* <<< part W_PLAYER_X_COORD_ADDR */
/* >>> part W_PLAYER_Y_COORD_ADDR */
#define W_PLAYER_Y_COORD_ADDR wPlayerYCoord_ADDR
/* <<< part W_PLAYER_Y_COORD_ADDR */
/* >>> part W_LOAD_NPC_X_POS_ADDR */
#define W_LOAD_NPC_X_POS_ADDR wLoadNPCXPos_ADDR
/* <<< part W_LOAD_NPC_X_POS_ADDR */
/* >>> part W_D3D0_ADDR */
#define W_D3D0_ADDR wd3d0_ADDR
/* <<< part W_D3D0_ADDR */

/* >>> factory Preload_Amy */
PreloadAmyResult Preload_Amy(void)
{
	uint8_t event = gb_read8(W_ACTIVE_GAME_EVENT_ADDR);
	uint8_t x = gb_read8(W_PLAYER_X_COORD_ADDR);
	uint8_t y = gb_read8(W_PLAYER_Y_COORD_ADDR);
	uint8_t a = 0;
	uint8_t f = 0x90u;

	gb_write8(W_D3D0_ADDR, 0);
	if (event != 0) {
		f = 0x10u;
		if (x == 0x14u) {
			if (y == 0x06u) {
				gb_write8(W_LOAD_NPC_X_POS_ADDR, 0x14u);
				gb_write8(W_D3D0_ADDR, 1);
				a = 1;
				f = 0x90u;
			} else {
				a = y;
			}
		} else {
			a = x;
		}
	}
	return (PreloadAmyResult){a, f};
}
/* <<< factory Preload_Amy */

/* >>> factory WaterClubMovePlayer */
WaterClubMovePlayerResult WaterClubMovePlayer(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t y = wPlayerYCoord;
	if (y != 8u) {
		uint8_t z = (y == 8u) ? 0x80u : 0u;
		uint8_t h = ((y & 0x0Fu) < (8u & 0x0Fu)) ? 0x20u : 0u;
		uint8_t carry = (y < 8u) ? 0x10u : 0u;
		uint8_t f = (uint8_t)(z | 0x40u | h | carry);
		return (WaterClubMovePlayerResult){y, f, b, c, hl};
	}
	uint8_t event = GetEventValue(EVENT_JOSHUA_STATE);
	if (event >= JOSHUA_DEFEATED) {
		uint8_t z = (event == JOSHUA_DEFEATED) ? 0x80u : 0u;
		uint8_t h = ((event & 0x0Fu) < (JOSHUA_DEFEATED & 0x0Fu)) ? 0x20u : 0u;
		uint8_t carry = (event < JOSHUA_DEFEATED) ? 0x10u : 0u;
		uint8_t f = (uint8_t)(z | 0x40u | h | carry);
		return (WaterClubMovePlayerResult){event, f, b, c, hl};
	}
	wTempNPC = NPC_JOSHUA;
	SetNextNPCAndScriptResult r = SetNextNPCAndScript(Script_NotReadyToSeeAmy_ADDR, hl);
	return (WaterClubMovePlayerResult){r.a, r.f, r.b, r.c, r.hl};
}
/* <<< factory WaterClubMovePlayer */

/* >>> factory WaterClubAfterDuel */
WaterClubAfterDuelResult WaterClubAfterDuel(void)
{
	gb_write8(0x2000u, WaterClubAfterDuel__after_duel_table_BANK);
	FindEndOfDuelScriptResult r = FindEndOfDuelScript(WaterClubAfterDuelTable);
	return (WaterClubAfterDuelResult){r.a, r.f, r.b, r.c, r.d, r.e, r.hl};
}
/* <<< factory WaterClubAfterDuel */
