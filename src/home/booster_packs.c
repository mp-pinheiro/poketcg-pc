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
