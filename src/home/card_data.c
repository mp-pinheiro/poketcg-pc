/* >>> part includes */
#include "home/card_data.h"

#include "generated/constants.h"
#include "generated/hram.h"
#include "generated/wram.h"
#include "generated/rom.h"
#include "home/card_id_bus.h"
#include "home/copy.h"
#include "home/frames.h"
#include "home/switch_rom.h"
#include "mem.h"
/* <<< part includes */
/* >>> factory statics */
#include "home/switch_rom.h"
#include "mem.h"

#include "home/switch_rom.h"
#include "home/copy.h"
#include "generated/hram.h"
/* <<< factory statics */

/* >>> part BANK_CARD_DATA */
/* Card data and CardPointers both live in ROM bank 0x0c (data/cards.asm). The asm
 * reaches them through BankpushROM2/BankpopROM, whose net effect is a temporary bank
 * switch -- collapsed here to direct rom_ptr reads. */
#define BANK_CARD_DATA      CardPointers_BANK
#define CARD_POINTERS       CardPointers_ADDR
#define GETCARDPTR_BOUND ((uint16_t)(CARD_POINTERS + 2u + 2u * NUM_CARDS))
/* <<< part BANK_CARD_DATA */

/* >>> part get_card_pointer */
static CardPtrResult get_card_pointer(CardId cardid)
{
	uint16_t entry = (uint16_t)(CARD_POINTERS + (uint16_t)cardid * 2u);
	if (entry >= GETCARDPTR_BOUND)
		return (CardPtrResult){entry, 1u, (uint8_t)(entry == GETCARDPTR_BOUND), 0u};
	const uint8_t *p = rom_ptr(BANK_CARD_DATA, entry);
	return (CardPtrResult){(uint16_t)(p[0] | (uint16_t)p[1] << 8), 0u, 0u, BANK_CARD_DATA};
}
/* <<< part get_card_pointer */

/* >>> part card_data */
static const uint8_t *card_data(CardId cardid)
{
	CardPtrResult pointer = get_card_pointer(cardid);
	return rom_ptr(pointer.bank, pointer.hl);
}
/* <<< part card_data */

/* >>> factory GetCardType */
/* card_data.asm:84-96 */
uint8_t GetCardType(CardId e)
{
	return card_data(e)[CARD_DATA_TYPE];
}
/* <<< factory GetCardType */

/* >>> factory GetCardName */
/* card_data.asm:99-114 */
uint16_t GetCardName(CardId e)
{
	const uint8_t *p = card_data(e) + CARD_DATA_NAME;
	return (uint16_t)(p[0] | (uint16_t)p[1] << 8);
}
/* <<< factory GetCardName */

/* >>> factory GetCardTypeRarityAndSet */
/* card_data.asm:117-138 */
CardTRS GetCardTypeRarityAndSet(CardId a)
{
	const uint8_t *p = card_data(a);
	return (CardTRS){p[CARD_DATA_TYPE], p[CARD_DATA_RARITY], p[CARD_DATA_SET]};
}
/* <<< factory GetCardTypeRarityAndSet */

/* >>> part load_card_data */
static void load_card_data(CardId cardid, uint16_t dest)
{
	LoadCardDataToHL_FromCardID(cardid, &dest, dest);
}
/* <<< part load_card_data */

/* >>> factory LoadCardDataToBuffer1_FromName */
/* card_data.asm:1-45. Scans CardPointers[1..] (skipping the leading NULL) for the
 * first card whose CARD_DATA_NAME matches de; on a hit copies it to wLoadedCard1.
 * CardPointers[229] is the NULL terminator. */
void LoadCardDataToBuffer1_FromName(uint16_t de)
{
	for (CardId i = 1u;; i++) {
		CardPtrResult pointer = get_card_pointer(i);
		if (pointer.carry)
			return;
		const uint8_t *cd = rom_ptr(pointer.bank, pointer.hl);
		uint16_t name = (uint16_t)(cd[CARD_DATA_NAME] | (uint16_t)cd[CARD_DATA_NAME + 1u] << 8);
		if (name == de) {
			load_card_data(i, wLoadedCard1_ADDR);
			return;
		}
	}
}
/* <<< factory LoadCardDataToBuffer1_FromName */

/* >>> factory LoadCardDataToBuffer1_FromCardID */
void LoadCardDataToBuffer1_FromCardID(CardId e)
{
	load_card_data(e, wLoadedCard1_ADDR);
}
/* <<< factory LoadCardDataToBuffer1_FromCardID */

/* >>> factory LoadCardDataToBuffer2_FromCardID */
void LoadCardDataToBuffer2_FromCardID(CardId e)
{
	load_card_data(e, wLoadedCard2_ADDR);
}
/* <<< factory LoadCardDataToBuffer2_FromCardID */

/* >>> part BANK_CARD_GFX */
#define BANK_CARD_GFX  CardGraphics_BANK
/* <<< part BANK_CARD_GFX */

/* >>> factory LoadCardGfx */
/* card_data.asm:176-205. The gfx index encodes its bank offset in bits 15-11
 * (bank = BANK(CardGraphics) + idx>>11) and the tile address in the rest (*8,
 * normalized into $4000-$7fff). */
void LoadCardGfx(uint16_t hl, uint16_t de, uint8_t b, uint8_t c)
{
	uint8_t saved = hBankROM;
	BankswitchROM((uint8_t)(BANK_CARD_GFX + (hl >> 11)));
	uint16_t src = (uint16_t)(hl << 3);
	src = (uint16_t)(((src & 0x7F00u) | 0x4000u) | (src & 0x00FFu));
	src = card_gfx_prepare(src);
	CopyGfxData(&src, &de, b, c);
	card_gfx_finish(src);
	BankswitchROM(saved);
}
/* <<< factory LoadCardGfx */



/* >>> factory GetCardPointer */
/* card_data.asm:140-168. e indexes CardPointers (2 bytes/entry, skipping neither
 * the leading NULL nor the trailing terminator here -- e > NUM_CARDS is out of
 * bounds). bound_zero mirrors the asm's own `cp`-pair Z bit at the boundary
 * check, needed by the probe adapter to reproduce the exact exit flags. */
CardPtrResult GetCardPointer(CardId e)
{
	return get_card_pointer(e);
}
/* <<< factory GetCardPointer */

/* >>> factory LoadCardDataToHL_FromCardID */
void LoadCardDataToHL_FromCardID(CardId e, uint16_t *hl, uint16_t saved_hl)
{
	uint16_t de = *hl;
	CardPtrResult card = GetCardPointer(e);
	if (card.carry) {
		*hl = saved_hl;
		return;
	}
	uint16_t bank_stack = (uint16_t)((uint16_t)hBankROM << 8);
	BankpushROM2Result pushed = BankpushROM2(card.bank, 0u, 0u, 0u, 0u, e, card.hl);
	uint16_t src = pushed.hl;
	uint8_t copy_length = PKMN_CARD_DATA_LENGTH;
	uint8_t spill[PKMN_CARD_DATA_LENGTH];
	size_t spilled = (size_t)(src + PKMN_CARD_DATA_LENGTH > 0x8000u ? src + PKMN_CARD_DATA_LENGTH - 0x8000u : 0u);
	int recorded = spilled != 0u && frame_boundary_overread(spill, spilled);
	for (uint8_t i = 0u; i < copy_length; i++) {
		uint8_t a = recorded && src >= 0x8000u ? spill[src - 0x8000u] : gb_read8(src);
		gb_write8(de, a);
		src = (uint16_t)(src + 1u);
		de = (uint16_t)(de + 1u);
	}
	(void)BankpopROM(0u, 0u, 0u, 0u, src, bank_stack, 0u);
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
