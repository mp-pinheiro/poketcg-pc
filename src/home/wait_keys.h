#ifndef POKETCG_HOME_WAIT_KEYS_H
#define POKETCG_HOME_WAIT_KEYS_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part WaitKeysResult */
typedef struct {
	uint8_t a;
	uint8_t f;
} WaitKeysResult;
/* <<< part WaitKeysResult */

/* >>> factory WaitUntilKeysArePressed */
WaitKeysResult WaitUntilKeysArePressed(uint8_t keys);
/* <<< factory WaitUntilKeysArePressed */

#endif
