/* >>> part BUFFERED_ANIM_RESET_OBJ_SIZE */
#define BUFFERED_ANIM_RESET_OBJ_SIZE 1
/* <<< part BUFFERED_ANIM_RESET_OBJ_SIZE */

/* >>> part includes */
#include "home/core.h"
#include <stdio.h>
#include <stdlib.h>

#include "generated/text_ids.h"
#include "generated/rom.h"
#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "bank_guard.h"
#include "mem.h"
#include "home/menus.h"
#include "home/map.h"
#ifdef POKETCG_DEBUG_MENU
#include "debug_cheats.h"
#endif
/* <<< part includes */
/* >>> part kDuelDataToSave */
static const DuelSaveEntry kDuelDataToSave[] = {
	{ wPlayerDuelVariables_ADDR, (uint16_t)(wOpponentDuelVariables_ADDR - wPlayerDuelVariables_ADDR) },
	{ wOpponentDuelVariables_ADDR, (uint16_t)(wPlayerDeck_ADDR - wOpponentDuelVariables_ADDR) },
	{ wPlayerDeck_ADDR, (uint16_t)(wDuelTempList_ADDR - wPlayerDeck_ADDR) },
	{ wWhoseTurn_ADDR, (uint16_t)(wDuelTheme_ADDR + 1u - wWhoseTurn_ADDR) },
	{ hWhoseTurn_ADDR, 1u },
	{ wRNG1_ADDR, (uint16_t)(wRNGCounter_ADDR + 1u - wRNG1_ADDR) },
	{ wAIDuelVars_ADDR, (uint16_t)(wAIDuelVarsEnd_ADDR - wAIDuelVars_ADDR) },
	{ 0u, 0u },
};
/* <<< part kDuelDataToSave */
/* --- part duel_save_total_size */
/* >>> part PRINT_SORT_NUMBER_IN_CARD_LIST */
/* GB address of PrintSortNumberInCardList (engine/duel/core.asm:3438), the
 * routine immediately following the setter: setter start + 15 bytes. The
 * dispatches through. */
#define PRINT_SORT_NUMBER_IN_CARD_LIST PrintSortNumberInCardList_ADDR
/* <<< part PRINT_SORT_NUMBER_IN_CARD_LIST */
/* --- part includes_is_duelist_type */
/* --- part is_duelist_type */
/* >>> part includes_DUELVARS_PRIZE_CARDS */
#include "home/core.h"


#include "home/switch_sram.h"


#include "home/card_color.h"
#include "home/duel.h"

#include "home/effect_commands.h"
#include "home/duel.h"

#include "home/card_color.h"
#include "home/duel.h"
#include "home/duel_core.h"
/* <<< part includes_DUELVARS_PRIZE_CARDS */
/* >>> part play_pokemon_card_in_order */
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
		uint8_t lo = gb_read8(de);
		de++;
		uint8_t hi = gb_read8(de);
		if ((uint8_t)(lo | hi) == 0x00u)
			return (PlayInOrderResult){0x00u, 0x90u, de, *hl};
		RemoveCardIDResult removed = RemoveCardIDInList(hl, (CardId)((uint16_t)hi << 8 | lo));
		de++;
		if ((removed.f & 0x10u) == 0x00u)
			continue;
		PutHandPokemonResult placed = PutHandPokemonCardInPlayArea(removed.a, removed.f);
		return (PlayInOrderResult){placed.a, (uint8_t)((placed.a == 0x00u) ? 0x80u : 0x00u), de, *hl};
	}
}
/* <<< part play_pokemon_card_in_order */
/* >>> part includes_DUEL_OTHER_GFX */
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


#include "home/core.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/core.h"
#include "generated/hram.h"

#include "home/menus.h"

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

#include "home/core.h"
#include "home/tiles.h"
#include "generated/wram.h"
/* <<< part includes_DUEL_OTHER_GFX */
/* >>> part includes_SCREEN_WIDTH */
#include "home/core.h"
#include "home/tiles.h"
#include "home/menus.h"
#include "home/empty_screen.h"
#include "mem.h"

#include "home/duel.h"
#include "home/core.h"
#include "home/load_animation.h"
#include "home/process_text.h"
#include "home/tiles.h"
#include "generated/wram.h"
/* <<< part includes_SCREEN_WIDTH */
/* --- part includes_SPRITE_ANIM_FLAG_UNSKIPPABLE */
/* --- part SPRITE_ANIM_FLAG_UNSKIPPABLE */
/* >>> part includes_SELECT_COMPUTER_OPPONENT_DATA_ADDR_580 */
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

#include "home/core.h"
#include "mem.h"

#include "home/core.h"
#include "home/script.h"
#include "home/print_text.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes_SELECT_COMPUTER_OPPONENT_DATA_ADDR_580 */
/* --- part includes_SPRITE_ANIM_89_850 */
/* --- part SPRITE_ANIM_89_850 */
/* === part PLAY_AREA_BENCH_1_730 */
/* >>> part includes_SAVE_DUEL_CHECKSUM_SEED */
#include "home/core.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes_SAVE_DUEL_CHECKSUM_SEED */
/* >>> part SAVE_DUEL_CHECKSUM_SEED */
#define SAVE_DUEL_CHECKSUM_SEED 0x2345u
/* <<< part SAVE_DUEL_CHECKSUM_SEED */
/* >>> part SAVE_DUEL_HEADER_SIZE */
#define SAVE_DUEL_HEADER_SIZE 4u
/* <<< part SAVE_DUEL_HEADER_SIZE */
/* >>> part kFaceDownCardTileNumbers */
static const uint8_t kFaceDownCardTileNumbers[8] = {
	0xd0u, 0x03u, /* basic */
	0xd4u, 0x03u, /* stage 1 */
	0xd8u, 0x02u, /* stage 2 */
	0xdcu, 0x02u, /* stage 2 special */
};
/* <<< part kFaceDownCardTileNumbers */
/* === part SYM_HP */
/* >>> part includes_hTempPlayAreaLocation_ff9d_ADDR */
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
/* <<< part includes_hTempPlayAreaLocation_ff9d_ADDR */
/* >>> part hTempPlayAreaLocation_ff9d_ADDR */
#define hTempPlayAreaLocation_ff9d_ADDR 0xFF9Du
/* <<< part hTempPlayAreaLocation_ff9d_ADDR */
/* >>> part includes_hTempCardIndex_ff9f_ADDR */
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

#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_hTempCardIndex_ff9f_ADDR */
/* >>> part hTempCardIndex_ff9f_ADDR */
#define hTempCardIndex_ff9f_ADDR 0xFF9Fu
/* <<< part hTempCardIndex_ff9f_ADDR */
/* >>> part hTemp_ffa0_ADDR */
#define hTemp_ffa0_ADDR 0xFFA0u
/* <<< part hTemp_ffa0_ADDR */
/* >>> part includes_V0_TILES1 */
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
#include "generated/wram.h"
#include "mem.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "home/substatus.h"

#include "generated/wram.h"
#include "home/effect_commands.h"

#include "generated/wram.h"
#include "home/duel_core.h"
#include "home/effect_commands.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/card_data.h"
#include "generated/hram.h"
/* <<< part includes_V0_TILES1 */
/* >>> part includes_LARGE_CARD_TILE_DATA */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "home/substatus.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "generated/wram.h"
#include "home/legendary_articuno.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"


#include "generated/wram.h"
#include "home/bg_map.h"
#include "home/credits_sequence_commands.h"
#include "home/duel_core.h"
#include "home/tiles.h"
/* <<< part includes_LARGE_CARD_TILE_DATA */
/* >>> part ITEM_SELECTION_MENU_PARAMETERS */
#define ITEM_SELECTION_MENU_PARAMETERS ItemSelectionMenuParameters_ADDR
/* <<< part ITEM_SELECTION_MENU_PARAMETERS */
/* >>> part includes_COIN_TOSS_7847 */
#include "home/core.h"
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
#include "home/sound.h"
#include "home/text_box.h"
#include "home/tiles.h"
/* <<< part includes_COIN_TOSS_7847 */
/* --- part DUELTYPE_LINK_7847 */
/* --- part TossCoin_CheckTransmissionError */
/* --- part TossCoin_WaitSerialByteRecv */
/* --- part TossCoin_SendSerialByte */
/* === part FLAG_Z_7847 */
/* >>> part TossCoin_SendByte */
static void TossCoin_SendByte(uint8_t a)
{
	hff96 = a;
}
/* <<< part TossCoin_SendByte */
/* >>> part TossCoin_GetOpponentCoinResult */
static uint8_t TossCoin_GetOpponentCoinResult(uint8_t a)
{
	hff96 = a;
	do {
		DoFrame();
	} while (CheckAnyAnimationPlaying().f & FLAG_C_7847);
	return hff96;
}
/* <<< part TossCoin_GetOpponentCoinResult */
/* >>> part TossCoin_WaitForOpponent */
static void TossCoin_WaitForOpponent(uint8_t a)
{
	hff96 = a;
	uint8_t frames = 30u;
	do {
		DoFrame();
		frames = (uint8_t)(frames - 1u);
	} while (frames != 0u);
}
/* <<< part TossCoin_WaitForOpponent */
/* >>> part includes_OPP_EFFECTCMDTYPE_BEFORE_DAMAGE */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/coin_toss.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/duel_core.h"
#include "home/substatus.h"
#include "home/menus.h"
#include "home/coin_toss.h"
#include "generated/wram.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/commands.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/commands.h"
#include "mem.h"

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

#include "generated/wram.h"




#include "generated/wram.h"
#include "home/core.h"
#include "home/empty_screen.h"
#include "home/frames.h"
#include "home/lcd.h"
#include "home/menus.h"
#include "home/play_animation.h"
#include "home/script.h"
#include "home/tiles.h"


#include "generated/hram.h"
#include "generated/wram.h"
#include "home/duel.h"

#include "home/effect_commands.h"
/* <<< part includes_OPP_EFFECTCMDTYPE_BEFORE_DAMAGE */
/* >>> part includes_OPP_METRONOME_CNF_SLP_PRZ */
#include "home/menus.h"
/* <<< part includes_OPP_METRONOME_CNF_SLP_PRZ */
/* --- part includes_SET_LINK_OPPONENT_TURN_FRAME_FUNCTION */
/* --- part SET_LINK_OPPONENT_TURN_FRAME_FUNCTION */
/* >>> part includes_PLAY_POKEMON_CARD_BASIC */
#include "generated/wram.h"
#include "home/duel.h"
#include "home/menus.h"
#include "mem.h"

/* HandlePoisonDamage (core.asm:7071). DUELVARS_ARENA_CARD_HP is already
 * defined above in this module's statics, so only these are missing. */


#include "home/core.h"
#include "home/lcd.h"
#include "generated/wram.h"


#include "home/ai.h"
#include "home/credits_sequence_commands.h"
#include "home/tiles.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#include "home/ai.h"
#include "home/duel.h"
#include "home/duel_menus.h"
#include "home/frames.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "home/script.h"

#include "home/duel_core_state.h"
#include "home/core.h"
#include "home/menus.h"
#include "home/duel.h"

#include "home/screen_effects.h"
#include "home/load_gfx.h"

#include "home/core.h"
#include "home/sound.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/ai.h"
#include "home/core.h"
#include "home/duel.h"

#include "home/core.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "home/script.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/duel_menus.h"
#include "home/core.h"

#include "generated/hram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/ai.h"
#include "home/duel.h"
#include "home/core.h"
#include "home/menus.h"
#include "home/script.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/duel_core_state.h"
#include "home/substatus.h"
#include "home/core.h"


#include "home/core.h"
#include "home/substatus.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/duel.h"

#include "home/duel.h"
#include "home/core.h"

#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "home/menus.h"

#include "home/frames.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/duel_core_state.h"
#include "home/substatus.h"

#include "generated/wram.h"
#include "home/duel.h"

#include "generated/wram.h"
#include "home/lcd.h"

#include "home/core.h"
#include "home/input.h"
#include "home/sound.h"
#include "generated/wram.h"

#include "home/core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/menus.h"
#include "home/print_text.h"
#include "home/substatus.h"
#include "mem.h"
/* <<< part includes_PLAY_POKEMON_CARD_BASIC */
/* >>> part PLAY_POKEMON_CARD_OPP_EVOLVE */
#define PLAY_POKEMON_CARD_OPP_EVOLVE 0x01u
/* <<< part PLAY_POKEMON_CARD_OPP_EVOLVE */
/* >>> part PLAY_POKEMON_CARD_OPP_BASIC */
#define PLAY_POKEMON_CARD_OPP_BASIC 0x00u
/* <<< part PLAY_POKEMON_CARD_OPP_BASIC */
/* --- factory ValidateSavedDuelDataFromHL */
/* --- factory CopyCGBCardPalette */
/* --- factory CreateCardAttrBlkPacket_DataSet */
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
	uint32_t bc = 0x334u;
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
/* --- factory LoadSavedDuelDataFromDE */
/* --- factory SetBGP7OrSGB2ToCardPalette */
/* --- factory JPWriteByteToBGMap0 */
/* >>> factory LoadPlayerDeck */
/* core.asm:6195-6211 */
void LoadPlayerDeck(void)
{
	EnableSRAM();
	uint8_t sel = gb_read8(sCurrentlySelectedDeck_ADDR);
	uint16_t de = HtimesL((uint16_t)(sel << 8 | (sDeck2Cards_ADDR - sDeck1Cards_ADDR)));
	de = (uint16_t)(de + sDeck1Cards_ADDR);
	DecompressSRAMDeck(de, wPlayerDeck_ADDR);
	DisableSRAM();
}
/* <<< factory LoadPlayerDeck */
/* >>> part DispatchOppAction */
/* core.asm:6246-6247: JumpToFunctionInTable(OppActionTable), core.asm:6487.
 * $08 skips OppAction_BeginUseAttack's own HRAM preamble in C, so the
 * dispatch supplies d/e from hTempCardIndex_ff9f/hTemp_ffa0 itself. */
static void DispatchOppAction(uint8_t action, uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	switch (action) {
	case 0x00u: OppAction_PlayBasicPokemonCard(); break;
	case 0x01u: OppAction_EvolvePokemonCard(); break;
	case 0x02u: OppAction_PlayEnergyCard(); break;
	case 0x03u: (void)OppAction_AttemptRetreat(); break;
	case 0x04u: OppAction_FinishTurnWithoutAttacking(); break;
	case 0x05u: OppAction_PlayTrainerCard(); break;
	case 0x06u: OppAction_ExecuteTrainerCardEffectCommands(b, d, e); break;
	case 0x07u:
		(void)OppAction_BeginUseAttack(action, 0u, b, c,
			hTempCardIndex_ff9f, hTemp_ffa0, 0u);
		break;
	case 0x08u: (void)OppAction_UseAttack(b, d, e); break;
	case 0x09u: OppAction_PlayAttackAnimationDealAttackDamage(); break;
	case 0x0Au: (void)OppAction_DrawCard(); break;
	case 0x0Bu: OppAction_UsePokemonPower(); break;
	case 0x0Cu: (void)OppAction_ExecutePokemonPowerEffect(b, d, e); break;
	case 0x0Du: OppAction_ForceSwitchActive(); break;
	case 0x0Eu:
	case 0x0Fu:
	case 0x12u:
		OppAction_NoAction();
		break;
	case 0x10u: (void)OppAction_TossCoinATimes(action, 0u, b, c, d, e, 0u); break;
	case 0x11u: (void)OppAction_6b30(); break;
	case 0x13u: OppAction_UseMetronomeAttack(b, c, d, e); break;
	case 0x14u: (void)OppAction_6b15(); break;
	case 0x15u: OppAction_DrawDuelMainScene(); break;
	default:
		abort();
	}
}
/* <<< part DispatchOppAction */
/* --- factory SetSGB3ToCardPalette */
/* >>> factory LookForCardIDInPlayArea_Bank5 */
/* core.asm:753-777 */
LookResult LookForCardIDInPlayArea_Bank5(uint16_t de, uint8_t b)
{
	for (;;) {
		DuelistVarResult r = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + b));
		if (r.a == 0xFFu)
			return (LookResult){r.a, b, 0xC0u};
		(void)LoadCardDataToBuffer1_FromDeckIndex(r.a);
		CardId card_id = card_id_read_at(wLoadedCard1ID_ADDR);
		if (de == card_id)
			return (LookResult){b, b, 0x90u};
		b++;
		if (b == MAX_PLAY_AREA_POKEMON)
			return (LookResult){MAX_PLAY_AREA_POKEMON, 0xFFu, 0x00u};
	}
}
/* <<< factory LookForCardIDInPlayArea_Bank5 */
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
	const uint8_t *entry = rom_ptr(ANIM_DATA_BANK, (uint16_t)(ANIM_COORDS_ADDR + (uint16_t)index * 3u));
	uint8_t x = entry[0];
	uint8_t y = entry[1];
	uint8_t flags = (uint8_t)(wAnimFlags & entry[2]);
	uint8_t f = (uint8_t)((flags == 0u ? 0x80u : 0u) | 0x20u);
	return (AnimCoordsResult){flags, f, x, y};
}
/* <<< factory GetAnimCoordsAndFlags */
/* >>> factory CheckEnergyFlagsNeededInList */
/* core.asm:1581-1658 */
EnergyFlagsResult CheckEnergyFlagsNeededInList(uint8_t a)
{
	uint8_t required = a;
	uint16_t hl = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl++);
		if (deck_index == 0xffu)
			return (EnergyFlagsResult){0xffu, 0u, required};

		CardId energy = GetCardIDFromDeckIndex(deck_index);
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
			return (EnergyFlagsResult){intersection, 1u, required};
	}
}
/* <<< factory CheckEnergyFlagsNeededInList */
/* --- factory PlaceCardImageOAM */
/* >>> factory PrintEnergiesOfColor */
/* core.asm:4416-4431 */
PrintEnergiesResult PrintEnergiesOfColor(uint8_t a, uint8_t b, uint8_t c, uint8_t e)
{
	uint8_t count;
	uint8_t value;

	e = (uint8_t)(e + 1u);
	count = (uint8_t)(a & 0x0Fu);
	if (count == 0u)
		return (PrintEnergiesResult){count, b, e};

	value = e;
	uint8_t written = value;
	do {
		written = WriteByteToBGMap0(value, b, c);
		b = (uint8_t)(b + 1u);
	} while (--count);

	return (PrintEnergiesResult){written, b, e};
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
			WriteByteToBGMap0(type, b, c);
			b = (uint8_t)(b + 1u);
		}
		mask = (uint8_t)(mask << 1);
	}
}
/* <<< factory PrintCardPageWeaknessesOrResistances */
/* --- factory Func_6423 */
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
	if ((a & DUELIST_TYPE_AI_OPP) == 0u) {
		a = wOpponentDuelistType;
		if ((a & DUELIST_TYPE_AI_OPP) == 0u)
			a = 0u;
	}
	wDuelType = a;
}
/* <<< factory InitVariablesToBeginDuel */
/* --- factory CreateCardAttrBlkPacket */
/* --- factory Func_14323 */
/* >>> factory CreateEnergyCardListFromHand */
CoreCardListResult CreateEnergyCardListFromHand(uint8_t a)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	uint16_t hand = (uint16_t)(((uint16_t)hWhoseTurn << 8) | DUELVARS_HAND);
	uint16_t dst = wDuelTempList_ADDR;
	uint8_t remaining = count;
	(void)a;
	while (remaining != 0u) {
		uint8_t deck_index = gb_read8(hand++);
		CardId card_id = GetCardIDFromDeckIndex(deck_index);
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
CoreCardListResult LookForCardIDInHand(CardId de)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	uint16_t hand = (uint16_t)(((uint16_t)hWhoseTurn << 8) | DUELVARS_HAND);
	uint8_t remaining = count;
	uint8_t last_a = 0u;
	while (remaining != 0u) {
		uint8_t deck_index = gb_read8(hand++);
		CardId card_id = GetCardIDFromDeckIndex(deck_index);
		uint8_t high = (uint8_t)(card_id >> 8);
		uint8_t target_high = (uint8_t)(de >> 8);
		last_a = high != target_high ? high : (uint8_t)card_id;
		if (card_id == de)
			return (CoreCardListResult){deck_index, deck_index == 0u ? 0x80u : 0x00u};
		remaining--;
	}
	return (CoreCardListResult){last_a, 0x90u};
}
/* <<< factory LookForCardIDInHand */
/* >>> factory LookForCardIDInHandList_Bank5 */
/* ai/core.asm:724-742. Every candidate index is parked in
 * hTempCardIndex_ff98 as it is tried; the card id to find in wTempCardIDToLook. */
CoreCardListResult LookForCardIDInHandList_Bank5(CardId de)
{
	(void)CreateHandCardList(0u);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			return (CoreCardListResult){0xFFu, 0xC0u};
		hTempCardIndex_ff98 = deck_index;
		(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (card_id_read_at(wLoadedCard1ID_ADDR) == de)
			return (CoreCardListResult){deck_index, 0x90u};
	}
}
/* <<< factory LookForCardIDInHandList_Bank5 */
/* >>> factory GetAnimationData */
AnimationDataResult GetAnimationData(void)
{
	uint8_t animation = wTempAnimation;
	uint16_t offset = (uint16_t)animation * 5u;
	uint16_t address = (uint16_t)(ANIMATIONS_ADDR + offset);
	uint8_t f = 0u;
	if (((offset & 0x0fffu) + (ANIMATIONS_ADDR & 0x0fffu)) > 0x0fffu)
		f |= 0x20u;
	if (address < ANIMATIONS_ADDR)
		f |= 0x10u;
	return (AnimationDataResult){animation, f, address};
}
/* <<< factory GetAnimationData */
/* >>> factory GetDamageNumberChars_ConvertDigitToCharTile */
DamageDigitResult GetDamageNumberChars_ConvertDigitToCharTile(uint16_t bc, uint16_t de, uint16_t hl)
{
	uint8_t chr = SPRITE_ANIM_DAMAGE_0 - 1u;
	uint16_t value = hl;
	for (;;) {
		chr = (uint8_t)(chr + 1u);
		uint32_t sum = (uint32_t)value + (uint32_t)bc;
		value = (uint16_t)sum;
		if (!(sum & 0x10000u))
			break;
	}
	gb_write8(de, chr);
	de = (uint16_t)(de + 1u);

	uint8_t c = (uint8_t)bc;
	uint8_t b = (uint8_t)(bc >> 8);
	uint8_t lo = (uint8_t)value;
	uint8_t hi = (uint8_t)(value >> 8);
	uint8_t borrow = (uint8_t)(lo < c);
	uint8_t new_lo = (uint8_t)(lo - c);
	uint8_t new_hi = (uint8_t)(hi - b - borrow);
	uint8_t f = (uint8_t)(0x40u
		| (new_hi == 0u ? 0x80u : 0u)
		| (((hi & 0x0Fu) < ((b & 0x0Fu) + borrow)) ? 0x20u : 0u)
		| (((uint16_t)hi < (uint16_t)b + borrow) ? 0x10u : 0u));
	return (DamageDigitResult){new_hi, f, de, (uint16_t)(((uint16_t)new_hi << 8) | new_lo)};
}
/* <<< factory GetDamageNumberChars_ConvertDigitToCharTile */
/* >>> factory GetDamageNumberChars */
void GetDamageNumberChars(void)
{
	uint16_t hl = (uint16_t)(wDuelAnimDamage |
		((uint16_t)gb_read8((uint16_t)(wDuelAnimDamage_ADDR + 1u)) << 8));
	DamageDigitResult digit = GetDamageNumberChars_ConvertDigitToCharTile(
		(uint16_t)-100, wDecimalChars_ADDR, hl);
	digit = GetDamageNumberChars_ConvertDigitToCharTile((uint16_t)-10, digit.de, digit.hl);
	gb_write8(digit.de, (uint8_t)((uint8_t)digit.hl + SPRITE_ANIM_DAMAGE_0));

	uint16_t scan = wDecimalChars_ADDR;
	for (uint8_t count = 2u; count != 0u; count--) {
		if (gb_read8(scan) != SPRITE_ANIM_DAMAGE_0)
			break;
		gb_write8(scan, 0x00u);
		scan = (uint16_t)(scan + 1u);
	}
}
/* <<< factory GetDamageNumberChars */
/* === factory CardPageSwitch_PokemonAttack2Page2 */
/* --- factory LoadLoaded1CardGfx */
/* >>> factory LoadLoaded1CardGfx */
void LoadLoaded1CardGfx(uint16_t de)
{
	uint16_t hl = (uint16_t)(gb_read8(wLoadedCard1Gfx_ADDR)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard1Gfx_ADDR + 1u)) << 8);
	LoadCardGfx(hl, de, 0x30u, TILE_SIZE);
}
/* <<< factory LoadLoaded1CardGfx */
/* --- factory SetBGP6OrSGB3ToCardPalette */
/* --- factory ResetDoFrameFunction_Bank1 */
/* >>> factory HandleFailedToContinueDuel */
/* core.asm:23-30 */
uint8_t HandleFailedToContinueDuel(uint16_t hl)
{
	(void)DrawWideTextBox_WaitForInput(hl);
	return (uint8_t)(0x80u | 0x10u);
}
/* <<< factory HandleFailedToContinueDuel */
/* --- factory Func_6ba2 */
/* >>> factory IsLoadedCard1BasicPokemon */
/* core.asm:2048-2081 */
IsLoadedCard1BasicPokemonResult IsLoadedCard1BasicPokemon(void)
{
	CardId id = card_id_read_at(wLoadedCard1ID_ADDR);
	if (id == MYSTERIOUS_FOSSIL || id == CLEFAIRY_DOLL)
		return (IsLoadedCard1BasicPokemonResult){1u, 0u};
	if (wLoadedCard1Type >= 0x08u || wLoadedCard1Stage != 0u)
		return (IsLoadedCard1BasicPokemonResult){0u, 0x90u};
	return (IsLoadedCard1BasicPokemonResult){1u, 0x80u};
}
/* <<< factory IsLoadedCard1BasicPokemon */
/* >>> factory PracticeDuel_PlayGoldeen */
PracticeDuelPlayGoldeenResult PracticeDuel_PlayGoldeen(void)
{
	if (card_id_read_at(wLoadedCard1ID_ADDR) == GOLDEEN)
		return (PracticeDuelPlayGoldeenResult){0xC0u};
	PrintPracticeDuelDrMasonInstructions(0x01A5u);
	return (PracticeDuelPlayGoldeenResult){0x10u};
}
/* <<< factory PracticeDuel_PlayGoldeen */
/* --- factory TwoByteNumberToTxSymbol_PadSpace_Bank1 */
/* >>> factory LookForCardIDInLocation_Bank5 */
LookForCardIDInLocationResult LookForCardIDInLocation_Bank5(
	uint8_t location, CardId card_id)
{
	uint8_t index = 0u;
	uint16_t hl = 0u;
	for (;;) {
		DuelistVarResult locations = GetTurnDuelistVariable(index);
		hl = locations.hl;
		if (locations.a == location &&
		    GetCardIDFromDeckIndex(index) == card_id)
			return (LookForCardIDInLocationResult){index,
				(uint8_t)(card_id >> 8), (uint8_t)card_id,
				location, index, 0x90u, hl};
		index++;
		if (index == DECK_SIZE)
			return (LookForCardIDInLocationResult){DECK_SIZE,
				(uint8_t)(card_id >> 8), (uint8_t)card_id,
				location, DECK_SIZE, 0x00u, hl};
	}
}
/* <<< factory LookForCardIDInLocation_Bank5 */
/* >>> factory CheckIfEnergyIsUseful */
CheckIfEnergyIsUsefulResult CheckIfEnergyIsUseful(uint8_t a)
{
	CardId energy = GetCardIDFromDeckIndex(a);
	CardId pokemon = card_id_read_at(wTempCardID_ADDR);
	if (energy == DOUBLE_COLORLESS_ENERGY || wTempCardType == TYPE_ENERGY_DOUBLE_COLORLESS)
		return (CheckIfEnergyIsUsefulResult){0x90u};
	CardId required = 0u;
	if (pokemon == EXEGGCUTE || pokemon == EXEGGUTOR ||
	    pokemon == PSYDUCK || pokemon == GOLDUCK)
		required = PSYCHIC_ENERGY;
	else if (pokemon == SURFING_PIKACHU_LV13 ||
	         pokemon == SURFING_PIKACHU_ALT_LV13)
		required = WATER_ENERGY;
	if (required != 0u && energy == required)
		return (CheckIfEnergyIsUsefulResult){0x90u};
	if (pokemon == EEVEE &&
	    (energy == WATER_ENERGY || energy == FIRE_ENERGY || energy == LIGHTNING_ENERGY))
		return (CheckIfEnergyIsUsefulResult){0x90u};
	return (CheckIfEnergyIsUsefulResult){GetCardType(energy) == wTempCardType ? 0x90u : 0u};
}
/* <<< factory CheckIfEnergyIsUseful */
/* >>> factory PracticeDuel_VerifyPlayerTurnActions */
/* core.asm:2701-2712 */
/* core.asm:2701-2722. wDuelTurns >> 1 indexes PracticeDuelTurnVerificationPointerTable
 * (core.asm:2912-2920); a wrong action falls through into
 * PracticeDuel_RepeatInstructions, which restores the turn's saved duel data
 * and returns carry. */
PracticeDuelTurnActionsResult PracticeDuel_VerifyPlayerTurnActions(void)
{
	uint8_t f;
	switch ((uint8_t)(wDuelTurns >> 1)) {
	case 0: f = PracticeDuelVerify_Turn1().f; break;
	case 1: f = PracticeDuelVerify_Turn2().f; break;
	case 2: f = PracticeDuelVerify_Turn3().f; break;
	case 3: f = PracticeDuelVerify_Turn4().f; break;
	case 4: f = PracticeDuelVerify_Turn5().f; break;
	case 5: f = PracticeDuelVerify_Turn6().f; break;
	default: f = PracticeDuelVerify_Turn7Or8().f; break;
	}
	if ((f & 0x10u) == 0u)
		return (PracticeDuelTurnActionsResult){f};
	(void)PracticeDuel_RepeatInstructions();
	return (PracticeDuelTurnActionsResult){FLAG_C};
}
/* <<< factory PracticeDuel_VerifyPlayerTurnActions */
/* >>> factory PrintCardNameFromCardIDInTextBox */
void PrintCardNameFromCardIDInTextBox(uint16_t hl)
{
	CardId card_id = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR) |
		(uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	(void)DrawWideTextBox_PrintText(hl);
}
/* <<< factory PrintCardNameFromCardIDInTextBox */
/* >>> factory RemoveCardIDInList */
RemoveCardIDResult RemoveCardIDInList(uint16_t *hl, CardId de)
{
	uint16_t scan = *hl;
	for (;;) {
		uint8_t index = gb_read8(scan++);
		if (index == 0xFFu)
			return (RemoveCardIDResult){index, 0x00u};
		hTempCardIndex_ff98 = index;
		if (GetCardIDFromDeckIndex(index) != de)
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
SortTempHandResult SortTempHandByIDList(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	if (gb_read8((uint16_t)(wAICardListPlayFromHandPriority_ADDR + 1u)) == 0u)
		return (SortTempHandResult){0u, 0x80u, b, c, d, e, hl};

	uint16_t de = (uint16_t)(gb_read8(wAICardListPlayFromHandPriority_ADDR) |
		((uint16_t)gb_read8((uint16_t)(wAICardListPlayFromHandPriority_ADDR + 1u)) << 8));
	c = 0u;
	for (;;) {
		if ((uint8_t)(gb_read8(de) | gb_read8((uint16_t)(de + 1u))) == 0u)
			return (SortTempHandResult){0u, 0x80u, 0u, c,
				(uint8_t)(de >> 8), (uint8_t)de, hl};
		de++;
		hl = (uint16_t)(wDuelTempList_ADDR + c);
		for (;;) {
			uint8_t entry = gb_read8(hl);
			hTempCardIndex_ff98 = entry;
			if (entry == 0xFFu)
				break;
			CardId wanted = (CardId)(gb_read8(de) |
				((uint16_t)gb_read8((uint16_t)(de + 1u)) << 8));
			if (GetCardIDFromDeckIndex(entry) == wanted) {
				uint16_t slot = (uint16_t)(wDuelTempList_ADDR + c);
				uint8_t old = gb_read8(slot);
				gb_write8(slot, hTempCardIndex_ff98);
				gb_write8(hl, old);
				c++;
			}
			hl++;
		}
	}
}
/* <<< factory SortTempHandByIDList */
/* >>> factory ApplyCardCGBAttributes */
ApplyCardCGBAttributesResult ApplyCardCGBAttributes(uint8_t a, uint16_t de)
{
	(void)a;
	hBankVRAM = 1u;
	gb_write8(0xFF4Fu, 1u);
	uint16_t src = wCardAttrMap_ADDR;
	uint16_t dst = DECoordToBGMap0Address((uint8_t)(de >> 8), (uint8_t)de);
	for (uint8_t row = 0u; row < 6u; row++) {
		SafeCopyDataHLtoDE(&src, &dst, 8u);
		dst = (uint16_t)(dst + (TILEMAP_WIDTH - 8u));
	}
	hBankVRAM = 0u;
	gb_write8(0xFF4Fu, 0u);
	return (ApplyCardCGBAttributesResult){8u, 0u, dst, src};
}
/* <<< factory ApplyCardCGBAttributes */
/* >>> factory SetCardPalette */
void SetCardPalette(uint8_t a)
{
	uint16_t src = wCardPalette_ADDR;
	uint8_t offset = (uint8_t)(a * PAL_SIZE);
	uint16_t dst = (uint16_t)(wBackgroundPalettesCGB_ADDR + offset);
	for (uint8_t i = 0u; i < 3u * PAL_SIZE; i++)
		gb_write8(dst++, gb_read8(src++));
	for (uint8_t i = 0u; i < 0x30u; i++) {
		uint16_t addr = (uint16_t)(wCardAttrMap_ADDR + i);
		gb_write8(addr, (uint8_t)(gb_read8(addr) + a));
	}
}
/* <<< factory SetCardPalette */
/* >>> factory SetBGP2ToCardPalette */
void SetBGP2ToCardPalette(void)
{
	SetCardPalette(2u);
}
/* <<< factory SetBGP2ToCardPalette */
/* >>> factory SetBGP5ToCardPalette */
void SetBGP5ToCardPalette(void)
{
	SetCardPalette(5u);
}
/* <<< factory SetBGP5ToCardPalette */
/* --- factory DecideLinkDuelVariables */
/* >>> factory DrawDuelHorizontalSeparator */
/* core.asm:2582-2616. The blocks are x, y, bytes[], 0: row 4 from x=0 for 11
 * tiles, rows 5-6 two tiles at x=9, row 7 from x=9 for 11 -- the separator
 * sits under the opponent's HUD, not at the left edge. CGB writes the same
 * blocks of palette 2 into VRAM bank 1. */
#define DUEL_HORIZONTAL_SEPARATOR_TILE_DATA DuelHorizontalSeparatorTileData_ADDR
#define DUEL_HORIZONTAL_SEPARATOR_CGB_PAL_DATA DuelHorizontalSeparatorCGBPalData_ADDR
void DrawDuelHorizontalSeparator(void)
{
	uint16_t data = DUEL_HORIZONTAL_SEPARATOR_TILE_DATA;
	uint16_t bg_map = 0u;
	uint8_t a = 0u, b = 0u, c = 0u;

	WriteDataBlocksToBGMap0(&data, &bg_map, &a, &b, &c);
	hBankVRAM = 1u;
	gb_write8(0xFF4Fu, 1u);
	data = DUEL_HORIZONTAL_SEPARATOR_CGB_PAL_DATA;
	WriteDataBlocksToBGMap0(&data, &bg_map, &a, &b, &c);
	hBankVRAM = 0u;
	gb_write8(0xFF4Fu, 0u);
}
/* <<< factory DrawDuelHorizontalSeparator */
/* --- factory Func_1585b */
/* === factory CardPageSwitch_TrainerPage2 */
/* >>> factory ValidateSavedDuelData */
ValidateSavedDuelDataResult ValidateSavedDuelData(uint16_t hl)
{
	EnableSRAM();
	uint8_t valid = gb_read8(hl++);
	uint8_t f;
	uint8_t e = (uint8_t)(SAVE_DUEL_CHECKSUM_SEED & 0xFFu);
	uint8_t d = (uint8_t)(SAVE_DUEL_CHECKSUM_SEED >> 8);
	if (valid != 0u) {
		e = (uint8_t)(gb_read8(hl) - e);
		hl++;
		d = (uint8_t)(gb_read8(hl) ^ d);
		hl = (uint16_t)(hl + 2u);
		uint32_t bc = 0x334u;
		while (bc != 0u) {
			uint8_t value = gb_read8(hl);
			e = (uint8_t)(e + value);
			value = gb_read8(hl++);
			d = (uint8_t)(d ^ value);
			bc--;
		}
		f = (e != 0u || d != 0u) ? 0x10u : 0x80u;
	} else {
		f = 0x90u;
	}
	DisableSRAM();
	return (ValidateSavedDuelDataResult){f, hl};
}
/* <<< factory ValidateSavedDuelData */
/* >>> factory LoadSavedDuelData */
void LoadSavedDuelData(uint16_t de)
{
	EnableSRAM();
	de = (uint16_t)(de + SAVE_DUEL_HEADER_SIZE);
	for (int i = 0; kDuelDataToSave[i].addr != 0u; i++) {
		uint16_t hl = kDuelDataToSave[i].addr;
		uint16_t bc = kDuelDataToSave[i].size;
		while (bc != 0u) {
			gb_write8(hl++, gb_read8(de++));
			bc--;
		}
	}
	DisableSRAM();
}
/* <<< factory LoadSavedDuelData */
/* >>> factory DiscardSavedDuelData */
void DiscardSavedDuelData(void)
{
	EnableSRAM();
	gb_write8(sCurrentDuel_ADDR, 0u);
	gb_write8(sCurrentDuelChecksum_ADDR, 0u);
	gb_write8((uint16_t)(sCurrentDuelChecksum_ADDR + 1u), 0u);
	DisableSRAM();
}
/* <<< factory DiscardSavedDuelData */
/* >>> factory LoadAndValidateDuelSaveData */
/* core.asm:6063-6084. */
uint8_t LoadAndValidateDuelSaveData(void)
{
	ValidateSavedDuelDataResult duel = ValidateSavedDuelData(sCurrentDuel_ADDR);
	if (duel.f & 0x10u)
		return duel.f;

	LoadSavedDuelData(sCurrentDuel_ADDR);

	uint8_t general_f = ValidateGeneralSaveData().f;
	if (!(general_f & 0x10u))
		return general_f;

	LoadGeneralSaveData();
	return 0x00u;
}
/* <<< factory LoadAndValidateDuelSaveData */
/* --- factory ValidateSavedNonLinkDuelData */
/* >>> factory SaveDuelData */
void SaveDuelData(void)
{
	SaveDuelDataToDE(sCurrentDuel_ADDR);
}
/* <<< factory SaveDuelData */
/* >>> factory AIAttachEnergyInHandToCardInPlayArea */
AIAttachEnergyInHandToCardInPlayAreaResult AIAttachEnergyInHandToCardInPlayArea(CardId bc, CardId de)
{
	CoreCardListResult hand = LookForCardIDInHandList_Bank5(de);
	if ((hand.f & 0x10u) == 0u)
		return (AIAttachEnergyInHandToCardInPlayAreaResult){hand.a, hand.f};
	hTemp_ffa0 = hand.a;
	LookResult location = LookForCardIDInPlayArea_Bank5(bc, PLAY_AREA_ARENA);
	hTempPlayAreaLocation_ffa1 = location.a;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_PLAY_ENERGY, 0u, 0u, 0u, 0u);
	return (AIAttachEnergyInHandToCardInPlayAreaResult){decision.a, decision.f};
}
/* <<< factory AIAttachEnergyInHandToCardInPlayArea */
/* >>> factory PracticeDuelVerify_Turn7Or8 */
PracticeDuelVerifyTurn7Or8Result PracticeDuelVerify_Turn7Or8(void)
{
	if (card_id_read_at(wTempCardID_ccc2_ADDR) != STARMIE)
		return (PracticeDuelVerifyTurn7Or8Result){0x10u};
	uint8_t attack = gb_read8(wSelectedAttack_ADDR);
	if (attack != SECOND_ATTACK)
		return (PracticeDuelVerifyTurn7Or8Result){0x10u};
	return (PracticeDuelVerifyTurn7Or8Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn7Or8 */
/* >>> factory PracticeDuelVerify_Turn6 */
PracticeDuelVerifyTurn6Result PracticeDuelVerify_Turn6(void)
{
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	if (wAttachedEnergies_PTR[WATER] != 3u)
		return (PracticeDuelVerifyTurn6Result){0x10u};
	if (*wPlayerArenaCardHP_PTR != 40u)
		return (PracticeDuelVerifyTurn6Result){0x10u};
	if (card_id_read_at(wTempCardID_ccc2_ADDR) != STARYU)
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
	if (card_id_read_at(wTempCardID_ccc2_ADDR) != SEAKING)
		return (PracticeDuelVerifyTurn4Result){ReturnWrongAction(0u)};
	if (gb_read8(wSelectedAttack_ADDR) != SECOND_ATTACK)
		return (PracticeDuelVerifyTurn4Result){ReturnWrongAction(0u)};
	return (PracticeDuelVerifyTurn4Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn4 */
/* >>> factory HandleDuelSetup */
HandleDuelSetupResult HandleDuelSetup(void)
{
retry:
	DuelCoreStateWideResult init = InitializeDuelVariables();
	SwapTurn();
	init = InitializeDuelVariables();
	SwapTurn();
	(void)PlayShuffleAndDrawCardsAnimation_BothDuelists(init.b, init.c, init.d, init.e, init.hl);
	ShuffleDeckAndDrawSevenCardsResult first_draw = ShuffleDeckAndDrawSevenCards();
	hTemp_ffa0 = first_draw.a;
	SwapTurn();
	ShuffleDeckAndDrawSevenCardsResult second_draw = ShuffleDeckAndDrawSevenCards();
	SwapTurn();
	uint8_t opponent_basic = hTemp_ffa0;
	uint8_t player_basic = second_draw.a;
	if ((uint8_t)(opponent_basic & player_basic) == 0u) {
		if ((uint8_t)(opponent_basic | player_basic) == 0u) {
			(void)DrawWideTextBox_WaitForInput(TX_NEITHER_BASIC);
			DisplayNoBasicPokemonInHandScreen();
			(void)InitializeDuelVariables();
			SwapTurn();
			DisplayNoBasicPokemonInHandScreen();
			(void)InitializeDuelVariables();
			SwapTurn();
			(void)PrintReturnCardsToDeckDrawAgain();
			goto retry;
		}
		if (opponent_basic != 0u)
			SwapTurn();
		for (;;) {
			(void)DisplayNoBasicPokemonInHandScreenAndText();
			DuelCoreStateWideResult reset = InitializeDuelVariables();
			PlayShuffleAndDrawCardsAnimation_TurnDuelist(
				reset.a, reset.f, reset.b, reset.c, reset.d, reset.e, reset.hl);
			ShuffleDeckAndDrawSevenCardsResult draw = ShuffleDeckAndDrawSevenCards();
			if ((draw.f & FLAG_C) == 0u)
				break;
		}
		if (opponent_basic != 0u)
			SwapTurn();
	}
	uint8_t saved_turn = hWhoseTurn;
	hWhoseTurn = PLAYER_TURN;
	(void)ChooseInitialArenaAndBenchPokemon();
	SwapTurn();
	ChooseInitialArenaAndBenchPokemonResult chosen = ChooseInitialArenaAndBenchPokemon();
	SwapTurn();
	if ((chosen.f & FLAG_C) != 0u) {
		hWhoseTurn = saved_turn;
		return (HandleDuelSetupResult){FLAG_C};
	}
	DrawPlayAreaToPlacePrizeCards();
	(void)DrawWideTextBox_WaitForInput(TX_PLACING_PRIZES);
	LoadTxRam3((uint16_t)wDuelInitialPrizes);
	(void)DrawWideTextBox_PrintText(TX_PLACE_PRIZES);
	EnableLCD();
	static const uint8_t prize_coordinates[] = {
		5u, 6u, 14u, 5u, 6u, 6u, 13u, 5u, 5u, 7u, 14u, 4u,
		6u, 7u, 13u, 4u, 5u, 8u, 14u, 3u, 6u, 8u, 13u, 3u,
	};
	uint8_t coordinate_index = 0u;
	uint8_t deck_index = (uint8_t)(DECK_SIZE - 7u - 1u);
	uint8_t prizes_left = wDuelInitialPrizes;
	for (;;) {
		uint8_t frames = 20u;
		while (frames != 0u) {
			DoFrame();
			CheckSkipDelayAllowedResult skip =
				CheckSkipDelayAllowed(0u, frames, 0u, prizes_left, deck_index, 0u);
			if ((skip.f & FLAG_C) != 0u)
				break;
			frames--;
		}
		uint8_t x = prize_coordinates[coordinate_index++];
		uint8_t y = prize_coordinates[coordinate_index++];
		WriteByteToBGMap0(0xACu, x, y);
		x = prize_coordinates[coordinate_index++];
		y = prize_coordinates[coordinate_index++];
		WriteByteToBGMap0(0xACu, x, y);
		PlaySFX(SFX_PLACE_PRIZE);
		WriteTwoDigitNumberInTxSymbolFormat(deck_index, 3u, 5u);
		WriteTwoDigitNumberInTxSymbolFormat(deck_index, 18u, 7u);
		deck_index--;
		prizes_left--;
		if (prizes_left == 0u)
			break;
	}
	(void)WaitForWideTextBoxInput();
	hWhoseTurn = saved_turn;
	(void)InitTurnDuelistPrizes();
	SwapTurn();
	(void)InitTurnDuelistPrizes();
	SwapTurn();
	EmptyScreen();
	DrawDuelBoxMessage(BOXMSG_COIN_TOSS);
	(void)DrawWideTextBox_WaitForInput(TX_COIN_TOSS);
	WaitResult final;
	if (hWhoseTurn == PLAYER_TURN) {
		(void)CopyPlayerName(wDefaultText_ADDR);
		LoadTxRam2(0u);
		TossCoinRoutineResult toss = TossCoin(TX_IF_HEADS, TX_YOU_PLAY_FIRST);
		if ((toss.f & FLAG_C) == 0u)
			SwapTurn();
		final = DrawWideTextBox_WaitForInput(
			toss.f & FLAG_C ? TX_YOU_PLAY_FIRST : TX_YOU_PLAY_SECOND);
	} else {
		(void)CopyOpponentName(wDefaultText_ADDR);
		LoadTxRam2(0u);
		TossCoinRoutineResult toss = TossCoin(TX_IF_HEADS, TX_YOU_PLAY_SECOND);
		if ((toss.f & FLAG_C) == 0u)
			SwapTurn();
		final = DrawWideTextBox_WaitForInput(
			toss.f & FLAG_C ? TX_YOU_PLAY_SECOND : TX_YOU_PLAY_FIRST);
	}
	return (HandleDuelSetupResult){final.a == 0u ? FLAG_Z : 0u};
}
/* <<< factory HandleDuelSetup */
/* --- factory WriteTwoDigitNumberInTxSymbol_PadSpace */
/* >>> factory PrintOpponentNumberOfHandAndDeckCards */
void PrintOpponentNumberOfHandAndDeckCards(void)
{
	uint8_t hand = (uint8_t)(wOpponentNumberOfCardsInHand + wNumCardsBeingDrawn);
	uint8_t deck = (uint8_t)(DECK_SIZE - wOpponentNumberOfCardsNotInDeck - wNumCardsBeingDrawn);
	WriteTwoDigitNumberInTxSymbolFormat(hand, 5u, 3u);
	WriteTwoDigitNumberInTxSymbolFormat(deck, 11u, 3u);
}
/* <<< factory PrintOpponentNumberOfHandAndDeckCards */
/* >>> factory PrintPlayerNumberOfHandAndDeckCards */
void PrintPlayerNumberOfHandAndDeckCards(void)
{
	uint8_t hand = (uint8_t)(wPlayerNumberOfCardsInHand + wNumCardsBeingDrawn);
	uint8_t deck = (uint8_t)(DECK_SIZE - wPlayerNumberOfCardsNotInDeck - wNumCardsBeingDrawn);
	WriteTwoDigitNumberInTxSymbolFormat(hand, 16u, 10u);
	WriteTwoDigitNumberInTxSymbolFormat(deck, 10u, 10u);
}
/* <<< factory PrintPlayerNumberOfHandAndDeckCards */
/* >>> factory PrintDuelResultStats */
/* core.asm:1618-1666. ProcessText preserves de, so d,e stay the text
 * coordinates throughout; b,c are the number coordinates. */
static void PrintDuelResultStats_PrintXCards(uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	WriteTwoDigitNumberInTxSymbolFormat(a, b, c);
	(void)InitTextPrinting_ProcessTextFromID(d, e, CardsText);
}

void PrintDuelResultStats(void)
{
	for (uint8_t turn = 0u; turn < 2u; ++turn) {
		uint8_t d = turn == 0u ? 8u : 1u;
		uint8_t e = d;
		(void)SetNoLineSeparation();
		(void)InitTextPrinting_ProcessTextFromID(d, e, PrizesLeftActivePokemonCardsInDeckText);
		(void)SetOneLineSeparation();
		uint8_t c = e;
		uint8_t b = (uint8_t)(d + 7u);
		d = (uint8_t)(b + 2u);
		PrintDuelResultStats_PrintXCards(CountPrizes(), b, c, d, e);
		e = (uint8_t)(e + 1u);
		c = (uint8_t)(c + 1u);
		DuelistVarResult pokemon = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		d = (uint8_t)(d - 1u);
		(void)InitTextPrinting_ProcessTextFromID(d, e, pokemon.a != 0u ? YesText : NoneText);
		e = (uint8_t)(e + 1u);
		d = (uint8_t)(d + 1u);
		c = (uint8_t)(c + 1u);
		DuelistVarResult cards_var = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
		PrintDuelResultStats_PrintXCards((uint8_t)(DECK_SIZE - gb_read8(cards_var.hl)), b, c, d, e);
		SwapTurn();
	}
}
/* <<< factory PrintDuelResultStats */
/* >>> factory ConvertColorToEnergyCardID */
ConvertColorResult ConvertColorToEnergyCardID(uint8_t a)
{
	static const CardId card_id[] = {
		FIRE_ENERGY,
		GRASS_ENERGY,
		LIGHTNING_ENERGY,
		WATER_ENERGY,
		FIGHTING_ENERGY,
		PSYCHIC_ENERGY,
		DOUBLE_COLORLESS_ENERGY,
	};
	CardId result = card_id[a];
	return (ConvertColorResult){a, (uint8_t)(result >> 8), (uint8_t)result};
}
/* <<< factory ConvertColorToEnergyCardID */
/* --- factory WriteOneByteNumberInTxSymbol_PadSpace */
/* >>> factory PrintReturnCardsToDeckDrawAgain */
PrintReturnCardsToDeckDrawAgainResult PrintReturnCardsToDeckDrawAgain(void)
{
	WaitResult wait = DrawWideTextBox_WaitForInput(ReturnCardsToDeckAndDrawAgainText);
	return (PrintReturnCardsToDeckDrawAgainResult){
		wait.a, wait.b, wait.c, wait.f, wait.hl, (uint16_t)((uint16_t)wait.d << 8 | wait.e)};
}
/* <<< factory PrintReturnCardsToDeckDrawAgain */
/* >>> factory PracticeDuelVerify_Turn3 */
PracticeDuelVerifyTurn3Result PracticeDuelVerify_Turn3(void)
{
	CardId card = card_id_read_at(wTempCardID_ccc2_ADDR);
	uint8_t a = (uint8_t)(card >> 8);
	if ((uint8_t)(card >> 8) == (uint8_t)(SEAKING >> 8))
		a = (uint8_t)card;
	if (card != SEAKING) {
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

	CardId same_pokemon_card_id = GetCardIDFromDeckIndex(wSamePokemonCardID);
	uint16_t same_pokemon_addr = wSamePokemonCardID_ADDR;
	card_id_write(&same_pokemon_addr, same_pokemon_card_id);

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
			CardId card_id = GetCardIDFromDeckIndex(deck_index);
			if (card_id != same_pokemon_card_id)
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
/* >>> factory PracticeDuelVerify_Turn5 */
PracticeDuelVerifyTurn5Result PracticeDuelVerify_Turn5(void)
{
	(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
	if (gb_read8((uint16_t)(wAttachedEnergies_ADDR + WATER)) != 2u)
		return (PracticeDuelVerifyTurn5Result){ReturnWrongAction(0u)};
	if (card_id_read_at(wTempCardID_ccc2_ADDR) != STARYU)
		return (PracticeDuelVerifyTurn5Result){ReturnWrongAction(0u)};
	return (PracticeDuelVerifyTurn5Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn5 */
/* >>> factory PracticeDuelVerify_Turn1 */
PracticeDuelVerify_Turn1Result PracticeDuelVerify_Turn1(void)
{
	if (card_id_read_at(wTempCardID_ccc2_ADDR) != GOLDEEN)
		return (PracticeDuelVerify_Turn1Result){ReturnWrongAction(0u)};
	return (PracticeDuelVerify_Turn1Result){0xC0u};
}
/* <<< factory PracticeDuelVerify_Turn1 */
/* >>> factory PracticeDuelVerify_Turn2 */
PracticeDuelVerify_Turn2Result PracticeDuelVerify_Turn2(void)
{
	if (card_id_read_at(wTempCardID_ccc2_ADDR) != SEAKING)
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

	DrawPlayerPortrait(0u, 5u); /* duel/core.asm:1593 lb bc, 0, 5 */

	hl = wDefaultText_ADDR;
	(void)CopyOpponentName(wDefaultText_ADDR);
	TextLength length = GetTextLengthInTiles(hl);
	InitTextPrinting((uint8_t)(length.a + SCREEN_WIDTH), 0);
	ProcessText(&hl);

	DrawOpponentPortrait(wOpponentPortrait, 13u, 1u, EMOTION_NEUTRAL);
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
		return (CheckEnergyNeededForAttackResult){0u, 0x90u, 0u, 0u, 0u, 0u, hl};
	a = wLoadedAttackCategory;
	if (a == POKEMON_POWER)
		return (CheckEnergyNeededForAttackResult){a, 0x90u, 0u, 0u, 0u, 0u, hl};

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
	ConvertColorResult converted = ConvertColorToEnergyCardID(a);
	a = converted.a;
	e = converted.e;
	d = converted.d;
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
	ConvertColorResult converted2 = ConvertColorToEnergyCardID(a);
	a = converted2.a;
	e = converted2.e;
	d = converted2.d;
	return (CheckEnergyNeededForAttackResult){a, final_f, b, c, d, e, hl};
}
/* <<< factory CheckEnergyNeededForAttack */
/* --- factory DrawOpponentSelectionScreen */
/* >>> factory DrawDamageAnimationArrow */
void DrawDamageAnimationArrow(uint8_t f)
{
	gb_write8(wDamageCharIndex_ADDR, 5u);
	uint16_t de = (uint16_t)(wAnimationQueue_ADDR + 6u);
	CreateDamageCharSprite(SPRITE_ANIM_DAMAGE_ARROW, f, de);
}
/* <<< factory DrawDamageAnimationArrow */
/* >>> factory DrawDamageAnimationWeak */
void DrawDamageAnimationWeak(void)
{
	wDamageCharIndex = 3u;
	CreateDamageCharSprite(SPRITE_ANIM_DAMAGE_WEAK, 0u, (uint16_t)(wAnimationQueue_ADDR + 4u));
}
/* <<< factory DrawDamageAnimationWeak */
/* >>> factory DrawDamageAnimationResist */
void DrawDamageAnimationResist(void)
{
	wDamageCharIndex = 4u;
	CreateDamageCharSprite(SPRITE_ANIM_DAMAGE_RESIST, 0u, (uint16_t)(wAnimationQueue_ADDR + 5u));
	wDamageCharAnimDelay = (uint8_t)(wDamageCharAnimDelay + 18u);
}
/* <<< factory DrawDamageAnimationResist */
/* --- factory Func_15886 */
/* --- factory Func_7364 */
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
	uint8_t discarded = AIPickEnergyCardToDiscard(discard_loc).a;
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
	ConvertColorResult converted3 = ConvertColorToEnergyCardID(a);
	e = converted3.e;
	d = converted3.d;
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
	ConvertColorResult converted4 = ConvertColorToEnergyCardID(a);
	e = converted4.e;
	d = converted4.d;
	return (CheckEnergyNeededForAttackAfterDiscardResult){b, c, d, e, final_f};
}
/* <<< factory CheckEnergyNeededForAttackAfterDiscard */
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
		WriteTwoByteNumberInTxSymbolFormat(damage, 15u, (uint8_t)(e + 1u));
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
	uint8_t saved_c = c;
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
	/* core.asm:4402-4404: `dec d` to zero (Z and N), then `pop bc` restores
	 * the caller's bc. */
	return (PrintAttackOrPkmnPowerInformationResult){last_a, b, saved_c, 0u, running_e, 0xC0u, hl};
}
/* <<< factory PrintAttackOrPkmnPowerInformation */
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
	WriteByteToBGMap0((uint8_t)(color + 1u), 18u, y);
	WriteByteToBGMap0(SYM_Lv, 14u, y);
	WriteTwoDigitNumberInTxSymbolFormat(wLoadedCard1Level, 15u, y);

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
/* >>> factory TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 */
TwoByteNumberToTxSymbolTrimResult TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(uint16_t hl)
{
	static const uint16_t places[] = {10000u, 1000u, 100u, 10u, 1u};
	uint16_t value = hl;
	for (uint8_t i = 0u; i < 5u; i++) {
		uint8_t digit = SYM_0;
		while (value >= places[i]) {
			value = (uint16_t)(value - places[i]);
			digit++;
		}
		gb_write8((uint16_t)(wStringBuffer_ADDR + i), digit);
	}
	gb_write8((uint16_t)(wStringBuffer_ADDR + 5u), 0u);
	uint8_t a;
	uint8_t f;
	uint8_t b = 4u;
	uint16_t out = wStringBuffer_ADDR;
	for (;;) {
		a = gb_read8(out);
		if (a != SYM_0) {
			f = 0x40u;
			break;
		}
		gb_write8(out, SYM_SPACE);
		out++;
		b--;
		if (b == 0u) {
			f = 0xC0u;
			break;
		}
	}
	return (TwoByteNumberToTxSymbolTrimResult){a, f, b, 0xFFu,
		(uint8_t)((wStringBuffer_ADDR + 5u) >> 8), (uint8_t)(wStringBuffer_ADDR + 5u), out};
}
/* <<< factory TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1 */
/* >>> factory WriteTwoByteNumberInTxSymbolFormat */
void WriteTwoByteNumberInTxSymbolFormat(uint8_t a, uint8_t b, uint8_t c)
{
	(void)TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(a);
	uint16_t src = (uint16_t)(wStringBuffer_ADDR + 2u);
	uint16_t dst = BCCoordToBGMap0Address(b, c);
	for (uint8_t i = 0u; i < 3u; i++) {
		gb_write8(dst++, gb_read8(src));
		src = (uint16_t)(src + 1u);
	}
}
/* <<< factory WriteTwoByteNumberInTxSymbolFormat */
/* >>> factory WriteTwoDigitNumberInTxSymbolFormat */
void WriteTwoDigitNumberInTxSymbolFormat(uint8_t a, uint8_t b, uint8_t c)
{
	(void)TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(a);
	uint16_t src = (uint16_t)(wStringBuffer_ADDR + 3u);
	uint16_t dst = BCCoordToBGMap0Address(b, c);
	for (uint8_t i = 0u; i < 2u; i++) {
		gb_write8(dst++, gb_read8(src));
		src = (uint16_t)(src + 1u);
	}
}
/* <<< factory WriteTwoDigitNumberInTxSymbolFormat */
/* >>> factory PrintPokemonCardLength */
void PrintPokemonCardLength(uint16_t hl, uint8_t b, uint8_t c)
{
	uint8_t values[2] = {(uint8_t)(hl >> 8), (uint8_t)hl};
	uint16_t texts[2] = {FeetText, InchesText};
	uint8_t x = b;
	for (uint8_t part = 0u; part < 2u; part++) {
		TwoByteNumberToTxSymbolTrimResult digits =
			TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(values[part]);
		uint8_t count = (uint8_t)(digits.b + 1u);
		wPokemonLengthPrintOffset = count;
		uint16_t src = digits.hl;
		uint16_t dst = BCCoordToBGMap0Address(x, c);
		SafeCopyDataHLtoDE(&src, &dst, count);
		x = (uint8_t)(x + count);
		InitTextPrinting(x, c);
		(void)ProcessTextFromID(texts[part]);
		x = (uint8_t)(x + 1u);
	}
}
/* <<< factory PrintPokemonCardLength */
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
	gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);
}
/* <<< factory OppAction_UsePokemonPower */
/* --- factory Func_616e */
/* --- factory FlushAllPalettesOrSendPal23Packet */
/* >>> factory LoadSelectedCardGfx */
void LoadSelectedCardGfx(void)
{
	DeckEntryResult result = GetCardInDuelTempList(hCurMenuItem, 0u);
	LoadCardDataToBuffer1_FromCardID(result.e);
	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	SetBGP5ToCardPalette();
	FlushAllPalettes();
}
/* <<< factory LoadSelectedCardGfx */
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
		uint8_t high = (uint8_t)(ApplyCardCGBAttributes(0u, 0x0C0Cu).de >> 8);
		return (CardListFunctionResult){high, (uint8_t)(high == 0u ? 0x80u : 0x00u)};
	}
	return (CardListFunctionResult){a, 0xA0u};
}
/* <<< factory CardListFunction */
/* >>> factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult CheckForBenchIDAtHalfHPAndCanUseSecondAttack(uint16_t de, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)f;
	gb_write8(wSamePokemonCardID_ADDR, (uint8_t)de);
	gb_write8((uint16_t)(wSamePokemonCardID_ADDR + 1u), (uint8_t)(de >> 8));
	uint8_t saved_location = hTempPlayAreaLocation_ff9d;
	uint8_t saved_attack = wSelectedAttack;
	d = saved_location;
	e = saved_attack;
	DuelistVarResult arena = GetTurnDuelistVariable(0xBBu);
	b = 0u;
	c = 0u;
	hl = arena.hl;
	CardId same_pokemon = de;
	for (;;) {
		c = (uint8_t)(c + 1u);
		uint8_t deck_index = gb_read8(hl++);
		if (deck_index == 0xFFu)
			break;
		(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		uint8_t current_hp = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + c)).a;
		uint8_t half_max_hp = (uint8_t)((wLoadedCard1HP >> 1) | (wLoadedCard1HP << 7));
		CardId loaded_id = card_id_read_at(wLoadedCard1ID_ADDR);
		if (half_max_hp >= current_hp || loaded_id != same_pokemon)
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
	f = (uint8_t)(b == 0u ? 0x80u : 0x10u);
	return (CheckForBenchIDAtHalfHPAndCanUseSecondAttackResult){b, f, b, c, d, e, hl};
}
/* <<< factory CheckForBenchIDAtHalfHPAndCanUseSecondAttack */
/* --- factory SendCardAttrBlkPacket */
/* --- factory ApplyBGP6OrSGB3ToCardImage */
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
	SetBGP5ToCardPalette();
	FlushAllPalettes();
	uint16_t hl = LARGE_CARD_TILE_DATA;
	uint16_t de = 0u;
	uint8_t a = 0u;
	uint8_t b = 0u;
	uint8_t c = 0u;
	WriteDataBlocksToBGMap0(&hl, &de, &a, &b, &c);
	(void)ApplyCardCGBAttributes(0u, (uint16_t)((6u << 8) | 3u));
}
/* <<< factory DrawLargePictureOfCard */
/* >>> factory DrawCardPageSurroundingBox */
void DrawCardPageSurroundingBox(void)
{
	uint16_t box = 0u;
	DrawRegularTextBox(&box, 0u, 20u, 18u, 0u, 0u);
	FillRectangle(0xA0u, 8u, 6u, (uint16_t)((6u << 8) | 4u), (uint16_t)((6u << 8) | 1u));
	(void)ApplyCardCGBAttributes(0u, (uint16_t)((6u << 8) | 4u));
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

	WriteByteToBGMap0((uint8_t)(color + 1u), 18u, 1u);
	DrawCardPageSet2AndRarityIconsResult result = DrawCardPageSet2AndRarityIcons(18u);
	return (PrintPokemonCardPageGenericInformationResult){result.b, result.hl};
}
/* <<< factory PrintPokemonCardPageGenericInformation */
/* >>> factory DrawDuelHUD */
uint16_t DrawDuelHUD(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
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
	if (arena.a == 0xFFu) return (uint16_t)(((uint16_t)name_d << 8) | name_e);
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena.a);
	CopyCardNameAndLevelResult copied = CopyCardNameAndLevel(32u, icon_b, icon_c, name_d, name_e);
	gb_write8(copied.hl, TX_END);
	uint8_t text_d = name_d;
	if (name_e == 0u) { TextLength length = GetTextLengthInTiles(wDefaultText_ADDR); text_d = (uint8_t)(length.a + SCREEN_WIDTH); }
	InitTextPrinting(text_d, name_e);
	uint16_t text_hl = wDefaultText_ADDR; ProcessText(&text_hl);
	WriteByteToBGMap0((uint8_t)(GetArenaCardColor() + 1u), (uint8_t)(text_d - 1u), name_e);
	uint8_t hud_x = wHUDEnergyAndHPBarsX, hud_y = wHUDEnergyAndHPBarsY;
	PrintPlayAreaCardAttachedEnergies(hud_x, hud_y, PLAY_AREA_ARENA);
	DuelistVarResult arena_again = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena_again.a);
	uint8_t max_hp = wLoadedCard1HP, cur_hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	DrawHPBar(max_hp, cur_hp);
	/* core.asm:2531-2543: the second HP bar row starts one map row below
	 * the first row's start (`push de` / `pop de` around the first copy),
	 * not below where that copy left de. */
	uint16_t row = BCCoordToBGMap0Address(hud_x, (uint8_t)(hud_y + 1u));
	uint16_t dst = row, src = wDefaultText_ADDR;
	SafeCopyDataHLtoDE(&src, &dst, 6u);
	dst = (uint16_t)(row + TILEMAP_WIDTH); src = (uint16_t)(wDefaultText_ADDR + 6u);
	SafeCopyDataHLtoDE(&src, &dst, 6u);
	uint8_t attr_b = (uint8_t)(hud_x + 6u), attr_c = (uint8_t)(hud_y + 1u);
	uint8_t plus = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_ATTACHED_PLUSPOWER).a;
	if (plus != 0u) { WriteByteToBGMap0(SYM_PLUSPOWER, attr_b, attr_c); WriteByteToBGMap0((uint8_t)(plus + SYM_0), (uint8_t)(attr_b + 1u), attr_c); }
	uint8_t defender = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_ATTACHED_DEFENDER).a;
	if (defender != 0u) { attr_c++; WriteByteToBGMap0(SYM_DEFENDER, attr_b, attr_c); WriteByteToBGMap0((uint8_t)(defender + SYM_0), (uint8_t)(attr_b + 1u), attr_c); }
	return dst;
}
/* <<< factory DrawDuelHUD */
/* >>> factory DrawCardListScreenLayout */
DrawCardListScreenLayoutResult DrawCardListScreenLayout(void)
{
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadSymbolsFont();
	TileCopyResult tiles = LoadDuelCardSymbolTiles();
	SetDefaultConsolePalettes();
	uint16_t box_hl = tiles.hl;
	DrawRegularTextBox(&box_hl, 0u, 20u, 13u, 0u, 0u);
	uint16_t image_hl = 0x0601u;
	FillRectangle(0xA0u, 8u, 6u, 0x0C0Cu, image_hl);
	(void)ApplyCardCGBAttributes(0u, 0x0C0Cu);
	PrintSortNumberInCardList_CallFromPointer();
	uint8_t a = gb_read8(wDuelTempList_ADDR);
	if (a == 0xFFu)
		return (DrawCardListScreenLayoutResult){a, 0x90u};
	return (DrawCardListScreenLayoutResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u)};
}
/* <<< factory DrawCardListScreenLayout */
/* --- factory ApplyBGP7OrSGB2ToCardImage */
/* >>> factory DisplayPracticeDuelPlayerHandScreen */
void DisplayPracticeDuelPlayerHandScreen(void)
{
	(void)CreateHandCardList(0u);
	EmptyScreen();
	SetDefaultConsolePalettes();
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
	/* core.asm:2357-2366: the arena images go to v0Tiles1 + $50 tiles and
	 * v0Tiles1 + $20 tiles -- $8D00 and $8A00, the tiles FillRectangle's
	 * $D0 and $A0 index -- not into v0Tiles0. */
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	LoadPlayAreaCardGfx(result.a, (uint16_t)(V0_TILES1 + 0x500u));
	SetBGP5ToCardPalette();
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		FillRectangle(0xD0u, 8u, 6u, 0x0005u, 0x0601u);
		(void)ApplyCardCGBAttributes(0u, 0x0005u);
	}
	SwapTurn();
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	LoadPlayAreaCardGfx(result.a, (uint16_t)(V0_TILES1 + 0x200u));
	SetBGP2ToCardPalette();
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		FillRectangle(0xA0u, 8u, 6u, 0x0C01u, 0x0601u);
		(void)ApplyCardCGBAttributes(0u, 0x0C01u);
		SwapTurn();
	}
	FlushAllPalettes();
	/* core.asm:2394 passes `DuelEAndHPTileData` ($01:5188); the callee walks
	 * hl until a block's first byte has bit 7 set. */
	uint16_t tile_data = DUEL_E_AND_HP_TILE_DATA;
	uint16_t bg_map = 0u;
	uint8_t a = 0u, b = 0u, c = 0u;
	WriteDataBlocksToBGMap0(&tile_data, &bg_map, &a, &b, &c);
	DrawDuelHorizontalSeparator();
	DrawDuelHUDs();
	(void)DrawWideTextBox();
	EnableLCD();
	if (restore_turn != 0u)
		gb_write8(hWhoseTurn_ADDR, saved_turn);
}
/* <<< factory DrawDuelMainScene */
/* >>> factory DisplayNoBasicPokemonInHandScreen */
void DisplayNoBasicPokemonInHandScreen(void)
{
	EmptyScreen();
	SetDefaultConsolePalettes();
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
/* >>> factory DisplayEnergyDiscardScreen */
void DisplayEnergyDiscardScreen(uint8_t a)
{
	wEnergyDiscardPlayAreaLocation = a;
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelFaceDownCardTiles();
	SetDefaultConsolePalettes();
	a = wEnergyDiscardPlayAreaLocation;
	wCurPlayAreaSlot = a;
	wCurPlayAreaY = 0u;
	(void)PrintPlayAreaCardInformation();
	wEnergyDiscardMenuNumerator = 0u;
	wEnergyDiscardMenuDenominator = 1u;
	DisplayEnergyDiscardMenu();
}
/* <<< factory DisplayEnergyDiscardScreen */
/* --- factory SetOBP1OrSGB3ToCardPalette */
/* >>> factory OpenAttackPage */
void OpenAttackPage(void)
{
	wCardPageNumber = CARDPAGE_POKEMON_OVERVIEW;
	wCurPlayAreaSlot = 0u;
	EmptyScreen();
	FinishQueuedAnimations();
	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	SetBGP5ToCardPalette();
	FlushAllPalettes();

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
		WriteTwoDigitNumberInTxSymbolFormat(numerator, b, c);
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
/* >>> factory PracticeDuel_RepeatInstructions */
uint8_t PracticeDuel_RepeatInstructions(void)
{
	PrintPracticeDuelDrMasonInstructions(FollowMyGuidancePracticeDuelText);
	BankswitchSRAM(sCurrentDuel_BANK);
	LoadSavedDuelData(sCurrentDuel_ADDR);
	BankswitchSRAM(0u);
	/* `xor a` for the SRAM0 bank leaves Z set and the trailing `scf` does not
	 * clear it, so the caller sees Z|C, not carry alone. */
	return 0x90u;
}
/* <<< factory PracticeDuel_RepeatInstructions */
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
	(void)LoadDuelCardSymbolTiles();
	SetDefaultConsolePalettes();
	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	SetBGP5ToCardPalette();
	FlushAllPalettes();
	b = 0u;
	gb_write8(wCardPageNumber_ADDR, 0u);
	{
		CardPageNavigationResult page = DisplayFirstOrNextCardPage(b);

		if ((page.f & 0x10u) != 0u)
			return;
		EnableLCD();
	}
	OpenCardPage_input_loop(b);
}
/* <<< factory OpenCardPage */
/* >>> factory OppAction_PlayTrainerCard */
void OppAction_PlayTrainerCard(void)
{
	(void)LoadNonPokemonCardEffectCommands();
	(void)DisplayUsedTrainerCardDetailScreen();
	PrintUsedTrainerCardDescription();
	gb_write8(wSkipDuelistIsThinkingDelay_ADDR, 1u);
}
/* <<< factory OppAction_PlayTrainerCard */
/* >>> factory DisplayPlayAreaScreenToUsePkmnPower */
/* core.asm:5618-5675. Carry (f bit 4) is the B press that leaves without a
 * power; a chosen power returns with it clear and hTemp_ffa0 holding the
 * card's deck index. */
DisplayPlayAreaScreenToUsePkmnPowerResult DisplayPlayAreaScreenToUsePkmnPower(void)
{
	gb_write8(wSelectedDuelSubMenuItem_ADDR, 0u);
draw_screen:
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelCheckPokemonScreenTiles();
	SetDefaultConsolePalettes();
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
	/* core.asm:5623-5627: the play area menu, arena card included, cursor on
	 * the last selection; as many items as cards. */
	{
		uint16_t params = PLAY_AREA_PARAMS_INCLUDED;
		InitializeMenuParameters(gb_read8(wSelectedDuelSubMenuItem_ADDR), &params);
	}
	gb_write8(wNumMenuItems_ADDR, gb_read8(wNumPlayAreaItems_ADDR));
	for (;;) {
		DoFrame();
		HandleMenuInputResult input = HandleMenuInput();
		gb_write8(hTempPlayAreaLocation_ff9d_ADDR, input.a);
		gb_write8(wHUDEnergyAndHPBarsX_ADDR, input.a);
		if ((input.f & 0x10u) == 0u)
			continue;
		if (input.a == MENU_CANCEL)
			return (DisplayPlayAreaScreenToUsePkmnPowerResult){0x10u, 0u, 0u};
		gb_write8(wSelectedDuelSubMenuItem_ADDR, input.a);
		if ((hKeysPressed & PAD_START) != 0u) {
			uint8_t item = (uint8_t)(hCurMenuItem + DUELVARS_ARENA_CARD);
			DuelistVarResult arena = GetTurnDuelistVariable(item);
			uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
			LoadCardDataToBuffer1_FromCardID(card_id);
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
		return (DisplayPlayAreaScreenToUsePkmnPowerResult){0x00u, answer.d, answer.e};
	}
}
/* <<< factory DisplayPlayAreaScreenToUsePkmnPower */
/* >>> factory DisplayCardPage_PokemonOverview */
/* core.asm:4280 `.attacks`: the tail of the overview page from the first
 * the same block into the SRAM gfx buffer at row 66. */
uint8_t DisplayCardPage_PokemonOverview_Attacks(uint8_t c)
{
	uint8_t page_type = gb_read8(wCardPageType_ADDR);
	uint8_t b, e, retreat;
	(void)PrintAttackOrPkmnPowerInformation(5u, c, 0u, c, wLoadedCard1Atk1Name_ADDR);
	c = (uint8_t)(c + 2u);
	(void)PrintAttackOrPkmnPowerInformation(5u, c, 0u, c, wLoadedCard1Atk2Name_ADDR);
	c = (uint8_t)(c + 2u);
	retreat = gb_read8(wLoadedCard1RetreatCost_ADDR);
	e = (uint8_t)(retreat + 1u);
	b = 8u;
	while (e != 0u) {
		e = (uint8_t)(e - 1u);
		if (e == 0u)
			break;
		WriteByteToBGMap0(SYM_COLORLESS, b, c);
		b = (uint8_t)(b + 1u);
	}
	c = (uint8_t)(c + 1u);
	if (page_type != CARDPAGETYPE_NOT_PLAY_AREA && gb_read8(wCurPlayAreaSlot_ADDR) == 0u) {
		retreat = GetArenaCardWeakness();
		e = GetArenaCardResistance();
	} else {
		retreat = gb_read8(wLoadedCard1Weakness_ADDR);
		e = gb_read8(wLoadedCard1Resistance_ADDR);
	}
	PrintCardPageWeaknessesOrResistances(retreat, 8u, c);
	PrintCardPageWeaknessesOrResistances(e, 8u, (uint8_t)(c + 1u));
	return b;
}

uint8_t DisplayCardPage_PokemonOverview(void)
{
	uint8_t page_type = gb_read8(wCardPageType_ADDR);
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
		/* b here is WriteDataBlocksToBGMap0's leftover; the overview's own exit
		 * b is the retreat count set below, so the icons' input does not matter. */
		(void)DrawCardPageSet2AndRarityIcons(0u);
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
		WriteTwoDigitNumberInTxSymbolFormat(gb_read8(wLoadedCard1Level_ADDR), 12u, 2u);
		WriteTwoByteNumberInTxSymbolFormat(gb_read8(wLoadedCard1HP_ADDR), 16u, 2u);
	}
	WriteTwoByteNumberInTxSymbolFormat(gb_read8(wLoadedCard1PokedexNumber_ADDR), 16u, 16u);
	return DisplayCardPage_PokemonOverview_Attacks(10u);
}
/* <<< factory DisplayCardPage_PokemonOverview */
/* >>> factory DisplayEnergyOrTrainerCardPage */
PrintAttackOrCardDescriptionResult DisplayEnergyOrTrainerCardPage(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t saved_hl = hl;
	(void)LoadCardTypeHeaderTiles(a);
	uint16_t box_hl = 0u;
	DrawRegularTextBox(&box_hl, 0u, 20u, 18u, 0u, 0u);
	ProcessTextHeaderResult text = InitTextPrinting_ProcessTextFromPointerToID(4u, 3u, wLoadedCard1Name_ADDR);
	a = text.a; d = text.d; e = text.e; f = text.f; hl = text.hl;
	FillRectangle(0xA0u, 8u, 6u, 0x0604u, 0x0601u);
	(void)ApplyCardCGBAttributes(0u, 0x0604u);
	FillRectangle(0xE0u, 8u, 2u, 0x0601u, 0x0108u);
	/* duel/core.asm:4697-4700: `lb bc, 8, 2` for the fill, then the icons. */
	DrawCardPageSet2AndRarityIconsResult icons = DrawCardPageSet2AndRarityIcons(8u);
	hl = icons.hl;
	d = 18u; e = 9u;
	return PrintAttackOrNonPokemonCardDescription(icons.b, saved_hl, d, e);
}
/* <<< factory DisplayEnergyOrTrainerCardPage */
/* --- factory Func_5a81 */
/* >>> factory _TossCoin */
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
	wCoinTossNumHeads = 0u;

	do {
		uint8_t anim;
		uint8_t result;
		uint8_t tile;

		/* skip the tally if it's only one coin toss */
		if (wCoinTossTotalNum >= 2u) {
			/* write "#coin/#total coins" */
			WriteTwoDigitNumberInTxSymbolFormat((uint8_t)(wCoinTossNumTossed + 1u), 15u, 11u);
			WriteByteToBGMap0(SYM_SLASH_7847, 17u, 11u);
			WriteTwoDigitNumberInTxSymbolFormat(wCoinTossTotalNum, 18u, 11u);
		}

		ResetAnimationQueue();
		(void)PlayDuelAnimation(DUEL_ANIM_COIN_SPIN_7847);

		if (wCoinTossDuelistType == DUELIST_TYPE_PLAYER_7847) {
			/* wait for input, and send a byte once the player is ready */
			(void)WaitForWideTextBoxInput();
			/* its EraseCursor tail exits WriteByteToBGMap0 with a = 0,
			 * which is the byte the ROM forwards here */
			TossCoin_SendByte(0u);
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
#ifdef POKETCG_DEBUG_MENU
		if (debug_cheats_coin_mode() == DEBUG_COIN_HEADS) {
			anim = DUEL_ANIM_COIN_TOSS_GOING_HEADS_7847;
			result = HEADS_7847;
		} else if (debug_cheats_coin_mode() == DEBUG_COIN_TAILS) {
			anim = DUEL_ANIM_COIN_TOSS_GOING_TAILS_7847;
			result = TAILS_7847;
		}
#endif

		/* play the tossing animation and wait for it to finish */
		(void)PlayDuelAnimation(anim);
		if (wCoinTossDuelistType == DUELIST_TYPE_PLAYER_7847) {
			do {
				DoFrame();
			} while (CheckAnyAnimationPlaying().f & FLAG_C_7847);
			TossCoin_SendByte(result);
		} else {
			result = TossCoin_GetOpponentCoinResult(result);
#ifdef POKETCG_DEBUG_MENU
			if (debug_cheats_coin_mode() == DEBUG_COIN_HEADS)
				result = HEADS_7847;
			else if (debug_cheats_coin_mode() == DEBUG_COIN_TAILS)
				result = TAILS_7847;
#endif
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
			TossCoin_WaitForOpponent(sent);
			/* "tossing until tails" (wCoinTossTotalNum == 0) with no heads
			 * yet also waits for input */
			if ((uint8_t)(wCoinTossTotalNum | wCoinTossNumHeads) == 0u)
				(void)WaitForWideTextBoxInput();
		} else {
			(void)WaitForWideTextBoxInput();
			TossCoin_SendByte(0u);
		}

		FinishQueuedAnimations();
	} while (wCoinTossNumTossed < wCoinTossTotalNum);

	FinishQueuedAnimations();
	ResetAnimationQueue();

	/* return carry if at least 1 heads */
	heads = wCoinTossNumHeads;
	return (TossCoinResult){heads, heads ? FLAG_C_7847 : FLAG_Z_7847};
}
/* <<< factory _TossCoin */
/* >>> factory OppAction_BeginUseAttack */
OppActionBeginUseAttackResult OppAction_BeginUseAttack(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	d = hTempCardIndex_ff9f;
	e = hTemp_ffa0;
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
			f = (uint8_t)(0x40u | ((a & 0x0Fu) < (CONFUSED & 0x0Fu) ? 0x20u : 0u)
				| (a < CONFUSED ? 0x10u : 0u));
			return (OppActionBeginUseAttackResult){a, f, b, c, d, e, hl};
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
OppAction_TossCoinATimesResult OppAction_TossCoinATimes(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	TossCoinATimesResult toss = TossCoinATimes(a, f, b, c, d, e, hl);
	wSkipDuelistIsThinkingDelay = 1u;
	return (OppAction_TossCoinATimesResult){toss.a, toss.f, 0x12u, 0u, 0x12u, 0x11u, toss.hl};
}
/* <<< factory OppAction_TossCoinATimes */
/* >>> factory DisplayOpponentUsedAttackScreen */
void DisplayOpponentUsedAttackScreen(void)
{
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelFaceDownCardTiles();
	CardId cardid = card_id_read_at(wTempCardID_ccc2_ADDR);
	LoadCardDataToBuffer1_FromCardID(cardid);
	wCardPageNumber = CARDPAGE_POKEMON_OVERVIEW;
	uint16_t hl = wLoadedCard1Atk1Name_ADDR;
	if (wSelectedAttack != 0u) {
		hl = wLoadedCard1Atk2Name_ADDR;
	}
	(void)PrintAttackOrPkmnPowerInformation(0u, 0u, 0u, 1u, hl);
	(void)PrintAttackOrCardDescription(0u, wLoadedAttackDescription_ADDR, 1u, 4u);
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
			(void)ApplyCardCGBAttributes(0u, 0x0C0Cu);
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

				/* HandleMenuInput reaches CardListFunction through
				 * CardListMenuFunction's wListFunctionPointer dispatch
				 * (home/menus.c), so its carry, cursor draw and SFX are
				 * the epilogue of this one call, as on the ROM. */
				HandleCardListInputResult input = HandleCardListInput();

				if ((input.f & FLAG_C) == 0u)
					continue;

				uint8_t list_scroll = input.d;
				uint8_t list_item = input.e;

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
/* --- factory Func_5542 */
/* --- factory CanArenaCardUseNonResidualAttack */
/* === factory OpenNonTurnHolderDiscardPileScreen */
/* >>> factory CheckIfActivePokemonCanUseAnyNonResidualAttack */
CheckIfActivePokemonCanUseAnyNonResidualAttackResult CheckIfActivePokemonCanUseAnyNonResidualAttack(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	CheckIfSelectedAttackIsUnusableResult first = CheckIfSelectedAttackIsUnusable(
		FIRST_ATTACK_OR_PKMN_POWER, 0x80u, b, c, d, e, hl);
	a = first.a;
	f = first.f;
	b = first.b;
	c = first.c;
	d = first.d;
	e = first.e;
	hl = first.hl;
	if ((f & FLAG_C) == 0u) {
		a = (uint8_t)(wLoadedAttackCategory & RESIDUAL);
		if (a == 0u)
			return (CheckIfActivePokemonCanUseAnyNonResidualAttackResult){0u, FLAG_C, b, c, d, e, hl};
	}

	wSelectedAttack = SECOND_ATTACK;
	CheckIfSelectedAttackIsUnusableResult second = CheckIfSelectedAttackIsUnusable(
		SECOND_ATTACK, f, b, c, d, e, hl);
	a = second.a;
	f = second.f;
	b = second.b;
	c = second.c;
	d = second.d;
	e = second.e;
	hl = second.hl;
	if ((f & FLAG_C) == 0u) {
		a = (uint8_t)(wLoadedAttackCategory & RESIDUAL);
		if (a == 0u)
			return (CheckIfActivePokemonCanUseAnyNonResidualAttackResult){0u, FLAG_C, b, c, d, e, hl};
	}
	if ((f & FLAG_C) != 0u)
		a = 0u;
	return (CheckIfActivePokemonCanUseAnyNonResidualAttackResult){
		a, (a == 0u) ? FLAG_Z : 0u, b, c, d, e, hl};
}
/* <<< factory CheckIfActivePokemonCanUseAnyNonResidualAttack */
/* >>> factory PrintDeckAndHandIconsAndNumberOfCards */
/* core.asm:1490-1504. The x, y, bytes[], 0 blocks live in this bank
 * ($01:4A35, $01:4A6E) and are passed by address, never copied into WRAM. */
#define DECK_AND_HAND_ICONS_TILE_DATA DeckAndHandIconsTileData_ADDR
void PrintDeckAndHandIconsAndNumberOfCards(void)
{
	uint16_t data = DECK_AND_HAND_ICONS_TILE_DATA;
	uint16_t bg_map = 0u;
	uint8_t a = 0u, b = 0u, c = 0u;

	(void)LoadDuelDrawCardsScreenTiles();
	WriteDataBlocksToBGMap0(&data, &bg_map, &a, &b, &c);
	PrintPlayerNumberOfHandAndDeckCards();
	PrintOpponentNumberOfHandAndDeckCards();
}
/* <<< factory PrintDeckAndHandIconsAndNumberOfCards */
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
		SetDefaultConsolePalettes();
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
/* >>> factory OppAction_ExecuteTrainerCardEffectCommands */
void OppAction_ExecuteTrainerCardEffectCommands(uint8_t b, uint8_t d, uint8_t e)
{
	TryExecuteEffectCommandFunctionResult first =
		TryExecuteEffectCommandFunction(OPP_EFFECTCMDTYPE_DISCARD_ENERGY, b, d, e);
	TryExecuteEffectCommandFunctionResult second =
		TryExecuteEffectCommandFunction(OPP_EFFECTCMDTYPE_BEFORE_DAMAGE,
			first.b, first.d, first.e);
	DrawDuelMainScene();
	uint8_t card_index = hTempCardIndex_ff9f;
	MoveCardResult moved = MoveHandCardToDiscardPile(card_index);
	DrawDuelMainScene();
}
/* <<< factory OppAction_ExecuteTrainerCardEffectCommands */
/* >>> factory OppAction_UseMetronomeAttack */
void OppAction_UseMetronomeAttack(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
	DrawDuelMainScene();
	DuelistVarResult status = GetTurnDuelistVariable(OPP_METRONOME_ARENA_STATUS);
	if ((status.a & OPP_METRONOME_CNF_SLP_PRZ) != OPP_METRONOME_CONFUSED) {
		PrintPokemonsAttackTextResult text = PrintPokemonsAttackText();
		b = text.b;
		d = text.d;
		e = text.e;
	}
	SwapTurn();
	AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(d, e);
	SwapTurn();
	wPlayerAttackingCardIndex = hTempCardIndex_ff9f;
	wPlayerAttackingAttackIndex = wSelectedAttack;
	uint16_t player_attacking_card_id = wPlayerAttackingCardID_ADDR;
	card_id_write(&player_attacking_card_id, card_id_read_at(wTempCardID_ccc2_ADDR));
	(void)UpdateArenaCardIDsAndClearTwoTurnDuelVars(copy.a, copy.f, b, copy.c,
		(uint8_t)(copy.de >> 8), (uint8_t)copy.de, copy.hl);
	wMetronomeEnergyCost = c;
	if ((status.a & OPP_METRONOME_CNF_SLP_PRZ) != OPP_METRONOME_CONFUSED)
		(void)WaitForWideTextBoxInput();
}
/* <<< factory OppAction_UseMetronomeAttack */
/* >>> factory AITryUseAttack */
/* ai/core.asm:133-166. Only b survives entry to the first dispatch: a/d/e are
 * reloaded from wSelectedAttack and the arena card, c comes from
 * CopyAttackDataAndDamage_FromDeckIndex, and hl/f are callee-clobbered.
 * The tail past the `ret c` at asm:144 threads AIMakeDecision's echoed b/c/d/e,
 * which is all its registered contract (compare "f") carries; the $09/$0A
 * dispatches it reaches are the unported OppActionTable traps. */
#define OPPACTION_BEGIN_ATTACK_C 0x07u
#define OPPACTION_USE_ATTACK_C 0x08u
#define OPPACTION_ATTACK_ANIM_AND_DAMAGE_C 0x09u
AITryUseAttackResult AITryUseAttack(uint8_t b)
{
	uint8_t e = wSelectedAttack;
	hTemp_ffa0 = e;
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	hTempCardIndex_ff9f = arena.a;
	AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(arena.a, e);
	AIMakeDecisionResult begin = AIMakeDecision(OPPACTION_BEGIN_ATTACK_C, b,
		copy.c, (uint8_t)(copy.de >> 8), (uint8_t)copy.de);
	if ((begin.f & FLAG_C) != 0u)
		return (AITryUseAttackResult){begin.a, begin.f};

	AISelectSpecialAttackParametersResult special = AISelectSpecialAttackParameters();
	if ((special.f & FLAG_C) == 0u)
		(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI_SELECTION,
			begin.b, begin.d, begin.e);

	e = wSelectedAttack;
	DuelistVarResult arena2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	AttackCopyResult copy2 = CopyAttackDataAndDamage_FromDeckIndex(arena2.a, e);
	AIMakeDecisionResult use = AIMakeDecision(OPPACTION_USE_ATTACK_C, begin.b,
		copy2.c, (uint8_t)(copy2.de >> 8), (uint8_t)copy2.de);
	if ((use.f & FLAG_C) != 0u)
		return (AITryUseAttackResult){use.a, use.f};

	(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AI_SWITCH_DEFENDING_PKMN,
		use.b, use.d, use.e);
	AIMakeDecisionResult anim = AIMakeDecision(OPPACTION_ATTACK_ANIM_AND_DAMAGE_C,
		use.b, use.c, use.d, use.e);
	return (AITryUseAttackResult){anim.a, anim.f};
}
/* <<< factory AITryUseAttack */
/* >>> factory PrintPokemonCardWeight */
PrintPokemonCardWeightResult PrintPokemonCardWeight(uint8_t b, uint8_t c, uint16_t hl)
{
	uint8_t entry_b = b;
	uint8_t entry_c = c;
	uint16_t quotient = (uint16_t)(hl / 10u);
	uint8_t remainder = (uint8_t)(hl % 10u);
	uint16_t cursor;
	uint16_t destination;
	uint8_t out_c;
	uint16_t source;
	uint16_t scan;
	uint8_t length;
	uint8_t sum;
	uint8_t f;

	(void)TwoByteNumberToTxSymbol_TrimLeadingZeros_Bank1(quotient);
	cursor = (uint16_t)(wStringBuffer_ADDR + 5u);
	if (remainder != 0u) {
		gb_write8(cursor, SYM_DOT);
		gb_write8((uint16_t)(cursor + 1u), (uint8_t)(remainder + SYM_0));
		cursor = (uint16_t)(cursor + 2u);
	}
	gb_write8(cursor, 0u);

	/* `ld c, b` inside BCCoordToBGMap0Address leaves the x coordinate in c,
	 * and nothing after it reloads c, so that is the c this routine returns. */
	destination = BCCoordToBGMap0Address(entry_b, entry_c);
	out_c = entry_b;

	source = wStringBuffer_ADDR;
	while (gb_read8(source) == 0u)
		source++;

	length = 0u;
	scan = source;
	while (gb_read8(scan) != 0u) {
		scan++;
		length++;
	}

	/* SafeCopyDataHLtoDE advances hl past the bytes it copied; the ROM returns
	 * that advanced pointer. */
	SafeCopyDataHLtoDE(&source, &destination, length);

	/* `ld a, b` / `add d`: string length plus the x coordinate, with the flags
	 * of that add. */
	sum = (uint8_t)(length + entry_b);
	f = (uint8_t)((sum == 0u ? 0x80u : 0u)
		| (((length & 0x0Fu) + (entry_b & 0x0Fu)) > 0x0Fu ? 0x20u : 0u)
		| (((uint16_t)length + (uint16_t)entry_b) > 0xFFu ? 0x10u : 0u));

	return (PrintPokemonCardWeightResult){sum, f, length, out_c, sum, entry_c, source};
}
/* <<< factory PrintPokemonCardWeight */
/* >>> factory DisplayCardPage_PokemonDescription */
/* core.asm:4554. Renders the Pokemon description card page: generic header,
 * LENGTH/WEIGHT labels, Lv/HP tiles, card symbol, level and HP numbers, the
 * category line, the length and weight values and finally the description
 * printed without line separation. The tail is `call SetOneLineSeparation /
 * ret`, and that routine is `xor a / ld [wLineSeparation], a / ret`, so the
 * exit registers are exactly the ones it produces. */
DisplayCardPage_PokemonDescriptionResult DisplayCardPage_PokemonDescription(void)
{
	uint16_t block_hl;
	uint16_t block_de;
	uint8_t block_a;
	uint8_t block_b;
	uint8_t block_c;
	uint16_t card_length;
	uint16_t card_weight;
	uint16_t description;
	uint8_t lines;
	uint8_t row;
	uint8_t separation;

	(void)PrintPokemonCardPageGenericInformation();
	(void)LoadDuelCardSymbolTiles2();
	(void)PlaceTextItems(CARD_PAGE_LENGTH_WEIGHT_TEXT_DATA);

	block_hl = CARD_PAGE_LV_HP_TEXT_TILE_DATA;
	block_de = 0u;
	block_a = 0u;
	block_b = 0u;
	block_c = 0u;
	WriteDataBlocksToBGMap0(&block_hl, &block_de, &block_a, &block_b, &block_c);

	DrawCardSymbol(3u, 2u);
	WriteTwoDigitNumberInTxSymbolFormat(gb_read8(wLoadedCard1Level_ADDR), 12u, 2u);
	WriteTwoByteNumberInTxSymbolFormat(gb_read8(wLoadedCard1HP_ADDR), 16u, 2u);

	{
		ProcessTextHeaderResult category =
			InitTextPrinting_ProcessTextFromPointerToID(1u, 10u, wLoadedCard1Category_ADDR);
		/* `ld a, TX_KATAKANA / call ProcessSpecialTextCharacter`: hl is still the
		 * cursor the category print left behind. */
		(void)ProcessSpecialTextCharacter(TX_KATAKANA, category.hl);
	}
	(void)ProcessTextFromID(PokemonText);

	/* `ld a, [hli] / ld l, [hl] / ld h, a`: the length word is stored feet
	 * first, so the low address byte becomes h and the high one l. */
	card_length = (uint16_t)(((uint16_t)gb_read8(wLoadedCard1Length_ADDR) << 8)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard1Length_ADDR + 1u)));
	PrintPokemonCardLength(card_length, 5u, 11u);

	/* `ld a, [hli] / ld h, [hl] / ld l, a`: the weight is a plain little-endian
	 * word, unlike the length above. */
	card_weight = (uint16_t)((uint16_t)gb_read8(wLoadedCard1Weight_ADDR)
		| ((uint16_t)gb_read8((uint16_t)(wLoadedCard1Weight_ADDR + 1u)) << 8));
	{
		/* PrintPokemonCardWeight leaves d = x coordinate just past the string it
		 * printed and e = the row, and that pair is what positions "lbs.". */
		PrintPokemonCardWeightResult weight_out = PrintPokemonCardWeight(5u, 12u, card_weight);
		(void)InitTextPrinting_ProcessTextFromID(weight_out.d, weight_out.e, LbsText);
	}

	(void)SetNoLineSeparation();
	description = (uint16_t)((uint16_t)gb_read8(wLoadedCard1Description_ADDR)
		| ((uint16_t)gb_read8((uint16_t)(wLoadedCard1Description_ADDR + 1u)) << 8));
	lines = CountLinesOfTextFromID(description);
	/* `lb de, 1, 13 / cp 4 / jr nc`: carry is set only when the line count is
	 * below four, and that is the branch that moves the text one row down. */
	row = 13u;
	if (lines < 4u)
		row = (uint8_t)(row + 1u);
	InitTextPrintingInTextbox(CARD_PAGE_DESCRIPTION_LINE_LENGTH, 1u, row);
	(void)ProcessTextFromPointerToID(wLoadedCard1Description_ADDR);

	separation = SetOneLineSeparation();
	/* duel/core.asm:4586 `lb bc, 5, 12` for the weight; every later call
	 * pushes and pops bc. */
	return (DisplayCardPage_PokemonDescriptionResult){separation, (uint8_t)(separation == 0u ? FLAG_Z : 0u), 5u};
}
/* <<< factory DisplayCardPage_PokemonDescription */
/* --- factory RequestToPrintCards_SelectStartCard */
/* >>> factory HandleSleepCheck */
/* core.asm:7027. hl points at a duelist's DUELVARS_ARENA_CARD_STATUS byte and
 * is only read/masked here, so it stays a plain address parameter. The early
 * `ret nz` exits with the `cp ASLEEP` flags; the full path exits with
 * WaitForWideTextBoxInput's, which is why only the flag byte is returned. */
HandleSleepCheckResult HandleSleepCheck(uint16_t hl)
{
	uint8_t sleep_status = (uint8_t)(gb_read8(hl) & CNF_SLP_PRZ);
	if (sleep_status != ASLEEP) {
		uint8_t f = (uint8_t)(0x40u
			| (((sleep_status & 0x0Fu) < (ASLEEP & 0x0Fu)) ? 0x20u : 0u)
			| ((sleep_status < ASLEEP) ? FLAG_C : 0u));
		return (HandleSleepCheckResult){f};
	}

	CardId non_turn_card_id = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	LoadCardDataToBuffer1_FromCardID(non_turn_card_id);
	/* `ld a, 18` is the pad width; bc and de are dead on entry to the callee. */
	CopyCardNameAndLevelResult name = CopyCardNameAndLevel(18u, 0u, 0u, 0u, 0u);
	gb_write8(name.hl, TX_END);
	wTxRam2 = 0u;
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), 0u);

	TossCoinRoutineResult toss = TossCoin(PokemonsSleepCheckText,
					     (uint16_t)(wTxRam2_ADDR + 1u));
	uint8_t anim = DUEL_ANIM_SLEEP_7027;
	uint16_t text = IsStillAsleepText;
	if (toss.f & FLAG_C) {
		/* heads: keep only the poison bits, clearing the sleep status */
		gb_write8(hl, (uint8_t)(gb_read8(hl) & DOUBLE_POISONED));
		anim = DUEL_ANIM_HEAL_7027;
		text = IsCuredOfSleepText;
	}

	RedrawTurnDuelistsMainSceneOrDuelHUD();
	PrintCardNameFromCardIDInTextBox(text);
	PlayBetweenTurnsAnimation(anim);
	return (HandleSleepCheckResult){WaitForWideTextBoxInput().f};
}
/* <<< factory HandleSleepCheck */
/* >>> factory ChooseInitialArenaAndBenchPokemon */
ChooseInitialArenaAndBenchPokemonResult ChooseInitialArenaAndBenchPokemon(void)
{
	DuelistVarResult duelist = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	uint8_t duelist_type = duelist.a;
	if (duelist_type != DUELIST_TYPE_PLAYER) {
		(void)AIDoAction_StartDuel();
		gb_write8(duelist.hl, duelist_type);
		return (ChooseInitialArenaAndBenchPokemonResult){
			(duelist_type == 0u) ? FLAG_Z : 0u};
	}
	EmptyScreen();
	DrawDuelBoxMessage(BOXMSG_ARENA_POKEMON);
	(void)DrawWideTextBox_WaitForInput(ChooseBasicPkmnToPlaceInArenaText);
	(void)DoPracticeDuelAction(PRACTICEDUEL_DRAW_SEVEN_CARDS);
	for (;;) {
		DisplayPlaceInitialPokemonCardsScreenResult choice =
			DisplayPlaceInitialPokemonCardsScreen(0u, PleaseChooseAnActivePokemonText);
		if (choice.f & FLAG_C)
			continue;
		uint8_t card_index = hTempCardIndex_ff98;
		(void)LoadCardDataToBuffer1_FromDeckIndex(card_index);
		uint8_t practice_flags = DoPracticeDuelAction(PRACTICEDUEL_PLAY_GOLDEEN);
		if (practice_flags & FLAG_C)
			continue;
		card_index = hTempCardIndex_ff98;
		(void)PutHandPokemonCardInPlayArea(card_index, practice_flags);
		card_index = hTempCardIndex_ff98;
		(void)DisplayCardDetailScreen(card_index, PlacedInTheArenaText);
		break;
	}
	EmptyScreen();
	DrawDuelBoxMessage(BOXMSG_BENCH_POKEMON);
	(void)PrintScrollableText_NoTextBoxLabel(ChooseUpTo5BasicPkmnToPlaceOnBenchText);
	(void)DoPracticeDuelAction(PRACTICEDUEL_PUT_STARYU_IN_BENCH);
bench_loop:
	for (;;) {
		DisplayPlaceInitialPokemonCardsScreenResult choice =
			DisplayPlaceInitialPokemonCardsScreen(TRUE, ChooseYourBenchPokemonText);
		if (choice.f & FLAG_C)
			break;
		DuelistVarResult count =
			GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (count.a >= MAX_PLAY_AREA_POKEMON) {
			(void)DrawWideTextBox_WaitForInput(NoSpaceOnTheBenchText);
			continue;
		}
		uint8_t card_index = hTempCardIndex_ff98;
		(void)PutHandPokemonCardInPlayArea(card_index, FLAG_C);
		card_index = hTempCardIndex_ff98;
		(void)DisplayCardDetailScreen(card_index, PlacedOnTheBenchText);
		(void)DoPracticeDuelAction(PRACTICEDUEL_DONE_PUTTING_ON_BENCH);
	}
	uint8_t verify_flags = DoPracticeDuelAction(PRACTICEDUEL_VERIFY_INITIAL_PLAY);
	if (verify_flags & FLAG_C)
		goto bench_loop;
	return (ChooseInitialArenaAndBenchPokemonResult){
		(verify_flags == 0u) ? FLAG_Z : 0u};
}
/* <<< factory ChooseInitialArenaAndBenchPokemon */
/* >>> factory TurnDuelistTakePrizes */
TurnDuelistTakePrizesResult TurnDuelistTakePrizes(void)
{
	FinishQueuedAnimations();
	LoadTxRam3((uint16_t)wNumberPrizeCardsToTake);
	DuelistVarResult duelist = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	if (duelist.a == DUELIST_TYPE_PLAYER) {
		(void)DrawWideTextBox_WaitForInput(WillDrawNPrizesText);
		SelectPrizeCards(wNumberPrizeCardsToTake);
	} else {
		uint16_t play_area = (uint16_t)(((uint16_t)hWhoseTurn << 8) | PLAYER_TURN);
		DrawYourOrOppPlayAreaScreen_Bank0(play_area);
		(void)DrawWideTextBox_PrintText(WillDrawNPrizesText);
		wTempNumRemainingPrizeCards = CountPrizes();
		(void)AIDoAction_TakePrize();
		for (uint8_t delay = 60u; delay != 0u; --delay)
			DoFrame();
		if (wTempNumRemainingPrizeCards < wNumberPrizeCardsToTake)
			LoadTxRam3((uint16_t)wTempNumRemainingPrizeCards);
		Func_82b6();
		(void)DrawWideTextBox_WaitForInput(DrewNPrizesText);
	}
	DuelistVarResult prizes = GetTurnDuelistVariable(DUELVARS_PRIZES);
	uint8_t f = (prizes.a == 0u) ? 0x90u : 0u;
	return (TurnDuelistTakePrizesResult){prizes.a, f, prizes.hl};
}
/* <<< factory TurnDuelistTakePrizes */
/* >>> factory Func_6fa5 */
Func6fa5Result Func_6fa5(void)
{
	DuelCoreStateWideResult knocked = CountKnockedOutPokemon();
	if ((knocked.f & 0x10u) == 0u)
		return (Func6fa5Result){knocked.f};

	SwapTurn();
	TurnDuelistTakePrizesResult prizes = TurnDuelistTakePrizes();
	SwapTurn();
	if ((prizes.f & 0x10u) == 0u)
		return (Func6fa5Result){prizes.f};

	SwapTurn();
	DrawDuelMainScene();
	(void)DrawWideTextBox_WaitForInput(TookAllThePrizesText);
	SwapTurn();
	return (Func6fa5Result){0x10u};
}
/* <<< factory Func_6fa5 */
/* >>> factory Func_1cb5e */
void Func_1cb5e(uint8_t a)
{
	if (a >= 0x96u) {
		Func_1ce03(a);
		return;
	}
	if (a != DUEL_ANIM_DAMAGE_HUD) {
		InitScreenAnimation();
		return;
	}

	uint8_t damage_high = gb_read8((uint16_t)(wDuelAnimDamage_ADDR + 1u));
	uint8_t damage_low = wDuelAnimDamage;
	if (damage_high > 0x03u || (damage_high == 0x03u && damage_low >= 0xE8u)) {
		return;
	}

	wDamageCharAnimDelay = 0u;
	wVRAMTileOffset = 0u;
	wWhichOBPalIndex = 0u;
	LoadOBPalette(PALETTE_DUEL_DAMAGE);

	DrawDamageAnimationNumbers();
	uint8_t effectiveness = wDuelAnimEffectiveness;
	if ((effectiveness & 0x01u) != 0u)
		DrawDamageAnimationWeak();
	wDamageCharAnimDelay = 18u;
	if ((effectiveness & 0x02u) != 0u)
		DrawDamageAnimationResist();
	if ((effectiveness & 0x04u) != 0u)
		DrawDamageAnimationArrow(0x20u);

	wDuelAnimEffectiveness = 0u;
}
/* <<< factory Func_1cb5e */
/* --- factory StartDuel */
/* >>> factory StartDuel_VSAIOpp */
void StartDuel_VSAIOpp(void)
{
	hWhoseTurn = PLAYER_TURN;
	wPlayerDuelistType = DUELIST_TYPE_PLAYER;
	wOpponentDeckID = wNPCDuelDeckID;
	LoadPlayerDeck();
	SwapTurn();
	(void)LoadOpponentDeck();
	SwapTurn();
	wCurrentDuelMenuItem = 0u;
	SetupDuel();
	wDuelInitialPrizes = wNPCDuelPrizes;
	InitVariablesToBeginDuel();
	PlaySong(wDuelTheme);
	if ((HandleDuelSetup().f & FLAG_C) != 0u)
		return;
	MainDuelLoop();
}
/* <<< factory StartDuel_VSAIOpp */
/* --- factory StartDuel_VSLinkOpp */
/* --- part LINK_OPP_TURN_CHECK_PLAY_AREA */
/* --- part LINK_OPP_TURN_NUM_OPP_ACTIONS */
/* --- part g_link_opponent_turn_return */
/* --- part g_link_opponent_turn_armed */
/* --- factory SetLinkDuelTransmissionFrameFunction */
/* >>> factory DisplayPlayAreaScreen */
/* core.asm:4933-5022. Draws the play area list, then loops on menu input.
 * Pressing one of wNoItemSelectionMenuKeys opens the highlighted card's page
 * and redraws; choosing a Pokemon with HP left exits without carry; cancelling
 * exits with carry. The Select shortcut hands off to the selection entry, which
 * re-enters this body with a narrower key mask. */
PlayAreaScreenResult DisplayPlayAreaScreen(uint8_t a)
{
	uint8_t saved_index = hTempCardIndex_ff98;
	uint16_t params;

	wNoItemSelectionMenuKeys = a;
	if (wPlayAreaScreenLoaded != 0u)
		goto init_menu;
	wSelectedDuelSubMenuItem = 0u;
	wPlayAreaScreenLoaded = 1u;

redraw:
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	SetDefaultConsolePalettes();
	(void)LoadDuelCardSymbolTiles();
	(void)LoadDuelCheckPokemonScreenTiles();
	PrintPlayAreaCardList();
	EnableLCD();

init_menu:
	params = wExcludeArenaPokemon != 0u ? PLAY_AREA_PARAMS_EXCLUDED
					    : PLAY_AREA_PARAMS_INCLUDED;
	InitializeMenuParameters(wSelectedDuelSubMenuItem, &params);
	wNumMenuItems = wNumPlayAreaItems;
	for (;;) {
		DoFrame();
		BenchPokemonMenuResult bench = SelectingBenchPokemonMenu();

		if ((bench.f & 0x10u) != 0u) {
			if (bench.a == 0x02u)
				goto exit_selected;
			hTempCardIndex_ff98 = saved_index;
			return OpenPlayAreaScreenForSelection();
		}

		HandleMenuInputResult input = HandleMenuInput();

		if ((input.f & 0x10u) == 0u)
			continue;
		wSelectedDuelSubMenuItem = input.e;
		wCurPlayAreaSlot = (uint8_t)(wExcludeArenaPokemon + input.e);
		if ((hKeysPressed & wNoItemSelectionMenuKeys) != 0u) {
			DuelistVarResult card = GetTurnDuelistVariable(
				(uint8_t)(wCurPlayAreaSlot + DUELVARS_ARENA_CARD));

			if (card.a != 0xFFu) {
				LoadCardDataToBuffer1_FromCardID(
					GetCardIDFromDeckIndex(card.a));
				OpenCardPage_FromCheckPlayArea(0u, 0u, 0u, 0u, 0u, 0u, 0u);
			}
			goto redraw;
		}
		hTempPlayAreaLocation_ff9d =
			(uint8_t)(hCurMenuItem + wExcludeArenaPokemon);
		if (hCurMenuItem == MENU_CANCEL)
			goto exit_cancel;
		{
			DuelistVarResult hp = GetTurnDuelistVariable((uint8_t)(
				hTempPlayAreaLocation_ff9d + DUELVARS_ARENA_CARD_HP));

			if (hp.a != 0u)
				goto exit_selected;
		}
		goto init_menu;
	}

exit_selected:
	hTempCardIndex_ff98 = saved_index;
	hCurMenuItem = hTempPlayAreaLocation_ff9d;
	return (PlayAreaScreenResult){hCurMenuItem,
		hCurMenuItem == 0u ? 0x80u : 0x00u};

exit_cancel:
	/* core.asm:5016-5021: `pop af` restores the entry flags before `scf`, so
	 * Z here is the caller's, not `cp MENU_CANCEL`'s. Callers test carry
	 * alone; a caller that needs the exact byte rebuilds it from its own
	 * entry flags (Potion_PlayerSelection). */
	hTempCardIndex_ff98 = saved_index;
	hCurMenuItem = hTempPlayAreaLocation_ff9d;
	return (PlayAreaScreenResult){hCurMenuItem, 0x90u};
}
/* <<< factory DisplayPlayAreaScreen */
/* >>> factory ReplaceKnockedOutPokemon */
ReplaceKnockedOutPokemonResult ReplaceKnockedOutPokemon(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)f;
	DuelistVarResult hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	if (hp.a != 0u)
		return (ReplaceKnockedOutPokemonResult){hp.a, hp.a == 0u ? FLAG_Z : 0u, b, c, d, e, hp.hl};

	ClearAllStatusConditions();
	HasAlivePokemonInPlayAreaResult bench = HasAlivePokemonInBench();
	if ((bench.f & FLAG_C) != 0u) {
		DrawDuelMainScene();
		WaitResult wait = DrawWideTextBox_WaitForInput(ThereAreNoPokemonInPlayAreaText);
		return (ReplaceKnockedOutPokemonResult){
			wait.a, (uint8_t)(wait.f | FLAG_C), wait.b, wait.c, wait.d, wait.e, wait.hl};
	}

	/* core.asm:7360-7407. The player's pick loops on the selection screen
	 * alone (`.select_pokemon`) until a slot is chosen and, after the
	 * practice duel's check, the chosen bench card is swapped into the arena. */
	DuelistVarResult type = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	int player = type.a == DUELIST_TYPE_PLAYER;
	if (player) {
		DrawDuelMainScene();
		(void)DrawWideTextBox_WaitForInput(SelectPokemonToPlaceInTheArenaText);
		wPlayAreaSelectAction = 1u;
		(void)DoPracticeDuelAction(PRACTICEDUEL_PLAY_STARYU_FROM_BENCH);
	}
	else {
		(void)AIDoAction_KOSwitch();
		hTempPlayAreaLocation_ff9d = hTemp_ffa0;
	}

	for (;;) {
		if (player) {
			PlayAreaScreenResult picked;
			while (((picked = OpenPlayAreaScreenForSelection()).f & FLAG_C) != 0u)
				;
			a = hTempPlayAreaLocation_ff9d;
		}
		FinishQueuedAnimations();
		if ((DoPracticeDuelAction(PRACTICEDUEL_REPLACE_KNOCKED_OUT_POKEMON) & FLAG_C) == 0u)
			break;
		player = 1;
	}
	(void)SwapPlayAreaPokemon(hTempPlayAreaLocation_ff9d, PLAY_AREA_ARENA);
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	WaitResult detail = DisplayCardDetailScreen(arena.a, DuelistPlacedACardText);
	return (ReplaceKnockedOutPokemonResult){
		detail.a, (uint8_t)(detail.f & 0x80u), detail.b, detail.c,
		detail.d, detail.e, detail.hl};
}
/* <<< factory ReplaceKnockedOutPokemon */
/* >>> factory DuelMainInterface */
void DuelMainInterface(void)
{
	uint8_t type;

	DrawDuelMainScene();
	type = wDuelistType;
	if (type == DUELIST_TYPE_PLAYER) {
		PrintDuelMenuAndHandleInput();
		return;
	}
	frame_boundary_vblank_sync();
	wVBlankCounter = 0u;
	wSkipDuelistIsThinkingDelay = 0u;
	(void)DrawWideTextBox_PrintTextNoDelay(DuelistIsThinkingText);
	(void)AIDoAction_Turn();
	wPlayerAttackingCardIndex = 0xFFu;
	wPlayerAttackingAttackIndex = 0xFFu;
}
/* <<< factory DuelMainInterface */
/* >>> factory DuelMenu_Done */
/* core.asm:467-475. `jp c, RestartPracticeDuelTurn` is a tail jump, so that
 * callee's `ret` reaches this routine's caller. */
void DuelMenu_Done(void)
{
	if ((DoPracticeDuelAction(PRACTICEDUEL_REPEAT_INSTRUCTIONS) & 0x10u) != 0u) {
		RestartPracticeDuelTurn();
		return;
	}
	hOppActionTableIndex = OPPACTION_FINISH_NO_ATTACK;
	ClearNonTurnTemporaryDuelvars();
}
/* <<< factory DuelMenu_Done */
/* >>> factory DuelMenu_Retreat */
/* core.asm:478-537. Every exit is a tail jump into DuelMainInterface or
 * PrintDuelMenuAndHandleInput, so those loops' exits are this one's. */
void DuelMenu_Retreat(void)
{
	uint8_t status = (uint8_t)(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ);
	hTemp_ffa0 = status;
	if (status == CONFUSED) {
		if (wConfusionRetreatCheckWasUnsuccessful == 0u) {
			CheckAbleToRetreatResult able = CheckAbleToRetreat();
			if ((able.f & 0x10u) != 0u) {
				(void)DrawWideTextBox_WaitForInput(able.hl);
				PrintDuelMenuAndHandleInput();
				return;
			}
			if ((DisplayRetreatScreen(status).f & 0x10u) != 0u) {
				DuelMainInterface();
				return;
			}
			(void)DrawWideTextBox_WaitForInput(SelectPkmnOnBenchToSwitchWithActiveText);
			PlayAreaScreenResult chosen = OpenPlayAreaScreenForSelection();
			if ((chosen.f & 0x10u) != 0u) {
				DuelMainInterface();
				return;
			}
			wBenchSelectedPokemon = chosen.a;
			hTempPlayAreaLocation_ffa1 = chosen.a;
			hOppActionTableIndex = OPPACTION_ATTEMPT_RETREAT;
			if ((AttemptRetreat().f & 0x10u) == 0u) {
				DuelMainInterface();
				return;
			}
			DrawDuelMainScene();
		}
		(void)DrawWideTextBox_WaitForInput(UnableToRetreatText);
		PrintDuelMenuAndHandleInput();
		return;
	}

	/* Not confused: the cost is discarded, returned so the play area screen
	 * lists the retreating Pokemon with its energies updated, then discarded
	 * for good by AttemptRetreat (core.asm:511-516). */
	CheckAbleToRetreatResult able = CheckAbleToRetreat();
	if ((able.f & 0x10u) != 0u) {
		(void)DrawWideTextBox_WaitForInput(able.hl);
		PrintDuelMenuAndHandleInput();
		return;
	}
	if ((DisplayRetreatScreen(status).f & 0x10u) != 0u) {
		DuelMainInterface();
		return;
	}
	(void)DiscardRetreatCostCards();
	(void)DrawWideTextBox_WaitForInput(SelectPkmnOnBenchToSwitchWithActiveText);
	PlayAreaScreenResult chosen = OpenPlayAreaScreenForSelection();
	wBenchSelectedPokemon = chosen.a;
	hTempPlayAreaLocation_ffa1 = chosen.a;
	(void)ReturnRetreatCostCardsToArena(0u, 0u, 0u, 0u, 0u);
	if ((chosen.f & 0x10u) != 0u) {
		DuelMainInterface();
		return;
	}
	hOppActionTableIndex = OPPACTION_ATTEMPT_RETREAT;
	(void)AttemptRetreat();
	DuelMainInterface();
}
/* <<< factory DuelMenu_Retreat */
/* >>> factory PlayEnergyCard */
/* core.asm:586-623. c is the energy card's type. Exits are tail jumps into
 * DuelMainInterface, OpenPlayerHandScreen or ReloadCardListScreen. */
void PlayEnergyCard(uint8_t c)
{
	int set_played;

	if (c == TYPE_ENERGY_WATER && (IsRainDanceActive().f & FLAG_C) != 0u) {
		/* .rain_dance_active */
		(void)HasAlivePokemonInPlayArea();
		if ((OpenPlayAreaScreenForSelection().f & FLAG_C) != 0u) {
			DuelMainInterface();
			return;
		}
		if ((CheckRainDanceScenario().f & FLAG_C) != 0u) {
			set_played = 0;
		} else if (wAlreadyPlayedEnergy == 0u) {
			set_played = 1;
		} else {
			(void)DrawWideTextBox_WaitForInput(MayOnlyAttachOneEnergyCardText);
			OpenPlayerHandScreen();
			return;
		}
	} else {
		/* .not_water_energy */
		if (wAlreadyPlayedEnergy != 0u) {
			/* .already_played_energy, then ReloadCardListScreen */
			(void)DrawWideTextBox_WaitForInput(MayOnlyAttachOneEnergyCardText);
			ReloadCardListScreen();
			return;
		}
		(void)HasAlivePokemonInPlayArea();
		if ((OpenPlayAreaScreenForSelection().f & FLAG_C) != 0u) {
			DuelMainInterface();
			return;
		}
		set_played = 1;
	}
	if (set_played)
		wAlreadyPlayedEnergy = TRUE;
	/* .play_energy */
	uint8_t location = hTempPlayAreaLocation_ff9d;
	hTempPlayAreaLocation_ffa1 = location;
	uint8_t index = hTempCardIndex_ff98;
	hTemp_ffa0 = index;
	(void)PutHandCardInPlayArea(index, location);
	(void)PrintPlayAreaCardList_EnableLCD();
	hOppActionTableIndex = OPPACTION_PLAY_ENERGY;
	PrintAttachedEnergyToPokemon();
	DuelMainInterface();
}
/* <<< factory PlayEnergyCard */
/* --- factory UnreferencedDrawCardFromDeckToHand */
/* >>> factory OppAction_ForceSwitchActive */
void OppAction_ForceSwitchActive(void)
{
	(void)DrawWideTextBox_WaitForInput(SelectPkmnOnBenchToSwitchWithActiveText);
	SwapTurn();
	(void)HasAlivePokemonInBench();
	wPlayAreaSelectAction = 1u;
	/* core.asm:6700-6702: the selection screen repeats until a slot is taken. */
	while ((OpenPlayAreaScreenForSelection().f & FLAG_C) != 0u)
		;
	SwapTurn();
	(void)0;
}
/* <<< factory OppAction_ForceSwitchActive */
/* >>> factory OppAction_UseAttack */
OppActionUseAttackResult OppAction_UseAttack(uint8_t b, uint8_t d, uint8_t e)
{
	(void)TryExecuteEffectCommandFunction(EFFECTCMDTYPE_DISCARD_ENERGY, b, d, e);
	CheckSelfConfusionDamageResult confusion = CheckSelfConfusionDamage();
	if ((confusion.f & 0x10u) != 0u) {
		(void)HandleConfusionDamageToSelf();
		wOpponentTurnEnded = 1u;
		return (OppActionUseAttackResult){1u};
	}
	DisplayOpponentUsedAttackScreen();
	PrintPokemonsAttackTextResult text = PrintPokemonsAttackText();
	(void)WaitForWideTextBoxInput();
	wSkipDuelistIsThinkingDelay = 1u;
	return (OppActionUseAttackResult){1u};
}
/* <<< factory OppAction_UseAttack */
/* --- factory HandleWaitingLinkOpponentMenu */
/* >>> factory HandleBetweenTurnsEvents */
/* core.asm:6827-6897. Nothing to show when neither arena card carries a
 * status condition: PlusPowers and Defenders are discarded and that is all.
 * Otherwise the "between turns" box message runs poison, sleep, and paralysis
 * for both sides and resolves any knockouts that produced. */

static void handle_between_turns_status(void)
{
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint16_t temp_non_turn_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_non_turn_card_id, GetCardIDFromDeckIndex(arena.a));
	uint16_t status = (uint16_t)(((uint16_t)hWhoseTurn << 8) | DUELVARS_ARENA_CARD_STATUS);
	if (gb_read8(status) == 0u)
		return;
	if ((HandlePoisonDamage(0u, status).f & 0x10u) != 0u)
		return;
	(void)HandleSleepCheck(status);
}

void HandleBetweenTurnsEvents(void)
{
	DuelCoreStatusResult turn = IsArenaPokemonAsleepOrPoisoned();
	uint8_t something = (uint8_t)((turn.f & 0x10u) != 0u || turn.a == PARALYZED);
	if (!something) {
		SwapTurn();
		DuelCoreStatusResult other = IsArenaPokemonAsleepOrPoisoned();
		SwapTurn();
		something = (uint8_t)((other.f & 0x10u) != 0u);
	}
	if (!something) {
		(void)DiscardAttachedPlusPowers();
		SwapTurn();
		(void)DiscardAttachedDefenders();
		SwapTurn();
		return;
	}
	ResetAnimationQueue();
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	DrawDuelBoxMessage(BOXMSG_BETWEEN_TURNS);
	(void)DrawWideTextBox_WaitForInput(BetweenTurnsText);

	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint16_t temp_non_turn_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_non_turn_card_id, GetCardIDFromDeckIndex(arena.a));
	uint16_t status = (uint16_t)(((uint16_t)hWhoseTurn << 8) | DUELVARS_ARENA_CARD_STATUS);
	if (gb_read8(status) != 0u && (HandlePoisonDamage(0u, status).f & 0x10u) == 0u) {
		(void)HandleSleepCheck(status);
		if ((gb_read8(status) & CNF_SLP_PRZ) == PARALYZED) {
			gb_write8(status, (uint8_t)(gb_read8(status) & DOUBLE_POISONED));
			RedrawTurnDuelistsMainSceneOrDuelHUD();
			PrintCardNameFromCardIDInTextBox(IsCuredOfParalysisText);
			PlayBetweenTurnsAnimation(DUEL_ANIM_HEAL_7027);
			(void)WaitForWideTextBoxInput();
		}
	}
	(void)DiscardAttachedPlusPowers();
	SwapTurn();
	handle_between_turns_status();
	(void)DiscardAttachedDefenders();
	SwapTurn();
	(void)HandleBetweenTurnKnockOuts();
}
/* <<< factory HandleBetweenTurnsEvents */
/* >>> factory MainDuelLoop */
/* core.asm:73-217. One turn per iteration: start-of-turn substatus, the turn
 * screen, the turn itself, then the between-turns work. wDuelFinished is
 * turns. The finished path draws the result, animates it with the matching
 * song, and a tie restarts the whole loop as sudden death. */
void MainDuelLoop(void)
{
	uint8_t saved_turn;
	uint8_t finished;
	uint8_t anim;
	uint8_t song;
	uint8_t emotion;
	uint16_t text;

main_loop:
	wCurrentDuelMenuItem = 0u;
	UpdateSubstatusConditions_StartOfTurn();
	DisplayDuelistTurnScreen();
	HandleTurn();

	/* .between_turns */
	if (wDuelFinished != 0u)
		goto duel_finished;
	UpdateSubstatusConditions_EndOfTurn();
	HandleBetweenTurnsEvents();
	FinishQueuedAnimations();
	if (wDuelFinished != 0u)
		goto duel_finished;

	wDuelTurns = (uint8_t)(wDuelTurns + 1u);
	/* eight player turns and seven opponent turns */
	if (wDuelType == DUELTYPE_PRACTICE && wIsPracticeDuel != 0u
	    && wDuelTurns >= 15u) {
		wDuelResult = DUEL_WIN_MAIN;
		return;
	}
	SwapTurn();
	goto main_loop;

duel_finished:
	ZeroObjectPositionsAndToggleOAMCopy();
	EmptyScreen();
	DrawDuelBoxMessage(BOXMSG_DECISION_MAIN);
	(void)DrawWideTextBox_WaitForInput(DECISION_TEXT_MAIN);
	EmptyScreen();
	saved_turn = hWhoseTurn;
	hWhoseTurn = PLAYER_TURN;
	DrawDuelistPortraitsAndNames();
	PrintDuelResultStats();
	hWhoseTurn = saved_turn;

	ResetAnimationQueue();
	finished = wDuelFinished;
	/* the winner is the active duelist on a win and the other one on a loss */
	if ((finished == TURN_PLAYER_WON && hWhoseTurn == PLAYER_TURN)
	    || (finished == TURN_PLAYER_LOST && hWhoseTurn != PLAYER_TURN)) {
		wDuelResult = DUEL_WIN_MAIN;
		anim = DUEL_ANIM_DUEL_WIN_MAIN;
		song = MUSIC_MATCH_VICTORY_MAIN;
		emotion = EMOTION_SAD;
		text = WON_DUEL_TEXT_MAIN;
	} else if (finished == TURN_PLAYER_WON || finished == TURN_PLAYER_LOST) {
		wDuelResult = DUEL_LOSS_MAIN;
		anim = DUEL_ANIM_DUEL_LOSS_MAIN;
		song = MUSIC_MATCH_LOSS_MAIN;
		emotion = EMOTION_HAPPY;
		text = LOST_DUEL_TEXT_MAIN;
	} else {
		anim = DUEL_ANIM_DUEL_DRAW_MAIN;
		song = MUSIC_MATCH_DRAW_MAIN;
		emotion = EMOTION_NEUTRAL;
		text = DUEL_WAS_A_DRAW_TEXT_MAIN;
	}

	(void)PlayDuelAnimation(anim);
	PlaySong(song);
	DrawOpponentPortrait(wOpponentPortrait, 13u, 1u, emotion);
	hWhoseTurn = OPPONENT_TURN_MAIN;
	(void)DrawWideTextBox_PrintText(text);
	EnableLCD();
	do {
		DoFrame();
	} while (AssertSongFinished() != 0u);

	if (wDuelFinished != TURN_PLAYER_TIED) {
		PlayDefaultSong();
		(void)WaitForWideTextBoxInput();
		FinishQueuedAnimations();
		hWhoseTurn = PLAYER_TURN;
		return;
	}

	/* .tied_duel: replay the duel as a one-prize sudden death match */
	(void)WaitForWideTextBoxInput();
	FinishQueuedAnimations();
	PlaySong(wDuelTheme);
	(void)DrawWideTextBox_WaitForInput(SUDDEN_DEATH_TEXT_MAIN);
	wDuelInitialPrizes = 1u;
	InitVariablesToBeginDuel();
	hWhoseTurn = PLAYER_TURN;
	(void)HandleDuelSetup();
	goto main_loop;
}
/* <<< factory MainDuelLoop */
/* --- factory _ContinueDuel */
/* --- factory DoLinkOpponentTurn */
/* >>> factory TryContinueDuel */
void TryContinueDuel(void)
{
	SetupDuel();
	uint8_t failed = LoadAndValidateDuelSaveData();
	if ((failed & 0x10u) != 0u) {
		(void)HandleFailedToContinueDuel(BackUpIsBrokenText);
		return;
	}
	ClearJoypad(0);
	PlaySong(wDuelTheme);
	wDuelFinished = 0u;
	DuelMainInterface();
	MainDuelLoop();
}
/* <<< factory TryContinueDuel */
/* >>> factory PlayPokemonCard */
PlayPokemonCardResult PlayPokemonCard(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)hl;
	uint8_t stage = wLoadedCard1Stage;
	if (stage == PLAY_POKEMON_CARD_BASIC) {
		DuelistVarResult count = GetTurnDuelistVariable(PLAY_POKEMON_CARD_NUM_POKEMON);
		if (count.a >= PLAY_POKEMON_CARD_MAX_PLAY_AREA) {
			WaitResult waited = DrawWideTextBox_WaitForInput(PLAY_POKEMON_CARD_NO_SPACE_TEXT);
			return (PlayPokemonCardResult){(uint8_t)(waited.f | 0x10u)};
		}

		hTemp_ffa0 = hTempCardIndex_ff98;
		PutHandPokemonResult placed = PutHandPokemonCardInPlayArea(hTemp_ffa0, f);
		hTempPlayAreaLocation_ff9d = placed.a;
		DuelistVarResult stage_var =
			GetTurnDuelistVariable((uint8_t)(hTempPlayAreaLocation_ff9d + PLAY_POKEMON_CARD_ARENA_STAGE));
		gb_write8(stage_var.hl, PLAY_POKEMON_CARD_BASIC);
		hOppActionTableIndex = PLAY_POKEMON_CARD_OPP_BASIC;

		(void)LoadCardDataToBuffer1_FromDeckIndex(hTempCardIndex_ff98);
		CopyCardNameAndLevelResult copied = CopyCardNameAndLevel(20u, b, c, d, e);
		gb_write8(copied.hl, 0u);
		LoadTxRam2(0u);
		WaitResult waited = DrawWideTextBox_WaitForInput(PLAY_POKEMON_CARD_PLACED_TEXT);
		DuelRoutineResult processed = ProcessPlayedPokemonCard(
			copied.a, waited.f, copied.b, copied.c, copied.d, copied.e, copied.hl);
		return (PlayPokemonCardResult){(uint8_t)(processed.a == 0u ? 0x80u : 0x00u)};
	}

	DuelistVarResult count = GetTurnDuelistVariable(PLAY_POKEMON_CARD_NUM_POKEMON);
	uint8_t candidate_found = 0u;
	uint16_t candidate_hl = 0u;
	for (uint8_t slot = PLAY_POKEMON_CARD_ARENA; slot < count.a; slot++) {
		EvolveResult check = CheckIfCanEvolveInto(hTempCardIndex_ff98, slot);
		if ((check.f & 0x10u) == 0u) {
			candidate_found = 1u;
			candidate_hl = check.hl;
			break;
		}
	}
	if (!candidate_found) {
		uint16_t reason = PLAY_POKEMON_CARD_NO_EVOLUTION_TEXT;
		for (uint8_t slot = PLAY_POKEMON_CARD_ARENA; slot < count.a; slot++) {
			EvolveResult check = CheckIfCanEvolveInto(hTempCardIndex_ff98, slot);
			if ((check.f & 0x10u) != 0u && (check.f & 0x80u) == 0u) {
				reason = PLAY_POKEMON_CARD_CANT_EVOLVE_TEXT;
				break;
			}
		}
		WaitResult waited = DrawWideTextBox_WaitForInput(reason);
		return (PlayPokemonCardResult){(uint8_t)(waited.f | 0x10u)};
	}

	PrehistoricPowerResult prehistoric = IsPrehistoricPowerActive(candidate_hl);
	if ((prehistoric.f & 0x10u) != 0u) {
		WaitResult waited = DrawWideTextBox_WaitForInput(prehistoric.hl);
		return (PlayPokemonCardResult){(uint8_t)(waited.f | 0x10u)};
	}
	(void)HasAlivePokemonInPlayArea();

	for (;;) {
		PlayAreaScreenResult screen = OpenPlayAreaScreenForSelection();
		if ((screen.f & 0x10u) != 0u)
			return (PlayPokemonCardResult){0u};
		hTemp_ffa0 = hTempCardIndex_ff98;
		hTempPlayAreaLocation_ffa1 = hTempPlayAreaLocation_ff9d;
		EvolveResult evolved = EvolvePokemonCardIfPossible(c);
		if ((evolved.f & 0x10u) != 0u)
			continue;
		hOppActionTableIndex = PLAY_POKEMON_CARD_OPP_EVOLVE;
		(void)PrintPlayAreaCardList_EnableLCD();
		PrintPokemonEvolvedIntoPokemon();
		DuelRoutineResult processed = ProcessPlayedPokemonCard(
			evolved.a, evolved.f, 0u, evolved.c, evolved.d, evolved.e, evolved.hl);
		(void)a;
		return (PlayPokemonCardResult){(uint8_t)(processed.a == 0u ? 0x80u : 0x00u)};
	}
}
/* <<< factory PlayPokemonCard */
/* === factory AIAttachEnergyInHandToCardInBench */
/* === factory AISelectSpecialAttackParameters */
/* === factory CheckDamageToMrMime */
/* === factory DrawDamageAnimationNumbers */
/* === factory LoadAnimCoordsAndFlags */
/* === factory LoadPlayAreaCardGfx */
/* === factory LookForEnergyNeededForAttackInHand */
/* === factory LookForEnergyNeededInHand */
/* === factory PlayBufferedDuelAnimations */
/* === factory PlayShuffleAndDrawCardsAnimation */
/* === factory PrintAndLoadAttacksToDuelTempList */
/* === factory RaiseAIScoreToAllMatchingIDsInBench */
/* === factory TrySetUpBossStartingPlayArea */
