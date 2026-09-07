#ifndef POKETCG_HOME_FIGHTING_CLUB_LOBBY_H
#define POKETCG_HOME_FIGHTING_CLUB_LOBBY_H

#include <stdint.h>

/* >>> factory FightingClubLobbyAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } FightingClubLobbyAfterDuelResult;
FightingClubLobbyAfterDuelResult FightingClubLobbyAfterDuel(void);
/* <<< factory FightingClubLobbyAfterDuel */
/* >>> factory Preload_Granny1 */
typedef struct { uint8_t a; uint8_t f; } PreloadGranny1Result;
PreloadGranny1Result Preload_Granny1(void);
/* <<< factory Preload_Granny1 */
/* >>> factory Preload_ImakuniInFightingClubLobby */
typedef struct { uint8_t a; uint8_t f; } PreloadImakuniInFightingClubLobbyResult;
PreloadImakuniInFightingClubLobbyResult Preload_ImakuniInFightingClubLobby(void);
/* <<< factory Preload_ImakuniInFightingClubLobby */
#endif /* POKETCG_HOME_FIGHTING_CLUB_LOBBY_H */
