#ifndef POKETCG_HOME_GIFT_CENTER_H
#define POKETCG_HOME_GIFT_CENTER_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} GiftCenterPreloadResult;

GiftCenterPreloadResult Preload_GiftCenterClerk(uint8_t f);
void Func_fcad(void);

#endif
