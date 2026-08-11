#ifndef HOME_WATER_CLUB_H
#define HOME_WATER_CLUB_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} PreloadAmyResult;

PreloadAmyResult Preload_Amy(void);

#endif
