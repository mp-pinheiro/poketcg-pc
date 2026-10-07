#ifndef POKETCG_HOME_ROCK_CLUB_LOBBY_H
#define POKETCG_HOME_ROCK_CLUB_LOBBY_H

#include <stdint.h>

/* >>> factory RockClubLobbyAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } RockClubLobbyAfterDuelResult;
RockClubLobbyAfterDuelResult RockClubLobbyAfterDuel(void);
/* <<< factory RockClubLobbyAfterDuel */
/* >>> factory Preload_Lass3 */
typedef struct { uint8_t a; uint8_t f; } PreloadLass3Result;
PreloadLass3Result Preload_Lass3(void);
/* <<< factory Preload_Lass3 */
/* >>> factory Preload_ChrisInRockClubLobby */
typedef struct { uint8_t a; uint8_t f; } PreloadChrisInRockClubLobbyResult;
PreloadChrisInRockClubLobbyResult Preload_ChrisInRockClubLobby(void);
/* <<< factory Preload_ChrisInRockClubLobby */
#endif /* POKETCG_HOME_ROCK_CLUB_LOBBY_H */
