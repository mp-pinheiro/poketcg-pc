#ifndef POKETCG_HOME_MAP_H
#define POKETCG_HOME_MAP_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint16_t hl;
} PermissionResult;

PermissionResult GetPermissionByteOfMapPosition(uint8_t b, uint8_t c);
uint8_t GetPermissionOfMapPosition(uint8_t b, uint8_t c);
void SetPermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c);
uint8_t UpdatePermissionOfMapPosition(uint8_t a, uint8_t b, uint8_t c);
PermissionResult GetLoadedNPCID(uint8_t a);
PermissionResult GetItemInLoadedNPCIndex(uint8_t a, uint8_t l);

#endif
