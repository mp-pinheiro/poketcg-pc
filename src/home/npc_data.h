#ifndef POKETCG_HOME_NPC_DATA_H
#define POKETCG_HOME_NPC_DATA_H

#include <stdint.h>

/* >>> factory GetNPCHeaderPointer */
typedef struct {
	uint16_t hl;
	uint8_t a;
	uint8_t f;
} GetNPCHeaderPointerResult;

GetNPCHeaderPointerResult GetNPCHeaderPointer(uint8_t a);
/* <<< factory GetNPCHeaderPointer */
/* >>> factory SetNPCOpponentNameAndPortrait */
void SetNPCOpponentNameAndPortrait(uint8_t a);
/* <<< factory SetNPCOpponentNameAndPortrait */
/* >>> factory GetNPCNameAndScript */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
} GetNPCNameAndScriptResult;

GetNPCNameAndScriptResult GetNPCNameAndScript(uint8_t a);
/* <<< factory GetNPCNameAndScript */
/* >>> factory LoadNPCSpriteData */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} LoadNPCSpriteDataResult;

LoadNPCSpriteDataResult LoadNPCSpriteData(uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory LoadNPCSpriteData */
/* >>> factory _GetNPCDuelConfigurations */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} _GetNPCDuelDuelConfigurationsResult;

_GetNPCDuelDuelConfigurationsResult _GetNPCDuelConfigurations(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory _GetNPCDuelConfigurations */
/* >>> factory SetNPCDeckIDAndDuelTheme */
typedef struct { uint8_t a; uint8_t f; } SetNPCDeckIDAndDuelThemeResult;
SetNPCDeckIDAndDuelThemeResult SetNPCDeckIDAndDuelTheme(uint8_t a);
/* <<< factory SetNPCDeckIDAndDuelTheme */
/* >>> factory _GetChallengeMachineDuelConfigurations */
typedef struct { uint8_t a; uint8_t f; uint8_t b; uint8_t c; uint8_t d; uint8_t e; uint16_t hl; } _GetChallengeMachineDuelConfigurationsResult;
_GetChallengeMachineDuelConfigurationsResult _GetChallengeMachineDuelConfigurations(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl);
/* <<< factory _GetChallengeMachineDuelConfigurations */
#endif /* POKETCG_HOME_NPC_DATA_H */
