#ifndef POKETCG_HOME_INPUT_H
#define POKETCG_HOME_INPUT_H

#include <stdint.h>

void ReadJoypad(void);
void SaveButtonsHeld(uint8_t c);
void ClearJoypad(uint16_t *hl);

#endif
