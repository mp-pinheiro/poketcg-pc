#ifndef POKETCG_HOME_DIVISION_H
#define POKETCG_HOME_DIVISION_H

#include <stdint.h>

/* poketcg/src/home/division.asm */

typedef struct {
	uint16_t quotient, remainder;
} DivResult;

/* Divides bc by de. The asm returns the quotient in bc and the remainder in hl,
 * preserves de, and leaves the caller's carry as it found it. */
DivResult DivideBCbyDE(uint16_t bc, uint16_t de);

#endif /* POKETCG_HOME_DIVISION_H */
