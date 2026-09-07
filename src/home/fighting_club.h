#ifndef POKETCG_HOME_FIGHTING_CLUB_H
#define POKETCG_HOME_FIGHTING_CLUB_H

#include <stdint.h>

/* >>> factory FightingClubAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } FightingClubAfterDuelResult;
FightingClubAfterDuelResult FightingClubAfterDuel(void);
/* <<< factory FightingClubAfterDuel */
/* >>> factory Preload_ChrisInFightingClub */
typedef struct { uint8_t a; uint8_t f; } PreloadPupilInFightingClubResult;
PreloadPupilInFightingClubResult Preload_ChrisInFightingClub(void);
/* <<< factory Preload_ChrisInFightingClub */
/* >>> factory Preload_MichaelInFightingClub */
PreloadPupilInFightingClubResult Preload_MichaelInFightingClub(void);
/* <<< factory Preload_MichaelInFightingClub */
/* >>> factory Preload_JessicaInFightingClub */
PreloadPupilInFightingClubResult Preload_JessicaInFightingClub(void);
/* <<< factory Preload_JessicaInFightingClub */
#endif /* POKETCG_HOME_FIGHTING_CLUB_H */
