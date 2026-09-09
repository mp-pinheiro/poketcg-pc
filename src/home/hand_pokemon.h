#ifndef POKETCG_HOME_HAND_POKEMON_H
#define POKETCG_HOME_HAND_POKEMON_H

#include <stdint.h>

/* >>> factory AIDecideSpecialEvolutions */
void AIDecideSpecialEvolutions(void);
/* <<< factory AIDecideSpecialEvolutions */
/* >>> factory AIDecideEvolution */
/* >>> factory AIDecideEvolution */
uint8_t AIDecideEvolution(void);
/* <<< factory AIDecideEvolution */
/* >>> factory AIDecidePlayLegendaryBirds */
/* >>> factory AIDecidePlayLegendaryBirds */
void AIDecidePlayLegendaryBirds(void);
/* <<< factory AIDecidePlayLegendaryBirds */
/* >>> factory AIDecidePlayPokemonCard */
typedef struct { uint8_t a; uint8_t f; } AIDecidePlayPokemonCardResult;
AIDecidePlayPokemonCardResult AIDecidePlayPokemonCard(void);
/* <<< factory AIDecidePlayPokemonCard */
#endif /* POKETCG_HOME_HAND_POKEMON_H */
