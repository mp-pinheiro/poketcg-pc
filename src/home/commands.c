#include "home/commands.h"

#include "generated/hram.h"
#include "home/duel.h"
#include "home/play_animation.h"

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

/* AnimationCommandPointerTable indices (commands.asm:162-171, table order). */
#define ANIMCMD_END 0x00u
#define ANIMCMD_NORMAL 0x01u
#define ANIMCMD_PLAYER_SIDE 0x02u
#define ANIMCMD_OPP_SIDE 0x03u
#define ANIMCMD_SET_SCREEN 0x04u
#define ANIMCMD_PLAY_AREA 0x05u
#define ANIMCMD_END_UNUSED 0x06u
#define NUM_ANIM_COMMANDS 0x07u

/* animation_constants.asm: values are the file's own hex annotations. */
#define DUEL_ANIM_SHOW_DAMAGE 0x09u
#define DUEL_ANIM_SMALL_SHAKE_X 0x61u
#define DUEL_ANIM_BIG_SHAKE_X 0x62u
#define DUEL_ANIM_SMALL_SHAKE_Y 0x63u
#define DUEL_ANIM_BIG_SHAKE_Y 0x64u
#define DUEL_ANIM_DAMAGE_HUD 0x8Cu
#define DUEL_ANIM_SET_SCREEN_CMD 0x96u
#define DUEL_ANIM_PRINT_DAMAGE 0x97u
#define DUEL_ANIM_UPDATE_HUD 0x98u
#define DUEL_ANIM_SHAKE1 0xFAu
#define DUEL_ANIM_SHAKE2 0xFBu
#define DUEL_ANIM_SHAKE3 0xFCu

#include "mem.h"

#include "generated/wram.h"
#include "home/substatus.h"
#include "home/print_text.h"

#define RESISTANCE 0x02u
#define WEAKNESS 0x01u
#define AttackDamageText 0x003au
#define NoDamageText 0x003bu
#define ResistanceLessDamageText 0x0036u
#define ResistanceNoDamageText 0x0039u
#define WeaknessMoreDamage2Text 0x0038u
#define WeaknessMoreDamageText 0x0037u

#include "home/printer.h"

#include "generated/wram.h"
#include "home/card_data.h"
#include "home/menus.h"
#include "mem.h"
#define ATK_ANIM_HEAL 0x79u
#define ATK_ANIM_HEALING_WIND_PLAY_AREA 0x86u
#define TX_END 0x00u

#include "generated/wram.h"
#include "home/core.h"
#include "mem.h"
#define DUEL_MAIN_SCENE 0x01u

#include "home/duel_menus.h"

#include "home/script.h"
#define BANK_POINTER_TABLE_ATTACK_ANIMATION 6u
#define POINTER_TABLE_ATTACK_ANIMATION 0x51A4u
#define DUEL_ANIM_SET_SCREEN 0x96u
#define TRUE 0x01u
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

/* >>> factory GetDamageText */
uint16_t GetDamageText(uint16_t hl)
{
	if (hl == 0u) {
		NoDamageOrEffectCheckResult check = CheckNoDamageOrEffect(hl);
		if (check.f & 0x10u)
			return check.hl;
		uint8_t effectiveness = gb_read8(wDamageAnimEffectiveness_ADDR);
		if (effectiveness & (1u << RESISTANCE))
			return ResistanceNoDamageText;
		return NoDamageText;
	}

	LoadTxRam3(hl);
	uint8_t effectiveness = gb_read8(wDamageAnimEffectiveness_ADDR);
	uint8_t flags = (uint8_t)(effectiveness & ((1u << RESISTANCE) | (1u << WEAKNESS)));
	if (flags == 0u)
		return AttackDamageText;
	if (flags == ((1u << RESISTANCE) | (1u << WEAKNESS)))
		return WeaknessMoreDamage2Text;
	if (flags & (1u << WEAKNESS))
		return WeaknessMoreDamageText;
	return ResistanceLessDamageText;
}
/* <<< factory GetDamageText */

/* >>> factory PlayAttackAnimationCommands_NextCommand */
/* commands.asm:41-45. `ld a, [de]` / `inc de` / dispatch through
 * AnimationCommandPointerTable. The incoming `a` is dead: the real routine reads
 * a fresh opcode from the command stream. Every handler continues the chain by
 * re-entering here, which is how the asm's tail-jumps compose into a loop.
 * Opcodes >= NUM_ANIM_COMMANDS index past the table in the real ROM, so they are
 * outside the contract; they terminate here as the END entries do. */
PlayAttackAnimationCommands_NextCommandResult PlayAttackAnimationCommands_NextCommand(uint8_t a, uint8_t d, uint8_t e)
{
	(void)a;
	uint16_t de = (uint16_t)(((uint16_t)d << 8) | e);
	uint8_t opcode = gb_read8(de);
	de++;
	uint8_t nd = (uint8_t)(de >> 8);
	uint8_t ne = (uint8_t)de;
	switch (opcode) {
	case ANIMCMD_NORMAL:
		return AnimationCommand_AnimNormal(nd, ne);
	case ANIMCMD_PLAYER_SIDE:
		return AnimationCommand_AnimPlayer(nd, ne);
	case ANIMCMD_OPP_SIDE:
		return AnimationCommand_AnimOpponent(nd, ne);
	case ANIMCMD_SET_SCREEN:
		return AnimationCommand_AnimScreen(nd, ne);
	case ANIMCMD_PLAY_AREA:
		return AnimationCommand_AnimPlayArea(nd, ne);
	case ANIMCMD_END:
	case ANIMCMD_END_UNUSED:
	default:
		return (PlayAttackAnimationCommands_NextCommandResult){nd, ne};
	}
}
/* <<< factory PlayAttackAnimationCommands_NextCommand */

/* >>> factory AnimationCommand_AnimNormal */
/* commands.asm:81-149. Reads the animation id from the stream; four ids take
 * dedicated paths, everything else plays the id as-is. `.check_duelist` picks
 * `c` when it is the player's turn or wDuelType is 0, otherwise `b`. */
PlayAttackAnimationCommands_NextCommandResult AnimationCommand_AnimNormal(uint8_t d, uint8_t e)
{
	uint16_t de = (uint16_t)(((uint16_t)d << 8) | e);
	uint8_t cmd = gb_read8(de);
	de++;
	const uint8_t nd = (uint8_t)(de >> 8);
	const uint8_t ne = (uint8_t)de;

	if (cmd == DUEL_ANIM_SHOW_DAMAGE) {
		/* .show_damage */
		(void)PlayDuelAnimation(DUEL_ANIM_PRINT_DAMAGE);
		gb_write8(wDuelAnimEffectiveness_ADDR,
			gb_read8(wDamageAnimEffectiveness_ADDR));
		gb_write8(wDuelAnimDamage_ADDR, gb_read8(wDamageAnimAmount_ADDR));
		gb_write8((uint16_t)(wDuelAnimDamage_ADDR + 1u),
			gb_read8((uint16_t)(wDamageAnimAmount_ADDR + 1u)));
		(void)PlayDuelAnimation(DUEL_ANIM_DAMAGE_HUD);
		if (gb_read8(wDuelDisplayedScreen_ADDR) == DUEL_MAIN_SCENE)
			(void)PlayDuelAnimation(DUEL_ANIM_UPDATE_HUD);
		return PlayAttackAnimationCommands_NextCommand(0u, nd, ne);
	}

	uint8_t anim = cmd;
	if (cmd == DUEL_ANIM_SHAKE1 || cmd == DUEL_ANIM_SHAKE2
			|| cmd == DUEL_ANIM_SHAKE3) {
		uint8_t c, b;
		if (cmd == DUEL_ANIM_SHAKE1) {
			c = DUEL_ANIM_SMALL_SHAKE_X;
			b = DUEL_ANIM_SMALL_SHAKE_Y;
		} else if (cmd == DUEL_ANIM_SHAKE2) {
			c = DUEL_ANIM_BIG_SHAKE_X;
			b = DUEL_ANIM_BIG_SHAKE_Y;
		} else {
			c = DUEL_ANIM_SMALL_SHAKE_Y;
			b = DUEL_ANIM_SMALL_SHAKE_X;
		}
		/* .check_duelist */
		if (gb_read8(hWhoseTurn_ADDR) == PLAYER_TURN
				|| gb_read8(wDuelType_ADDR) == 0u)
			anim = c;
		else
			anim = b;
	}

	/* .play_anim */
	(void)PlayDuelAnimation(anim);
	return PlayAttackAnimationCommands_NextCommand(0u, nd, ne);
}
/* <<< factory AnimationCommand_AnimNormal */

/* >>> factory AnimationCommand_AnimPlayer */
/* commands.asm:50-58. Records the acting side then falls into AnimNormal. */
PlayAttackAnimationCommands_NextCommandResult AnimationCommand_AnimPlayer(uint8_t d, uint8_t e)
{
	gb_write8(wDuelAnimDuelistSide_ADDR, gb_read8(hWhoseTurn_ADDR));
	if (gb_read8(wDuelType_ADDR) == 0u)
		gb_write8(wDuelAnimDuelistSide_ADDR, PLAYER_TURN);
	return AnimationCommand_AnimNormal(d, e);
}
/* <<< factory AnimationCommand_AnimPlayer */

/* >>> factory AnimationCommand_AnimOpponent */
/* commands.asm:60-70. Same as AnimPlayer but reads hWhoseTurn between two
 * SwapTurn calls, so it records the NON-turn holder. */
PlayAttackAnimationCommands_NextCommandResult AnimationCommand_AnimOpponent(uint8_t d, uint8_t e)
{
	SwapTurn();
	gb_write8(wDuelAnimDuelistSide_ADDR, gb_read8(hWhoseTurn_ADDR));
	SwapTurn();
	if (gb_read8(wDuelType_ADDR) == 0u)
		gb_write8(wDuelAnimDuelistSide_ADDR, OPPONENT_TURN);
	return AnimationCommand_AnimNormal(d, e);
}
/* <<< factory AnimationCommand_AnimOpponent */

/* >>> factory AnimationCommand_AnimPlayArea */
/* commands.asm:72-76. */
PlayAttackAnimationCommands_NextCommandResult AnimationCommand_AnimPlayArea(uint8_t d, uint8_t e)
{
	uint8_t location = (uint8_t)(gb_read8(wDamageAnimPlayAreaLocation_ADDR) & 0x7Fu);
	gb_write8(wDuelAnimLocationParam_ADDR, location);
	return AnimationCommand_AnimNormal(d, e);
}
/* <<< factory AnimationCommand_AnimPlayArea */

/* >>> factory AnimationCommand_AnimScreen */
/* commands.asm:151-160. */
PlayAttackAnimationCommands_NextCommandResult AnimationCommand_AnimScreen(uint8_t d, uint8_t e)
{
	uint16_t de = (uint16_t)(((uint16_t)d << 8) | e);
	uint8_t screen = gb_read8(de);
	de++;
	gb_write8(wDuelAnimSetScreen_ADDR, screen);
	gb_write8(wDuelAnimLocationParam_ADDR,
		gb_read8(wDamageAnimPlayAreaLocation_ADDR));
	(void)UpdateDuelAnimationScreen(0u);
	(void)PlayDuelAnimation(DUEL_ANIM_SET_SCREEN_CMD);
	return PlayAttackAnimationCommands_NextCommand(0u, (uint8_t)(de >> 8), (uint8_t)de);
}
/* <<< factory AnimationCommand_AnimScreen */

/* >>> factory DuelAnim157 */
void DuelAnim157(void)
{
	return; /* DuelAnim157 */
}
/* <<< factory DuelAnim157 */

/* >>> factory PrintDamageText */
/* commands.asm:277 */
PrintDamageTextResult PrintDamageText(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_b = b;
	uint8_t saved_c = c;
	uint8_t saved_d = d;
	uint8_t saved_e = e;
	uint16_t saved_hl = hl;
	uint8_t attack_animation = gb_read8(wLoadedAttackAnimation_ADDR);
	if (attack_animation == ATK_ANIM_HEAL || attack_animation == ATK_ANIM_HEALING_WIND_PLAY_AREA)
		return (PrintDamageTextResult){saved_b, saved_c, saved_d, saved_e, saved_hl};

	LoadCardDataToBuffer1_FromCardID(gb_read8(wTempNonTurnDuelistCardID_ADDR));
	CopyCardNameAndLevelResult copied = CopyCardNameAndLevel(18u, b, c, d, e);
	gb_write8(copied.hl, TX_END);
	gb_write8(wTxRam2_ADDR, 0u);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);
	uint16_t damage = (uint16_t)(gb_read8(wDamageAnimAmount_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wDamageAnimAmount_ADDR + 1u)) << 8);
	uint16_t text = GetDamageText(damage);
	if (text != 0u)
		(void)DrawWideTextBox_PrintText(text);
	return (PrintDamageTextResult){saved_b, saved_c, saved_d, saved_e, saved_hl};
}
/* <<< factory PrintDamageText */

/* >>> factory UpdateMainSceneHUD */
void UpdateMainSceneHUD(void)
{
	uint8_t displayed_screen = gb_read8(wDuelDisplayedScreen_ADDR);
	if (displayed_screen == DUEL_MAIN_SCENE) {
		DrawDuelHUDs();
	}
}
/* <<< factory UpdateMainSceneHUD */

/* >>> factory SetScreenForDuelAnimation */
void SetScreenForDuelAnimation(uint16_t hl)
{
	uint8_t set_screen = gb_read8(wDuelAnimSetScreen_ADDR);
	if (set_screen == SET_ANIM_SCREEN_MAIN) {
		gb_write8(wDuelAnimationScreen_ADDR, DUEL_ANIM_SCREEN_MAIN_SCENE);
		if (gb_read8(wDuelDisplayedScreen_ADDR) != DUEL_MAIN_SCENE)
			DrawDuelMainScene();
		return;
	}
	if (set_screen != SET_ANIM_SCREEN_PLAY_AREA)
		return;
	UpdateDuelAnimationScreenResult updated = UpdateDuelAnimationScreen(hl);
	uint8_t screen = (uint8_t)updated.hl;
	if (gb_read8(wDuelDisplayedScreen_ADDR) != screen) {
		uint8_t saved_screen = screen;
		uint8_t turn = PLAYER_TURN;
		if (gb_read8(wDuelType_ADDR) == 0u)
			turn = gb_read8(wWhoseTurn_ADDR);
		DrawYourOrOppPlayAreaScreen_Bank0((uint16_t)((updated.hl & 0xff00u) | turn));
		gb_write8(wDuelDisplayedScreen_ADDR, saved_screen);
	}
	(void)DrawWideTextBox();
}
/* <<< factory SetScreenForDuelAnimation */

/* >>> factory PlayAttackAnimationCommands */
PlayAttackAnimationCommands_NextCommandResult PlayAttackAnimationCommands(uint8_t a, uint8_t d, uint8_t e)
{
	(void)a;
	uint8_t loaded_animation = wLoadedAttackAnimation;
	if (loaded_animation == 0u)
		return (PlayAttackAnimationCommands_NextCommandResult){d, e};

	uint16_t table_address = (uint16_t)(POINTER_TABLE_ATTACK_ANIMATION
		+ (uint16_t)loaded_animation * 2u);
	const uint8_t *entry = rom_ptr(BANK_POINTER_TABLE_ATTACK_ANIMATION, table_address);
	uint16_t de = (uint16_t)(entry[0] | (uint16_t)(entry[1] << 8));

	if (wAttackAnimationIsPlaying == 0u) {
		wAttackAnimationIsPlaying = TRUE;
		ResetAnimationQueue();
		wDuelAnimationScreen = DUEL_ANIM_SCREEN_MAIN_SCENE;
		wDuelAnimSetScreen = SET_ANIM_SCREEN_MAIN;
		wDuelAnimLocationParam = 0u;
		if (gb_read8(de) != ANIMCMD_SET_SCREEN)
			(void)PlayDuelAnimation(DUEL_ANIM_SET_SCREEN);
	}

	return PlayAttackAnimationCommands_NextCommand(0u,
		(uint8_t)(de >> 8), (uint8_t)de);
}
/* <<< factory PlayAttackAnimationCommands */
