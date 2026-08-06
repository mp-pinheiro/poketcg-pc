#ifndef POKETCG_HOME_MEMORY_H
#define POKETCG_HOME_MEMORY_H

#include <stdint.h>

/* poketcg/src/home/memory.asm */

void DecompressDataFromBank(uint16_t bc, uint16_t de);
void CopyBankedDataToDE(uint16_t bc, uint16_t de);
void FillMemoryWithA(uint16_t hl, uint16_t bc, uint8_t a);
void FillMemoryWithDE(uint16_t hl, uint16_t bc, uint8_t d, uint8_t e);
uint8_t GetFarByte(uint8_t bank, uint16_t addr);

#endif /* POKETCG_HOME_MEMORY_H */
