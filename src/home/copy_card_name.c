#include "home/copy_card_name.h"

#include "generated/wram.h"
#include "mem.h"

#define TX_END 0x00u
#define TYPE_ENERGY 0x08u

CopyCardNameResult _CopyCardNameAndLevel_HalfwidthText(void)
{
	uint8_t b = (uint8_t)(wCardNameLength * 2u + 2u);
	uint16_t hl = wDefaultText_ADDR;

	for (;;) {
		b--;
		uint8_t a = gb_read8(hl++);
		if (a == TX_END)
			break;
	}
	--hl;

	if (wLoadedCard1Type < TYPE_ENERGY && wLoadedCard1Level != 0) {
		uint8_t c = wLoadedCard1Level;
		gb_write8(hl++, ' ');
		b--;
		gb_write8(hl++, 'L');
		b--;
		gb_write8(hl++, 'v');
		b--;
		if (c >= 10) {
			uint8_t first = (uint8_t)('0' - 1);
			while (c >= 10) {
				first++;
				c = (uint8_t)(c - 10);
			}
			gb_write8(hl++, first);
			b--;
		}
		gb_write8(hl++, (uint8_t)(c + '0'));
		b--;
	}

	uint16_t result_hl = hl;
	do {
		gb_write8(hl++, ' ');
		b--;
	} while (b != 0);
	gb_write8(hl, TX_END);

	return (CopyCardNameResult){' ', result_hl};
}
