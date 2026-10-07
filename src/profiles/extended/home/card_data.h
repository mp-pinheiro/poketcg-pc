#ifndef POKETCG_HOME_CARD_DATA_H
#define POKETCG_HOME_CARD_DATA_H

/* >>> part includes */
#include <stdint.h>
#include "home/card_id.h"
/* <<< part includes */

/* >>> factory GetCardType */
/* poketcg/src/home/card_data.asm */

uint8_t GetCardType(CardId e);
/* <<< factory GetCardType */
/* >>> factory GetCardName */
uint16_t GetCardName(CardId e);
/* <<< factory GetCardName */

/* >>> part CardTRS */
typedef struct { uint8_t type, rarity, set, carry; } CardTRS;
/* <<< part CardTRS */
/* >>> factory GetCardTypeRarityAndSet */
CardTRS GetCardTypeRarityAndSet(CardId a);
/* <<< factory GetCardTypeRarityAndSet */

/* >>> factory LoadCardDataToBuffer1_FromCardID */
void LoadCardDataToBuffer1_FromCardID(CardId e);
/* <<< factory LoadCardDataToBuffer1_FromCardID */
/* >>> factory LoadCardDataToBuffer2_FromCardID */
void LoadCardDataToBuffer2_FromCardID(CardId e);
/* <<< factory LoadCardDataToBuffer2_FromCardID */
/* >>> factory LoadCardDataToBuffer1_FromName */
void LoadCardDataToBuffer1_FromName(uint16_t de);
/* <<< factory LoadCardDataToBuffer1_FromName */

/* >>> part LoadCardGfx */
void LoadCardGfx(uint16_t hl, uint16_t de, uint8_t b, uint8_t c);
/* <<< part LoadCardGfx */

/* >>> part CardPtrResult */
typedef struct { uint16_t hl; uint8_t carry; uint8_t bank; } CardPtrResult;
/* <<< part CardPtrResult */
/* >>> factory GetCardPointer */
CardPtrResult GetCardPointer(CardId e);
/* <<< factory GetCardPointer */

/* >>> factory LoadCardDataToHL_FromCardID */
void LoadCardDataToHL_FromCardID(CardId e, uint16_t *hl, uint16_t saved_hl);
/* <<< factory LoadCardDataToHL_FromCardID */
#endif /* POKETCG_HOME_CARD_DATA_H */
