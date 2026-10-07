#ifndef POKETCG_HOME_BG_MAP_H
#define POKETCG_HOME_BG_MAP_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory WriteDataBlocksToBGMap0 */
void WriteDataBlocksToBGMap0(uint16_t *hl, uint16_t *de, uint8_t *a, uint8_t *b, uint8_t *c);
/* <<< factory WriteDataBlocksToBGMap0 */
/* >>> factory WriteDataBlockToBGMap0 */
void WriteDataBlockToBGMap0(uint16_t *hl, uint16_t *de, uint8_t *a, uint8_t *b, uint8_t *c);
/* <<< factory WriteDataBlockToBGMap0 */
/* >>> factory WriteByteToBGMap0 */
uint8_t WriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory WriteByteToBGMap0 */

/* >>> factory HblankWriteByteToBGMap0 */
/* Returns the exit value of a, which is always 0 -- see the note in bg_map.c. */
uint8_t HblankWriteByteToBGMap0(uint8_t a, uint8_t b, uint8_t c);
/* <<< factory HblankWriteByteToBGMap0 */
/* >>> factory CopyDataToBGMap0 */
void CopyDataToBGMap0(uint8_t a, uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c);
/* <<< factory CopyDataToBGMap0 */
/* >>> factory SafeCopyDataHLtoDE */
void SafeCopyDataHLtoDE(uint16_t *hl, uint16_t *de, uint8_t b);
/* <<< factory SafeCopyDataHLtoDE */

#endif
