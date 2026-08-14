#ifndef POKETCG_HOME_SCREEN_EFFECTS_H
#define POKETCG_HOME_SCREEN_EFFECTS_H

#include <stdint.h>

/* >>> factory DecrementScreenAnimDuration */
typedef struct { uint16_t hl; uint8_t f; } DecrementDurResult;
DecrementDurResult DecrementScreenAnimDuration(uint8_t f);
/* <<< factory DecrementScreenAnimDuration */
#endif /* POKETCG_HOME_SCREEN_EFFECTS_H */
