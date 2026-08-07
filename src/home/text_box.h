#ifndef POKETCG_HOME_TEXT_BOX_H
#define POKETCG_HOME_TEXT_BOX_H

#include <stdint.h>

void SafeCopyDataDEtoHL(uint16_t *de, uint16_t *hl, uint8_t c);
uint16_t DECoordToBGMap0Address(uint8_t d, uint8_t e);
void AdjustCoordinatesForBGScroll(uint8_t *d, uint8_t *e);
void CopyLine(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e);
void DrawRegularTextBoxCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e);
void ContinueDrawingTextBoxCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e);
void CopyCurrentLineTilesAndAttrCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e);
void CopyCurrentLineAttrCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e);

#endif
