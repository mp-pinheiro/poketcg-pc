#include "home/commands.h"

#include "generated/wram.h"
#include "mem.h"

/* >>> factory statics */
#define PLAYER_TURN ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))
#define SET_ANIM_SCREEN_MAIN 0x01u
#define SET_ANIM_SCREEN_PLAY_AREA 0x04u
#define DUEL_ANIM_SCREEN_MAIN_SCENE 0x00u
#define DUEL_ANIM_SCREEN_PLAYER_PLAY_AREA 0x01u
#define DUEL_ANIM_SCREEN_OPP_PLAY_AREA 0x02u
#define UNKNOWN_SCREEN_4 0x04u
#define UNKNOWN_SCREEN_5 0x05u

#include "mem.h"
/* <<< factory statics */



/* >>> factory AnimationCommand_AnimEnd2 */
/* commands.asm:78 */
uint8_t AnimationCommand_AnimEnd2(uint8_t a)
{
	return a;
}
/* <<< factory AnimationCommand_AnimEnd2 */


/* >>> factory UpdateDuelAnimationScreen */
/* commands.asm:176-234 */
UpdateDuelAnimationScreenResult UpdateDuelAnimationScreen(uint16_t hl)
{
	uint8_t set_screen = gb_read8(wDuelAnimSetScreen_ADDR);
	if (set_screen == SET_ANIM_SCREEN_MAIN) {
		gb_write8(wDuelAnimationScreen_ADDR, DUEL_ANIM_SCREEN_MAIN_SCENE);
		return (UpdateDuelAnimationScreenResult){DUEL_ANIM_SCREEN_MAIN_SCENE,
										 0xC0u, hl};
	}
	if (set_screen != SET_ANIM_SCREEN_PLAY_AREA) {
		uint8_t flags = set_screen == 0 ? 0x70u : 0x40u;
		return (UpdateDuelAnimationScreenResult){set_screen, flags, hl};
	}

	uint8_t location = gb_read8(wDuelAnimLocationParam_ADDR);
	uint8_t whose_turn = gb_read8(wWhoseTurn_ADDR);
	uint8_t duel_type = gb_read8(wDuelType_ADDR);
	uint8_t screen;
	uint8_t screen_turn;
	uint8_t screen_location;
	if (whose_turn == PLAYER_TURN) {
		if ((location & 0x80u) == 0) {
			screen_turn = PLAYER_TURN;
			screen_location = UNKNOWN_SCREEN_4;
			screen = DUEL_ANIM_SCREEN_PLAYER_PLAY_AREA;
		} else {
			screen_turn = OPPONENT_TURN;
			screen_location = UNKNOWN_SCREEN_5;
			screen = DUEL_ANIM_SCREEN_OPP_PLAY_AREA;
		}
	} else if (duel_type == 0) {
		if ((location & 0x80u) == 0) {
			screen_turn = OPPONENT_TURN;
			screen_location = UNKNOWN_SCREEN_4;
			screen = DUEL_ANIM_SCREEN_PLAYER_PLAY_AREA;
		} else {
			screen_turn = PLAYER_TURN;
			screen_location = UNKNOWN_SCREEN_5;
			screen = DUEL_ANIM_SCREEN_OPP_PLAY_AREA;
		}
	} else if ((location & 0x80u) == 0) {
		screen_turn = OPPONENT_TURN;
		screen_location = UNKNOWN_SCREEN_5;
		screen = DUEL_ANIM_SCREEN_OPP_PLAY_AREA;
	} else {
		screen_turn = PLAYER_TURN;
		screen_location = UNKNOWN_SCREEN_4;
		screen = DUEL_ANIM_SCREEN_PLAYER_PLAY_AREA;
	}
	gb_write8(wDuelAnimationScreen_ADDR, screen);
	return (UpdateDuelAnimationScreenResult){screen,
										(location & 0x80u) ? 0x20u : 0xA0u,
										(uint16_t)(((uint16_t)screen_turn << 8) | screen_location)};
}
/* <<< factory UpdateDuelAnimationScreen */

/* >>> factory DuelAnim153 */
/* commands.asm:349. Zero-length label: DuelAnim153 is an alias that falls
 * straight through into the following routine, so as an entry point on its own
 * it executes no instructions and touches no state. */
void DuelAnim153(void)
{
}
/* <<< factory DuelAnim153 */


/* >>> factory AnimationCommand_AnimEnd */
/* commands.asm:47-48 */
void AnimationCommand_AnimEnd(void)
{
	return;
}
/* <<< factory AnimationCommand_AnimEnd */

/* >>> factory DuelAnim154 */
/* commands.asm:350-350 */
void DuelAnim154(void)
{
	return; /* DuelAnim154 */
}
/* <<< factory DuelAnim154 */

/* >>> factory DuelAnim155 */
/* commands.asm:351-351 */
void DuelAnim155(void)
{
	return; /* DuelAnim155 */
}
/* <<< factory DuelAnim155 */

/* >>> factory DuelAnim156 */
/* commands.asm:352-352 */
void DuelAnim156(void)
{
	return; /* DuelAnim156 */
}
/* <<< factory DuelAnim156 */
