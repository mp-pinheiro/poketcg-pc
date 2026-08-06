#ifndef POKETCG_HOME_DECOMPRESS_H
#define POKETCG_HOME_DECOMPRESS_H

#include <stdint.h>

/* poketcg/src/home/decompress.asm */

/* de = source of compressed data, b = HIGH byte of the $100-byte secondary buffer,
 * which this also clears. Preserves bc and de. */
void InitDataDecompression(uint16_t de, uint8_t b);

/* Writes exactly bc bytes to de (bc == 0 means 65536), preserving de and hl.
 * Streaming: the wDecomp* state persists across calls, so callers pull one strided
 * row at a time (poketcg/src/engine/sgb.asm:295, overworld.asm:509). */
void DecompressData(uint16_t bc, uint16_t de);

/* pret symbol "DecompressData.Decompress". One byte per call, also appended to the
 * secondary buffer. Clobbers bc and hl, preserves de. */
uint8_t DecompressData_Decompress(void);

#endif /* POKETCG_HOME_DECOMPRESS_H */
