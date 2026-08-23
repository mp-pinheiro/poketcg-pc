#ifndef POKETCG_HOME_BOOSTER_PACKS_H
#define POKETCG_HOME_BOOSTER_PACKS_H

#include <stdint.h>

/* >>> factory GetCurrentRarityAmount */
typedef struct { uint8_t a; uint16_t hl; } RarityAmount;
RarityAmount GetCurrentRarityAmount(void);
/* <<< factory GetCurrentRarityAmount */
/* >>> factory GetBoosterCardType */
uint8_t GetBoosterCardType(uint8_t a);
/* <<< factory GetBoosterCardType */
/* >>> factory CalculateTypeChances */
uint8_t CalculateTypeChances(void);
/* <<< factory CalculateTypeChances */
/* >>> factory UpdateBoosterCardTypesChanceByte */
uint8_t UpdateBoosterCardTypesChanceByte(void);
/* <<< factory UpdateBoosterCardTypesChanceByte */
/* >>> factory AppendCurrentCardToHL */
void AppendCurrentCardToHL(uint16_t *hl);
/* <<< factory AppendCurrentCardToHL */
/* >>> factory AddBoosterCardToTempCardCollection */
void AddBoosterCardToTempCardCollection(void);
/* <<< factory AddBoosterCardToTempCardCollection */
/* >>> factory AddBoosterCardToDrawnEnergies */
typedef struct { uint8_t a; uint8_t f; } AddBoosterCardToDrawnEnergiesResult;
AddBoosterCardToDrawnEnergiesResult AddBoosterCardToDrawnEnergies(void);
/* <<< factory AddBoosterCardToDrawnEnergies */
/* >>> factory AddBoosterEnergyToDrawnEnergies */
typedef struct { uint8_t a; uint8_t f; } AddBoosterEnergyToDrawnEnergiesResult;
AddBoosterEnergyToDrawnEnergiesResult AddBoosterEnergyToDrawnEnergies(uint8_t a);
/* <<< factory AddBoosterEnergyToDrawnEnergies */
/* >>> factory ZeroBoosterRarityData */
void ZeroBoosterRarityData(void);
/* <<< factory ZeroBoosterRarityData */
/* >>> factory GenerateTwoTypesEnergyBooster */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } GenerateTwoTypesEnergyBoosterResult;
GenerateTwoTypesEnergyBoosterResult GenerateTwoTypesEnergyBooster(uint16_t hl);
/* <<< factory GenerateTwoTypesEnergyBooster */
/* >>> factory GenerateRandomEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateRandomEnergy(void);
/* <<< factory GenerateRandomEnergy */
/* >>> factory GenerateEnergyBoosterGrassPsychic */
GenerateTwoTypesEnergyBoosterResult GenerateEnergyBoosterGrassPsychic(void);
/* <<< factory GenerateEnergyBoosterGrassPsychic */
/* >>> factory GenerateEnergyBoosterLightningFire */
GenerateTwoTypesEnergyBoosterResult GenerateEnergyBoosterLightningFire(void);
/* <<< factory GenerateEnergyBoosterLightningFire */
/* >>> factory GenerateEnergyBoosterWaterFighting */
GenerateTwoTypesEnergyBoosterResult GenerateEnergyBoosterWaterFighting(void);
/* <<< factory GenerateEnergyBoosterWaterFighting */
/* >>> factory GenerateRandomEnergyBooster */
void GenerateRandomEnergyBooster(void);
/* <<< factory GenerateRandomEnergyBooster */
/* >>> factory PutEnergiesAndNonEnergiesTogether */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} PutEnergiesAndNonEnergiesTogetherResult;
PutEnergiesAndNonEnergiesTogetherResult PutEnergiesAndNonEnergiesTogether(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory PutEnergiesAndNonEnergiesTogether */
/* >>> factory LoadRarityAmountsToWram */
void LoadRarityAmountsToWram(void);
/* <<< factory LoadRarityAmountsToWram */
/* >>> factory DetermineBoosterCardType */
uint8_t DetermineBoosterCardType(uint8_t a);
/* <<< factory DetermineBoosterCardType */
/* >>> factory FindBoosterDataPointer */
uint16_t FindBoosterDataPointer(void);
/* <<< factory FindBoosterDataPointer */
/* >>> factory AddBoosterCardToDrawnNonEnergies */
void AddBoosterCardToDrawnNonEnergies(void);
/* <<< factory AddBoosterCardToDrawnNonEnergies */
/* >>> factory AddBoosterCardsToCollection */
void AddBoosterCardsToCollection(void);
/* <<< factory AddBoosterCardsToCollection */
/* >>> factory GenerateBoosterEnergies */
void GenerateBoosterEnergies(void);
/* <<< factory GenerateBoosterEnergies */
/* >>> factory DetermineBoosterCard */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } DetermineBoosterCardResult;
DetermineBoosterCardResult DetermineBoosterCard(uint8_t d, uint8_t e);
/* <<< factory DetermineBoosterCard */
/* >>> factory CheckCardInSetAndRarity */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } CheckCardInSetAndRarityResult;
CheckCardInSetAndRarityResult CheckCardInSetAndRarity(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory CheckCardInSetAndRarity */
/* >>> factory CheckCardAlreadyDrawn */
typedef struct { uint8_t a; uint8_t f; } CheckCardAlreadyDrawnResult;
CheckCardAlreadyDrawnResult CheckCardAlreadyDrawn(void);
/* <<< factory CheckCardAlreadyDrawn */
/* >>> factory FindCardsInSetAndRarity */
void FindCardsInSetAndRarity(void);
/* <<< factory FindCardsInSetAndRarity */
/* >>> factory GenerateBoosterNonEnergies */
typedef struct { uint8_t a; uint8_t f; } GenerateBoosterNonEnergiesResult;
GenerateBoosterNonEnergiesResult GenerateBoosterNonEnergies(void);
/* <<< factory GenerateBoosterNonEnergies */
/* >>> factory InitBoosterData */
void InitBoosterData(void);
/* <<< factory InitBoosterData */
/* >>> factory GenerateBoosterPack */
void GenerateBoosterPack(uint8_t a);
/* <<< factory GenerateBoosterPack */
#endif /* POKETCG_HOME_BOOSTER_PACKS_H */
