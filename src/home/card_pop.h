#ifndef POKETCG_HOME_CARD_POP_H
#define POKETCG_HOME_CARD_POP_H

#include <stdint.h>

uint8_t CreateCardPopCandidateList(uint8_t a);
void CalculateNameHash(uint16_t *hl, uint16_t *de);

#endif
