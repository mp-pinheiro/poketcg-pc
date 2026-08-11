#include "home/gift_center.h"

#include "generated/wram.h"
#include "mem.h"

#define CONSOLE_CGB 0x02u
#define NORTH 0x00u
#define EVENT_GIFT_CENTER_MENU_CHOICE_OFFSET 0x1Au
#define EVENT_GIFT_CENTER_MENU_CHOICE_MASK 0xFCu

GiftCenterPreloadResult Preload_GiftCenterClerk(uint8_t f)
{
	uint8_t console = gb_read8(wConsole_ADDR);
	uint8_t a = console;
	if (console != CONSOLE_CGB) {
		a = NORTH;
		gb_write8(wLoadNPCDirection_ADDR, NORTH);
	}
	(void)f;
	return (GiftCenterPreloadResult){a, (uint8_t)(console == CONSOLE_CGB ? 0x90u : 0x10u)};
}

void Func_fcad(void)
{
	uint16_t event = (uint16_t)(wEventVars_ADDR + EVENT_GIFT_CENTER_MENU_CHOICE_OFFSET);
	uint8_t value = gb_read8(wGiftCenterChoice_ADDR);
	uint8_t current;
	uint8_t encoded = (uint8_t)((value << 2) & EVENT_GIFT_CENTER_MENU_CHOICE_MASK);
	gb_write8(wLoadedEventBits_ADDR, EVENT_GIFT_CENTER_MENU_CHOICE_MASK);
	current = gb_read8(event);
	gb_write8(event, (uint8_t)((current & (uint8_t)~EVENT_GIFT_CENTER_MENU_CHOICE_MASK) | encoded));
}
