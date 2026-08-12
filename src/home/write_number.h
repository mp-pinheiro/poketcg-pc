#ifndef POKETCG_HOME_WRITE_NUMBER_H
#define POKETCG_HOME_WRITE_NUMBER_H

#include <stdint.h>

/* poketcg/src/home/write_number.asm:128 — write hl as exactly five ASCII digits
 * (leading zeros kept) followed by a $00 terminator at the GB address in *de.
 * Six bytes are written; *de is advanced by five, not six. Preserves bc. */
void TwoByteNumberToText(uint16_t hl, uint16_t *de);

/* poketcg/src/home/write_number.asm:78-86 — BCD digit to text charcode;
 * digits 10-15 map past '9' by +7 onto the half-width digit tiles. */
uint8_t WriteBCDDigitInTextFormat(uint8_t a, uint16_t *hl);

/* poketcg/src/home/write_number.asm:69-74 — write both BCD digits of `a` as
 * text (high nibble first via a nibble swap), then fall through into
 * WriteBCDDigitInTextFormat for the low nibble; returns its last char. */
uint8_t WriteBCDNumberInTextFormat(uint8_t a, uint16_t *hl);

#endif /* POKETCG_HOME_WRITE_NUMBER_H */
