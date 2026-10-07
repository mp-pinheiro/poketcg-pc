#ifndef POKETCG_HOME_DIVISION_H
#define POKETCG_HOME_DIVISION_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> part DivResult */
/* poketcg/src/home/division.asm */

typedef struct {
	uint16_t quotient, remainder;
} DivResult;
/* <<< part DivResult */

/* >>> factory DivideBCbyDE */
/* Divides bc by de. The asm returns the quotient in bc and the remainder in hl,
 * preserves de, and leaves the caller's carry as it found it. */
DivResult DivideBCbyDE(uint16_t bc, uint16_t de);
/* <<< factory DivideBCbyDE */

#endif /* POKETCG_HOME_DIVISION_H */
