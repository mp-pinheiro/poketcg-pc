#ifndef POKETCG_HOME_POKEMON_DOME_ENTRANCE_H
#define POKETCG_HOME_POKEMON_DOME_ENTRANCE_H

#include <stdint.h>

/* >>> factory PokemonDomeEntranceLoadMap */
typedef struct { uint8_t a; uint8_t f; } PokemonDomeEntranceLoadMapResult;
PokemonDomeEntranceLoadMapResult PokemonDomeEntranceLoadMap(void);
/* <<< factory PokemonDomeEntranceLoadMap */
/* >>> factory PokemonDomeEntranceCloseTextBox */
void PokemonDomeEntranceCloseTextBox(void);
/* <<< factory PokemonDomeEntranceCloseTextBox */
#endif /* POKETCG_HOME_POKEMON_DOME_ENTRANCE_H */
