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
/* >>> factory Script_f631_ows_f63c */
/* pokemon_dome_entrance.asm Script_f631.ows_f63c, the code portion (21 bytes)
 * of the local that `set_next_npc_and_script NPC_RONALD1` names; its
 * `start_script` rst at $7651 begins the bytecode the dispatcher continues
 * into. Reached by `jp hl`, so b, c, d, e and hl are the caller's. */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } ScriptF631OwsF63cResult;
ScriptF631OwsF63cResult Script_f631_ows_f63c(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
#define Script_f631_ows_f63c_START_SCRIPT 0x7651u
/* <<< factory Script_f631_ows_f63c */
#endif /* POKETCG_HOME_POKEMON_DOME_ENTRANCE_H */
