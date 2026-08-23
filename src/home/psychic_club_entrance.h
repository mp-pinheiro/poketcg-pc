#ifndef POKETCG_HOME_PSYCHIC_CLUB_ENTRANCE_H
#define POKETCG_HOME_PSYCHIC_CLUB_ENTRANCE_H

#include <stdint.h>

/* >>> factory TryFirstRonaldEncounter */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } TryFirstRonaldEncounterResult;
TryFirstRonaldEncounterResult TryFirstRonaldEncounter(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory TryFirstRonaldEncounter */
/* >>> factory TryFirstRonaldDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } TryFirstRonaldDuelResult;
TryFirstRonaldDuelResult TryFirstRonaldDuel(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory TryFirstRonaldDuel */
#endif /* POKETCG_HOME_PSYCHIC_CLUB_ENTRANCE_H */
