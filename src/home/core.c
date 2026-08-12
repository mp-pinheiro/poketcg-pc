#include "home/core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0x1Au
#define DUELVARS_ARENA_CARD_HP                  0x08u
#define MENU_CANCEL 0xFFu
#define PAD_A     0x01u
#define PAD_B     0x02u
#define PAD_START 0x08u
#define B_PAD_B_BIT 0x02u

#define ASLEEP           0x02u
#define CNF_SLP_PRZ       0x0Fu
#define PARALYZED        0x03u
#define DUELVARS_ARENA_CARD_STATUS 0x02u
#define TX_UnableDueToParalysisText 0x0000u
#define TX_UnableDueToSleepText     0x0001u

#define FLAG_Z 0x80u
#define FLAG_C 0x10u

#include "generated/wram.h"
#include "home/card_data.h"

#define TILE_SIZE 0x10u
#define PAL_SIZE 8u
#define ATTR_BLK_CTRL_INSIDE 1u
#define ATTR_BLK_CTRL_LINE 2u

#define LOAD_LOADED1_CARD_GFX_B 0x30u

#include "home/copy.h"
#include "home/switch_sram.h"

#define SAVE_DUEL_HEADER_SIZE 4u
#define SAVE_DUEL_CHECKSUM_SEED 0x2345u
#define RNGVARS_SIZE 10u
#define TRUE 1u

typedef struct {
	uint16_t addr;
	uint16_t size;
} DuelSaveEntry;

static const DuelSaveEntry kDuelDataToSave[] = {
	{ wPlayerDuelVariables_ADDR, (uint16_t)(wOpponentDuelVariables_ADDR - wPlayerDuelVariables_ADDR) },
	{ wOpponentDuelVariables_ADDR, (uint16_t)(wPlayerDeck_ADDR - wOpponentDuelVariables_ADDR) },
	{ wPlayerDeck_ADDR, (uint16_t)(wDuelTempList_ADDR - wPlayerDeck_ADDR) },
	{ wDuelStates_ADDR, (uint16_t)(wDuelStatesEnd_ADDR - wDuelStates_ADDR) },
	{ hWhoseTurn_ADDR, 1u },
	{ wRNGVars_ADDR, RNGVARS_SIZE },
	{ wAIDuelVars_ADDR, (uint16_t)(wAIDuelVarsEnd_ADDR - wAIDuelVars_ADDR) },
	{ 0u, 0u },
};

static uint32_t duel_save_total_size(void)
{
	uint32_t total = 0;
	for (int i = 0; kDuelDataToSave[i].addr != 0u; i++)
		total += kDuelDataToSave[i].size;
	return total;
}

#include "home/bg_map.h"

#define CONSOLE_DMG 0x00u
#define CONSOLE_SGB 0x01u
#define ATTR_BLK 0x04u

#include "home/objects.h"

#define CARDPAGE_TRAINER_1 0x0du
#define CARDPAGE_TRAINER_2 0x0eu

#include "generated/hram.h"
#include "generated/sram.h"
#include "home/random.h"

#define DECK_SIZE 60u
#define SAVE_DUEL_DATA_SIZE 0x0400u

#define DECK_SIZE_ 60u
#define SAVE_DUEL_DATA_SIZE_MINUS6 (0x100u - 6u)

#include "home/print_text.h"
#include "home/process_text.h"

#define DrMasonText 0x01a3u
#define PlayersTurnPracticeDuelText 0x01dbu
#define ReplaceDueToKnockoutPracticeDuelText 0x01dcu
/* <<< factory statics */

/* >>> factory SetLineSeparation */
/* core.asm:4772-4774 */
void SetLineSeparation(uint8_t a)
{
	wLineSeparation = a;
}
/* <<< factory SetLineSeparation */

/* >>> factory PlayAreaScreenMenuFunction */
/* core.asm:5040-5054 */
uint8_t PlayAreaScreenMenuFunction(void)
{
	uint8_t keys = (uint8_t)(hKeysPressed & (PAD_A | PAD_B | PAD_START));
	if (keys == 0u)
		return 0xA0u;
	if (keys & PAD_B) {
		hCurMenuItem = MENU_CANCEL;
		return 0x10u;
	}
	return 0x90u;
}
/* <<< factory PlayAreaScreenMenuFunction */

/* >>> factory SwitchAttackPage */
/* core.asm:1165-1170 */
void SwitchAttackPage(void)
{
	uint8_t v = wAttackPageNumber ^ 0x01u;
	wAttackPageNumber = v;
}
/* <<< factory SwitchAttackPage */

/* >>> factory CopyCGBCardPalette */
/* core.asm:3982-3997 */
void CopyCGBCardPalette(uint8_t a)
{
	uint16_t hl = (uint16_t)(wBackgroundPalettesCGB_ADDR + (uint16_t)(a * PAL_SIZE));
	uint16_t de = wCardPalette_ADDR;
	uint8_t b = PAL_SIZE;

	do {
		uint8_t v = gb_read8(de++);
		gb_write8(hl++, v);
	} while (--b);
}
/* <<< factory CopyCGBCardPalette */

/* >>> factory CreateCardAttrBlkPacket_DataSet */
/* core.asm:4100-4113 */
uint16_t CreateCardAttrBlkPacket_DataSet(uint16_t hl, uint8_t a, uint8_t d, uint8_t e)
{
	gb_write8(hl++, ATTR_BLK_CTRL_INSIDE + ATTR_BLK_CTRL_LINE);
	gb_write8(hl++, a);
	gb_write8(hl++, d);
	gb_write8(hl++, e);
	gb_write8(hl++, (uint8_t)(d + 7u));
	gb_write8(hl++, (uint8_t)(e + 5u));
	return hl;
}
/* <<< factory CreateCardAttrBlkPacket_DataSet */

/* >>> factory SaveDuelDataToDE */
/* core.asm:6001-6046 */
void SaveDuelDataToDE(uint16_t de)
{
	EnableSRAM();
	uint16_t base = de;
	uint16_t data_start = (uint16_t)(base + SAVE_DUEL_HEADER_SIZE);
	uint16_t cursor = data_start;
	for (int i = 0; kDuelDataToSave[i].addr != 0u; i++) {
		uint16_t hl = kDuelDataToSave[i].addr;
		CopyDataHLtoDE(&hl, &cursor, kDuelDataToSave[i].size);
	}
	uint16_t hl = data_start;
	uint8_t e = (uint8_t)(SAVE_DUEL_CHECKSUM_SEED & 0xFFu);
	uint8_t d = (uint8_t)(SAVE_DUEL_CHECKSUM_SEED >> 8);
	uint32_t bc = duel_save_total_size() - 6u;
	while (bc != 0u) {
		uint8_t val = gb_read8(hl);
		e = (uint8_t)(e - val);
		val = gb_read8(hl);
		hl = (uint16_t)(hl + 1);
		d = (uint8_t)(d ^ val);
		bc--;
	}
	gb_write8(base, TRUE);
	gb_write8((uint16_t)(base + 1), e);
	gb_write8((uint16_t)(base + 2), d);
	gb_write8((uint16_t)(base + 3), gb_read8(wDuelType_ADDR));
	DisableSRAM();
}
/* <<< factory SaveDuelDataToDE */

/* >>> factory LoadSavedDuelDataFromDE */
/* core.asm:6078-6119 */
void LoadSavedDuelDataFromDE(uint16_t de)
{
	EnableSRAM();
	de = (uint16_t)(de + SAVE_DUEL_HEADER_SIZE);
	for (int i = 0; kDuelDataToSave[i].addr != 0u; i++) {
		uint16_t hl = kDuelDataToSave[i].addr;
		uint32_t bc = kDuelDataToSave[i].size;
		while (bc != 0u) {
			uint8_t val = gb_read8(de);
			de = (uint16_t)(de + 1);
			gb_write8(hl, val);
			hl = (uint16_t)(hl + 1);
			bc--;
		}
	}
	DisableSRAM();
}
/* <<< factory LoadSavedDuelDataFromDE */

/* >>> factory SetBGP7OrSGB2ToCardPalette */
/* core.asm:3934-3963 */
void SetBGP7OrSGB2ToCardPalette(void)
{
	uint8_t console = gb_read8(wConsole_ADDR);

	if (console == CONSOLE_DMG)
		return;

	if (console == CONSOLE_SGB) {
		uint16_t hl = wCardPalette_ADDR;
		uint16_t de = (uint16_t)(wTempSGBPacket_ADDR + 1u);
		uint32_t n = PAL_SIZE;

		do {
			uint8_t value = gb_read8(hl++);
			gb_write8(de++, value);
		} while (--n);
		return;
	}

	CopyCGBCardPalette(0x07u);
}
/* <<< factory SetBGP7OrSGB2ToCardPalette */

/* >>> factory JPWriteByteToBGMap0 */
/* core.asm:4219-4221 */
void JPWriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c)
{
	WriteByteToBGMap0(a, b, c);
}
/* <<< factory JPWriteByteToBGMap0 */

/* >>> factory ZeroObjectPositionsAndToggleOAMCopy */
/* core.asm:3874-3878 */
void ZeroObjectPositionsAndToggleOAMCopy(void)
{
	ZeroObjectPositions();
	wVBlankOAMCopyToggle = TRUE;
}
/* <<< factory ZeroObjectPositionsAndToggleOAMCopy */

/* >>> factory LoadPlayerDeck */
/* core.asm:6195-6211 */
void LoadPlayerDeck(void)
{
	EnableSRAM();
	uint8_t sel = gb_read8(sCurrentlySelectedDeck_ADDR);
	uint16_t hl = HtimesL((uint16_t)(sel << 8 | (sDeck2Cards_ADDR - sDeck1Cards_ADDR)));
	hl = (uint16_t)(hl + sDeck1Cards_ADDR);
	uint16_t de = wPlayerDeck_ADDR;
	uint8_t c = DECK_SIZE_;
	do {
		uint8_t a = gb_read8(hl);
		hl++;
		gb_write8(de, a);
		de++;
		c--;
	} while (c != 0);
	DisableSRAM();
}
/* <<< factory LoadPlayerDeck */

/* >>> factory PrintPracticeDuelDrMasonInstructions */
/* core.asm:2748-2753 */
void PrintPracticeDuelDrMasonInstructions(uint16_t hl)
{
	(void)PrintScrollableText_WithTextBoxLabel(hl, DrMasonText);
}
/* <<< factory PrintPracticeDuelDrMasonInstructions */

/* >>> factory PrintPracticeDuelInstructionsTextBoxLabel */
/* core.asm:2767-2789 */
void PrintPracticeDuelInstructionsTextBoxLabel(void)
{
	uint8_t a = wDuelTurns;

	if (a == 7u) {
		(void)InitTextPrinting_ProcessTextFromID(1u, 0u, ReplaceDueToKnockoutPracticeDuelText);
		return;
	}
	LoadTxRam3((uint16_t)((a >> 1) + 1u));
	InitTextPrinting(1u, 0u);
	(void)PrintText(PlayersTurnPracticeDuelText, 1u, 0u);
}
/* <<< factory PrintPracticeDuelInstructionsTextBoxLabel */
