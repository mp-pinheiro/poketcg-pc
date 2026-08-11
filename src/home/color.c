#include "home/color.h"
#include "generated/hram.h"
#include "generated/sram.h"
#include "generated/wram.h"
#include "home/lcd.h"
#include "home/lcd_enable_frame.h"
#include "home/memory.h"
#include "home/palettes.h"
#include "home/switch_sram.h"
#include "mem.h"

static void fill_words(uint16_t address, uint16_t count, uint8_t lo, uint8_t hi)
{
    for (uint16_t i = 0; i < count; i++) {
        gb_write8((uint16_t)(address + i * 2), lo);
        gb_write8((uint16_t)(address + i * 2 + 1), hi);
    }
}

static uint8_t fade_component(uint8_t value, uint8_t target)
{
    if (value < target) {
        uint8_t distance = (uint8_t)(target - value);
        return (uint8_t)(value + (distance > 4 ? 4 : distance));
    }
    if (value > target) {
        uint8_t distance = (uint8_t)(value - target);
        return (uint8_t)(value - (distance > 4 ? 4 : distance));
    }
    return value;
}

static void fade_palette_bytes(uint16_t current, uint16_t target, uint8_t raw_count)
{
    uint16_t count = raw_count ? raw_count : 256;
    for (uint16_t i = 0; i < count; i++) {
        uint8_t current_lo = gb_read8((uint16_t)(current + i * 2));
        uint8_t current_hi = gb_read8((uint16_t)(current + i * 2 + 1));
        uint8_t target_lo = gb_read8((uint16_t)(target + i * 2));
        uint8_t target_hi = gb_read8((uint16_t)(target + i * 2 + 1));
        FadeColorResult result = FadePalIntoAnother_GetFadedColor(current_hi, current_lo, target_hi, target_lo);
        gb_write8((uint16_t)(current + i * 2), result.c);
        gb_write8((uint16_t)(current + i * 2 + 1), result.a);
    }
}

static void white_cgb(uint16_t address, uint16_t bytes)
{
    fill_words(address, (uint16_t)(bytes / 2), 0xff, 0x7f);
}

void LoadConsolePaletteData(void)
{
    (void)gb_read8(wConsole_ADDR);
    gb_write8(wConsolePaletteData_ADDR, 0);
    gb_write8(wd317_ADDR, 0);
}

void SetWhitePalettes(void)
{
    uint8_t value = gb_read8(wConsolePaletteData_ADDR);
    gb_write8(wBGP_ADDR, value);
    gb_write8(wOBP0_ADDR, value);
    gb_write8(wOBP1_ADDR, value);
    white_cgb(wBackgroundPalettesCGB_ADDR, 128);
}

void FadeScreenFromWhite_BackupPalsAndSetWhite(void)
{
    gb_write8(wTempBGP_ADDR, gb_read8(wBGP_ADDR));
    gb_write8(wTempOBP0_ADDR, gb_read8(wOBP0_ADDR));
    gb_write8(wTempOBP1_ADDR, gb_read8(wOBP1_ADDR));
    for (uint16_t i = 0; i < 128; i++)
        gb_write8((uint16_t)(wTempBackgroundPalettesCGB_ADDR + i), gb_read8((uint16_t)(wBackgroundPalettesCGB_ADDR + i)));
    SetWhitePalettes();
}

void RestoreFirstColorInOBPals(void)
{
    for (uint8_t palette = 0; palette < 8; palette++) {
        uint16_t source = (uint16_t)(wTempObjectPalettesCGB_ADDR + palette * 8);
        uint16_t destination = (uint16_t)(wObjectPalettesCGB_ADDR + palette * 8);
        gb_write8(destination, gb_read8(source));
        gb_write8((uint16_t)(destination + 1), gb_read8((uint16_t)(source + 1)));
    }
}

uint8_t FadePalIntoAnother_FadeColor(uint8_t a, uint16_t hl)
{
    return fade_component(a, (uint8_t)hl);
}

FadeColorResult FadePalIntoAnother_GetFadedColor(uint8_t b, uint8_t c, uint8_t d, uint8_t e)
{
    uint8_t red = fade_component((uint8_t)(c & 0x1f), (uint8_t)(e & 0x1f));
    uint8_t green = fade_component((uint8_t)(((c >> 5) & 7) | ((b & 3) << 3)), (uint8_t)(((e >> 5) & 7) | ((d & 3) << 3)));
    uint8_t blue = fade_component((uint8_t)((b >> 2) & 0x1f), (uint8_t)((d >> 2) & 0x1f));
    FadeColorResult result;
    result.a = (uint8_t)(((green >> 3) & 3) | (blue << 2));
    result.c = (uint8_t)(red | ((green & 7) << 5));
    return result;
}

void FadeOBPalIntoTemp(void)
{
    fade_palette_bytes(wObjectPalettesCGB_ADDR, wTempObjectPalettesCGB_ADDR, 32);
}

void FadeBGPalIntoTemp1(void)
{
    fade_palette_bytes(wBackgroundPalettesCGB_ADDR, wTempBackgroundPalettesCGB_ADDR, 16);
}

void FadeBGPalIntoTemp2(void)
{
    fade_palette_bytes((uint16_t)(wBackgroundPalettesCGB_ADDR + 32), (uint16_t)(wTempBackgroundPalettesCGB_ADDR + 32), 16);
}

void FadeBGPalIntoTemp3(void)
{
    fade_palette_bytes(wBackgroundPalettesCGB_ADDR, wTempBackgroundPalettesCGB_ADDR, 32);
}

static const uint8_t mix_shades[16] = { 0, 1, 1, 1, 0, 1, 2, 2, 1, 1, 2, 3, 2, 2, 2, 3 };

uint8_t FadeDMGPalettes_GetMixShadeValue(uint8_t b, uint8_t c)
{
    return mix_shades[((b & 3) << 2) | (c & 3)];
}

uint8_t FadeDMGPalettes_CalculateMixPalette(uint8_t b, uint8_t c)
{
    uint8_t output = 0;
    for (uint8_t i = 0; i < 4; i++) {
        uint8_t shade = FadeDMGPalettes_GetMixShadeValue(b, c);
        uint8_t combined = (uint8_t)(shade | output);
        output = (uint8_t)((combined << 2) | (combined >> 6));
        b = (uint8_t)((b << 2) | (b >> 6));
        c = (uint8_t)((c << 2) | (c >> 6));
    }
    return output;
}

void FadeDMGPalettes(void)
{
    uint16_t current = wBGP_ADDR;
    uint16_t target = wTempBGP_ADDR;
    for (uint8_t i = 0; i < 3; i++) {
        gb_write8(current, FadeDMGPalettes_CalculateMixPalette(gb_read8(current), gb_read8(target)));
        current++;
        target++;
    }
}

uint8_t FadeScreenToTempPals(void)
{
    uint8_t start = gb_read8(wVBlankCounter_ADDR);
    for (uint8_t count = 0x10; count != 0; count = (uint8_t)(count - 2)) {
        if ((count & 3) == 0)
            FadeDMGPalettes();
        FadeBGPalIntoTemp3();
        FadeOBPalIntoTemp();
        FlushAllPalettes();
        DoFrameIfLCDEnabled();
    }
    return (uint8_t)(gb_read8(wVBlankCounter_ADDR) - start);
}

void FadeScreenToWhite(void)
{
    uint8_t value = gb_read8(wConsolePaletteData_ADDR);
    if (gb_read8(wLCDC_ADDR) & 0x80) {
        gb_write8(wTempBGP_ADDR, value);
        gb_write8(wTempOBP0_ADDR, value);
        gb_write8(wTempOBP1_ADDR, value);
        white_cgb(wTempBackgroundPalettesCGB_ADDR, 128);
        RestoreFirstColorInOBPals();
        FadeScreenToTempPals();
        DisableLCD();
        return;
    }
    gb_write8(wBGP_ADDR, value);
    gb_write8(wOBP0_ADDR, value);
    gb_write8(wOBP1_ADDR, value);
    white_cgb(wBackgroundPalettesCGB_ADDR, 128);
    FlushAllPalettes();
}

uint8_t FadeScreenFromWhite(void)
{
    FadeScreenFromWhite_BackupPalsAndSetWhite();
    RestoreFirstColorInOBPals();
    FlushAllPalettes();
    EnableLCD();
    return FadeScreenToTempPals();
}

void CopyPalsToSRAMBuffer(void)
{
    uint8_t prior = hBankSRAM;
    BankswitchSRAM(1);
    EnableSRAM();
    uint16_t address = sGfxBuffer2_ADDR;
    gb_write8(address++, gb_read8(wBGP_ADDR));
    gb_write8(address++, gb_read8(wOBP0_ADDR));
    gb_write8(address++, gb_read8(wOBP1_ADDR));
    for (uint16_t i = 0; i < 128; i++)
        gb_write8((uint16_t)(address + i), gb_read8((uint16_t)(wBackgroundPalettesCGB_ADDR + i)));
    BankswitchSRAM(prior);
    DisableSRAM();
}

void LoadPalsFromSRAMBuffer(void)
{
    uint8_t prior = hBankSRAM;
    BankswitchSRAM(1);
    EnableSRAM();
    uint16_t address = sGfxBuffer2_ADDR;
    gb_write8(wBGP_ADDR, gb_read8(address++));
    gb_write8(wOBP0_ADDR, gb_read8(address++));
    gb_write8(wOBP1_ADDR, gb_read8(address++));
    for (uint16_t i = 0; i < 128; i++)
        gb_write8((uint16_t)(wBackgroundPalettesCGB_ADDR + i), gb_read8((uint16_t)(address + i)));
    BankswitchSRAM(prior);
    DisableSRAM();
}

void FlashScreenToWhite(uint8_t c)
{
    uint8_t prior = hBankSRAM;
    BankswitchSRAM(1);
    CopyPalsToSRAMBuffer();
    FadeScreenToWhite();
    if (c == 0) {
        LoadPalsFromSRAMBuffer();
        FadeScreenFromWhite();
    }
    EnableLCD();
    BankswitchSRAM(prior);
    DisableSRAM();
}

void Func_10d17(void)
{
    gb_write8(wTempBGP_ADDR, gb_read8(wBGP_ADDR));
    gb_write8(wTempOBP0_ADDR, gb_read8(wOBP0_ADDR));
    gb_write8(wTempOBP1_ADDR, gb_read8(wOBP1_ADDR));
    for (uint16_t i = 0; i < 128; i++)
        gb_write8((uint16_t)(wTempBackgroundPalettesCGB_ADDR + i), gb_read8((uint16_t)(wBackgroundPalettesCGB_ADDR + i)));
    gb_write8(wBGP_ADDR, gb_read8(wConsolePaletteData_ADDR));
    white_cgb(wBackgroundPalettesCGB_ADDR, 64);
    FlushAllPalettes();
    gb_write8(wd317_ADDR, 0x10);
}

void Func_10d50(void)
{
    uint8_t value = gb_read8(wConsolePaletteData_ADDR);
    gb_write8(wTempBGP_ADDR, value);
    gb_write8(wTempOBP0_ADDR, gb_read8(wOBP0_ADDR));
    gb_write8(wTempOBP1_ADDR, gb_read8(wOBP1_ADDR));
    white_cgb(wTempBackgroundPalettesCGB_ADDR, 64);
    gb_write8(wd317_ADDR, 0x10);
}

void Func_10d74(void)
{
    uint8_t value = gb_read8(wd317_ADDR);
    if (value == 0)
        return;
    uint8_t mode = value & 3;
    if (mode == 1)
        FadeDMGPalettes();
    if ((mode & 1) == 0)
        FadeBGPalIntoTemp1();
    else {
        FadeBGPalIntoTemp2();
        FlushAllPalettes();
    }
    gb_write8(wd317_ADDR, (uint8_t)(value - 1));
}
