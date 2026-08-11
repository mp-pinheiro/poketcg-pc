#ifndef POKETCG_HOME_MASTERS_BEATEN_LIST_H
#define POKETCG_HOME_MASTERS_BEATEN_LIST_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} MasterBeatenListResult;

MasterBeatenListResult AddMasterBeatenToList(uint8_t a);
MasterBeatenListResult ClearMasterBeatenList(void);

#endif /* POKETCG_HOME_MASTERS_BEATEN_LIST_H */
