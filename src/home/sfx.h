#ifndef POKETCG_HOME_SFX_H
#define POKETCG_HOME_SFX_H

#include <stdint.h>

void SFX_Play(uint8_t sfx_id);
void SFX_Update(void);

/* >>> factory Func_fc105 */
uint16_t Func_fc105(uint16_t bc, uint16_t de);
/* <<< factory Func_fc105 */
/* >>> factory SFX_end */
typedef struct {
	uint8_t a;
	uint8_t f;
	uint8_t b;
	uint8_t c;
	uint8_t d;
	uint8_t e;
	uint16_t hl;
} SFX_endResult;
SFX_endResult SFX_end(uint8_t b, uint8_t c, uint16_t caller_hl);
/* <<< factory SFX_end */
/* >>> factory SFX_frequency */
void SFX_frequency(uint16_t bc, uint16_t caller_hl, uint8_t high);
/* <<< factory SFX_frequency */
/* >>> factory ExecuteNextSFXCommand */
void ExecuteNextSFXCommand(uint16_t hl, uint16_t bc);
/* <<< factory ExecuteNextSFXCommand */
#endif
