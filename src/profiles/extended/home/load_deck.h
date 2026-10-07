#ifndef POKETCG_HOME_LOAD_DECK_H
#define POKETCG_HOME_LOAD_DECK_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory LoadDeck */
/* poketcg/src/home/load_deck.asm */

uint8_t LoadDeck(uint8_t a);
/* <<< factory LoadDeck */
/* >>> factory CompressDeckToSRAM */
void CompressDeckToSRAM(uint16_t de, uint16_t hl);
/* <<< factory CompressDeckToSRAM */
/* >>> factory DecompressSRAMDeck */
void DecompressSRAMDeck(uint16_t de, uint16_t hl);
/* <<< factory DecompressSRAMDeck */

#endif /* POKETCG_HOME_LOAD_DECK_H */
