#ifndef POKETCG_HOME_MASTERS_BEATEN_LIST_H
#define POKETCG_HOME_MASTERS_BEATEN_LIST_H

#include <stdint.h>

uint8_t ClearMasterBeatenList(uint8_t *f);
uint8_t AddMasterBeatenToList(uint8_t a, uint8_t *f);

/* >>> factory AddAllMastersToMastersBeatenList */
uint8_t AddAllMastersToMastersBeatenList(uint8_t *f);
/* <<< factory AddAllMastersToMastersBeatenList */
#endif
