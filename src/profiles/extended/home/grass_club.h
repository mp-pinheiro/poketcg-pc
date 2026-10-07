/* >>> part includes */
#include "generated/rom.h"
/* <<< part includes */
#ifndef POKETCG_HOME_GRASS_CLUB_H
#define POKETCG_HOME_GRASS_CLUB_H

/* >>> part includes_tail */
#include <stdint.h>
/* <<< part includes_tail */

/* >>> factory GrassClubAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } GrassClubAfterDuelResult;
GrassClubAfterDuelResult GrassClubAfterDuel(void);
/* <<< factory GrassClubAfterDuel */
/* >>> factory Script_Nikki */
typedef struct { uint8_t a; uint8_t f; } ScriptNikkiResult;
ScriptNikkiResult Script_Nikki(void);
/* <<< factory Script_Nikki */
/* >>> factory Preload_NikkiInGrassClub */
typedef struct { uint8_t a; uint8_t f; } PreloadNikkiInGrassClubResult;
PreloadNikkiInGrassClubResult Preload_NikkiInGrassClub(void);
/* <<< factory Preload_NikkiInGrassClub */
/* >>> part Script_Nikki_START_SCRIPT */
#define Script_Nikki_START_SCRIPT (Script_Nikki_ADDR + 0x08u)
/* <<< part Script_Nikki_START_SCRIPT */
#endif /* POKETCG_HOME_GRASS_CLUB_H */
