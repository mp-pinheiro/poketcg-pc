#include "home/duel_core.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/palettes.h"
#include "mem.h"
#include "home/frames.h"
#include "home/play_animation.h"
#include "home/menus.h"
#include "home/substatus.h"
#include "home/duel.h"

#define PLAYER_TURN  ((uint8_t)(wPlayerDuelVariables_ADDR >> 8))
#define OPPONENT_TURN ((uint8_t)(wOpponentDuelVariables_ADDR >> 8))

static uint16_t get_non_turn_duelvar_addr(uint8_t offset)
{
	uint8_t turn = hWhoseTurn == PLAYER_TURN ? OPPONENT_TURN : PLAYER_TURN;
	return (uint16_t)(((uint16_t)turn << 8) | offset);
}

static void load_tx_ram2(uint16_t text_id)
{
	gb_write8(wTxRam2_ADDR, (uint8_t)text_id);
	gb_write8((uint16_t)(wTxRam2_ADDR + 1), (uint8_t)(text_id >> 8));
}



#define TYPE_TRAINER 0x10u
#define TYPE_PKMN_COLORLESS 0x06u
#define CARD_LOCATION_PLAY_AREA 0x10u
#define CARD_DATA_HP 0x08u
#define CARD_DATA_AI_INFO 0x40u
#define TRAINER_TO_PKMN_DATA 0x6db9u /* bank 1 */
#define MYSTERIOUS_FOSSIL 0xccu
#define CLEFAIRY_DOLL 0xcbu

static const uint8_t *trainer_to_pkmn_data(void)
{
	return rom_ptr(1u, TRAINER_TO_PKMN_DATA);
}

/* core.asm:7123-7163. Entry: a = deck index (a duelvar offset), hl = wLoadedCard*
 * buffer, de = the card id. Overwrites a trainer card in the play area with a
 * generic colorless Pokemon (56 bytes from .trainer_to_pkmn_data). Exit contracts:
 *  - not a trainer:          a = card type, hl/de preserved
 *  - not in the play area:   a = 0, hl/de preserved
 *  - wrong id high byte:     a = d, hl/de preserved
 *  - overwrite:              a = last table byte, hl = buffer + $40, de preserved,
 *                            c = 0
 */
TrainerConvertResult ConvertSpecialTrainerCardToPokemon(uint8_t a, uint16_t hl, uint16_t de)
{
	uint8_t card_type = gb_read8(hl);
	if (card_type != TYPE_TRAINER)
		return (TrainerConvertResult){card_type, a, hl};

	uint8_t location = gb_read8((uint16_t)(((uint16_t)hWhoseTurn << 8) | a)) &
			   CARD_LOCATION_PLAY_AREA;
	if (!location)
		return (TrainerConvertResult){0, a, hl};

	/* core.asm:7136-7148. `cp` never modifies a, so the fossil check falls through
	 * with a = e; the second `cp CLEFAIRY_DOLL; ret nz` exits with a = e whenever
	 * e is neither doll nor fossil. Only the fossil-with-nonzero-high path exits
	 * with a = d. */
	uint8_t id_hi = (uint8_t)(de >> 8);
	uint8_t id_lo = (uint8_t)de;
	if (id_lo == MYSTERIOUS_FOSSIL) {
		if (id_hi != 0)
			return (TrainerConvertResult){id_hi, a, hl};
	} else {
		if (id_lo != CLEFAIRY_DOLL)
			return (TrainerConvertResult){id_lo, a, hl};
		if (id_hi != 0)
			return (TrainerConvertResult){id_hi, a, hl};
	}

	const uint8_t *table = trainer_to_pkmn_data();
	gb_write8(hl, TYPE_PKMN_COLORLESS);
	for (uint8_t i = 0; i < (uint8_t)(CARD_DATA_AI_INFO - CARD_DATA_HP); i++)
		gb_write8((uint16_t)(hl + CARD_DATA_HP + i), table[i]);
	return (TrainerConvertResult){table[CARD_DATA_AI_INFO - CARD_DATA_HP - 1u],
				      0, (uint16_t)(hl + CARD_DATA_AI_INFO)};
}

#define STAGE1 0x01u
#define STAGE2_WITHOUT_STAGE1 0x03u
#define TYPE_ENERGY 0x08u
#define DECK_SIZE 60u
#define DUELVARS_CARD_LOCATIONS 0x00u
#define DUELVARS_ARENA_CARD 0xBBu
#define DUELVARS_ARENA_CARD_STAGE 0xCEu

#define DUELVARS_ARENA_CARD_STATUS                0xF0u
#define DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX  0xF2u
#define DUELVARS_ARENA_CARD_LAST_TURN_DAMAGE       0xF3u
#define DUELVARS_ARENA_CARD_LAST_TURN_STATUS       0xF5u

#define NO_STATUS       0x00u
#define CONFUSED        0x01u
#define ASLEEP          0x02u
#define PARALYZED       0x03u
#define POISONED        0x80u
#define DOUBLE_POISONED 0xC0u
#define CNF_SLP_PRZ     0x0Fu
#define PSN_DBLPSN      0xF0u

#define THERE_WAS_NO_EFFECT_FROM_TX_RAM2_TEXT         0x014Bu
#define THERE_WAS_NO_EFFECT_FROM_POISON_CONFUSION_TEXT 0x0183u
#define THERE_WAS_NO_EFFECT_FROM_PARALYSIS_TEXT        0x0181u
#define THERE_WAS_NO_EFFECT_FROM_SLEEP_TEXT            0x0180u
#define THERE_WAS_NO_EFFECT_FROM_CONFUSION_TEXT        0x0182u
#define THERE_WAS_NO_EFFECT_FROM_POISON_TEXT           0x017Fu
#define THERE_WAS_NO_EFFECT_FROM_TOXIC_TEXT            0x017Eu

/* core.asm:8264-8267 */
void ResetAttackAnimationIsPlaying(void)
{
	wAttackAnimationIsPlaying = 0;
}

/* core.asm:8343-8350 */
void WaitAttackAnimation(void)
{
	if (gb_read8(wLoadedAttackAnimation_ADDR) == 0)
		return;
	do {
		DoFrame();
	} while (CheckAnyAnimationPlaying().f & 0x10u);
}

static void ApplyStatusConditionToArenaPokemon(uint8_t side, uint16_t *hl_addr)
{
	uint16_t arena_addr = (uint16_t)((uint16_t)side << 8 | DUELVARS_ARENA_CARD_STATUS);
	uint16_t lt_addr = (uint16_t)((uint16_t)side << 8 | DUELVARS_ARENA_CARD_LAST_TURN_STATUS);
	uint8_t remove_mask = gb_read8(*hl_addr);
	uint8_t add_mask = gb_read8((uint16_t)(*hl_addr + 1u));
	gb_write8(arena_addr,
		  (uint8_t)((gb_read8(arena_addr) & remove_mask) | add_mask));
	gb_write8(lt_addr,
		  (uint8_t)((gb_read8(lt_addr) & remove_mask) | add_mask));
	*hl_addr = (uint16_t)(*hl_addr + 2u);
}

/* core.asm:7181-7252 */
uint8_t ApplyStatusConditionQueue(void)
{
	wPlayerArenaCardLastTurnStatus = 0;
	wOpponentArenaCardLastTurnStatus = 0;

	uint8_t index = wStatusConditionQueueIndex;
	if (index == 0) return 0x80u;

	uint16_t term_addr = (uint16_t)(wStatusConditionQueue_ADDR + index);
	gb_write8(term_addr, 0);

	NoDamageOrEffectCheckResult ndoe = CheckNoDamageOrEffect(term_addr);
	if (ndoe.f & 0x10u) {
		if (ndoe.hl != 0)
			(void)DrawWideTextBox_PrintText(ndoe.hl);
		uint8_t whose_turn = wWhoseTurn;
		uint16_t hl = wStatusConditionQueue_ADDR;
		for (unsigned i = 0; i < 8u; i++) {
			uint8_t side = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			if (side == 0) break;
			if (side == whose_turn)
				ApplyStatusConditionToArenaPokemon(side, &hl);
			else
				hl = (uint16_t)(hl + 2u);
		}
		return 0x80u;
	}

	uint16_t hl = wStatusConditionQueue_ADDR;
	for (unsigned i = 0; i < 8u; i++) {
		uint8_t side = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (side == 0) break;
		ApplyStatusConditionToArenaPokemon(side, &hl);
	}
	return 0x90u;
}


CardOneStageBelowResult GetCardOneStageBelow(uint8_t d, uint8_t e)
{
	uint8_t slot = hTempPlayAreaLocation_ff9d;

	DuelistVarResult arena = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + slot));
	(void)LoadCardDataToBuffer2_FromDeckIndex(arena.a);
	uint8_t stage = wLoadedCard2Stage;

	if (stage == 0)
		return (CardOneStageBelowResult){stage, d, e, arena.hl, 0x90u};

	gb_write8(wAllStagesIndices_ADDR, 0xFFu);
	gb_write8((uint16_t)(wAllStagesIndices_ADDR + 1u), 0xFFu);
	gb_write8((uint16_t)(wAllStagesIndices_ADDR + 2u), 0xFFu);

	uint8_t target_location = (uint8_t)(slot | CARD_LOCATION_PLAY_AREA);
	DuelistVarResult locations = GetTurnDuelistVariable(DUELVARS_CARD_LOCATIONS);
	uint16_t hl = locations.hl;

	for (uint8_t i = 0; i < DECK_SIZE; i++) {
		if (gb_read8(hl) == target_location) {
			LoadCardDataToBuffer2_FromDeckIndex(i);
			if (wLoadedCard2Type < TYPE_ENERGY) {
				uint8_t stage = wLoadedCard2Stage;
				gb_write8((uint16_t)(wAllStagesIndices_ADDR + stage), i);
			}
		}
		hl = (uint16_t)(hl + 1u);
	}

	DuelistVarResult stage_var = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_STAGE + slot));
	uint16_t stage_addr = wAllStagesIndices_ADDR;
	if (stage_var.a != STAGE1 && stage_var.a != STAGE2_WITHOUT_STAGE1)
		stage_addr = (uint16_t)(stage_addr + 1u);
	uint8_t d_result = gb_read8(stage_addr);

	DuelistVarResult arena2 = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + slot));
	uint8_t a_result = arena2.a;
	uint8_t f_result = (a_result == 0) ? 0x80u : 0x00u;

	return (CardOneStageBelowResult){a_result, d_result, a_result, arena2.hl, f_result};
}

/* core.asm:7804-7816 */
void ClearNonTurnTemporaryDuelvars(void)
{
	uint16_t hl = get_non_turn_duelvar_addr(DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX);
	gb_write8(hl++, 0);
	gb_write8(hl++, 0);
	gb_write8(hl++, 0);
	gb_write8(hl++, 0);
	gb_write8(hl++, 0);
	gb_write8(hl++, 0);
	gb_write8(hl++, 0);
	gb_write8(hl, 0);
}

/* core.asm:7820-7825 */
void ClearNonTurnTemporaryDuelvars_CopyStatus(void)
{
	uint16_t addr = get_non_turn_duelvar_addr(DUELVARS_ARENA_CARD_STATUS);
	wUnused_DefendingPkmnStatus = gb_read8(addr);
	ClearNonTurnTemporaryDuelvars();
}

/* core.asm:7830-7845 */
void UpdateArenaCardLastTurnDamage(void)
{
	uint16_t hl = get_non_turn_duelvar_addr(DUELVARS_ARENA_CARD_LAST_TURN_DAMAGE);
	if (wDefendingWasForcedToSwitch) {
		gb_write8(hl, 0);
		gb_write8((uint16_t)(hl + 1), 0);
	} else {
		gb_write8(hl, wDealtDamage);
		gb_write8((uint16_t)(hl + 1), gb_read8((uint16_t)(wDealtDamage_ADDR + 1)));
	}
}

/* core.asm:7533-7566 */
uint16_t PrintThereWasNoEffectFromStatusText(void)
{
	uint8_t status = wNoEffectFromWhichStatus;
	if (!status) {
		uint16_t name = (uint16_t)((uint16_t)gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1)) << 8
					 | gb_read8(wLoadedAttackName_ADDR));
		load_tx_ram2(name);
		return THERE_WAS_NO_EFFECT_FROM_TX_RAM2_TEXT;
	}
	if (status == (POISONED | CONFUSED))
		return THERE_WAS_NO_EFFECT_FROM_POISON_CONFUSION_TEXT;
	if (status & PSN_DBLPSN) {
		if ((status & PSN_DBLPSN) == POISONED)
			return THERE_WAS_NO_EFFECT_FROM_POISON_TEXT;
		return THERE_WAS_NO_EFFECT_FROM_TOXIC_TEXT;
	}
	uint8_t cnf = status & CNF_SLP_PRZ;
	if (cnf == PARALYZED)
		return THERE_WAS_NO_EFFECT_FROM_PARALYSIS_TEXT;
	if (cnf == ASLEEP)
		return THERE_WAS_NO_EFFECT_FROM_SLEEP_TEXT;
	return THERE_WAS_NO_EFFECT_FROM_CONFUSION_TEXT;
}

void SetDefaultConsolePalettes(void)
{
	uint8_t console = gb_read8(wConsole_ADDR);
	if (console == 0x01u)
		return;
	if (console == 0x02u) {
		gb_write8(wTextBoxFrameType_ADDR, 4);
		uint16_t src = 0x5B44u;
		for (uint8_t i = 0; i < 40; i++)
			gb_write8((uint16_t)(wBackgroundPalettesCGB_ADDR + i),
			          gb_read8((uint16_t)(src + i)));
		for (uint8_t i = 0; i < 8; i++)
			gb_write8((uint16_t)(wObjectPalettesCGB_ADDR + i),
			          gb_read8((uint16_t)(src + i)));
		FlushAllPalettes();
		return;
	}
	uint8_t palette = 0xE4u;
	gb_write8(wOBP0_ADDR, palette);
	gb_write8(wBGP_ADDR, palette);
	gb_write8(wFlushPaletteFlags_ADDR, 0x01u);
}

