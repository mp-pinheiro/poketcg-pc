#ifndef POKETCG_HOME_CHALLENGE_HALL_H
#define POKETCG_HOME_CHALLENGE_HALL_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
} ChallengeHallClearResult;

typedef struct {
	uint8_t b;
	uint16_t hl;
} ChallengeHallBitResult;

ChallengeHallClearResult Func_f5db(void);
ChallengeHallBitResult Func_f5e9(uint8_t c);
void Script_Host(void);

/* >>> factory Func_f5cc */
/* Func_f5cc:: challenge_hall.asm:517-523. c = bit index (0-31) into the
 * wd698 4-byte flag bitmap, via Func_f5e9's byte/mask split. Exit carry
 * (f bit 0x10) is set iff the bit is set -- the only caller (Func_f580's
 * challenger picker) branches on carry alone; a holds the raw `and` result.
 * b/hl are Func_f5e9's internal byte/mask outputs, never read after this
 * call returns, so they are not part of the callable contract. */
typedef struct {
	uint8_t a;
	uint8_t f;
} ChallengeHallTestBitResult;
ChallengeHallTestBitResult Func_f5cc(uint8_t c);
/* <<< factory Func_f5cc */
/* >>> factory Func_f5d4 */
/* Func_f5d4:: challenge_hall.asm:525-530. c = bit index (0-31) into the
 * wd698 4-byte flag bitmap, via Func_f5e9's byte/mask split. Sets that bit
 * and writes the byte back through the same address; a is the post-OR byte
 * (never 0, since the mask is never 0), f is `or b`'s result flags
 * (N=H=C=0, Z from the OR). b/hl are Func_f5e9's internal outputs and are
 * not part of the callable contract (unread by the only caller). */
typedef struct {
	uint8_t a;
	uint8_t f;
} ChallengeHallSetBitResult;
ChallengeHallSetBitResult Func_f5d4(uint8_t c);
/* <<< factory Func_f5d4 */
#endif
