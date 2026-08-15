#ifndef POKETCG_HOME_PKMN_POWERS_H
#define POKETCG_HOME_PKMN_POWERS_H

#include <stdint.h>

/* >>> factory HandleAIShift */
typedef struct { uint8_t a; uint8_t f; } AIShiftResult;
AIShiftResult HandleAIShift(uint8_t c);
/* <<< factory HandleAIShift */
#endif /* POKETCG_HOME_PKMN_POWERS_H */
