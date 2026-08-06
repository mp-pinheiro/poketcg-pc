#ifndef POKETCG_HOME_WRITE_NUMBER_H
#define POKETCG_HOME_WRITE_NUMBER_H

#include <stdint.h>

/* poketcg/src/home/write_number.asm:128 — write hl as exactly five ASCII digits
 * (leading zeros kept) followed by a $00 terminator at the GB address in *de.
 * Six bytes are written; *de is advanced by five, not six. Preserves bc. */
void TwoByteNumberToText(uint16_t hl, uint16_t *de);

#endif /* POKETCG_HOME_WRITE_NUMBER_H */
