#ifndef POKETCG_HOME_EFFECT_COMMANDS_H
#define POKETCG_HOME_EFFECT_COMMANDS_H

#include <stdint.h>

/* poketcg/src/engine/duel/effect_commands.asm */

typedef struct { uint16_t hl; uint8_t carry; } EffectCmdLookup;
EffectCmdLookup CheckMatchingCommand(uint8_t a, uint16_t hl);

/* >>> factory TryExecuteEffectCommandFunction */
typedef struct { uint8_t a; uint8_t f; uint8_t c; uint16_t hl; } TryExecuteEffectCommandFunctionResult;
TryExecuteEffectCommandFunctionResult TryExecuteEffectCommandFunction(uint8_t a);
/* <<< factory TryExecuteEffectCommandFunction */
#endif /* POKETCG_HOME_EFFECT_COMMANDS_H */
