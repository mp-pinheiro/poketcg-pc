#include "home/debug.h"

#include "generated/wram.h"
#include "home/lcd.h"
#include "home/tiles.h"
#include "home/wait_keys.h"
/* >>> factory statics */
#include "home/random.h"
#include "mem.h"

#include "generated/hram.h"
#include "home/print_text.h"
#include "home/process_text.h"

#define SINGLE_SPACED 0x01u
#define FUNC_80C64_BANK 0x20u
#define FUNC_80C64_MENU_PARAMS_ADDR 0x4cbbu
#define FUNC_80C64_WIN_LOSE_PRIZES_TEXT 0x0385u
#define FUNC_80C64_USE_DUELISTS_DECK_TEXT 0x0386u

#include "home/debug_sprites.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/booster_packs.h"
#include "home/common.h"
#include "home/lcd_enable_frame.h"
#include "home/labels.h"
#include "home/menus.h"
#include "mem.h"

#define DEBUG_CREATE_BOOSTER_BANK 0x04u
#define DEBUG_CREATE_BOOSTER_MENU_PARAMS 0x6919u
#define DEBUG_CREATE_BOOSTER_MENU_POINTERS 0x67F1u
#define DEBUG_CREATE_BOOSTER_TYPES 0x67FBu

#define BOOSTER_COLOSSEUM_NEUTRAL 0x00u
#define BOOSTER_EVOLUTION_NEUTRAL 0x07u
#define BOOSTER_MYSTERY_NEUTRAL 0x0Eu
#define BOOSTER_LABORATORY_NEUTRAL 0x14u
#define BOOSTER_ENERGY_LIGHTNING_FIRE 0x19u

#include "home/sound.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/load_animation.h"
#include "home/load_gfx.h"
#include "home/overworld.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/sprite_animations.h"
#include "mem.h"
#define CONSOLE_CGB 0x02u
#define PALETTE_DEFAULT_CGB 0x00u
#define PALETTE_OVERWORLD_OAM 0x1du
#define SPRText 0x0384u
/* <<< factory statics */

DebugSGBFrameResult DebugSGBFrame(uint8_t b, uint8_t c, uint8_t d,
	uint8_t e, uint16_t hl)
{
	uint8_t border = wDebugSGBBorder;
	DisableLCD();
	uint8_t next = (uint8_t)(border + 1u);
	uint8_t f;
	if (next >= 4u) {
		next = 0;
		f = 0x90u;
	} else {
		f = 0x10u;
	}
	wDebugSGBBorder = next;
	return (DebugSGBFrameResult){next, f, b, c, d, e, hl};
}

DebugStandardBGCharacterResult DebugStandardBGCharacter(uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl)
{
	(void)b;
	(void)c;
	(void)d;
	(void)e;
	(void)hl;
	FillRectangle(0x80u, 16u, 16u, 0, 0x0110u);
	WaitKeysResult result = WaitUntilKeysArePressed(0xFFu);
	return (DebugStandardBGCharacterResult){result.a, 0x10u, 0, 0};
}

DebugQuitResult DebugQuit(uint8_t a, uint8_t f)
{
	(void)f;
	return (DebugQuitResult){a, (uint8_t)(a == 0 ? 0x80u : 0)};
}

/* >>> factory UnreferencedFillVRAMWithRandomData */
/* engine/gfx/debug.asm:53-62. Unreferenced. Fills v0Tiles0 ($8000-$87FF,
 * 2048 bytes) with RNG output, advancing wRNG1/wRNG2/wRNGCounter as a side
 * effect. The tail folds `ld a, b / or c` into the loop test: since the loop
 * always runs exactly 0x800 times, bc == 0 and a == 0 on exit regardless of
 * the last RNG byte, which is discarded. */
UnreferencedFillVRAMWithRandomDataResult UnreferencedFillVRAMWithRandomData(void)
{
	DisableLCD();
	uint16_t hl = 0x8000u;
	uint32_t n = 0x800u;
	do {
		gb_write8(hl, UpdateRNGSources());
		hl = (uint16_t)(hl + 1u);
	} while (--n != 0u);
	return (UnreferencedFillVRAMWithRandomDataResult){0, 0x80u, 0, 0, hl};
}
/* <<< factory UnreferencedFillVRAMWithRandomData */

/* >>> factory _DebugVEffect */
/* engine/gfx/debug.asm:66. Bare ret; unconditional no-op. Pret's comment
 * notes it once inspected overworld NPC sprites, but the body left in the
 * ROM is empty. */
void _DebugVEffect(void)
{
}
/* <<< factory _DebugVEffect */

/* >>> factory Func_80c64 */
/* engine/gfx/debug.asm:3-42. Unreferenced. Loads the opponent's name, the
 * duel prize count and the NPC's deck id into the shared print-text buffer,
 * prints the "you win/lose N prizes with duelist X" and "duelist uses deck
 * Y" labels for the abandoned prize/deck confirmation screen with a
 * temporary single-line spacing (restored before returning), then re-arms
 * the standard two-item cursor menu from its own local parameter table
 * (debug.asm:44-50, 8 bytes right after this routine in the same ROM bank).
 * That table is read via rom_ptr(bank $20, ...) rather than the bus: the
 * routine itself never bankswitches, relying on bank $20 already being
 * mapped in by whatever farcalled it -- the probe harness instead resets
 * the ROM bank to 1 before every call, so a bus read here would pull the
 * wrong bank's bytes. */
void Func_80c64(void)
{
	uint8_t saved_line_sep = wLineSeparation;
	wLineSeparation = SINGLE_SPACED;

	wTxRam2 = wOpponentName;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(wOpponentName_ADDR + 1u)));
	wTxRam3_b = wNPCDuelistCopy;
	gb_write8((uint16_t)(wTxRam3_b_ADDR + 1u), 0);

	wTxRam3 = wNPCDuelPrizes;
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0);
	InitTextPrinting(2u, 13u);
	(void)PrintTextNoDelay(FUNC_80C64_WIN_LOSE_PRIZES_TEXT, 2u, 13u);

	wTxRam3 = wNPCDuelDeckID;
	gb_write8((uint16_t)(wTxRam3_ADDR + 1u), 0);
	InitTextPrinting(2u, 15u);
	(void)PrintTextNoDelay(FUNC_80C64_USE_DUELISTS_DECK_TEXT, 2u, 15u);

	wLineSeparation = saved_line_sep;

	wCurMenuItem = 0;
	hCurMenuItem = 0;
	const uint8_t *params = rom_ptr(FUNC_80C64_BANK, FUNC_80C64_MENU_PARAMS_ADDR);
	for (uint8_t i = 0; i < 8u; i++)
		gb_write8((uint16_t)(wMenuCursorXOffset_ADDR + i), params[i]);
	wCursorBlinkCounter = 0;
}
/* <<< factory Func_80c64 */

/* >>> factory DebugVEffect */
/* engine/menus/debug.asm:6-9. Calls the no-op VEffect debug hook
 * (_DebugVEffect, engine/gfx/debug.asm:66, already ported and preserves
 * every register) via farcall, then unconditionally sets carry: scf
 * clears N/H, leaves Z untouched, so a,b,c,d,e,hl pass through
 * unchanged and only f's low nibble changes. */
DebugVEffectResult DebugVEffect(uint8_t a, uint8_t f, uint8_t b,
	uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	_DebugVEffect();
	f = (uint8_t)((f & 0x80u) | 0x10u);
	return (DebugVEffectResult){a, f, b, c, d, e, hl};
}
/* <<< factory DebugVEffect */

/* >>> factory DebugCGBTest */
/* engine/menus/debug.asm:73-76. Calls the no-op CGB-test debug hook
 * (Func_1c865, engine/menus/debug_sprites.asm, already ported and
 * preserves every register) via farcall, then unconditionally sets
 * carry: scf clears N/H, leaves Z untouched, so a,b,c,d,e,hl pass
 * through unchanged and only f's low nibble changes. */
DebugCGBTestResult DebugCGBTest(uint8_t a, uint8_t f, uint8_t b,
	uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	Func_1c865();
	f = (uint8_t)((f & 0x80u) | 0x10u);
	return (DebugCGBTestResult){a, f, b, c, d, e, hl};
}
/* <<< factory DebugCGBTest */

/* >>> factory DebugCreateBoosterPack */
void DebugCreateBoosterPack(void)
{
	uint8_t selected = wDebugBoosterSelection;
	for (;;) {
		InitAndPrintMenu(DEBUG_CREATE_BOOSTER_MENU_PARAMS, selected);

		HandleMenuInputResult first;
		do {
			DoFrameIfLCDEnabled();
			first = HandleMenuInput();
		} while ((first.f & 0x10u) == 0u);

		uint8_t item = hCurMenuItem;
		if (item != first.e)
			return;

		wDebugBoosterSelection = item;
		const uint8_t *menu_entry = rom_ptr(DEBUG_CREATE_BOOSTER_BANK,
			(uint16_t)(DEBUG_CREATE_BOOSTER_MENU_POINTERS +
			(uint16_t)item * 2u));
		uint16_t menu = (uint16_t)(menu_entry[0] |
			(uint16_t)menu_entry[1] << 8);
		InitAndPrintMenu(menu, 0u);

		HandleMenuInputResult second;
		do {
			DoFrameIfLCDEnabled();
			second = HandleMenuInput();
		} while ((second.f & 0x10u) == 0u);

		item = hCurMenuItem;
		if (item != second.e) {
			selected = wDebugBoosterSelection;
			continue;
		}

		const uint8_t *type_entry = rom_ptr(DEBUG_CREATE_BOOSTER_BANK,
			(uint16_t)(DEBUG_CREATE_BOOSTER_TYPES + wDebugBoosterSelection));
		uint8_t booster = (uint8_t)(type_entry[0] + second.e);
		GenerateBoosterPack(booster);
		OpenBoosterPack();
		return;
	}
}
/* <<< factory DebugCreateBoosterPack */

/* >>> factory DebugCredits */
void DebugCredits(void)
{
}
/* <<< factory DebugCredits */

/* >>> factory _DebugLookAtSprite */
void _DebugLookAtSprite(void)
{
	static const uint8_t npc_data[44][3] = {
		{0x00u, 0x00u, 0x1eu}, {0xffu, 0x00u, 0x00u},
		{0x01u, 0x04u, 0x0eu}, {0xffu, 0x00u, 0x00u},
		{0x02u, 0x00u, 0x26u}, {0x03u, 0x04u, 0x22u},
		{0x04u, 0x00u, 0x0eu}, {0x05u, 0x00u, 0x1au},
		{0x06u, 0x00u, 0x0eu}, {0x07u, 0x04u, 0x1eu},
		{0x08u, 0x04u, 0x0eu}, {0x09u, 0x00u, 0x16u},
		{0x0au, 0x00u, 0x0eu}, {0x0bu, 0x04u, 0x22u},
		{0x0cu, 0x00u, 0x12u}, {0x0du, 0x00u, 0x12u},
		{0xffu, 0x00u, 0x00u}, {0x0eu, 0x00u, 0x2au},
		{0xffu, 0x00u, 0x00u}, {0x0fu, 0x00u, 0x26u},
		{0xffu, 0x00u, 0x00u}, {0x10u, 0x00u, 0x0eu},
		{0xffu, 0x00u, 0x00u}, {0x11u, 0x04u, 0x16u},
		{0x12u, 0x04u, 0x1au}, {0x13u, 0x00u, 0x22u},
		{0x14u, 0x00u, 0x16u}, {0x15u, 0x00u, 0x26u},
		{0x16u, 0x00u, 0x26u}, {0x17u, 0x04u, 0x1eu},
		{0x18u, 0x00u, 0x0eu}, {0x19u, 0x00u, 0x1au},
		{0x1au, 0x00u, 0x16u}, {0x1bu, 0x00u, 0x22u},
		{0x1cu, 0x04u, 0x0eu}, {0x1du, 0x04u, 0x22u},
		{0x1eu, 0x00u, 0x1eu}, {0x1fu, 0x04u, 0x1au},
		{0x20u, 0x00u, 0x16u}, {0x21u, 0x0au, 0x30u},
		{0x22u, 0x00u, 0x16u}, {0x23u, 0x04u, 0x1eu},
		{0x24u, 0x00u, 0x16u}, {0x08u, 0x08u, 0x2eu}
	};

	DisableLCD();
	EmptyScreen();
	ClearSpriteAnimations();
	wWhichOBP = 0;
	wWhichBGPalIndex = 0;
	LoadBGPalette(PALETTE_DEFAULT_CGB);
	wWhichOBP = 0;
	wWhichOBPalIndex = 0;
	LoadOBPalette(PALETTE_OVERWORLD_OAM);
	wLoadNPCDirection = 0x02u;
	wLoadedNPCTempIndex = 0x01u;
	{
		uint8_t index = wLoadedNPCTempIndex;
		const uint8_t *data = npc_data[index - 1u];
		if (data[0] != 0xffu) {
			(void)CreateSpriteAndAnimBufferEntry(data[0], 0);
			uint8_t animation = (uint8_t)(data[wConsole == CONSOLE_CGB ? 2u : 1u] + wLoadNPCDirection);
			StartNewSpriteAnimation(animation);
			uint16_t property = GetSpriteAnimBufferProperty(0x02u);
			gb_write8(property, 0x48u);
			gb_write8((uint16_t)(property + 1u), 0x40u);
		}
	}
	{
		ProcessTextHeaderResult text;
		InitTextPrinting(0, 4);
		text = ProcessTextFromID(SPRText);
		WriteOneByteNumberInTxSymbol_PadSpace(wLoadedNPCTempIndex, 0, 0, text.d, text.e, text.hl);
	}
	EnableLCD();
	for (;;) {
		DoFrameIfLCDEnabled();
		{
			uint8_t keys = hKeysPressed;
			if ((keys & 0x01u) != 0) {
				wLoadNPCDirection = (uint8_t)((wLoadNPCDirection + 1u) & 0x03u);
				ClearSpriteAnimations();
				{
					uint8_t index = wLoadedNPCTempIndex;
					const uint8_t *data = npc_data[index - 1u];
					if (data[0] != 0xffu) {
						(void)CreateSpriteAndAnimBufferEntry(data[0], 0);
						uint8_t animation = (uint8_t)(data[wConsole == CONSOLE_CGB ? 2u : 1u] + wLoadNPCDirection);
						StartNewSpriteAnimation(animation);
						uint16_t property = GetSpriteAnimBufferProperty(0x02u);
						gb_write8(property, 0x48u);
						gb_write8((uint16_t)(property + 1u), 0x40u);
					}
				}
			}
			if ((keys & 0xf0u) != 0) {
				GetDirectionFromDPadResult direction = GetDirectionFromDPad((uint8_t)(keys & 0xf0u));
				uint8_t index = wLoadedNPCTempIndex;
				uint8_t step = 0;
				uint8_t increase = 0;
				switch (direction.a) {
				case 0: step = 10; break;
				case 1: step = 1; increase = 1; break;
				case 2: step = 10; increase = 1; break;
				case 3: step = 1; break;
				default: step = 0; break;
				}
				if (step != 0) {
					if (increase != 0) {
						uint8_t next = (uint8_t)(index + step);
						index = (index == 0x2cu || next < index || next >= 0x2cu) ? 0x01u : next;
					} else {
						index = (index == 0x01u || index < step || (uint8_t)(index - step) < 0x01u) ? 0x2cu : (uint8_t)(index - step);
					}
					wLoadedNPCTempIndex = index;
					ClearSpriteAnimations();
					{
						const uint8_t *data = npc_data[index - 1u];
						if (data[0] != 0xffu) {
							(void)CreateSpriteAndAnimBufferEntry(data[0], 0);
							uint8_t animation = (uint8_t)(data[wConsole == CONSOLE_CGB ? 2u : 1u] + wLoadNPCDirection);
							StartNewSpriteAnimation(animation);
							uint16_t property = GetSpriteAnimBufferProperty(0x02u);
							gb_write8(property, 0x48u);
							gb_write8((uint16_t)(property + 1u), 0x40u);
						}
					}
					{
						ProcessTextHeaderResult text;
						InitTextPrinting(0, 4);
						text = ProcessTextFromID(SPRText);
						WriteOneByteNumberInTxSymbol_PadSpace(wLoadedNPCTempIndex, 0, 0, text.d, text.e, text.hl);
					}
				}
			}
		}
		HandleAllSpriteAnimations();
		if ((hKeysPressed & 0x04u) != 0)
			return;
	}
}
/* <<< factory _DebugLookAtSprite */
