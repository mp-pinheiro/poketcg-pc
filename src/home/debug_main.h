#ifndef POKETCG_HOME_DEBUG_MAIN_H
#define POKETCG_HOME_DEBUG_MAIN_H

#include <stdint.h>

typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} Func126b3Result;

Func126b3Result Func_126b3(void);

/* >>> factory Func_12661 */
/* debug_main.asm:36 `ret` inherits Func_126b3's a/f/hl unchanged, so the
 * dispatcher's result type is this routine's too. */
Func126b3Result Func_12661(void);
/* <<< factory Func_12661 */
#endif
