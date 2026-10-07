#ifndef POKETCG_HOME_LCD_H
#define POKETCG_HOME_LCD_H

/* >>> part includes */
#include <stdint.h>
/* <<< part includes */

/* >>> factory EnableLCD */
uint8_t EnableLCD(void);
/* <<< factory EnableLCD */
/* >>> factory DisableLCD */
void DisableLCD(void);
/* <<< factory DisableLCD */
/* >>> factory Set_OBJ_8x8 */
void Set_OBJ_8x8(void);
/* <<< factory Set_OBJ_8x8 */
/* >>> factory Set_OBJ_8x16 */
void Set_OBJ_8x16(void);
/* <<< factory Set_OBJ_8x16 */
/* >>> factory SetWindowOn */
void SetWindowOn(void);
/* <<< factory SetWindowOn */
/* >>> factory SetWindowOff */
void SetWindowOff(void);
/* <<< factory SetWindowOff */

#endif
