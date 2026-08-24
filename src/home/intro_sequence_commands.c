#include "home/intro_sequence_commands.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
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
