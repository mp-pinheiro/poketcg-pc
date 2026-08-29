#ifndef POKETCG_HOME_CREDITS_H
#define POKETCG_HOME_CREDITS_H

#include <stdint.h>

/* >>> factory Func_1d758 */
void Func_1d758(void);
/* <<< factory Func_1d758 */
/* >>> factory Func_1d765 */
uint8_t Func_1d765(void);
/* <<< factory Func_1d765 */
/* >>> factory Func_1d7ee */
void Func_1d7ee(void);
/* <<< factory Func_1d7ee */
/* >>> factory Func_1d705 */
void Func_1d705(void);
/* <<< factory Func_1d705 */

/* >>> factory PlayCreditsSequence */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint16_t hl;
} PlayCreditsSequenceResult;
PlayCreditsSequenceResult PlayCreditsSequence(void);
/* <<< factory PlayCreditsSequence */
#endif /* POKETCG_HOME_CREDITS_H */
