#ifndef POKETCG_HOME_EFFECT_COMMANDS_H
#define POKETCG_HOME_EFFECT_COMMANDS_H

#include <stdint.h>
#include "home/effect_dispatch.h"

/* poketcg/src/engine/duel/effect_commands.asm */

typedef struct { uint16_t hl; uint8_t carry; } EffectCmdLookup;
EffectCmdLookup CheckMatchingCommand(uint8_t a, uint16_t hl);

/* >>> factory TryExecuteEffectCommandFunction */
typedef EffectDispatchState TryExecuteEffectCommandFunctionResult;
TryExecuteEffectCommandFunctionResult TryExecuteEffectCommandFunction(
	uint8_t command, uint8_t b, uint8_t d, uint8_t e);
/* <<< factory TryExecuteEffectCommandFunction */
#endif /* POKETCG_HOME_EFFECT_COMMANDS_H */
