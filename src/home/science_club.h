#ifndef POKETCG_HOME_SCIENCE_CLUB_H
#define POKETCG_HOME_SCIENCE_CLUB_H

#include <stdint.h>

/* >>> factory Preload_Joseph */
typedef struct { uint8_t a; uint8_t f; } PreloadJosephResult;
PreloadJosephResult Preload_Joseph(void);
/* <<< factory Preload_Joseph */
/* >>> factory ScienceClubAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } ScienceClubAfterDuelResult;
ScienceClubAfterDuelResult ScienceClubAfterDuel(void);
/* <<< factory ScienceClubAfterDuel */
#endif /* POKETCG_HOME_SCIENCE_CLUB_H */
