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
#endif /* POKETCG_HOME_BOOSTER_PACKS_H */
