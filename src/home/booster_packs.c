#include "home/booster_packs.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "mem.h"
/* >>> factory statics */
#include "generated/wram.h"
#include "mem.h"

#define NUM_CARD_TYPES              0x11u
#define NUM_BOOSTER_CARD_TYPES      0x09u
#define BOOSTER_CARD_TYPE_GRASS     0x00u
#define BOOSTER_CARD_TYPE_FIRE      0x01u
#define BOOSTER_CARD_TYPE_WATER     0x02u
#define BOOSTER_CARD_TYPE_LIGHTNING 0x03u
#define BOOSTER_CARD_TYPE_FIGHTING  0x04u
#define BOOSTER_CARD_TYPE_PSYCHIC   0x05u
#define BOOSTER_CARD_TYPE_COLORLESS 0x06u
#define BOOSTER_CARD_TYPE_TRAINER   0x07u
#define BOOSTER_CARD_TYPE_ENERGY    0x08u

/* booster_packs.asm:166-184 (CardTypeTable) */
static const uint8_t CardTypeTable[NUM_CARD_TYPES] = {
	BOOSTER_CARD_TYPE_FIRE,
	BOOSTER_CARD_TYPE_GRASS,
	BOOSTER_CARD_TYPE_LIGHTNING,
	BOOSTER_CARD_TYPE_WATER,
	BOOSTER_CARD_TYPE_FIGHTING,
	BOOSTER_CARD_TYPE_PSYCHIC,
	BOOSTER_CARD_TYPE_COLORLESS,
	BOOSTER_CARD_TYPE_TRAINER,
	BOOSTER_CARD_TYPE_ENERGY,
	BOOSTER_CARD_TYPE_ENERGY,
	BOOSTER_CARD_TYPE_ENERGY,
	BOOSTER_CARD_TYPE_ENERGY,
	BOOSTER_CARD_TYPE_ENERGY,
	BOOSTER_CARD_TYPE_ENERGY,
	BOOSTER_CARD_TYPE_ENERGY,
	BOOSTER_CARD_TYPE_TRAINER,
	BOOSTER_CARD_TYPE_TRAINER,
};

#include "generated/wram.h"

#include "home/booster_packs.h"
#include "generated/wram.h"
#include "mem.h"

#include "generated/wram.h"
#include "home/booster_packs.h"

#include "home/booster_packs.h"
#include "mem.h"

#define NUM_CARDS_IN_BOOSTER 0x0Au

#include "home/booster_packs.h"
#include "home/random.h"

#define NUM_COLORED_TYPES 0x06u

#include "home/booster_packs.h"

#include "home/booster_packs.h"

#include "generated/wram.h"

#define BOOSTER_DATA_BASE 0x64E4u

#include "home/booster_packs.h"
#include "generated/wram.h"

#include "home/booster_packs.h"
#include "home/card_collection.h"
#include "generated/wram.h"

#include "home/random.h"
#include "generated/wram.h"

#include "home/card_data.h"
#include "generated/wram.h"
/* <<< factory statics */

/* >>> factory GetCurrentRarityAmount */
/* booster_packs.asm:57-65 */
RarityAmount GetCurrentRarityAmount(void)
{
	uint8_t a = wBoosterCurrentRarity;
	return (RarityAmount){a, (uint16_t)(wBoosterData_CommonAmount_ADDR + a)};
}
/* <<< factory GetCurrentRarityAmount */

/* >>> factory GetBoosterCardType */
/* booster_packs.asm:152-164 */
uint8_t GetBoosterCardType(uint8_t a)
{
	if (a >= NUM_CARD_TYPES)
		return CardTypeTable[0];
	return CardTypeTable[a];
}
/* <<< factory GetBoosterCardType */

/* >>> factory CalculateTypeChances */
/* booster_packs.asm:190-217 */
uint8_t CalculateTypeChances(void)
{
	for (uint8_t i = 0; i < NUM_BOOSTER_CARD_TYPES; i++)
		gb_write8((uint16_t)(wBoosterTempTypeChancesTable_ADDR + i), 0u);
	wTempBoosterChances = 0u;
	for (uint8_t c = 0; c < NUM_BOOSTER_CARD_TYPES; c++) {
		uint8_t amount = gb_read8((uint16_t)(wBoosterAmountOfCardTypeTable_ADDR + c));
		if (amount == 0u)
			continue;
		uint8_t chance = gb_read8((uint16_t)(wBoosterData_TypeChances_ADDR + c));
		if (chance == 0u)
			continue;
		gb_write8((uint16_t)(wBoosterTempTypeChancesTable_ADDR + c), chance);
		wTempBoosterChances = (uint8_t)(wTempBoosterChances + chance);
	}
	return wTempBoosterChances;
}
/* <<< factory CalculateTypeChances */

/* >>> factory UpdateBoosterCardTypesChanceByte */
/* booster_packs.asm:293-311 */
uint8_t UpdateBoosterCardTypesChanceByte(void)
{
	uint16_t hl = (uint16_t)(wBoosterData_TypeChances_ADDR + wBoosterJustDrawnCardType);
	uint8_t c = wBoosterAveragedTypeChances;
	uint8_t v = gb_read8(hl);
	uint8_t res = (uint8_t)(v - c);
	gb_write8(hl, res);
	if (res == 0u || v < c) {
		res = 1u;
		gb_write8(hl, res);
	}
	return res;
}
/* <<< factory UpdateBoosterCardTypesChanceByte */

/* >>> factory AppendCurrentCardToHL */
void AppendCurrentCardToHL(uint16_t *hl)
{
	uint16_t cursor = *hl;
	while (gb_read8(cursor++) != 0u) {
	}
	cursor--;
	gb_write8(cursor++, wBoosterCurrentCard);
	gb_write8(cursor, 0u);
	*hl = cursor;
}
/* <<< factory AppendCurrentCardToHL */

/* >>> factory AddBoosterCardToTempCardCollection */
void AddBoosterCardToTempCardCollection(void)
{
	uint8_t card = gb_read8(wBoosterCurrentCard_ADDR);
	uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + card);
	gb_write8(slot, (uint8_t)(gb_read8(slot) + 1u));
}
/* <<< factory AddBoosterCardToTempCardCollection */

/* >>> factory AddBoosterCardToDrawnEnergies */
AddBoosterCardToDrawnEnergiesResult AddBoosterCardToDrawnEnergies(void)
{
	uint8_t card = wBoosterCurrentCard;
	uint16_t hl = wBoosterTempEnergiesDrawn_ADDR;
	AppendCurrentCardToHL(&hl);
	uint16_t address = (uint16_t)(wTempCardCollection_ADDR + card);
	uint8_t old = gb_read8(address);
	AddBoosterCardToTempCardCollection();
	uint8_t value = (uint8_t)(old + 1u);
	uint8_t flags = (uint8_t)((value == 0u ? 0x80u : 0u)
		| ((old & 0x0Fu) == 0x0Fu ? 0x20u : 0u));
	return (AddBoosterCardToDrawnEnergiesResult){card, flags};
}
/* <<< factory AddBoosterCardToDrawnEnergies */

/* >>> factory AddBoosterEnergyToDrawnEnergies */
AddBoosterEnergyToDrawnEnergiesResult AddBoosterEnergyToDrawnEnergies(uint8_t a)
{
	wBoosterCurrentCard = a;
	AddBoosterCardToDrawnEnergiesResult result = AddBoosterCardToDrawnEnergies();
	return (AddBoosterEnergyToDrawnEnergiesResult){result.a, result.f};
}
/* <<< factory AddBoosterEnergyToDrawnEnergies */

/* >>> factory ZeroBoosterRarityData */
void ZeroBoosterRarityData(void)
{
	wBoosterData_CommonAmount = 0u;
	wBoosterData_UncommonAmount = 0u;
	wBoosterData_RareAmount = 0u;
}
/* <<< factory ZeroBoosterRarityData */

/* >>> factory GenerateTwoTypesEnergyBooster */
GenerateTwoTypesEnergyBoosterResult GenerateTwoTypesEnergyBooster(uint16_t hl)
{
	for (uint8_t b = 0; b < 2u; b++) {
		uint8_t card = gb_read8(hl);
		for (uint8_t c = 0; c < NUM_CARDS_IN_BOOSTER / 2u; c++)
			(void)AddBoosterEnergyToDrawnEnergies(card);
		hl = (uint16_t)(hl + 1u);
	}
	ZeroBoosterRarityData();
	return (GenerateTwoTypesEnergyBoosterResult){0u, 0x80u, 0u, 0u, hl};
}
/* <<< factory GenerateTwoTypesEnergyBooster */

/* >>> factory GenerateRandomEnergy */
/* booster_packs.asm:342-350 */
AddBoosterEnergyToDrawnEnergiesResult GenerateRandomEnergy(void)
{
	uint8_t random = Random(NUM_COLORED_TYPES);
	return AddBoosterEnergyToDrawnEnergies((uint8_t)(random + 1u));
}
/* <<< factory GenerateRandomEnergy */

/* >>> factory GenerateEnergyBoosterGrassPsychic */
GenerateTwoTypesEnergyBoosterResult GenerateEnergyBoosterGrassPsychic(void)
{
	return GenerateTwoTypesEnergyBooster(0x63CDu);
}
/* <<< factory GenerateEnergyBoosterGrassPsychic */

/* >>> factory GenerateEnergyBoosterLightningFire */
GenerateTwoTypesEnergyBoosterResult GenerateEnergyBoosterLightningFire(void)
{
	return GenerateTwoTypesEnergyBooster(0x63C9u);
}
/* <<< factory GenerateEnergyBoosterLightningFire */

/* >>> factory GenerateEnergyBoosterWaterFighting */
GenerateTwoTypesEnergyBoosterResult GenerateEnergyBoosterWaterFighting(void)
{
	return GenerateTwoTypesEnergyBooster(0x63CBu);
}
/* <<< factory GenerateEnergyBoosterWaterFighting */

/* >>> factory GenerateRandomEnergyBooster */
void GenerateRandomEnergyBooster(void)
{
	uint8_t count = NUM_CARDS_IN_BOOSTER;
	while (count != 0u) {
		(void)GenerateRandomEnergy();
		--count;
	}
	ZeroBoosterRarityData();
}
/* <<< factory GenerateRandomEnergyBooster */

/* >>> factory PutEnergiesAndNonEnergiesTogether */
PutEnergiesAndNonEnergiesTogetherResult PutEnergiesAndNonEnergiesTogether(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint8_t *energy = wBoosterTempEnergiesDrawn_PTR;
	while ((a = *energy++) != 0u) {
		wBoosterCurrentCard = a;
		uint16_t cursor = 0xC400u;
		AppendCurrentCardToHL(&cursor);
	}
	a = 0u;
	f = 0x80u;
	return (PutEnergiesAndNonEnergiesTogetherResult){a, f, b, c, d, e, hl};
}
/* <<< factory PutEnergiesAndNonEnergiesTogether */

/* >>> factory LoadRarityAmountsToWram */
void LoadRarityAmountsToWram(void)
{
	uint8_t set = gb_read8(wBoosterData_Set_ADDR);
	uint8_t common = (set < 2u) ? 5u : 6u;
	uint8_t uncommon = 3u;
	uint8_t rare = 1u;
	gb_write8(wBoosterData_CommonAmount_ADDR, common);
	gb_write8(wBoosterData_UncommonAmount_ADDR, uncommon);
	gb_write8(wBoosterData_RareAmount_ADDR, rare);
}
/* <<< factory LoadRarityAmountsToWram */

/* >>> factory DetermineBoosterCardType */
uint8_t DetermineBoosterCardType(uint8_t a)
{
	wTempBoosterChances = a;
	uint8_t c = 0;
	uint8_t *table = wBoosterTempTypeChancesTable_PTR;
	for (;;) {
		uint8_t chance = *table;
		if (chance != 0u) {
			uint8_t remaining = wTempBoosterChances;
			uint8_t next = (uint8_t)(remaining - chance);
			wTempBoosterChances = next;
			if (remaining < chance)
				break;
		}
		++table;
		++c;
		if (c >= NUM_BOOSTER_CARD_TYPES)
			break;
	}
	wBoosterJustDrawnCardType = c;
	return c;
}
/* <<< factory DetermineBoosterCardType */

/* >>> factory FindBoosterDataPointer */
uint16_t FindBoosterDataPointer(void)
{
	uint8_t pack = gb_read8(wBoosterPackID_ADDR);
	return (uint16_t)(BOOSTER_DATA_BASE + (uint16_t)pack * 0x0Cu);
}
/* <<< factory FindBoosterDataPointer */

/* >>> factory AddBoosterCardToDrawnNonEnergies */
void AddBoosterCardToDrawnNonEnergies(void)
{
	uint16_t cursor = wBoosterTempNonEnergiesDrawn_ADDR;
	AppendCurrentCardToHL(&cursor);
	AddBoosterCardToTempCardCollection();
}
/* <<< factory AddBoosterCardToDrawnNonEnergies */

/* >>> factory AddBoosterCardsToCollection */
void AddBoosterCardsToCollection(void)
{
	uint16_t p = wBoosterCardsDrawn_ADDR;
	uint8_t card;
	while ((card = gb_read8(p++)) != 0u)
		AddCardToCollection(card);
}
/* <<< factory AddBoosterCardsToCollection */

/* >>> factory GenerateBoosterEnergies */
void GenerateBoosterEnergies(void)
{
	uint16_t ptr_addr = wBoosterData_EnergyFunctionPointer_ADDR;
	uint8_t hi = gb_read8((uint16_t)(ptr_addr + 1u));
	if (hi != 0u) {
		uint8_t lo = gb_read8(ptr_addr);
		uint16_t target = (uint16_t)(lo | ((uint16_t)hi << 8));
		if (target == 0x6390u) { GenerateRandomEnergyBooster(); return; }
		if (target == 0x639Cu) { GenerateEnergyBoosterLightningFire(); return; }
		if (target == 0x63A1u) { GenerateEnergyBoosterWaterFighting(); return; }
		if (target == 0x63A6u) { GenerateEnergyBoosterGrassPsychic(); return; }
		return;
	}
	uint8_t a = gb_read8(ptr_addr);
	if (a == 0u)
		return;
	(void)AddBoosterEnergyToDrawnEnergies(a);
}
/* <<< factory GenerateBoosterEnergies */

/* >>> factory DetermineBoosterCard */
DetermineBoosterCardResult DetermineBoosterCard(uint8_t d, uint8_t e)
{
	uint8_t type = wBoosterJustDrawnCardType;
	uint8_t b = 0u;
	uint8_t c = type;
	uint16_t hl = (uint16_t)(wBoosterAmountOfCardTypeTable_ADDR + type);
	uint8_t amount = gb_read8(hl);
	uint8_t chances = Random(amount);
	wTempBoosterChances = chances;
	hl = wBoosterViableCardList_ADDR;
	for (;;) {
		uint8_t card_id = gb_read8(hl);
		hl = (uint16_t)(hl + 1u);
		if (card_id == 0u)
			return (DetermineBoosterCardResult){0u, 0x90u, b, c, d, e, hl};
		wBoosterCurrentCard = card_id;
		uint8_t entry_type = gb_read8(hl);
		if (entry_type == type) {
			chances = wTempBoosterChances;
			if (chances == 0u)
				return (DetermineBoosterCardResult){0u, 0x80u, b, c, d, e, hl};
			chances = (uint8_t)(chances - 1u);
			wTempBoosterChances = chances;
		}
		hl = (uint16_t)(hl + 1u);
	}
}
/* <<< factory DetermineBoosterCard */

/* >>> factory CheckCardInSetAndRarity */
CheckCardInSetAndRarityResult CheckCardInSetAndRarity(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	CardTRS r = GetCardTypeRarityAndSet(e);
	wBoosterCurrentCardType = r.type;
	wBoosterCurrentCardRarity = r.rarity;
	wBoosterCurrentCardSet = r.set;

	uint8_t rarity = wBoosterCurrentCardRarity;
	uint8_t cur_rarity = wBoosterCurrentRarity;
	uint8_t a;
	if (cur_rarity != rarity) {
		a = cur_rarity;
		return (CheckCardInSetAndRarityResult){a, 0x10u, b, c, d, e, hl};
	}

	uint8_t card_type = wBoosterCurrentCardType;
	a = GetBoosterCardType(card_type);
	if (a != BOOSTER_CARD_TYPE_ENERGY) {
		uint8_t set_hi = (uint8_t)((wBoosterCurrentCardSet >> 4) & 0x0Fu);
		uint8_t data_set = wBoosterData_Set;
		if (data_set != set_hi) {
			a = data_set;
			return (CheckCardInSetAndRarityResult){a, 0x10u, b, c, d, e, hl};
		}
		a = data_set;
	}
	return (CheckCardInSetAndRarityResult){a, 0x00u, b, c, d, e, hl};
}
/* <<< factory CheckCardInSetAndRarity */

/* >>> factory CheckCardAlreadyDrawn */
CheckCardAlreadyDrawnResult CheckCardAlreadyDrawn(void)
{
	uint8_t index = gb_read8(wBoosterCurrentCard_ADDR);
	uint8_t value = gb_read8((uint16_t)(wTempCardCollection_ADDR + index));
	uint8_t f = 0x00u;
	if (value == 1u)
		f |= 0x80u;
	if (value != 0u)
		f |= 0x10u;
	return (CheckCardAlreadyDrawnResult){value, f};
}
/* <<< factory CheckCardAlreadyDrawn */
