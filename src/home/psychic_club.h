#ifndef POKETCG_HOME_PSYCHIC_CLUB_H
#define POKETCG_HOME_PSYCHIC_CLUB_H

#include <stdint.h>

/* >>> factory PsychicClubAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } PsychicClubAfterDuelResult;
PsychicClubAfterDuelResult PsychicClubAfterDuel(void);
/* <<< factory PsychicClubAfterDuel */
/* >>> factory Preload_Murray2 */
typedef struct { uint8_t a; uint8_t f; } Preload_Murray2Result;
Preload_Murray2Result Preload_Murray2(uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory Preload_Murray2 */
#endif /* POKETCG_HOME_PSYCHIC_CLUB_H */
