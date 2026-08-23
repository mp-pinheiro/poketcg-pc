#ifndef POKETCG_HOME_WATER_CLUB_LOBBY_H
#define POKETCG_HOME_WATER_CLUB_LOBBY_H

#include <stdint.h>

/* >>> factory WaterClubLobbyAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } WaterClubLobbyAfterDuelResult;
WaterClubLobbyAfterDuelResult WaterClubLobbyAfterDuel(void);
/* <<< factory WaterClubLobbyAfterDuel */
#endif /* POKETCG_HOME_WATER_CLUB_LOBBY_H */
