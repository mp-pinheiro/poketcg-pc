#ifndef POKETCG_HOME_GRASS_CLUB_ENTRANCE_H
#define POKETCG_HOME_GRASS_CLUB_ENTRANCE_H

#include <stdint.h>

/* >>> factory FindEndOfDuelScript */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } FindEndOfDuelScriptResult;
FindEndOfDuelScriptResult FindEndOfDuelScript(uint16_t hl);
/* <<< factory FindEndOfDuelScript */
#endif /* POKETCG_HOME_GRASS_CLUB_ENTRANCE_H */
