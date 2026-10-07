/* >>> part includes */
#include "home/lcd.h"
#include "probe.h"
/* <<< part includes */

/* >>> factory EnableLCD */
static void adapt_EnableLCD(ProbeState *s)
{
	EnableLCD();
	(void)s;
}
/* <<< factory EnableLCD */

/* >>> factory DisableLCD */
static void adapt_DisableLCD(ProbeState *s)
{
	DisableLCD();
	(void)s;
}
/* <<< factory DisableLCD */

/* >>> factory Set_OBJ_8x8 */
static void adapt_Set_OBJ_8x8(ProbeState *s)
{
	Set_OBJ_8x8();
	(void)s;
}
/* <<< factory Set_OBJ_8x8 */

/* >>> factory Set_OBJ_8x16 */
static void adapt_Set_OBJ_8x16(ProbeState *s)
{
	Set_OBJ_8x16();
	(void)s;
}
/* <<< factory Set_OBJ_8x16 */

/* >>> factory SetWindowOn */
static void adapt_SetWindowOn(ProbeState *s)
{
	SetWindowOn();
	(void)s;
}
/* <<< factory SetWindowOn */

/* >>> factory SetWindowOff */
static void adapt_SetWindowOff(ProbeState *s)
{
	SetWindowOff();
	(void)s;
}
/* <<< factory SetWindowOff */

/* >>> part probe_entries_lcd */
const ProbeEntry probe_entries_lcd[] = {
	{ "EnableLCD", adapt_EnableLCD },
	{ "DisableLCD", adapt_DisableLCD },
	{ "Set_OBJ_8x8", adapt_Set_OBJ_8x8 },
	{ "Set_OBJ_8x16", adapt_Set_OBJ_8x16 },
	{ "SetWindowOn", adapt_SetWindowOn },
	{ "SetWindowOff", adapt_SetWindowOff },
	{ NULL, NULL },
};
/* <<< part probe_entries_lcd */
