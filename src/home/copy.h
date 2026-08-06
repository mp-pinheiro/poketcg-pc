#ifndef POKETCG_HOME_COPY_H
#define POKETCG_HOME_COPY_H

#include <stdint.h>

/* poketcg/src/home/copy.asm */

/* copy.asm:3 — b blocks of c bytes, hl/de advanced past the whole run.
 * b == 0 is 256 blocks, c == 0 is 256 bytes per block. */
void CopyGfxData(uint16_t *hl, uint16_t *de, uint8_t b, uint8_t c);

/* copy.asm:49 — bc bytes, hl/de advanced. bc == 0 is 65536 bytes. */
void CopyDataHLtoDE(uint16_t *hl, uint16_t *de, uint16_t bc);

/* copy.asm:38 */
void CopyDataHLtoDE_SaveRegisters(uint16_t hl, uint16_t de, uint16_t bc);

#endif /* POKETCG_HOME_COPY_H */
