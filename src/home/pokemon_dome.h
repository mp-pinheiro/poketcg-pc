#ifndef POKETCG_HOME_POKEMON_DOME_H
#define POKETCG_HOME_POKEMON_DOME_H

#include <stdint.h>

typedef struct { uint8_t a, f; } PokemonDomeResult;

PokemonDomeResult Func_f762(void);
PokemonDomeResult Func_f782(uint8_t b, uint8_t c, uint8_t f);
PokemonDomeResult PlacePokemonDomeOpponentAtDuelTable(uint8_t f);

/* >>> factory Func_f77d */
PokemonDomeResult Func_f77d(uint8_t b, uint8_t c, uint8_t f);
/* <<< factory Func_f77d */
/* >>> factory PokemonDomeCloseTextBox */
void PokemonDomeCloseTextBox(void);
/* <<< factory PokemonDomeCloseTextBox */
/* >>> factory PokemonDomeMovePlayer */
void PokemonDomeMovePlayer(void);
/* <<< factory PokemonDomeMovePlayer */
/* >>> factory PokemonDomeLoadMap */
void PokemonDomeLoadMap(void);
/* <<< factory PokemonDomeLoadMap */
/* >>> factory PokemonDomeAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } PokemonDomeAfterDuelResult;
PokemonDomeAfterDuelResult PokemonDomeAfterDuel(void);
/* <<< factory PokemonDomeAfterDuel */
#endif
