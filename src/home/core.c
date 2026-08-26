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

#include "home/core.h"
#include "generated/hram.h"
#define OPPACTION_PLAY_ENERGY 0x03u

#include "home/text_box.h"
#include "home/empty_screen.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "home/menus.h"

#include "home/core.h"
#define DOUBLE_POISONED 0xC0u

#include "home/core.h"
#define LetsPlayTheGamePracticeDuelText 0x01d8u

#include "home/text_box.h"
#include "home/empty_screen.h"

#include "generated/wram.h"
#include "mem.h"
#define SECOND_ATTACK 0x01u
#define STARMIE 0x56u

#include "generated/hram.h"
#define ChooseTheCardYouWishToExamineText 0x0056u
#define OpponentsDiscardPileText 0x0218u
#define YourDiscardPileText 0x0217u

#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define AttachedEnergyToPokemonText 0x005fu

#include "home/core.h"
#include "home/menus.h"
#include "home/sound.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define SFX_POKEMON_EVOLUTION 0x5eu
#define PokemonEvolvedIntoPokemonText 0x0060u

#include "generated/wram.h"
#include "home/empty_screen.h"
#include "home/lcd.h"
#include "home/tiles.h"
#include "home/duel_core.h"
#include "home/process_text.h"

#include "generated/wram.h"
#include "home/duel.h"
#define STARYU 0x55u
#define WATER 0x03u

#include "generated/wram.h"
#include "mem.h"
#include "home/duel.h"
#define PLAY_AREA_BENCH_2 0x02u
#define SEAKING 0x54u

#include "generated/wram.h"
#include "home/duel.h"
#include "home/duel_core_state.h"

#define DUELTYPE_PRACTICE 0x80u
#define DUELVARS_HAND 0x42u
#define DUELVARS_DECK_CARDS 0x7Eu

#include "home/empty_screen.h"
#include "home/bg_map.h"
#include "home/core.h"
#include "generated/wram.h"

#include "home/core.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/print_text.h"
#include "mem.h"

#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xbau
#define CardsText 0x007eu
#define NoneText 0x007cu
#define PrizesLeftActivePokemonCardsInDeckText 0x007bu
#define YesText 0x007du

#include "home/core.h"
#include "home/empty_screen.h"
#include "home/bg_map.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/print_text.h"
#include "mem.h"

#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#define TYPE_ENERGY_F 0x03u
#define TYPE_TRAINER_F 0x04u

#include "home/core.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/core.h"
#include "generated/hram.h"

#include "home/menus.h"
#include "home/serial.h"
#define ReturnCardsToDeckAndDrawAgainText 0x006cu

#include "home/duel.h"
#include "home/core.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#include "home/core.h"
#include "home/play_animation.h"
#include "home/frames.h"
#include "home/script.h"
#include "generated/hram.h"
#define DUEL_ANIM_OPP_DRAW 0x57u
#define DUEL_ANIM_PLAYER_DRAW 0x56u

#include "home/core.h"
#include "home/tiles.h"
#include "generated/wram.h"
#define PROMOSTAR 0xffu
#define DUEL_OTHER_GFX 0x4008u
#define CardRarityTextIDs_ADDR 0x5e14u

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"

#include "home/duel.h"
#include "home/random.h"
#include "generated/wram.h"
#define DUELVARS_PRIZES 0xecu

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define DUELVARS_BENCH 0xbcu
#define PLAY_AREA_BENCH_5 0x05u

#define CONFUSED 0x01u
#define NO_STATUS 0x00u
#define SYM_ASLEEP 0x09u
#define SYM_CONFUSED 0x0au
#define SYM_PARALYZED 0x0bu

#include "home/core.h"
#include "home/load_animation.h"
#include "mem.h"
#define SPRITE_ANIM_FLAG_X_INVERTED_MASK 0x01u
#define SPRITE_ANIM_FLAG_Y_INVERTED_MASK 0x02u
#define SPRITE_ANIM_FLAG_X_FLIP_MASK 0x20u
#define SPRITE_ANIM_FLAG_Y_FLIP_MASK 0x40u

#include "home/core.h"
#include "home/menus.h"
#include "home/empty_screen.h"
#include "home/process_text.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"
#define UsedText 0x0033u

#include "home/core.h"
#include "home/duel.h"
#include "mem.h"

#include "home/core.h"
#include "generated/wram.h"
#include "mem.h"
#define GOLDEEN 0x53u

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "mem.h"
#define PSYCHIC 0x05u

#include "home/core.h"
#include "home/lcd.h"
#include "generated/wram.h"
#include "mem.h"
#define PracticeDuelText_SamTurn4 0x5346u

#include "home/core.h"
#include "home/tiles.h"
#include "home/menus.h"
#include "home/empty_screen.h"
#include "home/serial.h"
#include "mem.h"
#define BOXMSG_OPPONENTS_TURN 0x01u
#define BOXMSG_PLAYERS_TURN 0x00u
#define DuelistTurnText 0x005eu

#include "home/duel.h"
#include "home/core.h"
#include "home/load_animation.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "generated/wram.h"
#define SCREEN_WIDTH 20u

#include "home/core.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#include "home/core.h"
#include "home/sprite_animations.h"
#include "home/load_animation.h"
#include "generated/wram.h"
#include "mem.h"
#define SPRITE_ANIM_COORD_X 0x02u
#define SPRITE_ANIM_COORD_Y 0x03u
#define SPRITE_ANIM_FLAG_UNSKIPPABLE_F 0x07u
#define SPRITE_ANIM_FLAG_UNSKIPPABLE (1u << SPRITE_ANIM_FLAG_UNSKIPPABLE_F)
#define SPRITE_DUEL_DAMAGE 0x2Eu

#include "home/core.h"
#include "mem.h"

#include "home/core.h"
#include "home/script.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"
#define SELECT_COMPUTER_OPPONENT_DATA_ADDR_580 0x7408u

#include "home/core.h"
#include "generated/hram.h"
#include "mem.h"
#define PLAY_AREA_BENCH_1_730 0x01u
#define SelectStaryuPracticeDuelText 0x01D7u

#include "home/core.h"
#include "generated/wram.h"
#include "mem.h"
#define SPRITE_ANIM_89_850 0x59u

#include "home/core.h"
#include "generated/wram.h"
#include "mem.h"
#define SPRITE_ANIM_91 0x5Bu

#include "home/core.h"
#include "generated/wram.h"
#include "mem.h"
#define SPRITE_ANIM_90 0x5Au

#include "home/core.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/core.h"
#include "home/energy.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#include "home/core.h"
#include "home/substatus.h"
#include "home/duel.h"
#include "home/card_data.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"
#define TYPE_TRAINER 0x10u
#define EnergyCardsRequiredToRetreatText 0x00BFu
#define UnableToRetreatText 0x003Du

#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u

#include "home/core.h"
#include "home/frames.h"
#include "home/empty_screen.h"
#include "home/tiles.h"
#include "home/process_text.h"
#include "home/menus.h"
#include "home/lcd.h"
#include "home/script.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define NUM_DECK_IDS 0x35u
#define B_PAD_B 1u
#define B_PAD_RIGHT 4u
#define B_PAD_LEFT 5u
#define B_PAD_UP 6u
#define B_PAD_DOWN 7u

#include "home/core.h"
#include "home/common.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define COLORLESS 0x06u

#include "home/core.h"
#include "home/print_text.h"
#include "home/process_text.h"

#include "home/core.h"
#include "home/print_text.h"
#include "home/bg_map.h"
#include "generated/wram.h"
#include "mem.h"
#define CARD_DATA_ATTACK1_CATEGORY 0x17u
#define CARD_DATA_ATTACK1_ENERGY_COST 0x0Cu
#define DAMAGE_MINUS 0x02u
#define DAMAGE_PLUS 0x01u
#define DAMAGE_X 0x03u
#define RESIDUAL 0x80u
#define SYM_ATK_DESCR 0x0Eu
#define SYM_PLUS_OFFSET 0x2Au
#define PKMNPWRText 0x000Au

#include "home/core.h"

#define DUELVARS_ARENA_CARD_ATTACHED_DEFENDER 0xdau
#define DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER 0xe0u
#define DUELVARS_ARENA_CARD_STAGE 0xceu
#define SYM_Lv 0x11u
#define SYM_PLUSPOWER 0x14u
#define SYM_DEFENDER 0x15u

static const uint8_t kFaceDownCardTileNumbers[8] = {
	0xd0u, 0x02u, /* basic */
	0xd4u, 0x02u, /* stage 1 */
	0xd8u, 0x01u, /* stage 2 */
	0xdcu, 0x01u, /* stage 2 special */
};

#define FeetText 0x0215u
#define InchesText 0x0216u

#include "home/core.h"
#include "home/play_animation.h"
#include "home/frames.h"
#include "home/duel.h"
#include "home/print_text.h"
#include "home/menus.h"
#include "home/empty_screen.h"
#include "home/lcd.h"
#include "home/script.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define DECK_SIZE_490 0x3Cu
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK_490 0xBAu
#define DUEL_ANIM_OPP_SHUFFLE_490 0x52u
#define DUEL_ANIM_PLAYER_SHUFFLE_490 0x51u
#define PLAYER_TURN_490 0xC2u
#define SHUFFLE_DECK_490 0x09u
#define FLAG_C_490 0x10u
#define DeckHasXCardsText 0x0068u
#define ShufflesTheDeckText 0x0063u

#include "home/core.h"
#include "home/duel.h"
#include "home/print_text.h"
#include "home/bg_map.h"
#include "home/empty_screen.h"
#include "generated/wram.h"
#define KnockOutText 0x004eu
#define SYM_E 0x0Bu
#define SYM_HP 0x0Cu

#include "home/duel.h"
#include "home/core.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/empty_screen.h"
#include "home/tiles.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define hTempPlayAreaLocation_ff9d_ADDR 0xFF9Du

#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/menus.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/list.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define wDuelDisplayedScreen_ADDR 0xCAC2u
#define wDuelTempList_ADDR 0xC510u
#define wExcludeArenaPokemon_ADDR 0xCBD2u
#define wNumPlayAreaItems_ADDR 0xCBC8u

#include "home/core.h"
#include "home/duel.h"
#include "home/serial.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define EFFECTCMDTYPE_BEFORE_DAMAGE 0x03u
#define WillUseThePokemonPowerText 0x005Cu
#define hTempCardIndex_ff9f_ADDR 0xFF9Fu
#define hTemp_ffa0_ADDR 0xFFA0u
#define wLoadedAttackName_ADDR 0xCCAAu
#define wSkipDuelistIsThinkingDelay_ADDR 0xCBF9u
#define wTxRam2_b_ADDR 0xCE41u

#include "home/core.h"
#include "home/empty_screen.h"
#include "home/lcd.h"
#include "home/tiles.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/lcd.h"
#include "generated/wram.h"

#include "home/palettes.h"
#include "home/sgb.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "home/substatus.h"
#define EFFECTCMDTYPE_INITIAL_EFFECT_1 0x01u

#include "generated/wram.h"
#include "home/effect_commands.h"
#define EFFECTCMDTYPE_AFTER_DAMAGE 0x04u

#include "generated/wram.h"
#include "home/duel_core.h"
#include "home/effect_commands.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/card_data.h"
#include "generated/hram.h"
#define V0_TILES1 0x8800u

#include "home/trainer_cards.h"

#include "generated/hram.h"
#include "home/core.h"
#define PAD_SELECT 0x04u
#define PAD_CTRL_PAD 0xF0u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "home/substatus.h"
#define ATTACK_FLAG2_ADDRESS 0x08u
#define IGNORE_THIS_ATTACK_F 0x05u

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"
#define HAS_EVOLUTION 0x01u

#include "generated/wram.h"
#include "home/legendary_articuno.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/sgb.h"

#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/credits_sequence_commands.h"
#include "home/duel_core.h"
#include "home/tiles.h"
#define HEADER_ENERGY 0x01u
#define HEADER_POKEMON 0x02u
#define HEADER_TRAINER 0x00u
#define LARGE_CARD_PICTURE 0x08u
#define LARGE_CARD_TILE_DATA 0x5EB7u

#include "generated/wram.h"
#include "home/core.h"
#include "home/text_box.h"

#include "generated/wram.h"
#include "home/card_color.h"
#include "home/print_text.h"

#include "home/empty_screen.h"
#include "home/menus.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "home/process_text.h"
#include "home/bg_map.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define TX_END 0x00u
#define TX_SYMBOL 0x05u
#define SYM_POKEMON 0x0Du
#define SYM_PRIZE 0x30u
#define TILEMAP_WIDTH 32u

#include "mem.h"
#include "generated/hram.h"
#include "home/core.h"
#include "home/duel.h"
#define DUELIST_TYPE_PLAYER 0x00u
#define DUELVARS_DUELIST_TYPE 0xF1u

#include "generated/wram.h"
#include "home/core.h"
#include "home/text_box.h"
#include "home/credits_sequence_commands.h"
#include "home/tiles.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/duel.h"
#include "home/text_box.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "home/menus.h"
#include "home/print_text.h"
#define DuelistHandText 0x00a7u
#define CARD_LIST_PARAMETERS 0x5710u

#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/credits_sequence_commands.h"
#include "home/tiles.h"
#include "home/bg_map.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define DUEL_MAIN_SCENE 0x01u

#include "generated/wram.h"
#include "home/core.h"
#define PleaseSelectHandText 0x00AAu

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"

#include "home/core.h"
#include "generated/wram.h"
#define SELECT_CHECK 0x02u

#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/process_text.h"
#include "home/print_text.h"
#define TheCardYouReceivedText 0x0170u
#define YouReceivedTheseCardsText 0x0171u

#include "generated/wram.h"
#include "home/core.h"
#include "home/duel_core.h"
#include "home/menus.h"
#define FinishedTurnWithoutAttackingText 0x005du

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/core.h"
#include "home/duel.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/text_box.h"
#include "home/lcd.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "home/menus.h"
#include "home/print_text.h"
#define NoBasicPokemonCardListParameters 0x4e37u

#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define CARD_DATA_ATTACK1_NAME 0x10u

#include "generated/wram.h"
#include "home/core.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/core.h"
#include "home/menus.h"
#include "home/text_box.h"
#include "home/lcd.h"
#include "home/duel.h"
#define ChooseEnergyCardToDiscardText 0x0050u
#define EnergyDiscardCardListParameters 0x46f3u

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/core.h"
#define ATTACKPAGE_ATTACK1_1 0x00u
#define ATTACKPAGE_ATTACK2_1 0x02u
#define PAD_RIGHT 0x10u
#define PAD_LEFT 0x20u

#include "mem.h"
#include "generated/wram.h"
#include "home/frames.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/bg_map.h"
#include "home/core.h"
#define SYM_SLASH 0x2Eu

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/duel.h"

#include "mem.h"

#include "generated/sram.h"
#include "home/switch_sram.h"
#include "home/core.h"
#define FollowMyGuidancePracticeDuelText 0x01dau

#include "home/core.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "mem.h"

#include "home/core.h"
#include "home/frames.h"
#include "home/credits_sequence_commands.h"
#include "home/lcd.h"
#include "home/script.h"
#include "home/tiles.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/duel.h"

#include "generated/hram.h"
#include "home/core.h"

#include "home/core.h"
#include "home/menus.h"
#define ThereAreNoBasicPokemonInHand 0x006au

#define PAD_UP 0x40u
#define PAD_DOWN 0x80u
#include "generated/wram.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/frames.h"
#include "home/menus.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define PLAY_CHECK 0x01u
#define PlayCheck1Text 0x0084u
#define PlayCheck2Text 0x0085u
#define SelectCheckText 0x0086u

#include "home/core.h"
#include "generated/hram.h"
#define YouDrewText 0x0070u

#include "home/duel.h"
#include "home/card_data.h"
#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define PokemonPowerSelectNotRequiredText 0x0040u
#define UseThisPokemonPowerText 0x003fu
#include "home/effect_commands.h"

#include "generated/wram.h"
#include "home/core.h"
#include "home/menus.h"
#include "home/card_color.h"
#include "home/print_text.h"
#include "home/tiles.h"
#include "home/bg_map.h"
#include "mem.h"
#define CARDPAGETYPE_NOT_PLAY_AREA 0x00u
#define CARDPAGETYPE_PLAY_AREA 0x01u
#define SYM_COLORLESS 0x0Au
#define CARD_PAGE_RETREAT_WR_TEXT_DATA 0x4000u
#define CARD_PAGE_LV_HP_NO_TEXT_TILE_DATA 0x4004u
#define CARD_PAGE_NO_TEXT_TILE_DATA 0x400Cu

#include "generated/wram.h"
#include "home/core.h"
#include "home/text_box.h"
#include "home/tiles.h"
#include "home/print_text.h"

/* HEADER_ENERGY is defined in the existing core statics. */

/* 01:52c5 PracticeDuelTextPointerTable (poketcg/poketcg.sym). `ld hl,
 * PracticeDuelTextPointerTable` resolves in the routine's own bank, which is
 * bank $01 for every callsite, so the pointer pair is read from there. */
#define PRACTICE_DUEL_TEXT_POINTER_TABLE_BANK 0x01u
#define PRACTICE_DUEL_TEXT_POINTER_TABLE_ADDR 0x52C5u

#define NeedPracticeAgainPracticeDuelText 0x01d9u

#include "home/core.h"
#include "home/sgb.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
#include "home/bg_map.h"
#include "home/duel.h"
#include "home/empty_screen.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/play_animation.h"
#include "home/print_text.h"
#include "home/process_text.h"
#include "home/random.h"
#include "home/script.h"
#include "home/serial.h"
#include "home/sound.h"
#include "home/text_box.h"
#include "home/tiles.h"

#define COIN_TOSS_7847 0x06u
#define DUELIST_TYPE_PLAYER_7847 0x00u
#define DUELTYPE_LINK_7847 0x01u
#define DUELVARS_DUELIST_TYPE_7847 0xF1u
#define DUEL_ANIM_COIN_SPIN_7847 0x58u
#define DUEL_ANIM_COIN_TOSS_GOING_HEADS_7847 0x59u
#define DUEL_ANIM_COIN_TOSS_GOING_TAILS_7847 0x5Au
#define DUEL_ANIM_COIN_TAILS_7847 0x5Bu
#define DUEL_ANIM_COIN_HEADS_7847 0x5Cu
#define SFX_COIN_TOSS_HEADS_7847 0x54u
#define SFX_COIN_TOSS_TAILS_7847 0x55u
#define HEADS_7847 0x01u
#define TAILS_7847 0x00u
#define SYM_SLASH_7847 0x2Eu
#define TILE_CROSS_7847 0x34u
#define TILE_CIRCLE_7847 0x30u
#define FLAG_C_7847 0x10u
#define FLAG_Z_7847 0x80u

/* core.asm:8046-8054 (_TossCoin.CheckTransmissionError). The ROM's error
 * branch never pops the `push af` it entered with: DuelTransmissionError
 * reloads sp from wDuelReturnAddress and returns into the outer duel loop, so
 * that unbalanced frame is never observed from here. */
static void TossCoin_CheckTransmissionError(void)
{
	if (wSerialFlags == 0u)
		return;
	FinishQueuedAnimations();
	DuelTransmissionError();
}

/* core.asm:8041-8045 (_TossCoin.wait_serial_byte_recv): one frame at a time
 * until the link partner's byte has arrived; returns that byte. */
static uint8_t TossCoin_WaitSerialByteRecv(void)
{
	SerialByteResult recv;
	do {
		DoFrame();
		recv = SerialRecvByte();
	} while (recv.f & FLAG_C_7847);
	TossCoin_CheckTransmissionError();
	return recv.a;
}

/* core.asm:7999-8006 (_TossCoin.SendSerialByte): stash the byte in hff96 and,
 * in a link duel only, hand it to the serial ring. */
static void TossCoin_SendSerialByte(uint8_t a)
{
	hff96 = a;
	if (wDuelType != DUELTYPE_LINK_7847)
		return;
	(void)SerialSendByte(hff96);
	TossCoin_CheckTransmissionError();
}

/* core.asm:8008-8022 (_TossCoin.GetOpponentCoinResult): an AI opponent waits
 * out the toss animation and keeps the result generated beforehand, a link
 * opponent sends its own result over serial. */
static uint8_t TossCoin_GetOpponentCoinResult(uint8_t a)
{
	hff96 = a;
	if (wDuelType == DUELTYPE_LINK_7847)
		return TossCoin_WaitSerialByteRecv();
	do {
		DoFrame();
	} while (CheckAnyAnimationPlaying().f & FLAG_C_7847);
	return hff96;
}

/* core.asm:8027-8039 (_TossCoin.WaitForOpponent): the AI delays 30 frames, a
 * link opponent announces itself with a serial byte. Both callsites drop the
 * returned hff96, so this reports nothing. */
static void TossCoin_WaitForOpponent(uint8_t a)
{
	uint8_t frames;
	hff96 = a;
	if (wDuelType == DUELTYPE_LINK_7847) {
		(void)TossCoin_WaitSerialByteRecv();
		return;
	}
	frames = 30u;
	do {
		DoFrame();
		frames = (uint8_t)(frames - 1u);
	} while (frames != 0u);
}

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/coin_toss.h"
#define ConfusionCheckRetreatText 0x00f8u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "home/substatus.h"
#include "home/menus.h"
#include "home/serial.h"

#include "home/serial.h"
#include "home/coin_toss.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#define RetreatWasUnsuccessfulText 0x005bu
#define RetreatedToTheBenchText 0x005au

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/commands.h"
#define ATK_ANIM_BIG_HIT 0x02u
#define ATK_ANIM_HIT 0x01u

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/commands.h"
#include "mem.h"
#define ATK_ANIM_CONFUSION 0x7cu
#define ATK_ANIM_OWN_CONFUSION 0x7fu
#define ATK_ANIM_PARALYSIS 0x7du
#define ATK_ANIM_POISON 0x7bu
#define ATK_ANIM_SLEEP 0x7eu

#include "home/core.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "home/core.h"
#include "home/credits_sequence_commands.h"
#include "home/tiles.h"
#include "home/card_data.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"

#include "home/damage_calculation.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/core.h"
#include "home/menus.h"
#define TheDiscardPileHasNoCardsText 0x00a5u

#include "generated/wram.h"
#define NoCardsInHandText 0x00a4u

#define YouCannotSelectThisCardText 0x0071u

#define MR_MIME 0x9Bu

#define DRAW_CARDS 0x07u
#define SHUFFLE_DECK 0x09u
#define CannotDrawCardBecauseNoCardsInDeckText 0x0119u
#define DrawCardsFromTheDeckText 0x0118u

#include "generated/wram.h"
#include "home/core.h"
#include "home/empty_screen.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/play_animation.h"
#include "home/script.h"
#include "home/tiles.h"

#define DUEL_ANIM_BOTH_DRAW 0x55u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#define BASIC 0x00u
#define PlacedOnTheBenchText 0x0061u
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
		return (RemoveCardIDResult){index, 0x90u};
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

/* >>> factory AIAttachEnergyInHandToCardInPlayArea */
AIAttachEnergyInHandToCardInPlayAreaResult AIAttachEnergyInHandToCardInPlayArea(uint8_t d, uint8_t e)
{
	CoreCardListResult hand = LookForCardIDInHandList_Bank5(e);
	if ((hand.f & 0x10u) == 0u)
		return (AIAttachEnergyInHandToCardInPlayAreaResult){hand.a, hand.f};
	uint8_t energy = hand.a;
	LookResult location = LookForCardIDInPlayArea_Bank5(e, PLAY_AREA_ARENA);
	hTempPlayAreaLocation_ffa1 = location.a;
	hTemp_ffa0 = energy;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_PLAY_ENERGY);
	return (AIAttachEnergyInHandToCardInPlayAreaResult){OPPACTION_PLAY_ENERGY, decision.f};
}
/* <<< factory AIAttachEnergyInHandToCardInPlayArea */

/* >>> factory GoToPreviousCardPage */
CardPageNavigationResult GoToPreviousCardPage(void)
{
	uint8_t page = (uint8_t)(wCardPageNumber - 1u);
	wCardPageNumber = page;
	for (;;) {
		CardPageResult r = SwitchCardPage(page);
		if (r.carry) {
			page = r.a;
			wCardPageNumber = page;
			for (;;) {
				r = SwitchCardPage(page);
				if (r.a != 0u)
					return (CardPageNavigationResult){r.a, 0x10u, 0u};
				page = (uint8_t)(page - 1u);
				wCardPageNumber = page;
			}
		}
		if (r.a != 0u)
			return (CardPageNavigationResult){r.a, 0u, 0u};
		page = (uint8_t)(page - 1u);
		wCardPageNumber = page;
	}
}
/* <<< factory GoToPreviousCardPage */

/* >>> factory DrawWholeScreenTextBox */
void DrawWholeScreenTextBox(uint16_t hl)
{
	uint16_t box = hl;
	EmptyScreen();
	DrawRegularTextBox(&box, 0u, 20u, 18u, 0u, 0u);
	InitTextPrintingInTextbox(19u, 1u, 1u);
	(void)SetNoLineSeparation();
	(void)ProcessTextFromID(hl);
	EnableLCD();
	(void)SetOneLineSeparation();
	(void)WaitForWideTextBoxInput();
}
/* <<< factory DrawWholeScreenTextBox */

/* >>> factory HasAlivePokemonInPlayArea */
HasAlivePokemonInPlayAreaResult HasAlivePokemonInPlayArea(void)
{
	return _HasAlivePokemonInPlayArea(0u);
}
/* <<< factory HasAlivePokemonInPlayArea */

/* >>> factory CardPageSwitch_PokemonAttack1Page1 */
CardPageExistsResult CardPageSwitch_PokemonAttack1Page1(void)
{
	uint16_t hl = wLoadedCard1Atk1Name_ADDR;
	return CheckCardPageExists(&hl);
}
/* <<< factory CardPageSwitch_PokemonAttack1Page1 */

/* >>> factory CheckPrintDoublePoisoned */
uint8_t CheckPrintDoublePoisoned(uint8_t a, uint8_t b, uint8_t c)
{
	uint8_t status = a;
	uint8_t printed_status = 0u;
	if ((status & (DOUBLE_POISONED & (POISONED ^ 0xFFu))) != 0u)
		printed_status = POISONED;
	(void)CheckPrintPoisoned(printed_status, b, c);
	return status;
}
/* <<< factory CheckPrintDoublePoisoned */

/* >>> factory PrintPracticeDuelLetsPlayTheGame */
void PrintPracticeDuelLetsPlayTheGame(void)
{
	(void)PrintPracticeDuelDrMasonInstructions(LetsPlayTheGamePracticeDuelText);
}
/* <<< factory PrintPracticeDuelLetsPlayTheGame */

/* >>> factory AIAttachEnergyInHandToCardInBench */
AIAttachEnergyInHandToCardInBenchResult AIAttachEnergyInHandToCardInBench(uint8_t d, uint8_t e)
{
	CoreCardListResult hand = LookForCardIDInHandList_Bank5(e);
	if ((hand.f & 0x10u) == 0u)
		return (AIAttachEnergyInHandToCardInBenchResult){hand.a, hand.f};
	AIAttachEnergyInHandToCardInPlayAreaResult result = AIAttachEnergyInHandToCardInPlayArea(d, e);
	return (AIAttachEnergyInHandToCardInBenchResult){result.a, result.f};
}
/* <<< factory AIAttachEnergyInHandToCardInBench */

/* >>> factory DrawPracticeDuelInstructionsTextBox */
void DrawPracticeDuelInstructionsTextBox(void)
{
	uint16_t box = 0u;
	EmptyScreen();
	DrawRegularTextBox(&box, 0u, 20u, 12u, 0u, 0u);
	PrintPracticeDuelInstructionsTextBoxLabel();
}
/* <<< factory DrawPracticeDuelInstructionsTextBox */

/* >>> factory PracticeDuelVerify_Turn7Or8 */
PracticeDuelVerifyTurn7Or8Result PracticeDuelVerify_Turn7Or8(void)
{
	uint8_t card = gb_read8(wTempCardID_ccc2_ADDR);
	if (card != STARMIE)
		return (PracticeDuelVerifyTurn7Or8Result){0x10u};
	uint8_t attack = gb_read8(wSelectedAttack_ADDR);
	if (attack != SECOND_ATTACK)
		return (PracticeDuelVerifyTurn7Or8Result){0x10u};
	return (PracticeDuelVerifyTurn7Or8Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn7Or8 */

/* >>> factory SetDiscardPileScreenTexts */
void SetDiscardPileScreenTexts(void)
{
	uint16_t de = YourDiscardPileText;
	if (gb_read8(hWhoseTurn_ADDR) != PLAYER_TURN)
		de = OpponentsDiscardPileText;
	SetCardListHeaderText(de, ChooseTheCardYouWishToExamineText);
}
/* <<< factory SetDiscardPileScreenTexts */

/* >>> factory PrintAttachedEnergyToPokemon */
void PrintAttachedEnergyToPokemon(void)
{
	DuelistVarResult target = GetTurnDuelistVariable(
		(uint8_t)(DUELVARS_ARENA_CARD + hTempPlayAreaLocation_ff9d));
	(void)LoadCardNameToTxRam2_b(target.a);
	LoadCardNameToTxRam2(hTempCardIndex_ff98);
	(void)DrawWideTextBox_WaitForInput(AttachedEnergyToPokemonText);
}
/* <<< factory PrintAttachedEnergyToPokemon */

/* >>> factory PrintPokemonEvolvedIntoPokemon */
void PrintPokemonEvolvedIntoPokemon(void)
{
	PlaySFX(SFX_POKEMON_EVOLUTION);
	LoadCardNameToTxRam2(wPreEvolutionPokemonCard);
	(void)LoadCardNameToTxRam2_b(hTempCardIndex_ff98);
	(void)DrawWideTextBox_WaitForInput(PokemonEvolvedIntoPokemonText);
}
/* <<< factory PrintPokemonEvolvedIntoPokemon */

/* >>> factory SetupDuel */
void SetupDuel(void)
{
	wTileMapFill = SYM_SPACE;
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadSymbolsFont();
	SetDefaultConsolePalettes();
	(void)SetupText(0x38u, 0x9Fu);
	EnableLCD();
}
/* <<< factory SetupDuel */

/* >>> factory PracticeDuelVerify_Turn6 */
PracticeDuelVerifyTurn6Result PracticeDuelVerify_Turn6(void)
{
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	if (wAttachedEnergies_PTR[WATER] != 3u)
		return (PracticeDuelVerifyTurn6Result){0x10u};
	if (*wPlayerArenaCardHP_PTR != 40u)
		return (PracticeDuelVerifyTurn6Result){0x10u};
	if (*wTempCardID_ccc2_PTR != STARYU)
		return (PracticeDuelVerifyTurn6Result){0x10u};
	return (PracticeDuelVerifyTurn6Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn6 */

/* >>> factory PracticeDuelVerify_Turn4 */
PracticeDuelVerifyTurn4Result PracticeDuelVerify_Turn4(void)
{
	if (gb_read8(wPlayerNumberOfPokemonInPlayArea_ADDR) != 3u)
		return (PracticeDuelVerifyTurn4Result){ReturnWrongAction(0u)};
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_BENCH_2);
	if (gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER)) == 0u)
		return (PracticeDuelVerifyTurn4Result){ReturnWrongAction(0x80u)};
	if (gb_read8(wTempCardID_ccc2_ADDR) != SEAKING)
		return (PracticeDuelVerifyTurn4Result){ReturnWrongAction(0u)};
	if (gb_read8(wSelectedAttack_ADDR) != SECOND_ATTACK)
		return (PracticeDuelVerifyTurn4Result){ReturnWrongAction(0u)};
	return (PracticeDuelVerifyTurn4Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn4 */

/* >>> factory ShuffleDeckAndDrawSevenCards */
ShuffleDeckAndDrawSevenCardsResult ShuffleDeckAndDrawSevenCards(void)
{
	(void)InitializeDuelVariables();
	if (wDuelType != DUELTYPE_PRACTICE) {
		(void)ShuffleDeck(0u, 0u);
		(void)ShuffleDeck(0u, 0u);
	}
	for (uint8_t i = 0; i < 7u; i++) {
		DrawCardResult draw = DrawCardFromDeck();
		AddCardToHand(draw.a);
	}
	DuelistVarResult hand = GetTurnDuelistVariable(DUELVARS_HAND);
	uint16_t cursor = hand.hl;
	uint8_t any = 0u;
	for (uint8_t i = 0; i < 7u; i++) {
		uint8_t card = gb_read8(cursor++);
		(void)LoadCardDataToBuffer1_FromDeckIndex(card);
		IsLoadedCard1BasicPokemonResult basic = IsLoadedCard1BasicPokemon();
		if (basic.a != 0u)
			any = 1u;
	}
	return any != 0u ? (ShuffleDeckAndDrawSevenCardsResult){1u, 0x00u}
	                : (ShuffleDeckAndDrawSevenCardsResult){0u, 0x90u};
}
/* <<< factory ShuffleDeckAndDrawSevenCards */

/* >>> factory WriteTwoDigitNumberInTxSymbol_PadSpace */
void WriteTwoDigitNumberInTxSymbol_PadSpace(
	uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t number = (uint16_t)a;
	(void)TwoByteNumberToTxSymbol_PadSpace_Bank1(b, c, d, e, number);
	uint16_t dst = BCCoordToBGMap0Address(b, c);
	uint16_t src = (uint16_t)(wStringBuffer_ADDR + 3u);
	SafeCopyDataHLtoDE(&src, &dst, 2u);
	(void)hl;
}
/* <<< factory WriteTwoDigitNumberInTxSymbol_PadSpace */

/* >>> factory PrintOpponentNumberOfHandAndDeckCards */
void PrintOpponentNumberOfHandAndDeckCards(void)
{
	uint8_t hand = (uint8_t)(wOpponentNumberOfCardsInHand + wNumCardsBeingDrawn);
	uint8_t deck = (uint8_t)(DECK_SIZE - wOpponentNumberOfCardsNotInDeck - wNumCardsBeingDrawn);
	WriteTwoDigitNumberInTxSymbol_PadSpace(hand, 5, 3, hand, deck, 0);
	WriteTwoDigitNumberInTxSymbol_PadSpace(deck, 11, 3, hand, deck, 0);
}
/* <<< factory PrintOpponentNumberOfHandAndDeckCards */

/* >>> factory PrintPlayerNumberOfHandAndDeckCards */
void PrintPlayerNumberOfHandAndDeckCards(void)
{
	uint8_t hand = (uint8_t)(wPlayerNumberOfCardsInHand + wNumCardsBeingDrawn);
	uint8_t deck = (uint8_t)(DECK_SIZE - wPlayerNumberOfCardsNotInDeck - wNumCardsBeingDrawn);
	WriteTwoDigitNumberInTxSymbol_PadSpace(hand, 16, 10, hand, deck, wNumCardsBeingDrawn_ADDR);
	WriteTwoDigitNumberInTxSymbol_PadSpace(deck, 10, 10, hand, deck, wNumCardsBeingDrawn_ADDR);
}
/* <<< factory PrintPlayerNumberOfHandAndDeckCards */

/* >>> factory PrintDuelResultStats */
void PrintDuelResultStats(void)
{
	for (uint8_t turn = 0u; turn < 2u; ++turn) {
		uint8_t d = turn == 0u ? 8u : 1u;
		uint8_t e = d;
		(void)SetNoLineSeparation();
		ProcessTextHeaderResult heading = InitTextPrinting_ProcessTextFromID(
			d, e, PrizesLeftActivePokemonCardsInDeckText);
		d = heading.d;
		e = heading.e;
		(void)SetOneLineSeparation();
		uint8_t c = e;
		uint8_t b = (uint8_t)(d + 7u);
		d = (uint8_t)(b + 2u);
		uint8_t prizes = CountPrizes();
		WriteTwoDigitNumberInTxSymbol_PadSpace(
			prizes, b, c, d, e, heading.hl);
		e = (uint8_t)(e + 1u);
		c = (uint8_t)(c + 1u);
		DuelistVarResult pokemon = GetTurnDuelistVariable(
			DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		uint16_t pokemon_text = pokemon.a != 0u ? YesText : NoneText;
		d = (uint8_t)(d - 1u);
		ProcessTextHeaderResult pokemon_result = InitTextPrinting_ProcessTextFromID(
			d, e, pokemon_text);
		d = pokemon_result.d;
		e = pokemon_result.e;
		e = (uint8_t)(e + 1u);
		d = (uint8_t)(d + 1u);
		c = (uint8_t)(c + 1u);
		DuelistVarResult cards_var = GetTurnDuelistVariable(
			DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
		uint8_t cards = (uint8_t)(DECK_SIZE - gb_read8(cards_var.hl));
		WriteTwoDigitNumberInTxSymbol_PadSpace(
			cards, b, c, d, e, cards_var.hl);
		(void)InitTextPrinting_ProcessTextFromID(d, e, CardsText);
		SwapTurn();
	}
}
/* <<< factory PrintDuelResultStats */

/* >>> factory ConvertColorToEnergyCardID */
uint8_t ConvertColorToEnergyCardID(uint8_t a)
{
	static const uint8_t card_id[] = {
		FIRE_ENERGY,
		GRASS_ENERGY,
		LIGHTNING_ENERGY,
		WATER_ENERGY,
		FIGHTING_ENERGY,
		PSYCHIC_ENERGY,
		DOUBLE_COLORLESS_ENERGY,
	};
	uint8_t result = card_id[a];
	(void)Func_14323();
	return result;
}
/* <<< factory ConvertColorToEnergyCardID */

/* >>> factory WriteOneByteNumberInTxSymbol_PadSpace */
void WriteOneByteNumberInTxSymbol_PadSpace(
	uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t number = (uint16_t)a;
	(void)TwoByteNumberToTxSymbol_PadSpace_Bank1(b, c, d, e, number);
	uint16_t dst = BCCoordToBGMap0Address(b, c);
	uint16_t src = (uint16_t)(wStringBuffer_ADDR + 2u);
	SafeCopyDataHLtoDE(&src, &dst, 3u);
	(void)hl;
}
/* <<< factory WriteOneByteNumberInTxSymbol_PadSpace */

/* >>> factory PrintPracticeDuelNumberedInstruction */
PrintPracticeDuelNumberedInstructionResult PrintPracticeDuelNumberedInstruction(uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t c = gb_read8((uint16_t)(hl + 2u));
	uint8_t b = gb_read8((uint16_t)(hl + 3u));
	uint16_t text_id = (uint16_t)(c | ((uint16_t)b << 8));
	hl = (uint16_t)(hl + 4u);
	(void)SetNoLineSeparation();
	(void)InitTextPrinting_ProcessTextFromID(d, e, text_id);
	(void)SetOneLineSeparation();
	return (PrintPracticeDuelNumberedInstructionResult){hl};
}
/* <<< factory PrintPracticeDuelNumberedInstruction */

/* >>> factory PrintNextPracticeDuelInstruction */
void PrintNextPracticeDuelInstruction(void)
{
	gb_write8(hffb0_ADDR, 1u);
	PrintPracticeDuelInstructionsTextBoxLabel();
	uint16_t hl = (uint16_t)(gb_read8(wPracticeDuelTextPointer_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wPracticeDuelTextPointer_ADDR + 1u)) << 8);
	for (;;) {
		uint8_t a = gb_read8(wPracticeDuelTextY_ADDR);
		if (a < gb_read8(hl))
			break;
		uint8_t entry = gb_read8(hl++);
		if (entry == 0u)
			break;
		PrintPracticeDuelNumberedInstructionResult result =
			PrintPracticeDuelNumberedInstruction(1u, entry, hl);
		hl = result.hl;
	}
	gb_write8(hffb0_ADDR, 0u);
}
/* <<< factory PrintNextPracticeDuelInstruction */

/* >>> factory GoToFirstOrNextCardPage */
CardPageNavigationResult GoToFirstOrNextCardPage(void)
{
	uint8_t page = wCardPageNumber;
	if (page == 0u) {
		uint8_t type = wLoadedCard1Type;
		uint8_t initial_page = CARDPAGE_POKEMON_OVERVIEW;
		if ((type & (uint8_t)(1u << TYPE_ENERGY_F)) != 0u)
			initial_page = CARDPAGE_ENERGY;
		else if ((type & (uint8_t)(1u << TYPE_TRAINER_F)) != 0u)
			initial_page = CARDPAGE_TRAINER_1;
		wCardPageNumber = initial_page;
		return (CardPageNavigationResult){initial_page, 0u, type};
	}
	for (;;) {
		uint8_t next_page = (uint8_t)(wCardPageNumber + 1u);
		wCardPageNumber = next_page;
		CardPageResult r = SwitchCardPage(next_page);
		if (r.carry) {
			wCardPageNumber = r.a;
			return (CardPageNavigationResult){r.a, 0x10u, 0u};
		}
		if (r.a != 0u)
			return (CardPageNavigationResult){r.a, 0u, 0u};
	}
}
/* <<< factory GoToFirstOrNextCardPage */

/* >>> factory PrintPracticeDuelInstructions */
void PrintPracticeDuelInstructions(uint16_t hl)
{
	gb_write8(wPracticeDuelTextY_ADDR, 0u);
	gb_write8(wPracticeDuelTextPointer_ADDR, (uint8_t)hl);
	gb_write8((uint16_t)(wPracticeDuelTextPointer_ADDR + 1u), (uint8_t)(hl >> 8));
	for (;;) {
		PrintNextPracticeDuelInstruction();
		uint8_t a = gb_read8(hl++);
		gb_write8(wPracticeDuelTextY_ADDR, a);
		if (a == 0u) {
			PrintPracticeDuelLetsPlayTheGame();
			return;
		}
		uint16_t text_box_label = gb_read8(hl++);
		text_box_label |= (uint16_t)gb_read8(hl++) << 8;
		(void)PrintScrollableText_WithTextBoxLabel(text_box_label, DrMasonText);
		uint16_t text_id = gb_read8(hl++);
		text_id |= (uint16_t)gb_read8(hl++) << 8;
		(void)SetNoLineSeparation();
		uint8_t text_y = gb_read8(wPracticeDuelTextY_ADDR);
		(void)InitTextPrinting_ProcessTextFromID(1u, text_y, text_id);
		(void)SetOneLineSeparation();
	}
}
/* <<< factory PrintPracticeDuelInstructions */

/* >>> factory DisplayPreviousCardPage */
void DisplayPreviousCardPage(void)
{
	CardPageNavigationResult navigation = GoToPreviousCardPage();
	if ((navigation.f & 0x10u) == 0u)
		DisplayCardPage();
}
/* <<< factory DisplayPreviousCardPage */

/* >>> factory PrintNumberOfHandAndDeckCards */
void PrintNumberOfHandAndDeckCards(void)
{
	if (hWhoseTurn != PLAYER_TURN) {
		PrintOpponentNumberOfHandAndDeckCards();
		return;
	}
	PrintPlayerNumberOfHandAndDeckCards();
}
/* <<< factory PrintNumberOfHandAndDeckCards */

/* >>> factory PrintReturnCardsToDeckDrawAgain */
PrintReturnCardsToDeckDrawAgainResult PrintReturnCardsToDeckDrawAgain(void)
{
	(void)DrawWideTextBox_WaitForInput(ReturnCardsToDeckAndDrawAgainText);
	ExchangeRNGResult x = ExchangeRNG(0x12u, 0x11u, 0x1211u, 0xCD12u);
	return (PrintReturnCardsToDeckDrawAgainResult){x.a, x.b, x.c, x.f, x.hl, x.de};
}
/* <<< factory PrintReturnCardsToDeckDrawAgain */

/* >>> factory PracticeDuelVerify_Turn3 */
PracticeDuelVerifyTurn3Result PracticeDuelVerify_Turn3(void)
{
	uint8_t a = wTempCardID_ccc2;
	if (a != SEAKING) {
		uint8_t f = ReturnWrongAction(0x00u);
		return (PracticeDuelVerifyTurn3Result){a, f};
	}
	GetPlayAreaCardAttachedEnergies(PLAY_AREA_BENCH_1);
	uint8_t water = gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER));
	if (water == 0u) {
		uint8_t f = ReturnWrongAction(0x80u);
		return (PracticeDuelVerifyTurn3Result){water, f};
	}
	return (PracticeDuelVerifyTurn3Result){water, 0x00u};
}
/* <<< factory PracticeDuelVerify_Turn3 */

/* >>> factory CheckIfEnoughEnergiesToAttack */
CheckIfEnoughEnergiesToAttackResult CheckIfEnoughEnergiesToAttack(void)
{
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	HandleEnergyBurn();
	uint8_t menu_item = hCurMenuItem;
	uint8_t doubled = (uint8_t)(menu_item * 2u);
	uint16_t addr = (uint16_t)(wDuelTempList_ADDR + doubled);
	uint8_t d = gb_read8(addr);
	uint8_t e = gb_read8((uint16_t)(addr + 1u));
	CheckIfEnoughEnergiesForGivenAttackResult result = CheckIfEnoughEnergiesForGivenAttack(d, e);
	return (CheckIfEnoughEnergiesToAttackResult){result.a, result.f, result.d, result.e};
}
/* <<< factory CheckIfEnoughEnergiesToAttack */

/* >>> factory PlayTurnDuelistDrawAnimation */
PlayTurnDuelistDrawAnimationResult PlayTurnDuelistDrawAnimation(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint16_t hl)
{
	ResetAnimationQueue();
	uint8_t e = (hWhoseTurn == PLAYER_TURN) ? DUEL_ANIM_PLAYER_DRAW : DUEL_ANIM_OPP_DRAW;
	(void)PlayDuelAnimation(e);
	for (;;) {
		DoFrame();
		CheckSkipDelayAllowedResult skip = CheckSkipDelayAllowed(f, b, c, d, e, hl);
		b = skip.b; c = skip.c; d = skip.d; f = skip.f; hl = skip.hl;
		if (f & 0x10u)
			break;
		AnimationStatusResult playing = CheckAnyAnimationPlaying();
		if (!(playing.f & 0x10u))
			break;
	}
	FinishQueuedAnimations();
	return (PlayTurnDuelistDrawAnimationResult){e, f};
}
/* <<< factory PlayTurnDuelistDrawAnimation */

/* >>> factory DrawCardPageSet2AndRarityIcons */
DrawCardPageSet2AndRarityIconsResult DrawCardPageSet2AndRarityIcons(void)
{
	TileCopyResult tiles = LoadCardSet2Tiles(wLoadedCard1Set);
	if (tiles.hl >= DUEL_OTHER_GFX)
		FillRectangle(0xfcu, 2u, 2u, 0x0f08u, 0x0102u);
	uint8_t rarity = wLoadedCard1Rarity;
	if (rarity != PROMOSTAR) {
		ProcessTextHeaderResult result = PrintCardPageRarityIcon(rarity, 18u, 9u, CardRarityTextIDs_ADDR);
		return (DrawCardPageSet2AndRarityIconsResult){result.hl};
	}
	return (DrawCardPageSet2AndRarityIconsResult){CardRarityTextIDs_ADDR};
}
/* <<< factory DrawCardPageSet2AndRarityIcons */

/* >>> factory CountOppEnergyCardsInHandAndAttached */
CountOppEnergyCardsInHandAndAttachedResult CountOppEnergyCardsInHandAndAttached(void)
{
	gb_write8(wTempAI_ADDR, 0u);
	CoreCardListResult listed = CreateEnergyCardListFromHand(0u);
	if (!(listed.f & 0x10u)) {
		uint8_t count = 0u;
		uint16_t p = wDuelTempList_ADDR;
		while (gb_read8(p) != 0xFFu) {
			count++;
			p++;
		}
		gb_write8(wTempAI_ADDR, count);
	}

	DuelistVarResult numInPlay = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t d = numInPlay.a;
	uint8_t e = PLAY_AREA_ARENA;
	uint8_t f = 0u;
	for (;;) {
		CountNumberOfEnergyCardsAttachedResult r = CountNumberOfEnergyCardsAttached(e);
		uint8_t total = gb_read8(wTempAI_ADDR);
		uint16_t sum = (uint16_t)(total + r.a);
		uint8_t carry = (sum > 0xFFu) ? 0x10u : 0u;
		total = (uint8_t)sum;
		gb_write8(wTempAI_ADDR, total);
		e = (uint8_t)(e + 1u);
		d = (uint8_t)(d - 1u);
		f = (uint8_t)(carry | 0x40u | ((d == 0u) ? 0x80u : 0u) | (((d & 0x0Fu) == 0x0Fu) ? 0x20u : 0u));
		if (d == 0u)
			break;
	}
	return (CountOppEnergyCardsInHandAndAttachedResult){gb_read8(wTempAI_ADDR), f, wTempAI_ADDR};
}
/* <<< factory CountOppEnergyCardsInHandAndAttached */

/* >>> factory AIPickPrizeCards */
static void AIPickPrizeCards_PickPrizeCard(void)
{
	DuelistVarResult prizes = GetTurnDuelistVariable(DUELVARS_PRIZES);
	uint16_t hl = prizes.hl;
	uint8_t c = prizes.a;
	static const uint8_t prize_flags[6] = {1u, 2u, 4u, 8u, 16u, 32u};
	uint8_t e;
	for (;;) {
		e = Random(6u);
		if (prize_flags[e] & c)
			break;
	}
	uint8_t bit = prize_flags[e];
	gb_write8(hl, (uint8_t)(gb_read8(hl) & (uint8_t)~bit));

	DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(DUELVARS_PRIZE_CARDS + e));
	AddCardToHand(card.a);
}

void AIPickPrizeCards(void)
{
	uint8_t remaining_picks = wNumberPrizeCardsToTake;
	for (;;) {
		AIPickPrizeCards_PickPrizeCard();
		DuelistVarResult prizes = GetTurnDuelistVariable(DUELVARS_PRIZES);
		if (prizes.a == 0u)
			break;
		remaining_picks--;
		if (remaining_picks == 0u)
			break;
	}
}
/* <<< factory AIPickPrizeCards */

/* >>> factory HandleAIEnergyScoringForRepeatedBenchPokemon */
HandleAIEnergyScoringForRepeatedBenchPokemonResult HandleAIEnergyScoringForRepeatedBenchPokemon(void)
{
	ClearMemory_Bank5(MAX_PLAY_AREA_POKEMON, wSamePokemonEnergyScoreHandled_ADDR);

	uint16_t hl = GetTurnDuelistVariable(DUELVARS_BENCH).hl;
	uint8_t e = 0u;

loop_bench:
	ClearMemory_Bank5(MAX_PLAY_AREA_POKEMON, wSamePokemonEnergyScore_ADDR);

	e++;
	{
		uint8_t deck_index = gb_read8(hl);
		hl++;
		if (deck_index == 0xFFu)
			return (HandleAIEnergyScoringForRepeatedBenchPokemonResult){0xFFu, 0xC0u};
		wSamePokemonCardID = deck_index;
	}

	if (gb_read8((uint16_t)(wSamePokemonEnergyScoreHandled_ADDR + e)) != 0u)
		goto loop_bench;

	wSamePokemonCardID = (uint8_t)GetCardIDFromDeckIndex(wSamePokemonCardID);

	{
		uint16_t saved_hl = hl;
		uint8_t saved_e = e;

		{
			uint8_t dam = GetCardDamageAndMaxHP(e).a;
			uint8_t counters = ConvertHPToDamageCounters_Bank5(dam).a;
			uint8_t energy = CountNumberOfEnergyCardsAttached(e).a;
			gb_write8((uint16_t)(wSamePokemonEnergyScore_ADDR + e),
				(uint8_t)((uint8_t)(energy << 1) + 0x80u - counters));
			gb_write8((uint16_t)(wSamePokemonEnergyScoreHandled_ADDR + e), 0x01u);
		}
		for (;;) {
			e++;
			uint8_t deck_index = gb_read8(hl);
			hl++;
			if (deck_index == 0xFFu)
				break;
			uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
			if (card_id != wSamePokemonCardID)
				continue;
			uint8_t dam = GetCardDamageAndMaxHP(e).a;
			uint8_t counters = ConvertHPToDamageCounters_Bank5(dam).a;
			uint8_t energy = CountNumberOfEnergyCardsAttached(e).a;
			gb_write8((uint16_t)(wSamePokemonEnergyScore_ADDR + e),
				(uint8_t)((uint8_t)(energy << 1) + 0x80u - counters));
			gb_write8((uint16_t)(wSamePokemonEnergyScoreHandled_ADDR + e), 0x01u);
		}

		uint8_t count = 0u;
		for (uint8_t i = 0u; i < MAX_PLAY_AREA_POKEMON; i++)
			if (gb_read8((uint16_t)(wSamePokemonEnergyScore_ADDR + i)) != 0u)
				count++;

		if (count >= 2u) {
			uint8_t highest_score = 0u;
			uint8_t highest_loc = 0u;
			for (uint8_t loc = PLAY_AREA_BENCH_5 + 1u; ; ) {
				loc--;
				if (loc == 0u)
					break;
				uint8_t score = gb_read8((uint16_t)(wSamePokemonEnergyScore_ADDR + loc));
				if (score >= highest_score) {
					highest_score = score;
					highest_loc = loc;
				}
			}
			for (uint8_t b = PLAY_AREA_ARENA; ; b++) {
				uint16_t addr = (uint16_t)(wPlayAreaEnergyAIScore_ADDR + b);
				if (b == highest_loc) {
					gb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));
				} else {
					uint8_t score = gb_read8((uint16_t)(wSamePokemonEnergyScore_ADDR + b));
					if (score != 0u)
						gb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));
				}
				if ((uint8_t)(b + 1u) == MAX_PLAY_AREA_POKEMON)
					break;
			}
		}

		hl = saved_hl;
		e = saved_e;
	}
	goto loop_bench;
}
/* <<< factory HandleAIEnergyScoringForRepeatedBenchPokemon */

/* >>> factory CheckPrintCnfSlpPrz */
void CheckPrintCnfSlpPrz(uint8_t a, uint8_t b, uint8_t c)
{
	static const uint8_t status_symbols[4] = {SYM_SPACE, SYM_CONFUSED, SYM_ASLEEP, SYM_PARALYZED};
	uint8_t status = (uint8_t)(a & CNF_SLP_PRZ);
	WriteByteToBGMap0(status_symbols[status], b, c);
}
/* <<< factory CheckPrintCnfSlpPrz */

/* >>> factory LoadAnimCoordsAndFlags */
void LoadAnimCoordsAndFlags(void)
{
	uint16_t hl = GetSpriteAnimBufferProperty_SpriteInA(gb_read8(0xD423u), 0x01u);
	AnimCoordsResult r = GetAnimCoordsAndFlags();
	uint8_t attr = (uint8_t)((r.a & (SPRITE_ANIM_FLAG_Y_FLIP_MASK | SPRITE_ANIM_FLAG_X_FLIP_MASK)) | gb_read8(hl));
	gb_write8(hl, attr);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, r.b);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, r.c);
	hl = (uint16_t)(hl + 0x0Cu);
	uint8_t flags = (uint8_t)((r.a & (SPRITE_ANIM_FLAG_Y_INVERTED_MASK | SPRITE_ANIM_FLAG_X_INVERTED_MASK)) | gb_read8(hl));
	gb_write8(hl, flags);
}
/* <<< factory LoadAnimCoordsAndFlags */

/* >>> factory PrintUsedTrainerCardDescription */
void PrintUsedTrainerCardDescription(void)
{
	EmptyScreen();
	(void)SetNoLineSeparation();
	InitTextPrinting(1u, 1u);
	uint16_t hl = wLoadedCard1Name_ADDR;
	(void)ProcessTextFromPointerToID(hl);
	InitTextPrintingInTextbox(19u, 1u, 3u);
	hl = wLoadedCard1NonPokemonDescription_ADDR;
	(void)ProcessTextFromPointerToID(hl);
	(void)SetOneLineSeparation();
	hl = UsedText;
	(void)DrawWideTextBox_WaitForInput(hl);
}
/* <<< factory PrintUsedTrainerCardDescription */

/* >>> factory PracticeDuelVerify_Turn5 */
PracticeDuelVerifyTurn5Result PracticeDuelVerify_Turn5(void)
{
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	if (gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER)) != 2u)
		return (PracticeDuelVerifyTurn5Result){ReturnWrongAction(0u)};
	if (gb_read8(wTempCardID_ccc2_ADDR) != STARYU)
		return (PracticeDuelVerifyTurn5Result){ReturnWrongAction(0u)};
	return (PracticeDuelVerifyTurn5Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn5 */

/* >>> factory PracticeDuelVerify_Turn1 */
PracticeDuelVerify_Turn1Result PracticeDuelVerify_Turn1(void)
{
	uint8_t a = wTempCardID_ccc2;
	if (a != GOLDEEN)
		return (PracticeDuelVerify_Turn1Result){ReturnWrongAction(0u)};
	return (PracticeDuelVerify_Turn1Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn1 */

/* >>> factory PracticeDuelVerify_Turn2 */
PracticeDuelVerify_Turn2Result PracticeDuelVerify_Turn2(void)
{
	uint8_t a = wTempCardID_ccc2;
	if (a != SEAKING)
		return (PracticeDuelVerify_Turn2Result){ReturnWrongAction(0u)};
	uint8_t attack = wSelectedAttack;
	if (attack != SECOND_ATTACK)
		return (PracticeDuelVerify_Turn2Result){ReturnWrongAction(0u)};
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	uint8_t psychic = gb_read8((uint16_t)(wAttachedEnergies_ADDR + PSYCHIC));
	if (psychic == 0u)
		return (PracticeDuelVerify_Turn2Result){ReturnWrongAction(0x80u)};
	return (PracticeDuelVerify_Turn2Result){0x00u};
}
/* <<< factory PracticeDuelVerify_Turn2 */

/* >>> factory PracticeDuel_PlayStaryuFromBench */
PracticeDuel_PlayStaryuFromBenchResult PracticeDuel_PlayStaryuFromBench(void)
{
	uint8_t turns = wDuelTurns;
	if (turns != 7u)
		return (PracticeDuel_PlayStaryuFromBenchResult){(uint8_t)(turns == 0u ? 0x80u : 0x00u)};
	DrawPracticeDuelInstructionsTextBox();
	EnableLCD();
	PrintPracticeDuelInstructions(PracticeDuelText_SamTurn4);
	return (PracticeDuel_PlayStaryuFromBenchResult){0x00u};
}
/* <<< factory PracticeDuel_PlayStaryuFromBench */

/* >>> factory DisplayDuelistTurnScreen */
void DisplayDuelistTurnScreen(void)
{
	EmptyScreen();
	uint8_t c = BOXMSG_PLAYERS_TURN;
	uint8_t turn = hWhoseTurn;
	if (turn != PLAYER_TURN)
		c++;
	DrawDuelBoxMessage(c);
	(void)DrawWideTextBox_WaitForInput(DuelistTurnText);
	(void)ExchangeRNG(0u, 0u, 0u, 0u);
}
/* <<< factory DisplayDuelistTurnScreen */

/* >>> factory DrawDuelistPortraitsAndNames */
void DrawDuelistPortraitsAndNames(void)
{
	(void)LoadSymbolsFont();

	uint16_t hl = wDefaultText_ADDR;
	(void)CopyPlayerName(wDefaultText_ADDR);
	InitTextPrinting(0, 11);
	ProcessText(&hl);

	DrawPlayerPortrait();

	hl = wDefaultText_ADDR;
	(void)CopyOpponentName(wDefaultText_ADDR);
	TextLength length = GetTextLengthInTiles(hl);
	InitTextPrinting((uint8_t)(length.a + SCREEN_WIDTH), 0);
	ProcessText(&hl);

	DrawOpponentPortrait(wOpponentPortrait);
	DrawDuelHorizontalSeparator();
}
/* <<< factory DrawDuelistPortraitsAndNames */

/* >>> factory CheckEnergyNeededForAttack */
CheckEnergyNeededForAttackResult CheckEnergyNeededForAttack(void)
{
	DuelistVarResult duelist = GetTurnDuelistVariable((uint8_t)(hTempPlayAreaLocation_ff9d + DUELVARS_ARENA_CARD));
	uint8_t d = duelist.a;
	uint8_t e = wSelectedAttack;
	AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(d, e);
	d = (uint8_t)(copy.de >> 8);
	e = (uint8_t)copy.de;

	uint8_t name0 = gb_read8(wLoadedAttackName_ADDR);
	uint8_t name1 = gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1u));
	uint8_t a = (uint8_t)(name0 | name1);
	uint16_t hl = (uint16_t)(wLoadedAttackName_ADDR + 1u);
	if (a == 0u)
		return (CheckEnergyNeededForAttackResult){0u, 0x90u, 0u, 0u, d, 0u, hl};
	a = wLoadedAttackCategory;
	if (a == POKEMON_POWER)
		return (CheckEnergyNeededForAttackResult){a, 0x90u, 0u, 0u, d, 0u, hl};

	e = hTempPlayAreaLocation_ff9d;
	(void)GetPlayAreaCardAttachedEnergies(e);
	HandleEnergyBurn();

	wTempLoadedAttackEnergyCost = 0u;
	wTempLoadedAttackEnergyNeededAmount = 0u;
	wTempLoadedAttackEnergyNeededType = 0u;

	hl = wAttachedEnergies_ADDR;
	uint16_t de = wLoadedAttackEnergyCost_ADDR;
	uint8_t b = 0u;
	uint8_t c = (NUM_TYPES / 2u) - 1u;
	do {
		uint8_t byte0 = gb_read8(de);
		a = (uint8_t)((byte0 >> 4) | (byte0 << 4));
		CheckIfEnoughParticularAttachedEnergyResult r1 = CheckIfEnoughParticularAttachedEnergy(a, hl, b);
		b = r1.b; hl = r1.hl;
		a = gb_read8(de);
		CheckIfEnoughParticularAttachedEnergyResult r2 = CheckIfEnoughParticularAttachedEnergy(a, hl, b);
		b = r2.b; hl = r2.hl;
		de = (uint16_t)(de + 1u);
		c = (uint8_t)(c - 1u);
	} while (c != 0u);

	uint8_t byte1 = gb_read8(de);
	uint8_t swapped = (uint8_t)((byte1 >> 4) | (byte1 << 4));
	b = (uint8_t)(swapped & 0x0Fu);
	a = wTempLoadedAttackEnergyCost;
	hl = wTempLoadedAttackEnergyNeededAmount_ADDR;
	a = (uint8_t)(a - gb_read8(hl));
	c = a;
	a = wTotalAttachedEnergies;
	uint8_t sub1 = (uint8_t)(a - c);
	uint8_t sub2 = (uint8_t)(sub1 - b);
	a = sub2;
	if (sub1 < b) {
		uint8_t colorless_needed = (uint8_t)((uint8_t)(~a) + 1u);
		uint8_t not_enough_f = (uint8_t)(0x10u | (colorless_needed == 0u ? 0x80u : 0u));
		c = colorless_needed;
		b = wTempLoadedAttackEnergyNeededAmount;
		a = wTempLoadedAttackEnergyNeededType;
		a = ConvertColorToEnergyCardID(a);
		e = a;
		d = 0u;
		return (CheckEnergyNeededForAttackResult){a, not_enough_f, b, c, d, e, hl};
	}

	a = wTempLoadedAttackEnergyNeededAmount;
	if (a == 0u)
		/* The `ret z` "enough energy" exit. Nothing between the .loop above and
		 * this ret touches de, so the real ROM still holds the loop pointer,
		 * wLoadedAttackEnergyCost + 3 = $CCA9 -- NOT the d/e set at entry.
		 * Measured against the reference 2026-08-26; the landed body returned the
		 * stale entry values here, which no existing case observed because they
		 * all leave through the two not-enough exits below. */
		return (CheckEnergyNeededForAttackResult){0u, 0x80u, b, c,
			(uint8_t)(de >> 8), (uint8_t)de, hl};

	uint8_t colorless_needed2 = (uint8_t)((uint8_t)(~(uint8_t)0u) + 1u);
	uint8_t final_f = (uint8_t)(0x10u | (colorless_needed2 == 0u ? 0x80u : 0u));
	c = colorless_needed2;
	b = wTempLoadedAttackEnergyNeededAmount;
	a = wTempLoadedAttackEnergyNeededType;
	a = ConvertColorToEnergyCardID(a);
	e = a;
	d = 0u;
	return (CheckEnergyNeededForAttackResult){a, final_f, b, c, d, e, hl};
}
/* <<< factory CheckEnergyNeededForAttack */

/* >>> factory CreateDamageCharSprite */
void CreateDamageCharSprite(uint8_t a, uint8_t f, uint16_t de)
{
	uint8_t saved_a = a;
	uint8_t saved_f = f;
	(void)CreateSpriteAndAnimBufferEntry(SPRITE_DUEL_DAMAGE, f);
	gb_write8(de, wWhichSprite);
	wAnimFlags = SPRITE_ANIM_FLAG_UNSKIPPABLE;
	uint16_t hl = GetSpriteAnimBufferProperty(SPRITE_ANIM_COORD_X);
	AnimCoordsResult coords = GetAnimCoordsAndFlags();

	static const int8_t relative_x_pos[6] = { -16, -8, 0, 8, -8, -16 };
	uint8_t idx = wDamageCharIndex;
	uint8_t rel = (uint8_t)relative_x_pos[idx];
	uint8_t x = (uint8_t)(rel + coords.b);
	gb_write8(hl, x);
	hl = (uint16_t)(hl + 1u);
	gb_write8(hl, coords.c);

	uint8_t c = wDamageCharAnimDelay;
	Func_12ac9(saved_a, c);
	(void)saved_f;
}
/* <<< factory CreateDamageCharSprite */

/* >>> factory HasAlivePokemonInBench */
HasAlivePokemonInPlayAreaResult HasAlivePokemonInBench(void)
{
	return _HasAlivePokemonInPlayArea(1u);
}
/* <<< factory HasAlivePokemonInBench */

/* >>> factory DrawOpponentSelectionScreen */
void DrawOpponentSelectionScreen(uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t deck_id = gb_read8(wOpponentDeckID_ADDR);
	gb_write8(wNPCDuelDeckID_ADDR, deck_id);
	GetNPCDuelConfigurationsResult cfg = GetNPCDuelConfigurations(deck_id, f, b, c, d, e, hl);
	if ((cfg.f & 0x10u) == 0u) {
		gb_write8(wOpponentPortrait_ADDR, 0u);
		gb_write8(wOpponentName_ADDR, 0u);
		gb_write8((uint16_t)(wOpponentName_ADDR + 1u), 0u);
	}

	(void)PlaceTextItems(SELECT_COMPUTER_OPPONENT_DATA_ADDR_580);
	DrawDuelistPortraitsAndNames();

	uint8_t deck_id2 = gb_read8(wOpponentDeckID_ADDR);
	WriteOneByteNumberInTxSymbol_PadSpace(deck_id2, 5u, 16u, 0u, 0u, 0u);

	uint8_t prizes = gb_read8(wNPCDuelPrizes_ADDR);
	WriteOneByteNumberInTxSymbol_PadSpace(prizes, 15u, 10u, 0u, 0u, 0u);
}
/* <<< factory DrawOpponentSelectionScreen */

/* >>> factory PracticeDuel_ReplaceKnockedOutPokemon */
void PracticeDuel_ReplaceKnockedOutPokemon(void)
{
	uint8_t loc = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	if (loc == PLAY_AREA_BENCH_1_730)
		return;
	(void)HasAlivePokemonInBench();
	PrintPracticeDuelDrMasonInstructions(SelectStaryuPracticeDuelText);
}
/* <<< factory PracticeDuel_ReplaceKnockedOutPokemon */

/* >>> factory DrawDamageAnimationArrow */
void DrawDamageAnimationArrow(uint8_t f)
{
	gb_write8(wDamageCharIndex_ADDR, 5u);
	uint16_t de = (uint16_t)(wAnimationQueue_ADDR + 6u);
	CreateDamageCharSprite(SPRITE_ANIM_89_850, f, de);
}
/* <<< factory DrawDamageAnimationArrow */

/* >>> factory DrawDamageAnimationWeak */
void DrawDamageAnimationWeak(void)
{
	wDamageCharIndex = 3u;
	CreateDamageCharSprite(SPRITE_ANIM_91, 0u, (uint16_t)(wAnimationQueue_ADDR + 4u));
}
/* <<< factory DrawDamageAnimationWeak */

/* >>> factory DrawDamageAnimationResist */
void DrawDamageAnimationResist(void)
{
	wDamageCharIndex = 4u;
	CreateDamageCharSprite(SPRITE_ANIM_90, 0u, (uint16_t)(wAnimationQueue_ADDR + 5u));
	wDamageCharAnimDelay = (uint8_t)(wDamageCharAnimDelay + 18u);
}
/* <<< factory DrawDamageAnimationResist */

/* >>> factory DrawDamageAnimationNumbers */
void DrawDamageAnimationNumbers(void)
{
	GetDamageNumberChars();
	wDamageCharIndex = 0u;
	uint16_t hl = wDecimalChars_ADDR;
	uint16_t de = (uint16_t)(wAnimationQueue_ADDR + 1u);
	for (uint8_t i = 0; i < 3u; i++) {
		uint8_t ch = gb_read8(hl);
		if (ch != 0u) {
			CreateDamageCharSprite(ch, 0u, de);
		}
		hl = (uint16_t)(hl + 1u);
		de = (uint16_t)(de + 1u);
		wDamageCharIndex = (uint8_t)(wDamageCharIndex + 1u);
	}
}
/* <<< factory DrawDamageAnimationNumbers */

/* >>> factory Func_15886 */
CoreCardListResult Func_15886(uint16_t hl)
{
	CoreCardListResult check = CreateEnergyCardListFromHand(0u);
	if (check.f & 0x10u) {
		return check;
	}

	for (;;) {
		uint8_t flag = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (flag == 0u) {
			return (CoreCardListResult){0u, 0x80u};
		}
		uint8_t card_id = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		LookResult loc = LookForCardIDInPlayArea_Bank5(card_id, PLAY_AREA_ARENA);
		if (loc.f & 0x10u) {
			uint8_t e = loc.a;
			CountNumberOfEnergyCardsAttachedResult cnt = CountNumberOfEnergyCardsAttached(e);
			uint8_t threshold = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			if (cnt.a >= threshold) {
				continue;
			}
			hTempPlayAreaLocation_ff9d = e;
			uint8_t play_f = AITryToPlayEnergyCard();
			if (play_f & 0x10u) {
				return (CoreCardListResult){0u, play_f};
			}
			continue;
		}
		hl = (uint16_t)(hl + 1u);
	}
}
/* <<< factory Func_15886 */

/* >>> factory CheckAbleToRetreat */
CheckAbleToRetreatResult CheckAbleToRetreat(void)
{
	RetreatEffectResult r1 = CheckUnableToRetreatDueToEffect();
	if (r1.f & 0x10u) {
		return (CheckAbleToRetreatResult){0u, r1.f, r1.hl};
	}
	CheckIfActiveStatusResult r2 = CheckIfActiveCardParalyzedOrAsleep();
	if (r2.f & 0x10u) {
		return (CheckAbleToRetreatResult){r2.a, r2.f, r2.hl};
	}
	HasAlivePokemonInPlayAreaResult r3 = HasAlivePokemonInBench();
	if (r3.f & 0x10u) {
		uint8_t f_out = (uint8_t)((r3.f & 0x80u) | 0x10u);
		return (CheckAbleToRetreatResult){r3.a, f_out, UnableToRetreatText};
	}
	DuelistVarResult deck_idx = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint16_t card_id = GetCardIDFromDeckIndex(deck_idx.a);
	LoadCardDataToBuffer1_FromCardID((uint8_t)card_id);
	uint8_t card_type = wLoadedCard1Type;
	if (card_type == TYPE_TRAINER) {
		return (CheckAbleToRetreatResult){TYPE_TRAINER, 0x90u, UnableToRetreatText};
	}
	EnoughRetreatEnergiesResult r4 = CheckIfEnoughEnergiesToRetreat();
	if (r4.f & 0x10u) {
		uint8_t required = wEnergyCardsRequiredToRetreat;
		LoadTxRam3((uint16_t)required);
		return (CheckAbleToRetreatResult){0u, 0x90u, EnergyCardsRequiredToRetreatText};
	}
	uint8_t final_a = r4.a;
	uint8_t final_f = (uint8_t)((final_a == 0u) ? 0x80u : 0x00u);
	return (CheckAbleToRetreatResult){final_a, final_f, 0u};
}
/* <<< factory CheckAbleToRetreat */

/* >>> factory LookForEnergyNeededInHand */
uint8_t LookForEnergyNeededInHand(void)
{
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	CheckEnergyNeededForAttackResult r1 = CheckEnergyNeededForAttack();
	uint8_t total1 = (uint8_t)(r1.b + r1.c);
	if (total1 == 1u) {
		if (r1.b == 0u) {
			CoreCardListResult cr = CreateEnergyCardListFromHand(0u);
			if (!(cr.f & 0x10u)) {
				return 0x90u;
			}
		} else {
			CoreCardListResult cr = LookForCardIDInHandList_Bank5(r1.e);
			if (cr.f & 0x10u) {
				return cr.f;
			}
		}
		return 0x80u;
	}
	if (total1 == 2u && r1.c == 2u) {
		CoreCardListResult cr = LookForCardIDInHandList_Bank5(DOUBLE_COLORLESS_ENERGY);
		if (cr.f & 0x10u) {
			return cr.f;
		}
		return 0x80u;
	}

	wSelectedAttack = SECOND_ATTACK;
	CheckEnergyNeededForAttackResult r2 = CheckEnergyNeededForAttack();
	uint8_t total2 = (uint8_t)(r2.b + r2.c);
	if (total2 == 1u) {
		if (r2.b == 0u) {
			CoreCardListResult cr = CreateEnergyCardListFromHand(0u);
			if (!(cr.f & 0x10u)) {
				return 0x90u;
			}
		} else {
			CoreCardListResult cr = LookForCardIDInHandList_Bank5(r2.e);
			if (cr.f & 0x10u) {
				return cr.f;
			}
		}
		return 0x80u;
	}
	if (total2 == 2u && r2.c == 2u) {
		CoreCardListResult cr = LookForCardIDInHandList_Bank5(DOUBLE_COLORLESS_ENERGY);
		if (cr.f & 0x10u) {
			return cr.f;
		}
		return 0x80u;
	}
	return 0x80u;
}
/* <<< factory LookForEnergyNeededInHand */

/* >>> factory Func_7364 */
Func_7364Result Func_7364(void)
{
	wTileMapFill = 0u;
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadSymbolsFont();
	(void)SetupText(0x38u, 0x9Fu);
	(void)DrawWideTextBox();
	EnableLCD();

	wOpponentDeckID = 0u;
	DrawOpponentSelectionScreen(0u, 0u, 0u, 0u, 0u, 0u);

	for (;;) {
		DoFrame();
		uint8_t keys = hDPadHeld;
		if (keys == 0u) {
			continue;
		}
		uint8_t b = keys;
		if (keys & (PAD_A | PAD_START)) {
			uint8_t opp = wOpponentDeckID;
			wNPCDuelDeckID = opp;
			(void)GetNPCDuelConfigurations(opp, 0u, 0u, 0u, 0u, 0u, 0u);
			return (Func_7364Result){0u, 0x80u};
		}
		if (b & (1u << B_PAD_B)) {
			return (Func_7364Result){0u, 0x10u};
		}

		uint8_t a = wOpponentDeckID;
		if (b & (1u << B_PAD_RIGHT)) {
			a = (uint8_t)(a + 1u);
			if (a >= NUM_DECK_IDS) {
				a = 0u;
			}
		}
		if (b & (1u << B_PAD_LEFT)) {
			if (a != 0u) {
				a = (uint8_t)(a - 1u);
			} else {
				a = (uint8_t)(NUM_DECK_IDS - 1u);
			}
		}
		if (b & (1u << B_PAD_UP)) {
			a = (uint8_t)(a + 10u);
			if (a >= NUM_DECK_IDS) {
				a = 0u;
			}
		}
		if (b & (1u << B_PAD_DOWN)) {
			if (a >= 10u) {
				a = (uint8_t)(a - 10u);
			} else {
				a = (uint8_t)(NUM_DECK_IDS - 1u);
			}
		}
		wOpponentDeckID = a;
		DrawOpponentSelectionScreen(0u, 0u, 0u, 0u, 0u, 0u);
	}
}
/* <<< factory Func_7364 */

/* >>> factory CheckEnergyNeededForAttackAfterDiscard */
CheckEnergyNeededForAttackAfterDiscardResult CheckEnergyNeededForAttackAfterDiscard(void)
{
	DuelistVarResult duelist = GetTurnDuelistVariable((uint8_t)(hTempPlayAreaLocation_ff9d + DUELVARS_ARENA_CARD));
	uint8_t d = duelist.a;
	uint8_t e = wSelectedAttack;
	(void)CopyAttackDataAndDamage_FromDeckIndex(d, e);

	uint8_t name0 = gb_read8(wLoadedAttackName_ADDR);
	uint8_t name1 = gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1u));
	uint8_t a = (uint8_t)(name0 | name1);
	if (a == 0u)
		return (CheckEnergyNeededForAttackAfterDiscardResult){0u, 0u, d, 0u, 0x90u};
	a = wLoadedAttackCategory;
	if (a == POKEMON_POWER)
		return (CheckEnergyNeededForAttackAfterDiscardResult){0u, 0u, d, 0u, 0x90u};

	uint8_t discard_loc = hTempPlayAreaLocation_ff9d;
	uint8_t discarded = AIPickEnergyCardToDiscard(discard_loc);
	uint8_t deck_idx = LoadCardDataToBuffer1_FromDeckIndex(discarded);
	if (deck_idx == DOUBLE_COLORLESS_ENERGY) {
		uint16_t hl0 = (uint16_t)(wAttachedEnergies_ADDR + COLORLESS);
		gb_write8(hl0, (uint8_t)(gb_read8(hl0) - 1u));
		gb_write8(hl0, (uint8_t)(gb_read8(hl0) - 1u));
		gb_write8(wTotalAttachedEnergies_ADDR, (uint8_t)(gb_read8(wTotalAttachedEnergies_ADDR) - 1u));
		gb_write8(wTotalAttachedEnergies_ADDR, (uint8_t)(gb_read8(wTotalAttachedEnergies_ADDR) - 1u));
	} else {
		uint8_t idx = (uint8_t)(deck_idx - 1u);
		uint16_t hl0 = (uint16_t)(wAttachedEnergies_ADDR + idx);
		gb_write8(hl0, (uint8_t)(gb_read8(hl0) - 1u));
		gb_write8(wTotalAttachedEnergies_ADDR, (uint8_t)(gb_read8(wTotalAttachedEnergies_ADDR) - 1u));
	}

	HandleEnergyBurn();

	wTempLoadedAttackEnergyCost = 0u;
	wTempLoadedAttackEnergyNeededAmount = 0u;
	wTempLoadedAttackEnergyNeededType = 0u;

	uint16_t hl = wAttachedEnergies_ADDR;
	uint16_t de = wLoadedAttackEnergyCost_ADDR;
	uint8_t b = 0u;
	uint8_t c = (NUM_TYPES / 2u) - 1u;
	do {
		uint8_t byte0 = gb_read8(de);
		a = (uint8_t)((byte0 >> 4) | (byte0 << 4));
		CheckIfEnoughParticularAttachedEnergyResult r1 = CheckIfEnoughParticularAttachedEnergy(a, hl, b);
		b = r1.b; hl = r1.hl;
		a = gb_read8(de);
		CheckIfEnoughParticularAttachedEnergyResult r2 = CheckIfEnoughParticularAttachedEnergy(a, hl, b);
		b = r2.b; hl = r2.hl;
		de = (uint16_t)(de + 1u);
		c = (uint8_t)(c - 1u);
	} while (c != 0u);

	uint8_t byte1 = gb_read8(de);
	uint8_t swapped = (uint8_t)((byte1 >> 4) | (byte1 << 4));
	b = (uint8_t)(swapped & 0x0Fu);
	a = wTempLoadedAttackEnergyCost;
	hl = wTempLoadedAttackEnergyNeededAmount_ADDR;
	a = (uint8_t)(a - gb_read8(hl));
	c = a;
	a = wTotalAttachedEnergies;
	uint8_t sub1 = (uint8_t)(a - c);
	uint8_t sub2 = (uint8_t)(sub1 - b);
	a = sub2;
	if (sub1 < b) {
		uint8_t colorless_needed = (uint8_t)((uint8_t)(~a) + 1u);
		uint8_t not_enough_f = (uint8_t)((colorless_needed == 0u ? 0x80u : 0u) | 0x10u);
		c = colorless_needed;
		b = wTempLoadedAttackEnergyNeededAmount;
		a = wTempLoadedAttackEnergyNeededType;
		a = ConvertColorToEnergyCardID(a);
		e = a;
		d = 0u;
		return (CheckEnergyNeededForAttackAfterDiscardResult){b, c, d, e, not_enough_f};
	}

	a = wTempLoadedAttackEnergyNeededAmount;
	if (a == 0u)
		return (CheckEnergyNeededForAttackAfterDiscardResult){b, c, (uint8_t)(de >> 8), (uint8_t)de, 0x80u};

	uint8_t colorless_needed2 = (uint8_t)((uint8_t)(~(uint8_t)0u) + 1u);
	uint8_t final_f = (uint8_t)((colorless_needed2 == 0u ? 0x80u : 0u) | 0x10u);
	c = colorless_needed2;
	b = wTempLoadedAttackEnergyNeededAmount;
	a = wTempLoadedAttackEnergyNeededType;
	a = ConvertColorToEnergyCardID(a);
	e = a;
	d = 0u;
	return (CheckEnergyNeededForAttackAfterDiscardResult){b, c, d, e, final_f};
}
/* <<< factory CheckEnergyNeededForAttackAfterDiscard */

/* >>> factory DisplayFirstOrNextCardPage */
CardPageNavigationResult DisplayFirstOrNextCardPage(uint8_t b)
{
	CardPageNavigationResult r = GoToFirstOrNextCardPage();
	r.b = b;
	return r;
}
/* <<< factory DisplayFirstOrNextCardPage */

/* >>> factory PrintAttackOrCardDescription */
PrintAttackOrCardDescriptionResult PrintAttackOrCardDescription(uint16_t hl, uint8_t d, uint8_t e)
{
	(void)SetNoLineSeparation();
	uint16_t text_id = (uint16_t)(gb_read8(hl) | ((uint16_t)gb_read8((uint16_t)(hl + 1u)) << 8));
	uint8_t lines = CountLinesOfTextFromID(text_id);
	if (lines >= 7u) {
		e = (uint8_t)(e - 1u);
	}
	InitTextPrintingInTextbox(19u, d, e);
	ProcessTextHeaderResult text = ProcessTextFromID(text_id);
	(void)SetOneLineSeparation();
	return (PrintAttackOrCardDescriptionResult){text.a, text.d, text.e, text.f, text.hl};
}
/* <<< factory PrintAttackOrCardDescription */

/* >>> factory PrintAttackOrPkmnPowerInformation */
PrintAttackOrPkmnPowerInformationResult PrintAttackOrPkmnPowerInformation(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t lo = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint8_t hi = gb_read8(hl);
	if ((uint8_t)(lo | hi) == 0u) {
		return (PrintAttackOrPkmnPowerInformationResult){0u, b, c, d, e, 0x80u, hl};
	}

	uint16_t saved_hl = hl;
	(void)InitTextPrinting_ProcessTextFromPointerToID(7u, e, (uint16_t)(hl - 1u));
	hl = (uint16_t)(saved_hl + 2u);

	if (wCardPageNumber == 0u) {
		uint8_t alo = gb_read8((uint16_t)(hl - 1u));
		uint8_t ahi = gb_read8(hl);
		if ((uint8_t)(alo | ahi) != 0u) {
			WriteByteToBGMap0(SYM_ATK_DESCR, 18u, e);
		}
	}

	hl = (uint16_t)(hl + 3u);
	uint16_t damage_hl = hl;
	uint8_t damage = gb_read8(hl);
	if (damage != 0u) {
		WriteOneByteNumberInTxSymbol_PadSpace(damage, 15u, (uint8_t)(e + 1u), d, e, hl);
	}
	hl = (uint16_t)(damage_hl + 1u);

	uint8_t category = (uint8_t)(gb_read8(hl) & (uint8_t)~RESIDUAL);
	if (category == 0u) {
		/* .print_energy_cost, fallthrough below */
	} else if (category == POKEMON_POWER) {
		uint16_t text_hl = PKMNPWRText;
		ProcessTextHeaderResult text = InitTextPrinting_ProcessTextFromID(2u, e, text_hl);
		return (PrintAttackOrPkmnPowerInformationResult){text.a, b, c, text.d, text.e, text.f, text.hl};
	} else {
		uint8_t sym = (uint8_t)(category + SYM_PLUS_OFFSET);
		WriteByteToBGMap0(sym, 18u, (uint8_t)(e + 1u));
	}

	hl = (uint16_t)(hl - 11u);
	c = e;
	uint8_t row = 2u;
	uint8_t running_e = 0u;
	uint8_t last_a = 0u;
	for (uint8_t i = NUM_TYPES / 2u; i != 0u; i--) {
		uint8_t byte1 = gb_read8(hl);
		uint8_t swapped = (uint8_t)((byte1 >> 4) | (byte1 << 4));
		PrintEnergiesResult r1 = PrintEnergiesOfColor(swapped, row, c, running_e);
		row = r1.b; running_e = r1.e; last_a = r1.a;
		uint8_t byte2 = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		PrintEnergiesResult r2 = PrintEnergiesOfColor(byte2, row, c, running_e);
		row = r2.b; running_e = r2.e; last_a = r2.a;
	}
	return (PrintAttackOrPkmnPowerInformationResult){last_a, b, c, 0u, running_e, 0u, hl};
}
/* <<< factory PrintAttackOrPkmnPowerInformation */

/* >>> factory PrintAttackOrNonPokemonCardDescription */
PrintAttackOrCardDescriptionResult PrintAttackOrNonPokemonCardDescription(uint16_t hl, uint8_t d, uint8_t e)
{
	uint8_t a = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	uint8_t b = gb_read8(hl);
	a = (uint8_t)(a | b);
	if (a == 0u) {
		return (PrintAttackOrCardDescriptionResult){a, d, e, 0x80u, hl};
	}
	hl = (uint16_t)(hl - 1u);
	return PrintAttackOrCardDescription(hl, 1u, 11u);
}
/* <<< factory PrintAttackOrNonPokemonCardDescription */

/* >>> factory DisplayCardPageOnLeftOrRightPressed */
void DisplayCardPageOnLeftOrRightPressed(uint8_t a)
{
	if (a & (1u << B_PAD_LEFT)) {
		(void)GoToPreviousCardPage();
	} else {
		(void)GoToFirstOrNextCardPage();
	}
	DisplayCardPage();
}
/* <<< factory DisplayCardPageOnLeftOrRightPressed */

/* >>> factory PrintPlayAreaCardHeader */
void PrintPlayAreaCardHeader(void)
{
	uint8_t slot = wCurPlayAreaSlot;
	uint8_t y = wCurPlayAreaY;

	DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD));
	LoadCardDataToBuffer1_FromDeckIndex(card.a);
	InitTextPrinting(4u, y);

	uint16_t name_ptr = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8));
	CopyTextData_FromTextID(10u, name_ptr, wDefaultText_ADDR);
	uint16_t text_hl = wDefaultText_ADDR;
	ProcessText(&text_hl);

	uint8_t color = GetPlayAreaCardColor(slot);
	JPWriteByteToBGMap0((uint8_t)(color + 1u), 18u, y);
	WriteByteToBGMap0(SYM_Lv, 14u, y);
	WriteTwoDigitNumberInTxSymbol_PadSpace(wLoadedCard1Level, 15u, y, 0u, 0u, 0u);

	DuelistVarResult stage = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD_STAGE));
	uint8_t idx = (uint8_t)(stage.a * 2u);
	uint8_t tile = kFaceDownCardTileNumbers[idx];
	uint8_t palette = kFaceDownCardTileNumbers[(uint8_t)(idx + 1u)];
	uint16_t de = (uint16_t)(((uint16_t)2u << 8) | y);
	FillRectangle(tile, 2u, 2u, de, (uint16_t)((1u << 8) | 2u));

	if (wConsole == CONSOLE_CGB) {
		hBankVRAM = 1u;
		gb_write8(0xFF4Fu, 1u);
		FillRectangle(palette, 2u, 2u, de, 0u);
		hBankVRAM = 0u;
		gb_write8(0xFF4Fu, 0u);
	}

	if (slot == 0u) {
		uint8_t c = (uint8_t)(y + 2u);
		DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
		CheckPrintCnfSlpPrz(status.a, 2u, c);
		CheckPrintPoisoned(status.a, 3u, c);
		CheckPrintDoublePoisoned(status.a, 4u, c);
	}

	DuelistVarResult plus = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER));
	if (plus.a != 0u) {
		uint8_t c2 = (uint8_t)(y + 1u);
		WriteByteToBGMap0(SYM_PLUSPOWER, 15u, c2);
		WriteByteToBGMap0((uint8_t)(plus.a + SYM_0), 16u, c2);
	}

	DuelistVarResult def = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD_ATTACHED_DEFENDER));
	if (def.a != 0u) {
		uint8_t c3 = (uint8_t)(y + 1u);
		WriteByteToBGMap0(SYM_DEFENDER, 17u, c3);
		WriteByteToBGMap0((uint8_t)(def.a + SYM_0), 18u, c3);
	}
}
/* <<< factory PrintPlayAreaCardHeader */

/* >>> factory PrintPokemonCardLength */
void PrintPokemonCardLength(uint16_t hl, uint8_t b, uint8_t c)
{
	uint8_t feet = (uint8_t)(hl >> 8);
	uint8_t inches = (uint8_t)hl;
	uint8_t row = b;
	uint8_t col = c;

	{
		TwoByteNumberToTxSymbolPadResult digits = TwoByteNumberToTxSymbol_PadSpace_Bank1(0u, 0u, 0u, 0u, (uint16_t)feet);
		uint8_t offset = (uint8_t)(digits.b + 1u);
		gb_write8(wPokemonLengthPrintOffset_ADDR, offset);
		uint16_t bgmap_addr = BCCoordToBGMap0Address(row, col);
		uint16_t src = digits.hl;
		uint16_t dst = bgmap_addr;
		SafeCopyDataHLtoDE(&src, &dst, offset);
		uint8_t new_row = (uint8_t)(offset + row);
		InitTextPrinting(new_row, col);
		ProcessTextFromID(FeetText);
		row = (uint8_t)(new_row + 1u);
	}
	{
		TwoByteNumberToTxSymbolPadResult digits = TwoByteNumberToTxSymbol_PadSpace_Bank1(0u, 0u, 0u, 0u, (uint16_t)inches);
		uint8_t offset = (uint8_t)(digits.b + 1u);
		gb_write8(wPokemonLengthPrintOffset_ADDR, offset);
		uint16_t bgmap_addr = BCCoordToBGMap0Address(row, col);
		uint16_t src = digits.hl;
		uint16_t dst = bgmap_addr;
		SafeCopyDataHLtoDE(&src, &dst, offset);
		uint8_t new_row = (uint8_t)(offset + row);
		InitTextPrinting(new_row, col);
		ProcessTextFromID(InchesText);
	}
}
/* <<< factory PrintPokemonCardLength */

/* >>> factory PlayDeckShuffleAnimation */
/* The ROM leaves the animation id it selected in `e`, and ShuffleCardsInDeck
 * feeds that register straight to ShuffleDeck, so `e` is a real output and not
 * scratch. The one-card path never assigns it, so it has to arrive as a
 * parameter to survive. Measured: reference returns e=$51 on the player's turn
 * and e=$52 on the opponent's. */
PlayDeckShuffleAnimationResult PlayDeckShuffleAnimation(uint8_t e)
{
	if (gb_read8(wDuelDisplayedScreen_ADDR) != SHUFFLE_DECK_490) {
		ZeroObjectPositionsAndToggleOAMCopy();
		EmptyScreen();
		DrawDuelistPortraitsAndNames();
	}
	gb_write8(wDuelDisplayedScreen_ADDR, SHUFFLE_DECK_490);

	DuelistVarResult var = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK_490);
	uint8_t remaining = (uint8_t)(DECK_SIZE_490 - var.a);
	if (remaining < 2u) {
		uint16_t hl = remaining;
		LoadTxRam3(hl);
		(void)DrawWideTextBox_PrintText(DeckHasXCardsText);
		EnableLCD();
		uint8_t counter = 60u;
		do {
			DoFrame();
			counter = (uint8_t)(counter - 1u);
		} while (counter != 0u);
		return (PlayDeckShuffleAnimationResult){0x01u, e};
	}

	(void)DrawWideTextBox_PrintText(ShufflesTheDeckText);
	EnableLCD();
	ResetAnimationQueue();

	e = DUEL_ANIM_PLAYER_SHUFFLE_490;
	if (gb_read8(hWhoseTurn_ADDR) != PLAYER_TURN_490)
		e = DUEL_ANIM_OPP_SHUFFLE_490;

	(void)PlayDuelAnimation(e);
	(void)PlayDuelAnimation(e);
	(void)PlayDuelAnimation(e);

	for (;;) {
		DoFrame();
		CheckSkipDelayAllowedResult skip = CheckSkipDelayAllowed(0u, 0u, 0u, 0u, 0u, 0u);
		if ((skip.f & FLAG_C_490) != 0u)
			break;
		AnimationStatusResult anim = CheckAnyAnimationPlaying();
		if ((anim.f & FLAG_C_490) == 0u)
			break;
	}
	FinishQueuedAnimations();
	return (PlayDeckShuffleAnimationResult){0x01u, e};
}
/* <<< factory PlayDeckShuffleAnimation */

/* >>> factory OppAction_6b30 */
uint8_t OppAction_6b30(void)
{
	uint8_t saved = hWhoseTurn;
	hWhoseTurn = hTemp_ffa0;
	(void)PlayDeckShuffleAnimation(0u);
	hWhoseTurn = saved;
	return saved;
}
/* <<< factory OppAction_6b30 */

/* >>> factory PrintPlayAreaCardInformation */
PrintPlayAreaCardInformationResult PrintPlayAreaCardInformation(void)
{
	PrintPlayAreaCardHeader();

	uint8_t slot = wCurPlayAreaSlot;
	uint8_t e = slot;
	uint8_t y1 = (uint8_t)(wCurPlayAreaY + 1u);
	uint8_t c = y1;
	uint8_t b = 7u;
	PrintPlayAreaCardAttachedEnergies(b, c, e);

	c = (uint8_t)(wCurPlayAreaY + 1u);
	b = 5u;
	WriteByteToBGMap0(SYM_E, b, c);

	c = (uint8_t)(c + 1u);
	WriteByteToBGMap0(SYM_HP, b, c);

	DuelistVarResult hp = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD_HP));
	if (hp.a == 0u) {
		uint8_t ke = (uint8_t)(wCurPlayAreaY + 2u);
		uint8_t kd = 7u;
		ProcessTextHeaderResult r = InitTextPrinting_ProcessTextFromID(kd, ke, KnockOutText);
		return (PrintPlayAreaCardInformationResult){r.hl};
	}

	uint8_t hd = wLoadedCard1HP;
	DrawHPBar(hd, hp.a);

	c = (uint8_t)(wCurPlayAreaY + 2u);
	b = 7u;
	uint16_t de = BCCoordToBGMap0Address(b, c);
	uint16_t hl = wDefaultText_ADDR;
	SafeCopyDataHLtoDE(&hl, &de, 12u);
	return (PrintPlayAreaCardInformationResult){0u};
}
/* <<< factory PrintPlayAreaCardInformation */

/* >>> factory PrintPlayAreaCardInformationAndLocation */
void PrintPlayAreaCardInformationAndLocation(void)
{
	uint8_t slot = wCurPlayAreaSlot;
	DuelistVarResult r = GetTurnDuelistVariable((uint8_t)(slot + DUELVARS_ARENA_CARD));
	if (r.a == 0xFFu)
		return;
	(void)PrintPlayAreaCardInformation();
	PrintPlayAreaCardLocation();
}
/* <<< factory PrintPlayAreaCardInformationAndLocation */

/* >>> factory DisplayUsePokemonPowerScreen */
void DisplayUsePokemonPowerScreen(void)
{
	uint8_t slot = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	wCurPlayAreaSlot = slot;
	wCurPlayAreaY = 0u;
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelCheckPokemonScreenTiles();
	PrintPlayAreaCardInformationAndLocation();
	InitTextPrinting(1u, 4u);
	uint16_t hl = wLoadedCard1Atk1Name_ADDR;
	(void)InitTextPrinting_ProcessTextFromPointerToID(1u, 4u, hl);
	hl = wLoadedCard1Atk1Description_ADDR;
	(void)PrintAttackOrCardDescription(hl, 1u, 6u);
}
/* <<< factory DisplayUsePokemonPowerScreen */

/* >>> factory InitAndPrintPlayAreaCardInformationAndLocation */
void InitAndPrintPlayAreaCardInformationAndLocation(void)
{
	uint8_t a = gb_read8(hTempPlayAreaLocation_ff9d_ADDR);
	wCurPlayAreaSlot = a;
	uint8_t c = a;
	a = (uint8_t)(a + a);
	a = (uint8_t)(a + c);
	wCurPlayAreaY = a;
	PrintPlayAreaCardInformationAndLocation();
}
/* <<< factory InitAndPrintPlayAreaCardInformationAndLocation */

/* >>> factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox */
void InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox(void)
{
	InitAndPrintPlayAreaCardInformationAndLocation();
	uint8_t e = wCurPlayAreaY;
	(void)SetCursorParametersForTextBox_Default(0u, e);
}
/* <<< factory InitAndPrintPlayAreaCardInformationAndLocation_WithTextBox */

/* >>> factory PrintPlayAreaCardList */
void PrintPlayAreaCardList(void)
{
	gb_write8(wDuelDisplayedScreen_ADDR, PLAY_AREA_CARD_LIST);
	SetListPointer(wDuelTempList_ADDR);
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t b;
	for (b = 0u; b < count; ++b) {
		gb_write8(wCurPlayAreaSlot_ADDR, b);
		gb_write8(wCurPlayAreaY_ADDR, (uint8_t)(b + b + b));
		uint8_t card = GetTurnDuelistVariable((uint8_t)(b + DUELVARS_ARENA_CARD)).a;
		SetNextElementOfList(card);
		PrintPlayAreaCardInformationAndLocation();
	}
	uint8_t saved_count = b;
	uint8_t loc;
	for (loc = b; loc != MAX_PLAY_AREA_POKEMON; ++loc) {
		gb_write8(wCurPlayAreaSlot_ADDR, loc);
		gb_write8(wCurPlayAreaY_ADDR, (uint8_t)(loc + loc + loc));
		PrintPlayAreaCardLocation();
	}
	b = saved_count;
	gb_write8(wNumPlayAreaItems_ADDR, b);
	if (gb_read8(wExcludeArenaPokemon_ADDR) == 0u)
		return;
	b = (uint8_t)(b - 1u);
	gb_write8(wNumPlayAreaItems_ADDR, b);
	uint16_t src = (uint16_t)(wDuelTempList_ADDR + 1u);
	uint16_t dst = wDuelTempList_ADDR;
	do {
		uint8_t v = gb_read8(src);
		gb_write8(dst, v);
		src = (uint16_t)(src + 1u);
		dst = (uint16_t)(dst + 1u);
		--b;
	} while (b != 0u);
}
/* <<< factory PrintPlayAreaCardList */

/* >>> factory OppAction_UsePokemonPower */
void OppAction_UsePokemonPower(void)
{
	uint8_t d = gb_read8(hTempCardIndex_ff9f_ADDR);
	(void)CopyAttackDataAndDamage_FromDeckIndex(d, FIRST_ATTACK_OR_PKMN_POWER);
	uint8_t slot = gb_read8(hTemp_ffa0_ADDR);
	gb_write8(hTempPlayAreaLocation_ff9d_ADDR, slot);
	DisplayUsePokemonPowerScreen();
	uint8_t card = gb_read8(hTempCardIndex_ff9f_ADDR);
	LoadCardNameToTxRam2(card);
	uint16_t hl = wLoadedAttackName_ADDR;
	uint8_t lo = gb_read8(hl);
	hl = (uint16_t)(hl + 1u);
	gb_write8(wTxRam2_b_ADDR, lo);
	uint8_t hi = gb_read8(hl);
	gb_write8((uint16_t)(wTxRam2_b_ADDR + 1u), hi);
	(void)DrawWideTextBox_WaitForInput_Bank1(WillUseThePokemonPowerText);
	(void)ExchangeRNG(0u, 0u, 0u, 0u);
	gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);
}
/* <<< factory OppAction_UsePokemonPower */

/* >>> factory Func_616e */
void Func_616e(uint8_t a)
{
	gb_write8(hTempPlayAreaLocation_ff9d_ADDR, a);
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelCheckPokemonScreenTiles();
	gb_write8(wExcludeArenaPokemon_ADDR, 0u);
	PrintPlayAreaCardList();
	EnableLCD();
	InitAndPrintPlayAreaCardInformationAndLocation();
}
/* <<< factory Func_616e */

/* >>> factory PrintPlayAreaCardList_EnableLCD */
NumPlayAreaItemsResult PrintPlayAreaCardList_EnableLCD(void)
{
	gb_write8(wDuelDisplayedScreen_ADDR, PLAY_AREA_CARD_LIST);
	PrintPlayAreaCardList();
	EnableLCD();
	return (NumPlayAreaItemsResult){gb_read8(wNumPlayAreaItems_ADDR)};
}
/* <<< factory PrintPlayAreaCardList_EnableLCD */

/* >>> factory FlushAllPalettesOrSendPal23Packet */
void FlushAllPalettesOrSendPal23Packet(void)
{
	uint8_t console = gb_read8(wConsole_ADDR);
	if (console == 0u)
		return;
	if (console != 1u) {
		FlushAllPalettes();
		return;
	}
	gb_write8(wTempSGBPacket_ADDR, 9u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 1u), 0x9Cu);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 2u), 0x63u);
	gb_write8((uint16_t)(wTempSGBPacket_ADDR + 0x0Fu), 0u);
	SendSGBResult result = SendSGB(0u, 0x80u, 0u, 0u, 0u, 0u, wTempSGBPacket_ADDR);
	(void)result;
}
/* <<< factory FlushAllPalettesOrSendPal23Packet */

/* >>> factory CheckIfCardCanBePlayed */
CheckIfCardCanBePlayedResult CheckIfCardCanBePlayed(uint8_t a)
{
	hTempCardIndex_ff9f = a;
	(void)LoadCardDataToBuffer1_FromDeckIndex(a);
	uint8_t type = wLoadedCard1Type; /* verified post gate-flake fix */
	if (type < TYPE_ENERGY) {
		if (wLoadedCard1Stage == 0u) {
			DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
			uint8_t f = 0x40u;
			if (count.a == MAX_PLAY_AREA_POKEMON) f |= 0x80u;
			if ((count.a & 0x0Fu) < (MAX_PLAY_AREA_POKEMON & 0x0Fu)) f |= 0x20u;
			if (count.a < MAX_PLAY_AREA_POKEMON) f |= 0x10u;
			f ^= 0x10u;
			return (CheckIfCardCanBePlayedResult){count.a, f};
		}
		PrehistoricPowerResult power = IsPrehistoricPowerActive(0u);
		if (power.f & 0x10u)
			return (CheckIfCardCanBePlayedResult){power.a, power.f};
		DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		uint8_t remaining = count.a;
		uint8_t last_a = count.a;
		uint8_t last_f = 0x10u;
		for (uint8_t slot = 0u; slot < remaining; slot++) {
			EvolveResult check = CheckIfCanEvolveInto(a, slot);
			last_a = check.a;
			last_f = check.f;
			if ((check.f & 0x10u) == 0u)
				return (CheckIfCardCanBePlayedResult){check.a, check.f};
		}
		return (CheckIfCardCanBePlayedResult){last_a, (uint8_t)((last_f & 0x80u) | 0x10u)};
	}
	if (type == TYPE_TRAINER) {
		TrainerEffectResult blocked = CheckCantUseTrainerDueToEffect();
		if (blocked.f & 0x10u)
			return (CheckIfCardCanBePlayedResult){0u, blocked.f};
		LoadEffectResult loaded = LoadNonPokemonCardEffectCommands();
		TryExecuteEffectCommandFunctionResult effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_1, 0u, 0u, 0u);
		return (CheckIfCardCanBePlayedResult){effect.a, effect.f};
	}
	uint8_t energy = wAlreadyPlayedEnergy;
	uint8_t f = (energy == 0u) ? 0x80u : 0x10u;
	return (CheckIfCardCanBePlayedResult){energy, f};
}
/* <<< factory CheckIfCardCanBePlayed */

/* >>> factory OppAction_6b15 */
OppAction_6b15Result OppAction_6b15(void)
{
	TryExecuteEffectCommandFunctionResult effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AFTER_DAMAGE, 0u, 0u, 0u);
	wSkipDuelistIsThinkingDelay = 0x01u;
	return (OppAction_6b15Result){0x01u, effect.f, effect.c, effect.hl};
}
/* <<< factory OppAction_6b15 */

/* >>> factory OppAction_ExecutePokemonPowerEffect */
OppAction_ExecutePokemonPowerEffectResult OppAction_ExecutePokemonPowerEffect(void)
{
	ResetAttackAnimationIsPlaying();
	TryExecuteEffectCommandFunctionResult effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_BEFORE_DAMAGE, 0u, 0u, 0u);
	wSkipDuelistIsThinkingDelay = 0x01u;
	return (OppAction_ExecutePokemonPowerEffectResult){0x01u, effect.f, effect.c, effect.hl};
}
/* <<< factory OppAction_ExecutePokemonPowerEffect */

/* >>> factory LoadSelectedCardGfx */
void LoadSelectedCardGfx(void)
{
	DeckEntryResult result = GetCardInDuelTempList(hCurMenuItem, 0u);
	LoadCardDataToBuffer1_FromCardID(result.e);
	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	SetBGP6OrSGB3ToCardPalette();
	FlushAllPalettesOrSendPal23Packet();
}
/* <<< factory LoadSelectedCardGfx */

/* >>> factory AIProcessHandTrainerCards */
AIProcessHandTrainerCardsWrapResult AIProcessHandTrainerCards(uint8_t a)
{
	AIProcessHandTrainerCardsResult r = _AIProcessHandTrainerCards(a);
	return (AIProcessHandTrainerCardsWrapResult){r.a, r.f};
}
/* <<< factory AIProcessHandTrainerCards */

/* >>> factory CardListFunction */
CardListFunctionResult CardListFunction(void)
{
	uint8_t a = hKeysPressed;
	if ((a & PAD_B) != 0u) {
		hCurMenuItem = MENU_CANCEL;
		return (CardListFunctionResult){MENU_CANCEL, 0x10u};
	}
	a = (uint8_t)(a & (PAD_A | PAD_SELECT | PAD_START));
	if (a != 0u)
		return (CardListFunctionResult){a, 0x10u};
	a = (uint8_t)(hKeysReleased & PAD_CTRL_PAD);
	if (a != 0u) {
		LoadSelectedCardGfx();
		return (CardListFunctionResult){0u, 0x00u};
	}
	return (CardListFunctionResult){a, 0xA0u};
}
/* <<< factory CardListFunction */

/* >>> factory CheckIfSelectedAttackIsUnusable */
CheckIfSelectedAttackIsUnusableResult CheckIfSelectedAttackIsUnusable(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t location = hTempPlayAreaLocation_ff9d;
	if (location == 0u) {
		CantAttackResult cant = HandleCantAttackSubstatus();
		if (cant.f & 0x10u)
			return (CheckIfSelectedAttackIsUnusableResult){0u, cant.f, b, c, d, e, cant.hl};
		CheckIfActiveStatusResult active = CheckIfActiveCardParalyzedOrAsleep();
		if (active.f & 0x10u)
			return (CheckIfSelectedAttackIsUnusableResult){active.a, active.f, b, c, d, e, active.hl};
		DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
		d = arena.a;
		e = wSelectedAttack;
		AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(d, e);
		d = (uint8_t)(copy.de >> 8);
		e = (uint8_t)copy.de;
		c = copy.c;
		AmnesiaResult amnesia = HandleAmnesiaSubstatus();
		if (amnesia.f & 0x10u)
			return (CheckIfSelectedAttackIsUnusableResult){copy.a, amnesia.f, b, c, d, e, amnesia.hl};
		TryExecuteEffectCommandFunctionResult effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_1, b, d, e);
		if (effect.f & 0x10u)
			return (CheckIfSelectedAttackIsUnusableResult){effect.a, effect.f, effect.b, effect.c, effect.d, effect.e, effect.hl};
	}
	CheckEnergyNeededForAttackResult energy = CheckEnergyNeededForAttack();
	if (energy.f & 0x10u)
		return (CheckIfSelectedAttackIsUnusableResult){energy.a, energy.f, energy.b, energy.c, energy.d, energy.e, energy.hl};
	AttackFlagResult flag = CheckLoadedAttackFlag((uint8_t)(ATTACK_FLAG2_ADDRESS | IGNORE_THIS_ATTACK_F));
	return (CheckIfSelectedAttackIsUnusableResult){flag.a, flag.f, energy.b, energy.c, energy.d, energy.e, energy.hl};
}
/* <<< factory CheckIfSelectedAttackIsUnusable */

/* >>> factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult CheckForBenchIDAtHalfHPAndCanUseSecondAttack(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)f;
	wSamePokemonCardID = a;
	uint8_t saved_location = hTempPlayAreaLocation_ff9d;
	uint8_t saved_attack = wSelectedAttack;
	d = saved_location;
	e = saved_attack;
	DuelistVarResult arena = GetTurnDuelistVariable(0xBBu);
	b = 0u;
	c = 0u;
	hl = arena.hl;
	for (;;) {
		c = (uint8_t)(c + 1u);
		uint8_t deck_index = gb_read8(hl++);
		if (deck_index == 0xFFu)
			break;
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(0xBBu + c));
		(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		uint8_t current_hp = card.a;
		uint8_t half_max_hp = (uint8_t)((wLoadedCard1HP >> 1) | (wLoadedCard1HP << 7));
		if (half_max_hp >= current_hp || wLoadedCard1ID != wSamePokemonCardID)
			continue;
		hTempPlayAreaLocation_ff9d = c;
		wSelectedAttack = 1u;
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(1u, 0u, b, c, current_hp, deck_index, hl);
		if (unusable.f & 0x10u)
			continue;
		b = (uint8_t)(b + 1u);
	}
	wSelectedAttack = saved_attack;
	hTempPlayAreaLocation_ff9d = saved_location;
	a = b;
	f = (uint8_t)(b == 0u ? 0x80u : 0x10u);
	return (CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult){a, f, b, c, d, e, hl};
}
/* <<< factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */

/* >>> factory CountNumberOfSetUpBenchPokemon */
CountNumberOfSetUpBenchPokemonResult CountNumberOfSetUpBenchPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a;
	(void)f;
	uint8_t saved_location = hTempPlayAreaLocation_ff9d;
	uint8_t saved_attack = wSelectedAttack;
	DuelistVarResult bench = GetTurnDuelistVariable(DUELVARS_BENCH);
	b = 0u;
	c = 0u;
	hl = bench.hl;
	for (;;) {
		c = (uint8_t)(c + 1u);
		uint8_t deck_index = gb_read8(hl++);
		if (deck_index == 0xFFu)
			break;
		d = deck_index;
		(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + c));
		d = card.a;
		uint8_t half_max_hp = (uint8_t)((wLoadedCard1HP >> 1) | (wLoadedCard1HP << 7));
		if (half_max_hp >= d)
			continue;
		if ((wLoadedCard1AIInfo & HAS_EVOLUTION) != 0u) {
			CheckCardEvolutionInHandOrDeckResult evolution = CheckCardEvolutionInHandOrDeck(d);
			if ((evolution.f & 0x10u) != 0u)
				continue;
		}
		hTempPlayAreaLocation_ff9d = c;
		wSelectedAttack = SECOND_ATTACK;
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, 0u, b, c, d, deck_index, hl);
		if ((unusable.f & 0x10u) != 0u)
			continue;
		b = (uint8_t)(b + 1u);
	}
	wSelectedAttack = saved_attack;
	hTempPlayAreaLocation_ff9d = saved_location;
	a = b;
	f = (uint8_t)(b == 0u ? 0x80u : 0x10u);
	return (CountNumberOfSetUpBenchPokemonResult){a, f, b, c, saved_location, saved_attack, hl};
}
/* <<< factory CountNumberOfSetUpBenchPokemon */

/* >>> factory HandleLegendaryArticunoEnergyScoring */
void HandleLegendaryArticunoEnergyScoring(void)
{
	if (wOpponentDeckID == 0x0Eu) {
		ScoreLegendaryArticunoCards();
	}
}
/* <<< factory HandleLegendaryArticunoEnergyScoring */

/* >>> factory CheckIfArenaCardIsFullyPowered */
CheckIfArenaCardIsFullyPoweredResult CheckIfArenaCardIsFullyPowered(void)
{
	uint8_t f;
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t deck_index = arena.a;
	(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
	DuelistVarResult hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t d = hp.a;
	uint8_t a = wLoadedCard1HP;
	a = (uint8_t)((a >> 1) | (uint8_t)(a << 7));
	if (a >= d) {
		f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
		return (CheckIfArenaCardIsFullyPoweredResult){a, f};
	}
	a = (uint8_t)(wLoadedCard1AIInfo & HAS_EVOLUTION);
	if (a != 0u) {
		CheckCardEvolutionInHandOrDeckResult evolution = CheckCardEvolutionInHandOrDeck(d);
		a = evolution.a;
		f = evolution.f;
		if ((f & 0x10u) != 0u) {
			f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
			return (CheckIfArenaCardIsFullyPoweredResult){a, f};
		}
	}
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	wSelectedAttack = SECOND_ATTACK;
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, 0u, 0u, 0u, d, 0u, hp.hl);
	a = unusable.a;
	f = unusable.f;
	if ((f & 0x10u) != 0u) {
		f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
		return (CheckIfArenaCardIsFullyPoweredResult){a, f};
	}
	f = (uint8_t)((f & 0x80u) | 0x10u);
	return (CheckIfArenaCardIsFullyPoweredResult){a, f};
}
/* <<< factory CheckIfArenaCardIsFullyPowered */

/* >>> factory SendCardAttrBlkPacket */
SendCardAttrBlkPacketResult SendCardAttrBlkPacket(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)hl;
	uint16_t packet = CreateCardAttrBlkPacket(a, d, e);
	SendSGBResult result = SendSGB(a, f, b, c, d, e, packet);
	return (SendCardAttrBlkPacketResult){result.a, result.f, result.b, result.c, result.d, result.e, result.hl};
}
/* <<< factory SendCardAttrBlkPacket */

/* >>> factory ApplyBGP6OrSGB3ToCardImage */
SendCardAttrBlkPacketResult ApplyBGP6OrSGB3ToCardImage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t console = gb_read8(wConsole_ADDR);
	a = console;
	if (console == CONSOLE_DMG) {
		f = 0x80u;
		return (SendCardAttrBlkPacketResult){a, f, b, c, d, e, hl};
	}
	if (console == CONSOLE_SGB) {
		a = 0x0Cu;
		f = 0x80u;
		return SendCardAttrBlkPacket(a, f, b, c, d, e, hl);
	}
	a = 0x06u;
	f = 0x40u;
	ApplyCardCGBAttributes((uint16_t)((uint16_t)d << 8 | e));
	return (SendCardAttrBlkPacketResult){a, f, b, c, d, e, hl};
}
/* <<< factory ApplyBGP6OrSGB3ToCardImage */

/* >>> factory DrawLargePictureOfCard */
void DrawLargePictureOfCard(void)
{
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadSymbolsFont();
	SetDefaultConsolePalettes();
	wDuelDisplayedScreen = LARGE_CARD_PICTURE;
	(void)LoadCardOrDuelMenuBorderTiles();
	uint8_t header = HEADER_TRAINER;
	uint8_t type = wLoadedCard1Type;
	if (type != TYPE_TRAINER) {
		header = HEADER_ENERGY;
		if ((type & TYPE_ENERGY) == 0u)
			header = HEADER_POKEMON;
	}
	(void)LoadCardTypeHeaderTiles(header);
	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	SetBGP6OrSGB3ToCardPalette();
	FlushAllPalettesOrSendPal23Packet();
	uint16_t hl = LARGE_CARD_TILE_DATA;
	uint16_t de = 0u;
	uint8_t a = 0u;
	uint8_t b = 0u;
	uint8_t c = 0u;
	WriteDataBlocksToBGMap0(&hl, &de, &a, &b, &c);
	(void)ApplyBGP6OrSGB3ToCardImage(a, 0u, b, c, 6u, 3u, hl);
}
/* <<< factory DrawLargePictureOfCard */

/* >>> factory DrawCardPageSurroundingBox */
void DrawCardPageSurroundingBox(void)
{
	uint16_t hl = wTextBoxFrameType_ADDR;
	gb_write8(wTextBoxFrameType_ADDR, (uint8_t)(gb_read8(wTextBoxFrameType_ADDR) | 0x80u));
	DrawRegularTextBox(&hl, 0u, 20u, 18u, 0u, 0u);
	hl = wTextBoxFrameType_ADDR;
	gb_write8(wTextBoxFrameType_ADDR, (uint8_t)(gb_read8(wTextBoxFrameType_ADDR) & 0x7fu));
	SendCardAttrBlkPacketResult result = ApplyBGP6OrSGB3ToCardImage(0u, 0u, 0u, 0u, 4u, 6u, hl);
	(void)result;
}
/* <<< factory DrawCardPageSurroundingBox */

/* >>> factory PrintPokemonCardPageGenericInformation */
PrintPokemonCardPageGenericInformationResult PrintPokemonCardPageGenericInformation(void)
{
	DrawCardPageSurroundingBox();
	(void)InitTextPrinting_ProcessTextFromPointerToID(5u, 1u, wLoadedCard1Name_ADDR);

	uint8_t color;
	if (wCardPageType != 0u)
		color = GetPlayAreaCardColor(wCurPlayAreaSlot);
	else
		color = wLoadedCard1Type;

	JPWriteByteToBGMap0((uint8_t)(color + 1u), 18u, 1u);
	DrawCardPageSet2AndRarityIconsResult result = DrawCardPageSet2AndRarityIcons();
	return (PrintPokemonCardPageGenericInformationResult){result.hl};
}
/* <<< factory PrintPokemonCardPageGenericInformation */

/* >>> factory DrawDuelHUD */
void DrawDuelHUD(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	wHUDEnergyAndHPBarsX = b;
	wHUDEnergyAndHPBarsY = c;
	uint8_t name_d = d, name_e = e;
	uint8_t icon_b = (e == 0u) ? 1u : 15u, icon_c = e;
	WriteByteToBGMap0(SYM_POKEMON, icon_b, icon_c);
	icon_b++;
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	WriteByteToBGMap0((uint8_t)(count.a + SYM_0 - 1u), icon_b, icon_c);
	icon_b++;
	WriteByteToBGMap0(SYM_PRIZE, icon_b, icon_c);
	icon_b++;
	WriteByteToBGMap0((uint8_t)(CountPrizes() + SYM_0), icon_b, icon_c);
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (arena.a == 0xFFu) return;
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena.a);
	CopyCardNameAndLevelResult copied = CopyCardNameAndLevel(32u, icon_b, icon_c, name_d, name_e);
	gb_write8(copied.hl, TX_END);
	uint8_t text_d = name_d;
	if (name_e == 0u) { TextLength length = GetTextLengthInTiles(wDefaultText_ADDR); text_d = (uint8_t)(length.a + SCREEN_WIDTH); }
	InitTextPrinting(text_d, name_e);
	uint16_t text_hl = wDefaultText_ADDR; ProcessText(&text_hl);
	JPWriteByteToBGMap0((uint8_t)(GetArenaCardColor() + 1u), (uint8_t)(text_d - 1u), name_e);
	uint8_t hud_x = wHUDEnergyAndHPBarsX, hud_y = wHUDEnergyAndHPBarsY;
	PrintPlayAreaCardAttachedEnergies(hud_x, hud_y, PLAY_AREA_ARENA);
	DuelistVarResult arena_again = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena_again.a);
	uint8_t max_hp = wLoadedCard1HP, cur_hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	DrawHPBar(max_hp, cur_hp);
	uint16_t dst = BCCoordToBGMap0Address(hud_x, (uint8_t)(hud_y + 1u)), src = wDefaultText_ADDR;
	SafeCopyDataHLtoDE(&src, &dst, 6u);
	dst = (uint16_t)(dst + TILEMAP_WIDTH); src = (uint16_t)(wDefaultText_ADDR + 6u);
	SafeCopyDataHLtoDE(&src, &dst, 6u);
	uint8_t attr_b = (uint8_t)(hud_x + 6u), attr_c = (uint8_t)(hud_y + 1u);
	uint8_t plus = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER).a;
	if (plus != 0u) { WriteByteToBGMap0(SYM_PLUSPOWER, attr_b, attr_c); WriteByteToBGMap0((uint8_t)(plus + SYM_0), (uint8_t)(attr_b + 1u), attr_c); }
	uint8_t defender = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_ATTACHED_DEFENDER).a;
	if (defender != 0u) { attr_c++; WriteByteToBGMap0(SYM_DEFENDER, attr_b, attr_c); WriteByteToBGMap0((uint8_t)(defender + SYM_0), (uint8_t)(attr_b + 1u), attr_c); }
}
/* <<< factory DrawDuelHUD */

/* >>> factory DrawDuelHUDs */
void DrawDuelHUDs(void)
{
	DuelistVarResult turn = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	if (turn.a != DUELIST_TYPE_PLAYER) {
		uint8_t saved_turn = hWhoseTurn;
		hWhoseTurn = PLAYER_TURN;
		DrawDuelHUD(11u, 8u, 1u, 11u);
		DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
		CheckPrintCnfSlpPrz(status.a, 8u, 5u);
		uint8_t a = CheckPrintPoisoned(status.a, 8u, 6u);
		a = CheckPrintDoublePoisoned(a, 8u, 7u);
		SwapTurn();
		(void)GetNonTurnDuelistVariable(a);
		DrawDuelHUD(3u, 1u, 7u, 0u);
		status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
		CheckPrintCnfSlpPrz(status.a, 11u, 6u);
		a = CheckPrintPoisoned(status.a, 11u, 5u);
		(void)CheckPrintDoublePoisoned(a, 11u, 4u);
		SwapTurn();
		hWhoseTurn = saved_turn;
		return;
	}
	DrawDuelHUD(11u, 8u, 1u, 11u);
	DuelistVarResult status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	CheckPrintCnfSlpPrz(status.a, 8u, 5u);
	uint8_t a = CheckPrintPoisoned(status.a, 8u, 6u);
	a = CheckPrintDoublePoisoned(a, 8u, 7u);
	SwapTurn();
	(void)GetNonTurnDuelistVariable(a);
	DrawDuelHUD(3u, 1u, 7u, 0u);
	status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS);
	CheckPrintCnfSlpPrz(status.a, 11u, 6u);
	a = CheckPrintPoisoned(status.a, 11u, 5u);
	(void)CheckPrintDoublePoisoned(a, 11u, 4u);
	SwapTurn();
}
/* <<< factory DrawDuelHUDs */

/* >>> factory DrawCardListScreenLayout */
DrawCardListScreenLayoutResult DrawCardListScreenLayout(void)
{
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadSymbolsFont();
	TileCopyResult tiles = LoadDuelCardSymbolTiles();
	uint16_t box_hl = tiles.hl;
	DrawRegularTextBox(&box_hl, 0u, 20u, 13u, 0u, 0u);
	uint16_t image_hl = 0x0601u;
	FillRectangle(0xA0u, 8u, 6u, 0x0C0Cu, image_hl);
	(void)ApplyBGP6OrSGB3ToCardImage(0xA0u, 0u, 8u, 6u, 0x0Cu, 0x0Cu, image_hl);
	PrintSortNumberInCardList_CallFromPointer();
	uint8_t a = gb_read8(wDuelTempList_ADDR);
	if (a == 0xFFu)
		return (DrawCardListScreenLayoutResult){a, 0x90u};
	return (DrawCardListScreenLayoutResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u)};
}
/* <<< factory DrawCardListScreenLayout */

/* >>> factory ApplyBGP7OrSGB2ToCardImage */
/* core.asm:4043-4061 */
SendCardAttrBlkPacketResult ApplyBGP7OrSGB2ToCardImage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t console = gb_read8(wConsole_ADDR);
	a = console;
	if (console == CONSOLE_DMG) {
		f = 0x80u;
		return (SendCardAttrBlkPacketResult){a, f, b, c, d, e, hl};
	}
	if (console == CONSOLE_SGB) {
		/* 2 << 0 + 2 << 2 binds as (2 << 0) + (2 << 2), so the SGB byte is 0x0A. */
		a = 0x0Au;
		f = 0x80u;
		return SendCardAttrBlkPacket(a, f, b, c, d, e, hl);
	}
	a = 0x07u;
	f = 0x40u;
	ApplyCardCGBAttributes((uint16_t)((uint16_t)d << 8 | e));
	return (SendCardAttrBlkPacketResult){a, f, b, c, d, e, hl};
}
/* <<< factory ApplyBGP7OrSGB2ToCardImage */

/* >>> factory DisplayPracticeDuelPlayerHandScreen */
void DisplayPracticeDuelPlayerHandScreen(void)
{
	(void)CreateHandCardList(0u);
	EmptyScreen();
	TileCopyResult tiles = LoadDuelCardSymbolTiles();
	uint16_t box = tiles.hl;
	DrawRegularTextBox(&box, 0u, 20u, 13u, 0u, 0u);
	uint8_t count = CountCardsInDuelTempList().a;
	uint16_t params = CARD_LIST_PARAMETERS;
	PrintCardListItems(count, 0u, 0u, &params);
	InitTextPrinting(1u, 1u);
	(void)PrintTextNoDelay(DuelistHandText, 1u, 1u);
	EnableLCD();
}
/* <<< factory DisplayPracticeDuelPlayerHandScreen */

/* >>> factory DrawDuelMainScene */
void DrawDuelMainScene(void)
{
	uint8_t saved_turn = 0u;
	uint8_t restore_turn = 0u;
	DuelistVarResult result = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	if (result.a != DUELIST_TYPE_PLAYER) {
		saved_turn = gb_read8(hWhoseTurn_ADDR);
		gb_write8(hWhoseTurn_ADDR, PLAYER_TURN);
		restore_turn = 1u;
	}
	if (gb_read8(wDuelDisplayedScreen_ADDR) == DUEL_MAIN_SCENE) {
		if (restore_turn != 0u) {
			gb_write8(hWhoseTurn_ADDR, saved_turn);
			return;
		}
		return;
	}
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadSymbolsFont();
	gb_write8(wDuelDisplayedScreen_ADDR, DUEL_MAIN_SCENE);
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	LoadPlayAreaCardGfx(result.a, 0x8500u);
	SetBGP7OrSGB2ToCardPalette();
	SwapTurn();
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	LoadPlayAreaCardGfx(result.a, 0x8200u);
	SetBGP6OrSGB3ToCardPalette();
	FlushAllPalettesOrSendPal23Packet();
	SwapTurn();
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		FillRectangle(0xD0u, 8u, 6u, 0x0005u, 0x0601u);
		(void)ApplyBGP7OrSGB2ToCardImage(0xD0u, 0u, 8u, 6u, 0u, 5u, 0x0601u);
	}
	SwapTurn();
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		FillRectangle(0xA0u, 8u, 6u, 0x0C01u, 0x0601u);
		(void)ApplyBGP6OrSGB3ToCardImage(0xA0u, 0u, 8u, 6u, 0x0Cu, 1u, 0x0601u);
	}
	SwapTurn();
	uint16_t tile_data = 0u;
	uint16_t bg_map = 0u;
	uint8_t a = 0u, b = 0u, c = 0u;
	WriteDataBlocksToBGMap0(&tile_data, &bg_map, &a, &b, &c);
	DrawDuelHorizontalSeparator();
	DrawDuelHUDs();
	(void)DrawWideTextBox();
	EnableLCD();
	/* C helpers reuse wDuelDisplayedScreen internally; the asm leaves it as
	 * DUEL_MAIN_SCENE after rebuilding the scene. */
	gb_write8(wDuelDisplayedScreen_ADDR, DUEL_MAIN_SCENE);
	if (restore_turn != 0u)
		gb_write8(hWhoseTurn_ADDR, saved_turn);
}
/* <<< factory DrawDuelMainScene */

/* >>> factory InitAndDrawCardListScreenLayout */
DrawCardListScreenLayoutResult InitAndDrawCardListScreenLayout(void)
{
	wSelectedDuelSubMenuItem = 0u;
	wSortCardListByID = 0u;
	wPrintSortNumberInCardListPtr = 0u;
	gb_write8(wPrintSortNumberInCardListPtr_ADDR + 1u, 0u);
	wCardListItemSelectionMenuType = 0u;
	wNoItemSelectionMenuKeys = 0x08u;
	wCardListInfoBoxText = (uint8_t)(PleaseSelectHandText & 0xFFu);
	gb_write8(wCardListInfoBoxText_ADDR + 1u, (uint8_t)(PleaseSelectHandText >> 8));
	wCardListHeaderText = (uint8_t)(DuelistHandText & 0xFFu);
	gb_write8(wCardListHeaderText_ADDR + 1u, (uint8_t)(DuelistHandText >> 8));
	return DrawCardListScreenLayout();
}
/* <<< factory InitAndDrawCardListScreenLayout */

/* >>> factory RedrawTurnDuelistsDuelHUD */
void RedrawTurnDuelistsDuelHUD(void)
{
	if (hWhoseTurn == wWhoseTurn) {
		DrawDuelHUDs();
		return;
	}
	SwapTurn();
	DrawDuelHUDs();
	SwapTurn();
}
/* <<< factory RedrawTurnDuelistsDuelHUD */

/* >>> factory OppAction_DrawDuelMainScene */
void OppAction_DrawDuelMainScene(void)
{
	DrawDuelMainScene();
}
/* <<< factory OppAction_DrawDuelMainScene */

/* >>> factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu */
DrawCardListScreenLayoutResult InitAndDrawCardListScreenLayout_WithSelectCheckMenu(void)
{
	DrawCardListScreenLayoutResult result = InitAndDrawCardListScreenLayout();
	gb_write8(wCardListItemSelectionMenuType_ADDR, SELECT_CHECK);
	return (DrawCardListScreenLayoutResult){SELECT_CHECK, result.f};
}
/* <<< factory InitAndDrawCardListScreenLayout_WithSelectCheckMenu */

/* >>> factory DisplayCardListDetails */
DisplayCardListDetailsResult DisplayCardListDetails(void)
{
	uint8_t value = gb_read8(wDuelTempList_ADDR);
	if (value == 0xFFu) {
		uint8_t f = (uint8_t)(0x40u | (((value & 0x0Fu) < 0x0Fu) ? 0x20u : 0u) | ((value < 0xFFu) ? 0x10u : 0u) | 0x80u);
		return (DisplayCardListDetailsResult){value, f};
	}
	(void)InitAndDrawCardListScreenLayout();
	uint8_t count = CountCardsInDuelTempList().a;
	uint16_t params = CARD_LIST_PARAMETERS;
	PrintCardListItems(count, 0u, 0u, &params);
	InitTextPrinting(1u, 1u);
	(void)PrintTextNoDelay(TheCardYouReceivedText, 1u, 1u);
	(void)DrawWideTextBox_WaitForInput(YouReceivedTheseCardsText);
	return (DisplayCardListDetailsResult){value, 0u};
}
/* <<< factory DisplayCardListDetails */

/* >>> factory OppAction_FinishTurnWithoutAttacking */
void OppAction_FinishTurnWithoutAttacking(void)
{
	DrawDuelMainScene();
	ClearNonTurnTemporaryDuelvars();
	(void)DrawWideTextBox_WaitForInput(FinishedTurnWithoutAttackingText);
	wOpponentTurnEnded = 1u;
}
/* <<< factory OppAction_FinishTurnWithoutAttacking */

/* >>> factory RedrawTurnDuelistsMainSceneOrDuelHUD */
void RedrawTurnDuelistsMainSceneOrDuelHUD(void)
{
	if (wDuelDisplayedScreen == DUEL_MAIN_SCENE) {
		RedrawTurnDuelistsDuelHUD();
		return;
	}
	if (hWhoseTurn == wWhoseTurn) {
		DrawDuelMainScene();
		return;
	}
	SwapTurn();
	DrawDuelMainScene();
	SwapTurn();
}
/* <<< factory RedrawTurnDuelistsMainSceneOrDuelHUD */

/* >>> factory DisplayNoBasicPokemonInHandScreen */
void DisplayNoBasicPokemonInHandScreen(void)
{
	EmptyScreen();
	TileCopyResult tiles = LoadDuelCardSymbolTiles();
	uint16_t box = tiles.hl;
	DrawRegularTextBox(&box, 0u, 20u, 18u, 0u, 0u);
	(void)CreateHandCardList(0u);
	uint8_t count = CountCardsInDuelTempList().a;
	uint16_t params = NoBasicPokemonCardListParameters;
	PrintCardListItems(count, 0u, 0u, &params);
	InitTextPrinting(1u, 1u);
	(void)PrintTextNoDelay(DuelistHandText, 1u, 1u);
	EnableLCD();
	(void)WaitForWideTextBoxInput();
}
/* <<< factory DisplayNoBasicPokemonInHandScreen */

/* >>> factory PrintAndLoadAttacksToDuelTempList */
static uint8_t check_attack_slot_empty_or_pkmn_power(uint16_t de)
{
	uint8_t lo = gb_read8(de);
	uint8_t hi = gb_read8((uint16_t)(de + 1u));
	if ((uint8_t)(lo | hi) == 0u)
		return 1u;
	uint8_t category = gb_read8((uint16_t)(de + (CARD_DATA_ATTACK1_CATEGORY - CARD_DATA_ATTACK1_NAME + 1u)));
	category = (uint8_t)(category & (uint8_t)~RESIDUAL);
	return (uint8_t)(category == POKEMON_POWER);
}

uint8_t PrintAndLoadAttacksToDuelTempList(void)
{
	(void)DrawWideTextBox();
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t card_index = arena.a;
	gb_write8(hTempCardIndex_ff98_ADDR, card_index);
	(void)LoadCardDataToBuffer1_FromDeckIndex(card_index);
	uint8_t c = 0u;
	uint8_t b = 13u;
	uint16_t hl = wDuelTempList_ADDR;
	gb_write8(wCardPageNumber_ADDR, 0u);
	if (!check_attack_slot_empty_or_pkmn_power(wLoadedCard1Atk1Name_ADDR)) {
		gb_write8(hl++, card_index);
		gb_write8(hl++, 0u);
		c = (uint8_t)(c + 1u);
		(void)PrintAttackOrPkmnPowerInformation(b, c, 0u, b, wLoadedCard1Atk1Name_ADDR);
		b = (uint8_t)(b + 2u);
	}
	if (!check_attack_slot_empty_or_pkmn_power(wLoadedCard1Atk2Name_ADDR)) {
		gb_write8(hl++, card_index);
		gb_write8(hl++, 1u);
		c = (uint8_t)(c + 1u);
		(void)PrintAttackOrPkmnPowerInformation(b, c, 0u, b, wLoadedCard1Atk2Name_ADDR);
	}
	return c;
}
/* <<< factory PrintAndLoadAttacksToDuelTempList */

/* >>> factory DisplayPokemonAttackCardPage */
void DisplayPokemonAttackCardPage(uint8_t b, uint8_t c, uint8_t d, uint16_t de, uint16_t hl)
{
	(void)PrintPokemonCardPageGenericInformation();
	PrintAttackOrPkmnPowerInformationResult printed = PrintAttackOrPkmnPowerInformation(b, c, d, 2u, hl);
	(void)printed;
	PrintAttackOrNonPokemonCardDescription(de, 1u, 11u);
}
/* <<< factory DisplayPokemonAttackCardPage */

/* >>> factory DisplayCardPage_PokemonAttack2Page2 */
void DisplayCardPage_PokemonAttack2Page2(uint8_t b, uint8_t c, uint8_t d)
{
	DisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u), wLoadedCard1Atk2Name_ADDR);
}
/* <<< factory DisplayCardPage_PokemonAttack2Page2 */

/* >>> factory DisplayCardPage_PokemonAttack1Page1 */
void DisplayCardPage_PokemonAttack1Page1(uint8_t b, uint8_t c, uint8_t d)
{
	DisplayPokemonAttackCardPage(b, c, d, wLoadedCard1Atk1Description_ADDR, wLoadedCard1Atk1Name_ADDR);
}
/* <<< factory DisplayCardPage_PokemonAttack1Page1 */

/* >>> factory DisplayCardPage_PokemonAttack1Page2 */
void DisplayCardPage_PokemonAttack1Page2(uint8_t b, uint8_t c, uint8_t d)
{
	DisplayPokemonAttackCardPage(b, c, d, (uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u), wLoadedCard1Atk1Name_ADDR);
}
/* <<< factory DisplayCardPage_PokemonAttack1Page2 */

/* >>> factory DisplayCardPage_PokemonAttack2Page1 */
void DisplayCardPage_PokemonAttack2Page1(uint8_t b, uint8_t c, uint8_t d)
{
	DisplayPokemonAttackCardPage(b, c, d, wLoadedCard1Atk2Description_ADDR, wLoadedCard1Atk2Name_ADDR);
}
/* <<< factory DisplayCardPage_PokemonAttack2Page1 */

/* >>> factory DisplayAttackPage_Attack1Page1 */
void DisplayAttackPage_Attack1Page1(uint8_t b, uint8_t c, uint8_t d)
{
	DisplayCardPage_PokemonAttack1Page1(b, c, d);
	SwitchAttackPage();
}
/* <<< factory DisplayAttackPage_Attack1Page1 */

/* >>> factory DisplayAttackPage_Attack2Page1 */
void DisplayAttackPage_Attack2Page1(uint8_t b, uint8_t c, uint8_t d)
{
	DisplayCardPage_PokemonAttack2Page1(b, c, d);
	SwitchAttackPage();
}
/* <<< factory DisplayAttackPage_Attack2Page1 */

/* >>> factory DisplayAttackPage_Attack2Page2 */
void DisplayAttackPage_Attack2Page2(uint8_t b, uint8_t c, uint8_t d)
{
	uint8_t lo = gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 2u));
	uint8_t hi = gb_read8((uint16_t)(wLoadedCard1Atk2Description_ADDR + 3u));
	if ((uint8_t)(lo | hi) == 0u)
		return;
	DisplayCardPage_PokemonAttack2Page2(b, c, d);
	SwitchAttackPage();
}
/* <<< factory DisplayAttackPage_Attack2Page2 */

/* >>> factory DisplayAttackPage_Attack1Page2 */
void DisplayAttackPage_Attack1Page2(uint8_t b, uint8_t c, uint8_t d)
{
	uint8_t lo = gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 2u));
	uint8_t hi = gb_read8((uint16_t)(wLoadedCard1Atk1Description_ADDR + 3u));
	if ((uint8_t)(lo | hi) == 0u)
		return;
	DisplayCardPage_PokemonAttack1Page2(b, c, d);
	SwitchAttackPage();
}
/* <<< factory DisplayAttackPage_Attack1Page2 */

/* >>> factory DisplayEnergyDiscardMenu */
void DisplayEnergyDiscardMenu(void)
{
	uint16_t box_hl = 0u;
	DrawRegularTextBox(&box_hl, 0u, 20u, 10u, 0u, 3u);
	(void)DrawWideTextBox_PrintTextNoDelay(ChooseEnergyCardToDiscardText);
	EnableLCD();
	uint8_t count = CountCardsInDuelTempList().a;
	uint16_t params = EnergyDiscardCardListParameters;
	PrintCardListItems(count, 0u, 0u, &params);
	wCardListIndicatorYPosition = 4u;
}
/* <<< factory DisplayEnergyDiscardMenu */

/* >>> factory DisplayEnergyDiscardScreen */
void DisplayEnergyDiscardScreen(uint8_t a)
{
	wEnergyDiscardPlayAreaLocation = a;
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelFaceDownCardTiles();
	a = wEnergyDiscardPlayAreaLocation;
	wCurPlayAreaSlot = a;
	wCurPlayAreaY = 0u;
	(void)PrintPlayAreaCardInformation();
	wEnergyDiscardMenuNumerator = 0u;
	wEnergyDiscardMenuDenominator = 1u;
	DisplayEnergyDiscardMenu();
}
/* <<< factory DisplayEnergyDiscardScreen */

/* >>> factory OpenAttackPage */
static void SetOBP1OrSGB3ToCardPalette(void)
{
	wOBP0 = 0xE4u;
	uint8_t console = gb_read8(wConsole_ADDR);
	if (console == CONSOLE_DMG)
		return;
	if (console == CONSOLE_SGB) {
		SetSGB3ToCardPalette();
		return;
	}
	CopyCGBCardPalette(0x09u);
}

void OpenAttackPage(void)
{
	wCardPageNumber = CARDPAGE_POKEMON_OVERVIEW;
	wCurPlayAreaSlot = 0u;
	EmptyScreen();
	FinishQueuedAnimations();
	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	SetOBP1OrSGB3ToCardPalette();
	SetBGP6OrSGB3ToCardPalette();
	FlushAllPalettesOrSendPal23Packet();

	uint16_t oam_hl = 0u;
	uint16_t oam_de = (uint16_t)((0x38u << 8) | 0x30u);
	(void)PlaceCardImageOAM(&oam_hl, &oam_de);
	(void)ApplyBGP6OrSGB3ToCardImage(0u, 0u, 0u, 0u, 6u, 4u, 0u);

	uint8_t item = hCurMenuItem;
	wSelectedDuelSubMenuItem = item;
	uint8_t idx = (uint8_t)(item * 2u);
	uint8_t v = gb_read8((uint16_t)(wDuelTempList_ADDR + 1u + idx));
	wAttackPageNumber = (v != 0u) ? ATTACKPAGE_ATTACK2_1 : ATTACKPAGE_ATTACK1_1;

	for (;;) {
		DisplayAttackPage();
		EnableLCD();
		for (;;) {
			DoFrame();
			if ((hDPadHeld & (PAD_RIGHT | PAD_LEFT)) != 0u)
				break;
			if ((hKeysPressed & (PAD_A | PAD_B)) != 0u)
				return;
		}
	}
}
/* <<< factory OpenAttackPage */

/* >>> factory HandleEnergyDiscardMenuInput */
HandleEnergyDiscardMenuInputResult HandleEnergyDiscardMenuInput(void)
{
	uint8_t b = 16u;
	uint8_t c = 16u;
	uint8_t denominator = gb_read8(wEnergyDiscardMenuDenominator_ADDR);
	uint8_t numerator = gb_read8(wEnergyDiscardMenuNumerator_ADDR);
	if (denominator != 0u) {
		WriteByteToBGMap0((uint8_t)(numerator + SYM_0), b, c);
		b = (uint8_t)(b + 1u);
		WriteByteToBGMap0(SYM_SLASH, b, c);
		b = (uint8_t)(b + 1u);
		WriteByteToBGMap0((uint8_t)(denominator + SYM_0), b, c);
	} else {
		b = (uint8_t)(b + 1u);
		WriteTwoDigitNumberInTxSymbol_PadSpace(numerator, b, c, 0u, 0u, 0u);
	}
	HandleCardListInputResult input;
	do {
		DoFrame();
		input = HandleCardListInput();
	} while ((input.f & 0x10u) == 0u);
	if (input.a == MENU_CANCEL)
		return (HandleEnergyDiscardMenuInputResult){input.a, 0x90u};
	DeckCardResult card = GetCardInDuelTempList_OnlyDeckIndex(input.a, 0u);
	return (HandleEnergyDiscardMenuInputResult){card.a, (card.a == 0u) ? 0x80u : 0u};
}
/* <<< factory HandleEnergyDiscardMenuInput */

/* >>> factory DisplayRetreatScreen */
void DisplayRetreatScreen(uint8_t a)
{
	hTempRetreatCostCards = 0xFFu;
	uint8_t required = wEnergyCardsRequiredToRetreat;
	if (required == 0u)
		return;
	wNumRetreatEnergiesSelected = 0u;
	(void)CreateArenaOrBenchEnergyCardList(a);
	(void)SortCardsInDuelTempListByID(0u, 0u, wDuelTempList_ADDR);
	wTempRetreatCostCardsPos = (uint8_t)hTempRetreatCostCards_ADDR;
	DisplayEnergyDiscardScreen(PLAY_AREA_ARENA);
	wEnergyDiscardMenuDenominator = required;
	for (;;) {
		wEnergyDiscardMenuNumerator = wNumRetreatEnergiesSelected;
		HandleEnergyDiscardMenuInputResult input = HandleEnergyDiscardMenuInput();
		if ((input.f & 0x10u) != 0u)
			return;
		hTempCardIndex_ff98 = input.a;
		(void)LoadCardDataToBuffer2_FromDeckIndex(hTempCardIndex_ff98);
		uint8_t pos = wTempRetreatCostCardsPos;
		wTempRetreatCostCardsPos = (uint8_t)(pos + 1u);
		gb_write8((uint16_t)(0xFF00u + pos), hTempCardIndex_ff98);
		uint8_t amount = 1u;
		if (wLoadedCard2Type == TYPE_ENERGY_DOUBLE_COLORLESS)
			amount++;
		wNumRetreatEnergiesSelected = (uint8_t)(wNumRetreatEnergiesSelected + amount);
		if (wNumRetreatEnergiesSelected >= wEnergyCardsRequiredToRetreat) {
			gb_write8((uint16_t)(0xFF00u + wTempRetreatCostCardsPos), 0xFFu);
			return;
		}
		(void)RemoveCardFromDuelTempList(hTempCardIndex_ff98);
		DisplayEnergyDiscardMenu();
	}
}
/* <<< factory DisplayRetreatScreen */

/* >>> factory PrintPracticeDuelInstructions_Fast */
void PrintPracticeDuelInstructions_Fast(uint16_t hl)
{
	for (;;) {
		uint8_t count = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (count == 0u) {
			PrintPracticeDuelLetsPlayTheGame();
			return;
		}
		PrintPracticeDuelNumberedInstructionResult r = PrintPracticeDuelNumberedInstruction(1u, count, hl);
		hl = r.hl;
	}
}
/* <<< factory PrintPracticeDuelInstructions_Fast */

/* >>> factory PracticeDuel_RepeatInstructions */
uint8_t PracticeDuel_RepeatInstructions(void)
{
	PrintPracticeDuelDrMasonInstructions(FollowMyGuidancePracticeDuelText);
	BankswitchSRAM(sBackupCurrentDuel_BANK);
	LoadSavedDuelDataFromDE(sBackupCurrentDuel_ADDR);
	BankswitchSRAM(0u);
	/* `xor a` for the SRAM0 bank leaves Z set and the trailing `scf` does not
	 * clear it, so the caller sees Z|C, not carry alone. */
	return 0x90u;
}
/* <<< factory PracticeDuel_RepeatInstructions */

/* >>> factory _DisplayCardDetailScreen */
WaitResult _DisplayCardDetailScreen(uint16_t hl)
{
	uint16_t saved_hl = hl;
	DrawLargePictureOfCard();
	CopyCardNameAndLevelResult name = CopyCardNameAndLevel(18u, 0u, 0u, 6u, 3u);
	gb_write8(name.hl, 0u);
	LoadTxRam2(0u);
	WaitResult waited = DrawWideTextBox_WaitForInput(saved_hl);
	return waited;
}
/* <<< factory _DisplayCardDetailScreen */

/* >>> factory OpenCardPage */
void OpenCardPage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wCardPageType_ADDR, a);
	(void)f;
	(void)c;
	(void)d;
	(void)e;
	(void)hl;
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	FinishQueuedAnimations();
	TileCopyResult tiles = LoadDuelCardSymbolTiles();
	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	SetOBP1OrSGB3ToCardPalette();
	SetBGP6OrSGB3ToCardPalette();
	FlushAllPalettesOrSendPal23Packet();
	uint16_t oam_hl = tiles.hl;
	uint16_t oam_de = (uint16_t)((0x38u << 8) | 0x30u);
	uint8_t place_a = PlaceCardImageOAM(&oam_hl, &oam_de);
	SendCardAttrBlkPacketResult image =
		ApplyBGP6OrSGB3ToCardImage(place_a, 0u, b, 0u, 6u, 4u, oam_hl);
	b = image.b;
	gb_write8(wCardPageNumber_ADDR, 0u);
	for (;;) {
		CardPageNavigationResult page = DisplayFirstOrNextCardPage(b);
		if ((page.f & 0x10u) != 0u)
			return;
		EnableLCD();
		for (;;) {
			DoFrame();
			if ((gb_read8(wCardPageExitKeys_ADDR) & hDPadHeld) != 0u)
				return;
			uint8_t pressed = (uint8_t)(hKeysPressed & (PAD_START | PAD_A));
			if (pressed != 0u)
				break;
			pressed = (uint8_t)(hKeysPressed & (PAD_RIGHT | PAD_LEFT));
			if (pressed != 0u)
				DisplayCardPageOnLeftOrRightPressed(pressed);
		}
	}
}
/* <<< factory OpenCardPage */

/* >>> factory DisplayCardDetailScreen */
WaitResult DisplayCardDetailScreen(uint8_t a, uint16_t hl)
{
	/* LoadCardDataToBuffer1_FromDeckIndex preserves hl, so the caller's hl is
	 * what reaches the screen routine. */
	(void)LoadCardDataToBuffer1_FromDeckIndex(a);
	return _DisplayCardDetailScreen(hl);
}
/* <<< factory DisplayCardDetailScreen */

/* >>> factory OpenCardPage_FromHand */
void OpenCardPage_FromHand(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wCardPageExitKeys_ADDR, PAD_B);
	a = 0u;
	OpenCardPage(a, f, b, c, d, e, hl);
}
/* <<< factory OpenCardPage_FromHand */

/* >>> factory OpenCardPage_FromCheckPlayArea */
void OpenCardPage_FromCheckPlayArea(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wCardPageExitKeys_ADDR, PAD_B);
	OpenCardPage(1u, f, b, c, d, e, hl);
}
/* <<< factory OpenCardPage_FromCheckPlayArea */

/* >>> factory DisplayUsedTrainerCardDetailScreen */
WaitResult DisplayUsedTrainerCardDetailScreen(void)
{
	return DisplayCardDetailScreen(hTempCardIndex_ff9f, UsedText);
}
/* <<< factory DisplayUsedTrainerCardDetailScreen */

/* >>> factory DisplayNoBasicPokemonInHandScreenAndText */
DisplayNoBasicPokemonInHandScreenAndTextResult DisplayNoBasicPokemonInHandScreenAndText(void)
{
	(void)DrawWideTextBox_WaitForInput(ThereAreNoBasicPokemonInHand);
	DisplayNoBasicPokemonInHandScreen();
	PrintReturnCardsToDeckDrawAgainResult result = PrintReturnCardsToDeckDrawAgain();
	return (DisplayNoBasicPokemonInHandScreenAndTextResult){result.a, result.b, result.c, result.f, result.hl, result.de};
}
/* <<< factory DisplayNoBasicPokemonInHandScreenAndText */

/* >>> factory OpenCardPage_FromCheckHandOrDiscardPile */
void OpenCardPage_FromCheckHandOrDiscardPile(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	gb_write8(wCardPageExitKeys_ADDR, (uint8_t)(PAD_B | PAD_UP | PAD_DOWN));
	a = 0u;
	OpenCardPage(a, f, b, c, d, e, hl);
}
/* <<< factory OpenCardPage_FromCheckHandOrDiscardPile */

/* >>> factory CardListItemSelectionMenu */
CardListItemSelectionMenuResult CardListItemSelectionMenu(void)
{
	uint8_t menu_type = wCardListItemSelectionMenuType;
	if (menu_type == 0u)
		return (CardListItemSelectionMenuResult){0u, 0x80u};
	uint16_t text = SelectCheckText;
	if (menu_type == PLAY_CHECK) {
		(void)LoadCardDataToBuffer1_FromDeckIndex(hTempCardIndex_ff98);
		text = PlayCheck2Text;
		if (wLoadedCard1Type == TYPE_TRAINER)
			text = PlayCheck1Text;
	}
	(void)DrawNarrowTextBox_PrintTextNoDelay(text);
	uint16_t parameters = 0x0E01u;
	InitializeMenuParameters(0u, &parameters);
	for (;;) {
		DoFrame();
		HandleMenuInputResult input = HandleMenuInput();
		if ((input.f & 0x10u) == 0u)
			continue;
		if (input.a == MENU_CANCEL)
			return (CardListItemSelectionMenuResult){input.a, 0x10u};
		if (input.a == 0u)
			return (CardListItemSelectionMenuResult){input.a, 0x80u};
		(void)LoadCardDataToBuffer1_FromDeckIndex(hTempCardIndex_ff98);
		OpenCardPage_FromHand(input.a, input.f, 0u, 0u, 0u, 0u, text);
		DrawCardListScreenLayoutResult screen = DrawCardListScreenLayout();
		return (CardListItemSelectionMenuResult){screen.a, 0x10u};
	}
}
/* <<< factory CardListItemSelectionMenu */

/* >>> factory DisplayPlayerDrawCardScreen */
WaitResult DisplayPlayerDrawCardScreen(void)
{
	return DisplayCardDetailScreen(hTempCardIndex_ff98, YouDrewText);
}
/* <<< factory DisplayPlayerDrawCardScreen */

/* >>> factory OppAction_PlayTrainerCard */
void OppAction_PlayTrainerCard(void)
{
	(void)LoadNonPokemonCardEffectCommands();
	(void)DisplayUsedTrainerCardDetailScreen();
	PrintUsedTrainerCardDescription();
	(void)ExchangeRNG(0u, 0u, 0u, 0u);
	gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);
}
/* <<< factory OppAction_PlayTrainerCard */

/* >>> factory OpenActivePokemonScreen */
void OpenActivePokemonScreen(void)
{
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (arena.a == 0xFFu)
		return;
	uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
	LoadCardDataToBuffer1_FromCardID((uint8_t)card_id);
	wCurPlayAreaSlot = 0u;
	wCurPlayAreaY = 0u;
	OpenCardPage_FromCheckPlayArea(0u, 0u, 0u, 0u, 0u, (uint8_t)card_id, card_id);
}
/* <<< factory OpenActivePokemonScreen */

/* >>> factory DisplayPlayAreaScreenToUsePkmnPower */
void DisplayPlayAreaScreenToUsePkmnPower(void)
{
	/* DisplayPlayAreaScreenToUsePkmnPower */
	gb_write8(wSelectedDuelSubMenuItem_ADDR, 0u);
draw_screen:
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelCheckPokemonScreenTiles();
	SetListPointer(wDuelTempList_ADDR);
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t b = 0u;
	do {
		gb_write8(wHUDEnergyAndHPBarsX_ADDR, b);
		gb_write8(wCurPlayAreaY_ADDR, (uint8_t)(b + b + b));
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(b + DUELVARS_ARENA_CARD));
		SetNextElementOfList(card.a);
		PrintPlayAreaCardHeader();
		PrintPlayAreaCardLocation();
		if (wLoadedCard1Atk1Category == POKEMON_POWER) {
			uint8_t y = (uint8_t)(wCurPlayAreaY + 1u);
			(void)InitTextPrinting_ProcessTextFromPointerToID(4u, y, wLoadedCard1Atk1Name_ADDR);
		}
		SetNextElementOfList(wLoadedCard1Atk1Category);
		++b;
	} while (b != count);
	gb_write8(wNumPlayAreaItems_ADDR, b);
	EnableLCD();
	for (;;) {
		DoFrame();
		HandleMenuInputResult input = HandleMenuInput();
		gb_write8(hTempPlayAreaLocation_ff9d_ADDR, input.a);
		gb_write8(wHUDEnergyAndHPBarsX_ADDR, input.a);
		if ((input.f & 0x10u) == 0u)
			continue;
		if (input.a == MENU_CANCEL) {
			return;
		}
		gb_write8(wSelectedDuelSubMenuItem_ADDR, input.a);
		if ((hKeysPressed & PAD_START) != 0u) {
			uint8_t item = (uint8_t)(hCurMenuItem + DUELVARS_ARENA_CARD);
			DuelistVarResult arena = GetTurnDuelistVariable(item);
			uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
			LoadCardDataToBuffer1_FromCardID((uint8_t)card_id);
			OpenCardPage_FromCheckPlayArea(0u, 0u, 0u, 0u, 0u, (uint8_t)card_id, card_id);
			goto draw_screen;
		}
		uint8_t menu_item = hCurMenuItem;
		uint16_t list_entry = (uint16_t)(wDuelTempList_ADDR + 1u + (uint16_t)(menu_item + menu_item));
		uint8_t category = gb_read8(list_entry);
		if (category != POKEMON_POWER)
			continue;
		gb_write8(hTempCardIndex_ff98_ADDR, gb_read8((uint16_t)(list_entry - 1u)));
		(void)CopyAttackDataAndDamage_FromDeckIndex(gb_read8(hTempCardIndex_ff98_ADDR), FIRST_ATTACK_OR_PKMN_POWER);
		DisplayUsePokemonPowerScreen();
		TryExecuteEffectCommandFunctionResult effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_1, 0u, 0u, 0u);
		if ((effect.f & 0x10u) != 0u) {
			(void)DrawWideTextBox_WaitForInput(PokemonPowerSelectNotRequiredText);
			goto draw_screen;
		}
		HandleYesOrNoMenuResult answer = YesOrNoMenuWithText(UseThisPokemonPowerText);
		if ((answer.f & 0x10u) != 0u)
			goto draw_screen;
		gb_write8(hTemp_ffa0_ADDR, gb_read8(hTempCardIndex_ff98_ADDR));
		return;
	}
}
/* <<< factory DisplayPlayAreaScreenToUsePkmnPower */

/* >>> factory DisplayCardPage_PokemonOverview */
void DisplayCardPage_PokemonOverview(void)
{
	uint8_t page_type = gb_read8(wCardPageType_ADDR);
	uint8_t b, c, e, retreat;
	uint16_t hl, de;
	uint8_t data_a, data_b, data_c;
	if (page_type != CARDPAGETYPE_NOT_PLAY_AREA) {
		DrawCardPageSurroundingBox();
		(void)LoadDuelCheckPokemonScreenTiles();
		(void)PlaceTextItems(CARD_PAGE_RETREAT_WR_TEXT_DATA);
		hl = CARD_PAGE_NO_TEXT_TILE_DATA;
		de = 0u; data_a = 0u; data_b = 0u; data_c = 0u;
		WriteDataBlocksToBGMap0(&hl, &de, &data_a, &data_b, &data_c);
		gb_write8(wCurPlayAreaY_ADDR, 1u);
		(void)DrawCardPageSet2AndRarityIcons();
		PrintPlayAreaCardInformationAndLocation();
	} else {
		(void)PrintPokemonCardPageGenericInformation();
		(void)PlaceTextItems(CARD_PAGE_RETREAT_WR_TEXT_DATA);
		hl = CARD_PAGE_LV_HP_NO_TEXT_TILE_DATA;
		de = 0u; data_a = 0u; data_b = 0u; data_c = 0u;
		WriteDataBlocksToBGMap0(&hl, &de, &data_a, &data_b, &data_c);
		DrawCardSymbol(3u, 2u);
		if (gb_read8(wLoadedCard1Stage_ADDR) != 0u)
			(void)InitTextPrinting_ProcessTextFromPointerToID(1u, 3u, wLoadedCard1PreEvoName_ADDR);
		WriteTwoDigitNumberInTxSymbol_PadSpace(gb_read8(wLoadedCard1Level_ADDR), 12u, 2u, 0u, 0u, 0u);
		WriteOneByteNumberInTxSymbol_PadSpace(gb_read8(wLoadedCard1HP_ADDR), 16u, 2u, 0u, 0u, 0u);
	}
	WriteOneByteNumberInTxSymbol_PadSpace(gb_read8(wLoadedCard1PokedexNumber_ADDR), 16u, 16u, 0u, 0u, 0u);
	c = 10u;
	(void)PrintAttackOrPkmnPowerInformation(5u, c, 0u, c, wLoadedCard1Atk1Name_ADDR);
	c = 12u;
	(void)PrintAttackOrPkmnPowerInformation(5u, c, 0u, c, wLoadedCard1Atk2Name_ADDR);
	c = 14u;
	retreat = gb_read8(wLoadedCard1RetreatCost_ADDR);
	e = (uint8_t)(retreat + 1u);
	b = 8u;
	while (e != 0u) {
		e = (uint8_t)(e - 1u);
		if (e == 0u)
			break;
		JPWriteByteToBGMap0(SYM_COLORLESS, b, c);
		b = (uint8_t)(b + 1u);
	}
	c = 15u;
	if (page_type != CARDPAGETYPE_NOT_PLAY_AREA && gb_read8(wCurPlayAreaSlot_ADDR) == 0u) {
		retreat = GetArenaCardWeakness();
		e = GetArenaCardResistance();
	} else {
		retreat = gb_read8(wLoadedCard1Weakness_ADDR);
		e = gb_read8(wLoadedCard1Resistance_ADDR);
	}
	PrintCardPageWeaknessesOrResistances(retreat, 8u, c);
	PrintCardPageWeaknessesOrResistances(e, 8u, 16u);
}
/* <<< factory DisplayCardPage_PokemonOverview */

/* >>> factory DisplayEnergyOrTrainerCardPage */
PrintAttackOrCardDescriptionResult DisplayEnergyOrTrainerCardPage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t saved_hl = hl;
	TileCopyResult tiles = LoadCardTypeHeaderTiles(a);
	uint16_t box_hl = tiles.hl;
	DrawRegularTextBox(&box_hl, 0u, 20u, 18u, 0u, 0u);
	ProcessTextHeaderResult text = InitTextPrinting_ProcessTextFromPointerToID(4u, 3u, wLoadedCard1Name_ADDR);
	a = text.a; d = text.d; e = text.e; f = text.f; hl = text.hl;
	d = 6u; e = 4u;
	SendCardAttrBlkPacketResult image = ApplyBGP6OrSGB3ToCardImage(a, f, b, c, d, e, hl);
	a = image.a; f = image.f; b = image.b; c = image.c; d = image.d; e = image.e; hl = image.hl;
	FillRectangle(0xE0u, 8u, 2u, 0x0601u, 0x0108u);
	DrawCardPageSet2AndRarityIconsResult icons = DrawCardPageSet2AndRarityIcons();
	hl = icons.hl;
	d = 18u; e = 9u;
	return PrintAttackOrNonPokemonCardDescription(saved_hl, d, e);
}
/* <<< factory DisplayEnergyOrTrainerCardPage */

/* >>> factory DisplayCardPage_Energy */
PrintAttackOrCardDescriptionResult DisplayCardPage_Energy(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	PrintAttackOrCardDescriptionResult result = DisplayEnergyOrTrainerCardPage(HEADER_ENERGY, f, b, c, d, e, wLoadedCard1NonPokemonDescription_ADDR);
	return result;
}
/* <<< factory DisplayCardPage_Energy */

/* >>> factory DisplayCardPage_TrainerPage2 */
PrintAttackOrCardDescriptionResult DisplayCardPage_TrainerPage2(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	PrintAttackOrCardDescriptionResult result = DisplayEnergyOrTrainerCardPage(HEADER_TRAINER, f, b, c, d, e, wLoadedCard1NonPokemonDescription_ADDR + 2u);
	return result;
}
/* <<< factory DisplayCardPage_TrainerPage2 */

/* >>> factory DisplayCardPage_TrainerPage1 */
PrintAttackOrCardDescriptionResult DisplayCardPage_TrainerPage1(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	PrintAttackOrCardDescriptionResult result = DisplayEnergyOrTrainerCardPage(HEADER_TRAINER, f, b, c, d, e, wLoadedCard1NonPokemonDescription_ADDR);
	return result;
}
/* <<< factory DisplayCardPage_TrainerPage1 */

/* >>> factory PrintPracticeDuelInstructionsForCurrentTurn */
/* core.asm:2792-2807 */
void PrintPracticeDuelInstructionsForCurrentTurn(uint8_t a)
{
	/* `push af / ld a, [wDuelTurns] / and %11111110 / ld e, a / ld d, $00 /
	 * ld hl, PracticeDuelTextPointerTable / add hl, de / ld a, [hli] /
	 * ld h, [hl] / ld l, a / pop af`: the entry `a` survives the table read
	 * and only selects which printer the fallthrough runs. */
	const uint8_t *entry = rom_ptr(PRACTICE_DUEL_TEXT_POINTER_TABLE_BANK,
		(uint16_t)(PRACTICE_DUEL_TEXT_POINTER_TABLE_ADDR
			+ (uint16_t)(wDuelTurns & 0xFEu)));
	uint16_t hl = (uint16_t)(entry[0] | (uint16_t)entry[1] << 8);

	if (a != 0u) {
		PrintPracticeDuelInstructions_Fast(hl);
		return;
	}
	PrintPracticeDuelInstructions(hl);
}
/* <<< factory PrintPracticeDuelInstructionsForCurrentTurn */

/* >>> factory PracticeDuel_PrintTurnInstructions */
void PracticeDuel_PrintTurnInstructions(void)
{
	DrawPracticeDuelInstructionsTextBox();
	EnableLCD();
	uint8_t turns = gb_read8(wDuelTurns_ADDR);
	uint8_t previous_turn = gb_read8(wPracticeDuelTurn_ADDR);
	gb_write8(wPracticeDuelTurn_ADDR, turns);
	if (turns != previous_turn) {
		TextResult text = PrintScrollableText_WithTextBoxLabel_NoWait(NeedPracticeAgainPracticeDuelText, DrMasonText);
		(void)text;
		HandleYesOrNoMenuResult menu = YesOrNoMenu();
		PrintPracticeDuelInstructionsForCurrentTurn(menu.a);
		return;
	}
	PrintPracticeDuelInstructionsForCurrentTurn(0u);
}
/* <<< factory PracticeDuel_PrintTurnInstructions */

/* >>> factory Func_5a81 */
Func5a81Result Func_5a81(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t console = gb_read8(wConsole_ADDR);
	a = console;
	if (console == CONSOLE_DMG) {
		f = 0x80u;
		return (Func5a81Result){a, f, b, c, d, e, hl};
	}
	if (console == CONSOLE_SGB) {
		/* 2 << 0 + 2 << 2 binds as (2 << 0) + (2 << 2), yielding 0x0A. */
		a = 0x0Au;
		d = 0u;
		e = 5u;
		uint16_t packet = CreateCardAttrBlkPacket(a, d, e);
		gb_write8((uint16_t)(wTempSGBPacket_ADDR + 1u), 2u);
		/* 3 << 0 + 3 << 2 binds as (3 << 0) + (3 << 2), yielding 0x0F. */
		hl = (uint16_t)(wTempSGBPacket_ADDR + 8u);
		a = 0x0Fu;
		d = 12u;
		e = 1u;
		(void)CreateCardAttrBlkPacket_DataSet(hl, a, d, e);
		SendSGBResult result = SendSGB(a, f, b, c, d, e, packet);
		return (Func5a81Result){result.a, result.f, result.b, result.c, result.d, result.e, result.hl};
	}
	d = 0u;
	e = 5u;
	SendCardAttrBlkPacketResult first = ApplyBGP7OrSGB2ToCardImage(a, f, b, c, d, e, hl);
	d = 12u;
	e = 1u;
	SendCardAttrBlkPacketResult second = ApplyBGP6OrSGB3ToCardImage(first.a, first.f, first.b, first.c, d, e, first.hl);
	return (Func5a81Result){second.a, second.f, second.b, second.c, second.d, second.e, second.hl};
}
/* <<< factory Func_5a81 */

/* >>> factory _TossCoin */
/* core.asm:7847-7997. Drives the coin toss screen: one animated toss per
 * coin, synchronised with the opponent (30-frame AI delay or a link serial
 * byte), tallying heads in wCoinTossNumHeads. The four local subroutines live
 * as TossCoin_* statics above. Returns a = the heads count, carry set when it
 * is non-zero and Z when it is not. */
TossCoinResult _TossCoin(uint8_t a)
{
	uint8_t heads;

	wCoinTossTotalNum = a;
	if (wDuelDisplayedScreen != COIN_TOSS_7847) {
		wCoinTossNumTossed = 0u;
		EmptyScreen();
		(void)LoadDuelCoinTossResultTiles();
	}

	/* no need to print text if this is not the first coin toss */
	if (wCoinTossNumTossed == 0u) {
		uint16_t box = 0u; /* ld hl, NULL: the box carries no label */
		uint16_t text_id;

		wDuelDisplayedScreen = COIN_TOSS_7847;
		DrawLabeledTextBox(&box, COIN_TOSS_7847, 20u, 6u, 0u, 12u);
		EnableLCD();
		InitTextPrintingInTextbox(19u, 1u, 14u);
		text_id = (uint16_t)(gb_read8(wCoinTossScreenTextID_ADDR)
			| (uint16_t)gb_read8((uint16_t)(wCoinTossScreenTextID_ADDR + 1u)) << 8);
		(void)PrintText(text_id, 1u, 14u);
	}

	gb_write8(wCoinTossScreenTextID_ADDR, 0u);
	gb_write8((uint16_t)(wCoinTossScreenTextID_ADDR + 1u), 0u);

	/* store duelist type and reset number of heads */
	EnableLCD();
	wCoinTossDuelistType = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE_7847).a;
	(void)ExchangeRNG(0u, 0u, 0u, 0u);
	wCoinTossNumHeads = 0u;

	do {
		uint8_t anim;
		uint8_t result;
		uint8_t tile;

		/* skip the tally if it's only one coin toss */
		if (wCoinTossTotalNum >= 2u) {
			/* write "#coin/#total coins" */
			WriteTwoDigitNumberInTxSymbol_PadSpace(
				(uint8_t)(wCoinTossNumTossed + 1u), 15u, 11u, 0u, 0u, 0u);
			WriteByteToBGMap0(SYM_SLASH_7847, 17u, 11u);
			WriteTwoDigitNumberInTxSymbol_PadSpace(
				wCoinTossTotalNum, 18u, 11u, 0u, 0u, 0u);
		}

		ResetAnimationQueue();
		(void)PlayDuelAnimation(DUEL_ANIM_COIN_SPIN_7847);

		if (wCoinTossDuelistType == DUELIST_TYPE_PLAYER_7847) {
			/* wait for input, and send a byte once the player is ready */
			(void)WaitForWideTextBoxInput();
			/* its EraseCursor tail exits WriteByteToBGMap0 with a = 0,
			 * which is the byte the ROM forwards here */
			TossCoin_SendSerialByte(0u);
		} else {
			TossCoin_WaitForOpponent(wCoinTossDuelistType);
		}

		ResetAnimationQueue();
		anim = DUEL_ANIM_COIN_TOSS_GOING_TAILS_7847;
		result = TAILS_7847;
		if (!(UpdateRNGSources() & 0x01u)) { /* rra: carry = bit 0 */
			anim = DUEL_ANIM_COIN_TOSS_GOING_HEADS_7847;
			result = HEADS_7847;
		}

		/* play the tossing animation and wait for it to finish */
		(void)PlayDuelAnimation(anim);
		if (wCoinTossDuelistType == DUELIST_TYPE_PLAYER_7847) {
			do {
				DoFrame();
			} while (CheckAnyAnimationPlaying().f & FLAG_C_7847);
			TossCoin_SendSerialByte(result);
		} else {
			result = TossCoin_GetOpponentCoinResult(result);
		}

		anim = DUEL_ANIM_COIN_HEADS_7847;
		tile = TILE_CROSS_7847;
		if (result != 0u) {
			anim = DUEL_ANIM_COIN_TAILS_7847;
			tile = TILE_CIRCLE_7847;
			wCoinTossNumHeads = (uint8_t)(wCoinTossNumHeads + 1u);
		}
		(void)PlayDuelAnimation(anim);

		/* the result sound depends on whether it was the Player or the
		 * Opponent who got heads/tails */
		if (wCoinTossDuelistType != DUELIST_TYPE_PLAYER_7847)
			result ^= 0x01u;
		PlaySFX(result != 0u ? SFX_COIN_TOSS_HEADS_7847
				     : SFX_COIN_TOSS_TAILS_7847);

		/* on a multiple coin toss the result is registered on screen with
		 * a circle (o) or a cross (x) */
		if ((uint8_t)(wCoinTossTotalNum - 1u) != 0u) {
			uint8_t y = 0u;
			uint8_t x = wCoinTossNumTossed;

			/* below 10 the offset is wCoinTossNumTossed * 2, above it a
			 * y-offset is added for each multiple of 10 */
			while (x >= 10u) {
				y = (uint8_t)(y + 2u);
				x = (uint8_t)(x - 10u);
			}
			FillRectangle(tile, 2u, 2u,
				(uint16_t)((uint16_t)(uint8_t)(x * 2u) << 8 | y), 0x0102u);
		}

		wCoinTossNumTossed = (uint8_t)(wCoinTossNumTossed + 1u);

		if (wCoinTossDuelistType != DUELIST_TYPE_PLAYER_7847) {
			uint8_t sent = wCoinTossNumTossed;

			/* wait for input once every coin has been tossed */
			if (wCoinTossNumTossed == wCoinTossTotalNum) {
				(void)WaitForWideTextBoxInput();
				sent = 0u;
			}
			/* delay/wait for link opp input */
			TossCoin_WaitForOpponent(sent);
			/* "tossing until tails" (wCoinTossTotalNum == 0) with no heads
			 * yet also waits for input */
			if ((uint8_t)(wCoinTossTotalNum | wCoinTossNumHeads) == 0u)
				(void)WaitForWideTextBoxInput();
		} else {
			(void)WaitForWideTextBoxInput();
			TossCoin_SendSerialByte(0u);
		}

		FinishQueuedAnimations();
	} while (wCoinTossNumTossed < wCoinTossTotalNum);

	(void)ExchangeRNG(0u, 0u, 0u, 0u);
	FinishQueuedAnimations();
	ResetAnimationQueue();

	/* return carry if at least 1 heads */
	heads = wCoinTossNumHeads;
	return (TossCoinResult){heads, heads ? FLAG_C_7847 : FLAG_Z_7847};
}
/* <<< factory _TossCoin */

/* >>> factory AttemptRetreat */
AttemptRetreatResult AttemptRetreat(void)
{
	DiscardRetreatCostCardsResult discard = DiscardRetreatCostCards();
	if ((hTemp_ffa0 & CNF_SLP_PRZ) == CONFUSED) {
		TossCoinRoutineResult toss = TossCoin(ConfusionCheckRetreatText, discard.hl);
		if ((toss.f & 0x10u) == 0u) {
			wConfusionRetreatCheckWasUnsuccessful = 1u;
			return (AttemptRetreatResult){1u, 0x10u};
		}
	}
	SwapArenaWithBenchPokemon(hTempPlayAreaLocation_ffa1);
	wConfusionRetreatCheckWasUnsuccessful = 0u;
	return (AttemptRetreatResult){0u, 0x80u};
}
/* <<< factory AttemptRetreat */

/* >>> factory OppAction_BeginUseAttack */
OppActionBeginUseAttackResult OppAction_BeginUseAttack(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(d, e);
	a = copy.a;
	c = copy.c;
	f = copy.f;
	hl = copy.hl;
	d = (uint8_t)(copy.de >> 8);
	e = (uint8_t)copy.de;
	DuelRoutineResult updated = UpdateArenaCardIDsAndClearTwoTurnDuelVars(a, f, b, c, d, e, hl);
	a = updated.a;
	f = updated.f;
	b = updated.b;
	c = updated.c;
	d = updated.d;
	e = updated.e;
	hl = updated.hl;
wSkipDuelistIsThinkingDelay = 0x01u;
	SandAttackCheckResult check = CheckSandAttackOrSmokescreenSubstatus((uint16_t)((uint16_t)d << 8 | e));
	a = check.a;
	f = check.f;
	d = (uint8_t)(check.de >> 8);
	e = (uint8_t)check.de;
	hl = check.hl;
	if ((f & 0x10u) == 0u) {
		DuelistVarResult status = GetTurnDuelistVariable(0xF0u);
		a = (uint8_t)(status.a & CNF_SLP_PRZ);
		hl = status.hl;
		if (a != CONFUSED) {
			ExchangeRNGResult rng = ExchangeRNG(b, c, (uint16_t)((uint16_t)d << 8 | e), hl);
			return (OppActionBeginUseAttackResult){rng.a, rng.f, rng.b, rng.c, (uint8_t)(rng.de >> 8), (uint8_t)rng.de, rng.hl};
		}
	}
	DrawDuelMainScene();
	PrintPokemonsAttackTextResult text = PrintPokemonsAttackText();
	a = text.a;
	b = text.b;
	c = text.c;
	d = text.d;
	e = text.e;
	hl = text.hl;
	WaitResult wait = WaitForWideTextBoxInput();
	f = wait.f;
	ExchangeRNGResult rng = ExchangeRNG(b, c, (uint16_t)((uint16_t)d << 8 | e), hl);
	a = rng.a;
	f = rng.f;
	b = rng.b;
	c = rng.c;
	d = (uint8_t)(rng.de >> 8);
	e = (uint8_t)rng.de;
	hl = rng.hl;
	HandleSandAttackOrSmokescreenSubstatusResult handled = HandleSandAttackOrSmokescreenSubstatus((uint16_t)((uint16_t)d << 8 | e), hl);
	a = handled.a;
	f = handled.f;
	d = (uint8_t)(handled.de >> 8);
	e = (uint8_t)handled.de;
	hl = handled.hl;
	if ((f & 0x10u) == 0u)
		return (OppActionBeginUseAttackResult){a, f, b, c, d, e, hl};
	ClearNonTurnTemporaryDuelvars();
	a = 1u;
wOpponentTurnEnded = 0x01u;
	return (OppActionBeginUseAttackResult){a, f, b, c, d, e, hl};
}
/* <<< factory OppAction_BeginUseAttack */

/* >>> factory OppAction_TossCoinATimes */
OppAction_TossCoinATimesResult OppAction_TossCoinATimes(void)
{
	SerialRecv8BytesResult recv = SerialRecv8Bytes();
	TossCoinATimesResult toss = TossCoinATimes(recv.a, recv.f, recv.b, recv.c, recv.d, recv.e, recv.hl);
	wSkipDuelistIsThinkingDelay = 1u;
	return (OppAction_TossCoinATimesResult){1u, toss.f, 0x12u, 0u, 0x12u, 0x11u, toss.hl};
}
/* <<< factory OppAction_TossCoinATimes */

/* >>> factory OppAction_AttemptRetreat */
WaitResult OppAction_AttemptRetreat(void)
{
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	AttemptRetreatResult retreat = AttemptRetreat();
	uint16_t text;
	if ((retreat.f & 0x10u) != 0u) {
		text = RetreatWasUnsuccessfulText;
	} else {
		wDuelDisplayedScreen = 0u;
		text = RetreatedToTheBenchText;
	}
	DrawDuelMainScene();
	LoadCardNameToTxRam2(arena.a);
	return DrawWideTextBox_WaitForInput_Bank1(text);
}
/* <<< factory OppAction_AttemptRetreat */

/* >>> factory PlayAttackAnimation */
void PlayAttackAnimation(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t saved_h_whose_turn = hWhoseTurn;
	hWhoseTurn = wWhoseTurn;
	gb_write8(wDamageAnimEffectiveness_ADDR, c);
	if (hWhoseTurn != (uint8_t)(hl >> 8))
		b |= 0x80u;
	gb_write8(wDamageAnimPlayAreaLocation_ADDR, b);
	gb_write8(wDamageAnimPlayAreaSide_ADDR, wWhoseTurn);
	gb_write8(wDamageAnimCardID_ADDR, wTempNonTurnDuelistCardID);
	gb_write8(wDamageAnimAmount_ADDR, e);
	gb_write8(wDamageAnimAmount_ADDR + 1u, d);

	uint8_t loaded_animation = wLoadedAttackAnimation;
	if (loaded_animation == ATK_ANIM_HIT && e >= 70u) {
		loaded_animation = ATK_ANIM_BIG_HIT;
		wLoadedAttackAnimation = loaded_animation;
	}
	(void)PlayAttackAnimationCommands(wLoadedAttackAnimation, d, e);
	hWhoseTurn = saved_h_whose_turn;
	(void)a;
	(void)f;
	(void)hl;
}
/* <<< factory PlayAttackAnimation */

/* >>> factory PlayStatusConditionQueueAnimations */
void PlayStatusConditionQueueAnimations(void)
{
	uint8_t index = wStatusConditionQueueIndex;
	if (index == 0u)
		return;
	gb_write8((uint16_t)(wStatusConditionQueue_ADDR + index), 0u);
	uint16_t hl = wStatusConditionQueue_ADDR;
	for (;;) {
		uint8_t d = gb_read8(hl++);
		if (d == 0u)
			return;
		hl++;
		uint8_t condition = gb_read8(hl++);
		uint8_t animation;
		switch (condition) {
		case ASLEEP:
			animation = ATK_ANIM_SLEEP;
			break;
		case PARALYZED:
			animation = ATK_ANIM_PARALYSIS;
			break;
		case POISONED:
		case DOUBLE_POISONED:
			animation = ATK_ANIM_POISON;
			break;
		case CONFUSED:
			animation = (hWhoseTurn == d) ? ATK_ANIM_OWN_CONFUSION : ATK_ANIM_CONFUSION;
			break;
		default:
			continue;
		}
		wLoadedAttackAnimation = animation;
		wDuelAnimLocationParam = 0u;
		(void)PlayAttackAnimationCommands(animation, d, animation);
	}
}
/* <<< factory PlayStatusConditionQueueAnimations */

/* >>> factory PlayAttackAnimation_DealAttackDamageSimple */
PlayAttackAnimation_DealAttackDamageSimpleResult PlayAttackAnimation_DealAttackDamageSimple(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	PlayAttackAnimation(a, f, b, c, d, e, hl);
	WaitAttackAnimation();
	uint16_t damage = (uint16_t)(((uint16_t)d << 8) | e);
	SubtractHPResult hp = SubtractHP(hl, damage);
	(void)hp;
	uint8_t screen = wDuelDisplayedScreen;
	if (screen == 1u) {
		DrawDuelHUDs();
	}
	uint8_t result_f = 0x40u;
	if ((screen & 0x0fu) == 0u) {
		result_f |= 0x20u;
	}
	if (screen == 0u) {
		result_f |= 0x10u;
	}
	if (screen == 1u) {
		result_f = 0x80u;
	}
	return (PlayAttackAnimation_DealAttackDamageSimpleResult){screen, result_f};
}
/* <<< factory PlayAttackAnimation_DealAttackDamageSimple */

/* >>> factory DisplayOpponentUsedAttackScreen */
void DisplayOpponentUsedAttackScreen(void)
{
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelFaceDownCardTiles();
	uint8_t cardid = wTempCardID_ccc2;
	LoadCardDataToBuffer1_FromCardID(cardid);
	wCardPageNumber = CARDPAGE_POKEMON_OVERVIEW;
	uint16_t hl = wLoadedCard1Atk1Name_ADDR;
	if (wSelectedAttack != 0u) {
		hl = wLoadedCard1Atk2Name_ADDR;
	}
	(void)PrintAttackOrPkmnPowerInformation(0u, 0u, 0u, 1u, hl);
	(void)PrintAttackOrCardDescription(wLoadedAttackDescription_ADDR, 1u, 4u);
}
/* <<< factory DisplayOpponentUsedAttackScreen */

/* >>> factory DisplayCardList */
DisplayCardListResult DisplayCardList(void)
{
	/* Both `jr c, DisplayCardList` (the item selection menu was cancelled) and
	 * `jp DisplayCardList` (the card page was exited) re-enter at the top. */
	for (;;) {
		(void)DrawNarrowTextBox();
		PrintCardListHeaderAndInfoBoxTexts();

		uint8_t reenter = 0u;

		while (reenter == 0u) {
			/* .reload_list */
			uint8_t count = CountCardsInDuelTempList().a;
			uint8_t item = wSelectedDuelSubMenuItem;
			uint8_t scroll = wSelectedDuelSubMenuScrollOffset;
			uint16_t params = CARD_LIST_PARAMETERS;

			PrintCardListItems(count, scroll, item, &params);
			LoadSelectedCardGfx();
			EnableLCD();

			for (;;) {
				/* .wait_button */
				DoFrame();

				/* .UpdateListOnDPadInput */
				if ((hDPadHeld & PAD_CTRL_PAD) != 0u) {
					hffb0 = 1u;
					PrintCardListHeaderAndInfoBoxTexts();
					hffb0 = 0u;
				}

				HandleCardListInputResult input = HandleCardListInput();
				uint8_t list_item;
				uint8_t list_scroll;

				if ((input.f & FLAG_C) != 0u) {
					list_scroll = input.d;
					list_item = input.e;
				} else {
					/* CardListMenuFunction (home/menus.c) stops where the
					 * asm does `jp hl` on wListFunctionPointer, so the
					 * function PrintCardListItems armed out of
					 * CardListParameters -- CardListFunction ($5719) -- is
					 * called here, followed by the HandleMenuInput and
					 * HandleCardListInput epilogues the ROM reaches through
					 * it: draw the cursor, play the open/exit SFX, and
					 * report the scroll offset and item it settled on. */
					CardListFunctionResult list_fn = CardListFunction();

					if ((list_fn.f & FLAG_C) == 0u)
						continue;
					DrawCursor2();
					(void)PlayOpenOrExitScreenSFX(list_fn.a, list_fn.f);
					list_scroll = wListScrollOffset;
					list_item = wCurMenuItem;
				}

				/* refresh the position of the last checked card, so that the
				 * cursor points to it when the list is reloaded */
				wSelectedDuelSubMenuItem = list_item;
				wSelectedDuelSubMenuScrollOffset = list_scroll;

				uint8_t keys = hKeysPressed;

				if ((keys & PAD_SELECT) != 0u) {
					/* .select_pressed: sort the list by ID once, then start
					 * over from its first item */
					if (wSortCardListByID != 0u)
						continue;
					(void)SortCardsInDuelTempListByID(keys, 0u, (uint16_t)(((uint16_t)list_scroll << 8) | list_item));
					wSelectedDuelSubMenuItem = 0u;
					wSelectedDuelSubMenuScrollOffset = 0u;
					wSortCardListByID = TRUE;
					EraseCursor();
					break;
				}
				if ((keys & PAD_B) != 0u) {
					/* .b_pressed: hCurMenuItem is the MENU_CANCEL that
					 * CardListFunction wrote on its way out */
					return (DisplayCardListResult){hCurMenuItem, FLAG_C};
				}
				if ((wNoItemSelectionMenuKeys & keys) != 0u) {
					/* .open_card_page: no item selection menu, and PAD_UP or
					 * PAD_DOWN opens the card page of the card above or
					 * below the current one */
					for (;;) {
						DeckEntryResult card = GetCardInDuelTempList(hCurMenuItem, wSelectedDuelSubMenuScrollOffset_ADDR);
						uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(card.a);

						OpenCardPage_FromCheckHandOrDiscardPile(card_id, 0u, keys, 0u, card.d, card.e, card.hl);

						uint8_t held = hDPadHeld;

						if ((held & (PAD_UP | PAD_DOWN)) == 0u) {
							/* B: leave the card page and reload the list */
							(void)DrawCardListScreenLayout();
							break;
						}

						uint8_t next = hCurMenuItem;

						if ((held & PAD_UP) != 0u) {
							/* .up_pressed */
							if (next == 0u)
								continue; /* reopen the current card */
							next--;
						} else {
							/* .down_pressed */
							uint8_t total = CountCardsInDuelTempList().a;

							next++;
							if (next >= total)
								continue; /* reopen the current card */
						}
						/* .move_to_another_card: scroll the page to reflect
						 * the movement instead of moving the cursor */
						hCurMenuItem = next;
						wSelectedDuelSubMenuItem = 0u;
						wSelectedDuelSubMenuScrollOffset = next;
					}
					reenter = 1u;
					break;
				}

				/* the item selection menu (PLAY|CHECK or SELECT|CHECK) for the
				 * selected card, which opens the card page on CHECK */
				(void)GetCardInDuelTempList_OnlyDeckIndex(hCurMenuItem, wSelectedDuelSubMenuScrollOffset_ADDR);

				CardListItemSelectionMenuResult menu = CardListItemSelectionMenu();

				if ((menu.f & FLAG_C) != 0u) {
					/* B left the item selection menu: start over */
					reenter = 1u;
					break;
				}

				uint8_t selected = hTempCardIndex_ff98;

				return (DisplayCardListResult){selected, (uint8_t)(selected == 0u ? FLAG_Z : 0u)};
			}
		}
	}
}
/* <<< factory DisplayCardList */

/* >>> factory Func_5542 */
Func5542Result Func_5542(uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint8_t f, uint16_t hl)
{
	CardListResult discard = CreateDiscardPileCardList(c);
	if (discard.f & 0x10u)
		return (Func5542Result){discard.a, discard.b, discard.c, discard.d, discard.e, discard.f, discard.hl};
	(void)InitAndDrawCardListScreenLayout();
	SetDiscardPileScreenTexts();
	DisplayCardListResult display = DisplayCardList();
	return (Func5542Result){display.a, discard.b, discard.c, discard.d, discard.e, display.f, discard.hl};
}
/* <<< factory Func_5542 */

/* >>> factory CheckIfCanDamageDefendingPokemon */
/* core.asm:2310-2355. Stores the caller's a in hTempPlayAreaLocation_ff9d, tries
 * the first attack and, failing that, the second one, and reports in a the damage
 * the last EstimateDamage_VersusDefendingCard left in wDamage. The body itself
 * touches no register but a -- b/c/d/e/hl only travel from one callee to the next,
 * and neither their values nor d's are part of what this routine computes -- and
 * both exits are plain flag work: `or a` on the fallthrough, `scf` as soon as
 * either attack deals damage. a and the flags are the whole output contract. */
CheckIfCanDamageDefendingPokemonResult CheckIfCanDamageDefendingPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	hTempPlayAreaLocation_ff9d = a;
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	/* `xor a` hands the call a = 0 with Z set. */
	CheckIfSelectedAttackIsUnusableResult first =
		CheckIfSelectedAttackIsUnusable(FIRST_ATTACK_OR_PKMN_POWER, 0x80u, b, c, d, e, hl);
	a = first.a;
	f = first.f;
	b = first.b;
	c = first.c;
	d = first.d;
	e = first.e;
	hl = first.hl;
	if ((f & 0x10u) == 0u) {
		DamageCalculationResult estimate =
			EstimateDamage_VersusDefendingCard(FIRST_ATTACK_OR_PKMN_POWER);
		d = estimate.d;
		e = estimate.e;
		hl = estimate.hl;
		a = wDamage;
		if (a != 0u)
			return (CheckIfCanDamageDefendingPokemonResult){a, 0x10u};
		f = 0x80u; /* `or a` on a zero damage byte */
	}

	/* .second_attack */
	wSelectedAttack = SECOND_ATTACK;
	CheckIfSelectedAttackIsUnusableResult second =
		CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, f, b, c, d, e, hl);
	a = second.a;
	f = second.f;
	if ((f & 0x10u) == 0u) {
		(void)EstimateDamage_VersusDefendingCard(SECOND_ATTACK);
		a = wDamage;
		if (a != 0u)
			return (CheckIfCanDamageDefendingPokemonResult){a, 0x10u};
	}

	/* .no_carry */
	f = (a == 0u) ? 0x80u : 0x00u;
	return (CheckIfCanDamageDefendingPokemonResult){a, f};
}
/* <<< factory CheckIfCanDamageDefendingPokemon */

/* >>> factory OpenDiscardPileScreen */
OpenDiscardPileScreenResult OpenDiscardPileScreen(uint8_t c)
{
	CardListResult list = CreateDiscardPileCardList(c);
	if ((list.f & 0x10u) != 0u) {
		WaitResult wait = DrawWideTextBox_WaitForInput(TheDiscardPileHasNoCardsText);
		return (OpenDiscardPileScreenResult){(uint8_t)((wait.f & 0x80u) | 0x10u)};
	}
	(void)InitAndDrawCardListScreenLayout();
	SetDiscardPileScreenTexts();
	wNoItemSelectionMenuKeys = 0x09u;
	DisplayCardListResult display = DisplayCardList();
	return (OpenDiscardPileScreenResult){(uint8_t)(display.a == 0u ? 0x80u : 0u)};
}
/* <<< factory OpenDiscardPileScreen */

/* >>> factory OpenTurnHolderHandScreen_Simple */
uint8_t OpenTurnHolderHandScreen_Simple(void)
{
	HandListResult hand = CreateHandCardList(0u);
	if (hand.f & 0x10u) {
		WaitResult waited = DrawWideTextBox_WaitForInput(NoCardsInHandText);
		return waited.f;
	}
	(void)InitAndDrawCardListScreenLayout();
	wNoItemSelectionMenuKeys = (uint8_t)(PAD_START + PAD_A);
	return DisplayCardList().f;
}
/* <<< factory OpenTurnHolderHandScreen_Simple */

/* >>> factory OpenTurnHolderDiscardPileScreen */
OpenDiscardPileScreenResult OpenTurnHolderDiscardPileScreen(uint8_t c)
{
	return OpenDiscardPileScreen(c);
}
/* <<< factory OpenTurnHolderDiscardPileScreen */

/* >>> factory OpenNonTurnHolderHandScreen_Simple */
uint8_t OpenNonTurnHolderHandScreen_Simple(void)
{
	SwapTurn();
	uint8_t result = OpenTurnHolderHandScreen_Simple();
	SwapTurn();
	return result;
}
/* <<< factory OpenNonTurnHolderHandScreen_Simple */

/* >>> factory OpenNonTurnHolderDiscardPileScreen */
OpenDiscardPileScreenResult OpenNonTurnHolderDiscardPileScreen(uint8_t c)
{
	SwapTurn();
	OpenDiscardPileScreenResult result = OpenDiscardPileScreen(c);
	SwapTurn();
	return result;
}
/* <<< factory OpenNonTurnHolderDiscardPileScreen */

/* >>> factory CanArenaCardUseNonResidualAttack */
/* ai/core.asm:1383-1407. Tries the first attack, then the second when the first
 * is unusable or Residual. Carry means at least one usable non-Residual attack. */
CanArenaCardUseNonResidualAttackResult CanArenaCardUseNonResidualAttack(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	CheckIfSelectedAttackIsUnusableResult first = CheckIfSelectedAttackIsUnusable(FIRST_ATTACK_OR_PKMN_POWER, 0x80u, b, c, d, e, hl);
	a = first.a; f = first.f; b = first.b; c = first.c; d = first.d; e = first.e; hl = first.hl;
	if (!(f & 0x10u)) {
		a = (uint8_t)(wLoadedAttackCategory & RESIDUAL);
		f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
		if (a == 0u) {
			f = (uint8_t)((f & 0x80u) | 0x10u);
			return (CanArenaCardUseNonResidualAttackResult){a, f, b, c, d, e, hl};
		}
	}
	wSelectedAttack = SECOND_ATTACK;
	CheckIfSelectedAttackIsUnusableResult second = CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, f, b, c, d, e, hl);
	a = second.a; f = second.f; b = second.b; c = second.c; d = second.d; e = second.e; hl = second.hl;
	if (!(f & 0x10u)) {
		a = (uint8_t)(wLoadedAttackCategory & RESIDUAL);
		if (a == 0u) {
			f = (uint8_t)((f & 0x80u) | 0x10u);
			return (CanArenaCardUseNonResidualAttackResult){a, f, b, c, d, e, hl};
		}
	}
	f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
	return (CanArenaCardUseNonResidualAttackResult){a, f, b, c, d, e, hl};
}
/* <<< factory CanArenaCardUseNonResidualAttack */

/* >>> factory DisplayPlaceInitialPokemonCardsScreen */
DisplayPlaceInitialPokemonCardsScreenResult DisplayPlaceInitialPokemonCardsScreen(uint8_t a, uint16_t hl)
{
	wPlacingInitialBenchPokemon = a;
	(void)CreateHandCardList(a);
	(void)InitAndDrawCardListScreenLayout();
	SetCardListInfoBoxText(hl);
	wCardListItemSelectionMenuType = PLAY_CHECK;
	for (;;) {
		DisplayCardListResult display = DisplayCardList();
		if ((display.f & 0x10u) != 0u) {
			uint8_t placing = wPlacingInitialBenchPokemon;
			if (placing == 0u)
				continue;
			return (DisplayPlaceInitialPokemonCardsScreenResult){placing, 0x10u};
		}
		uint8_t card_index = hTempCardIndex_ff98;
		(void)LoadCardDataToBuffer1_FromDeckIndex(card_index);
		IsLoadedCard1BasicPokemonResult basic = IsLoadedCard1BasicPokemon();
		if ((basic.f & 0x10u) != 0u) {
			(void)DrawWideTextBox_WaitForInput(YouCannotSelectThisCardText);
			(void)DrawCardListScreenLayout();
			continue;
		}
		if (wSortCardListByID != 0u)
			(void)SortHandCardsByID();
		return (DisplayPlaceInitialPokemonCardsScreenResult){basic.a, basic.f};
	}
}
/* <<< factory DisplayPlaceInitialPokemonCardsScreen */

/* >>> factory PrintDeckAndHandIconsAndNumberOfCards */
/* duel/core.asm:1490-1504. The two data tables live in bank 1 and feed a
 * gb_read8-based block writer, so copy them to WRAM before calling it. */
void PrintDeckAndHandIconsAndNumberOfCards(void)
{
	static const uint8_t tiles[] = {
		0x04u, 0x03u, 0x2Du, 0x00u, 0x0Au, 0x03u, 0x2Du, 0x00u,
		0x08u, 0x02u, 0xF4u, 0xF5u, 0x00u, 0x08u, 0x03u, 0xF6u,
		0xF7u, 0x00u, 0x02u, 0x02u, 0xF8u, 0xF9u, 0x00u, 0x02u,
		0x03u, 0xFAu, 0xFBu, 0x00u, 0x09u, 0x0Au, 0x2Du, 0x00u,
		0x0Fu, 0x0Au, 0x2Du, 0x00u, 0x07u, 0x09u, 0xF4u, 0xF5u,
		0x00u, 0x07u, 0x0Au, 0xF6u, 0xF7u, 0x00u, 0x0Du, 0x09u,
		0xF8u, 0xF9u, 0x00u, 0x0Du, 0x0Au, 0xFAu, 0xFBu, 0x00u,
		0xFFu,
	};
	static const uint8_t palettes[] = {
		0x08u, 0x02u, 0x02u, 0x02u, 0x00u, 0x08u, 0x03u, 0x02u,
		0x02u, 0x00u, 0x02u, 0x02u, 0x02u, 0x02u, 0x00u, 0x02u,
		0x03u, 0x02u, 0x02u, 0x00u, 0x07u, 0x09u, 0x02u, 0x02u,
		0x00u, 0x07u, 0x0Au, 0x02u, 0x02u, 0x00u, 0x0Du, 0x09u,
		0x02u, 0x02u, 0x00u, 0x0Du, 0x0Au, 0x02u, 0x02u, 0x00u,
		0xFFu,
	};
	const uint16_t scratch = 0xC100u;
	uint16_t hl;
	uint16_t de;
	uint8_t a;
	uint8_t b;
	uint8_t c;

	(void)LoadDuelDrawCardsScreenTiles();
	for (uint8_t i = 0u; i < sizeof(tiles); i++)
		gb_write8((uint16_t)(scratch + i), tiles[i]);
	hl = scratch; de = 0u; a = 0u; b = 0u; c = 0u;
	WriteDataBlocksToBGMap0(&hl, &de, &a, &b, &c);
	if (wConsole == CONSOLE_CGB) {
		for (uint8_t i = 0u; i < sizeof(palettes); i++)
			gb_write8((uint16_t)(scratch + i), palettes[i]);
		hBankVRAM = 1u;
		gb_write8(0xFF4Fu, 1u);
		hl = scratch; de = 0u; a = 0u; b = 0u; c = 0u;
		WriteDataBlocksToBGMap0(&hl, &de, &a, &b, &c);
		hBankVRAM = 0u;
		gb_write8(0xFF4Fu, 0u);
	}
	PrintPlayerNumberOfHandAndDeckCards();
	PrintOpponentNumberOfHandAndDeckCards();
}
/* <<< factory PrintDeckAndHandIconsAndNumberOfCards */

/* >>> factory CheckDamageToMrMime */
CheckDamageToMrMimeResult CheckDamageToMrMime(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t original_a = a;
	DuelistVarResult arena = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
	SwapTurn();
	uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(arena.a);
	SwapTurn();
	if (card_id != MR_MIME)
		return (CheckDamageToMrMimeResult){card_id, 0x10u};
	CheckIfCanDamageDefendingPokemonResult check =
		CheckIfCanDamageDefendingPokemon(original_a, 0xC0u, original_a, f, d, e, arena.hl);
	if ((check.f & 0x10u) != 0u)
		return (CheckDamageToMrMimeResult){check.a, 0x10u};
	return (CheckDamageToMrMimeResult){check.a, check.f};
}
/* <<< factory CheckDamageToMrMime */

/* >>> factory DisplayDrawNCardsScreen */
void DisplayDrawNCardsScreen(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)f;
	wNumCardsTryingToDraw = a;
	wNumCardsBeingDrawn = 0u;
	DuelistVarResult cards = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint8_t available = (uint8_t)(DECK_SIZE - gb_read8(cards.hl));
	if (available < wNumCardsTryingToDraw)
		wNumCardsTryingToDraw = available;

	uint8_t displayed = wDuelDisplayedScreen;
	if (displayed != DRAW_CARDS && displayed != SHUFFLE_DECK) {
		EmptyScreen();
		DrawDuelistPortraitsAndNames();
	}
	wDuelDisplayedScreen = DRAW_CARDS;
	PrintDeckAndHandIconsAndNumberOfCards();
	if (wNumCardsTryingToDraw == 0u) {
		(void)DrawWideTextBox_WaitForInput(CannotDrawCardBecauseNoCardsInDeckText);
		return;
	}
	LoadTxRam3((uint16_t)wNumCardsTryingToDraw);
	(void)DrawWideTextBox_PrintText(DrawCardsFromTheDeckText);
	EnableLCD();
	while (wNumCardsBeingDrawn < wNumCardsTryingToDraw) {
		PlayTurnDuelistDrawAnimationResult animation =
			PlayTurnDuelistDrawAnimation(f, b, c, d, hl);
		e = animation.e;
		f = animation.f;
		wNumCardsBeingDrawn = (uint8_t)(wNumCardsBeingDrawn + 1u);
		PrintNumberOfHandAndDeckCards();
	}
	uint8_t delay = 30u;
	while (delay != 0u) {
		DoFrame();
		CheckSkipDelayAllowedResult skip = CheckSkipDelayAllowed(f, b, delay, d, e, hl);
		b = skip.b;
		d = skip.d;
		e = skip.e;
		f = skip.f;
		hl = skip.hl;
		if ((f & 0x10u) != 0u)
			break;
		delay = (uint8_t)(delay - 1u);
	}
}
/* <<< factory DisplayDrawNCardsScreen */

/* >>> factory PlayShuffleAndDrawCardsAnimation */
/* duel/core.asm:2173-2266.
 * The body reads its own frame twice: `ld hl, sp+$03` is the caller's pushed b
 * (shuffling animation) and `ld hl, sp+$00` is the caller's pushed c (drawing
 * animation), while the second `pop hl` reloads the pushed de as the drawing
 * text id. Every push is matched by a pop before the `ret`, so the words are
 * ordinary parameters here and the case module declares no `stack`.
 * b and c are the only registers the routine hands back: `pop bc` restores
 * them, everything else is left wherever FinishQueuedAnimations put it. */
void PlayShuffleAndDrawCardsAnimation(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t skipped = 0u;

	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	DrawDuelistPortraitsAndNames();
	(void)LoadDuelDrawCardsScreenTiles();
	wDuelDisplayedScreen = SHUFFLE_DECK;
	(void)DrawWideTextBox_PrintText(hl);
	EnableLCD();

	if (wDuelType == DUELTYPE_PRACTICE) {
		(void)WaitForWideTextBoxInput();
	} else {
		ResetAnimationQueue();
		(void)PlayDuelAnimation(b);
		(void)PlayDuelAnimation(b);
		(void)PlayDuelAnimation(b);
		for (;;) {
			DoFrame();
			CheckSkipDelayAllowedResult skip = CheckSkipDelayAllowed(0u, 0u, 0u, 0u, 0u, 0u);
			if ((skip.f & FLAG_C) != 0u)
				break;
			AnimationStatusResult anim = CheckAnyAnimationPlaying();
			if ((anim.f & FLAG_C) == 0u)
				break;
		}
		FinishQueuedAnimations();
	}

	wNumCardsBeingDrawn = 0u;
	PrintDeckAndHandIconsAndNumberOfCards();
	ResetAnimationQueue();
	/* the second `pop hl`: the caller's de is the text printed while drawing */
	(void)DrawWideTextBox_PrintText((uint16_t)(((uint16_t)d << 8) | e));

	for (;;) {
		(void)PlayDuelAnimation(c);
		for (;;) {
			DoFrame();
			CheckSkipDelayAllowedResult skip = CheckSkipDelayAllowed(0u, 0u, 0u, 0u, 0u, 0u);
			if ((skip.f & FLAG_C) != 0u) {
				/* `jr c, .done`: straight to the epilogue, no card counted */
				skipped = 1u;
				break;
			}
			AnimationStatusResult anim = CheckAnyAnimationPlaying();
			if ((anim.f & FLAG_C) == 0u)
				break;
		}
		if (skipped != 0u)
			break;
		wNumCardsBeingDrawn = (uint8_t)(wNumCardsBeingDrawn + 1u);
		if (c == DUEL_ANIM_BOTH_DRAW) {
			/* PrintDeckAndHandIconsAndNumberOfCards.not_cgb: the tail that
			 * skips the tile/palette reload and only reprints the counts */
			PrintPlayerNumberOfHandAndDeckCards();
			PrintOpponentNumberOfHandAndDeckCards();
		} else {
			PrintNumberOfHandAndDeckCards();
		}
		if (wNumCardsBeingDrawn >= 7u)
			break;
	}

	if (skipped == 0u) {
		uint8_t frames = 30u;

		for (;;) {
			DoFrame();
			CheckSkipDelayAllowedResult skip = CheckSkipDelayAllowed(0u, 0u, 0u, 0u, 0u, 0u);
			if ((skip.f & FLAG_C) != 0u)
				break;
			frames = (uint8_t)(frames - 1u);
			if (frames == 0u)
				break;
		}
	}
	FinishQueuedAnimations();
}
/* <<< factory PlayShuffleAndDrawCardsAnimation */

/* >>> factory DisplayDrawOneCardScreen */
void DisplayDrawOneCardScreen(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	a = 1u;
	DisplayDrawNCardsScreen(a, f, b, c, d, e, hl);
}
/* <<< factory DisplayDrawOneCardScreen */

/* >>> factory OppAction_PlayBasicPokemonCard */
void OppAction_PlayBasicPokemonCard(void)
{
	uint8_t card = hTemp_ffa0;
	hTempCardIndex_ff98 = card;
	PutHandPokemonResult placed = PutHandPokemonCardInPlayArea(card, 0u);
	hTempPlayAreaLocation_ff9d = placed.a;
	DuelistVarResult stage = GetTurnDuelistVariable((uint8_t)(placed.a + DUELVARS_ARENA_CARD_STAGE));
	gb_write8(stage.hl, BASIC);
	WaitResult displayed = DisplayCardDetailScreen(card, PlacedOnTheBenchText);
	return;
	(void)ProcessPlayedPokemonCard(card, displayed.f, 0u, 0u, 0u, 0u, 0u);
	DrawDuelMainScene();
}
/* <<< factory OppAction_PlayBasicPokemonCard */
