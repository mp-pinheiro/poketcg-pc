#ifndef POKETCG_HOME_CHALLENGE_HALL_LOBBY_H
#define POKETCG_HOME_CHALLENGE_HALL_LOBBY_H

#include <stdint.h>

typedef struct { uint8_t a, f; } ChallengeHallLobbyResult;
ChallengeHallLobbyResult Preload_ChallengeHallNPCs2(void);

/* >>> factory Preload_ChallengeHallNPCs1 */
typedef struct { uint8_t a, f; } PreloadChallengeHallNPCs1Result;
PreloadChallengeHallNPCs1Result Preload_ChallengeHallNPCs1(void);
/* <<< factory Preload_ChallengeHallNPCs1 */

/* >>> factory ChallengeHallLobbyLoadMap */
typedef struct { uint8_t a, f, b, c; uint16_t hl; } ChallengeHallLobbyLoadMapResult;
ChallengeHallLobbyLoadMapResult ChallengeHallLobbyLoadMap(uint8_t b, uint8_t c, uint16_t hl);
/* <<< factory ChallengeHallLobbyLoadMap */

/* >>> factory Preload_ChallengeHallLobbyRonald1 */
typedef struct { uint8_t a, f, b, c, d, e; uint16_t hl; } PreloadChallengeHallLobbyRonald1Result;
PreloadChallengeHallLobbyRonald1Result Preload_ChallengeHallLobbyRonald1(void);
/* <<< factory Preload_ChallengeHallLobbyRonald1 */

/* >>> factory SetRonaldChallengeHallLobbyState */
typedef struct { uint8_t a; uint8_t f; uint16_t hl; } SetRonaldChallengeHallLobbyStateResult;
SetRonaldChallengeHallLobbyStateResult SetRonaldChallengeHallLobbyState(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory SetRonaldChallengeHallLobbyState */
#endif
