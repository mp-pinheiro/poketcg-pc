#ifndef POKETCG_HOME_FIRE_CLUB_LOBBY_H
#define POKETCG_HOME_FIRE_CLUB_LOBBY_H

#include <stdint.h>

/* >>> factory FindExtraInteractableObjects */
typedef struct { uint16_t hl; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint8_t carry; } FindExtraInteractableObjectsResult;
FindExtraInteractableObjectsResult FindExtraInteractableObjects(uint16_t hl);
/* <<< factory FindExtraInteractableObjects */
/* >>> factory FireClubPressedA */
typedef struct { uint16_t hl; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint8_t carry; } FireClubPressedAResult;
FireClubPressedAResult FireClubPressedA(void);
/* <<< factory FireClubPressedA */
/* >>> factory FireClubLobbyAfterDuel */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } FindEndOfDuelScriptResult;
FindEndOfDuelScriptResult FindEndOfDuelScript(uint16_t hl);
FindEndOfDuelScriptResult FireClubLobbyAfterDuel(void);
/* <<< factory FireClubLobbyAfterDuel */
#endif /* POKETCG_HOME_FIRE_CLUB_LOBBY_H */
