#include "home/core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/duel.h"

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu
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

#define CARDPAGE_POKEMON_DESCRIPTION 0x06u

/* SwitchCardPage dispatch: only index 0 (CardPageSwitch_00) is in scope for
 * this port; it is the only handler whose asm is provided. */
#define CARDPAGE_POKEMON_DESCRIPTION_C 0x06u

#include "home/card_data.h"

#define TILE_SIZE 0x10u
#define SGB3_COPY_LEN 0x06u

#define MAX_PLAY_AREA_POKEMON 0x06u
#define DUELVARS_ARENA_CARD   0xBBu

#define CARDPAGE_POKEMON_OVERVIEW 0x01u

#include "generated/wram.h"
#include "mem.h"

#define TRUE_VAL 0x01u
/* GB address of PrintSortNumberInCardList (engine/duel/core.asm:3438), the
 * routine immediately following the setter: setter start + 15 bytes. The
 * setter is the only writer of this pointer, which the card-list printer
 * dispatches through. */
#define PRINT_SORT_NUMBER_IN_CARD_LIST 0x574Au

#include "generated/wram.h"

#include "generated/wram.h"
#include "home/duel_animation_core.h"
#include "home/play_animation.h"

#define ANIM_DATA_BANK 7u
#define ANIM_COORDS_INDEX_ADDR 0x49e0u
#define ANIM_COORDS_ADDR 0x4a04u
#define DUEL_ANIM_STRUCT_SIZE 8u
#define PLAYER_TURN 0xc2u
#define SPRITE_ANIM_FLAG_X_INVERTED 0x01u
#define SPRITE_ANIM_FLAG_Y_INVERTED 0x02u
#define SPRITE_ANIM_FLAG_CENTERED   0x04u
#define SPRITE_ANIM_FLAG_3          0x08u
#define SPRITE_ANIM_FLAG_X_FLIP     0x20u
#define SPRITE_ANIM_FLAG_Y_FLIP     0x40u

#define COLORLESS_F 0x80u
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define FIGHTING_ENERGY 0x05u
#define FIGHTING_F 0x20u
#define FIRE_ENERGY 0x02u
#define FIRE_F 0x04u
#define GRASS_ENERGY 0x01u
#define GRASS_F 0x02u
#define LIGHTNING_ENERGY 0x04u
#define LIGHTNING_F 0x08u
#define PSYCHIC_ENERGY 0x06u
#define PSYCHIC_F 0x40u
#define WATER_ENERGY 0x03u
#define WATER_F 0x10u

#include "home/objects.h"
#include "home/lcd.h"

#include "home/empty_screen.h"
#include "home/duel.h"
#include "home/bg_map.h"

#define NUM_TYPES 0x08u
#define SYM_SPACE 0x00u
#define SYM_FIRE 0xD0u
#define SYM_PLUS 0xD8u

#include "home/duel.h"
#include "generated/hram.h"

#include "home/empty_screen.h"
#include "home/duel.h"
#include "home/bg_map.h"
#define SYM_POISONED 0x08u
#define POISONED 0x80u

#include "home/duel.h"
#define PLAY_AREA_ARENA 0u
#define SYM_0 0x20u
#include "generated/hram.h"

#define CARDPAGE_ENERGY 0x09u

/* >>> factory CardPageSwitch_08 */
/* core.asm:3838-3842 */
CardPageResult CardPageSwitch_08(void)
{
	return (CardPageResult){CARDPAGE_ENERGY + 1u, 1u};
}
/* <<< factory CardPageSwitch_08 */

#include "home/core.h"

#define FIRE 0x00u

#include "home/switch_sram.h"

#define DUELIST_TYPE_AI_OPP 0x80u
#define DUELIST_TYPE_LINK_OPP 0x01u

static uint8_t is_duelist_type(uint8_t a)
{
	return (uint8_t)((a == DUELIST_TYPE_LINK_OPP) ||
		((a & DUELIST_TYPE_AI_OPP) != 0u));
}

#include "home/card_color.h"
#include "home/duel.h"

#include "home/effect_commands.h"
#define EFFECTCMDTYPE_INITIAL_EFFECT_2 0x02u
#define EFFECTCMDTYPE_REQUIRE_SELECTION 0x05u
#define TYPE_ENERGY 0x08u
#include "home/duel.h"

#include "home/card_color.h"
#include "home/duel.h"
#include "home/duel_core.h"
#define DUELVARS_PRIZE_CARDS 0x3Cu
#define DUELVARS_CARD_LOCATIONS 0x00u
#define CARD_LOCATION_DECK 0x00u

#define ANIMATIONS_ADDR 0x4e32u
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

/* >>> factory SwitchCardPage */
/* core.asm:3769-3790 */
CardPageResult SwitchCardPage(uint8_t a)
{
	(void)a;
	return CardPageSwitch_00();
}
/* <<< factory SwitchCardPage */

/* >>> factory CardPageSwitch_00 */
/* core.asm:3792-3795 */
CardPageResult CardPageSwitch_00(void)
{
	return (CardPageResult){CARDPAGE_POKEMON_DESCRIPTION_C, 1u};
}
/* <<< factory CardPageSwitch_00 */

/* >>> factory LoadLoaded1CardGfx */
/* core.asm:3925-3932 */
void LoadLoaded1CardGfx(uint16_t de)
{
	uint16_t hl = (uint16_t)(wLoadedCard1Gfx | (uint16_t)gb_read8((uint16_t)(wLoadedCard1Gfx_ADDR + 1u)) << 8);
	hl = (uint16_t)(gb_read8(wLoadedCard1Gfx_ADDR) | (uint16_t)gb_read8((uint16_t)(wLoadedCard1Gfx_ADDR + 1u)) << 8);
	LoadCardGfx(hl, de, 0x30u, TILE_SIZE);
}
/* <<< factory LoadLoaded1CardGfx */


/* >>> factory SetSGB3ToCardPalette */
/* core.asm:3965-3974 */
void SetSGB3ToCardPalette(void)
{
	uint16_t hl = (uint16_t)(wCardPalette_ADDR + 2u);
	uint16_t de = (uint16_t)(wTempSGBPacket_ADDR + 9u);

	for (uint8_t i = 0u; i < 6u; i++) {
		gb_write8(de, gb_read8(hl));
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(de + 1u);
	}
}
/* <<< factory SetSGB3ToCardPalette */

/* >>> factory LookForCardIDInPlayArea_Bank5 */
/* core.asm:753-777 */
LookResult LookForCardIDInPlayArea_Bank5(uint8_t a, uint8_t b)
{
	wTempCardIDToLook = a;
	for (;;) {
		DuelistVarResult r = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + b));
		if (r.a == 0xFFu)
			return (LookResult){0xFFu, b, 0xC0u};
		uint8_t c = LoadCardDataToBuffer1_FromDeckIndex(r.a);
		if (wTempCardIDToLook == c)
			return (LookResult){b, b, 0x90u};
		b++;
		if (b == MAX_PLAY_AREA_POKEMON)
			return (LookResult){MAX_PLAY_AREA_POKEMON, 0xFFu, 0x00u};
	}
}
/* <<< factory LookForCardIDInPlayArea_Bank5 */

/* >>> factory ClearMemory_Bank5 */
/* core.asm:942-954 */
void ClearMemory_Bank5(uint8_t a, uint16_t hl)
{
	uint32_t n = a ? a : 0x100u;
	for (uint32_t i = 0; i < n; i++)
		gb_write8((uint16_t)(hl + (uint16_t)i), 0u);
}
/* <<< factory ClearMemory_Bank5 */

/* >>> factory CheckCardPageExists */
/* core.asm:3827-3830 */
CardPageExistsResult CheckCardPageExists(uint16_t *hl)
{
	uint8_t a = gb_read8(*hl);
	*hl = (uint16_t)(*hl + 1u);
	a |= gb_read8(*hl);
	return (CardPageExistsResult){a, (uint8_t)(a == 0u)};
}
/* <<< factory CheckCardPageExists */

/* >>> factory CardPageSwitch_PokemonEnd */
/* core.asm:3833-3836. scf leaves Z untouched, clears N/H, sets C. */
CardPageResult CardPageSwitch_PokemonEnd(void)
{
	return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW, 1u};
}
/* <<< factory CardPageSwitch_PokemonEnd */

/* >>> factory SetCardListInfoBoxText */
/* core.asm:3129-3134 */
void SetCardListInfoBoxText(uint16_t hl)
{
	wCardListInfoBoxText = (uint8_t)hl;
	gb_write8((uint16_t)(wCardListInfoBoxText_ADDR + 1u), (uint8_t)(hl >> 8));
}
/* <<< factory SetCardListInfoBoxText */

/* >>> factory LoadCardNameToTxRam2 */
/* core.asm:6796 */
void LoadCardNameToTxRam2(uint8_t a)
{
	LoadCardDataToBuffer1_FromDeckIndex(a);
	wTxRam2 = wLoadedCard1Name;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)));
}
/* <<< factory LoadCardNameToTxRam2 */

/* >>> factory LoadCardNameToTxRam2_b */
/* core.asm:6806-6813 */
void LoadCardNameToTxRam2_b(uint8_t a)
{
	LoadCardDataToBuffer1_FromDeckIndex(a);
	wTxRam2_b = wLoadedCard1Name;
	gb_write8((uint16_t)(wTxRam2_b_ADDR + 1u), gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)));
}
/* <<< factory LoadCardNameToTxRam2_b */


/* >>> factory GetAnimCoordsAndFlags */
/* core.asm:183-229 */
AnimCoordsResult GetAnimCoordsAndFlags(void)
{
	uint8_t index = 0u;
	if (!(wAnimFlags & SPRITE_ANIM_FLAG_CENTERED)) {
		uint8_t c = (uint8_t)(wDuelAnimationScreen * 12u);
		if (wDuelAnimDuelistSide != PLAYER_TURN)
			c = (uint8_t)(c + 6u);
		c = (uint8_t)(c + wDuelAnimLocationParam);
		index = rom_ptr(ANIM_DATA_BANK, ANIM_COORDS_INDEX_ADDR)[c];
	}
	const uint8_t *entry = rom_ptr(ANIM_DATA_BANK, ANIM_COORDS_ADDR) + (uint16_t)index * 3u;
	uint8_t x = entry[0];
	uint8_t y = entry[1];
	uint8_t flags = (uint8_t)(wAnimFlags & entry[2]);
	uint8_t f = (uint8_t)((flags == 0u ? 0x80u : 0u) | 0x20u);
	return (AnimCoordsResult){flags, f, x, y};
}
/* <<< factory GetAnimCoordsAndFlags */


/* >>> factory PlayBufferedDuelAnimations */
/* core.asm:311-353 */
AnimBufferResult PlayBufferedDuelAnimations(void)
{
	uint8_t a, f;
	for (;;) {
		uint8_t size = wDuelAnimBufferSize;
		uint8_t cur = wDuelAnimBufferCurPos;
		if (cur == size) {
			a = cur;
			f = 0xc0u;
			break;
		}

		uint16_t src = (uint16_t)(wDuelAnimBuffer_ADDR + cur);
		wDuelAnimBufferCurPos = (uint8_t)((cur + DUEL_ANIM_STRUCT_SIZE) & 0x7fu);

		wTempAnimation = gb_read8(src);
		wDuelAnimationScreen = gb_read8((uint16_t)(src + 1u));
		wDuelAnimDuelistSide = gb_read8((uint16_t)(src + 2u));
		wDuelAnimLocationParam = gb_read8((uint16_t)(src + 3u));
		wDuelAnimDamage = gb_read8((uint16_t)(src + 4u));
		gb_write8((uint16_t)(wDuelAnimDamage_ADDR + 1u), gb_read8((uint16_t)(src + 5u)));
		wDuelAnimSetScreen = gb_read8((uint16_t)(src + 6u));
		wDuelAnimReturnBank = gb_read8((uint16_t)(src + 7u));

		PlayLoadedDuelAnimation();
		AnimationStatusResult r = CheckAnyAnimationPlaying();
		a = r.a;
		f = r.f;
		if (f & 0x10u)
			break;
	}
	return (AnimBufferResult){a, f};
}
/* <<< factory PlayBufferedDuelAnimations */

/* >>> factory CopyListWithFFTerminatorFromHLToDE_Bank5 */
/* core.asm:1329-1336 */
CopyListResult CopyListWithFFTerminatorFromHLToDE_Bank5(uint16_t *hl, uint16_t *de)
{
	uint16_t src = *hl;
	uint16_t dst = *de;

	for (;;) {
		uint8_t a = gb_read8(src);
		src = (uint16_t)(src + 1u);
		gb_write8(dst, a);
		if (a == 0xFFu) {
			*hl = src;
			*de = dst;
			return (CopyListResult){a, 0xC0u};
		}
		dst = (uint16_t)(dst + 1u);
	}
}
/* <<< factory CopyListWithFFTerminatorFromHLToDE_Bank5 */

/* >>> factory CheckEnergyFlagsNeededInList */
/* core.asm:1581-1658 */
EnergyFlagsResult CheckEnergyFlagsNeededInList(uint8_t a)
{
	uint8_t required = a;
	uint16_t hl = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl++);
		if (deck_index == 0xffu)
			return (EnergyFlagsResult){0xffu, 0u};

		uint8_t energy = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		uint8_t flags;

		if (energy == FIRE_ENERGY)
			flags = FIRE_F;
		else if (energy == GRASS_ENERGY)
			flags = GRASS_F;
		else if (energy == LIGHTNING_ENERGY)
			flags = LIGHTNING_F;
		else if (energy == WATER_ENERGY)
			flags = WATER_F;
		else if (energy == FIGHTING_ENERGY)
			flags = FIGHTING_F;
		else if (energy == PSYCHIC_ENERGY)
			flags = PSYCHIC_F;
		else if (energy == DOUBLE_COLORLESS_ENERGY)
			flags = COLORLESS_F;
		else
			continue;

		uint8_t intersection = (uint8_t)(flags & required);
		if (intersection != 0u)
			return (EnergyFlagsResult){intersection, 1u};
	}
}
/* <<< factory CheckEnergyFlagsNeededInList */

/* >>> factory PlaceCardImageOAM */
/* core.asm:3884-3924 */
uint8_t PlaceCardImageOAM(uint16_t *hl, uint16_t *de)
{
	uint8_t l = 0xa0u;
	uint8_t x = (uint8_t)(*de >> 8);
	uint8_t y = (uint8_t)*de;
	uint8_t columns = 8u;

	Set_OBJ_8x16();

	do {
		uint8_t rows = 3u;
		uint8_t row_y = y;

		do {
			SetOneObjectAttributes(row_y, x, l, 1u);
			l = (uint8_t)(l + 2u);
			row_y = (uint8_t)(row_y + 16u);
			rows--;
		} while (rows != 0u);

		x = (uint8_t)(x + 8u);
		columns--;
	} while (columns != 0u);

	*hl = (uint16_t)((*hl & 0xff00u) | l);
	*de = (uint16_t)((uint16_t)x << 8 | y);
	gb_write8(0xcac0u, TRUE);
	return TRUE;
}
/* <<< factory PlaceCardImageOAM */

/* >>> factory PrintPlayAreaCardAttachedEnergies */
/* core.asm:5566-5626 */
void PrintPlayAreaCardAttachedEnergies(uint8_t b, uint8_t c, uint8_t e)
{
	uint16_t hl;
	uint16_t de;
	uint8_t i;
	uint8_t color;
	uint8_t amount;
	uint8_t count = (uint8_t)(NUM_TYPES - 1u);

	GetPlayAreaCardAttachedEnergies(e);

	for (i = 0u; i < 8u; i++)
		gb_write8((uint16_t)(wDefaultText_ADDR + i), SYM_SPACE);

	hl = wDefaultText_ADDR;
	de = wAttachedEnergies_ADDR;
	color = SYM_FIRE;

	do {
		amount = (uint8_t)(gb_read8(de) + 1u);
		de = (uint16_t)(de + 1u);
		do {
			amount = (uint8_t)(amount - 1u);
			if (amount == 0u)
				break;
			gb_write8(hl, color);
			hl = (uint16_t)(hl + 1u);
		} while (1);

		color = (uint8_t)(color + 1u);
		count = (uint8_t)(count - 1u);
	} while (count != 0u);

	if (gb_read8(wTotalAttachedEnergies_ADDR) >= 9u)
		gb_write8((uint16_t)(wDefaultText_ADDR + 7u), SYM_PLUS);

	de = BCCoordToBGMap0Address(b, c);
	hl = wDefaultText_ADDR;
	SafeCopyDataHLtoDE(&hl, &de, 8u);
}
/* <<< factory PrintPlayAreaCardAttachedEnergies */

/* >>> factory DiscardRetreatCostCards */
/* core.asm:5776-5787 */
DiscardRetreatCostCardsResult DiscardRetreatCostCards(void)
{
	uint16_t hl = hTempRetreatCostCards_ADDR;

	for (;;) {
		uint8_t card = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (card == 0xFFu)
			return (DiscardRetreatCostCardsResult){0xFFu, 0xC0u, hl};
		PutCardInDiscardPile(card);
	}
}
/* <<< factory DiscardRetreatCostCards */

/* >>> factory OppAction_DrawCard */
/* core.asm:6514-6520 */
OppActionDrawResult OppAction_DrawCard(void)
{
	DrawCardResult r = DrawCardFromDeck();
	if ((r.f & 0x10u) == 0u)
		AddCardToHand(r.a);
	return (OppActionDrawResult){r.a, r.f};
}
/* <<< factory OppAction_DrawCard */

/* >>> factory PrintSortNumberInCardList_SetPointer */
void PrintSortNumberInCardList_SetPointer(void)
{
	gb_write8(wPrintSortNumberInCardListPtr_ADDR, (uint8_t)PRINT_SORT_NUMBER_IN_CARD_LIST);
	gb_write8((uint16_t)(wPrintSortNumberInCardListPtr_ADDR + 1u),
	          (uint8_t)(PRINT_SORT_NUMBER_IN_CARD_LIST >> 8));
	wSortCardListByID = TRUE_VAL;
}
/* <<< factory PrintSortNumberInCardList_SetPointer */

/* >>> factory PrintSortNumberInCardList */
void PrintSortNumberInCardList(void)
{
	uint8_t c = 2u;
	uint16_t hl = (uint16_t)(wDuelTempList_ADDR + 10u);
	for (;;) {
		uint8_t value = gb_read8(hl++);
		if (value == 0xFFu)
			break;
		if (value != SYM_SPACE)
			value = (uint8_t)(value + SYM_0);
		WriteByteToBGMap0(value, 1u, c);
		c = (uint8_t)(c + 2u);
	}
}
/* <<< factory PrintSortNumberInCardList */

/* >>> factory PrintEnergiesOfColor */
/* core.asm:4416-4431 */
PrintEnergiesResult PrintEnergiesOfColor(uint8_t a, uint8_t b, uint8_t c, uint8_t e)
{
	uint8_t count;
	uint8_t value;

	e = (uint8_t)(e + 1u);
	count = (uint8_t)(a & 0x0Fu);
	if (count == 0u)
		return (PrintEnergiesResult){a, b, e};

	value = e;
	do {
		JPWriteByteToBGMap0(value, b, c);
		b = (uint8_t)(b + 1u);
	} while (--count);

	return (PrintEnergiesResult){value, b, e};
}
/* <<< factory PrintEnergiesOfColor */

/* >>> factory PrintCardPageWeaknessesOrResistances */
/* core.asm:4432-4455 */
void PrintCardPageWeaknessesOrResistances(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t mask = a;
	uint8_t type = FIRE;

	for (;;) {
		type = (uint8_t)(type + 1u);
		if (type >= 8u)
			break;

		if (mask & 0x80u) {
			JPWriteByteToBGMap0(type, b, c);
			b = (uint8_t)(b + 1u);
		}
		mask = (uint8_t)(mask << 1);
	}
}
/* <<< factory PrintCardPageWeaknessesOrResistances */

/* >>> factory Func_6423 */
/* core.asm:5607-5620 */
Func6423Result Func_6423(uint8_t b, uint8_t c)
{
	uint16_t pos = wDefaultText_ADDR;
	uint8_t value = 0u;
	uint32_t n = 8u;

	do {
		value = gb_read8(pos);
		pos = (uint16_t)(pos + 1u);
		JPWriteByteToBGMap0(value, b, c);
		b = (uint8_t)(b + 1u);
	} while (--n);

	return (Func6423Result){value, b, pos};
}
/* <<< factory Func_6423 */

/* >>> factory InitVariablesToBeginDuel */
/* core.asm:7651-7710 */
void InitVariablesToBeginDuel(void)
{
	uint8_t a = 0u;

	wDuelFinished = 0u;
	wDuelTurns = 0u;
	wUnused_cce7 = 0u;
	wUnused_cc0f = 0xffu;
	wPlayerAttackingCardIndex = 0xffu;
	wPlayerAttackingAttackIndex = 0xffu;

	EnableSRAM();
	wSkipDelayAllowed = sSkipDelayAllowed;
	DisableSRAM();

	a = wPlayerDuelistType;
	if (is_duelist_type(a) == 0u) {
		a = wOpponentDuelistType;
		if (is_duelist_type(a) == 0u)
			a = 0u;
	}
	wDuelType = a;
}
/* <<< factory InitVariablesToBeginDuel */

/* >>> factory CreateCardAttrBlkPacket */
/* core.asm:4082-4101 */
uint16_t CreateCardAttrBlkPacket(uint8_t a, uint8_t d, uint8_t e)
{
	uint16_t hl = wTempSGBPacket_ADDR;
	gb_write8(hl, (uint8_t)((ATTR_BLK << 3) + 1u));
	hl++;
	gb_write8(hl, 1u);
	hl++;
	hl = CreateCardAttrBlkPacket_DataSet(hl, a, d, e);
	for (uint8_t i = 0u; i < 4u; i++)
		gb_write8(hl++, 0u);
	return wTempSGBPacket_ADDR;
}
/* <<< factory CreateCardAttrBlkPacket */

/* >>> factory CardPageSwitch_PokemonAttack1Page2 */
/* core.asm:3811-3815 */
CardPageExistsResult CardPageSwitch_PokemonAttack1Page2(uint16_t *hl)
{
	*hl = (uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u);
	return CheckCardPageExists(hl);
}
/* <<< factory CardPageSwitch_PokemonAttack1Page2 */

/* >>> factory CardPageSwitch_PokemonAttack2Page1 */
/* core.asm:3817-3821 */
CardPageExistsResult CardPageSwitch_PokemonAttack2Page1(void)
{
	uint16_t hl = wLoadedCard1Atk2Name_ADDR;
	return CheckCardPageExists(&hl);
}
/* <<< factory CardPageSwitch_PokemonAttack2Page1 */

/* >>> factory AIDiscourage */
/* core.asm:95-113 */
void AIDiscourage(uint8_t a)
{
	uint8_t score = wAIScore;

	if (score == 0u)
		return;
	if (score < a) {
		wAIScore = 0u;
		return;
	}
	wAIScore = (uint8_t)(score - a);
}
/* <<< factory AIDiscourage */

/* >>> factory ConvertHPToDamageCounters_Bank5 */
/* core.asm:963-975 */
ConvertHPToDamageCountersResult ConvertHPToDamageCounters_Bank5(uint8_t a)
{
	uint8_t value = a;
	uint8_t count = 0u;

	for (;;) {
		uint8_t next = (uint8_t)(value - 10u);
		if (value < 10u)
			break;
		value = next;
		count++;
	}

	return (ConvertHPToDamageCountersResult){count, 0x70u};
}
/* <<< factory ConvertHPToDamageCounters_Bank5 */

/* >>> factory CalculateBDividedByA_Bank5 */
/* core.asm:981-995 */
CalculateBDividedByAResult CalculateBDividedByA_Bank5(uint8_t a, uint8_t b)
{
	uint8_t divisor = a;
	uint8_t remainder = b;
	uint8_t quotient = 0u;

	for (;;) {
		uint8_t result = (uint8_t)(remainder - divisor);
		if (remainder < divisor) {
			uint8_t flags = 0x50u;
			if ((remainder & 0x0Fu) < (divisor & 0x0Fu))
				flags = (uint8_t)(flags | 0x20u);
			if (result == 0u)
				flags = (uint8_t)(flags | 0x80u);
			return (CalculateBDividedByAResult){quotient, flags};
		}
		remainder = result;
		quotient = (uint8_t)(quotient + 1u);
	}
}
/* <<< factory CalculateBDividedByA_Bank5 */

/* >>> factory PrintCardPageRarityIcon */
/* core.asm:4617-4626 */
ProcessTextHeaderResult PrintCardPageRarityIcon(uint8_t a, uint8_t d, uint8_t e, uint16_t hl)
{
	a = (uint8_t)((a + 1u) << 1);
	hl = (uint16_t)(hl + a);
	return InitTextPrinting_ProcessTextFromPointerToID(d, e, hl);
}
/* <<< factory PrintCardPageRarityIcon */

/* >>> factory SetNoLineSeparation */
/* core.asm:4768-4769 */
uint8_t SetNoLineSeparation(void)
{
	SetLineSeparation(1u);
	return 1u;
}
/* <<< factory SetNoLineSeparation */

/* >>> factory AIPlayInitialBasicCards */
AIPlayInitialBasicCardsResult AIPlayInitialBasicCards(void)
{
	(void)CreateHandCardList(0);
	uint16_t scan = wDuelTempList_ADDR;
	for (;;) {
		uint8_t index = gb_read8(scan++);
		hTempCardIndex_ff98 = index;
		if (index == 0xFFu)
			return (AIPlayInitialBasicCardsResult){0xFFu, 0xC0u};
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		if (wLoadedCard1Type >= TYPE_ENERGY || wLoadedCard1Stage != 0u)
			continue;
		(void)PutHandPokemonCardInPlayArea(index, 0x80u);
	}
}
/* <<< factory AIPlayInitialBasicCards */

/* >>> factory CheckIfEnoughParticularAttachedEnergy */
CheckIfEnoughParticularAttachedEnergyResult CheckIfEnoughParticularAttachedEnergy(
	uint8_t a, uint16_t hl, uint8_t b)
{
	uint8_t cost = (uint8_t)(a & 0x0Fu);
	if (cost == 0u)
		return (CheckIfEnoughParticularAttachedEnergyResult){b, 0x80u, (uint8_t)(b + 1u), (uint16_t)(hl + 1u)};
	wTempLoadedAttackEnergyCost = cost;
	uint8_t attached = gb_read8(hl);
	if (cost <= attached)
		return (CheckIfEnoughParticularAttachedEnergyResult){
			b, 0u, (uint8_t)(b + 1u), (uint16_t)(hl + 1u)};
	wTempLoadedAttackEnergyNeededAmount = (uint8_t)(cost - attached);
	wTempLoadedAttackEnergyNeededType = b;
	return (CheckIfEnoughParticularAttachedEnergyResult){
		b, 0x10u, (uint8_t)(b + 1u), (uint16_t)(hl + 1u)};
}
/* <<< factory CheckIfEnoughParticularAttachedEnergy */

/* >>> factory Func_14323 */
Func14323Result Func_14323(void)
{
	uint16_t commands = (uint16_t)(gb_read8(wLoadedAttackEffectCommands_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wLoadedAttackEffectCommands_ADDR + 1u)) << 8));
	EffectCmdLookup r = CheckMatchingCommand(EFFECTCMDTYPE_INITIAL_EFFECT_2, commands);
	if (r.carry != 0u)
		r = CheckMatchingCommand(EFFECTCMDTYPE_REQUIRE_SELECTION, r.hl);
	(void)r;
	return (Func14323Result){0x80u};
}
/* <<< factory Func_14323 */

/* >>> factory CreateEnergyCardListFromHand */
CoreCardListResult CreateEnergyCardListFromHand(uint8_t a)
{
	uint8_t count = GetTurnDuelistVariable(0xeeu).a;
	uint16_t hand = (uint16_t)(((uint16_t)hWhoseTurn << 8) | 0x42u);
	uint16_t dst = wDuelTempList_ADDR;
	(void)a;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t deck_index = gb_read8((uint16_t)(hand + i));
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		if ((GetCardType(card_id) & 0x08u) != 0u)
			gb_write8(dst++, deck_index);
	}
	gb_write8(dst, 0xFFu);
	uint8_t first = gb_read8(wDuelTempList_ADDR);
	return (CoreCardListResult){first, first == 0xFFu ? 0x90u : 0x00u};
}
/* <<< factory CreateEnergyCardListFromHand */

/* >>> factory LookForCardIDInHand */

CoreCardListResult LookForCardIDInHand(uint8_t a)
{
	uint8_t count = GetTurnDuelistVariable(0xeeu).a;
	uint16_t hand = (uint16_t)(((uint16_t)hWhoseTurn << 8) | 0x42u);
	uint8_t last_id = 0u;
	for (uint8_t i = 0; i < count; i++) {
		uint8_t deck_index = gb_read8((uint16_t)(hand + i));
		last_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		if (last_id == a) {
			uint8_t f = deck_index == 0u ? 0x80u : 0x00u;
			return (CoreCardListResult){deck_index, f};
		}
	}
	return (CoreCardListResult){last_id, 0x90u};
}
/* <<< factory LookForCardIDInHand */

/* >>> factory LookForCardIDInHandList_Bank5 */
CoreCardListResult LookForCardIDInHandList_Bank5(uint8_t a)
{
	(void)CreateHandCardList(0u);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			return (CoreCardListResult){0xFFu, 0xC0u};
		if ((uint8_t)GetCardIDFromDeckIndex(deck_index) == a)
			return (CoreCardListResult){deck_index, 0x90u};
	}
}
/* <<< factory LookForCardIDInHandList_Bank5 */

/* >>> factory CheckForEvolutionInDeck */
CheckForEvolutionInDeckResult CheckForEvolutionInDeck(uint8_t a)
{
	uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	DuelistVarResult arena_var = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	gb_write8(arena_var.hl, a);
	for (uint8_t e = 0; e < DUELVARS_PRIZE_CARDS; e++) {
		if (GetTurnDuelistVariable((uint8_t)(DUELVARS_CARD_LOCATIONS + e)).a != CARD_LOCATION_DECK)
			continue;
		EvolveResult r = CheckIfCanEvolveInto(e, PLAY_AREA_ARENA);
		if (!(r.f & 0x10u)) {
			gb_write8(arena_var.hl, arena);
			return (CheckForEvolutionInDeckResult){e, (uint8_t)(0x10u | (e == 0 ? 0x80u : 0u)), a, e, arena_var.hl};
		}
	}
	gb_write8(arena_var.hl, arena);
	return (CheckForEvolutionInDeckResult){arena, (uint8_t)(arena == 0 ? 0x80u : 0u), a, DUELVARS_PRIZE_CARDS, arena_var.hl};
}
/* <<< factory CheckForEvolutionInDeck */

/* >>> factory LookForCardThatIsKnockedOutOnDevolution */
LookForCardThatIsKnockedOutOnDevolutionResult LookForCardThatIsKnockedOutOnDevolution(void)
{
	uint8_t saved = hTempPlayAreaLocation_ff9d;
	SwapTurn();
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (uint8_t c = PLAY_AREA_ARENA; c < count; c++) {
		hTempPlayAreaLocation_ff9d = c;
		CardOneStageBelowResult below = GetCardOneStageBelow(0, c);
		if (below.f & 0x10u)
			continue;
		LoadCardDataToBuffer2_FromDeckIndex(below.d);
		uint8_t hp = wLoadedCard2HP;
		uint8_t current = GetCardDamageAndMaxHP(c).a;
		if (hp >= current) {
			SwapTurn(); hTempPlayAreaLocation_ff9d = saved;
			return (LookForCardThatIsKnockedOutOnDevolutionResult){c, 0x10u, count, c, (uint16_t)((uint16_t)(hWhoseTurn == 0xC2u ? 0xC3u : 0xC2u) << 8 | 0xBAu)};
		}
	}
	SwapTurn(); hTempPlayAreaLocation_ff9d = saved;
	return (LookForCardThatIsKnockedOutOnDevolutionResult){saved, (uint8_t)(saved == 0u ? 0x80u : 0u), count, count, (uint16_t)((uint16_t)(hWhoseTurn == 0xC2u ? 0xC3u : 0xC2u) << 8 | 0xBBu)};
}
/* <<< factory LookForCardThatIsKnockedOutOnDevolution */

/* >>> factory CalculateParticularAttachedEnergyNeeded */
CalculateParticularAttachedEnergyNeededResult CalculateParticularAttachedEnergyNeeded(uint8_t a, uint8_t b, uint16_t hl)
{
	uint8_t low = (uint8_t)(a & 0x0Fu);
	uint8_t next_b = (uint8_t)(b + 1u);
	if (low == 0u)
		return (CalculateParticularAttachedEnergyNeededResult){0u, (uint8_t)(next_b == 0u ? 0x80u : 0u), next_b, (uint16_t)(hl + 1u)};
	gb_write8(wTempLoadedAttackEnergyCost_ADDR, low);
	uint8_t current = gb_read8(hl);
	uint8_t result = (uint8_t)(low - current);
	if (low >= current)
		return (CalculateParticularAttachedEnergyNeededResult){result, (uint8_t)(next_b == 0u ? 0x80u : 0u), next_b, (uint16_t)(hl + 1u)};
	gb_write8(wTempLoadedAttackEnergyNeededAmount_ADDR, result);
	return (CalculateParticularAttachedEnergyNeededResult){result, (uint8_t)(0x10u | (next_b == 0u ? 0x80u : 0u)), next_b, (uint16_t)(hl + 1u)};
}
/* <<< factory CalculateParticularAttachedEnergyNeeded */

/* >>> factory GetAnimationData */
AnimationDataResult GetAnimationData(void)
{
	uint8_t animation = wTempAnimation;
	uint16_t offset = (uint16_t)animation * 6u;
	uint16_t address = (uint16_t)(ANIMATIONS_ADDR + offset);
	uint8_t f = 0u;
	if (((offset & 0x0fffu) + (ANIMATIONS_ADDR & 0x0fffu)) > 0x0fffu)
		f |= 0x20u;
	if (address < ANIMATIONS_ADDR)
		f |= 0x10u;
	return (AnimationDataResult){animation, f, address};
}
/* <<< factory GetAnimationData */
