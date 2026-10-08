/* >>> factory AddBoosterCardToTempCardCollection */
typedef struct { uint8_t a; uint8_t f; } AddBoosterCardToTempCardCollectionResult;
AddBoosterCardToTempCardCollectionResult AddBoosterCardToTempCardCollection(void);
/* <<< factory AddBoosterCardToTempCardCollection */
/* >>> factory AddBoosterEnergyToDrawnEnergies */
typedef struct { uint8_t a; uint8_t f; uint8_t d; uint8_t e; } AddBoosterEnergyToDrawnEnergiesResult;
AddBoosterEnergyToDrawnEnergiesResult AddBoosterEnergyToDrawnEnergies(CardId a);
/* <<< factory AddBoosterEnergyToDrawnEnergies */
/* >>> factory GenerateTwoTypesEnergyBooster */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } GenerateTwoTypesEnergyBoosterResult;
GenerateTwoTypesEnergyBoosterResult GenerateTwoTypesEnergyBooster(uint16_t hl);
/* <<< factory GenerateTwoTypesEnergyBooster */
/* === factory GenerateEnergyBoosterWaterFighting */
/* >>> factory GenerateFightingEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateFightingEnergy(void);
/* <<< factory GenerateFightingEnergy */
/* >>> factory GenerateFireEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateFireEnergy(void);
/* <<< factory GenerateFireEnergy */
/* >>> factory GenerateGrassEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateGrassEnergy(void);
/* <<< factory GenerateGrassEnergy */
/* >>> factory GenerateLightningEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateLightningEnergy(void);
/* <<< factory GenerateLightningEnergy */
/* >>> factory GeneratePsychicEnergy */
AddBoosterEnergyToDrawnEnergiesResult GeneratePsychicEnergy(void);
/* <<< factory GeneratePsychicEnergy */
/* >>> factory GenerateWaterEnergy */
AddBoosterEnergyToDrawnEnergiesResult GenerateWaterEnergy(void);
/* <<< factory GenerateWaterEnergy */
/* >>> factory GenerateRandomEnergyBooster */
AddBoosterEnergyToDrawnEnergiesResult GenerateRandomEnergyBooster(void);
/* <<< factory GenerateRandomEnergyBooster */
