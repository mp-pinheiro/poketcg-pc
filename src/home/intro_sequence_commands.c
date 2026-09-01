#include "home/intro_sequence_commands.h"

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

/* >>> factory statics */
#include "home/load_animation.h"
#include "home/random.h"
#include "home/sprite_animations.h"

#define CONSOLE_CGB                     0x02u
#define SPRITE_ANIM_215                 0xd7u
#define SPRITE_ANIM_216                 0xd8u
#define SPRITE_ANIM_ATTRIBUTES          0x01u
#define SPRITE_ANIM_COORD_X             0x02u
#define SPRITE_ANIM_FLAG_UNSKIPPABLE_F  0x07u
#define ORB_COUNTER_MASK                0x3fu
#define NUM_TITLE_SCREEN_ORBS           0x07u

/* intro_sequence_commands.asm:392-408 (.UpdateSpriteAttributes) */
static void UpdateSpriteAttributes(void)
{
	uint16_t de = wTitleScreenSprites_ADDR;
	for (uint8_t c = NUM_TITLE_SCREEN_ORBS; c != 0u; c--) {
		wWhichSprite = gb_read8(de);
		uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
		uint8_t x = gb_read8(hl);
		hl--;
		if (x == 152u)
			gb_write8(hl, (uint8_t)(gb_read8(hl) & (uint8_t)~(1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)));
		de = (uint16_t)(de + 1u);
	}
}

#include "generated/wram.h"
#include "mem.h"

#include "mem.h"

#include "home/intro_sequence_commands.h"
#include "generated/wram.h"

#include "home/intro_sequence_commands.h"
#include "home/sound.h"
#include "generated/wram.h"

#include "home/intro_sequence_commands.h"
#include "home/sprite_animations.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/intro_sequence_commands.h"
#include "home/sound.h"
#include "generated/wram.h"
#include "mem.h"
#define MUSIC_TITLESCREEN 0x01u

#include "home/intro_sequence_commands.h"
#include "home/color.h"
#include "generated/wram.h"
#include "mem.h"
#define TRUE 0x01u

#include "generated/wram.h"
#include "home/intro_sequence_commands.h"
#include "mem.h"

#include "home/sound.h"
#include "generated/wram.h"

#include "home/intro_sequence_commands.h"
#include "home/lcd.h"
#include "home/color.h"
#include "home/scenes.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/intro_sequence_commands.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/intro_sequence_commands.h"
#define SCENE_CHARIZARD_INTRO 0x05u

#define SCENE_TITLE_SCREEN 0x00u

#define SCENE_AERODACTYL_INTRO 0x07u

#include "home/intro_sequence_commands.h"
#define SCENE_SCYTHER_INTRO 0x06u

#include "home/intro_sequence_commands.h"
#include "generated/wram.h"
#define INTRO_SEQUENCE_CMD_WAIT_ORBS_ANIMATION 0x5444u
#define INTRO_SEQUENCE_CMD_WAIT 0x5460u
#define INTRO_SEQUENCE_CMD_SET_ORBS_ANIMATIONS 0x5469u
#define INTRO_SEQUENCE_CMD_SET_ORBS_COORDINATES 0x5486u
#define INTRO_SEQUENCE_CMD_PLAY_TITLE_SCREEN_MUSIC 0x5519u
#define INTRO_SEQUENCE_CMD_WAIT_SFX 0x5523u
#define INTRO_SEQUENCE_CMD_PLAY_SFX 0x5530u
#define INTRO_SEQUENCE_CMD_FADE_IN 0x5539u
#define INTRO_SEQUENCE_CMD_FADE_OUT 0x5543u
#define INTRO_SEQUENCE_CMD_LOAD_CHARIZARD_SCENE 0x5551u
#define INTRO_SEQUENCE_CMD_LOAD_SCYTHER_SCENE 0x5558u
#define INTRO_SEQUENCE_CMD_LOAD_AERODACTYL_SCENE 0x555fu
#define INTRO_SEQUENCE_CMD_LOAD_TITLE_SCREEN_SCENE 0x5575u
#define INTRO_SEQUENCE_LOAD_OPENING_SCENE_AND_UPDATE_SGB_BORDER 0x5564u
#define INTRO_SEQUENCE_LOAD_OPENING_SCENE 0x5582u
#define INTRO_SEQUENCE_EMPTY_FUNC 0x559cu
#define HANDLE_ALL_SPRITE_ANIMATIONS 0x3CB4u
#define SPRITE_ANIM_190 0xBEu
#define SPRITE_ANIM_191 0xBFu
#define SPRITE_PRESS_START 0x6Au
#define INTRO_SEQUENCE 0x559Du
#define PAD_A 0x01u
#define PAD_START 0x08u

/* <<< factory statics */

/* >>> factory AnimateRandomTitleScreenOrb */
/* intro_sequence_commands.asm:331-390 */
uint8_t AnimateRandomTitleScreenOrb(void)
{
	if (wConsole == CONSOLE_CGB)
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
	if (wConsole == CONSOLE_CGB)
		gb_write8(hl, (uint8_t)(gb_read8(hl) | (uint8_t)(1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)));
	hl++;
	gb_write8(hl, 248u);
	hl++;
	gb_write8(hl, 14u);
	a = (wConsole == CONSOLE_CGB) ? SPRITE_ANIM_216 : SPRITE_ANIM_215;
	StartSpriteAnimation(a);
	return a;
}
/* <<< factory AnimateRandomTitleScreenOrb */

/* >>> factory AdvanceIntroSequenceCmdPtr */
AdvanceIntroSequenceCmdPtrResult AdvanceIntroSequenceCmdPtr(uint8_t a)
{
	uint8_t low = gb_read8(wSequenceCmdPtr_ADDR);
	uint16_t low_sum = (uint16_t)a + (uint16_t)low;
	uint8_t carry = (uint8_t)(low_sum > 0xFFu);
	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)low_sum);
	uint8_t high_before = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint16_t high_sum = (uint16_t)high_before + (uint16_t)carry;
	uint8_t high = (uint8_t)high_sum;
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u), high);
	uint8_t f = (uint8_t)((high == 0u ? 0x80u : 0u) |
		((uint8_t)((high_before & 0x0Fu) + carry) > 0x0Fu ? 0x20u : 0u) |
		(high_sum > 0xFFu ? 0x10u : 0u));
	return (AdvanceIntroSequenceCmdPtrResult){high, f};
}
/* <<< factory AdvanceIntroSequenceCmdPtr */

/* >>> factory AdvanceIntroSequenceCmdPtrBy2 */
void AdvanceIntroSequenceCmdPtrBy2(void)
{
	AdvanceIntroSequenceCmdPtr(2u);
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy2 */

/* >>> factory AdvanceIntroSequenceCmdPtrBy4 */
void AdvanceIntroSequenceCmdPtrBy4(void)
{
	AdvanceIntroSequenceCmdPtr(4u);
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy4 */

/* >>> factory IntroSequenceEmptyFunc */
void IntroSequenceEmptyFunc(void)
{
	(void)0;
}
/* <<< factory IntroSequenceEmptyFunc */

/* >>> factory IntroSequenceCmd_FadeIn */
IntroSequenceCmd_FadeInResult IntroSequenceCmd_FadeIn(void)
{
	gb_write8(wIntroSequencePalsNeedUpdate_ADDR, 0x01u);
	AdvanceIntroSequenceCmdPtrBy2();
	uint8_t hi = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint8_t f = (uint8_t)((hi == 0u ? 0x80u : 0x00u) | 0x10u);
	return (IntroSequenceCmd_FadeInResult){hi, f};
}
/* <<< factory IntroSequenceCmd_FadeIn */

/* >>> factory IntroSequenceCmd_WaitSFX */
IntroSequenceCmdWaitSFXResult IntroSequenceCmd_WaitSFX(void)
{
	uint8_t a = AssertSFXFinished();
	if (a == 0u) {
		AdvanceIntroSequenceCmdPtrBy2();
		uint8_t hi = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
		uint8_t f = (uint8_t)((hi == 0u ? 0x80u : 0x00u) | 0x10u);
		return (IntroSequenceCmdWaitSFXResult){hi, f};
	}
	uint8_t f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
	return (IntroSequenceCmdWaitSFXResult){a, f};
}
/* <<< factory IntroSequenceCmd_WaitSFX */

/* >>> factory IntroSequenceCmd_WaitOrbsAnimation */
IntroSequenceCmdWaitOrbsAnimationResult IntroSequenceCmd_WaitOrbsAnimation(void)
{
	uint16_t de = wTitleScreenSprites_ADDR;
	uint8_t c = 7u;
	uint8_t counter;
	for (;;) {
		uint8_t a = gb_read8(de);
		wWhichSprite = a;
		counter = GetSpriteAnimCounter();
		if (counter != 0xFFu) {
			uint8_t z = (counter == 0u) ? 0x80u : 0x00u;
			return (IntroSequenceCmdWaitOrbsAnimationResult){counter, z};
		}
		de = (uint16_t)(de + 1u);
		c = (uint8_t)(c - 1u);
		if (c != 0u)
			continue;
		break;
	}
	AdvanceIntroSequenceCmdPtrBy2();
	uint8_t exit_a = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	return (IntroSequenceCmdWaitOrbsAnimationResult){exit_a, 0x90u};
}
/* <<< factory IntroSequenceCmd_WaitOrbsAnimation */

/* >>> factory IntroSequenceCmd_SetOrbsAnimations */
IntroSequenceCmdSetOrbsAnimationsResult IntroSequenceCmd_SetOrbsAnimations(uint8_t b, uint8_t c)
{
	uint16_t hl = (uint16_t)(((uint16_t)b << 8) | c);
	uint16_t de = wTitleScreenSprites_ADDR;
	for (uint8_t i = 0; i < 7u; i++) {
		uint8_t sprite = gb_read8(de);
		wWhichSprite = sprite;
		uint8_t anim = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		StartSpriteAnimation(anim);
		de = (uint16_t)(de + 1u);
	}
	AdvanceIntroSequenceCmdPtrBy4();
	uint8_t high_byte = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint8_t z = (high_byte == 0u) ? 0x80u : 0x00u;
	uint8_t f = (uint8_t)(z | 0x10u);
	return (IntroSequenceCmdSetOrbsAnimationsResult){high_byte, f, b, 0u, (uint8_t)(de >> 8), (uint8_t)(de & 0xFFu), hl};
}
/* <<< factory IntroSequenceCmd_SetOrbsAnimations */

/* >>> factory IntroSequenceCmd_SetOrbsCoordinates */
IntroSequenceCmdSetOrbsCoordinatesResult IntroSequenceCmd_SetOrbsCoordinates(uint8_t b, uint8_t c)
{
	uint16_t hl = (uint16_t)(((uint16_t)b << 8) | c);
	uint16_t de = wTitleScreenSprites_ADDR;
	for (uint8_t i = 0; i < 7u; i++) {
		uint8_t sprite = gb_read8(de);
		wWhichSprite = sprite;
		uint16_t prop_addr = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
		uint8_t x = (uint8_t)(gb_read8(hl) + 8u);
		hl = (uint16_t)(hl + 1u);
		gb_write8(prop_addr, x);
		uint8_t y = (uint8_t)(gb_read8(hl) + 16u);
		hl = (uint16_t)(hl + 1u);
		gb_write8((uint16_t)(prop_addr + 1u), y);
		de = (uint16_t)(de + 1u);
	}
	AdvanceIntroSequenceCmdPtrBy4();
	uint8_t high_byte = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint8_t z = (high_byte == 0u) ? 0x80u : 0x00u;
	uint8_t f = (uint8_t)(z | 0x10u);
	return (IntroSequenceCmdSetOrbsCoordinatesResult){high_byte, f, b, 0u, (uint8_t)(de >> 8), (uint8_t)(de & 0xFFu), hl};
}
/* <<< factory IntroSequenceCmd_SetOrbsCoordinates */

/* >>> factory IntroSequenceCmd_PlayTitleScreenMusic */
IntroSequenceCmd_PlayTitleScreenMusicResult IntroSequenceCmd_PlayTitleScreenMusic(void)
{
	PlaySong(MUSIC_TITLESCREEN);
	AdvanceIntroSequenceCmdPtrBy2();
	uint8_t ptr_hi = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint8_t exit_f = (uint8_t)((ptr_hi == 0u ? 0x80u : 0x00u) | 0x10u);
	return (IntroSequenceCmd_PlayTitleScreenMusicResult){ptr_hi, exit_f};
}
/* <<< factory IntroSequenceCmd_PlayTitleScreenMusic */

/* >>> factory IntroSequenceCmd_FadeOut */
IntroSequenceCmd_FadeOutResult IntroSequenceCmd_FadeOut(void)
{
	Func_10d50();
	wIntroSequencePalsNeedUpdate = TRUE;
	AdvanceIntroSequenceCmdPtrBy2();
	uint8_t ptr_hi = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint8_t exit_f = (uint8_t)((ptr_hi == 0u ? 0x80u : 0x00u) | 0x10u);
	return (IntroSequenceCmd_FadeOutResult){ptr_hi, exit_f};
}
/* <<< factory IntroSequenceCmd_FadeOut */

/* >>> factory AdvanceIntroSequenceCmdPtrBy3 */
void AdvanceIntroSequenceCmdPtrBy3(void)
{
	AdvanceIntroSequenceCmdPtr(3u);
}
/* <<< factory AdvanceIntroSequenceCmdPtrBy3 */

/* >>> factory IntroSequenceCmd_Wait */
IntroSequenceCmdWaitResult IntroSequenceCmd_Wait(uint8_t c)
{
	gb_write8(wSequenceDelay_ADDR, c);
	AdvanceIntroSequenceCmdPtrResult adv = AdvanceIntroSequenceCmdPtr(3u);
	uint8_t f = (uint8_t)((adv.f & 0x80u) | 0x10u);
	return (IntroSequenceCmdWaitResult){adv.a, f};
}
/* <<< factory IntroSequenceCmd_Wait */

/* >>> factory IntroSequenceCmd_PlaySFX */
IntroSequenceCmdPlaySFXResult IntroSequenceCmd_PlaySFX(uint8_t c)
{
	PlaySFX(c);
	AdvanceIntroSequenceCmdPtrBy3();
	uint8_t a = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint8_t f = (uint8_t)((a == 0u ? 0x80u : 0u) | 0x10u);
	return (IntroSequenceCmdPlaySFXResult){a, f};
}
/* <<< factory IntroSequenceCmd_PlaySFX */

/* >>> factory LoadOpeningScene */
void LoadOpeningScene(uint8_t a, uint8_t b, uint8_t c)
{
	DisableLCD();
	_LoadScene(a, b, c);
	Func_10d17();
	gb_write8(wIntroSequencePalsNeedUpdate_ADDR, 0u);
	AdvanceIntroSequenceCmdPtrBy2();
	EnableLCD();
}
/* <<< factory LoadOpeningScene */

/* >>> factory LoadOpeningSceneAndUpdateSGBBorder */
LoadOpeningSceneAndUpdateSGBBorderResult LoadOpeningSceneAndUpdateSGBBorder(uint8_t a, uint8_t b, uint8_t c)
{
	LoadOpeningScene(a, b, c);
	if (gb_read8(wConsole_ADDR) == 1u) {
		gb_write8(wTempSGBPacket_ADDR, 0x21u);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 1u), 1u);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 2u), 1u);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 3u), 0x0Au);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 4u), 0u);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 5u), 0u);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 6u), 19u);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 7u), 17u);
	}
	return (LoadOpeningSceneAndUpdateSGBBorderResult){0u, 0u, 20u, 18u};
}
/* <<< factory LoadOpeningSceneAndUpdateSGBBorder */

/* >>> factory IntroSequenceCmd_LoadCharizardScene */
LoadOpeningSceneAndUpdateSGBBorderResult IntroSequenceCmd_LoadCharizardScene(void)
{
	return LoadOpeningSceneAndUpdateSGBBorder(SCENE_CHARIZARD_INTRO, 6u, 3u);
}
/* <<< factory IntroSequenceCmd_LoadCharizardScene */

/* >>> factory IntroSequenceCmd_LoadTitleScreenScene */
IntroSequenceCmdLoadTitleScreenSceneResult IntroSequenceCmd_LoadTitleScreenScene(void)
{
	LoadOpeningScene(SCENE_TITLE_SCREEN, 0u, 0u);
	IntroSequenceEmptyFunc();
	return (IntroSequenceCmdLoadTitleScreenSceneResult){0x10u};
}
/* <<< factory IntroSequenceCmd_LoadTitleScreenScene */

/* >>> factory IntroSequenceCmd_LoadAerodactylScene */
LoadOpeningSceneAndUpdateSGBBorderResult IntroSequenceCmd_LoadAerodactylScene(void)
{
	return LoadOpeningSceneAndUpdateSGBBorder(SCENE_AERODACTYL_INTRO, 6u, 3u);
}
/* <<< factory IntroSequenceCmd_LoadAerodactylScene */

/* >>> factory IntroSequenceCmd_LoadScytherScene */
LoadOpeningSceneAndUpdateSGBBorderResult IntroSequenceCmd_LoadScytherScene(void)
{
	return LoadOpeningSceneAndUpdateSGBBorder(SCENE_SCYTHER_INTRO, 6u, 3u);
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
			LoadOpeningSceneAndUpdateSGBBorderResult r = IntroSequenceCmd_LoadCharizardScene();
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.mask = 0x3cu;
			result.carry = 1u;
			break;
		}
		case INTRO_SEQUENCE_CMD_LOAD_SCYTHER_SCENE: {
			LoadOpeningSceneAndUpdateSGBBorderResult r = IntroSequenceCmd_LoadScytherScene();
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.mask = 0x3cu;
			result.carry = 1u;
			break;
		}
		case INTRO_SEQUENCE_CMD_LOAD_AERODACTYL_SCENE: {
			LoadOpeningSceneAndUpdateSGBBorderResult r = IntroSequenceCmd_LoadAerodactylScene();
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
		case INTRO_SEQUENCE_LOAD_OPENING_SCENE_AND_UPDATE_SGB_BORDER: {
			LoadOpeningSceneAndUpdateSGBBorderResult r = LoadOpeningSceneAndUpdateSGBBorder(result.a, result.b, result.c);
			result.b = r.b;
			result.c = r.c;
			result.d = r.d;
			result.e = r.e;
			result.mask = 0x3cu;
			result.carry = 1u;
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

