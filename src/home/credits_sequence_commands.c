#include "home/credits_sequence_commands.h"

#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/credits_sequence_commands.h"
#include "home/color.h"
#include "home/lcd.h"

#include "generated/wram.h"
#include "home/credits.h"
#include "home/credits_sequence_commands.h"

#include "generated/wram.h"
#include "home/process_text.h"
#include "home/print_text.h"

#define SINGLE_SPACED 0x01u

#include "home/credits_sequence_commands.h"
#include "home/tiles.h"
#include "generated/wram.h"

#include "home/credits_sequence_commands.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "home/animation.h"
#include "home/empty_screen.h"
#include "home/scenes.h"
#include "home/default_palettes.h"

#include "home/load_animation.h"
#include "home/lcd_enable_frame.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/animation.h"
#include "home/empty_screen.h"
#include "home/load_animation.h"
#include "home/default_palettes.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/animation.h"
#include "home/empty_screen.h"
#include "home/scripting.h"
#include "home/load_overworld.h"
#include "home/load_gfx.h"

#define PALETTE_OVERWORLD_OAM 0x1Du

#include "home/load_animation.h"
#include "home/npc_data.h"
#include "home/sprite_animations.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#define SPRITE_ANIM_COORD_X 0x02u
/* <<< factory statics */

#define CREDITS_SEQUENCE_ADDR 0x5AEFu

void SetCreditsSequenceCmdPtr(void)
{
	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)CREDITS_SEQUENCE_ADDR);
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u),
	          (uint8_t)(CREDITS_SEQUENCE_ADDR >> 8));
	gb_write8(wSequenceDelay_ADDR, 0);
}

void ExecuteCreditsSequenceCmd(void)
{
	uint8_t delay = gb_read8(wSequenceDelay_ADDR);
	if (delay == 0 || delay == 0xFFu)
		return;
	gb_write8(wSequenceDelay_ADDR, (uint8_t)(delay - 1u));
}

void AdvanceCreditsSequenceCmdPtr(uint8_t a)
{
	uint16_t ptr = (uint16_t)(gb_read8(wSequenceCmdPtr_ADDR) |
	                          ((uint16_t)gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u)) << 8));
	ptr = (uint16_t)(ptr + a);
	gb_write8(wSequenceCmdPtr_ADDR, (uint8_t)ptr);
	gb_write8((uint16_t)(wSequenceCmdPtr_ADDR + 1u), (uint8_t)(ptr >> 8));
}

/* >>> factory AdvanceCreditsSequenceCmdPtrBy2 */
/* credits_sequence_commands.asm:45-47 */
void AdvanceCreditsSequenceCmdPtrBy2(void)
{
	AdvanceCreditsSequenceCmdPtr(2u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy2 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy3 */
/* credits_sequence_commands.asm:49-51 */
void AdvanceCreditsSequenceCmdPtrBy3(void)
{
	AdvanceCreditsSequenceCmdPtr(3u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy3 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy5 */
/* credits_sequence_commands.asm:53-55 */
void AdvanceCreditsSequenceCmdPtrBy5(void)
{
	AdvanceCreditsSequenceCmdPtr(5u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy5 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy6 */
/* credits_sequence_commands.asm:57-59 */
void AdvanceCreditsSequenceCmdPtrBy6(void)
{
	AdvanceCreditsSequenceCmdPtr(6u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy6 */

/* >>> factory AdvanceCreditsSequenceCmdPtrBy4 */
/* credits_sequence_commands.asm:61-65 (fallthrough into AdvanceCreditsSequenceCmdPtr) */
void AdvanceCreditsSequenceCmdPtrBy4(void)
{
	AdvanceCreditsSequenceCmdPtr(4u);
}
/* <<< factory AdvanceCreditsSequenceCmdPtrBy4 */


/* >>> factory CreditsSequenceCmd_Wait */
/* credits_sequence_commands.asm:76-79. Consumes the frame count in c, stores it
 * as the sequence delay, then tail-jumps into AdvanceCreditsSequenceCmdPtrBy3.
 * Exit registers/flags belong to that callee (called as a plain C function here),
 * so no register outputs are claimed; the observable effect is the wSequenceDelay
 * store plus the callee's cmd-pointer advance. */
void CreditsSequenceCmd_Wait(uint8_t c)
{
	wSequenceDelay = c;
	AdvanceCreditsSequenceCmdPtrBy3();
}
/* <<< factory CreditsSequenceCmd_Wait */


/* >>> factory CreditsSequenceCmd_DisableLCD */
/* credits_sequence_commands.asm:298-300. Turns the LCD off, then tail-jumps into
 * AdvanceCreditsSequenceCmdPtrBy2. Exit registers/flags are the callee's, so none
 * are claimed; effects are the LCD write and the cmd-pointer advance. */
void CreditsSequenceCmd_DisableLCD(void)
{
	DisableLCD();
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory CreditsSequenceCmd_DisableLCD */

/* >>> factory CreditsSequenceCmd_TransformOverlay */
void CreditsSequenceCmd_TransformOverlay(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	uint8_t changed = 0;
	uint8_t value = wd647;
	if (value != 0xFFu && value != c) {
		changed = 1;
		value = (uint8_t)(value + (value < c ? 2u : (uint8_t)-2));
	}
	wd647 = value;
	value = wd648;
	if (value != 0xFFu && value != b) {
		changed = 1;
		value = (uint8_t)(value + (value < b ? 2u : (uint8_t)-2));
	}
	wd648 = value;
	value = wd649;
	if (value != 0xFFu && value != e) {
		changed = 1;
		value = (uint8_t)(value + (value < e ? 2u : (uint8_t)-2));
	}
	wd649 = value;
	value = wd64a;
	if (value != 0xFFu && value != d) {
		changed = 1;
		value = (uint8_t)(value + (value < d ? 2u : (uint8_t)-2));
	}
	wd64a = value;
	if (changed != 0) {
		wSequenceDelay = 1;
		return;
	}
	(void)Func_1d765();
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory CreditsSequenceCmd_TransformOverlay */

/* >>> factory CreditsSequenceCmd_FadeIn */
void CreditsSequenceCmd_FadeIn(void)
{
	DisableLCD();
	SetWindowOn();
	FadeScreenFromWhite();
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory CreditsSequenceCmd_FadeIn */

/* >>> factory CreditsSequenceCmd_PrintTextBox */
void CreditsSequenceCmd_PrintTextBox(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	wLineSeparation = SINGLE_SPACED;
	InitTextPrinting(c, b);
	(void)PrintTextNoDelay((uint16_t)(((uint16_t)d << 8) | e), c, b);
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory CreditsSequenceCmd_PrintTextBox */

/* >>> factory CreditsSequenceCmd_InitOverlay */
void CreditsSequenceCmd_InitOverlay(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	wd647 = c;
	wd648 = b;
	wd649 = e;
	wd64a = d;
	(void)Func_1d765();
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory CreditsSequenceCmd_InitOverlay */

/* >>> factory CreditsSequenceCmd_InitVolcanoSprite */
void CreditsSequenceCmd_InitVolcanoSprite(uint8_t f)
{
	OverworldMap_InitVolcanoSprite(f);
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory CreditsSequenceCmd_InitVolcanoSprite */

/* >>> factory CreditsSequenceCmd_DrawRectangle */
CreditsSequenceCmdDrawRectangleResult CreditsSequenceCmd_DrawRectangle(uint8_t b, uint8_t c)
{
	uint8_t e = (uint8_t)(c | 0x20u);
	FillRectangle(0u, 20u, b, (uint16_t)((uint16_t)0u << 8 | e), 0u);
	AdvanceCreditsSequenceCmdPtrBy4();
	uint8_t hi = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint8_t f = (uint8_t)(hi == 0u ? 0x80u : 0x00u);
	return (CreditsSequenceCmdDrawRectangleResult){hi, f};
}
/* <<< factory CreditsSequenceCmd_DrawRectangle */

/* >>> factory CreditsSequenceCmd_PrintText */
void CreditsSequenceCmd_PrintText(uint8_t b, uint8_t c, uint16_t de)
{
	wLineSeparation = SINGLE_SPACED;
	uint8_t d = c;
	uint8_t e = (uint8_t)(b | 0x20u);
	InitTextPrinting(d, e);
	(void)PrintTextNoDelay(de, d, e);
	AdvanceCreditsSequenceCmdPtrBy6();
}
/* <<< factory CreditsSequenceCmd_PrintText */

/* >>> factory CreditsSequenceCmd_LoadBooster */
void CreditsSequenceCmd_LoadBooster(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	ClearNumLoadedFramesetSubgroups();
	EmptyScreen();
	hSCX = 0;
	hSCY = 0;
	SetDefaultPalettes();
	(void)LoadBoosterGfx(e, c, b);
	AdvanceCreditsSequenceCmdPtrBy5();
}
/* <<< factory CreditsSequenceCmd_LoadBooster */

/* >>> factory CreditsSequenceCmd_FadeOut */
void CreditsSequenceCmd_FadeOut(void)
{
	FadeScreenToWhite();
	ClearSpriteAnimations();
	EnableLCD();
	DoFrameIfLCDEnabled();
	DisableLCD();
	SetWindowOff();
	AdvanceCreditsSequenceCmdPtrBy2();
}
/* <<< factory CreditsSequenceCmd_FadeOut */

/* >>> factory CreditsSequenceCmd_LoadScene */
CreditsSequenceCmdLoadSceneResult CreditsSequenceCmd_LoadScene(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	ClearNumLoadedFramesetSubgroups();
	EmptyScreen();
	hSCX = 0;
	hSCY = 0;
	SetDefaultPalettes();
	LoadSceneResult loaded = LoadScene(e, f, c, b, d, e, hl);
	uint8_t low_before = gb_read8(wSequenceCmdPtr_ADDR);
	uint8_t high_before = gb_read8((uint16_t)(wSequenceCmdPtr_ADDR + 1u));
	uint16_t low_sum = (uint16_t)low_before + 5u;
	uint8_t carry = (uint8_t)(low_sum > 0xFFu);
	uint16_t high_sum = (uint16_t)high_before + carry;
	AdvanceCreditsSequenceCmdPtrBy5();
	uint8_t high = (uint8_t)high_sum;
	uint8_t exit_f = (uint8_t)((high == 0u ? 0x80u : 0u) |
		(((uint8_t)((high_before & 0x0Fu) + carry) > 0x0Fu) ? 0x20u : 0u) |
		(high_sum > 0xFFu ? 0x10u : 0u));
	return (CreditsSequenceCmdLoadSceneResult){high, exit_f, loaded.b, loaded.c, loaded.d, loaded.e};
}
/* <<< factory CreditsSequenceCmd_LoadScene */

/* >>> factory LoadOWMapForCreditsSequence */
void LoadOWMapForCreditsSequence(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	EmptyScreen();
	hSCX = c;
	hSCY = b;
	wCurMap = e;
	LoadMapTilesAndPals();
	(void)Func_c9c7();
	SafelyCopyBGMapFromSRAMToVRAM();
	DoMapOWFrame();
	wWhichOBP = 0;
	wWhichOBPalIndex = 0;
	LoadOBPalette(PALETTE_OVERWORLD_OAM);
}
/* <<< factory LoadOWMapForCreditsSequence */

/* >>> factory CreditsSequenceCmd_LoadOWMap */
/* credits_sequence_commands.asm:294-299 */
void CreditsSequenceCmd_LoadOWMap(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	LoadOWMapForCreditsSequence(b, c, d, e);
	AdvanceCreditsSequenceCmdPtrBy5();
}
/* <<< factory CreditsSequenceCmd_LoadOWMap */

/* >>> factory LoadNPCForCreditsSequence */
void LoadNPCForCreditsSequence(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	gb_write8(wLoadNPCXPos_ADDR, c);
	gb_write8(wLoadNPCYPos_ADDR, b);
	gb_write8(wLoadNPCDirection_ADDR, e);
	LoadNPCSpriteDataResult npc = LoadNPCSpriteData(d, b, c, d, e, 0u);
	(void)CreateSpriteAndAnimBufferEntry(wNPCSpriteID, npc.f);

	uint16_t sprite_property = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	uint8_t x = (uint8_t)((uint8_t)(gb_read8(wLoadNPCXPos_ADDR) * 8u) + 8u - hSCX);
	gb_write8(sprite_property, x);
	uint8_t y = (uint8_t)((uint8_t)(gb_read8(wLoadNPCYPos_ADDR) * 8u) + 16u - hSCY);
	gb_write8((uint16_t)(sprite_property + 1u), y);

	uint8_t animation = (uint8_t)(gb_read8(wLoadNPCDirection_ADDR) + wNPCAnim);
	StartNewSpriteAnimation(animation);
}
/* <<< factory LoadNPCForCreditsSequence */
