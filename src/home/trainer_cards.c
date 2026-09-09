#include "home/trainer_cards.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "home/card_data.h"
#include "home/duel.h"
#include "mem.h"
#include "home/random.h"
#define TYPE_TRAINER 0x10u
#define TYPE_ENERGY 0x08u

#include "home/card_data.h"
#include "home/duel.h"

#include "home/duel.h"
#include "home/card_data.h"

#include "home/trainer_cards.h"

#include "home/duel.h"
#include "home/card_data.h"
#include "home/trainer_cards.h"
#include "generated/wram.h"
#include "mem.h"
#define DUELVARS_NUMBER_OF_CARDS_IN_HAND 0xEEu
#define DUELVARS_ARENA_CARD_STATUS 0xF0u
#define DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK 0xBAu

#include "home/duel.h"
#include "home/card_data.h"
#include "home/trainer_cards.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/trainer_cards.h"
#include "home/duel.h"
#include "home/random.h"
#include "generated/wram.h"
#define DECK_SIZE 0x3cu

#include "home/duel.h"
#include "home/trainer_cards.h"
#include "generated/wram.h"
#define ENERGY_REMOVAL 0xd0u
#define MR_MIME 0x9bu
#define POKEMON_TRADER 0xc9u

#include "home/core.h"
#include "home/substatus.h"
#include "home/duel.h"
#include "home/common.h"
#include "home/trainer_cards.h"
#include "home/card_data.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define BLASTOISE 0x43u
#define CARD_LOCATION_DISCARD_PILE 0x02u
#define DUELVARS_ARENA_CARD 0xbbu
#define DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA 0xefu
#define GO_GO_RAIN_DANCE_DECK_ID 0x12u
#define MUK 0x27u
#define PLAY_AREA_ARENA 0x00u

#include "home/duel.h"
#include "home/common.h"
#include "home/substatus.h"
#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"

#define ALAKAZAM 0x90u
#define DRAGONITE_LV41 0xc1u
#define DUELVARS_ARENA_CARD_HP 0xc8u
#define GENGAR 0x98u
#define VENUSAUR_LV64 0x0au
#define VENUSAUR_LV67 0x0bu
#define VILEPLUME 0x1eu

#define MOLTRES_LV35 0x3fu
#define MOLTRES_LV37 0x40u

#define ARTICUNO_LV35 0x5eu
#define ARTICUNO_LV37 0x5fu
#define CARD_LOCATION_DECK 0x00u
#define CHANSEY 0xb8u
#define SNORLAX 0xbeu
#define DEWGONG 0x4cu
#define DITTO 0xbbu
#define LAPRAS 0x59u
#define SEEL 0x4bu

#define JIGGLYPUFF_LV12 0xadu
#define TAUROS 0xbau

#define ARCANINE_LV34 0x37u
#define DODRIO 0xb6u
#define DODUO 0xb5u
#define GROWLITHE 0x36u
#define RATICATE 0xa8u
#define RATTATA 0xa7u

#define GRIMER 0x26u
#define PROFESSOR_OAK 0xc3u

#define DIGLETT 0x79u
#define DOUBLE_COLORLESS_ENERGY 0x07u
#define DUGTRIO 0x7au
#define FIGHTING_ENERGY 0x05u
#define GEODUDE 0x80u
#define GOLEM 0x82u
#define GRAVELER 0x81u
#define ONIX 0x83u
#define RHYHORN 0x89u

#define ANGER_DECK_ID 0x31u
#define FIRE_CHARGE_DECK_ID 0x17u
#define ROCK_CRUSHER_DECK_ID 0x11u
#define WONDERS_OF_SCIENCE_DECK_ID 0x16u
#define EXCAVATION_DECK_ID 0x1Fu
#define MYSTERIOUS_FOSSIL 0xccu
#define WATER_ENERGY 0x03u
#define TRUE 0x01u
#define DUELVARS_CARD_LOCATIONS 0x00u
#define CARD_LOCATION_HAND 0x01u

#define DRAGONAIR 0xc0u
#define DRATINI 0xbfu
#define EEVEE 0xbcu
#define FLAREON_LV22 0x3du
#define JOLTEON_LV24 0x72u
#define VAPOREON_LV29 0x5au
#define ZAPDOS_LV68 0x76u

#define CLOYSTER 0x4eu
#define HORSEA 0x51u
#define KINGLER 0x50u
#define KRABBY 0x4fu
#define SEADRA 0x52u
#define SHELLDER 0x4du
#define TENTACOOL 0x49u
#define TENTACRUEL 0x4au

#define CHARIZARD 0x32u
#define CHARMANDER 0x30u
#define CHARMELEON 0x31u
#define GYARADOS 0x58u
#define KANGASKHAN 0xb9u
#define MAGIKARP 0x57u

#define ETCETERA_DECK_ID 0x28u
#define FIRE_ENERGY 0x02u
#define FLYING_PIKACHU 0x64u
#define GASTLY_LV8 0x94u
#define HARD_POKEMON_DECK_ID 0x21u
#define JYNX 0x9cu
#define LIGHTNING_ENERGY 0x04u
#define LOVELY_NIDORAN_DECK_ID 0x2fu
#define MACHOP 0x7du
#define MAGMAR_LV31 0x3cu
#define MAGNEMITE_LV13 0x69u
#define NIDOKING 0x19u
#define NIDOQUEEN 0x16u
#define NIDORANF 0x14u
#define NIDORANM 0x17u
#define NIDORINA 0x15u
#define NIDORINO 0x18u
#define PIKACHU_ALT_LV16 0x63u
#define PIKACHU_DECK_ID 0x25u
#define PIKACHU_LV12 0x60u
#define PIKACHU_LV14 0x61u
#define PIKACHU_LV16 0x62u
#define PSYCHIC_ENERGY 0x06u
#define RHYDON 0x8au

#include "home/trainer_cards.h"
#include "home/common.h"
#include "home/duel.h"
#include "generated/wram.h"
#include "mem.h"
#define PLAY_AREA_BENCH_1 0x01u

#include "home/trainer_cards.h"
#include "home/common.h"
#include "generated/wram.h"
#include "mem.h"
#define CUBONE 0x84u
#define MAROWAK_LV26 0x85u
#define PONYTA 0x39u
#define RAPIDASH 0x3au

#include "home/trainer_cards.h"
#include "home/common.h"
#include "generated/wram.h"
#include "mem.h"
#define ARCANINE_LV45 0x38u
#define FLAREON_LV28 0x3eu
#define NINETALES_LV32 0x34u
#define VULPIX 0x33u

#include "home/trainer_cards.h"
#include "home/common.h"
#include "generated/wram.h"
#include "mem.h"
#define BELLSPROUT 0x23u
#define BULBASAUR 0x08u
#define GLOOM 0x1du
#define IVYSAUR 0x09u
#define ODDISH 0x1cu
#define VICTREEBEL 0x25u
#define WEEPINBELL 0x24u

#include "home/trainer_cards.h"
#include "home/common.h"
#include "generated/wram.h"
#include "mem.h"
#define ELECTRODE_LV35 0x6eu
#define ELECTRODE_LV42 0x6fu
#define MAGNEMITE_LV15 0x6au
#define MAGNETON_LV28 0x6bu
#define MAGNETON_LV35 0x6cu
#define RAICHU_LV40 0x67u
#define VOLTORB 0x6du

#include "home/trainer_cards.h"
#include "generated/wram.h"
#include "mem.h"
#define LEGENDARY_MOLTRES_DECK_ID 0x0Cu
#define LEGENDARY_ARTICUNO_DECK_ID 0x0Eu
#define LEGENDARY_DRAGONITE_DECK_ID 0x0Fu
#define LEGENDARY_RONALD_DECK_ID 0x1Bu
#define BLISTERING_POKEMON_DECK_ID 0x20u
#define SOUND_OF_THE_WAVES_DECK_ID 0x24u
#define POWER_GENERATOR_DECK_ID 0x27u
#define FLOWER_GARDEN_DECK_ID 0x29u
#define STRANGE_POWER_DECK_ID 0x2Du
#define FLAMETHROWER_DECK_ID 0x32u

#include "home/core.h"
#include "home/common.h"
#include "home/duel.h"
#include "home/card_data.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define TYPE_ENERGY_FIRE 0x08u
#define TYPE_ENERGY_GRASS 0x09u
#define TYPE_ENERGY_LIGHTNING 0x0Au
#define HEATED_BATTLE_DECK_ID 0x1Du

#include "home/core.h"
#include "home/substatus.h"
#include "home/common.h"
#include "home/duel.h"
#include "home/effect_commands.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define AI_FLAG_MODIFIED_HAND 0x08u
#define AI_FLAG_USED_SWITCH 0x02u
#define EFFECTCMDTYPE_INITIAL_EFFECT_1 0x01u
#define OPPACTION_PLAY_TRAINER 0x06u
#define SWITCH 0xd2u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/coin_toss.h"
#include "home/core.h"
#define OPPACTION_EXECUTE_TRAINER_EFFECTS 0x07u
#define TrainerCardSuccessCheckText 0x00efu

#include "home/core.h"
#include "home/damage_calculation.h"
#include "home/duel.h"
#include "home/random.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/card_color.h"
#include "home/damage_calculation.h"
#include "mem.h"
#define AI_FLAG_USED_GUST_OF_WIND 0x10u
#define FIRST_ATTACK_OR_PKMN_POWER 0x00u
#define MEWTWO_LV53 0x9Du
#define MEW_LV23 0xA2u
#define POKEMON_POWER 0x04u
#define SECOND_ATTACK 0x01u

#include "home/core.h"
#include "home/damage_calculation.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/retreat.h"
#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/common.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/retreat.h"

#include "home/retreat.h"
#include "home/core.h"
#include "home/common.h"
#include "generated/wram.h"
#define ASLEEP 0x02u
#define CNF_SLP_PRZ 0x0Fu
#define CONFUSED 0x01u
#define GASTLY_LV17 0x95u
#define HAUNTER_LV22 0x97u
#define PARALYZED 0x03u
#define SCOOP_UP 0xD5u

#include "home/core.h"
#include "home/damage_calculation.h"
#include "home/duel.h"
#include "home/common.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/common.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/random.h"

#include "home/core.h"
#include "home/damage_calculation.h"
#include "home/duel.h"
#include "home/substatus.h"
#include "home/trainer_cards.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"
#define AI_FLAG_USED_PLUSPOWER 0x01u

#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"

#include "home/core.h"
#include "generated/wram.h"
#include "generated/hram.h"
#include "mem.h"
#define IMAKUNI_DECK_ID 0x34u
#define NUM_COLORED_TYPES 0x06u
#define CARD_LOCATION_ARENA 0x10u
#define PLAYER_TURN 0xC2u
#define DUELVARS_BENCH 0xBCu
#define ATTACK_FLAG1_ADDRESS 0x00u
#define HIGH_RECOIL_F 0x06u
#define LOW_RECOIL_F 0x04u
#define AI_MEWTWO_MILL 0x80u
#define GHOST_DECK_ID 0x2Bu
#define LASS 0xC7u
#define MEOWTH_LV15 0xB2u
#define ZUBAT 0x1Au

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/common.h"
#include "home/core.h"
#include "home/duel.h"
#include "home/random.h"
#define ATTACK_FLAG3_ADDRESS 0x10u
#define BOOST_IF_TAKEN_DAMAGE_F 0u

#include "home/core.h"
#include "generated/hram.h"
#include "generated/wram.h"
#define AI_FLAG_USED_PROFESSOR_OAK 0x04u

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/core.h"

#include "home/core.h"
#include "home/common.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/common.h"
#include "home/core.h"
#include "home/duel.h"

#include "home/common.h"
#include "home/retreat.h"
#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"

#include "home/common.h"
#include "home/retreat.h"
#include "home/core.h"
#include "home/duel.h"
#include "generated/hram.h"
#include "generated/wram.h"

#include "generated/wram.h"
#include "generated/hram.h"
#include "home/core.h"
#define WIGGLYTUFF 0xB0u
#define MAX_PLAY_AREA_POKEMON 0x06u
/* <<< factory statics */

/* The exit F register of a `cp n` and of an `or a`, for the decisions whose
 * carry is the verdict and whose a register becomes the card parameter. */
static uint8_t cp_flags(uint8_t a, uint8_t n)
{
	return (uint8_t)(0x40u
		| ((a == n) ? 0x80u : 0u)
		| (((a & 0x0Fu) < (n & 0x0Fu)) ? 0x20u : 0u)
		| ((a < n) ? 0x10u : 0u));
}

static uint8_t or_a_flags(uint8_t a)
{
	return a == 0u ? 0x80u : 0x00u;
}


/* >>> factory RemoveCardFromList */
/* trainer_cards.asm:2760-2776. Shifts the $ff-terminated list down by one byte,
 * removing the entry just before hl. Leaves hl decremented; de preserved. */
void RemoveCardFromList(uint16_t *hl)
{
	uint16_t src = *hl;
	uint16_t dst = (uint16_t)(src - 1u);
	uint8_t v;
	do {
		v = gb_read8(src);
		src = (uint16_t)(src + 1u);
		gb_write8(dst, v);
		dst = (uint16_t)(dst + 1u);
	} while (v != 0xFFu);
	*hl = (uint16_t)(*hl - 1u);
}
/* <<< factory RemoveCardFromList */


/* >>> factory FindDuplicateCards */
/* trainer_cards.asm:2788-2859 */
FindDupResult FindDuplicateCards(uint16_t hl, uint8_t d)
{
	wce0f = 0xFFu;
	gb_write8((uint16_t)(wce0f_ADDR + 1u), 0xFFu);
	uint16_t outer = hl;
	for (;;) {
		uint8_t idx = gb_read8(outer);
		outer = (uint16_t)(outer + 1u);
		if (idx == 0xFFu)
			break;
		d = 0u;
		uint8_t b = (uint8_t)GetCardIDFromDeckIndex(idx);
		uint16_t inner = outer;
		for (;;) {
			uint8_t c = gb_read8(inner);
			inner = (uint16_t)(inner + 1u);
			if (c == 0xFFu)
				break;
			if ((uint8_t)GetCardIDFromDeckIndex(c) != b)
				continue;
			if (GetCardType(b) < TYPE_ENERGY)
				wce0f = c;
			else
				gb_write8((uint16_t)(wce0f_ADDR + 1u), c);
			break;
		}
	}
	uint8_t lo = wce0f;
	uint8_t hi = gb_read8((uint16_t)(wce0f_ADDR + 1u));
	if (lo == 0xFFu && hi == 0xFFu)
		return (FindDupResult){0xFFu, 0x90u, outer, d};
	uint8_t a = (lo != 0xFFu) ? lo : hi;
	return (FindDupResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u), outer, d};
}
/* <<< factory FindDuplicateCards */

/* >>> factory FindAndRemoveCardFromList */
/* trainer_cards.asm:3072-3082 */
void FindAndRemoveCardFromList(uint8_t a, uint16_t hl)
{
	uint16_t p = hl;
	uint8_t v;
	do {
		v = gb_read8(p);
		p = (uint16_t)(p + 1u);
	} while (v != a);
	RemoveCardFromList(&p);
}
/* <<< factory FindAndRemoveCardFromList */
/* >>> factory PickPokedexCards */
PickPokedexResult PickPokedexCards(void)
{
	DuelistVarResult remaining = GetTurnDuelistVariable(0xBAu);
	uint16_t deck = (uint16_t)((remaining.hl & 0xFF00u) |
				   (uint8_t)(remaining.a + 0x7Eu));
	uint8_t types[5], indices[5];
	wAIPokedexCounter = 0;
	for (uint8_t i = 0; i < 5; i++) {
		indices[i] = gb_read8((uint16_t)(deck + i));
		types[i] = GetCardType((uint8_t)GetCardIDFromDeckIndex(indices[i]));
		gb_write8((uint16_t)(wce08_ADDR + i), types[i]);
		gb_write8((uint16_t)(wce0f_ADDR + i), indices[i]);
	}
	gb_write8((uint16_t)(wce08_ADDR + 5u), 0xFFu);
	uint8_t out = 0;
	for (uint8_t wanted = 0; wanted < 3; wanted++) {
		for (uint8_t i = 0; i < 5; i++) {
			uint8_t type = types[i];
			if ((wanted == 0 && !(type & TYPE_ENERGY)) ||
			    (wanted == 1 && type >= TYPE_ENERGY) ||
			    (wanted == 2 && type != TYPE_TRAINER))
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), indices[i]);
		}
	}
	/* de walks wce1a through the five picks and stays on the page. */
	return (PickPokedexResult){0xFFu, 0x90u, (uint8_t)((wce1a_ADDR + out) >> 8)};
}
/* <<< factory PickPokedexCards */
/* >>> factory AIDecide_Recycle */
AIDecideParameterResult AIDecide_Recycle(uint8_t d)
{
	/* trainer_cards.asm AIDecide_Recycle: the five priority slots live in
	 * wce08..wce0c and the first one filled is the card to recycle. */
	CardListResult discard = CreateDiscardPileCardList(0);
	if (discard.f & 0x10u)
		return (AIDecideParameterResult){discard.a, or_a_flags(discard.a), 0xC5u};
	for (uint8_t i = 0; i < 5u; i++)
		gb_write8((uint16_t)(wce08_ADDR + i), 0xFFu);
	uint16_t list = wDuelTempList_ADDR;
	uint8_t ghost = wOpponentDeckID == GHOST_DECK_ID;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			break;
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (!ghost) {
			if (card_id == DOUBLE_COLORLESS_ENERGY) gb_write8(wce08_ADDR, deck_index);
			else if (card_id == CHANSEY) gb_write8(wce08_ADDR + 1u, deck_index);
			else if (card_id == TAUROS) gb_write8(wce08_ADDR + 2u, deck_index);
			else if (card_id == JIGGLYPUFF_LV12) gb_write8(wce08_ADDR + 3u, deck_index);
		} else {
			if (card_id == GASTLY_LV17) gb_write8(wce08_ADDR, deck_index);
			else if (card_id == GASTLY_LV8) gb_write8(wce08_ADDR + 1u, deck_index);
			else if (card_id == ZUBAT) gb_write8(wce08_ADDR + 2u, deck_index);
			else if (card_id == DITTO) gb_write8(wce08_ADDR + 3u, deck_index);
			else if (card_id == MEOWTH_LV15) gb_write8(wce08_ADDR + 4u, deck_index);
		}
	}
	for (uint8_t i = 0; i < 5u; i++) {
		uint8_t chosen = gb_read8((uint16_t)(wce08_ADDR + i));
		if (chosen != 0xFFu)
			return (AIDecideParameterResult){chosen, 0x10u, 0xC5u};
	}
	return (AIDecideParameterResult){0xFFu, 0x00u, 0xC5u};
}
/* <<< factory AIDecide_Recycle */

/* >>> factory AIDecide_Maintenance */
AIDecideMaintenanceResult AIDecide_Maintenance(uint8_t d)
{
	DuelistVarResult hand = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (wOpponentDeckID == IMAKUNI_DECK_ID) {
		if (Random(10u) >= 2u || hand.a < 3u)
			return (AIDecideMaintenanceResult){hand.a,
				(uint8_t)(hand.a == 0u ? 0x80u : 0u), d};
		(void)CreateHandCardList(0);
		TempListResult count = CountCardsInDuelTempList();
		(void)ShuffleCards(count.a, wDuelTempList_ADDR);
		uint16_t p = wDuelTempList_ADDR;
		uint8_t target = wAITrainerCardToPlay, found = 0, out = 0;
		while (found < 2u) {
			uint8_t card = gb_read8(p++);
			if (card == 0xFFu)
				return (AIDecideMaintenanceResult){0, 0x00u, 0xCEu};
			if (card == target)
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), card);
			found++;
		}
		return (AIDecideMaintenanceResult){0, 0x10u, 0xCEu};
	}
	if (hand.a < 4u)
		return (AIDecideMaintenanceResult){hand.a,
			(uint8_t)(hand.a == 0u ? 0x80u : 0u), d};
	(void)CreateHandCardList(0);
	FindAndRemoveCardFromList(wAITrainerCardToPlay, wDuelTempList_ADDR);
	FindDupResult first = FindDuplicateCards(wDuelTempList_ADDR, 0xC5u);
	if (first.a == 0xFFu)
		return (AIDecideMaintenanceResult){first.a, 0x00u, first.d};
	wce1a = first.a;
	FindAndRemoveCardFromList(first.a, wDuelTempList_ADDR);
	FindDupResult second = FindDuplicateCards(wDuelTempList_ADDR, first.d);
	if (second.a == 0xFFu)
		return (AIDecideMaintenanceResult){second.a, 0x00u, second.d};
	wce1b = second.a;
	return (AIDecideMaintenanceResult){second.a, 0x10u, second.d};
}
/* <<< factory AIDecide_Maintenance */
/* >>> factory AIDecide_Lass */
AIDecideParameterResult AIDecide_Lass(uint8_t d)
{
	uint8_t hand_count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (hand_count < 7u)
		return (AIDecideParameterResult){hand_count, or_a_flags(hand_count), d};
	(void)CreateHandCardList(hand_count);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			return (AIDecideParameterResult){0xFFu, 0x90u, 0xC5u};
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (card_id == LASS)
			continue;
		uint8_t type = gb_read8(wLoadedCard1Type_ADDR);
		if (type == TYPE_TRAINER)
			return (AIDecideParameterResult){type, 0x00u, 0xC5u};
	}
}
/* <<< factory AIDecide_Lass */

/* >>> factory AIDecide_Imakuni */
AIDecideParameterResult AIDecide_Imakuni(uint8_t d)
{
	uint8_t status = (uint8_t)(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ);
	if (status == CONFUSED)
		return (AIDecideParameterResult){status, 0x00u, d};
	return (AIDecideParameterResult){status, 0x10u, d};
}
/* <<< factory AIDecide_Imakuni */
/* >>> factory AIDecide_PokemonFlute */
AIDecidePokemonFluteResult AIDecide_PokemonFlute(uint8_t c, uint8_t d)
{
	SwapTurn();
	CardListResult discard = CreateDiscardPileCardList(c);
	SwapTurn();
	if (discard.f & 0x10u)
		return (AIDecidePokemonFluteResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u), 0xC5u};
	uint8_t count = GetNonTurnDuelistVariable(0xEFu).a;
	if (count >= 6u)
		return (AIDecidePokemonFluteResult){count, (uint8_t)(count == 0u ? 0x80u : 0u), 0xC5u};
	wce06 = 0xFFu;
	wce08 = 0xFFu;
	for (uint16_t p = wDuelTempList_ADDR;; p++) {
		uint8_t index = gb_read8(p);
		if (index == 0xFFu)
			break;
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		if (wLoadedCard1Type >= TYPE_ENERGY || wLoadedCard1Stage != 0u ||
		    wLoadedCard1HP >= wce06)
			continue;
		wce06 = wLoadedCard1HP;
		wce08 = index;
	}
	if (wOpponentDeckID == IMAKUNI_DECK_ID) {
		if (Random(10u) >= 2u)
			return (AIDecidePokemonFluteResult){0, 0, 0xC5u};
		return (AIDecidePokemonFluteResult){wce08, wce08 == 0xFFu ? 0u : 0x10u, 0xC5u};
	}
	if (wce06 >= 50u)
		return (AIDecidePokemonFluteResult){wce06, 0, 0xC5u};
	return (AIDecidePokemonFluteResult){wce08, 0x10u, 0xC5u};
}
/* <<< factory AIDecide_PokemonFlute */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
/* trainer_cards.asm:4784-4812. The play area count is parked in wce06 for
 * the later phases; a Wigglytuff in the arena plays the card outright, with
 * `cp WIGGLYTUFF`'s Z under the carry. */
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(uint8_t d)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	if (count >= MAX_PLAY_AREA_POKEMON)
		return (AIDecidePokemonFluteResult){count, count == 0u ? 0x80u : 0u, d};
	wce06 = count;
	uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(arena);
	if (card_id == WIGGLYTUFF)
		return (AIDecidePokemonFluteResult){card_id, 0x90u, 0u};
	if (count < 4u)
		return (AIDecidePokemonFluteResult){count, 0x10u, 0u};
	return (AIDecidePokemonFluteResult){count, count == 0u ? 0x80u : 0u, 0u};
}
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */

/* >>> factory AIDecide_Defender_Phase14 */
AIDecideParameterResult AIDecide_Defender_Phase14(uint8_t d)
{
	/* trainer_cards.asm AIDecide_Defender_Phase14: play Defender when the
	 * chosen attack's recoil, after the card's own weakness and resistance
	 * and the 20 Defender prevents, would still not knock the card out.
	 * The recoil lives in d from `ld d, a` on; the no-recoil exit keeps the
	 * entry d. */
	AttackFlagResult recoil = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | HIGH_RECOIL_F);
	if ((recoil.f & 0x10u) == 0u)
		recoil = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | LOW_RECOIL_F);
	if ((recoil.f & 0x10u) == 0u)
		return (AIDecideParameterResult){recoil.a, or_a_flags(recoil.a), d};
	(void)LoadCardDataToBuffer2_FromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	uint8_t damage = wSelectedAttack == 0u ? wLoadedCard2Atk1EffectParam : wLoadedCard2Atk2EffectParam;
	uint8_t color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardWeakness() & color)
		damage = (uint8_t)(damage << 1);
	color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardResistance() & color) {
		uint8_t reduced = (uint8_t)(damage - 30u);
		if (damage < 30u)
			return (AIDecideParameterResult){reduced, or_a_flags(reduced), damage};
		damage = reduced;
	}
	if (damage == 0u)
		return (AIDecideParameterResult){0u, 0x80u, damage};
	damage = (uint8_t)(damage - 20u);
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - damage);
	if (hp <= damage)
		return (AIDecideParameterResult){left, or_a_flags(left), damage};
	return (AIDecideParameterResult){left, 0x10u, damage};
}
/* <<< factory AIDecide_Defender_Phase14 */

/* >>> factory AIDecide_Bill */
AIDecideParameterResult AIDecide_Bill(uint8_t d)
{
	/* trainer_cards.asm:1428-1432: a is the count the cp leaves. */
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 9u), d};
}
/* <<< factory AIDecide_Bill */

/* >>> factory AIDecide_Gambler */
AIDecideParameterResult AIDecide_Gambler(uint8_t d)
{
	if (wOpponentDeckID == IMAKUNI_DECK_ID) {
		/* .imakuni: play it two times in ten; a is the roll either way. */
		uint8_t roll = Random(10u);
		if (roll < 2u)
			return (AIDecideParameterResult){roll, 0x10u, d};
		return (AIDecideParameterResult){roll, or_a_flags(roll), d};
	}
	uint8_t mill = (uint8_t)(wAIBarrierFlagCounter & AI_MEWTWO_MILL);
	if (mill == 0u)
		return (AIDecideParameterResult){0u, 0x80u, d};
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	if (remaining >= DECK_SIZE - 4u)
		return (AIDecideParameterResult){remaining, (uint8_t)((remaining == DECK_SIZE - 4u ? 0x80u : 0u) | 0x10u), d};
	return (AIDecideParameterResult){remaining, or_a_flags(remaining), d};
}
/* <<< factory AIDecide_Gambler */

/* >>> factory AIDecide_Revive */
AIDecideReviveResult AIDecide_Revive(uint8_t d)
{
	CardListResult discard = CreateDiscardPileCardList(0);
	if (discard.f & 0x10u)
		return (AIDecideReviveResult){discard.a, 0x80u, 0xC5u};
	if (GetTurnDuelistVariable(0xEFu).a >= 4u) {
		uint8_t count = GetTurnDuelistVariable(0xEFu).a;
		return (AIDecideReviveResult){count, 0, 0xC5u};
	}
	for (uint16_t p = wDuelTempList_ADDR;; p++) {
		uint8_t index = gb_read8(p);
		if (index == 0xFFu)
			return (AIDecideReviveResult){0xFFu, 0, 0xC5u};
		uint8_t card = LoadCardDataToBuffer1_FromDeckIndex(index);
		if (card == 0x88u || card == 0x87u)
			return (AIDecideReviveResult){index, 0x90u, 0xC5u};
		if (card == 0xBAu)
			return (AIDecideReviveResult){0, 0x10u, 0xC5u};
	}
}
/* <<< factory AIDecide_Revive */

/* >>> factory AIDecide_ImposterProfessorOak */
AIDecideParameterResult AIDecide_ImposterProfessorOak(uint8_t d)
{
	uint8_t remaining = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	uint8_t hand = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (remaining < DECK_SIZE - 14u) {
		if (hand < 9u)
			return (AIDecideParameterResult){hand, or_a_flags(hand), d};
		return (AIDecideParameterResult){hand, (uint8_t)((hand == 9u ? 0x80u : 0u) | 0x10u), d};
	}
	if (hand < 6u)
		return (AIDecideParameterResult){hand, 0x10u, d};
	return (AIDecideParameterResult){hand, or_a_flags(hand), d};
}
/* <<< factory AIDecide_ImposterProfessorOak */

/* >>> factory PickPokedexCards_Unreferenced */
PickPokedexResult PickPokedexCards_Unreferenced(void)
{
	DuelistVarResult remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	uint16_t deck = (uint16_t)((remaining.hl & 0xFF00u) |
				   (uint8_t)(remaining.a + 0x7Eu));
	uint8_t types[5], indices[5];
	wAIPokedexCounter = 0;
	for (uint8_t i = 0; i < 5u; i++) {
		indices[i] = gb_read8((uint16_t)(deck + i));
		types[i] = GetCardType((uint8_t)GetCardIDFromDeckIndex(indices[i]));
		gb_write8((uint16_t)(wce08_ADDR + i), types[i]);
		gb_write8((uint16_t)(wce0f_ADDR + i), indices[i]);
	}
	gb_write8((uint16_t)(wce08_ADDR + 5u), 0xFFu);
	uint8_t out = 0;
	for (uint8_t wanted = 0; wanted < 3u; wanted++) {
		for (uint8_t i = 0; i < 5u; i++) {
			uint8_t type = types[i];
			if ((wanted == 0u && type >= TYPE_ENERGY) ||
			    (wanted == 1u && type != TYPE_TRAINER) ||
			    (wanted == 2u && !(type & TYPE_ENERGY)))
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), indices[i]);
		}
	}
	return (PickPokedexResult){0xFFu, (uint8_t)(0x80u | 0x10u)};
}
/* <<< factory PickPokedexCards_Unreferenced */

/* >>> factory AIDecide_Pokedex */
AIDecidePokedexResult AIDecide_Pokedex(uint8_t d)
{
	/* Every refusal keeps the entry d; only PickPokedexCards moves it. */
	uint8_t counter = wAIPokedexCounter;
	if (counter < 6u)
		return (AIDecidePokedexResult){counter, (uint8_t)(counter == 0u ? 0x80u : 0u), d};
	DuelistVarResult notindeck = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (notindeck.a >= (DECK_SIZE - 4u))
		return (AIDecidePokedexResult){notindeck.a, (uint8_t)(notindeck.a == 0u ? 0x80u : 0u), d};
	uint8_t roll = Random(10u);
	if (roll >= 3u)
		return (AIDecidePokedexResult){roll, (uint8_t)(roll == 0u ? 0x80u : 0u), d};
	PickPokedexResult picked = PickPokedexCards();
	return (AIDecidePokedexResult){picked.a, picked.f, picked.d};
}
/* <<< factory AIDecide_Pokedex */

/* >>> factory AIDecide_ItemFinder */
AIDecide_ItemFinderResult AIDecide_ItemFinder(uint8_t d)
{
	CardListResult discard = CreateDiscardPileCardList(0u);
	uint8_t a = discard.a;
	d = 0xC5u;
	if (!(discard.f & 0x10u)) {
		uint16_t hl = wDuelTempList_ADDR;
		uint8_t deck_index = 0u;
		uint8_t found = 0u;
		for (;;) {
			deck_index = gb_read8(hl);
			hl = (uint16_t)(hl + 1u);
			if (deck_index == 0xFFu) {
				a = 0xFFu;
				break;
			}
			uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
			if (card_id == ENERGY_REMOVAL) {
				found = 1u;
				break;
			}
		}
		if (found) {
			wce06 = deck_index;

			(void)CreateHandCardList(0u);
			hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t v = gb_read8(hl);
				hl = (uint16_t)(hl + 1u);
				if (v == 0xFFu)
					break;
				uint8_t card_id2 = LoadCardDataToBuffer1_FromDeckIndex(v);
				if (card_id2 == MR_MIME || card_id2 == POKEMON_TRADER)
					RemoveCardFromList(&hl);
			}

			FindAndRemoveCardFromList(wAITrainerCardToPlay, wDuelTempList_ADDR);
			FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR, d);
			a = dup1.a;
			d = dup1.d;
			if (!(dup1.f & 0x10u)) {
				wce1a = dup1.a;
				FindAndRemoveCardFromList(dup1.a, wDuelTempList_ADDR);
				FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR, d);
				a = dup2.a;
				d = dup2.d;
				if (!(dup2.f & 0x10u)) {
					wce1b = dup2.a;
					return (AIDecide_ItemFinderResult){wce06, 0x10u, d};
				}
			}
		}
	}
	return (AIDecide_ItemFinderResult){a, (uint8_t)(a == 0u ? 0x80u : 0u), d};
}
/* <<< factory AIDecide_ItemFinder */

/* >>> factory AIDecide_EnergyRetrieval */
AIDecideEnergyRetrievalResult AIDecide_EnergyRetrieval(uint8_t a, uint8_t d)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u), d};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideEnergyRetrievalResult){blastoise.a, (uint8_t)(blastoise.a == 0u ? 0x80u : 0u), d};
		}
	}

	/* CreateHandCardList leaves de on wDuelTempList's page. */
	d = CreateHandCardList(0u).d;
	FindDupResult dup = FindDuplicateCards(wDuelTempList_ADDR, d);
	d = dup.d;
	if (dup.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){dup.a, (uint8_t)(dup.a == 0u ? 0x80u : 0u), d};
	uint8_t saved_card = dup.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	d = discard.d;
	if (discard.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u), d};

	wce1a = 0xFFu;
	wce1b = 0xFFu;
	wce1c = 0xFFu;

	d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	while (d != 0u) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		wTempCardID = card_id;
		LoadCardDataToBuffer1_FromCardID(card_id);
		wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);

		uint16_t hl = wDuelTempList_ADDR;
		for (;;) {
			uint8_t entry = gb_read8(hl);
			hl++;
			if (entry == 0xFFu)
				break;
			if (!(CheckIfEnergyIsUseful(entry).f & 0x10u))
				continue;
			if (wce1a != 0xFFu) {
				wce1b = entry;
				return (AIDecideEnergyRetrievalResult){saved_card, 0x10u, d};
			}
			wce1a = entry;
			RemoveCardFromList(&hl);
			break;
		}
		e++;
		d--;
	}

	uint16_t hl2 = wDuelTempList_ADDR;
	for (;;) {
		uint8_t entry = gb_read8(hl2);
		hl2++;
		if (entry == 0xFFu)
			break;
		if (wce1a != 0xFFu) {
			wce1b = entry;
			return (AIDecideEnergyRetrievalResult){saved_card, 0x10u, d};
		}
		wce1a = entry;
		RemoveCardFromList(&hl2);
	}

	if (wce1a != 0xFFu)
		return (AIDecideEnergyRetrievalResult){saved_card, 0x10u, d};
	return (AIDecideEnergyRetrievalResult){wce1a, (uint8_t)(wce1a == 0u ? 0x80u : 0u), d};
}
/* <<< factory AIDecide_EnergyRetrieval */

/* >>> factory AIDecide_SuperEnergyRetrieval */
AIDecideSuperEnergyRetrievalResult AIDecide_SuperEnergyRetrieval(uint8_t a, uint8_t d)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideSuperEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u), d};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideSuperEnergyRetrievalResult){blastoise.a, (uint8_t)(blastoise.a == 0u ? 0x80u : 0u), d};
		}
	}

	/* CreateHandCardList leaves de on wDuelTempList's page. */
	d = CreateHandCardList(0u).d;
	FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR, d);
	d = dup1.d;
	if (dup1.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup1.a, (uint8_t)(dup1.a == 0u ? 0x80u : 0u), d};
	wce06 = dup1.a;

	FindAndRemoveCardFromList(wce06, wDuelTempList_ADDR);
	FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR, d);
	d = dup2.d;
	if (dup2.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup2.a, (uint8_t)(dup2.a == 0u ? 0x80u : 0u), d};
	wce08 = dup2.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	d = discard.d;
	if (discard.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u), d};

	wce1b = 0xFFu;
	wce1c = 0xFFu;
	wce1d = 0xFFu;
	wce1e = 0xFFu;
	wce1f = 0xFFu;

	d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	while (d != 0u) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		wTempCardID = card_id;
		LoadCardDataToBuffer1_FromCardID(card_id);
		wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);

		uint16_t hl = wDuelTempList_ADDR;
		for (;;) {
			uint8_t entry = gb_read8(hl);
			hl++;
			if (entry == 0xFFu)
				break;
			if (!(CheckIfEnergyIsUseful(entry).f & 0x10u))
				continue;
			if (wce1b == 0xFFu) {
				wce1b = entry;
				RemoveCardFromList(&hl);
			} else if (wce1c == 0xFFu) {
				wce1c = entry;
				RemoveCardFromList(&hl);
			} else if (wce1d == 0xFFu) {
				wce1d = entry;
				RemoveCardFromList(&hl);
			} else {
				wce1e = entry;
				wce1a = wce08;
				return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u, d};
			}
			break;
		}
		e++;
		d--;
	}

	uint16_t hl2 = wDuelTempList_ADDR;
	for (;;) {
		uint8_t entry = gb_read8(hl2);
		hl2++;
		if (entry == 0xFFu)
			break;
		if (wce1b == 0xFFu) {
			wce1b = entry;
			RemoveCardFromList(&hl2);
		} else if (wce1c == 0xFFu) {
			wce1c = entry;
			RemoveCardFromList(&hl2);
		} else if (wce1d == 0xFFu) {
			wce1d = entry;
			RemoveCardFromList(&hl2);
		} else {
			wce1e = entry;
			wce1a = wce08;
			return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u, d};
		}
	}

	if (wce1b != 0xFFu) {
		wce1a = wce08;
		return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u, d};
	}
	return (AIDecideSuperEnergyRetrievalResult){0xFFu, 0x00u, d};
}
/* <<< factory AIDecide_SuperEnergyRetrieval */

/* >>> factory AIDecide_PokemonBreeder */
AIDecidePokemonBreederResult AIDecide_PokemonBreeder(uint16_t hl_in, uint8_t d)
{
	/* d: the entry value on the Prehistoric Power refusal; `ld d, a` takes
	 * each hand card's deck index in the two hand loops (their callees are
	 * bracketed in `push de` / `pop de`), CreateHandCardList leaves
	 * wDuelTempList's page when the hand is empty, and the score loops start
	 * from `ld d, $00`. */
	PrehistoricPowerResult power = IsPrehistoricPowerActive(hl_in);
	if (power.f & 0x10u)
		return (AIDecidePokemonBreederResult){power.a, power.f, d};

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	d = CreateHandCardList(0u).d;
	uint16_t hl = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl);
		hl++;
		if (deck_index == 0xFFu)
			break;
		d = deck_index;

		uint8_t card_type = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (card_type == VENUSAUR_LV64 || card_type == VENUSAUR_LV67 ||
		    card_type == BLASTOISE || card_type == VILEPLUME ||
		    card_type == ALAKAZAM || card_type == GENGAR) {
			uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
			uint8_t e = PLAY_AREA_ARENA;
			for (; c != 0u; c--, e++) {
				EvolveResult evolve = CheckIfCanEvolveInto_BasicToStage2(deck_index, e);
				if (evolve.f & 0x10u)
					continue;

				uint8_t damage = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + e)).a;
				uint8_t counters = ConvertHPToDamageCounters_Bank8(damage);
				uint8_t hi = (uint8_t)(((counters & 0x0Fu) << 4) | ((counters & 0xF0u) >> 4));
				(void)GetPlayAreaCardAttachedEnergies(e);
				uint8_t energies = wTotalAttachedEnergies;
				uint8_t lo = (energies >= 16u) ? 15u : energies;
				gb_write8((uint16_t)(wce08_ADDR + e), (uint8_t)(hi | lo));
				gb_write8((uint16_t)(wce0f_ADDR + e), deck_index);
				wce06++;
			}
		}
	}

	if (wce06 != 0u) {
		wce06 = 0u;
		uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t e = PLAY_AREA_ARENA;
		uint8_t best_loc = 0u;
		for (; c != 0u; c--, e++) {
			uint8_t score = gb_read8((uint16_t)(wce08_ADDR + e));
			if (wce06 < score) {
				wce06 = score;
				best_loc = e;
			}
		}
		wce07 = best_loc;
		wce1a = gb_read8((uint16_t)(wce0f_ADDR + best_loc));
		return (AIDecidePokemonBreederResult){best_loc, 0x10u, 0u};
	}

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	d = CreateHandCardList(0u).d;
	uint16_t hl2 = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl2);
		hl2++;
		if (deck_index == 0xFFu)
			break;
		d = deck_index;

		uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t e = PLAY_AREA_ARENA;
		for (; c != 0u; c--, e++) {
			EvolveResult evolve = CheckIfCanEvolveInto_BasicToStage2(deck_index, e);
			if (evolve.f & 0x10u)
				continue;

			uint8_t evolving_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
			uint8_t dragonite_carry = 0u;
			if (evolving_id == DRAGONITE_LV41) {
				if (e == 0u) {
					uint8_t hp = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
					uint8_t counters = ConvertHPToDamageCounters_Bank8(hp);
					CountNumberOfEnergyCardsAttachedResult energy =
						CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA);
					if (counters >= 5u || energy.a < 3u)
						dragonite_carry = 1u;
				} else {
					uint8_t total_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
					uint8_t sum = 0u;
					uint8_t loc = total_count;
					while (loc != 0u) {
						loc--;
						uint8_t hp = GetCardDamageAndMaxHP(loc).a;
						sum = (uint8_t)(sum + ConvertHPToDamageCounters_Bank8(hp));
					}
					if (sum < 8u)
						dragonite_carry = 1u;
				}
			}
			if (dragonite_carry)
				continue;

			uint8_t damage = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + e)).a;
			uint8_t counters2 = ConvertHPToDamageCounters_Bank8(damage);
			uint8_t hi = (uint8_t)(((counters2 & 0x0Fu) << 4) | ((counters2 & 0xF0u) >> 4));
			(void)GetPlayAreaCardAttachedEnergies(e);
			uint8_t energies = wTotalAttachedEnergies;
			uint8_t lo = (energies >= 16u) ? 15u : energies;
			gb_write8((uint16_t)(wce08_ADDR + e), (uint8_t)(hi | lo));
			gb_write8((uint16_t)(wce0f_ADDR + e), deck_index);
			wce06++;
		}
	}

	if (wce06 == 0u)
		return (AIDecidePokemonBreederResult){0u, 0x80u, d};

	wce06 = 0u;
	wce07 = 0xFFu;
	d = 0u;
	{
		uint8_t c = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		uint8_t e = PLAY_AREA_ARENA;
		for (; c != 0u; c--, e++) {
			uint8_t score = gb_read8((uint16_t)(wce08_ADDR + e));
			if (wce06 < score) {
				uint8_t energy_count = (uint8_t)(score & 0x0Fu);
				if (energy_count >= 2u) {
					wce06 = score;
					wce07 = e;
				}
			}
		}
	}

	if (wce07 == 0xFFu)
		return (AIDecidePokemonBreederResult){0xFFu, 0x00u, d};

	wce1a = gb_read8((uint16_t)(wce0f_ADDR + wce07));
	return (AIDecidePokemonBreederResult){wce07, 0x10u, d};
}
/* <<< factory AIDecide_PokemonBreeder */

/* >>> factory AIDecide_PokemonTrader_LegendaryMoltres */
AIDecide_PokemonTrader_LegendaryMoltresResult AIDecide_PokemonTrader_LegendaryMoltres(uint8_t d)
{
	LookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MOLTRES_LV37, MOLTRES_LV35);
	if (!(r.f & 0x10u)) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryMoltresResult){r.a, f, r.d};
	}
	wce1a = r.a;
	return (AIDecide_PokemonTrader_LegendaryMoltresResult){r.e, 0x10u, r.d};
}
/* <<< factory AIDecide_PokemonTrader_LegendaryMoltres */

/* >>> factory AIDecide_PokemonTrader_StrangePower */
AIDecide_PokemonTrader_StrangePowerResult AIDecide_PokemonTrader_StrangePower(uint8_t d)
{
	LookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MR_MIME, MR_MIME);
	if (!(r.f & 0x10u)) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_StrangePowerResult){r.a, f, r.d};
	}
	wce1a = r.a;
	return (AIDecide_PokemonTrader_StrangePowerResult){r.e, 0x10u, r.d};
}
/* <<< factory AIDecide_PokemonTrader_StrangePower */

/* >>> factory AIDecide_PokemonTrader_LegendaryArticuno */
AIDecide_PokemonTrader_LegendaryArticunoResult AIDecide_PokemonTrader_LegendaryArticuno(uint8_t d)
{
	LookForCardIDInHandAndPlayAreaResult r = LookForCardIDInHandAndPlayArea(ARTICUNO_LV35);
	if (r.f & 0x10u) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f, 0xC5u};
	}
	r = LookForCardIDInHandAndPlayArea(LAPRAS);
	if (r.f & 0x10u) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f, 0xC5u};
	}
	r = LookForCardIDInHandAndPlayArea(SEEL);
	uint8_t found_in_deck = 0u;
	if (!(r.f & 0x10u)) {
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, SEEL);
		if (loc.f & 0x10u) {
			wce1a = loc.a;
			found_in_deck = 1u;
		}
	}
	if (!found_in_deck) {
		r = LookForCardIDInHandAndPlayArea(DEWGONG);
		if (r.f & 0x10u) {
			uint8_t f = (r.a == 0u) ? 0x80u : 0u;
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f, 0xC5u};
		}
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DEWGONG);
		if (!(loc.f & 0x10u)) {
			uint8_t f = (loc.a == 0u) ? 0x80u : 0u;
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){loc.a, f, 0u};
		}
		wce1a = loc.a;
	}
	CheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(CHANSEY);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u, 0xC5u};
	h = CheckIfHasCardIDInHand(DITTO);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u, 0xC5u};
	h = CheckIfHasCardIDInHand(ARTICUNO_LV37);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u, 0xC5u};
	uint8_t f = (h.a == 0u) ? 0x80u : 0u;
	return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, f, 0xC5u};
}
/* <<< factory AIDecide_PokemonTrader_LegendaryArticuno */

/* >>> factory AIDecide_ComputerSearch_FireCharge */
AIDecide_ComputerSearch_FireChargeResult AIDecide_ComputerSearch_FireCharge(uint8_t b, uint8_t c, uint8_t d)
{
	uint8_t target;
	LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(CHANSEY);
	d = 0xC5u;
	if (!(h.f & 0x10u)) {
		target = CHANSEY;
	} else {
		h = LookForCardIDInHandList_Bank8(TAUROS);
		d = 0xC5u;
		if (!(h.f & 0x10u)) {
			target = TAUROS;
		} else {
			h = LookForCardIDInHandList_Bank8(JIGGLYPUFF_LV12);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				target = JIGGLYPUFF_LV12;
			} else {
				uint8_t f = (h.a == 0u) ? 0x80u : 0u;
				return (AIDecide_ComputerSearch_FireChargeResult){h.a, f, d};
			}
		}
	}

	LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, target);
	d = 0u;
	if (!(loc.f & 0x10u)) {
		uint8_t f = (loc.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){loc.a, f, d};
	}
	wce06 = loc.a;

	d = CreateHandCardList(0u).d;
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult r1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	d = r1.d;
	if (!(r1.f & 0x10u)) {
		uint8_t f = (r1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){r1.a, f, d};
	}
	wce1a = r1.a;
	RemoveFromListDifferentCardOfGivenTypeResult r2 =
		RemoveFromListDifferentCardOfGivenType(r1.b, r1.c, r1.d, r1.e, r1.hl);
	d = r2.d;
	if (!(r2.f & 0x10u)) {
		uint8_t f = (r2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){r2.a, f, d};
	}
	wce1b = r2.a;
	return (AIDecide_ComputerSearch_FireChargeResult){wce06, 0x90u, d};
}
/* <<< factory AIDecide_ComputerSearch_FireCharge */

/* >>> factory AIDecide_ComputerSearch_Anger */
AIDecide_ComputerSearch_AngerResult AIDecide_ComputerSearch_Anger(uint8_t b, uint8_t c, uint8_t d)
{
	uint8_t a_val;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RATICATE, RATTATA);
	d = r.d;
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(RATTATA, RATICATE);
	d = r2.d;
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ARCANINE_LV34, GROWLITHE);
	d = r.d;
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(GROWLITHE, ARCANINE_LV34);
	d = r2.d;
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DODRIO, DODUO);
	d = r.d;
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DODUO, DODRIO);
	d = r2.d;
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	{
		uint8_t f = (a_val == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){a_val, f, d};
	}

find_discard_cards:
	wce06 = a_val;
	d = CreateHandCardList(0u).d;
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult rm1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	d = rm1.d;
	if (!(rm1.f & 0x10u)) {
		uint8_t f = (rm1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){rm1.a, f, d};
	}
	wce1a = rm1.a;
	RemoveFromListDifferentCardOfGivenTypeResult rm2 =
		RemoveFromListDifferentCardOfGivenType(rm1.b, rm1.c, rm1.d, rm1.e, rm1.hl);
	d = rm2.d;
	if (!(rm2.f & 0x10u)) {
		uint8_t f = (rm2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){rm2.a, f, d};
	}
	wce1b = rm2.a;
	return (AIDecide_ComputerSearch_AngerResult){wce06, 0x90u, d};
}
/* <<< factory AIDecide_ComputerSearch_Anger */

/* >>> factory AIDecide_ComputerSearch_WondersOfScience */
AIDecide_ComputerSearch_WondersOfScienceResult AIDecide_ComputerSearch_WondersOfScience(uint8_t b, uint8_t c, uint8_t d)
{
	uint8_t a_val;
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a < 5u) {
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PROFESSOR_OAK);
		d = 0u;
		a_val = loc.a;
		if (loc.f & 0x10u) goto find_discard_cards;
	}

	{
		LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(GRIMER);
		d = 0xC5u;
		if (!(h.f & 0x10u)) {
			LookForCardIDInLocationBank8Result loc2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GRIMER);
			d = 0u;
			a_val = loc2.a;
			if (loc2.f & 0x10u) goto find_discard_cards;
			goto no_carry;
		}
		h = LookForCardIDInHandList_Bank8(MUK);
		d = 0xC5u;
		if (!(h.f & 0x10u)) {
			LookForCardIDInLocationBank8Result loc3 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MUK);
			d = 0u;
			a_val = loc3.a;
			if (loc3.f & 0x10u) goto find_discard_cards;
			goto no_carry;
		}
		a_val = h.a;
	}

no_carry: ;
	{
		uint8_t f = (a_val == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){a_val, f, d};
	}

find_discard_cards:
	wce06 = a_val;
	d = CreateHandCardList(0u).d;
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult rm1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	d = rm1.d;
	if (!(rm1.f & 0x10u)) {
		uint8_t f = (rm1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){rm1.a, f, d};
	}
	wce1a = rm1.a;
	RemoveFromListDifferentCardOfGivenTypeResult rm2 =
		RemoveFromListDifferentCardOfGivenType(rm1.b, rm1.c, rm1.d, rm1.e, rm1.hl);
	d = rm2.d;
	if (!(rm2.f & 0x10u)) {
		uint8_t f = (rm2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){rm2.a, f, d};
	}
	wce1b = rm2.a;
	return (AIDecide_ComputerSearch_WondersOfScienceResult){wce06, 0x90u, d};
}
/* <<< factory AIDecide_ComputerSearch_WondersOfScience */

/* >>> factory AIDecide_ComputerSearch_RockCrusher */
AIDecide_ComputerSearch_RockCrusherResult AIDecide_ComputerSearch_RockCrusher(uint8_t b, uint8_t c, uint8_t d)
{
	uint8_t final_a;
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a == 3u) {
		LookForCardIDInLocationBank8Result oak = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PROFESSOR_OAK);
		d = 0u;
		if (!(oak.f & 0x10u)) {
			final_a = oak.a;
			goto no_carry;
		}
		wce06 = oak.a;
		wce1a = 0xFFu;
		wce1b = 0xFFu;
		(void)CreateHandCardList(c);
		d = 0xC5u;
		uint16_t scan = wDuelTempList_ADDR;
		uint16_t store = wce1a_ADDR;
		d = 0xCEu;
		uint8_t trainer_to_play = wAITrainerCardToPlay;
		for (;;) {
			uint8_t idx = gb_read8(scan);
			scan = (uint16_t)(scan + 1u);
			if (idx == 0xFFu)
				break;
			uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(idx);
			if (card_id == PROFESSOR_OAK || card_id == FIGHTING_ENERGY ||
			    card_id == DOUBLE_COLORLESS_ENERGY || card_id == DIGLETT ||
			    card_id == GEODUDE || card_id == ONIX || card_id == RHYHORN) {
				final_a = card_id;
				goto no_carry;
			}
			if (card_id == trainer_to_play)
				continue;
			gb_write8(store, idx);
			store = (uint16_t)(store + 1u);
		}
		if (gb_read8(wce1b_ADDR) != 0xFFu)
			return (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x10u, d};
		final_a = 0xFFu;
		goto no_carry;
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GRAVELER);
		d = 0u;
		if (loc.f & 0x10u) {
			wce06 = loc.a;
			LookForCardIDInHandAndPlayAreaResult geo = LookForCardIDInHandAndPlayArea(GEODUDE);
			d = 0xC5u;
			if (geo.f & 0x10u) {
				LookForCardIDInHandListResult grav_hand = LookForCardIDInHandList_Bank8(GRAVELER);
				d = 0xC5u;
				if (!(grav_hand.f & 0x10u)) {
					(void)CreateHandCardList(c);
					d = 0xC5u;
					uint16_t hl = wDuelTempList_ADDR;
					(void)RemoveCardIDInList(&hl, GEODUDE);
					goto find_discard_cards_2;
				}
			}
		}
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GOLEM);
		d = 0u;
		if (loc.f & 0x10u) {
			wce06 = loc.a;
			LookForCardIDInPlayAreaResult grav_pa = LookForCardIDInPlayArea_Bank8(GRAVELER, b);
			if (grav_pa.f & 0x10u) {
				LookForCardIDInHandListResult golem_hand = LookForCardIDInHandList_Bank8(GOLEM);
				d = 0xC5u;
				if (!(golem_hand.f & 0x10u)) {
					(void)CreateHandCardList(c);
					d = 0xC5u;
					goto find_discard_cards_2;
				}
			}
		}
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DUGTRIO);
		d = 0u;
		if (!(loc.f & 0x10u)) {
			final_a = loc.a;
			goto no_carry;
		}
		wce06 = loc.a;
		LookForCardIDInPlayAreaResult dig_pa = LookForCardIDInPlayArea_Bank8(DIGLETT, b);
		if (!(dig_pa.f & 0x10u)) {
			final_a = dig_pa.a;
			goto no_carry;
		}
		LookForCardIDInHandListResult dug_hand = LookForCardIDInHandList_Bank8(DUGTRIO);
		d = 0xC5u;
		if (dug_hand.f & 0x10u) {
			final_a = dug_hand.a;
			goto no_carry;
		}
		(void)CreateHandCardList(c);
		d = 0xC5u;
		goto find_discard_cards_2;
	}

no_carry: ;
	{
		uint8_t f = (final_a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_RockCrusherResult){final_a, f, d};
	}

find_discard_cards_2:
	wce1a = 0xFFu;
	wce1b = 0xFFu;
	{
		uint16_t bc_ptr = wce1a_ADDR;
		d = 0u;
		uint8_t trainer_to_play2 = wAITrainerCardToPlay;
		for (;;) {
			RemoveFromListDifferentCardOfGivenTypeResult r =
				RemoveFromListDifferentCardOfGivenType(b, c, d, trainer_to_play2, wDuelTempList_ADDR);
			if (r.f & 0x10u) {
				gb_write8(bc_ptr, r.a);
				bc_ptr = (uint16_t)(bc_ptr + 1u);
				if (gb_read8(wce1b_ADDR) != 0xFFu)
					return (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x10u, d};
				continue;
			}
			d = (uint8_t)(d + 1u);
			if (d == 3u) {
				final_a = r.a;
				goto no_carry;
			}
		}
	}
}
/* <<< factory AIDecide_ComputerSearch_RockCrusher */

/* >>> factory AIDecide_ComputerSearch */
AIDecide_ComputerSearchResult AIDecide_ComputerSearch(uint8_t b, uint8_t c, uint8_t d)
{
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a < 3u) {
		uint8_t f = (hand_count.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearchResult){hand_count.a, f, d};
	}
	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == ROCK_CRUSHER_DECK_ID) {
		AIDecide_ComputerSearch_RockCrusherResult r = AIDecide_ComputerSearch_RockCrusher(b, c, d);
		return (AIDecide_ComputerSearchResult){r.a, r.f, r.d};
	}
	if (deck_id == WONDERS_OF_SCIENCE_DECK_ID) {
		AIDecide_ComputerSearch_WondersOfScienceResult r = AIDecide_ComputerSearch_WondersOfScience(b, c, d);
		return (AIDecide_ComputerSearchResult){r.a, r.f, r.d};
	}
	if (deck_id == FIRE_CHARGE_DECK_ID) {
		AIDecide_ComputerSearch_FireChargeResult r = AIDecide_ComputerSearch_FireCharge(b, c, d);
		return (AIDecide_ComputerSearchResult){r.a, r.f, r.d};
	}
	if (deck_id == ANGER_DECK_ID) {
		AIDecide_ComputerSearch_AngerResult r = AIDecide_ComputerSearch_Anger(b, c, d);
		return (AIDecide_ComputerSearchResult){r.a, r.f, r.d};
	}
	uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
	return (AIDecide_ComputerSearchResult){deck_id, f, d};
}
/* <<< factory AIDecide_ComputerSearch */

/* >>> factory AIDecide_PokemonTrader_LegendaryRonald */
AIDecide_PokemonTrader_LegendaryRonaldResult AIDecide_PokemonTrader_LegendaryRonald(uint8_t d)
{
	uint8_t target_a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(FLAREON_LV22, EEVEE);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VAPOREON_LV29, EEVEE);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(JOLTEON_LV24, EEVEE);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, FLAREON_LV22);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, VAPOREON_LV29);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, JOLTEON_LV24);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONAIR, DRATINI);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONITE_LV41, DRAGONAIR);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DRATINI, DRAGONAIR);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DRAGONAIR, DRAGONITE_LV41);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	goto no_carry;

choose_hand: ;
	wce1a = target_a;
	{
		LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(ZAPDOS_LV68);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u, d};
		h = LookForCardIDInHandList_Bank8(ARTICUNO_LV37);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u, d};
		h = LookForCardIDInHandList_Bank8(MOLTRES_LV37);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u, d};
		target_a = h.a;
	}

no_carry: ;
	{
		uint8_t f = (target_a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryRonaldResult){target_a, f, d};
	}
}
/* <<< factory AIDecide_PokemonTrader_LegendaryRonald */

/* >>> factory AIDecide_PokemonTrader_SoundOfTheWaves */
AIDecide_PokemonTrader_SoundOfTheWavesResult AIDecide_PokemonTrader_SoundOfTheWaves(uint8_t d)
{
	uint8_t target_a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DEWGONG, SEEL);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(SEEL, DEWGONG);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(KINGLER, KRABBY);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(KRABBY, KINGLER);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CLOYSTER, SHELLDER);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(SHELLDER, CLOYSTER);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(SEADRA, HORSEA);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(HORSEA, SEADRA);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(TENTACRUEL, TENTACOOL);
	d = r.d;
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(TENTACOOL, TENTACRUEL);
	d = r2.d;
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	goto no_carry;

choose_hand: ;
	wce1a = target_a;
	{
		CheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(SEEL);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(KRABBY);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(HORSEA);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(SHELLDER);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(TENTACOOL);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f, d};
		target_a = h.a;
	}

no_carry: ;
	{
		uint8_t f = (target_a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_SoundOfTheWavesResult){target_a, f, d};
	}
}
/* <<< factory AIDecide_PokemonTrader_SoundOfTheWaves */

/* >>> factory AIDecide_PokemonTrader_LegendaryDragonite */
AIDecide_PokemonTrader_LegendaryDragoniteResult AIDecide_PokemonTrader_LegendaryDragonite(uint8_t d)
{
	uint8_t final_a;
	CountOppEnergyCardsInHandAndAttachedResult energy = CountOppEnergyCardsInHandAndAttached();
	d = 0u;
	uint8_t need_kangaskhan = 0u;
	if (energy.a < 5u) {
		need_kangaskhan = 1u;
	} else {
		uint8_t pokemon_count = CountPokemonCardsInHandAndInPlayArea(0u);
		d = (gb_read8(wDuelTempList_ADDR) != 0xFFu) ? 0u : 0xC5u;
		if (pokemon_count < 5u)
			need_kangaskhan = 1u;
	}

	if (!need_kangaskhan) {
		LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
		LookForCardIDInDeck_GivenCardIDInHandResult r2;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(GYARADOS, MAGIKARP);
		d = r.d;
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(MAGIKARP, GYARADOS);
		d = r2.d;
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONAIR, DRATINI);
		d = r.d;
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONITE_LV41, DRAGONAIR);
		d = r.d;
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(DRATINI, DRAGONAIR);
		d = r2.d;
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(DRAGONAIR, DRAGONITE_LV41);
		d = r2.d;
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARMELEON, CHARMANDER);
		d = r.d;
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARIZARD, CHARMELEON);
		d = r.d;
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(CHARMANDER, CHARMELEON);
		d = r2.d;
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(CHARMELEON, CHARIZARD);
		d = r2.d;
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		goto no_carry;
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, KANGASKHAN);
		d = 0u;
		if (!(loc.f & 0x10u)) {
			final_a = loc.a;
			goto no_carry;
		}
		final_a = loc.a;
	}

choose_hand: ;
	wce1a = final_a;
	{
		CheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(DRAGONAIR);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(CHARMELEON);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(GYARADOS);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(MAGIKARP);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(CHARMANDER);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f, d};
		h = CheckIfHasCardIDInHand(DRATINI);
		d = 0xC5u;
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f, d};
		final_a = h.a;
	}

no_carry: ;
	{
		uint8_t f = (final_a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryDragoniteResult){final_a, f, d};
	}
}
/* <<< factory AIDecide_PokemonTrader_LegendaryDragonite */

/* >>> factory AIDecide_Pokeball */
AIDecide_PokeballResult AIDecide_Pokeball(uint8_t d)
{
	uint8_t deck_id = wOpponentDeckID;

	if (deck_id == FIRE_CHARGE_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, CHANSEY);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, TAUROS);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, JIGGLYPUFF_LV12);
		d = 0u;
		return (AIDecide_PokeballResult){r.a, r.f, d};
	}

	if (deck_id == HARD_POKEMON_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, RHYHORN);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, RHYDON);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, ONIX);
		d = 0u;
		return (AIDecide_PokeballResult){r.a, r.f, d};
	}

	if (deck_id == PIKACHU_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV14);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV16);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_ALT_LV16);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV12);
		d = 0u;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, FLYING_PIKACHU);
		d = 0u;
		return (AIDecide_PokeballResult){r.a, r.f, d};
	}

	if (deck_id == ETCETERA_DECK_ID) {
		LookForCardIDInHandListResult h;
		LookForCardIDInLocationBank8Result r;

		h = LookForCardIDInHandList_Bank8(FIRE_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(CHARMANDER);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MAGMAR_LV31);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, CHARMANDER);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MAGMAR_LV31);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(LIGHTNING_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(PIKACHU_LV12);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MAGNEMITE_LV13);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV12);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MAGNEMITE_LV13);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(FIGHTING_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(DIGLETT);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MACHOP);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DIGLETT);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MACHOP);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(PSYCHIC_ENERGY);
		d = 0xC5u;
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(GASTLY_LV8);
			d = 0xC5u;
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(JYNX);
				d = 0xC5u;
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GASTLY_LV8);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, JYNX);
					d = 0u;
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
				}
			}
		}

		uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
		return (AIDecide_PokeballResult){deck_id, f, d};
	}

	if (deck_id == LOVELY_NIDORAN_DECK_ID) {
		LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
		LookForCardIDInDeck_GivenCardIDInHandResult r2;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDORINO, NIDORANM);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDOKING, NIDORINO);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORANM, NIDORINO);
		d = r2.d;
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORINO, NIDOKING);
		d = r2.d;
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f, d};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDORINA, NIDORANF);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDOQUEEN, NIDORINA);
		d = r.d;
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORANF, NIDORINA);
		d = r2.d;
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f, d};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORINA, NIDOQUEEN);
		d = r2.d;
		return (AIDecide_PokeballResult){r2.a, r2.f, d};
	}

	uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
	return (AIDecide_PokeballResult){deck_id, f, d};
}
/* <<< factory AIDecide_Pokeball */

/* >>> factory AIDecide_MrFuji */
AIDecideParameterResult AIDecide_MrFuji(uint8_t d)
{
	gb_write8(0xCE06u, 0xFFu);
	gb_write8(0xCE08u, 0xFFu);

	DuelistVarResult r1 = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t count = r1.a;
	if (count == 1u)
		return (AIDecideParameterResult){count, 0xC0u, d};

	d = (uint8_t)(count - 1u);
	uint8_t e = PLAY_AREA_BENCH_1;

	while (d != 0u) {
		DuelistVarResult r2 = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e));
		(void)LoadCardDataToBuffer1_FromDeckIndex(r2.a);

		uint8_t maxHP = wLoadedCard1HP;

		CardDamageResult dmg = GetCardDamageAndMaxHP(e);
		uint8_t counters = ConvertHPToDamageCounters_Bank8(dmg.a);
		if (counters != 0u) {
			CalculateBDividedByA_Bank8Result div = CalculateBDividedByA_Bank8(counters, maxHP);
			if (div.a < 20u && div.a < gb_read8(0xCE08u)) {
				gb_write8(0xCE08u, div.a);
				gb_write8(0xCE06u, e);
			}
		}
		e++;
		d--;
	}

	uint8_t chosen = gb_read8(0xCE06u);
	if (chosen == 0xFFu)
		return (AIDecideParameterResult){chosen, 0xC0u, 0u};
	return (AIDecideParameterResult){chosen, 0x10u, 0u};
}
/* <<< factory AIDecide_MrFuji */

/* >>> factory AIDecide_PokemonTrader_BlisteringPokemon */
AIDecide_PokemonTrader_BlisteringPokemonResult AIDecide_PokemonTrader_BlisteringPokemon(uint8_t d)
{
	uint8_t a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r1 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RHYDON, RHYHORN);
	a = r1.a;
	if (!(r1.f & 0x10u)) {
		LookForCardIDInDeck_GivenCardIDInHandResult r2 =
			LookForCardIDInDeck_GivenCardIDInHand(RHYHORN, RHYDON);
		a = r2.a;
		if (!(r2.f & 0x10u)) {
			LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r3 =
				LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAROWAK_LV26, CUBONE);
			a = r3.a;
			if (!(r3.f & 0x10u)) {
				LookForCardIDInDeck_GivenCardIDInHandResult r4 =
					LookForCardIDInDeck_GivenCardIDInHand(CUBONE, MAROWAK_LV26);
				a = r4.a;
				if (!(r4.f & 0x10u)) {
					LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r5 =
						LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RAPIDASH, PONYTA);
					a = r5.a;
					if (!(r5.f & 0x10u)) {
						LookForCardIDInDeck_GivenCardIDInHandResult r6 =
							LookForCardIDInDeck_GivenCardIDInHand(PONYTA, RAPIDASH);
						a = r6.a;
						if (!(r6.f & 0x10u))
							return (AIDecide_PokemonTrader_BlisteringPokemonResult){a, 0x00u, r6.d};
					}
				}
			}
		}
	}
	wce1a = a;
	FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
	if (dup.f & 0x10u)
		return (AIDecide_PokemonTrader_BlisteringPokemonResult){dup.a, 0x10u, dup.d};
	return (AIDecide_PokemonTrader_BlisteringPokemonResult){dup.a, 0x00u, dup.d};
}
/* <<< factory AIDecide_PokemonTrader_BlisteringPokemon */

/* >>> factory AIDecide_PokemonTrader_Flamethrower */
AIDecide_PokemonTrader_FlamethrowerResult AIDecide_PokemonTrader_Flamethrower(uint8_t d)
{
	uint8_t a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r1 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARMELEON, CHARMANDER);
	d = r1.d;
	a = r1.a;
	if (!(r1.f & 0x10u)) {
		LookForCardIDInDeck_GivenCardIDInHandResult r2 =
			LookForCardIDInDeck_GivenCardIDInHand(CHARMANDER, CHARMELEON);
		d = r2.d;
		a = r2.a;
		if (!(r2.f & 0x10u)) {
			LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r3 =
				LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARIZARD, CHARMELEON);
			d = r3.d;
			a = r3.a;
			if (!(r3.f & 0x10u)) {
				LookForCardIDInDeck_GivenCardIDInHandResult r4 =
					LookForCardIDInDeck_GivenCardIDInHand(CHARMELEON, CHARIZARD);
				d = r4.d;
				a = r4.a;
				if (!(r4.f & 0x10u)) {
					LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r5 =
						LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NINETALES_LV32, VULPIX);
					d = r5.d;
					a = r5.a;
					if (!(r5.f & 0x10u)) {
						LookForCardIDInDeck_GivenCardIDInHandResult r6 =
							LookForCardIDInDeck_GivenCardIDInHand(VULPIX, NINETALES_LV32);
						d = r6.d;
						a = r6.a;
						if (!(r6.f & 0x10u)) {
							LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r7 =
								LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ARCANINE_LV45, GROWLITHE);
							d = r7.d;
							a = r7.a;
							if (!(r7.f & 0x10u)) {
								LookForCardIDInDeck_GivenCardIDInHandResult r8 =
									LookForCardIDInDeck_GivenCardIDInHand(GROWLITHE, ARCANINE_LV45);
								d = r8.d;
								a = r8.a;
								if (!(r8.f & 0x10u)) {
									LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r9 =
										LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(FLAREON_LV28, EEVEE);
									d = r9.d;
									a = r9.a;
									if (!(r9.f & 0x10u)) {
										LookForCardIDInDeck_GivenCardIDInHandResult r10 =
											LookForCardIDInDeck_GivenCardIDInHand(EEVEE, FLAREON_LV28);
										d = r10.d;
										a = r10.a;
										if (!(r10.f & 0x10u)) {
											return (AIDecide_PokemonTrader_FlamethrowerResult){a, 0x00u, d};
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
	wce1a = a;
	FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
	d = dup.d;
	if (dup.f & 0x10u)
		return (AIDecide_PokemonTrader_FlamethrowerResult){dup.a, 0x10u, d};
	return (AIDecide_PokemonTrader_FlamethrowerResult){dup.a, 0x00u, d};
}
/* <<< factory AIDecide_PokemonTrader_Flamethrower */

/* >>> factory AIDecide_PokemonTrader_FlowerGarden */
AIDecide_PokemonTrader_FlowerGardenResult AIDecide_PokemonTrader_FlowerGarden(uint8_t d)
{
	uint8_t a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(IVYSAUR, BULBASAUR);
	d = r.d;
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VENUSAUR_LV67, IVYSAUR);
	d = r.d;
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(BULBASAUR, IVYSAUR);
	d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(IVYSAUR, VENUSAUR_LV67);
	d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(WEEPINBELL, BELLSPROUT);
	d = r.d;
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VICTREEBEL, WEEPINBELL);
	d = r.d;
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(BELLSPROUT, WEEPINBELL);
	d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(WEEPINBELL, VICTREEBEL);
	d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(GLOOM, ODDISH);
	d = r.d;
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VILEPLUME, GLOOM);
	d = r.d;
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(ODDISH, GLOOM);
	d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(GLOOM, VILEPLUME);
	d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	return (AIDecide_PokemonTrader_FlowerGardenResult){a, 0x00u, d};

find_duplicates:
	wce1a = a;
	{
		FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
		d = dup.d;
		if (dup.f & 0x10u)
			return (AIDecide_PokemonTrader_FlowerGardenResult){dup.a, 0x10u, d};
		return (AIDecide_PokemonTrader_FlowerGardenResult){dup.a, 0x00u, d};
	}
}
/* <<< factory AIDecide_PokemonTrader_FlowerGarden */

/* >>> factory AIDecide_PokemonTrader_PowerGenerator */
AIDecide_PokemonTrader_PowerGeneratorResult AIDecide_PokemonTrader_PowerGenerator(uint8_t d)
{
	uint8_t a = 0u;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r1 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RAICHU_LV40, PIKACHU_LV14);
	d = r1.d;
	a = r1.a;
	if (r1.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r2 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RAICHU_LV40, PIKACHU_LV12);
		d = r2.d;
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r3 =
		LookForCardIDInDeck_GivenCardIDInHand(PIKACHU_LV14, RAICHU_LV40);
		d = r3.d;
	a = r3.a;
	if (r3.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r4 =
		LookForCardIDInDeck_GivenCardIDInHand(PIKACHU_LV12, RAICHU_LV40);
		d = r4.d;
	a = r4.a;
	if (r4.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r5 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ELECTRODE_LV42, VOLTORB);
		d = r5.d;
	a = r5.a;
	if (r5.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r6 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ELECTRODE_LV35, VOLTORB);
		d = r6.d;
	a = r6.a;
	if (r6.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r7 =
		LookForCardIDInDeck_GivenCardIDInHand(VOLTORB, ELECTRODE_LV42);
		d = r7.d;
	a = r7.a;
	if (r7.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r8 =
		LookForCardIDInDeck_GivenCardIDInHand(VOLTORB, ELECTRODE_LV35);
		d = r8.d;
	a = r8.a;
	if (r8.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r9 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV35, MAGNEMITE_LV13);
		d = r9.d;
	a = r9.a;
	if (r9.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r10 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV35, MAGNEMITE_LV15);
		d = r10.d;
	a = r10.a;
	if (r10.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r11 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV28, MAGNEMITE_LV13);
		d = r11.d;
	a = r11.a;
	if (r11.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r12 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV28, MAGNEMITE_LV15);
		d = r12.d;
	a = r12.a;
	if (r12.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r13 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV15, MAGNETON_LV35);
		d = r13.d;
	a = r13.a;
	if (r13.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r14 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV13, MAGNETON_LV35);
		d = r14.d;
	a = r14.a;
	if (r14.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r15 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV15, MAGNETON_LV28);
		d = r15.d;
	a = r15.a;
	if (r15.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r16 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV13, MAGNETON_LV28);
		d = r16.d;
	a = r16.a;
	if (r16.f & 0x10u) goto find_duplicates;

find_duplicates:
	wce1a = a;
	{
		FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
		d = dup.d;
		if (dup.f & 0x10u)
			return (AIDecide_PokemonTrader_PowerGeneratorResult){dup.a, 0x10u, d};
		return (AIDecide_PokemonTrader_PowerGeneratorResult){dup.a, 0x00u, d};
	}
}
/* <<< factory AIDecide_PokemonTrader_PowerGenerator */

/* >>> factory AIDecide_PokemonTrader */
AIDecide_PokemonTraderResult AIDecide_PokemonTrader(uint8_t d)
{
	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == LEGENDARY_MOLTRES_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryMoltresResult r = AIDecide_PokemonTrader_LegendaryMoltres(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == LEGENDARY_ARTICUNO_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryArticunoResult r = AIDecide_PokemonTrader_LegendaryArticuno(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == LEGENDARY_DRAGONITE_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryDragoniteResult r = AIDecide_PokemonTrader_LegendaryDragonite(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == LEGENDARY_RONALD_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryRonaldResult r = AIDecide_PokemonTrader_LegendaryRonald(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == BLISTERING_POKEMON_DECK_ID) {
		AIDecide_PokemonTrader_BlisteringPokemonResult r = AIDecide_PokemonTrader_BlisteringPokemon(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == SOUND_OF_THE_WAVES_DECK_ID) {
		AIDecide_PokemonTrader_SoundOfTheWavesResult r = AIDecide_PokemonTrader_SoundOfTheWaves(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == POWER_GENERATOR_DECK_ID) {
		AIDecide_PokemonTrader_PowerGeneratorResult r = AIDecide_PokemonTrader_PowerGenerator(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == FLOWER_GARDEN_DECK_ID) {
		AIDecide_PokemonTrader_FlowerGardenResult r = AIDecide_PokemonTrader_FlowerGarden(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == STRANGE_POWER_DECK_ID) {
		AIDecide_PokemonTrader_StrangePowerResult r = AIDecide_PokemonTrader_StrangePower(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	if (deck_id == FLAMETHROWER_DECK_ID) {
		AIDecide_PokemonTrader_FlamethrowerResult r = AIDecide_PokemonTrader_Flamethrower(d);
		return (AIDecide_PokemonTraderResult){r.a, r.f, r.d};
	}
	return (AIDecide_PokemonTraderResult){deck_id, (uint8_t)(deck_id == 0u ? 0x80u : 0x00u), d};
}
/* <<< factory AIDecide_PokemonTrader */

/* >>> factory AIDecide_EnergySearch */
AIDecideEnergySearchResult AIDecide_EnergySearch(uint8_t a, uint8_t d)
{
	CoreCardListResult hand = CreateEnergyCardListFromHand(a);
	uint8_t e;
	uint8_t mode;
	uint8_t found;
	uint8_t found_flags;
	uint16_t hl;

	if (!(hand.f & 0x10u)) {
		d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		e = PLAY_AREA_ARENA;
		for (;;) {
			uint8_t slot = (uint8_t)(DUELVARS_ARENA_CARD + e);
			uint8_t deck_index = GetTurnDuelistVariable(slot).a;
			uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
			wTempCardID = card_id;
			LoadCardDataToBuffer1_FromCardID(card_id);
			wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);
			hl = wDuelTempList_ADDR;
			for (;;) {
				uint8_t entry = gb_read8(hl++);
				if (entry == 0xFFu)
					break;
				CheckIfEnergyIsUsefulResult useful = CheckIfEnergyIsUseful(entry);
				if (useful.f & 0x10u)
					return (AIDecideEnergySearchResult){entry, (uint8_t)(entry == 0u ? 0x80u : 0x00u), d};
			}
			e++;
			if (e == d)
				break;
		}
	}

	if (wOpponentDeckID == HEATED_BATTLE_DECK_ID)
		mode = 1u;
	else if (wOpponentDeckID == WONDERS_OF_SCIENCE_DECK_ID)
		mode = 1u;
	else
		mode = 0u;

	FindBasicEnergyCardsInLocationResult deck = FindBasicEnergyCardsInLocation(CARD_LOCATION_DECK);
	if (deck.f & 0x10u)
		return (AIDecideEnergySearchResult){0u, 0x80u, deck.d};

	d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	e = PLAY_AREA_ARENA;
	for (;;) {
		uint8_t slot = (uint8_t)(DUELVARS_ARENA_CARD + e);
		uint8_t deck_index = GetTurnDuelistVariable(slot).a;
		uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(deck_index);
		wTempCardID = card_id;
		LoadCardDataToBuffer1_FromCardID(card_id);
		wTempCardType = (uint8_t)(wLoadedCard1Type | TYPE_ENERGY);
		if (mode == 1u && wTempCardType != TYPE_ENERGY_FIRE && wTempCardType != TYPE_ENERGY_LIGHTNING)
			goto next_play_area;
		if (mode == 2u && wTempCardType != TYPE_ENERGY_GRASS)
			goto next_play_area;
		hl = wDuelTempList_ADDR;
		for (;;) {
			uint8_t entry = gb_read8(hl++);
			if (entry == 0xFFu)
				break;
			CheckIfEnergyIsUsefulResult useful = CheckIfEnergyIsUseful(entry);
			if (useful.f & 0x10u) {
				found = entry;
				found_flags = (uint8_t)(entry == 0u ? 0x90u : 0x10u);
				return (AIDecideEnergySearchResult){found, (uint8_t)(found_flags | 0x10u), d};
			}
		}

	next_play_area:
		e++;
		if (e == d)
			break;
	}

	if (mode == 1u)
		return (AIDecideEnergySearchResult){d, (uint8_t)(d == 0u ? 0x80u : 0x00u), d};
	return (AIDecideEnergySearchResult){wDuelTempList, 0x90u, d};
}
/* <<< factory AIDecide_EnergySearch */

/* >>> factory _AIProcessHandTrainerCards */
/* Adapters: every decide routine yields (a, f) -- a is the parameter stored
 * in wAITrainerCardParameter on carry -- and every play routine yields f.
 * Register arguments the C signatures still carry are the asm's incidental
 * inputs; the loop hands them the scratch values it has. */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; } TrainerDecision;
static TrainerDecision decide_AIDecide_Bill(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Bill(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ClefairyDollOrMysteriousFossil(uint8_t d, uint8_t e) { AIDecidePokemonFluteResult r = AIDecide_ClefairyDollOrMysteriousFossil(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ComputerSearch(uint8_t d, uint8_t e) { AIDecide_ComputerSearchResult r = AIDecide_ComputerSearch(0u, 0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Defender_Phase13(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Defender_Phase13(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Defender_Phase14(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Defender_Phase14(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_EnergyRemoval(uint8_t d, uint8_t e) { AIDecideEnergyRemovalResult r = AIDecide_EnergyRemoval(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_EnergyRetrieval(uint8_t d, uint8_t e) { AIDecideEnergyRetrievalResult r = AIDecide_EnergyRetrieval(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_EnergySearch(uint8_t d, uint8_t e) { AIDecideEnergySearchResult r = AIDecide_EnergySearch(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_FullHeal(uint8_t d, uint8_t e) { AIDecideFullHealResult r = AIDecide_FullHeal(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Gambler(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Gambler(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_GustOfWind(uint8_t d, uint8_t e) { AIDecideGustOfWindResult r = AIDecide_GustOfWind(d, e); return (TrainerDecision){r.a, r.f, r.d, r.e}; }
static TrainerDecision decide_AIDecide_Imakuni(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Imakuni(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ImposterProfessorOak(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_ImposterProfessorOak(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ItemFinder(uint8_t d, uint8_t e) { AIDecide_ItemFinderResult r = AIDecide_ItemFinder(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Lass(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Lass(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Maintenance(uint8_t d, uint8_t e) { AIDecideMaintenanceResult r = AIDecide_Maintenance(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_MrFuji(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_MrFuji(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PlusPower_Phase13(uint8_t d, uint8_t e) { AIDecide_PlusPower_Phase13Result r = AIDecide_PlusPower_Phase13(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PlusPower_Phase14(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_PlusPower_Phase14(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Pokeball(uint8_t d, uint8_t e) { AIDecide_PokeballResult r = AIDecide_Pokeball(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Pokedex(uint8_t d, uint8_t e) { AIDecidePokedexResult r = AIDecide_Pokedex(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonBreeder(uint8_t d, uint8_t e) { AIDecidePokemonBreederResult r = AIDecide_PokemonBreeder(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonCenter(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_PokemonCenter(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonFlute(uint8_t d, uint8_t e) { AIDecidePokemonFluteResult r = AIDecide_PokemonFlute(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_PokemonTrader(uint8_t d, uint8_t e) { AIDecide_PokemonTraderResult r = AIDecide_PokemonTrader(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Potion_Phase07(uint8_t d, uint8_t e) { AIDecidePotionPhase07Result r = AIDecide_Potion_Phase07(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Potion_Phase10(uint8_t d, uint8_t e) { AIDecidePotionPhase10Result r = AIDecide_Potion_Phase10(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ProfessorOak(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_ProfessorOak(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Recycle(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_Recycle(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Revive(uint8_t d, uint8_t e) { AIDecideReviveResult r = AIDecide_Revive(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_ScoopUp(uint8_t d, uint8_t e) { AIDecide_ScoopUpResult r = AIDecide_ScoopUp(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperEnergyRemoval(uint8_t d, uint8_t e) { AIDecideParameterResult r = AIDecide_SuperEnergyRemoval(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperEnergyRetrieval(uint8_t d, uint8_t e) { AIDecideSuperEnergyRetrievalResult r = AIDecide_SuperEnergyRetrieval(0u, d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperPotion_Phase08(uint8_t d, uint8_t e) { AIDecideSuperPotionPhase08Result r = AIDecide_SuperPotion_Phase08(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_SuperPotion_Phase11(uint8_t d, uint8_t e) { AIDecideSuperPotionPhase11Result r = AIDecide_SuperPotion_Phase11(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static TrainerDecision decide_AIDecide_Switch(uint8_t d, uint8_t e) { AIDecide_SwitchResult r = AIDecide_Switch(d); return (TrainerDecision){r.a, r.f, r.d, e}; }
static uint8_t play_AIPlay_Bill(uint8_t d, uint8_t e) { return AIPlay_Bill(d, e).f; }
static uint8_t play_AIPlay_ClefairyDollOrMysteriousFossil(uint8_t d, uint8_t e) { return AIPlay_ClefairyDollOrMysteriousFossil(d, e).f; }
static uint8_t play_AIPlay_ComputerSearch(uint8_t d, uint8_t e) { return AIPlay_ComputerSearch(d, e).f; }
static uint8_t play_AIPlay_Defender(uint8_t d, uint8_t e) { return AIPlay_Defender(d, e).f; }
static uint8_t play_AIPlay_EnergyRemoval(uint8_t d, uint8_t e) { return AIPlay_EnergyRemoval(d, e).f; }
static uint8_t play_AIPlay_EnergyRetrieval(uint8_t d, uint8_t e) { return AIPlay_EnergyRetrieval(d, e).f; }
static uint8_t play_AIPlay_EnergySearch(uint8_t d, uint8_t e) { return AIPlay_EnergySearch(d, e).f; }
static uint8_t play_AIPlay_FullHeal(uint8_t d, uint8_t e) { return AIPlay_FullHeal(d, e).f; }
static uint8_t play_AIPlay_Gambler(uint8_t d, uint8_t e) { return AIPlay_Gambler(d, e).f; }
static uint8_t play_AIPlay_GustOfWind(uint8_t d, uint8_t e) { return AIPlay_GustOfWind(d, e).f; }
static uint8_t play_AIPlay_Imakuni(uint8_t d, uint8_t e) { return AIPlay_Imakuni(d, e).f; }
static uint8_t play_AIPlay_ImposterProfessorOak(uint8_t d, uint8_t e) { return AIPlay_ImposterProfessorOak(d, e).f; }
static uint8_t play_AIPlay_ItemFinder(uint8_t d, uint8_t e) { return AIPlay_ItemFinder(d, e).f; }
static uint8_t play_AIPlay_Lass(uint8_t d, uint8_t e) { return AIPlay_Lass(d, e).f; }
static uint8_t play_AIPlay_Maintenance(uint8_t d, uint8_t e) { return AIPlay_Maintenance(d, e).f; }
static uint8_t play_AIPlay_MrFuji(uint8_t d, uint8_t e) { return AIPlay_MrFuji(d, e).f; }
static uint8_t play_AIPlay_PlusPower(uint8_t d, uint8_t e) { return AIPlay_PlusPower(d, e).f; }
static uint8_t play_AIPlay_Pokeball(uint8_t d, uint8_t e) { return AIPlay_Pokeball(d, e).f; }
static uint8_t play_AIPlay_Pokedex(uint8_t d, uint8_t e) { return AIPlay_Pokedex(d, e).f; }
static uint8_t play_AIPlay_PokemonBreeder(uint8_t d, uint8_t e) { return AIPlay_PokemonBreeder(d, e).f; }
static uint8_t play_AIPlay_PokemonCenter(uint8_t d, uint8_t e) { return AIPlay_PokemonCenter(d, e).f; }
static uint8_t play_AIPlay_PokemonFlute(uint8_t d, uint8_t e) { return AIPlay_PokemonFlute(d, e).f; }
static uint8_t play_AIPlay_PokemonTrader(uint8_t d, uint8_t e) { return AIPlay_PokemonTrader(d, e).f; }
static uint8_t play_AIPlay_Potion(uint8_t d, uint8_t e) { return AIPlay_Potion(d, e).f; }
static uint8_t play_AIPlay_ProfessorOak(uint8_t d, uint8_t e) { return AIPlay_ProfessorOak(d, e).f; }
static uint8_t play_AIPlay_Recycle(uint8_t d, uint8_t e) { return AIPlay_Recycle(d, e).f; }
static uint8_t play_AIPlay_Revive(uint8_t d, uint8_t e) { return AIPlay_Revive(d, e).f; }
static uint8_t play_AIPlay_ScoopUp(uint8_t d, uint8_t e) { return AIPlay_ScoopUp(d, e).f; }
static uint8_t play_AIPlay_SuperEnergyRemoval(uint8_t d, uint8_t e) { return AIPlay_SuperEnergyRemoval(d, e).f; }
static uint8_t play_AIPlay_SuperEnergyRetrieval(uint8_t d, uint8_t e) { return AIPlay_SuperEnergyRetrieval(d, e).f; }
static uint8_t play_AIPlay_SuperPotion(uint8_t d, uint8_t e) { return AIPlay_SuperPotion(d, e).f; }
static uint8_t play_AIPlay_Switch(uint8_t d, uint8_t e) { return AIPlay_Switch(d, e).f; }

typedef struct {
	uint8_t phase;
	uint8_t card;
	TrainerDecision (*decide)(uint8_t d, uint8_t e);
	uint8_t (*play)(uint8_t d, uint8_t e);
} TrainerLogic;

/* data/duel/ai_trainer_card_logic.asm, in table order. */
static const TrainerLogic trainer_logic[] = {
	{0x07u, 0xDDu, decide_AIDecide_Potion_Phase07, play_AIPlay_Potion}, /* POTION */
	{0x0Au, 0xDDu, decide_AIDecide_Potion_Phase10, play_AIPlay_Potion}, /* POTION */
	{0x08u, 0xDEu, decide_AIDecide_SuperPotion_Phase08, play_AIPlay_SuperPotion}, /* SUPER_POTION */
	{0x0Bu, 0xDEu, decide_AIDecide_SuperPotion_Phase11, play_AIPlay_SuperPotion}, /* SUPER_POTION */
	{0x0Du, 0xD9u, decide_AIDecide_Defender_Phase13, play_AIPlay_Defender}, /* DEFENDER */
	{0x0Eu, 0xD9u, decide_AIDecide_Defender_Phase14, play_AIPlay_Defender}, /* DEFENDER */
	{0x0Du, 0xD8u, decide_AIDecide_PlusPower_Phase13, play_AIPlay_PlusPower}, /* PLUSPOWER */
	{0x0Eu, 0xD8u, decide_AIDecide_PlusPower_Phase14, play_AIPlay_PlusPower}, /* PLUSPOWER */
	{0x09u, 0xD2u, decide_AIDecide_Switch, play_AIPlay_Switch}, /* SWITCH */
	{0x07u, 0xDBu, decide_AIDecide_GustOfWind, play_AIPlay_GustOfWind}, /* GUST_OF_WIND */
	{0x0Au, 0xDBu, decide_AIDecide_GustOfWind, play_AIPlay_GustOfWind}, /* GUST_OF_WIND */
	{0x04u, 0xC5u, decide_AIDecide_Bill, play_AIPlay_Bill}, /* BILL */
	{0x05u, 0xD0u, decide_AIDecide_EnergyRemoval, play_AIPlay_EnergyRemoval}, /* ENERGY_REMOVAL */
	{0x05u, 0xD1u, decide_AIDecide_SuperEnergyRemoval, play_AIPlay_SuperEnergyRemoval}, /* SUPER_ENERGY_REMOVAL */
	{0x07u, 0xCAu, decide_AIDecide_PokemonBreeder, play_AIPlay_PokemonBreeder}, /* POKEMON_BREEDER */
	{0x0Fu, 0xC3u, decide_AIDecide_ProfessorOak, play_AIPlay_ProfessorOak}, /* PROFESSOR_OAK */
	{0x0Au, 0xCDu, decide_AIDecide_EnergyRetrieval, play_AIPlay_EnergyRetrieval}, /* ENERGY_RETRIEVAL */
	{0x0Bu, 0xCEu, decide_AIDecide_SuperEnergyRetrieval, play_AIPlay_SuperEnergyRetrieval}, /* SUPER_ENERGY_RETRIEVAL */
	{0x06u, 0xD3u, decide_AIDecide_PokemonCenter, play_AIPlay_PokemonCenter}, /* POKEMON_CENTER */
	{0x07u, 0xC4u, decide_AIDecide_ImposterProfessorOak, play_AIPlay_ImposterProfessorOak}, /* IMPOSTER_PROFESSOR_OAK */
	{0x0Cu, 0xCFu, decide_AIDecide_EnergySearch, play_AIPlay_EnergySearch}, /* ENERGY_SEARCH */
	{0x03u, 0xD7u, decide_AIDecide_Pokedex, play_AIPlay_Pokedex}, /* POKEDEX */
	{0x07u, 0xDFu, decide_AIDecide_FullHeal, play_AIPlay_FullHeal}, /* FULL_HEAL */
	{0x0Au, 0xC6u, decide_AIDecide_MrFuji, play_AIPlay_MrFuji}, /* MR_FUJI */
	{0x0Au, 0xD5u, decide_AIDecide_ScoopUp, play_AIPlay_ScoopUp}, /* SCOOP_UP */
	{0x02u, 0xE1u, decide_AIDecide_Maintenance, play_AIPlay_Maintenance}, /* MAINTENANCE */
	{0x03u, 0xE4u, decide_AIDecide_Recycle, play_AIPlay_Recycle}, /* RECYCLE */
	{0x0Du, 0xC7u, decide_AIDecide_Lass, play_AIPlay_Lass}, /* LASS */
	{0x04u, 0xDAu, decide_AIDecide_ItemFinder, play_AIPlay_ItemFinder}, /* ITEM_FINDER */
	{0x01u, 0xC8u, decide_AIDecide_Imakuni, play_AIPlay_Imakuni}, /* IMAKUNI_CARD */
	{0x01u, 0xE3u, decide_AIDecide_Gambler, play_AIPlay_Gambler}, /* GAMBLER */
	{0x05u, 0xE0u, decide_AIDecide_Revive, play_AIPlay_Revive}, /* REVIVE */
	{0x0Du, 0xE2u, decide_AIDecide_PokemonFlute, play_AIPlay_PokemonFlute}, /* POKEMON_FLUTE */
	{0x05u, 0xCBu, decide_AIDecide_ClefairyDollOrMysteriousFossil, play_AIPlay_ClefairyDollOrMysteriousFossil}, /* CLEFAIRY_DOLL */
	{0x05u, 0xCCu, decide_AIDecide_ClefairyDollOrMysteriousFossil, play_AIPlay_ClefairyDollOrMysteriousFossil}, /* MYSTERIOUS_FOSSIL */
	{0x02u, 0xD4u, decide_AIDecide_Pokeball, play_AIPlay_Pokeball}, /* POKE_BALL */
	{0x02u, 0xD6u, decide_AIDecide_ComputerSearch, play_AIPlay_ComputerSearch}, /* COMPUTER_SEARCH */
	{0x02u, 0xC9u, decide_AIDecide_PokemonTrader, play_AIPlay_PokemonTrader}, /* POKEMON_TRADER */
};

static uint16_t relist_hand(void)
{
	(void)CreateHandCardList(0u);
	uint16_t hl = wDuelTempList_ADDR;
	uint16_t de = wTempHandCardList_ADDR;
	(void)CopyListWithFFTerminatorFromHLToDE_Bank8(&hl, &de);
	return de;
}

/* trainer_cards.asm:3-148. For every card in hand, every table row of the
 * requested phase naming that card is tried: the card must be playable
 * (Headache, its own initial effect, the AI's random abstention), its decide
 * routine must return carry, and the Play Trainer screen must not end the
 * turn. A hand modified by the card's effect is re-listed from the top. */
AIProcessHandTrainerCardsResult _AIProcessHandTrainerCards(uint8_t a)
{
	wAITrainerCardPhase = a;
	/* e is the register the asm never reloads: the list copy leaves de on the
	 * hand list's terminator, every decide routine is entered with the e its
	 * predecessor left, and a played card's effect commands receive the
	 * decide routine's exit de (PlayAttackAnimation stores that de into
	 * wDamageAnimAmount). AIDecide_GustOfWind reports its exit e; the other
	 * decide routines and the play routines pass the entry e through, which is
	 * exact for the ones whose asm never touches de and unmodeled for the
	 * rest (their exit e only ever reaches memory through that one store). */
	uint8_t e = (uint8_t)relist_hand();
	uint16_t hand = wTempHandCardList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(hand++);
		wAITrainerCardToPlay = card;
		if (card == 0xffu)
			return (AIProcessHandTrainerCardsResult){0xffu, 0xc0u};
		uint8_t phase = wAITrainerCardPhase;
		for (size_t row = 0; row < sizeof trainer_logic / sizeof trainer_logic[0]; row++) {
			const TrainerLogic *logic = &trainer_logic[row];
			wCurrentAIFlags = 0u;
			if (logic->phase != phase)
				continue;
			wAITrainerLogicCard = logic->card;
			uint8_t id = LoadCardDataToBuffer1_FromDeckIndex(wAITrainerCardToPlay);
			if (id == SWITCH && (wPreviousAIFlags & AI_FLAG_USED_SWITCH) != 0u)
				continue;
			if (id != wAITrainerLogicCard)
				continue;
			hTempCardIndex_ff9f = wAITrainerCardToPlay;
			if ((CheckCantUseTrainerDueToEffect().f & 0x10u) != 0u)
				continue;
			LoadEffectResult loaded = LoadNonPokemonCardEffectCommands();
			if ((TryExecuteEffectCommandFunction(EFFECTCMDTYPE_INITIAL_EFFECT_1, 0u, (uint8_t)(loaded.de >> 8), (uint8_t)loaded.de).f & 0x10u) != 0u)
				continue;
			if ((AIChooseRandomlyNotToDoAction().f & 0x10u) != 0u)
				continue;
			TrainerDecision decision = logic->decide(phase, e);
			/* trainer_cards.asm:12-98: the phase lives in d, the decide routine is
			 * called through CallIndirect with no `push de`, and every refusal
			 * (`jr nc, .inc_hl_by_4`, `jr c, .inc_hl_by_2`) rescans the rest of the
			 * table against the decide routine's exit d. A played card jumps to
			 * .loop_hand, which reloads d from wAITrainerCardPhase. */
			phase = decision.d;
			e = decision.e;
			if ((decision.f & 0x10u) == 0u)
				continue;
			wAITrainerCardParameter = decision.a;
			hTempCardIndex_ff9f = wAITrainerCardToPlay;
			if ((AIMakeDecision(OPPACTION_PLAY_TRAINER, 0u, 0u, 0u, 0u).f & 0x10u) != 0u)
				continue;
			(void)logic->play(phase, e);
			wPreviousAIFlags = (uint8_t)(wPreviousAIFlags | wCurrentAIFlags);
			if ((wPreviousAIFlags & AI_FLAG_MODIFIED_HAND) != 0u) {
				e = (uint8_t)relist_hand();
				hand = wTempHandCardList_ADDR;
				wPreviousAIFlags = (uint8_t)(wPreviousAIFlags & (uint8_t)~AI_FLAG_MODIFIED_HAND);
			}
			break;
		}
	}
}
/* <<< factory _AIProcessHandTrainerCards */

/* >>> factory AIPlay_Pokeball */
AIPlayPokeballResult AIPlay_Pokeball(uint8_t d, uint8_t e)
{
	uint8_t card = wAITrainerCardToPlay;
	hTempCardIndex_ff9f = card;
	TossCoinRoutineResult toss = TossCoin(TrainerCardSuccessCheckText, 0u);
	hTemp_ffa0 = toss.a;
	if ((toss.f & 0x10u) != 0u)
		hTempPlayAreaLocation_ffa1 = wAITrainerCardParameter;
	else
		hTempPlayAreaLocation_ffa1 = 0xffu;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIPlayPokeballResult){decision.f};
}
/* <<< factory AIPlay_Pokeball */

/* >>> factory AIPlay_Recycle */
AIDecideResult AIPlay_Recycle(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	TossCoinRoutineResult toss = TossCoin(TrainerCardSuccessCheckText, 0u);
	if ((toss.f & 0x10u) != 0u)
		hTemp_ffa0 = wAITrainerCardParameter;
	else
		hTemp_ffa0 = 0xffu;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Recycle */

/* >>> factory AIPlay_Bill */
/* trainer_cards.asm:1420-1425 */
AIDecideResult AIPlay_Bill(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Bill */

/* >>> factory AIPlay_Defender */
/* trainer_cards.asm:594-601 */
AIDecideResult AIPlay_Defender(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = 0u; /* PLAY_AREA_ARENA: AI always attaches Defender to the Active */
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Defender */

/* >>> factory AIPlay_Imakuni */
/* trainer_cards.asm:4520-4525 */
AIDecideResult AIPlay_Imakuni(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Imakuni */

/* >>> factory AIPlay_FullHeal */
/* trainer_cards.asm:3771-3776 */
AIDecideResult AIPlay_FullHeal(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_FullHeal */

/* >>> factory AIPlay_ClefairyDollOrMysteriousFossil */
/* trainer_cards.asm:4776-4781 */
AIDecideResult AIPlay_ClefairyDollOrMysteriousFossil(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ClefairyDollOrMysteriousFossil */

/* >>> factory AIPlay_ImposterProfessorOak */
/* trainer_cards.asm:3182-3187 */
AIDecideResult AIPlay_ImposterProfessorOak(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ImposterProfessorOak */

/* >>> factory AIPlay_PokemonCenter */
/* trainer_cards.asm:3083-3088 */
AIDecideResult AIPlay_PokemonCenter(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_PokemonCenter */


/* >>> factory AIDecide_PlusPower_Phase14 */
AIDecideParameterResult AIDecide_PlusPower_Phase14(uint8_t d)
{
	/* trainer_cards.asm AIDecide_PlusPower_Phase14: a usable attack that does
	 * not already knock out, a 30% roll, and no Mr. Mime wall past 30 damage.
	 * d follows the callees; GetCardIDFromDeckIndex's `ld d, $0` clears it on
	 * the Mr. Mime check. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	/* .CheckAttackDoesntKO */
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, d, 0u, 0u);
	d = unusable.d;
	if ((unusable.f & 0x10u) != 0u)
		return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a), d};
	d = EstimateDamage_VersusDefendingCard(wSelectedAttack).d;
	uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - wDamage);
	if (hp <= wDamage)
		return (AIDecideParameterResult){left, or_a_flags(left), d};
	/* .check_random */
	unusable = CheckIfSelectedAttackIsUnusable(left, 0x10u, 0u, 0u, d, 0u, 0u);
	d = unusable.d;
	if ((unusable.f & 0x10u) != 0u)
		return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a), d};
	d = EstimateDamage_VersusDefendingCard(wSelectedAttack).d;
	uint8_t minimum = wAIMinDamage;
	if (minimum < 10u)
		return (AIDecideParameterResult){minimum, or_a_flags(minimum), d};
	uint8_t roll = Random(10u);
	if (roll >= 3u)
		return (AIDecideParameterResult){roll, or_a_flags(roll), d};
	/* .MrMimeDamageCheck */
	uint8_t boosted = (uint8_t)(wDamage + 10u);
	if (boosted < 30u)
		return (AIDecideParameterResult){boosted, 0x10u, d};
	SwapTurn();
	uint8_t defender = (uint8_t)GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	d = 0u;
	SwapTurn();
	if (defender == MR_MIME)
		return (AIDecideParameterResult){defender, 0x00u, d};
	return (AIDecideParameterResult){defender, 0x10u, d};
}
/* <<< factory AIDecide_PlusPower_Phase14 */

/* >>> factory AIDecide_GustOfWind */
/* trainer_cards.asm AIDecide_GustOfWind. The local routines that stand a
 * bench card in for the player's arena card restore it through two `pop af`,
 * so the Z each carry-exit keeps is GetNonTurnDuelistVariable's own
 * `cp PLAYER_TURN`. */
static uint8_t non_turn_z(void)
{
	return hWhoseTurn == PLAYER_TURN ? 0x80u : 0x00u;
}

/* .CheckIfAttackDealsNoDamage: carry when the attack is a Pokemon Power or
 * can deal no damage at all to the defending card. */
static uint8_t gust_attack_deals_no_damage(uint8_t *d, uint8_t *e)
{
	AttackCopyResult copy = CopyAttackDataAndDamage_FromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a, wSelectedAttack);
	*d = (uint8_t)(copy.de >> 8);
	*e = (uint8_t)copy.de;
	if (wLoadedAttackCategory == POKEMON_POWER)
		return 1u;
	if (wDamage == 0u)
		return 0u;
	DamageCalculationResult estimate = EstimateDamage_VersusDefendingCard(wSelectedAttack);
	*d = estimate.d;
	*e = estimate.e;
	return wAIMaxDamage == 0u;
}

/* .CheckIfNoAttackDealsDamage */
static uint8_t gust_no_attack_deals_damage(uint8_t *d, uint8_t *e)
{
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	if (!gust_attack_deals_no_damage(d, e))
		return 0u;
	wSelectedAttack = SECOND_ATTACK;
	return gust_attack_deals_no_damage(d, e);
}

/* Stand the player's bench card at `location` in as the arena card, run
 * `check`, put the arena card back. Returns the check's verdict. */
typedef uint8_t (*GustArenaCheck)(uint8_t location);

static uint8_t gust_with_bench_card_in_arena(uint8_t location, GustArenaCheck check)
{
	DuelistVarResult arena = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t arena_card = arena.a;
	gb_write8(arena.hl, GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD)).a);
	uint8_t bench_hp = GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_HP)).a;
	DuelistVarResult hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t arena_hp = hp.a;
	gb_write8(hp.hl, bench_hp);
	uint8_t verdict = check(location);
	gb_write8(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).hl, arena_hp);
	gb_write8(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).hl, arena_card);
	return verdict;
}

/* .CheckIfAttackKnocksOut against the card in location e. */
static uint8_t gust_attack_knocks_out(uint8_t attack, uint8_t location)
{
	(void)EstimateDamage_VersusDefendingCard(attack);
	return GetNonTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD_HP + location)).a <= wDamage;
}

/* .CheckIfAnyAttackKnocksOut, then whether that attack can actually be used:
 * usable now, or usable once the energy in hand is attached. */
static uint8_t gust_knockout_check(uint8_t location)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (!gust_attack_knocks_out(FIRST_ATTACK_OR_PKMN_POWER, location)
	    && !gust_attack_knocks_out(SECOND_ATTACK, location))
		return 0u;
	if ((CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u)
		return 1u;
	return (LookForEnergyNeededForAttackInHand().f & 0x10u) != 0u;
}

/* .FindBenchCardToKnockOut */
static uint8_t gust_find_bench_card_to_knock_out(uint8_t *location_out)
{
	uint16_t bench = GetNonTurnDuelistVariable(DUELVARS_BENCH).hl;
	for (uint8_t location = PLAY_AREA_BENCH_1;; location++) {
		if (gb_read8(bench++) == 0xFFu)
			return 0u;
		if (gust_with_bench_card_in_arena(location, gust_knockout_check)) {
			*location_out = location;
			return 1u;
		}
	}
}

/* .CheckIfCanDamageBenchedCard's check */
static uint8_t gust_can_damage_arena(uint8_t location)
{
	(void)location;
	return (CheckIfCanDamageDefendingPokemon(PLAY_AREA_ARENA, 0x80u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) != 0u;
}

/* .FindBenchCardWithWeakness: a player's bench card weak to color b that the
 * arena card can damage. Carry-exit F keeps CheckIfCanDamageDefendingPokemon's Z. */
static uint8_t gust_find_bench_card_with_weakness(uint8_t color, uint8_t *location_out, uint8_t *z_out, uint8_t *d, uint8_t *e)
{
	uint16_t bench = GetNonTurnDuelistVariable(DUELVARS_BENCH).hl;
	for (uint8_t location = PLAY_AREA_BENCH_1;; location++) {
		uint8_t card = gb_read8(bench++);
		if (card == 0xFFu)
			return 0u;
		SwapTurn();
		(void)LoadCardDataToBuffer1_FromDeckIndex(card);
		SwapTurn();
		if ((wLoadedCard1Weakness & color) == 0u)
			continue;
		/* .check_can_damage saves only bc and hl around the call: d and e are
		 * the damage check's on every later exit, and the next probe starts
		 * from them. */
		CheckIfCanDamageDefendingPokemonResult damage =
			CheckIfCanDamageDefendingPokemon(PLAY_AREA_ARENA, 0x80u, 0u, 0u, *d, *e, 0u);
		*d = damage.d;
		*e = damage.e;
		if (damage.f & 0x10u) {
			*location_out = location;
			*z_out = (uint8_t)(damage.f & 0x80u);
			return 1u;
		}
	}
}

AIDecideGustOfWindResult AIDecide_GustOfWind(uint8_t d, uint8_t e)
{
	/* d follows the callees: GetCardIDFromDeckIndex clears it at .check_id,
	 * .FindBenchCardToKnockOut restores it through `pop de`, the damage
	 * probes of .FindBenchCardWithWeakness leave theirs, and `ld d, a` makes
	 * it the bench countdown in the two energy/HP loops. e travels the same
	 * way: the attack checks leave their damage estimate's e, .check_id makes
	 * it the arena card id, .FindBenchCardToKnockOut counts the bench in it
	 * (`pop de` / `inc e`) and hands back the location on a hit, the two
	 * energy/HP loops count in it, and the damage probes leave theirs. The
	 * exit e matters: a played Gust of Wind carries it into
	 * PlayAttackAnimation's wDamageAnimAmount store. */
	uint8_t bench_count = (uint8_t)(GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a - 1u);
	if (bench_count == 0u)
		return (AIDecideGustOfWindResult){0u, 0x80u, d, e};
	uint8_t used = (uint8_t)(wPreviousAIFlags & AI_FLAG_USED_GUST_OF_WIND);
	if (used != 0u)
		return (AIDecideGustOfWindResult){used, 0x20u, d, e};
	CanArenaCardUseNonResidualAttackResult attack =
		CanArenaCardUseNonResidualAttack(used, 0xA0u, 0u, 0u, d, e, 0u);
	d = attack.d;
	e = attack.e;
	if ((attack.f & 0x10u) == 0u)
		return (AIDecideGustOfWindResult){attack.a, attack.f, d, e};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	e = ko.e;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, e, 0u);
		d = unusable.d;
		e = unusable.e;
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideGustOfWindResult){unusable.a, or_a_flags(unusable.a), d, e};
		/* LookForEnergyNeededForAttackInHand's exit e is not modeled: this
		 * refusal leaves the attack check's e. */
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		d = energy.d;
		if (energy.f & 0x10u)
			return (AIDecideGustOfWindResult){energy.a, or_a_flags(energy.a), d, e};
	}
	/* .check_id */
	uint8_t arena_id = (uint8_t)GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	d = 0u;
	e = arena_id;
	if (arena_id == MEW_LV23 || arena_id == MEWTWO_LV53)
		return (AIDecideGustOfWindResult){arena_id, 0x00u, d, e};
	uint8_t location;
	uint8_t z;
	if (gust_find_bench_card_to_knock_out(&location))
		return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | non_turn_z()), d, location};
	/* .loop_4 ran off the bench: `inc e` once per bench card from PLAY_AREA_BENCH_1. */
	e = (uint8_t)(bench_count + 1u);
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (!gust_no_attack_deals_damage(&d, &e)) {
		uint8_t color = TranslateColorToWR(GetArenaCardColor());
		SwapTurn();
		uint8_t weak = (uint8_t)(GetArenaCardWeakness() & color);
		SwapTurn();
		if (weak != 0u)
			return (AIDecideGustOfWindResult){weak, 0x00u, d, e};
		if (gust_find_bench_card_with_weakness(color, &location, &z, &d, &e))
			return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | z), d, e};
		return (AIDecideGustOfWindResult){0xFFu, 0x00u, d, e};
	}
	/* .check_bench_energy: the arena card cannot damage the defending card.
	 * The asm never loads b here: it is whatever the last damage estimate
	 * left, and every estimate that reaches its weakness/resistance tail
	 * leaves `ld b, CARD_LOCATION_ARENA` (ApplyAttachedDefender's input,
	 * damage_calculation.asm:166). That value doubles as a WATER weakness
	 * mask. A ROM bug, modeled as the register it is. */
	if (gust_find_bench_card_with_weakness(CARD_LOCATION_ARENA, &location, &z, &d, &e))
		return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | z), d, e};
	d = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (location = PLAY_AREA_BENCH_1; --d != 0u; location++) {
		SwapTurn();
		(void)GetPlayAreaCardAttachedEnergies(location);
		SwapTurn();
		if (wTotalAttachedEnergies != 0u)
			continue;
		if (gust_with_bench_card_in_arena(location, gust_can_damage_arena))
			return (AIDecideGustOfWindResult){location, (uint8_t)(0x10u | non_turn_z()), d, location};
	}
	/* .check_bench_hp: the damageable bench card with the least HP left. */
	wce06 = 0xFFu;
	wce08 = 0u;
	d = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (location = PLAY_AREA_BENCH_1; --d != 0u; location++) {
		uint8_t hp = GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_HP)).a;
		if (wce06 < (uint8_t)(hp + 1u))
			continue;
		if (!gust_with_bench_card_in_arena(location, gust_can_damage_arena))
			continue;
		wce06 = hp;
		wce08 = location;
	}
	/* Both loops end with `dec d` reaching zero after `inc e` counted every
	 * play area slot: e is the non-turn duelist's play area count. */
	e = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t found = wce08;
	if (found == 0u)
		return (AIDecideGustOfWindResult){0u, 0x80u, d, e};
	return (AIDecideGustOfWindResult){found, 0x10u, d, e};
}
/* <<< factory AIDecide_GustOfWind */

/* >>> factory AIDecide_Defender_Phase13 */
AIDecideParameterResult AIDecide_Defender_Phase13(uint8_t d)
{
	/* trainer_cards.asm AIDecide_Defender_Phase13: play Defender when the
	 * player's strongest usable attack would knock the arena card out only
	 * without the 20 it prevents, and no knockout of the player's card is
	 * within reach this turn. d follows the callees until `ld d, a` takes
	 * the selected damage, then the damage minus Defender's 20. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
		d = unusable.d;
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a), d};
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		d = energy.d;
		if (energy.f & 0x10u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a), d};
	}
	/* .cannot_ko */
	CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHPResult same =
		CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHP();
	d = same.d;
	if ((same.f & 0x10u) == 0u)
		return (AIDecideParameterResult){same.a, or_a_flags(same.a), d};
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult selected =
		CheckIfSelectedAttackIsUnusable(same.a, same.f, 0u, 0u, d, 0u, 0u);
	SwapTurn();
	d = selected.d;
	if (selected.f & 0x10u)
		return (AIDecideParameterResult){selected.a, or_a_flags(selected.a), d};
	(void)EstimateDamage_FromDefendingPokemon(wSelectedAttack);
	uint8_t selected_damage = wDamage;
	wce06 = selected_damage;
	d = selected_damage;
	wSelectedAttack = (uint8_t)(SECOND_ATTACK - wSelectedAttack);
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult other =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, d, 0u, 0u);
	SwapTurn();
	uint8_t switch_back = (other.f & 0x10u) != 0u;
	if (!switch_back) {
		(void)EstimateDamage_FromDefendingPokemon(wSelectedAttack);
		switch_back = wDamage < selected_damage;
	}
	if (switch_back) {
		wSelectedAttack = (uint8_t)(SECOND_ATTACK - wSelectedAttack);
		wDamage = wce06;
	}
	/* .subtract */
	uint8_t after_defender = (uint8_t)(wDamage - 20u);
	d = after_defender;
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - after_defender);
	if (hp <= after_defender)
		return (AIDecideParameterResult){left, or_a_flags(left), d};
	return (AIDecideParameterResult){left, 0x10u, d};
}
/* <<< factory AIDecide_Defender_Phase13 */

/* >>> factory AIDecide_Switch */
AIDecide_SwitchResult AIDecide_Switch(uint8_t d)
{
	uint8_t cost;
	uint8_t attached;
	if (wAIPlayEnergyCardForRetreat != 0u) {
		hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
		cost = GetPlayAreaCardRetreatCost();
		if (GetTurnDuelistVariable(DUELVARS_BENCH).a != 0xFFu)
			d = 0u;
		attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA).a;
		uint8_t difference = (uint8_t)(cost - attached);
		if (cost < attached)
			goto check_cost_amount;
		if (difference >= 2u)
			goto do_switch;
	}

check_cost_amount:
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	cost = GetPlayAreaCardRetreatCost();
	if (GetTurnDuelistVariable(DUELVARS_BENCH).a != 0xFFu)
		d = 0u;
	if (cost >= 3u)
		goto do_switch;
	attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA).a;
	if (attached < cost)
		goto do_switch;
	return (AIDecide_SwitchResult){attached, (uint8_t)((attached == cost ? 0x80u : 0u) | 0x40u | ((attached & 0x0Fu) < (cost & 0x0Fu) ? 0x20u : 0u)), d};

do_switch:
	{
		AIDecideBenchPokemonToSwitchToResult r = AIDecideBenchPokemonToSwitchTo(d);
		d = r.d;
		return (AIDecide_SwitchResult){r.a, (uint8_t)((r.f & 0x80u) | ((r.f & 0x10u) ? 0u : 0x10u)), d};
	}
}
/* <<< factory AIDecide_Switch */

/* >>> factory AIDecide_SuperEnergyRemoval */
/* trainer_cards.asm AIDecide_SuperEnergyRemoval and its local routines. */

/* .CheckIfFewerThanTwoEnergyCards: carry when the card in location e has
 * fewer than two energy cards, or fewer than two energy counting a double
 * colorless as two. */
static uint8_t ser_fewer_than_two_energy(uint8_t location)
{
	(void)GetPlayAreaCardAttachedEnergies(location);
	if (wTotalAttachedEnergies < 2u)
		return 1u;
	uint8_t total = 0u;
	for (uint8_t color = 0u; color < NUM_COLORED_TYPES; color++)
		total = (uint8_t)(total + gb_read8((uint16_t)(wAttachedEnergies_ADDR + color)));
	total = (uint8_t)(total + (gb_read8((uint16_t)(wAttachedEnergies_ADDR + NUM_COLORED_TYPES)) >> 1));
	return total < 2u;
}

/* .CheckIfNotEnoughEnergyToAttack: carry when neither attack of the card in
 * location e has its energy, or only the second does and with a surplus of two. */
static uint8_t ser_not_enough_energy_to_attack(uint8_t location)
{
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	hTempPlayAreaLocation_ff9d = location;
	if ((CheckEnergyNeededForAttack().f & 0x10u) == 0u)
		return 0u;
	wSelectedAttack = SECOND_ATTACK;
	hTempPlayAreaLocation_ff9d = location;
	if ((CheckEnergyNeededForAttack().f & 0x10u) != 0u)
		return 1u;
	return CheckIfNoSurplusEnergyForAttack().a >= 2u;
}

/* .FindHighestDamagingAttack: the strongest attack of the card in location e
 * against the AI's arena card, kept in wce06 with its location in wce08. */
static void ser_find_highest_damaging_attack(uint8_t location)
{
	for (uint8_t attack = FIRST_ATTACK_OR_PKMN_POWER; attack <= SECOND_ATTACK; attack++) {
		hTempPlayAreaLocation_ff9d = location;
		(void)EstimateDamage_VersusDefendingCard(attack);
		uint8_t damage = wDamage;
		if (damage != 0u && wce06 < damage) {
			wce06 = damage;
			wce08 = location;
		}
	}
}

/* .LookForNonDoubleColorless: carry when the card in location e has a basic
 * energy card attached. */
static uint8_t ser_has_basic_energy(uint8_t location)
{
	(void)CreateArenaOrBenchEnergyCardList(location);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t card = gb_read8(list++);
		if (card == 0xFFu)
			return 0u;
		if (LoadCardDataToBuffer1_FromDeckIndex(card) < DOUBLE_COLORLESS_ENERGY)
			return 1u;
	}
}

AIDecideParameterResult AIDecide_SuperEnergyRemoval(uint8_t d)
{
	/* d follows the asm: `ld d, a` takes each play-area card's deck index in
	 * the loops (the helpers bracket themselves in `push de` / `pop de`),
	 * the knockout callees report theirs, and the energy discard pick's d
	 * is the one under the final `scf`. */
	/* A card of the AI's own with a basic energy to pay the cost. */
	uint8_t own = PLAY_AREA_BENCH_1;
	for (;; own++) {
		uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + own)).a;
		if (card == 0xFFu)
			return (AIDecideParameterResult){0xFFu, 0x00u, d};
		d = card;
		if (ser_has_basic_energy(own))
			break;
	}
	wce0f = own;
	/* Whether the arena card can knock the defending card out this turn:
	 * if it can, leave the player's arena card alone and look at the bench. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t start = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
		d = unusable.d;
		if ((unusable.f & 0x10u) == 0u) {
			start = PLAY_AREA_BENCH_1;
		} else {
			LookForEnergyNeededForAttackInHandResult hand = LookForEnergyNeededForAttackInHand();
			d = hand.d;
			if (hand.f & 0x10u)
				start = PLAY_AREA_BENCH_1;
		}
	}
	SwapTurn();
	uint8_t target = start;
	for (;; target++) {
		uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + target)).a;
		if (card == 0xFFu) {
			SwapTurn();
			return (AIDecideParameterResult){0xFFu, 0x00u, d};
		}
		d = card;
		if (ser_fewer_than_two_energy(target))
			continue;
		if (!ser_not_enough_energy_to_attack(target))
			break;
	}
	if (target != PLAY_AREA_ARENA) {
		/* .check_bench_damage: the bench card with the strongest attack. */
		wce06 = 0u;
		wce08 = 0u;
		for (uint8_t bench = PLAY_AREA_BENCH_1;; bench++) {
			uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + bench)).a;
			if (card == 0xFFu)
				break;
			d = card;
			if (ser_fewer_than_two_energy(bench) || ser_not_enough_energy_to_attack(bench))
				continue;
			ser_find_highest_damaging_attack(bench);
		}
		target = wce08;
		if (target == 0u) {
			SwapTurn();
			return (AIDecideParameterResult){0u, 0x80u, d};
		}
	}
	/* .pick_energy */
	wce1b = target;
	PickTwoResult picked = PickTwoAttachedEnergyCards(target);
	wce1c = picked.a;
	wce1d = picked.b;
	SwapTurn();
	uint8_t parameter = wce0f;
	PickEnergyResult discard = AIPickEnergyCardToDiscard(parameter);
	wce1a = discard.a;
	return (AIDecideParameterResult){parameter, (uint8_t)((picked.f & 0x80u) | 0x10u), discard.d};
}
/* <<< factory AIDecide_SuperEnergyRemoval */

/* >>> factory AIDecide_ScoopUp */
AIDecide_ScoopUpResult AIDecide_ScoopUp(uint8_t d)
{
	/* trainer_cards.asm AIDecide_ScoopUp. d follows the callees;
	 * GetCardIDFromDeckIndex's `ld d, $0` clears it, `ld d, a` takes the
	 * arena card's HP in damage counters, and the switch decision reports
	 * the chosen bench slot. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	DuelistVarResult count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	if (count.a < 2u)
		return (AIDecide_ScoopUpResult){count.a, or_a_flags(count.a), d};
	uint8_t deck_id = wOpponentDeckID;
	uint8_t slot;
	if (deck_id == LEGENDARY_ARTICUNO_DECK_ID) {
		/* .HandleLegendaryArticuno */
		count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (count.a < 3u)
			return (AIDecide_ScoopUpResult){count.a, or_a_flags(count.a), d};
		LookForCardIDInPlayAreaResult bench = LookForCardIDInPlayArea_Bank8(ARTICUNO_LV37, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto articuno_bench;
		}
		uint8_t arena_id = (uint8_t)GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
		d = 0u;
		if (arena_id != ARTICUNO_LV37 && arena_id != CHANSEY)
			return (AIDecide_ScoopUpResult){arena_id, or_a_flags(arena_id), d};
		/* .articuno_or_chansey */
		CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
		d = ko.d;
		if (ko.f & 0x10u) {
			CheckIfSelectedAttackIsUnusableResult unusable =
				CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
			d = unusable.d;
			if ((unusable.f & 0x10u) == 0u)
				return (AIDecide_ScoopUpResult){unusable.a, or_a_flags(unusable.a), d};
			LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
			d = energy.d;
			if (energy.f & 0x10u)
				return (AIDecide_ScoopUpResult){energy.a, or_a_flags(energy.a), d};
		}
		/* .check_ko */
		CheckIfDefendingPokemonCanKnockOutResult defending =
			CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, d, 0u, 0u);
		d = defending.d;
		if ((defending.f & 0x10u) == 0u)
			return (AIDecide_ScoopUpResult){defending.a, or_a_flags(defending.a), d};
		goto decide_switch;
	}
	if (deck_id == LEGENDARY_RONALD_DECK_ID) {
		/* .HandleLegendaryRonald */
		count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
		if (count.a < 3u)
			return (AIDecide_ScoopUpResult){count.a, or_a_flags(count.a), d};
		LookForCardIDInPlayAreaResult bench = LookForCardIDInPlayArea_Bank8(ARTICUNO_LV37, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto articuno_bench;
		}
		bench = LookForCardIDInPlayArea_Bank8(ZAPDOS_LV68, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto check_attached_energy;
		}
		bench = LookForCardIDInPlayArea_Bank8(MOLTRES_LV37, PLAY_AREA_BENCH_1);
		if (bench.f & 0x10u) {
			slot = bench.a;
			goto check_attached_energy;
		}
		return (AIDecide_ScoopUpResult){bench.a, or_a_flags(bench.a), d};
	}

	{
		CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
		d = ko.d;
		if (ko.f & 0x10u) {
			CheckIfSelectedAttackIsUnusableResult unusable =
				CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
			d = unusable.d;
			if ((unusable.f & 0x10u) == 0u)
				return (AIDecide_ScoopUpResult){unusable.a, or_a_flags(unusable.a), d};
			LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
			d = energy.d;
			if (energy.f & 0x10u)
				return (AIDecide_ScoopUpResult){energy.a, or_a_flags(energy.a), d};
		}
	}
	/* .cannot_ko */
	{
		uint8_t status = (uint8_t)(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ);
		if (status != PARALYZED && status != ASLEEP) {
			hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
			uint8_t cost = GetPlayAreaCardRetreatCost();
			/* GetLoadedCard1RetreatCost walks the bench (non-empty here) through
			 * GetCardIDFromDeckIndex. */
			d = 0u;
			uint8_t attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA).a;
			if (attached >= cost)
				return (AIDecide_ScoopUpResult){attached, or_a_flags(attached), d};
		}
	}
	/* .cannot_retreat */
	{
		DuelistVarResult arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
		(void)LoadCardDataToBuffer1_FromDeckIndex(arena.a);
		uint8_t counters = ConvertHPToDamageCounters_Bank8(wLoadedCard1HP);
		d = counters;
		CardDamageResult damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA);
		if (damage.a == 0u)
			return (AIDecide_ScoopUpResult){0u, 0x80u, d};
		uint8_t ratio = CalculateBDividedByA_Bank8(counters, damage.a).a;
		if (ratio < 7u)
			return (AIDecide_ScoopUpResult){ratio, or_a_flags(ratio), d};
	}
decide_switch:
	{
		AIDecideBenchPokemonToSwitchToResult choice = AIDecideBenchPokemonToSwitchTo(d);
		d = choice.d;
		if (choice.f & 0x10u)
			return (AIDecide_ScoopUpResult){choice.a, or_a_flags(choice.a), d};
		wce1a = choice.a;
		/* `xor a; scf` */
		return (AIDecide_ScoopUpResult){0u, 0x90u, d};
	}
articuno_bench:
	{
		/* `push af` keeps the bench slot around the defender's id lookup. */
		uint8_t defender_id = (uint8_t)GetCardIDFromDeckIndex(GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
		d = 0u;
		if (defender_id == SNORLAX)
			return (AIDecide_ScoopUpResult){defender_id, or_a_flags(defender_id), d};
	}
check_attached_energy:
	{
		/* `push af` / `pop bc` keep the slot; the Z flag is the energy count's. */
		uint8_t attached = CountNumberOfEnergyCardsAttached(slot).a;
		if (attached != 0u)
			return (AIDecide_ScoopUpResult){slot, or_a_flags(slot), d};
		/* .no_energy */
		wce1a = 0xffu;
		return (AIDecide_ScoopUpResult){slot, 0x90u, d};
	}
}
/* <<< factory AIDecide_ScoopUp */

/* >>> factory AIDecide_FullHeal */
AIDecideFullHealResult AIDecide_FullHeal(uint8_t d)
{
	/* trainer_cards.asm AIDecide_FullHeal. d follows the callees: the status
	 * checks and the play-area lookups keep it, the hand-list lookup leaves
	 * wDuelTempList's page, then Scoop Up, the damage check and the retreat
	 * decision each report their own. */
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	if (status == 0u)
		return (AIDecideFullHealResult){0u, 0x80u, d};
	status &= CNF_SLP_PRZ;
	if (status != PARALYZED && status != ASLEEP && status != CONFUSED)
		return (AIDecideFullHealResult){status, 0x10u, d};
	if (status == ASLEEP) {
		LookForCardIDInPlayAreaResult ghost = LookForCardIDInPlayArea_Bank8(GASTLY_LV8, PLAY_AREA_ARENA);
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, (uint8_t)((ghost.f & 0x80u) | 0x10u), d};
		ghost = LookForCardIDInPlayArea_Bank8(GASTLY_LV17, PLAY_AREA_ARENA);
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, (uint8_t)((ghost.f & 0x80u) | 0x10u), d};
		ghost = LookForCardIDInPlayArea_Bank8(HAUNTER_LV22, PLAY_AREA_ARENA);
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, (uint8_t)((ghost.f & 0x80u) | 0x10u), d};
	}
	/* .paralyzed / .confused share the Scoop Up and damage checks. */
	LookForCardIDInHandListResult hand = LookForCardIDInHandList_Bank8(SCOOP_UP);
	d = hand.d;
	if (hand.f & 0x10u) {
		AIDecide_ScoopUpResult scoop = AIDecide_ScoopUp(d);
		d = scoop.d;
		if (scoop.f & 0x10u)
			return (AIDecideFullHealResult){scoop.a, or_a_flags(scoop.a), d};
	}
	CheckIfCanDamageDefendingPokemonResult damage =
		CheckIfCanDamageDefendingPokemon(PLAY_AREA_ARENA, 0x80u, 0u, 0u, d, 0u, 0u);
	d = damage.d;
	if ((damage.f & 0x10u) == 0u)
		return (AIDecideFullHealResult){damage.a, or_a_flags(damage.a), d};
	uint8_t energy_for_retreat = wAIPlayEnergyCardForRetreat;
	if (energy_for_retreat != 0u)
		return (AIDecideFullHealResult){energy_for_retreat, 0x10u, d};
	if (status == CONFUSED)
		return (AIDecideFullHealResult){0u, 0x80u, d};
	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat(d);
	d = retreat.d;
	if ((retreat.f & 0x10u) == 0u)
		return (AIDecideFullHealResult){retreat.a, (uint8_t)((retreat.f & 0x80u) | 0x10u), d};
	return (AIDecideFullHealResult){retreat.a, or_a_flags(retreat.a), d};
}
/* <<< factory AIDecide_FullHeal */

/* >>> factory AIDecide_EnergyRemoval */
AIDecideEnergyRemovalResult AIDecide_EnergyRemoval(uint8_t d)
{
	/* trainer_cards.asm AIDecide_EnergyRemoval. d follows the knockout
	 * callees, then `ld d, a` takes each play-area card's deck index in the
	 * two loops (their helpers bracket themselves in `push de` / `pop de`),
	 * and the energy pick reports its own. .pick_energy's `push af` keeps
	 * the Z of the check that chose the card under the `scf`. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	uint8_t start = PLAY_AREA_ARENA;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
		d = unusable.d;
		if (unusable.f & 0x10u) {
			LookForEnergyNeededForAttackInHandResult hand = LookForEnergyNeededForAttackInHand();
			d = hand.d;
			if (hand.f & 0x10u)
				start = PLAY_AREA_BENCH_1;
		} else {
			start = PLAY_AREA_BENCH_1;
		}
	}
	wce0f = start;
	SwapTurn();
	uint8_t loc = start;
	uint8_t z = 0u;
	for (;; loc++) {
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + loc));
		if (card.a == 0xFFu)
			break;
		d = card.a;
		(void)GetPlayAreaCardAttachedEnergies(loc);
		if (wTotalAttachedEnergies == 0u)
			continue;
		/* .CheckIfNotEnoughEnergyToAttack */
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		hTempPlayAreaLocation_ff9d = loc;
		CheckEnergyNeededForAttackResult first = CheckEnergyNeededForAttack();
		uint8_t enough = (uint8_t)((first.f & 0x10u) == 0u);
		z = or_a_flags(first.a);
		if (!enough) {
			wSelectedAttack = SECOND_ATTACK;
			hTempPlayAreaLocation_ff9d = loc;
			CheckEnergyNeededForAttackResult second = CheckEnergyNeededForAttack();
			if ((second.f & 0x10u) == 0u) {
				CheckIfNoSurplusEnergyResult surplus = CheckIfNoSurplusEnergyForAttack();
				enough = (uint8_t)((surplus.f & 0x10u) != 0u);
				z = (uint8_t)(surplus.f & 0x80u);
			}
		}
		if (enough) {
			PickEnergyResult pick = PickAttachedEnergyCardToRemove(loc);
			wce1a = pick.a;
			SwapTurn();
			return (AIDecideEnergyRemovalResult){loc, (uint8_t)(z | 0x10u), pick.d};
		}
	}
	/* trainer_cards.asm .default never resets e, so the ROM's "active card"
	 * fallback inspects the loop's terminal slot - the first empty play-area
	 * location - which carries no energy. Reproduced, not corrected: the
	 * arena card is only ever picked through .check_bench_damage below. */
	if (start == PLAY_AREA_ARENA) {
		(void)GetPlayAreaCardAttachedEnergies(loc);
		if (wTotalAttachedEnergies != 0u) {
			PickEnergyResult pick = PickAttachedEnergyCardToRemove(loc);
			wce1a = pick.a;
			SwapTurn();
			return (AIDecideEnergyRemovalResult){loc, 0x10u, pick.d};
		}
	}
	wce06 = 0u;
	wce08 = 0u;
	for (loc = PLAY_AREA_BENCH_1;; loc++) {
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + loc));
		if (card.a == 0xFFu)
			break;
		d = card.a;
		(void)GetPlayAreaCardAttachedEnergies(loc);
		if (wTotalAttachedEnergies == 0u)
			continue;
		hTempPlayAreaLocation_ff9d = loc;
		(void)EstimateDamage_VersusDefendingCard(FIRST_ATTACK_OR_PKMN_POWER);
		if (wDamage > wce06) {
			wce06 = wDamage;
			wce08 = loc;
		}
		hTempPlayAreaLocation_ff9d = loc;
		(void)EstimateDamage_VersusDefendingCard(SECOND_ATTACK);
		if (wDamage > wce06) {
			wce06 = wDamage;
			wce08 = loc;
		}
	}
	if (wce08 != 0u) {
		uint8_t found = wce08;
		PickEnergyResult pick = PickAttachedEnergyCardToRemove(found);
		wce1a = pick.a;
		SwapTurn();
		return (AIDecideEnergyRemovalResult){found, 0x10u, pick.d};
	}
	SwapTurn();
	return (AIDecideEnergyRemovalResult){0u, 0x80u, d};
}
/* <<< factory AIDecide_EnergyRemoval */

/* >>> factory AIDecide_PokemonCenter */
AIDecideParameterResult AIDecide_PokemonCenter(uint8_t d)
{
	/* trainer_cards.asm AIDecide_PokemonCenter: not when a knockout is within
	 * reach this turn; otherwise when the damage to heal outweighs the energy
	 * lost and beats 60% of the total HP. d follows the callees, then `ld d, a`
	 * makes it the play-area countdown; HtimesL and CalculateWordTensDigit
	 * keep it. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
		d = unusable.d;
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a), d};
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		d = energy.d;
		if (energy.f & 0x10u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a), d};
	}

	wce06 = 0u;
	wce08 = 0u;
	wce0f = 0u;
	d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	uint8_t e = PLAY_AREA_ARENA;
	for (;;) {
		uint8_t deck_index = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		(void)LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		uint8_t hp_counters = ConvertHPToDamageCounters_Bank8(wLoadedCard1HP);
		wce06 = (uint8_t)(wce06 + hp_counters);

		CardDamageResult damage = GetCardDamageAndMaxHP(e);
		uint8_t damage_counters = ConvertHPToDamageCounters_Bank8(damage.a);
		wce08 = (uint8_t)(wce08 + damage_counters);

		(void)GetPlayAreaCardAttachedEnergies(e);
		uint8_t attached = wTotalAttachedEnergies;
		uint16_t energy_sum = (uint16_t)wce0f + attached;
		if (energy_sum > 0xffu)
			return (AIDecideParameterResult){(uint8_t)energy_sum, or_a_flags((uint8_t)energy_sum), d};
		wce0f = (uint8_t)energy_sum;
		if (--d == 0u)
			break;
		++e;
	}

	uint8_t half_damage = (uint8_t)(wce08 >> 1);
	if (half_damage < wce0f)
		return (AIDecideParameterResult){half_damage, or_a_flags(half_damage), d};
	uint16_t product = HtimesL((uint16_t)(0x0600u | wce06));
	uint8_t tens = (uint8_t)CalculateWordTensDigit(product);
	if (tens >= wce08)
		return (AIDecideParameterResult){tens, or_a_flags(tens), d};
	return (AIDecideParameterResult){tens, 0x10u, d};
}
/* <<< factory AIDecide_PokemonCenter */

/* >>> factory AIDecide_PlusPower_Phase13 */
AIDecide_PlusPower_Phase13Result AIDecide_PlusPower_Phase13(uint8_t d)
{
	/* The `xor a` / `ldh` pair is written twice in the source ("this is
	   mistakenly duplicated"); both stores are kept. d follows the callees;
	   GetCardIDFromDeckIndex's `ld d, $0` clears it before the substatus
	   check and again on the Mr. Mime check. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;

	CheckIfAnyAttackKnocksOutDefendingCardResult ko =
		CheckIfAnyAttackKnocksOutDefendingCard();
	d = ko.d;
	if ((ko.f & 0x10u) != 0u) {
		CheckIfSelectedAttackIsUnusableResult ko_attack =
			CheckIfSelectedAttackIsUnusable(ko.a, ko.f, 0u, 0u, d, 0u, 0u);
		d = ko_attack.d;
		/* `jr nc, .no_carry`: the attack is usable, so a KO is already in reach;
		   `or a` at .no_carry keeps a and sets Z from it, clearing N/H/C. */
		if ((ko_attack.f & 0x10u) == 0u)
			return (AIDecide_PlusPower_Phase13Result){ko_attack.a,
				(uint8_t)(ko_attack.a == 0u ? 0x80u : 0x00u), d};
		LookForEnergyNeededForAttackInHandResult energy =
			LookForEnergyNeededForAttackInHand();
		d = energy.d;
		if ((energy.f & 0x10u) != 0u)
			return (AIDecide_PlusPower_Phase13Result){energy.a,
				(uint8_t)(energy.a == 0u ? 0x80u : 0x00u), d};
	}

	/* .cannot_ko */
	DuelistVarResult attacker = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	wTempTurnDuelistCardID = (uint8_t)GetCardIDFromDeckIndex(attacker.a);

	SwapTurn();
	DuelistVarResult defender = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t defending_id = (uint8_t)GetCardIDFromDeckIndex(defender.a);
	d = 0u;
	wTempNonTurnDuelistCardID = defending_id;
	NoDamageOrEffectResult prevented =
		HandleNoDamageOrEffectSubstatus(d, defending_id, defender.hl);
	d = prevented.d;
	SwapTurn();
	if ((prevented.f & 0x10u) != 0u)
		/* .no_damage_or_effect in the callee does `ld a, e` (the substatus id)
		   immediately before `scf`, so a mirrors the returned e. */
		return (AIDecide_PlusPower_Phase13Result){prevented.e,
			(uint8_t)(prevented.e == 0u ? 0x80u : 0x00u), d};

	uint8_t attack = FIRST_ATTACK_OR_PKMN_POWER;
	for (;;) {
		wSelectedAttack = attack;

		/* .CheckAttackWithPluspower */
		uint8_t exit_a;
		uint8_t kos_with_pluspower = 0u;
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(attack, 0u, 0u, 0u, d, 0u, 0u);
		d = unusable.d;
		if ((unusable.f & 0x10u) != 0u) {
			exit_a = unusable.a; /* .unusable: or a; ret */
		} else {
			d = EstimateDamage_VersusDefendingCard(wSelectedAttack).d;
			uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
			uint8_t damage = wDamage;
			exit_a = (uint8_t)(hp - damage);
			/* `sub [hl]` then `jr c` (damage already exceeds HP) / `jr z` (attack
			   already KOs) both return no carry with the difference in a. */
			if (hp >= damage && exit_a != 0u) {
				uint8_t boosted = (uint8_t)(damage + 10u);
				exit_a = (uint8_t)(hp - boosted);
				/* `ret c` (boosted damage exceeds HP) and `scf` after `ret nz`
				   (exact KO) are the carry exits; `ret nz` does not KO. */
				kos_with_pluspower = (uint8_t)(hp <= boosted);
			}
		}

		if (kos_with_pluspower != 0u) {
			/* .MrMimeDamageCheck: `ret c` keeps the carry when the boosted
			   damage stays below 30, which Mr. Mime cannot prevent. */
			if ((uint8_t)(wDamage + 10u) >= 30u) {
				SwapTurn();
				DuelistVarResult arena =
					GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
				uint8_t defending = (uint8_t)GetCardIDFromDeckIndex(arena.a);
				d = 0u;
				SwapTurn();
				/* `cp MR_MIME` / `ret z` returns with a = MR_MIME and Z set,
				   so the `or a` at .no_carry leaves Z clear. */
				if (defending == MR_MIME)
					return (AIDecide_PlusPower_Phase13Result){defending, 0x00u, d};
			}
			/* `.first_atk_kos_with_pluspower` / `.second_atk_kos_with_pluspower`:
			   so `xor a; scf` yields $90 and `ld a, SECOND_ATTACK; scf` $10. */
			if (attack == FIRST_ATTACK_OR_PKMN_POWER)
				return (AIDecide_PlusPower_Phase13Result){
					FIRST_ATTACK_OR_PKMN_POWER, 0x90u, d};
			return (AIDecide_PlusPower_Phase13Result){SECOND_ATTACK, 0x10u, d};
		}

		if (attack == SECOND_ATTACK)
			/* .no_carry: `or a` on the second attack's exit value. */
			return (AIDecide_PlusPower_Phase13Result){exit_a,
				(uint8_t)(exit_a == 0u ? 0x80u : 0x00u), d};
		attack = SECOND_ATTACK;
	}
}
/* <<< factory AIDecide_PlusPower_Phase13 */

/* >>> factory AIPlay_PlusPower */
AIDecideResult AIPlay_PlusPower(uint8_t d, uint8_t e)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_USED_PLUSPOWER);
	wAIPlusPowerAttack = wAITrainerCardParameter;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_PlusPower */

/* >>> factory AIPlay_Potion */
AIDecideResult AIPlay_Potion(uint8_t d, uint8_t e)
{
	uint8_t card = wAITrainerCardToPlay;
	hTempCardIndex_ff9f = card;
	uint8_t parameter = wAITrainerCardParameter;
	hTemp_ffa0 = parameter;
	CardDamageResult damage = GetCardDamageAndMaxHP(parameter);
	uint8_t location = damage.a;
	if (location >= 20u)
		location = 20u;
	hTempPlayAreaLocation_ffa1 = location;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Potion */

/* >>> factory AIPlay_GustOfWind */
AIDecideResult AIPlay_GustOfWind(uint8_t d, uint8_t e)
{
	uint8_t flags = wCurrentAIFlags;
	flags |= 0x10u;
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(0x07u, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_GustOfWind */

/* >>> factory AIPlay_Switch */
AIDecideResult AIPlay_Switch(uint8_t d, uint8_t e)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_USED_SWITCH);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	(void)AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	wAIRetreatScore = 0u;
	return (AIDecideResult){0x80u};
}
/* <<< factory AIPlay_Switch */

/* >>> factory AIPlay_Maintenance */
AIDecideResult AIPlay_Maintenance(uint8_t d, uint8_t e)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Maintenance */

/* >>> factory AIPlay_ComputerSearch */
AIDecideResult AIPlay_ComputerSearch(uint8_t d, uint8_t e)
{
	uint8_t flags = wCurrentAIFlags;
	flags = (uint8_t)(flags | AI_FLAG_MODIFIED_HAND);
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTempRetreatCostCards = wAITrainerCardParameter;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ComputerSearch */

/* >>> factory AIPlay_ItemFinder */
AIDecideResult AIPlay_ItemFinder(uint8_t d, uint8_t e)
{
	uint8_t flags = wCurrentAIFlags;
	flags |= AI_FLAG_MODIFIED_HAND;
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	hTempRetreatCostCards = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ItemFinder */

/* >>> factory AIPlay_Pokedex */
AIDecideResult AIPlay_Pokedex(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	hTempRetreatCostCards = wce1c;
	gb_write8(hTempRetreatCostCards_ADDR + 1u, wce1d);
	gb_write8(hTempRetreatCostCards_ADDR + 2u, wce1e);
	gb_write8(hTempRetreatCostCards_ADDR + 3u, 0xffu);
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Pokedex */

/* >>> factory AIPlay_Gambler */
AIDecideResult AIPlay_Gambler(uint8_t d, uint8_t e)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	if (wOpponentDeckID == IMAKUNI_DECK_ID) {
		hTempCardIndex_ff9f = wAITrainerCardToPlay;
		AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
		return (AIDecideResult){decision.f};
	}
	uint8_t rng0 = wRNG1;
	uint8_t rng1 = gb_read8(wRNG1_ADDR + 1u);
	uint8_t rng2 = gb_read8(wRNG1_ADDR + 2u);
	wce06 = rng0;
	wce08 = rng1;
	wce0f = rng2;
	gb_write8(wRNG1_ADDR, 0x50u);
	gb_write8(wRNG1_ADDR + 1u, 0x50u);
	gb_write8(wRNG1_ADDR + 2u, 0x50u);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	gb_write8(wRNG1_ADDR, wce06);
	gb_write8(wRNG1_ADDR + 1u, wce08);
	gb_write8(wRNG1_ADDR + 2u, wce0f);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Gambler */

/* >>> factory AIPlay_EnergyRetrieval */
AIDecideResult AIPlay_EnergyRetrieval(uint8_t d, uint8_t e)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	hTempRetreatCostCards = wce1b;
	if (hTempRetreatCostCards != 0xffu)
		gb_write8(hTempRetreatCostCards_ADDR + 1u, 0xffu);
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_EnergyRetrieval */

/* >>> factory AIPlay_SuperEnergyRemoval */
AIDecideResult AIPlay_SuperEnergyRemoval(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	hTempRetreatCostCards = wce1b;
	gb_write8(hTempRetreatCostCards_ADDR + 1u, wce1c);
	gb_write8(hTempRetreatCostCards_ADDR + 2u, wce1d);
	gb_write8(hTempRetreatCostCards_ADDR + 3u, 0xffu);
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_SuperEnergyRemoval */

/* >>> factory AIDecide_SuperPotion_Phase11 */
AIDecideSuperPotionPhase11Result AIDecide_SuperPotion_Phase11(uint8_t d)
{
	/* trainer_cards.asm AIDecide_SuperPotion_Phase11. d is the knockout
	 * callee's exit d, then the knockout damage, then `ld d, a` takes each
	 * play-area card's deck index in the loop; the loop's helpers bracket
	 * themselves in `push de` / `pop de`. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, d, 0u, 0u);
	d = ko.d;
	uint8_t e = PLAY_AREA_ARENA;
	uint8_t prizes;
	if ((ko.f & 0x10u) != 0u) {
		d = ko.a;
		uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
		uint8_t damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
		if (damage >= 41u)
			damage = 40u;
		uint8_t total = (uint8_t)(hp + damage);
		uint8_t remaining = (uint8_t)(total - d);
		if (total >= d && remaining != 0u)
			return (AIDecideSuperPotionPhase11Result){remaining, 0u, d};
		SwapTurn();
		prizes = CountPrizes();
		SwapTurn();
		e = (uint8_t)(prizes - 1u) == 0u ? PLAY_AREA_ARENA : PLAY_AREA_BENCH_1;
	}
	for (;;) {
		uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		if (card == 0xffu)
			return (AIDecideSuperPotionPhase11Result){0xffu, 0xC0u, d};
		d = card;
		/* .CheckIfHasEnergies */
		(void)GetPlayAreaCardAttachedEnergies(e);
		if (wTotalAttachedEnergies == 0u) {
			e++;
			continue;
		}
		/* .CheckIfHasAttackWithBoostIfTakenDamageFlag */
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, d, e, 0u);
		if ((unusable.f & 0x10u) == 0u && (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F).f & 0x10u) != 0u) {
			e++;
			continue;
		}
		wSelectedAttack = SECOND_ATTACK;
		unusable = CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, 0u, 0u, 0u, d, e, 0u);
		if ((unusable.f & 0x10u) == 0u && (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F).f & 0x10u) != 0u) {
			e++;
			continue;
		}
		/* .CheckIfDiscardingMakesAttacksUnusable */
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		hTempPlayAreaLocation_ff9d = e;
		CheckEnergyNeededForAttackResult need = CheckEnergyNeededForAttack();
		if ((need.f & 0x10u) == 0u && (CheckEnergyNeededForAttackAfterDiscard().f & 0x10u) != 0u) {
			e++;
			continue;
		}
		wSelectedAttack = SECOND_ATTACK;
		hTempPlayAreaLocation_ff9d = e;
		need = CheckEnergyNeededForAttack();
		if ((need.f & 0x10u) == 0u && (CheckEnergyNeededForAttackAfterDiscard().f & 0x10u) != 0u) {
			e++;
			continue;
		}
		CardDamageResult card_damage = GetCardDamageAndMaxHP(e);
		if (card_damage.a < 40u) {
			e++;
			continue;
		}
		/* .found */
		if (e != PLAY_AREA_ARENA) {
			SwapTurn();
			prizes = CountPrizes();
			SwapTurn();
			if ((uint8_t)(prizes - 1u) != 0u) {
				uint8_t chance = Random(10u);
				if (chance < 3u)
					return (AIDecideSuperPotionPhase11Result){chance, (uint8_t)(chance == 0u ? 0x80u : 0u), d};
			}
			return (AIDecideSuperPotionPhase11Result){e, 0x10u, d};
		}
		/* .active_card */
		AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
		if ((recoil.f & 0x10u) != 0u)
			return (AIDecideSuperPotionPhase11Result){0u, 0x80u, d};
		return (AIDecideSuperPotionPhase11Result){e, 0x10u, d};
	}
}
/* <<< factory AIDecide_SuperPotion_Phase11 */

/* >>> factory AIPlay_EnergySearch */
/* trainer_cards.asm:3218-3233 */
AIDecideResult AIPlay_EnergySearch(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_EnergySearch */

/* >>> factory AIPlay_ScoopUp */
AIDecideResult AIPlay_ScoopUp(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ScoopUp */

/* >>> factory AIPlay_PokemonBreeder */
AIDecideResult AIPlay_PokemonBreeder(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTempPlayAreaLocation_ffa1 = wAITrainerCardParameter;
	hTemp_ffa0 = wce1a;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_PokemonBreeder */

/* >>> factory AIPlay_PokemonFlute */
AIDecideResult AIPlay_PokemonFlute(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_PokemonFlute */

/* >>> factory AIDecide_ProfessorOak */
/* .LookForEvolution: carry when a card in hand evolves the card in play area
 * location e; wce08 is set when any card of the deck could. */
static uint8_t oak_evolution_in_hand(uint8_t location)
{
	wce08 = 0u;
	for (uint8_t candidate = 0u; candidate < DECK_SIZE; candidate++) {
		if (CheckIfCanEvolveInto(candidate, location).f & 0x10u)
			continue;
		wce08 = TRUE;
		if (GetTurnDuelistVariable((uint8_t)(DUELVARS_CARD_LOCATIONS + candidate)).a == CARD_LOCATION_HAND)
			return 1u;
	}
	return 0u;
}

AIDecideParameterResult AIDecide_ProfessorOak(uint8_t d)
{
	/* trainer_cards.asm AIDecide_ProfessorOak: a score in wce06 against 60. */
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	if (remaining >= DECK_SIZE - 6u)
		return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 6u), d};

	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == LEGENDARY_ARTICUNO_DECK_ID) {
		/* .HandleLegendaryArticunoDeck */
		uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		if (count < 3u) {
			d = count;
			(void)CreateHandCardList(0u);
			uint8_t evolves = 0u;
			for (uint8_t location = PLAY_AREA_ARENA; location != count; location++) {
				uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + location)).a;
				if (CheckForEvolutionInList(card, 0u).f & 0x10u) {
					evolves = 1u;
					break;
				}
			}
			if (!evolves)
				return (AIDecideParameterResult){count, 0x90u, count};
		}
		/* .check_playable_cards */
		CountOppEnergyResult energy = CountOppEnergyCardsInHand(0u, 0u);
		if (energy.a >= 4u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a), d};
		(void)CreateHandCardList(0u);
		d = 0xC5u;
		uint16_t list = wDuelTempList_ADDR;
		(void)RemoveCardIDInList(&list, PROFESSOR_OAK);
		(void)RemoveCardIDInList(&list, PROFESSOR_OAK);
		for (;;) {
			uint8_t index = gb_read8(list++);
			if (index == 0xFFu)
				return (AIDecideParameterResult){0xFFu, 0x90u, d};
			CheckIfCardCanBePlayedResult playable = CheckIfCardCanBePlayed(index, d);
			d = playable.d;
			if ((playable.f & 0x10u) == 0u)
				return (AIDecideParameterResult){playable.a, or_a_flags(playable.a), d};
		}
	}

	if (deck_id == EXCAVATION_DECK_ID) {
		/* .HandleExcavationDeck */
		if (remaining >= 46u)
			return (AIDecideParameterResult){remaining, cp_flags(remaining, 46u), d};
		LookForCardIDInHandAndPlayAreaResult fossil = LookForCardIDInHandAndPlayArea(MYSTERIOUS_FOSSIL);
		d = 0xC5u;
		wce06 = (fossil.f & 0x10u) ? 0x1Eu : 0x50u;
	} else {
		if (deck_id == WONDERS_OF_SCIENCE_DECK_ID) {
			/* .HandleWondersOfScienceDeck */
			LookForCardIDInHandListResult found = LookForCardIDInHandList_Bank8(GRIMER);
			d = 0xC5u;
			if ((found.f & 0x10u) == 0u)
				found = LookForCardIDInHandList_Bank8(MUK);
				d = 0xC5u;
			if (found.f & 0x10u)
				return (AIDecideParameterResult){found.a, or_a_flags(found.a), d};
		}
		/* .general_logic */
		if (remaining >= DECK_SIZE - 14u)
			return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 14u), d};
		wce06 = 30u;
	}
	/* .general_logic_got_initial_score */
	uint8_t hand = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (hand < 4u)
		wce06 = (uint8_t)(wce06 + 50u);
	else if (hand >= 9u)
		wce06 = (uint8_t)(wce06 - 30u);
	if (CreateEnergyCardListFromHand(0u).f & 0x10u)
		wce06 = (uint8_t)(wce06 + 40u);
	/* .handle_blastoise: Blastoise in play, no Muk, and no Water Energy in hand. */
	if ((CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK).f & 0x10u) == 0u
	    && (CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE).f & 0x10u) != 0u
	    && (LookForCardIDInHand(WATER_ENERGY).f & 0x10u) != 0u)
		wce06 = (uint8_t)(wce06 + 10u);
	/* .check_hand: `jr c` where `jr nc` was meant, so only a Basic that is
	 * not a Pokemon card counts -- a Basic Energy or a Trainer. */
	(void)CreateHandCardList(0u);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t index = gb_read8(list++);
		if (index == 0xFFu)
			break;
		(void)LoadCardDataToBuffer1_FromDeckIndex(index);
		if (wLoadedCard1Type < TYPE_ENERGY)
			continue;
		if (wLoadedCard1Stage == 0u)
			wce06 = (uint8_t)(wce06 + 10u);
	}
	/* .check_evolutions */
	wce0f = 0u;
	gb_write8((uint16_t)(wce0f_ADDR + 1u), 0u);
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (uint8_t location = PLAY_AREA_ARENA; count != 0u; location++, count--) {
		if (oak_evolution_in_hand(location))
			wce0f = TRUE;
		if (wce08 == TRUE)
			gb_write8((uint16_t)(wce0f_ADDR + 1u), TRUE);
	}
	if (gb_read8((uint16_t)(wce0f_ADDR + 1u)) != 0u && wce0f == 0u)
		wce06 = (uint8_t)(wce06 + 10u);
	/* .check_score */
	uint8_t score = wce06;
	if (score >= 60u)
		return (AIDecideParameterResult){score, (uint8_t)((score == 60u ? 0x80u : 0u) | 0x10u), 0u};
	return (AIDecideParameterResult){score, or_a_flags(score), 0u};
}
/* <<< factory AIDecide_ProfessorOak */

/* >>> factory AIPlay_ProfessorOak */
AIDecideResult AIPlay_ProfessorOak(uint8_t d, uint8_t e)
{
	uint8_t flags = wCurrentAIFlags;
	flags = (uint8_t)(flags | AI_FLAG_USED_PROFESSOR_OAK | AI_FLAG_MODIFIED_HAND);
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ProfessorOak */

/* >>> factory AIPlay_PokemonTrader */
AIMakeDecisionResult AIPlay_PokemonTrader(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	return AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
}
/* <<< factory AIPlay_PokemonTrader */

/* >>> factory AIPlay_EnergyRemoval */
AIDecideResult AIPlay_EnergyRemoval(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_EnergyRemoval */

/* >>> factory AIDecide_Potion_Phase10 */
AIDecidePotionPhase10Result AIDecide_Potion_Phase10(uint8_t d)
{
	/* trainer_cards.asm AIDecide_Potion_Phase10. d is the knockout callee's
	 * exit d, or the knockout damage once `ld d, a` takes it; every helper in
	 * the bench loop brackets itself in `push de` / `pop de`. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, d, 0u, 0u);
	d = ko.d;
	uint8_t e;
	uint8_t prizes;
	if ((ko.f & 0x10u) != 0u) {
		d = ko.a;
		uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
		uint8_t damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
		if (damage > 20u) damage = 20u;
		uint8_t total = (uint8_t)(hp + damage);
		uint8_t remaining = (uint8_t)(total - d);
		if (total >= d && remaining != 0u)
			return (AIDecidePotionPhase10Result){remaining, 0u, d};
		SwapTurn();
		prizes = CountPrizes();
		SwapTurn();
		e = (uint8_t)(prizes - 1u) == 0u ? PLAY_AREA_ARENA : PLAY_AREA_BENCH_1;
	} else {
		e = PLAY_AREA_ARENA;
	}
	for (;;) {
		uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		if (card == 0xffu)
			return (AIDecidePotionPhase10Result){0xffu, 0xc0u, d};
		/* .CheckIfHasAttackWithBoostIfTakenDamageFlag */
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, d, e, 0u);
		if ((unusable.f & 0x10u) == 0u && (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F).f & 0x10u) != 0u) {
			e++;
			continue;
		}
		wSelectedAttack = SECOND_ATTACK;
		unusable = CheckIfSelectedAttackIsUnusable(SECOND_ATTACK, 0u, 0u, 0u, d, e, 0u);
		if ((unusable.f & 0x10u) == 0u && (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F).f & 0x10u) != 0u) {
			e++;
			continue;
		}
		CardDamageResult card_damage = GetCardDamageAndMaxHP(e);
		if (card_damage.a < 20u) {
			e++;
			continue;
		}
		if (e != PLAY_AREA_ARENA) {
			SwapTurn();
			prizes = CountPrizes();
			SwapTurn();
			if ((uint8_t)(prizes - 1u) != 0u) {
				uint8_t chance = Random(10u);
				if (chance < 3u)
					return (AIDecidePotionPhase10Result){chance, (uint8_t)(chance == 0u ? 0x80u : 0u), d};
			}
		}
		if (e == PLAY_AREA_ARENA) {
			AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
			if ((recoil.f & 0x10u) != 0u)
				return (AIDecidePotionPhase10Result){0u, 0x80u, d};
		}
		return (AIDecidePotionPhase10Result){e, 0x10u, d};
	}
}
/* <<< factory AIDecide_Potion_Phase10 */

/* >>> factory AIPlay_SuperPotion */
AIDecideResult AIPlay_SuperPotion(uint8_t d, uint8_t e)
{
	uint8_t card = wAITrainerCardToPlay;
	hTempCardIndex_ff9f = card;
	uint8_t parameter = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = parameter;
	uint8_t discarded = AIPickEnergyCardToDiscard(parameter).a;
	hTemp_ffa0 = discarded;
	CardDamageResult damage = GetCardDamageAndMaxHP(parameter);
	uint8_t retreatCost = damage.a;
	if (retreatCost >= 40u)
		retreatCost = 40u;
	hTempRetreatCostCards = retreatCost;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_SuperPotion */

/* >>> factory AIDecide_Potion_Phase07 */
AIDecidePotionPhase07Result AIDecide_Potion_Phase07(uint8_t d)
{
	/* trainer_cards.asm AIDecide_Potion_Phase07: d follows the three callees
	 * until `ld d, a` takes the knockout damage. */
	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat(d);
	d = retreat.d;
	if ((retreat.f & 0x10u) != 0u)
		return (AIDecidePotionPhase07Result){retreat.a, (uint8_t)(retreat.a == 0u ? 0x80u : 0u), d};
	AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
	d = recoil.d;
	if ((recoil.f & 0x10u) != 0u)
		return (AIDecidePotionPhase07Result){0u, 0x80u, d};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, d, 0u, 0u);
	d = ko.d;
	if ((ko.f & 0x10u) == 0u)
		return (AIDecidePotionPhase07Result){ko.a, (uint8_t)(ko.a == 0u ? 0x80u : 0u), d};
	d = ko.a;
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
	uint8_t heal = damage < 21u ? damage : 20u;
	uint8_t total = (uint8_t)(hp + heal);
	uint8_t remaining = (uint8_t)(total - d);
	if (total < d)
		return (AIDecidePotionPhase07Result){remaining, 0u, d};
	if (remaining == 0u)
		return (AIDecidePotionPhase07Result){remaining, 0x80u, d};
	return (AIDecidePotionPhase07Result){0u, 0x10u, d};
}
/* <<< factory AIDecide_Potion_Phase07 */

/* >>> factory AIPlay_Revive */
AIDecideResult AIPlay_Revive(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Revive */

/* >>> factory AIPlay_Lass */
AIDecideResult AIPlay_Lass(uint8_t d, uint8_t e)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Lass */

/* >>> factory AIPlay_MrFuji */
/* trainer_cards.asm:3870-3878 */
AIDecideResult AIPlay_MrFuji(uint8_t d, uint8_t e)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_MrFuji */

/* >>> factory AIDecide_SuperPotion_Phase08 */
AIDecideSuperPotionPhase08Result AIDecide_SuperPotion_Phase08(uint8_t d)
{
	/* trainer_cards.asm AIDecide_SuperPotion_Phase08: d follows the callees
	 * until `ld d, a` (written twice) takes the knockout damage. The recoil
	 * exit's a is CheckLoadedAttackFlag's masked byte, zero when it carries. */
	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat(d);
	d = retreat.d;
	if ((retreat.f & 0x10u) != 0u)
		return (AIDecideSuperPotionPhase08Result){retreat.a, (uint8_t)(retreat.a == 0u ? 0x80u : 0u), d};
	AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
	d = recoil.d;
	if ((recoil.f & 0x10u) != 0u)
		return (AIDecideSuperPotionPhase08Result){0u, 0x80u, d};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t e = PLAY_AREA_ARENA;
	/* .CheckIfHasEnergies */
	(void)GetPlayAreaCardAttachedEnergies(e);
	if (wTotalAttachedEnergies == 0u)
		return (AIDecideSuperPotionPhase08Result){0u, 0x80u, d};
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(wTotalAttachedEnergies, 0x10u, 0u, 0u, d, e, 0u);
	d = ko.d;
	if ((ko.f & 0x10u) == 0u)
		return (AIDecideSuperPotionPhase08Result){ko.a, (uint8_t)(ko.a == 0u ? 0x80u : 0u), d};
	d = ko.a;
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t damage = GetCardDamageAndMaxHP(e).a;
	if (damage >= 41u)
		damage = 40u;
	uint8_t total = (uint8_t)(hp + damage);
	uint8_t remaining = (uint8_t)(total - d);
	if (total < d || remaining == 0u)
		return (AIDecideSuperPotionPhase08Result){remaining, (uint8_t)(remaining == 0u ? 0x80u : 0u), d};
	return (AIDecideSuperPotionPhase08Result){e, 0x10u, d};
}
/* <<< factory AIDecide_SuperPotion_Phase08 */

/* >>> factory AIPlay_SuperEnergyRetrieval */
AIDecideResult AIPlay_SuperEnergyRetrieval(uint8_t d, uint8_t e)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	hTempRetreatCostCards = wce1b;
	gb_write8((uint16_t)(hTempRetreatCostCards_ADDR + 1u), wce1c);
	if (wce1c != 0xffu) {
		gb_write8((uint16_t)(hTempRetreatCostCards_ADDR + 2u), wce1d);
		if (wce1d != 0xffu) {
			gb_write8((uint16_t)(hTempRetreatCostCards_ADDR + 3u), wce1e);
			if (wce1e != 0xffu)
				gb_write8((uint16_t)(hTempRetreatCostCards_ADDR + 4u), 0xffu);
		}
	}
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, d, e);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_SuperEnergyRetrieval */
