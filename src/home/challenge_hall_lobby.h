#ifndef POKETCG_HOME_CHALLENGE_HALL_LOBBY_H
#define POKETCG_HOME_CHALLENGE_HALL_LOBBY_H

#include <stdint.h>

typedef struct { uint8_t a, f; } ChallengeHallLobbyResult;
ChallengeHallLobbyResult Preload_ChallengeHallNPCs2(void);

/* >>> factory SetRonaldChallengeHallLobbyState */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } SetRonaldChallengeHallLobbyStateResult;
SetRonaldChallengeHallLobbyStateResult SetRonaldChallengeHallLobbyState(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory SetRonaldChallengeHallLobbyState */
#endif
