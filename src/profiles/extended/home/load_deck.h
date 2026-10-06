#ifndef POKETCG_HOME_LOAD_DECK_H
#define POKETCG_HOME_LOAD_DECK_H

#include <stdint.h>

/* poketcg/src/home/load_deck.asm */

uint8_t LoadDeck(uint8_t a);
void CompressDeckToSRAM(uint16_t de, uint16_t hl);
void DecompressSRAMDeck(uint16_t de, uint16_t hl);

#endif /* POKETCG_HOME_LOAD_DECK_H */
