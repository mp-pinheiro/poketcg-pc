#include "home/core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/menus.h"
#include "home/serial.h"
/* >>> factory statics */
#define MAX_HP 120u
#define HP_BAR_LENGTH 12u
#define SYM_HP_OK 0x16u
#define SYM_HP_NOK 0x17u
#include "home/duel.h"

#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xEFu
#define DUELVARS_ARENA_CARD_HP                  0xC8u
#define MENU_CANCEL 0xFFu
#define PAD_A     0x01u
#define PAD_B     0x02u
#define PAD_START 0x08u
#define B_PAD_B_BIT 0x02u

#define ASLEEP           0x02u
#define CNF_SLP_PRZ       0x0Fu
#define PARALYZED        0x03u
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define DUELVARS_ARENA_CARD_LAST_TURN_STATUS 0xF5u
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
#include "home/text_box.h"
#include "home/process_text.h"
#include "home/print_text.h"

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

#include "home/frames.h"
#include "home/lcd.h"
#include "home/tiles.h"
#define CONSOLE_CGB 0x02u
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
#define TYPE_ENERGY_DOUBLE_COLORLESS 0x0Eu
#define EXEGGCUTE 0x28u
#define EXEGGUTOR 0x29u
#define PSYDUCK 0x44u
#define GOLDUCK 0x45u
#define SURFING_PIKACHU_LV13 0x65u
#define SURFING_PIKACHU_ALT_LV13 0x66u
#define EEVEE 0xBCu
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

/* SwitchCardPage dispatches the page-zero and overview handlers ported here. */

/* >>> factory CardPageSwitch_PokemonOverviewOrDescription */
/* core.asm:3797-3800 */
CardPageResult CardPageSwitch_PokemonOverviewOrDescription(void)
{
	return (CardPageResult){CARDPAGE_POKEMON_OVERVIEW, 0u};
}
/* <<< factory CardPageSwitch_PokemonOverviewOrDescription */

/* >>> factory SwitchCardPage */
/* core.asm:3769-3790 */
CardPageResult SwitchCardPage(uint8_t a)
{
	switch (a) {
	case 0u:
		return CardPageSwitch_00();
	case CARDPAGE_POKEMON_OVERVIEW:
		return CardPageSwitch_PokemonOverviewOrDescription();
	default:
		return (CardPageResult){a, 0u};
	}
}
/* <<< factory SwitchCardPage */

/* >>> factory CardPageSwitch_00 */
/* core.asm:3792-3795 */
CardPageResult CardPageSwitch_00(void)
{
	return (CardPageResult){CARDPAGE_POKEMON_DESCRIPTION_C, 1u};
}
/* <<< factory CardPageSwitch_00 */

/* SwitchCardPage dispatches the page-zero and overview handlers ported here. */

#include "home/duel_core.h"

#include "home/duel.h"

#include "home/copy.h"
#include "home/switch_sram.h"

#include "home/bg_map.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#define PLAY_AREA_BENCH_1   0x01u
#define POKEMON_POWER       0x04u

#include "home/menus.h"

#include "home/core.h"
#include "home/switch_sram.h"
#include "generated/sram.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/core.h"
#include "home/random.h"

/* Opponent deck IDs (deck_constants.asm). These six non-boss decks are the ones
 * whose AI skips a pending Trainer-card action half the time instead of a
 * quarter of the time. */
#define MUSCLES_FOR_BRAINS_DECK_ID      0x1au
#define BLISTERING_POKEMON_DECK_ID      0x1bu
#define WATERFRONT_POKEMON_DECK_ID      0x1cu
#define BOOM_BOOM_SELFDESTRUCT_DECK_ID  0x1du
#define KALEIDOSCOPE_DECK_ID            0x1eu
#define RESHUFFLE_DECK_ID               0x1fu

#include "home/duel.h"
#include "mem.h"

typedef struct { uint8_t a; uint8_t f; uint16_t de; uint16_t hl; } PlayInOrderResult;

/* core.asm:1201-1228 (.PlayPokemonCardInOrder). de enters pointing at the two-byte AI
 * priority-list pointer field; the field's first two bytes ARE the list pointer
 * (ld c,[de] / inc de / ld d,[de] / ld e,c recombine de = field[1]<<8|field[0]).
 * Walks the $00-terminated card-ID list, handing each ID to RemoveCardIDInList against
 * the hand list at *hl; the callee advances *hl and that advance persists across IDs
 * (and, in the caller, across the arena/bench calls -- the asm never restores hl).
 * On the first ID found in hand, plays it via PutHandPokemonCardInPlayArea and returns
 * its a with `or a` flags (Z iff a==0, C clear); on the terminator returns a=0 with
 * Z|C (or a set Z, then scf). de returns advanced past the byte last consumed. */
static PlayInOrderResult play_pokemon_card_in_order(uint16_t *hl, uint16_t de)
{
	uint8_t c = gb_read8(de);
	de++;
	uint8_t d = gb_read8(de);
	de = (uint16_t)((uint16_t)d << 8 | c);
	for (;;) {
		uint8_t a = gb_read8(de);
		de++;
		if (a == 0x00u)
			return (PlayInOrderResult){a, 0x90u, de, *hl};
		RemoveCardIDResult removed = RemoveCardIDInList(hl, a);
		if ((removed.f & 0x10u) == 0x00u)
			continue;
		PutHandPokemonResult placed = PutHandPokemonCardInPlayArea(removed.a, removed.f);
		return (PlayInOrderResult){placed.a, (uint8_t)((placed.a == 0x00u) ? 0x80u : 0x00u), de, *hl};
	}
}

typedef struct {
	uint8_t a;
	uint8_t f;
} CardPageEnergyResult;

#include "home/save.h"
#include "home/script.h"
#include "home/switch_sram.h"

#define DUELTYPE_LINK 0x01u
#define LINK_OPPONENT_TURN_FRAME_FUNCTION 0x0000u

static const uint8_t kPlayAreaLocationTileNumbers[24] = {
	0xe0u, 0xe1u, 0xe2u, 0x00u,
	0xe3u, 0xe4u, 0xe5u, 0x00u,
	0xe3u, 0xe4u, 0xe6u, 0x00u,
	0xe3u, 0xe4u, 0xe7u, 0x00u,
	0xe3u, 0xe4u, 0xe8u, 0x00u,
	0xe3u, 0xe4u, 0xe9u, 0x00u,
};

#include "home/empty_screen.h"
#include "home/tiles.h"

#define PLAY_AREA_CARD_LIST 0x02u

#include "generated/sram.h"
#include "home/core.h"
#include "home/unused_save_validation.h"

#include "generated/wram.h"
#include "home/core.h"
/* <<< factory statics */

/* >>> factory DrawHPBar */
void DrawHPBar(uint8_t d, uint8_t e)
{
	uint8_t a = MAX_HP;
	for (uint8_t i = 0u; i < HP_BAR_LENGTH; i++)
		gb_write8((uint16_t)(wDefaultText_ADDR + i), SYM_SPACE);

	a = d;
	uint8_t tile = SYM_HP_OK;
	uint16_t dst = wDefaultText_ADDR;
	while (a != 0u) {
		gb_write8(dst, tile);
		dst++;
		a = (uint8_t)(a - (MAX_HP / HP_BAR_LENGTH));
	}

	a = (uint8_t)(d - e);
	tile = SYM_HP_NOK;
	dst = wDefaultText_ADDR;
	while (a != 0u) {
		gb_write8(dst, tile);
		dst++;
		a = (uint8_t)(a - (MAX_HP / HP_BAR_LENGTH));
	}
}
/* <<< factory DrawHPBar */

/* >>> factory ValidateSavedDuelDataFromHL */
ValidateSavedDuelDataResult ValidateSavedDuelDataFromHL(uint16_t hl)
{
	EnableSRAM();
	uint8_t valid = gb_read8(hl++);
	uint8_t carry = 0u;
	if (valid != 0u) {
		uint8_t e = (uint8_t)(SAVE_DUEL_CHECKSUM_SEED & 0xFFu);
		uint8_t d = (uint8_t)(SAVE_DUEL_CHECKSUM_SEED >> 8);
		e = (uint8_t)(gb_read8(hl) - e);
		hl++;
		d = (uint8_t)(gb_read8(hl) ^ d);
		hl = (uint16_t)(hl + 2u);
		uint32_t bc = 820u;
		while (bc != 0u) {
			uint8_t value = gb_read8(hl);
			e = (uint8_t)(e + value);
			value = gb_read8(hl++);
			d = (uint8_t)(d ^ value);
			bc--;
		}
		carry = (uint8_t)((e != 0u || d != 0u) ? 0x10u : 0x80u);
	} else {
		carry = 0x90u;
	}
	DisableSRAM();
	return (ValidateSavedDuelDataResult){carry, hl};
}
/* <<< factory ValidateSavedDuelDataFromHL */

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
/* >>> factory CheckSkipDelayAllowed */
/* core.asm:6216-6224 */
CheckSkipDelayAllowedResult CheckSkipDelayAllowed(uint8_t f, uint8_t b, uint8_t c,
	uint8_t d, uint8_t e, uint16_t hl)
{
	if (gb_read8(wSkipDelayAllowed_ADDR) == 0u)
		f = FLAG_Z;
	else if ((gb_read8(hKeysHeld_ADDR) & PAD_B) != 0u)
		f = FLAG_C;
	else
		f = 0xa0u;
	return (CheckSkipDelayAllowedResult){b, c, d, e, f, hl};
}
/* <<< factory CheckSkipDelayAllowed */

/* >>> factory AIMakeDecision */
/* core.asm:6229-6263 */
AIMakeDecisionResult AIMakeDecision(uint8_t a)
{
	gb_write8(hOppActionTableIndex_ADDR, a);
	uint8_t delay = gb_read8(wSkipDuelistIsThinkingDelay_ADDR);
	gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 0u);
	if (delay == 0u) {
		while (gb_read8(wVBlankCounter_ADDR) < 60u)
			gb_write8(wVBlankCounter_ADDR,
			          (uint8_t)(gb_read8(wVBlankCounter_ADDR) + 1u));
	}

	gb_write8(wOpponentTurnEnded_ADDR, 0u);
	if (a == 0x08u)
		gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);
	uint8_t f = 0u;
	if (gb_read8(wDuelFinished_ADDR) != 0u ||
	    gb_read8(wOpponentTurnEnded_ADDR) != 0u)
		f = FLAG_C;
	if (gb_read8(wSkipDuelistIsThinkingDelay_ADDR) == 0u)
		gb_write8(wVBlankCounter_ADDR, 0u);
	return (AIMakeDecisionResult){0u, 0u, 0u, 0u, f};
}
/* <<< factory AIMakeDecision */

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


/* >>> factory PrintCardListHeaderAndInfoBoxTexts */
void PrintCardListHeaderAndInfoBoxTexts(void)
{
	uint8_t d = 1u;
	uint8_t e = 14u;
	AdjustCoordinatesForBGScroll(&d, &e);
	InitTextPrinting(d, e);
	uint16_t text = (uint16_t)(gb_read8(wCardListInfoBoxText_ADDR)
		| ((uint16_t)gb_read8((uint16_t)(wCardListInfoBoxText_ADDR + 1u)) << 8));
	(void)PrintTextNoDelay(text, d, e);
	text = (uint16_t)(gb_read8(wCardListHeaderText_ADDR)
		| ((uint16_t)gb_read8((uint16_t)(wCardListHeaderText_ADDR + 1u)) << 8));
	d = 1u;
	e = 1u;
	InitTextPrinting(d, e);
	(void)PrintTextNoDelay(text, d, e);
}
/* <<< factory PrintCardListHeaderAndInfoBoxTexts */




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
/* core.asm:6806-6821 */
uint8_t LoadCardNameToTxRam2_b(uint8_t a)
{
	LoadCardDataToBuffer1_FromDeckIndex(a);
	wTxRam2_b = wLoadedCard1Name;
	uint8_t hi = gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u));
	gb_write8((uint16_t)(wTxRam2_b_ADDR + 1u), hi);
	return hi;
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
/* >>> factory CardPageSwitch_EnergyEnd */
/* core.asm:3857-3860 */
CardPageResult CardPageSwitch_EnergyEnd(void)
{
	return (CardPageResult){CARDPAGE_ENERGY, 1u};
}
/* <<< factory CardPageSwitch_EnergyEnd */

/* >>> factory CardPageSwitch_0c */
/* core.asm:3863-3866 */
CardPageResult CardPageSwitch_0c(void)
{
	return (CardPageResult){CARDPAGE_TRAINER_2, 1u};
}
/* <<< factory CardPageSwitch_0c */

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
	EffectCmdLookup initial = CheckMatchingCommand(EFFECTCMDTYPE_INITIAL_EFFECT_2, commands);
	if (initial.carry == 0u)
		return (Func14323Result){FLAG_C};
	EffectCmdLookup selection = CheckMatchingCommand(EFFECTCMDTYPE_REQUIRE_SELECTION, initial.hl);
	return (Func14323Result){selection.carry == 0u ? FLAG_C : FLAG_Z};
}
/* <<< factory Func_14323 */

/* >>> factory CreateEnergyCardListFromHand */
CoreCardListResult CreateEnergyCardListFromHand(uint8_t a)
{
	uint8_t count = GetTurnDuelistVariable(0xeeu).a;
	uint16_t hand = (uint16_t)(((uint16_t)hWhoseTurn << 8) | 0x42u);
	uint16_t dst = wDuelTempList_ADDR;
	uint8_t remaining = count;
	(void)a;
	while (remaining != 0u) {
		uint8_t deck_index = gb_read8(hand++);
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		if ((GetCardType(card_id) & TYPE_ENERGY) != 0u)
			gb_write8(dst++, deck_index);
		remaining--;
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
		if (last_id == a)
			return (CoreCardListResult){deck_index, deck_index == 0u ? 0x80u : 0x00u};
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
		if ((uint8_t)LoadCardDataToBuffer1_FromDeckIndex(deck_index) == a)
			return (CoreCardListResult){deck_index, 0x90u};
	}
}
/* <<< factory LookForCardIDInHandList_Bank5 */


/* >>> factory CheckForEvolutionInDeck */
CheckForEvolutionInDeckResult CheckForEvolutionInDeck(uint8_t a, uint8_t f)
{
    DuelistVarResult av = GetTurnDuelistVariable(0xBBu); uint8_t arena = av.a;
    gb_write8(av.hl, a);
    for (uint8_t e = 0; e < 0x3Cu; e++) {
        if (GetTurnDuelistVariable(e).a != 0u) continue;
        EvolveResult r = CheckIfCanEvolveInto(e, 0u);
        if (!(r.f & 0x10u)) { gb_write8(av.hl, arena); return (CheckForEvolutionInDeckResult){e, (uint8_t)(0x10u | (f & 0x80u))}; }
    }
    gb_write8(av.hl, arena); return (CheckForEvolutionInDeckResult){arena, arena == 0u ? 0x80u : 0u};
}
/* <<< factory CheckForEvolutionInDeck */


/* >>> factory LookForCardThatIsKnockedOutOnDevolution */
LookForCardThatIsKnockedOutOnDevolutionResult LookForCardThatIsKnockedOutOnDevolution(uint8_t f)
{
    uint8_t saved = hTempPlayAreaLocation_ff9d; SwapTurn();
    uint8_t count = GetTurnDuelistVariable(0xEFu).a;
    uint8_t c=0; do { hTempPlayAreaLocation_ff9d=c; CardOneStageBelowResult b=GetCardOneStageBelow(0u,c); if (!(b.f&0x10u)) { LoadCardDataToBuffer2_FromDeckIndex(b.d); uint8_t hp=gb_read8(wLoadedCard2HP_ADDR); gb_write8(wTempAI_ADDR,hp); uint8_t rem=GetCardDamageAndMaxHP(c).a; if (hp <= rem) { SwapTurn(); hTempPlayAreaLocation_ff9d=saved; return (LookForCardThatIsKnockedOutOnDevolutionResult){c,(uint8_t)(0x10u|(f&0x80u))}; } } c=(uint8_t)(c+1u); } while (c != count);
    SwapTurn(); hTempPlayAreaLocation_ff9d=saved; return (LookForCardThatIsKnockedOutOnDevolutionResult){saved,saved?0u:0x80u};
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

/* >>> factory CheckCardEvolutionInHandOrDeck */
CheckCardEvolutionInHandOrDeckResult CheckCardEvolutionInHandOrDeck(uint8_t a)
{
	DuelistVarResult arena = GetTurnDuelistVariable(0xBBu);
	uint8_t original = arena.a;
	gb_write8(arena.hl, a);
	for (uint8_t e = 0; e < 60u; e++) {
		uint8_t location = GetTurnDuelistVariable(e).a;
		if (location != 0x00u && location != 0x01u)
			continue;
		EvolveResult check = CheckIfCanEvolveInto(e, 0u);
		if ((check.f & 0x10u) == 0u) {
			gb_write8(arena.hl, original);
			return (CheckCardEvolutionInHandOrDeckResult){e, 0x10u};
		}
	}
	gb_write8(arena.hl, original);
	return (CheckCardEvolutionInHandOrDeckResult){original, (uint8_t)(original == 0u ? 0x80u : 0u)};
}
/* <<< factory CheckCardEvolutionInHandOrDeck */


/* >>> factory CheckIfOpponentHasBossDeckID */
CheckIfOpponentHasBossDeckIDResult CheckIfOpponentHasBossDeckID(uint8_t a)
{
	uint8_t carry = (wOpponentDeckID >= 0x0Cu && wOpponentDeckID < 0x1Cu) ? 1u : 0u;
	return (CheckIfOpponentHasBossDeckIDResult){a, carry};
}
/* <<< factory CheckIfOpponentHasBossDeckID */


/* >>> factory RaiseAIScoreToAllMatchingIDsInBench */
uint16_t RaiseAIScoreToAllMatchingIDsInBench(uint8_t a)
{
	DuelistVarResult bench = GetTurnDuelistVariable(0xBCu);
	uint8_t e = 0u;
	for (;;) {
		e = (uint8_t)(e + 1u);
		uint8_t deck_index = gb_read8(bench.hl);
		bench.hl = (uint16_t)(bench.hl + 1u);
		if (deck_index == 0xFFu)
			return bench.hl;
		if ((uint8_t)GetCardIDFromDeckIndex(deck_index) != a)
			continue;
		uint16_t score = (uint16_t)(0xCDE4u + e);
		gb_write8(score, (uint8_t)(gb_read8(score) + 5u));
	}
}
/* <<< factory RaiseAIScoreToAllMatchingIDsInBench */

/* >>> factory GetDamageNumberChars */
void GetDamageNumberChars(void)
{
	uint16_t value = (uint16_t)(wDuelAnimDamage |
		((uint16_t)gb_read8((uint16_t)(wDuelAnimDamage_ADDR + 1u)) << 8));
	uint16_t divisors[2] = {100u, 10u};
	uint16_t dst = wDecimalChars_ADDR;
	for (uint8_t i = 0; i < 2u; i++) {
		uint8_t digit = 0x4Eu;
		for (;;) {
			digit = (uint8_t)(digit + 1u);
			uint16_t next = (uint16_t)(value - divisors[i]);
			if (next > value)
				break;
			value = next;
		}
		gb_write8(dst, digit);
		dst = (uint16_t)(dst + 1u);
	}
	gb_write8(dst, (uint8_t)(value + 0x4Fu));
	for (uint8_t i = 0; i < 2u; i++) {
		if (gb_read8((uint16_t)(wDecimalChars_ADDR + i)) != 0x4Fu)
			break;
		gb_write8((uint16_t)(wDecimalChars_ADDR + i), 0u);
	}
}
/* <<< factory GetDamageNumberChars */

/* >>> factory CardPageSwitch_PokemonAttack2Page2 */
/* core.asm:3823-3825 */
CardPageExistsResult CardPageSwitch_PokemonAttack2Page2(void)
{
	uint16_t hl = (uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u);
	return CheckCardPageExists(&hl);
}
/* <<< factory CardPageSwitch_PokemonAttack2Page2 */

/* >>> factory LoadPlayAreaCardGfx */
/* core.asm:3916-3923 */
void LoadPlayAreaCardGfx(uint8_t a, uint16_t de)
{
	if (a == 0xFFu)
		return;
	(void)LoadCardDataToBuffer1_FromDeckIndex(a);
	LoadLoaded1CardGfx(de);
}
/* <<< factory LoadPlayAreaCardGfx */

/* >>> factory SetBGP6OrSGB3ToCardPalette */
/* core.asm:3955-3963 */
void SetBGP6OrSGB3ToCardPalette(void)
{
	uint8_t console = gb_read8(wConsole_ADDR);

	if (console == CONSOLE_DMG)
		return;
	if (console == CONSOLE_SGB) {
		SetSGB3ToCardPalette();
		return;
	}
	CopyCGBCardPalette(0x06u);
}
/* <<< factory SetBGP6OrSGB3ToCardPalette */


/* >>> factory SetOneLineSeparation */
/* core.asm:4777-4779 */
uint8_t SetOneLineSeparation(void)
{
	SetLineSeparation(0u);
	return 0u;
}
/* <<< factory SetOneLineSeparation */

/* >>> factory _HasAlivePokemonInPlayArea */
/* core.asm:4670-4711 */
HasAlivePokemonInPlayAreaResult _HasAlivePokemonInPlayArea(uint8_t a)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t slots = (uint8_t)(count - a + 1u);
	uint8_t alive = 0u;
	wExcludeArenaPokemon = a;
	wPlayAreaScreenLoaded = 0u;
	wPlayAreaSelectAction = 0u;
	for (uint8_t slot = a; slots != 0u; slot++, slots--) {
		if (GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + slot)).a != 0u)
			alive++;
	}
	return (HasAlivePokemonInPlayAreaResult){alive, alive == 0u ? FLAG_C : 0u};
}
/* <<< factory _HasAlivePokemonInPlayArea */


/* >>> factory PrintPlayAreaCardLocation */
/* core.asm:5285-5328 */
void PrintPlayAreaCardLocation(void)
{
	uint8_t index = (uint8_t)(wCurPlayAreaSlot << 2);
	uint8_t offset = (hWhoseTurn == PLAYER_TURN) ? 0u : 0x0au;
	uint8_t y = wCurPlayAreaY;
	uint8_t i;

	for (i = 0u; i < 3u; ++i) {
		uint8_t tile = kPlayAreaLocationTileNumbers[index + i];
		WriteByteToBGMap0((uint8_t)(tile + offset), 1u, (uint8_t)(y + i));
	}
}
/* <<< factory PrintPlayAreaCardLocation */

/* >>> factory CheckPrintPoisoned */
/* core.asm:5010-5021 */
uint8_t CheckPrintPoisoned(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t status = a;
	if ((status & POISONED) != 0u)
		a = SYM_POISONED;
	WriteByteToBGMap0(a, b, c);
	return status;
}
/* <<< factory CheckPrintPoisoned */

/* >>> factory ResetDoFrameFunction_Bank1 */
void ResetDoFrameFunction_Bank1(void)
{
	gb_write8(wDoFrameFunction_ADDR, 0u);
	gb_write8((uint16_t)(wDoFrameFunction_ADDR + 1u), 0u);
}
/* <<< factory ResetDoFrameFunction_Bank1 */

/* >>> factory OppAction_NoAction */
/* core.asm:6791 */
void OppAction_NoAction(void)
{
}
/* <<< factory OppAction_NoAction */


/* >>> factory ReturnRetreatCostCardsToArena */
/* core.asm:5788-5809 */
ReturnRetreatCostCardsToArenaResult ReturnRetreatCostCardsToArena(
	uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t ignored_hl)
{
	uint16_t hl = hTempRetreatCostCards_ADDR;
	(void)ignored_hl;

	for (;;) {
		uint8_t card = gb_read8(hl++);
		if (card == 0xFFu)
			return (ReturnRetreatCostCardsToArenaResult){0xFFu, 0xC0u,
				b, c, d, e, hl};
		MoveDiscardResult moved = MoveDiscardPileCardToHand(card);
		AddCardToHand(moved.a);
		e = PLAY_AREA_ARENA;
		(void)PutHandCardInPlayArea(moved.a, e);
	}
}
/* <<< factory ReturnRetreatCostCardsToArena */

/* >>> factory FindHighestBenchScore */
FindHighestBenchScoreResult FindHighestBenchScore(void)
{
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t best = 0u;
	uint8_t location = 0u;
	for (uint8_t slot = 0u; slot < count.a; slot++) {
		uint8_t value = gb_read8((uint16_t)(wPlayAreaAIScore_ADDR + slot));
		if (value >= best) {
			best = value;
			location = slot;
		}
	}
	hTempPlayAreaLocation_ff9d = location;
	return (FindHighestBenchScoreResult){location, location == 0u ? 0x80u : 0u};
}
/* <<< factory FindHighestBenchScore */

/* >>> factory AIEncourage */
AIEncourageResult AIEncourage(uint8_t a)
{
	uint8_t score = wAIScore;
	uint16_t sum = (uint16_t)a + score;
	uint8_t result = (uint8_t)sum;
	wAIScore = sum > 0xFFu ? 0xFFu : result;
	return (AIEncourageResult){wAIScore, (uint8_t)((((a & 0x0Fu) + (score & 0x0Fu)) > 0x0Fu ? 0x20u : 0u) | (sum > 0xFFu ? 0x10u : 0u) | (result == 0u ? 0x80u : 0u))};
}
/* <<< factory AIEncourage */
/* >>> factory ReturnWrongAction */
/* core.asm:3004-3005 */
uint8_t ReturnWrongAction(uint8_t f)
{
	return (uint8_t)((f & 0x80u) | 0x10u);
}
/* <<< factory ReturnWrongAction */

/* >>> factory HandleFailedToContinueDuel */
/* core.asm:23-30 */
uint8_t HandleFailedToContinueDuel(uint16_t hl)
{
	(void)DrawWideTextBox_WaitForInput(hl);
	ResetSerial();
	return (uint8_t)(0x80u | 0x10u);
}
/* <<< factory HandleFailedToContinueDuel */
/* >>> factory Func_6ba2 */
/* core.asm:6818-6824 */
void Func_6ba2(uint16_t hl)
{
	(void)DrawWideTextBox_PrintText(hl);
	if (wDuelistType != DUELIST_TYPE_LINK_OPP)
		(void)WaitForWideTextBoxInput();
}
/* <<< factory Func_6ba2 */

/* >>> factory IsLoadedCard1BasicPokemon */
/* core.asm:2048-2081 */
IsLoadedCard1BasicPokemonResult IsLoadedCard1BasicPokemon(void)
{
	uint8_t id = wLoadedCard1ID;
	if (id == 0xCCu || id == 0xCBu)
		return (IsLoadedCard1BasicPokemonResult){1u, 0u};
	if (wLoadedCard1Type >= 0x08u || wLoadedCard1Stage != 0u)
		return (IsLoadedCard1BasicPokemonResult){0u, 0x90u};
	return (IsLoadedCard1BasicPokemonResult){1u, 0x80u};
}
/* <<< factory IsLoadedCard1BasicPokemon */

/* >>> factory PracticeDuel_PlayGoldeen */
PracticeDuelPlayGoldeenResult PracticeDuel_PlayGoldeen(void)
{
	if (wLoadedCard1ID == 0x53u)
		return (PracticeDuelPlayGoldeenResult){0xC0u};
	PrintPracticeDuelDrMasonInstructions(0x01A5u);
	return (PracticeDuelPlayGoldeenResult){0x10u};
}
/* <<< factory PracticeDuel_PlayGoldeen */

/* >>> factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */
/* core.asm:?? */
TwoByteNumberToTxSymbolPadResult TwoByteNumberToTxSymbol_PadSpace_Bank1(
	uint8_t entry_b, uint8_t entry_c, uint8_t entry_d, uint8_t entry_e,
	uint16_t hl)
{
	uint16_t value = hl;
	uint16_t places[] = {10000u, 1000u, 100u, 10u, 1u};
	uint8_t digits[5];
	uint8_t last_a = SYM_0;
	uint8_t f = 0u;

	for (uint8_t i = 0; i < 5u; i++) {
		uint8_t digit = 0u;
		while (value >= places[i]) {
			value = (uint16_t)(value - places[i]);
			digit++;
		}
		digits[i] = (uint8_t)(SYM_0 + digit);
		last_a = digits[i];
	}
	for (uint8_t i = 0; i < 5u; i++)
		gb_write8((uint16_t)(wStringBuffer_ADDR + i), digits[i]);
	gb_write8((uint16_t)(wStringBuffer_ADDR + 5u), 0u);

	uint8_t trim_b = 4u;
	uint16_t out_hl = (uint16_t)(wStringBuffer_ADDR + 4u);
	for (uint8_t i = 0; i < 4u; i++) {
		if (gb_read8((uint16_t)(wStringBuffer_ADDR + i)) != SYM_0) {
			last_a = gb_read8((uint16_t)(wStringBuffer_ADDR + i));
			f = 0x40u;
			trim_b = (uint8_t)(4u - i);
			out_hl = (uint16_t)(wStringBuffer_ADDR + i);
			break;
		}
		gb_write8((uint16_t)(wStringBuffer_ADDR + i), SYM_SPACE);
		trim_b = (uint8_t)(3u - i);
		if (i == 3u)
			f = 0xC0u;
	}
	(void)entry_d;
	(void)entry_e;
	return (TwoByteNumberToTxSymbolPadResult){last_a, f, trim_b, 0xFFu,
		(uint8_t)(wStringBuffer_ADDR >> 8),
		(uint8_t)(wStringBuffer_ADDR + 5u), out_hl};
}
/* <<< factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */


/* >>> factory DrawWideTextBox_WaitForInput_Bank1 */
WaitResult DrawWideTextBox_WaitForInput_Bank1(uint16_t hl)
{
	return DrawWideTextBox_WaitForInput(hl);
}
/* <<< factory DrawWideTextBox_WaitForInput_Bank1 */


/* >>> factory CardPageSwitch_EnergyOrTrainerPage1 */
/* core.asm:3845-3848 */
CardPageSwitchEnergyResult CardPageSwitch_EnergyOrTrainerPage1(void)
{
	return (CardPageSwitchEnergyResult){1u, 0u};
}
/* <<< factory CardPageSwitch_EnergyOrTrainerPage1 */


/* >>> factory CardPageSwitch_TrainerEnd */
/* core.asm:3869-3872 */
CardPageResult CardPageSwitch_TrainerEnd(void)
{
	return (CardPageResult){CARDPAGE_TRAINER_1, TRUE};
}
/* <<< factory CardPageSwitch_TrainerEnd */

/* >>> factory CheckIfEnoughEnergiesOfType */
CheckIfEnoughEnergiesResult CheckIfEnoughEnergiesOfType(uint8_t a, uint16_t hl)
{
	uint8_t required = (uint8_t)(a & 0x0Fu);
	uint8_t accumulated = gb_read8(wAttachedEnergiesAccum_ADDR);
	gb_write8(wAttachedEnergiesAccum_ADDR, (uint8_t)(accumulated + required));
	uint8_t attached = gb_read8(hl);
	uint16_t next = (uint16_t)(hl + 1u);
	if (required == 0u || required <= attached)
		return (CheckIfEnoughEnergiesResult){required,
			(uint8_t)(required == 0u ? 0x80u : 0x00u), next};
	return (CheckIfEnoughEnergiesResult){required, 0x10u, next};
}
/* <<< factory CheckIfEnoughEnergiesOfType */

/* >>> factory CheckIfActiveCardParalyzedOrAsleep */
CheckIfActiveStatusResult CheckIfActiveCardParalyzedOrAsleep(void)
{
	DuelistVarResult status = GetTurnDuelistVariable(0xF0u);
	uint8_t masked = (uint8_t)(status.a & 0x0Fu);
	if (masked == 0x03u)
		return (CheckIfActiveStatusResult){masked, 0x90u, 0x0025u};
	if (masked == 0x02u)
		return (CheckIfActiveStatusResult){masked, 0x90u, 0x0024u};
	return (CheckIfActiveStatusResult){masked,
		(uint8_t)(masked == 0u ? 0x80u : 0x00u), status.hl};
}
/* <<< factory CheckIfActiveCardParalyzedOrAsleep */

/* >>> factory GetAttacksEnergyCostBits */
static uint8_t get_energy_cost_bits(uint16_t hl)
{
	uint8_t c = 0;
	uint8_t b = gb_read8(hl++);
	if (b & 0xf0u)
		c |= FIRE_F;
	if (b & 0x0fu)
		c |= GRASS_F;
	b = gb_read8(hl++);
	if (b & 0xf0u)
		c |= LIGHTNING_F;
	if (b & 0x0fu)
		c |= WATER_F;
	b = gb_read8(hl++);
	if (b & 0xf0u)
		c |= FIGHTING_F;
	if (b & 0x0fu)
		c |= PSYCHIC_F;
	if (gb_read8(hl) & 0xf0u)
		c = 0xffu;
	return c;
}

EnergyCostBitsResult GetAttacksEnergyCostBits(uint8_t a)
{
	(void)LoadCardDataToBuffer2_FromDeckIndex(a);
	return (EnergyCostBitsResult){
		(uint8_t)(get_energy_cost_bits(wLoadedCard2Atk1EnergyCost_ADDR) |
			  get_energy_cost_bits(wLoadedCard2Atk2EnergyCost_ADDR)),
	};
}
/* <<< factory GetAttacksEnergyCostBits */

/* >>> factory CheckForEvolutionInList */
CheckForEvolutionInListResult CheckForEvolutionInList(uint8_t a, uint8_t f)
{
	uint8_t target = a;
	DuelistVarResult arena_var = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t original = arena_var.a;
	uint16_t arena = arena_var.hl;
	gb_write8(arena, target);
	uint16_t scan = wDuelTempList_ADDR;
	for (;;) {
		uint8_t candidate = gb_read8(scan++);
		if (candidate == 0xffu) {
			uint8_t f = original == 0u ? 0x80u : 0u;
			gb_write8(arena, original);
			return (CheckForEvolutionInListResult){original, target, 0u, 0u,
				f, arena};
		}
		EvolveResult check = CheckIfCanEvolveInto(candidate, PLAY_AREA_ARENA);
		if (check.f & 0x10u)
			continue;
		gb_write8(arena, original);
		return (CheckForEvolutionInListResult){candidate, target, candidate,
			PLAY_AREA_ARENA, (uint8_t)((f & FLAG_Z) | FLAG_C), arena};
	}
}
/* <<< factory CheckForEvolutionInList */

/* >>> factory CountNumberOfEnergyCardsAttached */
CountNumberOfEnergyCardsAttachedResult CountNumberOfEnergyCardsAttached(uint8_t e)
{
	GetPlayAreaCardAttachedEnergies(e);
	uint8_t total = wTotalAttachedEnergies;
	if (total == 0u)
		return (CountNumberOfEnergyCardsAttachedResult){0u, 0x80u};
	uint8_t count = 0u;
	for (uint8_t i = 0u; i < 6u; i++)
		count = (uint8_t)(count + gb_read8((uint16_t)(wAttachedEnergies_ADDR + i)));
	uint8_t colorless = gb_read8((uint16_t)(wAttachedEnergies_ADDR + 6u));
	count = (uint8_t)(count + (colorless >> 1));
	return (CountNumberOfEnergyCardsAttachedResult){count,
		(uint8_t)(count == 0u ? 0x80u : 0u)};
}
/* <<< factory CountNumberOfEnergyCardsAttached */

/* >>> factory LookForCardIDInLocation_Bank5 */
LookForCardIDInLocationResult LookForCardIDInLocation_Bank5(
	uint8_t location, uint8_t card_id)
{
	uint8_t index = 0u;
	uint16_t hl = 0u;
	for (;;) {
		DuelistVarResult locations = GetTurnDuelistVariable(index);
		hl = locations.hl;
		if (locations.a == location &&
		    (uint8_t)GetCardIDFromDeckIndex(index) == card_id)
			return (LookForCardIDInLocationResult){index, location, card_id, 0u,
				index, 0x90u, hl};
		index++;
		if (index == DECK_SIZE)
			return (LookForCardIDInLocationResult){DECK_SIZE, location, card_id,
				0u, DECK_SIZE, 0x00u, hl};
	}
}
/* <<< factory LookForCardIDInLocation_Bank5 */


/* >>> factory LoadDefendingPokemonColorWRAndPrizeCards */
void LoadDefendingPokemonColorWRAndPrizeCards(void)
{
	SwapTurn();
	wAIPlayerColor = TranslateColorToWR(GetArenaCardColor());
	wAIPlayerWeakness = GetArenaCardWeakness();
	wAIPlayerResistance = GetArenaCardResistance();
	wAIPlayerPrizeCount = CountPrizes();
	SwapTurn();
	wAIOpponentPrizeCount = CountPrizes();
}
/* <<< factory LoadDefendingPokemonColorWRAndPrizeCards */


/* >>> factory CheckIfEnergyIsUseful */
CheckIfEnergyIsUsefulResult CheckIfEnergyIsUseful(uint8_t a)
{
	uint8_t energy = (uint8_t)GetCardIDFromDeckIndex(a);
	if (energy == DOUBLE_COLORLESS_ENERGY || wTempCardType == TYPE_ENERGY_DOUBLE_COLORLESS)
		return (CheckIfEnergyIsUsefulResult){0x90u};
	uint8_t required = 0u;
	if (wTempCardID == EXEGGCUTE || wTempCardID == EXEGGUTOR ||
	    wTempCardID == PSYDUCK || wTempCardID == GOLDUCK)
		required = PSYCHIC_ENERGY;
	else if (wTempCardID == SURFING_PIKACHU_LV13 ||
	         wTempCardID == SURFING_PIKACHU_ALT_LV13)
		required = WATER_ENERGY;
	if (required != 0u && energy == required)
		return (CheckIfEnergyIsUsefulResult){0x90u};
	if (wTempCardID == EEVEE &&
	    (energy == WATER_ENERGY || energy == FIRE_ENERGY || energy == LIGHTNING_ENERGY))
		return (CheckIfEnergyIsUsefulResult){0x90u};
	return (CheckIfEnergyIsUsefulResult){GetCardType(energy) == wTempCardType ? 0x90u : 0u};
}
/* <<< factory CheckIfEnergyIsUseful */


/* >>> factory PickRandomBenchPokemon */
uint8_t PickRandomBenchPokemon(void)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	return (uint8_t)(Random((uint8_t)(count - 1u)) + 1u);
}
/* <<< factory PickRandomBenchPokemon */


/* >>> factory PracticeDuel_VerifyPlayerTurnActions */
/* core.asm:2701-2712 */
PracticeDuelTurnActionsResult PracticeDuel_VerifyPlayerTurnActions(void)
{
	uint8_t turn = (uint8_t)(wDuelTurns >> 1);
	uint8_t card = gb_read8(wTempCardID_ccc2_ADDR);
	uint8_t attack = gb_read8(wSelectedAttack_ADDR);
	EnergiesResult energy;
	uint8_t ok;
	switch (turn) {
	case 0: ok = card == 0x53u; break;
	case 1:
		energy = GetPlayAreaCardAttachedEnergies(0);
		ok = card == 0x54u && attack == 1u &&
		     gb_read8((uint16_t)(wAttachedEnergies_ADDR + 5u));
		break;
	case 2:
		energy = GetPlayAreaCardAttachedEnergies(1);
		ok = card == 0x54u && gb_read8((uint16_t)(wAttachedEnergies_ADDR + 2u));
		break;
	case 3:
		energy = GetPlayAreaCardAttachedEnergies(2);
		ok = wPlayerNumberOfPokemonInPlayArea == 3u &&
		     gb_read8((uint16_t)(wAttachedEnergies_ADDR + 2u)) &&
		     card == 0x54u && attack == 1u;
		break;
	case 4:
		energy = GetPlayAreaCardAttachedEnergies(0);
		ok = gb_read8((uint16_t)(wAttachedEnergies_ADDR + 2u)) == 2u && card == 0x55u;
		break;
	case 5:
		energy = GetPlayAreaCardAttachedEnergies(0);
		ok = gb_read8((uint16_t)(wAttachedEnergies_ADDR + 2u)) == 3u &&
		     wPlayerArenaCardHP == 40u && card == 0x55u;
		break;
	default: ok = card == 0x56u && attack == 1u; break;
	}
	return (PracticeDuelTurnActionsResult){ok ? 0xC0u : 0x10u};
}
/* <<< factory PracticeDuel_VerifyPlayerTurnActions */

/* >>> factory PrintCardNameFromCardIDInTextBox */
void PrintCardNameFromCardIDInTextBox(uint16_t hl)
{
	uint8_t card_id = wTempNonTurnDuelistCardID;
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	(void)DrawWideTextBox_PrintText(hl);
}
/* <<< factory PrintCardNameFromCardIDInTextBox */

/* >>> factory RemoveCardIDInList */
RemoveCardIDResult RemoveCardIDInList(uint16_t *hl, uint8_t e)
{
	uint16_t scan = *hl;
	for (;;) {
		uint8_t index = gb_read8(scan++);
		if (index == 0xFFu)
			return (RemoveCardIDResult){index, 0x00u};
		hTempCardIndex_ff98 = index;
		if ((uint8_t)GetCardIDFromDeckIndex(index) != e)
			continue;
		uint16_t dst = (uint16_t)(scan - 1u);
		uint16_t src = scan;
		for (;;) {
			uint8_t value = gb_read8(src++);
			gb_write8(dst++, value);
			if (value == 0xFFu)
				break;
		}
		*hl = scan;
		return (RemoveCardIDResult){index, 0x10u};
	}
}
/* <<< factory RemoveCardIDInList */

/* >>> factory SortTempHandByIDList */
SortTempHandResult SortTempHandByIDList(void)
{
	uint16_t priority = (uint16_t)(gb_read8(wAICardListPlayFromHandPriority_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wAICardListPlayFromHandPriority_ADDR + 1u)) << 8));
	if (gb_read8((uint16_t)(wAICardListPlayFromHandPriority_ADDR + 1u)) == 0u)
		return (SortTempHandResult){0u, 0x80u, 0u, 0u,
			0u, gb_read8(wAICardListPlayFromHandPriority_ADDR), 0u};
	uint16_t list_id = priority;
	uint8_t c = 0u;
	uint16_t hl = 0u;
	uint8_t b = 0u;
	for (;;) {
		b = gb_read8(list_id);
		if (b == 0u)
			return (SortTempHandResult){0u, 0x80u,
				(uint8_t)gb_read8((uint16_t)(list_id - 1u)), c,
				(uint8_t)(list_id >> 8), (uint8_t)list_id, hl};
		list_id++;
		hl = wDuelTempList_ADDR;
		for (;;) {
			uint8_t entry = gb_read8(hl);
			hTempCardIndex_ff98 = entry;
			if (entry == 0xFFu)
				break;
			if ((uint8_t)GetCardIDFromDeckIndex(entry) == b) {
				uint16_t slot = (uint16_t)(wDuelTempList_ADDR + c);
				uint8_t old = gb_read8(slot);
				gb_write8(slot, entry);
				gb_write8(hl, old);
				c++;
			}
			hl++;
		}
	}
}
/* <<< factory SortTempHandByIDList */


/* >>> factory ApplyCardCGBAttributes */
void ApplyCardCGBAttributes(uint16_t de)
{
	hBankVRAM = 1u;
	gb_write8(0xFF4Fu, 1u);
	FillRectangle(0x80u, 8u, 6u, de, 0u);
	hBankVRAM = 0u;
	gb_write8(0xFF4Fu, 0u);
}
/* <<< factory ApplyCardCGBAttributes */


/* >>> factory ApplyStatusConditionToArenaPokemon */
/* core.asm:7237-7253 */
uint8_t ApplyStatusConditionToArenaPokemon(uint16_t *hl, uint8_t d, uint8_t *e)
{
	uint16_t p = *hl;
	uint16_t de = (uint16_t)(d << 8 | DUELVARS_ARENA_CARD_STATUS);
	uint8_t a = (uint8_t)((gb_read8(de) & gb_read8(p)) | gb_read8((uint16_t)(p + 1u)));
	gb_write8(de, a);
	de = (uint16_t)(d << 8 | DUELVARS_ARENA_CARD_LAST_TURN_STATUS);
	a = (uint8_t)((gb_read8(de) & gb_read8(p)) | gb_read8((uint16_t)(p + 1u)));
	gb_write8(de, a);
	*hl = (uint16_t)(p + 2u);
	*e = DUELVARS_ARENA_CARD_LAST_TURN_STATUS;
	return a;
}
/* <<< factory ApplyStatusConditionToArenaPokemon */

/* >>> factory CheckIfEnoughEnergiesToRetreat */
EnoughRetreatEnergiesResult CheckIfEnoughEnergiesToRetreat(void)
{
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t required = GetPlayAreaCardRetreatCost();
	wEnergyCardsRequiredToRetreat = required;
	uint8_t attached = wTotalAttachedEnergies;
	if (attached < required)
		return (EnoughRetreatEnergiesResult){attached, 0x10u};
	wNumRetreatEnergiesSelected = attached;
	wEnergyCardsRequiredToRetreat = required;
	return (EnoughRetreatEnergiesResult){required,
		(uint8_t)(required == 0u ? 0x80u : 0u)};
}
/* <<< factory CheckIfEnoughEnergiesToRetreat */

/* >>> factory DecideLinkDuelVariables */
uint8_t DecideLinkDuelVariables(void)
{
	(void)Func_0e8e();
	(void)DrawWideTextBox_PrintText(0x0052u);
	EnableLCD();
	for (;;) {
		DoFrame();
		uint8_t keys = hKeysPressed;
		if (keys & PAD_B) {
			ResetSerial();
			return 0x90u;
		}
		Func0cc5Result ready = Func_0cc5(keys & PAD_START, 0u, 0u, 0u);
		if (ready.f & 0x10u) {
			uint16_t page = wSerialOp == 0x29u ?
				wPlayerDuelVariables_ADDR : wOpponentDuelVariables_ADDR;
			(void)page;
			return 0x00u;
		}
	}
}
/* <<< factory DecideLinkDuelVariables */

/* >>> factory DisplayAttackPage */
void DisplayAttackPage(void)
{
	switch (wAttackPageNumber) {
	case 0u:
	case 2u:
		SwitchAttackPage();
		break;
	case 1u:
		if (gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u)) ||
		    gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 3u)))
			SwitchAttackPage();
		break;
	case 3u:
		if (gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u)) ||
		    gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 3u)))
			SwitchAttackPage();
		break;
	default:
		break;
	}
}
/* >>> factory DisplayCardPage */
void DisplayCardPage(void)
{
	EnableLCD();
}
/* <<< factory DisplayCardPage */

/* >>> factory DoPracticeDuelAction */
uint8_t DoPracticeDuelAction(uint8_t a)
{
	wPracticeDuelAction = a;
	if (wIsPracticeDuel == 0u)
		return 0x80u;
	switch (a) {
	case 2u:
		return PracticeDuel_PlayGoldeen().f;
	case 6u:
		return PracticeDuel_VerifyPlayerTurnActions().f;
	default:
		return 0x00u;
	}
}
/* <<< factory DoPracticeDuelAction */

/* >>> factory DrawDuelHorizontalSeparator */
void DrawDuelHorizontalSeparator(void)
{
	for (uint8_t x = 0u; x < 9u; x++)
		WriteByteToBGMap0(0x37u, x, 4u);
	WriteByteToBGMap0(0x31u, 9u, 4u);
	WriteByteToBGMap0(0x32u, 10u, 4u);
	WriteByteToBGMap0(0x33u, 9u, 5u);
	WriteByteToBGMap0(0x34u, 10u, 5u);
	WriteByteToBGMap0(0x33u, 9u, 6u);
	WriteByteToBGMap0(0x34u, 10u, 6u);
	WriteByteToBGMap0(0x35u, 0u, 7u);
	WriteByteToBGMap0(0x36u, 1u, 7u);
	for (uint8_t x = 2u; x < 11u; x++)
		WriteByteToBGMap0(0x37u, x, 7u);
	if (wConsole == CONSOLE_CGB) {
		hBankVRAM = 1u;
		gb_write8(0xFF4Fu, 1u);
		for (uint8_t y = 4u; y <= 7u; y++)
			for (uint8_t x = 0u; x < 11u; x++)
				gb_write8((uint16_t)(0x9800u + (uint16_t)y * 32u + x), 0x02u);
		hBankVRAM = 0u;
		gb_write8(0xFF4Fu, 0u);
	}
}
/* <<< factory DrawDuelHorizontalSeparator */

/* >>> factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile */
void MoveAllTurnHolderKnockedOutPokemonToDiscardPile(void)
{
	uint8_t count = GetTurnDuelistVariable(
		DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint16_t hp = (uint16_t)(((uint16_t)hWhoseTurn << 8) |
		DUELVARS_ARENA_CARD_HP);
	for (uint8_t location = PLAY_AREA_ARENA; count != 0u;
	     count--, location++, hp++) {
		if (gb_read8(hp) == 0u)
			(void)MovePlayAreaCardToDiscardPile(location);
	}
}
/* <<< factory MoveAllTurnHolderKnockedOutPokemonToDiscardPile */

/* >>> factory PrintSortNumberInCardList_CallFromPointer */
void PrintSortNumberInCardList_CallFromPointer(void)
{
	PrintSortNumberInCardList();
}
/* <<< factory PrintSortNumberInCardList_CallFromPointer */
/* >>> factory PracticeDuel_VerifyInitialPlay */
/* core.asm:2664-2678 */
PracticeDuelInitialPlayResult PracticeDuel_VerifyInitialPlay(void)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	return (PracticeDuelInitialPlayResult){count == 2u ? 0xC0u : 0x10u};
}
/* <<< factory PracticeDuel_VerifyInitialPlay */

/* >>> factory CheckIfNoSurplusEnergyForAttack */
/* ai/core.asm:2158-2250 */
CheckIfNoSurplusEnergyResult CheckIfNoSurplusEnergyForAttack(void)
{
	uint8_t d = GetTurnDuelistVariable((uint8_t)(hTempPlayAreaLocation_ff9d + DUELVARS_ARENA_CARD)).a;
	uint8_t e = wSelectedAttack;
	CopyAttackDataAndDamage_FromDeckIndex(d, e);

	uint8_t n0 = gb_read8(wLoadedAttackName_ADDR);
	uint8_t n1 = gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1u));
	if ((uint8_t)(n0 | n1) == 0u)
		return (CheckIfNoSurplusEnergyResult){0u, 0x90u};
	if (wLoadedAttackCategory == POKEMON_POWER)
		return (CheckIfNoSurplusEnergyResult){POKEMON_POWER, 0x90u};

	GetPlayAreaCardAttachedEnergies(hTempPlayAreaLocation_ff9d);
	HandleEnergyBurn();
	wTempLoadedAttackEnergyCost = 0u;
	wTempLoadedAttackEnergyNeededAmount = 0u;
	wTempLoadedAttackEnergyNeededType = 0u;

	uint16_t hl = wAttachedEnergies_ADDR;
	uint16_t de = wLoadedAttackEnergyCost_ADDR;
	uint8_t b = 0u;
	for (uint8_t c = (NUM_TYPES / 2u) - 1u; c != 0u; c--) {
		uint8_t v = gb_read8(de);
		CalculateParticularAttachedEnergyNeededResult r =
			CalculateParticularAttachedEnergyNeeded((uint8_t)((v << 4) | (v >> 4)), b, hl);
		b = r.b;
		hl = r.hl;
		v = gb_read8(de);
		r = CalculateParticularAttachedEnergyNeeded(v, b, hl);
		b = r.b;
		hl = r.hl;
		de++;
	}

	b = (uint8_t)((gb_read8(de) >> 4) & 0x0Fu);
	uint8_t a1 = (uint8_t)(wTotalAttachedEnergies - wTempLoadedAttackEnergyCost);
	uint8_t a2 = (uint8_t)(a1 - b);
	uint8_t f = (uint8_t)(0x40u
		| (a2 == 0u ? 0x80u : 0u)
		| (((a1 & 0x0Fu) < (b & 0x0Fu)) ? 0x20u : 0u)
		| ((a1 < b) ? 0x10u : 0u));
	if (a1 < b)
		return (CheckIfNoSurplusEnergyResult){a2, f};
	if (a2 != 0u)
		return (CheckIfNoSurplusEnergyResult){a2, f};
	return (CheckIfNoSurplusEnergyResult){0u, 0x90u};
}
/* <<< factory CheckIfNoSurplusEnergyForAttack */

/* >>> factory Func_1585b */
/* core.asm:1238-1280. hl = $00-terminated list of 3-byte entries
 * (type, card ID, energy count). Entries whose first byte is not 1 are
 * skipped whole. For type-1 entries the card ID is looked up in the play
 * area starting at PLAY_AREA_BENCH_1; if found and the number of energy
 * cards attached is >= the entry's third byte, return that play area
 * position with carry set (Z from the `cp`, N/H cleared by `scf`).
 * Falling off the end of the list returns a = 0 with `or a` flags. */
Func1585bResult Func_1585b(uint16_t hl)
{
	for (;;) {
		uint8_t a = gb_read8(hl);
		hl = (uint16_t)(hl + 1);
		if (a == 0)
			return (Func1585bResult){ .a = 0, .f = 0x80u };
		if (a != 1) {
			hl = (uint16_t)(hl + 2);
			continue;
		}
		uint8_t id = gb_read8(hl);
		hl = (uint16_t)(hl + 1);
		LookResult lr = LookForCardIDInPlayArea_Bank5(id, PLAY_AREA_BENCH_1);
		if (!(lr.f & 0x10u)) {
			hl = (uint16_t)(hl + 1);
			continue;
		}
		uint8_t e = lr.a;
		uint8_t count = CountNumberOfEnergyCardsAttached(e).a;
		uint8_t needed = gb_read8(hl);
		if (count >= needed)
			return (Func1585bResult){ .a = e,
				.f = (uint8_t)((count == needed ? 0x80u : 0x00u) | 0x10u) };
		hl = (uint16_t)(hl + 1);
	}
}
/* <<< factory Func_1585b */

/* >>> factory CheckIfNotABossDeckID */
/* core.asm:2444-2464. Reads sReceivedLegendaryCards under its own
 * EnableSRAM/DisableSRAM pair; a nonzero value short-circuits to the
 * no-carry exit. Otherwise CheckIfOpponentHasBossDeckID decides: it
 * returning carry means "boss deck" and falls into the no-carry exit,
 * carry clear takes `scf`. Only a and carry are contractual -- the Z bit
 * on the scf path comes from inside the callee and is not modelled. */
CheckIfNotABossDeckIDResult CheckIfNotABossDeckID(void)
{
	EnableSRAM();
	uint8_t a = gb_read8(sReceivedLegendaryCards_ADDR);
	DisableSRAM();
	if (a != 0)
		return (CheckIfNotABossDeckIDResult){ .a = a, .carry = 0 };
	CheckIfOpponentHasBossDeckIDResult r = CheckIfOpponentHasBossDeckID(a);
	if (r.carry)
		return (CheckIfNotABossDeckIDResult){ .a = r.a, .carry = 0 };
	return (CheckIfNotABossDeckIDResult){ .a = r.a, .carry = 1 };
}
/* <<< factory CheckIfNotABossDeckID */

/* >>> factory AIChooseRandomlyNotToDoAction */
/* core.asm:2466-2522. Boss decks always use Trainer cards: CheckIfNotABossDeckID
 * returning carry clear exits immediately (never skip the action); its `or a`
 * exit on a nonzero deck ID leaves f = 0, modeled as such on that path.
 * Otherwise the opponent deck ID is compared against the six 50% decks; the
 * exit carry is the result of `cp 1` or `cp 2` on Random(4)'s output, so the
 * full Z/N/H/C byte is reconstructed. hl/de are pushed/popped around the whole
 * body and Random preserves bc, so b/c/d/e/hl all survive. */
AIChooseRandomlyNotToDoActionResult AIChooseRandomlyNotToDoAction(void)
{
	CheckIfNotABossDeckIDResult boss = CheckIfNotABossDeckID();
	if (!boss.carry)
		return (AIChooseRandomlyNotToDoActionResult){boss.a, 0x00u};

	uint8_t deck = wOpponentDeckID;
	uint8_t n = 0x01u; /* carry 25 percent */
	if (deck == MUSCLES_FOR_BRAINS_DECK_ID ||
	    deck == BLISTERING_POKEMON_DECK_ID ||
	    deck == WATERFRONT_POKEMON_DECK_ID ||
	    deck == BOOM_BOOM_SELFDESTRUCT_DECK_ID ||
	    deck == KALEIDOSCOPE_DECK_ID ||
	    deck == RESHUFFLE_DECK_ID)
		n = 0x02u; /* carry 50 percent */

	uint8_t r = Random(0x04u);
	uint8_t cpflags = 0x40u; /* cp leaves N set, low nibble clear */
	if (r == n)
		cpflags |= 0x80u;
	if ((r & 0x0fu) < (n & 0x0fu))
		cpflags |= 0x20u;
	if (r < n)
		cpflags |= 0x10u;
	return (AIChooseRandomlyNotToDoActionResult){r, cpflags};
}
/* <<< factory AIChooseRandomlyNotToDoAction */

/* >>> factory TrySetUpBossStartingPlayArea */
/* core.asm:1165-1200 (helper .PlayPokemonCardInOrder at 1201-1228, see above). The
 * `ld a,d / or a / jr z .set_carry` null check tests the high byte of the constant
 * field address and is therefore never taken (a = 0xcd at the CreateHandCardList
 * call, faithfully passed through). After picking the arena card, loops the bench
 * priority list until a card is missing (carry) or the play area reaches 3 cards.
 * .done recomputes flags with `or a` (Z iff a==0, C clear); the arena path returns
 * the helper's Z|C flags directly via `ret c`. b is never written by this routine or
 * its ported callees; c/d/e/hl are clobbered residue and are not part of the exit
 * contract. */
TrySetUpBossStartingPlayAreaResult TrySetUpBossStartingPlayArea(void)
{
	uint16_t de = wAICardListArenaPriority_ADDR;
	uint8_t a = (uint8_t)(de >> 8);
	if (a == 0x00u)
		return (TrySetUpBossStartingPlayAreaResult){a, 0x90u};
	(void)CreateHandCardList(a);
	uint16_t hl = wDuelTempList_ADDR;
	de = wAICardListArenaPriority_ADDR;
	PlayInOrderResult r = play_pokemon_card_in_order(&hl, de);
	if ((r.f & 0x10u) != 0x00u)
		return (TrySetUpBossStartingPlayAreaResult){r.a, r.f};
	for (;;) {
		de = wAICardListBenchPriority_ADDR;
		r = play_pokemon_card_in_order(&hl, de);
		if ((r.f & 0x10u) != 0x00u)
			break;
		if (r.a < 0x03u)
			continue;
		break;
	}
	return (TrySetUpBossStartingPlayAreaResult){r.a, (uint8_t)((r.a == 0x00u) ? 0x80u : 0x00u)};
}
/* <<< factory TrySetUpBossStartingPlayArea */

/* >>> factory CardPageSwitch_TrainerPage2 */
/* core.asm:3852-3856 */
TrainerPageResult CardPageSwitch_TrainerPage2(void)
{
	uint16_t hl = (uint16_t)(wLoadedCard1NonPokemonDescription_ADDR + 2u);
	CardPageExistsResult r = CheckCardPageExists(&hl);
	return (TrainerPageResult){hl, r.a, r.zero};
}
/* <<< factory CardPageSwitch_TrainerPage2 */

/* >>> factory LoadAndValidateDuelSaveData */
/* core.asm:6063-6084. */
uint8_t LoadAndValidateDuelSaveData(void)
{
	ValidateSavedDuelDataResult duel = ValidateSavedDuelDataFromHL(sCurrentDuel_ADDR);
	if (duel.f & 0x10u)
		return duel.f;

	LoadSavedDuelDataFromDE(sCurrentDuel_ADDR);

	uint8_t general_f = ValidateGeneralSaveData().f;
	if (!(general_f & 0x10u))
		return general_f;

	LoadGeneralSaveData();
	return 0x00u;
}
/* <<< factory LoadAndValidateDuelSaveData */

/* >>> factory ValidateSavedNonLinkDuelData */
/* core.asm:6130-6147. */
uint8_t ValidateSavedNonLinkDuelData(void)
{
	EnableSRAM();
	uint8_t duel_type = gb_read8(sCurrentDuelType_ADDR);
	DisableSRAM();

	if (duel_type != DUELTYPE_LINK)
		return ValidateSavedDuelDataFromHL(sCurrentDuel_ADDR).f;

	return 0x10u;
}
/* <<< factory ValidateSavedNonLinkDuelData */

/* >>> factory SetupPlayAreaScreen */
/* core.asm:5174-5196 */
void SetupPlayAreaScreen(void)
{
	wExcludeArenaPokemon = 0u;
	if (wDuelDisplayedScreen == PLAY_AREA_CARD_LIST)
		return;
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelCheckPokemonScreenTiles();
}
/* <<< factory SetupPlayAreaScreen */

/* >>> factory CheckIfEnoughEnergiesForGivenAttack */
CheckIfEnoughEnergiesForGivenAttackResult CheckIfEnoughEnergiesForGivenAttack(uint8_t d, uint8_t e)
{
	CheckIfEnoughEnergiesForGivenAttackResult r = {0, 0, d, e, d, e, 0};
	(void)LoadCardDataToBuffer1_FromDeckIndex(d);
	uint16_t cost = (e == 0u) ? wLoadedCard1Atk1EnergyCost_ADDR : wLoadedCard1Atk2EnergyCost_ADDR;
	uint16_t hl = (uint16_t)(cost + (0x10u - 0x0cu));
	uint8_t name = (uint8_t)(gb_read8(hl) | gb_read8((uint16_t)(hl + 1u)));
	r.a = name;
	r.hl = (uint16_t)(hl + 1u);
	if (name == 0u) {
		r.f = 0x80u;
		return r;
	}
	hl = (uint16_t)(cost + (0x17u - 0x0cu));
	uint8_t category = gb_read8(hl);
	r.a = category;
	r.hl = hl;
	if (category == 0x04u) {
		r.f = 0xc0u;
		return r;
	}
	gb_write8(wAttachedEnergiesAccum_ADDR, 0u);
	hl = wAttachedEnergies_ADDR;
	uint8_t count = 3u;
	while (count != 0u) {
		CheckIfEnoughEnergiesResult check = CheckIfEnoughEnergiesOfType(
			(uint8_t)(gb_read8(cost) >> 4), hl);
		r.a = check.a;
		r.f = check.f;
		r.hl = check.hl;
		hl = check.hl;
		if ((check.f & 0x10u) != 0u)
			return r;
		check = CheckIfEnoughEnergiesOfType(gb_read8(cost), hl);
		r.a = check.a;
		r.f = check.f;
		r.hl = check.hl;
		hl = check.hl;
		if ((check.f & 0x10u) != 0u)
			return r;
		cost = (uint16_t)(cost + 1u);
		count--;
	}
	uint8_t required_colorless = (uint8_t)((gb_read8(cost) >> 4) & 0x0fu);
	r.b = required_colorless;
	uint8_t accumulated = gb_read8(wAttachedEnergiesAccum_ADDR);
	r.c = accumulated;
	uint8_t remaining = (uint8_t)(gb_read8(wTotalAttachedEnergies_ADDR) - accumulated);
	r.a = remaining;
	if (remaining < required_colorless) {
		r.f = 0x10u;
		return r;
	}
	r.f = (remaining == 0u) ? 0x80u : 0x00u;
	return r;
}
/* <<< factory CheckIfEnoughEnergiesForGivenAttack */

/* >>> factory SaveDuelData */
void SaveDuelData(void)
{
	StubbedUnusedSaveDataValidation();
	SaveDuelDataToDE(sCurrentDuel_ADDR);
}
/* <<< factory SaveDuelData */

/* >>> factory SetCardListHeaderText */
void SetCardListHeaderText(uint16_t de, uint16_t hl)
{
	wCardListHeaderText = (uint8_t)de;
	wCardListHeaderText_PTR[1] = (uint8_t)(de >> 8);
	SetCardListInfoBoxText(hl);
}
/* <<< factory SetCardListHeaderText */
