#ifndef POKETCG_HOME_TEXT_BOX_H
#define POKETCG_HOME_TEXT_BOX_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory SafeCopyDataDEtoHL */
uint8_t SafeCopyDataDEtoHL(uint16_t *de, uint16_t *hl, uint8_t c);
/* <<< factory SafeCopyDataDEtoHL */
/* >>> factory DECoordToBGMap0Address */
uint16_t DECoordToBGMap0Address(uint8_t d, uint8_t e);
/* <<< factory DECoordToBGMap0Address */
/* >>> factory AdjustCoordinatesForBGScroll */
void AdjustCoordinatesForBGScroll(uint8_t *d, uint8_t *e);
/* <<< factory AdjustCoordinatesForBGScroll */
/* >>> factory CopyLine */
void CopyLine(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e);
/* <<< factory CopyLine */
/* >>> factory DrawRegularTextBox */
void DrawRegularTextBox(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory DrawRegularTextBox */
/* >>> factory ContinueDrawingTextBoxDMG */
void ContinueDrawingTextBoxDMG(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory ContinueDrawingTextBoxDMG */
/* >>> factory DrawRegularTextBoxCGB */
void DrawRegularTextBoxCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory DrawRegularTextBoxCGB */
/* >>> factory ContinueDrawingTextBoxCGB */
void ContinueDrawingTextBoxCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory ContinueDrawingTextBoxCGB */
/* >>> factory CopyCurrentLineTilesAndAttrCGB */
void CopyCurrentLineTilesAndAttrCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e);
/* <<< factory CopyCurrentLineTilesAndAttrCGB */
/* >>> factory CopyCurrentLineAttrCGB */
void CopyCurrentLineAttrCGB(uint16_t *hl, uint8_t a, uint8_t b, uint8_t d, uint8_t e);
/* <<< factory CopyCurrentLineAttrCGB */
/* >>> factory DrawLabeledTextBox */
void DrawLabeledTextBox(uint16_t *hl, uint8_t a, uint8_t b, uint8_t c, uint8_t d, uint8_t e);
/* <<< factory DrawLabeledTextBox */

#endif
