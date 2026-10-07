/* >>> part includes */
#include "home/duel.h"
#include <stdio.h>

#include "generated/text_ids.h"
#include "generated/rom.h"
#include "generated/constants.h"
/* <<< part includes */
/* >>> part MENU_CONFIRM */
#define MENU_CONFIRM 0x01u
/* <<< part MENU_CONFIRM */
/* >>> part CURSOR_BLINK_PERIOD_MASK */
#define CURSOR_BLINK_PERIOD_MASK 0x0Fu
/* <<< part CURSOR_BLINK_PERIOD_MASK */
/* >>> part B_CURSOR_BLINK_PERIOD */
#define B_CURSOR_BLINK_PERIOD 4u
/* <<< part B_CURSOR_BLINK_PERIOD */
/* >>> part PAL_SIZE */
#define PAL_SIZE 8u
/* <<< part PAL_SIZE */
/* >>> part includes_OPPONENT_TURN */
#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/card_id_bus.h"
#include "home/duel_core.h"
#include "home/card_color.h"
#include "home/substatus.h"
#include "home/print_text.h"
#include "home/palettes.h"
#include "home/switch_sram.h"
#include "home/menus.h"
#include "home/frames.h"
#include "mem.h"

#include "home/play_area.h"
#include "home/script.h"
#include "home/switch_rom.h"
/* <<< part includes_OPPONENT_TURN */
/* >>> factory _GetCardIDFromDeckIndex */
/* duel.asm:762-777: deck index -> card id, from the turn holder's deck.
 * `ld hl, wPlayerDeck / add hl, de / ld a, [hl]` leaves hl = deck + a. */
DeckCardResult _GetCardIDFromDeckIndex(uint8_t a)
{
	uint16_t deck = hWhoseTurn == PLAYER_TURN ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	uint16_t slot = card_id_index_address(deck, a);
	CardId id = card_id_read_at(slot);
	return (DeckCardResult){hWhoseTurn, id, (uint16_t)(slot + 1u)};
}
/* <<< factory _GetCardIDFromDeckIndex */
/* >>> factory GetCardIDFromDeckIndex_bc */
/* duel.asm:661-668: id in a and c, b = 0, hl preserved. */
DeckCardResult GetCardIDFromDeckIndex_bc(uint8_t a, uint16_t hl)
{
	CardId id = GetCardIDFromDeckIndex(a);
	return (DeckCardResult){hWhoseTurn, id, hl};
}
/* <<< factory GetCardIDFromDeckIndex_bc */
/* >>> factory GetCardInDuelTempList_OnlyDeckIndex */
/* duel.asm:670-684: the temp-list entry in a, shadowed in hTempCardIndex_ff98,
 * hl and de preserved. */
DeckCardResult GetCardInDuelTempList_OnlyDeckIndex(uint8_t a, uint16_t hl)
{
	uint8_t entry = gb_read8((uint16_t)(wDuelTempList_ADDR + a));
	hTempCardIndex_ff98 = entry;
	return (DeckCardResult){entry, 0u, hl};
}
/* <<< factory GetCardInDuelTempList_OnlyDeckIndex */
/* --- part BPA_CONSOLE_CGB */
/* --- part BPA_TILE_TWO_STAGE */
/* --- part BPA_TILE_TWO_STAGE_ALT */
/* === part V0_TILES0 */
/* >>> part V0_TILES1 */
#define V0_TILES1 0x8800u
/* <<< part V0_TILES1 */
/* === part PRIZE_TILE_CGB_ATTR */
/* >>> part copy_card_palette */
static void copy_card_palette(uint8_t palette)
{
	uint16_t src = wCardPalette_ADDR;
	uint8_t offset = (uint8_t)(palette * PAL_SIZE);
	uint16_t dst = (uint16_t)(wBackgroundPalettesCGB_ADDR + offset);
	for (uint8_t i = 0u; i < 3u * PAL_SIZE; i++)
		gb_write8(dst++, gb_read8(src++));
	for (uint8_t i = 0u; i < 0x30u; i++) {
		uint16_t addr = (uint16_t)(wCardAttrMap_ADDR + i);
		gb_write8(addr, (uint8_t)(gb_read8(addr) + palette));
	}
}
/* <<< part copy_card_palette */
/* === part OPPONENT_ICON_COORDS */
/* >>> part includes_hTempPlayAreaLocation_ff9d_ADDR */
#include "home/duel.h"
#include "generated/wram.h"
#include "generated/hram.h"

#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_hTempPlayAreaLocation_ff9d_ADDR */
/* >>> part hTempPlayAreaLocation_ff9d_ADDR */
#define hTempPlayAreaLocation_ff9d_ADDR 0xFF9Du
/* <<< part hTempPlayAreaLocation_ff9d_ADDR */
/* >>> part includes_PLAYER_ICON_COORDINATES_ADDR */
#include "home/duel.h"
#include "home/empty_screen.h"
#include "home/tiles.h"
#include "home/objects.h"
#include "generated/hram.h"
#include "generated/wram.h"
/* <<< part includes_PLAYER_ICON_COORDINATES_ADDR */
/* >>> part PLAYER_ICON_COORDINATES_ADDR */
#define PLAYER_ICON_COORDINATES_ADDR (_DrawPlayAreaToPlacePrizeCards_ADDR + 0x60u)
/* <<< part PLAYER_ICON_COORDINATES_ADDR */
/* >>> part OPP_ICON_COORDINATES_ADDR */
#define OPP_ICON_COORDINATES_ADDR (_DrawPlayAreaToPlacePrizeCards_ADDR + 0x66u)
/* <<< part OPP_ICON_COORDINATES_ADDR */
/* >>> part PEEK_WHICH_CARD_TEXT */
#define PEEK_WHICH_CARD_TEXT WhichCardWouldYouLikeToSeeText
/* <<< part PEEK_WHICH_CARD_TEXT */
/* >>> part HTEMP_LIST_PTR */
#define HTEMP_LIST_PTR 0xFF99u
/* <<< part HTEMP_LIST_PTR */
/* >>> factory SortCardsInListByID */
/* duel.asm:589-648. The terminator is $FF, whose bit 7 is the loop-exit test. Each
 * pass finds the lowest-ID card in the remaining span and swaps it to the front,
 * then advances the pointer; the final `bit 7, [hl]` on the terminator leaves
 * Z clear and H set. */
SortResult SortCardsInListByID(uint8_t b, uint8_t c, uint16_t de)
{
	for (;;) {
		uint16_t ptr = list_ptr();
		if (gb_read8(ptr) & 0x80u) {
			/* `bit 7, [hl]` on the $FF terminator: Z clear, H set. */
			return (SortResult){(uint8_t)ptr, b, c, (uint8_t)(de >> 8), (uint8_t)de,
						0x20u, ptr};
		}
		uint16_t lowest_pos = ptr;
		DeckCardResult first = GetCardIDFromDeckIndex_bc(gb_read8(ptr), 0);
		uint16_t lowest_id = first.id;
		uint8_t last_b = (uint8_t)(first.id >> 8);
		/* duel.asm:599-602, 618-622: the running lowest id lives in
		 * hTempCardID_ff9b (two bytes), rewritten on every new lowest. */
		uint16_t lowest_id_addr = hTempCardID_ff9b_ADDR;
		card_id_write(&lowest_id_addr, lowest_id);
		uint16_t scan = (uint16_t)(ptr + 1u);
		while (!(gb_read8(scan) & 0x80u)) {
			DeckCardResult candidate_result = GetCardIDFromDeckIndex_bc(gb_read8(scan), 0);
			uint16_t candidate = candidate_result.id;
			last_b = (uint8_t)(candidate >> 8);
			/* The asm's `cp / jr c, .not_lower_id` updates the slot on EQUAL ids
			 * too (only a strictly smaller current-lowest keeps the slot), so the
			 * sort is unstable: the last equal card moves to the front. */
			if (candidate <= lowest_id) {
				lowest_id = candidate;
				lowest_pos = scan;
				uint16_t lowest_id_addr = hTempCardID_ff9b_ADDR;
				card_id_write(&lowest_id_addr, lowest_id);
			}
			scan++;
		}
		uint8_t front = gb_read8(ptr);
		gb_write8(ptr, gb_read8(lowest_pos));
		gb_write8(lowest_pos, front);
		/* Every pass ends with b = 0 (GetCardIDFromDeckIndex_bc's `ld b, $0`),
		 * c = the swapped-out front, de = the lowest-card position. */
		b = last_b;
		c = front;
		de = lowest_pos;
		list_set_ptr((uint16_t)(ptr + 1u));
	}
}
/* <<< factory SortCardsInListByID */
/* >>> factory TranslateColorToWR */
/* duel.asm:1915-1922. The table is `db $80, $40, $20, $10, $08, $04, $02, $01`
 * (InvertedPowersOf2, 00:1A1A). Entry a is a color index; all other registers
 * are preserved. */
uint8_t TranslateColorToWR(uint8_t a)
{
	return rom_ptr(InvertedPowersOf2_BANK, InvertedPowersOf2_ADDR)[a];
}
/* <<< factory TranslateColorToWR */
/* >>> factory CountCardIDInLocation */
/* duel.asm:1290-1315. Entry hl supplies the page only: `ld l,
 * DUELVARS_CARD_LOCATIONS` overwrites the low byte before the walk, so only h
 * selects the duelist and the exit is page + 60 whatever l held. `ld a, c /
 * pop bc` leaves a = the count and restores bc. */
CardLocationCountResult CountCardIDInLocation(uint8_t b, CardId de, uint16_t hl)
{
	uint16_t base = (uint16_t)((hl & 0xFF00u) | DUELVARS_CARD_LOCATIONS);
	uint8_t count = 0;
	for (uint8_t l = 0; l < DECK_SIZE; l++) {
		if (gb_read8((uint16_t)(base + l)) != b)
			continue;
		if (card_id_read_at(card_id_index_address(
			hWhoseTurn == PLAYER_TURN ? wPlayerDeck_ADDR : wOpponentDeck_ADDR, l)) != de)
			continue;
		count++;
	}
	return (CardLocationCountResult){count, (uint16_t)(base + DECK_SIZE)};
}
/* <<< factory CountCardIDInLocation */
/* >>> part PLAYER2_TEXT_ID */
/* Text ID of the fallback opponent name. */
#define PLAYER2_TEXT_ID Player2Text
/* <<< part PLAYER2_TEXT_ID */
/* >>> factory CopyDeckData */
/* duel.asm:60-104. */
CardListResult CopyDeckData(uint16_t de)
{
	uint16_t deck = hWhoseTurn == PLAYER_TURN ? wPlayerDeck_ADDR : wOpponentDeck_ADDR;
	uint16_t last_slot = (uint16_t)(deck + DECK_SIZE_BYTES - 2u);
	uint16_t dst = deck;
	uint8_t count;
	uint8_t a;
	uint8_t f;

	gb_write8(last_slot, 0u);
	gb_write8((uint16_t)(last_slot + 1u), 0u);
	for (;;) {
		count = gb_read8(de++);
		if (!count)
			break;
		for (uint8_t i = 0u; i < count; i++) {
			CardId id = card_id_read(&de);
			card_id_write(&dst, id);
			de = (uint16_t)(de - 2u);
		}
		de = (uint16_t)(de + 2u);
	}
	gb_write8(wDeckName_ADDR, gb_read8(de++));
	gb_write8((uint16_t)(wDeckName_ADDR + 1u), gb_read8(de));

	uint16_t check = last_slot;
	a = gb_read8(check++);
	a = (uint8_t)(a | gb_read8(check));
	if (a == 0u) {
		f = 0x90u;
		return (CardListResult){a, 0u, (uint8_t)(DECK_SIZE_BYTES - 2u),
			(uint8_t)(de >> 8), (uint8_t)de, f, check};
	}
	check++;
	a = gb_read8(check++);
	a = (uint8_t)(a | gb_read8(check));
	f = a == 0u ? 0x80u : 0x10u;
	return (CardListResult){a, 0u, (uint8_t)(DECK_SIZE_BYTES - 2u),
		(uint8_t)(de >> 8), (uint8_t)de, f, check};
}
/* <<< factory CopyDeckData */
/* --- factory CheckPrizeTaken */
/* >>> factory CopyAttackDataAndDamage */
/* duel.asm:1442-1467. */
AttackCopyResult CopyAttackDataAndDamage(uint8_t e)
{
	CardId card_id = card_id_read_at(wLoadedCard1ID_ADDR);
	uint16_t src = (e == 1) ? wLoadedCard1Atk2_ADDR : wLoadedCard1Atk1_ADDR;
	uint16_t dst = wLoadedAttack_ADDR;
	uint8_t damage;

	uint16_t temp_card_id = wTempCardID_ccc2_ADDR;
	card_id_write(&temp_card_id, card_id);
	for (uint8_t i = 0; i < ATTACK_DATA_LEN; i++)
		gb_write8(dst++, gb_read8(src++));
	damage = gb_read8(wLoadedAttackDamage_ADDR);
	gb_write8(wDamage_ADDR, damage);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), 0);
	gb_write8(wNoDamageOrEffect_ADDR, 0);
	gb_write8(wDealtDamage_ADDR, 0);
	gb_write8((uint16_t)(wDealtDamage_ADDR + 1u), 0);
	return (AttackCopyResult){0, 0, 0x80u, (uint16_t)(wDealtDamage_ADDR + 1u), dst};
}
/* <<< factory CopyAttackDataAndDamage */
/* >>> factory CopyAttackDataAndDamage_FromCardID */
/* duel.asm:1415-1427. */
AttackCopyResult CopyAttackDataAndDamage_FromCardID(uint8_t b, uint8_t c, uint16_t de)
{
	gb_write8(wSelectedAttack_ADDR, c);
	hTempCardIndex_ff9f = b;
	LoadCardDataToBuffer1_FromCardID((CardId)de);
	return CopyAttackDataAndDamage(c);
}
/* <<< factory CopyAttackDataAndDamage_FromCardID */
/* >>> factory ApplyAttachedPlusPower */
/* duel.asm:1976-1988 / 1991-2006. a/f flow through the opaque HtimesL leaf and
 * are omitted. */
PowerModifierResult ApplyAttachedPlusPower(uint8_t b, uint16_t de)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t count = CountCardIDInLocation(b, (CardId)PLUSPOWER, page).a;
	uint16_t product = (uint16_t)(count * 10u);

	return (PowerModifierResult){product, (uint16_t)(de + product)};
}
/* <<< factory ApplyAttachedPlusPower */
/* >>> factory ApplyAttachedDefender */
PowerModifierResult ApplyAttachedDefender(uint8_t b, uint16_t de)
{
	uint16_t page = (uint16_t)((uint16_t)hWhoseTurn << 8);
	uint8_t count = CountCardIDInLocation(b, (CardId)DEFENDER, page).a;
	uint16_t product = (uint16_t)(count * 20u);

	return (PowerModifierResult){product, (uint16_t)(de - product)};
}
/* <<< factory ApplyAttachedDefender */
/* --- part WEAKNESS */
/* --- part RESISTANCE */
/* >>> factory ApplyDamageModifiers_DamageToTarget */
uint16_t ApplyDamageModifiers_DamageToTarget(void)
{
	gb_write8(wDamageEffectiveness_ADDR, 0);

	uint8_t lo = gb_read8(wDamage_ADDR);
	uint8_t hi_byte = gb_read8((uint16_t)(wDamage_ADDR + 1u));
	if (!(hi_byte | lo))
		return 0;

	hTempPlayAreaLocation_ff9d = 0;
	uint16_t de = (uint16_t)((uint16_t)hi_byte << 8 | lo);

	if (hi_byte & 0x80u) {
		de &= (uint16_t)~0x8000u;
		gb_write8(wDamageEffectiveness_ADDR, 0);
		de = HandleDoubleDamageSubstatus(de);
	} else {
		de = HandleDoubleDamageSubstatus(de);
		if (!de)
			return 0;

		uint8_t color = GetPlayAreaCardColor(hTempPlayAreaLocation_ff9d);
		uint8_t wr = TranslateColorToWR(color);

		SwapTurn();
		uint8_t weakness = GetArenaCardWeakness();
		SwapTurn();
		if (weakness & wr) {
			de <<= 1;
			gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | (1u << WEAKNESS)));
		}

		SwapTurn();
		uint8_t resistance = GetArenaCardResistance();
		SwapTurn();
		if (resistance & wr) {
			de = (uint16_t)(de - 30u);
			gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | (1u << RESISTANCE)));
		}
	}

	{
		PowerModifierResult r = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	SwapTurn();
	{
		PowerModifierResult r = ApplyAttachedDefender(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	de = HandleDamageReduction(de);
	if (de & 0x8000u)
		de = 0;
	SwapTurn();
	return de;
}
/* <<< factory ApplyDamageModifiers_DamageToTarget */
/* >>> factory ApplyDamageModifiers_DamageToSelf */
uint16_t ApplyDamageModifiers_DamageToSelf(void)
{
	gb_write8(wDamageEffectiveness_ADDR, 0);

	uint8_t lo = gb_read8(wDamage_ADDR);
	uint8_t hi_byte = gb_read8((uint16_t)(wDamage_ADDR + 1u));
	uint8_t nonzero = (uint8_t)(hi_byte | lo);
	if (!nonzero)
		return 0;

	uint16_t de = (uint16_t)((uint16_t)hi_byte << 8 | lo);
	uint8_t color = GetArenaCardColor();
	uint8_t wr = TranslateColorToWR(color);

	uint8_t weakness = GetArenaCardWeakness();
	if (weakness & wr) {
		de <<= 1;
		gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | (1u << WEAKNESS)));
	}
	uint8_t resistance = GetArenaCardResistance();
	if (resistance & wr) {
		de = (uint16_t)(de - 30u);
		gb_write8(wDamageEffectiveness_ADDR, (uint8_t)(gb_read8(wDamageEffectiveness_ADDR) | (1u << RESISTANCE)));
	}

	{
		PowerModifierResult r = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, de);
		de = r.de;
	}
	{
		PowerModifierResult r = ApplyAttachedDefender(CARD_LOCATION_ARENA, de);
		de = r.de;
	}


	if (de & 0x8000u)
		return 0;
	return de;
}
/* <<< factory ApplyDamageModifiers_DamageToSelf */
/* >>> part WAS_KNOCKED_OUT_TEXT */
#define WAS_KNOCKED_OUT_TEXT WasKnockedOutText
/* <<< part WAS_KNOCKED_OUT_TEXT */
/* >>> factory PrintKnockedOut */
uint8_t PrintKnockedOut(void)
{
	uint16_t card_id = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	LoadCardDataToBuffer1_FromCardID(card_id);
	uint16_t name = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR)
		| (uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8);
	LoadTxRam2(name);
	DrawWideTextBox_PrintText(WAS_KNOCKED_OUT_TEXT);
	uint8_t wait_frames = 40u;
	do {
		DoFrame();
	} while (--wait_frames);
	return 0x90u;
}
/* <<< factory PrintKnockedOut */
/* >>> factory PrintPlayAreaCardKnockedOutIfNoHP */
KnockoutCheckResult PrintPlayAreaCardKnockedOutIfNoHP(uint8_t a)
{
	uint8_t e_val = a;
	uint8_t hp = GetTurnDuelistVariable((uint8_t)(a + DUELVARS_ARENA_CARD_HP)).a;
	if (hp)
		return (KnockoutCheckResult){hp, 0x00u};
	CardId saved = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	uint8_t deck_idx = GetTurnDuelistVariable((uint8_t)(e_val + DUELVARS_ARENA_CARD)).a;
	LoadCardDataToBuffer1_FromDeckIndex(deck_idx);
	uint16_t temp_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, card_id_read_at(wLoadedCard1ID_ADDR));
	PrintKnockedOut();
	temp_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, saved);
	return (KnockoutCheckResult){(uint8_t)(saved >> 8), 0x90u};
}
/* <<< factory PrintPlayAreaCardKnockedOutIfNoHP */
/* >>> factory UpdateArenaCardIDsAndClearTwoTurnDuelVars */
DuelRoutineResult UpdateArenaCardIDsAndClearTwoTurnDuelVars(
	uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)d; (void)hl;
	DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	hTempCardIndex_ff9f = arena.a;
	uint16_t card_id = GetCardIDFromDeckIndex(arena.a);
	uint16_t temp_card_id = wTempTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, card_id);
	SwapTurn();
	arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	card_id = GetCardIDFromDeckIndex(arena.a);
	temp_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, card_id);
	SwapTurn();
	wSentAttackDataToLinkOpponent = 0;
	wStatusConditionQueueIndex = 0;
	wEffectFailed = 0;
	wIsDamageToSelf = 0;
	wDefendingWasForcedToSwitch = 0;
	wMetronomeEnergyCost = 0;
	wNoEffectFromWhichStatus = 0;
	ClearNonTurnTemporaryDuelvars_CopyStatus();
	(void)a;
	(void)e;
	(void)f;
	DuelistVarResult clear_start =
		GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_DISABLED_ATTACK_INDEX);
	return (DuelRoutineResult){0, 0x80u, b, c,
		(uint8_t)(card_id >> 8), (uint8_t)card_id,
		(uint16_t)(clear_start.hl + 7u)};
}
/* <<< factory UpdateArenaCardIDsAndClearTwoTurnDuelVars */
/* >>> factory DrawPlayArea_BenchCards */
/* duel.asm:877-1029 */
void DrawPlayArea_BenchCards(uint8_t c, uint8_t d, uint8_t e)
{
	uint8_t page = wCheckMenuPlayAreaWhichDuelist;
	uint16_t src;
	uint8_t count, n, b;

	if (page != wCheckMenuPlayAreaWhichLayout) {
		d = (uint8_t)(d + (uint8_t)(c * 4u));
		c = (uint8_t)(0u - c);
		page = wCheckMenuPlayAreaWhichDuelist;
	}

	count = gb_read8((uint16_t)(((uint16_t)page << 8) | BPA_DUELVARS_NUM_POKEMON));
	src = (uint16_t)(((uint16_t)page << 8) | BPA_DUELVARS_BENCH1_STAGE);

	for (;;) {
		uint8_t stage, tile;

		count = (uint8_t)(count - 1u);
		if (count == 0u)
			break;
		stage = gb_read8(src);
		src = (uint16_t)(src + 1u);
		tile = (uint8_t)((uint8_t)(stage << 2) + BPA_TILE_STAGE_BASE);
		FillRectangle(tile, 2u, 2u, (uint16_t)((uint16_t)d << 8 | e),
			BPA_RECT_STEPS_TILES);
		hBankVRAM = 1u;
		gb_write8(BPA_RVBK, 1u);
		FillRectangle(0x00u, 2u, 2u,
			(uint16_t)((uint16_t)d << 8 | e), BPA_RECT_STEPS_FLAT);
		hBankVRAM = 0u;
		gb_write8(BPA_RVBK, 0u);
		d = (uint8_t)(d + c);
	}

	count = gb_read8((uint16_t)(((uint16_t)page << 8) | BPA_DUELVARS_NUM_POKEMON));
	n = (uint8_t)(BPA_MAX_PLAY_AREA_POKEMON - count);
	if (n == 0u)
		return;

	b = (uint8_t)(n + 1u);
	for (;;) {
		b = (uint8_t)(b - 1u);
		if (b == 0u)
			break;
		FillRectangle(BPA_TILE_EMPTY_SLOT, 2u, 2u,
			(uint16_t)((uint16_t)d << 8 | e), BPA_RECT_STEPS_TILES);
		hBankVRAM = 1u;
		gb_write8(BPA_RVBK, 1u);
		FillRectangle(0x01u, 2u, 2u,
			(uint16_t)((uint16_t)d << 8 | e), BPA_RECT_STEPS_FLAT);
		hBankVRAM = 0u;
		gb_write8(BPA_RVBK, 0u);
		d = (uint8_t)(d + c);
	}
}
/* <<< factory DrawPlayArea_BenchCards */
/* --- factory Func_8bf2 */
/* --- factory SendAttackDataToLinkOpponent */
/* >>> factory DrawPlayArea_PrizeCards */
void DrawPlayArea_PrizeCards(uint16_t hl)
{
	GetDuelInitialPrizesUpperBitsSet();
	uint8_t page = wCheckMenuPlayAreaWhichDuelist;
	uint16_t prize_addr = (uint16_t)(((uint16_t)page << 8) | DUELVARS_PRIZES);
	uint8_t prize_bits = gb_read8(prize_addr);
	uint8_t count = wDuelInitialPrizes;
	for (uint8_t b = 0u; b < count; ++b) {
		uint8_t taken = (uint8_t)(prize_bits & 1u);
		prize_bits = (uint8_t)(prize_bits >> 1);
		uint8_t tile = taken != 0u ? 0xDCu : 0xE0u;
		uint8_t x = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint8_t y = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		uint16_t de = (uint16_t)(((uint16_t)y << 8) | x);
		FillRectangle(tile, 2u, 2u, de, 0x0102u);
		hBankVRAM = 1u;
		gb_write8(0xFF4Fu, 1u);
		FillRectangle(0x00u, 2u, 2u, de, 0x0000u);
		hBankVRAM = 0u;
		gb_write8(0xFF4Fu, 0u);
	}
}
/* <<< factory DrawPlayArea_PrizeCards */
/* --- factory _DrawPlayersPrizeAndBenchCards */
/* >>> factory DrawPlayArea_IconWithValue */
void DrawPlayArea_IconWithValue(uint8_t a, uint8_t b, uint16_t *hl)
{
	uint16_t coordinates = *hl;
	uint8_t d = gb_read8(coordinates++);
	uint8_t e = gb_read8(coordinates++);
	*hl = coordinates;
	uint16_t de = (uint16_t)(((uint16_t)d << 8) | e);
	FillRectangle(a, 2u, 2u, de, 0x0102u);

	hBankVRAM = 1u;
	gb_write8(0xFF4Fu, 1u);
	FillRectangle(0x00u, 2u, 2u, de, 0x0000u);
	hBankVRAM = 0u;
	gb_write8(0xFF4Fu, 0u);

	d = (uint8_t)(d + 2u);
	e = (uint8_t)(e + 1u);
	InitTextPrinting(d, e);
	CalculateOnesAndTensDigits(b);
	uint8_t ones = gb_read8(wDecimalDigitsSymbols_ADDR);
	uint8_t tens = gb_read8((uint16_t)(wDecimalDigitsSymbols_ADDR + 1u));

	gb_write8(wDefaultText_ADDR, TX_SYMBOL);
	gb_write8((uint16_t)(wDefaultText_ADDR + 1u), SYM_CROSS);
	gb_write8((uint16_t)(wDefaultText_ADDR + 2u), TX_SYMBOL);
	gb_write8((uint16_t)(wDefaultText_ADDR + 3u), tens);
	gb_write8((uint16_t)(wDefaultText_ADDR + 4u), TX_SYMBOL);
	gb_write8((uint16_t)(wDefaultText_ADDR + 5u), ones);
	gb_write8((uint16_t)(wDefaultText_ADDR + 6u), TX_END);

	uint16_t text_ptr = wDefaultText_ADDR;
	ProcessText(&text_ptr);
}
/* <<< factory DrawPlayArea_IconWithValue */
/* >>> factory SaveDuelStateToSRAM */
void SaveDuelStateToSRAM(void)
{
	BankswitchSRAM(sCurrentDuel_BANK);
	SaveDuelData();
	BankswitchSRAM(0u);
	EnableSRAM();
	uint8_t old = gb_read8(s0a008_ADDR);
	gb_write8(s0a008_ADDR, (uint8_t)(old + 1u));
	DisableSRAM();
	uint16_t buffer = (uint16_t)(0xA000u + (uint16_t)(old & 0x03u) * 0x0400u);
	BankswitchSRAM(3u);

	DuelistVarResult r1 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	CardId turn_card = GetCardIDFromDeckIndex(r1.a);
	uint16_t temp_addr = wTempTurnDuelistCardID_ADDR;
	card_id_write(&temp_addr, turn_card);
	SwapTurn();
	DuelistVarResult r2 = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	CardId non_turn_card = GetCardIDFromDeckIndex(r2.a);
	temp_addr = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_addr, non_turn_card);
	SwapTurn();

	EnableSRAM();
	uint16_t cursor = buffer;
	gb_write8(cursor++, wDuelTurns);
	card_id_write(&cursor, non_turn_card);
	card_id_write(&cursor, turn_card);
	DisableSRAM();

	SaveDuelDataToDE((uint16_t)(buffer + 0x0010u));
	BankswitchSRAM(0u);
}
/* <<< factory SaveDuelStateToSRAM */
/* >>> factory UsePokemonPower */
UsePokemonPowerResult UsePokemonPower(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	ResetAttackAnimationIsPlaying();
	TryExecuteEffectCommandFunctionResult initial = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_2, b, d, e);
	a = initial.a;
	f = initial.f;
	b = initial.b;
	c = initial.c;
	d = initial.d;
	e = initial.e;
	hl = initial.hl;
	if ((f & 0x10u) != 0u) {
		f = DisplayUsePokemonPowerScreen_WaitForInput(hl);
		return (UsePokemonPowerResult){a, f, b, c, d, e, (uint16_t)hl};
	}
	TryExecuteEffectCommandFunctionResult selection = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_REQUIRE_SELECTION, b, d, e);
	a = selection.a;
	f = selection.f;
	b = selection.b;
	c = selection.c;
	d = selection.d;
	e = selection.e;
	hl = selection.hl;
	if ((f & 0x10u) != 0u) {
		f = ReturnCarry(f);
		return (UsePokemonPowerResult){a, f, b, c, d, e, (uint16_t)hl};
	}
	hOppActionTableIndex = OPPACTION_USE_PKMN_POWER;
	hOppActionTableIndex = OPPACTION_EXECUTE_PKMN_POWER_EFFECT;
	TryExecuteEffectCommandFunctionResult before_damage = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_BEFORE_DAMAGE, b, d, e);
	a = before_damage.a;
	f = before_damage.f;
	b = before_damage.b;
	c = before_damage.c;
	d = before_damage.d;
	e = before_damage.e;
	hl = before_damage.hl;
	hOppActionTableIndex = OPPACTION_DUEL_MAIN_SCENE;
	a = OPPACTION_DUEL_MAIN_SCENE;
	return (UsePokemonPowerResult){a, f, b, c, d, e, hl};
}
/* <<< factory UsePokemonPower */
/* >>> factory DrawYourOrOppPlayArea_ActiveCardGfx */
uint16_t DrawYourOrOppPlayArea_ActiveCardGfx(uint16_t de)
{
	uint8_t page = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	uint16_t arena_addr = (uint16_t)(((uint16_t)page << 8) | DUELVARS_ARENA_CARD);
	uint8_t arena_card = gb_read8(arena_addr);
	if (arena_card == 0xFFu)
		return de;

	uint8_t turn = gb_read8(hWhoseTurn_ADDR);
	if (turn != page)
		SwapTurn();
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena_card);
	if (turn != page)
		SwapTurn();

	LoadLoaded1CardGfx((uint16_t)(V0_TILES1 + 0x200u));
	copy_card_palette(2u);
	FlushAllPalettes();
	FillRectangle(0xA0u, 8u, 6u, de, 0x0601u);
	ApplyCardCGBAttributesResult attributes = ApplyCardCGBAttributes(0xA0u, de);
	return attributes.de;
}
/* <<< factory DrawYourOrOppPlayArea_ActiveCardGfx */
/* >>> factory DealConfusionDamageToSelf */
/* duel.asm:1816-1841. Applies confusion self-damage: `a` is the raw damage, and
 * wNoDamageOrEffect plus wTempNonTurnDuelistCardID are saved, overridden (the
 * turn holder becomes its own target so the modifiers resolve against itself) and
 * restored on the way out. The bank1call targets are plain calls here. */
DealConfusionDamageToSelfResult DealConfusionDamageToSelf(uint8_t a, uint8_t f,
	uint8_t d, uint8_t e)
{
	(void)d;
	(void)e;
	gb_write8(wDamage_ADDR, a);
	gb_write8((uint16_t)(wDamage_ADDR + 1u), 0u);
	const uint8_t saved_no_damage = gb_read8(wNoDamageOrEffect_ADDR);
	gb_write8(wNoDamageOrEffect_ADDR, 0u);
	ResetAttackAnimationIsPlaying();
	CardId saved_non_turn = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	uint16_t temp_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, card_id_read_at(wTempTurnDuelistCardID_ADDR));
	/* ApplyDamageModifiers_DamageToSelf builds the modified damage in `de`
	 * (duel.asm:1940 `ld d, [hl]`), and DealAttackDamageSimple reads its damage
	 * from that pair -- so the return value has to be threaded through, not
	 * dropped in favour of the incoming d/e. */
	const uint16_t modified = ApplyDamageModifiers_DamageToSelf();
	const uint8_t c = gb_read8(wDamageEffectiveness_ADDR);
	DuelistVarResult hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	(void)PlayAttackAnimation_DealAttackDamageSimple(hp.a, f, PLAY_AREA_ARENA,
		c, (uint8_t)(modified >> 8), (uint8_t)modified, hp.hl);
	(void)PrintKnockedOutIfHLZero(hp.hl);
	temp_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, saved_non_turn);
	gb_write8(wNoDamageOrEffect_ADDR, saved_no_damage);
	return (DealConfusionDamageToSelfResult){saved_no_damage, f};
}
/* <<< factory DealConfusionDamageToSelf */
/* >>> factory Func_1bb4 */
/* duel.asm:2214-2223. A straight call sequence. Its own distinctive effect is the
 * `xor a` / `ldh [hTempPlayAreaLocation_ff9d], a` write; everything else is the
 * callees running for real.
 *
 * The contract deliberately compares only `a`. Measured 2026-08-26: the reference
 * leaves b=0x00 c=0x00 d=0xD8 f=0x80 here, and NO C caller can reproduce that,
 * because four of the five callees are registered with contracts too thin to carry
 * the registers they clobber (FinishQueuedAnimations, DrawDuelMainScene and
 * DrawDuelHUDs are compare=() returning void; WaitForWideTextBoxInput returns
 * {f} only). That debt is recorded against those callees, not worked around here:
 * widening them is what would let this contract grow. */
Func_1bb4Result Func_1bb4(uint8_t b, uint8_t c, uint16_t de, uint16_t hl)
{
	(void)b;
	(void)c;
	(void)de;
	(void)hl;
	FinishQueuedAnimations();
	DrawDuelMainScene();
	DrawDuelHUDs();
	gb_write8(hTempPlayAreaLocation_ff9d_ADDR, 0u); /* xor a ; PLAY_AREA_ARENA */
	(void)PrintFailedEffectText();
	WaitResult wait = WaitForWideTextBoxInput();
	return (Func_1bb4Result){wait.a};
}
/* <<< factory Func_1bb4 */
/* >>> factory DrawInPlayArea_ActiveCardGfx */
void DrawInPlayArea_ActiveCardGfx(void)
{
	DuelistVarResult result;
	gb_write8(wArenaCardsInPlayArea_ADDR, 0u);
	result = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		gb_write8(wArenaCardsInPlayArea_ADDR, (uint8_t)(gb_read8(wArenaCardsInPlayArea_ADDR) | 0x01u));
		(void)LoadCardDataToBuffer1_FromDeckIndex(result.a);
		LoadLoaded1CardGfx(0x8A00u);
		copy_card_palette(2u);
	}
	result = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
	if (result.a != 0xFFu) {
		gb_write8(wArenaCardsInPlayArea_ADDR, (uint8_t)(gb_read8(wArenaCardsInPlayArea_ADDR) | 0x02u));
		SwapTurn();
		(void)LoadCardDataToBuffer1_FromDeckIndex(result.a);
		LoadLoaded1CardGfx(0x9500u);
		copy_card_palette(5u);
		SwapTurn();
	}
	if (gb_read8(wArenaCardsInPlayArea_ADDR) == 0u)
		return;
	FlushAllPalettes();
	if ((gb_read8(wArenaCardsInPlayArea_ADDR) & 0x01u) != 0u) {
		FillRectangle(0xA0u, 8u, 6u, 0x0609u, 0x0601u);
		(void)ApplyCardCGBAttributes(0xA0u, 0x0609u);
	}
	if ((gb_read8(wArenaCardsInPlayArea_ADDR) & 0x02u) == 0u)
		return;
	SwapTurn();
	FillRectangle(0x50u, 8u, 6u, 0x0602u, 0x0601u);
	(void)ApplyCardCGBAttributes(0x50u, 0x0602u);
	SwapTurn();
}
/* <<< factory DrawInPlayArea_ActiveCardGfx */
/* >>> factory ProcessPlayedPokemonCard */
DuelRoutineResult ProcessPlayedPokemonCard(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t index = hTempCardIndex_ff98;
	ClearChangedTypesIfMuk(index);
	AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(index, FIRST_ATTACK_OR_PKMN_POWER);
	a = copy.a; c = copy.c; f = copy.f; hl = copy.hl; d = (uint8_t)(copy.de >> 8); e = (uint8_t)copy.de;
	DuelRoutineResult updated = UpdateArenaCardIDsAndClearTwoTurnDuelVars(a, f, b, c, d, e, hl);
	a = updated.a; f = updated.f; b = updated.b; c = updated.c; d = updated.d; e = updated.e; hl = updated.hl;
	index = hTempCardIndex_ff98;
	hTempCardIndex_ff9f = index;
	uint16_t card_id = GetCardIDFromDeckIndex(index);
	d = (uint8_t)(card_id >> 8); e = (uint8_t)card_id;
	uint16_t temp_card_id = wTempTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, card_id);
	{
		uint8_t category = wLoadedAttackCategory;
		uint8_t z_bit = (category == POKEMON_POWER) ? 0x80u : 0u;
		uint8_t h_bit = ((category & 0x0Fu) < (POKEMON_POWER & 0x0Fu)) ? 0x20u : 0u;
		uint8_t c_bit = (category < POKEMON_POWER) ? 0x10u : 0u;
		f = (uint8_t)(z_bit | 0x40u | h_bit | c_bit);
		if (category != POKEMON_POWER)
			return (DuelRoutineResult){category, f, b, c, d, e, hl};
	}
	DisplayUsePokemonPowerScreen();
	(void)LoadCardDataToBuffer1_FromDeckIndex(index);
	hl = (uint16_t)(gb_read8(wLoadedCard1Name_ADDR)
			| ((uint16_t)gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)) << 8));
	LoadTxRam2(hl);
	hl = HavePokemonPowerText;
	WaitResult wait = DrawWideTextBox_WaitForInput(hl);
	a = wait.a;
	f = wait.f;
	b = wait.b;
	c = wait.c;
	d = wait.d;
	e = wait.e;
	hl = wait.hl;
	if (card_id_read_at(wLoadedCard1ID_ADDR) != MUK) {
		PkmnPowerIncapableResult incapable = CheckIsIncapableOfUsingPkmnPower(PLAY_AREA_BENCH_1);
		if (incapable.f & 0x10u) {
			a = PLAY_AREA_BENCH_1; f = incapable.f; hl = incapable.hl;
			DisplayUsePokemonPowerScreen();
			hl = UnableToUsePkmnPowerDueToToxicGasText;
			wait = DrawWideTextBox_WaitForInput(hl);
			return (DuelRoutineResult){wait.a, wait.f, wait.b, wait.c, wait.d, wait.e, wait.hl};
		}
	}
	hl = (uint16_t)(gb_read8(wLoadedAttackEffectCommands_ADDR)
			| ((uint16_t)gb_read8((uint16_t)(wLoadedAttackEffectCommands_ADDR + 1u)) << 8));
	EffectCmdLookup command = CheckMatchingCommand(EFFECTCMDTYPE_PKMN_POWER_TRIGGER, hl);
	hl = command.hl;
	if (command.carry) { f |= 0x10u; return (DuelRoutineResult){a, f, b, c, d, e, hl}; }
	DrawDuelMainScene();
	index = hTempCardIndex_ff9f;
	(void)LoadCardDataToBuffer1_FromDeckIndex(index);
	gb_write8(wTxRam2_ADDR, gb_read8(wLoadedCard1Name_ADDR));
	gb_write8((uint16_t)(wTxRam2_ADDR + 1u), gb_read8((uint16_t)(wLoadedCard1Name_ADDR + 1u)));
	gb_write8((uint16_t)(wTxRam2_ADDR + 2u), gb_read8(wLoadedAttackName_ADDR));
	gb_write8((uint16_t)(wTxRam2_ADDR + 3u), gb_read8((uint16_t)(wLoadedAttackName_ADDR + 1u)));
	hl = WillUseThePokemonPowerText;
	wait = DrawWideTextBox_WaitForInput(hl);
	a = wait.a;
	f = wait.f;
	b = wait.b;
	c = wait.c;
	d = wait.d;
	e = wait.e;
	hl = wait.hl;
	ResetAttackAnimationIsPlaying();
	TryExecuteEffectCommandFunctionResult executed = TryExecuteEffectCommandFunction(
		EFFECTCMDTYPE_PKMN_POWER_TRIGGER, wait.b, wait.d, wait.e);
	return (DuelRoutineResult){executed.a, executed.f, executed.b, executed.c, executed.d, executed.e, executed.hl};
}
/* <<< factory ProcessPlayedPokemonCard */
/* >>> factory PlayTrainerCard */
PlayTrainerCardResult PlayTrainerCard(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)c;
	TrainerEffectResult blocked = CheckCantUseTrainerDueToEffect();
	f = blocked.f;
	hl = blocked.hl;
	if ((f & 0x10u) != 0u) {
		WaitResult wait = DrawWideTextBox_WaitForInput(hl);
		f = (uint8_t)(wait.f | 0x10u);
		return (PlayTrainerCardResult){f};
	}
	hl = (uint16_t)(((uint16_t)hWhoseTurn << 8) | (hl & 0x00FFu));
	a = hTempCardIndex_ff98;
	hTempCardIndex_ff9f = a;
	LoadEffectResult loaded = LoadNonPokemonCardEffectCommands();
	a = loaded.a;
	d = (uint8_t)(loaded.de >> 8);
	e = (uint8_t)loaded.de;
	hl = loaded.hl;
	TryExecuteEffectCommandFunctionResult effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_1, b, d, e);
	a = effect.a;
	f = effect.f;
	b = effect.b;
	c = effect.c;
	d = effect.d;
	e = effect.e;
	hl = effect.hl;
	if ((f & 0x10u) != 0u) {
		WaitResult wait = DrawWideTextBox_WaitForInput(hl);
		f = (uint8_t)(wait.f | 0x10u);
		return (PlayTrainerCardResult){f};
	}
	effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_2, b, d, e);
	a = effect.a;
	f = effect.f;
	b = effect.b;
	c = effect.c;
	d = effect.d;
	e = effect.e;
	hl = effect.hl;
	if ((f & 0x10u) != 0u) {
		f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
		return (PlayTrainerCardResult){f};
	}
	hOppActionTableIndex = OPPACTION_PLAY_TRAINER;
	WaitResult used = DisplayUsedTrainerCardDetailScreen();
	a = used.a;
	b = used.b;
	c = used.c;
	d = used.d;
	e = used.e;
	hl = used.hl;
	effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_DISCARD_ENERGY, b, d, e);
	a = effect.a;
	f = effect.f;
	b = effect.b;
	c = effect.c;
	d = effect.d;
	e = effect.e;
	hl = effect.hl;
	effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_REQUIRE_SELECTION, b, d, e);
	a = effect.a;
	f = effect.f;
	b = effect.b;
	c = effect.c;
	d = effect.d;
	e = effect.e;
	hl = effect.hl;
	hOppActionTableIndex = OPPACTION_EXECUTE_TRAINER_EFFECTS;
	effect = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_BEFORE_DAMAGE, b, d, e);
	a = effect.a;
	f = effect.f;
	b = effect.b;
	c = effect.c;
	d = effect.d;
	e = effect.e;
	hl = effect.hl;
	a = hTempCardIndex_ff9f;
	MoveCardResult moved = MoveHandCardToDiscardPile(a);
	a = moved.a;
	f = moved.f;
	hl = moved.hl;
	f = (uint8_t)(a == 0u ? 0x80u : 0x00u);
	return (PlayTrainerCardResult){f};
}
/* <<< factory PlayTrainerCard */
/* >>> factory DealDamageToPlayAreaPokemon */
DealDamageToPlayAreaPokemonResult DealDamageToPlayAreaPokemon(uint8_t b, uint16_t de, uint16_t hl)
{
	wTempPlayAreaLocation_cceb = b;
	if (b == 0u && wNoDamageOrEffect != 0u)
		return (DealDamageToPlayAreaPokemonResult){wNoDamageOrEffect, 0x00u};
	{
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + b));
		hl = card.hl;
		CardId target_id = GetCardIDFromDeckIndex(card.a);
		uint16_t temp_card_id = wTempNonTurnDuelistCardID_ADDR;
		card_id_write(&temp_card_id, target_id);
	}
	wNoDamageOrEffect = 0u;
	if (b == 0u && wIsDamageToSelf == 0u)
		SwapTurn();
	if (b == 0u) {
		PowerModifierResult plus = ApplyAttachedPlusPower(CARD_LOCATION_ARENA, de);
		de = plus.de;
		if (wIsDamageToSelf == 0u)
			SwapTurn();
	} else {
		PowerModifierResult defender = ApplyAttachedDefender((uint8_t)(b | CARD_LOCATION_PLAY_AREA), de);
		de = defender.de;
	}
	if (b == 0u) {
		NoDamageOrEffectResult no_damage = HandleNoDamageOrEffectSubstatus((uint8_t)(de >> 8), (uint8_t)de, hl);
		hl = no_damage.hl;
		de = HandleDamageReduction(de);
	}
	if (de & 0x8000u)
		de = 0u;
	{
		HandleDamageReductionOrNoDamageFromPkmnPowerEffectsResult reduced = HandleDamageReductionOrNoDamageFromPkmnPowerEffects(de, hl);
		de = reduced.de;
		hl = reduced.hl;
	}
	if (b == 0u) {
		uint16_t dealt = (uint16_t)(wDealtDamage | ((uint16_t)gb_read8((uint16_t)(wDealtDamage_ADDR + 1u)) << 8));
		dealt = (uint16_t)(dealt + de);
		gb_write8(wDealtDamage_ADDR, (uint8_t)dealt);
		gb_write8((uint16_t)(wDealtDamage_ADDR + 1u), (uint8_t)(dealt >> 8));
	}
	{
		DuelistVarResult hp = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + b));
		PlayAttackAnimation_DealAttackDamageSimpleResult animation = PlayAttackAnimation_DealAttackDamageSimple(hp.a, 0u, b, 0u, (uint8_t)(de >> 8), (uint8_t)de, hp.hl);
		if (animation.a != 0u)
			(void)PrintKnockedOutIfHLZero(hp.hl);
	}
	{
		StrikesBackResult strikes = HandleStrikesBack_AgainstDamagingAttack(de, hl);
		return (DealDamageToPlayAreaPokemonResult){strikes.a, strikes.f};
	}
}
/* <<< factory DealDamageToPlayAreaPokemon */
/* >>> factory Func_82b6 */
/* duel.asm:487-501. PrizeCardsCoordinateData_YourOrOppPlayArea is bank-2 ROM
 * data at $44B4/$44C0. DrawPlayArea_PrizeCards intentionally reads coordinates
 * through gb_read8, whose C probe path cannot represent a caller-owned banked
 * ROM pointer. Copy the selected 12-byte table to WRAM exactly like the landed
 * DrawPlayAreaToPlacePrizeCards is another caller of the same callee. */
void Func_82b6(void)
{
	uint8_t duelist = gb_read8(wCheckMenuPlayAreaWhichDuelist_ADDR);
	uint8_t layout = gb_read8(wCheckMenuPlayAreaWhichLayout_ADDR);

	DrawPlayArea_PrizeCards(duelist == layout ? PRIZE_COORDS_YOUR_OR_OPP_PLAYER
	                                          : PRIZE_COORDS_YOUR_OR_OPP_OPPONENT);
}
/* <<< factory Func_82b6 */
/* >>> factory DuelCheckMenu_InPlayArea */
/* menus/duel.asm:36-40 */
void DuelCheckMenu_InPlayArea(void)
{
	wInPlayAreaFromSelectButton = 0u;
	uint8_t saved_bank = hBankROM;
	BankswitchROM(OpenInPlayAreaScreen_BANK);
	OpenInPlayAreaScreen();
	BankswitchROM(saved_bank);
}
/* <<< factory DuelCheckMenu_InPlayArea */
/* >>> factory HandleAfterDamageEffects */
/* duel.asm:1596-1607. Runs the attack's after-damage effect command with the
 * defending card ID restored around it, then the whole post-attack chain down
 * to the knockout/prize resolution; `or a` leaves carry clear. */
HandleAfterDamageEffectsResult HandleAfterDamageEffects(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	(void)a; (void)f;
	CardId defending = card_id_read_at(wTempNonTurnDuelistCardID_ADDR);
	TryExecuteEffectCommandFunctionResult after = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_AFTER_DAMAGE, b, d, e);
	b = after.b; c = after.c; d = after.d; e = after.e; hl = after.hl;
	uint16_t temp_card_id = wTempNonTurnDuelistCardID_ADDR;
	card_id_write(&temp_card_id, defending);
	(void)HandleStrikesBack_AgainstResidualAttack();
	(void)ApplyStatusConditionQueue();
	(void)Func_1bb4(b, c, (uint16_t)(((uint16_t)d << 8) | e), hl);
	UpdateArenaCardLastTurnDamage();
	HandleBetweenTurnKnockOutsResult knockouts = HandleDestinyBondAndBetweenTurnKnockOuts();
	return (HandleAfterDamageEffectsResult){knockouts.a, (uint8_t)(knockouts.a == 0u ? 0x80u : 0x00u)};
}
/* <<< factory HandleAfterDamageEffects */
/* --- factory Func_17ed */
/* >>> factory UseAttackOrPokemonPower */
DuelRoutineResult UseAttackOrPokemonPower(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	a = wSelectedAttack;
	wPlayerAttackingAttackIndex = a;
	a = hTempCardIndex_ff9f;
	wPlayerAttackingCardIndex = a;
	CardId attacking_card = card_id_read_at(wTempCardID_ccc2_ADDR);
	uint16_t attacking_addr = wPlayerAttackingCardID_ADDR;
	card_id_write(&attacking_addr, attacking_card);
	a = wLoadedAttackCategory;
	if (a == POKEMON_POWER) {
		UsePokemonPowerResult power = UsePokemonPower(a, f, b, c, d, e, hl);
		return (DuelRoutineResult){power.a, power.f, power.b, power.c, power.d, power.e, power.hl};
	}
	DuelRoutineResult updated = UpdateArenaCardIDsAndClearTwoTurnDuelVars(a, f, b, c, d, e, hl);
	a = updated.a; f = updated.f; b = updated.b; c = updated.c; d = updated.d; e = updated.e; hl = updated.hl;
	TryExecuteEffectCommandFunctionResult initial = TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_1, b, d, e);
	a = initial.a; f = initial.f; b = initial.b; c = initial.c; d = initial.d; e = initial.e; hl = initial.hl;
	if ((f & 0x10u) != 0u)
		return (DuelRoutineResult){a, DrawWideTextBox_WaitForInput_ReturnCarry(hl), b, c, d, e, hl};
	SandAttackCheckResult sand = CheckSandAttackOrSmokescreenSubstatus((uint16_t)(((uint16_t)d << 8) | e));
	d = (uint8_t)(sand.de >> 8); e = (uint8_t)sand.de; hl = sand.hl;
	if ((sand.f & 0x10u) != 0u) {
		HandleSandAttackOrSmokescreenSubstatusResult handled = HandleSandAttackOrSmokescreenSubstatus(sand.de, sand.hl);
		a = handled.a; f = handled.f; d = (uint8_t)(handled.de >> 8); e = (uint8_t)handled.de; hl = handled.hl;
		if ((f & 0x10u) != 0u)
			return ClearNonTurnTemporaryDuelvars_ResetCarry(a, f, b, c, d, e, hl);
	}
	a = EFFECTCMDTYPE_INITIAL_EFFECT_2;
	TryExecuteEffectCommandFunctionResult second = TryExecuteEffectCommandFunction(a, b, d, e);
	a = second.a; f = second.f; b = second.b; c = second.c; d = second.d; e = second.e; hl = second.hl;
	if ((f & 0x10u) != 0u)
		return (DuelRoutineResult){a, ReturnCarry(f), b, c, d, e, hl};
	hOppActionTableIndex = OPPACTION_USE_ATTACK;
	a = EFFECTCMDTYPE_DISCARD_ENERGY;
	TryExecuteEffectCommandFunctionResult discard = TryExecuteEffectCommandFunction(a, b, d, e);
	a = discard.a; f = discard.f; b = discard.b; c = discard.c; d = discard.d; e = discard.e; hl = discard.hl;
	CheckSelfConfusionDamageResult confusion = CheckSelfConfusionDamage();
	a = confusion.a; f = confusion.f; hl = confusion.hl;
	if ((f & 0x10u) != 0u) {
		HandleConfusionDamageToSelfResult handled = HandleConfusionDamageToSelf();
		return (DuelRoutineResult){handled.a, handled.f, b, c, d, e, hl};
	}
	PrintPokemonsAttackTextResult printed = DrawDuelMainScene_PrintPokemonsAttackText();
	b = printed.b; c = printed.c; d = printed.d; e = printed.e; hl = printed.hl;
	WaitResult waited = WaitForWideTextBoxInput();
	a = waited.a; f = waited.f; b = waited.b; c = waited.c;
	d = waited.d; e = waited.e; hl = waited.hl;
	a = EFFECTCMDTYPE_REQUIRE_SELECTION;
	TryExecuteEffectCommandFunctionResult selection = TryExecuteEffectCommandFunction(a, b, d, e);
	a = selection.a; f = selection.f; b = selection.b; c = selection.c; d = selection.d; e = selection.e; hl = selection.hl;
	hOppActionTableIndex = OPPACTION_ATTACK_ANIM_AND_DAMAGE;
	HandleAfterDamageEffectsResult tail = PlayAttackAnimation_DealAttackDamage(OPPACTION_ATTACK_ANIM_AND_DAMAGE, f, b, c, d, e, hl);
	return (DuelRoutineResult){tail.a, tail.f, b, c, d, e, hl};
}
/* <<< factory UseAttackOrPokemonPower */
/* === factory GetCardIDFromDeckIndex */
/* === factory HandleCheckMenuInput_YourOrOppPlayArea */
/* === factory MoveCardToDiscardPileIfInPlayArea */
/* === factory YourOrOppPlayAreaScreen_HandleInput */
