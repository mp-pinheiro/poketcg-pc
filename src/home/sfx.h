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
/* >>> factory Func_fc279 */
void Func_fc279(void);
/* <<< factory Func_fc279 */
/* >>> factory Func_fc26c */
void Func_fc26c(void);
/* <<< factory Func_fc26c */
/* >>> factory SFX_loop */
void SFX_loop(uint16_t bc, uint16_t caller_de);
/* <<< factory SFX_loop */
/* >>> factory SFX_pan */
/* >>> factory SFX_pan */
void SFX_pan(uint16_t bc, uint16_t caller_hl);
/* <<< factory SFX_pan */
/* >>> factory SFX_unused */
void SFX_unused(uint16_t hl, uint16_t bc);
/* <<< factory SFX_unused */
/* >>> factory SFX_pitch_offset */
void SFX_pitch_offset(uint16_t bc, uint16_t caller_hl);
/* <<< factory SFX_pitch_offset */
/* >>> factory SFX_wave */
void SFX_wave(uint8_t a, uint16_t bc, uint16_t caller_hl);
/* <<< factory SFX_wave */
/* >>> factory SFX_duty */
void SFX_duty(uint8_t a, uint16_t bc, uint16_t caller_hl);
/* <<< factory SFX_duty */
/* >>> factory SFX_envelope */
/* >>> factory SFX_envelope */
void SFX_envelope(uint16_t bc, uint16_t caller_hl);
/* <<< factory SFX_envelope */
/* >>> factory SFX_endloop */
void SFX_endloop(uint16_t bc, uint16_t caller_word);
/* <<< factory SFX_endloop */
/* >>> factory SFX_wait */
uint16_t SFX_wait(uint16_t bc, uint16_t caller_hl);
/* <<< factory SFX_wait */
/* >>> factory SFX_ApplyPitchOffset */
void SFX_ApplyPitchOffset(uint8_t c);
/* <<< factory SFX_ApplyPitchOffset */
/* >>> factory Func_fc1cd */
void Func_fc1cd(void);
/* <<< factory Func_fc1cd */
#endif
