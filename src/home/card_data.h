#ifndef POKETCG_HOME_CARD_DATA_H
#define POKETCG_HOME_CARD_DATA_H

#include <stdint.h>

/* poketcg/src/home/card_data.asm */

uint8_t GetCardType(uint8_t e);
uint16_t GetCardName(uint8_t e);

typedef struct { uint8_t type, rarity, set; } CardTRS;
CardTRS GetCardTypeRarityAndSet(uint8_t a);

void LoadCardDataToBuffer1_FromCardID(uint8_t e);
void LoadCardDataToBuffer2_FromCardID(uint8_t e);
void LoadCardDataToBuffer1_FromName(uint16_t de);

void LoadCardGfx(uint16_t hl, uint16_t de, uint8_t b, uint8_t c);

typedef struct { uint16_t hl; uint8_t carry; uint8_t bound_zero; } CardPtrResult;
CardPtrResult GetCardPointer(uint8_t e);

/* >>> factory LoadCardDataToHL_FromCardID */
void LoadCardDataToHL_FromCardID(uint8_t e, uint16_t *hl, uint16_t saved_hl);
/* <<< factory LoadCardDataToHL_FromCardID */
#endif /* POKETCG_HOME_CARD_DATA_H */
