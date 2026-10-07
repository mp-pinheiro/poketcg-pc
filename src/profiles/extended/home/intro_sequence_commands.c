/* >>> part includes */
#include "home/intro_sequence_commands.h"

#include "generated/rom.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/color.h"
#include "home/init_menu.h"
#include "home/intro.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/play_animation.h"
#include "home/switch_rom.h"
#include "home/sound.h"
/* <<< part includes */
/* >>> part INTRO_SEQUENCE_CMD_WAIT_ORBS_ANIMATION */
#define INTRO_SEQUENCE_CMD_WAIT_ORBS_ANIMATION (IntroSequenceCmd_WaitOrbsAnimation_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_WAIT_ORBS_ANIMATION */
/* >>> part INTRO_SEQUENCE_CMD_WAIT */
#define INTRO_SEQUENCE_CMD_WAIT (IntroSequenceCmd_Wait_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_WAIT */
/* >>> part INTRO_SEQUENCE_CMD_SET_ORBS_ANIMATIONS */
#define INTRO_SEQUENCE_CMD_SET_ORBS_ANIMATIONS (IntroSequenceCmd_SetOrbsAnimations_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_SET_ORBS_ANIMATIONS */
/* >>> part INTRO_SEQUENCE_CMD_SET_ORBS_COORDINATES */
#define INTRO_SEQUENCE_CMD_SET_ORBS_COORDINATES (IntroSequenceCmd_SetOrbsCoordinates_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_SET_ORBS_COORDINATES */
/* >>> part INTRO_SEQUENCE_CMD_PLAY_TITLE_SCREEN_MUSIC */
#define INTRO_SEQUENCE_CMD_PLAY_TITLE_SCREEN_MUSIC (IntroSequenceCmd_PlayTitleScreenMusic_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_PLAY_TITLE_SCREEN_MUSIC */
/* >>> part INTRO_SEQUENCE_CMD_WAIT_SFX */
#define INTRO_SEQUENCE_CMD_WAIT_SFX (IntroSequenceCmd_WaitSFX_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_WAIT_SFX */
/* >>> part INTRO_SEQUENCE_CMD_PLAY_SFX */
#define INTRO_SEQUENCE_CMD_PLAY_SFX (IntroSequenceCmd_PlaySFX_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_PLAY_SFX */
/* >>> part INTRO_SEQUENCE_CMD_FADE_IN */
#define INTRO_SEQUENCE_CMD_FADE_IN (IntroSequenceCmd_FadeIn_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_FADE_IN */
/* >>> part INTRO_SEQUENCE_CMD_FADE_OUT */
#define INTRO_SEQUENCE_CMD_FADE_OUT (IntroSequenceCmd_FadeOut_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_FADE_OUT */
/* >>> part INTRO_SEQUENCE_CMD_LOAD_CHARIZARD_SCENE */
#define INTRO_SEQUENCE_CMD_LOAD_CHARIZARD_SCENE (IntroSequenceCmd_LoadCharizardScene_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_LOAD_CHARIZARD_SCENE */
/* >>> part INTRO_SEQUENCE_CMD_LOAD_SCYTHER_SCENE */
#define INTRO_SEQUENCE_CMD_LOAD_SCYTHER_SCENE (IntroSequenceCmd_LoadScytherScene_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_LOAD_SCYTHER_SCENE */
/* >>> part INTRO_SEQUENCE_CMD_LOAD_AERODACTYL_SCENE */
#define INTRO_SEQUENCE_CMD_LOAD_AERODACTYL_SCENE (IntroSequenceCmd_LoadAerodactylScene_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_LOAD_AERODACTYL_SCENE */
/* >>> part INTRO_SEQUENCE_CMD_LOAD_TITLE_SCREEN_SCENE */
#define INTRO_SEQUENCE_CMD_LOAD_TITLE_SCREEN_SCENE (IntroSequenceCmd_LoadTitleScreenScene_ADDR)
/* <<< part INTRO_SEQUENCE_CMD_LOAD_TITLE_SCREEN_SCENE */
/* --- part INTRO_SEQUENCE_LOAD_OPENING_SCENE_AND_UPDATE_SGB_BORDER */
/* >>> part INTRO_SEQUENCE_LOAD_OPENING_SCENE */
#define INTRO_SEQUENCE_LOAD_OPENING_SCENE (LoadOpeningScene_ADDR)
/* <<< part INTRO_SEQUENCE_LOAD_OPENING_SCENE */
/* >>> part INTRO_SEQUENCE_EMPTY_FUNC */
#define INTRO_SEQUENCE_EMPTY_FUNC (IntroSequenceEmptyFunc_ADDR)
/* <<< part INTRO_SEQUENCE_EMPTY_FUNC */
/* >>> factory AnimateRandomTitleScreenOrb */
/* intro_sequence_commands.asm:331-390 */
uint8_t AnimateRandomTitleScreenOrb(void)
{
	UpdateSpriteAttributes();
	uint8_t a = (uint8_t)(wTitleScreenOrbCounter & ORB_COUNTER_MASK);
	if (a != 0u)
		return a;

	do {
		uint8_t c = Random(NUM_TITLE_SCREEN_ORBS);
		wWhichSprite = gb_read8((uint16_t)(wTitleScreenSprites_ADDR + c));
		a = GetSpriteAnimCounter();
	} while (a != 0xffu);

	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_ATTRIBUTES);
	gb_write8(hl, (uint8_t)(gb_read8(hl) | (uint8_t)(1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)));
	hl++;
	gb_write8(hl, 248u);
	hl++;
	gb_write8(hl, 14u);
	return StartSpriteAnimation(SPRITE_ANIM_216);
}
/* <<< factory AnimateRandomTitleScreenOrb */
/* --- factory LoadOpeningSceneAndUpdateSGBBorder */
/* >>> factory IntroSequenceCmd_LoadCharizardScene */
IntroSequenceCmdLoadSceneResult IntroSequenceCmd_LoadCharizardScene(void)
{
	LoadOpeningScene(SCENE_CHARIZARD_INTRO, 6u, 3u);
	return (IntroSequenceCmdLoadSceneResult){0u, 0x20u, 0x7Fu, 0xFFu};
}
/* <<< factory IntroSequenceCmd_LoadCharizardScene */
/* >>> factory IntroSequenceCmd_LoadAerodactylScene */
IntroSequenceCmdLoadSceneResult IntroSequenceCmd_LoadAerodactylScene(void)
{
	LoadOpeningScene(SCENE_AERODACTYL_INTRO, 6u, 3u);
	return (IntroSequenceCmdLoadSceneResult){0u, 0x20u, 0x7Fu, 0xFFu};
}
/* <<< factory IntroSequenceCmd_LoadAerodactylScene */
/* >>> factory IntroSequenceCmd_LoadScytherScene */
IntroSequenceCmdLoadSceneResult IntroSequenceCmd_LoadScytherScene(void)
{
	LoadOpeningScene(SCENE_SCYTHER_INTRO, 6u, 3u);
	return (IntroSequenceCmdLoadSceneResult){0u, 0x20u, 0x7Fu, 0xFFu};
}
/* <<< factory IntroSequenceCmd_LoadScytherScene */
/* >>> factory ExecuteIntroSequenceCmd */
ExecuteIntroSequenceCmdResult ExecuteIntroSequenceCmd(void)
{
	uint8_t delay = wSequenceDelay;
	ExecuteIntroSequenceCmdResult result = {0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u, 0u};

	for (;;) {
		if (delay != 0u) {
			if (delay == 0xffu) {
				result.a = delay;
				result.f = 0xc0u;
				result.mask |= 0x03u;
				return result;
			}
			uint8_t next_delay = (uint8_t)(delay - 1u);
			wSequenceDelay = next_delay;
			result.a = next_delay;
			result.f = (uint8_t)(0x40u | (next_delay == 0u ? 0x80u : 0u) |
				((delay & 0x0fu) == 0u ? 0x20u : 0u) | 0x10u);
			result.mask |= 0x03u;
			return result;
		}

		BankswitchROM(7u);
		uint16_t command_ptr = (uint16_t)(wSequenceCmdPtr |
			((uint16_t)gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u)) << 8));
		uint8_t target_low = gb_read8(command_ptr);
		uint8_t target_high = gb_read8((uint16_t)(command_ptr + 1u));
		uint8_t c = gb_read8((uint16_t)(command_ptr + 2u));
		uint8_t b = gb_read8((uint16_t)(command_ptr + 3u));
		uint16_t target = (uint16_t)(target_low | ((uint16_t)target_high << 8));

		result.a = b;
		result.f = 0x80u;
		result.b = b;
		result.c = c;
		result.d = target_high;
		result.e = target_low;
		result.hl = target;
		result.mask = 0x7fu;
		result.carry = 0u;

		switch (target) {
		case INTRO_SEQUENCE_CMD_WAIT_ORBS_ANIMATION: {
			IntroSequenceCmdWaitOrbsAnimationResult r = IntroSequenceCmd_WaitOrbsAnimation();
			result.a = r.a;
			result.f = r.f;
			result.mask = 0x03u;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_WAIT: {
			IntroSequenceCmdWaitResult r = IntroSequenceCmd_Wait(c);
			result.a = r.a;
			result.f = r.f;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_SET_ORBS_ANIMATIONS: {
			IntroSequenceCmdSetOrbsAnimationsResult r = IntroSequenceCmd_SetOrbsAnimations(b, c);
			result.a = r.a;
			result.f = r.f;
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.hl = r.hl;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_SET_ORBS_COORDINATES: {
			IntroSequenceCmdSetOrbsCoordinatesResult r = IntroSequenceCmd_SetOrbsCoordinates(b, c);
			result.a = r.a;
			result.f = r.f;
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.hl = r.hl;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_PLAY_TITLE_SCREEN_MUSIC: {
			IntroSequenceCmd_PlayTitleScreenMusicResult r = IntroSequenceCmd_PlayTitleScreenMusic();
			result.a = r.a;
			result.f = r.f;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_WAIT_SFX: {
			IntroSequenceCmdWaitSFXResult r = IntroSequenceCmd_WaitSFX();
			result.a = r.a;
			result.f = r.f;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_PLAY_SFX: {
			IntroSequenceCmdPlaySFXResult r = IntroSequenceCmd_PlaySFX(c);
			result.a = r.a;
			result.f = r.f;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_FADE_IN: {
			IntroSequenceCmd_FadeInResult r = IntroSequenceCmd_FadeIn();
			result.a = r.a;
			result.f = r.f;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_FADE_OUT: {
			IntroSequenceCmd_FadeOutResult r = IntroSequenceCmd_FadeOut();
			result.a = r.a;
			result.f = r.f;
			result.mask = 0x03u;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_CMD_LOAD_CHARIZARD_SCENE: {
			IntroSequenceCmdLoadSceneResult r = IntroSequenceCmd_LoadCharizardScene();
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.mask = 0x3cu;
			result.carry = 1u;
			break;
		}
		case INTRO_SEQUENCE_CMD_LOAD_SCYTHER_SCENE: {
			IntroSequenceCmdLoadSceneResult r = IntroSequenceCmd_LoadScytherScene();
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.mask = 0x3cu;
			result.carry = 1u;
			break;
		}
		case INTRO_SEQUENCE_CMD_LOAD_AERODACTYL_SCENE: {
			IntroSequenceCmdLoadSceneResult r = IntroSequenceCmd_LoadAerodactylScene();
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.mask = 0x3cu;
			result.carry = 1u;
			break;
		}
		case INTRO_SEQUENCE_CMD_LOAD_TITLE_SCREEN_SCENE: {
			IntroSequenceCmdLoadTitleScreenSceneResult r = IntroSequenceCmd_LoadTitleScreenScene();
			result.f = r.f;
			result.mask = 0x02u;
			result.carry = (uint8_t)((r.f & 0x10u) != 0u);
			break;
		}
		case INTRO_SEQUENCE_LOAD_OPENING_SCENE:
			LoadOpeningScene(result.a, result.b, result.c);
			result.mask = 0u;
			break;
		case INTRO_SEQUENCE_EMPTY_FUNC:
			IntroSequenceEmptyFunc();
			break;
		default:
			return result;
		}

		if (result.carry == 0u)
			return result;
		delay = wSequenceDelay;
	}
}
/* <<< factory ExecuteIntroSequenceCmd */
/* === factory LoadOpeningScene */
