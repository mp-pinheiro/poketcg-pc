#ifndef POKETCG_HOME_LCD_H
#define POKETCG_HOME_LCD_H

#include <stdint.h>

uint8_t EnableLCD(void);
void DisableLCD(void);
void Set_OBJ_8x8(void);
void Set_OBJ_8x16(void);
void SetWindowOn(void);
void SetWindowOff(void);

#endif
