#ifndef POKETCG_HOME_PSYCHIC_CLUB_LOBBY_H
#define POKETCG_HOME_PSYCHIC_CLUB_LOBBY_H

#include <stdint.h>

/* >>> factory PsychicClubLobbyLoadMap */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint16_t hl; } PsychicClubLobbyLoadMapResult;
PsychicClubLobbyLoadMapResult PsychicClubLobbyLoadMap(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory PsychicClubLobbyLoadMap */
#endif /* POKETCG_HOME_PSYCHIC_CLUB_LOBBY_H */
