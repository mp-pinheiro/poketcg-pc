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
#define GHOST_DECK_ID 0x2Du
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
FindDupResult FindDuplicateCards(uint16_t hl)
{
	wce0f = 0xFFu;
	gb_write8((uint16_t)(wce0f_ADDR + 1u), 0xFFu);
	uint16_t outer = hl;
	for (;;) {
		uint8_t idx = gb_read8(outer);
		outer = (uint16_t)(outer + 1u);
		if (idx == 0xFFu)
			break;
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
		return (FindDupResult){0xFFu, 0x90u, outer};
	uint8_t a = (lo != 0xFFu) ? lo : hi;
	return (FindDupResult){a, (uint8_t)(a == 0u ? 0x80u : 0x00u), outer};
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
	return (PickPokedexResult){0xFFu, 0x90u};
}
/* <<< factory PickPokedexCards */
/* >>> factory AIDecide_Recycle */
AIDecideParameterResult AIDecide_Recycle(void)
{
	/* trainer_cards.asm AIDecide_Recycle: the five priority slots live in
	 * wce08..wce0c and the first one filled is the card to recycle. */
	CardListResult discard = CreateDiscardPileCardList(0);
	if (discard.f & 0x10u)
		return (AIDecideParameterResult){discard.a, or_a_flags(discard.a)};
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
			return (AIDecideParameterResult){chosen, 0x10u};
	}
	return (AIDecideParameterResult){0xFFu, 0x00u};
}
/* <<< factory AIDecide_Recycle */

/* >>> factory AIDecide_Maintenance */
AIDecideMaintenanceResult AIDecide_Maintenance(void)
{
	DuelistVarResult hand = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (wOpponentDeckID == 0x0Du) {
		if (Random(10u) >= 2u || hand.a < 3u)
			return (AIDecideMaintenanceResult){hand.a,
				(uint8_t)(hand.a == 0u ? 0x80u : 0u)};
		(void)CreateHandCardList(0);
		TempListResult count = CountCardsInDuelTempList();
		(void)ShuffleCards(count.a, wDuelTempList_ADDR);
		uint16_t p = wDuelTempList_ADDR;
		uint8_t target = wAITrainerCardToPlay, found = 0, out = 0;
		while (found < 2u) {
			uint8_t card = gb_read8(p++);
			if (card == 0xFFu)
				return (AIDecideMaintenanceResult){0, 0x00u};
			if (card == target)
				continue;
			gb_write8((uint16_t)(wce1a_ADDR + out++), card);
			found++;
		}
		return (AIDecideMaintenanceResult){0, 0x10u};
	}
	if (hand.a < 4u)
		return (AIDecideMaintenanceResult){hand.a,
			(uint8_t)(hand.a == 0u ? 0x80u : 0u)};
	(void)CreateHandCardList(0);
	FindAndRemoveCardFromList(wAITrainerCardToPlay, wDuelTempList_ADDR);
	FindDupResult first = FindDuplicateCards(wDuelTempList_ADDR);
	if (first.a == 0xFFu)
		return (AIDecideMaintenanceResult){first.a, 0x00u};
	wce1a = first.a;
	FindAndRemoveCardFromList(first.a, wDuelTempList_ADDR);
	FindDupResult second = FindDuplicateCards(wDuelTempList_ADDR);
	if (second.a == 0xFFu)
		return (AIDecideMaintenanceResult){second.a, 0x00u};
	wce1b = second.a;
	return (AIDecideMaintenanceResult){second.a, 0x10u};
}
/* <<< factory AIDecide_Maintenance */
/* >>> factory AIDecide_Lass */
AIDecideParameterResult AIDecide_Lass(void)
{
	uint8_t hand_count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (hand_count < 7u)
		return (AIDecideParameterResult){hand_count, or_a_flags(hand_count)};
	(void)CreateHandCardList(hand_count);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			return (AIDecideParameterResult){0xFFu, 0x90u};
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (card_id == LASS)
			continue;
		uint8_t type = gb_read8(wLoadedCard1Type_ADDR);
		if (type == TYPE_TRAINER)
			return (AIDecideParameterResult){type, 0x00u};
	}
}
/* <<< factory AIDecide_Lass */

/* >>> factory AIDecide_Imakuni */
AIDecideParameterResult AIDecide_Imakuni(void)
{
	uint8_t status = (uint8_t)(GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a & CNF_SLP_PRZ);
	if (status == CONFUSED)
		return (AIDecideParameterResult){status, 0x00u};
	return (AIDecideParameterResult){status, 0x10u};
}
/* <<< factory AIDecide_Imakuni */
/* >>> factory AIDecide_PokemonFlute */
AIDecidePokemonFluteResult AIDecide_PokemonFlute(uint8_t c)
{
	SwapTurn();
	CardListResult discard = CreateDiscardPileCardList(c);
	SwapTurn();
	if (discard.f & 0x10u)
		return (AIDecidePokemonFluteResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u)};
	uint8_t count = GetNonTurnDuelistVariable(0xEFu).a;
	if (count >= 6u)
		return (AIDecidePokemonFluteResult){count, (uint8_t)(count == 0u ? 0x80u : 0u)};
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
	if (wOpponentDeckID == 0x34u) {
		if (Random(10u) >= 2u)
			return (AIDecidePokemonFluteResult){0, 0};
		return (AIDecidePokemonFluteResult){wce08, wce08 == 0xFFu ? 0u : 0x10u};
	}
	if (wce06 >= 50u)
		return (AIDecidePokemonFluteResult){wce06, 0};
	return (AIDecidePokemonFluteResult){wce08, 0x10u};
}
/* <<< factory AIDecide_PokemonFlute */
/* >>> factory AIDecide_ClefairyDollOrMysteriousFossil */
/* trainer_cards.asm:4784-4812. The play area count is parked in wce06 for
 * the later phases; a Wigglytuff in the arena plays the card outright, with
 * `cp WIGGLYTUFF`'s Z under the carry. */
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(void)
{
	uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	if (count >= MAX_PLAY_AREA_POKEMON)
		return (AIDecidePokemonFluteResult){count, count == 0u ? 0x80u : 0u};
	wce06 = count;
	uint8_t arena = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	uint8_t card_id = (uint8_t)GetCardIDFromDeckIndex(arena);
	if (card_id == WIGGLYTUFF)
		return (AIDecidePokemonFluteResult){card_id, 0x90u};
	if (count < 4u)
		return (AIDecidePokemonFluteResult){count, 0x10u};
	return (AIDecidePokemonFluteResult){count, count == 0u ? 0x80u : 0u};
}
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */

/* >>> factory AIDecide_Defender_Phase14 */
AIDecideParameterResult AIDecide_Defender_Phase14(void)
{
	/* trainer_cards.asm AIDecide_Defender_Phase14: play Defender when the
	 * chosen attack's recoil, after the card's own weakness and resistance
	 * and the 20 Defender prevents, would still not knock the card out. */
	AttackFlagResult recoil = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | HIGH_RECOIL_F);
	if ((recoil.f & 0x10u) == 0u)
		recoil = CheckLoadedAttackFlag(ATTACK_FLAG1_ADDRESS | LOW_RECOIL_F);
	if ((recoil.f & 0x10u) == 0u)
		return (AIDecideParameterResult){recoil.a, or_a_flags(recoil.a)};
	(void)LoadCardDataToBuffer2_FromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	uint8_t damage = wSelectedAttack == 0u ? wLoadedCard2Atk1EffectParam : wLoadedCard2Atk2EffectParam;
	uint8_t color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardWeakness() & color)
		damage = (uint8_t)(damage << 1);
	color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardResistance() & color) {
		uint8_t reduced = (uint8_t)(damage - 30u);
		if (damage < 30u)
			return (AIDecideParameterResult){reduced, or_a_flags(reduced)};
		damage = reduced;
	}
	if (damage == 0u)
		return (AIDecideParameterResult){0u, 0x80u};
	damage = (uint8_t)(damage - 20u);
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - damage);
	if (hp <= damage)
		return (AIDecideParameterResult){left, or_a_flags(left)};
	return (AIDecideParameterResult){left, 0x10u};
}
/* <<< factory AIDecide_Defender_Phase14 */

/* >>> factory AIDecide_Bill */
AIDecideParameterResult AIDecide_Bill(void)
{
	/* trainer_cards.asm:1428-1432: a is the count the cp leaves. */
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 9u)};
}
/* <<< factory AIDecide_Bill */

/* >>> factory AIDecide_Gambler */
AIDecideParameterResult AIDecide_Gambler(void)
{
	if (wOpponentDeckID == IMAKUNI_DECK_ID) {
		/* .imakuni: play it two times in ten; a is the roll either way. */
		uint8_t roll = Random(10u);
		if (roll < 2u)
			return (AIDecideParameterResult){roll, 0x10u};
		return (AIDecideParameterResult){roll, or_a_flags(roll)};
	}
	uint8_t mill = (uint8_t)(wAIBarrierFlagCounter & AI_MEWTWO_MILL);
	if (mill == 0u)
		return (AIDecideParameterResult){0u, 0x80u};
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	if (remaining >= DECK_SIZE - 4u)
		return (AIDecideParameterResult){remaining, (uint8_t)((remaining == DECK_SIZE - 4u ? 0x80u : 0u) | 0x10u)};
	return (AIDecideParameterResult){remaining, or_a_flags(remaining)};
}
/* <<< factory AIDecide_Gambler */

/* >>> factory AIDecide_Revive */
AIDecideReviveResult AIDecide_Revive(void)
{
	CardListResult discard = CreateDiscardPileCardList(0);
	if (discard.f & 0x10u)
		return (AIDecideReviveResult){discard.a, 0x80u};
	if (GetTurnDuelistVariable(0xEFu).a >= 4u) {
		uint8_t count = GetTurnDuelistVariable(0xEFu).a;
		return (AIDecideReviveResult){count, 0};
	}
	for (uint16_t p = wDuelTempList_ADDR;; p++) {
		uint8_t index = gb_read8(p);
		if (index == 0xFFu)
			return (AIDecideReviveResult){0xFFu, 0};
		uint8_t card = LoadCardDataToBuffer1_FromDeckIndex(index);
		if (card == 0x88u || card == 0x87u)
			return (AIDecideReviveResult){index, 0x90u};
		if (card == 0xBAu)
			return (AIDecideReviveResult){0, 0x10u};
	}
}
/* <<< factory AIDecide_Revive */

/* >>> factory AIDecide_ImposterProfessorOak */
AIDecideParameterResult AIDecide_ImposterProfessorOak(void)
{
	uint8_t remaining = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	uint8_t hand = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (remaining < DECK_SIZE - 14u) {
		if (hand < 9u)
			return (AIDecideParameterResult){hand, or_a_flags(hand)};
		return (AIDecideParameterResult){hand, (uint8_t)((hand == 9u ? 0x80u : 0u) | 0x10u)};
	}
	if (hand < 6u)
		return (AIDecideParameterResult){hand, 0x10u};
	return (AIDecideParameterResult){hand, or_a_flags(hand)};
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
AIDecidePokedexResult AIDecide_Pokedex(void)
{
	uint8_t counter = wAIPokedexCounter;
	if (counter < 6u)
		return (AIDecidePokedexResult){counter, (uint8_t)(counter == 0u ? 0x80u : 0u)};
	DuelistVarResult notindeck = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK);
	if (notindeck.a >= (DECK_SIZE - 4u))
		return (AIDecidePokedexResult){notindeck.a, (uint8_t)(notindeck.a == 0u ? 0x80u : 0u)};
	uint8_t roll = Random(10u);
	if (roll >= 3u)
		return (AIDecidePokedexResult){roll, (uint8_t)(roll == 0u ? 0x80u : 0u)};
	PickPokedexResult picked = PickPokedexCards();
	return (AIDecidePokedexResult){picked.a, picked.f};
}
/* <<< factory AIDecide_Pokedex */

/* >>> factory AIDecide_ItemFinder */
AIDecide_ItemFinderResult AIDecide_ItemFinder(void)
{
	CardListResult discard = CreateDiscardPileCardList(0u);
	uint8_t a = discard.a;
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
			FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR);
			a = dup1.a;
			if (!(dup1.f & 0x10u)) {
				wce1a = dup1.a;
				FindAndRemoveCardFromList(dup1.a, wDuelTempList_ADDR);
				FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR);
				a = dup2.a;
				if (!(dup2.f & 0x10u)) {
					wce1b = dup2.a;
					return (AIDecide_ItemFinderResult){wce06, 0x10u};
				}
			}
		}
	}
	return (AIDecide_ItemFinderResult){a, (uint8_t)(a == 0u ? 0x80u : 0u)};
}
/* <<< factory AIDecide_ItemFinder */

/* >>> factory AIDecide_EnergyRetrieval */
AIDecideEnergyRetrievalResult AIDecide_EnergyRetrieval(uint8_t a)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u)};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideEnergyRetrievalResult){blastoise.a, (uint8_t)(blastoise.a == 0u ? 0x80u : 0u)};
		}
	}

	(void)CreateHandCardList(0u);
	FindDupResult dup = FindDuplicateCards(wDuelTempList_ADDR);
	if (dup.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){dup.a, (uint8_t)(dup.a == 0u ? 0x80u : 0u)};
	uint8_t saved_card = dup.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	if (discard.f & 0x10u)
		return (AIDecideEnergyRetrievalResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u)};

	wce1a = 0xFFu;
	wce1b = 0xFFu;
	wce1c = 0xFFu;

	uint8_t d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
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
				return (AIDecideEnergyRetrievalResult){saved_card, 0x10u};
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
			return (AIDecideEnergyRetrievalResult){saved_card, 0x10u};
		}
		wce1a = entry;
		RemoveCardFromList(&hl2);
	}

	if (wce1a != 0xFFu)
		return (AIDecideEnergyRetrievalResult){saved_card, 0x10u};
	return (AIDecideEnergyRetrievalResult){wce1a, (uint8_t)(wce1a == 0u ? 0x80u : 0u)};
}
/* <<< factory AIDecide_EnergyRetrieval */

/* >>> factory AIDecide_SuperEnergyRetrieval */
AIDecideSuperEnergyRetrievalResult AIDecide_SuperEnergyRetrieval(uint8_t a)
{
	CoreCardListResult hand_energy = CreateEnergyCardListFromHand(a);
	if (!(hand_energy.f & 0x10u))
		return (AIDecideSuperEnergyRetrievalResult){hand_energy.a, (uint8_t)(hand_energy.a == 0u ? 0x80u : 0u)};

	if (wOpponentDeckID == GO_GO_RAIN_DANCE_DECK_ID) {
		PkmnPowerCountResult muk = CountPokemonWithActivePkmnPowerInBothPlayAreas(MUK);
		if (!(muk.f & 0x10u)) {
			PkmnPowerCountResult blastoise = CountTurnDuelistPokemonWithActivePkmnPower(BLASTOISE);
			if (!(blastoise.f & 0x10u))
				return (AIDecideSuperEnergyRetrievalResult){blastoise.a, (uint8_t)(blastoise.a == 0u ? 0x80u : 0u)};
		}
	}

	(void)CreateHandCardList(0u);
	FindDupResult dup1 = FindDuplicateCards(wDuelTempList_ADDR);
	if (dup1.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup1.a, (uint8_t)(dup1.a == 0u ? 0x80u : 0u)};
	wce06 = dup1.a;

	FindAndRemoveCardFromList(wce06, wDuelTempList_ADDR);
	FindDupResult dup2 = FindDuplicateCards(wDuelTempList_ADDR);
	if (dup2.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){dup2.a, (uint8_t)(dup2.a == 0u ? 0x80u : 0u)};
	wce08 = dup2.a;

	FindBasicEnergyCardsInLocationResult discard = FindBasicEnergyCardsInLocation(CARD_LOCATION_DISCARD_PILE);
	if (discard.f & 0x10u)
		return (AIDecideSuperEnergyRetrievalResult){discard.a, (uint8_t)(discard.a == 0u ? 0x80u : 0u)};

	wce1b = 0xFFu;
	wce1c = 0xFFu;
	wce1d = 0xFFu;
	wce1e = 0xFFu;
	wce1f = 0xFFu;

	uint8_t d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
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
				return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u};
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
			return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u};
		}
	}

	if (wce1b != 0xFFu) {
		wce1a = wce08;
		return (AIDecideSuperEnergyRetrievalResult){wce06, 0x10u};
	}
	return (AIDecideSuperEnergyRetrievalResult){0xFFu, 0x00u};
}
/* <<< factory AIDecide_SuperEnergyRetrieval */

/* >>> factory AIDecide_PokemonBreeder */
AIDecidePokemonBreederResult AIDecide_PokemonBreeder(uint16_t hl_in)
{
	PrehistoricPowerResult power = IsPrehistoricPowerActive(hl_in);
	if (power.f & 0x10u)
		return (AIDecidePokemonBreederResult){power.a, power.f};

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	(void)CreateHandCardList(0u);
	uint16_t hl = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl);
		hl++;
		if (deck_index == 0xFFu)
			break;

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
		return (AIDecidePokemonBreederResult){best_loc, 0x10u};
	}

	ClearMemory_Bank8(7u, wce08_ADDR);
	wce06 = 0u;
	(void)CreateHandCardList(0u);
	uint16_t hl2 = wDuelTempList_ADDR;

	for (;;) {
		uint8_t deck_index = gb_read8(hl2);
		hl2++;
		if (deck_index == 0xFFu)
			break;

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
		return (AIDecidePokemonBreederResult){0u, 0x80u};

	wce06 = 0u;
	wce07 = 0xFFu;
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
		return (AIDecidePokemonBreederResult){0xFFu, 0x00u};

	wce1a = gb_read8((uint16_t)(wce0f_ADDR + wce07));
	return (AIDecidePokemonBreederResult){wce07, 0x10u};
}
/* <<< factory AIDecide_PokemonBreeder */

/* >>> factory AIDecide_PokemonTrader_LegendaryMoltres */
AIDecide_PokemonTrader_LegendaryMoltresResult AIDecide_PokemonTrader_LegendaryMoltres(void)
{
	LookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MOLTRES_LV37, MOLTRES_LV35);
	if (!(r.f & 0x10u)) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryMoltresResult){r.a, f};
	}
	wce1a = r.a;
	return (AIDecide_PokemonTrader_LegendaryMoltresResult){r.e, 0x10u};
}
/* <<< factory AIDecide_PokemonTrader_LegendaryMoltres */

/* >>> factory AIDecide_PokemonTrader_StrangePower */
AIDecide_PokemonTrader_StrangePowerResult AIDecide_PokemonTrader_StrangePower(void)
{
	LookForCardIDToTradeWithDifferentHandCardResult r = LookForCardIDToTradeWithDifferentHandCard(MR_MIME, MR_MIME);
	if (!(r.f & 0x10u)) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_StrangePowerResult){r.a, f};
	}
	wce1a = r.a;
	return (AIDecide_PokemonTrader_StrangePowerResult){r.e, 0x10u};
}
/* <<< factory AIDecide_PokemonTrader_StrangePower */

/* >>> factory AIDecide_PokemonTrader_LegendaryArticuno */
AIDecide_PokemonTrader_LegendaryArticunoResult AIDecide_PokemonTrader_LegendaryArticuno(void)
{
	LookForCardIDInHandAndPlayAreaResult r = LookForCardIDInHandAndPlayArea(ARTICUNO_LV35);
	if (r.f & 0x10u) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f};
	}
	r = LookForCardIDInHandAndPlayArea(LAPRAS);
	if (r.f & 0x10u) {
		uint8_t f = (r.a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f};
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
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){r.a, f};
		}
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DEWGONG);
		if (!(loc.f & 0x10u)) {
			uint8_t f = (loc.a == 0u) ? 0x80u : 0u;
			return (AIDecide_PokemonTrader_LegendaryArticunoResult){loc.a, f};
		}
		wce1a = loc.a;
	}
	CheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(CHANSEY);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u};
	h = CheckIfHasCardIDInHand(DITTO);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u};
	h = CheckIfHasCardIDInHand(ARTICUNO_LV37);
	if (h.f & 0x10u)
		return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, 0x10u};
	uint8_t f = (h.a == 0u) ? 0x80u : 0u;
	return (AIDecide_PokemonTrader_LegendaryArticunoResult){h.a, f};
}
/* <<< factory AIDecide_PokemonTrader_LegendaryArticuno */

/* >>> factory AIDecide_ComputerSearch_FireCharge */
AIDecide_ComputerSearch_FireChargeResult AIDecide_ComputerSearch_FireCharge(uint8_t b, uint8_t c)
{
	uint8_t target;
	LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(CHANSEY);
	if (!(h.f & 0x10u)) {
		target = CHANSEY;
	} else {
		h = LookForCardIDInHandList_Bank8(TAUROS);
		if (!(h.f & 0x10u)) {
			target = TAUROS;
		} else {
			h = LookForCardIDInHandList_Bank8(JIGGLYPUFF_LV12);
			if (!(h.f & 0x10u)) {
				target = JIGGLYPUFF_LV12;
			} else {
				uint8_t f = (h.a == 0u) ? 0x80u : 0u;
				return (AIDecide_ComputerSearch_FireChargeResult){h.a, f};
			}
		}
	}

	LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, target);
	if (!(loc.f & 0x10u)) {
		uint8_t f = (loc.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){loc.a, f};
	}
	wce06 = loc.a;

	(void)CreateHandCardList(0u);
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult r1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	if (!(r1.f & 0x10u)) {
		uint8_t f = (r1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){r1.a, f};
	}
	wce1a = r1.a;
	RemoveFromListDifferentCardOfGivenTypeResult r2 =
		RemoveFromListDifferentCardOfGivenType(r1.b, r1.c, r1.d, r1.e, r1.hl);
	if (!(r2.f & 0x10u)) {
		uint8_t f = (r2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_FireChargeResult){r2.a, f};
	}
	wce1b = r2.a;
	return (AIDecide_ComputerSearch_FireChargeResult){wce06, 0x90u};
}
/* <<< factory AIDecide_ComputerSearch_FireCharge */

/* >>> factory AIDecide_ComputerSearch_Anger */
AIDecide_ComputerSearch_AngerResult AIDecide_ComputerSearch_Anger(uint8_t b, uint8_t c)
{
	uint8_t a_val;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RATICATE, RATTATA);
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(RATTATA, RATICATE);
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ARCANINE_LV34, GROWLITHE);
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(GROWLITHE, ARCANINE_LV34);
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DODRIO, DODUO);
	a_val = r.a;
	if (r.f & 0x10u) goto find_discard_cards;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DODUO, DODRIO);
	a_val = r2.a;
	if (r2.f & 0x10u) goto find_discard_cards;

	{
		uint8_t f = (a_val == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){a_val, f};
	}

find_discard_cards:
	wce06 = a_val;
	(void)CreateHandCardList(0u);
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult rm1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	if (!(rm1.f & 0x10u)) {
		uint8_t f = (rm1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){rm1.a, f};
	}
	wce1a = rm1.a;
	RemoveFromListDifferentCardOfGivenTypeResult rm2 =
		RemoveFromListDifferentCardOfGivenType(rm1.b, rm1.c, rm1.d, rm1.e, rm1.hl);
	if (!(rm2.f & 0x10u)) {
		uint8_t f = (rm2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_AngerResult){rm2.a, f};
	}
	wce1b = rm2.a;
	return (AIDecide_ComputerSearch_AngerResult){wce06, 0x90u};
}
/* <<< factory AIDecide_ComputerSearch_Anger */

/* >>> factory AIDecide_ComputerSearch_WondersOfScience */
AIDecide_ComputerSearch_WondersOfScienceResult AIDecide_ComputerSearch_WondersOfScience(uint8_t b, uint8_t c)
{
	uint8_t a_val;
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a < 5u) {
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PROFESSOR_OAK);
		a_val = loc.a;
		if (loc.f & 0x10u) goto find_discard_cards;
	}

	{
		LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(GRIMER);
		if (!(h.f & 0x10u)) {
			LookForCardIDInLocationBank8Result loc2 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GRIMER);
			a_val = loc2.a;
			if (loc2.f & 0x10u) goto find_discard_cards;
			goto no_carry;
		}
		h = LookForCardIDInHandList_Bank8(MUK);
		if (!(h.f & 0x10u)) {
			LookForCardIDInLocationBank8Result loc3 = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MUK);
			a_val = loc3.a;
			if (loc3.f & 0x10u) goto find_discard_cards;
			goto no_carry;
		}
		a_val = h.a;
	}

no_carry: ;
	{
		uint8_t f = (a_val == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){a_val, f};
	}

find_discard_cards:
	wce06 = a_val;
	(void)CreateHandCardList(0u);
	uint8_t trainer_to_play = wAITrainerCardToPlay;
	RemoveFromListDifferentCardOfGivenTypeResult rm1 =
		RemoveFromListDifferentCardOfGivenType(b, c, 0u, trainer_to_play, wDuelTempList_ADDR);
	if (!(rm1.f & 0x10u)) {
		uint8_t f = (rm1.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){rm1.a, f};
	}
	wce1a = rm1.a;
	RemoveFromListDifferentCardOfGivenTypeResult rm2 =
		RemoveFromListDifferentCardOfGivenType(rm1.b, rm1.c, rm1.d, rm1.e, rm1.hl);
	if (!(rm2.f & 0x10u)) {
		uint8_t f = (rm2.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_WondersOfScienceResult){rm2.a, f};
	}
	wce1b = rm2.a;
	return (AIDecide_ComputerSearch_WondersOfScienceResult){wce06, 0x90u};
}
/* <<< factory AIDecide_ComputerSearch_WondersOfScience */

/* >>> factory AIDecide_ComputerSearch_RockCrusher */
AIDecide_ComputerSearch_RockCrusherResult AIDecide_ComputerSearch_RockCrusher(uint8_t b, uint8_t c)
{
	uint8_t final_a;
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a == 3u) {
		LookForCardIDInLocationBank8Result oak = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PROFESSOR_OAK);
		if (!(oak.f & 0x10u)) {
			final_a = oak.a;
			goto no_carry;
		}
		wce06 = oak.a;
		wce1a = 0xFFu;
		wce1b = 0xFFu;
		(void)CreateHandCardList(c);
		uint16_t scan = wDuelTempList_ADDR;
		uint16_t store = wce1a_ADDR;
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
			return (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x10u};
		final_a = 0xFFu;
		goto no_carry;
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GRAVELER);
		if (loc.f & 0x10u) {
			wce06 = loc.a;
			LookForCardIDInHandAndPlayAreaResult geo = LookForCardIDInHandAndPlayArea(GEODUDE);
			if (geo.f & 0x10u) {
				LookForCardIDInHandListResult grav_hand = LookForCardIDInHandList_Bank8(GRAVELER);
				if (!(grav_hand.f & 0x10u)) {
					(void)CreateHandCardList(c);
					uint16_t hl = wDuelTempList_ADDR;
					(void)RemoveCardIDInList(&hl, GEODUDE);
					goto find_discard_cards_2;
				}
			}
		}
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GOLEM);
		if (loc.f & 0x10u) {
			wce06 = loc.a;
			LookForCardIDInPlayAreaResult grav_pa = LookForCardIDInPlayArea_Bank8(GRAVELER, b);
			if (grav_pa.f & 0x10u) {
				LookForCardIDInHandListResult golem_hand = LookForCardIDInHandList_Bank8(GOLEM);
				if (!(golem_hand.f & 0x10u)) {
					(void)CreateHandCardList(c);
					goto find_discard_cards_2;
				}
			}
		}
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DUGTRIO);
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
		if (dug_hand.f & 0x10u) {
			final_a = dug_hand.a;
			goto no_carry;
		}
		(void)CreateHandCardList(c);
		goto find_discard_cards_2;
	}

no_carry: ;
	{
		uint8_t f = (final_a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearch_RockCrusherResult){final_a, f};
	}

find_discard_cards_2:
	wce1a = 0xFFu;
	wce1b = 0xFFu;
	{
		uint16_t bc_ptr = wce1a_ADDR;
		uint8_t d = 0u;
		uint8_t trainer_to_play2 = wAITrainerCardToPlay;
		for (;;) {
			RemoveFromListDifferentCardOfGivenTypeResult r =
				RemoveFromListDifferentCardOfGivenType(b, c, d, trainer_to_play2, wDuelTempList_ADDR);
			if (r.f & 0x10u) {
				gb_write8(bc_ptr, r.a);
				bc_ptr = (uint16_t)(bc_ptr + 1u);
				if (gb_read8(wce1b_ADDR) != 0xFFu)
					return (AIDecide_ComputerSearch_RockCrusherResult){wce06, 0x10u};
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
AIDecide_ComputerSearchResult AIDecide_ComputerSearch(uint8_t b, uint8_t c)
{
	DuelistVarResult hand_count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND);
	if (hand_count.a < 3u) {
		uint8_t f = (hand_count.a == 0u) ? 0x80u : 0u;
		return (AIDecide_ComputerSearchResult){hand_count.a, f};
	}
	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == ROCK_CRUSHER_DECK_ID) {
		AIDecide_ComputerSearch_RockCrusherResult r = AIDecide_ComputerSearch_RockCrusher(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	if (deck_id == WONDERS_OF_SCIENCE_DECK_ID) {
		AIDecide_ComputerSearch_WondersOfScienceResult r = AIDecide_ComputerSearch_WondersOfScience(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	if (deck_id == FIRE_CHARGE_DECK_ID) {
		AIDecide_ComputerSearch_FireChargeResult r = AIDecide_ComputerSearch_FireCharge(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	if (deck_id == ANGER_DECK_ID) {
		AIDecide_ComputerSearch_AngerResult r = AIDecide_ComputerSearch_Anger(b, c);
		return (AIDecide_ComputerSearchResult){r.a, r.f};
	}
	uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
	return (AIDecide_ComputerSearchResult){deck_id, f};
}
/* <<< factory AIDecide_ComputerSearch */

/* >>> factory AIDecide_PokemonTrader_LegendaryRonald */
AIDecide_PokemonTrader_LegendaryRonaldResult AIDecide_PokemonTrader_LegendaryRonald(void)
{
	uint8_t target_a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(FLAREON_LV22, EEVEE);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VAPOREON_LV29, EEVEE);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(JOLTEON_LV24, EEVEE);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, FLAREON_LV22);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, VAPOREON_LV29);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(EEVEE, JOLTEON_LV24);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONAIR, DRATINI);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONITE_LV41, DRAGONAIR);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DRATINI, DRAGONAIR);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(DRAGONAIR, DRAGONITE_LV41);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	goto no_carry;

choose_hand: ;
	wce1a = target_a;
	{
		LookForCardIDInHandListResult h = LookForCardIDInHandList_Bank8(ZAPDOS_LV68);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u};
		h = LookForCardIDInHandList_Bank8(ARTICUNO_LV37);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u};
		h = LookForCardIDInHandList_Bank8(MOLTRES_LV37);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryRonaldResult){h.a, 0x90u};
		target_a = h.a;
	}

no_carry: ;
	{
		uint8_t f = (target_a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryRonaldResult){target_a, f};
	}
}
/* <<< factory AIDecide_PokemonTrader_LegendaryRonald */

/* >>> factory AIDecide_PokemonTrader_SoundOfTheWaves */
AIDecide_PokemonTrader_SoundOfTheWavesResult AIDecide_PokemonTrader_SoundOfTheWaves(void)
{
	uint8_t target_a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DEWGONG, SEEL);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(SEEL, DEWGONG);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(KINGLER, KRABBY);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(KRABBY, KINGLER);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CLOYSTER, SHELLDER);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(SHELLDER, CLOYSTER);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(SEADRA, HORSEA);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(HORSEA, SEADRA);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(TENTACRUEL, TENTACOOL);
	target_a = r.a;
	if (r.f & 0x10u) goto choose_hand;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(TENTACOOL, TENTACRUEL);
	target_a = r2.a;
	if (r2.f & 0x10u) goto choose_hand;

	goto no_carry;

choose_hand: ;
	wce1a = target_a;
	{
		CheckIfHasCardIDInHandResult h = CheckIfHasCardIDInHand(SEEL);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(KRABBY);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(HORSEA);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(SHELLDER);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(TENTACOOL);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_SoundOfTheWavesResult){h.a, h.f};
		target_a = h.a;
	}

no_carry: ;
	{
		uint8_t f = (target_a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_SoundOfTheWavesResult){target_a, f};
	}
}
/* <<< factory AIDecide_PokemonTrader_SoundOfTheWaves */

/* >>> factory AIDecide_PokemonTrader_LegendaryDragonite */
AIDecide_PokemonTrader_LegendaryDragoniteResult AIDecide_PokemonTrader_LegendaryDragonite(void)
{
	uint8_t final_a;
	CountOppEnergyCardsInHandAndAttachedResult energy = CountOppEnergyCardsInHandAndAttached();
	uint8_t need_kangaskhan = 0u;
	if (energy.a < 5u) {
		need_kangaskhan = 1u;
	} else {
		uint8_t pokemon_count = CountPokemonCardsInHandAndInPlayArea(0u);
		if (pokemon_count < 5u)
			need_kangaskhan = 1u;
	}

	if (!need_kangaskhan) {
		LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
		LookForCardIDInDeck_GivenCardIDInHandResult r2;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(GYARADOS, MAGIKARP);
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(MAGIKARP, GYARADOS);
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONAIR, DRATINI);
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(DRAGONITE_LV41, DRAGONAIR);
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(DRATINI, DRAGONAIR);
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(DRAGONAIR, DRAGONITE_LV41);
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARMELEON, CHARMANDER);
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARIZARD, CHARMELEON);
		final_a = r.a;
		if (r.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(CHARMANDER, CHARMELEON);
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		r2 = LookForCardIDInDeck_GivenCardIDInHand(CHARMELEON, CHARIZARD);
		final_a = r2.a;
		if (r2.f & 0x10u) goto choose_hand;

		goto no_carry;
	}

	{
		LookForCardIDInLocationBank8Result loc = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, KANGASKHAN);
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
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(CHARMELEON);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(GYARADOS);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(MAGIKARP);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(CHARMANDER);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f};
		h = CheckIfHasCardIDInHand(DRATINI);
		if (h.f & 0x10u)
			return (AIDecide_PokemonTrader_LegendaryDragoniteResult){h.a, h.f};
		final_a = h.a;
	}

no_carry: ;
	{
		uint8_t f = (final_a == 0u) ? 0x80u : 0u;
		return (AIDecide_PokemonTrader_LegendaryDragoniteResult){final_a, f};
	}
}
/* <<< factory AIDecide_PokemonTrader_LegendaryDragonite */

/* >>> factory AIDecide_Pokeball */
AIDecide_PokeballResult AIDecide_Pokeball(void)
{
	uint8_t deck_id = wOpponentDeckID;

	if (deck_id == FIRE_CHARGE_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, CHANSEY);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, TAUROS);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, JIGGLYPUFF_LV12);
		return (AIDecide_PokeballResult){r.a, r.f};
	}

	if (deck_id == HARD_POKEMON_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, RHYHORN);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, RHYDON);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, ONIX);
		return (AIDecide_PokeballResult){r.a, r.f};
	}

	if (deck_id == PIKACHU_DECK_ID) {
		LookForCardIDInLocationBank8Result r;
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV14);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV16);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_ALT_LV16);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV12);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, FLYING_PIKACHU);
		return (AIDecide_PokeballResult){r.a, r.f};
	}

	if (deck_id == ETCETERA_DECK_ID) {
		LookForCardIDInHandListResult h;
		LookForCardIDInLocationBank8Result r;

		h = LookForCardIDInHandList_Bank8(FIRE_ENERGY);
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(CHARMANDER);
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MAGMAR_LV31);
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, CHARMANDER);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MAGMAR_LV31);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(LIGHTNING_ENERGY);
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(PIKACHU_LV12);
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MAGNEMITE_LV13);
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, PIKACHU_LV12);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MAGNEMITE_LV13);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(FIGHTING_ENERGY);
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(DIGLETT);
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(MACHOP);
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, DIGLETT);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, MACHOP);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
				}
			}
		}

		h = LookForCardIDInHandList_Bank8(PSYCHIC_ENERGY);
		if (h.f & 0x10u) {
			h = LookForCardIDInHandList_Bank8(GASTLY_LV8);
			if (!(h.f & 0x10u)) {
				h = LookForCardIDInHandList_Bank8(JYNX);
				if (!(h.f & 0x10u)) {
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, GASTLY_LV8);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
					r = LookForCardIDInLocation_Bank8(CARD_LOCATION_DECK, JYNX);
					if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
				}
			}
		}

		uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
		return (AIDecide_PokeballResult){deck_id, f};
	}

	if (deck_id == LOVELY_NIDORAN_DECK_ID) {
		LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
		LookForCardIDInDeck_GivenCardIDInHandResult r2;

		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDORINO, NIDORANM);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDOKING, NIDORINO);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORANM, NIDORINO);
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORINO, NIDOKING);
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDORINA, NIDORANF);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NIDOQUEEN, NIDORINA);
		if (r.f & 0x10u) return (AIDecide_PokeballResult){r.a, r.f};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORANF, NIDORINA);
		if (r2.f & 0x10u) return (AIDecide_PokeballResult){r2.a, r2.f};
		r2 = LookForCardIDInDeck_GivenCardIDInHand(NIDORINA, NIDOQUEEN);
		return (AIDecide_PokeballResult){r2.a, r2.f};
	}

	uint8_t f = (deck_id == 0u) ? 0x80u : 0u;
	return (AIDecide_PokeballResult){deck_id, f};
}
/* <<< factory AIDecide_Pokeball */

/* >>> factory AIDecide_MrFuji */
AIDecideParameterResult AIDecide_MrFuji(void)
{
	gb_write8(0xCE06u, 0xFFu);
	gb_write8(0xCE08u, 0xFFu);

	DuelistVarResult r1 = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t count = r1.a;
	if (count == 1u)
		return (AIDecideParameterResult){count, 0xC0u};

	uint8_t d = (uint8_t)(count - 1u);
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
		return (AIDecideParameterResult){chosen, 0xC0u};
	return (AIDecideParameterResult){chosen, 0x10u};
}
/* <<< factory AIDecide_MrFuji */

/* >>> factory AIDecide_PokemonTrader_BlisteringPokemon */
AIDecide_PokemonTrader_BlisteringPokemonResult AIDecide_PokemonTrader_BlisteringPokemon(void)
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
							return (AIDecide_PokemonTrader_BlisteringPokemonResult){a, 0x00u};
					}
				}
			}
		}
	}
	wce1a = a;
	FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
	if (dup.f & 0x10u)
		return (AIDecide_PokemonTrader_BlisteringPokemonResult){dup.a, 0x10u};
	return (AIDecide_PokemonTrader_BlisteringPokemonResult){dup.a, 0x00u};
}
/* <<< factory AIDecide_PokemonTrader_BlisteringPokemon */

/* >>> factory AIDecide_PokemonTrader_Flamethrower */
AIDecide_PokemonTrader_FlamethrowerResult AIDecide_PokemonTrader_Flamethrower(void)
{
	uint8_t a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r1 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARMELEON, CHARMANDER);
	a = r1.a;
	if (!(r1.f & 0x10u)) {
		LookForCardIDInDeck_GivenCardIDInHandResult r2 =
			LookForCardIDInDeck_GivenCardIDInHand(CHARMANDER, CHARMELEON);
		a = r2.a;
		if (!(r2.f & 0x10u)) {
			LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r3 =
				LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(CHARIZARD, CHARMELEON);
			a = r3.a;
			if (!(r3.f & 0x10u)) {
				LookForCardIDInDeck_GivenCardIDInHandResult r4 =
					LookForCardIDInDeck_GivenCardIDInHand(CHARMELEON, CHARIZARD);
				a = r4.a;
				if (!(r4.f & 0x10u)) {
					LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r5 =
						LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(NINETALES_LV32, VULPIX);
					a = r5.a;
					if (!(r5.f & 0x10u)) {
						LookForCardIDInDeck_GivenCardIDInHandResult r6 =
							LookForCardIDInDeck_GivenCardIDInHand(VULPIX, NINETALES_LV32);
						a = r6.a;
						if (!(r6.f & 0x10u)) {
							LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r7 =
								LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ARCANINE_LV45, GROWLITHE);
							a = r7.a;
							if (!(r7.f & 0x10u)) {
								LookForCardIDInDeck_GivenCardIDInHandResult r8 =
									LookForCardIDInDeck_GivenCardIDInHand(GROWLITHE, ARCANINE_LV45);
								a = r8.a;
								if (!(r8.f & 0x10u)) {
									LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r9 =
										LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(FLAREON_LV28, EEVEE);
									a = r9.a;
									if (!(r9.f & 0x10u)) {
										LookForCardIDInDeck_GivenCardIDInHandResult r10 =
											LookForCardIDInDeck_GivenCardIDInHand(EEVEE, FLAREON_LV28);
										a = r10.a;
										if (!(r10.f & 0x10u)) {
											return (AIDecide_PokemonTrader_FlamethrowerResult){a, 0x00u};
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
	if (dup.f & 0x10u)
		return (AIDecide_PokemonTrader_FlamethrowerResult){dup.a, 0x10u};
	return (AIDecide_PokemonTrader_FlamethrowerResult){dup.a, 0x00u};
}
/* <<< factory AIDecide_PokemonTrader_Flamethrower */

/* >>> factory AIDecide_PokemonTrader_FlowerGarden */
AIDecide_PokemonTrader_FlowerGardenResult AIDecide_PokemonTrader_FlowerGarden(void)
{
	uint8_t a;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r;
	LookForCardIDInDeck_GivenCardIDInHandResult r2;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(IVYSAUR, BULBASAUR);
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VENUSAUR_LV67, IVYSAUR);
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(BULBASAUR, IVYSAUR);
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(IVYSAUR, VENUSAUR_LV67);
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(WEEPINBELL, BELLSPROUT);
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VICTREEBEL, WEEPINBELL);
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(BELLSPROUT, WEEPINBELL);
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(WEEPINBELL, VICTREEBEL);
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(GLOOM, ODDISH);
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r = LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(VILEPLUME, GLOOM);
	a = r.a;
	if (r.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(ODDISH, GLOOM);
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	r2 = LookForCardIDInDeck_GivenCardIDInHand(GLOOM, VILEPLUME);
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	return (AIDecide_PokemonTrader_FlowerGardenResult){a, 0x00u};

find_duplicates:
	wce1a = a;
	{
		FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
		if (dup.f & 0x10u)
			return (AIDecide_PokemonTrader_FlowerGardenResult){dup.a, 0x10u};
		return (AIDecide_PokemonTrader_FlowerGardenResult){dup.a, 0x00u};
	}
}
/* <<< factory AIDecide_PokemonTrader_FlowerGarden */

/* >>> factory AIDecide_PokemonTrader_PowerGenerator */
AIDecide_PokemonTrader_PowerGeneratorResult AIDecide_PokemonTrader_PowerGenerator(void)
{
	uint8_t a = 0u;
	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r1 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RAICHU_LV40, PIKACHU_LV14);
	a = r1.a;
	if (r1.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r2 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(RAICHU_LV40, PIKACHU_LV12);
	a = r2.a;
	if (r2.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r3 =
		LookForCardIDInDeck_GivenCardIDInHand(PIKACHU_LV14, RAICHU_LV40);
	a = r3.a;
	if (r3.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r4 =
		LookForCardIDInDeck_GivenCardIDInHand(PIKACHU_LV12, RAICHU_LV40);
	a = r4.a;
	if (r4.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r5 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ELECTRODE_LV42, VOLTORB);
	a = r5.a;
	if (r5.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r6 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(ELECTRODE_LV35, VOLTORB);
	a = r6.a;
	if (r6.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r7 =
		LookForCardIDInDeck_GivenCardIDInHand(VOLTORB, ELECTRODE_LV42);
	a = r7.a;
	if (r7.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r8 =
		LookForCardIDInDeck_GivenCardIDInHand(VOLTORB, ELECTRODE_LV35);
	a = r8.a;
	if (r8.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r9 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV35, MAGNEMITE_LV13);
	a = r9.a;
	if (r9.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r10 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV35, MAGNEMITE_LV15);
	a = r10.a;
	if (r10.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r11 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV28, MAGNEMITE_LV13);
	a = r11.a;
	if (r11.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandAndPlayAreaResult r12 =
		LookForCardIDInDeck_GivenCardIDInHandAndPlayArea(MAGNETON_LV28, MAGNEMITE_LV15);
	a = r12.a;
	if (r12.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r13 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV15, MAGNETON_LV35);
	a = r13.a;
	if (r13.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r14 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV13, MAGNETON_LV35);
	a = r14.a;
	if (r14.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r15 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV15, MAGNETON_LV28);
	a = r15.a;
	if (r15.f & 0x10u) goto find_duplicates;

	LookForCardIDInDeck_GivenCardIDInHandResult r16 =
		LookForCardIDInDeck_GivenCardIDInHand(MAGNEMITE_LV13, MAGNETON_LV28);
	a = r16.a;
	if (r16.f & 0x10u) goto find_duplicates;

find_duplicates:
	wce1a = a;
	{
		FindDuplicatePokemonCardsResult dup = FindDuplicatePokemonCards();
		if (dup.f & 0x10u)
			return (AIDecide_PokemonTrader_PowerGeneratorResult){dup.a, 0x10u};
		return (AIDecide_PokemonTrader_PowerGeneratorResult){dup.a, 0x00u};
	}
}
/* <<< factory AIDecide_PokemonTrader_PowerGenerator */

/* >>> factory AIDecide_PokemonTrader */
AIDecide_PokemonTraderResult AIDecide_PokemonTrader(void)
{
	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == LEGENDARY_MOLTRES_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryMoltresResult r = AIDecide_PokemonTrader_LegendaryMoltres();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == LEGENDARY_ARTICUNO_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryArticunoResult r = AIDecide_PokemonTrader_LegendaryArticuno();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == LEGENDARY_DRAGONITE_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryDragoniteResult r = AIDecide_PokemonTrader_LegendaryDragonite();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == LEGENDARY_RONALD_DECK_ID) {
		AIDecide_PokemonTrader_LegendaryRonaldResult r = AIDecide_PokemonTrader_LegendaryRonald();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == BLISTERING_POKEMON_DECK_ID) {
		AIDecide_PokemonTrader_BlisteringPokemonResult r = AIDecide_PokemonTrader_BlisteringPokemon();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == SOUND_OF_THE_WAVES_DECK_ID) {
		AIDecide_PokemonTrader_SoundOfTheWavesResult r = AIDecide_PokemonTrader_SoundOfTheWaves();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == POWER_GENERATOR_DECK_ID) {
		AIDecide_PokemonTrader_PowerGeneratorResult r = AIDecide_PokemonTrader_PowerGenerator();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == FLOWER_GARDEN_DECK_ID) {
		AIDecide_PokemonTrader_FlowerGardenResult r = AIDecide_PokemonTrader_FlowerGarden();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == STRANGE_POWER_DECK_ID) {
		AIDecide_PokemonTrader_StrangePowerResult r = AIDecide_PokemonTrader_StrangePower();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	if (deck_id == FLAMETHROWER_DECK_ID) {
		AIDecide_PokemonTrader_FlamethrowerResult r = AIDecide_PokemonTrader_Flamethrower();
		return (AIDecide_PokemonTraderResult){r.a, r.f};
	}
	return (AIDecide_PokemonTraderResult){deck_id, (uint8_t)(deck_id == 0u ? 0x80u : 0x00u)};
}
/* <<< factory AIDecide_PokemonTrader */

/* >>> factory AIDecide_EnergySearch */
AIDecideEnergySearchResult AIDecide_EnergySearch(uint8_t a)
{
	CoreCardListResult hand = CreateEnergyCardListFromHand(a);
	uint8_t d;
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
				if (useful.f & 0x10u) {
					found = entry;
					found_flags = (uint8_t)(entry == 0u ? 0x90u : 0x10u);
					return (AIDecideEnergySearchResult){found, found_flags};
				}
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
		return (AIDecideEnergySearchResult){0u, 0x80u};

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
				return (AIDecideEnergySearchResult){found, (uint8_t)(found_flags | 0x10u)};
			}
		}

	next_play_area:
		e++;
		if (e == d)
			break;
	}

	return (AIDecideEnergySearchResult){wDuelTempList, 0x90u};
}
/* <<< factory AIDecide_EnergySearch */

/* >>> factory _AIProcessHandTrainerCards */
/* Adapters: every decide routine yields (a, f) -- a is the parameter stored
 * in wAITrainerCardParameter on carry -- and every play routine yields f.
 * Register arguments the C signatures still carry are the asm's incidental
 * inputs; the loop hands them the scratch values it has. */
typedef struct { uint8_t a; uint8_t f; } TrainerDecision;
static TrainerDecision decide_AIDecide_Bill(void) { AIDecideParameterResult r = AIDecide_Bill(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_ClefairyDollOrMysteriousFossil(void) { AIDecidePokemonFluteResult r = AIDecide_ClefairyDollOrMysteriousFossil(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_ComputerSearch(void) { AIDecide_ComputerSearchResult r = AIDecide_ComputerSearch(0u, 0u); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Defender_Phase13(void) { AIDecideParameterResult r = AIDecide_Defender_Phase13(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Defender_Phase14(void) { AIDecideParameterResult r = AIDecide_Defender_Phase14(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_EnergyRemoval(void) { AIDecideEnergyRemovalResult r = AIDecide_EnergyRemoval(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_EnergyRetrieval(void) { AIDecideEnergyRetrievalResult r = AIDecide_EnergyRetrieval(0u); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_EnergySearch(void) { AIDecideEnergySearchResult r = AIDecide_EnergySearch(0u); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_FullHeal(void) { AIDecideFullHealResult r = AIDecide_FullHeal(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Gambler(void) { AIDecideParameterResult r = AIDecide_Gambler(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_GustOfWind(void) { AIDecideParameterResult r = AIDecide_GustOfWind(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Imakuni(void) { AIDecideParameterResult r = AIDecide_Imakuni(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_ImposterProfessorOak(void) { AIDecideParameterResult r = AIDecide_ImposterProfessorOak(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_ItemFinder(void) { AIDecide_ItemFinderResult r = AIDecide_ItemFinder(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Lass(void) { AIDecideParameterResult r = AIDecide_Lass(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Maintenance(void) { AIDecideMaintenanceResult r = AIDecide_Maintenance(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_MrFuji(void) { AIDecideParameterResult r = AIDecide_MrFuji(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_PlusPower_Phase13(void) { AIDecide_PlusPower_Phase13Result r = AIDecide_PlusPower_Phase13(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_PlusPower_Phase14(void) { AIDecideParameterResult r = AIDecide_PlusPower_Phase14(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Pokeball(void) { AIDecide_PokeballResult r = AIDecide_Pokeball(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Pokedex(void) { AIDecidePokedexResult r = AIDecide_Pokedex(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_PokemonBreeder(void) { AIDecidePokemonBreederResult r = AIDecide_PokemonBreeder(0u); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_PokemonCenter(void) { AIDecideParameterResult r = AIDecide_PokemonCenter(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_PokemonFlute(void) { AIDecidePokemonFluteResult r = AIDecide_PokemonFlute(0u); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_PokemonTrader(void) { AIDecide_PokemonTraderResult r = AIDecide_PokemonTrader(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Potion_Phase07(void) { AIDecidePotionPhase07Result r = AIDecide_Potion_Phase07(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Potion_Phase10(void) { AIDecidePotionPhase10Result r = AIDecide_Potion_Phase10(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_ProfessorOak(void) { AIDecideParameterResult r = AIDecide_ProfessorOak(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Recycle(void) { AIDecideParameterResult r = AIDecide_Recycle(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Revive(void) { AIDecideReviveResult r = AIDecide_Revive(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_ScoopUp(void) { AIDecide_ScoopUpResult r = AIDecide_ScoopUp(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_SuperEnergyRemoval(void) { AIDecideParameterResult r = AIDecide_SuperEnergyRemoval(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_SuperEnergyRetrieval(void) { AIDecideSuperEnergyRetrievalResult r = AIDecide_SuperEnergyRetrieval(0u); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_SuperPotion_Phase08(void) { AIDecideSuperPotionPhase08Result r = AIDecide_SuperPotion_Phase08(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_SuperPotion_Phase11(void) { AIDecideSuperPotionPhase11Result r = AIDecide_SuperPotion_Phase11(); return (TrainerDecision){r.a, r.f}; }
static TrainerDecision decide_AIDecide_Switch(void) { AIDecide_SwitchResult r = AIDecide_Switch(); return (TrainerDecision){r.a, r.f}; }
static uint8_t play_AIPlay_Bill(void) { return AIPlay_Bill().f; }
static uint8_t play_AIPlay_ClefairyDollOrMysteriousFossil(void) { return AIPlay_ClefairyDollOrMysteriousFossil().f; }
static uint8_t play_AIPlay_ComputerSearch(void) { return AIPlay_ComputerSearch().f; }
static uint8_t play_AIPlay_Defender(void) { return AIPlay_Defender().f; }
static uint8_t play_AIPlay_EnergyRemoval(void) { return AIPlay_EnergyRemoval().f; }
static uint8_t play_AIPlay_EnergyRetrieval(void) { return AIPlay_EnergyRetrieval().f; }
static uint8_t play_AIPlay_EnergySearch(void) { return AIPlay_EnergySearch().f; }
static uint8_t play_AIPlay_FullHeal(void) { return AIPlay_FullHeal().f; }
static uint8_t play_AIPlay_Gambler(void) { return AIPlay_Gambler().f; }
static uint8_t play_AIPlay_GustOfWind(void) { return AIPlay_GustOfWind().f; }
static uint8_t play_AIPlay_Imakuni(void) { return AIPlay_Imakuni().f; }
static uint8_t play_AIPlay_ImposterProfessorOak(void) { return AIPlay_ImposterProfessorOak().f; }
static uint8_t play_AIPlay_ItemFinder(void) { return AIPlay_ItemFinder().f; }
static uint8_t play_AIPlay_Lass(void) { return AIPlay_Lass().f; }
static uint8_t play_AIPlay_Maintenance(void) { return AIPlay_Maintenance().f; }
static uint8_t play_AIPlay_MrFuji(void) { return AIPlay_MrFuji().f; }
static uint8_t play_AIPlay_PlusPower(void) { return AIPlay_PlusPower().f; }
static uint8_t play_AIPlay_Pokeball(void) { return AIPlay_Pokeball().f; }
static uint8_t play_AIPlay_Pokedex(void) { return AIPlay_Pokedex().f; }
static uint8_t play_AIPlay_PokemonBreeder(void) { return AIPlay_PokemonBreeder().f; }
static uint8_t play_AIPlay_PokemonCenter(void) { return AIPlay_PokemonCenter().f; }
static uint8_t play_AIPlay_PokemonFlute(void) { return AIPlay_PokemonFlute().f; }
static uint8_t play_AIPlay_PokemonTrader(void) { return AIPlay_PokemonTrader().f; }
static uint8_t play_AIPlay_Potion(void) { return AIPlay_Potion().f; }
static uint8_t play_AIPlay_ProfessorOak(void) { return AIPlay_ProfessorOak().f; }
static uint8_t play_AIPlay_Recycle(void) { return AIPlay_Recycle().f; }
static uint8_t play_AIPlay_Revive(void) { return AIPlay_Revive().f; }
static uint8_t play_AIPlay_ScoopUp(void) { return AIPlay_ScoopUp().f; }
static uint8_t play_AIPlay_SuperEnergyRemoval(void) { return AIPlay_SuperEnergyRemoval().f; }
static uint8_t play_AIPlay_SuperEnergyRetrieval(void) { return AIPlay_SuperEnergyRetrieval().f; }
static uint8_t play_AIPlay_SuperPotion(void) { return AIPlay_SuperPotion().f; }
static uint8_t play_AIPlay_Switch(void) { return AIPlay_Switch().f; }

typedef struct {
	uint8_t phase;
	uint8_t card;
	TrainerDecision (*decide)(void);
	uint8_t (*play)(void);
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

static void relist_hand(void)
{
	(void)CreateHandCardList(0u);
	uint16_t hl = wDuelTempList_ADDR;
	uint16_t de = wTempHandCardList_ADDR;
	(void)CopyListWithFFTerminatorFromHLToDE_Bank8(&hl, &de);
}

/* trainer_cards.asm:3-148. For every card in hand, every table row of the
 * requested phase naming that card is tried: the card must be playable
 * (Headache, its own initial effect, the AI's random abstention), its decide
 * routine must return carry, and the Play Trainer screen must not end the
 * turn. A hand modified by the card's effect is re-listed from the top. */
AIProcessHandTrainerCardsResult _AIProcessHandTrainerCards(uint8_t a)
{
	wAITrainerCardPhase = a;
	relist_hand();
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
			TrainerDecision decision = logic->decide();
			if ((decision.f & 0x10u) == 0u)
				continue;
			wAITrainerCardParameter = decision.a;
			hTempCardIndex_ff9f = wAITrainerCardToPlay;
			if ((AIMakeDecision(OPPACTION_PLAY_TRAINER, 0u, 0u, 0u, 0u).f & 0x10u) != 0u)
				continue;
			(void)logic->play();
			wPreviousAIFlags = (uint8_t)(wPreviousAIFlags | wCurrentAIFlags);
			if ((wPreviousAIFlags & AI_FLAG_MODIFIED_HAND) != 0u) {
				relist_hand();
				hand = wTempHandCardList_ADDR;
				wPreviousAIFlags = (uint8_t)(wPreviousAIFlags & (uint8_t)~AI_FLAG_MODIFIED_HAND);
			}
			break;
		}
	}
}
/* <<< factory _AIProcessHandTrainerCards */

/* >>> factory AIPlay_Pokeball */
AIPlayPokeballResult AIPlay_Pokeball(void)
{
	uint8_t card = wAITrainerCardToPlay;
	hTempCardIndex_ff9f = card;
	TossCoinRoutineResult toss = TossCoin(TrainerCardSuccessCheckText, 0u);
	hTemp_ffa0 = toss.a;
	if ((toss.f & 0x10u) != 0u)
		hTempPlayAreaLocation_ffa1 = wAITrainerCardParameter;
	else
		hTempPlayAreaLocation_ffa1 = 0xffu;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIPlayPokeballResult){decision.f};
}
/* <<< factory AIPlay_Pokeball */

/* >>> factory AIPlay_Recycle */
AIDecideResult AIPlay_Recycle(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	TossCoinRoutineResult toss = TossCoin(TrainerCardSuccessCheckText, 0u);
	if ((toss.f & 0x10u) != 0u)
		hTemp_ffa0 = wAITrainerCardParameter;
	else
		hTemp_ffa0 = 0xffu;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Recycle */

/* >>> factory AIPlay_Bill */
/* trainer_cards.asm:1420-1425 */
AIDecideResult AIPlay_Bill(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Bill */

/* >>> factory AIPlay_Defender */
/* trainer_cards.asm:594-601 */
AIDecideResult AIPlay_Defender(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = 0u; /* PLAY_AREA_ARENA: AI always attaches Defender to the Active */
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Defender */

/* >>> factory AIPlay_Imakuni */
/* trainer_cards.asm:4520-4525 */
AIDecideResult AIPlay_Imakuni(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Imakuni */

/* >>> factory AIPlay_FullHeal */
/* trainer_cards.asm:3771-3776 */
AIDecideResult AIPlay_FullHeal(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_FullHeal */

/* >>> factory AIPlay_ClefairyDollOrMysteriousFossil */
/* trainer_cards.asm:4776-4781 */
AIDecideResult AIPlay_ClefairyDollOrMysteriousFossil(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ClefairyDollOrMysteriousFossil */

/* >>> factory AIPlay_ImposterProfessorOak */
/* trainer_cards.asm:3182-3187 */
AIDecideResult AIPlay_ImposterProfessorOak(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ImposterProfessorOak */

/* >>> factory AIPlay_PokemonCenter */
/* trainer_cards.asm:3083-3088 */
AIDecideResult AIPlay_PokemonCenter(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_PokemonCenter */


/* >>> factory AIDecide_PlusPower_Phase14 */
AIDecideParameterResult AIDecide_PlusPower_Phase14(void)
{
	/* trainer_cards.asm AIDecide_PlusPower_Phase14: a usable attack that does
	 * not already knock out, a 30% roll, and no Mr. Mime wall past 30 damage. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	/* .CheckAttackDoesntKO */
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((unusable.f & 0x10u) != 0u)
		return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a)};
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - wDamage);
	if (hp <= wDamage)
		return (AIDecideParameterResult){left, or_a_flags(left)};
	/* .check_random */
	unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((unusable.f & 0x10u) != 0u)
		return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a)};
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	uint8_t minimum = wAIMinDamage;
	if (minimum < 10u)
		return (AIDecideParameterResult){minimum, or_a_flags(minimum)};
	uint8_t roll = Random(10u);
	if (roll >= 3u)
		return (AIDecideParameterResult){roll, or_a_flags(roll)};
	/* .MrMimeDamageCheck */
	uint8_t boosted = (uint8_t)(wDamage + 10u);
	if (boosted < 30u)
		return (AIDecideParameterResult){boosted, 0x10u};
	SwapTurn();
	uint8_t defender = (uint8_t)GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	SwapTurn();
	if (defender == MR_MIME)
		return (AIDecideParameterResult){defender, 0x00u};
	return (AIDecideParameterResult){defender, 0x10u};
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
static uint8_t gust_attack_deals_no_damage(void)
{
	(void)CopyAttackDataAndDamage_FromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a, wSelectedAttack);
	if (wLoadedAttackCategory == POKEMON_POWER)
		return 1u;
	if (wDamage == 0u)
		return 0u;
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	return wAIMaxDamage == 0u;
}

/* .CheckIfNoAttackDealsDamage */
static uint8_t gust_no_attack_deals_damage(void)
{
	wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
	if (!gust_attack_deals_no_damage())
		return 0u;
	wSelectedAttack = SECOND_ATTACK;
	return gust_attack_deals_no_damage();
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
static uint8_t gust_find_bench_card_with_weakness(uint8_t color, uint8_t *location_out, uint8_t *z_out)
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
		CheckIfCanDamageDefendingPokemonResult damage =
			CheckIfCanDamageDefendingPokemon(PLAY_AREA_ARENA, 0x80u, 0u, 0u, 0u, 0u, 0u);
		if (damage.f & 0x10u) {
			*location_out = location;
			*z_out = (uint8_t)(damage.f & 0x80u);
			return 1u;
		}
	}
}

AIDecideParameterResult AIDecide_GustOfWind(void)
{
	uint8_t bench_count = (uint8_t)(GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a - 1u);
	if (bench_count == 0u)
		return (AIDecideParameterResult){0u, 0x80u};
	uint8_t used = (uint8_t)(wPreviousAIFlags & AI_FLAG_USED_GUST_OF_WIND);
	if (used != 0u)
		return (AIDecideParameterResult){used, 0x20u};
	CanArenaCardUseNonResidualAttackResult attack =
		CanArenaCardUseNonResidualAttack(used, 0xA0u, 0u, 0u, 0u, 0u, 0u);
	if ((attack.f & 0x10u) == 0u)
		return (AIDecideParameterResult){attack.a, attack.f};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (CheckIfAnyAttackKnocksOutDefendingCard().f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a)};
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		if (energy.f & 0x10u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a)};
	}
	/* .check_id */
	uint8_t arena_id = (uint8_t)GetCardIDFromDeckIndex(GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a);
	if (arena_id == MEW_LV23 || arena_id == MEWTWO_LV53)
		return (AIDecideParameterResult){arena_id, 0x00u};
	uint8_t location;
	uint8_t z;
	if (gust_find_bench_card_to_knock_out(&location))
		return (AIDecideParameterResult){location, (uint8_t)(0x10u | non_turn_z())};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (!gust_no_attack_deals_damage()) {
		uint8_t color = TranslateColorToWR(GetArenaCardColor());
		SwapTurn();
		uint8_t weak = (uint8_t)(GetArenaCardWeakness() & color);
		SwapTurn();
		if (weak != 0u)
			return (AIDecideParameterResult){weak, 0x00u};
		if (gust_find_bench_card_with_weakness(color, &location, &z))
			return (AIDecideParameterResult){location, (uint8_t)(0x10u | z)};
		return (AIDecideParameterResult){0xFFu, 0x00u};
	}
	/* .check_bench_energy: the arena card cannot damage the defending card.
	 * The asm never loads b here: it is whatever the last damage estimate
	 * left, and every estimate that reaches its weakness/resistance tail
	 * leaves `ld b, CARD_LOCATION_ARENA` (ApplyAttachedDefender's input,
	 * damage_calculation.asm:166). That value doubles as a WATER weakness
	 * mask. A ROM bug, modeled as the register it is. */
	if (gust_find_bench_card_with_weakness(CARD_LOCATION_ARENA, &location, &z))
		return (AIDecideParameterResult){location, (uint8_t)(0x10u | z)};
	uint8_t count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (location = PLAY_AREA_BENCH_1; --count != 0u; location++) {
		SwapTurn();
		(void)GetPlayAreaCardAttachedEnergies(location);
		SwapTurn();
		if (wTotalAttachedEnergies != 0u)
			continue;
		if (gust_with_bench_card_in_arena(location, gust_can_damage_arena))
			return (AIDecideParameterResult){location, (uint8_t)(0x10u | non_turn_z())};
	}
	/* .check_bench_hp: the damageable bench card with the least HP left. */
	wce06 = 0xFFu;
	wce08 = 0u;
	count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	for (location = PLAY_AREA_BENCH_1; --count != 0u; location++) {
		uint8_t hp = GetNonTurnDuelistVariable((uint8_t)(location + DUELVARS_ARENA_CARD_HP)).a;
		if (wce06 < (uint8_t)(hp + 1u))
			continue;
		if (!gust_with_bench_card_in_arena(location, gust_can_damage_arena))
			continue;
		wce06 = hp;
		wce08 = location;
	}
	uint8_t found = wce08;
	if (found == 0u)
		return (AIDecideParameterResult){0u, 0x80u};
	return (AIDecideParameterResult){found, 0x10u};
}
/* <<< factory AIDecide_GustOfWind */

/* >>> factory AIDecide_Defender_Phase13 */
AIDecideParameterResult AIDecide_Defender_Phase13(void)
{
	/* trainer_cards.asm AIDecide_Defender_Phase13: play Defender when the
	 * player's strongest usable attack would knock the arena card out only
	 * without the 20 it prevents, and no knockout of the player's card is
	 * within reach this turn. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (CheckIfAnyAttackKnocksOutDefendingCard().f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a)};
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		if (energy.f & 0x10u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a)};
	}
	/* .cannot_ko */
	CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHPResult same =
		CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHP();
	if ((same.f & 0x10u) == 0u)
		return (AIDecideParameterResult){same.a, or_a_flags(same.a)};
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult selected =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	SwapTurn();
	if (selected.f & 0x10u)
		return (AIDecideParameterResult){selected.a, or_a_flags(selected.a)};
	(void)EstimateDamage_FromDefendingPokemon(wSelectedAttack);
	uint8_t selected_damage = wDamage;
	wce06 = selected_damage;
	wSelectedAttack = (uint8_t)(SECOND_ATTACK - wSelectedAttack);
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult other =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
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
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t left = (uint8_t)(hp - after_defender);
	if (hp <= after_defender)
		return (AIDecideParameterResult){left, or_a_flags(left)};
	return (AIDecideParameterResult){left, 0x10u};
}
/* <<< factory AIDecide_Defender_Phase13 */

/* >>> factory AIDecide_Switch */
AIDecide_SwitchResult AIDecide_Switch(void)
{
	uint8_t cost;
	uint8_t attached;
	if (wAIPlayEnergyCardForRetreat != 0u) {
		hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
		cost = GetPlayAreaCardRetreatCost();
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
	if (cost >= 3u)
		goto do_switch;
	attached = CountNumberOfEnergyCardsAttached(PLAY_AREA_ARENA).a;
	if (attached < cost)
		goto do_switch;
	return (AIDecide_SwitchResult){attached, (uint8_t)((attached == cost ? 0x80u : 0u) | 0x40u | ((attached & 0x0Fu) < (cost & 0x0Fu) ? 0x20u : 0u))};

do_switch:
	{
		AIDecideBenchPokemonToSwitchToResult r = AIDecideBenchPokemonToSwitchTo();
		return (AIDecide_SwitchResult){r.a, (uint8_t)((r.f & 0x80u) | ((r.f & 0x10u) ? 0u : 0x10u))};
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

AIDecideParameterResult AIDecide_SuperEnergyRemoval(void)
{
	/* A card of the AI's own with a basic energy to pay the cost. */
	uint8_t own = PLAY_AREA_BENCH_1;
	for (;; own++) {
		if (GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + own)).a == 0xFFu)
			return (AIDecideParameterResult){0xFFu, 0x00u};
		if (ser_has_basic_energy(own))
			break;
	}
	wce0f = own;
	/* Whether the arena card can knock the defending card out this turn:
	 * if it can, leave the player's arena card alone and look at the bench. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t start = PLAY_AREA_ARENA;
	if (CheckIfAnyAttackKnocksOutDefendingCard().f & 0x10u) {
		if ((CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u) == 0u
		    || (LookForEnergyNeededForAttackInHand().f & 0x10u) != 0u)
			start = PLAY_AREA_BENCH_1;
	}
	SwapTurn();
	uint8_t target = start;
	for (;; target++) {
		if (GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + target)).a == 0xFFu) {
			SwapTurn();
			return (AIDecideParameterResult){0xFFu, 0x00u};
		}
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
			if (GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + bench)).a == 0xFFu)
				break;
			if (ser_fewer_than_two_energy(bench) || ser_not_enough_energy_to_attack(bench))
				continue;
			ser_find_highest_damaging_attack(bench);
		}
		target = wce08;
		if (target == 0u) {
			SwapTurn();
			return (AIDecideParameterResult){0u, 0x80u};
		}
	}
	/* .pick_energy */
	wce1b = target;
	PickTwoResult picked = PickTwoAttachedEnergyCards(target);
	wce1c = picked.a;
	wce1d = picked.b;
	SwapTurn();
	uint8_t parameter = wce0f;
	wce1a = AIPickEnergyCardToDiscard(parameter);
	return (AIDecideParameterResult){parameter, (uint8_t)((picked.f & 0x80u) | 0x10u)};
}
/* <<< factory AIDecide_SuperEnergyRemoval */

/* >>> factory AIDecide_ScoopUp */
AIDecide_ScoopUpResult AIDecide_ScoopUp(void)
{
	hTempPlayAreaLocation_ff9d = 0u;
	DuelistVarResult count = GetTurnDuelistVariable(0xEFu);
	if (count.a < 2u)
		return (AIDecide_ScoopUpResult){count.a, count.a == 0u ? 0x80u : 0u};
	if (wOpponentDeckID == 0x0Eu || wOpponentDeckID == 0x1Bu)
		return (AIDecide_ScoopUpResult){0u, 0x80u};
	CheckIfAnyAttackKnocksOutDefendingCardResult any = CheckIfAnyAttackKnocksOutDefendingCard();
	if ((any.f & 0x10u) && !(CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u).f & 0x10u))
		return (AIDecide_ScoopUpResult){0u, 0x80u};
	uint8_t status = GetTurnDuelistVariable(0xF0u).a & 0x0Fu;
	if (status == 2u || status == 3u)
		return (AIDecide_ScoopUpResult){0u, 0x80u};
	uint8_t cost = GetPlayAreaCardRetreatCost();
	if (CountNumberOfEnergyCardsAttached(0u).a < cost)
		return (AIDecide_ScoopUpResult){0u, 0x80u};
	DuelistVarResult arena = GetTurnDuelistVariable(0xBBu);
	(void)LoadCardDataToBuffer1_FromDeckIndex(arena.a);
	uint8_t damage = ConvertHPToDamageCounters_Bank8(wLoadedCard1HP);
	CardDamageResult remaining = GetCardDamageAndMaxHP(0u);
	if (remaining.a == 0u || CalculateBDividedByA_Bank8(damage, remaining.a).a < 7u)
		return (AIDecide_ScoopUpResult){0u, 0x80u};
	AIDecideBenchPokemonToSwitchToResult choice = AIDecideBenchPokemonToSwitchTo();
	if (choice.f & 0x10u)
		return (AIDecide_ScoopUpResult){choice.a, choice.a == 0u ? 0x80u : 0u};
	wce1a = choice.a;
	return (AIDecide_ScoopUpResult){0u, 0x10u};
}
/* <<< factory AIDecide_ScoopUp */

/* >>> factory AIDecide_FullHeal */
AIDecideFullHealResult AIDecide_FullHeal(void)
{
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	status &= CNF_SLP_PRZ;
	if (status == 0u)
		return (AIDecideFullHealResult){0u, 0x80u};
	if (status == ASLEEP) {
		LookForCardIDInPlayAreaResult ghost = LookForCardIDInPlayArea_Bank8(GASTLY_LV8, PLAY_AREA_ARENA);
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, 0x10u};
		ghost = LookForCardIDInPlayArea_Bank8(GASTLY_LV17, PLAY_AREA_ARENA);
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, 0x10u};
		ghost = LookForCardIDInPlayArea_Bank8(HAUNTER_LV22, PLAY_AREA_ARENA);
		if (ghost.f & 0x10u)
			return (AIDecideFullHealResult){ghost.a, 0x10u};
	}
	if (status == PARALYZED || status == ASLEEP || status == CONFUSED) {
		LookForCardIDInHandListResult hand = LookForCardIDInHandList_Bank8(SCOOP_UP);
		if (hand.f & 0x10u) {
			AIDecide_ScoopUpResult scoop = AIDecide_ScoopUp();
			if (scoop.f & 0x10u)
				return (AIDecideFullHealResult){scoop.a, (uint8_t)(scoop.a == 0u ? 0x80u : 0u)};
		}
		CheckIfCanDamageDefendingPokemonResult damage =
			CheckIfCanDamageDefendingPokemon(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if (!(damage.f & 0x10u))
			return (AIDecideFullHealResult){damage.a, (uint8_t)(damage.a == 0u ? 0x80u : 0u)};
		if (wAIPlayEnergyCardForRetreat != 0u)
			return (AIDecideFullHealResult){wAIPlayEnergyCardForRetreat, 0x10u};
		if (status != CONFUSED) {
			AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat();
			if (!(retreat.f & 0x10u))
				return (AIDecideFullHealResult){retreat.a, 0x10u};
			return (AIDecideFullHealResult){retreat.a, (uint8_t)(retreat.a == 0u ? 0x80u : 0u)};
		}
	}
	return (AIDecideFullHealResult){status, 0x10u};
}
/* <<< factory AIDecide_FullHeal */

/* >>> factory AIDecide_EnergyRemoval */
AIDecideEnergyRemovalResult AIDecide_EnergyRemoval(void)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	uint8_t start = PLAY_AREA_ARENA;
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if (unusable.f & 0x10u) {
			LookForEnergyNeededForAttackInHandResult hand = LookForEnergyNeededForAttackInHand();
			if (hand.f & 0x10u)
				start = PLAY_AREA_BENCH_1;
		} else {
			start = PLAY_AREA_BENCH_1;
		}
	}
	wce0f = start;
	SwapTurn();
	for (uint8_t loc = start;; loc++) {
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + loc));
		if (card.a == 0xFFu)
			break;
		hTempPlayAreaLocation_ff9d = loc;
		(void)GetPlayAreaCardAttachedEnergies(loc);
		if (wTotalAttachedEnergies == 0u)
			continue;
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		CheckEnergyNeededForAttackResult first = CheckEnergyNeededForAttack();
		uint8_t enough = (uint8_t)((first.f & 0x10u) == 0u);
		if (!enough) {
			wSelectedAttack = SECOND_ATTACK;
			CheckEnergyNeededForAttackResult second = CheckEnergyNeededForAttack();
			if ((second.f & 0x10u) == 0u) {
				CheckIfNoSurplusEnergyResult surplus = CheckIfNoSurplusEnergyForAttack();
				enough = (uint8_t)((surplus.f & 0x10u) != 0u);
			}
		}
		if (enough) {
			wce1a = PickAttachedEnergyCardToRemove(loc);
			SwapTurn();
			return (AIDecideEnergyRemovalResult){loc, 0x10u};
		}
	}
	if (start == PLAY_AREA_ARENA) {
		hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
		(void)GetPlayAreaCardAttachedEnergies(PLAY_AREA_ARENA);
		if (wTotalAttachedEnergies != 0u) {
			wce1a = PickAttachedEnergyCardToRemove(PLAY_AREA_ARENA);
			SwapTurn();
			return (AIDecideEnergyRemovalResult){PLAY_AREA_ARENA, 0x10u};
		}
	}
	wce06 = 0u;
	wce08 = 0u;
	for (uint8_t loc = PLAY_AREA_BENCH_1;; loc++) {
		DuelistVarResult card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + loc));
		if (card.a == 0xFFu)
			break;
		hTempPlayAreaLocation_ff9d = loc;
		(void)GetPlayAreaCardAttachedEnergies(loc);
		if (wTotalAttachedEnergies == 0u)
			continue;
		DamageCalculationResult first_damage = EstimateDamage_VersusDefendingCard(FIRST_ATTACK_OR_PKMN_POWER);
		(void)first_damage;
		if (wDamage > wce06) {
			wce06 = wDamage;
			wce08 = loc;
		}
		DamageCalculationResult second_damage = EstimateDamage_VersusDefendingCard(SECOND_ATTACK);
		(void)second_damage;
		if (wDamage > wce06) {
			wce06 = wDamage;
			wce08 = loc;
		}
	}
	if (wce08 != 0u) {
		uint8_t loc = wce08;
		wce1a = PickAttachedEnergyCardToRemove(loc);
		SwapTurn();
		return (AIDecideEnergyRemovalResult){loc, 0x10u};
	}
	SwapTurn();
	return (AIDecideEnergyRemovalResult){0u, 0x80u};
}
/* <<< factory AIDecide_EnergyRemoval */

/* >>> factory AIDecide_PokemonCenter */
AIDecideParameterResult AIDecide_PokemonCenter(void)
{
	/* trainer_cards.asm AIDecide_PokemonCenter: not when a knockout is within
	 * reach this turn; otherwise when the damage to heal outweighs the energy
	 * lost and beats 60% of the total HP. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	if (CheckIfAnyAttackKnocksOutDefendingCard().f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if ((unusable.f & 0x10u) == 0u)
			return (AIDecideParameterResult){unusable.a, or_a_flags(unusable.a)};
		LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
		if (energy.f & 0x10u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a)};
	}

	wce06 = 0u;
	wce08 = 0u;
	wce0f = 0u;
	uint8_t d = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
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
			return (AIDecideParameterResult){(uint8_t)energy_sum, or_a_flags((uint8_t)energy_sum)};
		wce0f = (uint8_t)energy_sum;
		if (--d == 0u)
			break;
		++e;
	}

	uint8_t half_damage = (uint8_t)(wce08 >> 1);
	if (half_damage < wce0f)
		return (AIDecideParameterResult){half_damage, or_a_flags(half_damage)};
	uint16_t product = HtimesL((uint16_t)(0x0600u | wce06));
	uint8_t tens = (uint8_t)CalculateWordTensDigit(product);
	if (tens >= wce08)
		return (AIDecideParameterResult){tens, or_a_flags(tens)};
	return (AIDecideParameterResult){tens, 0x10u};
}
/* <<< factory AIDecide_PokemonCenter */

/* >>> factory AIDecide_PlusPower_Phase13 */
AIDecide_PlusPower_Phase13Result AIDecide_PlusPower_Phase13(void)
{
	/* The `xor a` / `ldh` pair is written twice in the source ("this is
	   mistakenly duplicated"); both stores are kept. */
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;

	CheckIfAnyAttackKnocksOutDefendingCardResult ko =
		CheckIfAnyAttackKnocksOutDefendingCard();
	if ((ko.f & 0x10u) != 0u) {
		CheckIfSelectedAttackIsUnusableResult ko_attack =
			CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		/* `jr nc, .no_carry`: a KO attack that is useable needs no PlusPower.
		   `or a` at .no_carry keeps a and sets Z from it, clearing N/H/C. */
		if ((ko_attack.f & 0x10u) == 0u)
			return (AIDecide_PlusPower_Phase13Result){ko_attack.a,
				(uint8_t)(ko_attack.a == 0u ? 0x80u : 0x00u)};
		LookForEnergyNeededForAttackInHandResult energy =
			LookForEnergyNeededForAttackInHand();
		if ((energy.f & 0x10u) != 0u)
			return (AIDecide_PlusPower_Phase13Result){energy.a,
				(uint8_t)(energy.a == 0u ? 0x80u : 0x00u)};
	}

	/* .cannot_ko: the active Pokemon's id goes to wTempTurnDuelistCardID. */
	DuelistVarResult attacker = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	wTempTurnDuelistCardID = (uint8_t)GetCardIDFromDeckIndex(attacker.a);

	SwapTurn();
	DuelistVarResult defender = GetTurnDuelistVariable(DUELVARS_ARENA_CARD);
	uint8_t defending_id = (uint8_t)GetCardIDFromDeckIndex(defender.a);
	wTempNonTurnDuelistCardID = defending_id;
	NoDamageOrEffectResult prevented =
		HandleNoDamageOrEffectSubstatus(defending_id, defender.hl);
	/* SwapTurn pushes af, so the substatus carry survives the swap back. */
	SwapTurn();
	if ((prevented.f & 0x10u) != 0u)
		/* .no_damage_or_effect is the only carry exit and does `ld a, e`
		   immediately before `scf`, so a mirrors the returned e. */
		return (AIDecide_PlusPower_Phase13Result){prevented.e,
			(uint8_t)(prevented.e == 0u ? 0x80u : 0x00u)};

	uint8_t attack = FIRST_ATTACK_OR_PKMN_POWER;
	for (;;) {
		wSelectedAttack = attack;

		/* .CheckAttackWithPluspower */
		uint8_t exit_a;
		uint8_t kos_with_pluspower = 0u;
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if ((unusable.f & 0x10u) != 0u) {
			exit_a = unusable.a; /* .unusable: or a; ret */
		} else {
			(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
			uint8_t hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
			uint8_t damage = wDamage;
			exit_a = (uint8_t)(hp - damage);
			/* `jr c` (damage exceeds the HP left) and `jr z` (the attack
			   already KOs) both return no carry with the difference in a. */
			if (hp >= damage && exit_a != 0u) {
				uint8_t boosted = (uint8_t)(damage + 10u);
				exit_a = (uint8_t)(hp - boosted);
				/* `ret c` (the boost overshoots the HP left) and `scf; ret`
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
				SwapTurn();
				/* `ret z`: no carry, a still holds e, and MR_MIME is non-zero
				   so the `or a` at .no_carry leaves Z clear. */
				if (defending == MR_MIME)
					return (AIDecide_PlusPower_Phase13Result){defending, 0x00u};
			}
			/* Both carry exits of the Mr. Mime check come back with Z clear,
			   so `xor a; scf` yields $90 and `ld a, SECOND_ATTACK; scf` $10. */
			if (attack == FIRST_ATTACK_OR_PKMN_POWER)
				return (AIDecide_PlusPower_Phase13Result){
					FIRST_ATTACK_OR_PKMN_POWER, 0x90u};
			return (AIDecide_PlusPower_Phase13Result){SECOND_ATTACK, 0x10u};
		}

		if (attack == SECOND_ATTACK)
			/* .no_carry: `or a` on whatever the second check left in a. */
			return (AIDecide_PlusPower_Phase13Result){exit_a,
				(uint8_t)(exit_a == 0u ? 0x80u : 0x00u)};
		attack = SECOND_ATTACK;
	}
}
/* <<< factory AIDecide_PlusPower_Phase13 */

/* >>> factory AIPlay_PlusPower */
AIDecideResult AIPlay_PlusPower(void)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_USED_PLUSPOWER);
	wAIPlusPowerAttack = wAITrainerCardParameter;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_PlusPower */

/* >>> factory AIPlay_Potion */
AIDecideResult AIPlay_Potion(void)
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
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Potion */

/* >>> factory AIPlay_GustOfWind */
AIDecideResult AIPlay_GustOfWind(void)
{
	uint8_t flags = wCurrentAIFlags;
	flags |= 0x10u;
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(0x07u, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_GustOfWind */

/* >>> factory AIPlay_Switch */
AIDecideResult AIPlay_Switch(void)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_USED_SWITCH);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	(void)AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	wAIRetreatScore = 0u;
	return (AIDecideResult){0x80u};
}
/* <<< factory AIPlay_Switch */

/* >>> factory AIPlay_Maintenance */
AIDecideResult AIPlay_Maintenance(void)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Maintenance */

/* >>> factory AIPlay_ComputerSearch */
AIDecideResult AIPlay_ComputerSearch(void)
{
	uint8_t flags = wCurrentAIFlags;
	flags = (uint8_t)(flags | AI_FLAG_MODIFIED_HAND);
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTempRetreatCostCards = wAITrainerCardParameter;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ComputerSearch */

/* >>> factory AIPlay_ItemFinder */
AIDecideResult AIPlay_ItemFinder(void)
{
	uint8_t flags = wCurrentAIFlags;
	flags |= AI_FLAG_MODIFIED_HAND;
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	hTempRetreatCostCards = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ItemFinder */

/* >>> factory AIPlay_Pokedex */
AIDecideResult AIPlay_Pokedex(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wce1a;
	hTempPlayAreaLocation_ffa1 = wce1b;
	hTempRetreatCostCards = wce1c;
	gb_write8(hTempRetreatCostCards_ADDR + 1u, wce1d);
	gb_write8(hTempRetreatCostCards_ADDR + 2u, wce1e);
	gb_write8(hTempRetreatCostCards_ADDR + 3u, 0xffu);
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Pokedex */

/* >>> factory AIPlay_Gambler */
AIDecideResult AIPlay_Gambler(void)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	if (wOpponentDeckID == IMAKUNI_DECK_ID) {
		hTempCardIndex_ff9f = wAITrainerCardToPlay;
		AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
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
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	gb_write8(wRNG1_ADDR, wce06);
	gb_write8(wRNG1_ADDR + 1u, wce08);
	gb_write8(wRNG1_ADDR + 2u, wce0f);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Gambler */

/* >>> factory AIPlay_EnergyRetrieval */
AIDecideResult AIPlay_EnergyRetrieval(void)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	hTempRetreatCostCards = wce1b;
	if (hTempRetreatCostCards != 0xffu)
		gb_write8(hTempRetreatCostCards_ADDR + 1u, 0xffu);
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_EnergyRetrieval */

/* >>> factory AIPlay_SuperEnergyRemoval */
AIDecideResult AIPlay_SuperEnergyRemoval(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	hTempRetreatCostCards = wce1b;
	gb_write8(hTempRetreatCostCards_ADDR + 1u, wce1c);
	gb_write8(hTempRetreatCostCards_ADDR + 2u, wce1d);
	gb_write8(hTempRetreatCostCards_ADDR + 3u, 0xffu);
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_SuperEnergyRemoval */

/* >>> factory AIDecide_SuperPotion_Phase11 */
AIDecideSuperPotionPhase11Result AIDecide_SuperPotion_Phase11(void)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	uint8_t e = PLAY_AREA_ARENA;
	if ((ko.f & 0x10u) != 0u) {
		uint8_t d = ko.a;
		uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
		uint8_t damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
		if (damage >= 41u) damage = 40u;
		uint8_t remaining = (uint8_t)(hp + damage - d);
		if (remaining != 0u && (uint8_t)(hp + damage) >= d) return (AIDecideSuperPotionPhase11Result){0u, 0u};
		uint8_t prizes;
		SwapTurn(); prizes = CountPrizes(); SwapTurn();
		e = ((uint8_t)(prizes - 1u) == 0u) ? PLAY_AREA_ARENA : PLAY_AREA_BENCH_1;
	}
	for (;;) {
		uint8_t card = GetTurnDuelistVariable((uint8_t)(DUELVARS_ARENA_CARD + e)).a;
		if (card == 0xffu) return (AIDecideSuperPotionPhase11Result){0xffu, 0xC0u};
		EnergiesResult energies = GetPlayAreaCardAttachedEnergies(e);
		if (wTotalAttachedEnergies == 0u || (energies.f & 0x10u) == 0u) { e++; continue; }
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, e, 0u, 0u);
		AttackFlagResult flag = CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F);
		if ((unusable.f & 0x10u) == 0u && (flag.f & 0x10u) != 0u) { e++; continue; }
		wSelectedAttack = SECOND_ATTACK;
		unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, e, 0u, 0u);
		flag = CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F);
		if ((unusable.f & 0x10u) == 0u && (flag.f & 0x10u) != 0u) { e++; continue; }
		hTempPlayAreaLocation_ff9d = e;
		CheckEnergyNeededForAttackResult need = CheckEnergyNeededForAttack();
		if ((need.f & 0x10u) == 0u) { CheckEnergyNeededForAttackAfterDiscardResult after = CheckEnergyNeededForAttackAfterDiscard(); if ((after.f & 0x10u) != 0u) { e++; continue; } }
		CardDamageResult card_damage = GetCardDamageAndMaxHP(e);
		if (card_damage.a < 40u) { e++; continue; }
		if (e != PLAY_AREA_ARENA) { uint8_t prizes; SwapTurn(); prizes = CountPrizes(); SwapTurn(); if ((uint8_t)(prizes - 1u) != 0u && Random(10u) < 3u) return (AIDecideSuperPotionPhase11Result){0u, 0u}; }
		if (e == PLAY_AREA_ARENA) { AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil(); if ((recoil.f & 0x10u) != 0u) return (AIDecideSuperPotionPhase11Result){0u, 0u}; }
		return (AIDecideSuperPotionPhase11Result){e, 0x10u};
	}
}
/* <<< factory AIDecide_SuperPotion_Phase11 */

/* >>> factory AIPlay_EnergySearch */
/* trainer_cards.asm:3218-3233 */
AIDecideResult AIPlay_EnergySearch(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_EnergySearch */

/* >>> factory AIPlay_ScoopUp */
AIDecideResult AIPlay_ScoopUp(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ScoopUp */

/* >>> factory AIPlay_PokemonBreeder */
AIDecideResult AIPlay_PokemonBreeder(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTempPlayAreaLocation_ffa1 = wAITrainerCardParameter;
	hTemp_ffa0 = wce1a;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_PokemonBreeder */

/* >>> factory AIPlay_PokemonFlute */
AIDecideResult AIPlay_PokemonFlute(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
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

AIDecideParameterResult AIDecide_ProfessorOak(void)
{
	/* trainer_cards.asm AIDecide_ProfessorOak: a score in wce06 against 60. */
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	if (remaining >= DECK_SIZE - 6u)
		return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 6u)};

	uint8_t deck_id = wOpponentDeckID;
	if (deck_id == LEGENDARY_ARTICUNO_DECK_ID) {
		/* .HandleLegendaryArticunoDeck */
		uint8_t count = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
		if (count < 3u) {
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
				return (AIDecideParameterResult){count, 0x90u};
		}
		/* .check_playable_cards */
		CountOppEnergyResult energy = CountOppEnergyCardsInHand(0u, 0u);
		if (energy.a >= 4u)
			return (AIDecideParameterResult){energy.a, or_a_flags(energy.a)};
		(void)CreateHandCardList(0u);
		uint16_t list = wDuelTempList_ADDR;
		(void)RemoveCardIDInList(&list, PROFESSOR_OAK);
		(void)RemoveCardIDInList(&list, PROFESSOR_OAK);
		for (;;) {
			uint8_t index = gb_read8(list++);
			if (index == 0xFFu)
				return (AIDecideParameterResult){0xFFu, 0x90u};
			CheckIfCardCanBePlayedResult playable = CheckIfCardCanBePlayed(index);
			if ((playable.f & 0x10u) == 0u)
				return (AIDecideParameterResult){playable.a, or_a_flags(playable.a)};
		}
	}

	if (deck_id == EXCAVATION_DECK_ID) {
		/* .HandleExcavationDeck */
		if (remaining >= 46u)
			return (AIDecideParameterResult){remaining, cp_flags(remaining, 46u)};
		LookForCardIDInHandAndPlayAreaResult fossil = LookForCardIDInHandAndPlayArea(MYSTERIOUS_FOSSIL);
		wce06 = (fossil.f & 0x10u) ? 0x1Eu : 0x50u;
	} else {
		if (deck_id == WONDERS_OF_SCIENCE_DECK_ID) {
			/* .HandleWondersOfScienceDeck */
			LookForCardIDInHandListResult found = LookForCardIDInHandList_Bank8(GRIMER);
			if ((found.f & 0x10u) == 0u)
				found = LookForCardIDInHandList_Bank8(MUK);
			if (found.f & 0x10u)
				return (AIDecideParameterResult){found.a, or_a_flags(found.a)};
		}
		/* .general_logic */
		if (remaining >= DECK_SIZE - 14u)
			return (AIDecideParameterResult){remaining, cp_flags(remaining, DECK_SIZE - 14u)};
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
		return (AIDecideParameterResult){score, (uint8_t)((score == 60u ? 0x80u : 0u) | 0x10u)};
	return (AIDecideParameterResult){score, or_a_flags(score)};
}
/* <<< factory AIDecide_ProfessorOak */

/* >>> factory AIPlay_ProfessorOak */
AIDecideResult AIPlay_ProfessorOak(void)
{
	uint8_t flags = wCurrentAIFlags;
	flags = (uint8_t)(flags | AI_FLAG_USED_PROFESSOR_OAK | AI_FLAG_MODIFIED_HAND);
	wCurrentAIFlags = flags;
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_ProfessorOak */

/* >>> factory AIPlay_PokemonTrader */
AIMakeDecisionResult AIPlay_PokemonTrader(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	return AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
}
/* <<< factory AIPlay_PokemonTrader */

/* >>> factory AIPlay_EnergyRemoval */
AIDecideResult AIPlay_EnergyRemoval(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = wce1a;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_EnergyRemoval */

/* >>> factory AIDecide_Potion_Phase10 */
AIDecidePotionPhase10Result AIDecide_Potion_Phase10(void)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	uint8_t e;
	uint8_t prizes;
	if ((ko.f & 0x10u) != 0u) {
		uint8_t d = ko.a;
		uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
		uint8_t damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
		if (damage > 20u) damage = 20u;
		uint8_t total = (uint8_t)(hp + damage);
		uint8_t remaining = (uint8_t)(total - d);
		if (total >= d && remaining != 0u)
			return (AIDecidePotionPhase10Result){remaining, 0u};
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
			return (AIDecidePotionPhase10Result){0xffu, 0xc0u};
		wSelectedAttack = FIRST_ATTACK_OR_PKMN_POWER;
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, e, 0u, 0u);
		if ((unusable.f & 0x10u) == 0u && (CheckLoadedAttackFlag(ATTACK_FLAG3_ADDRESS | BOOST_IF_TAKEN_DAMAGE_F).f & 0x10u) != 0u) {
			e++;
			continue;
		}
		wSelectedAttack = SECOND_ATTACK;
		unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, e, 0u, 0u);
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
					return (AIDecidePotionPhase10Result){chance, (uint8_t)(chance == 0u ? 0x80u : 0u)};
			}
		}
		if (e == PLAY_AREA_ARENA) {
			AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
			if ((recoil.f & 0x10u) != 0u)
				return (AIDecidePotionPhase10Result){e, 0x80u};
		}
		return (AIDecidePotionPhase10Result){e, 0x10u};
	}
}
/* <<< factory AIDecide_Potion_Phase10 */

/* >>> factory AIPlay_SuperPotion */
AIDecideResult AIPlay_SuperPotion(void)
{
	uint8_t card = wAITrainerCardToPlay;
	hTempCardIndex_ff9f = card;
	uint8_t parameter = wAITrainerCardParameter;
	hTempPlayAreaLocation_ffa1 = parameter;
	uint8_t discarded = AIPickEnergyCardToDiscard(parameter);
	hTemp_ffa0 = discarded;
	CardDamageResult damage = GetCardDamageAndMaxHP(parameter);
	uint8_t retreatCost = damage.a;
	if (retreatCost >= 40u)
		retreatCost = 40u;
	hTempRetreatCostCards = retreatCost;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_SuperPotion */

/* >>> factory AIDecide_Potion_Phase07 */
AIDecidePotionPhase07Result AIDecide_Potion_Phase07(void)
{
	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat();
	if ((retreat.f & 0x10u) != 0u)
		return (AIDecidePotionPhase07Result){retreat.a, (uint8_t)(retreat.a == 0u ? 0x80u : 0u)};
	AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
	if ((recoil.f & 0x10u) != 0u)
		return (AIDecidePotionPhase07Result){0u, 0x80u};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((ko.f & 0x10u) == 0u)
		return (AIDecidePotionPhase07Result){ko.a, (uint8_t)(ko.a == 0u ? 0x80u : 0u)};
	uint8_t d = ko.a;
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t damage = GetCardDamageAndMaxHP(PLAY_AREA_ARENA).a;
	uint8_t heal = damage < 21u ? damage : 20u;
	uint8_t total = (uint8_t)(hp + heal);
	uint8_t remaining = (uint8_t)(total - d);
	if (total < d)
		return (AIDecidePotionPhase07Result){remaining, 0u};
	if (remaining == 0u)
		return (AIDecidePotionPhase07Result){remaining, 0x80u};
	return (AIDecidePotionPhase07Result){0u, 0x10u};
}
/* <<< factory AIDecide_Potion_Phase07 */

/* >>> factory AIPlay_Revive */
AIDecideResult AIPlay_Revive(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Revive */

/* >>> factory AIPlay_Lass */
AIDecideResult AIPlay_Lass(void)
{
	wCurrentAIFlags = (uint8_t)(wCurrentAIFlags | AI_FLAG_MODIFIED_HAND);
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_Lass */

/* >>> factory AIPlay_MrFuji */
/* trainer_cards.asm:3870-3878 */
AIDecideResult AIPlay_MrFuji(void)
{
	hTempCardIndex_ff9f = wAITrainerCardToPlay;
	hTemp_ffa0 = wAITrainerCardParameter;
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_MrFuji */

/* >>> factory AIDecide_SuperPotion_Phase08 */
AIDecideSuperPotionPhase08Result AIDecide_SuperPotion_Phase08(void)
{
	AIDecideWhetherToRetreatResult retreat = AIDecideWhetherToRetreat();
	if ((retreat.f & 0x10u) != 0u)
		return (AIDecideSuperPotionPhase08Result){retreat.a, (uint8_t)(retreat.a == 0u ? 0x80u : 0u)};
	AICheckIfAttackIsHighRecoilResult recoil = AICheckIfAttackIsHighRecoil();
	if ((recoil.f & 0x10u) != 0u)
		return (AIDecideSuperPotionPhase08Result){retreat.a, (uint8_t)(retreat.a == 0u ? 0x80u : 0u)};
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	uint8_t e = PLAY_AREA_ARENA;
	EnergiesResult energies = GetPlayAreaCardAttachedEnergies(e);
	if (wTotalAttachedEnergies == 0u)
		return (AIDecideSuperPotionPhase08Result){0u, 0x80u};
	CheckIfDefendingPokemonCanKnockOutResult ko = CheckIfDefendingPokemonCanKnockOut(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((ko.f & 0x10u) == 0u)
		return (AIDecideSuperPotionPhase08Result){ko.a, (uint8_t)(ko.a == 0u ? 0x80u : 0u)};
	uint8_t d = ko.a;
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	uint8_t damage = GetCardDamageAndMaxHP(e).a;
	if (damage >= 41u)
		damage = 40u;
	uint8_t total = (uint8_t)(hp + damage);
	uint8_t remaining = (uint8_t)(total - d);
	if (total < d || remaining == 0u)
		return (AIDecideSuperPotionPhase08Result){remaining, (uint8_t)(remaining == 0u ? 0x80u : 0u)};
	return (AIDecideSuperPotionPhase08Result){e, 0x10u};
}
/* <<< factory AIDecide_SuperPotion_Phase08 */

/* >>> factory AIPlay_SuperEnergyRetrieval */
AIDecideResult AIPlay_SuperEnergyRetrieval(void)
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
	AIMakeDecisionResult decision = AIMakeDecision(OPPACTION_EXECUTE_TRAINER_EFFECTS, 0u, 0u, 0u, 0u);
	return (AIDecideResult){decision.f};
}
/* <<< factory AIPlay_SuperEnergyRetrieval */
