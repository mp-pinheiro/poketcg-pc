#ifndef POKETCG_HOME_POKEMON_DOME_H
#define POKETCG_HOME_POKEMON_DOME_H

#include <stdint.h>

typedef struct { uint8_t a, f; } PokemonDomeResult;

PokemonDomeResult Func_f762(void);
PokemonDomeResult Func_f782(uint8_t b, uint8_t c, uint8_t f);
PokemonDomeResult PlacePokemonDomeOpponentAtDuelTable(uint8_t f);

#endif
