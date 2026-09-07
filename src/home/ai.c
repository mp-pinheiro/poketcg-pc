#include "home/ai.h"

#include "generated/wram.h"
#include "home/duel.h"
#include "home/load_deck.h"
#include "mem.h"
#include <stdio.h>
#include <stdlib.h>
/* >>> factory statics */
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

#define BANK_DECK_AI_POINTER_TABLE 5u
#define DECK_AI_POINTER_TABLE_ADDR 0x4000u
#define AI_ACTION_TABLE_SAM_PRACTICE_ADDR 0x47BDu

#define AIACTION_START_DUEL 0x02u
#define AIACTION_FORCED_SWITCH 0x03u
#define AIACTION_KO_SWITCH 0x04u

#define AIACTION_TAKE_PRIZE 0x05u

#define AIACTION_DO_TURN 0x01u
/* <<< factory statics */

#define SAMS_PRACTICE_DECK_ID 0u
#define SAMS_NORMAL_DECK_ID 2u
#define PRACTICE_PLAYER_DECK_ID 1u
#define PRACTICE_PLAYER_DECK 3u
#define NUM_DECK_IDS 53u
#define DUELIST_TYPE_AI_OPP 0x80u
#define DUELVARS_DUELIST_TYPE 0xF1u

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
	uint16_t lists[6];     /* prize, arena, bench, play_hand, retreat, energy; all zero for the general start_duel */
} DeckAI;

static void turn_general_no_retreat(void) { (void)AIDoTurn_GeneralNoRetreat(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_moltres(void) { (void)AIDoTurn_LegendaryMoltres(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_zapdos(void) { (void)AIDoTurn_LegendaryZapdos(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_articuno(void) { (void)AIDoTurn_LegendaryArticuno(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_dragonite(void) { (void)AIDoTurn_LegendaryDragonite(0u, 0u, 0u, 0u, 0u, 0u, 0u); }
static void turn_legendary_ronald(void) { (void)AIDoTurn_LegendaryRonald(0u, 0u, 0u, 0u, 0u, 0u, 0u); }

static const DeckAI deck_ais[] = {
	{0x4668u, NULL, {0}},                                                                   /* GeneralDecks */
	{0x47BDu, NULL, {0}},                                                                   /* SamPractice, scripted below */
	{0x48DCu, turn_general_no_retreat, {0}},                                                /* GeneralNoRetreat */
	{0x49E8u, turn_legendary_moltres, {0x4A47u, 0x4A15u, 0x4A1Cu, 0x4A22u, 0x4A29u, 0x4A2Eu}},
	{0x4B0Fu, turn_legendary_zapdos, {0x4B69u, 0x4B3Cu, 0x4B43u, 0x4B43u, 0x4B49u, 0x4B50u}},
	{0x4C0Bu, turn_legendary_articuno, {0x4C60u, 0x4C38u, 0x4C3Fu, 0x4C3Fu, 0x4C45u, 0x4C4Au}},
	{0x4D60u, turn_legendary_dragonite, {0x4DBDu, 0x4D8Du, 0x4D93u, 0x4D93u, 0x4D99u, 0x4D9Eu}},
	{0x4E89u, NULL, {0x4EDDu, 0x4EB6u, 0x4EBBu, 0x4EBBu, 0x4EC0u, 0x4EC7u}},               /* FirstStrike */
	{0x4F0Eu, NULL, {0x4F5Eu, 0x4F3Bu, 0x4F40u, 0x4F40u, 0x4F45u, 0x4F48u}},               /* RockCrusher */
	{0x4F8Fu, NULL, {0x4FE6u, 0x4FBCu, 0x4FC1u, 0x4FC1u, 0x4FC6u, 0x4FCDu}},               /* GoGoRainDance */
	{0x5019u, NULL, {0x506Bu, 0x5046u, 0x504Cu, 0x504Cu, 0x5052u, 0x5055u}},               /* ZappingSelfdestruct */
	{0x509Bu, NULL, {0x50F2u, 0x50C8u, 0x50CCu, 0x50CCu, 0x50D0u, 0x50D9u}},               /* FlowerPower */
	{0x5122u, NULL, {0x517Au, 0x514Fu, 0x5155u, 0x5155u, 0x515Bu, 0x5164u}},               /* StrangePsyshock */
	{0x51ADu, NULL, {0x5202u, 0x51DAu, 0x51E1u, 0x51E1u, 0x51E8u, 0x51E9u}},               /* WondersOfScience */
	{0x5232u, NULL, {0x528Du, 0x525Fu, 0x5266u, 0x5266u, 0x526Du, 0x5274u}},               /* FireCharge */
	{0x52BDu, NULL, {0x531Bu, 0x52EAu, 0x52F1u, 0x52F1u, 0x52F8u, 0x52F9u}},               /* ImRonald */
	{0x534Bu, NULL, {0x53B7u, 0x5378u, 0x5383u, 0x5383u, 0x538Eu, 0x5395u}},               /* PowerfulRonald */
	{0x53E8u, NULL, {0x543Fu, 0x5415u, 0x541Cu, 0x541Cu, 0x5423u, 0x5426u}},               /* InvincibleRonald */
	{0x546Fu, turn_legendary_ronald, {0x54D3u, 0x549Cu, 0x54A3u, 0x54A7u, 0x54AEu, 0x54B1u}},
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
				action = AIDecideBenchPokemonToSwitchTo().a;
			break;
		case AIACTION_KO_SWITCH:
			if (sam && sam_scripted()) {
				GetPlayAreaLocationOfRaticateOrRattata();
				action = hTempPlayAreaLocation_ff9d;
			} else {
				action = AIDecideBenchPokemonToSwitchTo().a;
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
