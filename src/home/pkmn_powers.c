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
