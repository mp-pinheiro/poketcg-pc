/* >>> part includes */
#include "generated/rom.h"
/* <<< part includes */
#ifndef POKETCG_HOME_SCIENCE_CLUB_LOBBY_H
#define POKETCG_HOME_SCIENCE_CLUB_LOBBY_H

/* >>> part includes_tail */
#include <stdint.h>
/* <<< part includes_tail */

/* >>> factory ScienceClubLobbyAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } ScienceClubLobbyAfterDuelResult;
ScienceClubLobbyAfterDuelResult ScienceClubLobbyAfterDuel(void);
/* <<< factory ScienceClubLobbyAfterDuel */
/* >>> factory Script_Specs2 */
typedef struct { uint8_t a; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } ScriptSpecs2Result;
ScriptSpecs2Result Script_Specs2(void);
/* <<< factory Script_Specs2 */
/* >>> factory Preload_ImakuniInScienceClubLobby */
typedef struct { uint8_t a; uint8_t f; } PreloadImakuniInScienceClubLobbyResult;
PreloadImakuniInScienceClubLobbyResult Preload_ImakuniInScienceClubLobby(void);
/* <<< factory Preload_ImakuniInScienceClubLobby */
/* >>> part Script_Specs2_START_SCRIPT */
#define Script_Specs2_START_SCRIPT (Script_Specs2_ADDR + 0x18u)
/* <<< part Script_Specs2_START_SCRIPT */
#endif /* POKETCG_HOME_SCIENCE_CLUB_LOBBY_H */
