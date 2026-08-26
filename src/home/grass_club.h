#ifndef POKETCG_HOME_GRASS_CLUB_H
#define POKETCG_HOME_GRASS_CLUB_H

#include <stdint.h>

/* >>> factory GrassClubAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } GrassClubAfterDuelResult;
GrassClubAfterDuelResult GrassClubAfterDuel(void);
/* <<< factory GrassClubAfterDuel */
/* >>> factory Script_Nikki */
typedef struct { uint8_t a; uint8_t f; } ScriptNikkiResult;
ScriptNikkiResult Script_Nikki(void);
/* <<< factory Script_Nikki */
#endif /* POKETCG_HOME_GRASS_CLUB_H */
