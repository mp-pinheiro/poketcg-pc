#ifndef POKETCG_HOME_MEMORY_H
#define POKETCG_HOME_MEMORY_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory DecompressDataFromBank */
/* poketcg/src/home/memory.asm */

void DecompressDataFromBank(uint16_t bc, uint16_t de);
/* <<< factory DecompressDataFromBank */
/* >>> factory CopyBankedDataToDE */
void CopyBankedDataToDE(uint16_t bc, uint16_t de);
/* <<< factory CopyBankedDataToDE */
/* >>> factory FillMemoryWithA */
void FillMemoryWithA(uint16_t hl, uint16_t bc, uint8_t a);
/* <<< factory FillMemoryWithA */
/* >>> factory FillMemoryWithDE */
void FillMemoryWithDE(uint16_t hl, uint16_t bc, uint8_t d, uint8_t e);
/* <<< factory FillMemoryWithDE */
/* >>> factory GetFarByte */
uint8_t GetFarByte(uint8_t bank, uint16_t addr);
/* <<< factory GetFarByte */

#endif /* POKETCG_HOME_MEMORY_H */
