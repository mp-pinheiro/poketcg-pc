#ifndef POKETCG_HOME_SPECIAL_ATTACKS_H
#define POKETCG_HOME_SPECIAL_ATTACKS_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} CheckIfAnyBasicPokemonInDeckResult;

CheckIfAnyBasicPokemonInDeckResult CheckIfAnyBasicPokemonInDeck(uint8_t b,
									uint8_t c,
									uint8_t d);

#endif
