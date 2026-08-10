#ifndef POKETCG_HOME_LABELS_H
#define POKETCG_HOME_LABELS_H

#include <stdint.h>

typedef struct {
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} LabelsResult;

LabelsResult PrintLabels(uint16_t hl, uint8_t d, uint8_t e);

#endif
