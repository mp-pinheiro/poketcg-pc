#ifndef POKETCG_HOME_START_H
#define POKETCG_HOME_START_H

#include <stdint.h>

uint8_t ShowCardPopCGBDisclaimer(void);

/* >>> factory CheckIfHasSaveData */
typedef struct { uint8_t a; uint8_t f; } CheckIfHasSaveDataResult;
CheckIfHasSaveDataResult CheckIfHasSaveData(void);
/* <<< factory CheckIfHasSaveData */
#endif /* POKETCG_HOME_START_H */
