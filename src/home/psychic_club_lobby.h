#ifndef POKETCG_HOME_PSYCHIC_CLUB_LOBBY_H
#define POKETCG_HOME_PSYCHIC_CLUB_LOBBY_H

#include <stdint.h>

/* >>> factory PsychicClubLobbyLoadMap */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } PsychicClubLobbyLoadMapResult;
PsychicClubLobbyLoadMapResult PsychicClubLobbyLoadMap(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory PsychicClubLobbyLoadMap */
/* >>> factory PsychicClubLobbyAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } PsychicClubLobbyAfterDuelResult;
PsychicClubLobbyAfterDuelResult PsychicClubLobbyAfterDuel(void);
/* <<< factory PsychicClubLobbyAfterDuel */
#endif /* POKETCG_HOME_PSYCHIC_CLUB_LOBBY_H */
