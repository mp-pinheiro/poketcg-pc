#ifndef POKETCG_HOME_RANDOM_H
#define POKETCG_HOME_RANDOM_H

#include <stdint.h>

/* poketcg/src/home/random.asm:34 — advance wRNG1/wRNG2/wRNGCounter, return the
 * new wRNG2 ^ wRNG1. Preserves bc/de/hl. */
uint8_t UpdateRNGSources(void);

/* poketcg/src/home/random.asm:2 — shift-and-add multiply of the two halves of
 * hl: returns (h * l) in hl. Preserves bc/de. */
uint16_t HtimesL(uint16_t hl);

/* poketcg/src/home/random.asm:23 — a random value in [0, a). Advances the RNG
 * state. Preserves bc/de/hl. */
uint8_t Random(uint8_t a);

#endif /* POKETCG_HOME_RANDOM_H */
