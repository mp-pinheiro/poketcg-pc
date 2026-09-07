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
/* >>> factory Preload_Courtney */
PokemonDomeResult Preload_Courtney(void);
/* <<< factory Preload_Courtney */
/* >>> factory Preload_Steve */
PokemonDomeResult Preload_Steve(void);
/* <<< factory Preload_Steve */
/* >>> factory Preload_Jack */
PokemonDomeResult Preload_Jack(void);
/* <<< factory Preload_Jack */
/* >>> factory Preload_Rod */
PokemonDomeResult Preload_Rod(void);
/* <<< factory Preload_Rod */
/* >>> factory Preload_Ronald1InPokemonDome */
PokemonDomeResult Preload_Ronald1InPokemonDome(void);
/* <<< factory Preload_Ronald1InPokemonDome */
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
