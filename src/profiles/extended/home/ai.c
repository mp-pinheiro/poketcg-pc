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
	{AIActionTable_LegendaryZapdos_ADDR, turn_legendary_zapdos, {AIActionTable_LegendaryZapdos__list_prize_ADDR, AIActionTable_LegendaryZapdos__list_arena_ADDR, AIActionTable_LegendaryZapdos__list_bench_ADDR, AIActionTable_LegendaryZapdos__list_bench_ADDR, AIActionTable_LegendaryZapdos__list_retreat_ADDR, AIActionTable_LegendaryZapdos__list_energy_ADDR}},
	{AIActionTable_LegendaryArticuno_ADDR, turn_legendary_articuno, {AIActionTable_LegendaryArticuno__list_prize_ADDR, AIActionTable_LegendaryArticuno__list_arena_ADDR, AIActionTable_LegendaryArticuno__list_bench_ADDR, AIActionTable_LegendaryArticuno__list_bench_ADDR, AIActionTable_LegendaryArticuno__list_retreat_ADDR, AIActionTable_LegendaryArticuno__list_energy_ADDR}},
	{AIActionTable_LegendaryDragonite_ADDR, turn_legendary_dragonite, {AIActionTable_LegendaryDragonite__list_prize_ADDR, AIActionTable_LegendaryDragonite__list_arena_ADDR, AIActionTable_LegendaryDragonite__list_bench_ADDR, AIActionTable_LegendaryDragonite__list_bench_ADDR, AIActionTable_LegendaryDragonite__list_retreat_ADDR, AIActionTable_LegendaryDragonite__list_energy_ADDR}},
	{AIActionTable_FirstStrike_ADDR, NULL, {AIActionTable_FirstStrike__list_prize_ADDR, AIActionTable_FirstStrike__list_arena_ADDR, AIActionTable_FirstStrike__list_bench_ADDR, AIActionTable_FirstStrike__list_bench_ADDR, AIActionTable_FirstStrike__list_retreat_ADDR, AIActionTable_FirstStrike__list_energy_ADDR}}, /* FirstStrike */
	{AIActionTable_RockCrusher_ADDR, NULL, {AIActionTable_RockCrusher__list_prize_ADDR, AIActionTable_RockCrusher__list_arena_ADDR, AIActionTable_RockCrusher__list_bench_ADDR, AIActionTable_RockCrusher__list_bench_ADDR, AIActionTable_RockCrusher__list_retreat_ADDR, AIActionTable_RockCrusher__list_energy_ADDR}}, /* RockCrusher */
	{AIActionTable_GoGoRainDance_ADDR, NULL, {AIActionTable_GoGoRainDance__list_prize_ADDR, AIActionTable_GoGoRainDance__list_arena_ADDR, AIActionTable_GoGoRainDance__list_bench_ADDR, AIActionTable_GoGoRainDance__list_bench_ADDR, AIActionTable_GoGoRainDance__list_retreat_ADDR, AIActionTable_GoGoRainDance__list_energy_ADDR}}, /* GoGoRainDance */
	{AIActionTable_ZappingSelfdestruct_ADDR, NULL, {AIActionTable_ZappingSelfdestruct__list_prize_ADDR, AIActionTable_ZappingSelfdestruct__list_arena_ADDR, AIActionTable_ZappingSelfdestruct__list_bench_ADDR, AIActionTable_ZappingSelfdestruct__list_bench_ADDR, AIActionTable_ZappingSelfdestruct__list_retreat_ADDR, AIActionTable_ZappingSelfdestruct__list_energy_ADDR}}, /* ZappingSelfdestruct */
	{AIActionTable_FlowerPower_ADDR, NULL, {AIActionTable_FlowerPower__list_prize_ADDR, AIActionTable_FlowerPower__list_arena_ADDR, AIActionTable_FlowerPower__list_bench_ADDR, AIActionTable_FlowerPower__list_bench_ADDR, AIActionTable_FlowerPower__list_retreat_ADDR, AIActionTable_FlowerPower__list_energy_ADDR}}, /* FlowerPower */
	{AIActionTable_StrangePsyshock_ADDR, NULL, {AIActionTable_StrangePsyshock__list_prize_ADDR, AIActionTable_StrangePsyshock__list_arena_ADDR, AIActionTable_StrangePsyshock__list_bench_ADDR, AIActionTable_StrangePsyshock__list_bench_ADDR, AIActionTable_StrangePsyshock__list_retreat_ADDR, AIActionTable_StrangePsyshock__list_energy_ADDR}}, /* StrangePsyshock */
	{AIActionTable_WondersOfScience_ADDR, NULL, {AIActionTable_WondersOfScience__list_prize_ADDR, AIActionTable_WondersOfScience__list_arena_ADDR, AIActionTable_WondersOfScience__list_bench_ADDR, AIActionTable_WondersOfScience__list_bench_ADDR, AIActionTable_WondersOfScience__list_retreat_ADDR, AIActionTable_WondersOfScience__list_energy_ADDR}}, /* WondersOfScience */
	{AIActionTable_FireCharge_ADDR, NULL, {AIActionTable_FireCharge__list_prize_ADDR, AIActionTable_FireCharge__list_arena_ADDR, AIActionTable_FireCharge__list_bench_ADDR, AIActionTable_FireCharge__list_bench_ADDR, AIActionTable_FireCharge__list_retreat_ADDR, AIActionTable_FireCharge__list_energy_ADDR}}, /* FireCharge */
	{AIActionTable_ImRonald_ADDR, NULL, {AIActionTable_ImRonald__list_prize_ADDR, AIActionTable_ImRonald__list_arena_ADDR, AIActionTable_ImRonald__list_bench_ADDR, AIActionTable_ImRonald__list_bench_ADDR, AIActionTable_ImRonald__list_retreat_ADDR, AIActionTable_ImRonald__list_energy_ADDR}}, /* ImRonald */
	{AIActionTable_PowerfulRonald_ADDR, NULL, {AIActionTable_PowerfulRonald__list_prize_ADDR, AIActionTable_PowerfulRonald__list_arena_ADDR, AIActionTable_PowerfulRonald__list_bench_ADDR, AIActionTable_PowerfulRonald__list_bench_ADDR, AIActionTable_PowerfulRonald__list_retreat_ADDR, AIActionTable_PowerfulRonald__list_energy_ADDR}}, /* PowerfulRonald */
	{AIActionTable_InvincibleRonald_ADDR, NULL, {AIActionTable_InvincibleRonald__list_prize_ADDR, AIActionTable_InvincibleRonald__list_arena_ADDR, AIActionTable_InvincibleRonald__list_bench_ADDR, AIActionTable_InvincibleRonald__list_bench_ADDR, AIActionTable_InvincibleRonald__list_retreat_ADDR, AIActionTable_InvincibleRonald__list_energy_ADDR}}, /* InvincibleRonald */
	{AIActionTable_LegendaryRonald_ADDR, turn_legendary_ronald, {AIActionTable_LegendaryRonald__list_prize_ADDR, AIActionTable_LegendaryRonald__list_arena_ADDR, AIActionTable_LegendaryRonald__list_bench_ADDR, AIActionTable_LegendaryRonald__list_play_hand_ADDR, AIActionTable_LegendaryRonald__list_retreat_ADDR, AIActionTable_LegendaryRonald__list_energy_ADDR}},
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
