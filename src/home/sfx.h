#ifndef POKETCG_HOME_SFX_H
#define POKETCG_HOME_SFX_H

#include <stdint.h>

void SFX_Play(uint8_t sfx_id);
void SFX_Update(void);

/* >>> factory Func_fc105 */
uint16_t Func_fc105(uint16_t bc, uint16_t de);
/* <<< factory Func_fc105 */
#endif
