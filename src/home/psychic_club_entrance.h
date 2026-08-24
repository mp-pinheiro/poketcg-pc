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
/* >>> factory TrySecondRonaldDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } TrySecondRonaldDuelResult;
TrySecondRonaldDuelResult TrySecondRonaldDuel(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory TrySecondRonaldDuel */
/* >>> factory LoadClubEntrance */
void LoadClubEntrance(void);
/* <<< factory LoadClubEntrance */
/* >>> factory ClubEntranceAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } ClubEntranceAfterDuelResult;
ClubEntranceAfterDuelResult ClubEntranceAfterDuel(void);
/* <<< factory ClubEntranceAfterDuel */
/* >>> factory Func_e8a0 */
typedef struct { uint8_t a; uint8_t f; } Func_e8a0Result;
Func_e8a0Result Func_e8a0(uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory Func_e8a0 */
#endif /* POKETCG_HOME_PSYCHIC_CLUB_ENTRANCE_H */
