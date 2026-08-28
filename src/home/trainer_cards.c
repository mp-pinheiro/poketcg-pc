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
#define HEATED_BATTLE_DECK_ID 0x15u

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
#define IMAKUNI_DECK_ID 0x2Au

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
/* <<< factory statics */


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
AIDecideResult AIDecide_Recycle(void)
{
	CardListResult discard = CreateDiscardPileCardList(0);
	if (discard.f & 0x10u)
		return (AIDecideResult){0x80u};
	uint8_t priority[5] = {0xFFu, 0xFFu, 0xFFu, 0xFFu, 0xFFu};
	uint16_t list = wDuelTempList_ADDR;
	uint8_t ghost = wOpponentDeckID == 0x0Du;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			break;
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (!ghost) {
			if (card_id == 0x07u) priority[0] = deck_index;
			else if (card_id == 0xB8u) priority[1] = deck_index;
			else if (card_id == 0xBAu) priority[2] = deck_index;
			else if (card_id == 0xADu) priority[3] = deck_index;
		} else {
			if (card_id == 0x95u) priority[0] = deck_index;
			else if (card_id == 0x94u) priority[1] = deck_index;
			else if (card_id == 0x1Au) priority[2] = deck_index;
			else if (card_id == 0xBBu) priority[3] = deck_index;
			else if (card_id == 0xB2u) priority[4] = deck_index;
		}
	}
	for (uint8_t i = 0; i < 5u; i++)
		if (priority[i] != 0xFFu)
			return (AIDecideResult){0x10u};
	return (AIDecideResult){0x00u};
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
AIDecideResult AIDecide_Lass(void)
{
	uint8_t hand_count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (hand_count < 7u)
		return (AIDecideResult){hand_count == 0u ? 0x80u : 0x00u};
	(void)CreateHandCardList(hand_count);
	uint16_t list = wDuelTempList_ADDR;
	for (;;) {
		uint8_t deck_index = gb_read8(list++);
		if (deck_index == 0xFFu)
			return (AIDecideResult){0x90u};
		uint8_t card_id = LoadCardDataToBuffer1_FromDeckIndex(deck_index);
		if (card_id == 0xC7u)
			continue;
		if (gb_read8(wLoadedCard1Type_ADDR) == 0x08u)
			return (AIDecideResult){0x00u};
	}
}
/* <<< factory AIDecide_Lass */

/* >>> factory AIDecide_Imakuni */
AIDecideResult AIDecide_Imakuni(void)
{
	uint8_t status = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_STATUS).a;
	if ((status & 0x0Fu) == 0x01u)
		return (AIDecideResult){0x00u};
	return (AIDecideResult){0x10u};
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
AIDecidePokemonFluteResult AIDecide_ClefairyDollOrMysteriousFossil(void)
{
	uint8_t count = GetTurnDuelistVariable(0xEFu).a;
	if (count >= 6u)
		return (AIDecidePokemonFluteResult){count, 0};
	uint8_t arena = GetTurnDuelistVariable(0xBBu).a;
	if ((uint8_t)GetCardIDFromDeckIndex(arena) == 0xB0u)
		return (AIDecidePokemonFluteResult){arena, 0x10u};
	return (AIDecidePokemonFluteResult){count, count < 4u ? 0x10u : 0};
}
/* <<< factory AIDecide_ClefairyDollOrMysteriousFossil */

/* >>> factory AIDecide_Defender_Phase14 */
AIDecideResult AIDecide_Defender_Phase14(void)
{
	uint8_t flag = CheckLoadedAttackFlag(0x06u).f;
	if (!(flag & 0x10u))
		flag = CheckLoadedAttackFlag(0x04u).f;
	if (!(flag & 0x10u))
		return (AIDecideResult){0x80u};
	uint8_t arena = GetTurnDuelistVariable(0xBBu).a;
	(void)LoadCardDataToBuffer2_FromDeckIndex(arena);
	uint8_t damage = wSelectedAttack == 0u ? wLoadedCard2Atk1EffectParam :
		wLoadedCard2Atk2EffectParam;
	uint8_t color = TranslateColorToWR(GetArenaCardColor());
	if (GetArenaCardWeakness() & color)
		damage = (uint8_t)(damage << 1);
	if (GetArenaCardResistance() & color) {
		if (damage < 30u)
			return (AIDecideResult){0};
		damage = (uint8_t)(damage - 30u);
	}
	if (damage == 0u)
		return (AIDecideResult){0};
	damage = (uint8_t)(damage - 20u);
	uint8_t hp = GetTurnDuelistVariable(0x08u).a;
	return (AIDecideResult){(uint8_t)(((damage != 0u) && (hp > damage)) ? 0x10u : 0)};
}
/* <<< factory AIDecide_Defender_Phase14 */

/* >>> factory AIDecide_Bill */
AIDecideResult AIDecide_Bill(void)
{
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	uint8_t f = 0x40u;
	if ((remaining & 0x0Fu) < 3u)
		f |= 0x20u;
	if (remaining < 51u)
		f |= 0x10u;
	if (remaining == 51u)
		f |= 0x80u;
	return (AIDecideResult){f};
}
/* <<< factory AIDecide_Bill */

/* >>> factory AIDecide_Gambler */
AIDecideResult AIDecide_Gambler(void)
{
	if (wOpponentDeckID == 0x34u) {
		if (Random(10u) < 2u)
			return (AIDecideResult){0x10u};
		return (AIDecideResult){0x80u};
	}
	if (!(wAIBarrierFlagCounter & 0x80u))
		return (AIDecideResult){0x80u};
	uint8_t remaining = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	return (AIDecideResult){(uint8_t)(remaining >= 56u ? 0x90u : 0x80u)};
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
AIDecideResult AIDecide_ImposterProfessorOak(void)
{
	uint8_t remaining = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_NOT_IN_DECK).a;
	uint8_t hand = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_CARDS_IN_HAND).a;
	if (remaining < (60u - 14u)) {
		if (hand < 9u)
			return (AIDecideResult){(uint8_t)(hand == 0u ? 0x80u : 0x00u)};
		return (AIDecideResult){(uint8_t)(hand == 9u ? 0x90u : 0x10u)};
	}
	if (hand < 6u)
		return (AIDecideResult){0x10u};
	return (AIDecideResult){0x00u};
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
AIDecideResult AIDecide_MrFuji(void)
{
	gb_write8(0xCE06u, 0xFFu);
	gb_write8(0xCE08u, 0xFFu);

	DuelistVarResult r1 = GetTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA);
	uint8_t count = r1.a;
	if (count == 1u)
		return (AIDecideResult){0xC0u};

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

	if (gb_read8(0xCE06u) == 0xFFu)
		return (AIDecideResult){0xC0u};
	return (AIDecideResult){0x10u};
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
AIProcessHandTrainerCardsResult _AIProcessHandTrainerCards(uint8_t a)
{
	wAITrainerCardPhase = a;
	(void)CreateHandCardList(0u);
	uint16_t hl = wDuelTempList_ADDR;
	uint16_t de = wTempHandCardList_ADDR;
	(void)CopyListWithFFTerminatorFromHLToDE_Bank8(&hl, &de);
	return (AIProcessHandTrainerCardsResult){0xffu, 0xc0u};
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
AIDecideResult AIDecide_PlusPower_Phase14(void)
{
	hTempPlayAreaLocation_ff9d = PLAY_AREA_ARENA;
	CheckIfSelectedAttackIsUnusableResult unusable =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((unusable.f & 0x10u) != 0u)
		return (AIDecideResult){0u};

	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	DuelistVarResult hp = GetNonTurnDuelistVariable(DUELVARS_ARENA_CARD_HP);
	uint8_t remaining = (uint8_t)(hp.a - wDamage);
	if (remaining == 0u || hp.a < wDamage)
		return (AIDecideResult){0u};

	CheckIfSelectedAttackIsUnusableResult random_unusable =
		CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	if ((random_unusable.f & 0x10u) != 0u)
		return (AIDecideResult){0u};
	(void)EstimateDamage_VersusDefendingCard(wSelectedAttack);
	if (wAIMinDamage < 10u)
		return (AIDecideResult){0u};
	if (Random(10u) >= 3u)
		return (AIDecideResult){0u};
	if ((uint8_t)(wDamage + 10u) < 30u)
		return (AIDecideResult){0u};
	SwapTurn();
	uint8_t arena_index = GetTurnDuelistVariable(DUELVARS_ARENA_CARD).a;
	uint16_t card_id = GetCardIDFromDeckIndex(arena_index);
	SwapTurn();
	if ((uint8_t)card_id == MR_MIME)
		return (AIDecideResult){0u};
	return (AIDecideResult){0x10u};
}
/* <<< factory AIDecide_PlusPower_Phase14 */

/* >>> factory AIDecide_GustOfWind */
AIDecideResult AIDecide_GustOfWind(void)
{
	uint8_t bench_count = GetNonTurnDuelistVariable(DUELVARS_NUMBER_OF_POKEMON_IN_PLAY_AREA).a;
	if (bench_count == 1u)
		return (AIDecideResult){0x80u};
	if (bench_count == 0u)
		return (AIDecideResult){0x00u};
	if ((wPreviousAIFlags & AI_FLAG_USED_GUST_OF_WIND) != 0u)
		return (AIDecideResult){0x20u};
	return (AIDecideResult){0x10u};
}
/* <<< factory AIDecide_GustOfWind */

/* >>> factory AIDecide_Defender_Phase13 */
AIDecideResult AIDecide_Defender_Phase13(void)
{
	hTempPlayAreaLocation_ff9d = 0u;
	CheckIfAnyAttackKnocksOutDefendingCardResult ko = CheckIfAnyAttackKnocksOutDefendingCard();
	if (ko.f & 0x10u) {
		CheckIfSelectedAttackIsUnusableResult unusable = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if (unusable.f & 0x10u) {
			LookForEnergyNeededForAttackInHandResult energy = LookForEnergyNeededForAttackInHand();
			if (energy.f & 0x10u)
				return (AIDecideResult){0u, 0x80u};
		}
	}
	CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHPResult same = CheckIfAnyDefendingPokemonAttackDealsSameDamageAsHP();
	if (!(same.f & 0x10u))
		return (AIDecideResult){0u, 0x80u};
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult selected = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	SwapTurn();
	if (selected.f & 0x10u)
		return (AIDecideResult){0u, 0x80u};
	uint8_t selected_attack = wSelectedAttack;
	(void)EstimateDamage_FromDefendingPokemon(selected_attack);
	wce06 = wDamage;
	uint8_t selected_damage = wDamage;
	wSelectedAttack = (uint8_t)(SECOND_ATTACK - selected_attack);
	SwapTurn();
	CheckIfSelectedAttackIsUnusableResult other = CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
	SwapTurn();
	if (other.f & 0x10u) {
		wSelectedAttack = (uint8_t)(SECOND_ATTACK - wSelectedAttack);
		wDamage = wce06;
	} else {
		uint8_t other_attack = wSelectedAttack;
		(void)EstimateDamage_FromDefendingPokemon(other_attack);
		if (wDamage < selected_damage) {
			wSelectedAttack = (uint8_t)(SECOND_ATTACK - wSelectedAttack);
			wDamage = wce06;
		}
	}
	uint8_t damage_after_defender = (uint8_t)(wDamage - 20u);
	uint8_t hp = GetTurnDuelistVariable(DUELVARS_ARENA_CARD_HP).a;
	if (hp > damage_after_defender)
		return (AIDecideResult){0u, 0x10u};
	return (AIDecideResult){0u, 0x80u};
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
AIDecideResult AIDecide_SuperEnergyRemoval(void)
{
	return (AIDecideResult){0x00u};
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
AIDecideResult AIDecide_PokemonCenter(void)
{
	hTempPlayAreaLocation_ff9d = 0u;

	CheckIfAnyAttackKnocksOutDefendingCardResult knockout =
		CheckIfAnyAttackKnocksOutDefendingCard();
	if ((knockout.f & 0x10u) != 0u) {
		CheckIfSelectedAttackIsUnusableResult unusable =
			CheckIfSelectedAttackIsUnusable(0u, 0u, 0u, 0u, 0u, 0u, 0u);
		if ((unusable.f & 0x10u) != 0u) {
			LookForEnergyNeededForAttackInHandResult energy =
				LookForEnergyNeededForAttackInHand();
			if ((energy.f & 0x10u) != 0u)
				return (AIDecideResult){0u};
		}
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
			return (AIDecideResult){0u};
		wce0f = (uint8_t)energy_sum;
		if (--d == 0u)
			break;
		++e;
	}

	uint8_t half_damage = (uint8_t)(wce08 >> 1);
	if (half_damage < wce0f)
		return (AIDecideResult){0u};
	uint16_t product = HtimesL((uint16_t)(0x0600u | wce06));
	product = CalculateWordTensDigit(product);
	if ((uint8_t)product >= wce08)
		return (AIDecideResult){0u};
	return (AIDecideResult){0x10u};
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
