#ifndef POKETCG_HOME_LIGHTNING_CLUB_LOBBY_H
#define POKETCG_HOME_LIGHTNING_CLUB_LOBBY_H

#include <stdint.h>

/* >>> factory LightningClubLobbyAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } LightningClubLobbyAfterDuelResult;
LightningClubLobbyAfterDuelResult LightningClubLobbyAfterDuel(void);
/* <<< factory LightningClubLobbyAfterDuel */
#endif /* POKETCG_HOME_LIGHTNING_CLUB_LOBBY_H */
