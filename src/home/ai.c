/* >>> part includes */
#include "home/ai.h"

#include "generated/constants.h"
#include "generated/rom.h"
#include "generated/wram.h"
#include "home/duel.h"
#include "home/load_deck.h"
#include "mem.h"
#include <stdio.h>
#include <stdlib.h>
/* <<< part includes */
/* >>> part includes_2 */
#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/init.h"
#include "home/overworld.h"
#include "home/retreat.h"
#include "home/sams_practice.h"
#include "home/legendary_ronald.h"
#include "home/boss_deck_set_up.h"
#include "home/legendary_dragonite.h"
#include "home/legendary_articuno.h"
#include "home/legendary_zapdos.h"
#include "home/legendary_moltres.h"
#include "home/general_no_retreat.h"
#include "home/general.h"
#include "mem.h"
/* <<< part includes_2 */

/* >>> part BANK_DECK_AI_POINTER_TABLE */
#define BANK_DECK_AI_POINTER_TABLE DeckAIPointerTable_BANK
/* <<< part BANK_DECK_AI_POINTER_TABLE */
/* >>> part DECK_AI_POINTER_TABLE_ADDR */
#define DECK_AI_POINTER_TABLE_ADDR DeckAIPointerTable_ADDR
/* <<< part DECK_AI_POINTER_TABLE_ADDR */
/* >>> part AI_ACTION_TABLE_SAM_PRACTICE_ADDR */
#define AI_ACTION_TABLE_SAM_PRACTICE_ADDR AIActionTable_SamPractice_ADDR
/* <<< part AI_ACTION_TABLE_SAM_PRACTICE_ADDR */




/* >>> part DUELVARS_DUELIST_TYPE */
#define DUELVARS_DUELIST_TYPE 0xF1u
/* <<< part DUELVARS_DUELIST_TYPE */

/* >>> factory LoadOpponentDeck */
/* ai.asm:1-46. Sam paths (deck id 0 or 2) force PRACTICE_PLAYER_DECK onto the
 * OTHER duelist (swap in, load, swap back) and reseed the RNG to $57/$57/$57;
 * every path then loads the (possibly Sam-forced) deck for the current turn
 * holder and clamps wOpponentDeckID to PRACTICE_PLAYER_DECK_ID if it is past
 * NUM_DECK_IDS. Exit a/hl are the final duelist-type write, the only
 * deterministic register outputs -- everything else is LoadDeck/SwapTurn
 * clobber the asm never saves. */
DeckLoadResult LoadOpponentDeck(void)
{
	wIsPracticeDuel = 0;
	uint8_t deck_id = wOpponentDeckID;
	uint8_t load_arg;

	if (deck_id == SAMS_NORMAL_DECK_ID || deck_id == SAMS_PRACTICE_DECK_ID) {
		if (deck_id == SAMS_PRACTICE_DECK_ID)
			wIsPracticeDuel = 1;
		wOpponentDeckID = 0;
		SwapTurn();
		(void)LoadDeck(PRACTICE_PLAYER_DECK);
		SwapTurn();
		wRNG1 = 0x57;
		wRNG2 = 0x57;
		wRNGCounter = 0x57;
		load_arg = 2;
	} else {
		load_arg = (uint8_t)(deck_id + 2u);
	}

	(void)LoadDeck(load_arg);
	if (wOpponentDeckID >= NUM_DECK_IDS + 1u)
		wOpponentDeckID = PRACTICE_PLAYER_DECK_ID;

	DuelistVarResult dv = GetTurnDuelistVariable(DUELVARS_DUELIST_TYPE);
	uint8_t v = (uint8_t)(wOpponentDeckID | DUELIST_TYPE_AI_OPP);
	gb_write8(dv.hl, v);
	return (DeckLoadResult){v, dv.hl};
}
/* <<< factory LoadOpponentDeck */

/* >>> factory AIDoAction */
/* ai.asm:76-107 with the deck tables of engine/duel/ai/decks. Each deck
 * AI is a six-entry pointer table (deck_ai.asm:36-52): [1] do_turn,
 * [2] start_duel, [3] forced_switch, [4] ko_switch, [5] take_prize; entry 0
 * is the AI's deck data. Every deck picks its prizes with AIPickPrizeCards
 * and switches with AIDecideBenchPokemonToSwitchTo (Sam scripts both for his
 * first seven turns); the boss decks' start_duel stores six card-list
 * pointers before the shared setup; `lists` are those ROM labels, in the
 * order the deck writes them. */
typedef void (*DeckTurn)(void);

typedef struct {
	uint16_t table;
	DeckTurn do_turn;      /* NULL: AIMainTurnLogic */
	uint16_t lists[6];
} DeckAI;

static void turn_general_no_retreat(void) { (void)AIDoTurn_GeneralNoRetreat(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_moltres(void) { (void)AIDoTurn_LegendaryMoltres(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_zapdos(void) { (void)AIDoTurn_LegendaryZapdos(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_articuno(void) { (void)AIDoTurn_LegendaryArticuno(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_dragonite(void) { (void)AIDoTurn_LegendaryDragonite(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_ronald(void) { (void)AIDoTurn_LegendaryRonald(0u, 0u, 0u, 0u, 0u, 0u, 0u); }

static const DeckAI deck_ais[] = {
	{AIActionTable_GeneralDecks_ADDR, NULL, {0}}, /* GeneralDecks */
	{AIActionTable_SamPractice_ADDR, NULL, {0}}, /* SamPractice, scripted below */
	{AIActionTable_GeneralNoRetreat_ADDR, turn_general_no_retreat, {0}}, /* GeneralNoRetreat */
	{AIActionTable_LegendaryMoltres_ADDR, turn_legendary_moltres, {AIActionTable_LegendaryMoltres__list_prize_ADDR, AIActionTable_LegendaryMoltres__list_arena_ADDR, AIActionTable_LegendaryMoltres__list_bench_ADDR, AIActionTable_LegendaryMoltres__list_play_hand_ADDR, AIActionTable_LegendaryMoltres__list_retreat_ADDR, AIActionTable_LegendaryMoltres__list_energy_ADDR}},
	{AIActionTable_LegendaryZapdos_ADDR, turn_legendary_zapdos, {AIActionTable_LegendaryZapdos__list_prize_ADDR, AIActionTable_LegendaryZapdos__list_arena_ADDR, AIActionTable_LegendaryZapdos__list_bench_ADDR, AIActionTable_LegendaryZapdos__list_bench_ADDR, 0u, AIActionTable_LegendaryZapdos__list_energy_ADDR}},
	{AIActionTable_LegendaryArticuno_ADDR, turn_legendary_articuno, {AIActionTable_LegendaryArticuno__list_prize_ADDR, AIActionTable_LegendaryArticuno__list_arena_ADDR, AIActionTable_LegendaryArticuno__list_bench_ADDR, AIActionTable_LegendaryArticuno__list_bench_ADDR, 0u, AIActionTable_LegendaryArticuno__list_energy_ADDR}},
	{AIActionTable_LegendaryDragonite_ADDR, turn_legendary_dragonite, {AIActionTable_LegendaryDragonite__list_prize_ADDR, AIActionTable_LegendaryDragonite__list_arena_ADDR, AIActionTable_LegendaryDragonite__list_bench_ADDR, AIActionTable_LegendaryDragonite__list_bench_ADDR, 0u, AIActionTable_LegendaryDragonite__list_energy_ADDR}},
	{AIActionTable_FirstStrike_ADDR, NULL, {AIActionTable_FirstStrike__list_prize_ADDR, AIActionTable_FirstStrike__list_arena_ADDR, AIActionTable_FirstStrike__list_bench_ADDR, AIActionTable_FirstStrike__list_bench_ADDR, 0u, AIActionTable_FirstStrike__list_energy_ADDR}}, /* FirstStrike */
	{AIActionTable_RockCrusher_ADDR, NULL, {AIActionTable_RockCrusher__list_prize_ADDR, AIActionTable_RockCrusher__list_arena_ADDR, AIActionTable_RockCrusher__list_bench_ADDR, AIActionTable_RockCrusher__list_bench_ADDR, 0u, AIActionTable_RockCrusher__list_energy_ADDR}}, /* RockCrusher */
	{AIActionTable_GoGoRainDance_ADDR, NULL, {AIActionTable_GoGoRainDance__list_prize_ADDR, AIActionTable_GoGoRainDance__list_arena_ADDR, AIActionTable_GoGoRainDance__list_bench_ADDR, AIActionTable_GoGoRainDance__list_bench_ADDR, 0u, AIActionTable_GoGoRainDance__list_energy_ADDR}}, /* GoGoRainDance */
	{AIActionTable_ZappingSelfdestruct_ADDR, NULL, {AIActionTable_ZappingSelfdestruct__list_prize_ADDR, AIActionTable_ZappingSelfdestruct__list_arena_ADDR, AIActionTable_ZappingSelfdestruct__list_bench_ADDR, AIActionTable_ZappingSelfdestruct__list_bench_ADDR, 0u, AIActionTable_ZappingSelfdestruct__list_energy_ADDR}}, /* ZappingSelfdestruct */
	{AIActionTable_FlowerPower_ADDR, NULL, {AIActionTable_FlowerPower__list_prize_ADDR, AIActionTable_FlowerPower__list_arena_ADDR, AIActionTable_FlowerPower__list_bench_ADDR, AIActionTable_FlowerPower__list_bench_ADDR, 0u, AIActionTable_FlowerPower__list_energy_ADDR}}, /* FlowerPower */
	{AIActionTable_StrangePsyshock_ADDR, NULL, {AIActionTable_StrangePsyshock__list_prize_ADDR, AIActionTable_StrangePsyshock__list_arena_ADDR, AIActionTable_StrangePsyshock__list_bench_ADDR, AIActionTable_StrangePsyshock__list_bench_ADDR, 0u, AIActionTable_StrangePsyshock__list_energy_ADDR}}, /* StrangePsyshock */
	{AIActionTable_WondersOfScience_ADDR, NULL, {AIActionTable_WondersOfScience__list_prize_ADDR, AIActionTable_WondersOfScience__list_arena_ADDR, AIActionTable_WondersOfScience__list_bench_ADDR, AIActionTable_WondersOfScience__list_bench_ADDR, 0u, AIActionTable_WondersOfScience__list_energy_ADDR}}, /* WondersOfScience */
	{AIActionTable_FireCharge_ADDR, NULL, {AIActionTable_FireCharge__list_prize_ADDR, AIActionTable_FireCharge__list_arena_ADDR, AIActionTable_FireCharge__list_bench_ADDR, AIActionTable_FireCharge__list_bench_ADDR, 0u, AIActionTable_FireCharge__list_energy_ADDR}}, /* FireCharge */
	{AIActionTable_ImRonald_ADDR, NULL, {AIActionTable_ImRonald__list_prize_ADDR, AIActionTable_ImRonald__list_arena_ADDR, AIActionTable_ImRonald__list_bench_ADDR, AIActionTable_ImRonald__list_bench_ADDR, 0u, AIActionTable_ImRonald__list_energy_ADDR}}, /* ImRonald */
	{AIActionTable_PowerfulRonald_ADDR, NULL, {AIActionTable_PowerfulRonald__list_prize_ADDR, AIActionTable_PowerfulRonald__list_arena_ADDR, AIActionTable_PowerfulRonald__list_bench_ADDR, AIActionTable_PowerfulRonald__list_bench_ADDR, 0u, AIActionTable_PowerfulRonald__list_energy_ADDR}}, /* PowerfulRonald */
	{AIActionTable_InvincibleRonald_ADDR, NULL, {AIActionTable_InvincibleRonald__list_prize_ADDR, AIActionTable_InvincibleRonald__list_arena_ADDR, AIActionTable_InvincibleRonald__list_bench_ADDR, AIActionTable_InvincibleRonald__list_bench_ADDR, 0u, AIActionTable_InvincibleRonald__list_energy_ADDR}}, /* InvincibleRonald */
	{AIActionTable_LegendaryRonald_ADDR, turn_legendary_ronald, {AIActionTable_LegendaryRonald__list_prize_ADDR, AIActionTable_LegendaryRonald__list_arena_ADDR, AIActionTable_LegendaryRonald__list_bench_ADDR, AIActionTable_LegendaryRonald__list_play_hand_ADDR, 0u, AIActionTable_LegendaryRonald__list_energy_ADDR}},
};

static const DeckAI *deck_ai_for(uint16_t table)
{
	for (size_t i = 0; i < sizeof deck_ais / sizeof deck_ais[0]; i++)
		if (deck_ais[i].table == table)
			return &deck_ais[i];
	fprintf(stderr, "DeckAIPointerTable entry %04X is not a known deck AI\n", table);
	abort();
}

static void store_deck_list_pointers(const uint16_t *lists)
{
	static const uint16_t slots[6] = {
		wAICardListAvoidPrize_ADDR, wAICardListArenaPriority_ADDR, wAICardListBenchPriority_ADDR,
		wAICardListPlayFromHandPriority_ADDR, wAICardListRetreatBonus_ADDR, wAICardListEnergyBonus_ADDR,
	};
	for (size_t i = 0; i < 6; i++) {
		if (lists[i] == 0u)
			continue;
		gb_write8(slots[i], (uint8_t)lists[i]);
		gb_write8((uint16_t)(slots[i] + 1u), (uint8_t)(lists[i] >> 8));
	}
}

static int sam_scripted(void)
{
	return (IsAIPracticeScriptedTurn(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u;
}

uint8_t AIDoAction(uint8_t a)
{
	uint8_t action = a;
	uint8_t saved_bank = hBankROM;

	BankswitchROM(BANK_DECK_AI_POINTER_TABLE);
	const uint8_t *deck_entry = rom_ptr(
		BANK_DECK_AI_POINTER_TABLE,
		(uint16_t)(DECK_AI_POINTER_TABLE_ADDR +
			(uint16_t)wOpponentDeckID * 2u));
	uint16_t action_table = (uint16_t)(deck_entry[0] |
		((uint16_t)deck_entry[1] << 8));

	if (action == 0u) {
		const uint8_t *deck_data = rom_ptr(BANK_DECK_AI_POINTER_TABLE, action_table);
		uint16_t deck_pointer = (uint16_t)(deck_data[0] |
			((uint16_t)deck_data[1] << 8));
		CardListResult copied = CopyDeckData(deck_pointer);
		action = copied.a;
	} else {
		const DeckAI *deck = deck_ai_for(action_table);
		int sam = action_table == AI_ACTION_TABLE_SAM_PRACTICE_ADDR;
		switch (action) {
		case AIACTION_DO_TURN:
			if (sam && sam_scripted())
				(void)AIPerformScriptedTurn(0u, 0u, 0u, 0u, 0u, 0u, 0u);
			else if (deck->do_turn)
				deck->do_turn();
			else
				(void)AIMainTurnLogic(0u, 0u, 0u, 0u, 0u, 0u, 0u);
			break;
		case AIACTION_START_DUEL:
			if (sam) {
				action = SetSamsStartingPlayArea(0u, 0u, 0u, 0u, 0u, 0u, 0u).a;
			} else if (deck->lists[0] == 0u) {
				InitAIDuelVars();
				action = AIPlayInitialBasicCards().a;
			} else {
				InitAIDuelVars();
				store_deck_list_pointers(deck->lists);
				SetUpBossStartingHandAndDeck();
				TrySetUpBossStartingPlayAreaResult boss = TrySetUpBossStartingPlayArea();
				action = boss.a;
				if ((boss.f & 0x10u) != 0u)
					action = AIPlayInitialBasicCards().a;
			}
			break;
		case AIACTION_FORCED_SWITCH:
			if (sam && sam_scripted())
				action = PickRandomBenchPokemon();
			else
				action = AIDecideBenchPokemonToSwitchTo(0u).a;
			break;
		case AIACTION_KO_SWITCH:
			if (sam && sam_scripted()) {
				GetPlayAreaLocationOfRaticateOrRattata();
				action = hTempPlayAreaLocation_ff9d;
			} else {
				action = AIDecideBenchPokemonToSwitchTo(0u).a;
			}
			break;
		case AIACTION_TAKE_PRIZE:
			action = AIPickPrizeCards();
			break;
		default:
			fprintf(stderr, "AIDoAction: unknown action %u\n", action);
			abort();
		}
	}

	BankswitchROM(saved_bank);
	return action;
}
/* <<< factory AIDoAction */

/* >>> factory AIDoAction_ForcedSwitch */
uint8_t AIDoAction_ForcedSwitch(void)
{
	uint8_t result = AIDoAction(0x03u);
	hTempPlayAreaLocation_ff9d = result;
	return result;
}
/* <<< factory AIDoAction_ForcedSwitch */

/* >>> factory AIDoAction_KOSwitch */
uint8_t AIDoAction_KOSwitch(void)
{
	uint8_t result = AIDoAction(AIACTION_KO_SWITCH);
	hTemp_ffa0 = result;
	return result;
}
/* <<< factory AIDoAction_KOSwitch */

/* >>> factory AIDoAction_StartDuel */
uint8_t AIDoAction_StartDuel(void)
{
	return AIDoAction(0x02u);
}
/* <<< factory AIDoAction_StartDuel */

/* >>> factory AIDoAction_TakePrize */
uint8_t AIDoAction_TakePrize(void)
{
	return AIDoAction(AIACTION_TAKE_PRIZE);
}
/* <<< factory AIDoAction_TakePrize */

/* >>> factory AIDoAction_Turn */
uint8_t AIDoAction_Turn(void)
{
	return AIDoAction(AIACTION_DO_TURN);
}
/* <<< factory AIDoAction_Turn */
