/* >>> part includes_2 */
#include "home/card_id_bus.h"
#include "generated/wram.h"
#include "mem.h"
/* <<< part includes_2 */
/* >>> factory AppendCurrentCardToHL */
void AppendCurrentCardToHL(uint16_t *hl)
{
	uint16_t cursor = *hl;
	for (;;) {
		CardId card = card_id_read(&cursor);
		if (card == 0u)
			break;
	}
	cursor = (uint16_t)(cursor - 2u);
	card_id_write(&cursor, card_id_read_at(wBoosterCurrentCard_ADDR));
	card_id_write(&cursor, 0u);
	*hl = (uint16_t)(cursor - 1u);
}
/* <<< factory AppendCurrentCardToHL */
/* >>> factory AddBoosterCardToTempCardCollection */
AddBoosterCardToTempCardCollectionResult AddBoosterCardToTempCardCollection(void)
{
	CardId card = card_id_read_at(wBoosterCurrentCard_ADDR);
	uint32_t sum = (uint32_t)wTempCardCollection_ADDR + card;
	uint16_t slot = (uint16_t)sum;
	uint8_t old = gb_read8(slot);
	uint8_t value = (uint8_t)(old + 1u);
	gb_write8(slot, value);
	uint8_t flags = (uint8_t)(value == 0u ? 0x80u : 0u);
	if ((old & 0x0Fu) == 0x0Fu)
		flags = (uint8_t)(flags | 0x20u);
	if (sum > 0xFFFFu)
		flags = (uint8_t)(flags | 0x10u);
	return (AddBoosterCardToTempCardCollectionResult){(uint8_t)(slot >> 8), flags};
}
/* <<< factory AddBoosterCardToTempCardCollection */
/* >>> factory AddBoosterCardToDrawnEnergies */
AddBoosterCardToDrawnEnergiesResult AddBoosterCardToDrawnEnergies(void)
{
	uint16_t hl = wBoosterTempEnergiesDrawn_ADDR;
	AppendCurrentCardToHL(&hl);
	AddBoosterCardToTempCardCollectionResult result =
		AddBoosterCardToTempCardCollection();
	return (AddBoosterCardToDrawnEnergiesResult){result.a, result.f};
}
/* <<< factory AddBoosterCardToDrawnEnergies */
/* >>> factory AddBoosterEnergyToDrawnEnergies */
AddBoosterEnergyToDrawnEnergiesResult AddBoosterEnergyToDrawnEnergies(CardId a)
{
	uint16_t current = wBoosterCurrentCard_ADDR;
	card_id_write(&current, a);
	AddBoosterCardToDrawnEnergiesResult result =
		AddBoosterCardToDrawnEnergies();
	return (AddBoosterEnergyToDrawnEnergiesResult){
		result.a, result.f, (uint8_t)(a >> 8), (uint8_t)a};
}
/* <<< factory AddBoosterEnergyToDrawnEnergies */
/* >>> factory GenerateTwoTypesEnergyBooster */
GenerateTwoTypesEnergyBoosterResult GenerateTwoTypesEnergyBooster(uint16_t hl)
{
	CardId last = 0u;
	for (uint8_t b = 0; b < 2u; b++) {
		CardId card = card_id_read_at(hl);
		last = card;
		for (uint8_t c = 0; c < NUM_CARDS_IN_BOOSTER / 2u; c++)
			(void)AddBoosterEnergyToDrawnEnergies(card);
		hl = (uint16_t)(hl + 2u);
	}
	ZeroBoosterRarityData();
	return (GenerateTwoTypesEnergyBoosterResult){
		0u, 0x80u, 0u, 0u, (uint8_t)(last >> 8), (uint8_t)last, hl};
}
/* <<< factory GenerateTwoTypesEnergyBooster */
/* >>> factory GenerateRandomEnergy */
/* booster_packs.asm:342-350 */
AddBoosterEnergyToDrawnEnergiesResult GenerateRandomEnergy(void)
{
	uint8_t random = Random(NUM_COLORED_TYPES);
	return AddBoosterEnergyToDrawnEnergies((CardId)(random + 1u));
}
/* <<< factory GenerateRandomEnergy */
/* === factory GenerateEnergyBoosterWaterFighting */
/* >>> factory GenerateFightingEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateFightingEnergy(void)
{
	return AddBoosterEnergyToDrawnEnergies(FIGHTING_ENERGY);
}
/* <<< factory GenerateFightingEnergy */
/* >>> factory GenerateFireEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateFireEnergy(void)
{
	return AddBoosterEnergyToDrawnEnergies(FIRE_ENERGY);
}
/* <<< factory GenerateFireEnergy */
/* >>> factory GenerateGrassEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateGrassEnergy(void)
{
	return AddBoosterEnergyToDrawnEnergies(GRASS_ENERGY);
}
/* <<< factory GenerateGrassEnergy */
/* >>> factory GenerateLightningEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateLightningEnergy(void)
{
	return AddBoosterEnergyToDrawnEnergies(LIGHTNING_ENERGY);
}
/* <<< factory GenerateLightningEnergy */
/* >>> factory GeneratePsychicEnergy */
AddBoosterEnergyToDrawnEnergiesResult GeneratePsychicEnergy(void)
{
	return AddBoosterEnergyToDrawnEnergies(PSYCHIC_ENERGY);
}
/* <<< factory GeneratePsychicEnergy */
/* >>> factory GenerateWaterEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateWaterEnergy(void)
{
	return AddBoosterEnergyToDrawnEnergies(WATER_ENERGY);
}
/* <<< factory GenerateWaterEnergy */
/* >>> factory GenerateRandomEnergyBooster */
AddBoosterEnergyToDrawnEnergiesResult GenerateRandomEnergyBooster(void)
{
	AddBoosterEnergyToDrawnEnergiesResult last = {0u, 0u, 0u, 0u};
	uint8_t count = NUM_CARDS_IN_BOOSTER;
	while (count != 0u) {
		last = GenerateRandomEnergy();
		--count;
	}
	ZeroBoosterRarityData();
	return (AddBoosterEnergyToDrawnEnergiesResult){0u, 0x80u, last.d, last.e};
}
/* <<< factory GenerateRandomEnergyBooster */
/* >>> factory PutEnergiesAndNonEnergiesTogether */
PutEnergiesAndNonEnergiesTogetherResult PutEnergiesAndNonEnergiesTogether(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t energy = wBoosterTempEnergiesDrawn_ADDR;
	for (;;) {
		CardId card = card_id_read(&energy);
		if (card == 0u)
			break;
		uint16_t cursor = wBoosterCardsDrawn_ADDR;
		uint16_t current = wBoosterCurrentCard_ADDR;
		card_id_write(&current, card);
		AppendCurrentCardToHL(&cursor);
	}
	return (PutEnergiesAndNonEnergiesTogetherResult){0u, 0x80u, b, c, d, e, hl};
}
/* <<< factory PutEnergiesAndNonEnergiesTogether */
/* >>> factory AddBoosterCardsToCollection */
void AddBoosterCardsToCollection(void)
{
	uint16_t p = wBoosterCardsDrawn_ADDR;
	for (;;) {
		CardId card = card_id_read(&p);
		if (card == 0u)
			break;
		AddCardToCollection(card);
	}
}
/* <<< factory AddBoosterCardsToCollection */
/* >>> factory GenerateBoosterEnergies */
void GenerateBoosterEnergies(void)
{
	uint16_t ptr_addr = wBoosterData_EnergyFunctionPointer_ADDR;
	uint8_t hi = gb_read8((uint16_t)(ptr_addr + 1u));
	if (hi == 0u)
		return;
	uint8_t lo = gb_read8(ptr_addr);
	uint16_t target = (uint16_t)(lo | ((uint16_t)hi << 8));
	if (target == GenerateGrassEnergy_ADDR) {
		(void)GenerateGrassEnergy();
		return;
	}
	if (target == GenerateFireEnergy_ADDR) {
		(void)GenerateFireEnergy();
		return;
	}
	if (target == GenerateWaterEnergy_ADDR) {
		(void)GenerateWaterEnergy();
		return;
	}
	if (target == GenerateLightningEnergy_ADDR) {
		(void)GenerateLightningEnergy();
		return;
	}
	if (target == GenerateFightingEnergy_ADDR) {
		(void)GenerateFightingEnergy();
		return;
	}
	if (target == GeneratePsychicEnergy_ADDR) {
		(void)GeneratePsychicEnergy();
		return;
	}
	if (target == GenerateRandomEnergy_ADDR) {
		(void)GenerateRandomEnergy();
		return;
	}
	if (target == GenerateRandomEnergyBooster_ADDR) {
		GenerateRandomEnergyBooster();
		return;
	}
	if (target == GenerateEnergyBoosterLightningFire_ADDR) {
		(void)GenerateEnergyBoosterLightningFire();
		return;
	}
	if (target == GenerateEnergyBoosterWaterFighting_ADDR) {
		(void)GenerateEnergyBoosterWaterFighting();
		return;
	}
	if (target == GenerateEnergyBoosterGrassPsychic_ADDR)
		(void)GenerateEnergyBoosterGrassPsychic();
}
/* <<< factory GenerateBoosterEnergies */
/* >>> factory DetermineBoosterCard */
DetermineBoosterCardResult DetermineBoosterCard(uint8_t d, uint8_t e)
{
	uint8_t type = wBoosterJustDrawnCardType;
	uint8_t b = 0u;
	uint8_t c = type;
	uint16_t amount_addr = (uint16_t)(wBoosterAmountOfCardTypeTable_ADDR + type);
	uint8_t chances = Random(gb_read8(amount_addr));
	wTempBoosterChances = chances;
	uint16_t hl = wBoosterViableCardList_ADDR;
	for (;;) {
		uint8_t low = gb_read8(hl++);
		uint8_t high = gb_read8(hl);
		if ((uint8_t)(low | high) == 0u)
			return (DetermineBoosterCardResult){0u, 0x90u, b, c, d, e, hl};
		hl = (uint16_t)(hl - 1u);
		CardId card_id = (CardId)(gb_read8(hl)
			| ((uint16_t)gb_read8((uint16_t)(hl + 1u)) << 8));
		hl = (uint16_t)(hl + 2u);
		uint16_t current = wBoosterCurrentCard_ADDR;
		card_id_write(&current, card_id);
		uint8_t entry_type = gb_read8(hl);
		if (entry_type == type) {
			chances = wTempBoosterChances;
			if (chances == 0u)
				return (DetermineBoosterCardResult){0u, 0x80u, b, c, d, e, hl};
			wTempBoosterChances = (uint8_t)(chances - 1u);
		}
		hl = (uint16_t)(hl + 1u);
	}
}
/* <<< factory DetermineBoosterCard */
/* >>> factory CheckCardInSetAndRarity */
CheckCardInSetAndRarityResult CheckCardInSetAndRarity(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	CardTRS r = GetCardTypeRarityAndSet((CardId)(((uint16_t)d << 8) | e));
	wBoosterCurrentCardType = r.type;
	wBoosterCurrentCardRarity = r.rarity;
	wBoosterCurrentCardSet = r.set;
	if (r.carry != 0u)
		return (CheckCardInSetAndRarityResult){
			wBoosterCurrentRarity, 0x10u, b, c, d, e, hl};

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
	CardId card = card_id_read_at(wBoosterCurrentCard_ADDR);
	uint16_t slot = (uint16_t)(wTempCardCollection_ADDR + card);
	uint8_t value = gb_read8(slot);
	uint8_t f = (uint8_t)(value == 1u ? 0x80u : 0u);
	if (value != 0u)
		f = (uint8_t)(f | 0x10u);
	return (CheckCardAlreadyDrawnResult){value, f};
}
/* <<< factory CheckCardAlreadyDrawn */
/* >>> factory FindCardsInSetAndRarity */
void FindCardsInSetAndRarity(void)
{
	for (uint8_t i = 0u; i < NUM_BOOSTER_CARD_TYPES; i++)
		gb_write8((uint16_t)(wBoosterAmountOfCardTypeTable_ADDR + i), 0u);
	uint16_t list_ptr = wBoosterViableCardList_ADDR;
	card_id_write(&list_ptr, 0u);
	list_ptr = (uint16_t)(list_ptr - 2u);
	for (CardId card_id = 1u; card_id <= NUM_CARDS; card_id++) {
		uint16_t current = wBoosterCurrentCard_ADDR;
		card_id_write(&current, card_id);
		CheckCardAlreadyDrawnResult drawn = CheckCardAlreadyDrawn();
		if (drawn.f & 0x10u)
			continue;
		CheckCardInSetAndRarityResult r = CheckCardInSetAndRarity(
			0u, 0u, (uint8_t)(card_id >> 8), (uint8_t)card_id, 0u);
		if (r.f & 0x10u)
			continue;
		uint8_t card_type = wBoosterCurrentCardType;
		uint8_t type_index = GetBoosterCardType(card_type);
		uint8_t count = gb_read8((uint16_t)(wBoosterAmountOfCardTypeTable_ADDR + type_index));
		gb_write8((uint16_t)(wBoosterAmountOfCardTypeTable_ADDR + type_index),
			(uint8_t)(count + 1u));
		card_id_write(&list_ptr, card_id);
		gb_write8(list_ptr++, type_index);
		card_id_write(&list_ptr, 0u);
		list_ptr = (uint16_t)(list_ptr - 2u);
	}
}
/* <<< factory FindCardsInSetAndRarity */
/* >>> factory InitBoosterData */
void InitBoosterData(void)
{
	for (uint16_t addr = wBoosterCardsDrawn_ADDR; addr < wBoosterCardsDrawnEnd_ADDR; addr++)
		gb_write8(addr, 0u);
	for (uint16_t i = 0; i < CARD_COLLECTION_SIZE; i++)
		gb_write8((uint16_t)(wTempCardCollection_ADDR + i), 0u);

	uint16_t hl = FindBoosterDataPointer();
	uint16_t bc = (uint16_t)((wBoosterData_TypeChances_ADDR - wBoosterData_Set_ADDR) + NUM_BOOSTER_CARD_TYPES);
	const uint8_t *src = rom_ptr(BOOSTER_PACKS_BANK, hl);
	for (uint16_t i = 0; i < bc; i++)
		gb_write8((uint16_t)(wBoosterData_Set_ADDR + i), src[i]);
	LoadRarityAmountsToWram();

	uint8_t c = 0u;
	uint8_t e = 0u;
	uint16_t ptr = wBoosterData_TypeChances_ADDR;
	for (uint8_t d = NUM_BOOSTER_CARD_TYPES; d != 0u; d--) {
		uint8_t a = gb_read8(ptr);
		ptr++;
		if (a != 0u) {
			c = (uint8_t)(a + c);
			e++;
		}
	}
	DivResult r = DivideBCbyDE((uint16_t)c, (uint16_t)e);
	wBoosterAveragedTypeChances = (uint8_t)r.quotient;
}
/* <<< factory InitBoosterData */
