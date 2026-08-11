#ifndef POKETCG_HOME_MASON_LABORATORY_H
#define POKETCG_HOME_MASON_LABORATORY_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} PreloadDrMasonResult;

void Script_Tech1(void);
PreloadDrMasonResult Preload_DrMason(void);

#endif
