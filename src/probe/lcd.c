#include "home/lcd.h"
#include "probe.h"

static void adapt_EnableLCD(ProbeState *s)
{
	EnableLCD();
	(void)s;
}

static void adapt_DisableLCD(ProbeState *s)
{
	DisableLCD();
	(void)s;
}

static void adapt_Set_OBJ_8x8(ProbeState *s)
{
	Set_OBJ_8x8();
	(void)s;
}

static void adapt_Set_OBJ_8x16(ProbeState *s)
{
	Set_OBJ_8x16();
	(void)s;
}

static void adapt_SetWindowOn(ProbeState *s)
{
	SetWindowOn();
	(void)s;
}

static void adapt_SetWindowOff(ProbeState *s)
{
	SetWindowOff();
	(void)s;
}

const ProbeEntry probe_entries_lcd[] = {
	{ "EnableLCD", adapt_EnableLCD },
	{ "DisableLCD", adapt_DisableLCD },
	{ "Set_OBJ_8x8", adapt_Set_OBJ_8x8 },
	{ "Set_OBJ_8x16", adapt_Set_OBJ_8x16 },
	{ "SetWindowOn", adapt_SetWindowOn },
	{ "SetWindowOff", adapt_SetWindowOff },
	{ NULL, NULL },
};
