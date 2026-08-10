#ifndef POKETCG_HOME_WAIT_KEYS_H
#define POKETCG_HOME_WAIT_KEYS_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} WaitKeysResult;

WaitKeysResult WaitUntilKeysArePressed(uint8_t keys);

#endif
