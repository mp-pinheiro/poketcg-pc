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
