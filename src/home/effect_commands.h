#ifndef POKETCG_HOME_EFFECT_COMMANDS_H
#define POKETCG_HOME_EFFECT_COMMANDS_H

#include <stdint.h>

/* poketcg/src/engine/duel/effect_commands.asm */

typedef struct { uint16_t hl; uint8_t carry; } EffectCmdLookup;
EffectCmdLookup CheckMatchingCommand(uint8_t a, uint16_t hl);

#endif /* POKETCG_HOME_EFFECT_COMMANDS_H */
