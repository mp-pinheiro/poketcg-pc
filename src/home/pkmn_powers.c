#include "home/pkmn_powers.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "home/card_color.h"
#include "home/card_data.h"
#include "home/core.h"
#include "home/duel.h"

#include "generated/hram.h"
#include "generated/wram.h"

#include "mem.h"

#define DUELVARS_ARENA_CARD                 0xbbu
#define OPPACTION_USE_PKMN_POWER            0x0cu
#define OPPACTION_EXECUTE_PKMN_POWER_EFFECT 0x0du
#define OPPACTION_DUEL_MAIN_SCENE           0x16u
/* wce08: AI scratch byte holding the deck index the Pkmn Power acts on. */
#define WCE08_ADDR                          0xce08u

/* pkmn_powers.asm:618-729 (.CheckWhetherTurnDuelistHasColor). Returns 1 with
 * carry set if the turn duelist has a card in play whose color matches the
 * weakness WR mask in b: walks the play area slots starting at the arena card
 * variable until an $ff terminator. push bc around the card lookups keeps b
 * alive across the calls. Exit flags: 0x30 on a hit (and b sets H, scf sets C),
 * 0x00 on the terminator (or a with a = $ff). */
static uint8_t check_turn_duelist_has_color(uint8_t b, uint8_t *f)
{
	uint16_t hl = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).hl;
	for (;;) {
		uint8_t idx = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (idx == 0xffu) { /* .false */
			*f = 0x00u;
			return 0u;
		}
		uint16_t card_id = GetCardIDFromDeckIndex(idx);
		uint8_t wr = TranslateColorToWR(GetCardType((uint8_t)card_id));
		if ((uint8_t)(wr & b) != 0u) { /* and b ; jr z,.loop_play_area */
			*f = 0x30u;
			return 1u;
		}
	}
}

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/random.h"

#define AI_PEEK_TARGET_DECK                   0xffu
#define AI_PEEK_TARGET_HAND                   0x80u
#define AI_PEEK_TARGET_PRIZE                  0x40u
#define DECK_SIZE                             0x3cu
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK  0xbau
#define DUELVARS_PRIZES                       0xecu

#define DUELVARS_ARENA_CARD_HP 0xc8u
#define OPPACTION_6B15 0x15u
#define PLAY_AREA_ARENA 0x00u
/* <<< factory statics */

/* >>> factory HandleAIShift */
/* pkmn_powers.asm:618-729. AI handler for Venomoth's Shift power. c is the
 * Play Area location of Venomoth (0 = Arena card); any nonzero location
 * returns immediately. The c==0 path stores the defending Pokemon's weakness
 * to wAIDefendingPokemonWeakness and, when a usable color exists, runs the
 * OPPACTION_USE_PKMN_POWER / _EXECUTE_PKMN_POWER_EFFECT / _DUEL_MAIN_SCENE
 * sequence through AIMakeDecision. Produces a/f at every exit; b, c, d, e, hl
 * are preserved on the early paths. */
AIShiftResult HandleAIShift(uint8_t c)
{
	if (c != 0u) /* ld a,c ; or a ; ret nz */
		return (AIShiftResult){c, 0x00u};

	hTemp_ffa0 = 0u;
	uint8_t wr = TranslateColorToWR(GetArenaCardColor());
	SwapTurn();
	uint8_t weakness = GetArenaCardWeakness();
	wAIDefendingPokemonWeakness = weakness;
	SwapTurn();
	if (weakness == 0u) /* or a ; ret z */
		return (AIShiftResult){weakness, 0x80u};
	uint8_t overlap = (uint8_t)(weakness & wr);
	if (overlap != 0u) /* and b ; ret nz (and always sets H) */
		return (AIShiftResult){overlap, 0x20u};

	uint8_t f = 0u;
	if (!check_turn_duelist_has_color(weakness, &f)) {
		SwapTurn();
		uint8_t found = check_turn_duelist_has_color(weakness, &f);
		SwapTurn();
		if (!found) /* ret nc ; a/f from .false: a = $ff, or a */
			return (AIShiftResult){0xffu, 0x00u};
	}
	/* .found: dispatch the Shift Pkmn Power sequence */
	hTempCardIndex_ff9f = gb_read8(WCE08_ADDR);
	(void)AIMakeDecision(OPPACTION_USE_PKMN_POWER);

	/* converts WR_* back to a color index: rotate left until bit 7 is set */
	uint8_t color = 0u;
	uint8_t rot = wAIDefendingPokemonWeakness;
	while (!(rot & 0x80u)) {
		color = (uint8_t)(color + 1u);
		rot = (uint8_t)((rot << 1u) | (rot >> 7u));
	}

	hAIPkmnPowerEffectParam = color;
	(void)AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT);
	AIMakeDecisionResult r = AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE);
	return (AIShiftResult){OPPACTION_DUEL_MAIN_SCENE, r.f};
}
/* <<< factory HandleAIShift */

/* >>> factory HandleAIPeek */
/* pkmn_powers.asm:699-818. Decides whether the AI uses Peek: 47 of 50 Random(50)
 * rolls decline immediately (ret nc keeps a = the roll and f = the cp 3 flags).
 * Otherwise Random(3) picks the target: the Player's Deck (bail unless the Player
 * has >= 2 cards left, i.e. cards-not-in-deck < DECK_SIZE - 1), one of the AI's
 * own remaining prizes (bit-scan of wAIPeekedPrizes, lowest set bit; the flag is
 * cleared there and the prize index d is added to AI_PEEK_TARGET_PRIZE), or a
 * shuffled entry of the Player's hand list (turn is swapped around
 * CreateHandCardList; a is still the Random(3) result 1 at that call). The
 * target byte lands in hAIPkmnPowerEffectParam between two AIMakeDecision
 * oppactions; the tail always exits with a = OPPACTION_DUEL_MAIN_SCENE and
 * f = the final AIMakeDecision's flags (bank1call = plain call). */
AIPeekResult HandleAIPeek(uint8_t c)
{
	hTemp_ffa0 = c;

	uint8_t roll = Random(50u);
	if (roll >= 3u)
		return (AIPeekResult){roll, (uint8_t)(0x40u | (roll == 3u ? 0x80u : 0x00u) | (((roll & 0x0fu) < 3u) ? 0x20u : 0x00u))};

	uint8_t choice = Random(3u);
	uint8_t param;
	if (choice == 0u) {
		/* AI prizes */
		DuelistVarResult prizes = GetTurnDuelistVariable(DUELVARS_PRIZES);
		uint8_t avail = (uint8_t)(prizes.a & wAIPeekedPrizes);
		wAIPeekedPrizes = avail;
		if (avail == 0u)
			return (AIPeekResult){0x00u, 0x80u};
		uint8_t bit = 0x01u;
		uint8_t d = 0u;
		while ((avail & bit) == 0u) {
			bit = (uint8_t)(bit << 1u);
			d++;
		}
		wAIPeekedPrizes = (uint8_t)(avail - bit);
		param = (uint8_t)(AI_PEEK_TARGET_PRIZE + d);
	} else if (choice < 2u) {
		/* Player hand */
		SwapTurn();
		uint8_t hand = CreateHandCardList(choice).a;
		SwapTurn();
		if (hand == 0u)
			return (AIPeekResult){0x00u, 0x80u};
		ShuffleCards(CountCardsInDuelTempList().a, wDuelTempList_ADDR);
		param = (uint8_t)(wDuelTempList | AI_PEEK_TARGET_HAND);
	} else {
		/* Player deck */
		DuelistVarResult notindeck = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
		if (notindeck.a >= DECK_SIZE - 1u)
			return (AIPeekResult){notindeck.a, (uint8_t)(0x40u | (notindeck.a == DECK_SIZE - 1u ? 0x80u : 0x00u) | (((notindeck.a & 0x0fu) < 0x0bu) ? 0x20u : 0x00u))};
		param = AI_PEEK_TARGET_DECK;
	}

	hTempCardIndex_ff9f = wce08;
	AIMakeDecision(OPPACTION_USE_PKMN_POWER);
	hAIPkmnPowerEffectParam = param;
	AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT);
	AIMakeDecisionResult done = AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE);
	return (AIPeekResult){OPPACTION_DUEL_MAIN_SCENE, done.f};
}
/* <<< factory HandleAIPeek */

/* >>> factory HandleAIStrangeBehavior */
HandleAIStrangeBehaviorResult HandleAIStrangeBehavior(uint8_t c)
{
	if (c == 0u)
		return (HandleAIStrangeBehaviorResult){c, 0x80u};

	hTemp_ffa0 = c;
	CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
	if (damage.a == 0u)
		return (HandleAIStrangeBehaviorResult){damage.a, 0x80u};

	wce06 = damage.a;
	uint8_t hp = GetTurnDuelistVariable((uint8_t)(c + DUELVARS_ARENA_CARD_HP)).a;
	hp = (uint8_t)(hp - 10u);
	if (hp == 0u)
		return (HandleAIStrangeBehaviorResult){hp, 0x80u};

	uint8_t counters = hp;
	if (hp >= wce06)
		counters = wce06;

	hTempCardIndex_ff9f = wce08;
	(void)AIMakeDecision(OPPACTION_USE_PKMN_POWER);
	hAIPkmnPowerEffectParam = 0u;
	(void)AIMakeDecision(OPPACTION_EXECUTE_PKMN_POWER_EFFECT);

	counters = ConvertHPToDamageCounters_Bank8(counters);
	for (uint8_t e = counters; e != 0u; e--) {
		for (uint8_t d = 30u; d != 0u; d--)
			DoFrame();
		(void)AIMakeDecision(OPPACTION_6B15);
	}

	for (uint8_t d = 60u; d != 0u; d--)
		DoFrame();
	AIMakeDecisionResult result = AIMakeDecision(OPPACTION_DUEL_MAIN_SCENE);
	return (HandleAIStrangeBehaviorResult){OPPACTION_DUEL_MAIN_SCENE, result.f};
}
/* <<< factory HandleAIStrangeBehavior */
