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

/* poketcg/src/home/write_number.asm:3-19 — write the two-digit BCD number
 * `a` as text to wStringBuffer, then copy 2 bytes to the BGMap0 address for
 * coordinate (b, c). Preserves b, c, d, e, hl. */
void WriteTwoDigitBCDNumber(uint8_t a, uint8_t b, uint8_t c);

/* poketcg/src/home/write_number.asm:43-64 — write the four-digit BCD number
 * `hl` (high byte first) as text to wStringBuffer, then copy 4 bytes to the
 * BGMap0 address for coordinate (b, c). Preserves b, c, d, e, hl. */
void WriteFourDigitBCDNumber(uint16_t hl, uint8_t b, uint8_t c);

/* poketcg/src/home/write_number.asm:23-39 — write the one-digit BCD number
 * in the low nibble of `a` as text to wStringBuffer, then copy 1 byte to
 * the BGMap0 address for coordinate (b, c). Preserves b, c, d, e, hl. */
void WriteOneDigitBCDNumber(uint8_t a, uint8_t b, uint8_t c);

/* poketcg/src/home/write_number.asm:90-111 — write the one-byte number `a`
 * as three decimal digits (hundreds/tens/ones, leading zeros kept, no
 * terminator) to wStringBuffer, then copy those 3 bytes to the BGMap0
 * address for coordinate (b, c). Preserves b, c, hl only: the asm never
 * saves entry de, so exit d/e are scratch and not part of the contract. */
void WriteOneByteNumber(uint8_t a, uint8_t b, uint8_t c);

/* poketcg/src/home/write_number.asm:115-125 — write hl as five decimal
 * digits (leading zeros kept) via TwoByteNumberToText into wStringBuffer,
 * then copy those 5 bytes to the BGMap0 address for coordinate (b, c).
 * Preserves b, c only: the asm never saves entry hl or de (hl is consumed
 * as the number to convert), so exit hl/d/e are scratch and not part of
 * the contract. */
void WriteTwoByteNumber(uint16_t hl, uint8_t b, uint8_t c);

#endif /* POKETCG_HOME_WRITE_NUMBER_H */
