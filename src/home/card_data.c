#include "home/card_data.h"

#include "generated/hram.h"
#include "generated/wram.h"
#include "home/copy.h"
#include "home/switch_rom.h"
#include "mem.h"
/* >>> factory statics */
#include "home/switch_rom.h"
#include "mem.h"
#define PKMN_CARD_DATA_LENGTH 0x41u

#include "home/switch_rom.h"
#include "home/copy.h"
#include "generated/hram.h"
/* <<< factory statics */

/* Card data and CardPointers both live in ROM bank 0x0c (data/cards.asm). The asm
 * reaches them through BankpushROM2/BankpopROM, whose net effect is a temporary bank
 * switch -- collapsed here to direct rom_ptr reads. */
#define BANK_CARD_DATA      0x0cu
#define CARD_POINTERS       0x4c5cu
#define CARD_DATA_TYPE      0x00u
#define CARD_DATA_NAME      0x03u
#define CARD_DATA_RARITY    0x05u
#define CARD_DATA_SET       0x06u
#define PKMN_CARD_DATA_LEN  0x41u

static uint16_t get_card_pointer(uint8_t cardid)
{
	const uint8_t *p = rom_ptr(BANK_CARD_DATA, (uint16_t)(CARD_POINTERS + (uint16_t)cardid * 2u));
	return (uint16_t)(p[0] | (uint16_t)p[1] << 8);
}

static const uint8_t *card_data(uint8_t cardid)
{
	return rom_ptr(BANK_CARD_DATA, get_card_pointer(cardid));
}

/* card_data.asm:84-96 */
uint8_t GetCardType(uint8_t e)
{
	return card_data(e)[CARD_DATA_TYPE];
}

/* card_data.asm:99-114 */
uint16_t GetCardName(uint8_t e)
{
	const uint8_t *p = card_data(e) + CARD_DATA_NAME;
	return (uint16_t)(p[0] | (uint16_t)p[1] << 8);
}

/* card_data.asm:117-138 */
CardTRS GetCardTypeRarityAndSet(uint8_t a)
{
	const uint8_t *p = card_data(a);
	return (CardTRS){p[CARD_DATA_TYPE], p[CARD_DATA_RARITY], p[CARD_DATA_SET]};
}

/* card_data.asm:48-81. Both buffer wrappers fall through to LoadCardDataToHL, which is
 * not directly callable (it pops one more word than it pushes; the wrappers' leading
 * push hl balances it). Inlined as a single copy. Read via the switched bank, not
 * rom_ptr: the last card's 0x41-byte copy runs hl past $7fff into VRAM ($8000+). */
static void load_card_data(uint8_t cardid, uint16_t dest)
{
	uint8_t saved = hBankROM;
	BankswitchROM(BANK_CARD_DATA);
	uint16_t ptr = get_card_pointer(cardid);
	for (uint8_t i = 0; i < PKMN_CARD_DATA_LEN; i++)
		gb_write8((uint16_t)(dest + i), gb_read8((uint16_t)(ptr + i)));
	BankswitchROM(saved);
}

/* card_data.asm:1-45. Scans CardPointers[1..] (skipping the leading NULL) for the
 * first card whose CARD_DATA_NAME matches de; on a hit copies it to wLoadedCard1.
 * CardPointers[229] is the NULL terminator. */
void LoadCardDataToBuffer1_FromName(uint16_t de)
{
	for (uint8_t i = 1u;; i++) {
		const uint8_t *tp = rom_ptr(BANK_CARD_DATA, (uint16_t)(CARD_POINTERS + (uint16_t)i * 2u));
		uint16_t ptr = (uint16_t)(tp[0] | (uint16_t)tp[1] << 8);
		if (ptr == 0)
			return;
		const uint8_t *cd = rom_ptr(BANK_CARD_DATA, ptr);
		uint16_t name = (uint16_t)(cd[CARD_DATA_NAME] | (uint16_t)cd[CARD_DATA_NAME + 1u] << 8);
		if (name == de) {
			load_card_data(i, wLoadedCard1_ADDR);
			return;
		}
	}
}

void LoadCardDataToBuffer1_FromCardID(uint8_t e)
{
	load_card_data(e, wLoadedCard1_ADDR);
}

void LoadCardDataToBuffer2_FromCardID(uint8_t e)
{
	load_card_data(e, wLoadedCard2_ADDR);
}

#define BANK_CARD_GFX 0x31u
#define PAL_SIZE      0x08u

/* card_data.asm:176-205. The gfx index encodes its bank offset in bits 15-11
 * (bank = BANK(CardGraphics) + idx>>11) and the tile address in the rest (*8,
 * normalized into $4000-$7fff). */
void LoadCardGfx(uint16_t hl, uint16_t de, uint8_t b, uint8_t c)
{
	uint8_t saved = hBankROM;
	BankswitchROM((uint8_t)(BANK_CARD_GFX + (hl >> 11)));
	uint16_t src = (uint16_t)(hl << 3);
	src = (uint16_t)(((src & 0x7F00u) | 0x4000u) | (src & 0x00FFu));
	CopyGfxData(&src, &de, b, c);
	uint16_t pal = wCardPalette_ADDR;
	for (uint8_t i = 0; i < PAL_SIZE; i++)
		gb_write8(pal++, gb_read8(src++));
	BankswitchROM(saved);
}

#define NUM_CARDS 228u
#define GETCARDPTR_BOUND ((uint16_t)(CARD_POINTERS + 2u + 2u * NUM_CARDS))

/* card_data.asm:140-168. e indexes CardPointers (2 bytes/entry, skipping neither
 * the leading NULL nor the trailing terminator here -- e > NUM_CARDS is out of
 * bounds). bound_zero mirrors the asm's own `cp`-pair Z bit at the boundary
 * check, needed by the probe adapter to reproduce the exact exit flags. */
CardPtrResult GetCardPointer(uint8_t e)
{
	uint16_t hl = (uint16_t)(CARD_POINTERS + (uint16_t)e * 2u);
	if (hl >= GETCARDPTR_BOUND)
		return (CardPtrResult){hl, 1, (uint8_t)(hl == GETCARDPTR_BOUND)};
	const uint8_t *p = rom_ptr(BANK_CARD_DATA, hl);
	return (CardPtrResult){(uint16_t)(p[0] | (uint16_t)p[1] << 8), 0, 0};
}

/* >>> factory LoadCardDataToHL_FromCardID */
void LoadCardDataToHL_FromCardID(uint8_t e, uint16_t *hl, uint16_t saved_hl)
{
	uint16_t de = *hl;
	CardPtrResult card = GetCardPointer(e);
	if (card.carry) {
		*hl = saved_hl;
		return;
	}
	BankpushROM2Result pushed = BankpushROM2(BANK_CARD_DATA, 0u, 0u, 0u, 0u, e, card.hl);
	uint16_t src = pushed.hl;
	uint8_t copy_length = PKMN_CARD_DATA_LENGTH;
	for (uint8_t i = 0u; i < copy_length; i++) {
		uint8_t a = gb_read8(src);
		gb_write8(de, a);
		src = (uint16_t)(src + 1u);
		de = (uint16_t)(de + 1u);
	}
	(void)BankpopROM(0u, 0u, 0u, 0u, src, 0u, 0u);
	*hl = saved_hl;
}
/* <<< factory LoadCardDataToHL_FromCardID */

/* >>> factory CopyFontsOrDuelGraphicsTiles2 */
void CopyFontsOrDuelGraphicsTiles2(uint8_t a, uint8_t f, uint8_t b, uint8_t c, uint8_t d, uint8_t e, uint16_t hl)
{
	uint16_t bank_stack = (uint16_t)((uint16_t)hBankROM << 8);
	uint16_t saved_af = (uint16_t)(((uint16_t)a << 8) | f);
	BankpushROMResult pushed = BankpushROM(0x1du, f, b, c, d, e, hl);
	uint16_t src = pushed.hl;
	uint16_t dst = (uint16_t)(((uint16_t)d << 8) | e);
	uint8_t copy_length = 0x10u;
	CopyGfxData(&src, &dst, b, copy_length);
	(void)BankpopROM(0u, 0u, 0u, 0u, src, bank_stack, saved_af);
}
/* <<< factory CopyFontsOrDuelGraphicsTiles2 */
