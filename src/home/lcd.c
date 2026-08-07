#include "home/lcd.h"

#include "generated/wram.h"
#include "mem.h"

#define rLCDC 0xFF40u
#define rIE 0xFFFFu
#define rBGP 0xFF47u
#define rOBP0 0xFF48u
#define rOBP1 0xFF49u
#define LCDC_ON 0x80u
#define LCDC_WIN_ON 0x20u
#define LCDC_OBJ_16 0x04u
#define FLUSH_ALL_PALS 0xC0u
#define IE_VBLANK 0x01u

void EnableLCD(void)
{
	uint8_t value = gb_read8(wLCDC_ADDR);

	if (value & LCDC_ON)
		return;
	value |= LCDC_ON;
	gb_write8(wLCDC_ADDR, value);
	gb_write8(rLCDC, value);
	gb_write8(wFlushPaletteFlags_ADDR, FLUSH_ALL_PALS);
}

void DisableLCD(void)
{
	uint8_t value = gb_read8(rLCDC);
	uint8_t interrupt_enable;

	if (!(value & LCDC_ON))
		return;
	interrupt_enable = gb_read8(rIE);
	gb_write8(wIE_ADDR, interrupt_enable);
	gb_write8(rIE, (uint8_t)(interrupt_enable & (uint8_t)~IE_VBLANK));
	value &= (uint8_t)~LCDC_ON;
	gb_write8(rLCDC, value);
	gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_ON));
	gb_write8(rBGP, 0);
	gb_write8(rOBP0, 0);
	gb_write8(rOBP1, 0);
	gb_write8(rIE, interrupt_enable);
}

void Set_OBJ_8x8(void)
{
	gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_OBJ_16));
}

void Set_OBJ_8x16(void)
{
	gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | LCDC_OBJ_16));
}

void SetWindowOn(void)
{
	gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) | LCDC_WIN_ON));
}

void SetWindowOff(void)
{
	gb_write8(wLCDC_ADDR, (uint8_t)(gb_read8(wLCDC_ADDR) & (uint8_t)~LCDC_WIN_ON));
}
