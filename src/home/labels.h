#ifndef POKETCG_HOME_LABELS_H
#define POKETCG_HOME_LABELS_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part LabelsResult */
typedef struct {
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} LabelsResult;
/* <<< part LabelsResult */

/* >>> factory PrintLabels */
LabelsResult PrintLabels(uint16_t hl, uint8_t d, uint8_t e);
/* <<< factory PrintLabels */

/* >>> factory InitAndPrintMenu */
void InitAndPrintMenu(uint16_t hl, uint8_t a);
/* <<< factory InitAndPrintMenu */
#endif
